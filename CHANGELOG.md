# Changelog

All notable changes to FastCraft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Phase 3: Advanced Project Detection
- Migration support for existing projects
- Project structure analysis and recommendations
- Configuration file support (`.fastcraft.toml`)
- Project setup wizards for existing codebases

## [0.2.0] - 2024-12-19

### Added
- **Environment & Dependency Management** 🌍📦
  - Complete `.env` templates with database configurations (MongoDB, PostgreSQL, MySQL, SQLite)
  - `.env.sample` files for team collaboration
  - `requirements.txt` for core production dependencies
  - `requirements.dev.txt` for development tools and testing frameworks
  - `requirements.prod.txt` for production-optimized dependencies with Gunicorn
  - Redis and Celery configuration templates
  - JWT authentication and CORS configuration
  - Comprehensive logging and monitoring setup

- **Enhanced Project Generation**
  - Production-ready project structure with environment management
  - Database service configurations with default ports
  - Service integration templates (Redis, Celery, JWT, CORS)
  - Updated installation instructions using pip instead of poetry
  - Enhanced README templates with new file documentation

### Changed
- **Dependency Management**
  - Switched from poetry to pip-based dependency management
  - Updated all templates to use pip install commands
  - Enhanced README.md templates with new installation options
  - Updated success messages to reflect new file creation

- **Template System**
  - Added new environment and requirements file templates
  - Updated project generation to include all new files
  - Enhanced success messages and user guidance

### Technical Improvements
- **Code Quality**
  - Added comprehensive tests for new file generation
  - Updated test expectations to match new functionality
  - Enhanced template validation and testing
  - Improved user feedback and success messages

## [0.2.0] - 2024-12-19

### Added
- **Complete Module Management System** 🎉
  - `fastcraft list` command to display all domain modules with health status
  - `fastcraft remove <module_name>` command to safely remove modules
  - `fastcraft update <module_name>` command to update module templates
  - Rich CLI output with tables, color coding, and progress indicators
  - Automatic backup creation before updates with rollback capability
  - Safety confirmations for destructive operations
  - Automatic cleanup of main.py references after module removal

- **Enhanced Project Structure**
  - Domain-driven architecture with self-contained modules
  - Each module contains: models.py, schemas.py, services.py, routers.py, tests/
  - Config directory with settings.py, database.py, exceptions.py, middleware.py
  - Pydantic settings with environment variable support
  - Custom HTTP exception classes
  - CORS and timing middleware

- **Smart Project Detection**
  - Works with any existing FastAPI project
  - Automatically creates missing config structure
  - Validates project structure and module health
  - Cross-platform compatibility (Windows, macOS, Linux)

- **Comprehensive Testing**
  - 95 tests passing with 100% coverage for new features
  - Unit tests for all command functions
  - Integration tests for CLI commands
  - Mock-based tests for external dependencies
  - Error handling tests for edge cases

### Changed
- **Architecture Overhaul**
  - Replaced top-level modular structure with domain-driven design
  - Updated new project templates to use config/ directory
  - Modified main.py to use settings and middleware from config
  - Enhanced error handling with typer.Exit and rich console output

- **Template System**
  - New domain module templates with production-ready code
  - SQLAlchemy models with proper relationships
  - Pydantic schemas with validation
  - Service layer with business logic
  - FastAPI routers with CRUD endpoints
  - Comprehensive test templates

### Fixed
- **CLI Integration**
  - Fixed argument parsing for hello command
  - Improved error handling and user feedback
  - Better validation of module names and project paths
  - Consistent exit codes and error messages

- **Template Rendering**
  - Fixed variable substitution in main.py templates
  - Improved Jinja2 template organization
  - Better handling of optional template variables

### Technical Improvements
- **Code Quality**
  - Added type hints throughout the codebase
  - Improved error handling with specific exception types
  - Better separation of concerns between commands
  - Consistent use of pathlib.Path for file operations

- **Performance**
  - Efficient file system operations
  - Optimized template rendering
  - Smart caching of project detection results

## [0.1.0] - 2024-12-18

### Added
- **Initial FastCraft CLI** 🚀
  - `fastcraft new <project_name>` command to create new FastAPI projects
  - `fastcraft generate <module_name>` command to add domain modules
  - `fastcraft hello [name]` command for testing
  - `fastcraft version` command to show version

- **Project Generation**
  - Complete FastAPI project structure
  - Jinja2 template system for customizable generation
  - pyproject.toml with all necessary dependencies
  - README.md with project setup instructions
  - Basic FastAPI application with health check endpoints

- **Core Infrastructure**
  - Typer-based CLI framework
  - Rich console output for better user experience
  - Comprehensive test suite with pytest
  - Poetry for dependency management
  - Cross-platform compatibility

### Technical Features
- **Template System**
  - Modular template organization
  - Variable substitution for project names
  - Consistent file structure generation
  - Production-ready code templates

- **Testing**
  - 100% test coverage for core functionality
  - Unit tests for all commands
  - Integration tests for CLI
  - Template validation tests

---

## **Contributors**

### **Phase 2 (v0.2.0)**
- **Core Development**: Complete module management system
- **Architecture**: Domain-driven design implementation
- **Testing**: Comprehensive test suite expansion
- **Documentation**: Complete documentation overhaul

### **Phase 1 (v0.1.0)**
- **Initial Development**: FastCraft CLI foundation
- **Project Generation**: New project creation system
- **Template System**: Jinja2 template infrastructure
- **Testing**: Initial test suite implementation

---

## **Version History**

- **v0.2.0** - Complete Module Management System ✅
- **v0.1.0** - Initial FastCraft CLI ✅

---

**FastCraft - Making FastAPI development faster and easier!** 🚀
