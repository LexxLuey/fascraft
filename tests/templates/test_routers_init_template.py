"""Tests for fascraft/templates/new_project/routers/__init__.py.jinja2."""

from pathlib import Path


class TestRoutersInitTemplate:
    """Test class for routers/__init__.py.jinja2 template."""

    def test_routers_init_template_exists(self):
        """Test that routers/__init__.py.jinja2 template file exists."""
        template_path = Path(
            "fascraft/templates/new_project/routers/__init__.py.jinja2"
        )
        assert template_path.exists(), "Routers init template file should exist"

    def test_routers_init_template_content_structure(self):
        """Test routers/__init__.py.jinja2 template content structure."""
        template_path = Path(
            "fascraft/templates/new_project/routers/__init__.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test docstring
        assert '"""Routers package for {{ project_name }}."""' in content

        # Test import
        assert "from .base import base_router" in content

        # Test __all__ definition
        assert '__all__ = ["base_router"]' in content

    def test_routers_init_template_line_coverage(self):
        """Test routers/__init__.py.jinja2 template covers all lines."""
        template_path = Path(
            "fascraft/templates/new_project/routers/__init__.py.jinja2"
        )
        content = template_path.read_text(encoding="utf-8")

        # Test all lines are covered by our assertions
        lines = content.split("\n")

        # Line 1: Docstring
        assert '"""Routers package for {{ project_name }}."""' in content

        # Line 3: Import
        assert "from .base import base_router" in content

        # Line 5: __all__ definition
        assert '__all__ = ["base_router"]' in content

        # Verify we're testing the right content
        assert len(lines) >= 5, "Template should have at least 5 lines"
