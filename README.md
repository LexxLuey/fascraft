# FastCraft 🚀

[![PyPI version](https://badge.fury.io/py/fastcraft.svg)](https://badge.fury.io/py/fastcraft)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FastCraft** is a powerful CLI tool designed to streamline the creation and management of modular FastAPI projects. It eliminates boilerplate code and enforces best practices from the start, allowing developers to focus on business logic.

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
pip install fastcraft

# Or install from source
git clone https://github.com/yourusername/fastcraft.git
cd fastcraft
poetry install
```

### **Create Your First Project**

```bash
# Generate a new FastAPI project
fastcraft new my-awesome-api

# Navigate to your project
cd my-awesome-api

# Start the development server
uvicorn main:app --reload
```

### **Add Domain Modules**

```bash
# Generate a customers module
fastcraft generate customers

# Generate a products module
fastcraft generate products

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

## **📚 Available Commands**

### **Project Management**
```bash
fastcraft new <project_name>          # Create new FastAPI project
fastcraft generate <module_name>      # Add new domain module
```

### **Module Management**
```bash
fastcraft list                        # List all modules with health status
fastcraft remove <module_name>        # Remove module with safety confirmations
fastcraft update <module_name>        # Update module templates with backups
```

### **Utility Commands**
```bash
fastcraft hello [name]                # Say hello
fastcraft version                     # Show version
fastcraft --help                      # Show all available commands
```

## **🏗️ Project Structure**

FastCraft generates projects with a clean, domain-driven architecture:

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
├── pyproject.toml                    # Project dependencies and metadata
├── .env                              # Environment configuration (database, Redis, etc.)
├── .env.sample                       # Sample environment file
├── requirements.txt                  # Core dependencies
├── requirements.dev.txt              # Development dependencies
├── requirements.prod.txt             # Production dependencies
└── README.md                         # Project documentation
```

## **🌍 Environment & Dependency Management**

FastCraft generates comprehensive environment and dependency files for production-ready applications:

### **Environment Configuration**
- **`.env`** - Complete environment configuration with database connections
- **`.env.sample`** - Template for team collaboration
- **Database Support** - MongoDB, PostgreSQL, MySQL, SQLite configurations
- **Service Integration** - Redis, Celery, JWT, CORS settings
- **Production Ready** - Optimized for different deployment environments

### **Dependency Management**
- **`requirements.txt`** - Core dependencies for production
- **`requirements.dev.txt`** - Development tools and testing frameworks
- **`requirements.prod.txt`** - Production-optimized dependencies with Gunicorn

### **Quick Setup**
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.dev.txt

# Install production dependencies
pip install -r requirements.prod.txt
```

## **🔧 Module Management**

### **List Modules**
```bash
fastcraft list
```
Shows a beautiful table with:
- Module health status (✅ Healthy / ⚠️ Incomplete)
- File counts and test coverage
- Module size and last modified date

### **Remove Modules**
```bash
fastcraft remove customers
```
- Shows removal preview with file counts and size
- Asks for confirmation (use `--force` to skip)
- Automatically cleans up main.py references
- Cannot be undone (safety first!)

### **Update Modules**
```bash
fastcraft update customers
```
- Creates automatic backups before updating
- Refreshes all module templates
- Rollback capability if update fails
- Preserves your custom business logic

## **🎯 Use Cases**

- **🚀 Rapid Prototyping** - Get a production-ready API structure in seconds
- **🏢 Enterprise Applications** - Consistent architecture across teams
- **📚 Learning FastAPI** - Best practices built into every template
- **🔄 Legacy Migration** - Convert existing projects to domain-driven design
- **👥 Team Onboarding** - Standardized project structure for new developers

## **🛠️ Development**

### **Prerequisites**
- Python 3.8+
- Poetry (for dependency management)
- FastAPI knowledge (for customizing generated code)

### **Setup Development Environment**
```bash
git clone https://github.com/yourusername/fastcraft.git
cd fastcraft
poetry install
poetry run pytest  # Run all tests
```

### **Running Tests**
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=fastcraft

# Run specific test file
poetry run pytest tests/test_generate_command.py
```

## **📖 Documentation**

- **[ROADMAP.md](ROADMAP.md)** - Development phases and current status (Phase 3: Advanced Project Detection next)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to FastCraft
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
