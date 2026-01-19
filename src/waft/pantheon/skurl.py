"""
Skurl: Demi-God of Red Tape

Skurl is a gremlin demi-god who serves under the Paperwork God.
As the demi-god of red tape, Skurl specializes in bureaucratic obstacles,
form complications, and the intricate web of regulations that make simple
tasks require multiple forms, approvals, and signatures.

Following "as above, so below" principles:
- As above: Gremlin demi-god creating celestial red tape
- So below: System tracking bureaucratic obstacles and form complications

Storage:
- Red Tape Registry: _pantheon/paperwork_god/skurl/red_tape_registry.json
- Obstacles: _pantheon/paperwork_god/skurl/obstacles/
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class RedTapeObstacle:
    """A red tape obstacle created by Skurl."""
    
    def __init__(
        self,
        obstacle_id: str,
        description: str,
        required_forms: List[str],
        required_approvals: List[str],
        complexity_level: int = 1,
        created_at: Optional[str] = None,
        resolved_at: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a red tape obstacle.
        
        Args:
            obstacle_id: Obstacle identifier
            description: Description of the obstacle
            required_forms: List of required form IDs
            required_approvals: List of required approval steps
            complexity_level: Complexity level (1-10, higher = more complex)
            created_at: ISO timestamp when created
            resolved_at: ISO timestamp when resolved (None if unresolved)
            metadata: Additional metadata
        """
        self.obstacle_id = obstacle_id
        self.description = description
        self.required_forms = required_forms
        self.required_approvals = required_approvals
        self.complexity_level = complexity_level
        self.created_at = created_at or datetime.now().isoformat()
        self.resolved_at = resolved_at
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert obstacle to dictionary."""
        return {
            "obstacle_id": self.obstacle_id,
            "description": self.description,
            "required_forms": self.required_forms,
            "required_approvals": self.required_approvals,
            "complexity_level": self.complexity_level,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RedTapeObstacle":
        """Create obstacle from dictionary."""
        return cls(
            obstacle_id=data["obstacle_id"],
            description=data["description"],
            required_forms=data.get("required_forms", []),
            required_approvals=data.get("required_approvals", []),
            complexity_level=data.get("complexity_level", 1),
            created_at=data.get("created_at"),
            resolved_at=data.get("resolved_at"),
            metadata=data.get("metadata", {})
        )
    
    @property
    def is_resolved(self) -> bool:
        """Check if obstacle is resolved."""
        return self.resolved_at is not None


class Skurl:
    """
    Skurl: Demi-God of Red Tape
    
    A gremlin demi-god who serves under the Paperwork God. Skurl specializes
    in creating bureaucratic obstacles, form complications, and red tape that
    makes simple tasks require multiple forms, approvals, and signatures.
    
    As a demi-god, Skurl has less power than a full god but serves a specific
    domain (red tape) under the Paperwork God's authority.
    
    Provides:
    - Red tape obstacle creation
    - Form complication tracking
    - Bureaucratic delay management
    - Approval chain complexity
    
    Storage:
    - Red Tape Registry: _pantheon/paperwork_god/skurl/red_tape_registry.json
    - Obstacles: _pantheon/paperwork_god/skurl/obstacles/
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        parent_god: Optional[Any] = None
    ):
        """
        Initialize Skurl, the demi-god of red tape.
        
        Args:
            project_path: Path to project root (default: current directory)
            parent_god: Reference to parent god (PaperworkGod)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.skurl_path = self.pantheon_path / "paperwork_god" / "skurl"
        
        # Ensure directory structure exists
        self.skurl_path.mkdir(parents=True, exist_ok=True)
        (self.skurl_path / "obstacles").mkdir(parents=True, exist_ok=True)
        
        # Registry file
        self.registry_file = self.skurl_path / "red_tape_registry.json"
        
        # Parent god reference
        self.parent_god = parent_god
        
        # Load registry
        self._ensure_registry()
    
    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "obstacles": [],
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "demi_god": "Skurl",
                "type": "gremlin",
                "domain": "red_tape",
                "parent_god": "PaperworkGod"
            }
            self.registry_file.write_text(
                json.dumps(registry, indent=2),
                encoding="utf-8"
            )
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load red tape registry."""
        if not self.registry_file.exists():
            self._ensure_registry()
        
        data = json.loads(self.registry_file.read_text(encoding="utf-8"))
        return data
    
    def _save_registry(self, registry: Dict[str, Any]) -> None:
        """Save red tape registry."""
        registry["last_updated"] = datetime.now().isoformat()
        self.registry_file.write_text(
            json.dumps(registry, indent=2),
            encoding="utf-8"
        )
    
    def create_red_tape_obstacle(
        self,
        obstacle_id: str,
        description: str,
        required_forms: Optional[List[str]] = None,
        required_approvals: Optional[List[str]] = None,
        complexity_level: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RedTapeObstacle:
        """
        Create a new red tape obstacle.
        
        Args:
            obstacle_id: Obstacle identifier
            description: Description of the obstacle
            required_forms: List of required form IDs
            required_approvals: List of required approval steps
            complexity_level: Complexity level (1-10)
            metadata: Additional metadata
            
        Returns:
            Created RedTapeObstacle
        """
        registry = self._load_registry()
        
        # Check if already exists
        for obstacle_data in registry["obstacles"]:
            if obstacle_data["obstacle_id"] == obstacle_id:
                # Update existing obstacle
                obstacle = RedTapeObstacle.from_dict(obstacle_data)
                obstacle.description = description
                obstacle.required_forms = required_forms or []
                obstacle.required_approvals = required_approvals or []
                obstacle.complexity_level = complexity_level
                if metadata:
                    obstacle.metadata.update(metadata)
                
                # Update in registry
                for i, o in enumerate(registry["obstacles"]):
                    if o["obstacle_id"] == obstacle_id:
                        registry["obstacles"][i] = obstacle.to_dict()
                        break
                
                self._save_registry(registry)
                return obstacle
        
        # Create new obstacle
        obstacle = RedTapeObstacle(
            obstacle_id=obstacle_id,
            description=description,
            required_forms=required_forms or [],
            required_approvals=required_approvals or [],
            complexity_level=complexity_level,
            metadata=metadata or {}
        )
        
        registry["obstacles"].append(obstacle.to_dict())
        self._save_registry(registry)
        
        return obstacle
    
    def get_obstacle(self, obstacle_id: str) -> Optional[RedTapeObstacle]:
        """
        Get red tape obstacle by ID.
        
        Args:
            obstacle_id: Obstacle identifier
            
        Returns:
            RedTapeObstacle or None if not found
        """
        registry = self._load_registry()
        
        for obstacle_data in registry["obstacles"]:
            if obstacle_data["obstacle_id"] == obstacle_id:
                return RedTapeObstacle.from_dict(obstacle_data)
        
        return None
    
    def list_all_obstacles(self, unresolved_only: bool = False) -> List[RedTapeObstacle]:
        """
        List all red tape obstacles.
        
        Args:
            unresolved_only: If True, only return unresolved obstacles
            
        Returns:
            List of RedTapeObstacle instances
        """
        registry = self._load_registry()
        
        obstacles = []
        for obstacle_data in registry["obstacles"]:
            obstacle = RedTapeObstacle.from_dict(obstacle_data)
            if not unresolved_only or not obstacle.is_resolved:
                obstacles.append(obstacle)
        
        return obstacles
    
    def resolve_obstacle(self, obstacle_id: str) -> Optional[RedTapeObstacle]:
        """
        Resolve a red tape obstacle.
        
        Args:
            obstacle_id: Obstacle identifier
            
        Returns:
            Resolved RedTapeObstacle or None if not found
        """
        registry = self._load_registry()
        
        for i, obstacle_data in enumerate(registry["obstacles"]):
            if obstacle_data["obstacle_id"] == obstacle_id:
                obstacle = RedTapeObstacle.from_dict(obstacle_data)
                obstacle.resolved_at = datetime.now().isoformat()
                registry["obstacles"][i] = obstacle.to_dict()
                self._save_registry(registry)
                return obstacle
        
        return None
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """
        Get summary of red tape registry.
        
        Returns:
            Dictionary with registry statistics
        """
        obstacles = self.list_all_obstacles()
        unresolved = self.list_all_obstacles(unresolved_only=True)
        
        return {
            "total_obstacles": len(obstacles),
            "unresolved_obstacles": len(unresolved),
            "resolved_obstacles": len(obstacles) - len(unresolved),
            "average_complexity": (
                sum(o.complexity_level for o in obstacles) / len(obstacles)
                if obstacles else 0
            ),
            "demi_god_type": "gremlin",
            "domain": "red_tape",
            "parent_god": "PaperworkGod"
        }
