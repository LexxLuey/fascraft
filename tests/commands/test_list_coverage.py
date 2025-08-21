"""Tests to cover missing lines in fascraft/commands/list.py."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from fascraft.commands.list import analyze_module, display_modules_table


class TestListCoverage:
    """Test class to cover missing lines in list.py."""

    def test_display_modules_table_with_incomplete_modules(self):
        """Test display_modules_table to cover the commented health_style line."""
        # Mock console.print to avoid output during tests
        with patch("fascraft.commands.list.console.print"):
            # Create test data with incomplete modules to trigger the health status logic
            modules = [
                {
                    "name": "users",
                    "files": [
                        "models.py",
                        "schemas.py",
                    ],  # Missing services.py and routers.py
                    "has_tests": True,
                    "health_status": "incomplete",  # This triggers the commented line logic
                },
                {
                    "name": "products",
                    "files": ["models.py", "schemas.py", "services.py", "routers.py"],
                    "has_tests": False,
                    "health_status": "healthy",
                },
            ]

            project_path = Path("test-project")

            # This should execute the line where health_style is commented out
            # and use the alternative health_text logic
            display_modules_table(modules, project_path)

            # Test passes if no exception is raised
            # The commented line is in the loop where health_text is constructed

    def test_analyze_module_with_missing_files(self):
        """Test analyze_module to cover missing file logic."""
        # Create a simple test that will actually work
        # I need to mock BOTH exists AND stat since the function calls both!

        # Mock the Path.exists method to return False for domain files, True for others
        original_exists = Path.exists
        original_stat = Path.stat

        def mock_exists(self):
            path_str = str(self)
            # Return False for required domain files (models.py, schemas.py, services.py, routers.py)
            if any(
                path_str.endswith(f)
                for f in ["models.py", "schemas.py", "services.py", "routers.py"]
            ):
                return False
            # Return True for other files
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
            assert (
                result["health_status"] == "incomplete"
            )  # Should be incomplete due to missing domain files
            assert len(result["files"]) > 0  # Should have some files
            assert result["size"] > 0  # Should have some size
        finally:
            # Restore original methods
            Path.exists = original_exists
            Path.stat = original_stat
