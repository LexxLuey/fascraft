"""Tests for the config command functionality."""

from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest
import click

from fascraft.commands.config import (
    manage_config,
    show_config,
    create_config,
    update_config,
    validate_config,
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


class TestShowConfig:
    """Test the show_config function."""

    @patch("fascraft.commands.config.console.print")
    def test_show_config_exists(self, mock_print, tmp_path):
        """Test showing existing configuration."""
        config_path = tmp_path / "fascraft.toml"
        config_content = """# FasCraft project configuration
[project]
name = "test-project"
version = "0.1.0"

[router]
base_prefix = "/api/v1"
"""
        config_path.write_text(config_content)
        
        show_config(config_path, tmp_path)
        
        # Verify that console.print was called
        assert mock_print.call_count > 0

    @patch("fascraft.commands.config.console.print")
    def test_show_config_not_exists(self, mock_print, tmp_path):
        """Test showing non-existent configuration."""
        config_path = tmp_path / "fascraft.toml"
        
        show_config(config_path, tmp_path)
        
        # Verify error message is displayed
        mock_print.assert_called()
        # Check that error message is shown
        calls = [call.args[0] for call in mock_print.call_args_list]
        error_calls = [call for call in calls if "❌" in str(call)]
        assert len(error_calls) > 0


class TestCreateConfig:
    """Test the create_config function."""

    @patch("fascraft.commands.config.console.print")
    def test_create_config_success(self, mock_print, tmp_path):
        """Test successful configuration creation."""
        config_path = tmp_path / "fascraft.toml"
        
        create_config(config_path, tmp_path)
        
        # Check that config file was created
        assert config_path.exists()
        
        # Check config content
        config_content = config_path.read_text()
        assert "[project]" in config_content
        assert "[router]" in config_content
        assert "[database]" in config_content
        assert "[modules]" in config_content
        assert "[development]" in config_content
        assert "[production]" in config_content
        
        # Verify success message
        mock_print.assert_called()

    @patch("fascraft.commands.config.console.print")
    @patch("fascraft.commands.config.typer.confirm")
    def test_create_config_already_exists(self, mock_confirm, mock_print, tmp_path):
        """Test configuration creation when file already exists."""
        config_path = tmp_path / "fascraft.toml"
        existing_content = "# existing config\n[project]\nname = 'existing'"
        config_path.write_text(existing_content)
        
        # Mock the confirmation to return False (don't overwrite)
        mock_confirm.return_value = False
        
        create_config(config_path, tmp_path)
        
        # Check that existing content is preserved
        config_content = config_path.read_text()
        assert existing_content in config_content
        
        # Verify warning message
        mock_print.assert_called()


class TestUpdateConfig:
    """Test the update_config function."""

    @patch("fascraft.commands.config.console.print")
    def test_update_config_success(self, mock_print, tmp_path):
        """Test successful configuration update."""
        config_path = tmp_path / "fascraft.toml"
        config_content = """# FasCraft project configuration
[project]
name = "test-project"
version = "0.1.0"

[router]
base_prefix = "/api/v1"
"""
        config_path.write_text(config_content)
        
        update_config(config_path, "project.name", "updated-project")
        
        # Check that config was updated
        updated_content = config_path.read_text()
        assert "name = \"updated-project\"" in updated_content
        
        # Verify success message
        mock_print.assert_called()

    @patch("fascraft.commands.config.console.print")
    def test_update_config_invalid_key(self, mock_print, tmp_path):
        """Test configuration update with invalid key."""
        config_path = tmp_path / "fascraft.toml"
        config_content = """# FasCraft project configuration
[project]
name = "test-project"
"""
        config_path.write_text(config_content)
        
        # This should raise typer.Exit due to invalid key format
        with pytest.raises(click.exceptions.Exit) as exc_info:
            update_config(config_path, "invalid.key", "value")
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, click.exceptions.Exit)

    @patch("fascraft.commands.config.console.print")
    def test_update_config_file_not_exists(self, mock_print, tmp_path):
        """Test configuration update when file doesn't exist."""
        config_path = tmp_path / "fascraft.toml"
        
        update_config(config_path, "project.name", "value")
        
        # Verify error message
        mock_print.assert_called()
        # Check that error message is shown
        calls = [call.args[0] for call in mock_print.call_args_list]
        error_calls = [call for call in calls if "❌" in str(call)]
        assert len(error_calls) > 0


