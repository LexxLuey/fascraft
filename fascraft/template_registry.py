"""Template registry for managing available module template types."""

from dataclasses import dataclass
from pathlib import Path

from fascraft.exceptions import TemplateError


@dataclass
class TemplateMetadata:
    """Metadata for a module template."""

    name: str
    display_name: str
    description: str
    complexity: str  # "basic", "intermediate", "advanced"
    category: str  # "crud", "api_first", "event_driven", "microservice", "admin_panel"
    dependencies: list[str]
    template_path: Path
    preview_available: bool = True


class TemplateRegistry:
    """Registry for managing available module templates."""

    def __init__(self):
        self._templates: dict[str, TemplateMetadata] = {}
        self._load_default_templates()

    def _load_default_templates(self) -> None:
        """Load default templates from the module_templates directory."""
        # Basic template (existing)
        self._templates["basic"] = TemplateMetadata(
            name="basic",
            display_name="Basic CRUD",
            description="Simple CRUD operations with basic models and services",
            complexity="basic",
            category="crud",
            dependencies=["sqlalchemy", "pydantic"],
            template_path=Path("module_templates/basic"),
            preview_available=True,
        )

        # CRUD template (existing)
        self._templates["crud"] = TemplateMetadata(
            name="crud",
            display_name="Advanced CRUD",
            description="Enhanced CRUD with advanced features, indexes, and utilities",
            complexity="intermediate",
            category="crud",
            dependencies=["sqlalchemy", "pydantic"],
            template_path=Path("module_templates/crud"),
            preview_available=True,
        )

        # API-First template (new)
        self._templates["api_first"] = TemplateMetadata(
            name="api_first",
            display_name="API-First",
            description="API-centric design with comprehensive OpenAPI documentation",
            complexity="intermediate",
            category="api_first",
            dependencies=["sqlalchemy", "pydantic", "fastapi"],
            template_path=Path("module_templates/api_first"),
            preview_available=True,
        )

        # Event-Driven template (new)
        self._templates["event_driven"] = TemplateMetadata(
            name="event_driven",
            display_name="Event-Driven",
            description="Event-driven architecture with async event handlers",
            complexity="advanced",
            category="event_driven",
            dependencies=["sqlalchemy", "pydantic", "fastapi", "asyncio"],
            template_path=Path("module_templates/event_driven"),
            preview_available=True,
        )

        # Microservice template (new)
        self._templates["microservice"] = TemplateMetadata(
            name="microservice",
            display_name="Microservice",
            description="Lightweight, focused modules for microservice architecture",
            complexity="intermediate",
            category="microservice",
            dependencies=["fastapi", "pydantic"],
            template_path=Path("module_templates/microservice"),
            preview_available=True,
        )

        # Admin Panel template (new)
        self._templates["admin_panel"] = TemplateMetadata(
            name="admin_panel",
            display_name="Admin Panel",
            description="Administrative interface with role-based access control",
            complexity="advanced",
            category="admin_panel",
            dependencies=["sqlalchemy", "pydantic", "fastapi", "passlib"],
            template_path=Path("module_templates/admin_panel"),
            preview_available=True,
        )

    def get_template(self, template_name: str) -> TemplateMetadata:
        """Get template metadata by name."""
        if template_name not in self._templates:
            available = ", ".join(self._templates.keys())
            raise TemplateError(
                f"Template '{template_name}' not found",
                f"Available templates: {available}",
            )
        return self._templates[template_name]

    def list_templates(self, category: str | None = None) -> list[TemplateMetadata]:
        """List available templates, optionally filtered by category."""
        templates = list(self._templates.values())
        if category:
            templates = [t for t in templates if t.category == category]
        return sorted(templates, key=lambda t: (t.complexity, t.name))

    def get_template_categories(self) -> list[str]:
        """Get list of available template categories."""
        return sorted({t.category for t in self._templates.values()})

    def validate_template(self, template_name: str) -> bool:
        """Validate that a template exists and is accessible."""
        try:
            template = self.get_template(template_name)
            # Check if template directory exists
            template_dir = Path(__file__).parent / "templates" / template.template_path
            return template_dir.exists()
        except TemplateError:
            return False


# Global template registry instance
template_registry = TemplateRegistry()
