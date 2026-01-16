"""
Guardian Beings: MaintenanceStaff, SecurityTeam, and Curator

Three specialized Beings that maintain, protect, and explore the Prime Directive.
All are children of TheOne Being and have specialized roles.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from ..being import Being, BeingState


class MaintenanceStaff(Being):
    """
    MaintenanceStaff Being: Maintains Prime Directive structure.
    
    Responsibilities:
    - Validates Prime Directive integrity
    - Updates core principles when needed
    - Ensures all references point back to Prime Directive
    - Maintains hourglass/torus data structure
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        project_path: Optional[Path] = None,
        parent_being_id: str = "the_one",
        **kwargs
    ):
        """
        Initialize MaintenanceStaff Being.
        
        Args:
            being_id: Unique identifier
            reality_id: Reality ID
            project_path: Path to project root
            parent_being_id: Parent Being ID (default: TheOne)
            **kwargs: Additional Being initialization args
        """
        # Set specialized personality and goals
        personality = kwargs.get("personality", {})
        personality.update({
            "type": "systematic",
            "traits": ["meticulous", "organized", "maintenance-focused"],
            "focus": "Prime Directive integrity",
        })
        kwargs["personality"] = personality
        
        goals = kwargs.get("goals", [])
        goals.append({
            "type": "maintenance",
            "description": "Maintain Prime Directive structure and integrity",
            "priority": "high",
        })
        kwargs["goals"] = goals
        
        kwargs["custom_name"] = kwargs.get("custom_name", "MaintenanceStaff")
        
        super().__init__(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            **kwargs
        )
        
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.role = "maintenance_staff"
    
    def validate_directive_integrity(self, directive) -> Dict[str, Any]:
        """
        Validate Prime Directive integrity.
        
        Args:
            directive: PrimeDirective instance
            
        Returns:
            Validation results
        """
        validation = directive.validate()
        
        # Record validation in memories
        self.memories.append({
            "type": "validation",
            "timestamp": datetime.now().isoformat(),
            "result": validation,
        })
        
        return validation
    
    def ensure_references(self, directive) -> Dict[str, Any]:
        """
        Ensure all references point back to Prime Directive.
        
        Args:
            directive: PrimeDirective instance
            
        Returns:
            Reference check results
        """
        references = directive.get_references()
        
        # Check for missing references
        missing = []
        # (In full implementation, would check all systems)
        
        result = {
            "total_references": len(references),
            "missing_references": missing,
            "status": "ok" if len(missing) == 0 else "needs_attention",
        }
        
        # Record in memories
        self.memories.append({
            "type": "reference_check",
            "timestamp": datetime.now().isoformat(),
            "result": result,
        })
        
        return result


