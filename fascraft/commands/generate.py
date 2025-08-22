"""Command for generating new domain modules in existing FasCraft projects."""

from pathlib import Path

import typer
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from rich.text import Text

from fascraft.module_dependencies import dependency_analyzer, dependency_graph
from fascraft.template_registry import template_registry

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


def generate_dependency_imports(dependencies: list) -> str:
    """Generate import statements for dependencies."""
    if not dependencies:
        return ""

    imports = []
    for dep in dependencies:
        imports.append(f"from {dep} import models as {dep}_models")
        imports.append(f"from {dep} import services as {dep}_services")
        imports.append(f"from {dep} import schemas as {dep}_schemas")

    return "\n".join(imports)


def generate_dependency_injections(dependencies: list) -> str:
    """Generate dependency injection parameters for services and routers."""
    if not dependencies:
        return ""

    injections = []
    for dep in dependencies:
        injections.append(f"{dep}_service: {dep.title()}Service")

    return ", ".join(injections)


def ensure_config_structure(project_path: Path) -> None:
    """Ensure config directory and files exist."""
    config_dir = project_path / "config"

    if not config_dir.exists():
        console.print("📁 Creating config directory...", style="bold yellow")
        config_dir.mkdir(exist_ok=True)

        # Create basic config files if they don't exist
        if not (config_dir / "__init__.py").exists():
            (config_dir / "__init__.py").write_text('"""Configuration module."""\n')

        if not (config_dir / "settings.py").exists():
            (config_dir / "settings.py").write_text(
                '"""Application settings."""\n\napp_name = "{{ project_name }}"\n'
            )

        if not (config_dir / "database.py").exists():
            (config_dir / "database.py").write_text(
                '"""Database configuration."""\n\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\n\nBase = declarative_base()\n'
            )


