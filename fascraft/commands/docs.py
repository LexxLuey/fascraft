"""Command for generating documentation for FasCraft projects and modules."""

from pathlib import Path

import typer
from rich.console import Console
from rich.text import Text

from fascraft.exceptions import ModuleNotFoundError
from fascraft.module_dependencies import dependency_graph

# Initialize rich console
console = Console()


def is_fastapi_project(project_path: Path) -> bool:
    """Check if the given path is a FastAPI project."""
    # Check for FastAPI indicators
    if (project_path / "main.py").exists():
        content = (project_path / "main.py").read_text()
        if "FastAPI" in content or "fastapi" in content:
            return True

    # Check for pyproject.toml with FastAPI dependency
    if (project_path / "pyproject.toml").exists():
        content = (project_path / "pyproject.toml").read_text()
        if "fastapi" in content.lower():
            return True

    return False


def get_project_info(project_path: Path) -> dict:
    """Extract project information from various sources."""
    project_info = {
        "name": project_path.name,
        "path": str(project_path),
        "modules": [],
        "dependencies": [],
        "description": "",
        "version": "0.1.0",
    }

    # Try to get description from README
    readme_path = project_path / "README.md"
    if readme_path.exists():
        content = readme_path.read_text()
        # Extract first paragraph as description
        lines = content.split("\n")
        for line in lines:
            if line.strip() and not line.startswith("#"):
                project_info["description"] = line.strip()
                break

    # Try to get version from pyproject.toml
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        for line in content.split("\n"):
            if "version" in line and "=" in line:
                version = line.split("=")[1].strip().strip('"').strip("'")
                if version:
                    project_info["version"] = version
                break

    # Get modules from dependency graph
    if hasattr(dependency_graph, "modules"):
        project_info["modules"] = list(dependency_graph.modules.keys())

    return project_info


def get_module_info(project_path: Path, module_name: str) -> dict:
    """Extract module information."""
    module_path = project_path / module_name
    if not module_path.exists():
        raise ModuleNotFoundError(module_name, str(project_path))

    module_info = {
        "name": module_name,
        "path": str(module_path),
        "files": [],
        "dependencies": [],
        "description": f"{module_name.title()} module",
    }

    # Get module files
    for file_path in module_path.rglob("*.py"):
        if file_path.is_file() and not file_path.name.startswith("__"):
            module_info["files"].append(str(file_path.relative_to(module_path)))

    # Get dependencies from dependency graph
    if hasattr(dependency_graph, "modules") and module_name in dependency_graph.modules:
        module_data = dependency_graph.modules[module_name]
        if "dependencies" in module_data:
            module_info["dependencies"] = module_data["dependencies"]

    return module_info


def generate_api_documentation(
    project_path: Path, module_name: str | None = None
) -> str:
    """Generate OpenAPI/Swagger documentation."""
    # This would integrate with FastAPI's automatic OpenAPI generation
    # For now, we'll create a template-based approach

    if module_name:
        # Generate module-specific API docs
        return f"# API Documentation for {module_name.title()} Module\n\n"
    else:
        # Generate project-wide API docs
        project_info = get_project_info(project_path)
        return f"# API Documentation for {project_info['name']}\n\n"


def generate_readme_template(project_path: Path, module_name: str | None = None) -> str:
    """Generate README template for project or module."""
    if module_name:
        module_info = get_module_info(project_path, module_name)
        return f"# {module_name.title()} Module\n\n{module_info['description']}\n\n"
    else:
        project_info = get_project_info(project_path)
        return f"# {project_info['name']}\n\n{project_info['description']}\n\n"


def generate_changelog_template(
    project_path: Path, module_name: str | None = None
) -> str:
    """Generate changelog template."""
    if module_name:
        return f"# Changelog for {module_name.title()} Module\n\n## [Unreleased]\n\n### Added\n- Initial module implementation\n\n### Changed\n\n### Deprecated\n\n### Removed\n\n### Fixed\n\n### Security\n\n"
    else:
        project_info = get_project_info(project_path)
        return f"# Changelog for {project_info['name']}\n\n## [Unreleased]\n\n### Added\n- Initial project setup\n\n### Changed\n\n### Deprecated\n\n### Removed\n\n### Fixed\n\n### Security\n\n"