class SecurityTeam(Being):
    """
    SecurityTeam Being: Protects Prime Directive.
    
    Responsibilities:
    - Monitors access to Prime Directive
    - Validates changes to Prime Directive
    - Enforces security around Heart/CelestialBody
    - Logs all access attempts
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        project_path: Optional[Path] = None,
        parent_being_id: str = "the_one",
        **kwargs
    ):
        """
        Initialize SecurityTeam Being.
        
        Args:
            being_id: Unique identifier
            reality_id: Reality ID
            project_path: Path to project root
            parent_being_id: Parent Being ID (default: TheOne)
            **kwargs: Additional Being initialization args
        """
        # Set specialized personality and goals
        personality = kwargs.get("personality", {})
        personality.update({
            "type": "vigilant",
            "traits": ["protective", "alert", "security-focused"],
            "focus": "Prime Directive protection",
        })
        kwargs["personality"] = personality
        
        goals = kwargs.get("goals", [])
        goals.append({
            "type": "security",
            "description": "Protect Prime Directive from unauthorized access",
            "priority": "critical",
        })
        kwargs["goals"] = goals
        
        kwargs["custom_name"] = kwargs.get("custom_name", "SecurityTeam")
        
        super().__init__(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            **kwargs
        )
        
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.role = "security_team"
        self.access_log: List[Dict[str, Any]] = []
    
    def log_access(self, accessor_id: str, action: str, authorized: bool = True):
        """
        Log access attempt.
        
        Args:
            accessor_id: ID of entity accessing
            action: Action attempted
            authorized: Whether access was authorized
        """
        log_entry = {
            "accessor_id": accessor_id,
            "action": action,
            "authorized": authorized,
            "timestamp": datetime.now().isoformat(),
        }
        
        self.access_log.append(log_entry)
        self.memories.append({
            "type": "access_log",
            "timestamp": datetime.now().isoformat(),
            "entry": log_entry,
        })
    
    def validate_change(self, change_request: Dict[str, Any], requester_id: str) -> Dict[str, Any]:
        """
        Validate a change request to Prime Directive.
        
        Args:
            change_request: Change request data
            requester_id: ID of entity requesting change
            
        Returns:
            Validation result with authorization
        """
        # Log access
        self.log_access(requester_id, f"change_request:{change_request.get('type')}")
        
        # Validate change
        validation = {
            "authorized": False,
            "reason": "Default: requires review",
            "change_type": change_request.get("type"),
            "requester_id": requester_id,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Security rules (can be expanded)
        change_type = change_request.get("type")
        if change_type == "add_principle":
            validation["authorized"] = True
            validation["reason"] = "Adding principles is allowed with proper authorization"
        elif change_type == "remove_principle":
            validation["authorized"] = False
            validation["reason"] = "Removing principles requires special authorization"
        elif change_type == "swap_directive":
            validation["authorized"] = False
            validation["reason"] = "Swapping directive requires Curator authorization"
        
        # Record validation
        self.memories.append({
            "type": "change_validation",
            "timestamp": datetime.now().isoformat(),
            "result": validation,
        })
        
        return validation


class Curator(Being):
    """
    Curator Being: Explores and learns about Prime Directive.
    
    Responsibilities:
    - Builds Karma Museum around Heart
    - Documents evolution history
    - Provides interface for exploring Prime Directive
    - ULTIMATE POWER: Can swap out Prime Directive (with proper authorization)
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        project_path: Optional[Path] = None,
        parent_being_id: str = "the_one",
        **kwargs
    ):
        """
        Initialize Curator Being.
        
        Args:
            being_id: Unique identifier
            reality_id: Reality ID
            project_path: Path to project root
            parent_being_id: Parent Being ID (default: TheOne)
            **kwargs: Additional Being initialization args
        """
        # Set specialized personality and goals
        personality = kwargs.get("personality", {})
        personality.update({
            "type": "curious",
            "traits": ["exploratory", "documenting", "knowledge-seeking"],
            "focus": "Prime Directive exploration and learning",
        })
        kwargs["personality"] = personality
        
        goals = kwargs.get("goals", [])
        goals.append({
            "type": "curation",
            "description": "Build Karma Museum and document Prime Directive evolution",
            "priority": "high",
        })
        kwargs["goals"] = goals
        
        kwargs["custom_name"] = kwargs.get("custom_name", "Curator")
        
        super().__init__(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            **kwargs
        )
        
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.role = "curator"
    
    def swap_prime_directive(
        self,
        new_directive: Dict[str, Any],
        authorization: Dict[str, Any],
        directive,
        security_team: SecurityTeam
    ) -> Dict[str, Any]:
        """
        ULTIMATE POWER: Swap out the Prime Directive.
        
        This is the Curator's ultimate power - the ability to change
        the foundational principles themselves.
        
        Args:
            new_directive: New directive data
            authorization: Authorization data
            directive: PrimeDirective instance
            security_team: SecurityTeam instance for validation
            
        Returns:
            Swap result
        """
        # Validate authorization with SecurityTeam
        change_request = {
            "type": "swap_directive",
            "new_directive": new_directive,
            "authorization": authorization,
        }
        
        validation = security_team.validate_change(change_request, self.being_id)
        
        if not validation.get("authorized"):
            return {
                "success": False,
                "reason": validation.get("reason", "Authorization denied"),
                "timestamp": datetime.now().isoformat(),
            }
        
        # Create backup of old directive
        backup = {
            "old_principles": directive.get_principles(),
            "old_version": directive.version,
            "backup_timestamp": datetime.now().isoformat(),
        }
        
        # Update directive
        # (In full implementation, would update all principles)
        if "principles" in new_directive:
            # Clear existing and add new
            old_principles = directive.get_principles()
            for principle in old_principles:
                directive.remove_principle(principle, reason="Swapped by Curator")
            
            for principle in new_directive["principles"]:
                directive.add_principle(principle, reason="Swapped by Curator")
        
        # Record change in memories
        self.memories.append({
            "type": "directive_swap",
            "timestamp": datetime.now().isoformat(),
            "backup": backup,
            "new_directive": new_directive,
            "authorization": authorization,
        })
        
        return {
            "success": True,
            "backup": backup,
            "new_version": directive.version,
            "timestamp": datetime.now().isoformat(),
        }
    
    def document_evolution(self, evolution_data: Dict[str, Any]):
        """
        Document evolution history.
        
        Args:
            evolution_data: Evolution data to document
        """
        self.memories.append({
            "type": "evolution_documentation",
            "timestamp": datetime.now().isoformat(),
            "data": evolution_data,
        })
    
    def explore_directive(self, directive) -> Dict[str, Any]:
        """
        Explore and learn about Prime Directive.
        
        Args:
            directive: PrimeDirective instance
            
        Returns:
            Exploration results
        """
        exploration = {
            "principles": directive.get_principles(),
            "version": directive.version,
            "references": directive.get_references(),
            "change_history": directive.get_change_history(),
            "explored_at": datetime.now().isoformat(),
        }
        
        # Record exploration
        self.memories.append({
            "type": "directive_exploration",
            "timestamp": datetime.now().isoformat(),
            "results": exploration,
        })
        
        return exploration
