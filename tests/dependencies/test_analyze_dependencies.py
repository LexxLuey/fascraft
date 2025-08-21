"""Tests for the analyze-dependencies command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import click
import pytest
import typer

from fascraft.commands.analyze_dependencies import (
    add_module_dependencies,
    analyze_dependencies,
    analyze_project_dependencies,
    analyze_single_module,
    build_dependency_tree,
)
from fascraft.module_dependencies import dependency_graph


class TestAnalyzeDependenciesCommand:
    """Test the analyze-dependencies command."""

    @pytest.fixture
    def mock_project_path(self, tmp_path):
        """Create a mock project path."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()
        return project_path

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_dependencies_no_modules(self, mock_console, mock_project_path):
        """Test analyzing dependencies when no modules exist."""
        # Clear dependency graph
        dependency_graph.modules.clear()

        # Analyze dependencies
        analyze_dependencies(str(mock_project_path))

        # Verify appropriate message was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        no_modules_call = any(
            "No modules found in dependency graph" in str(call) for call in calls
        )
        assert no_modules_call

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_dependencies_path_not_found(self, mock_console):
        """Test analyzing dependencies with non-existent path."""
        with pytest.raises((typer.Exit, click.exceptions.Exit)):
            analyze_dependencies("nonexistent_path")

        # Verify error message
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Path 'nonexistent_path' does not exist" in str(call) for call in calls
        )
        assert error_call

    @patch("fascraft.commands.analyze_dependencies.console")
    @patch("fascraft.commands.analyze_dependencies.dependency_graph.export_graph")
    def test_analyze_dependencies_with_export(
        self, mock_export, mock_console, mock_project_path
    ):
        """Test analyzing dependencies with export functionality."""
        # Add some modules to dependency graph
        dependency_graph.modules.clear()
        dependency_graph.add_module("user", mock_project_path / "user")
        dependency_graph.add_module("auth", mock_project_path / "auth")

        # Mock successful export
        mock_export.return_value = None

        # Analyze with export
        analyze_dependencies(str(mock_project_path), export="deps.json")

        # Verify export was called
        mock_export.assert_called_once_with(Path("deps.json"))

        # Verify success message
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        success_call = any(
            "Dependency graph exported to" in str(call) for call in calls
        )
        assert success_call

    @patch("fascraft.commands.analyze_dependencies.console")
    @patch("fascraft.commands.analyze_dependencies.dependency_graph.export_graph")
    def test_analyze_dependencies_export_failure(
        self, mock_export, mock_console, mock_project_path
    ):
        """Test analyzing dependencies when export fails."""
        # Add some modules to dependency graph
        dependency_graph.modules.clear()
        dependency_graph.add_module("user", mock_project_path / "user")

        # Mock export failure
        mock_export.side_effect = Exception("Export failed")

        # Analyze with export
        analyze_dependencies(str(mock_project_path), export="deps.json")

        # Verify error message was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Failed to export dependency graph" in str(call) for call in calls
        )
        assert error_call


