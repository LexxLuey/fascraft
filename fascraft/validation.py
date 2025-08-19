"""Input validation utilities for FasCraft CLI."""

import os
import re
import shutil
from pathlib import Path

from fascraft.exceptions import (
    DiskSpaceError,
    FileSystemError,
    InvalidInputError,
    InvalidModuleNameError,
    InvalidProjectNameError,
    NetworkPathError,
    PermissionError,
    ReadOnlyFileSystemError,
)


def validate_project_name(project_name: str) -> str:
    """Validate project name and return cleaned version."""
    if not project_name or not project_name.strip():
        raise InvalidProjectNameError("", "Project name cannot be empty or whitespace")

    # Clean the name
    cleaned_name = project_name.strip()

    # Check for valid project name (allows hyphens, more flexible than Python identifier)
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", cleaned_name):
        raise InvalidProjectNameError(
            cleaned_name,
            "must start with a letter or underscore and contain only letters, numbers, underscores, and hyphens",
        )

    # Check for reserved Python keywords
    reserved_keywords = {
        "and",
        "as",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
        "false",
        "none",
        "true",
    }

    if cleaned_name.lower() in reserved_keywords:
        raise InvalidProjectNameError(
            cleaned_name, "cannot be a Python reserved keyword"
        )

    # Check length
    if len(cleaned_name) > 50:
        raise InvalidProjectNameError(cleaned_name, "must be 50 characters or less")

    return cleaned_name


def validate_module_name(module_name: str) -> str:
    """Validate module name and return cleaned version."""
    if not module_name or not module_name.strip():
        raise InvalidModuleNameError("", "Module name cannot be empty or whitespace")

    # Clean the name
    cleaned_name = module_name.strip()

    # Check for valid Python identifier (modules must be valid Python identifiers)
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", cleaned_name):
        raise InvalidModuleNameError(
            cleaned_name,
            "must be a valid Python identifier (start with letter/underscore, contain only letters, numbers, and underscores)",
        )

    # Check for reserved Python keywords
    reserved_keywords = {
        "and",
        "as",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
        "false",
        "none",
        "true",
    }

    if cleaned_name.lower() in reserved_keywords:
        raise InvalidModuleNameError(
            cleaned_name, "cannot be a Python reserved keyword"
        )

    # Check length
    if len(cleaned_name) > 30:
        raise InvalidModuleNameError(cleaned_name, "must be 30 characters or less")

    return cleaned_name


def validate_path(path) -> Path:
    """Validate and return a Path object."""
    # Handle both string and Path objects
    if isinstance(path, Path):
        path_str = str(path)
    else:
        path_str = str(path) if path else ""

    if not path_str or not path_str.strip():
        raise InvalidInputError("path", path_str, "Path cannot be empty or whitespace")

    try:
        path_obj = Path(path_str.strip()).resolve()
        return path_obj
    except (OSError, RuntimeError) as e:
        raise InvalidInputError("path", path_str, f"Invalid path: {str(e)}") from e


def validate_project_path(project_path: Path, project_name: str) -> None:
    """Validate that the project path is suitable for project creation."""
    # Check if project directory already exists
    if project_path.exists():
        raise InvalidInputError(
            "project_path",
            str(project_path),
            f"Project directory already exists at {project_path}",
        )

    # Check parent directory permissions (but don't require it to exist)
    parent_dir = project_path.parent

    # If parent directory exists, validate it
    if parent_dir.exists():
        if not parent_dir.is_dir():
            raise InvalidInputError(
                "project_path",
                str(project_path),
                f"Parent path is not a directory: {parent_dir}",
            )

        # Check write permissions
        if not os.access(parent_dir, os.W_OK):
            raise PermissionError(str(parent_dir), "write")

        # Check disk space (rough estimate: 100KB minimum)
        try:
            free_space = shutil.disk_usage(parent_dir).free
            if free_space < 102400:  # 100KB in bytes
                raise DiskSpaceError("100KB", f"{free_space // 1024}KB")
        except OSError:
            # Skip disk space check if we can't determine it
            pass
    # If parent directory doesn't exist, we'll create it during project creation
    # This allows for nested directory creation scenarios


def validate_fastapi_project(project_path: Path) -> None:
    """Validate that the path contains a FastAPI project."""
    if not project_path.exists():
        raise InvalidInputError(
            "project_path", str(project_path), "Project path does not exist"
        )

    if not project_path.is_dir():
        raise InvalidInputError(
            "project_path", str(project_path), "Project path is not a directory"
        )

    # Check for FastAPI indicators
    main_py = project_path / "main.py"
    pyproject_toml = project_path / "pyproject.toml"
    requirements_txt = project_path / "requirements.txt"

    has_fastapi = False

    # Check main.py for FastAPI imports
    if main_py.exists():
        try:
            content = main_py.read_text(encoding="utf-8")
            if "FastAPI" in content or "fastapi" in content:
                has_fastapi = True
        except (OSError, UnicodeDecodeError):
            pass

    # Check pyproject.toml for FastAPI dependency
    if pyproject_toml.exists():
        try:
            content = pyproject_toml.read_text(encoding="utf-8")
            if "fastapi" in content.lower():
                has_fastapi = True
        except (OSError, UnicodeDecodeError):
            pass

    # Check requirements.txt for FastAPI dependency
    if requirements_txt.exists():
        try:
            content = requirements_txt.read_text(encoding="utf-8")
            if "fastapi" in content.lower():
                has_fastapi = True
        except (OSError, UnicodeDecodeError):
            pass

    if not has_fastapi:
        raise InvalidInputError(
            "project_path",
            str(project_path),
            "Path does not contain a FastAPI project (missing FastAPI imports or dependencies)",
        )


