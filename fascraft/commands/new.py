"""Command for creating a new FastAPI project."""

from datetime import datetime
from pathlib import Path

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from fascraft.exceptions import (
    DiskSpaceError,
    FasCraftError,
    FileSystemError,
    PermissionError,
    TemplateError,
    TemplateNotFoundError,
    TemplateRenderError,
    CorruptedTemplateError,
)
from fascraft.validation import (
    validate_project_name,
    validate_project_path,
    validate_disk_space,
    validate_file_system_writable,
    validate_path_robust,
)

# Initialize rich console
console = Console(width=None, soft_wrap=False)


def create_new_project(
    project_name: str,
    path: str = typer.Option(
        ".", help="📁 The path where the new project directory will be created"
    ),
) -> None:
    """🏗️ Generates a new FastAPI project."""
    try:
        # Validate inputs with robust validation
        validated_project_name = validate_project_name(project_name)
        validated_path = validate_path_robust(path)
        project_path = validated_path / validated_project_name

        # Validate project path
        validate_project_path(project_path, validated_project_name)

        # Create project with rollback capability
        create_project_with_rollback(project_path, validated_project_name)

        # Display success message and next steps
        display_success_message(project_path, validated_project_name)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def create_project_structure(project_path: Path, project_name: str) -> None:
    """Create the basic project directory structure."""
    try:
        # Ensure project root exists
        project_path.mkdir(parents=True, exist_ok=True)

        # Create main directories
        (project_path / "config").mkdir(parents=True, exist_ok=True)
        (project_path / "routers").mkdir(parents=True, exist_ok=True)
        (project_path / "models").mkdir(parents=True, exist_ok=True)
        (project_path / "schemas").mkdir(parents=True, exist_ok=True)
        (project_path / "services").mkdir(parents=True, exist_ok=True)
        (project_path / "tests").mkdir(parents=True, exist_ok=True)

        console.print("📁 Created project directory structure", style="bold green")

    except OSError as e:
        if e.errno == 13:  # Permission denied
            raise PermissionError(str(project_path), "create directories") from e
        elif e.errno == 28:  # No space left on device
            raise DiskSpaceError("Unknown", "Unknown") from e
        else:
            raise FileSystemError(
                f"Failed to create project structure: {str(e)}"
            ) from e


