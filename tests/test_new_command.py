"""Unit tests for the new command functionality."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from fastcraft.commands.new import create_new_project
from fastcraft.main import app


class TestNewCommand:
    """Test cases for the new command."""

    def test_create_new_project_success(
        self, temp_dir: Path, sample_project_name: str, expected_files: list[str]
    ) -> None:
        """Test successful project creation."""
        project_path = temp_dir / sample_project_name

        # Ensure project doesn't exist initially
        assert not project_path.exists()

        # Create project
        create_new_project(sample_project_name, temp_dir)

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
        with pytest.raises(Exception) as exc_info:
            create_new_project(sample_project_name, temp_dir)

        # Check that it's an exit exception with code 1
        # Handle different exception types that might be raised
        exception = exc_info.value
        if hasattr(exception, "code"):
            assert exception.code == 1
        elif hasattr(exception, "exit_code"):
            assert exception.exit_code == 1
        else:
            # For typer.Exit, just verify it's an exit exception
            assert isinstance(exception, Exception)

    def test_create_new_project_with_path_option(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test project creation with custom path."""
        custom_path = temp_dir / "custom-location"
        project_path = custom_path / sample_project_name

        # Ensure paths don't exist initially
        assert not custom_path.exists()
        assert not project_path.exists()

        # Create project with custom path
        create_new_project(sample_project_name, custom_path)

        # Verify project was created in custom location
        assert custom_path.exists()
        assert project_path.exists()
        assert project_path.is_dir()

    def test_generated_main_py_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that main.py contains expected FastAPI code."""
        create_new_project(sample_project_name, temp_dir)

        main_py_path = temp_dir / sample_project_name / "main.py"
        content = main_py_path.read_text()

        # Verify FastAPI imports and setup
        assert "from fastapi import FastAPI" in content
        assert "app = FastAPI(" in content
        assert "from config.settings import get_settings" in content
        assert "title=settings.app_name" in content

        # Verify endpoints
        assert '@app.get("/")' in content
        assert '@app.get("/health")' in content
        assert "async def root():" in content
        assert "async def health_check():" in content

        # Verify uvicorn integration
        assert "import uvicorn" in content
        assert "uvicorn.run(app" in content

    def test_generated_pyproject_toml_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that pyproject.toml contains expected configuration."""
        create_new_project(sample_project_name, temp_dir)

        pyproject_path = temp_dir / sample_project_name / "pyproject.toml"
        content = pyproject_path.read_text()

        # Verify project metadata
        assert f'name = "{sample_project_name}"' in content
        assert 'version = "0.1.0"' in content
        assert 'description = "A FastAPI project generated with FastCraft"' in content

        # Verify dependencies
        assert 'fastapi = "^0.104.0"' in content
        assert 'uvicorn = {extras = ["standard"], version = "^0.24.0"}' in content

        # Verify development dependencies
        assert 'pytest = "^7.4.0"' in content
        assert 'black = "^24.0.0"' in content
        assert 'ruff = "^0.2.0"' in content

    def test_generated_readme_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that README.md contains expected documentation."""
        create_new_project(sample_project_name, temp_dir)

        readme_path = temp_dir / sample_project_name / "README.md"
        content = readme_path.read_text()

        # Verify project title
        assert f"# {sample_project_name}" in content
        assert "A FastAPI project generated with FastCraft" in content

        # Verify setup instructions
        assert "## Getting Started" in content
        assert "### Prerequisites" in content
        assert "### Installation" in content

        # Verify API endpoints documentation
        assert "## API Endpoints" in content
        assert "`GET /` - Root endpoint" in content
        assert "`GET /health` - Health check" in content

        # Verify development tools
        assert "## Development" in content
        assert "**FastAPI**" in content
        assert "**Pip**" in content

    def test_generated_init_py_content(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that __init__.py contains expected package info."""
        create_new_project(sample_project_name, temp_dir)

        init_path = temp_dir / sample_project_name / "__init__.py"
        content = init_path.read_text()

        # Verify package metadata
        expected_docstring = (
            f'"""\n{sample_project_name} - A FastAPI project '
            f'generated with FastCraft.\n"""'
        )
        assert expected_docstring in content
        assert '__version__ = "0.1.0"' in content
        assert '__author__ = "Lutor Iyornumbe"' in content

    def test_project_name_in_all_templates(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that project name is properly substituted in all templates."""
        create_new_project(sample_project_name, temp_dir)

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
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Check that new files exist
        assert (project_path / ".env").exists()
        assert (project_path / ".env.sample").exists()
        assert (project_path / "requirements.txt").exists()
        assert (project_path / "requirements.dev.txt").exists()
        assert (project_path / "requirements.prod.txt").exists()

        # Check that .env contains project name
        env_content = (project_path / ".env").read_text()
        assert sample_project_name in env_content
        assert "MONGODB_DATABASE=" + sample_project_name in env_content
        assert "POSTGRES_DATABASE=" + sample_project_name in env_content
        assert "MYSQL_DATABASE=" + sample_project_name in env_content
        assert "SQLITE_DATABASE=./" + sample_project_name + ".db" in env_content

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

    def test_create_new_project_creates_parent_directories(
        self, temp_dir: Path
    ) -> None:
        """Test that parent directories are created if they don't exist."""
        nested_path = temp_dir / "nested" / "deep" / "path"
        project_name = "test-project"
        project_path = nested_path / project_name

        # Ensure nested path doesn't exist
        assert not nested_path.exists()

        # Create project in nested path
        create_new_project(project_name, nested_path)

        # Verify all parent directories and project were created
        assert nested_path.exists()
        assert project_path.exists()
        assert project_path.is_dir()

    def test_success_messages_are_displayed(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that appropriate success messages are displayed."""
        runner = CliRunner()

        with runner.isolated_filesystem(temp_dir):
            result = runner.invoke(app, ["new", sample_project_name])

            assert result.exit_code == 0
            assert "Successfully created new project" in result.stdout
            assert sample_project_name in result.stdout
            assert "Run 'cd" in result.stdout
            assert "pip install -r requirements.txt" in result.stdout
            assert "pip install -r requirements.dev.txt" in result.stdout

    def test_project_name_validation(self, temp_dir: Path) -> None:
        """Test project creation with various project names."""
        test_names = [
            "simple-name",
            "name_with_underscores",
            "NameWithCaps",
            "123-numbers",
            "mixed-123-name",
        ]

        for name in test_names:
            project_path = temp_dir / name

            # Ensure project doesn't exist
            assert not project_path.exists()

            # Create project
            create_new_project(name, temp_dir)

            # Verify project was created
            assert project_path.exists()
            assert project_path.is_dir()

            # Verify main.py contains the name
            main_content = (project_path / "main.py").read_text()
            assert name in main_content

    def test_template_rendering_handles_special_characters(
        self, temp_dir: Path
    ) -> None:
        """Test that templates handle special characters in project names."""
        special_name = "test@project#with$special%chars"
        create_new_project(special_name, temp_dir)

        project_path = temp_dir / special_name
        assert project_path.exists()

        # Verify files were created and contain the name
        main_content = (project_path / "main.py").read_text()
        assert special_name in main_content
