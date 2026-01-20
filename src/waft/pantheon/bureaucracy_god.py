"""
BureaucracyGod: God of Bureaucracy and Personnel Management

The BureaucracyGod maintains personnel files, tracks Being employment records,
and ensures all bureaucratic processes are properly documented.

Following "as above, so below" principles:
- As above: Pantheon god organizing celestial bureaucracy
- So below: File-based system managing personnel records and CVs
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class PersonnelRecord:
    """A personnel record for a Being."""

    def __init__(
        self,
        being_id: str,
        personnel_file_path: Path,
        cv_version: float = 1.0,
        registered_at: str | None = None,
        last_updated: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Initialize a personnel record.

        Args:
            being_id: Being identifier
            personnel_file_path: Path to personnel file directory
            cv_version: CV version number
            registered_at: ISO timestamp when registered
            last_updated: ISO timestamp of last update
            metadata: Additional metadata
        """
        self.being_id = being_id
        self.personnel_file_path = personnel_file_path
        self.cv_version = cv_version
        self.registered_at = registered_at or datetime.now().isoformat()
        self.last_updated = last_updated or datetime.now().isoformat()
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "being_id": self.being_id,
            "personnel_file_path": str(self.personnel_file_path),
            "cv_version": self.cv_version,
            "registered_at": self.registered_at,
            "last_updated": self.last_updated,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PersonnelRecord":
        """Create record from dictionary."""
        return cls(
            being_id=data["being_id"],
            personnel_file_path=Path(data["personnel_file_path"]),
            cv_version=data.get("cv_version", 1.0),
            registered_at=data.get("registered_at"),
            last_updated=data.get("last_updated"),
            metadata=data.get("metadata", {}),
        )


class BureaucracyGod:
    """
    BureaucracyGod: God of Bureaucracy and Personnel Management

    Maintains registry of all Beings with personnel files, tracks CV versions,
    and manages bureaucratic processes.

    Storage:
    - Personnel Registry: _pantheon/bureaucracy_god/personnel_registry.json
    - Realm: _realms/bureaucracy_realm/
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize the BureaucracyGod.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.god_path = self.pantheon_path / "bureaucracy_god"

        # Ensure directory structure exists
        self.god_path.mkdir(parents=True, exist_ok=True)

        # Registry file
        self.registry_file = self.god_path / "personnel_registry.json"

        # Initialize bureaucracy realm
        from ..core.bureaucracy_realm import BureaucracyRealm

        self.realm = BureaucracyRealm(project_path=project_path)
        self.realm.create_realm()  # Ensure realm exists

        # Load registry
        self._ensure_registry()

    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "records": [],
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            }
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def _load_registry(self) -> dict[str, Any]:
        """Load personnel registry."""
        if not self.registry_file.exists():
            self._ensure_registry()

        data = json.loads(self.registry_file.read_text(encoding="utf-8"))
        return data

    def _save_registry(self, registry: dict[str, Any]) -> None:
        """Save personnel registry."""
        registry["last_updated"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def register_personnel_file(
        self, being_id: str, personnel_file_path: Path, metadata: dict[str, Any] | None = None
    ) -> PersonnelRecord:
        """
        Register a Being's personnel file.

        Args:
            being_id: Being identifier
            personnel_file_path: Path to personnel file directory
            metadata: Additional metadata

        Returns:
            Created PersonnelRecord
        """
        registry = self._load_registry()

        # Check if already registered
        for record_data in registry["records"]:
            if record_data["being_id"] == being_id:
                # Update existing record
                record = PersonnelRecord.from_dict(record_data)
                record.personnel_file_path = personnel_file_path
                record.cv_version += 0.1
                record.last_updated = datetime.now().isoformat()
                if metadata:
                    record.metadata.update(metadata)

                # Update in registry
                for i, r in enumerate(registry["records"]):
                    if r["being_id"] == being_id:
                        registry["records"][i] = record.to_dict()
                        break

                self._save_registry(registry)
                return record

        # Create new record
        record = PersonnelRecord(
            being_id=being_id, personnel_file_path=personnel_file_path, metadata=metadata or {}
        )

        registry["records"].append(record.to_dict())
        self._save_registry(registry)

        return record

    def get_personnel_record(self, being_id: str) -> PersonnelRecord | None:
        """
        Get personnel record for a Being.

        Args:
            being_id: Being identifier

        Returns:
            PersonnelRecord or None if not found
        """
        registry = self._load_registry()

        for record_data in registry["records"]:
            if record_data["being_id"] == being_id:
                return PersonnelRecord.from_dict(record_data)

        return None

    def list_all_personnel(self) -> list[PersonnelRecord]:
        """
        List all registered personnel records.

        Returns:
            List of PersonnelRecord instances
        """
        registry = self._load_registry()

        records = []
        for record_data in registry["records"]:
            records.append(PersonnelRecord.from_dict(record_data))

        return records

    def get_registry_summary(self) -> dict[str, Any]:
        """
        Get summary of personnel registry.

        Returns:
            Dictionary with registry statistics
        """
        records = self.list_all_personnel()

        return {
            "total_personnel": len(records),
            "realm_path": str(self.realm.realm_path),
            "registry_file": str(self.registry_file),
            "last_updated": self._load_registry().get("last_updated"),
        }
