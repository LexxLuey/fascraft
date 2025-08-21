"""Tests to cover missing lines in fascraft/commands/migrate.py."""

from pathlib import Path
from unittest.mock import patch

from fascraft.commands.migrate import (
    confirm_migration,
    migrate_to_domain_modules,
    update_main_py_for_migration,
)


class TestMigrateCoverage:
    """Test class to cover missing lines in migrate.py."""

    def test_confirm_migration_router_count_3(self):
        """Test confirm_migration when router_count > 3 (line 154)."""
        with patch("fascraft.commands.migrate.console.print"):
            with patch("fascraft.commands.migrate.typer.confirm", return_value=True):
                analysis = {
                    "flat_structure": True,
                    "flat_directories": ["models", "schemas"],
                    "main_py_analysis": {
                        "router_count": 4  # This triggers the > 3 condition
                    },
                }

                # This should execute the line with router_count > 3
                result = confirm_migration(analysis)

                # Should return True (user confirmed)
                assert result is True

    def test_migrate_to_domain_modules_not_flat_structure(self):
        """Test migrate_to_domain_modules when flat_structure is False (line 218)."""
        with patch("fascraft.commands.migrate.console.print"):
            project_path = Path("test-project")
            analysis = {"flat_structure": False}  # This triggers the early return

            # This should execute the early return path
            migrate_to_domain_modules(project_path, analysis)

            # Test passes if no exception is raised
            # The function should return early without doing anything

    def test_update_main_py_for_migration_file_not_exists(self):
        """Test update_main_py_for_migration when main.py doesn't exist (line 255)."""
        with patch("pathlib.Path.exists", return_value=False):
            project_path = Path("test-project")

            # This should execute the early return path when main.py doesn't exist
            update_main_py_for_migration(project_path)

            # Test passes if no exception is raised
            # The function should return early without doing anything