def generate_module(
    module_name: str,
    path: str = typer.Option(".", help="📁 The path to the existing FastAPI project"),
    template: str = typer.Option(
        "basic",
        help="🎨 Template type to use (basic, crud, api_first, event_driven, microservice, admin_panel)",
    ),
    depends_on: str = typer.Option(
        None,
        "--depends-on",
        help="🔗 Comma-separated list of modules this module depends on",
    ),
) -> None:
    """🔧 Generates a new domain module in an existing FastAPI project."""
    if not module_name or not module_name.strip():
        error_text = Text(
            "❌ Error: Module name cannot be empty or whitespace.", style="bold red"
        )
        console.print(error_text)
        raise typer.Exit(code=1)

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

    # Check if module already exists
    module_dir = path_obj / module_name
    if module_dir.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Module '{module_name}' already exists at ", style="white")
        error_text.append(f"{module_dir}", style="yellow")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Validate template selection
    try:
        selected_template = template_registry.get_template(template)
        console.print(
            f"🎨 Using template: {selected_template.display_name} ({selected_template.description})",
            style="bold blue",
        )
    except Exception as e:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Invalid template '{template}': {str(e)}", style="white")
        console.print(error_text)

        # Show available templates
        available_templates = template_registry.list_templates()
        console.print("\n📋 Available templates:", style="bold yellow")
        for t in available_templates:
            console.print(
                f"  • {t.name}: {t.display_name} - {t.description}", style="cyan"
            )

        raise typer.Exit(code=1) from e

    # Handle module dependencies
    dependencies = []
    if depends_on:
        dependencies = [dep.strip() for dep in depends_on.split(",") if dep.strip()]

        # Validate that all dependency modules exist
        for dep_module in dependencies:
            dep_path = path_obj / dep_module
            if not dep_path.exists():
                error_text = Text()
                error_text.append("❌ ", style="bold red")
                error_text.append("Error: ", style="bold red")
                error_text.append(
                    f"Dependency module '{dep_module}' not found at ", style="white"
                )
                error_text.append(f"{dep_path}", style="yellow")
                console.print(error_text)
                raise typer.Exit(code=1)

        # Check for circular dependencies
        if module_name in dependencies:
            error_text = Text()
            error_text.append("❌ ", style="bold red")
            error_text.append("Error: ", style="bold red")
            error_text.append(
                f"Module cannot depend on itself: '{module_name}'", style="white"
            )
            console.print(error_text)
            raise typer.Exit(code=1)

        console.print(f"🔗 Dependencies: {', '.join(dependencies)}", style="bold blue")

    # Register module in dependency graph
    module_path = path_obj / module_name
    dependency_graph.add_module(
        module_name,
        module_path,
        {"template": template, "generated_at": "now", "dependencies": dependencies},
    )

    # Register dependencies in the graph
    for dep_module in dependencies:
        dep_path = path_obj / dep_module
        if dep_module not in dependency_graph.modules:
            dependency_graph.add_module(
                dep_module, dep_path, {"type": "existing", "discovered_at": "now"}
            )

        # Add dependency relationship
        dependency_graph.add_dependency(
            module_name,
            dep_module,
            "import",
            "strong",
            f"{module_name} module depends on {dep_module}",
            module_path,
            1,
        )

    # Validate dependency graph health
    if dependencies:
        try:
            # Check for circular dependencies
            if dependency_graph.has_circular_dependencies():
                cycles = dependency_graph.find_circular_dependencies()
                error_text = Text()
                error_text.append("❌ ", style="bold red")
                error_text.append("Error: ", style="bold red")
                error_text.append("Circular dependencies detected:", style="white")
                console.print(error_text)

                for cycle in cycles:
                    cycle_text = Text()
                    cycle_text.append("  🔄 ", style="yellow")
                    cycle_text.append(" → ".join(cycle), style="cyan")
                    console.print(cycle_text)

                raise typer.Exit(code=1)

            # Analyze module health
            health = dependency_analyzer.analyze_module_health(module_name)
            if health["health_score"] < 70:
                warning_text = Text()
                warning_text.append("⚠️  ", style="bold yellow")
                warning_text.append("Warning: ", style="bold yellow")
                warning_text.append(
                    f"Module health score: {health['health_score']}/100", style="white"
                )
                console.print(warning_text)

                suggestions = dependency_analyzer.suggest_dependency_optimizations()
                for suggestion in suggestions:
                    if suggestion["type"] == "critical":
                        suggestion_text = Text()
                        suggestion_text.append("  💡 ", style="blue")
                        suggestion_text.append(
                            suggestion["recommendation"], style="cyan"
                        )
                        console.print(suggestion_text)
        except Exception as e:
            console.print(
                f"⚠️  Warning: Could not analyze dependencies: {str(e)}", style="yellow"
            )

    # Ensure config structure exists
    ensure_config_structure(path_obj)

    # Set up Jinja2 environment for the selected template
    template_path = f"templates/module_templates/{template}"
    env = Environment(
        loader=PackageLoader("fascraft", template_path),
        autoescape=select_autoescape(),
    )

    # Define module templates to render
    templates = [
        ("__init__.py.jinja2", f"{module_name}/__init__.py"),
        ("models.py.jinja2", f"{module_name}/models.py"),
        ("schemas.py.jinja2", f"{module_name}/schemas.py"),
        ("services.py.jinja2", f"{module_name}/services.py"),
        ("routers.py.jinja2", f"{module_name}/routers.py"),
        ("tests/__init__.py.jinja2", f"{module_name}/tests/__init__.py"),
        ("tests/test_models.py.jinja2", f"{module_name}/tests/test_models.py"),
    ]

    # Render all module templates
    for template_name, output_name in templates:
        template = env.get_template(template_name)
        content = template.render(
            module_name=module_name,
            project_name=path_obj.name,
            module_name_plural=f"{module_name}s",
            module_name_title=module_name.title(),
            dependencies=dependencies,
            dependency_imports=generate_dependency_imports(dependencies),
            dependency_injections=generate_dependency_injections(dependencies),
        )
        output_path = path_obj / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    # Update base router to include the new module
    update_base_router(path_obj, module_name)

    success_text = Text()
    success_text.append("🎯 ", style="bold green")
    success_text.append("Successfully generated domain module ", style="bold white")
    success_text.append(f"'{module_name}' ", style="bold cyan")
    success_text.append("using ", style="white")
    success_text.append(f"'{selected_template.display_name}' ", style="bold yellow")
    success_text.append("template in ", style="white")
    success_text.append(f"{path_obj}", style="bold blue")
    success_text.append(".", style="white")

    if dependencies:
        success_text.append(
            f"\n🔗 Module depends on: {', '.join(dependencies)}", style="bold green"
        )

    console.print(success_text)

    next_steps_text = Text()
    next_steps_text.append("🚀 ", style="bold yellow")
    next_steps_text.append("Next steps:", style="white")
    next_steps_text.append(
        f"\n  1. The {module_name} module has been automatically added to the base router",
        style="bold cyan",
    )
    next_steps_text.append(
        "\n  2. Run 'pip install -r requirements.txt' to install dependencies",
        style="bold cyan",
    )
    next_steps_text.append(
        f"\n  3. Test your new module with 'pytest {module_name}/tests/'",
        style="bold cyan",
    )

    if dependencies:
        next_steps_text.append(
            f"\n  4. Review dependency imports in {module_name}/models.py, {module_name}/services.py",
            style="bold cyan",
        )
        next_steps_text.append(
            "\n  5. Ensure all dependency modules are properly configured",
            style="bold cyan",
        )

    console.print(next_steps_text)

    module_info_text = Text()
    module_info_text.append("✨ ", style="bold green")
    module_info_text.append("Module includes: ", style="white")
    module_info_text.append(
        "Working routers, services, models, and schemas", style="bold cyan"
    )
    console.print(module_info_text)

    db_info_text = Text()
    db_info_text.append("🗄️ ", style="bold blue")
    db_info_text.append("Database ready: ", style="white")
    db_info_text.append(
        "Models are properly configured for SQLAlchemy and Alembic", style="bold cyan"
    )
    console.print(db_info_text)

    # Show dependency information if any
    if dependencies:
        dep_info_text = Text()
        dep_info_text.append("🔗 ", style="bold green")
        dep_info_text.append("Dependencies configured: ", style="white")
        dep_info_text.append(
            f"Import statements and dependency injections added for {', '.join(dependencies)}",
            style="bold cyan",
        )
        console.print(dep_info_text)

        # Show dependency graph info
        try:
            stats = dependency_analyzer.get_dependency_statistics()
            graph_info_text = Text()
            graph_info_text.append("📊 ", style="bold blue")
            graph_info_text.append("Dependency graph: ", style="white")
            graph_info_text.append(
                f"{stats['total_modules']} modules, {stats['total_dependencies']} dependencies",
                style="bold cyan",
            )
            console.print(graph_info_text)
        except Exception:  # nosec B110 - Silently fail if dependency analysis fails
            pass  # Silently fail if dependency analysis fails


