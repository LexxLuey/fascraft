# Database API Example

A complete database integration example demonstrating SQLAlchemy ORM, SQLite database, CRUD operations, relationships, and data persistence with FasCraft.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (recommended) or pip
- Docker (optional)

### Step-by-Step Setup

1. **Navigate to the project directory:**
   ```bash
   cd examples/database-api
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
database-api/
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
├── main.py                 # FastAPI application with database integration
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

### 2. **Database Integration**
- ✅ **SQLAlchemy ORM** - Modern Python ORM
- ✅ **SQLite Database** - File-based database (easy to start)
- ✅ **Model Definitions** - User, Product, Order models
- ✅ **Database Relationships** - Foreign keys and associations

### 3. **Data Operations**
- ✅ **CRUD Operations** - Create, Read, Update, Delete
- ✅ **Data Validation** - Input validation and error handling
- ✅ **Query Optimization** - Efficient database queries
- ✅ **Transaction Management** - Database transaction handling

### 4. **API Design**
- ✅ **RESTful Endpoints** - Standard HTTP methods
- ✅ **Query Parameters** - Filtering and pagination
- ✅ **Response Formatting** - Consistent JSON responses
- ✅ **Error Handling** - Proper HTTP status codes

### 5. **CI/CD Integration**
- ✅ **GitHub Actions** - Automated testing and deployment
- ✅ **Dependency Updates** - Automated security updates
- ✅ **Code Quality** - Linting, testing, security scanning

## 🎯 API Endpoints

### User Management
- `GET /api/users` - List all users
- `GET /api/users/{user_id}` - Get user details
- `POST /api/users` - Create new user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Product Management
- `GET /api/products` - List all products
- `GET /api/products/{product_id}` - Get product details
- `POST /api/products` - Create new product
- `PUT /api/products/{product_id}` - Update product
- `DELETE /api/products/{product_id}` - Delete product

### Order Management
- `GET /api/orders` - List all orders
- `GET /api/orders/{order_id}` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/{order_id}` - Update order
- `DELETE /api/orders/{order_id}` - Delete order

### System & Analytics
- `GET /` - Welcome message and status
- `GET /api/v1/health` - Health check (via base router)
- `GET /api/stats` - Database statistics and analytics

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

## 🛒 Sample Data

The API comes with pre-loaded sample data:

### Users
- **John Doe** - john@example.com
- **Jane Smith** - jane@example.com
- **Bob Johnson** - bob@example.com

### Products
- **Laptop** - $999.99 (Electronics, Stock: 10)
- **Smartphone** - $599.99 (Electronics, Stock: 15)
- **Headphones** - $99.99 (Electronics, Stock: 25)
- **Coffee Mug** - $19.99 (Home, Stock: 50)

### Orders
- **Order #1** - John Doe, 1 Laptop ($999.99, Completed)
- **Order #2** - Jane Smith, 1 Smartphone + 1 Headphones ($699.98, Pending)

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

### 1. Create a New User
```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "full_name": "New User"
  }'
```

### 2. Create a New Product
   ```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Mouse",
    "description": "High-performance gaming mouse",
    "price": 79.99,
    "stock": 30,
    "category": "Electronics"
  }'
```

### 3. Create a New Order
   ```bash
curl -X POST "http://localhost:8000/api/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2,
    "total_price": 1999.98
  }'
```

### 4. Get Database Statistics
   ```bash
curl "http://localhost:8000/api/stats"
```

**Response:**
```json
{
  "total_users": 3,
  "total_products": 4,
  "total_orders": 2,
  "total_revenue": 1699.97,
  "top_product": "Laptop",
  "most_active_user": "John Doe"
}
```

### 5. Filter Products by Category
   ```bash
curl "http://localhost:8000/api/products?category=Electronics"
```

### 6. Update Product Stock
```bash
curl -X PUT "http://localhost:8000/api/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock": 8,
    "category": "Electronics"
  }'
```

## 🗄️ Database Operations

### SQLAlchemy Features Demonstrated
- **Model Definitions** - SQLAlchemy declarative base
- **Relationships** - Foreign key associations
- **Query Building** - Filter, sort, and paginate
- **Transaction Management** - Database session handling
- **Data Validation** - Model-level validation

### Database Configuration
- **Engine Setup** - SQLite database engine
- **Session Management** - Database session lifecycle
- **Connection Pooling** - Efficient connection management
- **Migration Ready** - Alembic integration prepared

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

3. **Database errors:**
   - Check database file permissions
   - Ensure SQLite is supported
   - Verify model imports are correct

4. **Data validation errors:**
   - Check required field values
   - Verify data types (e.g., price as decimal)
   - Ensure unique constraints are met

## 📚 Learning Path

This example demonstrates:
1. **Database Integration** - SQLAlchemy ORM setup
2. **Data Modeling** - Table relationships and constraints
3. **CRUD Operations** - Complete data lifecycle
4. **API Design** - RESTful database endpoints
5. **FasCraft DDA** - Clean architecture principles

## 🚀 Production Considerations

### Database Scaling
- **SQLite to PostgreSQL** - For production workloads
- **Connection Pooling** - Optimize database connections
- **Indexing** - Add database indexes for performance
- **Backup Strategy** - Regular database backups

### Performance Optimization
- **Query Optimization** - Use database indexes
- **Pagination** - Implement result pagination
- **Caching** - Add Redis or similar caching
- **Monitoring** - Database performance monitoring

## 🎉 Success!

Your Database API is now running and demonstrates:
- ✅ **Database Integration** - SQLAlchemy ORM with SQLite
- ✅ **Data Operations** - Complete CRUD functionality
- ✅ **API Design** - RESTful database endpoints
- ✅ **FasCraft Integration** - Ready for scaling

**Next:** Start building your own database-driven application using `fascraft generate` to add modules as needed!