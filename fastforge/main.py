"""Main FastForge CLI application."""

import typer

from fastforge.commands import generate as generate_cmd
from fastforge.commands import list as list_cmd
from fastforge.commands import new
from fastforge.commands import remove as remove_cmd
from fastforge.commands import update as update_cmd

app = typer.Typer(
    help="FastForge CLI for generating modular FastAPI projects.",
    name="fastforge"
)

# Register commands
app.command(name="new")(new.create_new_project)
app.command(name="generate")(generate_cmd.generate_module)
app.command(name="list")(list_cmd.list_modules)
app.command(name="remove")(remove_cmd.remove_module)
app.command(name="update")(update_cmd.update_module)


@app.command()
def hello(name: str = typer.Argument("World", help="Name to greet")):
    """Say hello to someone."""
    typer.echo(f"Hello {name}!")
    typer.echo("Welcome to FastForge!")


@app.command()
def version():
    """Show FastForge version."""
    typer.echo("FastForge version 0.1.0")


if __name__ == "__main__":
    app()
