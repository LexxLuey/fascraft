# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2025-08-17

### 🚀 **Phase 3: Advanced Project Detection & Management - COMPLETED**

#### **Added**
- **Project Analysis Command** (`fascraft analyze`)
  - Intelligent project structure analysis and assessment
  - Configuration directory analysis (settings, database, exceptions, middleware)
  - Main.py analysis (router includes, FastAPI imports)
  - Domain module detection and health assessment
  - Missing component identification
  - Intelligent recommendations for project improvements
  - Beautiful Rich-based output with tables and formatting

- **Project Migration Command** (`fascraft migrate`)
  - Legacy project detection (flat structure vs. domain-driven)
  - Automatic conversion from flat structure to domain-driven architecture
  - Backup creation with timestamped directories
  - Base router structure implementation
  - Configuration file generation (`.fascraft.toml`)
  - Migration summary and progress tracking
  - Safety confirmations and rollback capabilities

- **Configuration Management Command** (`fascraft config`)
  - Project-specific configuration via `.fascraft.toml`
  - Configuration creation, display, update, and validation
  - TOML-based configuration format with multiple sections
  - Environment-specific settings (development, production)
  - Configuration validation and error handling
  - Key-value updates with dot notation support

- **Base Router Architecture**
  - Centralized router management (`/routers/base.py`)
  - Consistent API prefix (`/api/v1`) for all endpoints
  - Automatic module integration in base router
  - Health check endpoint (`/api/v1/health`)
  - Clean module routers without hardcoded prefixes
  - Automatic router updates when generating new modules

- **Git Integration**
  - Automatic `.gitignore` file generation for new projects
  - Project-specific ignore patterns
  - Ready for immediate version control setup

- **Enhanced Project Generation**
  - New project structure with base router integration
  - Improved module templates and success messages
  - Better project guidance and next steps

#### **Changed**
- **Module Router Templates**: Removed hardcoded prefixes from individual module routers
- **Main.py Integration**: Updated to use base router instead of individual module routers
- **Success Messages**: Enhanced with new feature information and guidance
- **Project Structure**: Added `routers/` directory with base router management

#### **Technical Improvements**
- **Dependency Management**: Added `tomli-w` for TOML file writing
- **Error Handling**: Enhanced error messages and user guidance
- **Testing**: Comprehensive test coverage for all new Phase 3 features
- **Documentation**: Complete documentation updates for all new features

#### **Files Added**
- `fascraft/commands/analyze.py` - Project analysis implementation
- `fascraft/commands/migrate.py` - Project migration implementation
- `fascraft/commands/config.py` - Configuration management implementation
- `fascraft/templates/new_project/.gitignore.jinja2` - Git ignore template
- `fascraft/templates/new_project/routers/__init__.py.jinja2` - Routers package init
- `fascraft/templates/new_project/routers/base.py.jinja2` - Base router template
- `fascraft/templates/new_project/fascraft.toml.jinja2` - Configuration template

#### **Files Modified**
- `fascraft/main.py` - Added new Phase 3 commands
- `fascraft/commands/new.py` - Enhanced with base router and git integration
- `fascraft/commands/generate.py` - Updated to use base router integration
- `fascraft/templates/new_project/main.py.jinja2` - Updated for base router
- `fascraft/templates/module/routers.py.jinja2` - Removed hardcoded prefixes
- `pyproject.toml` - Added `tomli-w` dependency

#### **Tests Added**
- `tests/test_analyze.py` - Comprehensive testing for analyze command
- `tests/test_migrate.py` - Comprehensive testing for migrate command
- `tests/test_config.py` - Comprehensive testing for config command
- Updated existing tests to reflect new architecture

## [0.3.0] - 2025-08-17

### 🚀 **Phase 2.5: Environment & Dependency Management - COMPLETED**

#### **Added**
- **Environment Configuration**
  - Complete `.env` file generation with database configurations
  - `.env.sample` template for team collaboration
  - Support for MongoDB, PostgreSQL, MySQL, and SQLite
  - Redis, Celery, JWT, and CORS configurations
  - Production-ready environment management

- **Dual Dependency Management**
  - Poetry configuration (`pyproject.toml`) with all dependencies
  - pip requirements files (`requirements.txt`, `requirements.dev.txt`, `requirements.prod.txt`)
  - Development tools and testing frameworks
  - Production-optimized dependencies with Gunicorn

- **Enhanced Project Structure**
  - Comprehensive configuration directory
  - Database and middleware configurations
  - Exception handling and custom HTTP exceptions
  - CORS and timing middleware

#### **Changed**
- **Project Generation**: Enhanced with environment and dependency files
- **Template System**: Improved templates with production-ready configurations
- **Success Messages**: Better guidance for dependency installation

## [0.2.0] - 2025-08-17

### 🚀 **Phase 2: Complete Module Management - COMPLETED**

#### **Added**
- **Module Listing** (`fascraft list`)
  - Beautiful table display of all modules
  - Health status indicators (✅ Healthy / ⚠️ Incomplete)
  - File counts and test coverage information
  - Module size and last modified dates

- **Module Removal** (`fascraft remove`)
  - Safe module removal with confirmations
  - Automatic cleanup of main.py references
  - Removal preview with file counts and sizes
  - Force removal option for automation

- **Module Updates** (`fascraft update`)
  - Template refresh with automatic backups
  - Rollback capability if updates fail
  - Preserves custom business logic
  - Safe update process with confirmations

#### **Changed**
- **Module Generation**: Enhanced templates and better error handling
- **Success Messages**: Improved guidance and next steps
- **Error Handling**: Better error messages and user guidance

## [0.1.0] - 2025-08-17

### 🚀 **Phase 1: Module Templates & Project Generation - COMPLETED**

#### **Added**
- **Project Generation** (`fascraft new`)
  - FastAPI project creation with domain-driven architecture
  - Complete project structure with configuration
  - Environment and dependency management
  - Production-ready templates

- **Module Generation** (`fascraft generate`)
  - Domain module creation (models, schemas, services, routers)
  - Self-contained modules with clear boundaries
  - Automatic integration with main.py
  - Test directory generation

- **Core CLI Framework**
  - Typer-based command structure
  - Rich text formatting and beautiful output
  - Comprehensive error handling
  - User-friendly confirmations and guidance

#### **Technical Foundation**
- **Template System**: Jinja2-based template rendering
- **Command Architecture**: Modular command structure
- **Testing Framework**: Comprehensive test suite
- **Documentation**: Complete user and developer guides

---

## **🚀 Version History Summary**

- **v0.3.1** - Phase 3: Advanced Project Detection & Management ✅ **COMPLETED**
- **v0.3.0** - Phase 2.5: Environment & Dependency Management ✅ **COMPLETED**
- **v0.2.0** - Phase 2: Complete Module Management ✅ **COMPLETED**
- **v0.1.0** - Phase 1: Module Templates & Project Generation ✅ **COMPLETED**

## **🔮 Upcoming Versions**

- **v0.4.0** - Phase 4: Interactive Experience & Advanced Module Features
- **v0.5.0** - Phase 5: Deployment & CI/CD Integration
- **v0.6.0** - Phase 6: Monitoring & Observability

---

**FasCraft** - Building better FastAPI projects, one command at a time! 🚀
