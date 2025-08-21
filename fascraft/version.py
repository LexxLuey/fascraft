"""Version information for FasCraft."""

import tomllib
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
    except ImportError:
        try:
            # Fallback for older Python versions
            import pkg_resources

            return pkg_resources.get_distribution("fascraft").version
        except Exception:
            pass

    # Final fallback - read from git tags or return unknown
    return get_version_from_git() or "unknown"


def get_version_from_git() -> str | None:
    """Try to get version from git tags."""
    try:
        import subprocess

        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        if result.returncode == 0:
            return result.stdout.strip().lstrip("v")
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def get_version_info() -> dict:
    """Get comprehensive version information."""
    return {
        "version": get_version(),
        "author": "FasCraft Team",
        "email": "support@fascraft.dev",
    }


# For backward compatibility and direct import
__version__ = get_version()
