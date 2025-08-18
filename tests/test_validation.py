"""Tests for the validation module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fascraft.exceptions import (
    DiskSpaceError,
    InvalidInputError,
    InvalidModuleNameError,
    InvalidProjectNameError,
    PermissionError,
)
from fascraft.validation import (
    sanitize_filename,
    validate_config_key,
    validate_config_value,
    validate_fastapi_project,
    validate_module_name,
    validate_path,
    validate_project_name,
    validate_project_path,
    validate_python_version,
)


class TestProjectNameValidation:
    """Test project name validation."""

    def test_valid_project_name(self):
        """Test valid project names."""
        valid_names = ["my_project", "Project123", "_private", "api_v2"]
        for name in valid_names:
            result = validate_project_name(name)
            assert result == name

    def test_empty_project_name(self):
        """Test empty project name raises error."""
        with pytest.raises(InvalidProjectNameError) as exc_info:
            validate_project_name("")
        assert "cannot be empty" in str(exc_info.value)

    def test_whitespace_project_name(self):
        """Test whitespace-only project name raises error."""
        with pytest.raises(InvalidProjectNameError) as exc_info:
            validate_project_name("   ")
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_characters(self):
        """Test project names with invalid characters."""
        invalid_names = [
            "my.project",
            "my/project",
            "my project",
            "123project",
            "@project",
        ]
        for name in invalid_names:
            with pytest.raises(InvalidProjectNameError) as exc_info:
                validate_project_name(name)
            assert "must start with a letter or underscore" in str(exc_info.value)

    def test_reserved_keywords(self):
        """Test project names that are Python reserved keywords."""
        reserved_keywords = ["class", "def", "import", "from", "True", "False"]
        for keyword in reserved_keywords:
            with pytest.raises(InvalidProjectNameError) as exc_info:
                validate_project_name(keyword)
            assert "cannot be a Python reserved keyword" in str(exc_info.value)

    def test_too_long_name(self):
        """Test project name that is too long."""
        long_name = "a" * 51
        with pytest.raises(InvalidProjectNameError) as exc_info:
            validate_project_name(long_name)
        assert "50 characters or less" in str(exc_info.value)

    def test_strips_whitespace(self):
        """Test that whitespace is stripped from valid names."""
        result = validate_project_name("  my_project  ")
        assert result == "my_project"


class TestModuleNameValidation:
    """Test module name validation."""

    def test_valid_module_name(self):
        """Test valid module names."""
        valid_names = ["users", "user_123", "_internal", "api_v1"]
        for name in valid_names:
            result = validate_module_name(name)
            assert result == name

    def test_empty_module_name(self):
        """Test empty module name raises error."""
        with pytest.raises(InvalidModuleNameError) as exc_info:
            validate_module_name("")
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_characters(self):
        """Test module names with invalid characters."""
        invalid_names = [
            "user.module",
            "user/module",
            "user module",
            "123module",
            "@module",
        ]
        for name in invalid_names:
            with pytest.raises(InvalidModuleNameError) as exc_info:
                validate_module_name(name)
            assert "must be a valid Python identifier" in str(exc_info.value)

    def test_reserved_keywords(self):
        """Test module names that are Python reserved keywords."""
        reserved_keywords = ["class", "def", "import", "from", "True", "False"]
        for keyword in reserved_keywords:
            with pytest.raises(InvalidModuleNameError) as exc_info:
                validate_module_name(keyword)
            assert "cannot be a Python reserved keyword" in str(exc_info.value)

    def test_too_long_name(self):
        """Test module name that is too long."""
        long_name = "a" * 31
        with pytest.raises(InvalidModuleNameError) as exc_info:
            validate_module_name(long_name)
        assert "30 characters or less" in str(exc_info.value)

    def test_strips_whitespace(self):
        """Test that whitespace is stripped from valid names."""
        result = validate_module_name("  users  ")
        assert result == "users"


class TestPathValidation:
    """Test path validation."""

    def test_valid_path(self):
        """Test valid path."""
        with patch("pathlib.Path.resolve") as mock_resolve:
            mock_resolve.return_value = Path("/valid/path")
            result = validate_path("/valid/path")
            assert result == Path("/valid/path")

    def test_empty_path(self):
        """Test empty path raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_path("")
        assert "cannot be empty" in str(exc_info.value)

    def test_whitespace_path(self):
        """Test whitespace-only path raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_path("   ")
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_path(self):
        """Test invalid path raises error."""
        with patch("pathlib.Path.resolve") as mock_resolve:
            mock_resolve.side_effect = OSError("Invalid path")
            with pytest.raises(InvalidInputError) as exc_info:
                validate_path("/invalid/path")
            assert "Invalid path" in str(exc_info.value)


class TestProjectPathValidation:
    """Test project path validation."""

    def test_project_path_does_not_exist(self):
        """Test validation when project path doesn't exist."""
        project_path = Path("/tmp/new_project")
        with patch("pathlib.Path.exists", return_value=False):
            with patch("os.access", return_value=True):
                validate_project_path(project_path, "new_project")

    def test_project_path_already_exists(self):
        """Test validation when project path already exists."""
        project_path = Path("/tmp/existing_project")
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(InvalidInputError) as exc_info:
                validate_project_path(project_path, "existing_project")
            assert "already exists" in str(exc_info.value)

    def test_parent_directory_not_exists(self):
        """Test validation when parent directory doesn't exist."""
        project_path = Path("/nonexistent/new_project")
        with patch("pathlib.Path.exists", side_effect=[False, False]):
            # Should not raise an error now - parent directories can be created
            validate_project_path(project_path, "new_project")

    def test_parent_directory_not_directory(self):
        """Test validation when parent path is not a directory."""
        project_path = Path("/tmp/file/new_project")
        with patch("pathlib.Path.exists", side_effect=[False, True]):
            with patch("pathlib.Path.is_dir", return_value=False):
                with pytest.raises(InvalidInputError) as exc_info:
                    validate_project_path(project_path, "new_project")
                assert "not a directory" in str(exc_info.value)

    def test_no_write_permission(self):
        """Test validation when no write permission."""
        project_path = Path("/tmp/new_project")
        with patch("pathlib.Path.exists", side_effect=[False, True]):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("os.access", return_value=False):
                    with pytest.raises(PermissionError) as exc_info:
                        validate_project_path(project_path, "new_project")
                    assert "write" in str(exc_info.value)

    def test_insufficient_disk_space(self):
        """Test validation when insufficient disk space."""
        project_path = Path("/tmp/new_project")
        with patch("pathlib.Path.exists", side_effect=[False, True]):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("os.access", return_value=True):
                    with patch("shutil.disk_usage") as mock_disk_usage:
                        mock_disk_usage.return_value = MagicMock(free=50000)  # 50KB
                        with pytest.raises(DiskSpaceError) as exc_info:
                            validate_project_path(project_path, "new_project")
                        assert "100KB" in str(exc_info.value)


