# Contributing to FastCraft 🤝

Thank you for your interest in contributing to FastCraft! This guide will help you get started with development and contributing to the project.

## **🎯 Project Status**

**Current Phase: Phase 2.5 - Environment & Dependency Management** ✅ **COMPLETED**

FastCraft has successfully completed multiple phases:
- **Phase 1**: Module Templates and project generation ✅
- **Phase 2**: Complete module management system ✅
- **Phase 2.5**: Environment and dependency management ✅

**Next Phase: Phase 3 - Advanced Project Detection** 🔄

## **🚀 Quick Start for Contributors**

### **Prerequisites**
- Python 3.8 or higher
- Poetry (for dependency management)
- Git
- Basic knowledge of FastAPI, Typer, and Jinja2

### **Setup Development Environment**

```bash
# Clone the repository
git clone https://github.com/yourusername/fastcraft.git
cd fastcraft

# Install dependencies
poetry install

# Verify installation
poetry run fastcraft --help
poetry run pytest  # Run all tests
```

## **🏗️ Project Architecture**

FastCraft follows a clean, modular architecture:

```
fastcraft/
├── commands/                 # CLI command implementations
│   ├── __init__.py
│   ├── new.py               # Create new projects
│   ├── generate.py           # Generate domain modules
│   ├── list.py               # List existing modules
│   ├── remove.py             # Remove modules
│   └── update.py             # Update module templates
├── templates/                # Jinja2 templates
│   ├── new_project/          # New project templates (including env & requirements)
│   └── module/               # Domain module templates
├── main.py                   # CLI application entry point
└── tests/                    # Comprehensive test suite
```

## **🧪 Testing**

FastCraft maintains **100% test coverage** with a comprehensive test suite.

### **Running Tests**

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=fastcraft --cov-report=html

# Run specific test categories
poetry run pytest tests/test_new_command.py      # Project generation
poetry run pytest tests/test_generate_command.py # Module generation
poetry run pytest tests/test_list_command.py     # Module listing
poetry run pytest tests/test_remove_command.py   # Module removal
poetry run pytest tests/test_update_command.py   # Module updates
poetry run pytest tests/test_cli_integration.py  # CLI integration
```

### **Test Structure**

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test CLI commands end-to-end
- **Template Tests**: Validate Jinja2 template rendering
- **Mock Tests**: Test external dependencies safely
- **File Generation Tests**: Verify new environment and requirements files
- **Template Validation Tests**: Ensure all templates exist and are loadable

### **Writing Tests**

When adding new features, ensure you:

1. **Write unit tests** for all new functions
2. **Add integration tests** for new CLI commands
3. **Maintain 100% coverage** for new code
4. **Follow existing patterns** in the test suite

## **📝 Code Style and Standards**

### **Python Standards**
- **PEP 8** compliance
- **Type hints** for all function signatures
- **Docstrings** for all public functions
- **Snake_case** for variables and functions
- **PascalCase** for classes

### **CLI Standards**
- **Typer** for command definitions
- **Rich** for beautiful output formatting
- **Consistent error handling** with `typer.Exit`
- **Helpful error messages** with actionable guidance

### **Template Standards**
- **Jinja2** for all template rendering
- **Consistent variable naming** across templates
- **Production-ready code** in generated files
- **Best practices** built into every template

## **🔧 Development Workflow**

### **1. Create a Feature Branch**

```bash
git checkout -b feature/your-feature-name
```

### **2. Make Your Changes**

- Write your code following the style guidelines
- Add comprehensive tests
- Update documentation if needed

### **3. Run Tests**

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=fastcraft

# Fix any failing tests
```

### **4. Commit Your Changes**

```bash
git add .
git commit -m "feat: add your feature description

- Detailed description of changes
- Any breaking changes
- Related issue numbers"
```

### **5. Push and Create Pull Request**

```bash
git push origin feature/your-feature-name
# Create PR on GitHub
```

## **🎯 Current Development Priorities**

### **Phase 3: Advanced Project Detection** (Next)
- [ ] Migration support for old modular projects
- [ ] Project structure analysis and recommendations
- [ ] Configuration file support (`.fastcraft.toml`)
- [ ] Environment detection (dev vs production)

### **Areas Needing Contributors**
- **Project Analysis**: Detect and analyze existing FastAPI projects
- **Migration Tools**: Convert old projects to domain-driven architecture
- **Configuration Management**: Project-specific settings and overrides
- **Documentation**: User guides and API documentation

## **🐛 Bug Reports and Feature Requests**

### **Bug Reports**
When reporting bugs, please include:

1. **FastCraft version**: `fastcraft version`
2. **Python version**: `python --version`
3. **Operating system**: Windows/macOS/Linux
4. **Steps to reproduce**: Clear, step-by-step instructions
5. **Expected vs actual behavior**: What you expected vs what happened
6. **Error messages**: Full error output and stack traces

### **Feature Requests**
For new features, please describe:

1. **Use case**: What problem does this solve?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: What other approaches were considered?
4. **Impact**: How will this benefit users?

## **📚 Learning Resources**

### **FastCraft Internals**
- **Commands**: Study `fastcraft/commands/` for command patterns
- **Templates**: Review `fastcraft/templates/` for template structure
- **Tests**: Examine `tests/` for testing patterns and examples

### **Technologies Used**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Web framework for APIs
- **[Typer](https://typer.tiangolo.com/)**: CLI framework
- **[Rich](https://rich.readthedocs.io/)**: Rich text and formatting
- **[Jinja2](https://jinja.palletsprojects.com/)**: Template engine
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Data validation

## **🤝 Community Guidelines**

- **Be respectful** and inclusive
- **Help newcomers** get started
- **Share knowledge** and best practices
- **Provide constructive feedback** on contributions
- **Celebrate successes** and contributions

## **📞 Getting Help**

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions
- **Documentation**: Check README.md and ROADMAP.md first

## **🎉 Recognition**

Contributors are recognized in:
- **README.md** contributors section
- **Release notes** for each version
- **GitHub contributors** page
- **Project documentation**

---

**Thank you for contributing to FastCraft! Together, we're making FastAPI development faster and easier for everyone.** 🚀
