"""Tests for the enhanced generate command with dependency support."""

from unittest.mock import MagicMock, patch

import pytest

from fascraft.commands.generate import (
    generate_dependency_imports,
    generate_dependency_injections,
    generate_module,
)
from fascraft.module_dependencies import dependency_graph


class TestDependencyHelperFunctions:
    """Test the dependency helper functions."""

    def test_generate_dependency_imports_empty(self):
        """Test generating imports with no dependencies."""
        imports = generate_dependency_imports([])
        assert imports == ""

    def test_generate_dependency_imports_single(self):
        """Test generating imports with single dependency."""
        imports = generate_dependency_imports(["user"])
        expected = "from user import models as user_models\nfrom user import services as user_services\nfrom user import schemas as user_schemas"
        assert imports == expected

    def test_generate_dependency_imports_multiple(self):
        """Test generating imports with multiple dependencies."""
        imports = generate_dependency_imports(["user", "auth"])
        expected = "from user import models as user_models\nfrom user import services as user_services\nfrom user import schemas as user_schemas\nfrom auth import models as auth_models\nfrom auth import services as auth_services\nfrom auth import schemas as auth_schemas"
        assert imports == expected

    def test_generate_dependency_injections_empty(self):
        """Test generating injections with no dependencies."""
        injections = generate_dependency_injections([])
        assert injections == ""

    def test_generate_dependency_injections_single(self):
        """Test generating injections with single dependency."""
        injections = generate_dependency_injections(["user"])
        assert injections == "user_service: UserService"

    def test_generate_dependency_injections_multiple(self):
        """Test generating injections with multiple dependencies."""
        injections = generate_dependency_injections(["user", "auth"])
        assert injections == "user_service: UserService, auth_service: AuthService"


