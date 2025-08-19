"""Tests for the dependencies command."""

from pathlib import Path
from unittest.mock import patch

from fascraft.commands.dependencies import (
    dependencies_app,
    resolve_dependencies,
    show_dependency_overview,
    show_detailed_analysis,
    show_module_health,
    show_project_health,
    show_validation_issues,
    validate_dependencies,
)
from fascraft.module_dependencies import dependency_graph


class TestDependenciesCommand:
    """Test the dependencies command structure."""

    def test_dependencies_app_exists(self):
        """Test that the dependencies app is properly configured."""
        assert dependencies_app is not None
        assert hasattr(dependencies_app, "commands")

        # Check that all expected commands exist
        command_names = [cmd.name for cmd in dependencies_app.commands]
        expected_commands = ["show", "check", "resolve", "health"]

        for expected in expected_commands:
            assert expected in command_names


class TestShowDependencyOverview:
    """Test the show dependency overview functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_show_dependency_overview(self, mock_console):
        """Test showing dependency overview."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add some modules
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

        # Show overview
        show_dependency_overview()

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify overview table was shown
        calls = mock_console.print.call_args_list
        overview_call = any("Project Dependencies" in str(call) for call in calls)
        assert overview_call

        # Verify statistics were shown
        stats_call = any("Total Modules" in str(call) for call in calls)
        assert stats_call

    @patch("fascraft.commands.dependencies.console")
    def test_show_dependency_overview_with_circular(self, mock_console):
        """Test showing overview when circular dependencies exist."""
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

        # Show overview
        show_dependency_overview()

        # Verify circular dependency warning was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        circular_warning = any(
            "Circular dependencies detected" in str(call) for call in calls
        )
        assert circular_warning


class TestShowDetailedAnalysis:
    """Test the detailed analysis functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_show_detailed_analysis(self, mock_console):
        """Test showing detailed dependency analysis."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with dependencies
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))
        dependency_graph.add_module("order", Path("modules/order"))

        # Create dependency chain
        dependency_graph.add_dependency(
            "order", "user", "import", "strong", "Order depends on user"
        )
        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )

        # Show detailed analysis
        show_detailed_analysis()

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify detailed analysis was shown
        calls = mock_console.print.call_args_list
        detailed_call = any("Detailed Analysis" in str(call) for call in calls)
        assert detailed_call

        # Verify modules with most dependencies were shown
        deps_call = any("Modules with Most Dependencies" in str(call) for call in calls)
        assert deps_call

        # Verify modules with most dependents were shown
        dependents_call = any(
            "Modules with Most Dependents" in str(call) for call in calls
        )
        assert dependents_call


class TestValidateDependencies:
    """Test the dependency validation functionality."""

    def test_validate_dependencies_no_issues(self):
        """Test validation when no issues exist."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules without issues
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))

        # Validate dependencies
        issues = validate_dependencies()

        # Should have no issues
        assert len(issues) == 0

    def test_validate_dependencies_circular(self):
        """Test validation when circular dependencies exist."""
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

        # Validate dependencies
        issues = validate_dependencies()

        # Should have circular dependency issue
        assert len(issues) >= 1

        circular_issue = next(
            (issue for issue in issues if issue["type"] == "circular"), None
        )
        assert circular_issue is not None
        assert circular_issue["severity"] == "critical"

    def test_validate_dependencies_high_count(self):
        """Test validation when modules have too many dependencies."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules with many dependencies
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))
        dependency_graph.add_module("db", Path("modules/db"))
        dependency_graph.add_module("cache", Path("modules/cache"))
        dependency_graph.add_module("logger", Path("modules/logger"))
        dependency_graph.add_module("config", Path("modules/config"))
        dependency_graph.add_module("utils", Path("modules/utils"))
        dependency_graph.add_module("models", Path("modules/models"))
        dependency_graph.add_module("schemas", Path("modules/schemas"))
        dependency_graph.add_module("services", Path("modules/services"))
        dependency_graph.add_module("api", Path("modules/api"))

        # Create many dependencies for one module
        for i in range(11):  # More than 10 dependencies
            dep_module = list(dependency_graph.modules.keys())[i]
            if dep_module != "api":
                dependency_graph.add_dependency(
                    "api",
                    dep_module,
                    "import",
                    "strong",
                    f"API depends on {dep_module}",
                )

        # Validate dependencies
        issues = validate_dependencies()

        # Should have high dependency count issue
        assert len(issues) >= 1

        high_count_issue = next(
            (issue for issue in issues if issue["type"] == "high_dependency_count"),
            None,
        )
        assert high_count_issue is not None
        assert high_count_issue["severity"] == "warning"


