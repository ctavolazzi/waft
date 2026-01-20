"""
State Capture System

Captures initial state (A) and final state (B) of the system for experimental analysis.
"""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SystemState:
    """A snapshot of system state."""

    timestamp: str
    state_type: str  # "initial" or "final"
    components: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    state_hash: str | None = None

    def __post_init__(self):
        """Calculate state hash if not provided."""
        if self.state_hash is None:
            self.state_hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        """Calculate hash of state for comparison."""
        state_str = json.dumps(asdict(self), sort_keys=True, default=str)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "state_type": self.state_type,
            "components": self.components,
            "metadata": self.metadata,
            "state_hash": self.state_hash,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SystemState":
        """Create from dictionary."""
        return cls(
            timestamp=data["timestamp"],
            state_type=data["state_type"],
            components=data.get("components", {}),
            metadata=data.get("metadata", {}),
            state_hash=data.get("state_hash"),
        )


class StateCapture:
    """Captures and stores system states."""

    def __init__(self, storage_path: Path):
        """
        Initialize state capture.

        Args:
            storage_path: Path to store state snapshots
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def capture_state(
        self, state_type: str, components: dict[str, Any], metadata: dict[str, Any] | None = None
    ) -> SystemState:
        """
        Capture a system state snapshot.

        Args:
            state_type: "initial" or "final"
            components: Dictionary of system components and their states
            metadata: Optional metadata about the state

        Returns:
            SystemState snapshot
        """
        state = SystemState(
            timestamp=datetime.now().isoformat(),
            state_type=state_type,
            components=components,
            metadata=metadata or {},
        )

        # Save state to file
        self._save_state(state)

        return state

    def capture_being_state(self, being: Any) -> dict[str, Any]:
        """
        Capture state of a Being.

        Args:
            being: Being instance

        Returns:
            Dictionary of being state
        """
        return {
            "being_id": being.being_id,
            "reality_id": being.reality_id,
            "skills": being.skills,
            "fitness": being.fitness,
            "memories_count": len(being.memories),
            "lessons_count": len(being.lessons_learned),
            "personality_type": being.personality_type,
            "will_to_live": being.will_to_live,
            "stamina": being.stamina,
            "decision_fatigue": being.decision_fatigue,
            "state": being.state.value if hasattr(being.state, "value") else str(being.state),
        }

    def capture_dnd_character_state(self, character: Any) -> dict[str, Any]:
        """
        Capture state of a D&D character.

        Args:
            character: DnD5eCharacter instance

        Returns:
            Dictionary of character state
        """
        return {
            "name": character.name,
            "level": character.level,
            "hp": character.hp,
            "max_hp": character.max_hp,
            "ac": character.ac,
            "strength": character.strength,
            "dexterity": character.dexterity,
            "constitution": character.constitution,
            "intelligence": character.intelligence,
            "wisdom": character.wisdom,
            "charisma": character.charisma,
        }

    def capture_system_components(
        self,
        beings: list[Any] | None = None,
        characters: list[Any] | None = None,
        other_components: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Capture multiple system components.

        Args:
            beings: List of Being instances
            characters: List of DnD character instances
            other_components: Other system components to capture

        Returns:
            Dictionary of all captured components
        """
        components = {}

        if beings:
            components["beings"] = [self.capture_being_state(b) for b in beings]

        if characters:
            components["characters"] = [self.capture_dnd_character_state(c) for c in characters]

        if other_components:
            components.update(other_components)

        return components

    def _save_state(self, state: SystemState):
        """Save state to file."""
        timestamp = state.timestamp.replace(":", "-").replace(".", "-")
        filename = f"state_{state.state_type}_{timestamp}.json"
        filepath = self.storage_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, indent=2, default=str)

    def load_state(self, state_hash: str) -> SystemState | None:
        """Load state by hash."""
        for filepath in self.storage_path.glob("state_*.json"):
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                state = SystemState.from_dict(data)
                if state.state_hash == state_hash:
                    return state
        return None

    def compare_states(self, initial: SystemState, final: SystemState) -> dict[str, Any]:
        """
        Compare initial and final states.

        Args:
            initial: Initial state
            final: Final state

        Returns:
            Dictionary of differences
        """
        differences = {
            "components_changed": [],
            "components_added": [],
            "components_removed": [],
            "value_changes": {},
        }

        # Compare components
        initial_components = set(initial.components.keys())
        final_components = set(final.components.keys())

        # Added components
        differences["components_added"] = list(final_components - initial_components)

        # Removed components
        differences["components_removed"] = list(initial_components - final_components)

        # Changed components
        common_components = initial_components & final_components
        for component in common_components:
            if initial.components[component] != final.components[component]:
                differences["components_changed"].append(component)
                differences["value_changes"][component] = {
                    "initial": initial.components[component],
                    "final": final.components[component],
                }

        return differences
