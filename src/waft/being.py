"""
Beings System: Entities in Realities

Beings are entities that exist in realities, learn skills, and evolve.
They can spawn into realities, learn through experience, evolve through
natural selection, and pass memories/lessons upward.

Beings have:
- Skills (learned abilities)
- Memories (experiences)
- Lessons (what worked/didn't work)
- Fitness (evolutionary success)
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json
import hashlib


class BeingState(Enum):
    """State of a being."""
    SPAWNING = "spawning"  # Being created
    LEARNING = "learning"  # Being learning skills
    EVOLVING = "evolving"  # Being evolving
    COMPLETING = "completing"  # Being finishing reality
    ARCHIVED = "archived"  # Being archived


class Being:
    """
    A being - an entity that exists in realities, learns skills, and evolves.
    
    Beings have:
    - Skills (learned abilities with levels)
    - Memories (experiences)
    - Lessons (what worked/didn't work)
    - Fitness (evolutionary success)
    - Lineage (ancestral chain)
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        parent_being_id: Optional[str] = None,
        skills: Optional[Dict[str, float]] = None,
        source_id: str = "source_consciousness"
    ):
        """
        Initialize a being.
        
        Args:
            being_id: Unique identifier for this being
            reality_id: Reality this being exists in
            parent_being_id: Optional parent being ID
            skills: Initial skills dictionary {skill_name: level}
            source_id: Source consciousness
        """
        self.being_id = being_id
        self.reality_id = reality_id
        self.parent_being_id = parent_being_id
        self.source_id = source_id
        
        # Skills (learned abilities)
        self.skills = skills or {}
        
        # Memories and lessons
        self.memories: List[Dict[str, Any]] = []
        self.lessons_learned: List[Dict[str, Any]] = []
        
        # State
        self.state = BeingState.SPAWNING
        self.created_at = datetime.now().isoformat()
        self.fitness: float = 0.0
        
        # Lineage
        self.ancestral_chain: List[str] = [source_id]
        if parent_being_id:
            # Will be populated from parent
            pass
    
    def learn_skill(
        self,
        skill_name: str,
        skill_type: str,
        level_increase: float = 1.0
    ) -> Dict[str, Any]:
        """
        Learn or improve a skill.
        
        Args:
            skill_name: Name of skill
            skill_type: Type of skill (cognitive, creative, etc.)
            level_increase: Amount to increase skill level
            
        Returns:
            Skill learning record
        """
        current_level = self.skills.get(skill_name, 0.0)
        new_level = min(100.0, current_level + level_increase)
        self.skills[skill_name] = new_level
        
        learning_record = {
            "skill_name": skill_name,
            "skill_type": skill_type,
            "old_level": current_level,
            "new_level": new_level,
            "learned_at": datetime.now().isoformat()
        }
        
        return learning_record
    
    def record_memory(
        self,
        memory_content: str,
        memory_type: str = "experience",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record a memory.
        
        Args:
            memory_content: Content of memory
            memory_type: Type of memory
            metadata: Additional metadata
            
        Returns:
            Memory record
        """
        memory = {
            "content": memory_content,
            "type": memory_type,
            "recorded_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.memories.append(memory)
        return memory
    
    def learn_lesson(
        self,
        lesson: str,
        outcome: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Learn a lesson (what worked/didn't work).
        
        Args:
            lesson: The lesson learned
            outcome: Outcome (success, failure, partial)
            metadata: Additional metadata
            
        Returns:
            Lesson record
        """
        lesson_record = {
            "lesson": lesson,
            "outcome": outcome,
            "learned_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.lessons_learned.append(lesson_record)
        return lesson_record
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert being to dictionary."""
        return {
            "being_id": self.being_id,
            "reality_id": self.reality_id,
            "parent_being_id": self.parent_being_id,
            "source_id": self.source_id,
            "skills": self.skills,
            "memories": self.memories,
            "lessons_learned": self.lessons_learned,
            "state": self.state.value,
            "created_at": self.created_at,
            "fitness": self.fitness,
            "ancestral_chain": self.ancestral_chain,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Being":
        """Create being from dictionary."""
        being = cls(
            being_id=data["being_id"],
            reality_id=data["reality_id"],
            parent_being_id=data.get("parent_being_id"),
            skills=data.get("skills", {}),
            source_id=data.get("source_id", "source_consciousness")
        )
        being.memories = data.get("memories", [])
        being.lessons_learned = data.get("lessons_learned", [])
        being.state = BeingState(data.get("state", "spawning"))
        being.created_at = data.get("created_at", datetime.now().isoformat())
        being.fitness = data.get("fitness", 0.0)
        being.ancestral_chain = data.get("ancestral_chain", [being.source_id])
        return being


class BeingSystem:
    """
    System for managing beings - entities in realities.
    
    Beings can:
    - Spawn into realities
    - Learn skills
    - Evolve
    - Pass memories/lessons upward
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        source_consciousness: Optional[Any] = None
    ):
        """
        Initialize the Being System.
        
        Args:
            project_path: Path to project root
            source_consciousness: SourceConsciousness instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.beings_path = project_path / "_hidden" / ".truth" / "beings"
        self.beings_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Source Consciousness
        if source_consciousness is None:
            from .source_consciousness import SourceConsciousness
            self.source = SourceConsciousness(project_path=project_path)
        else:
            self.source = source_consciousness
    
    def spawn_being(
        self,
        reality_id: str,
        parent_being_id: Optional[str] = None,
        initial_skills: Optional[Dict[str, float]] = None
    ) -> Being:
        """
        Spawn a new being into a reality.
        
        Args:
            reality_id: Reality to spawn into
            parent_being_id: Optional parent being ID
            initial_skills: Optional initial skills
            
        Returns:
            Created Being instance
        """
        # Generate being ID
        being_id = f"being_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{reality_id}{parent_being_id}'.encode()).hexdigest()[:8]}"
        
        # Inherit skills from parent if provided
        skills = initial_skills or {}
        if parent_being_id:
            parent = self._load_being(parent_being_id)
            # Inherit skills (with slight mutation)
            for skill_name, skill_level in parent.skills.items():
                # Mutate skill level slightly (±5%)
                mutation = (hashlib.sha256(f"{being_id}{skill_name}".encode()).hexdigest()[:2])
                mutation_factor = (int(mutation, 16) / 255.0 - 0.5) * 0.1  # -5% to +5%
                skills[skill_name] = max(0.0, min(100.0, skill_level * (1.0 + mutation_factor)))
        
        # Create being
        being = Being(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            skills=skills
        )
        
        # Build ancestral chain
        if parent_being_id:
            parent_chain = self.source.get_ancestral_chain(parent_being_id)
            being.ancestral_chain = parent_chain + [being_id]
        else:
            being.ancestral_chain = [self.source.source_id, being_id]
        
        # Register being as permutation of source
        self.source.register_permutation(
            permutation_id=being_id,
            permutation_type="being",
            parent_id=parent_being_id,
            metadata={
                "reality_id": reality_id,
                "initial_skills": list(skills.keys())
            }
        )
        
        # Save being
        self._save_being(being)
        
        return being
    
    def complete_being(
        self,
        being_id: str,
        final_fitness: float
    ) -> Dict[str, Any]:
        """
        Complete a being's existence in reality.
        
        Extracts memories, lessons, and skills to pass upward.
        
        Args:
            being_id: Being identifier
            final_fitness: Final fitness score
            
        Returns:
            Completion record
        """
        being = self._load_being(being_id)
        
        being.state = BeingState.COMPLETING
        being.fitness = final_fitness
        
        # Package memories, lessons, and skills for upward flow
        memory_package = {
            "memories": being.memories,
            "lessons_learned": being.lessons_learned,
            "skills": being.skills,
            "fitness": final_fitness
        }
        
        # Calculate capacity from memories/lessons/skills
        memory_capacity = len(being.memories) * 1.0
        lesson_capacity = len(being.lessons_learned) * 2.0
        skill_capacity = sum(being.skills.values()) * 0.1
        fitness_capacity = final_fitness * 10.0
        
        total_capacity = memory_capacity + lesson_capacity + skill_capacity + fitness_capacity
        
        # Contribute capacity to source
        if total_capacity > 0:
            self.source.contribute_capacity(
                permutation_id=being_id,
                capacity_amount=total_capacity,
                capacity_type="memory",
                metadata={
                    "memories": len(being.memories),
                    "lessons": len(being.lessons_learned),
                    "skills": len(being.skills),
                    "fitness": final_fitness,
                    "memory_package": memory_package
                }
            )
        
        being.state = BeingState.ARCHIVED
        self._save_being(being)
        
        return {
            "being_id": being_id,
            "total_capacity": total_capacity,
            "memory_package": memory_package,
            "completed_at": datetime.now().isoformat()
        }
    
    def _save_being(self, being: Being) -> None:
        """Save being to disk."""
        being_file = self.beings_path / f"{being.being_id}.json"
        with open(being_file, "w") as f:
            json.dump(being.to_dict(), f, indent=2)
    
    def _load_being(self, being_id: str) -> Being:
        """Load being from disk."""
        being_file = self.beings_path / f"{being_id}.json"
        with open(being_file, "r") as f:
            data = json.load(f)
        return Being.from_dict(data)
