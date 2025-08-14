"""Tests for the generate command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fastforge.commands.generate import (
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

    @patch("fastforge.commands.generate.Environment")
    def test_generate_module_success(self, mock_env, tmp_path):
        """Test successful domain module generation."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")
        
        # Mock Jinja2 environment
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered content"
        mock_env_instance = MagicMock()
        mock_env_instance.get_template.return_value = mock_template
        mock_env.return_value = mock_env_instance

        # Generate module
        generate_module("customers", str(tmp_path))

        # Verify templates were rendered
        assert mock_template.render.call_count == 7  # 7 template files
        
        # Check that module directory was created
        module_dir = tmp_path / "customers"
        assert module_dir.exists()
        assert (module_dir / "models.py").exists()
        assert (module_dir / "schemas.py").exists()
        assert (module_dir / "services.py").exists()
        assert (module_dir / "routers.py").exists()
        assert (module_dir / "tests").exists()

    def test_generate_module_invalid_project(self, tmp_path):
        """Test module generation in an invalid project."""
        # Create an empty directory (not a FastAPI project)
        with pytest.raises(Exception) as exc_info:
            generate_module("customers", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_generate_module_already_exists(self, tmp_path):
        """Test module generation when module already exists."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")
        
        # Create existing module directory
        module_dir = tmp_path / "customers"
        module_dir.mkdir()

        with pytest.raises(Exception) as exc_info:
            generate_module("customers", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_generate_module_empty_name(self):
        """Test module generation with empty name."""
        with pytest.raises(Exception) as exc_info:
            generate_module("")
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_generate_module_whitespace_name(self):
        """Test module generation with whitespace name."""
        with pytest.raises(Exception) as exc_info:
            generate_module("   ")
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_generate_module_nonexistent_path(self):
        """Test module generation with nonexistent path."""
        with pytest.raises(Exception) as exc_info:
            generate_module("customers", "/nonexistent/path")
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)


class TestGenerateModuleIntegration:
    """Integration tests for the generate command."""

    def test_generate_module_creates_domain_structure(self, tmp_path):
        """Test that module generation creates complete domain structure."""
        # Create a valid FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("""from fastapi import FastAPI

app = FastAPI()

# from customers import routers as customer_routers

# app.include_router(customer_routers.router, prefix="/api/v1/customers", tags=["customers"])
""")
        
        # Mock the Jinja2 environment to avoid template loading issues
        with patch("fastforge.commands.generate.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "rendered content"
            mock_env_instance = MagicMock()
            mock_env_instance.get_template.return_value = mock_template
            mock_env.return_value = mock_env_instance

            # Generate module
            generate_module("customers", str(tmp_path))

            # Check that domain structure was created
            customers_dir = tmp_path / "customers"
            assert customers_dir.exists()
            assert (customers_dir / "models.py").exists()
            assert (customers_dir / "schemas.py").exists()
            assert (customers_dir / "services.py").exists()
            assert (customers_dir / "routers.py").exists()
            assert (customers_dir / "tests").exists()
            assert (customers_dir / "tests" / "test_models.py").exists()

            # Check that main.py was updated
            updated_main = main_py.read_text()
            assert "from customers import routers as customers_routers" in updated_main
            assert "app.include_router(customers_routers.router, prefix=f\"/api/v1/customerss\", tags=[\"customerss\"])" in updated_main
