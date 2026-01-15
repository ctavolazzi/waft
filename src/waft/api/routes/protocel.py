"""
ProtoCel API endpoints for self-contained evolving cells.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.protocel import ProtoCelSystem, ProtoCel
from waft.being import BeingSystem

router = APIRouter()


# Request models
class CreateProtoCelRequest(BaseModel):
    name: Optional[str] = Field(default=None, description="Optional name for the ProtoCel")
    description: Optional[str] = Field(default=None, description="Optional description")


class ObserveBeingRequest(BaseModel):
    being_id: str = Field(description="ID of the being to observe")
    fetch_data: bool = Field(default=True, description="Whether to fetch being data")


class InteractWithBeingRequest(BaseModel):
    being_id: str = Field(description="ID of the being to interact with")
    interaction_type: str = Field(description="Type of interaction")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Optional interaction data")


@router.post("/create")
async def create_protocel(request: CreateProtoCelRequest) -> Dict[str, Any]:
    """
    Create a new ProtoCel.
    
    Args:
        request: Creation request with optional name and description
        
    Returns:
        ProtoCel data
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel = system.create_protocel(
            name=request.name,
            description=request.description
        )
        
        return {
            "protocel_id": protocel.protocel_id,
            "name": protocel.name,
            "description": protocel.description,
            "state": protocel.state.value,
            "cell_path": str(protocel.cell_path),
            "created_at": protocel.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_protocels() -> Dict[str, Any]:
    """
    List all ProtoCels.
    
    Returns:
        List of ProtoCel IDs
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel_ids = system.list_protocels()
        
        return {
            "protocels": protocel_ids,
            "count": len(protocel_ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{protocel_id}")
async def get_protocel(protocel_id: str) -> Dict[str, Any]:
    """
    Get ProtoCel by ID.
    
    Args:
        protocel_id: ProtoCel ID
        
    Returns:
        ProtoCel state
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel = system.get_protocel(protocel_id)
        
        return protocel.get_state()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{protocel_id}/observe")
async def observe_being(
    protocel_id: str,
    request: ObserveBeingRequest
) -> Dict[str, Any]:
    """
    Observe a being from the ProtoCel.
    
    Args:
        protocel_id: ProtoCel ID
        request: Observation request
        
    Returns:
        Observation result
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel = system.get_protocel(protocel_id)
        
        being_data = None
        if request.fetch_data:
            # Fetch being data from BeingSystem
            being_system = BeingSystem(project_path=project_root)
            try:
                being = being_system._load_being(request.being_id)
                being_data = {
                    "being_id": being.being_id,
                    "reality_id": being.reality_id,
                    "state": being.state.value if hasattr(being.state, 'value') else str(being.state),
                    "skills": being.skills,
                    "fitness": being.fitness,
                    "generation": being.generation if hasattr(being, 'generation') else 0
                }
            except Exception:
                # Being not found, continue without data
                pass
        
        result = protocel.observe_being(request.being_id, being_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{protocel_id}/interact")
async def interact_with_being(
    protocel_id: str,
    request: InteractWithBeingRequest
) -> Dict[str, Any]:
    """
    Interact with a being from the ProtoCel.
    
    Args:
        protocel_id: ProtoCel ID
        request: Interaction request
        
    Returns:
        Interaction result
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel = system.get_protocel(protocel_id)
        
        result = protocel.interact_with_being(
            request.being_id,
            request.interaction_type,
            request.data
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{protocel_id}/evolve")
async def evolve_protocel(protocel_id: str) -> Dict[str, Any]:
    """
    Manually trigger ProtoCel evolution.
    
    Args:
        protocel_id: ProtoCel ID
        
    Returns:
        Evolution result
    """
    try:
        system = ProtoCelSystem(project_path=project_root)
        protocel = system.get_protocel(protocel_id)
        
        result = protocel.evolve()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
