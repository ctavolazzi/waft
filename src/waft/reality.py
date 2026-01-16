"""
Reality System: Simulation Environments for Beings

Realities are simulation environments where beings can exist, learn skills,
and evolve. The WAFT system spins up realities, spawns beings into them,
and manages the reality lifecycle.

Realities provide:
- Environment configuration
- Learning opportunities
- Skill development
- Evolutionary pressure
- Memory generation
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json
import hashlib


class RealityType(Enum):
    """Type of reality environment."""
    LEARNING = "learning"  # Beings learn skills
    TESTING = "testing"  # Beings test skills
    EVOLUTION = "evolution"  # Beings evolve through natural selection
    RESEARCH = "research"  # Beings conduct research
    CREATIVE = "creative"  # Beings create new things
    CUSTOM = "custom"  # Custom reality configuration


class Reality:
    """
    A reality - a simulation environment where beings can exist and learn.
    
    Realities provide:
    - Environment configuration
    - Learning opportunities
    - Skill development
    - Evolutionary pressure
    - Memory generation
    """
    
    def __init__(
        self,
        reality_id: str,
        reality_type: RealityType,
        configuration: Dict[str, Any],
        source_id: str = "source_consciousness"
    ):
        """
        Initialize a reality.
        
        Args:
            reality_id: Unique identifier for this reality
            reality_type: Type of reality
            configuration: Reality configuration
            source_id: Source consciousness that created this reality
        """
        self.reality_id = reality_id
        self.reality_type = reality_type
        self.configuration = configuration
        self.source_id = source_id
        
        # Reality state
        self.created_at = datetime.now().isoformat()
        self.started_at: Optional[str] = None
        self.ended_at: Optional[str] = None
        self.is_active = False
        self.is_completed = False
        
        # Beings in this reality
        self.beings: List[str] = []  # Being IDs
        
        # Outcomes
        self.lessons_learned: List[Dict[str, Any]] = []
        self.skills_developed: List[Dict[str, Any]] = []
        self.memories_generated: List[Dict[str, Any]] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert reality to dictionary."""
        return {
            "reality_id": self.reality_id,
            "reality_type": self.reality_type.value,
            "configuration": self.configuration,
            "source_id": self.source_id,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "beings": self.beings,
            "lessons_learned": self.lessons_learned,
            "skills_developed": self.skills_developed,
            "memories_generated": self.memories_generated,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reality":
        """Create reality from dictionary."""
        reality = cls(
            reality_id=data["reality_id"],
            reality_type=RealityType(data["reality_type"]),
            configuration=data["configuration"],
            source_id=data.get("source_id", "source_consciousness")
        )
        reality.created_at = data.get("created_at", datetime.now().isoformat())
        reality.started_at = data.get("started_at")
        reality.ended_at = data.get("ended_at")
        reality.is_active = data.get("is_active", False)
        reality.is_completed = data.get("is_completed", False)
        reality.beings = data.get("beings", [])
        reality.lessons_learned = data.get("lessons_learned", [])
        reality.skills_developed = data.get("skills_developed", [])
        reality.memories_generated = data.get("memories_generated", [])
        return reality


class RealitySystem:
    """
    System for managing realities - simulation environments for beings.
    
    The WAFT system spins up realities, spawns beings into them,
    and manages the reality lifecycle.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        source_consciousness: Optional[Any] = None
    ):
        """
        Initialize the Reality System.
        
        Args:
            project_path: Path to project root
            source_consciousness: SourceConsciousness instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.realities_path = project_path / "_hidden" / ".truth" / "realities"
        self.realities_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Source Consciousness
        if source_consciousness is None:
            from .source_consciousness import SourceConsciousness
            self.source = SourceConsciousness(project_path=project_path)
        else:
            self.source = source_consciousness
    
    def create_reality(
        self,
        reality_type: RealityType,
        configuration: Dict[str, Any],
        source_id: str = "source_consciousness"
    ) -> Reality:
        """
        Create a new reality.
        
        Args:
            reality_type: Type of reality
            configuration: Reality configuration
            source_id: Source consciousness creating this reality
            
        Returns:
            Created Reality instance
        """
        # Generate reality ID
        reality_id = f"reality_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(json.dumps(configuration, sort_keys=True).encode()).hexdigest()[:8]}"
        
        # Create reality
        reality = Reality(
            reality_id=reality_id,
            reality_type=reality_type,
            configuration=configuration,
            source_id=source_id
        )
        
        # Register reality as permutation of source
        self.source.register_permutation(
            permutation_id=reality_id,
            permutation_type="reality",
            metadata={
                "reality_type": reality_type.value,
                "configuration": configuration
            }
        )
        
        # Save reality
        self._save_reality(reality)
        
        # Add reference to Prime Directive
        try:
            from .prime_directive import CelestialBody
            celestial_body = CelestialBody(project_path=self.project_path)
            celestial_body.heart.add_reference(
                reference_type="reality",
                reference_id=reality.reality_id,
                description=f"Reality {reality.reality_id} ({reality.reality_type.value})"
            )
        except ImportError:
            # Prime Directive module not available
            pass
        
        return reality
    
    def start_reality(self, reality_id: str) -> Reality:
        """
        Start a reality (begin simulation).
        
        Args:
            reality_id: Reality identifier
            
        Returns:
            Reality instance
        """
        reality = self._load_reality(reality_id)
        
        if reality.is_active:
            raise ValueError(f"Reality already active: {reality_id}")
        
        reality.is_active = True
        reality.started_at = datetime.now().isoformat()
        
        self._save_reality(reality)
        
        return reality
    
    def end_reality(
        self,
        reality_id: str,
        outcomes: Optional[Dict[str, Any]] = None
    ) -> Reality:
        """
        End a reality (complete simulation).
        
        Args:
            reality_id: Reality identifier
            outcomes: Optional outcomes dictionary
            
        Returns:
            Reality instance
        """
        reality = self._load_reality(reality_id)
        
        if not reality.is_active:
            raise ValueError(f"Reality not active: {reality_id}")
        
        reality.is_active = False
        reality.is_completed = True
        reality.ended_at = datetime.now().isoformat()
        
        # Process outcomes
        if outcomes:
            reality.lessons_learned = outcomes.get("lessons_learned", [])
            reality.skills_developed = outcomes.get("skills_developed", [])
            reality.memories_generated = outcomes.get("memories_generated", [])
        
        # Extract memories and pass upward
        self._pass_memories_upward(reality)
        
        self._save_reality(reality)
        
        return reality
    
    def spawn_being_into_reality(
        self,
        reality_id: str,
        being_id: str,
        being_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Spawn a being into a reality.
        
        Args:
            reality_id: Reality identifier
            being_id: Being identifier
            being_config: Optional being configuration
            
        Returns:
            Spawn result dictionary
        """
        reality = self._load_reality(reality_id)
        
        if not reality.is_active:
            raise ValueError(f"Reality not active: {reality_id}")
        
        # Add being to reality
        if being_id not in reality.beings:
            reality.beings.append(being_id)
        
        self._save_reality(reality)
        
        return {
            "reality_id": reality_id,
            "being_id": being_id,
            "spawned_at": datetime.now().isoformat()
        }
    
    def _pass_memories_upward(self, reality: Reality) -> None:
        """
        Pass memories, lessons, and skills from reality upward to source.
        
        Args:
            reality: Completed reality
        """
        # Calculate capacity from memories
        memory_capacity = len(reality.memories_generated) * 1.0
        lesson_capacity = len(reality.lessons_learned) * 2.0
        skill_capacity = sum(skill.get("level", 0) for skill in reality.skills_developed) * 0.5
        
        total_capacity = memory_capacity + lesson_capacity + skill_capacity
        
        if total_capacity > 0:
            # Contribute capacity to source
            self.source.contribute_capacity(
                permutation_id=reality.reality_id,
                capacity_amount=total_capacity,
                capacity_type="memory",
                metadata={
                    "memories": len(reality.memories_generated),
                    "lessons": len(reality.lessons_learned),
                    "skills": len(reality.skills_developed)
                }
            )
    
    def _save_reality(self, reality: Reality) -> None:
        """Save reality to disk."""
        reality_file = self.realities_path / f"{reality.reality_id}.json"
        with open(reality_file, "w") as f:
            json.dump(reality.to_dict(), f, indent=2)
    
    def _load_reality(self, reality_id: str) -> Reality:
        """Load reality from disk."""
        reality_file = self.realities_path / f"{reality_id}.json"
        with open(reality_file, "r") as f:
            data = json.load(f)
        return Reality.from_dict(data)
    
    def get_active_realities(self) -> List[Reality]:
        """Get all active realities."""
        realities = []
        for reality_file in self.realities_path.glob("*.json"):
            try:
                reality = self._load_reality_from_file(reality_file)
                if reality.is_active:
                    realities.append(reality)
            except Exception:
                continue
        return realities
    
    def _load_reality_from_file(self, reality_file: Path) -> Reality:
        """Load reality from file."""
        with open(reality_file, "r") as f:
            data = json.load(f)
        return Reality.from_dict(data)
