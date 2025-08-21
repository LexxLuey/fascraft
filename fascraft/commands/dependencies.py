"""Command for managing module dependencies."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from fascraft.module_dependencies import dependency_analyzer, dependency_graph

# Initialize rich console
console = Console()

# Create sub-app for dependencies
dependencies_app = typer.Typer(
    help="🔗 Manage module dependencies in your FastAPI project", name="dependencies"
)


@dependencies_app.command()
def show(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="📋 Show detailed dependency information"
    ),
) -> None:
    """🔍 Visualize and analyze module dependencies."""

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

    # Show dependency overview
    show_dependency_overview()

    # Show detailed analysis if verbose
    if verbose:
        show_detailed_analysis()
        show_dependency_tree()


@dependencies_app.command()
def check(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project"),
    strict: bool = typer.Option(
        False, "--strict", help="🔒 Fail on warnings (not just errors)"
    ),
) -> None:
    """✅ Validate dependencies and check for issues."""

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

    # Perform dependency validation
    issues = validate_dependencies()

    if not issues:
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append("All dependencies are valid!", style="bold white")
        console.print(success_text)
        return

    # Show validation issues
    show_validation_issues(issues)

    # Exit with error code if there are critical issues
    critical_issues = [issue for issue in issues if issue["severity"] == "critical"]
    if critical_issues or (strict and issues):
        raise typer.Exit(code=1)


@dependencies_app.command()
def resolve(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project"),
    auto: bool = typer.Option(
        False, "--auto", help="🤖 Automatically resolve issues without prompting"
    ),
    force: bool = typer.Option(
        False, "--force", help="💪 Force resolution even for risky operations"
    ),
) -> None:
    """🔧 Automatically resolve dependency issues."""

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

    # Get current issues
    issues = validate_dependencies()

    if not issues:
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append("No dependency issues to resolve!", style="bold white")
        console.print(success_text)
        return

    # Show what will be resolved
    console.print("🔧 Dependency Resolution Plan", style="bold blue")
    console.print("=" * 50, style="blue")

    for issue in issues:
        severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[
            issue["severity"]
        ]
        console.print(
            f"{severity_icon} {issue['title']}: {issue['description']}", style="white"
        )

    # Perform resolution
    resolved_issues = resolve_dependencies(issues, force)

    # Show results
    show_resolution_results(resolved_issues)


@dependencies_app.command()
def health(
    path: str = typer.Option(".", help="📁 The path to the FastAPI project"),
    module: str | None = typer.Option(
        None, "--module", "-m", help="🔍 Check health of specific module"
    ),
) -> None:
    """🏥 Show dependency health metrics and scores."""

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
        show_module_health(module)
    else:
        show_project_health()


# Helper functions


def show_dependency_overview() -> None:
    """Show an overview of the dependency graph."""
    console.print("🔗 Dependency Overview", style="bold blue")
    console.print("=" * 50, style="blue")

    stats = dependency_analyzer.get_dependency_statistics()

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

    # Show quick health summary
    if stats["has_circular_dependencies"]:
        warning_text = Text()
        warning_text.append("⚠️  ", style="bold red")
        warning_text.append(
            "Critical: Circular dependencies detected!", style="bold red"
        )
        console.print(warning_text)
    elif stats["total_dependencies"] > stats["total_modules"] * 2:
        warning_text = Text()
        warning_text.append("⚠️  ", style="bold yellow")
        warning_text.append("Warning: High dependency complexity", style="bold yellow")
        console.print(warning_text)
    else:
        success_text = Text()
        success_text.append("✅ ", style="bold green")
        success_text.append("Dependencies look healthy", style="bold green")
        console.print(success_text)


def show_detailed_analysis() -> None:
    """Show detailed dependency analysis."""
    console.print("\n🔍 Detailed Analysis", style="bold blue")
    console.print("=" * 50, style="blue")

    stats = dependency_analyzer.get_dependency_statistics()

    # Show modules with most dependencies
    if stats["modules_with_most_dependencies"]:
        console.print("📥 Modules with Most Dependencies:", style="bold green")
        for module_name, count in stats["modules_with_most_dependencies"]:
            console.print(f"  • {module_name}: {count} dependencies", style="cyan")

    # Show modules with most dependents
    if stats["modules_with_most_dependents"]:
        console.print("\n📤 Modules with Most Dependents:", style="bold yellow")
        for module_name, count in stats["modules_with_most_dependents"]:
            console.print(f"  • {module_name}: {count} dependents", style="cyan")

    # Show leaf and root modules
    if stats["leaf_modules"]:
        console.print("\n🍃 Leaf Modules (No Dependencies):", style="bold green")
        for module_name in stats["leaf_modules"]:
            console.print(f"  • {module_name}", style="cyan")

    if stats["root_modules"]:
        console.print("\n🌳 Root Modules (No Dependents):", style="bold yellow")
        for module_name in stats["root_modules"]:
            console.print(f"  • {module_name}", style="cyan")


def show_dependency_tree() -> None:
    """Show dependency tree visualization."""
    console.print("\n🌳 Dependency Tree", style="bold blue")
    console.print("=" * 50, style="blue")

    tree = build_dependency_tree()
    console.print(tree)


def build_dependency_tree() -> Tree:
    """Build a tree representation of the dependency graph."""
    tree = Tree("📦 Project")

    # Find root modules (no dependents)
    root_modules = dependency_graph.get_root_modules()

    for root_module in root_modules:
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
        dep_tree = parent_tree.add(f"📥 {dep.target_module}")
        add_module_dependencies(dep_tree, dep.target_module, visited.copy())


def validate_dependencies() -> list:
    """Validate dependencies and return list of issues."""
    issues = []

    # Check for circular dependencies
    if dependency_graph.has_circular_dependencies():
        cycles = dependency_graph.find_circular_dependencies()
        for cycle in cycles:
            issues.append(
                {
                    "severity": "critical",
                    "title": "Circular Dependency",
                    "description": f"Cycle detected: {' → '.join(cycle)}",
                    "cycle": cycle,
                    "type": "circular",
                }
            )

    # Check for modules with too many dependencies
    stats = dependency_analyzer.get_dependency_statistics()
    for module_name, count in stats["modules_with_most_dependencies"]:
        if count > 10:
            issues.append(
                {
                    "severity": "warning",
                    "title": "High Dependency Count",
                    "description": f"Module '{module_name}' has {count} dependencies",
                    "module": module_name,
                    "count": count,
                    "type": "high_dependency_count",
                }
            )

    # Check for orphaned modules
    orphaned_modules = stats["root_modules"]
    if len(orphaned_modules) > 0:
        issues.append(
            {
                "severity": "info",
                "title": "Orphaned Modules",
                "description": f"Found {len(orphaned_modules)} modules with no dependents",
                "modules": orphaned_modules,
                "type": "orphaned",
            }
        )

    return issues


def show_validation_issues(issues: list) -> None:
    """Display validation issues in a formatted way."""
    console.print(f"\n🔍 Found {len(issues)} dependency issue(s):", style="bold blue")
    console.print("=" * 50, style="blue")

    for issue in issues:
        severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[
            issue["severity"]
        ]
        severity_color = {"critical": "red", "warning": "yellow", "info": "blue"}[
            issue["severity"]
        ]

        issue_text = Text()
        issue_text.append(f"{severity_icon} ", style=f"bold {severity_color}")
        issue_text.append(f"{issue['title']}: ", style=f"bold {severity_color}")
        issue_text.append(issue["description"], style="white")
        console.print(issue_text)


def resolve_dependencies(issues: list, force: bool) -> list:
    """Attempt to resolve dependency issues."""
    resolved_issues = []

    for issue in issues:
        if issue["type"] == "circular":
            resolved = resolve_circular_dependency(issue, force)
            if resolved:
                resolved_issues.append(issue)

        elif issue["type"] == "high_dependency_count":
            resolved = resolve_high_dependency_count(issue, force)
            if resolved:
                resolved_issues.append(issue)

    return resolved_issues


def resolve_circular_dependency(issue: dict, force: bool) -> bool:
    """Attempt to resolve a circular dependency."""
    cycle = issue["cycle"]

    console.print(
        f"🔄 Attempting to resolve circular dependency: {' → '.join(cycle)}",
        style="yellow",
    )

    # Simple resolution: remove the last dependency in the cycle
    if len(cycle) >= 2:
        source = cycle[-2]
        target = cycle[-1]

        try:
            dependency_graph.remove_dependency(source, target)
            console.print(
                f"✅ Removed dependency {source} → {target} to break cycle",
                style="green",
            )
            return True
        except Exception as e:
            console.print(
                f"❌ Failed to resolve circular dependency: {str(e)}", style="red"
            )
            return False

    return False


def resolve_high_dependency_count(issue: dict, force: bool) -> bool:
    """Attempt to resolve high dependency count."""
    module_name = issue["module"]
    count = issue["count"]

    console.print(f"📥 Module '{module_name}' has {count} dependencies", style="yellow")
    console.print(
        "💡 Consider breaking down this module into smaller, focused modules",
        style="blue",
    )

    # This is more of a suggestion than an automatic fix
    return False


def show_resolution_results(resolved_issues: list) -> None:
    """Show the results of dependency resolution."""
    if not resolved_issues:
        console.print("❌ No issues were automatically resolved.", style="yellow")
        return

    console.print(
        f"\n✅ Successfully resolved {len(resolved_issues)} issue(s):",
        style="bold green",
    )
    console.print("=" * 50, style="blue")

    for issue in resolved_issues:
        console.print(f"✅ {issue['title']}: {issue['description']}", style="green")


def show_module_health(module_name: str) -> None:
    """Show health metrics for a specific module."""
    if module_name not in dependency_graph.modules:
        error_text = Text()
        error_text.append("❌ ", style="bold red")
        error_text.append("Error: ", style="bold red")
        error_text.append(
            f"Module '{module_name}' not found in dependency graph.", style="white"
        )
        console.print(error_text)
        return

    console.print(f"🏥 Module Health: {module_name}", style="bold blue")
    console.print("=" * 50, style="blue")

    health = dependency_analyzer.analyze_module_health(module_name)

    # Create health table
    health_table = Table(title=f"📊 {module_name} Health Metrics")
    health_table.add_column("Metric", style="cyan", no_wrap=True)
    health_table.add_column("Value", style="white")
    health_table.add_column("Status", style="white")

    # Health score with color coding
    score = health["health_score"]
    if score >= 80:
        status = "🟢 Excellent"
    elif score >= 60:
        status = "🟡 Good"
    else:
        status = "🔴 Poor"

    health_table.add_row("Health Score", f"{score}/100", status)
    health_table.add_row("Dependencies", str(health["dependency_count"]), "")
    health_table.add_row("Dependents", str(health["dependent_count"]), "")
    health_table.add_row("Depth", str(health["depth"]), "")
    health_table.add_row(
        "Circular Dependencies", "Yes" if health["is_circular"] else "No", ""
    )

    console.print(health_table)

    # Show recommendations
    if score < 70:
        console.print("\n💡 Recommendations:", style="bold blue")
        if health["is_circular"]:
            console.print(
                "  • Break circular dependencies by refactoring modules", style="cyan"
            )
        if health["dependency_count"] > 10:
            console.print(
                "  • Consider breaking down this module into smaller modules",
                style="cyan",
            )
        if health["dependent_count"] == 0:
            console.print(
                "  • This module may be unused - consider removing it", style="cyan"
            )


def show_project_health() -> None:
    """Show overall project health metrics."""
    console.print("🏥 Project Health Overview", style="bold blue")
    console.print("=" * 50, style="blue")

    stats = dependency_analyzer.get_dependency_statistics()

    # Calculate overall health score
    total_health = 0
    module_count = 0

    for module_name in dependency_graph.modules:
        try:
            health = dependency_analyzer.analyze_module_health(module_name)
            total_health += health["health_score"]
            module_count += 1
        except Exception:
            pass

    overall_health = total_health / module_count if module_count > 0 else 0

    # Create health summary table
    health_table = Table(title="📊 Overall Health Metrics")
    health_table.add_column("Metric", style="cyan", no_wrap=True)
    health_table.add_column("Value", style="white")
    health_table.add_column("Status", style="white")

    # Overall health score
    if overall_health >= 80:
        status = "🟢 Excellent"
    elif overall_health >= 60:
        status = "🟡 Good"
    else:
        status = "🔴 Poor"

    health_table.add_row("Overall Health", f"{overall_health:.1f}/100", status)
    health_table.add_row("Total Modules", str(stats["total_modules"]), "")
    health_table.add_row("Total Dependencies", str(stats["total_dependencies"]), "")
    health_table.add_row(
        "Circular Dependencies",
        "Yes" if stats["has_circular_dependencies"] else "No",
        "",
    )
    health_table.add_row(
        "Complexity Score", f"{stats['average_dependencies_per_module']:.2f}", ""
    )

    console.print(health_table)

    # Show top modules by health
    console.print("\n🏆 Top Modules by Health:", style="bold blue")

    module_health_scores = []
    for module_name in dependency_graph.modules:
        try:
            health = dependency_analyzer.analyze_module_health(module_name)
            module_health_scores.append((module_name, health["health_score"]))
        except Exception:
            pass

    # Sort by health score (descending)
    module_health_scores.sort(key=lambda x: x[1], reverse=True)

    for i, (module_name, score) in enumerate(module_health_scores[:5]):
        rank = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
        console.print(f"  {rank} {module_name}: {score}/100", style="cyan")
