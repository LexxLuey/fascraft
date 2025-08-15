"""Tests for Jinja2 template validation and rendering."""

from pathlib import Path

import pytest
from jinja2 import Environment, PackageLoader, select_autoescape

from fastcraft.commands.new import create_new_project


class TestTemplateRendering:
    """Test template rendering and validation."""

    def test_jinja2_environment_setup(self) -> None:
        """Test that Jinja2 environment is properly configured."""
        env = Environment(
            loader=PackageLoader("fastcraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        # Verify environment is configured
        assert env is not None
        assert env.loader is not None
        assert env.autoescape is not None

    def test_all_templates_exist_and_loadable(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that all required templates exist and can be loaded."""
        env = Environment(
            loader=PackageLoader("fastcraft", "templates/new_project"),
            autoescape=select_autoescape(),
        )

        required_templates = [
            "__init__.py.jinja2",
            "main.py.jinja2",
            "pyproject.toml.jinja2",
            "README.md.jinja2",
        ]

        for template_name in required_templates:
            template = env.get_template(template_name)
            assert template is not None

            # Test basic rendering
            rendered = template.render(project_name=sample_project_name)
            assert rendered is not None
            assert len(rendered) > 0

    def test_template_variable_substitution(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template variables are properly substituted."""
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Check main.py template substitution
        main_content = (project_path / "main.py").read_text()
        assert sample_project_name in main_content
        assert "from config.settings import get_settings" in main_content
        assert "title=settings.app_name" in main_content

        # Check pyproject.toml template substitution
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert f'name = "{sample_project_name}"' in pyproject_content

        # Check README.md template substitution
        readme_content = (project_path / "README.md").read_text()
        assert f"# {sample_project_name}" in readme_content

    def test_template_rendering_consistency(self, temp_dir: Path) -> None:
        """Test that template rendering is consistent across different names."""
        test_names = ["project1", "project2", "different-name"]

        for name in test_names:
            project_path = temp_dir / name

            # Create project
            create_new_project(name, temp_dir)

            # Verify main.py contains the name
            main_content = (project_path / "main.py").read_text()
            assert name in main_content
            assert "from config.settings import get_settings" in main_content
            assert "title=settings.app_name" in main_content

            # Verify pyproject.toml contains the name
            pyproject_content = (project_path / "pyproject.toml").read_text()
            assert f'name = "{name}"' in pyproject_content

    def test_template_file_structure(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that generated files have proper structure and content."""
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Test main.py structure
        main_content = (project_path / "main.py").read_text()
        assert "from fastapi import FastAPI" in main_content
        assert "app = FastAPI(" in main_content
        assert '@app.get("/")' in main_content
        assert '@app.get("/health")' in main_content
        assert "async def root():" in main_content
        assert "async def health_check():" in main_content

        # Test pyproject.toml structure
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert "[tool.poetry]" in pyproject_content
        assert "[tool.poetry.dependencies]" in pyproject_content
        assert "[tool.poetry.group.dev.dependencies]" in pyproject_content
        assert "fastapi = " in pyproject_content
        assert "uvicorn = " in pyproject_content

        # Test README.md structure
        readme_content = (project_path / "README.md").read_text()
        assert "# " in readme_content
        assert "## Getting Started" in readme_content
        assert "## API Endpoints" in readme_content
        assert "## Development" in readme_content

    def test_template_encoding_and_formatting(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that templates generate properly formatted and encoded content."""
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Test main.py formatting
        main_content = (project_path / "main.py").read_text()
        lines = main_content.splitlines()

        # Check for proper imports
        assert any("from fastapi import FastAPI" in line for line in lines)

        # Check for proper function definitions
        assert any("async def root():" in line for line in lines)
        assert any("async def health_check():" in line for line in lines)

        # Check for proper decorators
        assert any('@app.get("/")' in line for line in lines)
        assert any('@app.get("/health")' in line for line in lines)

    def test_template_error_handling(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template errors are handled gracefully."""
        # This test ensures that our templates don't have syntax errors
        # and can render without issues

        try:
            create_new_project(sample_project_name, temp_dir)
            # If we get here, templates rendered successfully
            assert True
        except Exception as e:
            pytest.fail(f"Template rendering failed: {e}")

    def test_generated_files_are_valid_python(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that generated Python files are syntactically valid."""
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Test main.py syntax
        main_path = project_path / "main.py"
        try:
            # Try to compile the Python code
            compile(main_path.read_text(), str(main_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated main.py has syntax error: {e}")

        # Test __init__.py syntax
        init_path = project_path / "__init__.py"
        try:
            compile(init_path.read_text(), str(init_path), "exec")
        except SyntaxError as e:
            pytest.fail(f"Generated __init__.py has syntax error: {e}")

    def test_template_content_validation(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template content meets quality standards."""
        create_new_project(sample_project_name, temp_dir)

        project_path = temp_dir / sample_project_name

        # Test main.py content quality
        main_content = (project_path / "main.py").read_text()

        # Should have proper docstring
        assert '"""Main FastAPI application for' in main_content

        # Should have proper imports
        assert "from fastapi import FastAPI" in main_content

        # Should have proper app configuration
        assert "app = FastAPI(" in main_content
        assert "title=" in main_content
        assert "description=" in main_content
        assert "version=" in main_content

        # Should have proper endpoints
        assert "async def root():" in main_content
        assert "async def health_check():" in main_content

        # Should have proper uvicorn integration
        assert 'if __name__ == "__main__":' in main_content
        assert "import uvicorn" in main_content
        assert "uvicorn.run(app" in main_content