def update_base_router(project_path: Path, module_name: str) -> None:
    """Update base router to include the new module."""
    base_router_path = project_path / "routers" / "base.py"

    if not base_router_path.exists():
        console.print(
            "⚠️  Warning: base router not found, skipping module integration",
            style="yellow",
        )
        return

    content = base_router_path.read_text()

    # Add import if not present
    import_statement = f"from {module_name} import routers as {module_name}_routers"
    if import_statement not in content:
        # Find the comment line for imports
        lines = content.split("\n")
        new_lines = []
        import_added = False

        for line in lines:
            new_lines.append(line)
            if line.strip().startswith("# from") and not import_added:
                new_lines.append(import_statement)
                import_added = True

        if not import_added:
            # Add after existing imports
            for i, line in enumerate(lines):
                if line.strip().startswith("# from") and not import_added:
                    new_lines.insert(i + 1, import_statement)
                    import_added = True
                    break

        content = "\n".join(new_lines)

    # Add router include if not present
    router_include = f'base_router.include_router({module_name}_routers.router, prefix="/{module_name}s", tags=["{module_name}s"])'
    if router_include not in content:
        # Find the comment line for router includes
        lines = content.split("\n")
        new_lines = []
        router_added = False

        for line in lines:
            new_lines.append(line)
            if (
                line.strip().startswith("# base_router.include_router")
                and not router_added
            ):
                new_lines.append(router_include)
                router_added = True

        if not router_added:
            # Add after existing router includes
            for i, line in enumerate(lines):
                if (
                    line.strip().startswith("# base_router.include_router")
                    and not router_added
                ):
                    new_lines.insert(i + 1, router_include)
                    router_added = True
                    break

        content = "\n".join(new_lines)

    # Write updated content
    base_router_path.write_text(content)
    console.print(
        f"📝 Updated base router to include {module_name} module", style="bold green"
    )
