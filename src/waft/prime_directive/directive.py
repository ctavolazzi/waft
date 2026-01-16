"""
Prime Directive: The Central Organizing Principle

The Prime Directive contains the core principles that guide all of WAFT.
Everything in the system points back to these principles.

Core Principles:
- "Don't just build agents. Breed them."
- "Humanity creates reality"
- Evolutionary principles (Scint system, fitness functions)
- Being lifecycle principles
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import hashlib


class PrimeDirective:
    """
    The Prime Directive - the central organizing principle of WAFT.
    
    Stores core principles, tracks versions, maintains change history,
    validates integrity, and tracks what references this directive.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        directive_path: Optional[Path] = None
    ):
        """
        Initialize the Prime Directive.
        
        Args:
            project_path: Path to project root
            directive_path: Path to directive storage (default: _hidden/.truth/celestial_body/heart/)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        
        if directive_path is None:
            directive_path = project_path / "_hidden" / ".truth" / "celestial_body" / "heart"
        else:
            directive_path = Path(directive_path)
        
        self.directive_path = directive_path
        self.directive_path.mkdir(parents=True, exist_ok=True)
        
        self.directive_file = directive_path / "directive.json"
        
        # Core principles
        self.principles: List[str] = []
        self.version: str = "1.0.0"
        self.created_at: str = datetime.now().isoformat()
        self.updated_at: str = datetime.now().isoformat()
        
        # Change history
        self.change_history: List[Dict[str, Any]] = []
        
        # Reference tracking (what references this directive)
        self.references: List[Dict[str, Any]] = []
        
        # Load existing directive or initialize with defaults
        if self.directive_file.exists():
            self._load()
        else:
            self._initialize_defaults()
            self._save()
    
    def _initialize_defaults(self):
        """Initialize with default core principles."""
        self.principles = [
            "Don't just build agents. Breed them.",
            "Humanity creates reality",
            "Code is DNA - agents evolve through genetic modification",
            "Scint System serves as the fitness function",
            "Beings learn, evolve, and pass memories upward",
            "Everything points back to the Prime Directive",
            "Evolution is recorded generation after generation, cycle after cycle, forevermore",
            "Observation Creates the Bridge",
        ]
        
        # Record initial creation
        self.change_history.append({
            "version": self.version,
            "timestamp": self.created_at,
            "type": "creation",
            "description": "Prime Directive initialized with core principles",
            "principles": self.principles.copy(),
        })
    
    def _load(self):
        """Load directive from disk."""
        with open(self.directive_file, 'r') as f:
            data = json.load(f)
        
        self.principles = data.get("principles", [])
        self.version = data.get("version", "1.0.0")
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.updated_at = data.get("updated_at", datetime.now().isoformat())
        self.change_history = data.get("change_history", [])
        self.references = data.get("references", [])
        
        # Ensure "Observation Creates the Bridge" is present
        if "Observation Creates the Bridge" not in self.principles:
            self.add_principle("Observation Creates the Bridge", reason="Realm colonization system requirement")
    
    def _save(self):
        """Save directive to disk."""
        data = {
            "principles": self.principles,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "change_history": self.change_history,
            "references": self.references,
        }
        
        with open(self.directive_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_principles(self) -> List[str]:
        """Get all core principles."""
        return self.principles.copy()
    
    def add_principle(self, principle: str, reason: Optional[str] = None) -> bool:
        """
        Add a new principle.
        
        Args:
            principle: The principle to add
            reason: Optional reason for adding this principle
            
        Returns:
            True if added successfully
        """
        if principle in self.principles:
            return False
        
        self.principles.append(principle)
        self.updated_at = datetime.now().isoformat()
        
        # Update version (patch increment)
        version_parts = self.version.split('.')
        version_parts[2] = str(int(version_parts[2]) + 1)
        self.version = '.'.join(version_parts)
        
        # Record change
        self.change_history.append({
            "version": self.version,
            "timestamp": self.updated_at,
            "type": "add_principle",
            "description": f"Added principle: {principle}",
            "reason": reason,
            "principle": principle,
        })
        
        self._save()
        return True
    
    def remove_principle(self, principle: str, reason: Optional[str] = None) -> bool:
        """
        Remove a principle.
        
        Args:
            principle: The principle to remove
            reason: Optional reason for removal
            
        Returns:
            True if removed successfully
        """
        if principle not in self.principles:
            return False
        
        self.principles.remove(principle)
        self.updated_at = datetime.now().isoformat()
        
        # Update version (minor increment for removal)
        version_parts = self.version.split('.')
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = "0"
        self.version = '.'.join(version_parts)
        
        # Record change
        self.change_history.append({
            "version": self.version,
            "timestamp": self.updated_at,
            "type": "remove_principle",
            "description": f"Removed principle: {principle}",
            "reason": reason,
            "principle": principle,
        })
        
        self._save()
        return True
    
    def update_principle(self, old_principle: str, new_principle: str, reason: Optional[str] = None) -> bool:
        """
        Update an existing principle.
        
        Args:
            old_principle: The principle to replace
            new_principle: The new principle
            reason: Optional reason for update
            
        Returns:
            True if updated successfully
        """
        if old_principle not in self.principles:
            return False
        
        index = self.principles.index(old_principle)
        self.principles[index] = new_principle
        self.updated_at = datetime.now().isoformat()
        
        # Update version (minor increment)
        version_parts = self.version.split('.')
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = "0"
        self.version = '.'.join(version_parts)
        
        # Record change
        self.change_history.append({
            "version": self.version,
            "timestamp": self.updated_at,
            "type": "update_principle",
            "description": f"Updated principle: {old_principle} -> {new_principle}",
            "reason": reason,
            "old_principle": old_principle,
            "new_principle": new_principle,
        })
        
        self._save()
        return True
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate directive integrity.
        
        Returns:
            Dict with validation results
        """
        issues = []
        
        # Check principles exist
        if not self.principles:
            issues.append("No principles defined")
        
        # Check version format
        try:
            parts = self.version.split('.')
            if len(parts) != 3:
                issues.append(f"Invalid version format: {self.version}")
            else:
                [int(p) for p in parts]  # Validate numeric
        except ValueError:
            issues.append(f"Invalid version format: {self.version}")
        
        # Check change history consistency
        if len(self.change_history) == 0:
            issues.append("No change history (should have at least creation)")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "version": self.version,
            "principle_count": len(self.principles),
            "reference_count": len(self.references),
        }
    
    def add_reference(self, reference_type: str, reference_id: str, description: Optional[str] = None):
        """
        Add a reference to this directive.
        
        Args:
            reference_type: Type of reference (e.g., "being", "reality", "system")
            reference_id: ID of the referencing entity
            description: Optional description
        """
        reference = {
            "type": reference_type,
            "id": reference_id,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Avoid duplicates
        if reference not in self.references:
            self.references.append(reference)
            self._save()
    
    def get_references(self, reference_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get references to this directive.
        
        Args:
            reference_type: Optional filter by type
            
        Returns:
            List of references
        """
        if reference_type:
            return [r for r in self.references if r["type"] == reference_type]
        return self.references.copy()
    
    def get_change_history(self) -> List[Dict[str, Any]]:
        """Get change history."""
        return self.change_history.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "principles": self.principles,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "change_history": self.change_history,
            "references": self.references,
        }
