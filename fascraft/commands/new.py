"""Command for creating a new FastAPI project."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from fascraft.exceptions import (
    CorruptedTemplateError,
    DiskSpaceError,
    FasCraftError,
    FileSystemError,
    PermissionError,
    TemplateError,
    TemplateNotFoundError,
    TemplateRenderError,
    ValidationError,
)
from fascraft.validation import (
    validate_disk_space,
    validate_file_system_writable,
    validate_path_robust,
    validate_project_name,
    validate_project_path,
)

# Initialize rich console
console = Console(width=None, soft_wrap=False)


def create_new_project(
    project_name: Optional[str] = typer.Argument(
        None, help="🏗️ The name of the new FastAPI project"
    ),
    path: str = typer.Option(
        ".", help="📁 The path where the new project directory will be created"
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="🎯 Enable interactive mode for guided setup"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d", help="🔍 Preview changes without applying them"
    ),
    confirm: bool = typer.Option(
        False, "--confirm", "-y", help="✅ Skip confirmation prompts"
    ),
) -> None:
    """🏗️ Generates a new FastAPI project with interactive guidance."""
    try:
        # Interactive mode or use provided arguments
        if interactive or project_name is None:
            project_name, path = interactive_project_setup()
        else:
            project_name = project_name
            path = path

        # Validate inputs with robust validation
        validated_project_name = validate_project_name(project_name)
        validated_path = validate_path_robust(path)
        project_path = validated_path / validated_project_name

        # Validate project path
        validate_project_path(project_path, validated_project_name)

        # Show project summary and confirm
        if not confirm and not dry_run:
            if not confirm_project_creation(project_path, validated_project_name):
                console.print("❌ Project creation cancelled.", style="bold red")
                raise typer.Exit(code=0)

        # Dry run mode
        if dry_run:
            perform_dry_run(project_path, validated_project_name)
            return

        # Create project with rollback capability
        create_project_with_rollback(project_path, validated_project_name)

        # Display success message and next steps
        display_success_message(project_path, validated_project_name)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def interactive_project_setup() -> tuple:
    """Interactive setup for project creation."""
    console.print("\n🎯 [bold blue]FasCraft Interactive Project Setup[/bold blue]")
    console.print("Let's create your FastAPI project step by step!\n")

    # Project name
    project_name = Prompt.ask(
        "📝 [bold cyan]Project Name[/bold cyan]",
        default="my-fastapi-app",
        show_default=True
    )
    
    # Validate project name
    try:
        validate_project_name(project_name)
    except FasCraftError as e:
        console.print(f"❌ Invalid project name: {e.message}", style="red")
        project_name = Prompt.ask(
            "📝 [bold cyan]Project Name[/bold cyan] (use only letters, numbers, hyphens, underscores)",
            default="my-fastapi-app"
        )

    # Project path
    path = Prompt.ask(
        "📁 [bold cyan]Project Path[/bold cyan]",
        default=".",
        show_default=True
    )

    # Project type selection
    project_type = Prompt.ask(
        "🏗️ [bold cyan]Project Type[/bold cyan]",
        choices=["basic", "ecommerce", "auth", "database", "custom"],
        default="basic",
        show_default=True
    )

    # Additional features
    features = []
    if Confirm.ask("🐳 [bold cyan]Include Docker support?[/bold cyan]", default=True):
        features.append("docker")
    
    if Confirm.ask("🚀 [bold cyan]Include CI/CD workflows?[/bold cyan]", default=True):
        features.append("ci-cd")
    
    if Confirm.ask("🗄️ [bold cyan]Include database configuration?[/bold cyan]", default=True):
        features.append("database")
    
    if Confirm.ask("🧪 [bold cyan]Include testing setup?[/bold cyan]", default=True):
        features.append("testing")

    # Show summary
    display_interactive_summary(project_name, path, project_type, features)

    return project_name, path


def display_interactive_summary(project_name: str, path: str, project_type: str, features: list):
    """Display summary of interactive choices."""
    console.print("\n📋 [bold green]Project Setup Summary[/bold green]")
    
    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Setting", style="cyan")
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("Project Name", project_name)
    summary_table.add_row("Project Path", path)
    summary_table.add_row("Project Type", project_type)
    summary_table.add_row("Features", ", ".join(features) if features else "None")
    
    console.print(summary_table)
    
    if not Confirm.ask("\n✅ [bold green]Proceed with these settings?[/bold green]", default=True):
        raise typer.Exit(code=0)


def confirm_project_creation(project_path: Path, project_name: str) -> bool:
    """Confirm project creation with user."""
    console.print("\n🔍 [bold yellow]Project Creation Summary[/bold yellow]")
    
    # Check if directory exists
    if project_path.exists():
        console.print(f"⚠️ [bold red]Warning: Directory '{project_path}' already exists![/bold red]")
        if not Confirm.ask("🗑️ [bold red]This will overwrite existing content. Continue?[/bold red]", default=False):
            return False
    
    # Show what will be created
    creation_table = Table(show_header=True, header_style="bold blue")
    creation_table.add_column("Component", style="cyan")
    creation_table.add_column("Description", style="white")
    
    creation_table.add_row("📁 Project Structure", "config/, routers/, .github/")
    creation_table.add_row("🐍 Python Files", "main.py, __init__.py, settings.py")
    creation_table.add_row("📦 Dependencies", "requirements.txt, requirements.dev.txt")
    creation_table.add_row("🐳 Docker", "Dockerfile, docker-compose.yml")
    creation_table.add_row("🚀 CI/CD", "GitHub Actions, GitLab CI")
    creation_table.add_row("📝 Documentation", "README.md, .env.sample")
    
    console.print(creation_table)
    
    # Show disk space info
    try:
        import shutil
        total, used, free = shutil.disk_usage(project_path.parent)
        free_gb = free // (1024**3)
        console.print(f"💾 [bold blue]Available disk space: {free_gb} GB[/bold blue]")
    except:
        pass
    
    return Confirm.ask("\n✅ [bold green]Create project with these settings?[/bold green]", default=True)


def perform_dry_run(project_path: Path, project_name: str) -> None:
    """Perform dry run to preview changes."""
    console.print("\n🔍 [bold blue]DRY RUN MODE - No changes will be made[/bold blue]")
    
    # Show what would be created
    console.print(f"\n📁 [bold cyan]Project would be created at:[/bold cyan] {project_path}")
    
    # Show directory structure
    console.print("\n📂 [bold cyan]Directory structure that would be created:[/bold cyan]")
    structure_tree = f"""
{project_name}/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── database.py
│   ├── exceptions.py
│   └── middleware.py
├── routers/
│   ├── __init__.py
│   └── base.py
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── dependency-update.yml
├── main.py
├── requirements.txt
├── requirements.dev.txt
├── requirements.prod.txt
├── Dockerfile
├── docker-compose.yml
├── fascraft.toml
├── .gitignore
└── README.md
"""
    console.print(Syntax(structure_tree, "text", theme="monokai"))
    
    # Show template previews
    console.print("\n📄 [bold cyan]Key files that would be generated:[/bold cyan]")
    
    # Preview main.py
    try:
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )
        template = env.get_template("main.py.jinja2")
        main_content = template.render(project_name=project_name, author_name="Lutor Iyornumbe")
        
        preview_panel = Panel(
            Syntax(main_content[:500] + "..." if len(main_content) > 500 else main_content, 
                   "python", theme="monokai"),
            title="main.py preview",
            border_style="blue"
        )
        console.print(preview_panel)
    except Exception as e:
        console.print(f"⚠️ Could not preview main.py: {e}", style="yellow")
    
    # Show next steps
    console.print("\n🚀 [bold green]To create the project, run:[/bold green]")
    console.print(f"  fascraft new {project_name} --path {project_path.parent}", style="cyan")
    
    console.print("\n✨ [bold yellow]Dry run completed![/bold yellow]")


def create_project_structure(project_path: Path, project_name: str) -> None:
    """Create the basic project directory structure."""
    try:
        # Ensure project root exists
        project_path.mkdir(parents=True, exist_ok=True)

        # Create main directories (DDA approach - only essential folders)
        (project_path / "config").mkdir(parents=True, exist_ok=True)
        (project_path / "routers").mkdir(parents=True, exist_ok=True)
        
        # Create CI/CD directory structure
        (project_path / ".github" / "workflows").mkdir(parents=True, exist_ok=True)

        console.print("📁 Created project directory structure", style="bold green")

    except OSError as e:
        if e.errno == 13:  # Permission denied
            raise PermissionError(str(project_path), "create directories") from e
        elif e.errno == 28:  # No space left on device
            raise DiskSpaceError("Unknown", "Unknown") from e
        else:
            raise FileSystemError(
                f"Failed to create project structure: {str(e)}"
            ) from e


def render_project_templates_with_progress(
    project_path: Path, project_name: str
) -> None:
    """Render all project templates with progress tracking."""
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
        (".gitignore.jinja2", ".gitignore"),
        ("routers/__init__.py.jinja2", "routers/__init__.py"),
        ("routers/base.py.jinja2", "routers/base.py"),
        ("fascraft.toml.jinja2", "fascraft.toml"),
        # Docker templates
        ("Dockerfile.jinja2", "Dockerfile"),
        ("docker-compose.yml.jinja2", "docker-compose.yml"),
        (".dockerignore.jinja2", ".dockerignore"),
        ("database/init.sql.jinja2", "database/init.sql"),
        # CI/CD templates
        (".github/workflows/ci.yml.jinja2", ".github/workflows/ci.yml"),
        (
            ".github/workflows/dependency-update.yml.jinja2",
            ".github/workflows/dependency-update.yml",
        ),
        (".gitlab-ci.yml.jinja2", ".gitlab-ci.yml"),
        (".pre-commit-config.yaml.jinja2", ".pre-commit-config.yaml"),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Rendering templates...", total=len(templates))

        for template_name, output_name in templates:
            try:
                render_single_template(
                    project_path, project_name, template_name, output_name
                )
                progress.advance(task)
            except Exception as e:
                progress.stop()
                raise TemplateRenderError(template_name, str(e)) from e


def display_success_message(project_path: Path, project_name: str) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Successfully created new project ", style="bold white")
    success_text.append(f"'{project_name}' ", style="bold cyan")
    success_text.append("at ", style="white")
    success_text.append(f"{project_path}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    # Display next steps
    display_next_steps(project_path, project_name)

    # Display project features
    display_project_features()

    # Display best wishes
    display_best_wishes()


def display_next_steps(project_path: Path, project_name: str) -> None:
    """Display next steps for the user."""
    console.print("\n⚡ [bold yellow]Next Steps:[/bold yellow]")
    
    # Create a table for next steps
    steps_table = Table(show_header=True, header_style="bold green")
    steps_table.add_column("Step", style="cyan", width=20)
    steps_table.add_column("Command", style="white", width=40)
    steps_table.add_column("Description", style="white")
    
    steps_table.add_row(
        "1. Navigate", 
        f"cd {project_name}", 
        "Enter project directory"
    )
    steps_table.add_row(
        "2. Install Dependencies", 
        "pip install -r requirements.txt", 
        "Install production dependencies"
    )
    steps_table.add_row(
        "3. Install Dev Dependencies", 
        "pip install -r requirements.dev.txt", 
        "Install development tools"
    )
    steps_table.add_row(
        "4. Run Application", 
        "python main.py", 
        "Start the FastAPI server"
    )
    steps_table.add_row(
        "5. View API Docs", 
        "http://localhost:8000/docs", 
        "Interactive API documentation"
    )
    
    console.print(steps_table)
    
    # Additional guidance
    console.print("\n🛠️ [bold blue]Development Commands:[/bold blue]")
    console.print("  • [cyan]pytest[/cyan] - Run tests")
    console.print("  • [cyan]black .[/cyan] - Format code")
    console.print("  • [cyan]ruff check .[/cyan] - Lint code")
    
    console.print("\n🐳 [bold blue]Docker Commands:[/bold blue]")
    console.print("  • [cyan]docker-compose up --build[/cyan] - Run with Docker")
    console.print("  • [cyan]docker-compose --profile production up[/cyan] - Production mode")


def display_project_features() -> None:
    """Display information about project features."""
    console.print("\n🔧 [bold blue]Project Features:[/bold blue]")
    
    features_table = Table(show_header=True, header_style="bold blue")
    features_table.add_column("Feature", style="cyan", width=20)
    features_table.add_column("Description", style="white")
    
    features_table.add_row("🏗️ Architecture", "Domain-Driven Design (DDA) with clean structure")
    features_table.add_row("⚙️ Configuration", "Environment-based settings with Pydantic")
    features_table.add_row("🗄️ Database", "SQLAlchemy ORM with migration support")
    features_table.add_row("🔄 Routing", "Modular router system for scalability")
    features_table.add_row("🐳 Docker", "Multi-stage production-ready containers")
    features_table.add_row("🚀 CI/CD", "GitHub Actions, GitLab CI, pre-commit hooks")
    features_table.add_row("🧪 Testing", "Pytest setup with coverage support")
    features_table.add_row("📝 Documentation", "Auto-generated API docs with FastAPI")
    
    console.print(features_table)


def display_best_wishes() -> None:
    """Display encouraging best wishes message."""
    console.print("\n🚀 [bold green]Best wishes on your FastAPI journey![/bold green]")
    console.print("Your project is set up for success!", style="bold cyan")

    console.print("\n💡 [bold blue]Pro Tips:[/bold blue]")
    console.print("  • Use [cyan]fascraft generate <module>[/cyan] to add new features")
    console.print("  • Use [cyan]fascraft analyze[/cyan] to get project insights")
    console.print("  • Check [cyan]docs/[/cyan] for detailed guides")
    console.print("  • Join our community for support!")

    console.print("\n✨ [bold yellow]Happy coding![/bold yellow]")
    console.print("Your modular architecture will make future you very grateful!", style="bold cyan")


def display_error_message(error: FasCraftError) -> None:
    """Display user-friendly error message with recovery guidance."""
    error_text = Text(no_wrap=True)
    error_text.append("❌ ", style="bold red")
    error_text.append("Error: ", style="bold red")
    error_text.append(error.message, style="white")
    console.print(error_text, soft_wrap=False)

    if error.suggestion:
        suggestion_text = Text(no_wrap=True)
        suggestion_text.append("💡 ", style="bold yellow")
        suggestion_text.append("Suggestion: ", style="bold yellow")
        suggestion_text.append(error.suggestion, style="white")
        console.print(suggestion_text, soft_wrap=False)

    # Add specific error recovery guidance
    display_error_recovery_guidance(error)


def display_error_recovery_guidance(error: FasCraftError) -> None:
    """Display specific recovery guidance based on error type."""
    console.print("\n🔧 [bold blue]Error Recovery Guidance:[/bold blue]")
    
    if isinstance(error, PermissionError):
        display_permission_error_guidance()
    elif isinstance(error, DiskSpaceError):
        display_disk_space_error_guidance()
    elif isinstance(error, TemplateError):
        display_template_error_guidance()
    elif isinstance(error, ValidationError):
        display_validation_error_guidance()
    elif isinstance(error, FileSystemError):
        display_file_system_error_guidance()
    else:
        display_general_error_guidance()


def display_permission_error_guidance() -> None:
    """Display guidance for permission errors."""
    console.print("\n🔐 [bold yellow]Permission Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Check Path", 
        "Verify target directory permissions", 
        "Ensure you have write access"
    )
    guidance_table.add_row(
        "2. Run as Admin", 
        "Use administrator privileges", 
        "Right-click terminal → Run as Administrator"
    )
    guidance_table.add_row(
        "3. Change Location", 
        "Try different directory", 
        "Use --path ~/ or /tmp/ for testing"
    )
    guidance_table.add_row(
        "4. Check Antivirus", 
        "Disable antivirus temporarily", 
        "Some antivirus software blocks file operations"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry run fascraft new my-project --path ~/[/cyan]")


def display_disk_space_error_guidance() -> None:
    """Display guidance for disk space errors."""
    console.print("\n💾 [bold yellow]Disk Space Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Check Space", 
        "Verify available disk space", 
        "Run: df -h (Linux/Mac) or dir C:\\ (Windows)"
    )
    guidance_table.add_row(
        "2. Free Space", 
        "Remove unnecessary files", 
        "Clear temp files, downloads, recycle bin"
    )
    guidance_table.add_row(
        "3. Change Drive", 
        "Use different disk/partition", 
        "Try: --path D:\\projects\\ (Windows)"
    )
    guidance_table.add_row(
        "4. Clean System", 
        "Use disk cleanup tools", 
        "Windows: Disk Cleanup, Linux: apt autoremove"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry run fascraft new my-project --path D:\\projects\\[/cyan]")


def display_template_error_guidance() -> None:
    """Display guidance for template errors."""
    console.print("\n📄 [bold yellow]Template Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Reinstall", 
        "Reinstall FasCraft", 
        "pip uninstall fascraft && pip install fascraft"
    )
    guidance_table.add_row(
        "2. Clear Cache", 
        "Remove template cache", 
        "rm -rf ~/.fascraft/templates/"
    )
    guidance_table.add_row(
        "3. Check Version", 
        "Verify FasCraft version", 
        "poetry run fascraft --version"
    )
    guidance_table.add_row(
        "4. Report Issue", 
        "Create GitHub issue", 
        "Include error details and environment"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry install && poetry run fascraft new my-project[/cyan]")


def display_validation_error_guidance() -> None:
    """Display guidance for validation errors."""
    console.print("\n✅ [bold yellow]Validation Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Check Input", 
        "Verify project name", 
        "Use only letters, numbers, hyphens, underscores"
    )
    guidance_table.add_row(
        "2. Use Interactive", 
        "Try interactive mode", 
        "poetry run fascraft new --interactive"
    )
    guidance_table.add_row(
        "3. Check Path", 
        "Verify project path", 
        "Ensure path exists and is writable"
    )
    guidance_table.add_row(
        "4. Follow Naming", 
        "Use valid naming conventions", 
        "Examples: my-api, user-management, api_v1"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry run fascraft new --interactive[/cyan]")


def display_file_system_error_guidance() -> None:
    """Display guidance for file system errors."""
    console.print("\n📁 [bold yellow]File System Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Check Path", 
        "Verify directory exists", 
        "Create parent directory if needed"
    )
    guidance_table.add_row(
        "2. Check Permissions", 
        "Verify write permissions", 
        "Ensure you can create files in target location"
    )
    guidance_table.add_row(
        "3. Try Different Path", 
        "Use alternative location", 
        "Try home directory or temp folder"
    )
    guidance_table.add_row(
        "4. Check Disk Health", 
        "Verify disk integrity", 
        "Run disk check tools"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry run fascraft new my-project --path ~/[/cyan]")


def display_general_error_guidance() -> None:
    """Display general error recovery guidance."""
    console.print("\n🔍 [bold yellow]General Error - Recovery Steps:[/bold yellow]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Check Logs", 
        "Review error details", 
        "Look for specific error messages"
    )
    guidance_table.add_row(
        "2. Restart Terminal", 
        "Close and reopen terminal", 
        "Sometimes resolves environment issues"
    )
    guidance_table.add_row(
        "3. Update Dependencies", 
        "Update Python packages", 
        "poetry update && poetry install"
    )
    guidance_table.add_row(
        "4. Get Help", 
        "Check troubleshooting guide", 
        "docs/troubleshooting.md"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Quick Fix:[/bold blue]")
    console.print("  Try: [cyan]poetry update && poetry run fascraft new my-project[/cyan]")


def display_unexpected_error(error: Exception) -> None:
    """Display unexpected error message with recovery guidance."""
    error_text = Text()
    error_text.append("💥 ", style="bold red")
    error_text.append("Unexpected error: ", style="bold red")
    error_text.append(str(error), style="white")
    console.print(error_text)

    suggestion_text = Text()
    suggestion_text.append("🆘 ", style="bold yellow")
    suggestion_text.append(
        "This is unexpected. Please report this bug at: ", style="white"
    )
    suggestion_text.append(
        "https://github.com/LexxLuey/fascraft/issues", style="bold cyan"
    )
    console.print(suggestion_text)

    # Add recovery guidance for unexpected errors
    display_unexpected_error_guidance(error)


def display_unexpected_error_guidance(error: Exception) -> None:
    """Display guidance for unexpected errors."""
    console.print("\n🔧 [bold blue]Unexpected Error - Recovery Steps:[/bold blue]")
    
    guidance_table = Table(show_header=True, header_style="bold green")
    guidance_table.add_column("Step", style="cyan", width=15)
    guidance_table.add_column("Action", style="white", width=50)
    guidance_table.add_column("Details", style="white")
    
    guidance_table.add_row(
        "1. Report Bug", 
        "Create detailed issue report", 
        "Include error traceback and environment"
    )
    guidance_table.add_row(
        "2. Check Environment", 
        "Verify Python and dependencies", 
        "python --version && poetry --version"
    )
    guidance_table.add_row(
        "3. Try Clean Install", 
        "Remove and reinstall FasCraft", 
        "poetry remove fascraft && poetry add fascraft"
    )
    guidance_table.add_row(
        "4. Get Community Help", 
        "Ask in Discord or Discussions", 
        "Real-time support from community"
    )
    
    console.print(guidance_table)
    
    console.print("\n💡 [bold blue]Immediate Actions:[/bold blue]")
    console.print("  1. [cyan]Join Discord[/cyan]: https://discord.gg/fascraft")
    console.print("  2. [cyan]Check Issues[/cyan]: https://github.com/LexxLuey/fascraft/issues")
    console.print("  3. [cyan]Read Troubleshooting[/cyan]: docs/troubleshooting.md")


def create_project_with_rollback(project_path: Path, project_name: str) -> None:
    """Create project with automatic rollback on failure."""
    backup_path = None
    created_files = []

    try:
        # Validate file system and disk space before starting
        # Only validate if parent directory exists, otherwise we'll create it
        if project_path.parent.exists():
            validate_file_system_writable(project_path.parent)
            validate_disk_space(project_path.parent, required_space_mb=20)

        # Create backup of existing directory if it exists
        if project_path.exists():
            backup_path = create_backup_directory(project_path)

        # Create project structure
        create_project_structure(project_path, project_name)
        created_files.append("structure")

        # Render templates
        try:
            render_project_templates_with_progress(project_path, project_name)
            created_files.append("templates")
        except Exception as e:
            console.print(f"⚠️ Template rendering failed: {e}", style="yellow")
            console.print("Creating minimal project structure...", style="yellow")
            render_essential_templates(project_path, project_name)
            created_files.append("templates")

        # Validate generated project
        validate_generated_project(project_path)
        created_files.append("validation")

    except Exception as e:
        # Rollback on any failure
        console.print("🔄 Rolling back due to error...", style="bold yellow")
        rollback_project_creation(project_path, backup_path, created_files)
        raise e from e


def create_backup_directory(path: Path) -> Path:
    """Create backup of existing directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.name}_backup_{timestamp}"
    backup_path = path.parent / backup_name

    try:
        import shutil

        shutil.copytree(path, backup_path)
        console.print(f"💾 Created backup at: {backup_path}", style="green")
        return backup_path
    except Exception as e:
        console.print(f"⚠️ Warning: Failed to create backup: {e}", style="yellow")
        return None


