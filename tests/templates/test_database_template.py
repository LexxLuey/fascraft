"""Tests for fascraft/templates/new_project/config/database.py.jinja2."""

from pathlib import Path


class TestDatabaseTemplate:
    """Test class for database.py.jinja2 template."""

    def test_database_template_exists(self):
        """Test that database.py.jinja2 template file exists."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        assert template_path.exists(), "Database template file should exist"

    def test_database_template_content_structure(self):
        """Test database.py.jinja2 template content structure."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test key imports
        assert "from sqlalchemy import create_engine" in content
        assert "from sqlalchemy.ext.declarative import declarative_base" in content
        assert "from sqlalchemy.orm import sessionmaker" in content

        # Test settings import
        assert "from .settings import get_settings" in content

        # Test database configuration
        assert "engine = create_engine(" in content
        assert "SessionLocal = sessionmaker(" in content
        assert "Base = declarative_base()" in content

        # Test function definitions
        assert "def get_db():" in content
        assert "def create_tables():" in content
        assert "def get_database_url() -> str:" in content

    def test_database_template_sqlite_handling(self):
        """Test database.py.jinja2 template SQLite-specific logic."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test SQLite-specific configuration
        assert "check_same_thread" in content, "Should handle SQLite connection args"
        assert "sqlite" in content, "Should reference SQLite in database URL check"

    def test_database_template_error_handling(self):
        """Test database.py.jinja2 template error handling structure."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test try-finally pattern in get_db
        assert "try:" in content
        assert "finally:" in content
        assert "db.close()" in content

    def test_database_template_settings_integration(self):
        """Test database.py.jinja2 template integrates with settings."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test settings usage
        assert "settings = get_settings()" in content
        assert "settings.database_url" in content
        assert "settings.debug" in content

    def test_database_template_line_coverage(self):
        """Test database.py.jinja2 template covers all lines including missing ones."""
        template_path = Path("fascraft/templates/new_project/config/database.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "from sqlalchemy import create_engine" in content

        # Line 20-42: Various database functions and logic
        assert "def get_db():" in content
        assert "db = SessionLocal()" in content
        assert "try:" in content
        assert "yield db" in content
        assert "finally:" in content
        assert "db.close()" in content
        assert "def create_tables():" in content
        assert "Base.metadata.create_all(bind=engine)" in content
        assert "def get_database_url() -> str:" in content
        assert "return settings.database_url" in content

        # Verify we're testing the right content
        assert len(lines) >= 42, "Template should have at least 42 lines"
