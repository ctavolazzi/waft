"""
Bureaucracy Realm - Realm for bureaucratic operations and personnel management.

Manages realm structure, personnel files, and integration with BureaucracyGod.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from ..being import BeingSystem
from ..reality import RealitySystem, RealityType
from .dnd_scenario.security import validate_realm_path


class BureaucracyRealm:
    """
    Manages Bureaucracy Realm for personnel management and bureaucratic operations.

    Features:
    - Realm structure creation
    - Personnel file management
    - Integration with BureaucracyGod
    - Path validation for all operations
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize Bureaucracy Realm.

        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.realm_path = project_path / "_realms" / "bureaucracy_realm"
        self.realm_path.mkdir(parents=True, exist_ok=True)

        # Set directory permissions (0o700)
        try:
            os.chmod(self.realm_path, 0o700)
        except (OSError, PermissionError):
            pass

        # Initialize systems
        self.reality_system = RealitySystem(project_path=project_path)
        self.being_system = BeingSystem(project_path=project_path)

        # Ensure realm structure
        self._ensure_realm_structure()

    def _ensure_realm_structure(self) -> None:
        """Ensure realm directory structure exists with proper permissions."""
        directories = [
            self.realm_path / "personnel_registry",
            self.realm_path / "forms",
            self.realm_path / "records",
            self.realm_path / "creatures",
            self.realm_path / "creatures" / "goblins",
            self.realm_path / "creatures" / "ghouls",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            try:
                os.chmod(directory, 0o700)
            except (OSError, PermissionError):
                pass

    def create_realm(self) -> dict[str, Any]:
        """
        Create and initialize the bureaucracy realm.

        Returns:
            Realm creation metadata
        """
        # Ensure structure
        self._ensure_realm_structure()

        # Create Reality for bureaucracy realm
        try:
            reality = self.reality_system.create_reality(
                reality_type=RealityType.LEARNING,
                configuration={
                    "realm_name": "bureaucracy_realm",
                    "realm_path": str(self.realm_path),
                    "special": True,
                    "purpose": "bureaucratic_operations",
                },
            )
        except Exception as e:
            raise OSError(f"Failed to create realm reality: {e}")

        # Create realm manifest
        manifest = {
            "realm_name": "bureaucracy_realm",
            "realm_path": str(self.realm_path),
            "reality_id": reality.reality_id,
            "created_at": datetime.now().isoformat(),
            "purpose": "Personnel management and bureaucratic operations",
            "god": "PaperworkGod",
            "demi_god": "Skurl",
            "creatures": {
                "goblins": "Form filers and bureaucratic assistants",
                "ghouls": "Record guardians and archive keepers",
            },
        }

        manifest_path = self.realm_path / "realm_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "realm_path": str(self.realm_path),
            "reality_id": reality.reality_id,
            "created_at": datetime.now().isoformat(),
        }

    def validate_path(self, path: Path) -> bool:
        """
        Validate path is within realm boundaries.

        Args:
            path: Path to validate

        Returns:
            True if valid, False otherwise
        """
        return validate_realm_path(path, self.realm_path)

    def get_creatures_summary(self) -> dict[str, Any]:
        """
        Get summary of creatures in the bureaucracy realm.

        Returns:
            Dictionary with creature statistics
        """
        goblins_path = self.realm_path / "creatures" / "goblins"
        ghouls_path = self.realm_path / "creatures" / "ghouls"

        # Count creature files
        goblin_count = len(list(goblins_path.glob("*.json"))) if goblins_path.exists() else 0
        ghoul_count = len(list(ghouls_path.glob("*.json"))) if ghouls_path.exists() else 0

        return {
            "goblins": goblin_count,
            "ghouls": ghoul_count,
            "total_creatures": goblin_count + ghoul_count,
        }

    def create_goblin(
        self,
        goblin_id: str,
        name: str,
        role: str = "form_filer",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a goblin creature in the bureaucracy realm.

        Args:
            goblin_id: Goblin identifier
            name: Goblin name
            role: Role in bureaucracy (form_filer, record_keeper, etc.)
            metadata: Additional metadata

        Returns:
            Goblin data dictionary
        """
        goblins_path = self.realm_path / "creatures" / "goblins"
        goblins_path.mkdir(parents=True, exist_ok=True)

        goblin_data = {
            "goblin_id": goblin_id,
            "name": name,
            "role": role,
            "type": "goblin",
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        goblin_file = goblins_path / f"{goblin_id}.json"
        goblin_file.write_text(json.dumps(goblin_data, indent=2), encoding="utf-8")

        return goblin_data

    def create_ghoul(
        self,
        ghoul_id: str,
        name: str,
        role: str = "record_guardian",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a ghoul creature in the bureaucracy realm.

        Args:
            ghoul_id: Ghoul identifier
            name: Ghoul name
            role: Role in bureaucracy (record_guardian, archive_keeper, etc.)
            metadata: Additional metadata

        Returns:
            Ghoul data dictionary
        """
        ghouls_path = self.realm_path / "creatures" / "ghouls"
        ghouls_path.mkdir(parents=True, exist_ok=True)

        ghoul_data = {
            "ghoul_id": ghoul_id,
            "name": name,
            "role": role,
            "type": "ghoul",
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        ghoul_file = ghouls_path / f"{ghoul_id}.json"
        ghoul_file.write_text(json.dumps(ghoul_data, indent=2), encoding="utf-8")

        return ghoul_data
