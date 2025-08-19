"""Command for managing environment configurations in FastAPI projects."""

from pathlib import Path
from typing import Any

import typer
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from fascraft.exceptions import FasCraftError, FileSystemError, TemplateRenderError
from fascraft.validation import validate_path_robust

# Initialize rich console
console = Console(width=None, soft_wrap=False)

app = typer.Typer(help="🌍 Manage environment configurations for FastAPI projects")


@app.command()
def init(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    environments: str = typer.Option(
        "dev,staging,prod",
        "--environments",
        "-e",
        help="Comma-separated list of environments to create",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="🔄 Overwrite existing environment files"
    ),
) -> None:
    """🌍 Initialize environment management for a FastAPI project."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Check if it's a FastAPI project
        main_py = project_path / "main.py"
        if not main_py.exists():
            raise FileSystemError(
                f"Not a FastAPI project: main.py not found at {project_path}"
            )

        # Parse environments
        env_list = [env.strip() for env in environments.split(",") if env.strip()]
        if not env_list:
            raise FileSystemError("No valid environments specified")

        # Check for existing environment files
        existing_files = check_existing_environment_files(project_path, env_list)

        if existing_files and not force:
            console.print(
                f"⚠️  Environment files already exist: {', '.join(existing_files)}",
                style="bold yellow",
            )
            console.print("Use --force to overwrite existing files", style="yellow")
            raise typer.Exit(code=1)

        # Initialize environment management
        initialize_environment_management(project_path, env_list, force)

        # Display success message
        display_success_message(project_path, env_list)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


@app.command()
def create(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    name: str = typer.Option(
        ..., "--name", "-n", help="Name of the environment to create"
    ),
    template: str = typer.Option(
        "development",
        "--template",
        "-t",
        help="Template to use: development, staging, production, custom",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="🔄 Overwrite existing environment"
    ),
) -> None:
    """🌍 Create a new environment configuration."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Check if it's a FastAPI project
        main_py = project_path / "main.py"
        if not main_py.exists():
            raise FileSystemError(
                f"Not a FastAPI project: main.py not found at {project_path}"
            )

        # Validate template choice
        valid_templates = ["development", "staging", "production", "custom"]
        if template not in valid_templates:
            raise FileSystemError(
                f"Invalid template: {template}. Choose from: {', '.join(valid_templates)}"
            )

        # Create environment
        create_environment(project_path, name, template, force)

        # Display success message
        display_environment_created(project_path, name, template)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


@app.command()
def list_envs(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
) -> None:
    """📋 List all available environments."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # List environments
        list_environments(project_path)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


@app.command()
def switch(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    environment: str = typer.Option(
        ..., "--environment", "-e", help="Environment to switch to"
    ),
) -> None:
    """🔄 Switch to a different environment."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Switch environment
        switch_environment(project_path, environment)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


