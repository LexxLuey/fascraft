"""Command for managing FasCraft project configuration."""

try:
    import tomllib
except ImportError:
    # Fallback for Python < 3.11
    import tomli as tomllib

from pathlib import Path

import tomli_w
import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Initialize rich console
console = Console()


def manage_config(
    action: str = typer.Argument(
        "show", help="Action to perform: show, create, update, or validate"
    ),
    path: str = typer.Option(".", help="📁 The path to the FastAPI project"),
    key: str | None = typer.Option(
        None, help="Configuration key to update (for update action)"
    ),
    value: str | None = typer.Option(
        None, help="New value for the configuration key (for update action)"
    ),
) -> None:
    """⚙️ Manage FasCraft project configuration."""
    path_obj = Path(path)

    if not path_obj.exists():
        error_text = Text("❌ Error: Path does not exist.", style="bold red")
        console.print(error_text)
        raise typer.Exit(code=1)

    if not is_fastapi_project(path_obj):
        error_text = Text("❌ Error: This is not a FastAPI project.", style="bold red")
        console.print(error_text)
        raise typer.Exit(code=1)

    config_path = path_obj / "fascraft.toml"

    if action == "show":
        show_config(config_path, path_obj)
    elif action == "create":
        create_config(config_path, path_obj)
    elif action == "update":
        if not key or not value:
            error_text = Text(
                "❌ Error: Both --key and --value are required for update action.",
                style="bold red",
            )
            console.print(error_text)
            raise typer.Exit(code=1)
        update_config(config_path, key, value)
    elif action == "validate":
        validate_config(config_path)
    else:
        error_text = Text(
            f"❌ Error: Unknown action '{action}'. Use: show, create, update, or validate",
            style="bold red",
        )
        console.print(error_text)
        raise typer.Exit(code=1)


def is_fastapi_project(project_path: Path) -> bool:
    """Check if the given path is a FastAPI project."""
    if (project_path / "main.py").exists():
        content = (project_path / "main.py").read_text()
        if "FastAPI" in content or "fastapi" in content:
            return True

    if (project_path / "pyproject.toml").exists():
        content = (project_path / "pyproject.toml").read_text()
        if "fastapi" in content.lower():
            return True

    return False


def show_config(config_path: Path, project_path: Path) -> None:
    """Show the current FasCraft configuration."""
    if not config_path.exists():
        console.print("❌ No FasCraft configuration found.", style="bold red")
        console.print("💡 Use 'fascraft config create' to create one.", style="yellow")
        return

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        console.print(
            f"📋 FasCraft Configuration for: {project_path.name}", style="bold green"
        )

        # Project section
        if "project" in config:
            project_table = Table(title="Project Settings")
            project_table.add_column("Setting", style="cyan")
            project_table.add_column("Value", style="white")

            for key, value in config["project"].items():
                project_table.add_row(key, str(value))

            console.print(project_table)

        # Router section
        if "router" in config:
            router_table = Table(title="Router Settings")
            router_table.add_column("Setting", style="cyan")
            router_table.add_column("Value", style="white")

            for key, value in config["router"].items():
                router_table.add_row(key, str(value))

            console.print(router_table)

        # Database section
        if "database" in config:
            db_table = Table(title="Database Settings")
            db_table.add_column("Setting", style="cyan")
            db_table.add_column("Value", style="white")

            for key, value in config["database"].items():
                if isinstance(value, list):
                    db_table.add_row(key, ", ".join(value))
                else:
                    db_table.add_row(key, str(value))

            console.print(db_table)

        # Modules section
        if "modules" in config:
            modules_table = Table(title="Module Settings")
            modules_table.add_column("Setting", style="cyan")
            modules_table.add_column("Value", style="white")

            for key, value in config["modules"].items():
                modules_table.add_row(key, str(value))

            console.print(modules_table)

        # Environment sections
        for env in ["development", "production"]:
            if env in config:
                env_table = Table(title=f"{env.title()} Settings")
                env_table.add_column("Setting", style="cyan")
                env_table.add_column("Value", style="white")

                for key, value in config[env].items():
                    env_table.add_row(key, str(value))

                console.print(env_table)

    except Exception as e:
        error_text = Text(f"❌ Error reading configuration: {str(e)}", style="bold red")
        console.print(error_text)
        raise typer.Exit(code=1) from e


