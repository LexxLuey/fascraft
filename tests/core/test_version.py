"""Tests for the version module."""

from unittest.mock import mock_open, patch

from fascraft.version import get_version, get_version_info


class TestVersionModule:
    """Test the version module functionality."""

    def test_get_version_from_pyproject_toml(self):
        """Test getting version from pyproject.toml."""
        mock_toml_data = {"tool": {"poetry": {"version": "1.2.3"}}}

        with patch("builtins.open", mock_open()):
            with patch("fascraft.version.tomllib.load", return_value=mock_toml_data):
                with patch("pathlib.Path.exists", return_value=True):
                    version = get_version()
                    assert version == "1.2.3"

    def test_get_version_fallback_to_metadata(self):
        """Test fallback to package metadata when pyproject.toml fails."""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("importlib.metadata.version", return_value="2.0.0"):
                version = get_version()
                assert version == "2.0.0"

    def test_get_version_final_fallback(self):
        """Test final fallback when all methods fail."""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("importlib.metadata.version", side_effect=Exception()):
                version = get_version()
                assert version == "unknown"

    def test_get_version_info(self):
        """Test getting comprehensive version information."""
        with patch("fascraft.version.get_version", return_value="5.0.0"):
            info = get_version_info()
            assert info["version"] == "5.0.0"
            assert info["author"] == "FasCraft Team"
            assert info["email"] == "support@fascraft.dev"

    def test_pyproject_toml_file_not_found(self):
        """Test handling when pyproject.toml file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("importlib.metadata.version", return_value="6.0.0"):
                version = get_version()
                assert version == "6.0.0"

    def test_pyproject_toml_key_error(self):
        """Test handling when pyproject.toml has missing keys."""
        mock_toml_data = {"tool": {}}  # Missing poetry section

        with patch("builtins.open", mock_open()):
            with patch("fascraft.version.tomllib.load", return_value=mock_toml_data):
                with patch("pathlib.Path.exists", return_value=True):
                    with patch("importlib.metadata.version", return_value="7.0.0"):
                        version = get_version()
                        assert version == "7.0.0"

    def test_pyproject_toml_io_error(self):
        """Test handling when pyproject.toml can't be read."""
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("importlib.metadata.version", return_value="8.0.0"):
                    version = get_version()
                    assert version == "8.0.0"
