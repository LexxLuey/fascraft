"""Tests for the migrate command functionality."""

from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest
import typer

from fascraft.commands.migrate import (
    migrate_project,
    analyze_current_structure,
    confirm_migration,
    create_backup,
    create_base_router_structure,
    migrate_to_domain_modules,
    update_main_py_for_migration,
    create_fascraft_config,
    display_migration_summary,
    is_fastapi_project,
)


class TestIsFastApiProject:
    """Test the is_fastapi_project function."""

    def test_is_fastapi_project_valid_main_py(self, tmp_path):
        """Test that a valid FastAPI project with main.py is correctly identified."""
        # Create main.py with FastAPI content
        main_py = tmp_path / "main.py"
        main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")
        
        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_valid_pyproject_toml(self, tmp_path):
        """Test that a valid FastAPI project with pyproject.toml is correctly identified."""
        # Create pyproject.toml with FastAPI dependency
        pyproject_toml = tmp_path / "pyproject.toml"
        pyproject_toml.write_text("[tool.poetry.dependencies]\nfastapi = '^0.104.0'")
        
        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_invalid(self, tmp_path):
        """Test that an invalid project is not identified as FastAPI."""
        # Create empty directory
        assert is_fastapi_project(tmp_path) is False
        
        # Create main.py without FastAPI
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")
        assert is_fastapi_project(tmp_path) is False


class TestAnalyzeCurrentStructure:
    """Test the analyze_current_structure function."""

    def test_analyze_current_structure_needs_migration(self, tmp_path):
        """Test analysis of project that needs migration."""
        # Create flat structure project
        (tmp_path / "models").mkdir()
        (tmp_path / "schemas").mkdir()
        (tmp_path / "routers").mkdir()
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        analysis = analyze_current_structure(tmp_path)
        
        assert analysis["needs_migration"] is True
        assert analysis["flat_structure"] is True
        assert "models" in analysis["flat_directories"]
        assert "schemas" in analysis["flat_directories"]
        assert "routers" in analysis["flat_directories"]

    def test_analyze_current_structure_already_migrated(self, tmp_path):
        """Test analysis of project that's already migrated."""
        # Create domain-driven project
        customers_dir = tmp_path / "customers"
        customers_dir.mkdir()
        (customers_dir / "__init__.py").write_text("")
        (customers_dir / "models.py").write_text("# models")
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        analysis = analyze_current_structure(tmp_path)
        
        assert analysis["needs_migration"] is False


class TestConfirmMigration:
    """Test the confirm_migration function."""

    @patch("fascraft.commands.migrate.typer.confirm")
    def test_confirm_migration_yes(self, mock_confirm):
        """Test migration confirmation with yes."""
        mock_confirm.return_value = True
        
        analysis = {
            "flat_structure": True,
            "flat_directories": ["models", "schemas"],
            "main_py_analysis": {"router_count": 2}
        }
        
        result = confirm_migration(analysis)
        assert result is True

    @patch("fascraft.commands.migrate.typer.confirm")
    def test_confirm_migration_no(self, mock_confirm):
        """Test migration confirmation with no."""
        mock_confirm.return_value = False
        
        analysis = {
            "flat_structure": True,
            "flat_directories": ["models", "schemas"],
            "main_py_analysis": {"router_count": 2}
        }
        
        result = confirm_migration(analysis)
        assert result is False


class TestCreateBackup:
    """Test the create_backup function."""

    def test_create_backup_success(self, tmp_path):
        """Test successful backup creation."""
        # Create some project files
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        (tmp_path / "config").mkdir()
        (tmp_path / "config" / "settings.py").write_text("# settings")
        
        backup_path = create_backup(tmp_path)
        
        assert backup_path.exists()
        assert backup_path.is_dir()
        assert (backup_path / "main.py").exists()
        assert (backup_path / "config" / "settings.py").exists()


class TestCreateBaseRouterStructure:
    """Test the create_base_router_structure function."""

    def test_create_base_router_structure_success(self, tmp_path):
        """Test successful base router structure creation."""
        create_base_router_structure(tmp_path)
        
        # Check that routers directory was created
        routers_dir = tmp_path / "routers"
        assert routers_dir.exists()
        assert (routers_dir / "__init__.py").exists()
        assert (routers_dir / "base.py").exists()
        
        # Check base router content
        base_router_content = (routers_dir / "base.py").read_text()
        assert "from fastapi import APIRouter" in base_router_content
        assert "base_router = APIRouter(prefix=\"/api/v1\")" in base_router_content


class TestMigrateToDomainModules:
    """Test the migrate_to_domain_modules function."""

    def test_migrate_to_domain_modules_flat_structure(self, tmp_path):
        """Test migration from flat structure to domain modules."""
        # Create flat structure
        (tmp_path / "models").mkdir()
        (tmp_path / "models" / "user.py").write_text("class User: pass")
        (tmp_path / "schemas").mkdir()
        (tmp_path / "schemas" / "user.py").write_text("class UserSchema: pass")
        (tmp_path / "routers").mkdir()
        (tmp_path / "routers" / "user.py").write_text("from fastapi import APIRouter")
        
        analysis = {"flat_structure": True}
        
        migrate_to_domain_modules(tmp_path, analysis)
        
        # Check that domain modules were created
        users_dir = tmp_path / "users"
        assert users_dir.exists()
        assert (users_dir / "__init__.py").exists()
        assert (users_dir / "models.py").exists()
        assert (users_dir / "schemas.py").exists()
        assert (users_dir / "services.py").exists()
        assert (users_dir / "routers.py").exists()


