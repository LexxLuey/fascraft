"""Tests for the CI/CD command."""

from unittest.mock import MagicMock, patch

import pytest

from fascraft.commands.ci_cd import (
    add_ci_cd,
    add_ci_cd_support,
    check_existing_ci_cd_files,
    render_ci_cd_template,
    setup_ci_cd_environments,
)
from fascraft.exceptions import FileSystemError


class TestCICDCommand:
    """Test cases for CI/CD command functionality."""

    def test_add_ci_cd_github_success(self, tmp_path):
        """Test successful GitHub CI/CD support addition."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.ci_cd.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "ci-cd content"
            mock_env.return_value.get_template.return_value = mock_template

            add_ci_cd_support(project_path, "github", force=False)

            # Verify CI/CD files were created
            assert (project_path / ".github" / "workflows" / "ci.yml").exists()
            assert (
                project_path / ".github" / "workflows" / "dependency-update.yml"
            ).exists()
            assert (project_path / ".pre-commit-config.yaml").exists()

    def test_add_ci_cd_gitlab_success(self, tmp_path):
        """Test successful GitLab CI/CD support addition."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.ci_cd.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "ci-cd content"
            mock_env.return_value.get_template.return_value = mock_template

            add_ci_cd_support(project_path, "gitlab", force=False)

            # Verify CI/CD files were created
            assert (project_path / ".gitlab-ci.yml").exists()
            assert (project_path / ".pre-commit-config.yaml").exists()

    def test_add_ci_cd_both_success(self, tmp_path):
        """Test successful both platforms CI/CD support addition."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.ci_cd.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "ci-cd content"
            mock_env.return_value.get_template.return_value = mock_template

            add_ci_cd_support(project_path, "both", force=False)

            # Verify CI/CD files were created for both platforms
            assert (project_path / ".github" / "workflows" / "ci.yml").exists()
            assert (
                project_path / ".github" / "workflows" / "dependency-update.yml"
            ).exists()
            assert (project_path / ".gitlab-ci.yml").exists()
            assert (project_path / ".pre-commit-config.yaml").exists()

    def test_check_existing_ci_cd_files(self, tmp_path):
        """Test checking for existing CI/CD files."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create some existing CI/CD files
        (project_path / ".github" / "workflows").mkdir(parents=True)
        (project_path / ".github" / "workflows" / "ci.yml").write_text("# existing")
        (project_path / ".gitlab-ci.yml").write_text("# existing")

        # Check GitHub platform
        existing_files = check_existing_ci_cd_files(project_path, "github")
        assert ".github/workflows/ci.yml" in existing_files

        # Check GitLab platform
        existing_files = check_existing_ci_cd_files(project_path, "gitlab")
        assert ".gitlab-ci.yml" in existing_files

        # Check both platforms
        existing_files = check_existing_ci_cd_files(project_path, "both")
        assert ".github/workflows/ci.yml" in existing_files
        assert ".gitlab-ci.yml" in existing_files

    def test_render_ci_cd_template(self, tmp_path):
        """Test individual CI/CD template rendering."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered content"
        mock_env.get_template.return_value = mock_template

        render_ci_cd_template(
            mock_env,
            project_path,
            "test-project",
            "ci.yml.jinja2",
            ".github/workflows/ci.yml",
        )

        # Verify template was rendered
        mock_env.get_template.assert_called_once_with("ci.yml.jinja2")
        mock_template.render.assert_called_once_with(project_name="test-project")

        # Verify file was written
        assert (project_path / ".github" / "workflows" / "ci.yml").exists()
        assert (
            project_path / ".github" / "workflows" / "ci.yml"
        ).read_text() == "rendered content"

    def test_setup_ci_cd_environments(self, tmp_path):
        """Test CI/CD environment setup."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        setup_ci_cd_environments(project_path)

        # Verify environment files were created
        assert (project_path / ".env.dev").exists()
        assert (project_path / ".env.staging").exists()
        assert (project_path / ".env.prod").exists()

        # Verify content
        dev_content = (project_path / ".env.dev").read_text()
        assert "ENVIRONMENT=development" in dev_content
        assert "DEBUG=true" in dev_content

    def test_ci_cd_not_fastapi_project(self, tmp_path):
        """Test CI/CD fails for non-FastAPI projects."""
        project_path = tmp_path / "not-fastapi"
        project_path.mkdir()
        # No main.py file

        with pytest.raises(FileSystemError, match="Not a FastAPI project"):
            add_ci_cd(project_path, platform="github", force=False)

    def test_ci_cd_project_not_exists(self, tmp_path):
        """Test CI/CD fails for non-existent projects."""
        project_path = tmp_path / "non-existent"

        with pytest.raises(FileSystemError, match="Project path does not exist"):
            add_ci_cd(project_path, platform="github", force=False)

    def test_ci_cd_invalid_platform(self, tmp_path):
        """Test CI/CD fails for invalid platform."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with pytest.raises(FileSystemError, match="Invalid platform"):
            add_ci_cd(project_path, platform="invalid", force=False)
