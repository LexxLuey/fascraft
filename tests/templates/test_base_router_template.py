"""Tests for fascraft/templates/new_project/routers/base.py.jinja2."""

from pathlib import Path


class TestBaseRouterTemplate:
    """Test class for base.py.jinja2 router template."""

    def test_base_router_template_exists(self):
        """Test that base.py.jinja2 router template file exists."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        assert template_path.exists(), "Base router template file should exist"

    def test_base_router_template_content_structure(self):
        """Test base.py.jinja2 router template content structure."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test imports
        assert "from fastapi import APIRouter" in content

        # Test router creation
        assert 'base_router = APIRouter(prefix="/api/v1")' in content

    def test_base_router_template_commented_imports(self):
        """Test base.py.jinja2 router template commented import structure."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test commented import examples
        assert "# from users import routers as user_routers" in content
        assert "# from products import routers as product_routers" in content

        # Test commented router inclusion examples
        assert (
            '# base_router.include_router(user_routers.router, prefix="/users", tags=["users"])'
            in content
        )
        assert (
            '# base_router.include_router(product_routers.router, prefix="/products", tags=["products"])'
            in content
        )

    def test_base_router_template_health_endpoint(self):
        """Test base.py.jinja2 router template health check endpoint."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test health check endpoint
        assert '@base_router.get("/health")' in content
        assert "async def health_check():" in content
        assert '"""Health check endpoint."""' in content
        assert 'return {"status": "healthy", "version": "0.1.0"}' in content

    def test_base_router_template_api_structure(self):
        """Test base.py.jinja2 router template API structure."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test API versioning
        assert "/api/v1" in content, "Should use API v1 prefix"

        # Test endpoint structure
        assert "/health" in content, "Should have health endpoint"

        # Test response format
        assert "status" in content, "Health response should have status field"
        assert "version" in content, "Health response should have version field"

    def test_base_router_template_documentation(self):
        """Test base.py.jinja2 router template documentation."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test docstrings
        assert '"""Base router for {{ project_name }} API endpoints."""' in content
        assert '"""Health check endpoint."""' in content

        # Test comments
        assert "# Create base router with common prefix" in content
        assert "# Import all module routers here" in content
        assert "# Include all module routers" in content
        assert "# Health check endpoint" in content

    def test_base_router_template_line_coverage(self):
        """Test base.py.jinja2 router template covers all lines including missing ones."""
        template_path = Path("fascraft/templates/new_project/routers/base.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "from fastapi import APIRouter" in content

        # Line 18-20: Health check endpoint decorator and function
        assert '@base_router.get("/health")' in content
        assert "async def health_check():" in content
        assert 'return {"status": "healthy", "version": "0.1.0"}' in content

        # Verify we're testing the right content
        assert len(lines) >= 20, "Template should have at least 20 lines"
