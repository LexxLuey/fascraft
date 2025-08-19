"""Command for generating deployment scripts and templates."""

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

app = typer.Typer(
    help="🚀 Generate deployment scripts and templates for FastAPI projects"
)


@app.command()
def generate(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
    platform: str = typer.Option(
        "aws",
        "--platform",
        "-p",
        help="Deployment platform: aws, kubernetes, terraform, or all",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="🔄 Overwrite existing deployment files"
    ),
) -> None:
    """🚀 Generate deployment scripts and templates for a FastAPI project."""
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
        if platform not in ["aws", "kubernetes", "terraform", "all"]:
            raise FileSystemError(
                f"Invalid platform: {platform}. Choose from: aws, kubernetes, terraform, all"
            )

        # Check for existing deployment files
        existing_files = check_existing_deployment_files(project_path, platform)

        if existing_files and not force:
            console.print(
                f"⚠️  Deployment files already exist: {', '.join(existing_files)}",
                style="bold yellow",
            )
            console.print("Use --force to overwrite existing files", style="yellow")
            raise typer.Exit(code=1)

        # Generate deployment files
        generate_deployment_files(project_path, platform, force)

        # Display success message
        display_success_message(project_path, platform)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def check_existing_deployment_files(project_path: Path, platform: str) -> list:
    """Check for existing deployment files."""
    existing_files = []

    if platform in ["aws", "all"]:
        deploy_dir = project_path / "deploy" / "aws"
        if deploy_dir.exists():
            for file in deploy_dir.glob("*"):
                existing_files.append(f"deploy/aws/{file.name}")

    if platform in ["kubernetes", "all"]:
        deploy_dir = project_path / "deploy" / "kubernetes"
        if deploy_dir.exists():
            for file in deploy_dir.glob("*"):
                existing_files.append(f"deploy/kubernetes/{file.name}")

    if platform in ["terraform", "all"]:
        deploy_dir = project_path / "deploy" / "terraform"
        if deploy_dir.exists():
            for file in deploy_dir.glob("*"):
                existing_files.append(f"deploy/terraform/{file.name}")

    monitoring_dir = project_path / "deploy" / "monitoring"
    if monitoring_dir.exists():
        for file in monitoring_dir.glob("*"):
            existing_files.append(f"deploy/monitoring/{file.name}")

    return existing_files


