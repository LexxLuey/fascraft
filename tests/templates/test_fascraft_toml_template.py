"""Tests for fascraft/templates/new_project/fascraft.toml.jinja2."""

from pathlib import Path


class TestFascraftTomlTemplate:
    """Test class for fascraft.toml.jinja2 template."""

    def test_fascraft_toml_template_exists(self):
        """Test that fascraft.toml.jinja2 template file exists."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        assert template_path.exists(), "Fascraft TOML template file should exist"

    def test_fascraft_toml_template_content_structure(self):
        """Test fascraft.toml.jinja2 template content structure."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test TOML structure - this is a custom FasCraft config, not Poetry
        assert "[project]" in content, "Should have project section"
        assert 'name = "{{ project_name }}"' in content, "Should have project name"
        assert 'version = "0.1.0"' in content, "Should have version"
        assert 'description = "A FastAPI project generated with FasCraft"' in content

    def test_fascraft_toml_template_router_configuration(self):
        """Test fascraft.toml.jinja2 template router configuration."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test router configuration
        assert "[router]" in content
        assert 'base_prefix = "/api/v1"' in content
        assert "health_endpoint = true" in content

    def test_fascraft_toml_template_database_configuration(self):
        """Test fascraft.toml.jinja2 template database configuration."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test database configuration
        assert "[database]" in content
        assert 'default = "sqlite"' in content
        assert 'supported = ["sqlite", "postgresql", "mysql", "mongodb"]' in content

    def test_fascraft_toml_template_modules_configuration(self):
        """Test fascraft.toml.jinja2 template modules configuration."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test modules configuration
        assert "[modules]" in content
        assert "auto_import = true" in content
        assert 'prefix_strategy = "plural"' in content
        assert "test_coverage = true" in content

    def test_fascraft_toml_template_environment_configuration(self):
        """Test fascraft.toml.jinja2 template environment configuration."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test development configuration
        assert "[development]" in content
        assert "auto_reload = true" in content
        assert "debug = true" in content
        assert 'log_level = "DEBUG"' in content

        # Test production configuration
        assert "[production]" in content
        assert "auto_reload = false" in content
        assert "debug = false" in content
        assert 'log_level = "INFO"' in content

    def test_fascraft_toml_template_header_comment(self):
        """Test fascraft.toml.jinja2 template header comment."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test header comment
        assert "# FasCraft project configuration for {{ project_name }}" in content

    def test_fascraft_toml_template_line_coverage(self):
        """Test fascraft.toml.jinja2 template covers all lines including missing ones."""
        template_path = Path("fascraft/templates/new_project/fascraft.toml.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Project section start
        assert "[project]" in content

        # Line 17: Database section start
        assert "[database]" in content

        # Line 21-29: Various configuration values
        assert 'default = "sqlite"' in content
        assert 'supported = ["sqlite", "postgresql", "mysql", "mongodb"]' in content
        assert "[modules]" in content
        assert "auto_import = true" in content
        assert 'prefix_strategy = "plural"' in content
        assert "test_coverage = true" in content

        # Verify we're testing the right content
        assert len(lines) >= 29, "Template should have at least 29 lines"
