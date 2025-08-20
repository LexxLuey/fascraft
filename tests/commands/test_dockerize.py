"""Tests for the dockerize command."""

from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.dockerize import (
    add_docker,
    add_docker_support,
    render_docker_template,
)
import typer
from fascraft.exceptions import FileSystemError


class TestDockerizeCommand:
    """Test cases for dockerize command functionality."""

    def test_add_docker_success(self, tmp_path):
        """Test successful Docker support addition."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.dockerize.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "docker content"
            mock_env.return_value.get_template.return_value = mock_template

            add_docker_support(project_path, force=False)

            # Verify Docker files were created
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()
            assert (project_path / ".dockerignore").exists()
            assert (project_path / "database" / "init.sql").exists()

    def test_add_docker_existing_files_no_force(self, tmp_path):
        """Test Docker addition fails when files exist and force=False."""
        # Create a mock FastAPI project with existing Docker files
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")
        (project_path / "Dockerfile").write_text("# existing dockerfile")

        with pytest.raises(typer.Exit) as exc_info:
            add_docker(project_path, force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_add_docker_existing_files_with_force(self, tmp_path):
        """Test Docker addition succeeds when files exist and force=True."""
        # Create a mock FastAPI project with existing Docker files
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")
        (project_path / "Dockerfile").write_text("# existing dockerfile")

        with patch("fascraft.commands.dockerize.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "new docker content"
            mock_env.return_value.get_template.return_value = mock_template

            add_docker_support(project_path, force=True)

            # Verify Docker files were updated
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

    def test_render_docker_template(self, tmp_path):
        """Test individual Docker template rendering."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered content"
        mock_env.get_template.return_value = mock_template

        render_docker_template(
            mock_env, project_path, "test-project", "Dockerfile.jinja2", "Dockerfile"
        )

        # Verify template was rendered
        mock_env.get_template.assert_called_once_with("Dockerfile.jinja2")
        mock_template.render.assert_called_once_with(project_name="test-project")

        # Verify file was written
        assert (project_path / "Dockerfile").exists()
        assert (project_path / "Dockerfile").read_text() == "rendered content"

    def test_dockerize_not_fastapi_project(self, tmp_path):
        """Test dockerize fails for non-FastAPI projects."""
        project_path = tmp_path / "not-fastapi"
        project_path.mkdir()
        # No main.py file

        with pytest.raises(typer.Exit) as exc_info:
            add_docker(project_path, force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_dockerize_project_not_exists(self, tmp_path):
        """Test dockerize fails for non-existent projects."""
        project_path = tmp_path / "non-existent"

        with pytest.raises(typer.Exit) as exc_info:
            add_docker(project_path, force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1
