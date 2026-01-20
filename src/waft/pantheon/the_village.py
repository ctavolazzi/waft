"""
The Village: Pantheon Entity of Community, Connection, and Collective Wisdom

The Village serves as a community space for coordination, sharing, and organic
collaboration. Inspired by Avatar's Na'vi village and Fern Gully's fairy community,
The Village provides a more organic, interconnected approach to work.

Following "as above, so below" principles:
- As above: Community gathering place where beings connect and share
- So below: File-based system managing community coordination, quest sharing, and collective wisdom
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class VillageGathering:
    """A gathering in The Village - community coordination event."""

    def __init__(
        self,
        gathering_id: str,
        topic: str,
        description: str,
        participants: list[str] | None = None,
        insights: list[str] | None = None,
        created_at: str | None = None,
    ):
        """
        Initialize a village gathering.

        Args:
            gathering_id: Unique identifier
            topic: Gathering topic
            description: What the gathering is about
            participants: List of participant identifiers
            insights: Collective insights from the gathering
            created_at: ISO timestamp
        """
        self.gathering_id = gathering_id
        self.topic = topic
        self.description = description
        self.participants = participants or []
        self.insights = insights or []
        self.created_at = created_at or datetime.now().isoformat()
        self.status = "active"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "gathering_id": self.gathering_id,
            "topic": self.topic,
            "description": self.description,
            "participants": self.participants,
            "insights": self.insights,
            "created_at": self.created_at,
            "status": self.status,
        }


class VillageConnection:
    """A connection between beings in The Village."""

    def __init__(
        self,
        connection_id: str,
        from_being: str,
        to_being: str,
        connection_type: str = "collaboration",
        strength: float = 1.0,
        created_at: str | None = None,
    ):
        """
        Initialize a village connection.

        Args:
            connection_id: Unique identifier
            from_being: Source being identifier
            to_being: Target being identifier
            connection_type: Type of connection (collaboration, mentorship, discovery)
            strength: Connection strength (0.0-1.0)
            created_at: ISO timestamp
        """
        self.connection_id = connection_id
        self.from_being = from_being
        self.to_being = to_being
        self.connection_type = connection_type
        self.strength = strength
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "connection_id": self.connection_id,
            "from_being": self.from_being,
            "to_being": self.to_being,
            "connection_type": self.connection_type,
            "strength": self.strength,
            "created_at": self.created_at,
        }


class TheVillage:
    """
    The Village: Community space for organic coordination and sharing.

    Provides:
    - Community gatherings for coordination
    - Quest sharing and discovery
    - Connection tracking between beings
    - Collective wisdom and insights
    - Organic collaboration patterns
    """

    def __init__(self, project_path: Path):
        """
        Initialize The Village.

        Args:
            project_path: Project root path
        """
        self.project_path = project_path
        self.village_path = project_path / "_pantheon" / "the_village"
        self.village_path.mkdir(parents=True, exist_ok=True)

        # Village directories
        self.gatherings_path = self.village_path / "gatherings"
        self.gatherings_path.mkdir(exist_ok=True)
        self.connections_path = self.village_path / "connections"
        self.connections_path.mkdir(exist_ok=True)
        self.wisdom_path = self.village_path / "wisdom"
        self.wisdom_path.mkdir(exist_ok=True)

        # Registry
        self.registry_file = self.village_path / "village_registry.json"
        self._ensure_registry()

    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "active_gatherings": [],
                "connections": [],
                "shared_quests": [],
                "collective_wisdom": [],
                "last_update": datetime.now().isoformat(),
            }
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def create_gathering(
        self, topic: str, description: str, participants: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Create a village gathering.

        Args:
            topic: Gathering topic
            description: What the gathering is about
            participants: Initial participants

        Returns:
            Gathering data
        """
        gathering_id = f"gathering_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        gathering = VillageGathering(
            gathering_id=gathering_id,
            topic=topic,
            description=description,
            participants=participants or [],
        )

        gathering_file = self.gatherings_path / f"{gathering_id}.json"
        gathering_file.write_text(json.dumps(gathering.to_dict(), indent=2), encoding="utf-8")

        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["active_gatherings"].append(gathering_id)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return gathering.to_dict()

    def add_insight(
        self, gathering_id: str, insight: str, contributor: str | None = None
    ) -> dict[str, Any]:
        """
        Add an insight to a gathering.

        Args:
            gathering_id: Gathering identifier
            insight: Insight text
            contributor: Who contributed the insight

        Returns:
            Updated gathering
        """
        gathering_file = self.gatherings_path / f"{gathering_id}.json"

        if not gathering_file.exists():
            raise ValueError(f"Gathering {gathering_id} not found")

        gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))
        insight_entry = {
            "insight": insight,
            "contributor": contributor,
            "added_at": datetime.now().isoformat(),
        }
        gathering_data["insights"].append(insight_entry)

        gathering_file.write_text(json.dumps(gathering_data, indent=2), encoding="utf-8")

        return gathering_data

    def create_connection(
        self,
        from_being: str,
        to_being: str,
        connection_type: str = "collaboration",
        strength: float = 1.0,
    ) -> dict[str, Any]:
        """
        Create a connection between beings.

        Args:
            from_being: Source being identifier
            to_being: Target being identifier
            connection_type: Type of connection
            strength: Connection strength

        Returns:
            Connection data
        """
        connection_id = f"conn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        connection = VillageConnection(
            connection_id=connection_id,
            from_being=from_being,
            to_being=to_being,
            connection_type=connection_type,
            strength=strength,
        )

        connection_file = self.connections_path / f"{connection_id}.json"
        connection_file.write_text(json.dumps(connection.to_dict(), indent=2), encoding="utf-8")

        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["connections"].append(connection_id)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return connection.to_dict()

    def share_quest(self, quest_id: str, shared_by: str) -> dict[str, Any]:
        """
        Share a quest in The Village.

        Args:
            quest_id: Quest identifier
            shared_by: Who is sharing the quest

        Returns:
            Sharing confirmation
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))

        share_entry = {
            "quest_id": quest_id,
            "shared_by": shared_by,
            "shared_at": datetime.now().isoformat(),
        }

        registry["shared_quests"].append(share_entry)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return {
            "quest_id": quest_id,
            "status": "shared",
            "message": "Quest has been shared with The Village",
        }

    def add_wisdom(self, wisdom: str, source: str | None = None) -> dict[str, Any]:
        """
        Add to collective wisdom.

        Args:
            wisdom: Wisdom text
            source: Source of the wisdom

        Returns:
            Wisdom entry
        """
        wisdom_id = f"wisdom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        wisdom_entry = {
            "wisdom_id": wisdom_id,
            "wisdom": wisdom,
            "source": source,
            "added_at": datetime.now().isoformat(),
        }

        wisdom_file = self.wisdom_path / f"{wisdom_id}.json"
        wisdom_file.write_text(json.dumps(wisdom_entry, indent=2), encoding="utf-8")

        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["collective_wisdom"].append(wisdom_id)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return wisdom_entry

    def get_village_summary(self) -> dict[str, Any]:
        """
        Get Village summary.

        Returns:
            Summary of village activity
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))

        # Count active gatherings
        active_gatherings = 0
        for gathering_id in registry["active_gatherings"]:
            gathering_file = self.gatherings_path / f"{gathering_id}.json"
            if gathering_file.exists():
                gathering_data = json.loads(gathering_file.read_text(encoding="utf-8"))
                if gathering_data.get("status") == "active":
                    active_gatherings += 1

        return {
            "active_gatherings": active_gatherings,
            "total_connections": len(registry["connections"]),
            "shared_quests": len(registry["shared_quests"]),
            "collective_wisdom_count": len(registry["collective_wisdom"]),
            "last_update": registry["last_update"],
        }
