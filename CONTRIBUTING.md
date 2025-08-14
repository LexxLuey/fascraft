# Contributing to FastForge

**Welcome!** 🎉 We're excited you want to help make FastForge better. This guide is written for beginners - no experience required!

## What is FastForge?

FastForge is a CLI tool that helps developers create new FastAPI projects quickly using Jinja2 templates. It's like a "project starter kit" that saves time and ensures consistency.

## How Can I Help?

### 🐛 **Report Bugs**
Found something that doesn't work? Tell us about it!

**What to include:**
- What you were trying to do
- What happened instead
- What you expected to happen
- Your operating system (Windows, Mac, Linux)
- Python version (`python --version`)
- FastForge version (`fastforge version`)

**Example:**
```
I tried to create a new project with "fastforge new my-api"
But I got an error: "Permission denied"
I expected it to create a new folder
I'm on Windows 10, Python 3.11, FastForge 0.1.0
```

### 💡 **Suggest Features**
Have an idea for something new? We want to hear it!

**What to include:**
- What you want FastForge to do
- Why it would be helpful
- Any examples of how it might work

**Example:**
```
I'd like FastForge to create a basic FastAPI app.py file
This would save me from writing boilerplate code
It could work like: fastforge new my-api --with-app
```

### 🔧 **Fix Code**
Want to help write code? Great! Here's how to get started.

## Setting Up Your Development Environment

### 1. Get the Code
```bash
# Download FastForge to your computer
git clone https://github.com/your-username/fastforge.git

# Go into the folder
cd fastforge
```

### 2. Install Python Tools
```bash
# Install Poetry (manages dependencies)
pip install poetry

# Install all the tools FastForge needs
poetry install
```

### 3. Test Your Setup
```bash
# Make sure everything works
poetry run fastforge --help
poetry run fastforge hello
```

## How FastForge Works (Simple Version)

### 📁 **Project Structure**
```
fastforge/
├── fastforge/           # The main code
│   ├── main.py         # Command line interface
│   ├── commands/       # Different commands (new, hello, etc.)
│   └── templates/      # Jinja2 templates for generating projects
├── pyproject.toml      # Project settings and dependencies
└── README.md          # This file
```

### 🎯 **Key Concepts**
- **Commands**: Functions that do things (like `new`, `hello`)
- **Templates**: Jinja2 files that get rendered and customized for new projects
- **CLI**: Command Line Interface - how users interact with FastForge

## Testing

### 🧪 **Running Tests**

FastForge has **100% test coverage** with a comprehensive test suite to ensure everything works correctly. Before making any changes, make sure all tests pass.

**Current Test Status:** ✅ 36 tests passing, 0 failed, 0 skipped

#### **Run All Tests**
```bash
# Activate the poetry environment
poetry shell

# Run all tests with verbose output
poetry run pytest tests/ -v

# Run tests with short traceback for failures
poetry run pytest tests/ -v --tb=short

# Run tests and stop on first failure
poetry run pytest tests/ -x
```

#### **Run Specific Test Files**
```bash
# Test only the new command functionality
poetry run pytest tests/test_new_command.py -v

# Test only CLI integration
poetry run pytest tests/test_cli_integration.py -v

# Test only template rendering
poetry run pytest tests/test_templates.py -v
```

#### **Run Specific Test Functions**
```bash
# Run a specific test function
poetry run pytest tests/test_new_command.py::TestNewCommand::test_create_new_project_success -v

# Run tests matching a pattern
poetry run pytest tests/ -k "template" -v
```

#### **Test Coverage**
```bash
# Install pytest-cov for coverage reporting
poetry add --group dev pytest-cov

# Run tests with coverage report
poetry run pytest tests/ --cov=fastforge --cov-report=html

# View coverage report in browser
# Open htmlcov/index.html
```

### 📝 **Writing New Tests**

When adding new features or fixing bugs, always write tests to ensure your changes work correctly and don't break existing functionality.

