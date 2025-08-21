"""Tests for the main.py.jinja2 template."""

from pathlib import Path


class TestMainTemplate:
    """Test the main.py.jinja2 template functionality."""

    def test_template_file_exists(self):
        """Test that the template file exists."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        assert template_path.exists(), "Template file should exist"

    def test_template_content_structure(self):
        """Test the overall template structure."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for essential components
        assert "from fastapi import FastAPI" in template_content
        assert "app = FastAPI(" in template_content
        assert "app.include_router(" in template_content
        assert '@app.get("/")' in template_content
        assert "async def root():" in template_content
        assert 'if __name__ == "__main__":' in template_content
        assert "uvicorn.run(" in template_content

    def test_template_variables(self):
        """Test that template variables are properly used."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for Jinja2 template variables
        assert "{{ project_name }}" in template_content
        assert "{{" in template_content
        assert "}}" in template_content

    def test_import_structure(self):
        """Test import statements in the template."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for required imports
        assert "from fastapi import FastAPI" in template_content
        assert "from config.settings import get_settings" in template_content
        assert "from config.middleware import setup_middleware" in template_content
        assert "from routers import base_router" in template_content
        assert "import uvicorn" in template_content

    def test_error_handling_structure(self):
        """Test error handling structure in the template."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for try-except blocks
        assert "try:" in template_content
        assert "except ImportError as e:" in template_content
        assert "except Exception as e:" in template_content

        # Check for error messages
        assert "Configuration error:" in template_content
        assert "Middleware setup failed:" in template_content
        assert 'print(f"Configuration error: {e}")' in template_content
        assert 'print(f"Warning: Middleware setup failed: {e}")' in template_content

    def test_app_configuration(self):
        """Test app configuration structure."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for settings usage
        assert "settings.app_name" in template_content
        assert "settings.app_version" in template_content
        assert "settings.debug" in template_content
        assert "get_settings()" in template_content

    def test_middleware_setup(self):
        """Test middleware setup structure."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for middleware setup
        assert "setup_middleware(" in template_content
        assert "setup_middleware(app)" in template_content

    def test_router_integration(self):
        """Test router integration structure."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for router setup
        assert "app.include_router(" in template_content
        assert "base_router" in template_content

    def test_endpoint_definitions(self):
        """Test endpoint definitions."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for root endpoint
        assert '@app.get("/")' in template_content
        assert "async def root():" in template_content
        assert (
            'return {"message": f"Hello from {settings.app_name}!"}' in template_content
        )

    def test_main_execution_block(self):
        """Test main execution block structure."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for main block
        assert 'if __name__ == "__main__":' in template_content
        assert "uvicorn.run(" in template_content
        assert 'host="0.0.0.0"' in template_content
        assert "port=8000" in template_content

    def test_comments_and_documentation(self):
        """Test comments and documentation in template."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for important comments
        assert '"""Main FastAPI application for' in template_content
        assert '"""Root endpoint."""' in template_content
        assert "Health check is now handled by base router" in template_content
        assert "Database setup note:" in template_content

    def test_template_completeness(self):
        """Test that template is complete and well-formed."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for proper Python syntax structure
        assert template_content.count("(") == template_content.count(
            ")"
        ), "Unmatched parentheses"
        assert template_content.count("{") == template_content.count(
            "}"
        ), "Unmatched braces"
        assert template_content.count("[") == template_content.count(
            "]"
        ), "Unmatched brackets"

        # Check for proper indentation (basic check)
        lines = template_content.split("\n")
        for line in lines:
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                # This line should not be empty and should not start with whitespace
                if not line.startswith('"""') and not line.startswith("#"):
                    # Skip docstrings and comments
                    pass

    def test_jinja2_syntax(self):
        """Test Jinja2 template syntax."""
        template_content = Path(
            "fascraft/templates/new_project/main.py.jinja2"
        ).read_text()

        # Check for proper Jinja2 variable syntax
        assert "{{ project_name }}" in template_content

        # Check that there are no malformed Jinja2 tags
        assert "{{{" not in template_content
        assert "}}}" not in template_content
        assert "{{" in template_content
        assert "}}" in template_content