def generate_documentation(
    path: str = typer.Option(".", help="📁 The path to the existing FastAPI project"),
    module: str | None = typer.Option(
        None, "--module", "-m", help="📦 Specific module to document (optional)"
    ),
    output_dir: str = typer.Option(
        "docs", help="📂 Output directory for documentation"
    ),
    format: str = typer.Option(
        "markdown", help="📝 Documentation format (markdown, html, rst)"
    ),
    include_api: bool = typer.Option(
        True, "--include-api/--no-api", help="🔌 Include API documentation"
    ),
    include_readme: bool = typer.Option(
        True, "--include-readme/--no-readme", help="📖 Include README templates"
    ),
    include_changelog: bool = typer.Option(
        True,
        "--include-changelog/--no-changelog",
        help="📋 Include changelog templates",
    ),
) -> None:
    """📚 Generate comprehensive documentation for FasCraft projects and modules."""

    # Convert string path to Path object
    path_obj = Path(path)
    if not path_obj.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Path '{path_obj}' does not exist.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if it's a FastAPI project
    if not is_fastapi_project(path_obj):
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"'{path_obj}' is not a FastAPI project.", style="white")
        error_text.append(
            "\nMake sure you're in a project with FastAPI dependencies.", style="white"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Create output directory
    output_path = path_obj / output_dir
    output_path.mkdir(exist_ok=True)

    # Get project information
    try:
        project_info = get_project_info(path_obj)
        console.print(
            f"📊 Project: {project_info['name']} v{project_info['version']}",
            style="bold blue",
        )
    except Exception as e:
        console.print(
            f"⚠️  Warning: Could not extract project info: {str(e)}", style="yellow"
        )
        project_info = {"name": path_obj.name, "version": "0.1.0", "description": ""}

    # Generate documentation based on options
    generated_files = []

    if include_api:
        try:
            api_docs = generate_api_documentation(path_obj, module)
            api_file = output_path / "api_documentation.md"
            api_file.write_text(api_docs)
            generated_files.append("API Documentation")
            console.print("🔌 Generated API documentation", style="bold green")
        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not generate API docs: {str(e)}", style="yellow"
            )

    if include_readme:
        try:
            readme_content = generate_readme_template(path_obj, module)
            readme_file = output_path / "README_template.md"
            readme_file.write_text(readme_content)
            generated_files.append("README Template")
            console.print("📖 Generated README template", style="bold green")
        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not generate README template: {str(e)}",
                style="yellow",
            )

    if include_changelog:
        try:
            changelog_content = generate_changelog_template(path_obj, module)
            changelog_file = output_path / "CHANGELOG_template.md"
            changelog_file.write_text(changelog_content)
            generated_files.append("Changelog Template")
            console.print("📋 Generated changelog template", style="bold green")
        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not generate changelog template: {str(e)}",
                style="yellow",
            )

    # Generate module-specific documentation if specified
    if module:
        try:
            module_info = get_module_info(path_obj, module)
            console.print(f"📦 Module: {module_info['name']}", style="bold cyan")

            # Generate module overview
            module_overview = f"# {module_info['name'].title()} Module Overview\n\n"
            module_overview += f"**Path:** `{module_info['path']}`\n\n"
            module_overview += f"**Description:** {module_info['description']}\n\n"

            if module_info["files"]:
                module_overview += "**Files:**\n"
                for file in module_info["files"]:
                    module_overview += f"- `{file}`\n"
                module_overview += "\n"

            if module_info["dependencies"]:
                module_overview += (
                    f"**Dependencies:** {', '.join(module_info['dependencies'])}\n\n"
                )

            module_file = output_path / f"{module}_overview.md"
            module_file.write_text(module_overview)
            generated_files.append(f"{module.title()} Module Overview")
            console.print(f"📦 Generated {module} module overview", style="bold green")

        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not generate module documentation: {str(e)}",
                style="yellow",
            )
    else:
        # Generate project overview
        try:
            project_overview = f"# {project_info['name']} Project Overview\n\n"
            project_overview += f"**Version:** {project_info['version']}\n\n"
            project_overview += f"**Description:** {project_info['description']}\n\n"

            if project_info["modules"]:
                project_overview += "**Modules:**\n"
                for module_name in project_info["modules"]:
                    project_overview += f"- `{module_name}`\n"
                project_overview += "\n"

            project_file = output_path / "project_overview.md"
            project_file.write_text(project_overview)
            generated_files.append("Project Overview")
            console.print("📊 Generated project overview", style="bold green")

        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not generate project overview: {str(e)}",
                style="yellow",
            )

    # Success message
    success_text = Text()
    success_text.append("🎯 ", style="bold green")
    success_text.append("Successfully generated documentation in ", style="bold white")
    success_text.append(f"{output_path}", style="bold blue")
    success_text.append(".", style="white")
    console.print(success_text)

    # Show generated files
    if generated_files:
        files_text = Text()
        files_text.append("📁 Generated files:\n", style="bold yellow")
        for file_type in generated_files:
            files_text.append(f"  • {file_type}\n", style="cyan")
        console.print(files_text)

    # Next steps
    next_steps_text = Text()
    next_steps_text.append("🚀 ", style="bold yellow")
    next_steps_text.append("Next steps:", style="white")
    next_steps_text.append(
        f"\n  1. Review generated documentation in {output_path}",
        style="bold cyan",
    )
    next_steps_text.append(
        "\n  2. Customize templates to match your project needs",
        style="bold cyan",
    )
    next_steps_text.append(
        "\n  3. Add generated files to version control",
        style="bold cyan",
    )
    console.print(next_steps_text)