#### **Test Structure**
```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_new_command.py      # Tests for the new command
├── test_cli_integration.py  # CLI integration tests
├── test_templates.py        # Template validation tests
└── test_utils.py            # Utility function tests
```

#### **Test Naming Conventions**
- **Files**: `test_*.py` (e.g., `test_new_command.py`)
- **Classes**: `Test*` (e.g., `TestNewCommand`)
- **Functions**: `test_*` (e.g., `test_create_new_project_success`)

#### **Writing Test Functions**
```python
def test_function_name(self, fixture_name: Type) -> None:
    """Test description of what this test verifies."""
    # Arrange - set up test data
    test_data = "example"
    
    # Act - call the function being tested
    result = function_being_tested(test_data)
    
    # Assert - verify the result
    assert result == "expected_value"
```

#### **Using Fixtures**
```python
def test_with_fixtures(self, temp_dir: Path, sample_project_name: str) -> None:
    """Test using shared fixtures."""
    # temp_dir provides a temporary directory that gets cleaned up
    # sample_project_name provides a consistent test project name
    
    project_path = temp_dir / sample_project_name
    # ... test logic here
```

#### **Testing CLI Commands**
```python
def test_cli_command(self, cli_runner: CliRunner) -> None:
    """Test CLI command execution."""
    result = cli_runner.invoke(app, ["command", "arg"])
    
    assert result.exit_code == 0
    assert "expected output" in result.output
```

#### **Testing Error Conditions**
```python
def test_error_handling(self) -> None:
    """Test that errors are handled correctly."""
    with pytest.raises(ExpectedException) as exc_info:
        function_that_should_fail()
    
    assert exc_info.value.code == 1
```

#### **Testing File Generation**
```python
def test_file_creation(self, temp_dir: Path) -> None:
    """Test that files are created correctly."""
    # Create project
    create_new_project("test-project", temp_dir)
    
    # Verify files exist
    project_path = temp_dir / "test-project"
    assert (project_path / "main.py").exists()
    assert (project_path / "pyproject.toml").exists()
    
    # Verify file contents
    content = (project_path / "main.py").read_text()
    assert "from fastapi import FastAPI" in content
```

### 🔧 **Test Best Practices**

1. **Test One Thing**: Each test should verify one specific behavior
2. **Use Descriptive Names**: Test names should clearly describe what they test
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Use Fixtures**: Reuse common test setup with pytest fixtures
5. **Test Edge Cases**: Include tests for error conditions and boundary cases
6. **Clean Up**: Use temporary directories that get cleaned up automatically
7. **Mock External Dependencies**: Use mocking to isolate the code being tested

## Making Changes

### 1. **Pick Something Small**
Start with something simple:
- Fix a typo in a message
- Add a new example to the help text
- Change a default value

### 2. **Make Your Change**
- Edit the file you want to change
- Test your change: `poetry run fastforge --help`
- Make sure it still works!

### 3. **Test Your Changes**
```bash
# Run the tool to make sure it works
poetry run fastforge hello
poetry run fastforge version

# If you added a new command, test it
poetry run fastforge your-new-command
```

## Adding a New Command

Want to add a new feature? Here's how:

### 1. **Create a New File**
Create `fastforge/commands/your_command.py`:

```python
"""Your new command description."""

import typer

def your_new_command():
    """What your command does."""
    typer.echo("Hello from your new command!")

# Add this to main.py:
# app.command(name="your-command")(your_new_command)
```

### 2. **Add It to Main**
In `fastforge/main.py`, add:
```python
from fastforge.commands import your_command

app.command(name="your-command")(your_command.your_new_command)
```

### 3. **Test It**
```bash
poetry run fastforge your-command
```

## Code Style (Don't Panic!)

We use tools to make code look nice automatically:

```bash
# Format your code (makes it look pretty)
poetry run black .

# Sort imports and format code (organizes import statements)
poetry run ruff format .

# Check for problems
poetry run ruff check .

# Auto-fix many issues
poetry run ruff check --fix .

# Run all checks at once
poetry run ruff check . && poetry run ruff format --check . && poetry run black --check .
```

**Don't worry about this too much** - these tools fix most formatting issues automatically!

### Using the Makefile (Optional)

For even easier development, you can use the included Makefile:

```bash
# Show all available commands
make help

# Run all code quality checks
make all-checks

# Format and lint code
make format
make lint

# Run tests
make test
```

## Git Workflow and Commit Strategy

### 1. **Create a Feature Branch**
Never work directly on the main branch:

```bash
# Make sure you're on main and it's up to date
git checkout main
git pull origin main

# Create a new branch for your changes
git checkout -b feature/your-feature-name

# Example branch names:
git checkout -b fix/typo-in-readme
git checkout -b feature/add-generate-command
git checkout -b docs/improve-contributing-guide
```

### 2. **Make Your Changes**
- Edit files as needed
- Test your changes thoroughly
- Run code quality tools: `poetry run black . && poetry run isort .`

### 3. **Commit Your Changes**
Use clear, descriptive commit messages:

```bash
# See what you changed
git status

# Add your changes
git add .

# Commit with a clear message
git commit -m "feat: add new generate command for creating API endpoints

- Add generate.py command file
- Implement endpoint generation logic
- Add tests for new functionality
- Update help text and documentation"
```

### 4. **Commit Message Format**
Follow this pattern: `type: brief description`

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting, missing semicolons, etc.
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "fix: resolve help command crash on Python 3.13"
git commit -m "docs: add contributing guide for beginners"
git commit -m "feat: add --template option to new command"
git commit -m "style: format code with black and isort"
```

### 5. **Push Your Branch**
```bash
# Push your feature branch to GitHub
git push origin feature/your-feature-name
```

## Creating a Pull Request

### 1. **Go to GitHub**
- Navigate to the FastForge repository
- You should see a banner suggesting to create a PR for your branch
- Click "Compare & pull request"

### 2. **Fill Out the PR Template**
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] I have tested my changes locally
- [ ] I have run the test suite
- [ ] I have formatted code with black/isort

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have updated documentation if needed
- [ ] My changes generate no new warnings
```

### 3. **Submit and Wait for Review**
- Submit the PR
- Wait for maintainers to review
- Respond to any feedback or requested changes
- Once approved, your changes will be merged!

## Responding to PR Feedback

### 1. **Address Review Comments**
- Read each comment carefully
- Make the requested changes
- Test your changes again

### 2. **Update Your Branch**
```bash
# Make your changes
git add .
git commit -m "fix: address PR review feedback

- Fix typo in error message
- Add missing docstring
- Update test case"
git push origin feature/your-feature-name
```

### 3. **The PR Updates Automatically**
- GitHub automatically updates your PR with new commits
- Maintainers will review the updated code
- Repeat until approved!

## Need Help?

**Don't be afraid to ask questions!** We were all beginners once.

**Ways to get help:**
- Open an issue on GitHub
- Ask in discussions
- Join our community chat (if we have one)
- Comment on your PR if you're stuck

## What Makes a Good Contribution?

✅ **Good:**
- Fixes a real problem
- Makes something easier to use
- Adds helpful documentation
- Improves error messages
- Follows existing code patterns
- Includes tests for new functionality

❌ **Not so good:**
- Changes that break existing features
- Adding complexity without clear benefit
- Changing things just because you can
- Ignoring code style guidelines
- Not testing your changes

## Remember

- **Start small** - tiny changes are perfect!
- **Ask questions** - we're here to help
- **Test your changes** - make sure they work
- **Be patient** - learning takes time
- **Follow the workflow** - it helps everyone

---

**Thank you for wanting to help!** 🚀 Every contribution, no matter how small, makes FastForge better for everyone.
