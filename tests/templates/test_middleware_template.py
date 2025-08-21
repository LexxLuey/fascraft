"""Tests for fascraft/templates/new_project/config/middleware.py.jinja2."""

from pathlib import Path


class TestMiddlewareTemplate:
    """Test class for middleware.py.jinja2 template."""

    def test_middleware_template_exists(self):
        """Test that middleware.py.jinja2 template file exists."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        assert template_path.exists(), "Middleware template file should exist"

    def test_middleware_template_content_structure(self):
        """Test middleware.py.jinja2 template content structure."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test imports
        assert "import time" in content
        assert "from typing import Callable" in content
        assert "from fastapi import Request, Response" in content
        assert "from fastapi.middleware.cors import CORSMiddleware" in content

        # Test try-except import fallback
        assert "try:" in content
        assert "from starlette.middleware.base import BaseHTTPMiddleware" in content
        assert "except ImportError:" in content
        assert "from fastapi.middleware.base import BaseHTTPMiddleware" in content

    def test_middleware_template_timing_middleware(self):
        """Test middleware.py.jinja2 template TimingMiddleware class."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test TimingMiddleware class
        assert "class TimingMiddleware(BaseHTTPMiddleware):" in content
        assert "async def dispatch(" in content
        assert "start_time = time.time()" in content
        assert "process_time = time.time() - start_time" in content
        assert 'response.headers["X-Process-Time"]' in content

    def test_middleware_template_setup_function(self):
        """Test middleware.py.jinja2 template setup_middleware function."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test setup_middleware function
        assert "def setup_middleware(app):" in content
        assert "settings = get_settings()" in content

        # Test CORS middleware setup
        assert "app.add_middleware(" in content
        assert "CORSMiddleware" in content
        assert "allow_origins=settings.cors_origins" in content
        assert "allow_credentials=settings.cors_allow_credentials" in content
        assert "allow_methods=settings.cors_allow_methods" in content
        assert "allow_headers=settings.cors_allow_headers" in content

        # Test timing middleware setup
        assert "app.add_middleware(TimingMiddleware)" in content

    def test_middleware_template_error_handling(self):
        """Test middleware.py.jinja2 template error handling structure."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test import error handling
        assert "try:" in content
        assert "except ImportError:" in content
        assert "print(" in content
        assert "Configuration error:" in content
        assert "raise" in content

    def test_middleware_template_settings_integration(self):
        """Test middleware.py.jinja2 template integrates with settings."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test settings usage
        assert "from .settings import get_settings" in content
        assert "settings = get_settings()" in content
        assert "settings.cors_origins" in content
        assert "settings.cors_allow_credentials" in content
        assert "settings.cors_allow_methods" in content
        assert "settings.cors_allow_headers" in content

    def test_middleware_template_line_coverage(self):
        """Test middleware.py.jinja2 template covers all lines including missing ones."""
        template_path = Path(
            "fascraft/templates/new_project/config/middleware.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "import time" in content

        # Line 15: Import statement
        assert "from fastapi import Request, Response" in content

        # Line 18-49: Various middleware components
        assert "from fastapi.middleware.cors import CORSMiddleware" in content
        assert "try:" in content
        assert "from starlette.middleware.base import BaseHTTPMiddleware" in content
        assert "except ImportError:" in content
        assert "from fastapi.middleware.base import BaseHTTPMiddleware" in content
        assert "print(" in content
        assert "Configuration error:" in content
        assert "raise" in content
        assert "class TimingMiddleware(BaseHTTPMiddleware):" in content
        assert "async def dispatch(" in content
        assert "start_time = time.time()" in content
        assert "process_time = time.time() - start_time" in content
        assert 'response.headers["X-Process-Time"]' in content
        assert "def setup_middleware(app):" in content
        assert "settings = get_settings()" in content
        assert "app.add_middleware(" in content
        assert "allow_origins=settings.cors_origins" in content
        assert "allow_credentials=settings.cors_allow_credentials" in content
        assert "allow_methods=settings.cors_allow_methods" in content
        assert "allow_headers=settings.cors_allow_headers" in content
        assert "app.add_middleware(TimingMiddleware)" in content

        # Verify we're testing the right content
        assert len(lines) >= 49, "Template should have at least 49 lines"
