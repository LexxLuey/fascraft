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
```

## **📚 Available Commands**

### **Project Management**
```bash
fascraft new <project_name>          # Create new FastAPI project
fascraft generate <module_name>      # Add new domain module
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

FasCraft generates projects with a clean, domain-driven architecture:

```
my-awesome-api/
├── config/                           # Configuration and shared utilities
│   ├── __init__.py
│   ├── settings.py                   # Pydantic settings with environment support
│   ├── database.py                   # SQLAlchemy configuration
│   ├── exceptions.py                 # Custom HTTP exceptions
│   └── middleware.py                 # CORS and timing middleware
├── customers/                        # Domain module (self-contained)
│   ├── __init__.py
│   ├── models.py                     # SQLAlchemy models
│   ├── schemas.py                    # Pydantic schemas
│   ├── services.py                   # Business logic
│   ├── routers.py                    # FastAPI routes
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

### **Remove Modules**
```bash
fascraft remove customers
```
- Shows removal preview with file counts and size
- Asks for confirmation (use `--force` to skip)
- Automatically cleans up main.py references
- Cannot be undone (safety first!)

### **Update Modules**
```bash
fascraft update customers
```
- Creates automatic backups before updating
- Refreshes all module templates
- Rollback capability if update fails
- Preserves your custom business logic

## **💡 Practical Examples**

### **Getting Started with Poetry**
```bash
# Create and navigate to your project
fascraft new my-api
cd my-api

# Install all dependencies (recommended for development)
poetry install

# Run your FastAPI app
poetry run uvicorn main:app --reload

# Add new dependencies
poetry add redis
poetry add --group dev pytest-cov
```

### **Getting Started with pip**
```bash
# Create and navigate to your project
fascraft new my-api
cd my-api

# Install core dependencies
pip install -r requirements.txt

# Install development tools (optional, for testing and development)
pip install -r requirements.dev.txt

# Run your FastAPI app
uvicorn main:app --reload

# Add new dependencies
pip install redis
pip install pytest-cov
```

### **Production Deployment**
```bash
# Using Poetry
poetry install --only main,prod
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using pip
pip install -r requirements.prod.txt
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
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
