"""
Campaign Session Tracker
========================

Tracks D&D campaign sessions, character progression, and campaign evolution.
Stores session data in JSON and Markdown formats for easy retrieval and narrative documentation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class CampaignSessionTracker:
    """
    Tracks D&D campaign sessions with metadata, notes, and evolution.

    Stores data in:
    - JSON for structured data (sessions.json)
    - Markdown for narrative notes (session_XX.md)
    """

    def __init__(self, campaign_id: str, base_path: Path):
        """
        Initialize tracker for a campaign.

        Args:
            campaign_id: Unique identifier for the campaign
            base_path: Base directory for storing session data
        """
        self.campaign_id = campaign_id
        self.base_path = Path(base_path) / "session_tracker" / campaign_id
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.sessions_file = self.base_path / "sessions.json"
        self.characters_file = self.base_path / "characters.json"
        self.evolution_file = self.base_path / "evolution.json"

        # Load existing data
        self.sessions = self._load_json(self.sessions_file, [])
        self.characters = self._load_json(self.characters_file, {})
        self.evolution = self._load_json(self.evolution_file, [])

    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Load JSON file or return default if not exists."""
        if file_path.exists():
            try:
                with open(file_path, encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                return default
        return default

    def _save_json(self, file_path: Path, data: Any):
        """Save data to JSON file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_session(
        self,
        session_number: int,
        title: str,
        date: str | None = None,
        summary: str = "",
        characters_present: list[str] | None = None,
        key_events: list[str] | None = None,
        evolution_notes: str = "",
        markdown_content: str | None = None,
    ) -> dict[str, Any]:
        """
        Add a new session to the campaign.

        Args:
            session_number: Sequential session number
            title: Session title
            date: Session date (ISO format, defaults to today)
            summary: Brief session summary
            characters_present: List of character names/IDs
            key_events: List of important events
            evolution_notes: Notes on how campaign evolved
            markdown_content: Full markdown narrative (optional)

        Returns:
            Session data dictionary
        """
        if date is None:
            date = datetime.now().isoformat()

        if characters_present is None:
            characters_present = []

        if key_events is None:
            key_events = []

        session_data = {
            "session_number": session_number,
            "title": title,
            "date": date,
            "summary": summary,
            "characters_present": characters_present,
            "key_events": key_events,
            "evolution_notes": evolution_notes,
            "created_at": datetime.now().isoformat(),
        }

        # Add to sessions list
        # Remove existing session with same number if present
        self.sessions = [s for s in self.sessions if s.get("session_number") != session_number]
        self.sessions.append(session_data)
        self.sessions.sort(key=lambda x: x.get("session_number", 0))

        # Save JSON
        self._save_json(self.sessions_file, self.sessions)

        # Save Markdown if provided
        if markdown_content:
            md_file = self.base_path / f"session_{session_number:02d}.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"session_number: {session_number}\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date}\n")
                f.write("---\n\n")
                f.write(markdown_content)

        return session_data

    def update_character(
        self, character_name: str, changes: dict[str, Any], session_number: int | None = None
    ):
        """
        Update character progression.

        Args:
            character_name: Character name/ID
            changes: Dictionary of changes (level, stats, equipment, etc.)
            session_number: Session where changes occurred
        """
        if character_name not in self.characters:
            self.characters[character_name] = {
                "name": character_name,
                "created_at": datetime.now().isoformat(),
                "progression": [],
            }

        progression_entry = {
            "session_number": session_number,
            "date": datetime.now().isoformat(),
            "changes": changes,
        }

        self.characters[character_name]["progression"].append(progression_entry)
        self.characters[character_name]["last_updated"] = datetime.now().isoformat()

        self._save_json(self.characters_file, self.characters)

    def add_evolution_entry(
        self,
        entry_type: str,
        description: str,
        session_number: int | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Add a campaign evolution entry.

        Args:
            entry_type: Type of evolution (world_change, rule_change, etc.)
            description: Description of the change
            session_number: Session where change occurred
            metadata: Additional metadata
        """
        evolution_entry = {
            "type": entry_type,
            "description": description,
            "session_number": session_number,
            "date": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        self.evolution.append(evolution_entry)
        self._save_json(self.evolution_file, self.evolution)

    def get_campaign_data(self) -> dict[str, Any]:
        """Get complete campaign data for binder generation."""
        return {
            "campaign_id": self.campaign_id,
            "sessions": self.sessions,
            "characters": self.characters,
            "evolution": self.evolution,
            "session_count": len(self.sessions),
            "character_count": len(self.characters),
            "last_updated": datetime.now().isoformat(),
        }

    def get_session_markdown(self, session_number: int) -> str | None:
        """Get markdown content for a session."""
        md_file = self.base_path / f"session_{session_number:02d}.md"
        if md_file.exists():
            return md_file.read_text(encoding="utf-8")
        return None
