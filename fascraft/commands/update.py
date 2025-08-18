"""Command for updating existing domain modules with latest templates."""

from pathlib import Path

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.text import Text

from .generate import is_fastapi_project

# Initialize rich console
console = Console()


def update_module(
    module_name: str,
    path: str = typer.Option(".", help="📁 The path to the existing FastAPI project"),
    force: bool = typer.Option(
        False, "--force", "-f", help="🚨 Force update without confirmation"
    ),
    backup: bool = typer.Option(
        True, "--no-backup", help="💾 Create backup before updating"
    ),
) -> None:
    """🔄 Updates an existing domain module with the latest templates."""
    if not module_name or not module_name.strip():
        error_text = Text(
            "❌ Error: Module name cannot be empty or whitespace.", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Convert string path to Path object
    path_obj = Path(path)
    if not path_obj.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Path '{path_obj}' does not exist.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if it's a FastAPI project
    if not is_fastapi_project(path_obj):
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"'{path_obj}' is not a FastAPI project.", style="white")
        error_text.append(
            "\nMake sure you're in a project with FastAPI dependencies.", style="white"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if module exists
    module_path = path_obj / module_name
    if not module_path.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Module '{module_name}' does not exist at ", style="white")
        error_text.append(f"{module_path}", style="yellow")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Verify it's actually a domain module
    if not is_domain_module(module_path):
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(
            f"'{module_name}' is not a valid domain module.", style="white"
        )
        error_text.append(
            "\nOnly domain modules can be updated with this command.", style="white"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Show module details and what will be updated
    module_info = analyze_module(module_path)
    display_update_preview(module_info, path_obj)

    # Confirm update
    if not force:
        if not confirm_update(module_name):
            console.print("⏹️ Module update cancelled.", style="bold yellow")
            return

    # Create backup if requested
    backup_path = None
    if backup:
        backup_path = create_backup(module_path, path_obj)

    # Update the module
    try:
        update_module_files(module_path, module_name, path_obj.name)

        success_text = Text()
        success_text.append("🔄 ", style="bold green")
        success_text.append("Successfully updated module ", style="bold white")
        success_text.append(f"'{module_name}' ", style="bold cyan")
        success_text.append("in ", style="white")
        success_text.append(f"{path_obj.name}", style="bold blue")
        success_text.append(".", style="white")
        console.print(success_text)

        if backup_path:
            backup_text = Text()
            backup_text.append("💾 ", style="bold blue")
            backup_text.append("Backup created at: ", style="white")
            backup_text.append(f"{backup_path}", style="bold cyan")
            console.print(backup_text)

    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Failed to update module '{module_name}': ", style="white")
        error_text.append(str(e), style="yellow")
        console.print(error_text)

        # Restore from backup if available
        if backup_path:
            restore_text = Text()
            restore_text.append("🔄 ", style="bold yellow")
            restore_text.append("Attempting to restore from backup...", style="white")
            console.print(restore_text)
            restore_from_backup(backup_path, module_path)

        raise typer.Exit(code=1) from e


def is_domain_module(module_path: Path) -> bool:
    """Check if a directory is a domain module."""
    required_files = ["models.py", "schemas.py", "services.py", "routers.py"]

    for file_name in required_files:
        if not (module_path / file_name).exists():
            return False

    return True


def analyze_module(module_path: Path) -> dict:
    """Analyze a domain module and return information about it."""
    module_info = {
        "name": module_path.name,
        "path": module_path,
        "files": [],
        "size": 0,
        "has_tests": False,
        "last_modified": None,
    }

    # Count files and calculate size
    for file_path in module_path.rglob("*"):
        if file_path.is_file():
            module_info["files"].append(str(file_path.relative_to(module_path)))
            module_info["size"] += file_path.stat().st_size

            # Track last modification time
            mtime = file_path.stat().st_mtime
            if (
                module_info["last_modified"] is None
                or mtime > module_info["last_modified"]
            ):
                module_info["last_modified"] = mtime

    # Check if tests directory exists
    if (module_path / "tests").exists():
        module_info["has_tests"] = True

    return module_info


def display_update_preview(module_info: dict, project_path: Path) -> None:
    """Display what will be updated."""
    preview_text = Text()
    preview_text.append("🔄 ", style="bold blue")
    preview_text.append("Module Update Preview", style="bold white")
    console.print(preview_text)
    console.print()

    details_text = Text()
    details_text.append("📁 ", style="bold blue")
    details_text.append("Module: ", style="white")
    details_text.append(f"{module_info['name']}", style="bold cyan")
    console.print(details_text)

    details_text = Text()
    details_text.append("📊 ", style="bold blue")
    details_text.append("Files: ", style="white")
    details_text.append(f"{len(module_info['files'])}", style="bold cyan")
    details_text.append(" files will be updated", style="white")
    console.print(details_text)

    details_text = Text()
    details_text.append("💾 ", style="bold blue")
    details_text.append("Current size: ", style="white")
    details_text.append(f"{module_info['size'] / 1024:.1f} KB", style="bold cyan")
    console.print(details_text)

    if module_info["has_tests"]:
        details_text = Text()
        details_text.append("🧪 ", style="bold blue")
        details_text.append("Tests: ", style="white")
        details_text.append("Will be updated", style="bold green")
        console.print(details_text)

    console.print()

    warning_text = Text()
    warning_text.append("⚠️ ", style="bold yellow")
    warning_text.append(" This will overwrite existing files!", style="bold white")
    console.print(warning_text)
    console.print()


def confirm_update(module_name: str) -> bool:
    """Ask user to confirm module update."""
    confirm_text = Text()
    confirm_text.append("Are you sure you want to update module ", style="white")
    confirm_text.append(f"'{module_name}'", style="bold cyan")
    confirm_text.append("? (y/N): ", style="white")

    response = input(confirm_text.plain)
    return response.lower() in ["y", "yes"]


def create_backup(module_path: Path, project_path: Path) -> Path:
    """Create a backup of the module before updating."""
    import shutil
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{module_path.name}_backup_{timestamp}"
    backup_path = project_path / backup_name

    try:
        shutil.copytree(module_path, backup_path)
        console.print(f"💾 Created backup at: {backup_path}", style="green")
        return backup_path
    except Exception as e:
        console.print(f"⚠️  Warning: Failed to create backup: {e}", style="yellow")
        return None


def update_module_files(module_path: Path, module_name: str, project_name: str) -> None:
    """Update the module files with latest templates."""
    # Set up Jinja2 environment for module templates
    env = Environment(
        loader=PackageLoader("fascraft", "templates/module"),
        autoescape=select_autoescape(),
    )

    # Define module templates to render
    templates = [
        ("__init__.py.jinja2", f"{module_name}/__init__.py"),
        ("models.py.jinja2", f"{module_name}/models.py"),
        ("schemas.py.jinja2", f"{module_name}/schemas.py"),
        ("services.py.jinja2", f"{module_name}/services.py"),
        ("routers.py.jinja2", f"{module_name}/routers.py"),
        ("tests/__init__.py.jinja2", f"{module_name}/tests/__init__.py"),
        ("tests/test_models.py.jinja2", f"{module_name}/tests/test_models.py"),
    ]

    # Render all module templates
    for template_name, output_name in templates:
        template = env.get_template(template_name)
        content = template.render(
            module_name=module_name,
            project_name=project_name,
            module_name_plural=f"{module_name}s",
            module_name_title=module_name.title(),
        )
        output_path = module_path.parent / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        console.print(f"📝 Updated {output_name}", style="green")


def restore_from_backup(backup_path: Path, module_path: Path) -> None:
    """Restore module from backup after failed update."""
    import shutil

    try:
        if module_path.exists():
            shutil.rmtree(module_path)
        shutil.copytree(backup_path, module_path)
        console.print("✅ Module restored from backup", style="green")
    except Exception as e:
        console.print(f"❌ Failed to restore from backup: {e}", style="red")
