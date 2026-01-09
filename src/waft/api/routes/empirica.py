"""
Empirica endpoint.
"""

from fastapi import APIRouter, Request
from pathlib import Path

from ...core.empirica import EmpiricaManager

router = APIRouter()


@router.get("/empirica")
async def get_empirica(request: Request):
    """
    Get Empirica epistemic state.

    Returns epistemic vectors, moon phase, and learning metrics.
    """
    project_path: Path = request.app.state.project_path
    empirica = EmpiricaManager(project_path)
    
    if not empirica.is_initialized():
        return {
            "initialized": False,
            "message": "Empirica not initialized"
        }
    
    context = empirica.project_bootstrap()
    if context:
        epistemic_state = context.get("epistemic_state", {})
        return {
            "initialized": True,
            "epistemic_state": epistemic_state,
            "goals": context.get("goals", [])
        }
    
    return {
        "initialized": True,
        "epistemic_state": None,
        "goals": []
    }
