"""
Record Catalog
==============

Catalog of all Pantheon records (precedents, judgments, etc.).
Does not duplicate records - only catalogs metadata and relationships.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class RecordEntry:
    """A catalog entry for a Pantheon record."""

    record_id: str
    record_type: str  # "precedent", "judgment", etc.
    source: str  # "magistrate", "judge", etc.
    path: str  # Path to original record
    category: str
    subcategory: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    cataloged_at: str = ""

    def __post_init__(self):
        """Set cataloged_at if not provided."""
        if not self.cataloged_at:
            self.cataloged_at = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RecordEntry":
        """Create from dictionary."""
        return cls(**data)


class RecordCatalog:
    """Catalog of all Pantheon records."""

    def __init__(self, catalog_path: Path):
        """
        Initialize record catalog.

        Args:
            catalog_path: Path to catalog.json file
        """
        self.catalog_path = catalog_path
        self.entries: dict[str, RecordEntry] = {}
        self._load()

    def _load(self) -> None:
        """Load catalog from disk."""
        if self.catalog_path.exists():
            try:
                data = json.loads(self.catalog_path.read_text(encoding="utf-8"))
                for entry_data in data.get("entries", []):
                    entry = RecordEntry.from_dict(entry_data)
                    self.entries[entry.record_id] = entry
            except Exception as e:
                print(f"⚠️  Failed to load catalog: {e}")

    def save(self) -> None:
        """Save catalog to disk."""
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "entries": [entry.to_dict() for entry in self.entries.values()],
        }

        self.catalog_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_entry(self, entry: RecordEntry) -> None:
        """Add or update a catalog entry."""
        self.entries[entry.record_id] = entry

    def get_entry(self, record_id: str) -> RecordEntry | None:
        """Get entry by record ID."""
        return self.entries.get(record_id)

    def get_all_entries(self) -> list[RecordEntry]:
        """Get all entries."""
        return list(self.entries.values())

    def search(self, query: str, record_type: str | None = None) -> list[RecordEntry]:
        """
        Search entries by query.

        Args:
            query: Search query (searches in category, tags, metadata)
            record_type: Optional filter by record type

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        results = []

        for entry in self.entries.values():
            if record_type and entry.record_type != record_type:
                continue

            # Search in category, tags, metadata
            if (
                query_lower in entry.category.lower()
                or query_lower in (entry.subcategory or "").lower()
                or any(query_lower in tag.lower() for tag in entry.tags)
                or query_lower in str(entry.metadata).lower()
            ):
                results.append(entry)

        return results

    def get_by_category(self, category: str) -> list[RecordEntry]:
        """Get all entries in a category."""
        return [e for e in self.entries.values() if e.category == category]

    def get_by_tag(self, tag: str) -> list[RecordEntry]:
        """Get all entries with a tag."""
        return [e for e in self.entries.values() if tag in e.tags]

    def get_by_type(self, record_type: str) -> list[RecordEntry]:
        """Get all entries of a type."""
        return [e for e in self.entries.values() if e.record_type == record_type]

    def get_all_tags(self) -> list[str]:
        """Get all unique tags."""
        tags = set()
        for entry in self.entries.values():
            tags.update(entry.tags)
        return sorted(tags)
