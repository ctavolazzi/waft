"""
External Drive Realm: Pantheon Entity (Timeless Force that Binds Reality Together)

The External Drive Realm is a timeless Entity that maintains the fundamental
principle of content-aware storage routing. As a Force that Binds Reality Together,
the External Drive Realm holds the Aspect of Creation related to storage and
content organization, which should not change until evidence collected by Beings
proves that change is needed.

The External Drive Realm doesn't move much - it maintains stable storage principles
and only evolves when sufficient evidence warrants modification of its fundamental nature.

Following "as above, so below" principles:
- As above: Realm Entity organizing storage across physical boundaries
- So below: File-based system managing content routing to external drives
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..utils import (
    StorageRegistry,
    classify_content_type,
    detect_external_drive,
    get_external_drive_base,
)


class ExternalDriveRealm:
    """
    External Drive Realm: Pantheon Entity of Storage and Content Organization

    A timeless Entity that maintains the fundamental principle of content-aware
    storage routing. The Realm manages the external drive as a bounded space where
    augmented content is stored, following stable storage principles.

    Storage:
    - Realm Registry: _pantheon/external_drive_realm/realm_registry.json
    - Content Manifest: _pantheon/external_drive_realm/content_manifest.json
    - Realm Status: _pantheon/external_drive_realm/realm_status.json
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize the External Drive Realm.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.realm_path = self.pantheon_path / "external_drive_realm"

        # Ensure directory structure exists
        self.realm_path.mkdir(parents=True, exist_ok=True)
        (self.realm_path / "realms").mkdir(parents=True, exist_ok=True)
        (self.realm_path / "content").mkdir(parents=True, exist_ok=True)

        # Registry files
        self.registry_file = self.realm_path / "realm_registry.json"
        self.manifest_file = self.realm_path / "content_manifest.json"
        self.status_file = self.realm_path / "realm_status.json"

        # Initialize registries
        self._ensure_registry()
        self._update_realm_status()

    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "realms": [],
                "drive_configurations": {},
                "storage_principles": {
                    "core_content_local": True,
                    "augmented_content_external": True,
                    "fallback_to_local": True,
                },
                "created_at": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat(),
            }
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def _update_realm_status(self) -> None:
        """Update realm status with current drive availability."""
        drive_path = detect_external_drive()
        drive_available = drive_path is not None

        status = {
            "realm_active": drive_available,
            "drive_path": str(drive_path) if drive_path else None,
            "drive_name": "Easystore",
            "last_checked": datetime.now().isoformat(),
            "storage_stats": self._get_storage_stats() if drive_available else {},
        }

        self.status_file.write_text(json.dumps(status, indent=2), encoding="utf-8")

    def _get_storage_stats(self) -> dict[str, Any]:
        """Get storage statistics."""
        try:
            registry = StorageRegistry(self.project_path)
            stats = registry.get_storage_stats()
            return {
                "total_content": stats.get("total_content", 0),
                "content_on_external": stats.get("content_on_external", 0),
                "content_local": stats.get("content_local", 0),
                "total_pdfs": stats.get("total_pdfs", 0),
                "pdfs_on_external": stats.get("pdfs_on_external", 0),
                "pdfs_local": stats.get("pdfs_local", 0),
            }
        except Exception:
            return {}

    def register_realm(
        self, realm_name: str, drive_name: str = "Easystore", project_name: str | None = None
    ) -> dict[str, Any]:
        """
        Register a new realm on the external drive.

        Args:
            realm_name: Name of the realm (e.g., "Universe", "Earth")
            drive_name: Name of the external drive
            project_name: Project name (auto-detected if None)

        Returns:
            Realm registration data
        """
        # Detect drive
        drive_path = detect_external_drive(drive_name)
        if not drive_path:
            return {"success": False, "error": f"External drive '{drive_name}' not available"}

        # Get base path
        try:
            base_path = get_external_drive_base(project_name)
            if not base_path:
                return {"success": False, "error": "Could not create external drive base path"}
        except Exception as e:
            return {"success": False, "error": str(e)}

        # Create realm structure: Realms/[realm_name]/
        realm_storage_path = base_path / "Realms" / realm_name
        realm_storage_path.mkdir(parents=True, exist_ok=True)

        # Register realm
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))

        realm_data = {
            "realm_id": f"realm_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "realm_name": realm_name,
            "drive_name": drive_name,
            "drive_path": str(drive_path),
            "realm_storage_path": str(realm_storage_path),
            "project_name": project_name or Path.cwd().name,
            "created_at": datetime.now().isoformat(),
            "status": "active",
        }

        registry["realms"].append(realm_data)
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        # Update status
        self._update_realm_status()

        return {"success": True, "realm": realm_data}

    def get_realm_storage_path(
        self, realm_name: str, relative_path: Path, project_name: str | None = None
    ) -> Path | None:
        """
        Get storage path for content in a realm.

        Args:
            realm_name: Name of the realm
            relative_path: Relative path within the realm
            project_name: Project name (auto-detected if None)

        Returns:
            Full path to storage location, or None if drive not available
        """
        # Get base path
        base_path = get_external_drive_base(project_name)
        if not base_path:
            return None

        # Build realm path: Realms/[realm_name]/[relative_path]
        realm_path = base_path / "Realms" / realm_name / relative_path

        # Create directory structure
        try:
            realm_path.parent.mkdir(parents=True, exist_ok=True)
            return realm_path.resolve()
        except Exception:
            return None

    def route_content_to_realm(
        self, content_path: Path, realm_name: str, project_name: str | None = None
    ) -> Path | None:
        """
        Route content to a specific realm on external drive.

        This is the Realm Entity's method for content routing, maintaining
        the stable principle of realm-based storage organization.

        Args:
            content_path: Path to content (relative to project)
            realm_name: Name of the realm to route to
            project_name: Project name (auto-detected if None)

        Returns:
            Path where content should be stored, or None if routing failed
        """
        # Check if content should go to external drive
        content_type = classify_content_type(content_path)

        # Core content stays local (realm doesn't handle it)
        if content_type == "core":
            return None

        # Augmented content routes to realm
        realm_storage = self.get_realm_storage_path(
            realm_name=realm_name, relative_path=content_path, project_name=project_name
        )

        if realm_storage:
            # Register content in manifest
            self._register_content_in_manifest(
                content_path=content_path,
                realm_name=realm_name,
                storage_path=realm_storage,
                content_type=content_type,
            )

        return realm_storage

    def _register_content_in_manifest(
        self, content_path: Path, realm_name: str, storage_path: Path, content_type: str
    ) -> None:
        """Register content in the realm manifest."""
        if not self.manifest_file.exists():
            manifest = {"content": [], "created_at": datetime.now().isoformat()}
        else:
            manifest = json.loads(self.manifest_file.read_text(encoding="utf-8"))

        content_entry = {
            "content_path": str(content_path),
            "realm_name": realm_name,
            "storage_path": str(storage_path),
            "content_type": content_type,
            "registered_at": datetime.now().isoformat(),
        }

        # Check if already registered
        existing = [
            entry
            for entry in manifest["content"]
            if entry.get("content_path") == str(content_path)
            and entry.get("realm_name") == realm_name
        ]

        if not existing:
            manifest["content"].append(content_entry)
            manifest["last_update"] = datetime.now().isoformat()
            self.manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    def get_realm_summary(self) -> dict[str, Any]:
        """
        Get summary of the External Drive Realm.

        Returns:
            Summary of realm status, registered realms, and storage stats
        """
        # Load status
        if self.status_file.exists():
            status = json.loads(self.status_file.read_text(encoding="utf-8"))
        else:
            status = {}

        # Load registry
        if self.registry_file.exists():
            registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        else:
            registry = {"realms": []}

        # Load manifest
        if self.manifest_file.exists():
            manifest = json.loads(self.manifest_file.read_text(encoding="utf-8"))
            content_count = len(manifest.get("content", []))
        else:
            content_count = 0

        return {
            "realm_active": status.get("realm_active", False),
            "drive_available": status.get("realm_active", False),
            "drive_path": status.get("drive_path"),
            "registered_realms": len(registry.get("realms", [])),
            "content_in_realms": content_count,
            "storage_principles": registry.get("storage_principles", {}),
            "storage_stats": status.get("storage_stats", {}),
            "last_update": status.get("last_checked"),
        }

    def list_realms(self) -> list[dict[str, Any]]:
        """
        List all registered realms.

        Returns:
            List of realm data
        """
        if not self.registry_file.exists():
            return []

        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        return registry.get("realms", [])

    def get_realm_content(self, realm_name: str) -> list[dict[str, Any]]:
        """
        Get all content stored in a specific realm.

        Args:
            realm_name: Name of the realm

        Returns:
            List of content entries in the realm
        """
        if not self.manifest_file.exists():
            return []

        manifest = json.loads(self.manifest_file.read_text(encoding="utf-8"))
        return [
            entry for entry in manifest.get("content", []) if entry.get("realm_name") == realm_name
        ]
