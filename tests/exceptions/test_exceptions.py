"""Tests for FasCraft custom exceptions."""

from fascraft.exceptions import (
    ConfigurationError,
    ConfigurationNotFoundError,
    DiskSpaceError,
    FasCraftError,
    FileSystemError,
    InvalidInputError,
    InvalidModuleNameError,
    InvalidProjectNameError,
    ModuleAlreadyExistsError,
    ModuleError,
    ModuleNotFoundError,
    NotFastAPIProjectError,
    PermissionError,
    ProjectAlreadyExistsError,
    ProjectError,
    ProjectNotFoundError,
    TemplateError,
    TemplateNotFoundError,
    TemplateRenderError,
    ValidationError,
)


class TestFasCraftError:
    """Test the base FasCraftError class."""

    def test_base_error_with_message(self):
        """Test creating base error with message only."""
        error = FasCraftError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.suggestion is None

    def test_base_error_with_suggestion(self):
        """Test creating base error with message and suggestion."""
        error = FasCraftError("Test error", "Test suggestion")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.suggestion == "Test suggestion"


class TestProjectError:
    """Test project-related errors."""

    def test_project_already_exists_error(self):
        """Test ProjectAlreadyExistsError creation and properties."""
        error = ProjectAlreadyExistsError("test_project", "/path/to/project")
        assert "test_project" in error.message
        assert "/path/to/project" in error.message
        assert "different project name" in error.suggestion.lower()

    def test_invalid_project_name_error(self):
        """Test InvalidProjectNameError creation and properties."""
        error = InvalidProjectNameError("invalid-name", "contains invalid characters")
        assert "invalid-name" in error.message
        assert "contains invalid characters" in error.message
        assert "valid python identifiers" in error.suggestion.lower()

    def test_project_not_found_error(self):
        """Test ProjectNotFoundError creation and properties."""
        error = ProjectNotFoundError("/path/to/project")
        assert "/path/to/project" in error.message
        assert "correct directory" in error.suggestion.lower()

    def test_not_fastapi_project_error(self):
        """Test NotFastAPIProjectError creation and properties."""
        error = NotFastAPIProjectError("/path/to/project")
        assert "/path/to/project" in error.message
        assert "fascraft new" in error.suggestion


class TestModuleError:
    """Test module-related errors."""

    def test_module_already_exists_error(self):
        """Test ModuleAlreadyExistsError creation and properties."""
        error = ModuleAlreadyExistsError("test_module", "/path/to/module")
        assert "test_module" in error.message
        assert "/path/to/module" in error.message
        assert "different module name" in error.suggestion.lower()

    def test_invalid_module_name_error(self):
        """Test InvalidModuleNameError creation and properties."""
        error = InvalidModuleNameError("invalid-module", "contains invalid characters")
        assert "invalid-module" in error.message
        assert "contains invalid characters" in error.message
        assert "valid python identifiers" in error.suggestion.lower()

    def test_module_not_found_error(self):
        """Test ModuleNotFoundError creation and properties."""
        error = ModuleNotFoundError("test_module", "/path/to/project")
        assert "test_module" in error.message
        assert "/path/to/project" in error.message
        assert "fascraft list" in error.suggestion


class TestConfigurationError:
    """Test configuration-related errors."""

    def test_configuration_not_found_error(self):
        """Test ConfigurationNotFoundError creation and properties."""
        error = ConfigurationNotFoundError("/path/to/config")
        assert "/path/to/config" in error.message
        assert "fascraft config create" in error.suggestion


class TestPermissionError:
    """Test permission-related errors."""

    def test_permission_error(self):
        """Test PermissionError creation and properties."""
        error = PermissionError("/path/to/file", "read")
        assert "/path/to/file" in error.message
        assert "read" in error.message
        assert "permissions" in error.suggestion.lower()


class TestDiskSpaceError:
    """Test disk space errors."""

    def test_disk_space_error(self):
        """Test DiskSpaceError creation and properties."""
        error = DiskSpaceError("/path/to/file", "write")
        assert "/path/to/file" in error.message
        assert "write" in error.message
        assert "disk space" in error.suggestion.lower()


