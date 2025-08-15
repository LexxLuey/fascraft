"""Main FastCraft CLI application."""

import typer
from rich.console import Console
from rich.text import Text

from fastcraft.commands import generate as generate_cmd
from fastcraft.commands import list as list_cmd
from fastcraft.commands import new
from fastcraft.commands import remove as remove_cmd
from fastcraft.commands import update as update_cmd

# Initialize rich console
console = Console()

app = typer.Typer(
    help="FastCraft CLI for generating modular FastAPI projects.",
    name="fastcraft"
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
    welcome_text = Text()
    welcome_text.append("👋 ", style="bold blue")
    welcome_text.append(f"Hello {name}!", style="bold white")
    console.print(welcome_text)
    
    fastcraft_text = Text()
    fastcraft_text.append("🚀 ", style="bold green")
    fastcraft_text.append("Welcome to ", style="white")
    fastcraft_text.append("FastCraft", style="bold cyan")
    fastcraft_text.append("!", style="white")
    console.print(fastcraft_text)


@app.command()
def version():
    """Show FastCraft version."""
    version_text = Text()
    version_text.append("📦 ", style="bold yellow")
    version_text.append("FastCraft ", style="bold cyan")
    version_text.append("version ", style="white")
    version_text.append("0.1.0", style="bold green")
    console.print(version_text)


if __name__ == "__main__":
    app()
