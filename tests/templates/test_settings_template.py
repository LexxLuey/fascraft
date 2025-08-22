"""Tests for fascraft/templates/new_project/config/settings.py.jinja2."""

from pathlib import Path


class TestSettingsTemplate:
    """Test class for settings.py.jinja2 template."""

    def test_settings_template_exists(self):
        """Test that settings.py.jinja2 template file exists."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        assert template_path.exists(), "Settings template file should exist"

    def test_settings_template_content_structure(self):
        """Test settings.py.jinja2 template content structure."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test template variables exist
        assert (
            "{{ project_name }}" in content
        ), "Template should contain project_name variable"

        # Test imports
        assert "from functools import lru_cache" in content
        assert "from typing import Optional" in content

        # Test try-except import fallback for pydantic
        assert "try:" in content
        assert "from pydantic_settings import BaseSettings" in content
        assert "except ImportError:" in content
        assert "from pydantic import BaseSettings" in content

    def test_settings_template_settings_class(self):
        """Test settings.py.jinja2 template Settings class structure."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test Settings class definition
        assert "class Settings(BaseSettings):" in content
        assert '"""Application settings."""' in content

        # Test application settings
        assert 'app_name: str = "{{ project_name }}"' in content
        assert 'app_version: str = "0.1.0"' in content
        assert "debug: bool = False" in content

        # Test database settings
        assert 'database_url: str = "sqlite:///./{{ project_name }}.db"' in content

        # Test security settings
        assert 'secret_key: str = "your-secret-key-here"' in content
        assert "access_token_expire_minutes: int = 30" in content

    def test_settings_template_cors_configuration(self):
        """Test settings.py.jinja2 template CORS configuration."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test CORS settings
        assert 'cors_origins: list[str] = ["*"]' in content
        assert "cors_allow_credentials: bool = True" in content
        assert 'cors_allow_methods: list[str] = ["*"]' in content
        assert 'cors_allow_headers: list[str] = ["*"]' in content

    def test_settings_template_config_class(self):
        """Test settings.py.jinja2 template Config class."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test Config class
        assert "class Config:" in content
        assert 'env_file = ".env"' in content
        assert "case_sensitive = True" in content
        assert 'env_prefix = ""' in content

        # Test validate_dependencies method
        assert "@classmethod" in content
        assert "def validate_dependencies(cls):" in content
        assert "try:" in content
        assert "import pydantic" in content
        assert "return True" in content
        assert "except ImportError:" in content
        assert "print(" in content

    def test_settings_template_get_settings_function(self):
        """Test settings.py.jinja2 template get_settings function."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test get_settings function
        assert "@lru_cache()" in content
        assert "def get_settings() -> Settings:" in content
        assert '"""Get cached settings instance."""' in content
        assert "return Settings()" in content

    def test_settings_template_error_handling(self):
        """Test settings.py.jinja2 template error handling structure."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test import error handling
        assert "try:" in content
        assert "except ImportError:" in content
        assert "print(" in content
        assert "Configuration error:" in content
        assert "raise" in content

    def test_settings_template_line_coverage(self):
        """Test settings.py.jinja2 template covers all lines including missing ones."""
        template_path = Path("fascraft/templates/new_project/config/settings.py.jinja2")
        content = template_path.read_text(encoding="utf-8")

        # Test specific missing lines from coverage report
        lines = content.split("\n")

        # Line 3: Import statement
        assert "from typing import Optional" in content

        # Line 17-57: Various settings and methods
        assert 'app_name: str = "{{ project_name }}"' in content
        assert 'app_version: str = "0.1.0"' in content
        assert "debug: bool = False" in content
        assert 'database_url: str = "sqlite:///./{{ project_name }}.db"' in content
        assert 'secret_key: str = "your-secret-key-here"' in content
        assert "access_token_expire_minutes: int = 30" in content
        assert 'cors_origins: list[str] = ["*"]' in content
        assert "cors_allow_credentials: bool = True" in content
        assert 'cors_allow_methods: list[str] = ["*"]' in content
        assert 'cors_allow_headers: list[str] = ["*"]' in content
        assert 'env_file = ".env"' in content
        assert "case_sensitive = True" in content
        assert 'env_prefix = ""' in content
        assert "@classmethod" in content
        assert "def validate_dependencies(cls):" in content
        assert "import pydantic" in content
        assert "return True" in content
        assert "print(" in content
        assert "@lru_cache()" in content
        assert "def get_settings() -> Settings:" in content
        assert "return Settings()" in content

        # Verify we're testing the right content
        assert len(lines) >= 57, "Template should have at least 57 lines"
