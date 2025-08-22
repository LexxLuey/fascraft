"""Simple tests for achieving coverage of the new.py command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from fascraft.commands.list import analyze_module


class TestNewCommandCoverage:
    """Test coverage for new command functions."""

    def test_new_command_error_guidance_coverage(self):
        """Test error guidance functions to cover lines 514, 516, 520, 522."""
        from fascraft.commands.new import (
            display_disk_space_error_guidance,
            display_permission_error_guidance,
            display_template_error_guidance,
        )

        with patch("fascraft.commands.new.console.print") as mock_print:
            display_permission_error_guidance()
            assert mock_print.call_count > 0

        with patch("fascraft.commands.new.console.print") as mock_print:
            display_disk_space_error_guidance()
            assert mock_print.call_count > 0

        with patch("fascraft.commands.new.console.print") as mock_print:
            display_template_error_guidance()
            assert mock_print.call_count > 0

    def test_analyze_module_with_files(self):
        """Test analyze_module function to cover missing lines."""
        # Mock Path.exists and Path.stat to avoid FileNotFoundError
        original_exists = Path.exists
        original_stat = Path.stat

        def mock_exists(self):
            path_str = str(self)
            if any(
                path_str.endswith(f)
                for f in ["models.py", "schemas.py", "services.py", "routers.py"]
            ):
                return False
            return True

        def mock_stat(self):
            mock_stat_obj = MagicMock()
            mock_stat_obj.st_size = 100
            return mock_stat_obj

        Path.exists = mock_exists
        Path.stat = mock_stat

        try:
            module_path = Path("test-module")
            result = analyze_module(module_path)

            assert result["health_status"] == "incomplete"
            assert result["size"] > 0
            assert len(result["files"]) > 0
        finally:
            Path.exists = original_exists
            Path.stat = original_stat