class TestFastAPIProjectValidation:
    """Test FastAPI project validation."""

    def test_valid_fastapi_project_main_py(self):
        """Test validation of FastAPI project with FastAPI in main.py."""
        project_path = Path("/tmp/fastapi_project")
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("pathlib.Path.read_text") as mock_read:
                    mock_read.return_value = "from fastapi import FastAPI"
                    validate_fastapi_project(project_path)

    def test_valid_fastapi_project_pyproject_toml(self):
        """Test validation of FastAPI project with FastAPI in pyproject.toml."""
        project_path = Path("/tmp/fastapi_project")
        with patch("pathlib.Path.exists", side_effect=[True, True, False, False]):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("pathlib.Path.read_text") as mock_read:
                    mock_read.return_value = 'fastapi = "^0.100.0"'
                    validate_fastapi_project(project_path)

    def test_valid_fastapi_project_requirements_txt(self):
        """Test validation of FastAPI project with FastAPI in requirements.txt."""
        project_path = Path("/tmp/fastapi_project")
        with patch("pathlib.Path.exists", side_effect=[True, False, True, False]):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("pathlib.Path.read_text") as mock_read:
                    mock_read.return_value = "fastapi>=0.100.0"
                    validate_fastapi_project(project_path)

    def test_not_fastapi_project(self):
        """Test validation when project is not a FastAPI project."""
        project_path = Path("/tmp/not_fastapi_project")
        with patch("pathlib.Path.exists", side_effect=[True, False, False, False]):
            with patch("pathlib.Path.is_dir", return_value=True):
                with patch("pathlib.Path.read_text") as mock_read:
                    mock_read.return_value = "from flask import Flask"
                    with pytest.raises(InvalidInputError) as exc_info:
                        validate_fastapi_project(project_path)
                    assert "does not contain a FastAPI project" in str(exc_info.value)

    def test_project_path_not_exists(self):
        """Test validation when project path doesn't exist."""
        project_path = Path("/tmp/nonexistent_project")
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(InvalidInputError) as exc_info:
                validate_fastapi_project(project_path)
            assert "does not exist" in str(exc_info.value)

    def test_project_path_not_directory(self):
        """Test validation when project path is not a directory."""
        project_path = Path("/tmp/not_directory")
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_dir", return_value=False):
                with pytest.raises(InvalidInputError) as exc_info:
                    validate_fastapi_project(project_path)
                assert "not a directory" in str(exc_info.value)