class TestAnalyzeSingleModule:
    """Test analyzing a single module."""

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_single_module(self, mock_console):
        """Test analyzing a single module's dependencies."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))
        dependency_graph.add_module("order", Path("modules/order"))

        # Add dependencies
        dependency_graph.add_dependency(
            "order", "user", "import", "strong", "Order depends on user"
        )
        dependency_graph.add_dependency(
            "order", "auth", "import", "strong", "Order depends on auth"
        )

        # Analyze single module
        analyze_single_module("order")

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify health table was shown
        calls = mock_console.print.call_args_list
        # Check if a Table object was printed (Rich Table objects will be passed as arguments)
        table_call = any(
            len(call[0]) > 0
            and hasattr(call[0][0], "title")
            and "📊 order Module Health" in str(call[0][0].title)
            for call in calls
            if call[0] and len(call[0]) > 0
        )
        assert (
            table_call
        ), f"Expected Table with '📊 order Module Health' title in console calls. Actual calls: {[str(call) for call in calls]}"

        # Verify dependencies were shown
        deps_call = any("📥 Dependencies:" in str(call) for call in calls)
        assert deps_call

        # Verify dependency chain was shown
        chain_call = any("🔗 Dependency Chain:" in str(call) for call in calls)
        assert chain_call


class TestAnalyzeProjectDependencies:
    """Test analyzing project-wide dependencies."""

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_project_dependencies(self, mock_console):
        """Test analyzing project dependencies."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with dependencies
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))
        dependency_graph.add_module("order", Path("modules/order"))
        dependency_graph.add_module("db", Path("modules/db"))

        # Create dependency chain: order -> user -> auth -> db
        dependency_graph.add_dependency(
            "order", "user", "import", "strong", "Order depends on user"
        )
        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )
        dependency_graph.add_dependency(
            "auth", "db", "import", "strong", "Auth depends on db"
        )

        # Analyze project dependencies
        analyze_project_dependencies()

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify overview table was shown
        calls = mock_console.print.call_args_list
        # Check if a Table object with the expected title was printed
        overview_call = any(
            len(call[0]) > 0
            and hasattr(call[0][0], "title")
            and "📊 Project Overview" in str(call[0][0].title)
            for call in calls
            if call[0] and len(call[0]) > 0
        )
        assert (
            overview_call
        ), f"Expected Table with '📊 Project Overview' title. Actual calls: {[str(call) for call in calls]}"

        # Verify statistics were shown
        # Since Rich Table objects are printed, we can verify that a Table object was printed
        # The "Total Modules" text is inside the Table object
        table_call = any(
            len(call[0]) > 0 and "rich.table.Table" in str(call[0][0])
            for call in calls
            if call[0] and len(call[0]) > 0
        )
        assert (
            table_call
        ), f"Expected Rich Table object to be printed. Actual calls: {[str(call) for call in calls]}"

        # Verify leaf and root modules were identified
        leaf_call = any("🍃 Leaf Modules" in str(call) for call in calls)
        assert leaf_call

        root_call = any("🌳 Root Modules" in str(call) for call in calls)
        assert root_call

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_project_dependencies_with_circular(self, mock_console):
        """Test analyzing project dependencies with circular dependencies."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with circular dependency
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))

        # Create circular dependency
        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )
        dependency_graph.add_dependency(
            "auth", "user", "import", "strong", "Auth depends on user"
        )

        # Analyze project dependencies
        analyze_project_dependencies()

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify circular dependencies were shown
        calls = mock_console.print.call_args_list
        circular_call = any("🔄 Circular Dependencies" in str(call) for call in calls)
        assert circular_call

        # Verify optimization suggestions were shown
        suggestions_call = any(
            "💡 Optimization Suggestions" in str(call) for call in calls
        )
        assert suggestions_call


class TestDependencyTree:
    """Test building dependency trees."""

    def test_build_dependency_tree_simple(self):
        """Test building a simple dependency tree."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with simple dependency chain
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))

        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )

        # Build tree
        tree = build_dependency_tree()

        # Verify tree structure
        assert tree.label == "📦 Project"
        assert len(tree.children) == 1  # Only user module (root)

        user_node = tree.children[0]
        assert "user" in user_node.label
        assert len(user_node.children) == 1  # auth dependency

        auth_node = user_node.children[0]
        assert "auth" in auth_node.label
        assert len(auth_node.children) == 0  # No further dependencies

    def test_build_dependency_tree_complex(self):
        """Test building a complex dependency tree."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with complex dependency chain
        dependency_graph.add_module("order", Path("modules/order"))
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))
        dependency_graph.add_module("db", Path("modules/db"))

        # Create dependency chain: order -> user -> auth -> db
        dependency_graph.add_dependency(
            "order", "user", "import", "strong", "Order depends on user"
        )
        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )
        dependency_graph.add_dependency(
            "auth", "db", "import", "strong", "Auth depends on db"
        )

        # Build tree
        tree = build_dependency_tree()

        # Verify tree structure
        assert tree.label == "📦 Project"
        assert len(tree.children) == 1  # Only order module (root)

        order_node = tree.children[0]
        assert "order" in order_node.label
        assert len(order_node.children) == 1  # user dependency

        user_node = order_node.children[0]
        assert "user" in user_node.label
        assert len(user_node.children) == 1  # auth dependency

        auth_node = user_node.children[0]
        assert "auth" in auth_node.label
        assert len(auth_node.children) == 1  # db dependency

        db_node = auth_node.children[0]
        assert "db" in db_node.label
        assert len(db_node.children) == 0  # No further dependencies

    def test_add_module_dependencies_recursive(self):
        """Test recursively adding module dependencies."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))

        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )

        # Create a mock tree node
        mock_tree = MagicMock()
        visited = set()

        # Add dependencies recursively
        add_module_dependencies(mock_tree, "user", visited)

        # Verify tree was populated
        assert mock_tree.add.called

        # Verify visited set was updated
        assert "user" in visited
        assert "auth" in visited


class TestModuleSpecificAnalysis:
    """Test analyzing specific modules."""

    @pytest.fixture
    def mock_project_path(self, tmp_path):
        """Create a mock project path."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()
        return project_path

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_dependencies_specific_module(
        self, mock_console, mock_project_path
    ):
        """Test analyzing a specific module."""
        # Add modules to dependency graph
        dependency_graph.modules.clear()
        dependency_graph.add_module("user", mock_project_path / "user")
        dependency_graph.add_module("auth", mock_project_path / "auth")

        # Analyze specific module
        analyze_dependencies(str(mock_project_path), module="user")

        # Verify single module analysis was called
        mock_console.print.assert_called()

        # Verify module-specific output
        calls = mock_console.print.call_args_list
        module_call = any("🔍 Analyzing module: user" in str(call) for call in calls)
        assert module_call

    @patch("fascraft.commands.analyze_dependencies.console")
    def test_analyze_dependencies_module_not_found(
        self, mock_console, mock_project_path
    ):
        """Test analyzing a non-existent module."""
        # Add some modules to dependency graph
        dependency_graph.modules.clear()
        dependency_graph.add_module("user", mock_project_path / "user")

        # Try to analyze non-existent module
        with pytest.raises((typer.Exit, click.exceptions.Exit)):
            analyze_dependencies(str(mock_project_path), module="nonexistent")

        # Verify error message
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Module 'nonexistent' not found" in str(call) for call in calls
        )
        assert error_call

        # Verify available modules were shown
        available_call = any("Available modules:" in str(call) for call in calls)
        assert available_call