def create_config(config_path: Path, project_path: Path) -> None:
    """Create a new FasCraft configuration file."""
    if config_path.exists():
        console.print("⚠️  Configuration file already exists.", style="yellow")
        response = typer.confirm("Do you want to overwrite it?")
        if not response:
            return

    config = {
        "project": {
            "name": project_path.name,
            "version": "0.1.0",
            "description": "A FastAPI project managed with FasCraft",
        },
        "router": {"base_prefix": "/api/v1", "health_endpoint": True},
        "database": {
            "default": "sqlite",
            "supported": ["sqlite", "postgresql", "mysql", "mongodb"],
        },
        "modules": {
            "auto_import": True,
            "prefix_strategy": "plural",
            "test_coverage": True,
        },
        "development": {"auto_reload": True, "debug": True, "log_level": "DEBUG"},
        "production": {"auto_reload": False, "debug": False, "log_level": "INFO"},
    }

    try:
        with open(config_path, "wb") as f:
            tomli_w.dump(config, f)

        console.print(
            "✅ FasCraft configuration created successfully!", style="bold green"
        )
        console.print(f"📁 Location: {config_path}", style="white")

    except Exception as e:
        error_text = Text(
            f"❌ Error creating configuration: {str(e)}", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1) from e


def update_config(config_path: Path, key: str, value: str) -> None:
    """Update a configuration value."""
    if not config_path.exists():
        console.print("❌ No FasCraft configuration found.", style="bold red")
        console.print(
            "💡 Use 'fascraft config create' to create one first.", style="yellow"
        )
        return

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        # Parse the key (e.g., "project.name" -> config["project"]["name"])
        keys = key.split(".")
        if len(keys) != 2:
            error_text = Text(
                "❌ Error: Key must be in format 'section.key' (e.g., 'project.name')",
                style="bold red",
            )
            console.print(error_text)
            raise typer.Exit(code=1)

        section, setting = keys

        if section not in config:
            error_text = Text(
                f"❌ Error: Section '{section}' not found in configuration",
                style="bold red",
            )
            console.print(error_text)
            raise typer.Exit(code=1)

        # Convert value to appropriate type
        if value.lower() in ["true", "false"]:
            value = value.lower() == "true"
        elif value.isdigit():
            value = int(value)
        elif value.startswith("[") and value.endswith("]"):
            # Simple list parsing
            value = [item.strip().strip("\"'") for item in value[1:-1].split(",")]

        # Update the value
        old_value = config[section][setting]
        config[section][setting] = value

        # Write back to file
        with open(config_path, "wb") as f:
            tomli_w.dump(config, f)

        console.print(f"✅ Updated {key}: {old_value} → {value}", style="bold green")

    except Exception as e:
        error_text = Text(
            f"❌ Error updating configuration: {str(e)}", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1) from e


def validate_config(config_path: Path) -> None:
    """Validate the FasCraft configuration file."""
    if not config_path.exists():
        console.print("❌ No FasCraft configuration found.", style="bold red")
        return

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        console.print("🔍 Validating FasCraft configuration...", style="bold blue")

        validation_table = Table(title="Configuration Validation")
        validation_table.add_column("Section", style="cyan")
        validation_table.add_column("Status", style="white")
        validation_table.add_column("Details", style="white")

        # Validate required sections
        required_sections = ["project", "router", "database", "modules"]
        for section in required_sections:
            if section in config:
                validation_table.add_row(section, "✅ Present", "Valid")
            else:
                validation_table.add_row(section, "❌ Missing", "Required")

        # Validate project section
        if "project" in config:
            project = config["project"]
            if "name" in project and project["name"]:
                validation_table.add_row(
                    "project.name", "✅ Valid", f"'{project['name']}'"
                )
            else:
                validation_table.add_row(
                    "project.name", "❌ Invalid", "Must not be empty"
                )

        # Validate router section
        if "router" in config:
            router = config["router"]
            if "base_prefix" in router and router["base_prefix"].startswith("/"):
                validation_table.add_row(
                    "router.base_prefix", "✅ Valid", router["base_prefix"]
                )
            else:
                validation_table.add_row(
                    "router.base_prefix", "❌ Invalid", "Must start with '/'"
                )

        console.print(validation_table)

        # Check for warnings
        warnings = []
        if "database" in config:
            db = config["database"]
            if "default" in db and db["default"] not in db.get("supported", []):
                warnings.append(
                    f"Default database '{db['default']}' not in supported list"
                )

        if warnings:
            console.print("\n⚠️  Warnings:", style="bold yellow")
            for warning in warnings:
                console.print(f"• {warning}", style="white")

        console.print("\n✅ Configuration validation completed!", style="bold green")

    except Exception as e:
        error_text = Text(
            f"❌ Error validating configuration: {str(e)}", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1) from e
