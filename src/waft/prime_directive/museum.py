"""
Karma Museum: Evolution History Documentation

The Karma Museum is built around the Heart (Prime Directive) and documents
the evolution history of the system. It contains exhibits, artifacts, and
a timeline of important moments.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class KarmaMuseum:
    """
    Karma Museum: Documents evolution history around the Heart.

    Structure:
    - exhibits/ - Evolution exhibits (generations, cycles)
    - artifacts/ - Important moments in evolution
    - timeline/ - Chronological evolution record
    - index.json - Museum catalog
    """

    def __init__(self, project_path: Path | None = None, museum_path: Path | None = None):
        """
        Initialize Karma Museum.

        Args:
            project_path: Path to project root
            museum_path: Path to museum storage
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path

        if museum_path is None:
            museum_path = project_path / "_hidden" / ".truth" / "celestial_body" / "karma_museum"
        else:
            museum_path = Path(museum_path)

        self.museum_path = museum_path
        self.museum_path.mkdir(parents=True, exist_ok=True)

        self.exhibits_path = self.museum_path / "exhibits"
        self.artifacts_path = self.museum_path / "artifacts"
        self.timeline_path = self.museum_path / "timeline"
        self.index_file = self.museum_path / "index.json"

        self.exhibits_path.mkdir(exist_ok=True)
        self.artifacts_path.mkdir(exist_ok=True)
        self.timeline_path.mkdir(exist_ok=True)

        # Museum catalog
        self.catalog: dict[str, Any] = {
            "exhibits": [],
            "artifacts": [],
            "timeline_entries": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self._load()

    def _load(self):
        """Load museum catalog from disk."""
        if self.index_file.exists():
            with open(self.index_file) as f:
                self.catalog = json.load(f)

    def _save(self):
        """Save museum catalog to disk."""
        self.catalog["updated_at"] = datetime.now().isoformat()
        with open(self.index_file, "w") as f:
            json.dump(self.catalog, f, indent=2)

    def create_exhibit(
        self,
        exhibit_id: str,
        title: str,
        description: str,
        exhibit_data: dict[str, Any],
        generation: int | None = None,
        cycle: int | None = None,
    ) -> dict[str, Any]:
        """
        Create an evolution exhibit.

        Args:
            exhibit_id: Unique exhibit identifier
            title: Exhibit title
            description: Exhibit description
            exhibit_data: Exhibit data
            generation: Optional generation number
            cycle: Optional cycle number

        Returns:
            Created exhibit data
        """
        exhibit = {
            "id": exhibit_id,
            "title": title,
            "description": description,
            "generation": generation,
            "cycle": cycle,
            "data": exhibit_data,
            "created_at": datetime.now().isoformat(),
        }

        # Save exhibit file
        exhibit_file = self.exhibits_path / f"{exhibit_id}.json"
        with open(exhibit_file, "w") as f:
            json.dump(exhibit, f, indent=2)

        # Add to catalog
        self.catalog["exhibits"].append(
            {
                "id": exhibit_id,
                "title": title,
                "generation": generation,
                "cycle": cycle,
                "created_at": exhibit["created_at"],
            }
        )

        self._save()

        return exhibit

    def create_artifact(
        self,
        artifact_id: str,
        title: str,
        description: str,
        artifact_data: dict[str, Any],
        importance: str = "medium",
    ) -> dict[str, Any]:
        """
        Create an artifact (important moment).

        Args:
            artifact_id: Unique artifact identifier
            title: Artifact title
            description: Artifact description
            artifact_data: Artifact data
            importance: Importance level (low, medium, high, critical)

        Returns:
            Created artifact data
        """
        artifact = {
            "id": artifact_id,
            "title": title,
            "description": description,
            "importance": importance,
            "data": artifact_data,
            "created_at": datetime.now().isoformat(),
        }

        # Save artifact file
        artifact_file = self.artifacts_path / f"{artifact_id}.json"
        with open(artifact_file, "w") as f:
            json.dump(artifact, f, indent=2)

        # Add to catalog
        self.catalog["artifacts"].append(
            {
                "id": artifact_id,
                "title": title,
                "importance": importance,
                "created_at": artifact["created_at"],
            }
        )

        self._save()

        return artifact

    def add_timeline_entry(
        self,
        entry_id: str,
        timestamp: str,
        event_type: str,
        description: str,
        event_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Add a timeline entry.

        Args:
            entry_id: Unique entry identifier
            timestamp: Event timestamp
            event_type: Type of event
            description: Event description
            event_data: Optional event data

        Returns:
            Created timeline entry
        """
        entry = {
            "id": entry_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "description": description,
            "data": event_data or {},
            "created_at": datetime.now().isoformat(),
        }

        # Save timeline entry
        entry_file = self.timeline_path / f"{entry_id}.json"
        with open(entry_file, "w") as f:
            json.dump(entry, f, indent=2)

        # Add to catalog
        self.catalog["timeline_entries"].append(
            {
                "id": entry_id,
                "timestamp": timestamp,
                "event_type": event_type,
                "description": description,
            }
        )

        # Sort timeline by timestamp
        self.catalog["timeline_entries"].sort(key=lambda e: e["timestamp"])

        self._save()

        return entry

    def get_exhibit(self, exhibit_id: str) -> dict[str, Any] | None:
        """
        Get an exhibit.

        Args:
            exhibit_id: Exhibit ID

        Returns:
            Exhibit data or None
        """
        exhibit_file = self.exhibits_path / f"{exhibit_id}.json"

        if exhibit_file.exists():
            with open(exhibit_file) as f:
                return json.load(f)

        return None

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        """
        Get an artifact.

        Args:
            artifact_id: Artifact ID

        Returns:
            Artifact data or None
        """
        artifact_file = self.artifacts_path / f"{artifact_id}.json"

        if artifact_file.exists():
            with open(artifact_file) as f:
                return json.load(f)

        return None

    def get_timeline(
        self,
        start_timestamp: str | None = None,
        end_timestamp: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get timeline entries.

        Args:
            start_timestamp: Optional start timestamp filter
            end_timestamp: Optional end timestamp filter
            event_type: Optional event type filter
            limit: Optional limit on results

        Returns:
            List of timeline entries
        """
        entries = []

        for entry_info in self.catalog["timeline_entries"]:
            entry_file = self.timeline_path / f"{entry_info['id']}.json"

            if entry_file.exists():
                with open(entry_file) as f:
                    entry = json.load(f)

                    # Apply filters
                    if start_timestamp and entry["timestamp"] < start_timestamp:
                        continue
                    if end_timestamp and entry["timestamp"] > end_timestamp:
                        continue
                    if event_type and entry["event_type"] != event_type:
                        continue

                    entries.append(entry)

        # Sort by timestamp
        entries.sort(key=lambda e: e["timestamp"])

        # Apply limit
        if limit:
            entries = entries[-limit:]

        return entries

    def get_catalog(self) -> dict[str, Any]:
        """Get museum catalog."""
        return self.catalog.copy()

    def get_statistics(self) -> dict[str, Any]:
        """Get museum statistics."""
        return {
            "total_exhibits": len(self.catalog["exhibits"]),
            "total_artifacts": len(self.catalog["artifacts"]),
            "total_timeline_entries": len(self.catalog["timeline_entries"]),
            "created_at": self.catalog["created_at"],
            "updated_at": self.catalog["updated_at"],
        }
