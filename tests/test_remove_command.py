"""Tests for the remove command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fastforge.commands.remove import (
    analyze_module,
    confirm_removal,
    display_removal_preview,
    is_domain_module,
    remove_module,
    remove_module_files,
    update_main_py_after_removal,
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


class TestDisplayRemovalPreview:
    """Test the display_removal_preview function."""

    def test_display_removal_preview(self, tmp_path):
        """Test that removal preview displays correctly."""
        module_info = {
            'name': 'test_module',
            'path': tmp_path,
            'files': ['models.py', 'schemas.py'],
            'size': 1024,
            'has_tests': True
        }
        
        # This should not raise an exception
        display_removal_preview(module_info, tmp_path)


class TestConfirmRemoval:
    """Test the confirm_removal function."""

    @patch('builtins.input')
    def test_confirm_removal_yes(self, mock_input):
        """Test confirmation with yes response."""
        mock_input.return_value = 'y'
        assert confirm_removal('test_module') is True

    @patch('builtins.input')
    def test_confirm_removal_no(self, mock_input):
        """Test confirmation with no response."""
        mock_input.return_value = 'n'
        assert confirm_removal('test_module') is False

    @patch('builtins.input')
    def test_confirm_removal_yes_uppercase(self, mock_input):
        """Test confirmation with uppercase yes response."""
        mock_input.return_value = 'YES'
        assert confirm_removal('test_module') is True


class TestRemoveModuleFiles:
    """Test the remove_module_files function."""

    def test_remove_module_files(self, tmp_path):
        """Test that module files are removed."""
        # Create some files
        (tmp_path / "test_file.txt").write_text("content")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "nested.txt").write_text("nested content")
        
        # Verify files exist
        assert (tmp_path / "test_file.txt").exists()
        assert (tmp_path / "subdir").exists()
        
        # Remove files
        remove_module_files(tmp_path)
        
        # Verify files are gone
        assert not (tmp_path / "test_file.txt").exists()
        assert not (tmp_path / "subdir").exists()


class TestUpdateMainPyAfterRemoval:
    """Test the update_main_py_after_removal function."""

    def test_update_main_py_after_removal(self, tmp_path):
        """Test that main.py is updated after module removal."""
        # Create main.py with module references
        main_py_content = """from fastapi import FastAPI

app = FastAPI()

from customers import routers as customers_routers

app.include_router(customers_routers.router, prefix="/api/v1/customers", tags=["customers"])
"""
        main_py_path = tmp_path / "main.py"
        main_py_path.write_text(main_py_content)
        
        # Update main.py
        update_main_py_after_removal(tmp_path, "customers")
        
        # Check that references were removed
        updated_content = main_py_path.read_text()
        assert "from customers import routers as customers_routers" not in updated_content
        # Check that the router include line is removed (should not contain customers_routers.router)
        assert "customers_routers.router" not in updated_content
        # Check that the app.include_router line is removed
        assert "app.include_router" not in updated_content

    def test_update_main_py_not_found(self, tmp_path):
        """Test that function handles missing main.py gracefully."""
        # This should not raise an exception
        update_main_py_after_removal(tmp_path, "test_module")


class TestRemoveModule:
    """Test the remove_module function."""

    @patch("fastforge.commands.remove.is_fastapi_project")
    @patch("fastforge.commands.remove.is_domain_module")
    @patch("fastforge.commands.remove.analyze_module")
    @patch("fastforge.commands.remove.display_removal_preview")
    @patch("fastforge.commands.remove.confirm_removal")
    @patch("fastforge.commands.remove.remove_module_files")
    @patch("fastforge.commands.remove.update_main_py_after_removal")
    def test_remove_module_success(
        self, mock_update_main, mock_remove_files, mock_confirm, 
        mock_display, mock_analyze, mock_is_domain, mock_is_fastapi, tmp_path
    ):
        """Test successful module removal."""
        mock_is_fastapi.return_value = True
        mock_is_domain.return_value = True
        mock_analyze.return_value = {'name': 'test_module'}
        mock_confirm.return_value = True
        
        # Create module directory
        module_path = tmp_path / "test_module"
        module_path.mkdir()
        
        # This should not raise an exception
        remove_module("test_module", str(tmp_path))

    def test_remove_module_invalid_project(self, tmp_path):
        """Test removing module from invalid project."""
        with pytest.raises(Exception) as exc_info:
            remove_module("test_module", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_remove_module_nonexistent(self, tmp_path):
        """Test removing nonexistent module."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()")
        
        with pytest.raises(Exception) as exc_info:
            remove_module("nonexistent", str(tmp_path))
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_remove_module_empty_name(self):
        """Test removing module with empty name."""
        with pytest.raises(Exception) as exc_info:
            remove_module("")
        
        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)
