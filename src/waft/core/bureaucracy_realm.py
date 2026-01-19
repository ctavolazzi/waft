"""
Bureaucracy Realm - Realm for bureaucratic operations and personnel management.

Manages realm structure, personnel files, and integration with BureaucracyGod.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..reality import RealitySystem, RealityType
from ..being import BeingSystem
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
    
    def __init__(self, project_path: Optional[Path] = None):
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
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            try:
                os.chmod(directory, 0o700)
            except (OSError, PermissionError):
                pass
    
    def create_realm(self) -> Dict[str, Any]:
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
                    "purpose": "bureaucratic_operations"
                }
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
            "god": "BureaucracyGod",
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
