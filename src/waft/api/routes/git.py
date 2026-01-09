"""
Git status endpoint.
"""

from fastapi import APIRouter, Request
from pathlib import Path

from ...core.visualizer import Visualizer

router = APIRouter()


@router.get("/git")
async def get_git_status(request: Request):
    """
    Get git status information.

    Returns detailed git status including branch, uncommitted files,
    commits ahead/behind, and recent commit history.
    """
    project_path: Path = request.app.state.project_path
    visualizer = Visualizer(project_path)
    git_status = visualizer._get_git_status()
    return git_status
