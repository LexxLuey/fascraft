# FasCraft Test Suite Organization

This directory contains the comprehensive test suite for the FasCraft project, organized into logical categories for better maintainability and discovery.

## 📁 Test Organization Structure

### **`commands/`** - CLI Command Tests
Tests for all CLI commands and their functionality.

- **`test_new_command.py`** - Tests for project creation command
- **`test_generate_command.py`** - Tests for module generation command
- **`test_list_command.py`** - Tests for listing projects/modules command
- **`test_remove_command.py`** - Tests for removal command
- **`test_update_command.py`** - Tests for update command
- **`test_migrate.py`** - Tests for migration command
- **`test_config.py`** - Tests for configuration command
- **`test_analyze.py`** - Tests for project analysis command
- **`test_docs.py`** - Tests for documentation generation command
- **`test_enhanced_new_command.py`** - Enhanced new command tests
- **`test_enhanced_generate.py`** - Enhanced generate command tests

### **`core/`** - Core Functionality Tests
Tests for core utilities and fundamental functionality.

- **`test_utils.py`** - Tests for utility functions
- **`test_testing_utils.py`** - Tests for testing utilities
- **`test_generate_test.py`** - Tests for test generation functionality

### **`integration/`** - Integration Tests
Tests for integration features and cross-component functionality.

- **`test_cli_integration.py`** - CLI integration tests
- **`test_analyze_cli_integration.py`** - Analyze command CLI integration
- **`test_analyze_docs_integration.py`** - Documentation analysis integration

### **`dependencies/`** - Dependency Management Tests
Tests for dependency tracking and management features.

- **`test_dependencies_command.py`** - Dependency command tests
- **`test_analyze_dependencies.py`** - Dependency analysis tests
- **`test_module_dependencies.py`** - Module dependency tests

### **`templates/`** - Template System Tests
Tests for the Jinja2 template system and registry.

- **`test_templates.py`** - Basic template tests
- **`test_template_registry.py`** - Template registry tests
- **`test_list_templates_command.py`** - Template listing command tests

### **`validation/`** - Validation Logic Tests
Tests for input validation and data validation.

- **`test_validation.py`** - Core validation tests
- **`test_enhanced_validation.py`** - Enhanced validation tests

### **`exceptions/`** - Exception Handling Tests
Tests for custom exception classes and error handling.

- **`test_exceptions.py`** - Basic exception tests
- **`test_enhanced_exceptions.py`** - Enhanced exception tests

## 🧪 Running Tests

### Run All Tests
```bash
python -m pytest tests/
```

### Run Tests by Category
```bash
# Run only command tests
python -m pytest tests/commands/

# Run only core functionality tests
python -m pytest tests/core/

# Run only integration tests
python -m pytest tests/integration/

# Run only dependency tests
python -m pytest tests/dependencies/

# Run only template tests
python -m pytest tests/templates/

# Run only validation tests
python -m pytest tests/validation/

# Run only exception tests
python -m pytest tests/exceptions/
```

### Run Specific Test Files
```bash
# Run a specific test file
python -m pytest tests/commands/test_new_command.py

# Run with verbose output
python -m pytest tests/commands/test_new_command.py -v

# Run with coverage
python -m pytest tests/commands/test_new_command.py --cov=fascraft
```

### Run Tests with Specific Markers
```bash
# Run only fast tests
python -m pytest tests/ -m "not slow"

# Run only integration tests
python -m pytest tests/ -m "integration"

# Run only unit tests
python -m pytest tests/ -m "not integration"
```

## 📊 Test Coverage

The test suite provides comprehensive coverage for:

- ✅ **CLI Commands**: All command functionality and edge cases
- ✅ **Core Utilities**: Utility functions and helper modules
- ✅ **Integration**: Cross-component functionality and workflows
- ✅ **Dependencies**: Dependency tracking and management
- ✅ **Templates**: Jinja2 template system and registry
- ✅ **Validation**: Input validation and data validation
- ✅ **Exceptions**: Error handling and custom exceptions

## 🔧 Test Configuration

### **`conftest.py`**
Contains shared test fixtures and configuration that are available to all tests.

### **`__init__.py`**
Makes each test directory a proper Python package, enabling imports and test discovery.

## 📝 Adding New Tests

When adding new tests, follow these guidelines:

1. **Place tests in the appropriate category directory**
2. **Follow the naming convention**: `test_<module_name>.py`
3. **Use descriptive test class and method names**
4. **Include proper docstrings for test methods**
5. **Add appropriate test markers** (e.g., `@pytest.mark.integration`)
6. **Update this README** when adding new test categories

### Example Test Structure
```python
"""Tests for the new feature."""

import pytest
from fascraft.feature import new_function


class TestNewFeature:
    """Test the new feature functionality."""

    def test_new_function_basic(self):
        """Test basic functionality of new_function."""
        result = new_function("test")
        assert result == "expected_result"

    @pytest.mark.integration
    def test_new_function_integration(self):
        """Test integration with other components."""
        # Integration test logic
        pass
```

## 🚀 Continuous Integration

The test suite is designed to work with CI/CD pipelines:

- **Fast execution** for development feedback
- **Comprehensive coverage** for quality assurance
- **Clear organization** for maintainability
- **Proper isolation** for reliable results

## 📚 Additional Resources

- **pytest Documentation**: https://docs.pytest.org/
- **Testing Best Practices**: See project development guidelines
- **Test Coverage**: Use `--cov` flag for coverage reports
- **Test Markers**: Use `pytest --markers` to see available markers