def rollback_project_creation(
    project_path: Path, backup_path: Path, created_files: list
) -> None:
    """Rollback project creation on failure."""
    try:
        # Remove created project directory
        if project_path.exists():
            import shutil

            shutil.rmtree(project_path)
            console.print("🗑️ Removed failed project directory", style="yellow")

        # Restore from backup if available
        if backup_path and backup_path.exists():
            import shutil

            shutil.copytree(backup_path, project_path)
            console.print("🔄 Restored from backup", style="green")

    except Exception as e:
        console.print(f"⚠️ Warning: Rollback failed: {e}", style="yellow")
        console.print("Manual cleanup may be required", style="red")


def create_project_with_graceful_degradation(
    project_path: Path, project_name: str
) -> None:
    """Create project with graceful degradation for partial failures."""
    warnings = []

    try:
        # Create project structure
        try:
            create_project_structure(project_path, project_name)
        except Exception as e:
            warnings.append(f"Failed to create complete structure: {e}")
            create_minimal_structure(project_path, project_name)

        # Render templates
        try:
            render_project_templates_with_progress(project_path, project_name)
        except Exception as e:
            warnings.append(f"Failed to render some templates: {e}")
            render_essential_templates(project_path, project_name)

        # Display warnings if any
        if warnings:
            display_partial_success_warnings(warnings)

    except Exception as e:
        # If even minimal setup fails, rollback
        rollback_project_creation(project_path, None, [])
        raise e


