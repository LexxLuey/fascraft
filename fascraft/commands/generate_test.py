"""Command for generating test files."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize rich console
console = Console()


def testing_utils_help() -> None:
    """Show help for testing utilities."""
    show_testing_utilities()


def generate_test(
    module_name: str,
    path: str = typer.Option(".", help="📁 The path to the existing FastAPI project"),
    strategy: str = typer.Option(
        "basic", help="🧪 Testing strategy (basic, integration, performance, all)"
    ),
    force: bool = typer.Option(
        False, "--force", help="💪 Overwrite existing test files"
    ),
) -> None:
    """🧪 Generate test files for a module."""

    path_obj = Path(path)
    if not path_obj.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Path '{path_obj}' does not exist.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if module exists
    module_path = path_obj / module_name
    if not module_path.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Module '{module_name}' not found at ", style="white")
        error_text.append(f"{module_path}", style="yellow")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Validate testing strategy
    valid_strategies = ["basic", "integration", "performance", "all"]
    if strategy not in valid_strategies:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Invalid testing strategy '{strategy}'. ", style="white")
        error_text.append(
            f"Valid options: {', '.join(valid_strategies)}", style="yellow"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Generate tests
    try:
        generated_files = generate_test_files(module_name, module_path, strategy, force)

        # Show success message
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append(
            f"Successfully generated test files for module '{module_name}'",
            style="bold white",
        )
        console.print(success_text)

        # Show generated files
        console.print("\n📁 Generated test files:", style="bold blue")
        for file_path in generated_files:
            console.print(f"  • {file_path}", style="cyan")

        # Show next steps
        console.print("\n💡 Next steps:", style="bold blue")
        console.print(
            f"  1. Install test dependencies: pip install -r {module_name}/tests/requirements-test.txt",
            style="white",
        )
        console.print(
            f"  2. Run tests: python {module_name}/tests/run_tests.py", style="white"
        )
        console.print("  3. Customize test logic as needed", style="white")

    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Failed to generate test files: {str(e)}", style="white")
        console.print(error_text)
        raise typer.Exit(code=1) from e


def generate_test_files(
    module_name: str, module_path: Path, strategy: str, force: bool
) -> list:
    """Generate test files based on the specified strategy."""
    generated_files = []

    # Create tests directory
    tests_dir = module_path / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Determine which test files to generate
    test_files = []

    if strategy in ["basic", "all"]:
        test_files.extend(
            [
                ("test_models.py.jinja2", "test_models.py"),
                ("__init__.py.jinja2", "__init__.py"),
            ]
        )

    if strategy in ["integration", "all"]:
        test_files.extend(
            [
                ("test_integration.py.jinja2", "test_integration.py"),
                ("conftest.py.jinja2", "conftest.py"),
            ]
        )

    if strategy in ["performance", "all"]:
        test_files.extend(
            [
                ("test_performance.py.jinja2", "test_performance.py"),
            ]
        )

    if strategy in ["all"]:
        test_files.extend(
            [
                ("run_tests.py.jinja2", "run_tests.py"),
                ("requirements-test.txt.jinja2", "requirements-test.txt"),
            ]
        )

    # Generate each test file
    for template_name, output_name in test_files:
        template_path = get_template_path(template_name)
        if template_path and template_path.exists():
            output_path = tests_dir / output_name

            # Check if file exists and force flag
            if output_path.exists() and not force:
                console.print(
                    f"⚠️  Skipping {output_name} (already exists, use --force to overwrite)",
                    style="yellow",
                )
                continue

            # Generate test file content
            content = generate_test_content(template_path, module_name)

            # Write test file
            output_path.write_text(content)
            generated_files.append(output_path)

            console.print(f"✅ Generated {output_name}", style="green")

    return generated_files


def get_template_path(template_name: str) -> Path | None:
    """Get the path to a test template file."""
    # Look for template in basic module templates first
    template_path = (
        Path("fascraft/templates/module_templates/basic/tests") / template_name
    )

    if template_path.exists():
        return template_path

    # If not found in basic, return None (will skip this file)
    return None


def generate_test_content(template_path: Path, module_name: str) -> str:
    """Generate test content from a Jinja2 template."""
    try:
        from jinja2 import Template

        # Read template content
        template_content = template_path.read_text()

        # Create Jinja2 template
        template = Template(template_content)

        # Render template with module context
        context = {
            "module_name": module_name,
            "module_name_plural": f"{module_name}s",
            "module_name_title": module_name.title(),
        }

        return template.render(**context)

    except ImportError:
        # Fallback: simple string replacement if Jinja2 is not available
        content = template_path.read_text()

        # Simple replacements
        replacements = {
            "{{ module_name }}": module_name,
            "{{ module_name_plural }}": f"{module_name}s",
            "{{ module_name_title }}": module_name.title(),
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        return content


def show_test_strategies() -> None:
    """Show available testing strategies."""
    strategies_panel = Panel(
        """🧪 Available Testing Strategies:

🔵 basic: Unit tests for models and basic functionality
🔵 integration: Integration tests with database and services
🔵 performance: Performance and load testing
🔵 all: Complete test suite with all strategies

💡 Usage: fascraft test generate <module_name> --strategy <strategy>
💡 Testing utilities available: fascraft testing-utils --help""",
        title="Test Generation Strategies",
        border_style="blue",
    )

    console.print(strategies_panel)


def show_testing_utilities() -> None:
    """Show available testing utilities."""
    utils_panel = Panel(
        """🛠️ Available Testing Utilities:

🔧 Database Fixtures: SQLite, PostgreSQL, MySQL configurations
🎭 Mock Data: Users, Products, Orders, Custom templates
📊 Coverage Reporting: Line, branch, and module coverage
⚡ Performance Monitoring: Duration, memory, CPU tracking
📋 Test Reports: JSON reports with comprehensive metrics

💡 Usage: Import from fascraft.testing_utils
💡 Quick start: from fascraft.testing_utils import create_test_utilities""",
        title="Testing Utilities",
        border_style="green",
    )

    console.print(utils_panel)
