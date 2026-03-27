"""
Empirica Brain: first Waft unit for narrative software engineering.

This unit does two things:
1) Builds a dungeon-framed engineering prompt that enforces Empirica CASCADE.
2) Runs a minimal CASCADE gate cycle to establish a real execution spine.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .empirica import EmpiricaManager


@dataclass(frozen=True)
class BrainCycleResult:
    session_id: str | None
    gate_result: str | None
    preflight_submitted: bool
    postflight_submitted: bool
    proceed: bool
    message: str


class EmpiricaBrain:
    DEFAULT_PREFLIGHT_VECTORS = {
        "engagement": 0.85,
        "know": 0.55,
        "uncertainty": 0.4,
    }

    DEFAULT_POSTFLIGHT_VECTORS = {
        "engagement": 0.9,
        "know": 0.8,
        "uncertainty": 0.18,
    }

    def __init__(
        self,
        project_path: Path,
        empirica_manager: EmpiricaManager | None = None,
        ai_id: str = "waft-empirica-brain",
    ) -> None:
        self.project_path = Path(project_path)
        self.ai_id = ai_id
        self.empirica = empirica_manager or EmpiricaManager(self.project_path)

    def build_narrative_prompt(self, mission: str, session_type: str = "dungeon-engineering") -> str:
        mission_text = str(mission).strip() or "Deliver real software engineering output."
        return (
            "=== EMPIRICA BRAIN: DUNGEON ENGINEERING CONTRACT ===\n\n"
            "Narrative Frame:\n"
            "- You are a systems engineer traversing a hostile AI dungeon.\n"
            "- Every chamber is a real repo task, not pure roleplay.\n"
            "- Survival condition: produce working software artifacts with evidence.\n\n"
            "Mandatory Empirica CASCADE Sequence:\n"
            f"1) Create session: waft session create --ai-id {self.ai_id} --type {session_type}\n"
            "2) Submit PREFLIGHT vectors before edits.\n"
            "3) Run CHECK gate before major implementation/risky operations.\n"
            "4) Log findings and unknowns during execution.\n"
            "5) Submit POSTFLIGHT vectors after validation.\n\n"
            "Engineering Deliverable Contract:\n"
            "- Ship concrete code changes in files.\n"
            "- Add or update tests for behavior.\n"
            "- Run validation commands and report outputs.\n"
            "- Log what changed and why.\n\n"
            "Sentinel Rule:\n"
            "- HALT means stop and request human approval.\n"
            "- BRANCH means investigate before merge.\n"
            "- REVISE means adapt approach and resubmit.\n\n"
            f"Mission:\n{mission_text}\n"
        )

    def run_cascade_cycle(
        self,
        mission: str,
        session_type: str = "dungeon-engineering",
        preflight_vectors: dict[str, Any] | None = None,
        postflight_vectors: dict[str, Any] | None = None,
        gate_operation: dict[str, Any] | None = None,
        preflight_reasoning: str = "",
        postflight_reasoning: str = "",
    ) -> BrainCycleResult:
        ready = self.empirica.ensure_ready(
            ai_id=self.ai_id,
            session_type=session_type,
            force_session=False,
        )
        if not ready.get("ready"):
            return BrainCycleResult(
                session_id=None,
                gate_result=None,
                preflight_submitted=False,
                postflight_submitted=False,
                proceed=False,
                message=ready.get("message", "Empirica is not ready"),
            )

        session_id = self.empirica.create_session(ai_id=self.ai_id, session_type=session_type)
        if not session_id:
            return BrainCycleResult(
                session_id=None,
                gate_result=None,
                preflight_submitted=False,
                postflight_submitted=False,
                proceed=False,
                message="Failed to create Empirica session",
            )

        preflight_ok = self.empirica.submit_preflight(
            session_id=session_id,
            vectors=preflight_vectors or dict(self.DEFAULT_PREFLIGHT_VECTORS),
            reasoning=preflight_reasoning or f"Mission preflight: {mission}",
        )
        if not preflight_ok:
            return BrainCycleResult(
                session_id=session_id,
                gate_result=None,
                preflight_submitted=False,
                postflight_submitted=False,
                proceed=False,
                message="Failed to submit preflight",
            )

        operation = gate_operation or {
            "type": "code_generation",
            "scope": "high",
            "mission": str(mission).strip(),
        }
        gate_result = self.empirica.check_submit(operation=operation)
        if gate_result == "HALT":
            return BrainCycleResult(
                session_id=session_id,
                gate_result=gate_result,
                preflight_submitted=True,
                postflight_submitted=False,
                proceed=False,
                message="Gate returned HALT",
            )

        postflight_ok = self.empirica.submit_postflight(
            session_id=session_id,
            vectors=postflight_vectors or dict(self.DEFAULT_POSTFLIGHT_VECTORS),
            reasoning=postflight_reasoning or f"Mission postflight: {mission}",
        )
        if not postflight_ok:
            return BrainCycleResult(
                session_id=session_id,
                gate_result=gate_result,
                preflight_submitted=True,
                postflight_submitted=False,
                proceed=False,
                message="Failed to submit postflight",
            )

        return BrainCycleResult(
            session_id=session_id,
            gate_result=gate_result,
            preflight_submitted=True,
            postflight_submitted=True,
            proceed=True,
            message="Empirica Brain cycle completed",
        )
