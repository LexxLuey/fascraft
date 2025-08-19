# Contributing to FasCraft

Thank you for your interest in contributing to FasCraft! 🚀 This guide will help you get started with contributing to our project.

## 📋 **Table of Contents**

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community Guidelines](#community-guidelines)
- [Release Process](#release-process)

---

## 🚀 **Getting Started**

### **Before You Begin**

1. **Read the Documentation**: Familiarize yourself with [our guides](docs/) and [examples](../examples/)
2. **Check Existing Issues**: Search [GitHub issues](https://github.com/LexxLuey/fascraft/issues) to see if your idea is already being worked on
3. **Join the Community**: Connect with us on [Discord](https://discord.gg/fascraft) and [GitHub Discussions](https://github.com/LexxLuey/fascraft/discussions)

### **Types of Contributions**

We welcome various types of contributions:

- 🐛 **Bug Fixes**: Help fix issues and improve stability
- 💡 **New Features**: Add functionality that benefits users
- 📚 **Documentation**: Improve guides, examples, and API docs
- 🧪 **Tests**: Add test coverage and improve reliability
- 🔧 **Infrastructure**: Improve CI/CD, tooling, and development experience
- 🌍 **Internationalization**: Help with translations and localization
- 🎨 **UI/UX**: Improve user interface and experience

---

## 🛠️ **Development Setup**

### **Prerequisites**

- **Python 3.10+** (3.11+ recommended)
- **Poetry** for dependency management
- **Git** for version control
- **Docker** (optional, for testing)

### **Local Development Setup**

1. **Fork and Clone**:
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/fascraft.git
   cd fascraft
   
   # Add the upstream remote
   git remote add upstream https://github.com/LexxLuey/fascraft.git
   ```

2. **Install Dependencies**:
   ```bash
   # Install Poetry if you haven't already
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install project dependencies
   poetry install
   
   # Install pre-commit hooks
   poetry run pre-commit install
   ```

3. **Verify Setup**:
   ```bash
   # Run tests to ensure everything works
   poetry run pytest
   
   # Check code quality
   poetry run black --check .
   poetry run ruff check .
   ```

### **Development Environment**

#### **VS Code Setup** (Recommended)
1. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
2. Install the [Pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
3. Set Python interpreter to the Poetry virtual environment
4. Enable format on save with Black

#### **PyCharm Setup**
1. Open the project in PyCharm
2. Configure the Poetry virtual environment as the project interpreter
3. Install and configure Black, Ruff, and other tools

---

## 📝 **Code Standards**

### **Python Style Guide**

We follow **PEP 8** and use modern Python features:

#### **Code Formatting**
- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **String Quotes**: Double quotes for strings, single quotes for characters
- **Imports**: Grouped and sorted (use `isort`)

#### **Naming Conventions**
- **Functions and Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Methods**: `_leading_underscore`

#### **Code Examples**

```python
# ✅ Good
from typing import List, Optional
from pathlib import Path

def create_project_structure(project_path: Path, project_name: str) -> None:
    """Create the basic project directory structure."""
    try:
        project_path.mkdir(parents=True, exist_ok=True)
        console.print("📁 Created project structure", style="bold green")
    except OSError as e:
        raise FileSystemError(f"Failed to create structure: {e}") from e

# ❌ Bad
from typing import *
import pathlib

def CreateProjectStructure(projectPath, projectName):
    projectPath.mkdir(parents=True, exist_ok=True)
    print("Created project structure")
```

### **Documentation Standards**

#### **Docstrings**
Use Google-style docstrings for all public functions:

```python
def create_new_project(
    project_name: str,
    path: str = ".",
    interactive: bool = False
) -> None:
    """Create a new FastAPI project with FasCraft.
    
    Args:
        project_name: Name of the new project
        path: Directory path where project will be created
        interactive: Enable interactive mode for guided setup
        
    Raises:
        FasCraftError: If project creation fails
        ValidationError: If inputs are invalid
        
    Example:
        >>> create_new_project("my-api", interactive=True)
        🎉 Successfully created new project 'my-api'
    """
```

#### **Type Hints**
Always include type hints for function parameters and return values:

```python
from typing import List, Optional, Union
from pathlib import Path

def process_templates(
    template_paths: List[Path],
    context: Optional[dict] = None
) -> Union[str, bytes]:
    """Process Jinja2 templates with context."""
```

### **Error Handling**

#### **Exception Guidelines**
- Use custom exceptions from `fascraft.exceptions`
- Include meaningful error messages
- Provide suggestions for resolution
- Use proper exception chaining with `from e`

```python
# ✅ Good
try:
    project_path.mkdir(parents=True, exist_ok=True)
except PermissionError as e:
    raise PermissionError(
        str(project_path), 
        "create directory"
    ) from e

# ❌ Bad
try:
    project_path.mkdir(parents=True, exist_ok=True)
except:
    raise Exception("Failed")
```

---

## 🧪 **Testing Guidelines**

### **Test Structure**

Organize tests to mirror the source code structure:

```
tests/
├── unit/                    # Unit tests
│   ├── test_commands/      # Command tests
│   ├── test_templates/     # Template tests
│   └── test_validation/    # Validation tests
├── integration/             # Integration tests
│   ├── test_project_creation/
│   └── test_module_generation/
└── fixtures/               # Test fixtures and data
```

### **Test Naming**

Use descriptive test names that explain the behavior:

```python
# ✅ Good
def test_create_project_with_invalid_name_raises_validation_error():
    """Test that invalid project names raise ValidationError."""
    
def test_project_creation_creates_all_required_directories():
    """Test that project creation creates all required directories."""
    
def test_template_rendering_with_special_characters():
    """Test template rendering handles special characters correctly."""

# ❌ Bad
def test_1():
def test_project():
def test_error():
```

### **Test Coverage**

- **Minimum Coverage**: 90% for new code
- **Critical Paths**: 100% coverage required
- **Edge Cases**: Test boundary conditions and error scenarios

### **Test Examples**

#### **Unit Tests**
```python
import pytest
from pathlib import Path
from fascraft.validation import validate_project_name
from fascraft.exceptions import ValidationError

class TestProjectNameValidation:
    """Test project name validation."""
    
    def test_valid_project_names(self):
        """Test that valid project names pass validation."""
        valid_names = ["my-project", "api_v1", "user-management"]
        
        for name in valid_names:
            result = validate_project_name(name)
            assert result == name
    
    def test_invalid_project_names_raise_error(self):
        """Test that invalid project names raise ValidationError."""
        invalid_names = ["", " ", "my project", "my@project", "my.project"]
        
        for name in invalid_names:
            with pytest.raises(ValidationError) as exc_info:
                validate_project_name(name)
            assert "invalid project name" in str(exc_info.value).lower()
    
    def test_project_name_length_limits(self):
        """Test project name length validation."""
        # Test minimum length
        with pytest.raises(ValidationError):
            validate_project_name("a")
        
        # Test maximum length
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            validate_project_name(long_name)
```

#### **Integration Tests**
```python
import pytest
import tempfile
from pathlib import Path
from fascraft.commands.new import create_new_project

class TestProjectCreation:
    """Integration tests for project creation."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    
    def test_create_basic_project(self, temp_dir):
        """Test creating a basic project."""
        project_name = "test-project"
        project_path = temp_dir / project_name
        
        # Create project
        create_new_project(project_name, str(temp_dir))
        
        # Verify project structure
        assert project_path.exists()
        assert (project_path / "main.py").exists()
        assert (project_path / "config").exists()
        assert (project_path / "routers").exists()
    
    def test_create_project_with_interactive_mode(self, temp_dir, monkeypatch):
        """Test interactive project creation."""
        # Mock user input
        inputs = iter(["test-interactive", ".", "basic", "y", "y", "y", "y", "y", "y"])
        monkeypatch.setattr("rich.prompt.Prompt.ask", lambda *args, **kwargs: next(inputs))
        
        project_name = "test-interactive"
        project_path = temp_dir / project_name
        
        # Create project in interactive mode
        create_new_project(interactive=True)
        
        # Verify project was created
        assert project_path.exists()
```

### **Test Fixtures**

Use fixtures for common test setup:

```python
import pytest
from pathlib import Path
from fascraft.templates import TemplateManager

@pytest.fixture
def template_manager():
    """Provide template manager for testing."""
    return TemplateManager()

@pytest.fixture
def sample_project_context():
    """Provide sample project context for testing."""
    return {
        "project_name": "test-project",
        "author_name": "Test Author",
        "description": "Test project description"
    }

@pytest.fixture
def temp_project_dir(tmp_path):
    """Provide temporary project directory."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()
    return project_dir
```

---

## 🔄 **Pull Request Process**

### **Before Submitting**

1. **Ensure Tests Pass**:
```bash
poetry run pytest
   poetry run black --check .
   poetry run ruff check .
   poetry run mypy fascraft/
   ```

2. **Update Documentation**:
   - Update relevant documentation files
   - Add docstrings for new functions
   - Update examples if needed

3. **Check Coverage**:
   ```bash
   poetry run pytest --cov=fascraft --cov-report=html
   ```

### **Pull Request Guidelines**

#### **Title Format**
```
[FEATURE] Add interactive mode for project creation
[BUGFIX] Fix template rendering with special characters
[DOCS] Update quickstart guide with new features
[TEST] Add comprehensive test coverage for validation
```

#### **Description Template**
```markdown
## 🎯 **What This PR Does**

Brief description of the changes and why they're needed.

## 🔄 **Changes Made**

- [ ] Added interactive mode with guided setup
- [ ] Enhanced error handling for template rendering
- [ ] Updated documentation with new features
- [ ] Added comprehensive test coverage

## 🧪 **Testing**

- [ ] All tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated existing tests as needed
- [ ] Tested on multiple Python versions

## 📚 **Documentation**

- [ ] Updated relevant documentation
- [ ] Added docstrings for new functions
- [ ] Updated examples if applicable
- [ ] Added changelog entry

## 🔍 **Additional Notes**

Any additional context, breaking changes, or considerations.

## 📋 **Checklist**

- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Self-review completed
```

### **Review Process**

1. **Automated Checks**: CI/CD pipeline runs tests and quality checks
2. **Code Review**: At least one maintainer must approve
3. **Testing**: Changes are tested in staging environment
4. **Merge**: PR is merged after approval and testing

---

## 🐛 **Issue Guidelines**

### **Bug Reports**

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages and logs

### **Feature Requests**

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:

- Problem statement
- Proposed solution
- Use cases and examples
- Impact assessment

### **Questions/Support**

Use the [question template](.github/ISSUE_TEMPLATE/question.md) and include:

- What you're trying to accomplish
- What you've already tried
- Specific questions or help needed

---

## 🤝 **Community Guidelines**

### **Code of Conduct**

We are committed to providing a welcoming and inclusive environment:

- **Be Respectful**: Treat everyone with respect and dignity
- **Be Inclusive**: Welcome people of all backgrounds and experience levels
- **Be Collaborative**: Work together to solve problems
- **Be Constructive**: Provide helpful, constructive feedback

### **Communication Channels**

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussions
- **Discord**: Real-time chat and support
- **Email**: Security issues and private matters

### **Getting Help**

- Check the [troubleshooting guide](docs/troubleshooting.md)
- Search [existing issues](https://github.com/LexxLuey/fascraft/issues)
- Ask in [GitHub Discussions](https://github.com/LexxLuey/fascraft/discussions)
- Join our [Discord server](https://discord.gg/fascraft)

---

## 🚀 **Release Process**

### **Versioning**

We follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

### **Release Checklist**

Before each release:

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Security review completed

### **Release Steps**

1. **Prepare Release**:
```bash
   # Update version in pyproject.toml
   poetry version patch  # or minor/major
   
   # Update changelog
   # Update documentation
   ```

2. **Create Release Branch**:
```bash
   git checkout -b release/v0.5.0
   git add .
   git commit -m "Release v0.5.0"
   git push origin release/v0.5.0
   ```

3. **Create Pull Request**:
   - Merge release branch to main
   - Create GitHub release
   - Tag the release

4. **Publish to PyPI**:
   ```bash
   poetry build
   poetry publish
   ```

---

## 🎯 **Areas for Contribution**

### **High Priority**

- **Testing**: Improve test coverage and add integration tests
- **Documentation**: Enhance guides and add more examples
- **Error Handling**: Improve error messages and recovery
- **Performance**: Optimize template rendering and file operations

### **Medium Priority**

- **New Commands**: Add useful CLI commands
- **Template System**: Enhance template engine and customization
- **Configuration**: Improve configuration management
- **CI/CD**: Enhance GitHub Actions and deployment

### **Low Priority**

- **Internationalization**: Add multi-language support
- **Plugins**: Create plugin system for extensions
- **GUI**: Add graphical user interface
- **Mobile**: Create mobile app companion

---

## 🙏 **Recognition**

### **Contributor Hall of Fame**

We recognize contributors in several ways:

- **GitHub Contributors**: Listed on the main repository
- **Release Notes**: Acknowledged in release announcements
- **Documentation**: Featured in contributing guides
- **Community**: Recognized in community events

### **Getting Started**

1. **Pick an Issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Ask Questions**: Don't hesitate to ask for clarification
3. **Start Small**: Begin with documentation or simple bug fixes
4. **Get Feedback**: Share your work early and often

---

## 📞 **Contact and Support**

### **Maintainers**

- **Lead Developer**: [@LexxLuey](https://github.com/LexxLuey)
- **Community Manager**: [@FasCraftTeam](https://github.com/FasCraftTeam)

### **Getting Help**

- **Documentation**: [Complete guides](docs/)
- **Examples**: [Working projects](../examples/)
- **Discord**: [Real-time support](https://discord.gg/fascraft)
- **GitHub**: [Issues and discussions](https://github.com/LexxLuey/fascraft)

---

**Thank you for contributing to FasCraft! 🚀**

Your contributions help make FasCraft better for developers around the world. Whether you're fixing bugs, adding features, improving documentation, or helping other users, every contribution matters.

Together, we're building the future of FastAPI project generation! ✨