def create_minimal_structure(project_path: Path, project_name: str) -> None:
    """Create minimal project structure when full structure fails."""
    try:
        (project_path / "main.py").parent.mkdir(parents=True, exist_ok=True)
        console.print("⚠️ Created minimal project structure", style="yellow")
    except Exception as e:
        raise FileSystemError(
            f"Failed to create even minimal structure: {str(e)}"
        ) from e


def render_essential_templates(project_path: Path, project_name: str) -> None:
    """Render only essential templates when full rendering fails."""
    essential_templates = [
        ("main.py.jinja2", "main.py"),
        ("pyproject.toml.jinja2", "pyproject.toml"),
        ("requirements.txt.jinja2", "requirements.txt"),
        ("__init__.py.jinja2", "__init__.py"),
        ("config/__init__.py.jinja2", "config/__init__.py"),
        ("config/settings.py.jinja2", "config/settings.py"),
        ("routers/__init__.py.jinja2", "routers/__init__.py"),
        ("routers/base.py.jinja2", "routers/base.py"),
    ]

    for template_name, output_name in essential_templates:
        try:
            render_single_template(
                project_path, project_name, template_name, output_name
            )
        except Exception as e:
            console.print(f"⚠️ Failed to render {output_name}: {e}", style="yellow")


def display_partial_success_warnings(warnings: list) -> None:
    """Display warnings for partial failures."""
    console.print("\n⚠️ Project created with warnings:", style="bold yellow")
    for warning in warnings:
        console.print(f"  • {warning}", style="yellow")
    console.print("Some features may not work correctly", style="yellow")


