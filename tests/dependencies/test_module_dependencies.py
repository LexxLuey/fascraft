"""Tests for the module dependencies system."""

from pathlib import Path

import pytest

from fascraft.exceptions import TemplateError
from fascraft.module_dependencies import (
    DependencyAnalyzer,
    DependencyGraph,
    ModuleDependency,
    ModuleInfo,
    dependency_analyzer,
    dependency_graph,
)


class TestModuleDependency:
    """Test the ModuleDependency dataclass."""

    def test_module_dependency_creation(self):
        """Test creating a ModuleDependency instance."""
        dependency = ModuleDependency(
            source_module="user",
            target_module="auth",
            dependency_type="import",
            strength="strong",
            description="User module imports auth utilities",
            file_path=Path("user/models.py"),
            line_number=15,
        )

        assert dependency.source_module == "user"
        assert dependency.target_module == "auth"
        assert dependency.dependency_type == "import"
        assert dependency.strength == "strong"
        assert dependency.description == "User module imports auth utilities"
        assert dependency.file_path == Path("user/models.py")
        assert dependency.line_number == 15

    def test_module_dependency_defaults(self):
        """Test ModuleDependency with default values."""
        dependency = ModuleDependency(
            source_module="user", target_module="auth", dependency_type="import"
        )

        assert dependency.source_module == "user"
        assert dependency.target_module == "auth"
        assert dependency.dependency_type == "import"
        assert dependency.strength == "strong"
        assert dependency.description == ""
        assert dependency.file_path is None
        assert dependency.line_number is None


class TestModuleInfo:
    """Test the ModuleInfo dataclass."""

    def test_module_info_creation(self):
        """Test creating a ModuleInfo instance."""
        module_info = ModuleInfo(
            name="user",
            path=Path("modules/user"),
            metadata={"version": "1.0", "author": "dev"},
        )

        assert module_info.name == "user"
        assert module_info.path == Path("modules/user")
        assert module_info.metadata == {"version": "1.0", "author": "dev"}
        assert module_info.dependencies == []
        assert module_info.dependents == []
        assert module_info.is_circular is False
        assert module_info.circular_path == []

    def test_module_info_defaults(self):
        """Test ModuleInfo with default values."""
        module_info = ModuleInfo(name="user", path=Path("modules/user"))

        assert module_info.name == "user"
        assert module_info.path == Path("modules/user")
        assert module_info.metadata == {}
        assert module_info.dependencies == []
        assert module_info.dependents == []


class TestDependencyGraph:
    """Test the DependencyGraph class."""

    def test_dependency_graph_initialization(self):
        """Test DependencyGraph initialization."""
        graph = DependencyGraph()

        assert graph.modules == {}
        assert graph.dependency_matrix == {}
        assert graph.reverse_dependencies == {}

    def test_add_module(self):
        """Test adding a module to the graph."""
        graph = DependencyGraph()
        module_info = graph.add_module("user", Path("modules/user"))

        assert "user" in graph.modules
        assert graph.modules["user"] == module_info
        assert module_info.name == "user"
        assert module_info.path == Path("modules/user")
        assert "user" in graph.dependency_matrix
        assert "user" in graph.reverse_dependencies

    def test_add_module_duplicate(self):
        """Test adding a duplicate module returns existing module."""
        graph = DependencyGraph()
        module1 = graph.add_module("user", Path("modules/user"))
        module2 = graph.add_module("user", Path("modules/user"))

        assert module1 is module2
        assert len(graph.modules) == 1

    def test_add_dependency(self):
        """Test adding a dependency between modules."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))

        graph.add_dependency("user", "auth", "import", "strong", "User imports auth")

        # Check dependency matrix
        assert "auth" in graph.dependency_matrix["user"]

        # Check reverse dependencies
        assert "user" in graph.reverse_dependencies["auth"]

        # Check dependency objects
        user_deps = graph.modules["user"].dependencies
        assert len(user_deps) == 1
        assert user_deps[0].source_module == "user"
        assert user_deps[0].target_module == "auth"
        assert user_deps[0].dependency_type == "import"
        assert user_deps[0].strength == "strong"
        assert user_deps[0].description == "User imports auth"

        # Check dependents
        auth_dependents = graph.modules["auth"].dependents
        assert len(auth_dependents) == 1
        assert auth_dependents[0].source_module == "user"
        assert auth_dependents[0].target_module == "auth"

    def test_add_dependency_source_not_found(self):
        """Test adding dependency with non-existent source module."""
        graph = DependencyGraph()
        graph.add_module("auth", Path("modules/auth"))

        with pytest.raises(TemplateError, match="Source module 'user' not found"):
            graph.add_dependency("user", "auth")

    def test_add_dependency_target_not_found(self):
        """Test adding dependency with non-existent target module."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))

        with pytest.raises(TemplateError, match="Target module 'auth' not found"):
            graph.add_dependency("user", "auth")

    def test_remove_dependency(self):
        """Test removing a dependency."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_dependency("user", "auth")

        # Verify dependency exists
        assert "auth" in graph.dependency_matrix["user"]
        assert "user" in graph.reverse_dependencies["auth"]

        # Remove dependency
        graph.remove_dependency("user", "auth")

        # Verify dependency is removed
        assert "auth" not in graph.dependency_matrix["user"]
        assert "user" not in graph.reverse_dependencies["auth"]
        assert len(graph.modules["user"].dependencies) == 0
        assert len(graph.modules["auth"].dependents) == 0

    def test_get_dependencies(self):
        """Test getting dependencies for a module."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("user", "db")

        dependencies = graph.get_dependencies("user")
        assert len(dependencies) == 2

        target_modules = [dep.target_module for dep in dependencies]
        assert "auth" in target_modules
        assert "db" in target_modules

    def test_get_dependents(self):
        """Test getting dependents for a module."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("db", "auth")

        dependents = graph.get_dependents("auth")
        assert len(dependents) == 2

        source_modules = [dep.source_module for dep in dependents]
        assert "user" in source_modules
        assert "db" in source_modules

    def test_simple_dependency_chain(self):
        """Test getting dependency chain for a simple graph."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        chain = graph.get_dependency_chain("user")
        # Should be in dependency order: db (leaf), auth, user (root)
        assert len(chain) == 3
        assert chain[0] == "db"  # Leaf node
        assert chain[1] == "auth"  # Middle node
        assert chain[2] == "user"  # Root node

    def test_circular_dependency_detection(self):
        """Test detecting circular dependencies."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))

        # Create circular dependency: user -> auth -> user
        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "user")

        assert graph.has_circular_dependencies() is True

        # Should raise error when trying to get topological order
        with pytest.raises(TemplateError, match="Cannot create topological order"):
            graph.get_topological_order()

    def test_find_circular_dependencies(self):
        """Test finding circular dependency cycles."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        # Create circular dependency: user -> auth -> db -> user
        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")
        graph.add_dependency("db", "user")

        cycles = graph.find_circular_dependencies()
        assert len(cycles) == 1
        assert len(cycles[0]) == 4  # user -> auth -> db -> user

    def test_get_topological_order(self):
        """Test getting topological order for acyclic graph."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        order = graph.get_topological_order()
        assert len(order) == 3

        # Check that dependencies come before dependents
        db_index = order.index("db")
        auth_index = order.index("auth")
        user_index = order.index("user")

        assert db_index < auth_index < user_index

    def test_get_module_depth(self):
        """Test getting module depth in dependency graph."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        assert graph.get_module_depth("db") == 0  # Leaf node
        assert graph.get_module_depth("auth") == 1  # Depends on db
        assert graph.get_module_depth("user") == 2  # Depends on auth

    def test_get_leaf_modules(self):
        """Test getting leaf modules (no dependencies)."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        leaf_modules = graph.get_leaf_modules()
        assert "db" in leaf_modules
        assert "user" not in leaf_modules
        assert "auth" not in leaf_modules

    def test_get_root_modules(self):
        """Test getting root modules (no dependents)."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        root_modules = graph.get_root_modules()
        assert "user" in root_modules
        assert "auth" not in root_modules
        assert "db" not in root_modules


