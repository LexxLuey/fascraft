"""Custom exceptions for database-api."""

from fastapi import HTTPException, status


class FasCraftException(HTTPException):
    """Base exception for FasCraft applications."""
    
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ValidationError(FasCraftException):
    """Raised when data validation fails."""
    
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class NotFoundError(FasCraftException):
    """Raised when a resource is not found."""
    
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND
        )


class ConflictError(FasCraftException):
    """Raised when there's a conflict with existing data."""
    
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT
        )