"""
Skills System: Learned Abilities

Skills are what beings can learn and evolve. Skills have levels (0-100),
can evolve through use, can mutate/improve, and can be passed to offspring.

Skills contribute to fitness and are part of the memory/lesson passing system.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json


class SkillType(Enum):
    """Type of skill."""
    COGNITIVE = "cognitive"  # Thinking, reasoning, analysis
    CREATIVE = "creative"  # Creation, expression, innovation
    SOCIAL = "social"  # Communication, collaboration
    TECHNICAL = "technical"  # Code, tools, systems
    META = "meta"  # Learning how to learn


class Skill:
    """
    A skill - a learned ability that beings can develop.
    
    Skills have:
    - Name and type
    - Level (0-100)
    - Evolution history
    - Fitness contribution
    """
    
    def __init__(
        self,
        skill_name: str,
        skill_type: SkillType,
        level: float = 0.0,
        parent_skill: Optional["Skill"] = None
    ):
        """
        Initialize a skill.
        
        Args:
            skill_name: Name of skill
            skill_type: Type of skill
            level: Current level (0-100)
            parent_skill: Optional parent skill (for inheritance)
        """
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.level = max(0.0, min(100.0, level))
        self.parent_skill = parent_skill
        
        # Evolution tracking
        self.created_at = datetime.now().isoformat()
        self.evolution_history: List[Dict[str, Any]] = []
        
        # Fitness contribution
        self.fitness_contribution: float = 0.0
    
    def improve(self, amount: float = 1.0) -> Dict[str, Any]:
        """
        Improve skill level.
        
        Args:
            amount: Amount to improve
            
        Returns:
            Improvement record
        """
        old_level = self.level
        self.level = max(0.0, min(100.0, self.level + amount))
        
        improvement = {
            "old_level": old_level,
            "new_level": self.level,
            "improved_at": datetime.now().isoformat()
        }
        
        self.evolution_history.append(improvement)
        return improvement
    
    def mutate(self, mutation_factor: float = 0.1) -> Dict[str, Any]:
        """
        Mutate skill (random change).
        
        Args:
            mutation_factor: Mutation strength
            
        Returns:
            Mutation record
        """
        import random
        mutation = (random.random() - 0.5) * mutation_factor * 100.0
        old_level = self.level
        self.level = max(0.0, min(100.0, self.level + mutation))
        
        mutation_record = {
            "old_level": old_level,
            "new_level": self.level,
            "mutation": mutation,
            "mutated_at": datetime.now().isoformat()
        }
        
        self.evolution_history.append(mutation_record)
        return mutation_record
    
    def calculate_fitness_contribution(self) -> float:
        """
        Calculate how much this skill contributes to fitness.
        
        Returns:
            Fitness contribution (0.0-1.0)
        """
        # Higher level = higher contribution
        # Different skill types have different weights
        base_contribution = self.level / 100.0
        
        type_weights = {
            SkillType.COGNITIVE: 1.2,
            SkillType.CREATIVE: 1.1,
            SkillType.SOCIAL: 0.9,
            SkillType.TECHNICAL: 1.0,
            SkillType.META: 1.5  # Meta-learning is highly valuable
        }
        
        weight = type_weights.get(self.skill_type, 1.0)
        self.fitness_contribution = min(1.0, base_contribution * weight)
        
        return self.fitness_contribution
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary."""
        return {
            "skill_name": self.skill_name,
            "skill_type": self.skill_type.value,
            "level": self.level,
            "fitness_contribution": self.fitness_contribution,
            "created_at": self.created_at,
            "evolution_history": self.evolution_history,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create skill from dictionary."""
        skill = cls(
            skill_name=data["skill_name"],
            skill_type=SkillType(data["skill_type"]),
            level=data.get("level", 0.0)
        )
        skill.fitness_contribution = data.get("fitness_contribution", 0.0)
        skill.created_at = data.get("created_at", datetime.now().isoformat())
        skill.evolution_history = data.get("evolution_history", [])
        return skill


class SkillSystem:
    """
    System for managing skills - learned abilities.
    
    Skills can:
    - Be learned by beings
    - Evolve through use
    - Mutate/improve
    - Be inherited by offspring
    - Contribute to fitness
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the Skill System.
        
        Args:
            project_path: Path to project root
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.skills_path = project_path / "_hidden" / ".truth" / "skills"
        self.skills_path.mkdir(parents=True, exist_ok=True)
    
    def create_skill(
        self,
        skill_name: str,
        skill_type: SkillType,
        initial_level: float = 0.0
    ) -> Skill:
        """
        Create a new skill.
        
        Args:
            skill_name: Name of skill
            skill_type: Type of skill
            initial_level: Initial level
            
        Returns:
            Created Skill instance
        """
        skill = Skill(
            skill_name=skill_name,
            skill_type=skill_type,
            level=initial_level
        )
        
        self._save_skill(skill)
        return skill
    
    def inherit_skill(
        self,
        parent_skill: Skill,
        mutation_factor: float = 0.05
    ) -> Skill:
        """
        Inherit a skill from parent (with mutation).
        
        Args:
            parent_skill: Parent skill
            mutation_factor: Mutation strength
            
        Returns:
            Inherited Skill instance
        """
        # Create new skill with inherited level
        skill = Skill(
            skill_name=parent_skill.skill_name,
            skill_type=parent_skill.skill_type,
            level=parent_skill.level,
            parent_skill=parent_skill
        )
        
        # Apply mutation
        skill.mutate(mutation_factor)
        
        self._save_skill(skill)
        return skill
    
    def _save_skill(self, skill: Skill) -> None:
        """Save skill to disk."""
        skill_file = self.skills_path / f"{skill.skill_name}_{skill.skill_type.value}.json"
        with open(skill_file, "w") as f:
            json.dump(skill.to_dict(), f, indent=2)
    
    def _load_skill(self, skill_name: str, skill_type: SkillType) -> Optional[Skill]:
        """Load skill from disk."""
        skill_file = self.skills_path / f"{skill_name}_{skill_type.value}.json"
        if skill_file.exists():
            with open(skill_file, "r") as f:
                data = json.load(f)
            return Skill.from_dict(data)
        return None
