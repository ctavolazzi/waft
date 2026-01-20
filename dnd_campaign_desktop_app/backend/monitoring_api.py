"""
Monitoring API Endpoints

Exposes monitoring data via FastAPI endpoints.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from monitoring import get_monitoring

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/startup-data")
async def get_startup_data() -> dict[str, Any]:
    """Get first-time startup data."""
    monitoring = get_monitoring()
    if not monitoring:
        raise HTTPException(status_code=503, detail="Monitoring not initialized")

    startup_data = monitoring.get_startup_data()
    if not startup_data:
        raise HTTPException(status_code=404, detail="No startup data available")

    return startup_data


@router.get("/is-first-startup")
async def is_first_startup() -> dict[str, bool]:
    """Check if this is the first startup."""
    monitoring = get_monitoring()
    if not monitoring:
        return {"is_first_startup": False}

    return {"is_first_startup": monitoring.is_first_startup()}


@router.get("/stats")
async def get_monitoring_stats() -> dict[str, Any]:
    """Get monitoring statistics."""
    monitoring = get_monitoring()
    if not monitoring:
        raise HTTPException(status_code=503, detail="Monitoring not initialized")

    # Count events
    event_count = 0
    if monitoring.events_file.exists():
        with open(monitoring.events_file) as f:
            event_count = sum(1 for _ in f)

    # Count metrics
    metric_count = 0
    if monitoring.metrics_file.exists():
        with open(monitoring.metrics_file) as f:
            metric_count = sum(1 for _ in f)

    return {
        "is_first_startup": monitoring.is_first_startup(),
        "has_startup_data": monitoring.startup_data_file.exists(),
        "event_count": event_count,
        "metric_count": metric_count,
        "monitoring_dir": str(monitoring.monitoring_dir),
    }
