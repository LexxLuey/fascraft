"""Tests for the documentation generation command."""

import json
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from fascraft.commands.docs import (
    docs_app,
    generate_api_documentation,
    generate_changelog_template,
    generate_documentation,
    generate_openapi_spec,
    generate_readme_template,
    get_module_info,
    get_project_info,
    is_fastapi_project,
)


class TestFastAPIProjectDetection:
    """Test FastAPI project detection functionality."""

    def test_is_fastapi_project_with_main_py(self, tmp_path):
        """Test detection when main.py contains FastAPI."""
        main_file = tmp_path / "main.py"
        main_file.write_text("from fastapi import FastAPI\napp = FastAPI()")

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_with_pyproject_toml(self, tmp_path):
        """Test detection when pyproject.toml contains FastAPI dependency."""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text(
            "[tool.poetry.dependencies]\npython = '^3.8'\nfastapi = '^0.68.0'"
        )

        assert is_fastapi_project(tmp_path) is True

    def test_is_fastapi_project_without_indicators(self, tmp_path):
        """Test detection when no FastAPI indicators are present."""
        assert is_fastapi_project(tmp_path) is False

    def test_is_fastapi_project_case_insensitive(self, tmp_path):
        """Test detection is case insensitive."""
        main_file = tmp_path / "main.py"
        main_file.write_text("from FastAPI import FastAPI\napp = FastAPI()")

        assert is_fastapi_project(tmp_path) is True


class TestProjectInfoExtraction:
    """Test project information extraction functionality."""

    def test_get_project_info_basic(self, tmp_path):
        """Test basic project info extraction."""
        project_info = get_project_info(tmp_path)

        assert project_info["name"] == tmp_path.name
        assert project_info["path"] == str(tmp_path)
        assert project_info["version"] == "0.1.0"
        assert project_info["description"] == ""

    def test_get_project_info_with_readme(self, tmp_path):
        """Test project info extraction with README."""
        readme_file = tmp_path / "README.md"
        readme_file.write_text("# Test Project\n\nThis is a test project description.")

        project_info = get_project_info(tmp_path)

        assert project_info["description"] == "This is a test project description."

    def test_get_project_info_with_pyproject_toml(self, tmp_path):
        """Test project info extraction with pyproject.toml."""
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text("[tool.poetry]\nversion = '1.2.3'")

        project_info = get_project_info(tmp_path)

        assert project_info["version"] == "1.2.3"

    @patch("fascraft.commands.docs.dependency_graph")
    def test_get_project_info_with_modules(self, mock_dependency_graph, tmp_path):
        """Test project info extraction with modules."""
        mock_dependency_graph.modules = {"users": {}, "products": {}}

        project_info = get_project_info(tmp_path)

        assert "users" in project_info["modules"]
        assert "products" in project_info["modules"]


class TestModuleInfoExtraction:
    """Test module information extraction functionality."""

    def test_get_module_info_basic(self, tmp_path):
        """Test basic module info extraction."""
        module_path = tmp_path / "test_module"
        module_path.mkdir()

        # Create some Python files
        (module_path / "__init__.py").write_text("")
        (module_path / "models.py").write_text("")
        (module_path / "services.py").write_text("")

        module_info = get_module_info(tmp_path, "test_module")

        assert module_info["name"] == "test_module"
        assert module_info["path"] == str(module_path)
        assert "models.py" in module_info["files"]
        assert "services.py" in module_info["files"]

    def test_get_module_info_not_found(self, tmp_path):
        """Test module info extraction when module doesn't exist."""
        with pytest.raises(FileNotFoundError):  # ModuleNotFoundError
            get_module_info(tmp_path, "nonexistent_module")

    @patch("fascraft.commands.docs.dependency_graph")
    def test_get_module_info_with_dependencies(self, mock_dependency_graph, tmp_path):
        """Test module info extraction with dependencies."""
        module_path = tmp_path / "test_module"
        module_path.mkdir()

        mock_dependency_graph.modules = {
            "test_module": {"dependencies": ["users", "products"]}
        }

        module_info = get_module_info(tmp_path, "test_module")

        assert "users" in module_info["dependencies"]
        assert "products" in module_info["dependencies"]


class TestDocumentationGeneration:
    """Test documentation generation functionality."""

    def test_generate_api_documentation_project(self, tmp_path):
        """Test API documentation generation for project."""
        docs = generate_api_documentation(tmp_path)

        assert "API Documentation for" in docs
        assert tmp_path.name in docs

    def test_generate_api_documentation_module(self, tmp_path):
        """Test API documentation generation for module."""
        docs = generate_api_documentation(tmp_path, "test_module")

        assert "API Documentation for Test_Module Module" in docs

    def test_generate_readme_template_project(self, tmp_path):
        """Test README template generation for project."""
        readme = generate_readme_template(tmp_path)

        assert "# " in readme
        assert tmp_path.name in readme

    def test_generate_readme_template_module(self, tmp_path):
        """Test README template generation for module."""
        readme = generate_readme_template(tmp_path, "test_module")

        assert "# Test_Module Module" in readme

    def test_generate_changelog_template_project(self, tmp_path):
        """Test changelog template generation for project."""
        changelog = generate_changelog_template(tmp_path)

        assert "Changelog for" in changelog
        assert tmp_path.name in changelog

    def test_generate_changelog_template_module(self, tmp_path):
        """Test changelog template generation for module."""
        changelog = generate_changelog_template(tmp_path, "test_module")

        assert "Changelog for Test_Module Module" in changelog


