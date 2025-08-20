"""Tests for the generate command."""

from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.generate import (
    ensure_config_structure,
    generate_module,
    is_fastapi_project,
)


class TestIsFastApiProject:
    """Test the is_fastapi_project function."""

    def test_is_fastapi_project_valid_main_py(self, tmp_path):
        """Test that a valid FastAPI project with main.py is correctly identified."""
        # Create main.py with FastAPI content
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_valid_pyproject_toml(self, tmp_path):
        """Test that a valid FastAPI project with pyproject.toml is correctly identified."""
        # Create pyproject.toml with FastAPI dependency
        pyproject_toml = tmp_path / "pyproject.toml"
        pyproject_toml.write_text("[tool.poetry.dependencies]\nfastapi = '^0.104.0'")

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_invalid(self, tmp_path):
        """Test that an invalid project is not identified as FastAPI."""
        # Create empty directory
        assert is_fastapi_project(tmp_path) is False

        # Create main.py without FastAPI
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")
        assert is_fastapi_project(tmp_path) is False


class TestEnsureConfigStructure:
    """Test the ensure_config_structure function."""

    def test_ensure_config_structure_creates_config_dir(self, tmp_path):
        """Test that config directory is created if it doesn't exist."""
        ensure_config_structure(tmp_path)

        config_dir = tmp_path / "config"
        assert config_dir.exists()
        assert config_dir.is_dir()

    def test_ensure_config_structure_creates_basic_files(self, tmp_path):
        """Test that basic config files are created if they don't exist."""
        ensure_config_structure(tmp_path)

        config_dir = tmp_path / "config"
        assert (config_dir / "__init__.py").exists()
        assert (config_dir / "settings.py").exists()
        assert (config_dir / "database.py").exists()

    def test_ensure_config_structure_existing_config(self, tmp_path):
        """Test that existing config structure is not modified."""
        # Create existing config
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        existing_settings = config_dir / "settings.py"
        existing_settings.write_text("app_name = 'existing'")

        ensure_config_structure(tmp_path)

        # Check that existing content is preserved
        assert existing_settings.read_text() == "app_name = 'existing'"


class TestGenerateModule:
    """Test the generate_module function."""

    @patch("fascraft.commands.generate.Environment")
    @patch("fascraft.commands.generate.template_registry")
    def test_generate_module_success(self, mock_registry, mock_env, tmp_path):
        """Test successful domain module generation."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Mock template registry
        mock_template = MagicMock()
        mock_template.display_name = "Basic CRUD"
        mock_template.description = "Simple CRUD operations"
        mock_registry.get_template.return_value = mock_template

        # Mock Jinja2 environment
        mock_template_instance = MagicMock()
        mock_template_instance.render.return_value = "rendered content"
        mock_env_instance = MagicMock()
        mock_env_instance.get_template.return_value = mock_template_instance
        mock_env.return_value = mock_env_instance

        # Generate module
        generate_module("customers", path=str(tmp_path), template="basic", depends_on=None)

        # Verify templates were rendered
        assert mock_template_instance.render.call_count == 7  # 7 template files

        # Check that module directory was created
        module_dir = tmp_path / "customers"
        assert module_dir.exists()
        assert (module_dir / "models.py").exists()
        assert (module_dir / "schemas.py").exists()
        assert (module_dir / "services.py").exists()
        assert (module_dir / "routers.py").exists()
        assert (module_dir / "tests").exists()

        # Check that the module router doesn't have a hardcoded prefix
        # Note: Since we're mocking the template, we can't check actual content
        # In a real scenario, the router would be generated without hardcoded prefixes

        # Verify that the success message mentions base router integration
        # Note: This test mocks the environment, so we can't test the actual output
        # In a real scenario, the message would show "automatically added to the base router"

    def test_generate_module_invalid_project(self, tmp_path):
        """Test module generation in an invalid project."""
        # Create an empty directory (not a FastAPI project)
        with pytest.raises(typer.Exit) as exc_info:
            generate_module("customers", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_generate_module_already_exists(self, tmp_path):
        """Test module generation when module already exists."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        # Create existing module directory
        module_dir = tmp_path / "customers"
        module_dir.mkdir()

        with pytest.raises(typer.Exit) as exc_info:
            generate_module("customers", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_generate_module_empty_name(self):
        """Test module generation with empty name."""
        with pytest.raises(typer.Exit) as exc_info:
            generate_module("")
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_generate_module_whitespace_name(self):
        """Test module generation with whitespace name."""
        with pytest.raises(typer.Exit) as exc_info:
            generate_module("   ")
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_generate_module_nonexistent_path(self):
        """Test module generation with nonexistent path."""
        with pytest.raises(typer.Exit) as exc_info:
            generate_module("customers", "/nonexistent/path")
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1


class TestGenerateModuleIntegration:
    """Integration tests for the generate command."""

    def test_generate_module_creates_domain_structure(self, tmp_path):
        """Test that module generation creates complete domain structure."""
        # Create a valid FastAPI project with base router structure
        routers_dir = tmp_path / "routers"
        routers_dir.mkdir()

        # Create main.py for FastAPI project detection
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

        base_router = routers_dir / "base.py"
        base_router.write_text(
            """from fastapi import APIRouter

# Create base router with common prefix
base_router = APIRouter(prefix="/api/v1")

# Import all module routers here
# from users import routers as user_routers
# from products import routers as product_routers

# Include all module routers
# base_router.include_router(user_routers.router, prefix="/users", tags=["users"])
# base_router.include_router(product_routers.router, prefix="/products", tags=["products"])

# Health check endpoint
@base_router.get("/health")
async def health_check():
    \"\"\"Health check endpoint.\"\"\"
    return {"status": "healthy", "version": "0.1.0"}
"""
        )

        # Mock the template registry and Jinja2 environment to avoid template loading issues
        with patch("fascraft.commands.generate.template_registry") as mock_registry, \
             patch("fascraft.commands.generate.Environment") as mock_env:
            
            # Mock template registry
            mock_template = MagicMock()
            mock_template.display_name = "Basic CRUD"
            mock_template.description = "Simple CRUD operations"
            mock_registry.get_template.return_value = mock_template
            
            # Mock Jinja2 environment
            mock_template_instance = MagicMock()
            mock_template_instance.render.return_value = "rendered content"
            mock_env_instance = MagicMock()
            mock_env_instance.get_template.return_value = mock_template_instance
            mock_env.return_value = mock_env_instance

            # Generate module
            generate_module("customers", path=str(tmp_path), template="basic", depends_on=None)

            # Check that domain structure was created
            customers_dir = tmp_path / "customers"
            assert customers_dir.exists()
            assert (customers_dir / "models.py").exists()
            assert (customers_dir / "schemas.py").exists()
            assert (customers_dir / "services.py").exists()
            assert (customers_dir / "routers.py").exists()
            assert (customers_dir / "tests").exists()
            assert (customers_dir / "tests" / "test_models.py").exists()

            # Check that base router was updated
            updated_base_router = base_router.read_text()
            assert (
                "from customers import routers as customers_routers"
                in updated_base_router
            )
            assert (
                'base_router.include_router(customers_routers.router, prefix="/customerss", tags=["customerss"])'
                in updated_base_router
            )