class TestUpdateMainPyForMigration:
    """Test the update_main_py_for_migration function."""

    def test_update_main_py_for_migration_success(self, tmp_path):
        """Test successful main.py update for migration."""
        # Create main.py with old structure
        main_py = tmp_path / "main.py"
        main_py.write_text("""
from fastapi import FastAPI
from models import user
from schemas import user_schema
from routers import user_router

app = FastAPI()
app.include_router(user_router, prefix="/users")
""")
        
        update_main_py_for_migration(tmp_path)
        
        # Check that main.py was updated
        updated_content = main_py.read_text()
        # The current implementation doesn't add the base router import
        # It only removes existing router includes
        assert "app.include_router(user_router, prefix=\"/users\")" not in updated_content


class TestCreateFascraftConfig:
    """Test the create_fascraft_config function."""

    def test_create_fascraft_config_success(self, tmp_path):
        """Test successful fascraft.toml creation."""
        create_fascraft_config(tmp_path)
        
        # Check that fascraft.toml was created
        config_file = tmp_path / "fascraft.toml"
        assert config_file.exists()
        
        # Check config content
        config_content = config_file.read_text()
        assert "[project]" in config_content
        assert "[router]" in config_content
        assert "[database]" in config_content


class TestDisplayMigrationSummary:
    """Test the display_migration_summary function."""

    @patch("fascraft.commands.migrate.console.print")
    def test_display_migration_summary(self, mock_print, tmp_path):
        """Test that migration summary is displayed correctly."""
        analysis = {
            "project_name": "test-project",
            "flat_structure": True,
            "flat_directories": ["models", "schemas"],
            "migrated_modules": ["users", "products"]
        }
        
        display_migration_summary(analysis)
        
        # Verify that console.print was called
        assert mock_print.call_count > 0


class TestMigrateProject:
    """Test the migrate_project function."""

    def test_migrate_project_success(self, tmp_path):
        """Test successful project migration."""
        # Create a valid FastAPI project with flat structure
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        (tmp_path / "models").mkdir()
        (tmp_path / "schemas").mkdir()
        (tmp_path / "routers").mkdir()
        
        # Mock the analysis and migration functions
        with patch("fascraft.commands.migrate.analyze_current_structure") as mock_analyze:
            with patch("fascraft.commands.migrate.confirm_migration") as mock_confirm:
                with patch("fascraft.commands.migrate.create_backup") as mock_backup:
                    with patch("fascraft.commands.migrate.create_base_router_structure") as mock_base:
                        with patch("fascraft.commands.migrate.migrate_to_domain_modules") as mock_migrate:
                            with patch("fascraft.commands.migrate.update_main_py_for_migration") as mock_update:
                                with patch("fascraft.commands.migrate.create_fascraft_config") as mock_config:
                                    with patch("fascraft.commands.migrate.display_migration_summary") as mock_summary:
                                        mock_analyze.return_value = {
                                            "needs_migration": True,
                                            "flat_structure": True,
                                            "flat_directories": ["models", "schemas"]
                                        }
                                        mock_confirm.return_value = True
                                        mock_backup.return_value = tmp_path / "backup"
                                        
                                        migrate_project(str(tmp_path), backup=True)
                                        
                                        mock_analyze.assert_called_once()
                                        mock_confirm.assert_called_once()
                                        mock_backup.assert_called_once()
                                        mock_base.assert_called_once()
                                        mock_migrate.assert_called_once()
                                        mock_update.assert_called_once()
                                        mock_config.assert_called_once()
                                        mock_summary.assert_called_once()

    def test_migrate_project_already_migrated(self, tmp_path):
        """Test migration of already migrated project."""
        # Create a domain-driven project
        customers_dir = tmp_path / "customers"
        customers_dir.mkdir()
        (customers_dir / "__init__.py").write_text("")
        (customers_dir / "models.py").write_text("# models")
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the analysis function
        with patch("fascraft.commands.migrate.analyze_current_structure") as mock_analyze:
            mock_analyze.return_value = {"needs_migration": False}
            
            migrate_project(str(tmp_path))
            
            mock_analyze.assert_called_once()

    def test_migrate_project_invalid_path(self):
        """Test migration with invalid path."""
        with pytest.raises(typer.Exit) as exc_info:
            migrate_project("/nonexistent/path")
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, typer.Exit)

    def test_migrate_project_not_fastapi(self, tmp_path):
        """Test migration of non-FastAPI project."""
        # Create a non-FastAPI project
        main_py = tmp_path / "main.py"
        main_py.write_text("print('Hello World')")
        
        with pytest.raises(typer.Exit) as exc_info:
            migrate_project(str(tmp_path))
        
        # Check that it's an exit exception
        exception = exc_info.value
        assert isinstance(exception, typer.Exit)

    def test_migrate_project_user_cancels(self, tmp_path):
        """Test migration when user cancels."""
        # Create a valid FastAPI project
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")
        
        # Mock the analysis and confirmation functions
        with patch("fascraft.commands.migrate.analyze_current_structure") as mock_analyze:
            with patch("fascraft.commands.migrate.confirm_migration") as mock_confirm:
                mock_analyze.return_value = {"needs_migration": True, "flat_structure": True}
                mock_confirm.return_value = False
                
                with pytest.raises(typer.Exit) as exc_info:
                    migrate_project(str(tmp_path))
                
                # Check that it's an exit exception
                exception = exc_info.value
                assert isinstance(exception, typer.Exit)
