"""Command for creating a new FastAPI project."""

from pathlib import Path

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.text import Text

# Initialize rich console
console = Console()


def create_new_project(
    project_name: str,
    path: str = typer.Option(
        ".", help="📁 The path where the new project directory will be created"
    ),
) -> None:
    """🏗️ Generates a new FastAPI project."""
    # Convert string path to Path object
    path_obj = Path(path)
    project_path = path_obj / project_name
    if project_path.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Directory '{project_path}' already exists.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    project_path.mkdir(parents=True, exist_ok=True)

    # Set up Jinja2 environment
    env = Environment(
        loader=PackageLoader("fastforge", "templates/new_project"),
        autoescape=select_autoescape(),
    )

    # Define templates to render
    templates = [
        ("__init__.py.jinja2", "__init__.py"),
        ("main.py.jinja2", "main.py"),
        ("pyproject.toml.jinja2", "pyproject.toml"),
        ("README.md.jinja2", "README.md"),
    ]

    # Render all templates
    for template_name, output_name in templates:
        template = env.get_template(template_name)
        content = template.render(
            project_name=project_name, author_name="Lutor Iyornumbe"
        )
        (project_path / output_name).write_text(content)

    success_text = Text()
    success_text.append("✅ ", style="bold green")
    success_text.append("Successfully created new project ", style="bold white")
    success_text.append(f"'{project_name}' ", style="bold cyan")
    success_text.append("at ", style="white")
    success_text.append(f"{project_path}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    next_steps_text = Text()
    next_steps_text.append("🚀 ", style="bold yellow")
    next_steps_text.append("Run ", style="white")
    next_steps_text.append(f"'cd {project_name} && poetry install' ", style="bold cyan")
    next_steps_text.append("to get started.", style="white")
    console.print(next_steps_text)