class TestShowValidationIssues:
    """Test the validation issues display functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_show_validation_issues(self, mock_console):
        """Test displaying validation issues."""
        # Create test issues
        issues = [
            {
                "severity": "critical",
                "title": "Circular Dependency",
                "description": "Cycle detected: user → auth → user",
                "type": "circular",
            },
            {
                "severity": "warning",
                "title": "High Dependency Count",
                "description": "Module 'api' has 15 dependencies",
                "type": "high_dependency_count",
            },
            {
                "severity": "info",
                "title": "Orphaned Modules",
                "description": "Found 3 modules with no dependents",
                "type": "orphaned",
            },
        ]

        # Show validation issues
        show_validation_issues(issues)

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify issues were displayed
        calls = mock_console.print.call_args_list
        assert len(calls) >= 3  # At least 3 issues should be shown

        # Verify severity icons were shown
        critical_call = any("🔴" in str(call) for call in calls)
        warning_call = any("🟡" in str(call) for call in calls)
        info_call = any("🔵" in str(call) for call in calls)

        assert critical_call
        assert warning_call
        assert info_call


class TestResolveDependencies:
    """Test the dependency resolution functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_resolve_dependencies_circular(self, mock_console):
        """Test resolving circular dependencies."""
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

        # Create issue for resolution
        issues = [
            {
                "type": "circular",
                "cycle": ["user", "auth", "user"],
                "severity": "critical",
                "title": "Circular Dependency",
                "description": "Cycle detected: user → auth → user",
            }
        ]

        # Resolve dependencies
        resolved = resolve_dependencies(issues, force=False)

        # Should have resolved the circular dependency
        assert len(resolved) == 1

        # Verify resolution message was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        resolution_call = any("Removed dependency" in str(call) for call in calls)
        assert resolution_call

    @patch("fascraft.commands.dependencies.console")
    def test_resolve_dependencies_high_count(self, mock_console):
        """Test resolving high dependency count issues."""
        # Create issue for resolution
        issues = [
            {
                "type": "high_dependency_count",
                "module": "api",
                "count": 15,
                "severity": "warning",
                "title": "High Dependency Count",
                "description": "Module 'api' has 15 dependencies",
            }
        ]

        # Resolve dependencies
        resolved = resolve_dependencies(issues, force=False)

        # High dependency count is not automatically resolvable
        assert len(resolved) == 0

        # Verify suggestion was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        suggestion_call = any("Consider breaking down" in str(call) for call in calls)
        assert suggestion_call


class TestShowModuleHealth:
    """Test the module health display functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_show_module_health(self, mock_console):
        """Test showing module health metrics."""
        # Clear and setup dependency graph
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Add modules
        dependency_graph.add_module("user", Path("modules/user"))
        dependency_graph.add_module("auth", Path("modules/auth"))

        # Add dependency
        dependency_graph.add_dependency(
            "user", "auth", "import", "strong", "User depends on auth"
        )

        # Show module health
        show_module_health("user")

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify health table was shown
        calls = mock_console.print.call_args_list
        health_call = any("Health Metrics" in str(call) for call in calls)
        assert health_call

        # Verify health score was shown
        score_call = any("Health Score" in str(call) for call in calls)
        assert score_call

    @patch("fascraft.commands.dependencies.console")
    def test_show_module_health_not_found(self, mock_console):
        """Test showing health for non-existent module."""
        # Clear dependency graph
        dependency_graph.modules.clear()

        # Try to show health for non-existent module
        show_module_health("nonexistent")

        # Verify error message was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any("not found in dependency graph" in str(call) for call in calls)
        assert error_call


class TestShowProjectHealth:
    """Test the project health display functionality."""

    @patch("fascraft.commands.dependencies.console")
    def test_show_project_health(self, mock_console):
        """Test showing overall project health."""
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
            "user", "auth", "import", "strong", "User depends on auth"
        )

        # Show project health
        show_project_health()

        # Verify console output was called
        mock_console.print.assert_called()

        # Verify health overview was shown
        calls = mock_console.print.call_args_list
        overview_call = any("Project Health Overview" in str(call) for call in calls)
        assert overview_call

        # Verify overall health metrics were shown
        metrics_call = any("Overall Health Metrics" in str(call) for call in calls)
        assert metrics_call

        # Verify top modules were shown
        top_modules_call = any("Top Modules by Health" in str(call) for call in calls)
        assert top_modules_call


class TestDependenciesCommandIntegration:
    """Test integration of dependencies command with main app."""

    def test_dependencies_command_registration(self):
        """Test that dependencies command is properly registered."""
        # This test verifies that the dependencies command is accessible
        # through the main fascraft app
        assert hasattr(dependencies_app, "commands")
        assert len(dependencies_app.commands) >= 4  # show, check, resolve, health

        # Verify command names
        command_names = [cmd.name for cmd in dependencies_app.commands]
        expected_commands = ["show", "check", "resolve", "health"]

        for expected in expected_commands:
            assert (
                expected in command_names
            ), f"Command '{expected}' not found in dependencies app"
