"""Command for adding CI/CD support to existing FastAPI projects."""

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

app = typer.Typer(help="🚀 Add CI/CD support to existing FastAPI projects")


@app.command()
def add_ci_cd(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    platform: str = typer.Option(
        "github", "--platform", "-p", help="CI/CD platform: github, gitlab, or both"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="🔄 Overwrite existing CI/CD files"
    ),
) -> None:
    """🚀 Add CI/CD support to an existing FastAPI project."""
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

        # Validate platform choice
        if platform not in ["github", "gitlab", "both"]:
            raise FileSystemError(
                f"Invalid platform: {platform}. Choose from: github, gitlab, both"
            )

        # Check for existing CI/CD files
        existing_files = check_existing_ci_cd_files(project_path, platform)

        if existing_files and not force:
            console.print(
                f"⚠️  CI/CD files already exist: {', '.join(existing_files)}",
                style="bold yellow",
            )
            console.print("Use --force to overwrite existing files", style="yellow")
            raise typer.Exit(code=1)

        # Add CI/CD support
        add_ci_cd_support(project_path, platform, force)

        # Display success message
        display_success_message(project_path, platform)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def check_existing_ci_cd_files(project_path: Path, platform: str) -> list:
    """Check for existing CI/CD files."""
    existing_files = []

    if platform in ["github", "both"]:
        github_dir = project_path / ".github" / "workflows"
        if github_dir.exists():
            for workflow_file in github_dir.glob("*.yml"):
                existing_files.append(f".github/workflows/{workflow_file.name}")

    if platform in ["gitlab", "both"]:
        gitlab_file = project_path / ".gitlab-ci.yml"
        if gitlab_file.exists():
            existing_files.append(".gitlab-ci.yml")

    pre_commit_file = project_path / ".pre-commit-config.yaml"
    if pre_commit_file.exists():
        existing_files.append(".pre-commit-config.yaml")

    return existing_files


def add_ci_cd_support(project_path: Path, platform: str, force: bool) -> None:
    """Add CI/CD support to the project."""
    try:
        # Get project name from directory
        project_name = project_path.name

        # Setup Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # CI/CD templates to render
        ci_cd_templates = []

        if platform in ["github", "both"]:
            ci_cd_templates.extend(
                [
                    (".github/workflows/ci.yml.jinja2", ".github/workflows/ci.yml"),
                    (
                        ".github/workflows/dependency-update.yml.jinja2",
                        ".github/workflows/dependency-update.yml",
                    ),
                ]
            )

        if platform in ["gitlab", "both"]:
            ci_cd_templates.append((".gitlab-ci.yml.jinja2", ".gitlab-ci.yml"))

        ci_cd_templates.append(
            (".pre-commit-config.yaml.jinja2", ".pre-commit-config.yaml")
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Adding CI/CD support...", total=len(ci_cd_templates)
            )

            for template_name, output_name in ci_cd_templates:
                try:
                    render_ci_cd_template(
                        env, project_path, project_name, template_name, output_name
                    )
                    progress.advance(task)
                except Exception as e:
                    progress.stop()
                    raise TemplateRenderError(template_name, str(e)) from e

        console.print("🚀 CI/CD support added successfully!", style="bold green")

    except Exception as e:
        raise FileSystemError(f"Failed to add CI/CD support: {str(e)}") from e


def render_ci_cd_template(
    env: Environment,
    project_path: Path,
    project_name: str,
    template_name: str,
    output_name: str,
) -> None:
    """Render a single CI/CD template."""
    try:
        template = env.get_template(template_name)
        content = template.render(project_name=project_name)

        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        raise TemplateRenderError(template_name, str(e)) from e


