"""Module dependency analysis and management system."""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fascraft.exceptions import TemplateError


@dataclass
class ModuleDependency:
    """Represents a dependency between two modules."""

    source_module: str
    target_module: str
    dependency_type: str  # "import", "service", "model", "router"
    strength: str = "strong"  # "strong", "weak", "optional"
    description: str = ""
    file_path: Path | None = None
    line_number: int | None = None


@dataclass
class ModuleInfo:
    """Information about a module and its dependencies."""

    name: str
    path: Path
    dependencies: list[ModuleDependency] = field(default_factory=list)
    dependents: list[ModuleDependency] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    is_circular: bool = False
    circular_path: list[str] = field(default_factory=list)


class DependencyGraph:
    """Represents the dependency graph between modules."""

    def __init__(self):
        self.modules: dict[str, ModuleInfo] = {}
        self.dependency_matrix: dict[str, set[str]] = defaultdict(set)
        self.reverse_dependencies: dict[str, set[str]] = defaultdict(set)

    def add_module(
        self,
        module_name: str,
        module_path: Path,
        metadata: dict[str, Any] | None = None,
    ) -> ModuleInfo:
        """Add a module to the dependency graph."""
        if module_name not in self.modules:
            module_info = ModuleInfo(
                name=module_name, path=module_path, metadata=metadata or {}
            )
            self.modules[module_name] = module_info
            self.dependency_matrix[module_name] = set()
            self.reverse_dependencies[module_name] = set()

        return self.modules[module_name]

    def add_dependency(
        self,
        source: str,
        target: str,
        dependency_type: str = "import",
        strength: str = "strong",
        description: str = "",
        file_path: Path | None = None,
        line_number: int | None = None,
    ) -> None:
        """Add a dependency between two modules."""
        if source not in self.modules:
            raise TemplateError(
                f"Source module '{source}' not found in dependency graph"
            )

        if target not in self.modules:
            raise TemplateError(
                f"Target module '{target}' not found in dependency graph"
            )

        # Create dependency object
        dependency = ModuleDependency(
            source_module=source,
            target_module=target,
            dependency_type=dependency_type,
            strength=strength,
            description=description,
            file_path=file_path,
            line_number=line_number,
        )

        # Add to source module's dependencies
        self.modules[source].dependencies.append(dependency)

        # Add to target module's dependents
        self.modules[target].dependents.append(dependency)

        # Update dependency matrix
        self.dependency_matrix[source].add(target)
        self.reverse_dependencies[target].add(source)

    def remove_dependency(self, source: str, target: str) -> None:
        """Remove a dependency between two modules."""
        if source in self.modules and target in self.modules:
            # Remove from dependency matrix
            self.dependency_matrix[source].discard(target)
            self.reverse_dependencies[target].discard(source)

            # Remove dependency objects
            self.modules[source].dependencies = [
                d
                for d in self.modules[source].dependencies
                if not (d.source_module == source and d.target_module == target)
            ]

            self.modules[target].dependents = [
                d
                for d in self.modules[target].dependents
                if not (d.source_module == source and d.target_module == target)
            ]

    def get_dependencies(self, module_name: str) -> list[ModuleDependency]:
        """Get all dependencies for a module."""
        if module_name not in self.modules:
            return []
        return self.modules[module_name].dependencies.copy()

    def get_dependents(self, module_name: str) -> list[ModuleDependency]:
        """Get all modules that depend on this module."""
        if module_name not in self.modules:
            return []
        return self.modules[module_name].dependents.copy()

    def get_dependency_chain(self, module_name: str) -> list[str]:
        """Get the complete dependency chain for a module (topological order)."""
        if module_name not in self.modules:
            return []

        visited = set()
        temp_visited = set()
        order = []

        def dfs(node: str) -> None:
            if node in temp_visited:
                raise TemplateError(
                    f"Circular dependency detected involving module '{node}'"
                )

            if node in visited:
                return

            temp_visited.add(node)

            for dependency in self.dependency_matrix[node]:
                dfs(dependency)

            temp_visited.remove(node)
            visited.add(node)
            order.append(node)

        try:
            dfs(module_name)
            return order
        except TemplateError:
            # If circular dependency detected, return empty list
            return []

    def has_circular_dependencies(self) -> bool:
        """Check if the dependency graph has circular dependencies."""
        try:
            self._detect_circular_dependencies()
            return False
        except TemplateError:
            return True

    def _detect_circular_dependencies(self) -> None:
        """Detect circular dependencies in the graph."""
        visited = set()
        temp_visited = set()

        def dfs(node: str) -> None:
            if node in temp_visited:
                raise TemplateError(
                    f"Circular dependency detected involving module '{node}'"
                )

            if node in visited:
                return

            temp_visited.add(node)

            for dependency in self.dependency_matrix[node]:
                dfs(dependency)

            temp_visited.remove(node)
            visited.add(node)

        for module_name in self.modules:
            if module_name not in visited:
                dfs(module_name)

    def find_circular_dependencies(self) -> list[list[str]]:
        """Find all circular dependency cycles in the graph."""
        cycles = []
        visited = set()
        temp_visited = set()
        path = []

        def dfs(node: str) -> None:
            if node in temp_visited:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return

            if node in visited:
                return

            temp_visited.add(node)
            path.append(node)

            for dependency in self.dependency_matrix[node]:
                dfs(dependency)

            path.pop()
            temp_visited.remove(node)
            visited.add(node)

        for module_name in self.modules:
            if module_name not in visited:
                dfs(module_name)

        return cycles

    def get_topological_order(self) -> list[str]:
        """Get modules in topological order (dependency order)."""
        if self.has_circular_dependencies():
            raise TemplateError(
                "Cannot create topological order: circular dependencies detected"
            )

        visited = set()
        order = []

        def dfs(node: str) -> None:
            if node in visited:
                return

            visited.add(node)

            for dependency in self.dependency_matrix[node]:
                dfs(dependency)

            order.append(node)

        for module_name in self.modules:
            if module_name not in visited:
                dfs(module_name)

        return order

    def get_module_depth(self, module_name: str) -> int:
        """Get the depth of a module in the dependency graph."""
        if module_name not in self.modules:
            return 0

        visited = {}

        def dfs(node: str) -> int:
            if node in visited:
                return visited[node]

            max_depth = 0
            for dependency in self.dependency_matrix[node]:
                depth = dfs(dependency)
                max_depth = max(max_depth, depth + 1)

            visited[node] = max_depth
            return max_depth

        return dfs(module_name)

    def get_leaf_modules(self) -> list[str]:
        """Get modules that have no dependencies (leaf nodes)."""
        return [name for name, deps in self.dependency_matrix.items() if not deps]

    def get_root_modules(self) -> list[str]:
        """Get modules that are not depended upon by any other module."""
        all_dependents = set()
        for deps in self.reverse_dependencies.values():
            all_dependents.update(deps)

        return [name for name in self.modules if name not in all_dependents]

    def export_graph(self, file_path: Path) -> None:
        """Export the dependency graph to a JSON file."""
        graph_data = {
            "modules": {},
            "dependencies": [],
            "metadata": {
                "total_modules": len(self.modules),
                "has_circular_dependencies": self.has_circular_dependencies(),
            },
        }

        # Export module information
        for module_name, module_info in self.modules.items():
            graph_data["modules"][module_name] = {
                "path": str(module_info.path),
                "metadata": module_info.metadata,
                "dependency_count": len(module_info.dependencies),
                "dependent_count": len(module_info.dependents),
                "depth": self.get_module_depth(module_name),
            }

        # Export dependencies
        for module_info in self.modules.values():
            for dependency in module_info.dependencies:
                graph_data["dependencies"].append(
                    {
                        "source": dependency.source_module,
                        "target": dependency.target_module,
                        "type": dependency.dependency_type,
                        "strength": dependency.strength,
                        "description": dependency.description,
                        "file_path": (
                            str(dependency.file_path) if dependency.file_path else None
                        ),
                        "line_number": dependency.line_number,
                    }
                )

        with open(file_path, "w") as f:
            json.dump(graph_data, f, indent=2, default=str)

    def import_graph(self, file_path: Path) -> None:
        """Import a dependency graph from a JSON file."""
        with open(file_path) as f:
            graph_data = json.load(f)

        # Clear existing graph
        self.modules.clear()
        self.dependency_matrix.clear()
        self.reverse_dependencies.clear()

        # Import modules
        for module_name, module_data in graph_data["modules"].items():
            self.add_module(
                module_name, Path(module_data["path"]), module_data.get("metadata", {})
            )

        # Import dependencies
        for dep_data in graph_data["dependencies"]:
            self.add_dependency(
                source=dep_data["source"],
                target=dep_data["target"],
                dependency_type=dep_data["type"],
                strength=dep_data["strength"],
                description=dep_data["description"],
                file_path=(
                    Path(dep_data["file_path"]) if dep_data["file_path"] else None
                ),
                line_number=dep_data["line_number"],
            )


