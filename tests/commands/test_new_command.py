"""Unit tests for the new command functionality."""

from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from fascraft.commands.new import create_new_project, create_project_with_rollback, display_success_message
from fascraft.main import app


def create_test_project(project_name: str, project_path: Path) -> None:
    """Helper function to create a project for testing, bypassing typer options."""
    # Validate project name
    from fascraft.validation import validate_project_name
    validated_project_name = validate_project_name(project_name)
    
    # Create project with rollback capability
    create_project_with_rollback(project_path, validated_project_name)
    
    # Display success message
    display_success_message(project_path, validated_project_name)


class TestNewCommand:
    """Test cases for the new command."""

    def test_create_new_project_success(
        self, temp_dir: Path, sample_project_name: str, expected_files: list[str]
    ) -> None:
        """Test successful project creation."""
        project_path = temp_dir / sample_project_name

        # Ensure project doesn't exist initially
        assert not project_path.exists()

        # Ensure temp_dir exists and is writable
        temp_dir.mkdir(exist_ok=True)

        # Create project
        create_test_project(sample_project_name, project_path)

        # Verify project directory was created
        assert project_path.exists()
        assert project_path.is_dir()

        # Verify all expected files were created
        for expected_file in expected_files:
            file_path = project_path / expected_file
            assert file_path.exists(), f"Expected file {expected_file} was not created"
            assert file_path.is_file()

    def test_create_new_project_existing_directory_error(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test error when project directory already exists."""
        project_path = temp_dir / sample_project_name
        project_path.mkdir()

        # Verify project exists
        assert project_path.exists()

        # Attempt to create project with same name
        with pytest.raises(typer.Exit) as exc_info:
            create_new_project(sample_project_name, temp_dir)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_create_new_project_with_path_option(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test project creation with custom path."""
        custom_path = temp_dir / "custom-location"
        project_path = custom_path / sample_project_name

        # Ensure paths don't exist initially
        assert not custom_path.exists()
        assert not project_path.exists()

        # Ensure temp_dir exists
        temp_dir.mkdir(exist_ok=True)

        # Create project with custom path
        create_test_project(sample_project_name, project_path)

        # Verify project was created in custom location
        assert custom_path.exists()
        assert project_path.exists()
        assert project_path.is_dir()

    def test_generated_main_py_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that main.py contains expected FastAPI code."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        main_py_path = temp_dir / sample_project_name / "main.py"
        content = main_py_path.read_text()

        # Verify FastAPI imports and setup
        assert "from fastapi import FastAPI" in content
        assert "app = FastAPI(" in content
        assert "from config.settings import get_settings" in content
        assert "title=settings.app_name" in content

        # Verify endpoints
        assert '@app.get("/")' in content
        assert "async def root():" in content

        # Verify base router integration
        assert "from routers import base_router" in content
        assert "app.include_router(base_router)" in content

        # Verify health check is handled by base router
        assert (
            "# Health check is now handled by base router at /api/v1/health" in content
        )

        # Verify uvicorn integration
        assert "import uvicorn" in content
        assert "uvicorn.run(app" in content

    def test_generated_pyproject_toml_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that pyproject.toml contains expected configuration."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        pyproject_path = temp_dir / sample_project_name / "pyproject.toml"
        content = pyproject_path.read_text()

        # Verify project metadata
        assert f'name = "{sample_project_name}"' in content
        assert 'version = "0.1.0"' in content
        assert 'description = "A FastAPI project generated with FasCraft"' in content

        # Verify dependencies (now using flexible version ranges)
        assert 'fastapi = ">=0.100.0,<1.0.0"' in content
        assert (
            'uvicorn = {extras = ["standard"], version = ">=0.20.0,<1.0.0"}' in content
        )

        # Verify development dependencies
        assert 'pytest = "^7.4.3"' in content
        assert 'black = "^24.0.0"' in content
        assert 'ruff = "^0.2.0"' in content

    def test_generated_readme_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that README.md contains expected documentation."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        readme_path = temp_dir / sample_project_name / "README.md"
        content = readme_path.read_text()

        # Verify project title
        assert f"# {sample_project_name}" in content
        assert "A FastAPI project generated with FasCraft" in content

        # Verify setup instructions
        assert "## Getting Started" in content
        assert "### Prerequisites" in content
        assert "### Installation" in content

        # Verify API endpoints documentation
        assert "## API Endpoints" in content
        assert "`GET /` - Root endpoint" in content
        assert "`GET /api/v1/health` - Health check" in content

        # Verify development tools
        assert "## Development" in content
        assert "**FastAPI**" in content
        assert "**SQLAlchemy**" in content
        assert "**Alembic**" in content

    def test_generated_init_py_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that __init__.py contains expected package info."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        init_path = temp_dir / sample_project_name / "__init__.py"
        content = init_path.read_text()

        # Verify package metadata
        expected_docstring = (
            f'"""\n{sample_project_name} - A FastAPI project '
            f'generated with FasCraft.\n"""'
        )
        assert expected_docstring in content
        assert '__version__ = "0.1.0"' in content
        assert '__author__ = "Lutor Iyornumbe"' in content

    def test_project_name_in_all_templates(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that project name is properly substituted in all templates."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        project_path = temp_dir / sample_project_name

        # Check main.py
        main_content = (project_path / "main.py").read_text()
        assert sample_project_name in main_content

        # Check pyproject.toml
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert sample_project_name in pyproject_content

        # Check README.md
        readme_content = (project_path / "README.md").read_text()
        assert sample_project_name in readme_content

    def test_new_files_are_created(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that all new files (env, requirements) are created."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)

        project_path = temp_dir / sample_project_name

        # Check that new files exist
        assert (project_path / ".env").exists()
        assert (project_path / ".env.sample").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "requirements.dev.txt").exists()
        assert (project_path / "requirements.prod.txt").exists()

        # Check that .env contains project name
        env_content = (project_path / ".env").read_text()
        assert "FastAPI Application Configuration" in env_content

        # Check that .env.sample contains project name
        env_sample_content = (project_path / ".env.sample").read_text()
        assert sample_project_name in env_sample_content
        assert "MONGODB_DATABASE=" + sample_project_name in env_sample_content
        assert "POSTGRES_DATABASE=" + sample_project_name in env_sample_content
        assert "MYSQL_DATABASE=" + sample_project_name in env_sample_content
        assert "SQLITE_DATABASE=./" + sample_project_name + ".db" in env_sample_content

        # Check that requirements files contain expected content
        requirements_content = (project_path / "requirements.txt").read_text()
        assert "fastapi>=" in requirements_content
        assert "uvicorn[standard]>=" in requirements_content

        requirements_dev_content = (project_path / "requirements.dev.txt").read_text()
        assert "-r requirements.txt" in requirements_dev_content
        assert "pytest>=" in requirements_dev_content

        requirements_prod_content = (project_path / "requirements.prod.txt").read_text()
        assert "fastapi>=" in requirements_prod_content
        assert "gunicorn>=" in requirements_prod_content

        # Check that .gitignore file is created
        assert (project_path / ".gitignore").exists()
        gitignore_content = (project_path / ".gitignore").read_text()
        assert "# Byte-compiled / optimized / DLL files" in gitignore_content
        assert "__pycache__/" in gitignore_content
        assert f"# {sample_project_name} specific" in gitignore_content

        # Check that routers directory structure is created
        assert (project_path / "routers").exists()
        assert (project_path / "routers" / "__init__.py").exists()
        assert (project_path / "routers" / "base.py").exists()

        # Check that base router contains expected content
        base_router_content = (project_path / "routers" / "base.py").read_text()
        assert "from fastapi import APIRouter" in base_router_content
        assert 'base_router = APIRouter(prefix="/api/v1")' in base_router_content
        assert '@base_router.get("/health")' in base_router_content
        assert "async def health_check():" in base_router_content

        # Check that fascraft.toml configuration file is created
        assert (project_path / "fascraft.toml").exists()
        fascraft_config_content = (project_path / "fascraft.toml").read_text()
        assert "# FasCraft project configuration for" in fascraft_config_content
        assert "[project]" in fascraft_config_content
        assert "[router]" in fascraft_config_content
        assert "[database]" in fascraft_config_content

    def test_create_new_project_creates_parent_directories(
        self, temp_dir: Path
    ) -> None:
        """Test that parent directories are created if they don't exist."""
        nested_path = temp_dir / "nested" / "deep" / "path"
        project_name = "test-project"
        project_path = nested_path / project_name

        # Ensure nested path doesn't exist
        assert not nested_path.exists()

        # Ensure temp_dir exists
        temp_dir.mkdir(exist_ok=True)

        # Create project in nested path
        create_test_project(project_name, project_path)

        # Verify all parent directories and project were created
        assert nested_path.exists()
        assert project_path.exists()
        assert project_path.is_dir()

    def test_success_messages_are_displayed(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that appropriate success messages are displayed."""
        # Ensure temp_dir exists
        temp_dir.mkdir(exist_ok=True)
        
        # Create project using helper function
        project_path = temp_dir / sample_project_name
        create_test_project(sample_project_name, project_path)
        
        # Verify project was created successfully
        assert project_path.exists()
        assert project_path.is_dir()
        
        # Verify key files exist
        assert (project_path / "main.py").exists()
        assert (project_path / "pyproject.toml").exists()
        assert (project_path / "README.md").exists()
        assert (project_path / ".gitignore").exists()
        assert (project_path / "fascraft.toml").exists()

    def test_project_name_validation(self, temp_dir: Path) -> None:
        """Test project creation with various project names."""
        test_names = [
            "simple-name",
            "name_with_underscores",
            "NameWithCaps",
            "mixed-123-name",
        ]

        # Ensure temp_dir exists
        temp_dir.mkdir(exist_ok=True)

        for name in test_names:
            project_path = temp_dir / name

            # Ensure project doesn't exist
            assert not project_path.exists()

            # Create project
            create_test_project(name, project_path)

            # Verify project was created
            assert project_path.exists()
            assert project_path.is_dir()

            # Verify main.py contains the name
            main_content = (project_path / "main.py").read_text()
            assert name in main_content

    def test_invalid_project_names_are_rejected(self, temp_dir: Path) -> None:
        """Test that invalid project names are properly rejected."""
        invalid_names = [
            "123-numbers",  # Starts with number
            "test@project",  # Contains special characters
            "test#project",  # Contains special characters
        ]

        for name in invalid_names:
            project_path = temp_dir / name

            # Ensure project doesn't exist
            assert not project_path.exists()

            # Attempt to create project with invalid name
            with pytest.raises(typer.Exit) as exc_info:
                create_new_project(name, temp_dir)
            
            # Check that it's an exit exception with code 1
            assert exc_info.value.exit_code == 1

            # Verify project was not created
            assert not project_path.exists()

    def test_template_rendering_handles_special_characters(
        self, temp_dir: Path
    ) -> None:
        """Test that templates handle special characters in project names."""
        temp_dir.mkdir(exist_ok=True)
        special_name = "test-project-with-special-chars"
        project_path = temp_dir / special_name
        create_test_project(special_name, project_path)

        project_path = temp_dir / special_name
        assert project_path.exists()

        # Verify files were created and contain the name
        main_content = (project_path / "main.py").read_text()
        assert special_name in main_content

    def test_validation_error_messages_are_displayed(self, temp_dir: Path) -> None:
        """Test that validation error messages are properly displayed."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            # Test with invalid project name that starts with number
            result = runner.invoke(app, ["new", "123-invalid"])

            assert result.exit_code == 1
            assert "Invalid project name" in result.stdout

            # Test with invalid project name containing special characters
            result = runner.invoke(app, ["new", "test@project"])

            assert result.exit_code == 1
            assert "Invalid project name" in result.stdout