def display_success_message(project_path: Path, platform: str) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("CI/CD support added to ", style="bold white")
    success_text.append(f"{project_path.name}", style="bold cyan")
    success_text.append(" successfully!", style="white")
    console.print(success_text)

    # Display platform-specific information
    platform_text = Text()
    platform_text.append("🚀 ", style="bold blue")
    platform_text.append("Platform: ", style="bold white")
    platform_text.append(platform.upper(), style="bold cyan")
    console.print(platform_text)

    # Display next steps
    next_steps_text = Text()
    next_steps_text.append("📋 ", style="bold blue")
    next_steps_text.append("Next steps:", style="bold white")
    console.print(next_steps_text)

    if platform in ["github", "both"]:
        github_text = Text()
        github_text.append("  🔗 ", style="bold blue")
        github_text.append("GitHub Actions: ", style="white")
        github_text.append(
            "Push to main/develop branches to trigger workflows", style="bold cyan"
        )
        console.print(github_text)

    if platform in ["gitlab", "both"]:
        gitlab_text = Text()
        gitlab_text.append("  🔗 ", style="bold blue")
        gitlab_text.append("GitLab CI: ", style="white")
        gitlab_text.append("Push to trigger CI/CD pipeline", style="bold cyan")
        console.print(gitlab_text)

    pre_commit_text = Text()
    pre_commit_text.append("  🔧 ", style="bold blue")
    pre_commit_text.append("Pre-commit hooks: ", style="white")
    pre_commit_text.append("'pre-commit install' to enable", style="bold cyan")
    console.print(pre_commit_text)

    setup_text = Text()
    setup_text.append("  ⚙️ ", style="bold blue")
    setup_text.append("Setup: ", style="white")
    setup_text.append(
        "'fascraft ci-cd setup' to configure environments", style="bold cyan"
    )
    console.print(setup_text)


@app.command()
def setup(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
) -> None:
    """⚙️ Setup CI/CD environments and configurations."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Setup CI/CD environments
        setup_ci_cd_environments(project_path)

        # Display setup instructions
        display_setup_instructions(project_path)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def setup_ci_cd_environments(project_path: Path) -> None:
    """Setup CI/CD environments and configurations."""
    try:
        console.print("⚙️ Setting up CI/CD environments...", style="bold blue")

        # Create environment configuration files
        create_environment_configs(project_path)

        # Setup pre-commit hooks
        setup_pre_commit_hooks(project_path)

        console.print(
            "✅ CI/CD environments configured successfully!", style="bold green"
        )

    except Exception as e:
        raise FileSystemError(f"Failed to setup CI/CD environments: {str(e)}") from e


def create_environment_configs(project_path: Path) -> None:
    """Create environment configuration files."""
    # Create .env files for different environments
    env_files = {
        ".env.dev": "ENVIRONMENT=development\nDEBUG=true\nLOG_LEVEL=DEBUG",
        ".env.staging": "ENVIRONMENT=staging\nDEBUG=false\nLOG_LEVEL=INFO",
        ".env.prod": "ENVIRONMENT=production\nDEBUG=false\nLOG_LEVEL=WARNING",
    }

    for filename, content in env_files.items():
        env_file = project_path / filename
        if not env_file.exists():
            env_file.write_text(content)
            console.print(f"📝 Created {filename}", style="green")


def setup_pre_commit_hooks(project_path: Path) -> None:
    """Setup pre-commit hooks."""
    pre_commit_file = project_path / ".pre-commit-config.yaml"
    if pre_commit_file.exists():
        console.print("🔧 Pre-commit hooks configuration found", style="green")
        console.print("   Run 'pre-commit install' to enable hooks", style="yellow")


def display_setup_instructions(project_path: Path) -> None:
    """Display setup instructions."""
    instructions_text = Text()
    instructions_text.append("📚 ", style="bold blue")
    instructions_text.append("Setup Instructions:", style="bold white")
    console.print(instructions_text)

    # GitHub Actions setup
    github_dir = project_path / ".github" / "workflows"
    if github_dir.exists():
        github_text = Text()
        github_text.append("  🔗 ", style="bold blue")
        github_text.append("GitHub Actions: ", style="white")
        github_text.append("Workflows are ready to use", style="bold cyan")
        console.print(github_text)

    # GitLab CI setup
    gitlab_file = project_path / ".gitlab-ci.yml"
    if gitlab_file.exists():
        gitlab_text = Text()
        gitlab_text.append("  🔗 ", style="bold blue")
        gitlab_text.append("GitLab CI: ", style="white")
        gitlab_text.append("Pipeline configuration ready", style="bold cyan")
        console.print(gitlab_text)

    # Pre-commit setup
    pre_commit_text = Text()
    pre_commit_text.append("  🔧 ", style="bold blue")
    pre_commit_text.append("Pre-commit: ", style="white")
    pre_commit_text.append(
        "Run 'pre-commit install' to enable hooks", style="bold cyan"
    )
    console.print(pre_commit_text)


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
