# Contributing to FasCraft 🚀

Thank you for your interest in contributing to FasCraft! This document provides guidelines and information for contributors, including AI assistants.

## **📋 Project Status**

**Current Phase:** Phase 3 - Advanced Project Detection & Management ✅ **COMPLETED**  
**Version:** 0.3.2
**Status:** All Phase 3 features implemented and tested

### **✅ Recently Completed Features:**
- **Project Analysis** (`fascraft analyze`) - Intelligent project structure analysis
- **Migration Tools** (`fascraft migrate`) - Legacy project conversion
- **Configuration Management** (`fascraft config`) - Project-specific settings
- **Base Router Architecture** - Centralized router management
- **Git Integration** - Automatic `.gitignore` generation

## **🏗️ Project Structure**

FasCraft follows a clean, modular architecture:

```
fascraft/
├── main.py                 # CLI entry point and command registration
├── commands/               # Individual command implementations
│   ├── __init__.py
│   ├── new.py             # Create new projects
│   ├── generate.py         # Generate domain modules
│   ├── list.py             # List modules with health status
│   ├── remove.py           # Remove modules safely
│   ├── update.py           # Update module templates
│   ├── analyze.py          # Project analysis (NEW)
│   ├── migrate.py          # Project migration (NEW)
│   └── config.py           # Configuration management (NEW)
├── templates/               # Jinja2 templates for file generation
│   ├── new_project/        # Templates for new projects
│   └── module/             # Templates for domain modules
└── utils/                   # Shared utilities and helpers
```

### **New Phase 3 Commands:**
- **`analyze`** - Project structure analysis and recommendations
- **`migrate`** - Legacy project conversion to domain-driven architecture
- **`config`** - Project configuration management via `.fascraft.toml`

## **🔒 Architecture Stability Guidelines**

**CRITICAL:** FasCraft is built on a **stable, well-designed architecture** that must be preserved.

### **🚫 What CANNOT Be Changed:**
- **CLI Command Structure** - Command names, arguments, and basic flow
- **Template System** - Jinja2-based template rendering approach
- **Project Architecture** - Core domain-driven design principles
- **Module System** - Basic module generation and management
- **File Organization** - Directory structure and file naming conventions

### **✅ What CAN Be Enhanced:**
- **Template Content** - Improve existing template quality and features
- **New Commands** - Add new functionality through additional commands
- **Configuration Options** - Extend configuration parameters
- **Error Handling** - Improve error messages and validation
- **Testing** - Add more comprehensive test coverage

### **🏗️ Architectural Boundaries:**
- **Commands** - Each command should be self-contained and focused
- **Templates** - Templates should remain in the `templates/` directory
- **Utilities** - Shared code should go in `utils/` directory
- **Configuration** - Use existing configuration patterns

### **🔄 Migration Strategy:**
- **Backward Compatibility** - Existing projects must continue to work
- **Gradual Adoption** - New features should be opt-in
- **Clear Documentation** - All changes must be documented
- **Migration Tools** - Provide tools to help adopt new features

## **🤖 AI Contributor Guidelines**

**Special Instructions for AI Assistants:**

### **🚫 Critical Restrictions:**
1. **NEVER change the CLI command structure** - Commands must work exactly as documented
2. **NEVER modify the template system** - Keep Jinja2-based rendering
3. **NEVER change the project architecture** - Maintain domain-driven design
4. **NEVER break existing functionality** - All current features must work

### **✅ Safe Enhancement Areas:**
1. **Template Content** - Improve existing templates with better code
2. **Error Messages** - Make error messages more helpful and user-friendly
3. **Documentation** - Update docs to reflect new features
4. **Testing** - Add more comprehensive test coverage
5. **New Commands** - Add new functionality through additional commands

### **🔍 Before Making Changes:**
1. **Read the existing code** - Understand current implementation
2. **Check the roadmap** - Ensure changes align with planned phases
3. **Test thoroughly** - All changes must pass existing tests
4. **Update documentation** - Keep docs in sync with code changes