class DependencyAnalyzer:
    """Analyzes module dependencies and provides insights."""

    def __init__(self, graph: DependencyGraph):
        self.graph = graph

    def analyze_module_health(self, module_name: str) -> dict[str, Any]:
        """Analyze the health of a specific module."""
        if module_name not in self.graph.modules:
            return {"error": f"Module '{module_name}' not found"}

        dependencies = self.graph.get_dependencies(module_name)
        dependents = self.graph.get_dependents(module_name)

        # Check for circular dependencies
        circular_cycles = self.graph.find_circular_dependencies()
        module_cycles = [cycle for cycle in circular_cycles if module_name in cycle]

        health_score = 100

        # Deduct points for various issues
        if module_cycles:
            health_score -= 30
        if len(dependencies) > 10:
            health_score -= 20
        if len(dependents) == 0:
            health_score -= 10

        return {
            "module_name": module_name,
            "health_score": max(0, health_score),
            "dependency_count": len(dependencies),
            "dependent_count": len(dependents),
            "depth": self.graph.get_module_depth(module_name),
            "is_circular": bool(module_cycles),
            "circular_cycles": module_cycles,
            "strong_dependencies": len(
                [d for d in dependencies if d.strength == "strong"]
            ),
            "weak_dependencies": len([d for d in dependencies if d.strength == "weak"]),
            "optional_dependencies": len(
                [d for d in dependencies if d.strength == "optional"]
            ),
        }

    def get_dependency_statistics(self) -> dict[str, Any]:
        """Get overall dependency statistics."""
        total_modules = len(self.graph.modules)
        total_dependencies = sum(
            len(deps) for deps in self.graph.dependency_matrix.values()
        )

        # Calculate average dependencies per module
        avg_dependencies = (
            total_dependencies / total_modules if total_modules > 0 else 0
        )

        # Find modules with most dependencies
        module_dependency_counts = [
            (name, len(deps)) for name, deps in self.graph.dependency_matrix.items()
        ]
        module_dependency_counts.sort(key=lambda x: x[1], reverse=True)

        # Find modules with most dependents
        module_dependent_counts = [
            (name, len(self.graph.reverse_dependencies[name]))
            for name in self.graph.modules
        ]
        module_dependent_counts.sort(key=lambda x: x[1], reverse=True)

        return {
            "total_modules": total_modules,
            "total_dependencies": total_dependencies,
            "average_dependencies_per_module": round(avg_dependencies, 2),
            "modules_with_most_dependencies": module_dependency_counts[:5],
            "modules_with_most_dependents": module_dependent_counts[:5],
            "leaf_modules": self.graph.get_leaf_modules(),
            "root_modules": self.graph.get_root_modules(),
            "has_circular_dependencies": self.graph.has_circular_dependencies(),
            "circular_dependency_cycles": self.graph.find_circular_dependencies(),
        }

    def suggest_dependency_optimizations(self) -> list[dict[str, Any]]:
        """Suggest optimizations for the dependency graph."""
        suggestions = []

        # Check for circular dependencies
        if self.graph.has_circular_dependencies():
            cycles = self.graph.find_circular_dependencies()
            suggestions.append(
                {
                    "type": "critical",
                    "issue": "Circular Dependencies Detected",
                    "description": f"Found {len(cycles)} circular dependency cycles",
                    "cycles": cycles,
                    "recommendation": "Break circular dependencies by refactoring modules or using dependency injection",
                }
            )

        # Check for modules with too many dependencies
        for module_name, deps in self.graph.dependency_matrix.items():
            if len(deps) > 10:
                suggestions.append(
                    {
                        "type": "warning",
                        "issue": "High Dependency Count",
                        "description": f"Module '{module_name}' has {len(deps)} dependencies",
                        "recommendation": "Consider breaking down the module into smaller, more focused modules",
                    }
                )

        # Check for modules with no dependents (orphaned)
        orphaned_modules = self.graph.get_root_modules()
        if len(orphaned_modules) > 0:
            suggestions.append(
                {
                    "type": "info",
                    "issue": "Orphaned Modules",
                    "description": f"Found {len(orphaned_modules)} modules with no dependents",
                    "modules": orphaned_modules,
                    "recommendation": "Review if these modules are still needed or if they should be integrated",
                }
            )

        return suggestions


# Global dependency graph instance
dependency_graph = DependencyGraph()
dependency_analyzer = DependencyAnalyzer(dependency_graph)
