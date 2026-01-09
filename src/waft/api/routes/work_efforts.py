"""
Work efforts endpoint.
"""

from fastapi import APIRouter, Request
from pathlib import Path

from ...core.visualizer import Visualizer

router = APIRouter()


@router.get("/work-efforts")
async def get_work_efforts(request: Request):
    """
    Get work efforts information.

    Returns list of active work efforts and recent devlog entries.
    """
    project_path: Path = request.app.state.project_path
    visualizer = Visualizer(project_path)
    work_efforts = visualizer._get_work_efforts()
    devlog = visualizer._get_recent_devlog()
    return {
        "work_efforts": work_efforts,
        "devlog": devlog
    }
