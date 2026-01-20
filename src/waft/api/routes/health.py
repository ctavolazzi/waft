"""
Health check endpoint for WAFT API.
"""

from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status with timestamp
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "service": "WAFT API"}
