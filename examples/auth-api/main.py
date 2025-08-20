"""Main FastAPI application for auth-api."""

import hashlib
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

try:
    from config.middleware import setup_middleware
    from config.settings import get_settings
    from routers import base_router
except ImportError as e:
    print(f"Configuration error: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    raise

# Get application settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A FastAPI project generated with FasCraft - Auth API Example",
    version=settings.app_version,
    debug=settings.debug,
)

# Setup middleware
try:
    setup_middleware(app)
except Exception as e:
    print(f"Warning: Middleware setup failed: {e}")
    print("Application will run without custom middleware")

# Include base router (all module routers are included here)
app.include_router(base_router)

# Security
security = HTTPBearer()

# Sample data for demonstration (in production, use a real database)
users = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": hashlib.sha256(b"admin123").hexdigest(),
        "is_active": True,
        "role": "admin",
    },
    {
        "id": 2,
        "username": "user1",
        "email": "user1@example.com",
        "hashed_password": hashlib.sha256(b"user123").hexdigest(),
        "is_active": True,
        "role": "user",
    },
]

# JWT configuration (in production, use environment variables)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    except jwt.JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name} - Authentication API!",
        "status": "running",
    }


@app.post("/api/auth/register")
async def register_user(username: str, email: str, password: str):
    """Register a new user."""
    # Check if username already exists
    if any(u["username"] == username for u in users):
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email already exists
    if any(u["email"] == email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = {
        "id": max(u["id"] for u in users) + 1,
        "username": username,
        "email": email,
        "hashed_password": hashlib.sha256(password.encode()).hexdigest(),
        "is_active": True,
        "role": "user",
    }
    users.append(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user["id"],
            "username": new_user["username"],
            "email": new_user["email"],
            "role": new_user["role"],
        },
    }


@app.post("/api/auth/login")
async def login(username: str, password: str):
    """Login user and return access token."""
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not user["is_active"]:
        raise HTTPException(status_code=400, detail="User account is disabled")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user["hashed_password"] != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        },
    }


@app.get("/api/auth/me")
async def get_current_user(username: str = Depends(verify_token)):
    """Get current user information."""
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
    }


@app.get("/api/auth/users")
async def get_users(current_user: str = Depends(verify_token)):
    """Get all users (admin only)."""
    user = next((u for u in users if u["username"] == current_user), None)
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {
        "users": [
            {
                "id": u["id"],
                "username": u["username"],
                "email": u["email"],
                "role": u["role"],
                "is_active": u["is_active"],
            }
            for u in users
        ]
    }


@app.post("/api/auth/refresh")
async def refresh_token(current_user: str = Depends(verify_token)):
    """Refresh access token."""
    user = next((u for u in users if u["username"] == current_user), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


# Health check is now handled by base router at /api/v1/health

# Database setup note:
# After creating models, run 'alembic init alembic' to initialize migrations
# Then configure alembic/env.py to import your models and use your database URL
# See README.md for detailed setup instructions

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
