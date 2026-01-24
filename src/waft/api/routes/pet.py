"""
Pet API endpoints for the WAFT Pet System.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.being import BeingState, BeingSystem
from waft.karma import KarmaMerchant
from waft.pet.card_generator import PetCardGenerator
from waft.pet.emotion_adapter import EmotionAdapter
from waft.pet.pet_being import PetBeing, load_latest_pet, load_pet, pet_realm_path, save_pet

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message sent to pet")


class ActionRequest(BaseModel):
    action: str = Field(..., min_length=1, description="Action requested for pet")


class FeedRequest(BaseModel):
    amount: float = Field(default=10.0, description="Pleasure/affection boost amount")


def _get_or_create_pet(pet_id: str | None = None) -> PetBeing:
    if pet_id:
        try:
            return load_pet(project_root, pet_id)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Pet not found: {pet_id}")

    pet = load_latest_pet(project_root)
    if pet:
        return pet

    being_system = BeingSystem(project_path=project_root)
    being = being_system.spawn_being(reality_id="waft_pet")
    pet = PetBeing.from_dict(being.to_dict())
    save_pet(pet, project_root)
    return pet


def _pet_status(pet: PetBeing) -> dict[str, Any]:
    karma_data = KarmaMerchant(project_path=project_root).access_akasha(pet.soul_id or pet.being_id)
    return {
        "pet_id": pet.being_id,
        "name": pet.display_name,
        "emotion": EmotionAdapter.get_emotion(pet),
        "visual_state": pet.visual_state,
        "affection": pet.affection,
        "last_interaction": pet.last_interaction,
        "lifetimes": pet.lifetimes,
        "state": pet.state.value,
        "stats": {
            "pleasure": pet.pleasure,
            "pain": pet.pain,
            "will_to_live": pet.will_to_live,
            "decision_fatigue": pet.decision_fatigue,
            "is_sleeping": pet.is_sleeping,
        },
        "karma": {
            "total": karma_data.get("total_karma", 0.0),
            "lifetimes": len(karma_data.get("lifetimes", [])),
        },
    }


@router.get("/status")
async def pet_status(pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        return _pet_status(pet)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/chat")
async def pet_chat(request: ChatRequest, pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        pet.record_memory(request.message, memory_type="chat")
        pet.pleasure = min(100.0, pet.pleasure + 2.0)
        pet.affection = min(100.0, pet.affection + 1.0)
        pet.touch()
        save_pet(pet, project_root)

        response = f"{pet.display_name} chirps softly in response."
        return {
            "pet_id": pet.being_id,
            "response": response,
            "status": _pet_status(pet),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/action")
async def pet_action(request: ActionRequest, pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        pet.visual_state = request.action
        pet.record_memory(request.action, memory_type="action")
        pet.touch()
        save_pet(pet, project_root)

        return {
            "pet_id": pet.being_id,
            "action": request.action,
            "status": _pet_status(pet),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/feed")
async def pet_feed(request: FeedRequest, pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        pet.pleasure = min(100.0, pet.pleasure + request.amount)
        pet.affection = min(100.0, pet.affection + (request.amount / 2.0))
        pet.record_memory(f"Fed {request.amount}", memory_type="feed")
        pet.touch()
        save_pet(pet, project_root)

        return {
            "pet_id": pet.being_id,
            "status": _pet_status(pet),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/cards")
async def pet_cards(pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        generator = PetCardGenerator(project_path=project_root)
        return generator.generate_cards_for_pet(pet)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/reincarnate")
async def pet_reincarnate(pet_id: str | None = None) -> dict[str, Any]:
    try:
        pet = _get_or_create_pet(pet_id)
        if pet.state != BeingState.DEAD:
            raise HTTPException(status_code=400, detail="Pet must be dead to reincarnate")

        graveyard_dir = pet_realm_path(project_root) / "graveyard"
        lineage_dir = pet_realm_path(project_root) / "lineage"
        graveyard_dir.mkdir(parents=True, exist_ok=True)
        lineage_dir.mkdir(parents=True, exist_ok=True)

        tombstone = {
            "pet_id": pet.being_id,
            "name": pet.display_name,
            "died_at": datetime.now().isoformat(),
            "lifetimes": pet.lifetimes,
        }
        (graveyard_dir / f"{pet.being_id}.json").write_text(
            json.dumps(tombstone, indent=2), encoding="utf-8"
        )

        new_being = BeingSystem(project_path=project_root).spawn_being(reality_id="waft_pet")
        new_pet = PetBeing.from_dict(new_being.to_dict())
        new_pet.lifetimes = pet.lifetimes + 1
        save_pet(new_pet, project_root)

        lineage_entry = {
            "previous_pet_id": pet.being_id,
            "new_pet_id": new_pet.being_id,
            "reborn_at": datetime.now().isoformat(),
        }
        lineage_path = lineage_dir / f"{new_pet.being_id}.json"
        lineage_path.write_text(json.dumps(lineage_entry, indent=2), encoding="utf-8")

        return {
            "previous_pet_id": pet.being_id,
            "new_pet_id": new_pet.being_id,
            "status": _pet_status(new_pet),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
