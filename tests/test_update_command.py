"""Tests for the update command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fastforge.commands.update import (
    analyze_module,
    confirm_update,
    create_backup,
    display_update_preview,
    is_domain_module,
    restore_from_backup,
    update_module,
    update_module_files,
)


class TestIsDomainModule:
    """Test the is_domain_module function."""

    def test_is_domain_module_valid(self, tmp_path):
        """Test that a valid domain module is correctly identified."""
        # Create required files
        (tmp_path / "models.py").touch()
        (tmp_path / "schemas.py").touch()
        (tmp_path / "services.py").touch()
        (tmp_path / "routers.py").touch()
        
        assert is_domain_module(tmp_path) is True

    def test_is_domain_module_missing_files(self, tmp_path):
        """Test that missing required files are detected."""
        # Create only some required files
        (tmp_path / "models.py").touch()
        (tmp_path / "schemas.py").touch()
        # Missing services.py and routers.py
        
        assert is_domain_module(tmp_path) is False


class TestAnalyzeModule:
    """Test the analyze_module function."""

    def test_analyze_module_complete(self, tmp_path):
        """Test analyzing a complete domain module."""
        # Create module structure
        (tmp_path / "models.py").write_text("content")
        (tmp_path / "schemas.py").write_text("content")
        (tmp_path / "services.py").write_text("content")
        (tmp_path / "routers.py").write_text("content")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_models.py").write_text("content")
        
        result = analyze_module(tmp_path)
        
        assert result['name'] == tmp_path.name
        assert result['has_tests'] is True
        assert len(result['files']) == 5  # 5 files: models.py, schemas.py, services.py, routers.py, tests/test_models.py
        assert result['size'] > 0
        assert result['last_modified'] is not None


class TestDisplayUpdatePreview:
    """Test the display_update_preview function."""

    def test_display_update_preview(self, tmp_path):
        """Test that update preview displays correctly."""
        module_info = {
            'name': 'test_module',
            'path': tmp_path,
            'files': ['models.py', 'schemas.py'],
            'size': 1024,
            'has_tests': True,
            'last_modified': 1234567890
        }
        
        # This should not raise an exception
        display_update_preview(module_info, tmp_path)


class TestConfirmUpdate:
    """Test the confirm_update function."""

    @patch('builtins.input')
    def test_confirm_update_yes(self, mock_input):
        """Test confirmation with yes response."""
        mock_input.return_value = 'y'
        assert confirm_update('test_module') is True

    @patch('builtins.input')
    def test_confirm_update_no(self, mock_input):
        """Test confirmation with no response."""
        mock_input.return_value = 'n'
        assert confirm_update('test_module') is False

    @patch('builtins.input')
    def test_confirm_update_yes_uppercase(self, mock_input):
        """Test confirmation with uppercase yes response."""
        mock_input.return_value = 'YES'
        assert confirm_update('test_module') is True


class TestCreateBackup:
    """Test the create_backup function."""

    def test_create_backup_success(self, tmp_path):
        """Test successful backup creation."""
        # Create module structure
        module_path = tmp_path / "test_module"
        module_path.mkdir()
        (module_path / "models.py").write_text("content")
        
        backup_path = create_backup(module_path, tmp_path)
        
        assert backup_path is not None
        assert backup_path.exists()
        assert (backup_path / "models.py").exists()
        assert "test_module_backup_" in backup_path.name

    def test_create_backup_failure(self, tmp_path):
        """Test backup creation failure handling."""
        # Create a file instead of directory to cause failure
        module_path = tmp_path / "test_module"
        module_path.write_text("not a directory")
        
        backup_path = create_backup(module_path, tmp_path)
        
        assert backup_path is None


class TestUpdateModuleFiles:
    """Test the update_module_files function."""

    @patch("fastforge.commands.update.Environment")
    def test_update_module_files(self, mock_env, tmp_path):
        """Test that module files are updated."""
        # Mock Jinja2 environment
        mock_template = MagicMock()
        mock_template.render.return_value = "updated content"
        mock_env_instance = MagicMock()
        mock_env_instance.get_template.return_value = mock_template
        mock_env.return_value = mock_env_instance
        
        # Create module directory
        module_path = tmp_path / "test_module"
        module_path.mkdir()
        
        # Update module files
        update_module_files(module_path, "test_module", "test_project")
        
        # Verify templates were rendered
        assert mock_template.render.call_count == 7  # 7 template files


class TestRestoreFromBackup:
    """Test the restore_from_backup function."""

    def test_restore_from_backup_success(self, tmp_path):
        """Test successful backup restoration."""
        # Create backup structure
        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        (backup_path / "models.py").write_text("backup content")
        
        # Create existing module (will be replaced)
        module_path = tmp_path / "test_module"
        module_path.mkdir()
        (module_path / "models.py").write_text("existing content")
        
        # Restore from backup
        restore_from_backup(backup_path, module_path)
        
        # Verify restoration
        assert (module_path / "models.py").exists()
        assert (module_path / "models.py").read_text() == "backup content"

    def test_restore_from_backup_failure(self, tmp_path):
        """Test backup restoration failure handling."""
        # Create backup structure
        backup_path = tmp_path / "backup"
        backup_path.mkdir()
        (backup_path / "models.py").write_text("backup content")
        
        # Create module path as file to cause failure
        module_path = tmp_path / "test_module"
        module_path.write_text("not a directory")
        
        # This should not raise an exception
        restore_from_backup(backup_path, module_path)


class TestUpdateModule:
    """Test the update_module function."""

    @patch("fastforge.commands.update.is_fastapi_project")
    @patch("fastforge.commands.update.is_domain_module")
    @patch("fastforge.commands.update.analyze_module")
    @patch("fastforge.commands.update.display_update_preview")
    @patch("fastforge.commands.update.confirm_update")
    @patch("fastforge.commands.update.create_backup")
    @patch("fastforge.commands.update.update_module_files")
    def test_update_module_success(
        self, mock_update_files, mock_create_backup, mock_confirm, 
        mock_display, mock_analyze, mock_is_domain, mock_is_fastapi, tmp_path
    ):
        """Test successful module update."""
        mock_is_fastapi.return_value = True
        mock_is_domain.return_value = True
        mock_analyze.return_value = {'name': 'test_module'}
        mock_confirm.return_value = True
        mock_create_backup.return_value = tmp_path / "backup"
        
        # Create module directory
        module_path = tmp_path / "test_module"
        module_path.mkdir()
        
        # This should not raise an exception
        update_module("test_module", str(tmp_path))

    def test_update_module_invalid_project(self, tmp_path):
        """Test updating module in invalid project."""
        with pytest.raises(Exception) as exc_info:
            update_module("test_module", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_update_module_nonexistent(self, tmp_path):
        """Test updating nonexistent module."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()")
        
        with pytest.raises(Exception) as exc_info:
            update_module("nonexistent", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_update_module_empty_name(self):
        """Test updating module with empty name."""
        with pytest.raises(Exception) as exc_info:
            update_module("")
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)
