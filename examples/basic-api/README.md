# Basic API Example

A simple, clean FastAPI application demonstrating basic CRUD operations and FasCraft's core features.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Docker (optional)

### Step-by-Step Setup

1. **Navigate to the project directory:**
   ```bash
   cd examples/basic-api
   ```

2. **Install dependencies:**
   ```bash
   # Using Poetry (recommended)
   poetry install
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Using Poetry
   poetry run python main.py
   
   # Or directly
   python main.py
   ```

4. **Access the API:**
   - **API Base URL:** http://localhost:8000
   - **Interactive Docs:** http://localhost:8000/docs
   - **ReDoc Documentation:** http://localhost:8000/redoc

## 📁 Project Structure (DDA Approach)

```
basic-api/
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── settings.py         # App settings and environment
│   ├── database.py         # Database configuration
│   ├── exceptions.py       # Custom exception handling
│   └── middleware.py       # Custom middleware
├── routers/                # Router structure
│   ├── __init__.py
│   └── base.py            # Base router for module management
├── .github/                # CI/CD workflows
│   └── workflows/
│       ├── ci.yml         # GitHub Actions CI pipeline
│       └── dependency-update.yml
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Production dependencies
├── requirements.dev.txt    # Development dependencies
├── requirements.prod.txt   # Production dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service orchestration
├── fascraft.toml          # FasCraft project configuration
└── README.md              # This file
```

## 🔧 FasCraft Features Demonstrated

### 1. **Project Generation**
- ✅ **Clean DDA Structure** - No unnecessary MVC folders
- ✅ **Essential Configuration** - Settings, database, middleware
- ✅ **Router Foundation** - Base router for module management

### 2. **Configuration Management**
- ✅ **Environment Variables** - `.env` and `.env.sample` files
- ✅ **Settings Module** - Centralized configuration
- ✅ **Database Config** - Ready for database integration

### 3. **CI/CD Integration**
- ✅ **GitHub Actions** - Automated testing and deployment
- ✅ **Dependency Updates** - Automated security updates
- ✅ **Code Quality** - Linting, testing, security scanning

### 4. **Containerization**
- ✅ **Docker Support** - Multi-stage Dockerfile
- ✅ **Docker Compose** - Multi-service orchestration
- ✅ **Production Ready** - Optimized for production deployment

### 5. **Development Tools**
- ✅ **Development Dependencies** - Testing, linting, formatting
- ✅ **Production Dependencies** - Optimized runtime packages
- ✅ **FasCraft Integration** - Ready for module generation

## 🎯 API Endpoints

### Basic Operations
- `GET /` - Welcome message and status
- `GET /api/items` - List all items
- `GET /api/items/{item_id}` - Get specific item
- `POST /api/items` - Create new item

### Health & Status
- `GET /api/v1/health` - Health check (via base router)

## 🚀 Next Steps with FasCraft

### Add New Modules
```bash
# Generate a new user module
fascraft generate user

# Generate a product module  
fascraft generate product

# Generate an order module
fascraft generate order
```

### Analyze Project
```bash
# Get insights on your project structure
fascraft analyze

# Check dependencies
fascraft dependencies list
```

### Testing
```bash
# Install development dependencies
pip install -r requirements.dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## 🐳 Docker Deployment

### Development
   ```bash
docker-compose up --build
   ```

### Production
   ```bash
docker-compose --profile production up --build
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in main.py
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. **Import errors:**
```bash
   # Ensure dependencies are installed
   pip install -r requirements.txt
   ```

3. **Permission errors:**
```bash
   # Check file permissions
   # Ensure you have write access to the directory
   ```

## 📚 Learning Path

This example demonstrates:
1. **FastAPI Fundamentals** - Basic endpoint creation
2. **FasCraft DDA Principles** - Clean, minimal structure
3. **Configuration Management** - Environment-based settings
4. **CI/CD Setup** - GitHub Actions integration
5. **Containerization** - Docker deployment

## 🎉 Success!

Your Basic API is now running and demonstrates:
- ✅ **Clean Architecture** - DDA principles in action
- ✅ **Professional Setup** - CI/CD, Docker, configuration
- ✅ **FastAPI Best Practices** - Modern API development
- ✅ **FasCraft Integration** - Ready for scaling

**Next:** Explore the other examples to see more advanced features, or start building your own application using `fascraft generate` to add modules as needed!