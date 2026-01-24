"""
PetBeing: lightweight pet wrapper around Being.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from waft.being import Being, BeingState


def pet_realm_path(project_path: Path) -> Path:
    return Path(project_path) / "_realms" / "waft_pet"


def pet_storage_path(project_path: Path) -> Path:
    path = pet_realm_path(project_path) / "pets"
    path.mkdir(parents=True, exist_ok=True)
    return path


class PetBeing(Being):
    def __init__(
        self,
        *,
        affection: float = 0.0,
        visual_state: str = "idle",
        last_interaction: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.affection = affection
        self.visual_state = visual_state
        self.last_interaction = last_interaction or datetime.now().isoformat()

    def touch(self) -> None:
        self.last_interaction = datetime.now().isoformat()

    def get_emotion(self) -> str:
        if self.state == BeingState.DEAD:
            return "dead"
        if self.is_sleeping:
            return "sleeping"
        if self.pain > 50:
            return "sad"
        if self.pleasure > 70:
            return "excited"
        if self.decision_fatigue < 3:
            return "tired"
        if self.will_to_live < 30:
            return "depressed"
        return "content"

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "affection": self.affection,
                "visual_state": self.visual_state,
                "last_interaction": self.last_interaction,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PetBeing":
        pet = cls(
            being_id=data["being_id"],
            reality_id=data["reality_id"],
            parent_being_id=data.get("parent_being_id"),
            skills=data.get("skills", {}),
            source_id=data.get("source_id", "source_consciousness"),
            will_to_live=data.get("will_to_live"),
            luck=data.get("luck"),
            decision_fatigue=data.get("decision_fatigue"),
            decision_quota_max=data.get("decision_quota_max"),
            pleasure=data.get("pleasure"),
            pain=data.get("pain"),
            personality=data.get("personality"),
            goals=data.get("goals"),
            personality_type=data.get("personality_type"),
            soul_id=data.get("soul_id"),
            is_sleeping=data.get("is_sleeping"),
            sleep_duration=data.get("sleep_duration"),
            sleep_duration_base=data.get("sleep_duration_base"),
            cycles_slept=data.get("cycles_slept"),
            last_cycle_number=data.get("last_cycle_number"),
            lifetimes=data.get("lifetimes", data.get("cycles_alive", 0)),
            recent_experiences=data.get("recent_experiences"),
            custom_name=data.get("custom_name"),
            has_physical_form=data.get("has_physical_form"),
            hp=data.get("hp"),
            max_hp=data.get("max_hp"),
            affection=data.get("affection", 0.0),
            visual_state=data.get("visual_state", "idle"),
            last_interaction=data.get("last_interaction"),
        )
        pet.memories = data.get("memories", [])
        pet.lessons_learned = data.get("lessons_learned", [])
        pet.state = BeingState(data.get("state", "spawning"))
        pet.created_at = data.get("created_at", datetime.now().isoformat())
        pet.fitness = data.get("fitness", 0.0)
        pet.ancestral_chain = data.get("ancestral_chain", [pet.source_id])
        pet.purpose_being_id = data.get("purpose_being_id")
        pet.purpose = data.get("purpose")
        return pet


def save_pet(pet: PetBeing, project_path: Path) -> Path:
    storage_dir = pet_storage_path(project_path)
    path = storage_dir / f"{pet.being_id}.json"
    path.write_text(json.dumps(pet.to_dict(), indent=2), encoding="utf-8")
    return path


def load_pet(project_path: Path, pet_id: str) -> PetBeing:
    path = pet_storage_path(project_path) / f"{pet_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return PetBeing.from_dict(data)


def load_latest_pet(project_path: Path) -> PetBeing | None:
    storage_dir = pet_storage_path(project_path)
    pet_files = sorted(storage_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not pet_files:
        return None
    return load_pet(project_path, pet_files[0].stem)