@app.command()
def validate(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    environment: str | None = typer.Option(
        None,
        "--environment",
        "-e",
        help="Specific environment to validate (default: all)",
    ),
) -> None:
    """✅ Validate environment configurations."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Validate environments
        validate_environments(project_path, environment)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def check_existing_environment_files(project_path: Path, environments: list) -> list:
    """Check for existing environment files."""
    existing_files = []

    for env in environments:
        env_file = project_path / f".env.{env}"
        if env_file.exists():
            existing_files.append(f".env.{env}")

    # Check for environment config directory
    env_config_dir = project_path / "config" / "environments"
    if env_config_dir.exists():
        for env_file in env_config_dir.glob("*.yml"):
            existing_files.append(f"config/environments/{env_file.name}")

    return existing_files


def initialize_environment_management(
    project_path: Path, environments: list, force: bool
) -> None:
    """Initialize environment management for the project."""
    try:
        # Get project name from directory
        project_name = project_path.name

        # Setup Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Initializing environment management...", total=len(environments) + 2
            )

            # Create environment configuration directory
            env_config_dir = project_path / "config" / "environments"
            env_config_dir.mkdir(parents=True, exist_ok=True)
            progress.advance(task)

            # Create environment-specific .env files
            for env_name in environments:
                create_environment_file(project_path, env_name, env, project_name)
                progress.advance(task)

            # Create environment configuration YAML
            create_environment_config_yaml(project_path, environments, project_name)
            progress.advance(task)

            # Create enhanced settings.py with environment support
            create_enhanced_settings(project_path, project_name, env)

        console.print(
            "🌍 Environment management initialized successfully!", style="bold green"
        )

    except Exception as e:
        raise FileSystemError(
            f"Failed to initialize environment management: {str(e)}"
        ) from e


def create_environment_file(
    project_path: Path, env_name: str, jinja_env: Environment, project_name: str
) -> None:
    """Create an environment-specific .env file."""
    try:
        # Get template content
        template = jinja_env.get_template("env.sample.jinja2")

        # Environment-specific overrides
        env_overrides = get_environment_overrides(env_name)

        # Render template with environment-specific values
        content = template.render(project_name=project_name, **env_overrides)

        # Write environment file
        env_file = project_path / f".env.{env_name}"
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(f"📝 Created .env.{env_name}", style="green")

    except Exception as e:
        raise TemplateRenderError(f"env.{env_name}", str(e)) from e


def get_environment_overrides(env_name: str) -> dict[str, Any]:
    """Get environment-specific configuration overrides."""
    overrides = {
        "development": {
            "DEBUG": "True",
            "ENVIRONMENT": "development",
            "LOG_LEVEL": "DEBUG",
            "DATABASE_URL": "sqlite:///./app_dev.db",
            "REDIS_URI": "redis://localhost:6379/1",
            "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8080"]',
        },
        "staging": {
            "DEBUG": "False",
            "ENVIRONMENT": "staging",
            "LOG_LEVEL": "INFO",
            "DATABASE_URL": "postgresql://staging_user:staging_pass@staging_db:5432/staging_db",
            "REDIS_URI": "redis://staging_redis:6379/0",
            "CORS_ORIGINS": '["https://staging.example.com"]',
        },
        "production": {
            "DEBUG": "False",
            "ENVIRONMENT": "production",
            "LOG_LEVEL": "WARNING",
            "DATABASE_URL": "postgresql://prod_user:prod_pass@prod_db:5432/prod_db",
            "REDIS_URI": "redis://prod_redis:6379/0",
            "CORS_ORIGINS": '["https://example.com"]',
        },
        "testing": {
            "DEBUG": "False",
            "ENVIRONMENT": "testing",
            "LOG_LEVEL": "DEBUG",
            "DATABASE_URL": "sqlite:///./test.db",
            "REDIS_URI": "redis://localhost:6379/2",
            "CORS_ORIGINS": '["http://localhost:3000"]',
        },
    }

    return overrides.get(env_name, overrides["development"])


def create_environment_config_yaml(
    project_path: Path, environments: list, project_name: str
) -> None:
    """Create environment configuration YAML file."""
    try:
        env_config_dir = project_path / "config" / "environments"

        # Create main environment config
        main_config = {
            "project": project_name,
            "default_environment": "development",
            "environments": {},
        }

        for env in environments:
            main_config["environments"][env] = {
                "description": f"{env.title()} environment configuration",
                "config_file": f".env.{env}",
                "settings_file": f"config/environments/{env}.yml",
            }

        # Write main config
        main_config_file = env_config_dir / "environments.yml"
        with open(main_config_file, "w", encoding="utf-8") as f:
            yaml.dump(main_config, f, default_flow_style=False, indent=2)

        # Create individual environment configs
        for env in environments:
            create_individual_env_config(env_config_dir, env, project_name)

        console.print(
            "📝 Created environment configuration in config/environments/",
            style="green",
        )

    except Exception as e:
        raise FileSystemError(
            f"Failed to create environment config YAML: {str(e)}"
        ) from e


def create_individual_env_config(
    env_config_dir: Path, env_name: str, project_name: str
) -> None:
    """Create individual environment configuration file."""
    try:
        env_config = {
            "environment": env_name,
            "project": project_name,
            "app": {
                "name": project_name,
                "version": "0.1.0",
                "debug": env_name == "development",
                "host": "0.0.0.0",
                "port": 8000,
            },
            "database": {
                "url": (
                    f"sqlite:///./{project_name}_{env_name}.db"
                    if env_name == "development"
                    else f"postgresql://{env_name}_user:{env_name}_pass@{env_name}_db:5432/{env_name}_db"
                ),
                "pool_size": 5 if env_name == "development" else 20,
                "max_overflow": 10 if env_name == "development" else 30,
            },
            "redis": {
                "url": f"redis://localhost:6379/{['development', 'staging', 'production', 'testing'].index(env_name) if env_name in ['development', 'staging', 'production', 'testing'] else 0}",
                "pool_size": 5 if env_name == "development" else 10,
            },
            "logging": {
                "level": "DEBUG" if env_name == "development" else "INFO",
                "format": "detailed" if env_name == "development" else "json",
            },
            "security": {
                "secret_key": f"your-{env_name}-secret-key-here",
                "access_token_expire_minutes": 30 if env_name == "development" else 15,
            },
        }

        # Write environment config
        env_config_file = env_config_dir / f"{env_name}.yml"
        with open(env_config_file, "w", encoding="utf-8") as f:
            yaml.dump(env_config, f, default_flow_style=False, indent=2)

    except Exception as e:
        raise FileSystemError(f"Failed to create {env_name} config: {str(e)}") from e


def create_enhanced_settings(
    project_path: Path, project_name: str, jinja_env: Environment
) -> None:
    """Create enhanced settings.py with environment support."""
    try:
        # Create enhanced settings template
        enhanced_settings_content = f'''"""Enhanced application settings with environment support."""

import os
from functools import lru_cache
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        print("Configuration error: pydantic not available")
        print("Please install required dependencies: pip install -r requirements.txt")
        raise

import yaml


class EnvironmentSettings(BaseSettings):
    """Environment-specific settings."""

    environment: str = "development"
    config_dir: str = "config/environments"

    class Config:
        env_file = ".env"
        case_sensitive = True


class Settings(BaseSettings):
    """Application settings with environment support."""

    # Environment
    environment: str = "development"
    debug: bool = False

    # Application
    app_name: str = "{project_name}"
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "sqlite:///./{project_name}.db"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_size: int = 5

    # Security
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"
    log_format: str = "standard"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""


def load_environment_config(environment: str, config_dir: str = "config/environments") -> Dict[str, Any]:
    """Load environment-specific configuration."""
    try:
        config_path = Path(config_dir) / f"{{environment}}.yml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Failed to load environment config for {{environment}}: {{e}}")

    return {{}}


def merge_configs(base_config: Dict[str, Any], env_config: Dict[str, Any]) -> Dict[str, Any]:
    """Merge base configuration with environment-specific overrides."""
    merged = base_config.copy()

    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value

    deep_merge(merged, env_config)
    return merged


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance with environment support."""
    # Get environment from environment variables or .env file
    env_settings = EnvironmentSettings()
    environment = env_settings.environment

    # Load base settings
    base_settings = Settings()

            # Load environment-specific configuration
        env_config = load_environment_config(environment, env_settings.config_dir)

        # Merge configurations
        if env_config:
            # Update settings with environment-specific values
            for key, value in env_config.items():
                if hasattr(base_settings, key):
                    setattr(base_settings, key, value)
                elif isinstance(value, dict):
                    # Handle nested configuration
                    for nested_key, nested_value in value.items():
                        full_key = f"{{key}}_{{nested_key}}"
                        if hasattr(base_settings, full_key):
                            setattr(base_settings, full_key, nested_value)

    return base_settings


