"""Main FastAPI application for database-api."""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from datetime import datetime
import os

try:
    from config.settings import get_settings
    from config.middleware import setup_middleware
except ImportError as e:
    print(f"Configuration error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    raise

# Get application settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A FastAPI project generated with FasCraft - Database Integration Example",
    version=settings.app_version,
    debug=settings.debug
)

# Setup middleware
try:
    setup_middleware(app)
except Exception as e:
    print(f"Warning: Middleware setup failed: {e}")
    print("Application will run without custom middleware")

# Import base router
from routers import base_router

# Include base router (all module routers are included here)
app.include_router(base_router)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./example.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    category = Column(String, index=True)
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    total_amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": f"Welcome to {settings.app_name} - Database Integration API!", "status": "running"}

# User endpoints
@app.post("/api/users")
async def create_user(
    username: str, 
    email: str, 
    full_name: str, 
    db: Session = Depends(get_db)
):
    """Create a new user."""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = User(
        username=username,
        email=email,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "message": "User created successfully",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "created_at": db_user.created_at
        }
    }

@app.get("/api/users")
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination."""
    users = db.query(User).offset(skip).limit(limit).all()
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at
            }
            for user in users
        ],
        "total": len(users),
        "skip": skip,
        "limit": limit
    }

@app.get("/api/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

# Product endpoints
@app.post("/api/products")
async def create_product(
    name: str,
    description: str,
    price: float,
    category: str,
    stock_quantity: int = 0,
    db: Session = Depends(get_db)
):
    """Create a new product."""
    db_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock_quantity=stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return {
        "message": "Product created successfully",
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "category": db_product.category,
            "stock_quantity": db_product.stock_quantity,
            "created_at": db_product.created_at
        }
    }

@app.get("/api/products")
async def get_products(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional category filter and pagination."""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.offset(skip).limit(limit).all()
    
    return {
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "stock_quantity": product.stock_quantity,
                "created_at": product.created_at
            }
            for product in products
        ],
        "total": len(products),
        "skip": skip,
        "limit": limit,
        "category": category
    }

@app.get("/api/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock_quantity": product.stock_quantity,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

# Order endpoints
@app.post("/api/orders")
async def create_order(
    user_id: int,
    total_amount: float,
    status: str = "pending",
    db: Session = Depends(get_db)
):
    """Create a new order."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status=status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return {
        "message": "Order created successfully",
        "order": {
            "id": db_order.id,
            "user_id": db_order.user_id,
            "total_amount": db_order.total_amount,
            "status": db_order.status,
            "created_at": db_order.created_at
        }
    }

@app.get("/api/orders")
async def get_orders(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all orders with optional user filter and pagination."""
    query = db.query(Order)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    orders = query.offset(skip).limit(limit).all()
    
    return {
        "orders": [
            {
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at
            }
            for order in orders
        ],
        "total": len(orders),
        "skip": skip,
        "limit": limit,
        "user_id": user_id
    }

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }

# Database statistics
@app.get("/api/stats")
async def get_database_stats(db: Session = Depends(get_db)):
    """Get database statistics."""
    user_count = db.query(User).count()
    product_count = db.query(Product).count()
    order_count = db.query(Order).count()
    
    # Get category distribution
    categories = db.query(Product.category).distinct().all()
    category_stats = {}
    for category in categories:
        count = db.query(Product).filter(Product.category == category[0]).count()
        category_stats[category[0]] = count
    
    return {
        "total_users": user_count,
        "total_products": product_count,
        "total_orders": order_count,
        "categories": category_stats,
        "database": "SQLite",
        "status": "connected"
    }

# Health check is now handled by base router at /api/v1/health

# Database setup note:
# This example uses SQLite for simplicity
# For production, consider using PostgreSQL or MySQL
# The database file will be created automatically at ./example.db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)