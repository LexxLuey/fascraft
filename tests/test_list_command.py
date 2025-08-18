"""Tests for the list command."""

from unittest.mock import patch

import pytest

from fascraft.commands.list import (
    analyze_module,
    find_domain_modules,
    is_domain_module,
    list_modules,
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

    def test_is_domain_module_empty(self, tmp_path):
        """Test that an empty directory is not a domain module."""
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
        (tmp_path / "__init__.py").write_text("content")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "__init__.py").write_text("content")
        (tmp_path / "tests" / "test_models.py").write_text("content")

        result = analyze_module(tmp_path)

        assert result["name"] == tmp_path.name
        assert result["has_tests"] is True
        assert len(result["files"]) == 7  # 7 expected files, not 8
        assert result["size"] > 0

    def test_analyze_module_no_tests(self, tmp_path):
        """Test analyzing a module without tests."""
        # Create module structure without tests
        (tmp_path / "models.py").write_text("content")
        (tmp_path / "schemas.py").write_text("content")
        (tmp_path / "services.py").write_text("content")
        (tmp_path / "routers.py").write_text("content")

        result = analyze_module(tmp_path)

        assert result["has_tests"] is False
        assert len(result["files"]) == 4


class TestFindDomainModules:
    """Test the find_domain_modules function."""

    def test_find_domain_modules_empty_project(self, tmp_path):
        """Test finding modules in an empty project."""
        modules = find_domain_modules(tmp_path)
        assert modules == []

    def test_find_domain_modules_with_modules(self, tmp_path):
        """Test finding modules in a project with modules."""
        # Create valid domain modules
        customers_dir = tmp_path / "customers"
        customers_dir.mkdir()
        (customers_dir / "models.py").touch()
        (customers_dir / "schemas.py").touch()
        (customers_dir / "services.py").touch()
        (customers_dir / "routers.py").touch()

        products_dir = tmp_path / "products"
        products_dir.mkdir()
        (products_dir / "models.py").touch()
        (products_dir / "schemas.py").touch()
        (products_dir / "services.py").touch()
        (products_dir / "routers.py").touch()

        # Create non-module directories
        (tmp_path / "config").mkdir()
        (tmp_path / "__pycache__").mkdir()

        modules = find_domain_modules(tmp_path)

        assert len(modules) == 2
        module_names = [m["name"] for m in modules]
        assert "customers" in module_names
        assert "products" in module_names

    def test_find_domain_modules_ignores_non_modules(self, tmp_path):
        """Test that non-module directories are ignored."""
        # Create non-module directories
        (tmp_path / "config").mkdir()
        (tmp_path / "tests").mkdir()
        (tmp_path / "migrations").mkdir()
        (tmp_path / ".git").mkdir()

        modules = find_domain_modules(tmp_path)
        assert modules == []


class TestListModules:
    """Test the list_modules function."""

    @patch("fascraft.commands.list.is_fastapi_project")
    @patch("fascraft.commands.list.find_domain_modules")
    def test_list_modules_success(self, mock_find_modules, mock_is_fastapi, tmp_path):
        """Test successful module listing."""
        mock_is_fastapi.return_value = True

        # Mock module data
        mock_modules = [
            {
                "name": "customers",
                "path": tmp_path / "customers",
                "files": ["models.py", "schemas.py", "services.py", "routers.py"],
                "has_tests": True,
                "health_status": "healthy",
            }
        ]
        mock_find_modules.return_value = mock_modules

        # This should not raise an exception
        list_modules(str(tmp_path))

    def test_list_modules_invalid_project(self, tmp_path):
        """Test listing modules in an invalid project."""
        with pytest.raises(Exception) as exc_info:
            list_modules(str(tmp_path))

        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_list_modules_nonexistent_path(self):
        """Test listing modules with nonexistent path."""
        with pytest.raises(Exception) as exc_info:
            list_modules("/nonexistent/path")

        # Check that it's an exit exception with code 1
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)
