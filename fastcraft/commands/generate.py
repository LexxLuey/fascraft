"""Command for generating new domain modules in existing FastCraft projects."""

from pathlib import Path
from typing import Optional

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.text import Text

# Initialize rich console
console = Console()


def is_fastapi_project(project_path: Path) -> bool:
    """Check if the given path is a FastAPI project."""
    # Check for FastAPI indicators
    if (project_path / "main.py").exists():
        content = (project_path / "main.py").read_text()
        if "FastAPI" in content or "fastapi" in content:
            return True
    
    # Check for pyproject.toml with FastAPI dependency
    if (project_path / "pyproject.toml").exists():
        content = (project_path / "pyproject.toml").read_text()
        if "fastapi" in content.lower():
            return True
    
    return False


def ensure_config_structure(project_path: Path) -> None:
    """Ensure config directory and files exist."""
    config_dir = project_path / "config"
    
    if not config_dir.exists():
        console.print("📁 Creating config directory...", style="bold yellow")
        config_dir.mkdir(exist_ok=True)
        
        # Create basic config files if they don't exist
        if not (config_dir / "__init__.py").exists():
            (config_dir / "__init__.py").write_text('"""Configuration module."""\n')
        
        if not (config_dir / "settings.py").exists():
            (config_dir / "settings.py").write_text('"""Application settings."""\n\napp_name = "{{ project_name }}"\n')
        
        if not (config_dir / "database.py").exists():
            (config_dir / "database.py").write_text('"""Database configuration."""\n\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\n\nBase = declarative_base()\n')


def generate_module(
    module_name: str,
    path: str = typer.Option(
        ".", help="📁 The path to the existing FastAPI project"
    ),
) -> None:
    """🔧 Generates a new domain module in an existing FastAPI project."""
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

    # Check if module already exists
    module_dir = path_obj / module_name
    if module_dir.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Module '{module_name}' already exists at ", style="white")
        error_text.append(f"{module_dir}", style="yellow")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Ensure config structure exists
    ensure_config_structure(path_obj)

    # Set up Jinja2 environment for module templates
    env = Environment(
        loader=PackageLoader("fastcraft", "templates/module"),
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
            project_name=path_obj.name,
            module_name_plural=f"{module_name}s",
            module_name_title=module_name.title(),
        )
        output_path = path_obj / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    # Update main.py to include the new router
    update_main_py(path_obj, module_name)

    success_text = Text()
    success_text.append("🎯 ", style="bold green")
    success_text.append("Successfully generated domain module ", style="bold white")
    success_text.append(f"'{module_name}' ", style="bold cyan")
    success_text.append("in ", style="white")
    success_text.append(f"{path_obj}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    next_steps_text = Text()
    next_steps_text.append("🚀 ", style="bold yellow")
    next_steps_text.append("Next steps:", style="white")
    next_steps_text.append(f"\n  1. Import the new {module_name} module in main.py", style="bold cyan")
    next_steps_text.append(f"\n  2. Run 'pip install -r requirements.txt' to install dependencies", style="bold cyan")
    next_steps_text.append(f"\n  3. Test your new module with 'pytest {module_name}/tests/'", style="bold cyan")
    console.print(next_steps_text)


def update_main_py(project_path: Path, module_name: str) -> None:
    """Update main.py to include the new module router."""
    main_py_path = project_path / "main.py"
    
    if not main_py_path.exists():
        console.print("⚠️  Warning: main.py not found, skipping router integration", style="yellow")
        return
    
    content = main_py_path.read_text()
    
    # Add import if not present
    import_statement = f"from {module_name} import routers as {module_name}_routers"
    if import_statement not in content:
        # Find the comment line for imports
        lines = content.split('\n')
        new_lines = []
        import_added = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith("# from") and not import_added:
                new_lines.append(import_statement)
                import_added = True
        
        if not import_added:
            # Add after existing imports
            for i, line in enumerate(lines):
                if line.strip().startswith("from fastapi import"):
                    new_lines.insert(i + 1, import_statement)
                    break
        
        content = '\n'.join(new_lines)
    
    # Add router include if not present
    router_include = f"app.include_router({module_name}_routers.router, prefix=f\"/api/v1/{module_name}s\", tags=[\"{module_name}s\"])"
    if router_include not in content:
        # Find the comment line for router includes
        lines = content.split('\n')
        new_lines = []
        router_added = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith("# app.include_router") and not router_added:
                new_lines.append(router_include)
                router_added = True
        
        if not router_added:
            # Add after existing router includes
            for i, line in enumerate(lines):
                if line.strip().startswith("app.include_router"):
                    new_lines.insert(i + 1, router_include)
                    break
        
        content = '\n'.join(new_lines)
    
    # Write updated content
    main_py_path.write_text(content)
    console.print(f"📝 Updated main.py to include {module_name} router", style="bold green")
