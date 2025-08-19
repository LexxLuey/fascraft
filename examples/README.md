# FasCraft Examples

Welcome to the FasCraft examples directory! This collection demonstrates how to build scalable, maintainable FastAPI applications using FasCraft's Domain-Driven Architecture (DDA) approach.

## 🎯 What You'll Learn

Each example showcases different aspects of modern API development while maintaining FasCraft's clean, minimal structure. You'll learn:

- **Domain-Driven Architecture** - Clean, scalable project structure
- **FastAPI Best Practices** - Modern API development patterns
- **FasCraft CLI Usage** - Project generation and module management
- **Professional Setup** - CI/CD, Docker, configuration management
- **Real-world Scenarios** - Business logic, security, database integration

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Docker (optional)

### Choose Your Example

1. **Basic API** - Start here for fundamentals
2. **E-commerce API** - Business logic and validation
3. **Authentication API** - Security and user management
4. **Database API** - ORM integration and data persistence

## 📁 Example Projects

### 1. [Basic API](./basic-api/) - **Start Here!**
**Perfect for beginners** - Demonstrates core FasCraft features with simple CRUD operations.

**What you'll learn:**
- ✅ FastAPI fundamentals
- ✅ FasCraft DDA principles
- ✅ Configuration management
- ✅ CI/CD setup
- ✅ Containerization

**Key Features:**
- Basic item management endpoints
- Clean project structure
- GitHub Actions integration
- Docker deployment ready

---

### 2. [E-commerce API](./ecommerce-api/) - **Business Logic**
**Intermediate level** - Shows how to implement business rules and complex data relationships.

**What you'll learn:**
- ✅ Business logic implementation
- ✅ Data validation patterns
- ✅ RESTful API design
- ✅ Error handling strategies
- ✅ Sample data management

**Key Features:**
- Product and order management
- Stock validation
- Business rule enforcement
- Query parameter filtering

---

### 3. [Authentication API](./auth-api/) - **Security First**
**Advanced security** - Demonstrates JWT authentication, role-based access control, and security best practices.

**What you'll learn:**
- ✅ JWT token management
- ✅ Password security (hashing)
- ✅ Role-based access control
- ✅ Protected endpoints
- ✅ Security best practices

**Key Features:**
- User registration and login
- JWT token authentication
- Admin and user roles
- Secure password handling

---

### 4. [Database API](./database-api/) - **Data Persistence**
**Database integration** - Complete ORM setup with SQLAlchemy, relationships, and data operations.

**What you'll learn:**
- ✅ SQLAlchemy ORM integration
- ✅ Database relationships
- ✅ CRUD operations
- ✅ Data validation
- ✅ Database analytics

**Key Features:**
- SQLite database with SQLAlchemy
- User, Product, Order models
- Foreign key relationships
- Database statistics endpoint

## 🔧 FasCraft Features Demonstrated

### Core Architecture
- **Domain-Driven Design** - Clean, minimal project structure
- **Modular Generation** - Add features as needed with `fascraft generate`
- **Configuration Management** - Environment-based settings
- **Router Foundation** - Scalable endpoint organization

### Development Tools
- **CI/CD Integration** - GitHub Actions workflows
- **Dependency Management** - Poetry and requirements files
- **Code Quality** - Linting, testing, security scanning
- **Containerization** - Docker and Docker Compose

### Professional Features
- **Health Checks** - System monitoring endpoints
- **Error Handling** - Consistent error responses
- **API Documentation** - Auto-generated Swagger/ReDoc
- **Security Ready** - Authentication and authorization patterns

## 🚀 Getting Started with Any Example

### Step 1: Choose Your Example
```bash
cd examples/[example-name]
# e.g., cd examples/basic-api
```

### Step 2: Install Dependencies
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
# Using Poetry
poetry run python main.py

# Or directly
python main.py
```

### Step 4: Explore the API
- **Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🎓 Learning Path

### Beginner Path
1. **Start with Basic API** - Learn fundamentals
2. **Explore E-commerce API** - Understand business logic
3. **Study Authentication API** - Master security concepts
4. **Dive into Database API** - Learn data persistence

### Advanced Path
1. **Customize examples** - Modify endpoints and logic
2. **Add new modules** - Use `fascraft generate <module_name>`
3. **Extend functionality** - Add new features and endpoints
4. **Deploy to production** - Use Docker and CI/CD

## 🛠️ FasCraft CLI Commands

### Project Management
```bash
# Create new project
fascraft new my-project

# Generate new module
fascraft generate user

# Analyze project structure
fascraft analyze

# Check dependencies
fascraft dependencies list
```

### Module Generation
```bash
# Generate user module
fascraft generate user

# Generate product module
fascraft generate product

# Generate order module
fascraft generate order

# Generate custom module
fascraft generate my-custom-module
```

## 🔍 Understanding the DDA Approach

### What Makes FasCraft Different

**Traditional MVC Approach:**
```
project/
├── models/          # ❌ Pre-created (often empty)
├── schemas/         # ❌ Pre-created (often empty)
├── services/        # ❌ Pre-created (often empty)
└── tests/           # ❌ Pre-created (often empty)
```

**FasCraft DDA Approach:**
```
project/
├── config/          # ✅ Essential configuration
├── routers/         # ✅ Router foundation
└── .github/         # ✅ CI/CD ready
```

### Why This Matters

1. **Clean Start** - No unnecessary empty folders
2. **On-Demand Growth** - Add modules when you need them
3. **Focused Development** - Work on what matters
4. **Scalable Architecture** - Grow organically with your needs

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

1. **Port conflicts:**
   ```bash
   # Change port in main.py
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

2. **Import errors:**
   ```bash
   # Ensure dependencies are installed
   pip install -r requirements.txt
   ```

3. **Permission issues:**
   ```bash
   # Check file permissions
   # Ensure write access to project directory
   ```

## 📚 Next Steps

### After Running Examples

1. **Modify endpoints** - Change logic and responses
2. **Add new features** - Extend functionality
3. **Create your own project** - Use `fascraft new`
4. **Generate modules** - Use `fascraft generate`
5. **Deploy to production** - Use Docker and CI/CD

### Advanced Topics

- **Database migrations** - Alembic integration
- **Testing strategies** - Unit and integration tests
- **Performance optimization** - Caching and query optimization
- **Security hardening** - Rate limiting, CORS, HTTPS
- **Monitoring and logging** - Application observability

## 🎉 Success!

You now have:
- ✅ **4 complete, functional examples** demonstrating different aspects of API development
- ✅ **Step-by-step setup instructions** for each example
- ✅ **All major FasCraft features** showcased and explained
- ✅ **Professional-grade setup** with CI/CD, Docker, and configuration
- ✅ **DDA principles** in action - clean, scalable architecture

**Ready to build?** Start with the Basic API example, then explore the others to see how FasCraft scales with your needs!

## 🤝 Contributing

Found an issue or have a suggestion? The examples are designed to be:
- **Easy to modify** - Simple, clear code
- **Well-documented** - Comprehensive READMEs
- **Production-ready** - Professional setup and configuration

Feel free to customize, extend, and improve these examples for your own projects!
