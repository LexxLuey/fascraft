# E-commerce API Example

A complete e-commerce system demonstrating product management, order processing, and business logic implementation with FasCraft.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Docker (optional)

### Step-by-Step Setup

1. **Navigate to the project directory:**
   ```bash
   cd examples/ecommerce-api
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
ecommerce-api/
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
├── main.py                 # FastAPI application with e-commerce logic
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

### 2. **Business Logic Implementation**
- ✅ **Product Management** - CRUD operations with validation
- ✅ **Order Processing** - Business rules and stock management
- ✅ **Data Validation** - Input validation and error handling
- ✅ **Business Rules** - Stock checking, order calculations

### 3. **API Design Patterns**
- ✅ **RESTful Endpoints** - Standard HTTP methods
- ✅ **Query Parameters** - Filtering and pagination
- ✅ **Error Handling** - Proper HTTP status codes
- ✅ **Response Formatting** - Consistent JSON responses

### 4. **CI/CD Integration**
- ✅ **GitHub Actions** - Automated testing and deployment
- ✅ **Dependency Updates** - Automated security updates
- ✅ **Code Quality** - Linting, testing, security scanning

### 5. **Containerization**
- ✅ **Docker Support** - Multi-stage Dockerfile
- ✅ **Docker Compose** - Multi-service orchestration
- ✅ **Production Ready** - Optimized for production deployment

## 🎯 API Endpoints

### Product Management
- `GET /api/products` - List all products (with category filtering)
- `GET /api/products/{product_id}` - Get product details
- `POST /api/products` - Create new product

### Order Management
- `GET /api/orders` - List all orders
- `GET /api/orders/{order_id}` - Get order details
- `POST /api/orders` - Create new order

### System
- `GET /` - Welcome message and status
- `GET /api/v1/health` - Health check (via base router)

## 🛒 Sample Data

The API comes with pre-loaded sample data:

### Products
- **Laptop** - $999.99 (Electronics, Stock: 10)
- **Smartphone** - $599.99 (Electronics, Stock: 15)
- **Headphones** - $99.99 (Electronics, Stock: 25)
- **Coffee Mug** - $19.99 (Home, Stock: 50)

### Orders
- **Order #1** - Customer 101, 1 Laptop ($999.99, Completed)
- **Order #2** - Customer 102, 1 Smartphone + 1 Headphones ($699.98, Pending)

## 🚀 Next Steps with FasCraft

### Add New Modules
```bash
# Generate a customer module
fascraft generate customer

# Generate a payment module
fascraft generate payment

# Generate a shipping module
fascraft generate shipping
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

## 🔍 API Usage Examples

### Create a New Product
   ```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Gaming Mouse&price=79.99&category=Electronics&stock=30"
```

### Create a New Order
```bash
curl -X POST "http://localhost:8000/api/orders" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "customer_id=103&product_ids=1,3&quantities=1,2"
```

### Filter Products by Category
```bash
curl "http://localhost:8000/api/products?category=Electronics"
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

3. **Business logic errors:**
   - Check stock availability before creating orders
   - Ensure product IDs exist before referencing them
   - Validate input data format

## 📚 Learning Path

This example demonstrates:
1. **Business Logic** - Product and order management
2. **API Design** - RESTful endpoint patterns
3. **Data Validation** - Input validation and error handling
4. **Business Rules** - Stock management and order processing
5. **FasCraft DDA** - Clean architecture principles

## 🎉 Success!

Your E-commerce API is now running and demonstrates:
- ✅ **Business Logic** - Product and order management
- ✅ **API Design** - RESTful endpoint patterns
- ✅ **Data Validation** - Input validation and error handling
- ✅ **FasCraft Integration** - Ready for scaling

**Next:** Explore the Authentication API to learn about security, or the Database API to see ORM integration!