### **📝 Code Quality Standards:**
- **Follow PEP 8** - Use consistent Python formatting
- **Add type hints** - All functions should have type annotations
- **Write tests** - New features need comprehensive test coverage
- **Update docs** - Keep documentation current and accurate

## **🧪 Testing Standards**

### **Coverage Requirements:**
- **Minimum Coverage:** 90% for all new code
- **Test Quality:** Tests must be meaningful and comprehensive
- **Integration Testing:** Test command interactions and file generation
- **Error Handling:** Test both success and failure scenarios

### **Testing Patterns:**
- **Command Tests** - Test each command's functionality
- **Mock Testing** - Use mocks for file system and external dependencies
- **File System Tests** - Verify generated file content and structure
- **Error Scenario Tests** - Test error handling and edge cases

### **Running Tests:**
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_new_command.py

# Run with coverage
poetry run pytest --cov=fascraft

# Run specific test
poetry run pytest tests/test_new_command.py::test_new_project_success
```

## **📚 Documentation Requirements**

### **What Must Be Updated:**
- **README.md** - Reflect new features and capabilities
- **ROADMAP.md** - Update phase status and completed features
- **CONTRIBUTING.md** - Keep guidelines current
- **Command Help** - All commands must have clear help text
- **Examples** - Provide practical usage examples

### **Documentation Standards:**
- **Clear Examples** - Show real-world usage scenarios
- **Up-to-date** - Keep docs in sync with code changes
- **User-focused** - Write for end users, not developers
- **Comprehensive** - Cover all features and options

## **🚀 Development Workflow**

### **1. Setup Development Environment:**
```bash
git clone https://github.com/LexxLuey/fascraft.git
cd fascraft
poetry install
```

### **2. Make Changes:**
- **Follow guidelines** - Respect architectural boundaries
- **Write tests** - Add tests for new functionality
- **Update docs** - Keep documentation current

### **3. Test Your Changes:**
```bash
# Run all tests
poetry run pytest

# Test specific functionality
poetry run pytest tests/test_new_command.py

# Check code quality
poetry run ruff check .
poetry run black --check .
```

### **4. Submit Changes:**
- **Clear description** - Explain what and why you changed
- **Test results** - Show that all tests pass
- **Documentation updates** - Include doc changes

## **🔍 Common Issues & Solutions**

### **Template Rendering Issues:**
- **Problem:** Templates not rendering correctly
- **Solution:** Check Jinja2 syntax and template variables
- **Prevention:** Test template rendering in isolation

### **Command Integration Issues:**
- **Problem:** New commands not working
- **Solution:** Verify command registration in `main.py`
- **Prevention:** Follow existing command patterns

### **File Generation Issues:**
- **Problem:** Generated files have incorrect content
- **Solution:** Check template logic and file paths
- **Prevention:** Test file generation thoroughly

## **📞 Getting Help**

### **Before Asking:**
1. **Read the documentation** - Check README and CONTRIBUTING
2. **Search existing issues** - Look for similar problems
3. **Test your changes** - Ensure tests pass locally

### **When Asking:**
1. **Describe the problem** - What are you trying to do?
2. **Show your changes** - What did you modify?
3. **Include error messages** - What went wrong?
4. **Provide context** - What were you working on?

## **🎯 Contribution Priorities**

### **High Priority:**
- **Bug fixes** - Fix issues in existing functionality
- **Documentation** - Improve and update docs
- **Testing** - Add missing test coverage
- **Error handling** - Improve error messages

### **Medium Priority:**
- **Template improvements** - Better generated code
- **New commands** - Additional functionality
- **Performance** - Optimize existing code
- **User experience** - Improve CLI interactions

### **Low Priority:**
- **Major refactoring** - Large architectural changes
- **New features** - Significant new functionality
- **Integration changes** - Modify external integrations

---

**Thank you for contributing to FasCraft!** 🚀

Remember: **Stability first, enhancement second.** We're building tools that developers rely on, so reliability is paramount.
