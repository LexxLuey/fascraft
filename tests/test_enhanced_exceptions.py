"""Tests for enhanced exception types in FasCraft."""


from fascraft.exceptions import (
    CorruptedTemplateError,
    ReadOnlyFileSystemError,
    PartialFailureError,
    NetworkPathError,
    TemplateError,
    FasCraftError,
    FileSystemError,
)


class TestCorruptedTemplateError:
    """Test the CorruptedTemplateError exception."""

    def test_corrupted_template_error_creation(self):
        """Test creating a CorruptedTemplateError."""
        error = CorruptedTemplateError("test.jinja2", "Syntax error")

        assert error.message == "Template 'test.jinja2' is corrupted: Syntax error"
        assert error.suggestion == "Reinstall FasCraft or restore from backup"
        assert str(error) == "Template 'test.jinja2' is corrupted: Syntax error"

    def test_corrupted_template_error_with_details(self):
        """Test creating a CorruptedTemplateError with detailed error message."""
        error = CorruptedTemplateError("config.py.jinja2", "Invalid Jinja2 syntax")

        assert "Invalid Jinja2 syntax" in error.message
        assert "config.py.jinja2" in error.message


class TestReadOnlyFileSystemError:
    """Test the ReadOnlyFileSystemError exception."""

    def test_readonly_filesystem_error_creation(self):
        """Test creating a ReadOnlyFileSystemError."""
        error = ReadOnlyFileSystemError("/readonly/path")

        assert error.message == "Cannot write to read-only file system at /readonly/path"
        assert error.suggestion == "Check file system permissions or choose a different location"
        assert str(error) == "Cannot write to read-only file system at /readonly/path"

    def test_readonly_filesystem_error_with_different_path(self):
        """Test creating a ReadOnlyFileSystemError with different path."""
        error = ReadOnlyFileSystemError("/mnt/readonly")

        assert "/mnt/readonly" in error.message


class TestPartialFailureError:
    """Test the PartialFailureError exception."""

    def test_partial_failure_error_creation(self):
        """Test creating a PartialFailureError."""
        warnings = ["Template rendering failed", "Disk space low"]
        error = PartialFailureError("Operation partially completed", warnings)

        assert error.message == "Operation partially completed"
        assert error.suggestion == "Operation completed with warnings - some features may not work correctly"
        assert error.warnings == warnings
        assert str(error) == "Operation partially completed"

    def test_partial_failure_error_with_empty_warnings(self):
        """Test creating a PartialFailureError with empty warnings."""
        error = PartialFailureError("Minimal success", [])

        assert error.warnings == []
        assert "Minimal success" in error.message


class TestNetworkPathError:
    """Test the NetworkPathError exception."""

    def test_network_path_error_creation(self):
        """Test creating a NetworkPathError."""
        error = NetworkPathError("\\\\server\\share", "Access denied")

        assert error.message == "Network path error at \\\\server\\share: Access denied"
        assert error.suggestion == "Check network connectivity or use local paths"
        assert str(error) == "Network path error at \\\\server\\share: Access denied"

    def test_network_path_error_with_different_details(self):
        """Test creating a NetworkPathError with different error details."""
        error = NetworkPathError("//remote/path", "Connection timeout")

        assert "Connection timeout" in error.message
        assert "//remote/path" in error.message


class TestExceptionInheritance:
    """Test that exceptions inherit correctly from base classes."""

    def test_corrupted_template_error_inheritance(self):
        """Test that CorruptedTemplateError inherits from TemplateError."""
        error = CorruptedTemplateError("test.jinja2", "Error")

        assert isinstance(error, CorruptedTemplateError)
        assert isinstance(error, TemplateError)
        assert isinstance(error, FasCraftError)
        assert isinstance(error, Exception)

    def test_readonly_filesystem_error_inheritance(self):
        """Test that ReadOnlyFileSystemError inherits from FileSystemError."""
        error = ReadOnlyFileSystemError("/path")

        assert isinstance(error, ReadOnlyFileSystemError)
        assert isinstance(error, FileSystemError)
        assert isinstance(error, FasCraftError)
        assert isinstance(error, Exception)

    def test_partial_failure_error_inheritance(self):
        """Test that PartialFailureError inherits from FasCraftError."""
        error = PartialFailureError("Message", [])

        assert isinstance(error, PartialFailureError)
        assert isinstance(error, FasCraftError)
        assert isinstance(error, Exception)

    def test_network_path_error_inheritance(self):
        """Test that NetworkPathError inherits from FileSystemError."""
        error = NetworkPathError("/path", "Error")

        assert isinstance(error, NetworkPathError)
        assert isinstance(error, FileSystemError)
        assert isinstance(error, FasCraftError)
        assert isinstance(error, Exception)