def validate_config_key(key: str) -> None:
    """Validate configuration key format."""
    if not key or not key.strip():
        raise InvalidInputError(
            "key", key, "Configuration key cannot be empty or whitespace"
        )

    # Check format: section.key
    if "." not in key:
        raise InvalidInputError(
            "key",
            key,
            "Configuration key must be in format 'section.key' (e.g., 'project.name')",
        )

    section, setting = key.split(".", 1)

    if not section.strip() or not setting.strip():
        raise InvalidInputError(
            "key", key, "Both section and setting must be non-empty"
        )

    # Validate section and setting names
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", section.strip()):
        raise InvalidInputError(
            "key", key, f"Section name '{section}' must be a valid identifier"
        )

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", setting.strip()):
        raise InvalidInputError(
            "key", key, f"Setting name '{setting}' must be a valid identifier"
        )


def validate_config_value(value: str) -> None:
    """Validate configuration value."""
    if not value:
        raise InvalidInputError(
            "value", str(value), "Configuration value cannot be None"
        )

    # Check length
    if len(str(value)) > 1000:
        raise InvalidInputError(
            "value", str(value), "Configuration value must be 1000 characters or less"
        )


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations."""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, "_")

    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")

    # Ensure it's not empty
    if not filename:
        filename = "unnamed"

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename


def validate_python_version(version: str) -> None:
    """Validate Python version string."""
    if not version or not version.strip():
        raise InvalidInputError(
            "python_version", version, "Python version cannot be empty"
        )

    # Check format: major.minor or major.minor.patch
    version_pattern = r"^(\d+)\.(\d+)(?:\.(\d+))?$"
    match = re.match(version_pattern, version.strip())

    if not match:
        raise InvalidInputError(
            "python_version",
            version,
            "Python version must be in format 'major.minor' or 'major.minor.patch' (e.g., '3.10' or '3.10.0')",
        )

    major, minor = int(match.group(1)), int(match.group(2))

    # Check minimum version (3.8+)
    if major < 3 or (major == 3 and minor < 8):
        raise InvalidInputError(
            "python_version", version, "Python version must be 3.8 or higher"
        )

    # Check maximum version (3.12+)
    if major > 3 or (major == 3 and minor > 12):
        raise InvalidInputError(
            "python_version", version, "Python version must be 3.12 or lower"
        )


def validate_disk_space(path: Path, required_space_mb: int = 10) -> None:
    """Validate sufficient disk space is available."""
    try:
        # Get disk space info
        stat = shutil.disk_usage(path)
        available_mb = stat.free / (1024 * 1024)

        if available_mb < required_space_mb:
            raise DiskSpaceError(f"{required_space_mb}MB", f"{available_mb:.1f}MB")
    except OSError as e:
        # Handle network paths or permission issues
        if "No space left on device" in str(e):
            raise DiskSpaceError(f"{required_space_mb}MB", "Unknown") from e
        elif "Permission denied" in str(e):
            raise PermissionError(str(path), "check disk space") from e
        else:
            raise FileSystemError(f"Failed to check disk space: {str(e)}") from e


def validate_file_system_writable(path: Path) -> None:
    """Validate that the file system is writable."""
    try:
        test_file = path / ".fascraft_test_write"
        test_file.write_text("test")
        test_file.unlink()
    except OSError as e:
        if "Read-only file system" in str(e):
            raise ReadOnlyFileSystemError(str(path)) from e
        elif "Permission denied" in str(e):
            raise PermissionError(str(path), "write test file") from e
        else:
            raise FileSystemError(f"File system validation failed: {str(e)}") from e


def validate_path_robust(path: str) -> Path:
    """Robust path validation with edge case handling."""
    try:
        path_obj = Path(path)

        # Handle extremely long paths
        if len(str(path_obj)) > 260:  # Windows MAX_PATH limit
            raise InvalidInputError(
                "path", path, "Path is too long (max 260 characters)"
            )

        # Handle special characters and non-ASCII
        if not is_path_safe(str(path_obj)):
            raise InvalidInputError("path", path, "Path contains unsafe characters")

        # Handle reserved system names (Windows)
        for part in path_obj.parts:
            if is_windows_reserved_name(part):
                raise InvalidInputError(
                    "path", path, "Path contains reserved system name"
                )

        # Handle network path issues
        if is_network_path(path_obj):
            validate_network_path(path_obj)

        return path_obj

    except Exception as e:
        if isinstance(e, InvalidInputError):
            raise
        raise InvalidInputError(
            "path", path, f"Path validation failed: {str(e)}"
        ) from e


def is_path_safe(path_str: str) -> bool:
    """Check if path contains only safe characters."""
    # Allow alphanumeric, spaces, dots, hyphens, underscores, forward slashes, backslashes, and colons
    # Note: Colons are allowed for Windows drive letters (e.g., C:), backslashes for Windows paths
    safe_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-_/\\:"
    )
    return all(c in safe_chars for c in path_str)


def is_windows_reserved_name(name: str) -> bool:
    """Check if name is a Windows reserved name."""
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    return name.upper() in reserved_names


def is_network_path(path: Path) -> bool:
    """Check if path is a network path."""
    return str(path).startswith(("\\\\", "//"))


def validate_network_path(path: Path) -> None:
    """Validate network path accessibility."""
    try:
        # Try to access the parent directory
        parent = path.parent
        if parent.exists():
            # Test write access
            test_file = parent / ".fascraft_network_test"
            test_file.write_text("test")
            test_file.unlink()
    except Exception as e:
        raise NetworkPathError(
            str(path), f"Network path validation failed: {str(e)}"
        ) from e
