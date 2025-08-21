"""Main FastAPI application for ecommerce-api."""

from fastapi import FastAPI, HTTPException

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
    description="A FastAPI project generated with FasCraft - E-commerce API Example",
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

# Sample data for demonstration
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics",
        "stock": 10,
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 599.99,
        "category": "Electronics",
        "stock": 15,
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 99.99,
        "category": "Electronics",
        "stock": 25,
    },
    {"id": 4, "name": "Coffee Mug", "price": 19.99, "category": "Home", "stock": 50},
]

orders = [
    {
        "id": 1,
        "customer_id": 101,
        "products": [{"product_id": 1, "quantity": 1}],
        "total": 999.99,
        "status": "completed",
    },
    {
        "id": 2,
        "customer_id": 102,
        "products": [
            {"product_id": 2, "quantity": 1},
            {"product_id": 3, "quantity": 1},
        ],
        "total": 699.98,
        "status": "pending",
    },
]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name} - E-commerce API!",
        "status": "running",
    }


@app.get("/api/products")
async def get_products(category: str = None):
    """Get all products or filter by category."""
    if category:
        filtered_products = [
            p for p in products if p["category"].lower() == category.lower()
        ]
        return {"products": filtered_products, "count": len(filtered_products)}
    return {"products": products, "count": len(products)}


@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID."""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/products")
async def create_product(name: str, price: float, category: str, stock: int = 0):
    """Create a new product."""
    new_id = max(p["id"] for p in products) + 1
    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "category": category,
        "stock": stock,
    }
    products.append(new_product)
    return {"message": "Product created successfully", "product": new_product}


@app.get("/api/orders")
async def get_orders():
    """Get all orders."""
    return {"orders": orders, "count": len(orders)}


@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    """Get a specific order by ID."""
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/api/orders")
async def create_order(customer_id: int, product_ids: list[int], quantities: list[int]):
    """Create a new order."""
    if len(product_ids) != len(quantities):
        raise HTTPException(
            status_code=400, detail="Product IDs and quantities must match"
        )

    order_items = []
    total = 0.0

    for i, product_id in enumerate(product_ids):
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {product_id} not found"
            )

        quantity = quantities[i]
        if product["stock"] < quantity:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for product {product_id}"
            )

        order_items.append({"product_id": product_id, "quantity": quantity})
        total += product["price"] * quantity

    new_order = {
        "id": max(o["id"] for o in orders) + 1,
        "customer_id": customer_id,
        "products": order_items,
        "total": round(total, 2),
        "status": "pending",
    }

    orders.append(new_order)
    return {"message": "Order created successfully", "order": new_order}


# Health check is now handled by base router at /api/v1/health

# Database setup note:
# After creating models, run 'alembic init alembic' to initialize migrations
# Then configure alembic/env.py to import your models and use your database URL
# See README.md for detailed setup instructions

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
