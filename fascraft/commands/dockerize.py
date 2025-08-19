"""Command for adding Docker support to existing FastAPI projects."""

from pathlib import Path

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from fascraft.exceptions import FasCraftError, FileSystemError, TemplateRenderError
from fascraft.validation import validate_path_robust

# Initialize rich console
console = Console(width=None, soft_wrap=False)

app = typer.Typer(help="🐳 Add Docker support to existing FastAPI projects")


@app.command()
def add_docker(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    force: bool = typer.Option(
        False, "--force", "-f", help="🔄 Overwrite existing Docker files"
    ),
) -> None:
    """🐳 Add Docker support to an existing FastAPI project."""
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

        # Check for existing Docker files
        docker_files = [
            project_path / "Dockerfile",
            project_path / "docker-compose.yml",
            project_path / ".dockerignore",
        ]

        existing_files = [f for f in docker_files if f.exists()]

        if existing_files and not force:
            console.print(
                f"⚠️  Docker files already exist: {', '.join(f.name for f in existing_files)}",
                style="bold yellow",
            )
            console.print("Use --force to overwrite existing files", style="yellow")
            raise typer.Exit(code=1)

        # Add Docker support
        add_docker_support(project_path, force)

        # Display success message
        display_success_message(project_path)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def add_docker_support(project_path: Path, force: bool) -> None:
    """Add Docker support to the project."""
    try:
        # Get project name from directory
        project_name = project_path.name

        # Create database directory if it doesn't exist
        database_dir = project_path / "database"
        database_dir.mkdir(exist_ok=True)

        # Setup Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Docker templates to render
        docker_templates = [
            ("Dockerfile.jinja2", "Dockerfile"),
            ("docker-compose.yml.jinja2", "docker-compose.yml"),
            (".dockerignore.jinja2", ".dockerignore"),
            ("database/init.sql.jinja2", "database/init.sql"),
        ]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Adding Docker support...", total=len(docker_templates)
            )

            for template_name, output_name in docker_templates:
                try:
                    render_docker_template(
                        env, project_path, project_name, template_name, output_name
                    )
                    progress.advance(task)
                except Exception as e:
                    progress.stop()
                    raise TemplateRenderError(template_name, str(e)) from e

        console.print("🐳 Docker support added successfully!", style="bold green")

    except Exception as e:
        raise FileSystemError(f"Failed to add Docker support: {str(e)}") from e


def render_docker_template(
    env: Environment,
    project_path: Path,
    project_name: str,
    template_name: str,
    output_name: str,
) -> None:
    """Render a single Docker template."""
    try:
        template = env.get_template(template_name)
        content = template.render(project_name=project_name)

        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        raise TemplateRenderError(template_name, str(e)) from e


def display_success_message(project_path: Path) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Docker support added to ", style="bold white")
    success_text.append(f"{project_path.name}", style="bold cyan")
    success_text.append(" successfully!", style="white")
    console.print(success_text)

    # Display next steps
    next_steps_text = Text()
    next_steps_text.append("🚀 ", style="bold blue")
    next_steps_text.append("Next steps:", style="bold white")
    console.print(next_steps_text)

    docker_text = Text()
    docker_text.append("  🐳 ", style="bold blue")
    docker_text.append("Build and run: ", style="white")
    docker_text.append("'docker-compose up --build'", style="bold cyan")
    console.print(docker_text)

    docker_prod_text = Text()
    docker_prod_text.append("  🚀 ", style="bold blue")
    docker_prod_text.append("Production: ", style="white")
    docker_prod_text.append(
        "'docker-compose --profile production up --build'", style="bold cyan"
    )
    console.print(docker_prod_text)


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
