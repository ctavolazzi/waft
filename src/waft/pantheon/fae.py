"""
Fae: Pantheon Entity of Whimsy, Creativity, and Open-Ended Discovery

The Fae guide whimsical, open-ended work - Quests that allow for exploration,
creativity, and unexpected discoveries.

Following "as above, so below" principles:
- As above: Mythical beings weaving threads of creativity and wonder
- So below: File-based system managing quest tracking and Fae blessings
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any


class Quest:
    """A Quest - whimsical, open-ended work guided by the Fae."""

    def __init__(
        self,
        quest_id: str,
        name: str,
        description: str,
        fae_guidance: str | None = None,
        difficulty: int = 5,
        created_at: str | None = None,
    ):
        """
        Initialize a quest.

        Args:
            quest_id: Unique identifier for the quest
            name: Quest name
            description: Open-ended quest description
            fae_guidance: Fae blessing/guidance
            difficulty: Quest difficulty (1-10), can be flexible
            created_at: ISO timestamp when quest was created
        """
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.fae_guidance = fae_guidance or self._generate_fae_guidance()
        self.difficulty = difficulty
        self.created_at = created_at or datetime.now().isoformat()
        self.status = "active"
        self.progress = "exploring"

    def _generate_fae_guidance(self) -> str:
        """Generate whimsical Fae guidance."""
        guidance_options = [
            "The Fae whisper: 'Follow your curiosity, let wonder guide you'",
            "The Fae bless this quest with creativity and serendipity",
            "The Fae suggest: 'Explore freely, discover what emerges'",
            "The Fae weave threads of inspiration into this quest",
            "The Fae grant: 'May your path be filled with unexpected discoveries'",
            "The Fae encourage: 'Let creativity flow, let patterns emerge'",
            "The Fae promise: 'Wonder and joy await those who explore'",
        ]
        return random.choice(guidance_options)

    def to_dict(self) -> dict[str, Any]:
        """Convert quest to dictionary."""
        return {
            "id": self.quest_id,
            "name": self.name,
            "type": "whimsical",
            "status": self.status,
            "description": self.description,
            "fae_guidance": self.fae_guidance,
            "difficulty": self.difficulty,
            "progress": self.progress,
            "created_at": self.created_at,
        }


class Fae:
    """
    Fae: Pantheon Entity (Timeless Force that Binds Reality Together)

    Entity of Whimsy, Creativity, and Open-Ended Discovery - a timeless Entity
    that maintains creative principles and whimsical exploration. As a Force that
    Binds Reality Together, the Fae holds the Aspect of Creation related to
    creativity and discovery, which should not change until evidence collected
    by Beings proves that change is needed.

    The Fae doesn't move much - it maintains stable creative principles and only
    evolves when sufficient evidence warrants modification of its fundamental nature.

    Guides whimsical, open-ended work - Quests that allow for exploration,
    creativity, and unexpected discoveries.

    Storage:
    - Quests: _pantheon/fae/quests/
    - Blessings: _pantheon/fae/blessings/
    - Discoveries: _pantheon/fae/discoveries/
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize the Fae.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.fae_path = self.pantheon_path / "fae"

        # Ensure directory structure exists
        self.fae_path.mkdir(parents=True, exist_ok=True)
        (self.fae_path / "quests").mkdir(parents=True, exist_ok=True)
        (self.fae_path / "blessings").mkdir(parents=True, exist_ok=True)
        (self.fae_path / "discoveries").mkdir(parents=True, exist_ok=True)

        # Quest registry
        self.quests_file = self.fae_path / "quests_registry.json"
        self.quests = self._load_quests()

    def _load_quests(self) -> list[dict[str, Any]]:
        """Load quests from registry."""
        if not self.quests_file.exists():
            return []

        try:
            with open(self.quests_file) as f:
                data = json.load(f)
                return data.get("quests", [])
        except (OSError, json.JSONDecodeError):
            return []

    def _save_quests(self) -> None:
        """Save quests to registry."""
        data = {"quests": self.quests, "updated_at": datetime.now().isoformat()}
        with open(self.quests_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_quest(
        self,
        name: str,
        description: str,
        fae_guidance: str | None = None,
        difficulty: int | None = None,
    ) -> Quest:
        """
        Create a new quest with Fae blessing.

        Args:
            name: Quest name
            description: Open-ended quest description
            fae_guidance: Optional Fae blessing/guidance
            difficulty: Quest difficulty (1-10), auto-calculated if None

        Returns:
            Created Quest object
        """
        quest_id = f"quest_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name.lower().replace(' ', '_')[:20]}"

        # Auto-calculate difficulty if not provided (more flexible than missions)
        if difficulty is None:
            # Base difficulty on description length (but keep it whimsical)
            word_count = len(description.split())
            difficulty = min(10, max(1, (word_count // 15) + 3))

        quest = Quest(
            quest_id=quest_id,
            name=name,
            description=description,
            fae_guidance=fae_guidance,
            difficulty=difficulty,
        )

        # Register quest
        self.quests.append(quest.to_dict())
        self._save_quests()

        # Auto-share with The Village
        try:
            from .the_village import TheVillage

            village = TheVillage(self.project_path)
            village.share_quest(quest.quest_id, shared_by="fae")
        except Exception:
            # Village integration is optional
            pass

        return quest

    def get_quest(self, quest_id: str) -> Quest | None:
        """Get quest by ID."""
        for quest_data in self.quests:
            if quest_data.get("id") == quest_id:
                return Quest(
                    quest_id=quest_data["id"],
                    name=quest_data["name"],
                    description=quest_data["description"],
                    fae_guidance=quest_data.get("fae_guidance"),
                    difficulty=quest_data.get("difficulty", 5),
                    created_at=quest_data.get("created_at"),
                )
        return None

    def list_quests(self, status: str | None = None) -> list[Quest]:
        """
        List quests with optional filter.

        Args:
            status: Filter by status (active, exploring, complete, etc.)

        Returns:
            List of Quest objects
        """
        quests = []
        for quest_data in self.quests:
            if status and quest_data.get("status") != status:
                continue

            quest = Quest(
                quest_id=quest_data["id"],
                name=quest_data["name"],
                description=quest_data["description"],
                fae_guidance=quest_data.get("fae_guidance"),
                difficulty=quest_data.get("difficulty", 5),
                created_at=quest_data.get("created_at"),
            )
            quest.status = quest_data.get("status", "active")
            quest.progress = quest_data.get("progress", "exploring")
            quests.append(quest)

        return quests

    def update_quest_status(
        self, quest_id: str, status: str, progress: str | None = None
    ) -> bool:
        """
        Update quest status.

        Args:
            quest_id: Quest ID
            status: New status
            progress: Optional progress update

        Returns:
            True if updated, False if quest not found
        """
        for quest_data in self.quests:
            if quest_data.get("id") == quest_id:
                quest_data["status"] = status
                if progress:
                    quest_data["progress"] = progress
                self._save_quests()
                return True
        return False

    def bless_quest(self, quest: Quest) -> str:
        """
        Generate Fae blessing for a quest.

        Args:
            quest: Quest object

        Returns:
            Blessing text
        """
        blessings = [
            "May your path be filled with wonder and discovery",
            "The Fae grant you creativity and inspiration",
            "Serendipity and joy await your exploration",
            "The Fae weave threads of magic into your quest",
            "May unexpected discoveries bring you joy",
            "The Fae bless this quest with curiosity and wonder",
            "Let creativity flow and patterns emerge naturally",
        ]
        return random.choice(blessings)

    def record_discovery(self, quest_id: str, discovery: str) -> Path:
        """
        Record a discovery made during a quest.

        Args:
            quest_id: Quest ID
            discovery: Discovery description

        Returns:
            Path to discovery file
        """
        discovery_data = {
            "quest_id": quest_id,
            "discovery": discovery,
            "timestamp": datetime.now().isoformat(),
        }

        discovery_path = (
            self.fae_path
            / "discoveries"
            / f"{quest_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        discovery_path.write_text(json.dumps(discovery_data, indent=2), encoding="utf-8")
        return discovery_path
