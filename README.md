# FasCraft 🚀

[![PyPI version](https://badge.fury.io/py/fascraft.svg)](https://badge.fury.io/py/fascraft)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FasCraft** is a powerful CLI tool designed to streamline the creation and management of modular FastAPI projects. It eliminates boilerplate code and enforces best practices from the start, allowing developers to focus on business logic.

## **✨ Features**

- **🚀 Project Generation** - Create new FastAPI projects with domain-driven architecture
- **🔧 Module Management** - Generate, list, update, and remove domain modules
- **🏗️ Domain-Driven Design** - Self-contained modules with models, schemas, services, and routers
- **⚙️ Smart Configuration** - Automatic project detection and configuration management
- **🛡️ Safety First** - Confirmations, backups, and rollback capabilities
- **🎨 Rich CLI** - Beautiful tables, color coding, and progress indicators
- **🧪 Production Ready** - Comprehensive testing and error handling
- **🌍 Environment Management** - Complete .env templates with database configurations
- **📦 Dependency Management** - Production-ready requirements files for development and production
- **🗄️ Database Support** - MongoDB, PostgreSQL, MySQL, and SQLite configurations
- **⚡ Service Integration** - Redis, Celery, JWT, and CORS configurations
- **🔍 Project Analysis** - Analyze existing projects and suggest improvements
- **🚀 Migration Tools** - Convert legacy projects to domain-driven architecture
- **⚙️ Configuration Management** - Project-specific FasCraft settings via `.fascraft.toml`
- **🔄 Base Router Architecture** - Centralized router management for all modules
- **📝 Git Integration** - Automatic `.gitignore` file generation for new projects

## **🚀 Quick Start**

### **Installation**

```bash
# Install from PyPI
pip install fascraft

# Or install from source
git clone https://github.com/LexxLuey/fascraft.git
cd fascraft
poetry install
```

**Note:** FasCraft itself uses Poetry for development, but the projects it generates support both Poetry and pip!

### **Create Your First Project**

```bash
# Generate a new FastAPI project
fascraft new my-awesome-api

# Navigate to your project
cd my-awesome-api

# Install dependencies (choose your preferred method)
# Option 1: Using Poetry (recommended)
poetry install

# Option 2: Using pip
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload
```

**💡 Pro Tip:** Your generated project includes both Poetry and pip configurations, so you can use whichever dependency manager you prefer!

**⚠️ Important:** You must install dependencies before running the FastAPI server. The generated project structure is ready, but dependencies need to be installed first.

### **Add Domain Modules**

```bash
# Generate a customers module
fascraft generate customers

# Generate a products module
fascraft generate products

# Your project now has:
# ├── customers/
# │   ├── models.py
# │   ├── schemas.py
# │   ├── services.py
# │   ├── routers.py
# │   └── tests/
# └── products/
#     ├── models.py
#     ├── schemas.py
#     ├── services.py
#     ├── routers.py
#     └── tests/
```

### **Advanced Project Management**

```bash
# Analyze your project structure and get recommendations
fascraft analyze

# Migrate legacy projects to domain-driven architecture
fascraft migrate

# Manage project configuration
fascraft config show
fascraft config create
fascraft config update project.name "new-name"
fascraft config validate
```

## **🏗️ Architecture & Stability**

FasCraft is built on a **stable, well-designed architecture** that prioritizes reliability and maintainability:

- **🔒 Stable Core**: The CLI architecture and template system are designed to last
- **🏛️ Modular Design**: Clean separation of concerns with extensible command structure
- **🔄 Base Router System**: Centralized router management for consistent API structure
- **📁 Domain-Driven**: Self-contained modules with clear boundaries
- **⚙️ Configuration First**: Project-specific settings via `.fascraft.toml`
- **🧪 Comprehensive Testing**: 100% test coverage ensures reliability
- **📝 Git Ready**: Automatic `.gitignore` generation for immediate version control

**Our commitment**: New features extend the existing architecture rather than replacing it, ensuring your projects remain stable and maintainable.

## **🚀 Complete Workflow Example**

Here's the complete workflow from project creation to running your API:

```bash
# 1. Create new project
fascraft new my-ecommerce-api

# 2. Navigate to project directory
cd my-ecommerce-api

# 3. Install dependencies (choose one)
poetry install                    # Poetry (recommended)
# OR
pip install -r requirements.txt   # pip

# 4. Start development server
uvicorn main:app --reload

# 5. Add domain modules as needed
fascraft generate products
fascraft generate orders

# 6. Analyze your project structure
fascraft analyze

# 7. Manage project configuration
fascraft config show
```

## **📚 Available Commands**

### **Project Management**
```bash
fascraft new <project_name>          # Create new FastAPI project
fascraft generate <module_name>      # Add new domain module
```

### **Advanced Project Management (Phase 3)**
```bash
fascraft analyze [path]              # Analyze project structure and get recommendations
fascraft migrate [path]              # Convert legacy projects to domain-driven architecture
fascraft config <action> [path]      # Manage project configuration (.fascraft.toml)
```

### **Module Management**
```bash
fascraft list                        # List all modules with health status
fascraft remove <module_name>        # Remove module with safety confirmations
fascraft update <module_name>        # Update module templates with backups
```

### **Utility Commands**
```bash
fascraft hello [name]                # Say hello
fascraft version                     # Show version
fascraft --help                      # Show all available commands
```

## **🏗️ Project Structure**

FasCraft generates projects with a clean, domain-driven architecture and centralized router management:

```
my-awesome-api/
├── config/                           # Configuration and shared utilities
│   ├── __init__.py
│   ├── settings.py                   # Pydantic settings with environment support
│   ├── database.py                   # SQLAlchemy configuration
│   ├── exceptions.py                 # Custom HTTP exceptions
│   └── middleware.py                 # CORS and timing middleware
├── routers/                          # Centralized router management
│   ├── __init__.py
│   └── base.py                       # Base router with common prefix (/api/v1)
├── customers/                        # Domain module (self-contained)
│   ├── __init__.py
│   ├── models.py                     # SQLAlchemy models
│   ├── schemas.py                    # Pydantic schemas
│   ├── services.py                   # Business logic
│   ├── routers.py                    # FastAPI routes (no hardcoded prefix)
│   └── tests/                        # Module-specific tests
├── products/                         # Another domain module
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   ├── routers.py
│   └── tests/
├── main.py                           # FastAPI application entry point
├── pyproject.toml                    # Poetry configuration with all dependencies
├── .env                              # Environment configuration (database, Redis, etc.)
├── .env.sample                       # Sample environment file
├── requirements.txt                  # Core dependencies (pip)
├── requirements.dev.txt              # Development dependencies (pip)
├── requirements.prod.txt             # Production dependencies (pip)
├── .gitignore                        # Git ignore file (automatically generated)
├── fascraft.toml                     # FasCraft project configuration
└── README.md                         # Project documentation
```

## **🌍 Environment & Dependency Management**

FasCraft generates comprehensive environment and dependency files for production-ready applications:

### **Environment Configuration**
- **`.env`** - Configure your environment like a true 12 factor app that it is.
- **`.env.sample`** - Template for team collaboration. Complete environment configuration with database connections
- **Database Support** - MongoDB, PostgreSQL, MySQL, SQLite configurations
- **Service Integration** - Redis, Celery, JWT, CORS settings
- **Production Ready** - Optimized for different deployment environments

### **Dependency Management**
FasCraft generates projects with **dual dependency management** - you can use either Poetry or pip!

- **`pyproject.toml`** - Complete Poetry configuration with all dependencies and development tools
- **`requirements.txt`** - Core production dependencies for pip users
- **`requirements.dev.txt`** - Development tools and testing frameworks for pip users
- **`requirements.prod.txt`** - Production-optimized dependencies with Gunicorn for pip users

### **Quick Setup**

**Option 1: Using Poetry (Recommended)**
```bash
# Install all dependencies (production + development)
poetry install

# Install only production dependencies
poetry install --only main

# Install with specific groups
poetry install --with dev,prod
```

**Option 2: Using pip**
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.dev.txt

# Install production dependencies
pip install -r requirements.prod.txt
```

## **📦 Dual Dependency Management**

FasCraft generates projects with **both Poetry and pip support**, giving you the flexibility to choose your preferred dependency manager:

### **🎯 Poetry Configuration (`pyproject.toml`)**
- **Complete dependency management** with version pinning
- **Development tools** (pytest, black, ruff, mypy, etc.)
- **Production dependencies** (Gunicorn, database drivers, etc.)
- **Group-based installation** (main, dev, prod)
- **Lock file** for reproducible builds

### **🔧 pip Configuration (requirements files)**
- **`requirements.txt`** - Core production dependencies
- **`requirements.dev.txt`** - Development and testing tools
- **`requirements.prod.txt`** - Production-optimized with Gunicorn
- **Simple installation** with standard pip commands
- **Easy deployment** to environments without Poetry

### **🚀 Why Both?**
- **Team flexibility** - Some developers prefer Poetry, others prefer pip
- **Deployment options** - CI/CD pipelines often work better with requirements files
- **Learning curve** - New developers can start with pip, graduate to Poetry
- **Production ready** - Both approaches are production-tested

## **🔧 Module Management**

### **List Modules**
```bash
fascraft list
```
Shows a beautiful table with:
- Module health status (✅ Healthy / ⚠️ Incomplete)
- File counts and test coverage
- Module size and last modified date

## **🚀 Advanced Project Management**

FasCraft now includes powerful tools for analyzing, migrating, and configuring existing FastAPI projects:

### **🔍 Project Analysis (`fascraft analyze`)**

Analyze your project structure and get intelligent recommendations:

```bash
# Analyze current directory
fascraft analyze

# Analyze specific project
fascraft analyze /path/to/project

# What you get:
# 📊 Project Overview - Structure analysis and module count
# 🏗️ Structure Analysis - Configuration and architecture assessment
# 💡 Recommendations - Specific improvements for your project
# 📦 Missing Components - What could be added for better structure
```

**Example Output:**
```
📊 Project Overview
┌─────────────────┬─────────┐
│ Property        │ Value   │
├─────────────────┼─────────┤
│ Project Name    │ my-api  │
│ Domain Modules  │ 3       │
│ Config Files    │ 2       │
│ Router Includes │ 5       │
└─────────────────┴─────────┘

💡 Recommendations
• Consider adding FasCraft configuration for better project management
• Use 'fascraft generate <module_name>' to create additional domain modules
```

### **🔄 Project Migration (`fascraft migrate`)**

Convert legacy FastAPI projects to modern domain-driven architecture:

```bash
# Migrate current directory
fascraft migrate

# Migrate with backup
fascraft migrate --backup

# What happens:
# 1. 🔍 Analysis - Detects current project structure
# 2. 💾 Backup - Creates timestamped backup (optional)
# 3. 🏗️ Restructure - Creates base router and domain modules
# 4. ⚙️ Configuration - Generates fascraft.toml
# 5. 📝 Summary - Shows what was migrated
```

**Migration Features:**
- **Flat Structure Detection** - Identifies projects with separate `models/`, `schemas/`, `routers/` directories
- **Automatic Restructuring** - Converts to domain-driven modules
- **Base Router Creation** - Implements centralized router management
- **Configuration Generation** - Creates project-specific settings

### **⚙️ Configuration Management (`fascraft config`)**

Manage your project's FasCraft configuration:

```bash
# Show current configuration
fascraft config show

# Create new configuration
fascraft config create

# Update specific settings
fascraft config update project.name "new-name"
fascraft config update router.base_prefix "/api/v2"

# Validate configuration
fascraft config validate
```

**Configuration Sections:**
```toml
[project]
name = "my-api"
version = "0.1.0"

[router]
base_prefix = "/api/v1"
health_endpoint = true

[database]
type = "postgresql"
pool_size = 20

[modules]
auto_include = true
prefix_strategy = "plural"
```

## **🔄 Base Router Architecture**

FasCraft now implements a **centralized router system** that provides:

- **Consistent API Structure** - All endpoints use `/api/v1` prefix
- **Automatic Module Integration** - New modules are automatically added to the base router
- **Health Check Endpoint** - Built-in `/api/v1/health` endpoint
- **Clean Module Routers** - Individual module routers focus on business logic, not URL structure

**How It Works:**
1. **Base Router** (`/routers/base.py`) manages all module routers
2. **Module Routers** contain only business logic, no hardcoded prefixes
3. **Automatic Integration** - `fascraft generate` automatically updates the base router
4. **Consistent Structure** - All endpoints follow the same pattern

**Example API Structure:**
```
/api/v1/health                    # Health check
/api/v1/customers                # Customer endpoints
/api/v1/products                 # Product endpoints
/api/v1/orders                   # Order endpoints
```

## **💡 Practical Examples**

### **Getting Started with Poetry**
```bash
# Create and navigate to your project
fascraft new my-api
cd my-api

# Install dependencies
poetry install

# Start development server
uvicorn main:app --reload
```

### **Complete Development Workflow**
```bash
# 1. Create project
fascraft new ecommerce-api
cd ecommerce-api

# 2. Install dependencies
poetry install

# 3. Generate domain modules
fascraft generate users
fascraft generate products
fascraft generate orders

# 4. Analyze project structure
fascraft analyze

# 5. Customize configuration
fascraft config update project.name "E-Commerce API"
fascraft config update router.base_prefix "/api/v2"

# 6. Start development
uvicorn main:app --reload
```

### **Migrating Legacy Projects**
```bash
# Navigate to existing FastAPI project
cd /path/to/legacy-project

# Analyze current structure
fascraft analyze

# Migrate to domain-driven architecture
fascraft migrate --backup

# Verify migration
fascraft analyze
```

### **Module Management**
```bash
# List all modules with health status
fascraft list

# Remove a module (with confirmation)
fascraft remove old-module

# Update module templates
fascraft update users
```

## **🔧 Configuration Reference**

### **Environment Variables**
FasCraft generates comprehensive environment configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/dbname
DATABASE_POOL_SIZE=20

# Redis Configuration
REDIS_URL=redis://localhost:6379

# JWT Configuration
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]
```

### **FasCraft Configuration (.fascraft.toml)**
```toml
[project]
name = "my-api"
version = "0.1.0"
description = "A FastAPI project generated with FasCraft"

[router]
base_prefix = "/api/v1"
health_endpoint = true
auto_include_modules = true

[database]
type = "postgresql"
pool_size = 20
echo_queries = false

[modules]
prefix_strategy = "plural"
auto_generate_tests = true

[development]
debug = true
reload = true
host = "0.0.0.0"
port = 8000

[production]
debug = false
reload = false
workers = 4
```

## **🎯 Use Cases**

- **🚀 Rapid Prototyping** - Get a production-ready API structure in seconds
- **🏢 Enterprise Applications** - Consistent architecture across teams
- **📚 Learning FastAPI** - Best practices built into every template
- **🔄 Legacy Migration** - Convert existing projects to domain-driven design
- **👥 Team Onboarding** - Standardized project structure for new developers

## **🛠️ Development**

### **Prerequisites**
- Python 3.8+
- Poetry (for dependency management) - **Optional for generated projects**
- FastAPI knowledge (for customizing generated code)

### **Setup Development Environment**
```bash
git clone https://github.com/LexxLuey/fascraft.git
cd fascraft
poetry install
poetry run pytest  # Run all tests
```

### **Running Tests**
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=fascraft

# Run specific test file
poetry run pytest tests/test_generate_command.py
```

## **📖 Documentation**

- **[ROADMAP.md](ROADMAP.md)** - Development phases and current status (Phase 3: Advanced Project Detection next)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to FasCraft
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## **🤝 Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## **📄 License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **🙏 Acknowledgments**

- **FastAPI** - The amazing web framework that makes this possible
- **Typer** - Beautiful CLI framework
- **Rich** - Rich text and beautiful formatting
- **Jinja2** - Powerful templating engine

---

**Made with ❤️ for the FastAPI community**
