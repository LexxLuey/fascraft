"""Command for analyzing module dependencies."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from fascraft.module_dependencies import dependency_analyzer, dependency_graph

# Initialize rich console
console = Console()


def analyze_dependencies(
    path: str = ".", 
    module: str | None = None,
    export: str | None = None,
    verbose: bool = False,
) -> None:
    """🔍 Analyze module dependencies in a FastAPI project."""

    project_path = Path(path)
    if not project_path.exists():
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(f"Path '{project_path}' does not exist.", style="white")
        console.print(error_text)
        raise typer.Exit(code=1)

    # Check if dependency graph has any modules
    if not dependency_graph.modules:
        console.print("📭 No modules found in dependency graph.", style="yellow")
        console.print(
            "💡 Try generating a module with dependencies first using 'fascraft generate --depends-on'",
            style="blue",
        )
        return

    if module:
        # Analyze specific module
        if module not in dependency_graph.modules:
            error_text = Text()
            error_text.append("❌ ", style="bold red")
            error_text.append("Error: ", style="bold red")
            error_text.append(
                f"Module '{module}' not found in dependency graph.", style="white"
            )
            console.print(error_text)
            console.print(
                f"Available modules: {', '.join(dependency_graph.modules.keys())}",
                style="cyan",
            )
            raise typer.Exit(code=1)

        analyze_single_module(module)
    else:
        # Analyze entire project
        analyze_project_dependencies()

    # Export if requested
    if export:
        export_path = Path(export)
        try:
            dependency_graph.export_graph(export_path)
            success_text = Text()
            success_text.append("💾 ", style="bold green")
            success_text.append("Dependency graph exported to: ", style="white")
            success_text.append(f"{export_path}", style="bold cyan")
            console.print(success_text)
        except Exception as e:
            error_text = Text()
            error_text.append("❌ ", style="bold red")
            error_text.append("Error: ", style="bold red")
            error_text.append(
                f"Failed to export dependency graph: {str(e)}", style="white"
            )
            console.print(error_text)


def analyze_dependencies_cli(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project to analyze"),
    module: str | None = typer.Option(
        None, "--module", "-m", help="🔍 Analyze specific module only"
    ),
    export: str | None = typer.Option(
        None, "--export", help="💾 Export dependency graph to JSON file"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="📋 Show detailed dependency information"
    ),
) -> None:
    """🔍 CLI wrapper for analyzing module dependencies in a FastAPI project."""
    analyze_dependencies(path=path, module=module, export=export, verbose=verbose)


def analyze_single_module(module_name: str) -> None:
    """Analyze dependencies for a single module."""
    console.print(f"🔍 Analyzing module: {module_name}", style="bold blue")
    console.print("=" * 60, style="blue")

    # Get module health with error handling
    try:
        health = dependency_analyzer.analyze_module_health(module_name)
        
        # Check if health analysis failed
        if "error" in health:
            console.print(f"❌ Error analyzing module: {health['error']}", style="red")
            return
            
    except Exception as e:
        console.print(f"❌ Error analyzing module health: {str(e)}", style="red")
        return

    # Create health summary table
    health_table = Table(title=f"📊 {module_name} Module Health")
    health_table.add_column("Metric", style="cyan", no_wrap=True)
    health_table.add_column("Value", style="white")

    health_table.add_row("Health Score", f"{health['health_score']}/100")
    health_table.add_row("Dependencies", str(health["dependency_count"]))
    health_table.add_row("Dependents", str(health["dependent_count"]))
    health_table.add_row("Depth", str(health["depth"]))
    health_table.add_row(
        "Circular Dependencies", "Yes" if health["is_circular"] else "No"
    )

    console.print(health_table)

    # Show dependencies
    dependencies = dependency_graph.get_dependencies(module_name)
    if dependencies:
        console.print("\n📥 Dependencies:", style="bold green")
        for dep in dependencies:
            dep_text = Text()
            dep_text.append(f"  • {dep.target_module}", style="cyan")
            dep_text.append(f" ({dep.dependency_type}, {dep.strength})", style="white")
            if dep.description:
                dep_text.append(f" - {dep.description}", style="dim")
            console.print(dep_text)

    # Show dependents
    dependents = dependency_graph.get_dependents(module_name)
    if dependents:
        console.print("\n📤 Dependents:", style="bold yellow")
        for dep in dependents:
            dep_text = Text()
            dep_text.append(f"  • {dep.source_module}", style="cyan")
            dep_text.append(f" ({dep.dependency_type}, {dep.strength})", style="white")
            if dep.description:
                dep_text.append(f" - {dep.description}", style="dim")
            console.print(dep_text)

    # Show dependency chain
    chain = dependency_graph.get_dependency_chain(module_name)
    if chain:
        console.print("\n🔗 Dependency Chain:", style="bold blue")
        chain_text = " → ".join(chain)
        console.print(f"  {chain_text}", style="cyan")

    # Show circular dependencies if any
    if health["is_circular"]:
        console.print("\n🔄 Circular Dependencies:", style="bold red")
        for cycle in health["circular_cycles"]:
            cycle_text = " → ".join(cycle)
            console.print(f"  {cycle_text}", style="red")


def analyze_project_dependencies() -> None:
    """Analyze dependencies for the entire project."""
    console.print("🔍 Project Dependency Analysis", style="bold blue")
    console.print("=" * 60, style="blue")

    # Get overall statistics with error handling
    try:
        stats = dependency_analyzer.get_dependency_statistics()
    except Exception as e:
        console.print(f"❌ Error getting dependency statistics: {str(e)}", style="red")
        return

    # Create overview table
    overview_table = Table(title="📊 Project Overview")
    overview_table.add_column("Metric", style="cyan", no_wrap=True)
    overview_table.add_column("Value", style="white")

    overview_table.add_row("Total Modules", str(stats["total_modules"]))
    overview_table.add_row("Total Dependencies", str(stats["total_dependencies"]))
    overview_table.add_row(
        "Average Dependencies/Module", str(stats["average_dependencies_per_module"])
    )
    overview_table.add_row(
        "Circular Dependencies", "Yes" if stats["has_circular_dependencies"] else "No"
    )
    overview_table.add_row("Leaf Modules", str(len(stats["leaf_modules"])))
    overview_table.add_row("Root Modules", str(len(stats["root_modules"])))

    console.print(overview_table)

    # Show modules with most dependencies
    if stats["modules_with_most_dependencies"]:
        console.print("\n📥 Modules with Most Dependencies:", style="bold green")
        for module_name, count in stats["modules_with_most_dependencies"]:
            console.print(f"  • {module_name}: {count} dependencies", style="cyan")

    # Show modules with most dependents
    if stats["modules_with_most_dependents"]:
        console.print("\n📤 Modules with Most Dependents:", style="bold yellow")
        for module_name, count in stats["modules_with_most_dependents"]:
            console.print(f"  • {module_name}: {count} dependents", style="cyan")

    # Show leaf modules
    if stats["leaf_modules"]:
        console.print("\n🍃 Leaf Modules (No Dependencies):", style="bold green")
        for module_name in stats["leaf_modules"]:
            console.print(f"  • {module_name}", style="cyan")

    # Show root modules
    if stats["root_modules"]:
        console.print("\n🌳 Root Modules (No Dependents):", style="bold yellow")
        for module_name in stats["root_modules"]:
            console.print(f"  • {module_name}", style="cyan")

    # Show circular dependencies if any
    if stats["has_circular_dependencies"]:
        console.print("\n🔄 Circular Dependencies:", style="bold red")
        for cycle in stats["circular_dependency_cycles"]:
            cycle_text = " → ".join(cycle)
            console.print(f"  {cycle_text}", style="red")

    # Show optimization suggestions
    suggestions = dependency_analyzer.suggest_dependency_optimizations()
    if suggestions:
        console.print("\n💡 Optimization Suggestions:", style="bold blue")
        for suggestion in suggestions:
            suggestion_type = suggestion["type"]
            color = {"critical": "red", "warning": "yellow", "info": "blue"}.get(
                suggestion_type, "white"
            )

            suggestion_text = Text()
            suggestion_text.append(f"  {suggestion['issue']}", style=f"bold {color}")
            suggestion_text.append(f": {suggestion['description']}", style="white")
            console.print(suggestion_text)

            if "recommendation" in suggestion:
                recommendation_text = Text()
                recommendation_text.append("    💡 ", style="blue")
                recommendation_text.append(suggestion["recommendation"], style="cyan")
                console.print(recommendation_text)

    # Show dependency tree
    console.print("\n🌳 Dependency Tree:", style="bold blue")
    tree = build_dependency_tree()
    console.print(tree)


def build_dependency_tree() -> Tree:
    """Build a tree representation of the dependency graph."""
    tree = Tree("📦 Project")

    # Find root modules (no dependents)
    root_modules = dependency_graph.get_root_modules()

    for root_module in root_modules:
        # Make module name clearly visible
        module_tree = tree.add(f"🔧 {root_module}")
        add_module_dependencies(module_tree, root_module, set())

    return tree


def add_module_dependencies(parent_tree: Tree, module_name: str, visited: set) -> None:
    """Recursively add module dependencies to the tree."""
    if module_name in visited:
        return

    visited.add(module_name)
    dependencies = dependency_graph.get_dependencies(module_name)

    for dep in dependencies:
        # Make module name clearly visible in the tree
        dep_tree = parent_tree.add(f"📥 {dep.target_module}")
        # Use the same visited set to allow proper tracking
        add_module_dependencies(dep_tree, dep.target_module, visited)
