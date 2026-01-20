"""
CelestialBody: The Heart, Mind, Body, and Spirit of WAFT

The CelestialBody houses the Prime Directive (Heart) at the center,
along with CelestialMind (knowledge/evolution), CelestialBody (physical structure),
and CelestialSpirit (connection to TheOne/karma).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .directive import PrimeDirective


class CelestialMind:
    """
    CelestialMind: Knowledge, understanding, and evolution tracking.

    Stores knowledge about the system, tracks evolution patterns,
    and maintains understanding of how the system works.
    """

    def __init__(self, mind_path: Path):
        """
        Initialize CelestialMind.

        Args:
            mind_path: Path to mind data storage
        """
        self.mind_path = Path(mind_path)
        self.mind_path.mkdir(parents=True, exist_ok=True)

        self.knowledge_file = self.mind_path / "knowledge.json"
        self.evolution_patterns_file = self.mind_path / "evolution_patterns.json"

        self.knowledge: dict[str, Any] = {}
        self.evolution_patterns: list[dict[str, Any]] = []

        self._load()

    def _load(self):
        """Load mind data from disk."""
        if self.knowledge_file.exists():
            with open(self.knowledge_file) as f:
                self.knowledge = json.load(f)

        if self.evolution_patterns_file.exists():
            with open(self.evolution_patterns_file) as f:
                self.evolution_patterns = json.load(f)

    def _save(self):
        """Save mind data to disk."""
        with open(self.knowledge_file, "w") as f:
            json.dump(self.knowledge, f, indent=2)

        with open(self.evolution_patterns_file, "w") as f:
            json.dump(self.evolution_patterns, f, indent=2)

    def record_knowledge(self, topic: str, knowledge: Any):
        """
        Record knowledge about a topic.

        Args:
            topic: Topic name
            knowledge: Knowledge data
        """
        self.knowledge[topic] = {
            "content": knowledge,
            "recorded_at": datetime.now().isoformat(),
        }
        self._save()

    def get_knowledge(self, topic: str | None = None) -> dict[str, Any]:
        """
        Get knowledge.

        Args:
            topic: Optional topic to get (None = all knowledge)

        Returns:
            Knowledge dict
        """
        if topic:
            return self.knowledge.get(topic, {})
        return self.knowledge.copy()

    def record_evolution_pattern(self, pattern: dict[str, Any]):
        """
        Record an evolution pattern.

        Args:
            pattern: Pattern data
        """
        pattern["recorded_at"] = datetime.now().isoformat()
        self.evolution_patterns.append(pattern)
        self._save()

    def get_evolution_patterns(self) -> list[dict[str, Any]]:
        """Get all evolution patterns."""
        return self.evolution_patterns.copy()


class CelestialSpirit:
    """
    CelestialSpirit: Essence, karma, and connection to TheOne.

    Maintains the spiritual connection to TheOne Being and tracks
    karma-related evolution.
    """

    def __init__(self, spirit_path: Path, the_one_being_id: str):
        """
        Initialize CelestialSpirit.

        Args:
            spirit_path: Path to spirit data storage
            the_one_being_id: ID of TheOne Being
        """
        self.spirit_path = Path(spirit_path)
        self.spirit_path.mkdir(parents=True, exist_ok=True)

        self.the_one_being_id = the_one_being_id

        self.spirit_file = self.spirit_path / "spirit.json"
        self.karma_evolution_file = self.spirit_path / "karma_evolution.json"

        self.essence: dict[str, Any] = {
            "the_one_being_id": the_one_being_id,
            "connected_at": datetime.now().isoformat(),
        }
        self.karma_evolution: list[dict[str, Any]] = []

        self._load()

    def _load(self):
        """Load spirit data from disk."""
        if self.spirit_file.exists():
            with open(self.spirit_file) as f:
                self.essence = json.load(f)

        if self.karma_evolution_file.exists():
            with open(self.karma_evolution_file) as f:
                self.karma_evolution = json.load(f)

    def _save(self):
        """Save spirit data to disk."""
        with open(self.spirit_file, "w") as f:
            json.dump(self.essence, f, indent=2)

        with open(self.karma_evolution_file, "w") as f:
            json.dump(self.karma_evolution, f, indent=2)

    def record_karma_event(self, event: dict[str, Any]):
        """
        Record a karma evolution event.

        Args:
            event: Event data
        """
        event["timestamp"] = datetime.now().isoformat()
        self.karma_evolution.append(event)
        self._save()

    def get_karma_evolution(self) -> list[dict[str, Any]]:
        """Get karma evolution history."""
        return self.karma_evolution.copy()

    def get_essence(self) -> dict[str, Any]:
        """Get essence data."""
        return self.essence.copy()


class CelestialBody:
    """
    CelestialBody: The complete structure housing Heart, Mind, Body, and Spirit.

    The CelestialBody is the physical and metaphysical structure that houses
    the Prime Directive (Heart) at its center, along with Mind, Body, and Spirit.
    """

    def __init__(
        self,
        project_path: Path | None = None,
        the_one_being_id: str = "the_one",
        celestial_body_path: Path | None = None,
    ):
        """
        Initialize CelestialBody.

        Args:
            project_path: Path to project root
            the_one_being_id: ID of TheOne Being
            celestial_body_path: Path to celestial body storage
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.the_one_being_id = the_one_being_id

        if celestial_body_path is None:
            celestial_body_path = project_path / "_hidden" / ".truth" / "celestial_body"
        else:
            celestial_body_path = Path(celestial_body_path)

        self.celestial_body_path = celestial_body_path
        self.celestial_body_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        heart_path = celestial_body_path / "heart"
        mind_path = celestial_body_path / "mind"
        body_path = celestial_body_path / "body"
        spirit_path = celestial_body_path / "spirit"

        # Heart: Prime Directive (at center)
        self.heart = PrimeDirective(project_path=project_path, directive_path=heart_path)

        # Mind: Knowledge and evolution tracking
        self.mind = CelestialMind(mind_path)

        # Body: Physical structure and persistence
        self.body_path = body_path
        self.body_path.mkdir(parents=True, exist_ok=True)
        self.body_state_file = body_path / "state.json"
        self.body_state: dict[str, Any] = {
            "initialized_at": datetime.now().isoformat(),
            "the_one_being_id": the_one_being_id,
            "cycles_recorded": 0,
            "generations_recorded": 0,
        }
        self._load_body_state()

        # Spirit: Connection to TheOne and karma
        self.spirit = CelestialSpirit(spirit_path, the_one_being_id)

        # Record initialization
        self.heart.add_reference(
            reference_type="celestial_body",
            reference_id="celestial_body_main",
            description="CelestialBody housing the Prime Directive",
        )

    def _load_body_state(self):
        """Load body state from disk."""
        if self.body_state_file.exists():
            with open(self.body_state_file) as f:
                self.body_state = json.load(f)

    def _save_body_state(self):
        """Save body state to disk."""
        with open(self.body_state_file, "w") as f:
            json.dump(self.body_state, f, indent=2)

    def record_cycle(self, cycle_data: dict[str, Any]):
        """
        Record a cycle in the evolution.

        Args:
            cycle_data: Cycle data to record
        """
        self.body_state["cycles_recorded"] += 1
        self.body_state["last_cycle_at"] = datetime.now().isoformat()
        self._save_body_state()

        # Record in mind
        self.mind.record_evolution_pattern(
            {
                "type": "cycle",
                "cycle_number": self.body_state["cycles_recorded"],
                "data": cycle_data,
            }
        )

    def record_generation(self, generation_data: dict[str, Any]):
        """
        Record a generation in the evolution.

        Args:
            generation_data: Generation data to record
        """
        self.body_state["generations_recorded"] += 1
        self.body_state["last_generation_at"] = datetime.now().isoformat()
        self._save_body_state()

        # Record in mind
        self.mind.record_evolution_pattern(
            {
                "type": "generation",
                "generation_number": self.body_state["generations_recorded"],
                "data": generation_data,
            }
        )

    def query_history(
        self, query_type: str | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Query evolution history.

        Args:
            query_type: Optional filter by type (cycle, generation)
            limit: Optional limit on results

        Returns:
            List of history entries
        """
        patterns = self.mind.get_evolution_patterns()

        if query_type:
            patterns = [p for p in patterns if p.get("type") == query_type]

        if limit:
            patterns = patterns[-limit:]

        return patterns

    def evolve(self, evolution_data: dict[str, Any]):
        """
        Record evolution event.

        Args:
            evolution_data: Evolution data
        """
        evolution_data["timestamp"] = datetime.now().isoformat()
        evolution_data["the_one_being_id"] = self.the_one_being_id

        # Record in mind
        self.mind.record_evolution_pattern(
            {
                "type": "evolution",
                "data": evolution_data,
            }
        )

        # Record karma event if present
        if "karma" in evolution_data:
            self.spirit.record_karma_event(
                {
                    "type": "evolution",
                    "karma": evolution_data["karma"],
                    "data": evolution_data,
                }
            )

    def get_state(self) -> dict[str, Any]:
        """Get current state of CelestialBody."""
        return {
            "heart": {
                "version": self.heart.version,
                "principle_count": len(self.heart.get_principles()),
            },
            "mind": {
                "knowledge_topics": list(self.mind.get_knowledge().keys()),
                "pattern_count": len(self.mind.get_evolution_patterns()),
            },
            "body": self.body_state.copy(),
            "spirit": {
                "the_one_being_id": self.spirit.the_one_being_id,
                "karma_events": len(self.spirit.get_karma_evolution()),
            },
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "the_one_being_id": self.the_one_being_id,
            "heart": self.heart.to_dict(),
            "mind": self.mind.get_knowledge(),
            "body": self.body_state,
            "spirit": self.spirit.get_essence(),
        }
