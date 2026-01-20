"""
Standard API response models.
"""

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: str  # Error type/code
    message: str  # Human-readable message
    detail: dict[str, Any] | None = None  # Additional context
    timestamp: str  # ISO format

    class Config:
        json_schema_extra = {
            "example": {
                "error": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "detail": {"field_name": ["Error message 1", "Error message 2"]},
                "timestamp": "2026-01-16T20:19:00",
            }
        }


# Error codes
class ErrorCodes:
    """Standard error codes."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    BAD_REQUEST = "BAD_REQUEST"
