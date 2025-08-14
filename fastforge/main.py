"""Main CLI application for FastForge."""

import typer
from rich.console import Console
from rich.text import Text

from fastforge.commands import new as new_cmd

# Initialize rich console
console = Console()

app = typer.Typer(
    help="🚀 FastForge CLI for generating modular FastAPI projects.", rich_markup_mode=None
)


@app.command()
def hello(name: str = "World"):
    """👋 Say hello to the user."""
    welcome_text = Text()
    welcome_text.append("👋 ", style="bold blue")
    welcome_text.append(f"Hello {name}! ", style="bold white")
    welcome_text.append("Welcome to FastForge!", style="bold cyan")
    console.print(welcome_text)


@app.command()
def version():
    """📦 Show the current version of FastForge."""
    from fastforge import __version__

    version_text = Text()
    version_text.append("📦 ", style="bold green")
    version_text.append("FastForge version ", style="bold white")
    version_text.append(f"{__version__}", style="bold yellow")
    console.print(version_text)


app.command(name="new")(new_cmd.create_new_project)

if __name__ == "__main__":
    app()
