"""Application settings and configuration."""

from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        print("Configuration error: pydantic not available")
        print("Please install required dependencies: pip install -r requirements.txt")
        raise


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "ecommerce-api"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./ecommerce-api.db"

    # Security
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = ""  # No prefix for environment variables

        # Fallback for missing dependencies
        @classmethod
        def validate_dependencies(cls):
            try:
                # Check if pydantic is available without importing
                import importlib.util

                return importlib.util.find_spec("pydantic") is not None
            except ImportError:
                print("Warning: pydantic not available, using basic settings")
                return False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