class TestConfigValidation:
    """Test configuration validation."""

    def test_valid_config_key(self):
        """Test valid configuration key."""
        validate_config_key("project.name")

    def test_empty_config_key(self):
        """Test empty config key raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key("")
        assert "cannot be empty" in str(exc_info.value)

    def test_missing_dot_in_config_key(self):
        """Test config key without dot raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key("projectname")
        assert "section.key" in str(exc_info.value)

    def test_empty_section_in_config_key(self):
        """Test config key with empty section raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key(".name")
        assert "non-empty" in str(exc_info.value)

    def test_empty_setting_in_config_key(self):
        """Test config key with empty setting raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key("project.")
        assert "non-empty" in str(exc_info.value)

    def test_invalid_section_name(self):
        """Test config key with invalid section name raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key("project-name.setting")
        assert "valid identifier" in str(exc_info.value)

    def test_invalid_setting_name(self):
        """Test config key with invalid setting name raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_key("project.setting-name")
        assert "valid identifier" in str(exc_info.value)

    def test_valid_config_value(self):
        """Test valid configuration value."""
        validate_config_value("test_value")

    def test_none_config_value(self):
        """Test None config value raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_value(None)
        assert "cannot be None" in str(exc_info.value)

    def test_too_long_config_value(self):
        """Test config value that is too long raises error."""
        long_value = "a" * 1001
        with pytest.raises(InvalidInputError) as exc_info:
            validate_config_value(long_value)
        assert "1000 characters or less" in str(exc_info.value)


class TestFilenameSanitization:
    """Test filename sanitization."""

    def test_safe_filename(self):
        """Test that safe filenames are unchanged."""
        safe_names = ["normal_file.txt", "file_123.py", "README.md"]
        for name in safe_names:
            result = sanitize_filename(name)
            assert result == name

    def test_unsafe_characters_replaced(self):
        """Test that unsafe characters are replaced with underscores."""
        unsafe_names = [
            ("file<name>.txt", "file_name_.txt"),
            ("file:name.txt", "file_name.txt"),
            ("file/name.txt", "file_name.txt"),
            ("file\\name.txt", "file_name.txt"),
            ("file|name.txt", "file_name.txt"),
            ("file?name.txt", "file_name.txt"),
            ("file*name.txt", "file_name.txt"),
        ]
        for unsafe, expected in unsafe_names:
            result = sanitize_filename(unsafe)
            assert result == expected

    def test_leading_trailing_dots_removed(self):
        """Test that leading and trailing dots are removed."""
        result = sanitize_filename("...file.txt...")
        assert result == "file.txt"

    def test_empty_filename_handled(self):
        """Test that empty filename is handled."""
        result = sanitize_filename("")
        assert result == "unnamed"

    def test_whitespace_only_filename_handled(self):
        """Test that whitespace-only filename is handled."""
        result = sanitize_filename("   ")
        assert result == "unnamed"

    def test_too_long_filename_truncated(self):
        """Test that too long filename is truncated."""
        long_name = "a" * 300
        result = sanitize_filename(long_name)
        assert len(result) == 255


class TestPythonVersionValidation:
    """Test Python version validation."""

    def test_valid_python_versions(self):
        """Test valid Python version strings."""
        valid_versions = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.8.0", "3.10.1"]
        for version in valid_versions:
            validate_python_version(version)

    def test_empty_version(self):
        """Test empty version raises error."""
        with pytest.raises(InvalidInputError) as exc_info:
            validate_python_version("")
        assert "cannot be empty" in str(exc_info.value)

    def test_invalid_format(self):
        """Test invalid version format raises error."""
        invalid_versions = ["3", "3.8.0.0", "3.8.0a1", "3.8.0b1", "3.8.0rc1"]
        for version in invalid_versions:
            with pytest.raises(InvalidInputError) as exc_info:
                validate_python_version(version)
            assert "format" in str(exc_info.value)

    def test_version_too_old(self):
        """Test version too old raises error."""
        old_versions = ["2.7", "3.0", "3.7"]
        for version in old_versions:
            with pytest.raises(InvalidInputError) as exc_info:
                validate_python_version(version)
            assert "3.8 or higher" in str(exc_info.value)

    def test_version_too_new(self):
        """Test version too new raises error."""
        new_versions = ["3.13", "4.0", "5.0"]
        for version in new_versions:
            with pytest.raises(InvalidInputError) as exc_info:
                validate_python_version(version)
            assert "3.12 or lower" in str(exc_info.value)
