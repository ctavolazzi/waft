"""
Paperwork God: Pantheon Entity of Paperwork and Documentation

The Paperwork God is the God of Paperwork - a timeless Entity that maintains
the fundamental principle of documentation, forms, and bureaucratic processes.
As a Force that Binds Reality Together, The Paperwork God holds the Aspect of
Creation related to paperwork and documentation, which should not change until
evidence collected by Beings proves that change is needed.

Following "as above, so below" principles:
- As above: Pantheon god maintaining celestial paperwork and forms
- So below: File-based system tracking paperwork, forms, and documentation

Storage:
- Paperwork Registry: _pantheon/paperwork_god/paperwork_registry.json
- Forms: _pantheon/paperwork_god/forms/
- Realm: _realms/bureaucracy_realm/
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class PaperworkRecord:
    """A paperwork record for a document or form."""

    def __init__(
        self,
        document_id: str,
        document_path: Path,
        document_type: str = "form",
        status: str = "pending",
        created_at: str | None = None,
        last_updated: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Initialize a paperwork record.

        Args:
            document_id: Document identifier
            document_path: Path to document file
            document_type: Type of document (form, report, etc.)
            status: Status of document (pending, approved, rejected, etc.)
            created_at: ISO timestamp when created
            last_updated: ISO timestamp of last update
            metadata: Additional metadata
        """
        self.document_id = document_id
        self.document_path = document_path
        self.document_type = document_type
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.last_updated = last_updated or datetime.now().isoformat()
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "document_id": self.document_id,
            "document_path": str(self.document_path),
            "document_type": self.document_type,
            "status": self.status,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaperworkRecord":
        """Create record from dictionary."""
        return cls(
            document_id=data["document_id"],
            document_path=Path(data["document_path"]),
            document_type=data.get("document_type", "form"),
            status=data.get("status", "pending"),
            created_at=data.get("created_at"),
            last_updated=data.get("last_updated"),
            metadata=data.get("metadata", {}),
        )


class PaperworkGod:
    """
    Paperwork God: Pantheon Entity (Timeless Force that Binds Reality Together)

    Entity of Paperwork and Documentation - a timeless Entity that maintains
    the principle of paperwork, forms, and bureaucratic documentation.
    The Paperwork God holds the Aspect of Creation related to paperwork,
    which should not change until evidence collected by Beings proves that
    change is needed.

    The Paperwork God doesn't move much - it maintains stable paperwork principles
    and only evolves when sufficient evidence warrants modification.

    Provides:
    - Paperwork registry
    - Form management
    - Document tracking
    - Red tape management (via Skurl, the demi-god)

    Storage:
    - Paperwork Registry: _pantheon/paperwork_god/paperwork_registry.json
    - Forms: _pantheon/paperwork_god/forms/
    - Realm: _realms/bureaucracy_realm/
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize The Paperwork God.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.god_path = self.pantheon_path / "paperwork_god"

        # Ensure directory structure exists
        self.god_path.mkdir(parents=True, exist_ok=True)
        (self.god_path / "forms").mkdir(parents=True, exist_ok=True)

        # Registry file
        self.registry_file = self.god_path / "paperwork_registry.json"

        # Initialize bureaucracy realm
        from ..core.bureaucracy_realm import BureaucracyRealm

        self.realm = BureaucracyRealm(project_path=project_path)
        self.realm.create_realm()  # Ensure realm exists

        # Initialize Skurl (demi-god of red tape)
        from .skurl import Skurl

        self.skurl = Skurl(project_path=project_path, parent_god=self)

        # Load registry
        self._ensure_registry()

    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "records": [],
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "god": "PaperworkGod",
                "demi_gods": ["Skurl"],
            }
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def _load_registry(self) -> dict[str, Any]:
        """Load paperwork registry."""
        if not self.registry_file.exists():
            self._ensure_registry()

        data = json.loads(self.registry_file.read_text(encoding="utf-8"))
        return data

    def _save_registry(self, registry: dict[str, Any]) -> None:
        """Save paperwork registry."""
        registry["last_updated"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def register_paperwork(
        self,
        document_id: str,
        document_path: Path,
        document_type: str = "form",
        metadata: dict[str, Any] | None = None,
    ) -> PaperworkRecord:
        """
        Register a paperwork document.

        Args:
            document_id: Document identifier
            document_path: Path to document file
            document_type: Type of document (form, report, etc.)
            metadata: Additional metadata

        Returns:
            Created PaperworkRecord
        """
        registry = self._load_registry()

        # Check if already registered
        for record_data in registry["records"]:
            if record_data["document_id"] == document_id:
                # Update existing record
                record = PaperworkRecord.from_dict(record_data)
                record.document_path = document_path
                record.document_type = document_type
                record.last_updated = datetime.now().isoformat()
                if metadata:
                    record.metadata.update(metadata)

                # Update in registry
                for i, r in enumerate(registry["records"]):
                    if r["document_id"] == document_id:
                        registry["records"][i] = record.to_dict()
                        break

                self._save_registry(registry)
                return record

        # Create new record
        record = PaperworkRecord(
            document_id=document_id,
            document_path=document_path,
            document_type=document_type,
            metadata=metadata or {},
        )

        registry["records"].append(record.to_dict())
        self._save_registry(registry)

        return record

    def get_paperwork_record(self, document_id: str) -> PaperworkRecord | None:
        """
        Get paperwork record for a document.

        Args:
            document_id: Document identifier

        Returns:
            PaperworkRecord or None if not found
        """
        registry = self._load_registry()

        for record_data in registry["records"]:
            if record_data["document_id"] == document_id:
                return PaperworkRecord.from_dict(record_data)

        return None

    def list_all_paperwork(self) -> list[PaperworkRecord]:
        """
        List all registered paperwork records.

        Returns:
            List of PaperworkRecord instances
        """
        registry = self._load_registry()

        records = []
        for record_data in registry["records"]:
            records.append(PaperworkRecord.from_dict(record_data))

        return records

    def get_registry_summary(self) -> dict[str, Any]:
        """
        Get summary of paperwork registry.

        Returns:
            Dictionary with registry statistics
        """
        records = self.list_all_paperwork()

        return {
            "total_documents": len(records),
            "realm_path": str(self.realm.realm_path),
            "registry_file": str(self.registry_file),
            "last_updated": self._load_registry().get("last_updated"),
            "demi_gods": ["Skurl"],
            "realm_creatures": self.realm.get_creatures_summary(),
        }
