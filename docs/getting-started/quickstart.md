# FasCraft Quickstart Guide

Get up and running with FasCraft in minutes! This guide will walk you through creating your first FastAPI project using FasCraft's Domain-Driven Architecture (DDA) approach.

## 🚀 What You'll Build

By the end of this guide, you'll have:
- A fully functional FastAPI application
- Clean, scalable project structure
- CI/CD pipeline ready
- Docker deployment configured
- Professional-grade setup

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed
- **Poetry** for dependency management (recommended)
- **Git** for version control
- **Docker** (optional, for containerization)

### Install Poetry (if not installed)
```bash
# Windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

## 🎯 Step 1: Install FasCraft

### Option 1: Install from Source (Development)
```bash
# Clone the repository
git clone https://github.com/your-org/fascraft.git
cd fascraft

# Install in development mode
poetry install
poetry run pip install -e .
```

### Option 2: Install from PyPI (Release)
```bash
pip install fascraft
```

### Verify Installation
```bash
fascraft --help
```

You should see the available commands:
```
Usage: fascraft [OPTIONS] COMMAND [ARGS]...

  FasCraft CLI for generating modular FastAPI projects.

Options:
  --help  Show this message and exit.

Commands:
  new       Create a new FastAPI project
  generate  Generate a new module for an existing project
  analyze   Analyze project structure and provide insights
```

## 🏗️ Step 2: Create Your First Project

### Create a New Project
```bash
# Create a new project called "my-awesome-api"
fascraft new my-awesome-api

# Or specify a custom path
fascraft new my-awesome-api --path /custom/path
```

### What Gets Created
```
my-awesome-api/
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── settings.py         # App settings
│   ├── database.py         # Database config
│   ├── exceptions.py       # Custom exceptions
│   └── middleware.py       # Custom middleware
├── routers/                # Router foundation
│   ├── __init__.py
│   └── base.py            # Base router
├── .github/                # CI/CD workflows
│   └── workflows/
│       ├── ci.yml         # GitHub Actions CI
│       └── dependency-update.yml
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── requirements.dev.txt    # Development dependencies
├── requirements.prod.txt   # Production dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service orchestration
├── fascraft.toml          # FasCraft configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🚀 Step 3: Run Your Application

### Navigate to Project
```bash
cd my-awesome-api
```

### Install Dependencies
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

### Start the Server
```bash
# Using Poetry
poetry run python main.py

# Or directly
python main.py
```

### Access Your API
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc Documentation:** http://localhost:8000/redoc

## 🎉 Congratulations!

Your FastAPI application is now running! You should see:
- A welcome message at the root endpoint
- Health check endpoint at `/api/v1/health`
- Interactive API documentation

## 🔧 Step 4: Add Your First Module

Now let's add some functionality to your project:

### Generate a User Module
```bash
fascraft generate user
```

This creates:
```
my-awesome-api/
├── users/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── services.py        # Business logic
│   ├── routers.py         # API endpoints
│   └── tests/             # Test files
```

### Generate More Modules
```bash
# Add product management
fascraft generate product

# Add order processing
fascraft generate order

# Add authentication
fascraft generate auth
```

## 🧪 Step 5: Test Your Setup

### Run Tests
```bash
# Install development dependencies
pip install -r requirements.dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

### Check Project Structure
```bash
# Analyze your project
fascraft analyze

# List dependencies
fascraft dependencies list
```

## 🐳 Step 6: Deploy with Docker

### Build and Run
```bash
# Development
docker-compose up --build

# Production
docker-compose --profile production up --build
```

### Access Containerized API
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

## 📚 What You've Learned

✅ **Project Creation** - Using `fascraft new`  
✅ **Module Generation** - Using `fascraft generate`  
✅ **DDA Principles** - Clean, minimal structure  
✅ **FastAPI Integration** - Modern web framework  
✅ **CI/CD Setup** - GitHub Actions ready  
✅ **Containerization** - Docker deployment  
✅ **Professional Setup** - Production-ready configuration  

## 🚀 Next Steps

### Explore Examples
Check out the `examples/` directory for more complex scenarios:
- **Basic API** - Simple CRUD operations
- **E-commerce API** - Business logic patterns
- **Authentication API** - Security implementation
- **Database API** - ORM integration

### Customize Your Project
- Modify endpoints in `main.py`
- Add business logic to generated modules
- Customize configuration in `config/settings.py`
- Extend CI/CD workflows

### Learn More
- Read the [Project Generation Guide](project-generation.md)
- Explore [Module Management](module-management.md)
- Understand [Configuration Management](configuration.md)
- Learn about [Database Migrations](migration.md)

## 🔍 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Import errors:**
```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

**Permission errors:**
```bash
# Check file permissions
# Ensure write access to project directory
```

### Getting Help

- Check the [examples](../examples/) directory
- Review [project generation](project-generation.md) guide
- Explore [module management](module-management.md) documentation
- Check [configuration](configuration.md) options

## 🎯 Success Checklist

- [ ] FasCraft installed and working
- [ ] New project created successfully
- [ ] Application running on localhost:8000
- [ ] API documentation accessible
- [ ] First module generated
- [ ] Tests running successfully
- [ ] Docker deployment working

---

**You're now ready to build amazing FastAPI applications with FasCraft! 🚀**

The clean, scalable architecture you've created will grow with your needs. Add modules as you need them, customize functionality, and deploy with confidence using the professional-grade setup included.
