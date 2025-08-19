# Module Management Guide

Learn how to add new functionality to your FasCraft projects using the `generate` command. This guide covers module generation, customization, and integration patterns.

## 🚀 Overview

The `fascraft generate` command creates complete domain modules with:
- Database models (SQLAlchemy)
- API schemas (Pydantic)
- Business logic services
- RESTful endpoints
- Comprehensive tests
- Database migrations

## 📋 Basic Usage

### Generate a New Module
```bash
# Basic module generation
fascraft generate user

# Generate with custom path
fascraft generate user --path ./custom/modules/

# Generate multiple modules
fascraft generate user product order
```

### Command Options
```bash
fascraft generate --help
```

Available options:
- `--path`: Specify custom module path
- `--template`: Use custom module template
- `--help`: Show help message

## 🏗️ What Gets Created

### Module Structure
```
users/
├── __init__.py             # Module initialization
├── models.py               # SQLAlchemy database models
├── schemas.py              # Pydantic request/response schemas
├── services.py             # Business logic and data operations
├── routers.py              # FastAPI router with endpoints
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_models.py      # Model tests
│   ├── test_schemas.py     # Schema tests
│   ├── test_services.py    # Service tests
│   └── test_routers.py     # Router tests
└── migrations/             # Database migrations (if enabled)
    ├── __init__.py
    └── initial.py
```

## 🔧 Generated Files Explained

### `models.py` - Database Models
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from config.database import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### `schemas.py` - Pydantic Schemas
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

### `services.py` - Business Logic
```python
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: schemas.UserCreate) -> models.UserModel:
        # Hash password, validate data, create user
        db_user = models.UserModel(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user(self, user_id: int) -> Optional[models.UserModel]:
        return self.db.query(models.UserModel).filter(
            models.UserModel.id == user_id
        ).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[models.UserModel]:
        return self.db.query(models.UserModel).offset(skip).limit(limit).all()
```

### `routers.py` - API Endpoints
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from . import schemas, services

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    user_service = services.UserService(db)
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID."""
    user_service = services.UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of users with pagination."""
    user_service = services.UserService(db)
    return user_service.get_users(skip=skip, limit=limit)
```

## 🔄 Integration with Main Application

### Include Module Router
Add the generated module to your `main.py`:

```python
from fastapi import FastAPI
from routers.base import router as base_router
from users.routers import router as users_router

app = FastAPI(title="My API", version="1.0.0")

# Include base router
app.include_router(base_router, prefix="/api/v1")

# Include users module
app.include_router(users_router, prefix="/api/v1")

# Your custom endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to My API!"}
```

### Database Integration
Ensure your database configuration supports the new models:

```python
# config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings

settings = get_settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import all models to register them
from users.models import UserModel  # Add this line
```

## 🎯 Common Module Types

### User Management Module
```bash
fascraft generate user
```
**Features:**
- User registration and authentication
- Profile management
- Role-based access control
- Password hashing and validation

### Product Management Module
```bash
fascraft generate product
```
**Features:**
- Product catalog management
- Category organization
- Inventory tracking
- Price management

### Order Processing Module
```bash
fascraft generate order
```
**Features:**
- Order creation and management
- Status tracking
- Payment integration
- Order history

### Authentication Module
```bash
fascraft generate auth
```
**Features:**
- JWT token management
- Login/logout functionality
- Password reset
- Session management

## 🔧 Customization Options

### Custom Module Templates
Create custom module templates:

```bash
# Create custom template directory
mkdir -p ~/.fascraft/templates/custom_module

# Copy and modify template files
cp -r fascraft/templates/module/* ~/.fascraft/templates/custom_module/

# Use custom template
fascraft generate user --template custom_module
```

### Modify Generated Code
After generation, customize the module:

```python
# users/services.py - Add custom business logic
class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: schemas.UserCreate) -> models.UserModel:
        # Custom validation
        if self.db.query(models.UserModel).filter(
            models.UserModel.email == user.email
        ).first():
            raise ValueError("Email already registered")
        
        # Custom password hashing
        hashed_password = self._hash_password(user.password)
        user_data = user.dict()
        user_data["password"] = hashed_password
        
        db_user = models.UserModel(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def _hash_password(self, password: str) -> str:
        # Implement your password hashing logic
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
```

## 🧪 Testing Generated Modules

### Run Module Tests
```bash
# Run all tests
pytest

# Run specific module tests
pytest users/tests/

# Run with coverage
pytest --cov=users

# Run specific test file
pytest users/tests/test_services.py
```

### Test Examples
```python
# users/tests/test_services.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from users.services import UserService
from users import schemas

# Test database setup
engine = create_engine("sqlite:///./test.db")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_user():
    db = TestingSessionLocal()
    user_service = UserService(db)
    
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    
    user = user_service.create_user(user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    
    db.close()
```

## 🔄 Database Migrations

### Initialize Alembic (if not done)
```bash
# Install alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Configure alembic.ini and env.py
```

### Generate Migration for New Module
```bash
# Generate migration
alembic revision --autogenerate -m "Add user module"

# Apply migration
alembic upgrade head

# Check status
alembic current
```

## 🎯 Best Practices

### Module Naming
- Use singular, descriptive names
- Follow Python naming conventions
- Examples: `user`, `product`, `order`, `auth`

### Code Organization
- Keep business logic in services
- Use schemas for data validation
- Keep models focused on database structure
- Implement proper error handling

### Testing Strategy
- Test each layer independently
- Use fixtures for common setup
- Mock external dependencies
- Achieve high test coverage

### Security Considerations
- Validate all input data
- Implement proper authentication
- Use parameterized queries
- Sanitize user inputs

## 🔍 Troubleshooting

### Common Issues

**Module not found after generation:**
```bash
# Check module directory exists
ls -la users/

# Verify __init__.py files
find users/ -name "__init__.py"

# Check import paths in main.py
```

**Database model errors:**
```bash
# Verify model imports
python -c "from users.models import UserModel; print('OK')"

# Check database configuration
python -c "from config.database import Base; print('OK')"
```

**Router integration issues:**
```bash
# Check router import
python -c "from users.routers import router; print('OK')"

# Verify FastAPI app includes router
grep -r "include_router" main.py
```

## 📚 Next Steps

After generating modules:

1. **Review Generated Code** - Understand the structure
2. **Customize Business Logic** - Add your specific requirements
3. **Integrate with Main App** - Include routers and models
4. **Write Tests** - Ensure functionality works correctly
5. **Run Migrations** - Update database schema
6. **Test Endpoints** - Verify API functionality

## 🎉 Success Checklist

- [ ] Module generated successfully
- [ ] All files and directories created
- [ ] Models integrated with database
- [ ] Router included in main application
- [ ] Tests passing
- [ ] API endpoints working
- [ ] Database migrations applied

---

**Your module is now ready for development! 🚀**

The generated module provides a solid foundation for your domain logic. Customize the business logic, add your specific requirements, and integrate with the rest of your application. Use the comprehensive test suite to ensure everything works correctly.