class TestDocumentationCommand:
    """Test the main documentation generation command."""

    @patch("fascraft.commands.docs.is_fastapi_project")
    @patch("fascraft.commands.docs.get_project_info")
    def test_generate_documentation_success(
        self, mock_get_project_info, mock_is_fastapi, tmp_path
    ):
        """Test successful documentation generation."""
        mock_is_fastapi.return_value = True
        mock_get_project_info.return_value = {
            "name": "test_project",
            "version": "1.0.0",
            "description": "Test project",
        }

        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        generate_documentation(
            path=str(tmp_path),
            output_dir="docs",
            include_api=True,
            include_readme=True,
            include_changelog=True,
        )

        # Check that docs directory was created
        docs_dir = tmp_path / "docs"
        assert docs_dir.exists()

        # Check that files were generated
        assert (docs_dir / "api_documentation.md").exists()
        assert (docs_dir / "README_template.md").exists()
        assert (docs_dir / "CHANGELOG_template.md").exists()
        assert (docs_dir / "project_overview.md").exists()

    @patch("fascraft.commands.docs.is_fastapi_project")
    def test_generate_documentation_not_fastapi_project(
        self, mock_is_fastapi, tmp_path
    ):
        """Test documentation generation with non-FastAPI project."""
        mock_is_fastapi.return_value = False

        with pytest.raises(typer.Exit):
            generate_documentation(path=str(tmp_path))

    @patch("fascraft.commands.docs.is_fastapi_project")
    def test_generate_documentation_path_not_exists(self, mock_is_fastapi):
        """Test documentation generation with non-existent path."""
        mock_is_fastapi.return_value = True

        with pytest.raises(typer.Exit):
            generate_documentation(path="/nonexistent/path")

    @patch("fascraft.commands.docs.is_fastapi_project")
    @patch("fascraft.commands.docs.get_project_info")
    @patch("fascraft.commands.docs.get_module_info")
    def test_generate_documentation_with_module(
        self, mock_get_module_info, mock_get_project_info, mock_is_fastapi, tmp_path
    ):
        """Test documentation generation for specific module."""
        mock_is_fastapi.return_value = True
        mock_get_project_info.return_value = {
            "name": "test_project",
            "version": "1.0.0",
            "description": "Test project",
        }
        mock_get_module_info.return_value = {
            "name": "test_module",
            "path": str(tmp_path / "test_module"),
            "files": ["models.py", "services.py"],
            "dependencies": ["users"],
        }

        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        generate_documentation(
            path=str(tmp_path), module="test_module", output_dir="docs"
        )

        # Check that module-specific documentation was generated
        docs_dir = tmp_path / "docs"
        assert (docs_dir / "test_module_overview.md").exists()


class TestOpenAPIGeneration:
    """Test OpenAPI specification generation."""

    @patch("fascraft.commands.docs.is_fastapi_project")
    def test_generate_openapi_spec_success(self, mock_is_fastapi, tmp_path):
        """Test successful OpenAPI specification generation."""
        mock_is_fastapi.return_value = True

        # Create a mock main.py
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        generate_openapi_spec(
            path=str(tmp_path), output_file="openapi.json", format="json"
        )

        # Check that OpenAPI spec was generated
        openapi_file = tmp_path / "openapi.json"
        assert openapi_file.exists()

        # Check content
        content = json.loads(openapi_file.read_text())
        assert content["openapi"] == "3.0.0"
        assert content["info"]["title"] == tmp_path.name

    @patch("fascraft.commands.docs.is_fastapi_project")
    def test_generate_openapi_spec_not_fastapi_project(self, mock_is_fastapi, tmp_path):
        """Test OpenAPI generation with non-FastAPI project."""
        mock_is_fastapi.return_value = False

        with pytest.raises(typer.Exit):
            generate_openapi_spec(path=str(tmp_path))

    @patch("fascraft.commands.docs.is_fastapi_project")
    def test_generate_openapi_spec_no_main_py(self, mock_is_fastapi, tmp_path):
        """Test OpenAPI generation without main.py."""
        mock_is_fastapi.return_value = True

        with pytest.raises(typer.Exit):
            generate_openapi_spec(path=str(tmp_path))


