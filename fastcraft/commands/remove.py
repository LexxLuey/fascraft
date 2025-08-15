"""Command for removing domain modules from a FastAPI project."""

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.text import Text

from .generate import is_fastapi_project
from .list import find_domain_modules

# Initialize rich console
console = Console()


def remove_module(
    module_name: str,
    path: str = typer.Option(
        ".", help="📁 The path to the existing FastAPI project"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="🚨 Force removal without confirmation"
    ),
) -> None:
    """🗑️ Removes a domain module from a FastAPI project."""
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
        error_text.append("\nMake sure you're in a project with FastAPI dependencies.", style="white")
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
        error_text.append(f"'{module_name}' is not a valid domain module.", style="white")
        error_text.append("\nOnly domain modules can be removed with this command.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Show module details before removal
    module_info = analyze_module(module_path)
    display_removal_preview(module_info, path_obj)

    # Confirm removal
    if not force:
        if not confirm_removal(module_name):
            console.print("⏹️ Module removal cancelled.", style="bold yellow")
            return

    # Remove the module
    try:
        remove_module_files(module_path)
        update_main_py_after_removal(path_obj, module_name)
        
        success_text = Text()
        success_text.append("🗑️ ", style="bold green")
        success_text.append("Successfully removed module ", style="bold white")
        success_text.append(f"'{module_name}' ", style="bold cyan")
        success_text.append("from ", style="white")
        success_text.append(f"{path_obj.name}", style="bold blue")
        success_text.append(".", style="white")
        console.print(success_text)
        
    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Failed to remove module '{module_name}': ", style="white")
        error_text.append(str(e), style="yellow")
        console.print(error_text)
        raise typer.Exit(code=1)


def is_domain_module(module_path: Path) -> bool:
    """Check if a directory is a domain module."""
    required_files = ['models.py', 'schemas.py', 'services.py', 'routers.py']
    
    for file_name in required_files:
        if not (module_path / file_name).exists():
            return False
    
    return True


def analyze_module(module_path: Path) -> dict:
    """Analyze a domain module and return information about it."""
    module_info = {
        'name': module_path.name,
        'path': module_path,
        'files': [],
        'size': 0,
        'has_tests': False
    }
    
    # Count files and calculate size
    for file_path in module_path.rglob('*'):
        if file_path.is_file():
            module_info['files'].append(str(file_path.relative_to(module_path)))
            module_info['size'] += file_path.stat().st_size
    
    # Check if tests directory exists
    if (module_path / 'tests').exists():
        module_info['has_tests'] = True
    
    return module_info


def display_removal_preview(module_info: dict, project_path: Path) -> None:
    """Display what will be removed."""
    preview_text = Text()
    preview_text.append("🗑️ ", style="bold red")
    preview_text.append("Module Removal Preview", style="bold white")
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
    details_text.append(" files", style="white")
    console.print(details_text)
    
    details_text = Text()
    details_text.append("💾 ", style="bold blue")
    details_text.append("Size: ", style="white")
    details_text.append(f"{module_info['size'] / 1024:.1f} KB", style="bold cyan")
    console.print(details_text)
    
    if module_info['has_tests']:
        details_text = Text()
        details_text.append("🧪 ", style="bold blue")
        details_text.append("Tests: ", style="white")
        details_text.append("Yes", style="bold green")
        console.print(details_text)
    
    console.print()


def confirm_removal(module_name: str) -> bool:
    """Ask user to confirm module removal."""
    warning_text = Text()
    warning_text.append("⚠️ ", style="bold yellow")
    warning_text.append(" This action cannot be undone!", style="bold white")
    console.print(warning_text)
    
    confirm_text = Text()
    confirm_text.append("Are you sure you want to remove module ", style="white")
    confirm_text.append(f"'{module_name}'", style="bold cyan")
    confirm_text.append("? (y/N): ", style="white")
    
    response = input(confirm_text.plain)
    return response.lower() in ['y', 'yes']


def remove_module_files(module_path: Path) -> None:
    """Remove all files and directories in the module."""
    if module_path.exists():
        shutil.rmtree(module_path)


def update_main_py_after_removal(project_path: Path, module_name: str) -> None:
    """Update main.py to remove references to the deleted module."""
    main_py_path = project_path / "main.py"
    
    if not main_py_path.exists():
        console.print("⚠️  Warning: main.py not found, skipping cleanup", style="yellow")
        return
    
    content = main_py_path.read_text()
    
    # Remove import statement
    import_pattern = f"from {module_name} import routers as {module_name}_routers"
    if import_pattern in content:
        content = content.replace(import_pattern, "")
        console.print(f"📝 Removed import for {module_name} from main.py", style="green")
    
    # Remove router include - use simpler pattern matching
    # Look for lines containing the router variable
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that contain the router variable for this module
        if f"{module_name}_routers.router" in line:
            console.print(f"📝 Removed router include for {module_name} from main.py", style="green")
            continue
        
        # Skip lines that contain the import for this module
        if f"from {module_name} import routers as {module_name}_routers" in line:
            continue
        
        cleaned_lines.append(line)
    
    # Clean up consecutive empty lines
    final_lines = []
    for i, line in enumerate(cleaned_lines):
        if i > 0 and line.strip() == "" and cleaned_lines[i-1].strip() == "":
            continue
        final_lines.append(line)
    
    # Write updated content
    main_py_path.write_text('\n'.join(final_lines))
