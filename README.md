# FastForge

**FastForge** is a simple CLI tool for generating modular FastAPI project structures for you. Think of it as a project generator that sets up all the basic files you need to start building a FastAPI application.

## What Does FastForge Do?

- 🚀 **Creates new FastAPI projects** with one command
- 📁 **Sets up project structure** automatically
- 🎯 **Uses templates** to generate consistent code
- ⚡ **Saves time** - no more manual setup!

## Quick Start

### 1. Install FastForge

**Option A: Install from source (development)**
```bash
# Clone the repository
git clone https://github.com/your-username/fastforge.git
cd fastforge

# Install with Poetry
pip install poetry
poetry install
poetry run fastforge --help
```

**Option B: Install via pip (when published)**
```bash
pip install fastforge
```

### 2. Create a New Project
```bash
# If installed via Poetry
poetry run fastforge new my-awesome-api

# If installed via pip
fastforge new my-awesome-api
```

That's it! FastForge will create a new folder called `my-awesome-api` with all the basic files you need.

### 3. What You Get
```
my-awesome-api/
├── __init__.py    # Project metadata and version info
├── main.py        # FastAPI application with endpoints
├── pyproject.toml # Poetry configuration and dependencies
└── README.md      # Project documentation and setup guide
```

## Available Commands

- `fastforge new <project-name>` - Create a new FastAPI project
- `fastforge hello` - Say hello to FastForge
- `fastforge version` - Show FastForge version
- `fastforge --help` - Show all available commands

## Examples

```bash
# Create a project in current directory
fastforge new my-api

# Create a project in a specific folder
fastforge new my-api --path /path/to/projects

# Say hello
fastforge hello

# Check version
fastforge version
```

## Requirements

- **Python**: 3.10 or higher
- **Dependencies**: FastForge automatically handles all required packages
- **Templates**: Uses Jinja2 for customizable project generation

## How It Works

FastForge uses **Jinja2 templates** to generate project files. When you run `fastforge new <project-name>`, it:

1. Creates a new directory with your project name
2. Reads templates from `fastforge/templates/`
3. Renders templates with your project-specific data
4. Generates all necessary files automatically

## Need Help?

If something goes wrong or you have questions:
1. Check the error message - it usually tells you what's wrong
2. Verify Python version: `python --version` (must be 3.10+)
3. Try running `fastforge --help` to see all options
4. Check the [Contributing Guide](CONTRIBUTING.md) for development setup

## What's Next?

After creating your project with FastForge:
1. Navigate to your project folder: `cd my-awesome-api`
2. Install FastAPI and dependencies: `pip install fastapi uvicorn`
3. Start building your API!

## Development

For developers who want to contribute or modify FastForge:
- See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions
- Uses Poetry for dependency management
- Includes code quality tools (Black, Ruff, Flake8)
- Pre-commit hooks for automated code formatting
- Makefile for common development commands

## Testing

FastForge has **100% test coverage** with a comprehensive test suite:

```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test categories
poetry run pytest tests/test_new_command.py -v      # Core functionality
poetry run pytest tests/test_cli_integration.py -v  # CLI integration
poetry run pytest tests/test_templates.py -v        # Template validation

# Run with coverage
poetry run pytest tests/ --cov=fastforge --cov-report=html
```

**Test Results:** ✅ 36 tests passing, 0 failed, 0 skipped

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed testing instructions and best practices.

---

**FastForge** - Making FastAPI development faster and easier! 🚀
