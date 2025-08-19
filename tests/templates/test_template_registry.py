"""Tests for the template registry system."""

from pathlib import Path

import pytest

from fascraft.template_registry import (
    TemplateMetadata,
    TemplateRegistry,
    template_registry,
)


class TestTemplateMetadata:
    """Test the TemplateMetadata dataclass."""

    def test_template_metadata_creation(self):
        """Test creating a TemplateMetadata instance."""
        metadata = TemplateMetadata(
            name="test",
            display_name="Test Template",
            description="A test template",
            complexity="basic",
            category="test",
            dependencies=["fastapi"],
            template_path=Path("test/path"),
            preview_available=True,
        )

        assert metadata.name == "test"
        assert metadata.display_name == "Test Template"
        assert metadata.description == "A test template"
        assert metadata.complexity == "basic"
        assert metadata.category == "test"
        assert metadata.dependencies == ["fastapi"]
        assert metadata.template_path == Path("test/path")
        assert metadata.preview_available is True


class TestTemplateRegistry:
    """Test the TemplateRegistry class."""

    def test_template_registry_initialization(self):
        """Test that TemplateRegistry initializes with default templates."""
        registry = TemplateRegistry()

        # Check that default templates are loaded
        assert "basic" in registry._templates
        assert "crud" in registry._templates
        assert "api_first" in registry._templates
        assert "event_driven" in registry._templates
        assert "microservice" in registry._templates
        assert "admin_panel" in registry._templates

    def test_get_template_existing(self):
        """Test getting an existing template."""
        registry = TemplateRegistry()
        template = registry.get_template("basic")

        assert template.name == "basic"
        assert template.display_name == "Basic CRUD"
        assert template.category == "crud"

    def test_get_template_nonexistent(self):
        """Test getting a non-existent template raises error."""
        registry = TemplateRegistry()

        with pytest.raises(Exception) as exc_info:
            registry.get_template("nonexistent")

        assert "Template 'nonexistent' not found" in str(exc_info.value)

    def test_list_templates_all(self):
        """Test listing all templates."""
        registry = TemplateRegistry()
        templates = registry.list_templates()

        assert len(templates) == 6  # 6 default templates
        template_names = [t.name for t in templates]
        assert "basic" in template_names
        assert "crud" in template_names
        assert "api_first" in template_names

    def test_list_templates_by_category(self):
        """Test listing templates filtered by category."""
        registry = TemplateRegistry()
        crud_templates = registry.list_templates(category="crud")

        assert len(crud_templates) == 2  # basic and crud
        for template in crud_templates:
            assert template.category == "crud"

    def test_get_template_categories(self):
        """Test getting template categories."""
        registry = TemplateRegistry()
        categories = registry.get_template_categories()

        expected_categories = [
            "admin_panel",
            "api_first",
            "crud",
            "event_driven",
            "microservice",
        ]
        assert set(categories) == set(expected_categories)

    def test_validate_template_existing(self):
        """Test validating an existing template."""
        registry = TemplateRegistry()
        assert registry.validate_template("basic") is True

    def test_validate_template_nonexistent(self):
        """Test validating a non-existent template."""
        registry = TemplateRegistry()
        assert registry.validate_template("nonexistent") is False


class TestGlobalTemplateRegistry:
    """Test the global template registry instance."""

    def test_global_registry_available(self):
        """Test that the global template registry is available."""
        assert template_registry is not None
        assert isinstance(template_registry, TemplateRegistry)

    def test_global_registry_has_templates(self):
        """Test that the global registry has the expected templates."""
        templates = template_registry.list_templates()
        assert len(templates) == 6

        template_names = [t.name for t in templates]
        expected_names = [
            "basic",
            "crud",
            "api_first",
            "event_driven",
            "microservice",
            "admin_panel",
        ]
        assert set(template_names) == set(expected_names)

    def test_global_registry_template_details(self):
        """Test that global registry templates have correct details."""
        api_first = template_registry.get_template("api_first")

        assert api_first.name == "api_first"
        assert api_first.display_name == "API-First"
        assert api_first.category == "api_first"
        assert api_first.complexity == "intermediate"
        assert "fastapi" in api_first.dependencies
        assert api_first.preview_available is True
