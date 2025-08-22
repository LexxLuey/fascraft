"""Version information for FasCraft."""

try:
    import tomllib
except ImportError:
    # Fallback for Python < 3.11
    import tomli as tomllib

from pathlib import Path


def get_version() -> str:
    """Get the current FasCraft version from pyproject.toml."""
    try:
        # Try to read from pyproject.toml first
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data["tool"]["poetry"]["version"]
    except (KeyError, FileNotFoundError, OSError):
        pass

    try:
        # Fallback to package metadata (for installed packages)
        import importlib.metadata

        return importlib.metadata.version("fascraft")
    except Exception:  # nosec B110 - Intentional fallback, don't expose internal errors
        pass

    # Final fallback - return unknown
    return "unknown"


def get_version_info() -> dict:
    """Get comprehensive version information."""
    return {
        "version": get_version(),
        "author": "FasCraft Team",
        "email": "support@fascraft.dev",
    }


# For backward compatibility and direct import
__version__ = get_version()
