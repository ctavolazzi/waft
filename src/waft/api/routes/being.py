"""
Being API endpoints for testing Being system with Empirica integration.
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.being import BeingSystem, Being
from waft.reality import RealitySystem

router = APIRouter()


@router.post("/spawn")
async def spawn_being(
    reality_id: str = "test_reality",
    parent_being_id: Optional[str] = None,
    initial_skills: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Spawn a new Being (first Being will use Empirica).
    
    Args:
        reality_id: Reality to spawn into
        parent_being_id: Optional parent being ID
        initial_skills: Optional initial skills dict
    
    Returns:
        Being data with Empirica session info if first Being
    """
    try:
        being_system = BeingSystem(project_path=project_root)
        being = being_system.spawn_being(
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            initial_skills=initial_skills or {}
        )
        
        return {
            "being_id": being.being_id,
            "reality_id": being.reality_id,
            "parent_being_id": being.parent_being_id,
            "lifetimes": being.lifetimes,
            "is_first_being": being._is_first_being,
            "empirica_session_id": being.empirica_session_id,
            "empirica_enabled": being.empirica_manager is not None,
            "skills": being.skills,
            "stamina": being.stamina,
            "will_to_live": being.will_to_live,
            "decision_fatigue": being.decision_fatigue,
            "personality_type": being.personality_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{being_id}/decision")
async def make_decision(
    being_id: str,
    decision_type: Optional[str] = None,
    stamina_cost: float = 5.0
) -> Dict[str, Any]:
    """
    Make a decision for a Being (uses Empirica if first Being).
    
    Args:
        being_id: Being ID
        decision_type: Optional decision type (if None, BeingDecisionSystem chooses)
        stamina_cost: Stamina cost for decision
    
    Returns:
        Decision result with Empirica gate info
    """
    try:
        being_system = BeingSystem(project_path=project_root)
        being = being_system._load_being(being_id)
        
        if decision_type:
            # Direct decision
            result = being.make_decision(decision_type, stamina_cost)
        else:
            # Use BeingDecisionSystem
            from waft.core.being_decisions import BeingDecisionSystem
            decision_system = BeingDecisionSystem()
            result = await decision_system.make_decision(being)
        
        return {
            "decision_type": result.get("decision_type"),
            "experience": result.get("experience"),
            "decision_fatigue_remaining": result.get("decision_fatigue_remaining"),
            "stamina_remaining": result.get("stamina_remaining", being.stamina),
            "stamina_depleted": result.get("stamina_depleted", being.is_stamina_depleted()),
            "empirica_gate": result.get("empirica_gate"),
            "empirica_enabled": being.empirica_manager is not None,
            "being_state": {
                "stamina": being.stamina,
                "stamina_max": being.stamina_max,
                "will_to_live": being.will_to_live,
                "decision_fatigue": being.decision_fatigue,
                "is_sleeping": being.is_sleeping
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{being_id}")
async def get_being(being_id: str) -> Dict[str, Any]:
    """
    Get Being information.
    
    Args:
        being_id: Being ID
    
    Returns:
        Being data
    """
    try:
        being_system = BeingSystem(project_path=project_root)
        being = being_system._load_being(being_id)
        
        return {
            "being_id": being.being_id,
            "reality_id": being.reality_id,
            "parent_being_id": being.parent_being_id,
            "lifetimes": being.lifetimes,
            "is_first_being": being._is_first_being,
            "empirica_session_id": being.empirica_session_id,
            "empirica_enabled": being.empirica_manager is not None,
            "skills": being.skills,
            "stamina": being.stamina,
            "stamina_max": being.stamina_max,
            "will_to_live": being.will_to_live,
            "decision_fatigue": being.decision_fatigue,
            "decision_quota_max": being.decision_quota_max,
            "personality_type": being.personality_type,
            "is_sleeping": being.is_sleeping,
            "memories_count": len(being.memories),
            "lessons_count": len(being.lessons_learned)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{being_id}/decisions/make-multiple")
async def make_multiple_decisions(
    being_id: str,
    count: int = 5
) -> Dict[str, Any]:
    """
    Make multiple decisions for a Being (for testing).
    
    Args:
        being_id: Being ID
        count: Number of decisions to make
    
    Returns:
        List of decision results
    """
    try:
        being_system = BeingSystem(project_path=project_root)
        being = being_system._load_being(being_id)
        
        from waft.core.being_decisions import BeingDecisionSystem
        decision_system = BeingDecisionSystem()
        
        results = []
        for i in range(count):
            try:
                result = await decision_system.make_decision(being)
                results.append({
                    "decision_number": i + 1,
                    "decision_type": result.get("decision_type"),
                    "experience": result.get("experience"),
                    "empirica_gate": result.get("empirica_gate"),
                    "stamina_remaining": being.stamina,
                    "decision_fatigue_remaining": being.decision_fatigue
                })
            except ValueError as e:
                # Being needs to sleep or can't make decisions
                results.append({
                    "decision_number": i + 1,
                    "error": str(e),
                    "stamina_remaining": being.stamina,
                    "decision_fatigue_remaining": being.decision_fatigue
                })
                break
        
        return {
            "being_id": being_id,
            "decisions_made": len(results),
            "results": results,
            "final_state": {
                "stamina": being.stamina,
                "will_to_live": being.will_to_live,
                "decision_fatigue": being.decision_fatigue,
                "is_sleeping": being.is_sleeping
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
