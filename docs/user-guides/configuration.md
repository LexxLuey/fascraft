# Configuration Management Guide

Learn how to manage configuration in your FasCraft projects. This guide covers environment variables, settings management, database configuration, and best practices for different deployment environments.

## 🚀 Overview

FasCraft provides a robust configuration system that:
- Centralizes all application settings
- Supports multiple environments (development, staging, production)
- Uses environment variables for sensitive data
- Provides type-safe configuration with Pydantic
- Includes sensible defaults for common scenarios

## 📋 Configuration Structure

### Generated Configuration Files
```
config/
├── __init__.py             # Configuration module initialization
├── settings.py             # Main settings and environment configuration
├── database.py             # Database connection and session management
├── exceptions.py           # Custom exception definitions
└── middleware.py           # Custom middleware configuration
```

## 🔧 Core Configuration

### `config/settings.py` - Main Settings
```python
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Application settings
    app_name: str = "FasCraft API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # Database settings
    database_url: str = "sqlite:///./app.db"
    database_echo: bool = False
    
    # Security settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

### Environment Variable Mapping
```bash
# Application settings
APP_NAME="My Custom API"
APP_VERSION="2.0.0"
DEBUG=true
ENVIRONMENT="development"

# Server settings
HOST="127.0.0.1"
PORT=8001
RELOAD=true

# Database settings
DATABASE_URL="postgresql://user:pass@localhost:5432/mydb"
DATABASE_ECHO=true

# Security settings
SECRET_KEY="your-super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS settings
CORS_ORIGINS=["http://localhost:3000","https://myapp.com"]
CORS_ALLOW_CREDENTIALS=true

# Logging settings
LOG_LEVEL="DEBUG"
```

## 🗄️ Database Configuration

### `config/database.py` - Database Setup
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config.settings import get_settings

settings = get_settings()

# Database engine configuration
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
```

### Database URL Examples
```python
# SQLite (Development)
DATABASE_URL="sqlite:///./app.db"
DATABASE_URL="sqlite:///:memory:"  # In-memory for testing

# PostgreSQL (Production)
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
DATABASE_URL="postgresql://user:password@host:port/dbname?sslmode=require"

# MySQL
DATABASE_URL="mysql://user:password@localhost:3306/dbname"
DATABASE_URL="mysql+pymysql://user:password@localhost:3306/dbname"

# SQL Server
DATABASE_URL="mssql+pyodbc://user:password@server/dbname?driver=ODBC+Driver+17+for+SQL+Server"
```

## 🔒 Security Configuration

### JWT Configuration
```python
# config/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.settings import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### CORS Configuration
```python
# config/cors.py
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings

settings = get_settings()

