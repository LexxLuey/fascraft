"""Main FasCraft CLI application."""

import typer
from rich.console import Console
from rich.text import Text

from fascraft.commands import (
    analyze,
    analyze_dependencies,
    ci_cd,
    config,
    dependencies,
    deploy,
    dockerize,
    docs,
    environment,
)
from fascraft.commands import generate as generate_cmd
from fascraft.commands import generate_test
from fascraft.commands import list as list_cmd
from fascraft.commands import list_templates, migrate, new
from fascraft.commands import remove as remove_cmd
from fascraft.commands import update as update_cmd

# Initialize rich console
console = Console()

app = typer.Typer(
    help="FasCraft CLI for generating modular FastAPI projects.", name="fascraft"
)

# Register commands
app.command(name="new")(new.create_new_project)
app.command(name="generate")(generate_cmd.generate_module)
app.command(name="list")(list_cmd.list_modules)
app.command(name="remove")(remove_cmd.remove_module)
app.command(name="update")(update_cmd.update_module)
app.command(name="analyze")(analyze.analyze_project)
app.command(name="migrate")(migrate.migrate_project)
app.command(name="config")(config.manage_config)
app.command(name="list-templates")(list_templates.list_templates)
app.command(name="analyze-dependencies")(analyze_dependencies.analyze_dependencies)
app.add_typer(dependencies.dependencies_app, name="dependencies")
app.command(name="test")(generate_test.generate_test)
app.command(name="testing-utils")(generate_test.testing_utils_help)
app.add_typer(docs.docs_app, name="docs")
app.command(name="dockerize")(dockerize.add_docker)
app.add_typer(ci_cd.app, name="ci-cd")
app.add_typer(deploy.app, name="deploy")
app.add_typer(environment.app, name="environment")


@app.command()
def hello(name: str = typer.Argument("World", help="Name to greet")):
    """Say hello to someone."""
    welcome_text = Text()
    welcome_text.append("👋 ", style="bold blue")
    welcome_text.append(f"Hello {name}!", style="bold white")
    console.print(welcome_text)

    fascraft_text = Text()
    fascraft_text.append("🚀 ", style="bold green")
    fascraft_text.append("Welcome to ", style="white")
    fascraft_text.append("FasCraft", style="bold cyan")
    fascraft_text.append("!", style="white")
    console.print(fascraft_text)


@app.command()
def version():
    """Show FasCraft version."""
    version_text = Text()
    version_text.append("📦 ", style="bold yellow")
    version_text.append("FasCraft ", style="bold cyan")
    version_text.append("version ", style="white")
    version_text.append("", style="bold green")
    console.print(version_text)


if __name__ == "__main__":
    app()