class TestValidateConfig:
    """Test the validate_config function."""

    @patch("fascraft.commands.config.console.print")
    def test_validate_config_valid(self, mock_print, tmp_path):
        """Test validation of valid configuration."""
        config_path = tmp_path / "fascraft.toml"
        config_content = """# FasCraft project configuration
[project]
name = "test-project"
version = "0.1.0"

[router]
base_prefix = "/api/v1"
"""
        config_path.write_text(config_content)
        
        validate_config(config_path)
        
        # Verify success message
        mock_print.assert_called()

    @patch("fascraft.commands.config.console.print")
    def test_validate_config_invalid_toml(self, mock_print, tmp_path):
        """Test validation of invalid TOML configuration."""
        config_path = tmp_path / "fascraft.toml"
        invalid_content = """# Invalid TOML
[project
name = "test-project"
"""
        config_path.write_text(invalid_content)
        
        # This should raise typer.Exit due to TOML parsing error
        with pytest.raises(click.exceptions.Exit) as exc_info:
            validate_config(config_path)
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, click.exceptions.Exit)

    @patch("fascraft.commands.config.console.print")
    def test_validate_config_missing_sections(self, mock_print, tmp_path):
        """Test validation of configuration with missing required sections."""
        config_path = tmp_path / "fascraft.toml"
        incomplete_content = """# Incomplete configuration
[project]
name = "test-project"
"""
        config_path.write_text(incomplete_content)
        
        validate_config(config_path)
        
        # Verify warning message
        mock_print.assert_called()

    @patch("fascraft.commands.config.console.print")
    def test_validate_config_file_not_exists(self, mock_print, tmp_path):
        """Test validation of non-existent configuration file."""
        config_path = tmp_path / "fascraft.toml"
        
        validate_config(config_path)
        
        # Verify error message
        mock_print.assert_called()
        # Check that error message is shown
        calls = [call.args[0] for call in mock_print.call_args_list]
        error_calls = [call for call in calls if "❌" in str(call)]
        assert len(error_calls) > 0


class TestManageConfig:
    """Test the manage_config function."""

    def test_manage_config_show(self, tmp_path):
        """Test show action."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the show_config function
        with patch("fascraft.commands.config.show_config") as mock_show:
            manage_config("show", str(tmp_path))
            mock_show.assert_called_once()

    def test_manage_config_create(self, tmp_path):
        """Test create action."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the create_config function
        with patch("fascraft.commands.config.create_config") as mock_create:
            manage_config("create", str(tmp_path))
            mock_create.assert_called_once()

    def test_manage_config_update_success(self, tmp_path):
        """Test update action with valid parameters."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the update_config function
        with patch("fascraft.commands.config.update_config") as mock_update:
            manage_config("update", str(tmp_path), "project.name", "new-value")
            mock_update.assert_called_once_with(
                tmp_path / "fascraft.toml", "project.name", "new-value"
            )

    def test_manage_config_update_missing_params(self, tmp_path):
        """Test update action with missing parameters."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Create a fascraft.toml file so the function doesn't default to show action
        config_path = tmp_path / "fascraft.toml"
        config_content = """# FasCraft project configuration
[project]
name = "test-project"
version = "0.1.0"

[router]
base_prefix = "/api/v1"
"""
        config_path.write_text(config_content)
        
        # Mock the console.print function
        with patch("fascraft.commands.config.console.print") as mock_print:
            with pytest.raises(click.exceptions.Exit) as exc_info:
                manage_config(action="update", path=str(tmp_path))
            
            # Check that it's an exit exception
            exception = exc_info.value
            assert isinstance(exception, click.exceptions.Exit)
            
            # Verify error message was printed
            mock_print.assert_called()

    def test_manage_config_validate(self, tmp_path):
        """Test validate action."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the validate_config function
        with patch("fascraft.commands.config.validate_config") as mock_validate:
            manage_config("validate", str(tmp_path))
            mock_validate.assert_called_once()

    def test_manage_config_unknown_action(self, tmp_path):
        """Test unknown action."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        with pytest.raises(click.exceptions.Exit) as exc_info:
            manage_config("unknown", str(tmp_path))
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, click.exceptions.Exit)

    def test_manage_config_invalid_path(self):
        """Test management with invalid path."""
        with pytest.raises(click.exceptions.Exit) as exc_info:
            manage_config("show", "/nonexistent/path")
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, click.exceptions.Exit)

    def test_manage_config_not_fastapi(self, tmp_path):
        """Test management of non-FastAPI project."""
        # Create a non-FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")
        
        with pytest.raises(click.exceptions.Exit) as exc_info:
            manage_config("show", str(tmp_path))
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, click.exceptions.Exit)