class TestEnhancedGenerateCommand:
    """Test the enhanced generate command with dependency support."""

    @pytest.fixture
    def mock_project_path(self, tmp_path):
        """Create a mock FastAPI project structure."""
        project_path = tmp_path / "test_project"
        project_path.mkdir()

        # Create main.py with FastAPI
        main_py = project_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Create pyproject.toml
        pyproject = project_path / "pyproject.toml"
        pyproject.write_text("[tool.poetry.dependencies]\nfastapi = '^0.100.0'")

        # Create existing modules
        user_module = project_path / "user"
        user_module.mkdir()
        (user_module / "__init__.py").write_text('"""User module."""')

        auth_module = project_path / "auth"
        auth_module.mkdir()
        (auth_module / "__init__.py").write_text('"""Auth module."""')

        return project_path

    @patch("fascraft.commands.generate.console")
    @patch("fascraft.commands.generate.template_registry")
    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.update_base_router")
    def test_generate_module_with_dependencies(
        self,
        mock_update_router,
        mock_env,
        mock_registry,
        mock_console,
        mock_project_path,
    ):
        """Test generating a module with dependencies."""
        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja environment
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "Generated content"
        mock_env.return_value.get_template.return_value = mock_template_instance

        # Clear dependency graph for testing
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Generate module with dependencies
        generate_module("order", str(mock_project_path), "basic", "user,auth")

        # Verify module was added to dependency graph
        assert "order" in dependency_graph.modules
        assert "user" in dependency_graph.modules
        assert "auth" in dependency_graph.modules

        # Verify dependencies were created
        order_deps = dependency_graph.get_dependencies("order")
        assert len(order_deps) == 2

        dep_modules = [dep.target_module for dep in order_deps]
        assert "user" in dep_modules
        assert "auth" in dep_modules

        # Verify dependency metadata
        order_module = dependency_graph.modules["order"]
        assert order_module.metadata["template"] == "basic"
        assert order_module.metadata["dependencies"] == ["user", "auth"]

    @patch("fascraft.commands.generate.console")
    def test_generate_module_dependency_not_found(
        self, mock_console, mock_project_path
    ):
        """Test generating module with non-existent dependency."""
        with pytest.raises(SystemExit):
            generate_module("order", str(mock_project_path), "basic", "nonexistent")

        # Verify error message
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Dependency module 'nonexistent' not found" in str(call) for call in calls
        )
        assert error_call

    @patch("fascraft.commands.generate.console")
    def test_generate_module_self_dependency(self, mock_console, mock_project_path):
        """Test generating module that depends on itself."""
        with pytest.raises(SystemExit):
            generate_module("order", str(mock_project_path), "basic", "order")

        # Verify error message
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Module cannot depend on itself" in str(call) for call in calls
        )
        assert error_call

    @patch("fascraft.commands.generate.console")
    @patch("fascraft.commands.generate.template_registry")
    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.update_base_router")
    def test_generate_module_circular_dependency_detection(
        self,
        mock_update_router,
        mock_env,
        mock_registry,
        mock_console,
        mock_project_path,
    ):
        """Test that circular dependencies are detected and prevented."""
        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja environment
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "Generated content"
        mock_env.return_value.get_template.return_value = mock_template_instance

        # Clear dependency graph for testing
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # First, create a user module that depends on order
        dependency_graph.add_module("user", mock_project_path / "user")
        dependency_graph.add_module("order", mock_project_path / "order")
        dependency_graph.add_dependency(
            "user", "order", "import", "strong", "User depends on order"
        )

        # Now try to create order module that depends on user (circular!)
        with pytest.raises(SystemExit):
            generate_module("order", str(mock_project_path), "basic", "user")

        # Verify circular dependency error was shown
        mock_console.print.assert_called()
        calls = mock_console.print.call_args_list
        error_call = any(
            "Circular dependencies detected" in str(call) for call in calls
        )
        assert error_call

    @patch("fascraft.commands.generate.console")
    @patch("fascraft.commands.generate.template_registry")
    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.update_base_router")
    def test_generate_module_dependency_validation(
        self,
        mock_update_router,
        mock_env,
        mock_registry,
        mock_console,
        mock_project_path,
    ):
        """Test that dependency validation works correctly."""
        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja environment
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "Generated content"
        mock_env.return_value.get_template.return_value = mock_template_instance

        # Clear dependency graph for testing
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Generate module with valid dependencies
        generate_module("order", str(mock_project_path), "basic", "user,auth")

        # Verify dependencies were validated and registered
        assert "order" in dependency_graph.modules
        assert "user" in dependency_graph.modules
        assert "auth" in dependency_graph.modules

        # Verify dependency relationships
        order_deps = dependency_graph.get_dependencies("order")
        assert len(order_deps) == 2

        # Verify dependency metadata
        for dep in order_deps:
            assert dep.dependency_type == "import"
            assert dep.strength == "strong"
            assert "depends on" in dep.description

    @patch("fascraft.commands.generate.console")
    @patch("fascraft.commands.generate.template_registry")
    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.update_base_router")
    def test_generate_module_no_dependencies(
        self,
        mock_update_router,
        mock_env,
        mock_registry,
        mock_console,
        mock_project_path,
    ):
        """Test generating module without dependencies."""
        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja environment
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "Generated content"
        mock_env.return_value.get_template.return_value = mock_template_instance

        # Clear dependency graph for testing
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Generate module without dependencies
        generate_module("order", str(mock_project_path), "basic")

        # Verify module was added to dependency graph
        assert "order" in dependency_graph.modules

        # Verify no dependencies were created
        order_deps = dependency_graph.get_dependencies("order")
        assert len(order_deps) == 0

        # Verify module metadata
        order_module = dependency_graph.modules["order"]
        assert order_module.metadata["template"] == "basic"
        assert order_module.metadata["dependencies"] == []

    @patch("fascraft.commands.generate.console")
    @patch("fascraft.commands.generate.template_registry")
    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.update_base_router")
    def test_generate_module_template_rendering_with_dependencies(
        self,
        mock_update_router,
        mock_env,
        mock_registry,
        mock_console,
        mock_project_path,
    ):
        """Test that templates are rendered with dependency information."""
        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja environment
        mock_template_instance = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template_instance

        # Clear dependency graph for testing
        dependency_graph.modules.clear()
        dependency_graph.dependency_matrix.clear()
        dependency_graph.reverse_dependencies.clear()

        # Generate module with dependencies
        generate_module("order", str(mock_project_path), "basic", "user,auth")

        # Verify template was rendered with dependency context
        mock_template_instance.render.assert_called()
        render_calls = mock_template_instance.render.call_args_list

        for call in render_calls:
            kwargs = call[1]  # Get keyword arguments
            assert "dependencies" in kwargs
            assert kwargs["dependencies"] == ["user", "auth"]
            assert "dependency_imports" in kwargs
            assert "dependency_injections" in kwargs

            # Verify dependency imports were generated
            imports = kwargs["dependency_imports"]
            assert "from user import models as user_models" in imports
            assert "from auth import models as auth_models" in imports

            # Verify dependency injections were generated
            injections = kwargs["dependency_injections"]
            assert "user_service: UserService" in injections
            assert "auth_service: AuthService" in injections