def get_environment() -> str:
    """Get current environment name."""
    return get_settings().environment


def is_development() -> bool:
    """Check if running in development environment."""
    return get_environment() == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return get_environment() == "production"


def is_staging() -> bool:
    """Check if running in staging environment."""
    return get_environment() == "staging"


def is_testing() -> bool:
    """Check if running in testing environment."""
    return get_environment() == "testing"
'''

        # Write enhanced settings
        settings_file = project_path / "config" / "settings.py"
        settings_file.parent.mkdir(parents=True, exist_ok=True)

        with open(settings_file, "w", encoding="utf-8") as f:
            f.write(enhanced_settings_content)

        console.print(
            "📝 Enhanced settings.py created with environment support", style="green"
        )

    except Exception as e:
        raise FileSystemError(f"Failed to create enhanced settings: {str(e)}") from e


def create_environment(
    project_path: Path, name: str, template: str, force: bool
) -> None:
    """Create a new environment configuration."""
    try:
        # Check if environment already exists
        env_file = project_path / f".env.{name}"
        env_config_file = project_path / "config" / "environments" / f"{name}.yml"

        if (env_file.exists() or env_config_file.exists()) and not force:
            raise FileSystemError(
                f"Environment '{name}' already exists. Use --force to overwrite."
            )

        # Get project name
        project_name = project_path.name

        # Setup Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Create environment file
        create_environment_file(project_path, name, env, project_name)

        # Create environment config
        env_config_dir = project_path / "config" / "environments"
        env_config_dir.mkdir(parents=True, exist_ok=True)
        create_individual_env_config(env_config_dir, name, project_name)

        # Update main environment config
        update_main_environment_config(project_path, name)

        console.print(
            f"🌍 Environment '{name}' created successfully!", style="bold green"
        )

    except Exception as e:
        raise FileSystemError(f"Failed to create environment '{name}': {str(e)}") from e


def update_main_environment_config(project_path: Path, new_env: str) -> None:
    """Update main environment configuration to include new environment."""
    try:
        main_config_file = project_path / "config" / "environments" / "environments.yml"

        if main_config_file.exists():
            with open(main_config_file, encoding="utf-8") as f:
                config = yaml.safe_load(f)
        else:
            config = {
                "project": project_path.name,
                "default_environment": "development",
                "environments": {},
            }

        # Add new environment
        config["environments"][new_env] = {
            "description": f"{new_env.title()} environment configuration",
            "config_file": f".env.{new_env}",
            "settings_file": f"config/environments/{new_env}.yml",
        }

        # Write updated config
        with open(main_config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)

    except Exception as e:
        console.print(
            f"⚠️ Warning: Failed to update main environment config: {e}", style="yellow"
        )


def list_environments(project_path: Path) -> None:
    """List all available environments."""
    try:
        # Check for environment files
        env_files = list(project_path.glob(".env.*"))

        # Check for environment configs
        env_config_dir = project_path / "config" / "environments"
        env_configs = (
            list(env_config_dir.glob("*.yml")) if env_config_dir.exists() else []
        )

        if not env_files and not env_configs:
            console.print(
                "📋 No environments found. Run 'fascraft environment init' to create environments.",
                style="yellow",
            )
            return

        # Create table
        table = Table(title="🌍 Available Environments")
        table.add_column("Environment", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Config File", style="blue")

        # Add environment files
        for env_file in env_files:
            env_name = env_file.name.replace(".env.", "")
            table.add_row(env_name, "Environment File", "✅", str(env_file))

        # Add environment configs
        for env_config in env_configs:
            if env_config.name != "environments.yml":
                env_name = env_config.stem
                table.add_row(env_name, "YAML Config", "✅", str(env_config))

        console.print(table)

        # Show current environment
        current_env = get_current_environment(project_path)
        if current_env:
            console.print(f"🔄 Current environment: {current_env}", style="bold green")

    except Exception as e:
        raise FileSystemError(f"Failed to list environments: {str(e)}") from e


def get_current_environment(project_path: Path) -> str | None:
    """Get the current active environment."""
    try:
        # Check for .env file
        env_file = project_path / ".env"
        if env_file.exists():
            with open(env_file, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("ENVIRONMENT="):
                        return line.split("=", 1)[1].strip().strip('"')

        # Check for environment indicator file
        env_indicator = project_path / ".current_environment"
        if env_indicator.exists():
            return env_indicator.read_text().strip()

    except Exception:
        pass

    return None


def switch_environment(project_path: Path, environment: str) -> None:
    """Switch to a different environment."""
    try:
        # Check if environment exists
        env_file = project_path / f".env.{environment}"
        if not env_file.exists():
            raise FileSystemError(
                f"Environment '{environment}' not found. Run 'fascraft environment list' to see available environments."
            )

        # Create .env file from environment template
        with open(env_file, encoding="utf-8") as f:
            env_content = f.read()

        # Write to .env file
        target_env_file = project_path / ".env"
        with open(target_env_file, "w", encoding="utf-8") as f:
            f.write(env_content)

        # Create environment indicator
        env_indicator = project_path / ".current_environment"
        env_indicator.write_text(environment)

        console.print(f"🔄 Switched to environment: {environment}", style="bold green")
        console.print(
            f"📝 Updated .env file with {environment} configuration", style="green"
        )

    except Exception as e:
        raise FileSystemError(
            f"Failed to switch to environment '{environment}': {str(e)}"
        ) from e


def validate_environments(project_path: Path, specific_env: str | None = None) -> None:
    """Validate environment configurations."""
    try:
        # Get environments to validate
        if specific_env:
            environments = [specific_env]
        else:
            env_files = list(project_path.glob(".env.*"))
            environments = [f.stem.replace(".env.", "") for f in env_files]

        if not environments:
            console.print("📋 No environments found to validate.", style="yellow")
            return

        # Validate each environment
        validation_results = []

        for env in environments:
            result = validate_single_environment(project_path, env)
            validation_results.append(result)

        # Display validation results
        display_validation_results(validation_results)

    except Exception as e:
        raise FileSystemError(f"Failed to validate environments: {str(e)}") from e


def validate_single_environment(project_path: Path, env_name: str) -> dict[str, Any]:
    """Validate a single environment configuration."""
    result = {"environment": env_name, "valid": True, "errors": [], "warnings": []}

    try:
        # Check environment file
        env_file = project_path / f".env.{env_name}"
        if not env_file.exists():
            result["valid"] = False
            result["errors"].append(f"Environment file .env.{env_name} not found")
            return result

        # Check environment config
        env_config_file = project_path / "config" / "environments" / f"{env_name}.yml"
        if not env_config_file.exists():
            result["warnings"].append(f"Environment config {env_name}.yml not found")

        # Validate environment file format
        with open(env_file, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    if not key.strip() or not value.strip():
                        result["warnings"].append(
                            f"Line {line_num}: Empty key or value"
                        )

        # Validate environment config YAML
        if env_config_file.exists():
            try:
                with open(env_config_file, encoding="utf-8") as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                result["valid"] = False
                result["errors"].append(f"Invalid YAML in {env_name}.yml: {e}")

    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Validation error: {e}")

    return result


def display_validation_results(results: list) -> None:
    """Display environment validation results."""
    console.print("✅ Environment Validation Results", style="bold blue")

    for result in results:
        if result["valid"]:
            status_style = "green"
            status_icon = "✅"
        else:
            status_style = "red"
            status_icon = "❌"

        # Environment header
        env_text = Text()
        env_text.append(f"{status_icon} ", style=status_style)
        env_text.append(f"{result['environment']}", style="bold white")
        console.print(env_text)

        # Errors
        if result["errors"]:
            for error in result["errors"]:
                error_text = Text()
                error_text.append("  ❌ ", style="red")
                error_text.append(error, style="red")
                console.print(error_text)

        # Warnings
        if result["warnings"]:
            for warning in result["warnings"]:
                warning_text = Text()
                warning_text.append("  ⚠️ ", style="yellow")
                warning_text.append(warning, style="yellow")
                console.print(warning_text)

        console.print()  # Empty line for separation


def display_success_message(project_path: Path, environments: list) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Environment management initialized for ", style="bold white")
    success_text.append(f"{project_path.name}", style="bold cyan")
    success_text.append(" successfully!", style="white")
    console.print(success_text)

    # Display created environments
    env_text = Text()
    env_text.append("🌍 ", style="bold blue")
    env_text.append("Environments created: ", style="bold white")
    env_text.append(", ".join(environments), style="bold cyan")
    console.print(env_text)

    # Display next steps
    next_steps_text = Text()
    next_steps_text.append("📋 ", style="bold blue")
    next_steps_text.append("Next steps:", style="bold white")
    console.print(next_steps_text)

    # Environment management commands
    env_manage_text = Text()
    env_manage_text.append("  🌍 ", style="bold blue")
    env_manage_text.append("Environment Management: ", style="white")
    env_manage_text.append(
        "'fascraft environment list' to see all environments", style="bold cyan"
    )
    console.print(env_manage_text)

    switch_text = Text()
    switch_text.append("  🔄 ", style="bold blue")
    switch_text.append("Switch Environment: ", style="white")
    switch_text.append(
        "'fascraft environment switch --environment dev' to switch", style="bold cyan"
    )
    console.print(switch_text)

    validate_text = Text()
    validate_text.append("  ✅ ", style="bold blue")
    validate_text.append("Validate: ", style="white")
    validate_text.append(
        "'fascraft environment validate' to check configurations", style="bold cyan"
    )
    console.print(validate_text)

    create_text = Text()
    create_text.append("  ➕ ", style="bold blue")
    create_text.append("Create New: ", style="white")
    create_text.append(
        "'fascraft environment create --name custom --template custom'",
        style="bold cyan",
    )
    console.print(create_text)


def display_environment_created(project_path: Path, name: str, template: str) -> None:
    """Display environment creation success message."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Environment ", style="bold white")
    success_text.append(f"'{name}'", style="bold cyan")
    success_text.append(" created successfully!", style="white")
    console.print(success_text)

    # Display environment details
    details_text = Text()
    details_text.append("📋 ", style="bold blue")
    details_text.append("Environment Details:", style="bold white")
    console.print(details_text)

    name_text = Text()
    name_text.append("  🌍 ", style="bold blue")
    name_text.append("Name: ", style="white")
    name_text.append(name, style="bold cyan")
    console.print(name_text)

    template_text = Text()
    template_text.append("  📝 ", style="bold blue")
    template_text.append("Template: ", style="white")
    template_text.append(template, style="bold cyan")
    console.print(template_text)

    # Display next steps
    next_steps_text = Text()
    next_steps_text.append("📋 ", style="bold blue")
    next_steps_text.append("Next steps:", style="bold white")
    console.print(next_steps_text)

    switch_text = Text()
    switch_text.append("  🔄 ", style="bold blue")
    switch_text.append("Switch to: ", style="bold blue")
    switch_text.append(
        f"'fascraft environment switch --environment {name}'", style="bold cyan"
    )
    console.print(switch_text)

    validate_text = Text()
    validate_text.append("  ✅ ", style="bold blue")
    validate_text.append("Validate: ", style="white")
    validate_text.append(
        f"'fascraft environment validate --environment {name}'", style="bold cyan"
    )
    console.print(validate_text)


def display_error_message(error: FasCraftError) -> None:
    """Display error message."""
    error_text = Text()
    error_text.append("❌ ", style="bold red")
    error_text.append("Error: ", style="bold white")
    error_text.append(str(error), style="red")
    console.print(error_text)


def display_unexpected_error(error: Exception) -> None:
    """Display unexpected error message."""
    error_text = Text()
    error_text.append("💥 ", style="bold red")
    error_text.append("Unexpected error: ", style="bold white")
    error_text.append(str(error), style="red")
    console.print(error_text)


if __name__ == "__main__":
    app()
