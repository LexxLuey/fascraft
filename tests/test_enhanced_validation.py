"""Tests for enhanced validation functions in FasCraft."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from fascraft.validation import (
    validate_disk_space,
    validate_file_system_writable,
    validate_path_robust,
    is_path_safe,
    is_windows_reserved_name,
    is_network_path,
    validate_network_path,
)
from fascraft.exceptions import (
    DiskSpaceError,
    PermissionError,
    FileSystemError,
    InvalidInputError,
    NetworkPathError,
    ReadOnlyFileSystemError,
)


class TestValidateDiskSpace:
    """Test the validate_disk_space function."""

    @patch("fascraft.validation.shutil.disk_usage")
    def test_validate_disk_space_sufficient(self, mock_disk_usage):
        """Test disk space validation with sufficient space."""
        # Mock sufficient disk space (100MB available, 10MB required)
        mock_stat = MagicMock()
        mock_stat.free = 100 * 1024 * 1024  # 100MB in bytes
        mock_disk_usage.return_value = mock_stat

        # Should not raise an exception
        validate_disk_space(Path("/test/path"), required_space_mb=10)

    @patch("fascraft.validation.shutil.disk_usage")
    def test_validate_disk_space_insufficient(self, mock_disk_usage):
        """Test disk space validation with insufficient space."""
        # Mock insufficient disk space (5MB available, 10MB required)
        mock_stat = MagicMock()
        mock_stat.free = 5 * 1024 * 1024  # 5MB in bytes
        mock_disk_usage.return_value = mock_stat

        with pytest.raises(DiskSpaceError) as exc_info:
            validate_disk_space(Path("/test/path"), required_space_mb=10)

        assert "10MB" in str(exc_info.value)
        assert "5.0MB" in str(exc_info.value)

    @patch("fascraft.validation.shutil.disk_usage")
    def test_validate_disk_space_permission_denied(self, mock_disk_usage):
        """Test disk space validation with permission denied."""
        mock_disk_usage.side_effect = OSError(13, "Permission denied")

        with pytest.raises(PermissionError) as exc_info:
            validate_disk_space(Path("/test/path"), required_space_mb=10)

        assert "check disk space" in str(exc_info.value)

    @patch("fascraft.validation.shutil.disk_usage")
    def test_validate_disk_space_no_space_error(self, mock_disk_usage):
        """Test disk space validation with 'No space left on device' error."""
        mock_disk_usage.side_effect = OSError(28, "No space left on device")

        with pytest.raises(DiskSpaceError) as exc_info:
            validate_disk_space(Path("/test/path"), required_space_mb=10)

        assert "10MB" in str(exc_info.value)
        assert "Unknown" in str(exc_info.value)

    @patch("fascraft.validation.shutil.disk_usage")
    def test_validate_disk_space_other_os_error(self, mock_disk_usage):
        """Test disk space validation with other OSError."""
        mock_disk_usage.side_effect = OSError(2, "No such file or directory")

        with pytest.raises(FileSystemError) as exc_info:
            validate_disk_space(Path("/test/path"), required_space_mb=10)

        assert "Failed to check disk space" in str(exc_info.value)


class TestValidateFileSystemWritable:
    """Test the validate_file_system_writable function."""

    def test_validate_file_system_writable_success(self, tmp_path):
        """Test file system writability validation with success."""
        # Should not raise an exception
        validate_file_system_writable(tmp_path)

    @patch("pathlib.Path.write_text")
    def test_validate_file_system_writable_readonly_error(self, mock_write_text):
        """Test file system writability validation with read-only error."""
        mock_write_text.side_effect = OSError(30, "Read-only file system")

        with pytest.raises(ReadOnlyFileSystemError) as exc_info:
            validate_file_system_writable(Path("/readonly/path"))

        assert "Cannot write to read-only file system" in str(exc_info.value)

    @patch("pathlib.Path.write_text")
    def test_validate_file_system_writable_permission_denied(self, mock_write_text):
        """Test file system writability validation with permission denied."""
        mock_write_text.side_effect = OSError(13, "Permission denied")

        with pytest.raises(PermissionError) as exc_info:
            validate_file_system_writable(Path("/restricted/path"))

        assert "write test file" in str(exc_info.value)

    @patch("pathlib.Path.write_text")
    def test_validate_file_system_writable_other_os_error(self, mock_write_text):
        """Test file system writability validation with other OSError."""
        mock_write_text.side_effect = OSError(2, "No such file or directory")

        with pytest.raises(FileSystemError) as exc_info:
            validate_file_system_writable(Path("/nonexistent/path"))

        assert "File system validation failed" in str(exc_info.value)


class TestValidatePathRobust:
    """Test the validate_path_robust function."""

    def test_validate_path_robust_success(self):
        """Test robust path validation with valid path."""
        result = validate_path_robust("/valid/path")

        assert isinstance(result, Path)
        assert result.as_posix() == "/valid/path"

    def test_validate_path_robust_too_long(self):
        """Test robust path validation with path too long."""
        long_path = "/" + "a" * 260  # Exceeds Windows MAX_PATH

        with pytest.raises(InvalidInputError) as exc_info:
            validate_path_robust(long_path)

        assert "Path is too long" in str(exc_info.value)
        assert "max 260 characters" in str(exc_info.value)

    def test_validate_path_robust_unsafe_characters(self):
        """Test robust path validation with unsafe characters."""
        unsafe_path = "/path/with/<unsafe>chars"

        with pytest.raises(InvalidInputError) as exc_info:
            validate_path_robust(unsafe_path)

        assert "Path contains unsafe characters" in str(exc_info.value)

    def test_validate_path_robust_windows_reserved_name(self):
        """Test robust path validation with Windows reserved name."""
        reserved_paths = [
            "/path/CON/file.txt",      # CON is a Windows reserved name
            "/CON/path/file.txt",      # Reserved name in first component
            "/path/file/PRN",          # Reserved name in last component
        ]

        for reserved_path in reserved_paths:
            with pytest.raises(InvalidInputError) as exc_info:
                validate_path_robust(reserved_path)

            assert "Path contains reserved system name" in str(exc_info.value)

    @patch("fascraft.validation.validate_network_path")
    def test_validate_path_robust_network_path(self, mock_validate_network):
        """Test robust path validation with network path."""
        network_path = "//server/share"

        validate_path_robust(network_path)

        mock_validate_network.assert_called_once()

    def test_validate_path_robust_validation_error_propagation(self):
        """Test that validation errors are properly propagated."""
        with patch("fascraft.validation.validate_network_path") as mock_validate:
            mock_validate.side_effect = NetworkPathError("/path", "Test error")

            with pytest.raises(InvalidInputError) as exc_info:
                validate_path_robust("//server/share")

            assert "Path validation failed" in str(exc_info.value)


class TestPathUtilityFunctions:
    """Test the utility functions for path validation."""

    def test_is_path_safe_valid(self):
        """Test is_path_safe with valid characters."""
        safe_paths = [
            "/normal/path",
            "C:\\Windows\\Path",  # Windows paths with backslashes
            "D:Programs\\App",    # Windows drive letter with colon
            "/path/with_underscores",
            "/path/with-dashes",
            "/path/with.dots",
            "/path/with spaces",
        ]

        for path in safe_paths:
            assert is_path_safe(path), f"Path should be safe: {path}"

    def test_is_path_safe_unsafe(self):
        """Test is_path_safe with unsafe characters."""
        unsafe_paths = [
            "/path/with/<brackets>",
            "/path/with/\"quotes\"",
            "/path/with/|pipe|",
            "/path/with/*wildcard*",
            "/path/with/?question?",
            "/path/with/&ampersand",
        ]

        for path in unsafe_paths:
            assert not is_path_safe(path), f"Path should be unsafe: {path}"

    def test_is_windows_reserved_name(self):
        """Test is_windows_reserved_name function."""
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]
        normal_names = ["file", "document", "test", "my_file"]

        for name in reserved_names:
            assert is_windows_reserved_name(name), f"Should be reserved: {name}"

        for name in normal_names:
            assert not is_windows_reserved_name(name), f"Should not be reserved: {name}"

    def test_is_network_path(self):
        """Test is_network_path function."""
        network_paths = [
            "\\\\server\\share",
            "//server/share",
            "\\\\192.168.1.1\\share",
        ]
        local_paths = [
            "/local/path",
            "C:\\local\\path",
            "./relative/path",
        ]

        for path in network_paths:
            assert is_network_path(Path(path)), f"Should be network path: {path}"

        for path in local_paths:
            assert not is_network_path(Path(path)), f"Should not be network path: {path}"


class TestValidateNetworkPath:
    """Test the validate_network_path function."""

    def test_validate_network_path_success(self, tmp_path):
        """Test network path validation with success."""
        # Create a test file to simulate network path validation
        test_file = tmp_path / ".fascraft_network_test"
        test_file.write_text("test")

        with patch("pathlib.Path.parent", return_value=tmp_path):
            # Should not raise an exception
            validate_network_path(Path("//server/share"))

    def test_validate_network_path_write_error(self):
        """Test network path validation with write error."""
        # Create a completely mocked path object
        mock_path = MagicMock()
        mock_parent = MagicMock()
        mock_test_file = MagicMock()

        # Set up the mock chain
        mock_path.parent = mock_parent
        mock_parent.exists.return_value = True
        mock_parent.__truediv__.return_value = mock_test_file

        # Make the test file write_text fail
        mock_test_file.write_text.side_effect = OSError(13, "Permission denied")

        with pytest.raises(NetworkPathError) as exc_info:
            validate_network_path(mock_path)

        assert "Network path validation failed" in str(exc_info.value)