def get_cors_middleware():
    """Get CORS middleware configuration."""
    return CORSMiddleware(
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
```

## 📝 Environment Files

### `.env.sample` - Template File
```bash
# Application Configuration
APP_NAME="FasCraft API"
APP_VERSION="1.0.0"
DEBUG=true
ENVIRONMENT="development"

# Server Configuration
HOST="0.0.0.0"
PORT=8000
RELOAD=true

# Database Configuration
DATABASE_URL="sqlite:///./app.db"
DATABASE_ECHO=false

# Security Configuration
SECRET_KEY="change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
CORS_ALLOW_CREDENTIALS=true

# Logging Configuration
LOG_LEVEL="INFO"
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# External Services
REDIS_URL="redis://localhost:6379"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
```

### `.env` - Local Development
```bash
# Copy from .env.sample and customize
cp .env.sample .env

# Edit .env with your local values
DEBUG=true
ENVIRONMENT="development"
DATABASE_URL="sqlite:///./dev.db"
SECRET_KEY="dev-secret-key"
```

### `.env.production` - Production
```bash
# Production environment variables
DEBUG=false
ENVIRONMENT="production"
DATABASE_URL="postgresql://user:pass@prod-host:5432/prod-db"
SECRET_KEY="production-secret-key-from-secrets-manager"
CORS_ORIGINS=["https://myapp.com","https://api.myapp.com"]
```

## 🚀 Environment-Specific Configuration

### Development Environment
```python
# config/environments/development.py
from config.settings import Settings

class DevelopmentSettings(Settings):
    debug: bool = True
    environment: str = "development"
    database_url: str = "sqlite:///./dev.db"
    log_level: str = "DEBUG"
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
```

### Production Environment
```python
# config/environments/production.py
from config.settings import Settings

class ProductionSettings(Settings):
    debug: bool = False
    environment: str = "production"
    database_url: str = "postgresql://user:pass@host:5432/db"
    log_level: str = "WARNING"
    cors_origins: list = ["https://myapp.com"]
    
    class Config:
        env_file = ".env.production"
```

### Environment Factory
```python
# config/environments/__init__.py
import os
from config.environments.development import DevelopmentSettings
from config.environments.production import ProductionSettings
from config.settings import Settings

def get_environment_settings() -> Settings:
    """Get settings based on environment."""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "development":
        return DevelopmentSettings()
    else:
        return Settings()
```

## 🔧 Configuration Usage

### In Main Application
```python
# main.py
from fastapi import FastAPI
from config.settings import get_settings
from config.database import init_db
from config.cors import get_cors_middleware

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(get_cors_middleware())

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
from routers.base import router as base_router
app.include_router(base_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
```

### In Modules
```python
# users/services.py
from config.database import get_db
from config.settings import get_settings

settings = get_settings()

class UserService:
    def __init__(self, db):
        self.db = db
        self.default_limit = 100
    
    def get_users(self, skip: int = 0, limit: int = None):
        if limit is None:
            limit = self.default_limit
        return self.db.query(UserModel).offset(skip).limit(limit).all()
```

## 🐳 Docker Configuration

### Environment Variables in Docker
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set default environment
ENV ENVIRONMENT=production
ENV DEBUG=false

EXPOSE 8000
CMD ["python", "main.py"]
```

### Docker Compose Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
      - DATABASE_URL=sqlite:///./dev.db
    volumes:
      - .:/app
    profiles:
      - development
  
  api-prod:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - DATABASE_URL=postgresql://user:pass@db:5432/prod
    depends_on:
      - db
    profiles:
      - production
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=prod
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    profiles:
      - production

volumes:
  postgres_data:
```

## 🔍 Configuration Validation

### Settings Validation
```python
# config/validation.py
from pydantic import validator
from config.settings import Settings

class ValidatedSettings(Settings):
    @validator('database_url')
    def validate_database_url(cls, v):
        if not v:
            raise ValueError('Database URL cannot be empty')
        if v.startswith('sqlite://') and 'memory' not in v:
            # Ensure SQLite file path is valid
            import os
            db_path = v.replace('sqlite:///', '')
            if db_path and not os.path.exists(os.path.dirname(db_path)):
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return v
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters long')
        return v
    
    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
```

### Configuration Testing
```python
# tests/test_config.py
import pytest
from config.settings import get_settings
from config.database import get_db, init_db

def test_settings_loading():
    """Test that settings load correctly."""
    settings = get_settings()
    assert settings.app_name is not None
    assert settings.port > 0
    assert settings.port <= 65535

def test_database_connection():
    """Test database connection."""
    db = next(get_db())
    assert db is not None
    db.close()

def test_environment_variables():
    """Test environment variable override."""
    import os
    os.environ['APP_NAME'] = 'Test API'
    os.environ['DEBUG'] = 'true'
    
    settings = get_settings()
    assert settings.app_name == 'Test API'
    assert settings.debug is True
```

## 🎯 Best Practices

### Security
- **Never commit `.env` files** to version control
- **Use strong, unique secret keys** for each environment
- **Rotate secrets regularly** in production
- **Use environment variables** for sensitive data
- **Validate configuration** at startup

### Environment Management
- **Use `.env.sample`** as a template
- **Document all configuration options** with examples
- **Use different files** for different environments
- **Validate configuration** before application startup
- **Provide sensible defaults** for development

### Configuration Organization
- **Centralize configuration** in the `config/` module
- **Use Pydantic** for type safety and validation
- **Separate concerns** (database, security, logging)
- **Use dependency injection** for configuration access
- **Cache settings** with `@lru_cache`

### Production Considerations
- **Use secrets management** for sensitive data
- **Validate all configuration** at startup
- **Use environment-specific** configuration files
- **Monitor configuration changes** in production
- **Backup configuration** and environment files

## 🔍 Troubleshooting

### Common Issues

**Configuration not loading:**
```bash
# Check environment file
ls -la .env*

# Verify environment variable
echo $ENVIRONMENT

# Check file permissions
ls -la .env
```

**Database connection errors:**
```bash
# Test database URL
python -c "from config.database import engine; print('OK')"

# Check database service
docker ps | grep postgres

# Verify credentials
echo $DATABASE_URL
```

**Secret key issues:**
```bash
# Check secret key length
echo $SECRET_KEY | wc -c

# Verify secret key format
echo $SECRET_KEY | head -c 10
```

## 📚 Next Steps

After configuring your application:

1. **Set up environment files** for different environments
2. **Configure database connections** for your use case
3. **Set up security settings** (JWT, CORS, etc.)
4. **Test configuration** in different environments
5. **Deploy with proper configuration** management

## 🎉 Success Checklist

- [ ] Configuration files created and organized
- [ ] Environment variables properly set
- [ ] Database configuration working
- [ ] Security settings configured
- [ ] CORS policy defined
- [ ] Environment-specific configs created
- [ ] Configuration validation working
- [ ] Docker environment configured

---

**Your configuration is now properly managed! 🚀**

The robust configuration system provides flexibility for different environments while maintaining security and best practices. Use environment variables for sensitive data, validate configuration at startup, and deploy with confidence across different environments.
