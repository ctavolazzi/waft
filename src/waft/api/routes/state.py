"""
Project state endpoint - main data gathering endpoint.
"""

from fastapi import APIRouter, Request
from pathlib import Path
from datetime import datetime

from ...core.visualizer import Visualizer

router = APIRouter()


@router.get("/health")
async def get_health():
    """
    Health check endpoint.

    Returns API health status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "waft-visualizer-api"
    }


@router.get("/state")
async def get_state(request: Request):
    """
    Get complete project state.

    Returns all project information including git status, _pyrite structure,
    gamification stats, work efforts, and devlog.
    """
    project_path: Path = request.app.state.project_path
    visualizer = Visualizer(project_path)
    state = visualizer.gather_state()
    return state