def generate_openapi_spec(
    path: str = typer.Option(".", help="📁 The path to the existing FastAPI project"),
    output_file: str = typer.Option(
        "openapi.json", help="📄 Output file for OpenAPI specification"
    ),
    format: str = typer.Option("json", help="📝 Output format (json, yaml)"),
) -> None:
    """🔌 Generate OpenAPI specification for FastAPI project."""

    # Convert string path to Path object
    path_obj = Path(path)
    if not path_obj.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Path '{path_obj}' does not exist.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if it's a FastAPI project
    if not is_fastapi_project(path_obj):
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"'{path_obj}' is not a FastAPI project.", style="white")
        error_text.append(
            "\nMake sure you're in a project with FastAPI dependencies.", style="white"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if main.py exists and can be run
    main_file = path_obj / "main.py"
    if not main_file.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append("main.py not found in project.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    console.print("🔌 Generating OpenAPI specification...", style="bold blue")

    # For now, we'll create a template-based OpenAPI spec
    # In a real implementation, this would run the FastAPI app and extract the spec

    openapi_content = {
        "openapi": "3.0.0",
        "info": {
            "title": path_obj.name,
            "version": "0.1.0",
            "description": f"API documentation for {path_obj.name}",
        },
        "paths": {},
        "components": {"schemas": {}, "responses": {}},
    }

    # Write OpenAPI spec
    output_path = path_obj / output_file
    if format.lower() == "json":
        import json

        output_path.write_text(json.dumps(openapi_content, indent=2))
    else:
        import yaml

        output_path.write_text(yaml.dump(openapi_content, default_flow_style=False))

    success_text = Text()
    success_text.append("🎯 ", style="bold green")
    success_text.append(
        "Successfully generated OpenAPI specification: ", style="bold white"
    )
    success_text.append(f"{output_path}", style="bold blue")
    console.print(success_text)


# Create the main docs app
docs_app = typer.Typer(
    help="📚 Documentation generation commands for FasCraft projects.", name="docs"
)

# Register commands
docs_app.command(name="generate")(generate_documentation)
docs_app.command(name="openapi")(generate_openapi_spec)