def validate_generated_project(project_path: Path) -> None:
    """Validate that the generated project is valid."""
    essential_files = ["main.py", "pyproject.toml"]

    for file_name in essential_files:
        file_path = project_path / file_name
        if not file_path.exists():
            raise TemplateError(f"Essential file {file_name} was not generated")

        # Check if file has content
        try:
            content = file_path.read_text()
            if not content.strip():
                raise TemplateError(f"Generated file {file_name} is empty")
        except Exception as e:
            raise TemplateError(
                f"Failed to read generated file {file_name}: {str(e)}"
            ) from e


def render_single_template(
    project_path: Path, project_name: str, template_name: str, output_name: str
) -> None:
    """Render a single template file."""
    try:
        # Set up Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Load and render template
        template = env.get_template(template_name)
        content = template.render(
            project_name=project_name, author_name="Lutor Iyornumbe"
        )

        # Ensure output directory exists
        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write rendered content
        output_path.write_text(content, encoding="utf-8")

    except Exception as e:
        if "No such file or directory" in str(e):
            raise TemplateNotFoundError(template_name, "templates/new_project") from e
        elif "Template syntax error" in str(e) or "Template error" in str(e):
            raise CorruptedTemplateError(template_name, str(e)) from e
        else:
            raise TemplateRenderError(template_name, str(e)) from e
