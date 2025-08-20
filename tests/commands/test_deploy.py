"""Tests for the deploy command."""

from unittest.mock import MagicMock, patch

import pytest
import typer

from fascraft.commands.deploy import (
    check_existing_deployment_files,
    generate,
    generate_deployment_files,
    render_deployment_template,
    setup_monitoring_config,
)
from fascraft.exceptions import FileSystemError


class TestDeployCommand:
    """Test cases for deploy command functionality."""

    def test_generate_deployment_files_aws_success(self, tmp_path):
        """Test successful AWS deployment files generation."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.deploy.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "deployment content"
            mock_env.return_value.get_template.return_value = mock_template

            generate_deployment_files(project_path, "aws", force=False)

            # Verify deployment files were created
            assert (project_path / "deploy" / "aws" / "ecs-deploy.sh").exists()
            assert (project_path / "deploy" / "monitoring" / "prometheus.yml").exists()

    def test_generate_deployment_files_kubernetes_success(self, tmp_path):
        """Test successful Kubernetes deployment files generation."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.deploy.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "deployment content"
            mock_env.return_value.get_template.return_value = mock_template

            generate_deployment_files(project_path, "kubernetes", force=False)

            # Verify deployment files were created
            assert (project_path / "deploy" / "kubernetes" / "deployment.yaml").exists()
            assert (project_path / "deploy" / "monitoring" / "prometheus.yml").exists()

    def test_generate_deployment_files_terraform_success(self, tmp_path):
        """Test successful Terraform deployment files generation."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.deploy.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "deployment content"
            mock_env.return_value.get_template.return_value = mock_template

            generate_deployment_files(project_path, "terraform", force=False)

            # Verify deployment files were created
            assert (project_path / "deploy" / "terraform" / "main.tf").exists()
            assert (project_path / "deploy" / "monitoring" / "prometheus.yml").exists()

    def test_generate_deployment_files_all_success(self, tmp_path):
        """Test successful all platforms deployment files generation."""
        # Create a mock FastAPI project
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with patch("fascraft.commands.deploy.Environment") as mock_env:
            mock_template = MagicMock()
            mock_template.render.return_value = "deployment content"
            mock_env.return_value.get_template.return_value = mock_template

            generate_deployment_files(project_path, "all", force=False)

            # Verify deployment files were created for all platforms
            assert (project_path / "deploy" / "aws" / "ecs-deploy.sh").exists()
            assert (project_path / "deploy" / "kubernetes" / "deployment.yaml").exists()
            assert (project_path / "deploy" / "terraform" / "main.tf").exists()
            assert (project_path / "deploy" / "monitoring" / "prometheus.yml").exists()

    def test_check_existing_deployment_files(self, tmp_path):
        """Test checking for existing deployment files."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        # Create some existing deployment files
        (project_path / "deploy" / "aws").mkdir(parents=True)
        (project_path / "deploy" / "aws" / "ecs-deploy.sh").write_text("# existing")
        (project_path / "deploy" / "kubernetes").mkdir(parents=True)
        (project_path / "deploy" / "kubernetes" / "deployment.yaml").write_text(
            "# existing"
        )

        # Check AWS platform
        existing_files = check_existing_deployment_files(project_path, "aws")
        assert "deploy/aws/ecs-deploy.sh" in existing_files

        # Check Kubernetes platform
        existing_files = check_existing_deployment_files(project_path, "kubernetes")
        assert "deploy/kubernetes/deployment.yaml" in existing_files

        # Check all platforms
        existing_files = check_existing_deployment_files(project_path, "all")
        assert "deploy/aws/ecs-deploy.sh" in existing_files
        assert "deploy/kubernetes/deployment.yaml" in existing_files

    def test_render_deployment_template(self, tmp_path):
        """Test individual deployment template rendering."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "rendered content"
        mock_env.get_template.return_value = mock_template

        render_deployment_template(
            mock_env,
            project_path,
            "test-project",
            "deployment.yaml.jinja2",
            "deploy/kubernetes/deployment.yaml",
        )

        # Verify template was rendered
        mock_env.get_template.assert_called_once_with("deployment.yaml.jinja2")
        mock_template.render.assert_called_once_with(project_name="test-project")

        # Verify file was written
        assert (project_path / "deploy" / "kubernetes" / "deployment.yaml").exists()
        assert (
            project_path / "deploy" / "kubernetes" / "deployment.yaml"
        ).read_text() == "rendered content"

    def test_setup_monitoring_config(self, tmp_path):
        """Test monitoring configuration setup."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        setup_monitoring_config(project_path)

        # Verify monitoring files were created
        assert (project_path / "deploy" / "monitoring" / "monitoring.yml").exists()
        assert (project_path / "config" / "logging.yml").exists()

        # Verify content
        monitoring_content = (
            project_path / "deploy" / "monitoring" / "monitoring.yml"
        ).read_text()
        assert "monitoring:" in monitoring_content
        assert "prometheus:" in monitoring_content

    def test_deploy_not_fastapi_project(self, tmp_path):
        """Test deploy fails for non-FastAPI projects."""
        project_path = tmp_path / "not-fastapi"
        project_path.mkdir()
        # No main.py file

        with pytest.raises(typer.Exit) as exc_info:
            generate(project_path, platform="aws", force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_deploy_project_not_exists(self, tmp_path):
        """Test deploy fails for non-existent projects."""
        project_path = tmp_path / "non-existent"

        with pytest.raises(typer.Exit) as exc_info:
            generate(project_path, platform="aws", force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1

    def test_deploy_invalid_platform(self, tmp_path):
        """Test deploy fails for invalid platform."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()
        (project_path / "main.py").write_text("# FastAPI app")

        with pytest.raises(typer.Exit) as exc_info:
            generate(project_path, platform="invalid", force=False)
        
        # Check that it's an exit exception with code 1
        assert exc_info.value.exit_code == 1