class TestCLIInterface:
    """Test the CLI interface for documentation commands."""

    def test_docs_app_help(self):
        """Test that docs app provides help."""
        runner = CliRunner()
        result = runner.invoke(docs_app, ["--help"])

        assert result.exit_code == 0
        assert "Documentation generation commands" in result.output

    def test_generate_command_help(self):
        """Test that generate command provides help."""
        runner = CliRunner()
        result = runner.invoke(docs_app, ["generate", "--help"])

        assert result.exit_code == 0
        assert "Generate comprehensive documentation" in result.output

    def test_openapi_command_help(self):
        """Test that openapi command provides help."""
        runner = CliRunner()
        result = runner.invoke(docs_app, ["openapi", "--help"])

        assert result.exit_code == 0
        assert "Generate OpenAPI specification" in result.output


class TestErrorHandling:
    """Test error handling in documentation generation."""

    @patch("fascraft.commands.docs.is_fastapi_project")
    @patch("fascraft.commands.docs.get_project_info")
    def test_generate_documentation_with_warnings(
        self, mock_get_project_info, mock_is_fastapi, tmp_path
    ):
        """Test documentation generation with warnings."""
        mock_is_fastapi.return_value = True
        mock_get_project_info.side_effect = Exception("Project info error")

        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        # Should not raise exception, just show warnings
        generate_documentation(path=str(tmp_path), output_dir="docs")

        # Check that docs directory was still created
        docs_dir = tmp_path / "docs"
        assert docs_dir.exists()

    @patch("fascraft.commands.docs.is_fastapi_project")
    @patch("fascraft.commands.docs.get_project_info")
    @patch("fascraft.commands.docs.generate_api_documentation")
    def test_generate_documentation_api_docs_failure(
        self, mock_generate_api, mock_get_project_info, mock_is_fastapi, tmp_path
    ):
        """Test documentation generation when API docs generation fails."""
        mock_is_fastapi.return_value = True
        mock_get_project_info.return_value = {
            "name": "test_project",
            "version": "1.0.0",
            "description": "Test project",
        }
        mock_generate_api.side_effect = Exception("API docs error")

        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        # Should not raise exception, just show warnings
        generate_documentation(path=str(tmp_path), output_dir="docs", include_api=True)

        # Check that docs directory was still created
        docs_dir = tmp_path / "docs"
        assert docs_dir.exists()


class TestTemplateRendering:
    """Test template rendering functionality."""

    def test_template_variables_substitution(self, tmp_path):
        """Test that template variables are properly substituted."""
        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        # Mock project info
        with patch("fascraft.commands.docs.get_project_info") as mock_get_project_info:
            mock_get_project_info.return_value = {
                "name": "test_project",
                "version": "2.0.0",
                "description": "A test project",
                "modules": ["users", "products"],
            }

            generate_documentation(
                path=str(tmp_path), output_dir="docs", include_readme=True
            )

            # Check that variables were substituted
            readme_file = tmp_path / "docs" / "README_template.md"
            content = readme_file.read_text()

            assert "test_project" in content
            assert "2.0.0" in content
            assert "A test project" in content
            assert "users" in content
            assert "products" in content


class TestIntegration:
    """Integration tests for documentation generation."""

    @patch("fascraft.commands.docs.is_fastapi_project")
    @patch("fascraft.commands.docs.get_project_info")
    @patch("fascraft.commands.docs.get_module_info")
    def test_full_documentation_generation_workflow(
        self, mock_get_module_info, mock_get_project_info, mock_is_fastapi, tmp_path
    ):
        """Test the complete documentation generation workflow."""
        mock_is_fastapi.return_value = True
        mock_get_project_info.return_value = {
            "name": "test_project",
            "version": "1.0.0",
            "description": "Test project",
            "modules": ["users", "products"],
        }
        mock_get_module_info.return_value = {
            "name": "users",
            "path": str(tmp_path / "users"),
            "files": ["models.py", "services.py"],
            "dependencies": [],
        }

        # Create a mock main.py to satisfy FastAPI detection
        (tmp_path / "main.py").write_text("from fastapi import FastAPI")

        # Generate documentation for a specific module
        generate_documentation(
            path=str(tmp_path),
            module="users",
            output_dir="docs",
            include_api=True,
            include_readme=True,
            include_changelog=True,
        )

        # Verify all expected files were generated
        docs_dir = tmp_path / "docs"
        expected_files = [
            "api_documentation.md",
            "README_template.md",
            "CHANGELOG_template.md",
            "users_overview.md",
        ]

        for expected_file in expected_files:
            assert (
                docs_dir / expected_file
            ).exists(), f"Expected file {expected_file} was not generated"

        # Verify file contents
        users_overview = docs_dir / "users_overview.md"
        content = users_overview.read_text()
        assert "Users Module Overview" in content
        assert "models.py" in content
        assert "services.py" in content
