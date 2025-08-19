# Project Generation Guide

Learn how to create new FastAPI projects using FasCraft's `new` command. This guide covers everything from basic project creation to advanced configuration options.

## 🚀 Overview

The `fascraft new` command creates a complete, production-ready FastAPI project with:
- Clean Domain-Driven Architecture (DDA) structure
- Professional configuration management
- CI/CD pipeline setup
- Docker containerization
- Development and production dependencies

## 📋 Basic Usage

### Simple Project Creation
```bash
# Create a new project in current directory
fascraft new my-project

# Create with custom path
fascraft new my-project --path /custom/path

# Create in specific directory
fascraft new my-project --path ./projects/
```

### Command Options
```bash
fascraft new --help
```

Available options:
- `--path`: Specify custom project path
- `--help`: Show help message

## 🏗️ What Gets Created

### Project Structure
```
my-project/
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── settings.py         # App settings and environment
│   ├── database.py         # Database configuration
│   ├── exceptions.py       # Custom exception handling
│   └── middleware.py       # Custom middleware
├── routers/                # Router structure
│   ├── __init__.py
│   └── base.py            # Base router for module management
├── .github/                # CI/CD workflows
│   └── workflows/
│       ├── ci.yml         # GitHub Actions CI pipeline
│       └── dependency-update.yml
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Production dependencies
├── requirements.dev.txt    # Development dependencies
├── requirements.prod.txt   # Production dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service orchestration
├── fascraft.toml          # FasCraft project configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🔧 Configuration Files Explained

### `fascraft.toml`
Project-specific FasCraft configuration:
```toml
[project]
name = "my-project"
description = "A FastAPI project generated with FasCraft"
version = "0.1.0"
python_version = "3.10"

[templates]
source = "fascraft/templates/new_project"
```

### `requirements.txt`
Core production dependencies:
```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
```

### `requirements.dev.txt`
Development and testing dependencies:
```txt
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
ruff>=0.1.0
flake8>=6.0.0
```

### `requirements.prod.txt`
Production deployment dependencies:
```txt
gunicorn>=21.0.0
uvicorn[standard]>=0.24.0
```

## 🐳 Docker Configuration

### `Dockerfile`
Multi-stage production Docker image:
```dockerfile
# Build stage
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

### `docker-compose.yml`
Multi-service orchestration:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
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
    profiles:
      - production
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### `ci.yml` - Continuous Integration
- **Testing:** Multiple Python versions (3.10, 3.11, 3.12)
- **Code Quality:** Black, Ruff, isort, Flake8
- **Security:** Bandit, Safety
- **Build:** Docker image creation
- **Deployment:** Staging and production environments

#### `dependency-update.yml` - Dependency Management
- **Automated Updates:** Weekly security updates
- **Manual Triggers:** Security, all, or major updates
- **Pull Requests:** Automatic PR creation for updates
- **Testing:** Validation after updates

## 🎯 Project Customization

### Modify Main Application
Edit `main.py` to customize your API:

```python
from fastapi import FastAPI
from config.settings import get_settings
from routers.base import router as base_router

app = FastAPI(
    title="My Custom API",
    description="A custom FastAPI application",
    version="1.0.0"
)

# Include base router
app.include_router(base_router, prefix="/api/v1")

# Add custom endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to My Custom API!"}

@app.get("/custom")
async def custom_endpoint():
    return {"feature": "Custom functionality"}
```

### Environment Configuration
Customize `config/settings.py`:

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "My Custom API"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
```

### Custom Middleware
Extend `config/middleware.py`:

```python
from fastapi import Request
import time

async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 🚀 Advanced Usage

### Custom Project Templates
Create custom project templates:

```bash
# Create custom template directory
mkdir -p ~/.fascraft/templates/custom

# Copy and modify template files
cp -r fascraft/templates/new_project/* ~/.fascraft/templates/custom/

# Use custom template
fascraft new my-project --template custom
```

### Project Variants
Generate different project types:

```bash
# Basic API project
fascraft new basic-api

# E-commerce project
fascraft new ecommerce-api

# Authentication project
fascraft new auth-api

# Database integration project
fascraft new database-api
```

## 🔍 Project Analysis

### Analyze Generated Project
```bash
cd my-project

# Get project insights
fascraft analyze

# Check dependencies
fascraft dependencies list

# Validate structure
fascraft validate
```

### Project Health Check
```bash
# Run tests
pytest

# Check code quality
black --check .
ruff check .

# Security scan
bandit -r .
```

## 🎯 Best Practices

### Project Naming
- Use descriptive, lowercase names
- Avoid special characters and spaces
- Use hyphens for multi-word names
- Examples: `user-management-api`, `ecommerce-service`

### Directory Structure
- Keep the clean DDA structure
- Don't add unnecessary folders upfront
- Use `fascraft generate` for domain modules
- Maintain separation of concerns

### Configuration Management
- Use environment variables for sensitive data
- Keep configuration centralized in `config/`
- Use `.env` files for local development
- Never commit secrets to version control

## 🔍 Troubleshooting

### Common Issues

**Project creation fails:**
```bash
# Check permissions
ls -la /target/directory

# Verify FasCraft installation
fascraft --version

# Check available disk space
df -h
```

**Template rendering errors:**
```bash
# Verify template files
ls -la fascraft/templates/new_project/

# Check Jinja2 installation
pip show jinja2
```

**Dependency installation issues:**
```bash
# Update pip
pip install --upgrade pip

# Clear cache
pip cache purge

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 📚 Next Steps

After creating your project:

1. **Read the README** - Understand the generated structure
2. **Install Dependencies** - Set up your development environment
3. **Run the Application** - Verify everything works
4. **Add Modules** - Use `fascraft generate` for functionality
5. **Customize** - Modify endpoints and configuration
6. **Deploy** - Use Docker and CI/CD pipeline

## 🎉 Success Checklist

- [ ] Project created successfully
- [ ] All files and directories present
- [ ] Dependencies installed without errors
- [ ] Application runs on localhost:8000
- [ ] API documentation accessible
- [ ] Docker build successful
- [ ] CI/CD workflows configured

---

**Your FastAPI project is now ready for development! 🚀**

The clean, professional structure you've created provides a solid foundation for building scalable applications. Use `fascraft generate` to add modules as your needs grow, and deploy with confidence using the included CI/CD and Docker configuration.
