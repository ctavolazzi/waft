"""
Corporations System: Manage multiple corporations

Main system for managing corporations, their economic simulations,
and integration with WAFT systems (Beings, Realities, Typst).
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal
import json
import os

from .corporation import Corporation
from .security import validate_corp_id, validate_path_in_project, write_secure_file, read_secure_json, set_directory_permissions


class CorporationsSystem:
    """
    Main system for managing multiple corporations.
    
    Provides:
    - Corporation creation and management
    - Economic simulation coordination
    - Integration with Being system
    - Typst document generation
    - Experiment configuration management
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize Corporations System.
        
        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = Path(project_path)
        self.corporations_path = self.project_path / "_realms" / "bureaucracy_realm" / "corporations"
        self.corporations_path.mkdir(parents=True, exist_ok=True)
        
        # Registry of loaded corporations
        self._corporations: Dict[str, Corporation] = {}
        
        # System manifest
        self.manifest_path = self.corporations_path / "system_manifest.json"
        self._ensure_manifest()
    
    def _ensure_manifest(self) -> None:
        """Ensure system manifest exists."""
        if not self.manifest_path.exists():
            manifest = {
                "corporations": [],
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat()
            }
            # CRITICAL: Use secure file write with permissions
            write_secure_file(
                self.manifest_path,
                json.dumps(manifest, indent=2),
                encoding="utf-8"
            )
            # Set directory permissions
            set_directory_permissions(self.manifest_path.parent)
    
    def create_corporation(
        self,
        name: str,
        sector: str = "",
        mission: str = "",
        founded_date: Optional[datetime] = None,
        initial_capital: Optional[Decimal] = None,
        corp_id: Optional[str] = None
    ) -> Corporation:
        """
        Create a new corporation.
        
        Args:
            name: Corporation name
            sector: Industry sector
            mission: Mission statement
            founded_date: Founding date (defaults to now)
            initial_capital: Initial capital investment
            corp_id: Optional corporation ID (auto-generated if not provided)
            
        Returns:
            Created Corporation
        """
        if founded_date is None:
            founded_date = datetime.utcnow()
        
        if corp_id is None:
            # Generate corp_id from name and timestamp
            timestamp = founded_date.strftime("%Y%m%d_%H%M%S")
            safe_name = name.lower().replace(" ", "_").replace("-", "_")
            corp_id = f"{safe_name}_{timestamp}"
        
        # CRITICAL: Validate corp_id for security
        if not validate_corp_id(corp_id):
            raise ValueError(f"Invalid corp_id: {corp_id}. Must contain only alphanumeric characters, underscores, and hyphens.")
        
        # Create corporation
        corporation = Corporation(
            corp_id=corp_id,
            name=name,
            founded_date=founded_date,
            sector=sector,
            mission=mission,
            project_path=self.project_path,
            initial_capital=initial_capital
        )
        
        # Register in system
        self._corporations[corp_id] = corporation
        self._update_manifest()
        
        return corporation
    
    def get_corporation(self, corp_id: str) -> Optional[Corporation]:
        """
        Get a corporation by ID.
        
        Args:
            corp_id: Corporation identifier
            
        Returns:
            Corporation if found, None otherwise
        """
        # Check if already loaded
        if corp_id in self._corporations:
            return self._corporations[corp_id]
        
        # Try to load from disk
        corp_path = self.corporations_path / corp_id
        manifest_path = corp_path / "corporate_manifest.json"
        
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            corporation = Corporation.from_dict(manifest, project_path=self.project_path)
            self._corporations[corp_id] = corporation
            return corporation
        
        return None
    
    def list_corporations(self) -> List[str]:
        """
        List all corporation IDs.
        
        Returns:
            List of corporation IDs
        """
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return manifest.get("corporations", [])
    
    def get_all_corporations(self) -> List[Corporation]:
        """
        Get all corporations.
        
        Returns:
            List of all Corporation objects
        """
        corp_ids = self.list_corporations()
        corporations = []
        
        for corp_id in corp_ids:
            corp = self.get_corporation(corp_id)
            if corp:
                corporations.append(corp)
        
        return corporations
    
    def _update_manifest(self) -> None:
        """Update system manifest with current corporations."""
        try:
            manifest = read_secure_json(self.manifest_path)
        except (ValueError, IOError, json.JSONDecodeError):
            # If manifest is invalid, create new one
            manifest = {
                "corporations": [],
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat()
            }
        
        # Update corporation list
        corp_ids = list(self._corporations.keys())
        
        # Also check disk for any not in memory
        if self.corporations_path.exists():
            for corp_dir in self.corporations_path.iterdir():
                # CRITICAL: Validate directory name before using
                if corp_dir.is_dir() and validate_corp_id(corp_dir.name):
                    if (corp_dir / "corporate_manifest.json").exists():
                        if corp_dir.name not in corp_ids:
                            corp_ids.append(corp_dir.name)
        
        manifest["corporations"] = sorted(set(corp_ids))
        manifest["last_updated"] = datetime.utcnow().isoformat()
        
        # CRITICAL: Use secure file write
        write_secure_file(
            self.manifest_path,
            json.dumps(manifest, indent=2),
            encoding="utf-8"
        )
