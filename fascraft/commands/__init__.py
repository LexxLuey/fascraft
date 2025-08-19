"""FasCraft CLI commands package."""

from . import (
    analyze,
    analyze_dependencies,
    config,
    dependencies,
    docs,
    generate,
    generate_test,
    list,
    list_templates,
    migrate,
    new,
    remove,
    update,
)

__all__ = [
    "new",
    "generate",
    "list",
    "remove",
    "update",
    "analyze",
    "migrate",
    "config",
    "list_templates",
    "analyze_dependencies",
    "dependencies",
    "generate_test",
    "docs",
]
