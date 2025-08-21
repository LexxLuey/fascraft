"""Tests for fascraft/templates/new_project/main.py.jinja2."""

from pathlib import Path


class TestMainPyTemplate:
    """Test class for main.py.jinja2 template."""

    def test_main_py_template_exists(self):
        """Test that main.py.jinja2 template file exists."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        assert template_path.exists(), "Main.py template file should exist"

    def test_main_py_template_content_structure(self):
        """Test main.py.jinja2 template content structure."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test imports
        assert "from fastapi import FastAPI" in content
        assert "from config.settings import get_settings" in content
        assert "from config.middleware import setup_middleware" in content

        # Test FastAPI app creation
        assert "app = FastAPI(" in content
        assert "title=settings.app_name" in content
        assert 'description="A FastAPI project generated with FasCraft"' in content
        assert "version=settings.app_version" in content
        assert "debug=settings.debug" in content

    def test_main_py_template_import_error_handling(self):
        """Test main.py.jinja2 template import error handling."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test try-except blocks for imports
        assert "try:" in content
        assert "from config.settings import get_settings" in content
        assert "from config.middleware import setup_middleware" in content
        assert "except ImportError as e:" in content
        assert 'print(f"Configuration error: {e}")' in content
        assert (
            'print("Please install required dependencies: pip install -r requirements.txt")'
            in content
        )
        assert "raise" in content

    def test_main_py_template_middleware_setup(self):
        """Test main.py.jinja2 template middleware setup."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test middleware setup
        assert "try:" in content
        assert "setup_middleware(app)" in content
        assert "except Exception as e:" in content
        assert 'print(f"Warning: Middleware setup failed: {e}")' in content
        assert 'print("Application will run without custom middleware")' in content

    def test_main_py_template_router_integration(self):
        """Test main.py.jinja2 template router integration."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test router imports and inclusion
        assert "from routers import base_router" in content
        assert "app.include_router(base_router)" in content

    def test_main_py_template_root_endpoint(self):
        """Test main.py.jinja2 template root endpoint."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test root endpoint
        assert '@app.get("/")' in content
        assert "async def root():" in content
        assert '"""Root endpoint."""' in content
        assert 'return {"message": f"Hello from {settings.app_name}!"}' in content

    def test_main_py_template_main_block(self):
        """Test main.py.jinja2 template main block."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test main block
        assert 'if __name__ == "__main__":' in content
        assert "import uvicorn" in content
        assert 'uvicorn.run(app, host="0.0.0.0", port=8000)' in content

    def test_main_py_template_database_notes(self):
        """Test main.py.jinja2 template database setup notes."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test database setup comments
        assert "# Database setup note:" in content
        assert "After creating models, run 'alembic init alembic'" in content
        assert "See README.md for detailed setup instructions" in content

    def test_main_py_template_health_check_comment(self):
        """Test main.py.jinja2 template health check comment."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test health check comment
        assert (
            "# Health check is now handled by base router at /api/v1/health" in content
        )

    def test_main_py_template_line_coverage(self):
        """Test main.py.jinja2 template covers all lines including missing ones."""
        template_path = Path("fascraft/templates/new_project/main.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "from fastapi import FastAPI" in content

        # Line 25-53: Various sections and comments
        assert "from routers import base_router" in content
        assert "app.include_router(base_router)" in content
        assert '@app.get("/")' in content
        assert "async def root():" in content
        assert 'return {"message": f"Hello from {settings.app_name}!"}' in content
        assert (
            "# Health check is now handled by base router at /api/v1/health" in content
        )
        assert "# Database setup note:" in content
        assert "After creating models, run 'alembic init alembic'" in content
        assert "See README.md for detailed setup instructions" in content
        assert 'if __name__ == "__main__":' in content
        assert "import uvicorn" in content
        assert 'uvicorn.run(app, host="0.0.0.0", port=8000)' in content

        # Verify we're testing the right content
        assert len(lines) >= 53, "Template should have at least 53 lines"
