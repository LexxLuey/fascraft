"""Tests for template rendering and generation."""

from pathlib import Path
from unittest.mock import patch

import pytest

from fascraft.commands.new import create_project_structure, render_essential_templates


class TestTemplateRendering:
    """Test template rendering functionality."""

    def test_template_variable_substitution(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template variables are properly substituted."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        # Mock console to avoid output during tests
        with patch("fascraft.commands.new.console"):
            # Create project structure and render essential templates directly
            create_project_structure(project_path, sample_project_name)
            render_essential_templates(project_path, sample_project_name)

        # Check main.py template substitution
        main_content = (project_path / "main.py").read_text()
        assert sample_project_name in main_content
        assert "from config.settings import get_settings" in main_content
        assert "title=settings.app_name" in main_content

        # Check pyproject.toml template substitution
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert f'name = "{sample_project_name}"' in pyproject_content

        # Check __init__.py template substitution
        init_content = (project_path / "__init__.py").read_text()
        assert sample_project_name in init_content

        # Check README.md template substitution
        readme_content = (project_path / "README.md").read_text()
        assert f"# {sample_project_name}" in readme_content

        # Check fascraft.toml template substitution
        fascraft_content = (project_path / "fascraft.toml").read_text()
        assert sample_project_name in fascraft_content

    def test_template_rendering_consistency(self, temp_dir: Path) -> None:
        """Test that template rendering is consistent across different names."""
        test_names = ["project1", "project2", "different-name"]

        # Ensure temp_dir exists
        temp_dir.mkdir(exist_ok=True)

        with patch("fascraft.commands.new.console"):
            for name in test_names:
                project_path = temp_dir / name

                # Create project structure and render essential templates directly
                create_project_structure(project_path, name)
                render_essential_templates(project_path, name)

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
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        with patch("fascraft.commands.new.console"):
            # Create project structure and render essential templates directly
            create_project_structure(project_path, sample_project_name)
            render_essential_templates(project_path, sample_project_name)

        # Test main.py structure
        main_content = (project_path / "main.py").read_text()
        assert "from fastapi import FastAPI" in main_content
        assert "app = FastAPI(" in main_content
        assert '@app.get("/")' in main_content
        assert "async def root():" in main_content

        # Test base router integration
        assert "from routers import base_router" in main_content
        assert "app.include_router(base_router)" in main_content
        assert (
            "# Health check is now handled by base router at /api/v1/health"
            in main_content
        )

        # Test pyproject.toml structure
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert "[tool.poetry]" in pyproject_content
        assert "[tool.poetry.dependencies]" in pyproject_content
        assert "[tool.poetry.group.dev.dependencies]" in pyproject_content
        assert "fastapi = " in pyproject_content
        assert "uvicorn = " in pyproject_content

        # Test config files structure
        config_init = (project_path / "config" / "__init__.py").read_text()
        assert config_init is not None
        assert len(config_init) > 0

        # Test router files structure
        router_init = (project_path / "routers" / "__init__.py").read_text()
        assert router_init is not None
        assert len(router_init) > 0

        # Test README.md structure
        readme_content = (project_path / "README.md").read_text()
        assert "# " in readme_content
        assert "## " in readme_content
        assert "Getting Started" in readme_content

        # Test fascraft.toml structure
        fascraft_content = (project_path / "fascraft.toml").read_text()
        assert fascraft_content is not None
        assert len(fascraft_content) > 0

        # Test .env.sample structure
        env_sample_content = (project_path / ".env.sample").read_text()
        assert env_sample_content is not None
        assert len(env_sample_content) > 0

        # Test .gitignore structure
        gitignore_content = (project_path / ".gitignore").read_text()
        assert gitignore_content is not None
        assert len(gitignore_content) > 0

        # Test .dockerignore structure
        dockerignore_content = (project_path / ".dockerignore").read_text()
        assert dockerignore_content is not None
        assert len(dockerignore_content) > 0

    def test_template_encoding_and_formatting(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that templates generate properly formatted and encoded content."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        with patch("fascraft.commands.new.console"):
            # Create project structure and render essential templates directly
            create_project_structure(project_path, sample_project_name)
            render_essential_templates(project_path, sample_project_name)

        # Test file encoding
        main_content = (project_path / "main.py").read_text(encoding="utf-8")
        assert main_content is not None
        assert len(main_content) > 0

        # Test that files are properly formatted
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert pyproject_content is not None
        assert len(pyproject_content) > 0

        init_content = (project_path / "__init__.py").read_text()
        assert init_content is not None
        assert len(init_content) > 0

        readme_content = (project_path / "README.md").read_text()
        assert readme_content is not None
        assert len(readme_content) > 0

        # Test additional essential templates
        fascraft_content = (project_path / "fascraft.toml").read_text()
        assert fascraft_content is not None
        assert len(fascraft_content) > 0

        env_sample_content = (project_path / ".env.sample").read_text()
        assert env_sample_content is not None
        assert len(env_sample_content) > 0

        gitignore_content = (project_path / ".gitignore").read_text()
        assert gitignore_content is not None
        assert len(gitignore_content) > 0

        dockerignore_content = (project_path / ".dockerignore").read_text()
        assert dockerignore_content is not None
        assert len(dockerignore_content) > 0

    def test_template_error_handling(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template errors are handled gracefully."""
        # This test ensures that our templates don't have syntax errors
        # and can render without issues

        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        try:
            with patch("fascraft.commands.new.console"):
                # Create project structure and render essential templates directly
                create_project_structure(project_path, sample_project_name)
                render_essential_templates(project_path, sample_project_name)

            # If we get here, templates rendered successfully
            assert True
        except Exception as e:
            pytest.fail(f"Template rendering failed: {e}")

    def test_generated_files_are_valid_python(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that generated Python files are syntactically valid."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        with patch("fascraft.commands.new.console"):
            # Create project structure and render essential templates directly
            create_project_structure(project_path, sample_project_name)
            render_essential_templates(project_path, sample_project_name)

        # Test Python syntax validity
        import ast

        # Test main.py
        main_content = (project_path / "main.py").read_text()
        try:
            ast.parse(main_content)
        except SyntaxError as e:
            pytest.fail(f"main.py has invalid Python syntax: {e}")

        # Test config files
        config_init = (project_path / "config" / "__init__.py").read_text()
        try:
            ast.parse(config_init)
        except SyntaxError as e:
            pytest.fail(f"config/__init__.py has invalid Python syntax: {e}")

        # Test router files
        router_init = (project_path / "routers" / "__init__.py").read_text()
        try:
            ast.parse(router_init)
        except SyntaxError as e:
            pytest.fail(f"routers/__init__.py has invalid Python syntax: {e}")

    def test_template_content_validation(
        self, temp_dir: Path, sample_project_name: str
    ) -> None:
        """Test that template content meets quality standards."""
        temp_dir.mkdir(exist_ok=True)
        project_path = temp_dir / sample_project_name

        with patch("fascraft.commands.new.console"):
            # Create project structure and render essential templates directly
            create_project_structure(project_path, sample_project_name)
            render_essential_templates(project_path, sample_project_name)

        # Validate main.py content
        main_content = (project_path / "main.py").read_text()
        assert "FastAPI" in main_content
        assert "app = FastAPI(" in main_content
        assert "async def" in main_content

        # Validate pyproject.toml content
        pyproject_content = (project_path / "pyproject.toml").read_text()
        assert "name =" in pyproject_content
        assert "version =" in pyproject_content
        assert "description =" in pyproject_content

        # Validate __init__.py content
        init_content = (project_path / "__init__.py").read_text()
        assert init_content is not None
        assert len(init_content) > 0

        # Validate README.md content
        readme_content = (project_path / "README.md").read_text()
        assert "# " in readme_content
        assert "## " in readme_content
        assert "Getting Started" in readme_content

        # Validate fascraft.toml content
        fascraft_content = (project_path / "fascraft.toml").read_text()
        assert fascraft_content is not None
        assert len(fascraft_content) > 0

        # Validate .env.sample content
        env_sample_content = (project_path / ".env.sample").read_text()
        assert env_sample_content is not None
        assert len(env_sample_content) > 0

        # Validate .gitignore content
        gitignore_content = (project_path / ".gitignore").read_text()
        assert gitignore_content is not None
        assert len(gitignore_content) > 0

        # Validate .dockerignore content
        dockerignore_content = (project_path / ".dockerignore").read_text()
        assert dockerignore_content is not None
        assert len(dockerignore_content) > 0
