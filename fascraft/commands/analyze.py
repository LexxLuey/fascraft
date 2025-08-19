"""Command for analyzing existing FastAPI projects and suggesting improvements."""

import json
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Initialize rich console
console = Console()


def analyze_project(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project to analyze"),
    docs_only: bool = typer.Option(
        False, "--docs-only", "-d", help="📚 Analyze only documentation quality"
    ),
    version_report: bool = typer.Option(
        False,
        "--version-report",
        "-v",
        help="🏷️ Generate detailed version consistency report",
    ),
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

    if version_report:
        console.print(
            f"🏷️ Generating version consistency report for: {path_obj}",
            style="bold blue",
        )

        # Generate version report
        version_report_data = generate_documentation_version_report(path_obj)

        # Display version report
        display_version_report(version_report_data)

    elif docs_only:
        console.print(
            f"📚 Analyzing documentation quality at: {path_obj}", style="bold magenta"
        )

        # Analyze only documentation
        doc_analysis = analyze_documentation_quality(path_obj)

        # Display documentation analysis results
        display_documentation_analysis(doc_analysis)

        # Provide documentation recommendations
        if doc_analysis["doc_suggestions"]:
            console.print("\n💡 Documentation Recommendations:", style="bold yellow")
            for i, suggestion in enumerate(doc_analysis["doc_suggestions"], 1):
                console.print(f"{i}. {suggestion}", style="white")

            console.print(
                "\n🚀 Use 'fascraft docs generate' to create missing documentation",
                style="bold cyan",
            )
        else:
            console.print(
                "🎉 Your documentation is comprehensive and follows best practices!",
                style="bold green",
            )
    else:
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

    # Analyze documentation quality
    analysis["documentation"] = analyze_documentation_quality(project_path)

    return analysis


def analyze_documentation_quality(project_path: Path) -> dict:
    """Analyze documentation quality and completeness."""
    doc_analysis = {
        "has_readme": False,
        "has_changelog": False,
        "has_api_docs": False,
        "has_project_docs": False,
        "has_module_docs": False,
        "docs_directory": False,
        "readme_quality": 0,
        "changelog_quality": 0,
        "api_docs_quality": 0,
        "missing_docs": [],
        "doc_suggestions": [],
        "version_info": {},
    }

    # Check for README
    readme_path = project_path / "README.md"
    if readme_path.exists():
        doc_analysis["has_readme"] = True
        doc_analysis["readme_quality"] = analyze_readme_quality(readme_path)

    # Check for CHANGELOG
    changelog_path = project_path / "CHANGELOG.md"
    if changelog_path.exists():
        doc_analysis["has_changelog"] = True
        doc_analysis["changelog_quality"] = analyze_changelog_quality(changelog_path)

    # Check for docs directory
    docs_path = project_path / "docs"
    if docs_path.exists():
        doc_analysis["docs_directory"] = True
        doc_analysis.update(analyze_docs_directory(docs_path))

    # Check for API documentation
    if (project_path / "openapi.json").exists() or (
        project_path / "openapi.yaml"
    ).exists():
        doc_analysis["has_api_docs"] = True
        doc_analysis["api_docs_quality"] = analyze_api_docs_quality(project_path)

    # Check for project documentation
    if (project_path / "docs" / "project_overview.md").exists():
        doc_analysis["has_project_docs"] = True

    # Check for module documentation
    modules = [
        item
        for item in project_path.iterdir()
        if item.is_dir() and (item / "__init__.py").exists()
    ]
    for module in modules:
        if (project_path / "docs" / f"{module.name}_overview.md").exists():
            doc_analysis["has_module_docs"] = True
            break

    # Identify missing documentation
    if not doc_analysis["has_readme"]:
        doc_analysis["missing_docs"].append("README.md")
    if not doc_analysis["has_changelog"]:
        doc_analysis["missing_docs"].append("CHANGELOG.md")
    if not doc_analysis["has_api_docs"]:
        doc_analysis["missing_docs"].append("API Documentation")
    if not doc_analysis["has_project_docs"]:
        doc_analysis["missing_docs"].append("Project Overview")

    # Get version information
    doc_analysis["version_info"] = extract_version_info(project_path)

    # Generate suggestions
    doc_analysis["doc_suggestions"] = generate_doc_suggestions(doc_analysis)

    return doc_analysis


def analyze_readme_quality(readme_path: Path) -> int:
    """Analyze README quality and return a score (0-100)."""
    content = readme_path.read_text()
    score = 0

    # Basic structure checks
    if "# " in content:  # Has title
        score += 10
    if "## " in content:  # Has sections
        score += 10
    if "```" in content:  # Has code blocks
        score += 10
    if "http" in content:  # Has links
        score += 5
    if "requirements" in content.lower() or "dependencies" in content.lower():
        score += 10
    if "install" in content.lower() or "setup" in content.lower():
        score += 10
    if "usage" in content.lower() or "example" in content.lower():
        score += 10
    if "api" in content.lower() or "endpoint" in content.lower():
        score += 10
    if "test" in content.lower():
        score += 5
    if "contributing" in content.lower():
        score += 5
    if "license" in content.lower():
        score += 5

    return min(score, 100)


def analyze_changelog_quality(changelog_path: Path) -> int:
    """Analyze changelog quality and return a score (0-100)."""
    content = changelog_path.read_text()
    score = 0

    # Structure checks
    if "## [" in content:  # Has version sections
        score += 20
    if "### Added" in content:  # Has change categories
        score += 20
    if "### Changed" in content:
        score += 20
    if "### Fixed" in content:
        score += 20
    if "### Security" in content:
        score += 20

    return min(score, 100)


def analyze_api_docs_quality(project_path: Path) -> int:
    """Analyze API documentation quality and return a score (0-100)."""
    score = 0

    # Check for OpenAPI spec
    if (project_path / "openapi.json").exists():
        try:
            with open(project_path / "openapi.json") as f:
                spec = json.load(f)
                if spec.get("openapi") and spec.get("info"):
                    score += 50
                if spec.get("paths"):
                    score += 30
                if spec.get("components", {}).get("schemas"):
                    score += 20
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    return min(score, 100)


def analyze_docs_directory(docs_path: Path) -> dict:
    """Analyze the docs directory structure."""
    docs_analysis = {
        "total_files": 0,
        "markdown_files": 0,
        "api_docs": False,
        "project_docs": False,
        "module_docs": False,
        "templates": False,
    }

    for item in docs_path.rglob("*"):
        if item.is_file():
            docs_analysis["total_files"] += 1
            if item.suffix == ".md":
                docs_analysis["markdown_files"] += 1
            if "api" in item.name.lower():
                docs_analysis["api_docs"] = True
            if "project" in item.name.lower() or "overview" in item.name.lower():
                docs_analysis["project_docs"] = True
            if "module" in item.name.lower():
                docs_analysis["module_docs"] = True
            if "template" in item.name.lower():
                docs_analysis["templates"] = True

    return docs_analysis


def extract_version_info(project_path: Path) -> dict:
    """Extract version information from various sources."""
    version_info = {
        "pyproject_version": None,
        "readme_version": None,
        "changelog_version": None,
        "latest_version": None,
        "version_consistency": False,
    }

    # Check pyproject.toml
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        for line in content.split("\n"):
            if "version" in line and "=" in line:
                version = line.split("=")[1].strip().strip('"').strip("'")
                if version:
                    version_info["pyproject_version"] = version
                break

    # Check README for version
    readme_path = project_path / "README.md"
    if readme_path.exists():
        content = readme_path.read_text()
        # Look for version patterns
        import re

        version_patterns = [
            r"version[:\s]+([0-9]+\.[0-9]+\.[0-9]+)",
            r"v([0-9]+\.[0-9]+\.[0-9]+)",
            r"([0-9]+\.[0-9]+\.[0-9]+)",
        ]
        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                version_info["readme_version"] = match.group(1)
                break

    # Check CHANGELOG for latest version
    changelog_path = project_path / "CHANGELOG.md"
    if changelog_path.exists():
        content = changelog_path.read_text()
        import re

        version_match = re.search(r"## \[([0-9]+\.[0-9]+\.[0-9]+)\]", content)
        if version_match:
            version_info["changelog_version"] = version_match.group(1)

    # Determine latest version
    versions = [
        v
        for v in [
            version_info["pyproject_version"],
            version_info["readme_version"],
            version_info["changelog_version"],
        ]
        if v
    ]
    if versions:
        # Simple version comparison (assumes semantic versioning)
        latest = max(versions, key=lambda x: tuple(map(int, x.split("."))))
        version_info["latest_version"] = latest

        # Check consistency
        version_info["version_consistency"] = len(set(versions)) == 1

    return version_info


def generate_doc_suggestions(doc_analysis: dict) -> list[str]:
    """Generate documentation improvement suggestions."""
    suggestions = []

    if not doc_analysis["has_readme"]:
        suggestions.append("Create a comprehensive README.md file")
    elif doc_analysis["readme_quality"] < 70:
        suggestions.append("Improve README.md quality and completeness")

    if not doc_analysis["has_changelog"]:
        suggestions.append("Add a CHANGELOG.md file following Keep a Changelog format")
    elif doc_analysis["changelog_quality"] < 80:
        suggestions.append(
            "Enhance CHANGELOG.md with proper version sections and categories"
        )

    if not doc_analysis["has_api_docs"]:
        suggestions.append("Generate API documentation using 'fascraft docs openapi'")
    elif doc_analysis["api_docs_quality"] < 80:
        suggestions.append(
            "Improve API documentation with detailed endpoint descriptions"
        )

    if not doc_analysis["has_project_docs"]:
        suggestions.append(
            "Generate project overview documentation using 'fascraft docs generate'"
        )

    if not doc_analysis["has_module_docs"]:
        suggestions.append(
            "Generate module-specific documentation for existing modules"
        )

    if not doc_analysis["docs_directory"]:
        suggestions.append("Create a docs/ directory for organized documentation")

    if not doc_analysis["version_info"]["version_consistency"]:
        suggestions.append(
            "Ensure version consistency across pyproject.toml, README, and CHANGELOG"
        )

    return suggestions


def generate_documentation_version_report(project_path: Path) -> dict:
    """Generate a comprehensive documentation version report."""
    version_report = {
        "timestamp": datetime.now().isoformat(),
        "project_path": str(project_path),
        "version_sources": {},
        "consistency_issues": [],
        "recommendations": [],
    }

    # Extract version from pyproject.toml
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        for line in content.split("\n"):
            if "version" in line and "=" in line:
                version = line.split("=")[1].strip().strip('"').strip("'")
                if version:
                    version_report["version_sources"]["pyproject.toml"] = version
                break

    # Extract version from README
    readme_path = project_path / "README.md"
    if readme_path.exists():
        content = readme_path.read_text()
        import re

        version_match = re.search(
            r"version[:\s]+([0-9]+\.[0-9]+\.[0-9]+)", content, re.IGNORECASE
        )
        if version_match:
            version_report["version_sources"]["README.md"] = version_match.group(1)

    # Extract version from CHANGELOG
    changelog_path = project_path / "CHANGELOG.md"
    if changelog_path.exists():
        content = changelog_path.read_text()
        import re

        version_match = re.search(r"## \[([0-9]+\.[0-9]+\.[0-9]+)\]", content)
        if version_match:
            version_report["version_sources"]["CHANGELOG.md"] = version_match.group(1)

    # Check for version consistency
    versions = list(version_report["version_sources"].values())
    if len(set(versions)) > 1:
        version_report["consistency_issues"].append(
            f"Version mismatch: {', '.join(versions)}"
        )
        version_report["recommendations"].append(
            "Update all version references to match"
        )

    if not versions:
        version_report["consistency_issues"].append("No version information found")
        version_report["recommendations"].append(
            "Add version information to pyproject.toml"
        )

    # Add semantic versioning check
    for source, version in version_report["version_sources"].items():
        if not is_semantic_version(version):
            version_report["consistency_issues"].append(
                f"Invalid semantic version in {source}: {version}"
            )
            version_report["recommendations"].append(
                "Use semantic versioning format (MAJOR.MINOR.PATCH)"
            )

    return version_report


def is_semantic_version(version: str) -> bool:
    """Check if a version string follows semantic versioning."""
    import re

    pattern = r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
    return bool(re.match(pattern, version))


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


def display_documentation_analysis(doc_analysis: dict) -> None:
    """Display documentation analysis results."""
    console.print("\n📚 Documentation Analysis", style="bold magenta")

    # Documentation overview table
    doc_table = Table(title="Documentation Status")
    doc_table.add_column("Document Type", style="cyan")
    doc_table.add_column("Status", style="white")
    doc_table.add_column("Quality Score", style="yellow")

    # README status
    readme_status = "✅ Present" if doc_analysis["has_readme"] else "❌ Missing"
    readme_score = (
        f"{doc_analysis['readme_quality']}/100" if doc_analysis["has_readme"] else "N/A"
    )
    doc_table.add_row("README.md", readme_status, readme_score)

    # CHANGELOG status
    changelog_status = "✅ Present" if doc_analysis["has_changelog"] else "❌ Missing"
    changelog_score = (
        f"{doc_analysis['changelog_quality']}/100"
        if doc_analysis["has_changelog"]
        else "N/A"
    )
    doc_table.add_row("CHANGELOG.md", changelog_status, changelog_score)

    # API Documentation status
    api_status = "✅ Present" if doc_analysis["has_api_docs"] else "❌ Missing"
    api_score = (
        f"{doc_analysis['api_docs_quality']}/100"
        if doc_analysis["has_api_docs"]
        else "N/A"
    )
    doc_table.add_row("API Documentation", api_status, api_score)

    # Project Documentation status
    project_status = "✅ Present" if doc_analysis["has_project_docs"] else "❌ Missing"
    doc_table.add_row("Project Overview", project_status, "N/A")

    # Module Documentation status
    module_status = "✅ Present" if doc_analysis["has_module_docs"] else "❌ Missing"
    doc_table.add_row("Module Documentation", module_status, "N/A")

    console.print(doc_table)

    # Version information
    if doc_analysis["version_info"]["latest_version"]:
        console.print("\n🏷️ Version Information", style="bold blue")
        version_table = Table()
        version_table.add_column("Source", style="cyan")
        version_table.add_column("Version", style="white")

        version_info = doc_analysis["version_info"]
        if version_info["pyproject_version"]:
            version_table.add_row("pyproject.toml", version_info["pyproject_version"])
        if version_info["readme_version"]:
            version_table.add_row("README.md", version_info["readme_version"])
        if version_info["changelog_version"]:
            version_table.add_row("CHANGELOG.md", version_info["changelog_version"])

        console.print(version_table)

        # Version consistency warning
        if not version_info["version_consistency"]:
            console.print(
                "⚠️ Version inconsistency detected across files", style="bold yellow"
            )
        else:
            console.print("✅ Version consistency verified", style="bold green")

    # Documentation directory analysis
    if doc_analysis["docs_directory"]:
        docs_info = doc_analysis.get("total_files", 0)
        markdown_files = doc_analysis.get("markdown_files", 0)
        console.print(
            f"\n📁 Documentation Directory: {docs_info} total files, {markdown_files} markdown files",
            style="bold green",
        )

    # Missing documentation
    if doc_analysis["missing_docs"]:
        console.print(
            f"\n❌ Missing Documentation: {', '.join(doc_analysis['missing_docs'])}",
            style="bold red",
        )


def display_version_report(version_report: dict) -> None:
    """Display the version consistency report."""
    console.print("\n🏷️ Version Consistency Report", style="bold blue")

    # Project information
    console.print(f"📁 Project: {version_report['project_path']}", style="cyan")
    console.print(f"⏰ Generated: {version_report['timestamp']}", style="cyan")

    # Version sources table
    if version_report["version_sources"]:
        console.print("\n📋 Version Sources Found:", style="bold green")
        version_table = Table()
        version_table.add_column("Source", style="cyan")
        version_table.add_column("Version", style="white")

        for source, version in version_report["version_sources"].items():
            version_table.add_row(source, version)

        console.print(version_table)
    else:
        console.print(
            "\n❌ No version information found in any source files", style="bold red"
        )

    # Consistency issues
    if version_report["consistency_issues"]:
        console.print("\n⚠️ Version Consistency Issues:", style="bold yellow")
        for issue in version_report["consistency_issues"]:
            console.print(f"  • {issue}", style="yellow")

    # Recommendations
    if version_report["recommendations"]:
        console.print("\n💡 Recommendations:", style="bold magenta")
        for i, rec in enumerate(version_report["recommendations"], 1):
            console.print(f"  {i}. {rec}", style="white")

    # Summary
    if not version_report["consistency_issues"] and version_report["version_sources"]:
        console.print(
            "\n✅ Version consistency verified across all sources", style="bold green"
        )
    elif not version_report["version_sources"]:
        console.print("\n❌ No version information available", style="bold red")
    else:
        console.print("\n⚠️ Version consistency issues detected", style="bold yellow")

    # Missing components
    if version_report.get("missing_components"):
        console.print(
            f"\n❌ Missing Components: {', '.join(version_report['missing_components'])}",
            style="bold red",
        )

    # Documentation analysis
    if "documentation" in version_report:
        display_documentation_analysis(version_report["documentation"])


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

    # Add documentation recommendations
    if "documentation" in analysis:
        doc_suggestions = analysis["documentation"]["doc_suggestions"]
        if doc_suggestions:
            console.print("\n📚 Documentation Recommendations:", style="bold magenta")
            for i, suggestion in enumerate(doc_suggestions, 1):
                console.print(f"  {i}. {suggestion}", style="white")

            console.print(
                "\n💡 Use 'fascraft docs generate' to create missing documentation",
                style="bold cyan",
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
