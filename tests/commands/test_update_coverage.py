"""Tests to cover missing lines in fascraft/commands/update.py."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.list import analyze_module
from fascraft.commands.update import is_domain_module, update_module


class TestUpdateCoverage:
    """Test class to cover missing lines in update.py."""

    def test_update_module_path_not_exists(self):
        """Test update_module when path doesn't exist (line 37-42)."""
        with patch("fascraft.commands.update.console.print"):
            with pytest.raises(typer.Exit):
                update_module(
                    "nonexistent-path", "test-module", force=False, backup=False
                )

    def test_update_module_not_fastapi_project(self):
        """Test update_module when path is not a FastAPI project (line 45-52)."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=False
            ):
                with patch("fascraft.commands.update.console.print"):
                    with pytest.raises(typer.Exit):
                        update_module(
                            "test-path", "test-module", force=False, backup=False
                        )

    def test_update_module_module_not_exists(self):
        """Test update_module when module doesn't exist (line 55-62)."""
        with patch("pathlib.Path.exists", side_effect=[True, False]):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=True
            ):
                with patch("fascraft.commands.update.console.print"):
                    with pytest.raises(typer.Exit):
                        update_module(
                            "test-path", "test-module", force=False, backup=False
                        )

    def test_update_module_not_domain_module(self):
        """Test update_module when module is not a domain module (line 65-72)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.update.is_domain_module", return_value=False
                ):
                    with patch("fascraft.commands.update.console.print"):
                        with pytest.raises(typer.Exit):
                            update_module(
                                "test-path", "test-module", force=False, backup=False
                            )

    def test_update_module_cancelled(self):
        """Test update_module when user cancels (line 87-89)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.update.is_domain_module", return_value=True
                ):
                    with patch("fascraft.commands.update.analyze_module"):
                        with patch("fascraft.commands.update.display_update_preview"):
                            with patch(
                                "fascraft.commands.update.confirm_update",
                                return_value=False,
                            ):
                                with patch("fascraft.commands.update.console.print"):
                                    # Should return without updating
                                    update_module(
                                        "test-path",
                                        "test-module",
                                        force=False,
                                        backup=False,
                                    )

    def test_update_module_with_backup(self):
        """Test update_module with backup enabled (line 116-132)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.update.is_domain_module", return_value=True
                ):
                    with patch("fascraft.commands.update.analyze_module"):
                        with patch("fascraft.commands.update.display_update_preview"):
                            with patch(
                                "fascraft.commands.update.confirm_update",
                                return_value=True,
                            ):
                                with patch(
                                    "fascraft.commands.update.create_backup",
                                    return_value=Path("backup"),
                                ):
                                    with patch(
                                        "fascraft.commands.update.update_module_files"
                                    ):
                                        with patch(
                                            "fascraft.commands.update.console.print"
                                        ):
                                            # Should create backup and update
                                            update_module(
                                                "test-path",
                                                "test-module",
                                                force=False,
                                                backup=True,
                                            )

    def test_update_module_error_with_backup_restore(self):
        """Test update_module error handling with backup restore (line 116-132)."""
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            with patch(
                "fascraft.commands.update.is_fastapi_project", return_value=True
            ):
                with patch(
                    "fascraft.commands.update.is_domain_module", return_value=True
                ):
                    with patch("fascraft.commands.update.analyze_module"):
                        with patch("fascraft.commands.update.display_update_preview"):
                            with patch(
                                "fascraft.commands.update.confirm_update",
                                return_value=True,
                            ):
                                with patch(
                                    "fascraft.commands.update.create_backup",
                                    return_value=Path("backup"),
                                ):
                                    with patch(
                                        "fascraft.commands.update.update_module_files",
                                        side_effect=Exception("Update failed"),
                                    ):
                                        with patch(
                                            "fascraft.commands.update.restore_from_backup"
                                        ):
                                            with patch(
                                                "fascraft.commands.update.console.print"
                                            ):
                                                with pytest.raises(typer.Exit):
                                                    # Should attempt restore from backup
                                                    update_module(
                                                        "test-path",
                                                        "test-module",
                                                        force=False,
                                                        backup=True,
                                                    )

    def test_is_domain_module_missing_files(self):
        """Test is_domain_module with missing required files."""
        with patch("pathlib.Path.exists", return_value=False):
            module_path = Path("test-module")
            result = is_domain_module(module_path)
            assert result is False

    def test_analyze_module_with_files(self):
        """Test analyze_module with existing files."""
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