class TestTemplateError:
    """Test template-related errors."""

    def test_template_not_found_error(self):
        """Test TemplateNotFoundError creation and properties."""
        error = TemplateNotFoundError("test_template", "/path/to/templates")
        assert "test_template" in error.message
        assert "/path/to/templates" in error.message
        assert "template exists" in error.suggestion.lower()

    def test_template_render_error(self):
        """Test TemplateRenderError creation and properties."""
        error = TemplateRenderError("test_template", "syntax error")
        assert "test_template" in error.message
        assert "syntax error" in error.message
        assert "project configuration" in error.suggestion.lower()


class TestFileSystemError:
    """Test file system errors."""

    def test_file_system_error(self):
        """Test FileSystemError creation and properties."""
        error = FileSystemError("Failed to create file")
        assert "Failed to create file" in error.message
        assert "file permissions" in error.suggestion.lower()


class TestValidationError:
    """Test validation errors."""

    def test_validation_error(self):
        """Test ValidationError creation and properties."""
        error = ValidationError("Invalid input")
        assert "Invalid input" in error.message
        # ValidationError is a base class, so no suggestion
        assert error.suggestion is None


class TestInvalidInputError:
    """Test invalid input errors."""

    def test_invalid_input_error(self):
        """Test InvalidInputError creation and properties."""
        error = InvalidInputError("field_name", "invalid_value", "reason")
        assert "field_name" in error.message
        assert "invalid_value" in error.message
        assert "reason" in error.message
        assert "valid value" in error.suggestion.lower()


class TestErrorInheritance:
    """Test error class inheritance hierarchy."""

    def test_error_inheritance(self):
        """Test that all errors properly inherit from base classes."""
        # Test project errors
        assert issubclass(ProjectError, FasCraftError)
        assert issubclass(ProjectAlreadyExistsError, ProjectError)
        assert issubclass(InvalidProjectNameError, ProjectError)
        assert issubclass(ProjectNotFoundError, ProjectError)
        assert issubclass(NotFastAPIProjectError, ProjectError)

        # Test module errors
        assert issubclass(ModuleError, FasCraftError)
        assert issubclass(ModuleAlreadyExistsError, ModuleError)
        assert issubclass(InvalidModuleNameError, ModuleError)
        assert issubclass(ModuleNotFoundError, ModuleError)

        # Test configuration errors
        assert issubclass(ConfigurationError, FasCraftError)
        assert issubclass(ConfigurationNotFoundError, ConfigurationError)

        # Test other errors
        assert issubclass(PermissionError, FileSystemError)
        assert issubclass(DiskSpaceError, FileSystemError)
        assert issubclass(TemplateError, FasCraftError)
        assert issubclass(TemplateNotFoundError, TemplateError)
        assert issubclass(TemplateRenderError, TemplateError)
        assert issubclass(FileSystemError, FasCraftError)
        assert issubclass(ValidationError, FasCraftError)
        assert issubclass(InvalidInputError, ValidationError)


class TestErrorMessages:
    """Test error message formatting and content."""

    def test_error_messages_are_strings(self):
        """Test that all error messages are strings."""
        errors = [
            ProjectAlreadyExistsError("test", "/path"),
            InvalidProjectNameError("test", "invalid format"),
            ProjectNotFoundError("/path"),
            NotFastAPIProjectError("/path"),
            ModuleAlreadyExistsError("test", "/path"),
            InvalidModuleNameError("test", "invalid format"),
            ModuleNotFoundError("test", "/path"),
            ConfigurationNotFoundError("/path"),
            PermissionError("/path", "read"),
            DiskSpaceError("path", "write"),
            TemplateNotFoundError("test"),
            TemplateRenderError("test", "error"),
            FileSystemError("message"),
            ValidationError("message"),
            InvalidInputError("field", "value", "reason"),
        ]

        for error in errors:
            assert isinstance(error.message, str)
            assert len(error.message) > 0
            if error.suggestion:
                assert isinstance(error.suggestion, str)
                assert len(error.suggestion) > 0

    def test_error_messages_are_helpful(self):
        """Test that error messages provide helpful information."""
        error = ProjectAlreadyExistsError("my_project", "/tmp/my_project")
        assert "my_project" in error.message
        assert "/tmp/my_project" in error.message
        assert error.suggestion is not None
        assert len(error.suggestion) > 10  # Should be substantial
