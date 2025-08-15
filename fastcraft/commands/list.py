"""Command for listing existing modules in a FastAPI project."""

from pathlib import Path
from typing import List

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .generate import is_fastapi_project

# Initialize rich console
console = Console()


def list_modules(
    path: str = typer.Option(
        ".", help="📁 The path to the existing FastAPI project"
    ),
) -> None:
    """📋 Lists all existing domain modules in a FastAPI project."""
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

    # Find all domain modules
    modules = find_domain_modules(path_obj)
    
    if not modules:
        info_text = Text()
        info_text.append("💡 ", style="bold blue")
        info_text.append(" No domain modules found in this project.", style="white")
        info_text.append("\nUse ", style="white")
        info_text.append("'fastcraft generate <module_name>' ", style="bold cyan")
        info_text.append("to create your first module.", style="white")
        console.print(info_text)
        return

    # Display modules in a table
    display_modules_table(modules, path_obj)


def find_domain_modules(project_path: Path) -> List[dict]:
    """Find all domain modules in the project."""
    modules = []
    
    for item in project_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['config', '__pycache__', 'tests', 'migrations']:
            # Check if it's a domain module by looking for key files
            if is_domain_module(item):
                module_info = analyze_module(item)
                modules.append(module_info)
    
    # Sort modules by name
    modules.sort(key=lambda x: x['name'])
    return modules


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
        'size': 0,  # Add size field
        'has_tests': False,
        'health_status': 'healthy'
    }
    
    # Check for all expected files
    expected_files = [
        'models.py', 'schemas.py', 'services.py', 'routers.py',
        '__init__.py', 'tests/__init__.py', 'tests/test_models.py'
    ]
    
    for file_name in expected_files:
        file_path = module_path / file_name
        if file_path.exists():
            module_info['files'].append(file_name)
            # Calculate size for existing files
            module_info['size'] += file_path.stat().st_size
        else:
            if file_name in ['models.py', 'schemas.py', 'services.py', 'routers.py']:
                module_info['health_status'] = 'incomplete'
    
    # Check if tests directory exists
    if (module_path / 'tests').exists():
        module_info['has_tests'] = True
    
    return module_info


def display_modules_table(modules: List[dict], project_path: Path) -> None:
    """Display modules information in a rich table."""
    # Header
    header_text = Text()
    header_text.append("📋 ", style="bold blue")
    header_text.append(f"Found {len(modules)} domain module(s) in ", style="white")
    header_text.append(f"{project_path.name}", style="bold cyan")
    console.print(header_text)
    console.print()
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module Name", style="cyan", width=20)
    table.add_column("Files", style="white", width=30)
    table.add_column("Tests", style="white", width=10)
    table.add_column("Health", style="white", width=15)
    
    for module in modules:
        # Health status with color
        health_style = "green" if module['health_status'] == 'healthy' else "yellow"
        health_text = "✅ Healthy" if module['health_status'] == 'healthy' else "⚠️ Incomplete"
        
        # Files count
        files_text = f"{len(module['files'])}/7 files"
        
        # Tests status
        tests_text = "✅ Yes" if module['has_tests'] else "❌ No"
        
        table.add_row(
            module['name'],
            files_text,
            tests_text,
            health_text
        )
    
    console.print(table)
    
    # Footer with actions
    footer_text = Text()
    footer_text.append("💡 ", style="bold yellow")
    footer_text.append("Actions: ", style="white")
    footer_text.append("'fastcraft remove <module>' ", style="bold cyan")
    footer_text.append("to remove a module, ", style="white")
    footer_text.append("'fastcraft update <module>' ", style="bold cyan")
    footer_text.append("to update templates", style="white")
    console.print(footer_text)