def generate_deployment_files(project_path: Path, platform: str, force: bool) -> None:
    """Generate deployment files for the project."""
    try:
        # Get project name from directory
        project_name = project_path.name

        # Setup Jinja2 environment
        env = Environment(
            loader=PackageLoader("fascraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Deployment templates to render
        deployment_templates = []

        # AWS deployment templates
        if platform in ["aws", "all"]:
            deployment_templates.extend(
                [
                    ("deploy/aws/ecs-deploy.sh.jinja2", "deploy/aws/ecs-deploy.sh"),
                ]
            )

        # Kubernetes deployment templates
        if platform in ["kubernetes", "all"]:
            deployment_templates.extend(
                [
                    (
                        "deploy/kubernetes/deployment.yaml.jinja2",
                        "deploy/kubernetes/deployment.yaml",
                    ),
                ]
            )

        # Terraform templates
        if platform in ["terraform", "all"]:
            deployment_templates.extend(
                [
                    ("deploy/terraform/main.tf.jinja2", "deploy/terraform/main.tf"),
                ]
            )

        # Monitoring templates (always included)
        deployment_templates.extend(
            [
                (
                    "deploy/monitoring/prometheus.yml.jinjaja2",
                    "deploy/monitoring/prometheus.yml",
                ),
            ]
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Generating deployment files...", total=len(deployment_templates)
            )

            for template_name, output_name in deployment_templates:
                try:
                    render_deployment_template(
                        env, project_path, project_name, template_name, output_name
                    )
                    progress.advance(task)
                except Exception as e:
                    progress.stop()
                    raise TemplateRenderError(template_name, str(e)) from e

        # Make shell scripts executable
        make_scripts_executable(project_path, platform)

        console.print("🚀 Deployment files generated successfully!", style="bold green")

    except Exception as e:
        raise FileSystemError(f"Failed to generate deployment files: {str(e)}") from e


def render_deployment_template(
    env: Environment,
    project_path: Path,
    project_name: str,
    template_name: str,
    output_name: str,
) -> None:
    """Render a single deployment template."""
    try:
        template = env.get_template(template_name)
        content = template.render(project_name=project_name)

        output_path = project_path / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        raise TemplateRenderError(template_name, str(e)) from e


def make_scripts_executable(project_path: Path, platform: str) -> None:
    """Make shell scripts executable."""
    try:
        if platform in ["aws", "all"]:
            aws_dir = project_path / "deploy" / "aws"
            if aws_dir.exists():
                for script_file in aws_dir.glob("*.sh"):
                    script_file.chmod(0o755)
                    console.print(f"🔧 Made executable: {script_file}", style="green")
    except Exception as e:
        console.print(
            f"⚠️ Warning: Failed to make scripts executable: {e}", style="yellow"
        )


@app.command()
def setup_monitoring(
    path: str = typer.Option(".", help="📁 Path to the existing FastAPI project"),
) -> None:
    """📊 Setup monitoring and logging for the project."""
    try:
        # Validate project path
        project_path = validate_path_robust(path)

        if not project_path.exists():
            raise FileSystemError(f"Project path does not exist: {project_path}")

        # Setup monitoring
        setup_monitoring_config(project_path)

        # Display setup instructions
        display_monitoring_instructions(project_path)

    except FasCraftError as e:
        display_error_message(e)
        raise typer.Exit(code=1) from e
    except Exception as e:
        display_unexpected_error(e)
        raise typer.Exit(code=1) from e


def setup_monitoring_config(project_path: Path) -> None:
    """Setup monitoring configuration."""
    try:
        console.print("📊 Setting up monitoring configuration...", style="bold blue")

        # Create monitoring configuration files
        create_monitoring_configs(project_path)

        # Setup logging configuration
        setup_logging_config(project_path)

        console.print(
            "✅ Monitoring configuration completed successfully!", style="bold green"
        )

    except Exception as e:
        raise FileSystemError(f"Failed to setup monitoring: {str(e)}") from e


def create_monitoring_configs(project_path: Path) -> None:
    """Create monitoring configuration files."""
    # Create monitoring directory
    monitoring_dir = project_path / "deploy" / "monitoring"
    monitoring_dir.mkdir(parents=True, exist_ok=True)

    # Create basic monitoring config
    monitoring_config = monitoring_dir / "monitoring.yml"
    if not monitoring_config.exists():
        monitoring_config.write_text(
            """# Monitoring configuration for the project
monitoring:
  enabled: true
  prometheus:
    enabled: true
    port: 9090
  grafana:
    enabled: true
    port: 3000
  alertmanager:
    enabled: true
    port: 9093
"""
        )
        console.print("📝 Created monitoring.yml", style="green")


def setup_logging_config(project_path: Path) -> None:
    """Setup logging configuration."""
    # Create logging configuration
    logging_config = project_path / "config" / "logging.yml"
    if not logging_config.exists():
        logging_config.parent.mkdir(parents=True, exist_ok=True)
        logging_config.write_text(
            """# Logging configuration
version: 1
formatters:
  standard:
    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
  json:
    format: '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: json
    filename: logs/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: json
    filename: logs/error.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  {{ project_name }}:
    level: INFO
    handlers: [console, file, error_file]
    propagate: false

root:
  level: INFO
  handlers: [console]
"""
        )
        console.print("📝 Created logging.yml", style="green")


def display_success_message(project_path: Path, platform: str) -> None:
    """Display success message and next steps."""
    success_text = Text()
    success_text.append("🎉 ", style="bold green")
    success_text.append("Deployment files generated for ", style="bold white")
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

    if platform in ["aws", "all"]:
        aws_text = Text()
        aws_text.append("  ☁️ ", style="bold blue")
        aws_text.append("AWS ECS: ", style="white")
        aws_text.append(
            "Run 'deploy/aws/ecs-deploy.sh deploy' to deploy", style="bold cyan"
        )
        console.print(aws_text)

    if platform in ["kubernetes", "all"]:
        k8s_text = Text()
        k8s_text.append("  ☸️ ", style="bold blue")
        k8s_text.append("Kubernetes: ", style="white")
        k8s_text.append(
            "Run 'kubectl apply -f deploy/kubernetes/' to deploy", style="bold cyan"
        )
        console.print(k8s_text)

    if platform in ["terraform", "all"]:
        terraform_text = Text()
        terraform_text.append("  🏗️ ", style="bold blue")
        terraform_text.append("Terraform: ", style="white")
        terraform_text.append(
            "Run 'terraform init && terraform apply' in deploy/terraform/",
            style="bold cyan",
        )
        console.print(terraform_text)

    monitoring_text = Text()
    monitoring_text.append("  📊 ", style="bold blue")
    monitoring_text.append("Monitoring: ", style="white")
    monitoring_text.append(
        "Run 'fascraft deploy setup-monitoring' to configure", style="bold cyan"
    )
    console.print(monitoring_text)


def display_monitoring_instructions(project_path: Path) -> None:
    """Display monitoring setup instructions."""
    instructions_text = Text()
    instructions_text.append("📚 ", style="bold blue")
    instructions_text.append("Monitoring Setup Instructions:", style="bold white")
    console.print(instructions_text)

    # Prometheus setup
    prometheus_text = Text()
    prometheus_text.append("  📊 ", style="bold blue")
    prometheus_text.append("Prometheus: ", style="white")
    prometheus_text.append(
        "Configuration ready in deploy/monitoring/", style="bold cyan"
    )
    console.print(prometheus_text)

    # Logging setup
    logging_text = Text()
    logging_text.append("  📝 ", style="bold blue")
    logging_text.append("Logging: ", style="white")
    logging_text.append("Configuration ready in config/logging.yml", style="bold cyan")
    console.print(logging_text)

    # Next steps
    next_steps_text = Text()
    next_steps_text.append("  🚀 ", style="bold blue")
    next_steps_text.append("Next: ", style="white")
    next_steps_text.append(
        "Deploy monitoring stack and configure alerts", style="bold cyan"
    )
    console.print(next_steps_text)


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
