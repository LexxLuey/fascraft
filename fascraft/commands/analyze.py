"""Command for analyzing existing FastAPI projects and suggesting improvements."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Initialize rich console
console = Console()


def analyze_project(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project to analyze"),
) -> None:
    """🔍 Analyzes a FastAPI project and suggests improvements."""
    path_obj = Path(path)

    if not path_obj.exists():
        error_text = Text("❌ Error: Path does not exist.", style="bold red")
        console.print(error_text)
        raise typer.Exit(code=1)

    if not is_fastapi_project(path_obj):
        error_text = Text("❌ Error: This is not a FastAPI project.", style="bold red")
        console.print(error_text)
        raise typer.Exit(code=1)

    console.print(f"🔍 Analyzing project at: {path_obj}", style="bold blue")

    # Analyze project structure
    analysis = analyze_project_structure(path_obj)

    # Display analysis results
    display_analysis_results(analysis)

    # Provide recommendations
    provide_recommendations(analysis)


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


def analyze_project_structure(project_path: Path) -> dict:
    """Analyze the project structure and return analysis results."""
    analysis = {
        "project_name": project_path.name,
        "structure": {},
        "modules": [],
        "routers": [],
        "config_files": [],
        "missing_components": [],
        "suggestions": [],
    }

    # Analyze directory structure
    for item in project_path.iterdir():
        if item.is_dir():
            if item.name in ["__pycache__", ".git", ".venv", "venv", "env"]:
                continue

            if item.name == "config":
                analysis["structure"]["config"] = analyze_config_directory(item)
            elif item.name in ["models", "schemas", "services", "routers"]:
                analysis["structure"]["flat_structure"] = True
                analysis["suggestions"].append(
                    "Consider converting to domain-driven architecture"
                )
            elif not item.name.startswith("."):
                # Check if it's a domain module
                if (item / "__init__.py").exists() and (item / "models.py").exists():
                    analysis["modules"].append(item.name)
                else:
                    analysis["structure"]["other_dirs"] = analysis["structure"].get(
                        "other_dirs", []
                    )
                    analysis["structure"]["other_dirs"].append(item.name)

    # Analyze main.py
    main_py_path = project_path / "main.py"
    if main_py_path.exists():
        analysis["main_py"] = analyze_main_py(main_py_path)

    # Check for configuration files
    config_files = ["fascraft.toml", ".env", "pyproject.toml", "requirements.txt"]
    for config_file in config_files:
        if (project_path / config_file).exists():
            analysis["config_files"].append(config_file)

    # Identify missing components
    if not analysis["modules"]:
        analysis["missing_components"].append("Domain modules")

    if "routers" not in analysis["structure"]:
        analysis["missing_components"].append("Centralized router management")

    if "fascraft.toml" not in analysis["config_files"]:
        analysis["missing_components"].append("FasCraft configuration")

    return analysis


def analyze_config_directory(config_path: Path) -> dict:
    """Analyze the config directory structure."""
    config_analysis = {"files": [], "has_settings": False, "has_database": False}

    for item in config_path.iterdir():
        if item.is_file():
            config_analysis["files"].append(item.name)
            if item.name == "settings.py":
                config_analysis["has_settings"] = True
            elif item.name == "database.py":
                config_analysis["has_database"] = True

    return config_analysis


def analyze_main_py(main_py_path: Path) -> dict:
    """Analyze the main.py file structure."""
    content = main_py_path.read_text()

    analysis = {
        "has_fastapi_import": "FastAPI" in content,
        "has_router_includes": "app.include_router" in content,
        "router_count": content.count("app.include_router"),
        "has_base_router": "from routers import base_router" in content,
        "lines": len(content.split("\n")),
    }

    return analysis


def display_analysis_results(analysis: dict) -> None:
    """Display the analysis results in a formatted table."""
    console.print("\n📊 Project Analysis Results", style="bold green")

    # Project overview
    overview_table = Table(title="Project Overview")
    overview_table.add_column("Property", style="cyan")
    overview_table.add_column("Value", style="white")

    overview_table.add_row("Project Name", analysis["project_name"])
    overview_table.add_row("Domain Modules", str(len(analysis["modules"])))
    overview_table.add_row("Config Files", str(len(analysis["config_files"])))
    overview_table.add_row(
        "Router Includes", str(analysis.get("main_py", {}).get("router_count", 0))
    )

    console.print(overview_table)

    # Structure analysis
    if analysis["structure"]:
        console.print("\n🏗️ Structure Analysis", style="bold blue")
        structure_table = Table()
        structure_table.add_column("Component", style="cyan")
        structure_table.add_column("Status", style="white")

        if "config" in analysis["structure"]:
            config = analysis["structure"]["config"]
            structure_table.add_row("Config Directory", "✅ Present")
            structure_table.add_row(
                "Settings", "✅ Present" if config["has_settings"] else "❌ Missing"
            )
            structure_table.add_row(
                "Database Config",
                "✅ Present" if config["has_database"] else "❌ Missing",
            )

        if "flat_structure" in analysis["structure"]:
            structure_table.add_row(
                "Architecture", "⚠️ Flat Structure (Consider domain-driven)"
            )

        console.print(structure_table)

    # Modules found
    if analysis["modules"]:
        console.print(
            f"\n📦 Domain Modules Found: {', '.join(analysis['modules'])}",
            style="bold green",
        )

    # Missing components
    if analysis["missing_components"]:
        console.print(
            f"\n❌ Missing Components: {', '.join(analysis['missing_components'])}",
            style="bold red",
        )


def provide_recommendations(analysis: dict) -> None:
    """Provide specific recommendations based on analysis."""
    console.print("\n💡 Recommendations", style="bold yellow")

    recommendations = []

    if not analysis["modules"]:
        recommendations.append(
            "Use 'fascraft generate <module_name>' to create domain modules"
        )

    if "fascraft.toml" not in analysis["config_files"]:
        recommendations.append(
            "Consider adding FasCraft configuration for better project management"
        )

    if analysis.get("main_py", {}).get("router_count", 0) > 3:
        recommendations.append(
            "Consider consolidating routers using a base router pattern"
        )

    if "flat_structure" in analysis["structure"]:
        recommendations.append(
            "Migrate to domain-driven architecture for better organization"
        )

    if not recommendations:
        console.print("🎉 Your project follows best practices!", style="bold green")
    else:
        for i, rec in enumerate(recommendations, 1):
            console.print(f"{i}. {rec}", style="white")

    console.print(
        "\n🚀 Use 'fascraft migrate' to automatically apply improvements",
        style="bold cyan",
    )
