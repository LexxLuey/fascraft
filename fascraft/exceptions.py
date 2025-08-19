"""Custom exceptions for FasCraft CLI."""


class FasCraftError(Exception):
    """Base exception for all FasCraft errors."""

    def __init__(self, message: str, suggestion: str | None = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)


class ProjectError(FasCraftError):
    """Raised when there's an issue with project operations."""

    pass


class ProjectAlreadyExistsError(ProjectError):
    """Raised when trying to create a project that already exists."""

    def __init__(self, project_name: str, project_path: str):
        message = f"Project '{project_name}' already exists at {project_path}"
        suggestion = "Use a different project name or remove the existing directory"
        super().__init__(message, suggestion)


class InvalidProjectNameError(ProjectError):
    """Raised when the project name is invalid."""

    def __init__(self, project_name: str, details: str = ""):
        if details:
            message = f"Invalid project name: '{project_name}' - {details}"
        else:
            message = f"Invalid project name: '{project_name}'"
        suggestion = "Project names must be valid Python identifiers and contain only letters, numbers, and underscores"
        super().__init__(message, suggestion)


class ProjectNotFoundError(ProjectError):
    """Raised when a project cannot be found."""

    def __init__(self, project_path: str):
        message = f"Project not found at: {project_path}"
        suggestion = (
            "Make sure you're in the correct directory or specify the correct path"
        )
        super().__init__(message, suggestion)


class NotFastAPIProjectError(ProjectError):
    """Raised when the directory is not a FastAPI project."""

    def __init__(self, project_path: str):
        message = f"'{project_path}' is not a FastAPI project"
        suggestion = "Make sure you're in a FastAPI project directory or use 'fascraft new' to create one"
        super().__init__(message, suggestion)


class ModuleError(FasCraftError):
    """Raised when there's an issue with module operations."""

    pass


class ModuleAlreadyExistsError(ModuleError):
    """Raised when trying to create a module that already exists."""

    def __init__(self, module_name: str, module_path: str):
        message = f"Module '{module_name}' already exists at {module_path}"
        suggestion = "Use a different module name or remove the existing module"
        super().__init__(message, suggestion)


class InvalidModuleNameError(ModuleError):
    """Raised when the module name is invalid."""

    def __init__(self, module_name: str, details: str = ""):
        if details:
            message = f"Invalid module name: '{module_name}' - {details}"
        else:
            message = f"Invalid module name: '{module_name}'"
        suggestion = "Module names must be valid Python identifiers and contain only letters, numbers, and underscores"
        super().__init__(message, suggestion)


class ModuleNotFoundError(ModuleError):
    """Raised when a module cannot be found."""

    def __init__(self, module_name: str, project_path: str):
        message = f"Module '{module_name}' not found in project at {project_path}"
        suggestion = "Use 'fascraft list' to see available modules or 'fascraft generate' to create a new one"
        super().__init__(message, suggestion)


class ConfigurationError(FasCraftError):
    """Raised when there's an issue with configuration."""

    pass


class ConfigurationNotFoundError(ConfigurationError):
    """Raised when a configuration file cannot be found."""

    def __init__(self, config_path: str):
        message = f"Configuration file not found at: {config_path}"
        suggestion = "Use 'fascraft config create' to create a new configuration file"
        super().__init__(message, suggestion)


class InvalidConfigurationError(ConfigurationError):
    """Raised when a configuration file is invalid."""

    def __init__(self, config_path: str, details: str):
        message = f"Invalid configuration file at {config_path}: {details}"
        suggestion = "Use 'fascraft config validate' to check for issues or 'fascraft config create' to regenerate"
        super().__init__(message, suggestion)


class TemplateError(FasCraftError):
    """Raised when there's an issue with template rendering."""

    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a required template cannot be found."""

    def __init__(self, template_name: str, template_path: str = ""):
        if template_path:
            message = f"Template not found: {template_name} at {template_path}"
        else:
            message = f"Template not found: {template_name}"
        suggestion = "Check if the template exists or this might be a FasCraft installation issue"
        super().__init__(message, suggestion)


class TemplateRenderError(TemplateError):
    """Raised when template rendering fails."""

    def __init__(self, template_name: str, error: str):
        message = f"Failed to render template '{template_name}': {error}"
        suggestion = "Check your project configuration or report this as a bug"
        super().__init__(message, suggestion)


class FileSystemError(FasCraftError):
    """Raised when there's an issue with file system operations."""

    def __init__(self, message: str, suggestion: str | None = None):
        if suggestion is None:
            suggestion = "Check file permissions and disk space"
        super().__init__(message, suggestion)


class PermissionError(FileSystemError):
    """Raised when there are permission issues."""

    def __init__(self, path: str, operation: str):
        message = f"Permission denied: Cannot {operation} at {path}"
        suggestion = "Check file permissions or run with appropriate privileges"
        super().__init__(message, suggestion)


class DiskSpaceError(FileSystemError):
    """Raised when there's insufficient disk space."""

    def __init__(self, required_space: str, available_space: str):
        message = f"Insufficient disk space. Required: {required_space}, Available: {available_space}"
        suggestion = "Free up disk space or choose a different location"
        super().__init__(message, suggestion)


class ValidationError(FasCraftError):
    """Raised when input validation fails."""

    pass


class InvalidInputError(ValidationError):
    """Raised when user input is invalid."""

    def __init__(self, field: str, value: str, reason: str):
        message = f"Invalid {field}: '{value}' - {reason}"
        suggestion = "Please provide a valid value and try again"
        super().__init__(message, suggestion)


class DependencyError(FasCraftError):
    """Raised when there are dependency-related issues."""

    pass


class MissingDependencyError(DependencyError):
    """Raised when a required dependency is missing."""

    def __init__(self, dependency: str):
        message = f"Missing required dependency: {dependency}"
        suggestion = f"Install the dependency with: pip install {dependency}"
        super().__init__(message, suggestion)


class VersionConflictError(DependencyError):
    """Raised when there are version conflicts."""

    def __init__(self, dependency: str, required_version: str, installed_version: str):
        message = f"Version conflict for {dependency}. Required: {required_version}, Installed: {installed_version}"
        suggestion = f"Update the dependency: pip install --upgrade {dependency}"
        super().__init__(message, suggestion)


class CorruptedTemplateError(TemplateError):
    """Raised when a template file is corrupted or invalid."""

    def __init__(self, template_name: str, details: str):
        message = f"Template '{template_name}' is corrupted: {details}"
        suggestion = "Reinstall FasCraft or restore from backup"
        super().__init__(message, suggestion)


class ReadOnlyFileSystemError(FileSystemError):
    """Raised when trying to write to a read-only file system."""

    def __init__(self, path: str):
        message = f"Cannot write to read-only file system at {path}"
        suggestion = "Check file system permissions or choose a different location"
        super().__init__(message, suggestion)


class PartialFailureError(FasCraftError):
    """Raised when an operation partially fails but can continue."""

    def __init__(self, message: str, warnings: list[str]):
        self.warnings = warnings
        super().__init__(
            message,
            "Operation completed with warnings - some features may not work correctly",
        )


class NetworkPathError(FileSystemError):
    """Raised when there are issues with network paths."""

    def __init__(self, path: str, details: str):
        message = f"Network path error at {path}: {details}"
        suggestion = "Check network connectivity or use local paths"
        super().__init__(message, suggestion)
