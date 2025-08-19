"""Common middleware for ecommerce-api."""

import time
from typing import Callable

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
try:
    from starlette.middleware.base import BaseHTTPMiddleware
except ImportError:
    from fastapi.middleware.base import BaseHTTPMiddleware

try:
    from .settings import get_settings
except ImportError:
    print("Configuration error: settings module not available")
    print("Please install required dependencies: pip install -r requirements.txt")
    raise


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to add timing information to responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_middleware(app):
    """Setup all middleware for the application."""
    settings = get_settings()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add timing middleware
    app.add_middleware(TimingMiddleware)