def render_project_templates_with_progress(
    project_path: Path, project_name: str
) -> None:
    """Render all project templates with progress tracking."""
    templates = [
        ("__init__.py.jinja2", "__init__.py"),
        ("main.py.jinja2", "main.py"),
        ("pyproject.toml.jinja2", "pyproject.toml"),
        ("README.md.jinja2", "README.md"),
        ("env.jinja2", ".env"),
        ("env.sample.jinja2", ".env.sample"),
        ("requirements.txt.jinja2", "requirements.txt"),
        ("requirements.dev.txt.jinja2", "requirements.dev.txt"),
        ("requirements.prod.txt.jinja2", "requirements.prod.txt"),
        ("config/__init__.py.jinja2", "config/__init__.py"),
        ("config/settings.py.jinja2", "config/settings.py"),
        ("config/database.py.jinja2", "config/database.py"),
        ("config/exceptions.py.jinja2", "config/exceptions.py"),
        ("config/middleware.py.jinja2", "config/middleware.py"),
        (".gitignore.jinja2", ".gitignore"),
        ("routers/__init__.py.jinja2", "routers/__init__.py"),
        ("routers/base.py.jinja2", "routers/base.py"),
        ("fascraft.toml.jinja2", "fascraft.toml"),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Rendering templates...", total=len(templates))

        for template_name, output_name in templates:
            try:
                render_single_template(
                    project_path, project_name, template_name, output_name
                )
                progress.advance(task)
            except Exception as e:
                progress.stop()
                raise TemplateRenderError(template_name, str(e)) from e


def display_success_message(project_path: Path, project_name: str) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Successfully created new project ", style="bold white")
    success_text.append(f"'{project_name}' ", style="bold cyan")
    success_text.append("at ", style="white")
    success_text.append(f"{project_path}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    # Display next steps
    display_next_steps(project_path, project_name)

    # Display project features
    display_project_features()

    # Display best wishes
    display_best_wishes()


def display_next_steps(project_path: Path, project_name: str) -> None:
    """Display next steps for the user."""
    next_steps_text = Text()
    next_steps_text.append("⚡ ", style="bold yellow")
    next_steps_text.append("Run ", style="white")
    next_steps_text.append(
        f"'cd {project_name} && pip install -r requirements.txt' ", style="bold cyan"
    )
    next_steps_text.append("to get started.", style="white")
    console.print(next_steps_text)

    dev_deps_text = Text()
    dev_deps_text.append("🛠️ ", style="bold blue")
    dev_deps_text.append("For development, run: ", style="white")
    dev_deps_text.append("'pip install -r requirements.dev.txt'", style="bold cyan")
    console.print(dev_deps_text)


def display_project_features() -> None:
    """Display information about project features."""
    config_info_text = Text()
    config_info_text.append("🔧 ", style="bold blue")
    config_info_text.append("Project includes configuration: ", style="white")
    config_info_text.append("config/settings.py, config/database.py", style="bold cyan")
    console.print(config_info_text)

    router_info_text = Text()
    router_info_text.append("🔄 ", style="bold blue")
    router_info_text.append("Router structure: ", style="white")
    router_info_text.append(
        "Base router with centralized module management", style="bold cyan"
    )
    console.print(router_info_text)

    gitignore_info_text = Text()
    gitignore_info_text.append("📝 ", style="bold blue")
    gitignore_info_text.append("Git integration: ", style="white")
    gitignore_info_text.append(".gitignore file included", style="bold cyan")
    console.print(gitignore_info_text)

    config_file_info_text = Text()
    config_file_info_text.append("⚙️ ", style="bold blue")
    config_file_info_text.append("Configuration: ", style="white")
    config_file_info_text.append("fascraft.toml file created", style="bold cyan")
    console.print(config_file_info_text)

    env_info_text = Text()
    env_info_text.append("🌍 ", style="bold green")
    env_info_text.append("Environment files created: ", style="white")
    env_info_text.append(".env, .env.sample", style="bold cyan")
    console.print(env_info_text)

    deps_info_text = Text()
    deps_info_text.append("📦 ", style="bold yellow")
    deps_info_text.append("Dependency files created: ", style="white")
    deps_info_text.append(
        "requirements.txt, requirements.dev.txt, requirements.prod.txt",
        style="bold cyan",
    )
    console.print(deps_info_text)

    db_setup_text = Text()
    db_setup_text.append("🗄️ ", style="bold green")
    db_setup_text.append("Database setup: ", style="white")
    db_setup_text.append(
        "Run 'alembic init alembic' to initialize migrations", style="bold cyan"
    )
    console.print(db_setup_text)

    db_config_text = Text()
    db_config_text.append("⚙️ ", style="bold blue")
    db_config_text.append(
        "Configure alembic/env.py to import your models and use your database URL",
        style="white",
    )
    console.print(db_config_text)

    generate_info_text = Text()
    generate_info_text.append("✨ ", style="bold yellow")
    generate_info_text.append("Use ", style="white")
    generate_info_text.append("'fascraft generate <module_name>' ", style="bold cyan")
    generate_info_text.append("to add new domain modules.", style="white")
    console.print(generate_info_text)

    readme_text = Text()
    readme_text.append("📖 ", style="bold yellow")
    readme_text.append(
        "See README.md for detailed database setup and migration instructions",
        style="white",
    )
    console.print(readme_text)


def display_best_wishes() -> None:
    """Display encouraging best wishes message."""
    best_wishes_text = Text()
    best_wishes_text.append("🚀 ", style="bold green")
    best_wishes_text.append("Best wishes on your FastAPI journey! ", style="white")
    best_wishes_text.append("Your project is set up for success!", style="bold cyan")
    console.print(best_wishes_text)

    pro_tip_text = Text()
    pro_tip_text.append("💡 ", style="bold blue")
    pro_tip_text.append("Pro tip: ", style="white")
    pro_tip_text.append(
        "Use 'fascraft analyze' to get insights on your project structure!",
        style="bold cyan",
    )
    console.print(pro_tip_text)

    final_text = Text()
    final_text.append("✨ ", style="bold yellow")
    final_text.append("Happy coding! ", style="white")
    final_text.append(
        "Your modular architecture will make future you very grateful!",
        style="bold cyan",
    )
    console.print(final_text)


def display_error_message(error: FasCraftError) -> None:
    """Display user-friendly error message."""
    error_text = Text(no_wrap=True)
    error_text.append("❌ ", style="bold red")
    error_text.append("Error: ", style="bold red")
    error_text.append(error.message, style="white")
    console.print(error_text, soft_wrap=False)

    if error.suggestion:
        suggestion_text = Text(no_wrap=True)
        suggestion_text.append("💡 ", style="bold yellow")
        suggestion_text.append("Suggestion: ", style="bold yellow")
        suggestion_text.append(error.suggestion, style="white")
        console.print(suggestion_text, soft_wrap=False)


def display_unexpected_error(error: Exception) -> None:
    """Display unexpected error message."""
    error_text = Text()
    error_text.append("💥 ", style="bold red")
    error_text.append("Unexpected error: ", style="bold red")
    error_text.append(str(error), style="white")
    console.print(error_text)

    suggestion_text = Text()
    suggestion_text.append("🆘 ", style="bold yellow")
    suggestion_text.append(
        "This is unexpected. Please report this bug at: ", style="white"
    )
    suggestion_text.append(
        "https://github.com/LexxLuey/fascraft/issues", style="bold cyan"
    )
    console.print(suggestion_text)


def create_project_with_rollback(project_path: Path, project_name: str) -> None:
    """Create project with automatic rollback on failure."""
    backup_path = None
    created_files = []

    try:
        # Validate file system and disk space before starting
        # Only validate if parent directory exists, otherwise we'll create it
        if project_path.parent.exists():
            validate_file_system_writable(project_path.parent)
            validate_disk_space(project_path.parent, required_space_mb=20)

        # Create backup of existing directory if it exists
        if project_path.exists():
            backup_path = create_backup_directory(project_path)

        # Create project structure
        create_project_structure(project_path, project_name)
        created_files.append("structure")

        # Render templates
        try:
            render_project_templates_with_progress(project_path, project_name)
            created_files.append("templates")
        except Exception as e:
            console.print(f"⚠️ Template rendering failed: {e}", style="yellow")
            console.print("Creating minimal project structure...", style="yellow")
            render_essential_templates(project_path, project_name)
            created_files.append("templates")

        # Validate generated project
        validate_generated_project(project_path)
        created_files.append("validation")

    except Exception as e:
        # Rollback on any failure
        console.print("🔄 Rolling back due to error...", style="bold yellow")
        rollback_project_creation(project_path, backup_path, created_files)
        raise e from e


def create_backup_directory(path: Path) -> Path:
    """Create backup of existing directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.name}_backup_{timestamp}"
    backup_path = path.parent / backup_name

    try:
        import shutil

        shutil.copytree(path, backup_path)
        console.print(f"💾 Created backup at: {backup_path}", style="green")
        return backup_path
    except Exception as e:
        console.print(f"⚠️ Warning: Failed to create backup: {e}", style="yellow")
        return None


def rollback_project_creation(
    project_path: Path, backup_path: Path, created_files: list
) -> None:
    """Rollback project creation on failure."""
    try:
        # Remove created project directory
        if project_path.exists():
            import shutil

            shutil.rmtree(project_path)
            console.print("🗑️ Removed failed project directory", style="yellow")

        # Restore from backup if available
        if backup_path and backup_path.exists():
            import shutil

            shutil.copytree(backup_path, project_path)
            console.print("🔄 Restored from backup", style="green")

    except Exception as e:
        console.print(f"⚠️ Warning: Rollback failed: {e}", style="yellow")
        console.print("Manual cleanup may be required", style="red")


def create_project_with_graceful_degradation(
    project_path: Path, project_name: str
) -> None:
    """Create project with graceful degradation for partial failures."""
    warnings = []

    try:
        # Create project structure
        try:
            create_project_structure(project_path, project_name)
        except Exception as e:
            warnings.append(f"Failed to create complete structure: {e}")
            create_minimal_structure(project_path, project_name)

        # Render templates
        try:
            render_project_templates_with_progress(project_path, project_name)
        except Exception as e:
            warnings.append(f"Failed to render some templates: {e}")
            render_essential_templates(project_path, project_name)

        # Display warnings if any
        if warnings:
            display_partial_success_warnings(warnings)

    except Exception as e:
        # If even minimal setup fails, rollback
        rollback_project_creation(project_path, None, [])
        raise e


def create_minimal_structure(project_path: Path, project_name: str) -> None:
    """Create minimal project structure when full structure fails."""
    try:
        (project_path / "main.py").parent.mkdir(parents=True, exist_ok=True)
        console.print("⚠️ Created minimal project structure", style="yellow")
    except Exception as e:
        raise FileSystemError(
            f"Failed to create even minimal structure: {str(e)}"
        ) from e


def render_essential_templates(project_path: Path, project_name: str) -> None:
    """Render only essential templates when full rendering fails."""
    essential_templates = [
        ("main.py.jinja2", "main.py"),
        ("pyproject.toml.jinja2", "pyproject.toml"),
        ("requirements.txt.jinja2", "requirements.txt"),
        ("__init__.py.jinja2", "__init__.py"),
        ("config/__init__.py.jinja2", "config/__init__.py"),
        ("config/settings.py.jinja2", "config/settings.py"),
        ("routers/__init__.py.jinja2", "routers/__init__.py"),
        ("routers/base.py.jinja2", "routers/base.py"),
    ]

    for template_name, output_name in essential_templates:
        try:
            render_single_template(
                project_path, project_name, template_name, output_name
            )
        except Exception as e:
            console.print(f"⚠️ Failed to render {output_name}: {e}", style="yellow")


def display_partial_success_warnings(warnings: list) -> None:
    """Display warnings for partial failures."""
    console.print("\n⚠️ Project created with warnings:", style="bold yellow")
    for warning in warnings:
        console.print(f"  • {warning}", style="yellow")
    console.print("Some features may not work correctly", style="yellow")


def validate_generated_project(project_path: Path) -> None:
    """Validate that the generated project is valid."""
    essential_files = ["main.py", "pyproject.toml"]

    for file_name in essential_files:
        file_path = project_path / file_name
        if not file_path.exists():
            raise TemplateError(f"Essential file {file_name} was not generated")

        # Check if file has content
        try:
            content = file_path.read_text()
            if not content.strip():
                raise TemplateError(f"Generated file {file_name} is empty")
        except Exception as e:
            raise TemplateError(
                f"Failed to read generated file {file_name}: {str(e)}"
            ) from e


def render_single_template(
    project_path: Path, project_name: str, template_name: str, output_name: str
) -> None:
    """Render a single template file."""
    try:
        # Set up Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Load and render template
        template = env.get_template(template_name)
        content = template.render(
            project_name=project_name, author_name="Lutor Iyornumbe"
        )

        # Ensure output directory exists
        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write rendered content
        output_path.write_text(content, encoding="utf-8")

    except Exception as e:
        if "No such file or directory" in str(e):
            raise TemplateNotFoundError(template_name, "templates/new_project") from e
        elif "Template syntax error" in str(e) or "Template error" in str(e):
            raise CorruptedTemplateError(template_name, str(e)) from e
        else:
            raise TemplateRenderError(template_name, str(e)) from e
