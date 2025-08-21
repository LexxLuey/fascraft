"""Tests to cover missing lines in fascraft/commands/remove.py."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.list import analyze_module
from fascraft.commands.remove import (
    is_domain_module,
    remove_module,
    remove_module_files,
    update_main_py_after_removal,
)


class TestRemoveCoverage:
    """Test class to cover missing lines in remove.py."""

    def test_remove_module_path_not_exists(self):
        """Test remove_module when path doesn't exist (line 34-39)."""
        with patch("fascraft.commands.remove.console.print"):
            with pytest.raises(typer.Exit):
                remove_module("nonexistent-path", "test-module", force=False)

    def test_remove_module_not_fastapi_project(self):
        """Test remove_module when path is not a FastAPI project (line 42-49)."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "fascraft.commands.remove.is_fastapi_project", return_value=False
            ):
                with patch("fascraft.commands.remove.console.print"):
                    with pytest.raises(typer.Exit):
                        remove_module("test-path", "test-module", force=False)

    def test_remove_module_module_not_exists(self):
        """Test remove_module when module doesn't exist (line 52-59)."""
        with patch("pathlib.Path.exists", side_effect=[True, False]):
            with patch(
                "fascraft.commands.remove.is_fastapi_project", return_value=True
            ):
                with patch("fascraft.commands.remove.console.print"):
                    with pytest.raises(typer.Exit):
                        remove_module("test-path", "test-module", force=False)

    def test_remove_module_not_domain_module(self):
        """Test remove_module when module is not a domain module (line 62-69)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.remove.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.remove.is_domain_module", return_value=False
                ):
                    with patch("fascraft.commands.remove.console.print"):
                        with pytest.raises(typer.Exit):
                            remove_module("test-path", "test-module", force=False)

    def test_remove_module_cancelled(self):
        """Test remove_module when user cancels (line 84-86)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.remove.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.remove.is_domain_module", return_value=True
                ):
                    with patch("fascraft.commands.remove.analyze_module"):
                        with patch("fascraft.commands.remove.display_removal_preview"):
                            with patch(
                                "fascraft.commands.remove.confirm_removal",
                                return_value=False,
                            ):
                                with patch("fascraft.commands.remove.console.print"):
                                    # Should return without removing
                                    remove_module(
                                        "test-path", "test-module", force=False
                                    )

    def test_is_domain_module_missing_files(self):
        """Test is_domain_module with missing required files (line 66-76)."""
        with patch("pathlib.Path.exists", return_value=False):
            module_path = Path("test-module")
            result = is_domain_module(module_path)
            assert result is False

    def test_analyze_module_with_files(self):
        """Test analyze_module with existing files (line 84-86)."""
        # Create a simple test that will actually work
        # I need to mock BOTH exists AND stat since the function calls both!

        # Mock the Path.exists method to return True for all files
        original_exists = Path.exists
        original_stat = Path.stat

        def mock_exists(self):
            return True

        def mock_stat(self):
            # Return a mock stat object with size
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_size = 100
            return mock_stat_obj

        # Apply both mocks
        Path.exists = mock_exists
        Path.stat = mock_stat

        try:
            # Test the function
            module_path = Path("test-module")
            result = analyze_module(module_path)

            # Verify the logic works
            assert result["size"] > 0  # Should have size since all files exist
            assert len(result["files"]) > 0  # Should have files
        finally:
            # Restore original methods
            Path.exists = original_exists
            Path.stat = original_stat

    def test_remove_module_files_success(self):
        """Test remove_module_files function."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.iterdir") as mock_iterdir:
                mock_iterdir.return_value = [Path("test.py")]
                with patch("pathlib.Path.is_file", return_value=True):
                    with patch("pathlib.Path.unlink"):
                        with patch("pathlib.Path.rmdir"):
                            with patch("shutil.rmtree"):  # Mock shutil.rmtree
                                module_path = Path("test-module")
                                remove_module_files(module_path)

    def test_update_main_py_after_removal_file_not_exists(self):
        """Test update_main_py_after_removal when main.py doesn't exist (line 102-109)."""
        with patch("pathlib.Path.exists", return_value=False):
            project_path = Path("test-project")
            update_main_py_after_removal(project_path, "test-module")
            # Should return early without doing anything

    def test_remove_module_exception_handling(self):
        """Test remove_module exception handling (lines 102-109)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.remove.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.remove.is_domain_module", return_value=True
                ):
                    with patch("fascraft.commands.remove.analyze_module"):
                        with patch("fascraft.commands.remove.display_removal_preview"):
                            with patch(
                                "fascraft.commands.remove.confirm_removal",
                                return_value=True,
                            ):
                                with patch(
                                    "fascraft.commands.remove.remove_module_files"
                                ) as mock_remove:
                                    # Make remove_module_files raise an exception
                                    mock_remove.side_effect = Exception("Test error")
                                    with patch(
                                        "fascraft.commands.remove.console.print"
                                    ) as mock_print:
                                        with pytest.raises(typer.Exit):
                                            remove_module(
                                                "test-path", "test-module", force=False
                                            )

                                        # Verify error text was created and printed
                                        assert mock_print.call_count >= 1

    def test_update_main_py_after_removal_warning_message(self):
        """Test line 239: warning message when main.py not found."""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("fascraft.commands.remove.console.print") as mock_print:
                project_path = Path("test-project")
                update_main_py_after_removal(project_path, "test-module")
                mock_print.assert_called_with(
                    "⚠️  Warning: main.py not found, skipping cleanup", style="yellow"
                )
