"""Main FastAPI application for basic-api."""

from fastapi import FastAPI

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
    description="A FastAPI project generated with FasCraft - Basic API Example",
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

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": f"Hello from {settings.app_name}!", "status": "running"}

@app.get("/api/items")
async def get_items():
    """Get a list of sample items."""
    return {
        "items": [
            {"id": 1, "name": "Sample Item 1", "description": "A basic item"},
            {"id": 2, "name": "Sample Item 2", "description": "Another basic item"},
            {"id": 3, "name": "Sample Item 3", "description": "Yet another item"}
        ]
    }

@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID."""
    if item_id < 1 or item_id > 3:
        return {"error": "Item not found"}, 404
    
    items = {
        1: {"id": 1, "name": "Sample Item 1", "description": "A basic item"},
        2: {"id": 2, "name": "Sample Item 2", "description": "Another basic item"},
        3: {"id": 3, "name": "Sample Item 3", "description": "Yet another item"}
    }
    return items[item_id]

@app.post("/api/items")
async def create_item(name: str, description: str = ""):
    """Create a new item."""
    return {
        "message": "Item created successfully",
        "item": {
            "id": 4,
            "name": name,
            "description": description
        }
    }

# Health check is now handled by base router at /api/v1/health

# Database setup note:
# After creating models, run 'alembic init alembic' to initialize migrations
# Then configure alembic/env.py to import your models and use your database URL
# See README.md for detailed setup instructions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)