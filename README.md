# FastForge 🚀

**FastForge** is a powerful CLI tool designed to streamline the creation and management of modular FastAPI projects. It eliminates boilerplate code and enforces best practices from the start, allowing developers to focus on business logic.

## **✨ Features**

- **🚀 Project Generation** - Create new FastAPI projects with domain-driven architecture
- **🔧 Module Management** - Generate, list, update, and remove domain modules
- **🏗️ Domain-Driven Design** - Self-contained modules with models, schemas, services, and routers
- **⚙️ Smart Configuration** - Automatic project detection and configuration management
- **🛡️ Safety First** - Confirmations, backups, and rollback capabilities
- **🎨 Rich CLI** - Beautiful tables, color coding, and progress indicators
- **🧪 Production Ready** - Comprehensive testing and error handling

## **🚀 Quick Start**

### **Installation**

```bash
# Install from PyPI
pip install fastforge

# Or install from source
git clone https://github.com/yourusername/fastforge.git
cd fastforge
poetry install
```

### **Create Your First Project**

```bash
# Generate a new FastAPI project
fastforge new my-awesome-api

# Navigate to your project
cd my-awesome-api

# Start the development server
uvicorn main:app --reload
```

### **Add Domain Modules**

```bash
# Generate a customers module
fastforge generate customers

# Generate a products module
fastforge generate products

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
fastforge new <project_name>          # Create new FastAPI project
fastforge generate <module_name>      # Add new domain module
```

### **Module Management**
```bash
fastforge list                        # List all modules with health status
fastforge remove <module_name>        # Remove module with safety confirmations
fastforge update <module_name>        # Update module templates with backups
```

### **Utility Commands**
```bash
fastforge hello [name]                # Say hello
fastforge version                     # Show version
fastforge --help                      # Show all available commands
```

## **🏗️ Project Structure**

FastForge generates projects with a clean, domain-driven architecture:

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
└── README.md                         # Project documentation
```

## **🔧 Module Management**

### **List Modules**
```bash
fastforge list
```
Shows a beautiful table with:
- Module health status (✅ Healthy / ⚠️ Incomplete)
- File counts and test coverage
- Module size and last modified date

### **Remove Modules**
```bash
fastforge remove customers
```
- Shows removal preview with file counts and size
- Asks for confirmation (use `--force` to skip)
- Automatically cleans up main.py references
- Cannot be undone (safety first!)

### **Update Modules**
```bash
fastforge update customers
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
git clone https://github.com/yourusername/fastforge.git
cd fastforge
poetry install
poetry run pytest  # Run all tests
```

### **Running Tests**
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=fastforge

# Run specific test file
poetry run pytest tests/test_generate_command.py
```

## **📖 Documentation**

- **[ROADMAP.md](ROADMAP.md)** - Development phases and current status
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to FastForge
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
