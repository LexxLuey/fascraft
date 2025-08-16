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
    if not project_name or not project_name.strip():
        error_text = Text(
            "❌ Error: Project name cannot be empty or whitespace.", style="bold red"
        )
        console.print(error_text, err=True)
        raise typer.Exit(code=1)

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

    # Create config directory structure
    (project_path / "config").mkdir(exist_ok=True)

    # Set up Jinja2 environment
    env = Environment(
        loader=PackageLoader("fascraft", "templates/new_project"),
        autoescape=select_autoescape(),
    )

    # Define templates to render
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
    ]

    # Render all templates
    for template_name, output_name in templates:
        template = env.get_template(template_name)
        content = template.render(
            project_name=project_name, author_name="Lutor Iyornumbe"
        )
        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Successfully created new project ", style="bold white")
    success_text.append(f"'{project_name}' ", style="bold cyan")
    success_text.append("at ", style="white")
    success_text.append(f"{project_path}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    next_steps_text = Text()
    next_steps_text.append("⚡ ", style="bold yellow")
    next_steps_text.append("Run ", style="white")
    next_steps_text.append(f"'cd {project_name} && pip install -r requirements.txt' ", style="bold cyan")
    next_steps_text.append("to get started.", style="white")
    console.print(next_steps_text)

    dev_deps_text = Text()
    dev_deps_text.append("🛠️ ", style="bold blue")
    dev_deps_text.append("For development, run: ", style="white")
    dev_deps_text.append("'pip install -r requirements.dev.txt'", style="bold cyan")
    console.print(dev_deps_text)

    config_info_text = Text()
    config_info_text.append("🔧 ", style="bold blue")
    config_info_text.append("Project includes configuration: ", style="white")
    config_info_text.append("config/settings.py, config/database.py", style="bold cyan")
    console.print(config_info_text)

    env_info_text = Text()
    env_info_text.append("🌍 ", style="bold green")
    env_info_text.append("Environment files created: ", style="white")
    env_info_text.append(".env, .env.sample", style="bold cyan")
    console.print(env_info_text)

    deps_info_text = Text()
    deps_info_text.append("📦 ", style="bold yellow")
    deps_info_text.append("Dependency files created: ", style="white")
    deps_info_text.append("requirements.txt, requirements.dev.txt, requirements.prod.txt", style="bold cyan")
    console.print(deps_info_text)

    db_setup_text = Text()
    db_setup_text.append("🗄️ ", style="bold green")
    db_setup_text.append("Database setup: ", style="white")
    db_setup_text.append("Run 'alembic init alembic' to initialize migrations", style="bold cyan")
    console.print(db_setup_text)

    db_config_text = Text()
    db_config_text.append("⚙️ ", style="bold blue")
    db_config_text.append("Configure alembic/env.py to import your models and use your database URL", style="white")
    console.print(db_config_text)

    generate_info_text = Text()
    generate_info_text.append("✨ ", style="bold yellow")
    generate_info_text.append("Use ", style="white")
    generate_info_text.append("'fascraft generate <module_name>' ", style="bold cyan")
    generate_info_text.append("to add new domain modules.", style="white")
    console.print(generate_info_text)

    readme_text = Text()
    readme_text.append("📖 ", style="bold yellow")
    readme_text.append("See README.md for detailed database setup and migration instructions", style="white")
    console.print(readme_text)