class TestDependencyAnalyzer:
    """Test the DependencyAnalyzer class."""

    def test_analyze_module_health(self):
        """Test analyzing module health."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        analyzer = DependencyAnalyzer(graph)
        health = analyzer.analyze_module_health("user")

        assert health["module_name"] == "user"
        assert health["dependency_count"] == 1
        assert health["dependent_count"] == 0
        assert health["depth"] == 2
        assert health["is_circular"] is False
        assert health["health_score"] == 90  # 100 - 10 (no dependents)

    def test_analyze_module_health_circular(self):
        """Test analyzing module health with circular dependencies."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "user")

        analyzer = DependencyAnalyzer(graph)
        health = analyzer.analyze_module_health("user")

        assert health["is_circular"] is True
        assert health["health_score"] == 70  # 100 - 30 (circular)

    def test_get_dependency_statistics(self):
        """Test getting dependency statistics."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))
        graph.add_module("db", Path("modules/db"))

        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "db")

        analyzer = DependencyAnalyzer(graph)
        stats = analyzer.get_dependency_statistics()

        assert stats["total_modules"] == 3
        assert stats["total_dependencies"] == 2
        assert stats["average_dependencies_per_module"] == 0.67
        assert stats["has_circular_dependencies"] is False
        assert len(stats["leaf_modules"]) == 1
        assert len(stats["root_modules"]) == 1

    def test_suggest_dependency_optimizations(self):
        """Test suggesting dependency optimizations."""
        graph = DependencyGraph()
        graph.add_module("user", Path("modules/user"))
        graph.add_module("auth", Path("modules/auth"))

        # Create circular dependency
        graph.add_dependency("user", "auth")
        graph.add_dependency("auth", "user")

        analyzer = DependencyAnalyzer(graph)
        suggestions = analyzer.suggest_dependency_optimizations()

        # Should have suggestion for circular dependency
        circular_suggestion = next(
            (s for s in suggestions if s["issue"] == "Circular Dependencies Detected"),
            None,
        )
        assert circular_suggestion is not None
        assert circular_suggestion["type"] == "critical"


class TestGlobalInstances:
    """Test the global dependency graph and analyzer instances."""

    def test_global_dependency_graph(self):
        """Test that global dependency graph is available."""
        assert dependency_graph is not None
        assert isinstance(dependency_graph, DependencyGraph)

    def test_global_dependency_analyzer(self):
        """Test that global dependency analyzer is available."""
        assert dependency_analyzer is not None
        assert isinstance(dependency_analyzer, DependencyAnalyzer)
        assert dependency_analyzer.graph == dependency_graph
