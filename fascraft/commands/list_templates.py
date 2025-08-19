"""Command for listing available module templates."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from fascraft.template_registry import template_registry

# Initialize rich console
console = Console()


def list_templates(
    category: str | None = typer.Option(None, help="Filter templates by category"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed template information"
    ),
) -> None:
    """📋 List available module templates with their metadata and descriptions."""

    try:
        # Get templates, optionally filtered by category
        templates = template_registry.list_templates(category=category)

        if not templates:
            if category:
                console.print(
                    f"❌ No templates found in category '{category}'", style="bold red"
                )
            else:
                console.print("❌ No templates available", style="bold red")
            return

        # Create table for template listing
        table = Table(title="🎨 Available Module Templates")
        table.add_column("Template", style="cyan", no_wrap=True)
        table.add_column("Display Name", style="white", no_wrap=True)
        table.add_column("Category", style="green", no_wrap=True)
        table.add_column("Complexity", style="yellow", no_wrap=True)
        table.add_column("Description", style="white")

        # Add template rows
        for template in templates:
            complexity_color = {
                "basic": "green",
                "intermediate": "yellow",
                "advanced": "red",
            }.get(template.complexity, "white")

            table.add_row(
                template.name,
                template.display_name,
                template.category,
                f"[{complexity_color}]{template.complexity}[/{complexity_color}]",
                template.description,
            )

        # Display the table
        console.print(table)

        # Show category information
        if not category:
            categories = template_registry.get_template_categories()
            category_text = Text()
            category_text.append("📂 Template Categories: ", style="bold blue")
            category_text.append(", ".join(categories), style="cyan")
            console.print(category_text)

        # Show usage information
        usage_text = Text()
        usage_text.append("💡 Usage: ", style="bold green")
        usage_text.append(
            "fascraft generate <module_name> --template <template_name>", style="cyan"
        )
        console.print(usage_text)

        # Show verbose information if requested
        if verbose:
            console.print("\n" + "=" * 80)
            console.print("🔍 Detailed Template Information", style="bold blue")

            for template in templates:
                # Create detailed panel for each template
                dependencies_text = (
                    ", ".join(template.dependencies)
                    if template.dependencies
                    else "None"
                )

                panel_content = f"""
Template: {template.name}
Display Name: {template.display_name}
Category: {template.category}
Complexity: {template.complexity}
Description: {template.description}
Dependencies: {dependencies_text}
Template Path: {template.template_path}
Preview Available: {'Yes' if template.preview_available else 'No'}
                """.strip()

                panel = Panel(
                    panel_content,
                    title=f"🎨 {template.display_name}",
                    border_style="blue",
                )
                console.print(panel)

        # Show template selection tips
        tips_text = Text()
        tips_text.append("💡 Template Selection Tips:", style="bold yellow")
        tips_text.append("\n• ", style="white")
        tips_text.append("basic", style="cyan")
        tips_text.append(": Simple CRUD operations, good for learning", style="white")
        tips_text.append("\n• ", style="white")
        tips_text.append("crud", style="cyan")
        tips_text.append(": Enhanced CRUD with advanced features", style="white")
        tips_text.append("\n• ", style="cyan")
        tips_text.append("api_first", style="cyan")
        tips_text.append(
            ": API-centric design with comprehensive documentation", style="white"
        )
        tips_text.append("\n• ", style="cyan")
        tips_text.append("event_driven", style="cyan")
        tips_text.append(
            ": Event-driven architecture with async support", style="white"
        )
        tips_text.append("\n• ", style="cyan")
        tips_text.append("microservice", style="cyan")
        tips_text.append(": Lightweight, focused modules", style="white")
        tips_text.append("\n• ", style="cyan")
        tips_text.append("admin_panel", style="cyan")
        tips_text.append(": Administrative interface with RBAC", style="white")

        console.print(tips_text)

    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Failed to list templates: {str(e)}", style="white")
        console.print(error_text)
        raise typer.Exit(code=1) from e
