"""
Scenario Realm - Original Realm management for DnD scenarios.

Manages realm creation, structure, and integration with existing systems.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..realm_colonization import RealmColonizationSystem
from ...reality import RealitySystem, RealityType
from ...being import BeingSystem
from .security import validate_realm_path


class ScenarioRealm:
    """
    Manages Original Realm for DnD scenario system.
    
    Features:
    - Realm structure creation
    - PrimeBeing creation via RealmColonizationSystem
    - Reality system integration
    - Path validation for all operations
    - Access control and audit logging
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize Scenario Realm.
        
        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.realm_path = project_path / "_realms" / "dnd_scenario_realm"
        self.realm_path.mkdir(parents=True, exist_ok=True)
        
        # Set directory permissions (0o700)
        os.chmod(self.realm_path, 0o700)
        
        # Initialize systems
        self.realm_colonization = RealmColonizationSystem(project_path=project_path)
        self.reality_system = RealitySystem(project_path=project_path)
        self.being_system = BeingSystem(project_path=project_path)
        
        # Ensure realm structure
        self._ensure_realm_structure()
    
    def _ensure_realm_structure(self) -> None:
        """Ensure realm directory structure exists with proper permissions."""
        directories = [
            "lore/locations",
            "lore/npcs",
            "lore/events",
            "encounters",
            "campaigns",
            "experiments",
            "crystallized_state"
        ]
        
        for dir_path in directories:
            full_path = self.realm_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            os.chmod(full_path, 0o700)
        
        # Create realm manifest if it doesn't exist
        manifest_file = self.realm_path / "realm_manifest.json"
        if not manifest_file.exists():
            manifest = {
                "realm_id": "dnd_scenario_realm",
                "realm_name": "DnD Scenario Realm",
                "realm_type": "original",
                "created_at": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            manifest_file.write_text(json.dumps(manifest, indent=2))
            os.chmod(manifest_file, 0o600)
    
    def create_realm(self) -> Dict[str, Any]:
        """
        Create and initialize the scenario realm.
        
        Returns:
            Realm creation metadata
        """
        # Ensure structure
        self._ensure_realm_structure()
        
        # Create Reality for scenario realm
        try:
            reality = self.reality_system.create_reality(
                reality_type=RealityType.LEARNING,
                configuration={
                    "realm_name": "dnd_scenario_realm",
                    "realm_path": str(self.realm_path),
                    "special": True,
                    "purpose": "dnd_scenario_management"
                }
            )
        except Exception as e:
            raise OSError(f"Failed to create realm reality: {e}")
        
        # Create PrimeBeing for realm (via RealmColonizationSystem pattern)
        try:
            the_one = self.being_system.get_or_create_the_one()
            
            prime_being_id = f"prime_being_dnd_scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            from ...being import Being
            
            prime_being = Being(
                being_id=prime_being_id,
                reality_id=reality.reality_id,
                parent_being_id=the_one.being_id,
                custom_name="PrimeBeing-DnD-Scenario",
                skills={
                    "realm_governance": 10.0,
                    "scenario_coordination": 10.0,
                    "lore_management": 10.0
                }
            )
            self.being_system.save_being(prime_being)
        except Exception as e:
            raise OSError(f"Failed to create prime being: {e}")
        
        return {
            "realm_path": str(self.realm_path),
            "reality_id": reality.reality_id,
            "prime_being_id": prime_being_id,
            "created_at": datetime.now().isoformat()
        }
    
    def validate_path(self, path: Path) -> bool:
        """
        Validate path is within realm directory.
        
        Args:
            path: Path to validate
            
        Returns:
            True if valid, False otherwise
        """
        return validate_realm_path(path, self.realm_path)
    
    def get_realm_manifest(self) -> Dict[str, Any]:
        """Get realm manifest."""
        manifest_file = self.realm_path / "realm_manifest.json"
        if manifest_file.exists():
            return json.loads(manifest_file.read_text())
        return {}
