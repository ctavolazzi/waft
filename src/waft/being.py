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
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from enum import Enum
import json
import hashlib
import random
import os


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
    - Lifecycle attributes (will_to_live, luck, decision_fatigue, pleasure, pain)
    - Personality and goals
    - Sleep state
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        parent_being_id: Optional[str] = None,
        skills: Optional[Dict[str, float]] = None,
        source_id: str = "source_consciousness",
        # New lifecycle attributes
        will_to_live: Optional[float] = None,
        luck: Optional[float] = None,
        decision_fatigue: Optional[int] = None,
        decision_quota_max: Optional[int] = None,
        pleasure: Optional[float] = None,
        pain: Optional[float] = None,
        # Personality and goals
        personality: Optional[Dict[str, Any]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        personality_type: Optional[str] = None,
        # Karma connection
        soul_id: Optional[str] = None,
        # Sleep state
        is_sleeping: Optional[bool] = None,
        sleep_duration: Optional[int] = None,
        sleep_duration_base: Optional[int] = None,
        cycles_slept: Optional[int] = None,
        # Cycle tracking
        last_cycle_number: Optional[int] = None,
        lifetimes: Optional[int] = None,
        # Experience tracking
        recent_experiences: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize a being.
        
        Args:
            being_id: Unique identifier for this being
            reality_id: Reality this being exists in
            parent_being_id: Optional parent being ID
            skills: Initial skills dictionary {skill_name: level}
            source_id: Source consciousness
            will_to_live: Initial will to live (default: 100.0)
            luck: Initial luck (default: 50.0)
            decision_fatigue: Initial decision fatigue (default: calculated from personality/skills)
            decision_quota_max: Max decisions before sleep (default: calculated)
            pleasure: Initial pleasure (default: 0.0)
            pain: Initial pain (default: 0.0)
            personality: Personality traits dict (default: {})
            goals: Lifetime goals list (default: [])
            personality_type: Personality type (default: "balanced")
            soul_id: Link to karma system (default: None, will be created)
            is_sleeping: Whether being is sleeping (default: False)
            sleep_duration: Cycles to sleep (default: 0)
            sleep_duration_base: Base sleep duration (default: random 3-10)
            cycles_slept: Current sleep counter (default: 0)
            last_cycle_number: Last cycle number (default: 0)
            lifetimes: Number of reincarnations (default: 0)
            recent_experiences: Recent experiences (default: [])
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
        
        # Lifecycle attributes
        self.will_to_live: float = will_to_live if will_to_live is not None else 100.0
        self.luck: float = luck if luck is not None else 50.0
        self.pleasure: float = pleasure if pleasure is not None else 0.0
        self.pain: float = pain if pain is not None else 0.0
        
        # Personality and goals (NEW - Being doesn't have AgentState)
        # Set these BEFORE calculating willpower/stamina which depend on them
        self.personality: Dict[str, Any] = personality if personality is not None else {}
        self.goals: List[Dict[str, Any]] = goals if goals is not None else []
        self.personality_type: str = personality_type if personality_type is not None else "balanced"
        
        # Cycle tracking (needed for stamina calculation)
        self.last_cycle_number: int = last_cycle_number if last_cycle_number is not None else 0
        # lifetimes: Number of reincarnations
        # If explicitly provided, use it
        # If None and no parent: this is a new birth (lifetime 1)
        # If None and has parent: will be set by spawn_being() (parent + 1)
        # If loading from storage: will be set by from_dict()
        if lifetimes is not None:
            self.lifetimes = lifetimes
        elif parent_being_id is None:
            # Direct instantiation without parent = new birth (lifetime 1)
            self.lifetimes = 1
        else:
            # Has parent but lifetimes not set - will be set by spawn_being()
            # Default to 0 for now (spawn_being will increment from parent)
            self.lifetimes = 0
        
        # Stamina system (NEW)
        # Willpower: Core stat derived from personality and will_to_live
        self.willpower: float = self._calculate_willpower()
        # Stamina: Calculated from all stats, especially willpower
        self.stamina: float = self._calculate_stamina()
        self.stamina_max: float = self.stamina  # Maximum stamina (recalculated each cycle)
        self.stamina_regeneration_rate: float = 5.0  # Stamina regenerated per cycle
        
        # Karma connection (NEW)
        self.soul_id: Optional[str] = soul_id
        
        # Calculate initial decision quota based on personality and skills
        if decision_quota_max is None:
            base_quota = 10
            personality_modifier = self._calculate_personality_modifier()
            skill_bonus = min(5, sum(self.skills.values()) / 100.0)
            decision_quota_max = int(base_quota + personality_modifier + skill_bonus)
        
        self.decision_quota_max: int = decision_quota_max
        self.decision_fatigue: int = decision_fatigue if decision_fatigue is not None else self.decision_quota_max
        
        # Sleep state
        self.is_sleeping: bool = is_sleeping if is_sleeping is not None else False
        if sleep_duration_base is None:
            # Random base duration (3-10 cycles)
            sleep_duration_base = random.randint(3, 10)
        self.sleep_duration_base: int = sleep_duration_base
        self.sleep_duration: int = sleep_duration if sleep_duration is not None else 0
        self.cycles_slept: int = cycles_slept if cycles_slept is not None else 0
        
        # Experience tracking (for pleasure/pain calculation)
        self.recent_experiences: List[Dict[str, Any]] = recent_experiences if recent_experiences is not None else []
    
    def _calculate_personality_modifier(self) -> float:
        """Calculate decision quota modifier based on personality type."""
        modifiers = {
            "analytical": 5.0,
            "systematic": 5.0,
            "creative": -2.0,
            "intuitive": -2.0,
            "balanced": 0.0
        }
        return modifiers.get(self.personality_type, 0.0)
    
    def _calculate_willpower(self) -> float:
        """
        Calculate willpower from personality and will_to_live.
        
        Willpower is the core stat that heavily influences stamina.
        Formula: (will_to_live / 100.0) * personality_willpower_modifier
        
        Returns:
            Willpower value (0.0-100.0)
        """
        # Base willpower from will_to_live
        base_willpower = (self.will_to_live / 100.0) * 50.0
        
        # Personality modifiers for willpower
        personality_willpower = {
            "analytical": 1.2,  # High willpower
            "systematic": 1.3,  # Very high willpower
            "creative": 0.9,    # Lower willpower (more impulsive)
            "intuitive": 0.9,   # Lower willpower
            "balanced": 1.0     # Base willpower
        }
        modifier = personality_willpower.get(self.personality_type, 1.0)
        
        # Add skill bonus (skills contribute to willpower)
        skill_bonus = min(20.0, sum(self.skills.values()) / 10.0)
        
        willpower = (base_willpower * modifier) + skill_bonus
        return max(0.0, min(100.0, willpower))
    
    def _calculate_stamina(self) -> float:
        """
        Calculate stamina from all being stats, heavily weighted by willpower.
        
        Stamina is the product of crunching numbers on all stats:
        - Willpower (heaviest weight: 40%)
        - Will to live (20%)
        - Skills total (15%)
        - Luck (10%)
        - Cycles alive (experience bonus: 5%)
        - Pleasure (positive energy: 5%)
        - Pain (negative energy: -5%)
        
        Returns:
            Stamina value (0.0-100.0)
        """
        # Recalculate willpower first (it may have changed)
        self.willpower = self._calculate_willpower()
        
        # Weighted components
        willpower_component = self.willpower * 0.40  # 40% weight
        will_to_live_component = (self.will_to_live / 100.0) * 100.0 * 0.20  # 20% weight
        skills_component = min(100.0, sum(self.skills.values()) / len(self.skills) if self.skills else 0.0) * 0.15  # 15% weight
        luck_component = self.luck * 0.10  # 10% weight
        experience_component = min(100.0, self.lifetimes * 0.5) * 0.05  # 5% weight (experience bonus from reincarnations)
        pleasure_component = self.pleasure * 100.0 * 0.05  # 5% weight (positive energy)
        pain_component = -self.pain * 100.0 * 0.05  # -5% weight (negative energy)
        
        # Sum all components
        stamina = (
            willpower_component +
            will_to_live_component +
            skills_component +
            luck_component +
            experience_component +
            pleasure_component +
            pain_component
        )
        
        # Clamp to 0.0-100.0
        stamina = max(0.0, min(100.0, stamina))
        
        # Update stamina_max
        self.stamina_max = stamina
        
        return stamina
    
    def consume_stamina(self, amount: float) -> float:
        """
        Consume stamina for an action.
        
        Args:
            amount: Stamina to consume
        
        Returns:
            Actual stamina consumed (may be less if depleted)
        """
        actual_consumption = min(amount, self.stamina)
        self.stamina = max(0.0, self.stamina - actual_consumption)
        return actual_consumption
    
    def is_stamina_depleted(self) -> bool:
        """
        Check if stamina is depleted (below 10% threshold).
        
        Returns:
            True if stamina is critically low
        """
        return self.stamina < (self.stamina_max * 0.1)
    
    def get_stamina_ratio(self) -> float:
        """
        Get stamina as a ratio of max (0.0-1.0).
        
        Returns:
            Stamina ratio
        """
        if self.stamina_max == 0:
            return 0.0
        return self.stamina / self.stamina_max
    
    def regenerate_stamina(self, amount: Optional[float] = None) -> float:
        """
        Regenerate stamina (called each cycle).
        
        Args:
            amount: Amount to regenerate (defaults to stamina_regeneration_rate)
        
        Returns:
            Actual stamina regenerated
        """
        if amount is None:
            amount = self.stamina_regeneration_rate
        
        # Regeneration is faster when will_to_live is high
        will_to_live_modifier = self.will_to_live / 100.0
        effective_regeneration = amount * (0.5 + will_to_live_modifier * 0.5)
        
        old_stamina = self.stamina
        self.stamina = min(self.stamina_max, self.stamina + effective_regeneration)
        
        return self.stamina - old_stamina
    
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
    
    def calculate_will_to_live_change(
        self,
        cycle_data: Dict[str, Any]
    ) -> float:
        """
        Calculate change to will_to_live based on cycle data.
        
        Depletion factors:
        - Time-based: -0.1 per cycle
        - Decision-based: -0.5 per decision made
        - Pain-based: -pain_value × 10.0
        
        Regeneration factors:
        - Pleasure-based: +pleasure_value × 5.0 (capped at 100.0)
        
        Args:
            cycle_data: Dictionary with:
                - decisions_made: Number of decisions made this cycle
                - pain: Current pain value
                - pleasure: Current pleasure value
        
        Returns:
            Change to will_to_live (can be negative or positive)
        """
        change = 0.0
        
        # Time-based depletion (per cycle)
        change -= 0.1
        
        # Decision-based depletion
        decisions_made = cycle_data.get("decisions_made", 0)
        change -= decisions_made * 0.5
        
        # Pain-based depletion
        pain_value = cycle_data.get("pain", self.pain)
        change -= pain_value * 10.0
        
        # Pleasure-based regeneration
        pleasure_value = cycle_data.get("pleasure", self.pleasure)
        change += pleasure_value * 5.0
        
        return change
    
    def calculate_luck(self, karma_balance: float) -> float:
        """
        Calculate luck based on karma balance.
        
        Formula:
        - Base luck: 50.0
        - Karma modifier: (karma_balance / 1000.0) × 20.0 (max +20.0)
        - Random variance: -10.0 to +10.0
        - Clamped to 0.0-100.0
        
        Args:
            karma_balance: Current karma balance
        
        Returns:
            Luck value (0.0-100.0)
        """
        base_luck = 50.0
        karma_modifier = min(20.0, (karma_balance / 1000.0) * 20.0)
        random_variance = random.uniform(-10.0, 10.0)
        
        luck = base_luck + karma_modifier + random_variance
        return max(0.0, min(100.0, luck))
    
    def calculate_pleasure_pain(
        self,
        personality: Optional[Dict[str, Any]] = None,
        goals: Optional[List[Dict[str, Any]]] = None,
        experience: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, float]:
        """
        Calculate pleasure and pain based on personality-goal-experience alignment.
        
        Uses PersonalityAlignment class for calculation.
        
        Args:
            personality: Personality traits dict (defaults to self.personality)
            goals: Lifetime goals list (defaults to self.goals)
            experience: Experience dict from current cycle (defaults to recent_experiences)
        
        Returns:
            (pleasure, pain) tuple (0.0-1.0 each)
        """
        from .core.personality_alignment import PersonalityAlignment
        
        # Use defaults if not provided
        if personality is None:
            personality = self.personality
        if goals is None:
            goals = self.goals
        if experience is None:
            # Use most recent experience if available
            if self.recent_experiences:
                experience = self.recent_experiences[-1]
            else:
                # No experience - return neutral
                return (0.0, 0.0)
        
        alignment = PersonalityAlignment()
        return alignment.calculate_alignment(personality, goals, experience)
    
    def check_death(self) -> bool:
        """
        Check if being should die (will_to_live <= 0.0).
        
        Returns:
            True if being should die, False otherwise
        """
        return self.will_to_live <= 0.0
    
    def enter_sleep(self) -> None:
        """Enter sleep state (being must sleep when decision_fatigue reaches 0)."""
        self.is_sleeping = True
        self.sleep_duration = self.sleep_duration_base
        self.cycles_slept = 0
    
    def process_sleep(self) -> bool:
        """
        Process sleep state - decrement sleep counter.
        
        Also evolves sleep duration based on being's needs.
        
        Returns:
            True if being is now awake, False if still sleeping
        """
        if not self.is_sleeping:
            return True
        
        self.cycles_slept += 1
        
        if self.cycles_slept >= self.sleep_duration:
            # Awake - reset decision quota
            self.is_sleeping = False
            self.decision_fatigue = self.decision_quota_max
            self.cycles_slept = 0
            
            # Evolve sleep duration based on being's needs
            self._evolve_sleep_duration()
            
            return True
        
        return False
    
    def _evolve_sleep_duration(self) -> None:
        """
        Evolve sleep duration based on being's needs.
        
        Adaptation algorithm:
        - If being frequently exhausted (uses full quota often) → increase duration
        - If being rarely uses full quota → decrease duration
        - Tracks exhaustion history over last 10 cycles
        """
        # Simple evolution: track if being entered sleep with 0 fatigue
        # (indicates exhaustion)
        
        # For now, use a simple adaptation:
        # - If being slept because fatigue reached 0, increase duration slightly
        # - If being rarely uses full quota, decrease duration slightly
        
        # Track exhaustion (being entered sleep with 0 fatigue)
        # This would require tracking history, so for now use simple heuristic:
        # If decision_quota_max is frequently exhausted, increase sleep duration
        
        # Simple evolution: adjust based on current quota usage
        # If quota is consistently exhausted, increase sleep duration
        # If quota is rarely used, decrease sleep duration
        
        # For initial implementation, use simple random walk with bounds
        # In future, can track exhaustion history
        
        # Evolve sleep_duration_base (bounded between 3-15 cycles)
        if self.decision_fatigue == 0 and self.is_sleeping:
            # Being was exhausted - increase sleep duration slightly
            self.sleep_duration_base = min(15, self.sleep_duration_base + 1)
        elif self.decision_fatigue > self.decision_quota_max * 0.5:
            # Being rarely uses full quota - decrease sleep duration slightly
            self.sleep_duration_base = max(3, self.sleep_duration_base - 1)
        
        # Update sleep_duration for next sleep
        self.sleep_duration = self.sleep_duration_base
    
    def make_decision(self, decision_type: str, stamina_cost: float = 5.0) -> Dict[str, Any]:
        """
        Make a decision (decrements fatigue, consumes stamina, returns experience).
        
        When stamina is depleted, actions become sluggish, shitty, and make mistakes.
        
        Args:
            decision_type: Type of decision (learn_skill, record_memory, pursue_goal, rest, explore)
            stamina_cost: Stamina cost for this action (default: 5.0)
        
        Returns:
            Decision result with experience data, including mistakes if stamina depleted
        """
        if self.is_sleeping:
            raise ValueError("Being is sleeping and cannot make decisions")
        
        if self.decision_fatigue <= 0:
            # Must sleep - enter sleep state
            self.enter_sleep()
            raise ValueError("Decision fatigue depleted - being must sleep")
        
        # Decrement fatigue
        self.decision_fatigue -= 1
        
        # Consume stamina
        actual_stamina_consumed = self.consume_stamina(stamina_cost)
        stamina_depleted = self.is_stamina_depleted()
        stamina_ratio = self.get_stamina_ratio()
        
        # Generate experience based on decision type
        experience = {
            "type": "neutral",
            "intensity": 0.5,
            "decision_type": decision_type,
            "timestamp": datetime.now().isoformat(),
            "stamina_consumed": actual_stamina_consumed,
            "stamina_remaining": self.stamina,
            "stamina_ratio": stamina_ratio
        }
        
        # Apply depleted stamina effects (mistakes, randomness, sluggishness)
        if stamina_depleted:
            experience["stamina_depleted"] = True
            experience["mistakes"] = self._generate_stamina_mistakes()
            experience["quality"] = "poor"  # Sluggish and shitty
            experience["intensity"] *= 0.5  # Reduced intensity due to exhaustion
        else:
            experience["stamina_depleted"] = False
            experience["mistakes"] = []
            # Quality scales with stamina ratio
            if stamina_ratio > 0.7:
                experience["quality"] = "excellent"
            elif stamina_ratio > 0.4:
                experience["quality"] = "good"
            else:
                experience["quality"] = "fair"
        
        # Record experience for next cycle's pleasure/pain calculation
        self.recent_experiences.append(experience)
        
        # Keep recent_experiences bounded (last 10)
        if len(self.recent_experiences) > 10:
            self.recent_experiences.pop(0)
        
        return {
            "decision_type": decision_type,
            "experience": experience,
            "decision_fatigue_remaining": self.decision_fatigue,
            "stamina_remaining": self.stamina,
            "stamina_depleted": stamina_depleted
        }
    
    def _generate_stamina_mistakes(self) -> List[str]:
        """
        Generate random mistakes when stamina is depleted.
        
        Returns:
            List of mistake descriptions
        """
        mistakes = [
            "forgot important detail",
            "made calculation error",
            "misinterpreted information",
            "lost focus mid-action",
            "took wrong approach",
            "overlooked critical step",
            "made hasty decision",
            "missed obvious solution",
            "confused priorities",
            "executed action poorly"
        ]
        
        # Random number of mistakes (1-3 when severely depleted)
        num_mistakes = random.randint(1, 3) if self.get_stamina_ratio() < 0.05 else random.randint(0, 1)
        return random.sample(mistakes, min(num_mistakes, len(mistakes)))
    
    def record_experience(self, experience: Dict[str, Any]) -> None:
        """
        Record an experience for pleasure/pain calculation.
        
        Args:
            experience: Experience dict with type, intensity, etc.
        """
        experience["timestamp"] = datetime.now().isoformat()
        self.recent_experiences.append(experience)
        
        # Keep recent_experiences bounded (last 10)
        if len(self.recent_experiences) > 10:
            self.recent_experiences.pop(0)
    
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
            # Lifecycle attributes
            "will_to_live": self.will_to_live,
            "luck": self.luck,
            "decision_fatigue": self.decision_fatigue,
            "decision_quota_max": self.decision_quota_max,
            "pleasure": self.pleasure,
            "pain": self.pain,
            # Stamina system
            "willpower": self.willpower,
            "stamina": self.stamina,
            "stamina_max": self.stamina_max,
            "stamina_regeneration_rate": self.stamina_regeneration_rate,
            # Personality and goals
            "personality": self.personality,
            "goals": self.goals,
            "personality_type": self.personality_type,
            # Karma connection
            "soul_id": self.soul_id,
            # Sleep state
            "is_sleeping": self.is_sleeping,
            "sleep_duration": self.sleep_duration,
            "sleep_duration_base": self.sleep_duration_base,
            "cycles_slept": self.cycles_slept,
            # Cycle tracking
            "last_cycle_number": self.last_cycle_number,
            "lifetimes": self.lifetimes,
            # Experience tracking
            "recent_experiences": self.recent_experiences,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Being":
        """Create being from dictionary (with backward compatibility for missing attributes)."""
        being = cls(
            being_id=data["being_id"],
            reality_id=data["reality_id"],
            parent_being_id=data.get("parent_being_id"),
            skills=data.get("skills", {}),
            source_id=data.get("source_id", "source_consciousness"),
            # Lifecycle attributes (with defaults for backward compatibility)
            will_to_live=data.get("will_to_live"),
            luck=data.get("luck"),
            decision_fatigue=data.get("decision_fatigue"),
            decision_quota_max=data.get("decision_quota_max"),
            pleasure=data.get("pleasure"),
            pain=data.get("pain"),
            # Stamina system (will be calculated if not present)
            # Personality and goals
            personality=data.get("personality"),
            goals=data.get("goals"),
            personality_type=data.get("personality_type"),
            # Karma connection
            soul_id=data.get("soul_id"),
            # Sleep state
            is_sleeping=data.get("is_sleeping"),
            sleep_duration=data.get("sleep_duration"),
            sleep_duration_base=data.get("sleep_duration_base"),
            cycles_slept=data.get("cycles_slept"),
            # Cycle tracking
            last_cycle_number=data.get("last_cycle_number"),
            lifetimes=data.get("lifetimes", data.get("cycles_alive", 0)),  # Support old name for migration
            # Experience tracking
            recent_experiences=data.get("recent_experiences")
        )
        being.memories = data.get("memories", [])
        being.lessons_learned = data.get("lessons_learned", [])
        being.state = BeingState(data.get("state", "spawning"))
        being.created_at = data.get("created_at", datetime.now().isoformat())
        being.fitness = data.get("fitness", 0.0)
        being.ancestral_chain = data.get("ancestral_chain", [being.source_id])
        
        # Initialize stamina system if not present (backward compatibility)
        if not hasattr(being, 'willpower') or being.willpower is None:
            being.willpower = being._calculate_willpower()
        if not hasattr(being, 'stamina') or being.stamina is None:
            being.stamina = being._calculate_stamina()
        if not hasattr(being, 'stamina_max') or being.stamina_max is None:
            being.stamina_max = being.stamina
        if not hasattr(being, 'stamina_regeneration_rate') or being.stamina_regeneration_rate is None:
            being.stamina_regeneration_rate = 5.0
        
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
        
        # Set directory permissions (0700 = owner read/write/execute only)
        try:
            self.beings_path.chmod(0o700)
        except (OSError, PermissionError):
            # Ignore if permissions can't be set (e.g., on Windows)
            pass
        
        # Initialize Source Consciousness
        if source_consciousness is None:
            from .source_consciousness import SourceConsciousness
            self.source = SourceConsciousness(project_path=project_path)
        else:
            self.source = source_consciousness
    
    def _validate_being_id(self, being_id: str) -> bool:
        """
        Validate being_id is safe for file system use.
        
        Rejects:
        - IDs with path traversal (.., /, \)
        - IDs with null bytes or control characters
        - IDs that are too long (>255 characters)
        - IDs that aren't alphanumeric + underscore + hyphen
        
        Args:
            being_id: Being ID to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not being_id:
            return False
        if len(being_id) > 255:
            return False
        if any(c in being_id for c in ['..', '/', '\\', '\x00']):
            return False
        # Check for control characters
        if any(ord(c) < 32 and c not in ['\t', '\n', '\r'] for c in being_id):
            return False
        # Allow alphanumeric, underscore, hyphen
        if not being_id.replace('_', '').replace('-', '').isalnum():
            return False
        return True
    
    def _validate_path_in_project(self, file_path: Path) -> bool:
        """
        Validate file path is within project directory.
        
        Args:
            file_path: Path to validate
        
        Returns:
            True if path is within project, False otherwise
        """
        try:
            resolved = file_path.resolve()
            project_resolved = self.project_path.resolve()
            return resolved.is_relative_to(project_resolved)
        except (ValueError, OSError):
            return False
    
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
        parent_lifetimes = 0
        if parent_being_id:
            parent = self._load_being(parent_being_id)
            # Inherit skills (with slight mutation)
            for skill_name, skill_level in parent.skills.items():
                # Mutate skill level slightly (±5%)
                mutation = (hashlib.sha256(f"{being_id}{skill_name}".encode()).hexdigest()[:2])
                mutation_factor = (int(mutation, 16) / 255.0 - 0.5) * 0.1  # -5% to +5%
                skills[skill_name] = max(0.0, min(100.0, skill_level * (1.0 + mutation_factor)))
            # Get parent's lifetimes for reincarnation
            parent_lifetimes = parent.lifetimes
        
        # Create being (lifetimes will be set after creation)
        being = Being(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            skills=skills
        )
        
        # Set lifetimes: increment from parent if reincarnated, or 1 if first birth
        if parent_being_id:
            # Reincarnation: parent's lifetimes + 1
            being.lifetimes = parent_lifetimes + 1
        else:
            # First birth: this is lifetime 1
            being.lifetimes = 1
        
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
    
    def get_karma_balance(self, being: Being) -> float:
        """
        Get karma balance for a being via soul_id.
        
        If being doesn't have soul_id, create one from being_id.
        If karma_merchant is not available, returns 0.0.
        
        Args:
            being: Being instance
        
        Returns:
            Karma balance (0.0 if not available)
        """
        # Create soul_id from being_id if missing
        if being.soul_id is None:
            being.soul_id = f"soul_{being.being_id}"
        
        # Validate soul_id
        if not self._validate_being_id(being.soul_id):
            # Fallback: use being_id as soul_id (sanitized)
            sanitized_id = being.being_id.replace('..', '').replace('/', '_').replace('\\', '_')
            being.soul_id = f"soul_{sanitized_id}"
        
        # Try to get karma from KarmaMerchant if available
        try:
            from .karma import KarmaMerchant
            karma_merchant = KarmaMerchant(project_path=self.project_path)
            akasha_data = karma_merchant.access_akasha(being.soul_id)
            if akasha_data and isinstance(akasha_data, dict):
                return akasha_data.get("karma_balance", akasha_data.get("total_karma", 0.0))
        except (ImportError, AttributeError, Exception):
            # KarmaMerchant not available or access_akasha not implemented
            pass
        
        return 0.0
    
    def _save_being(self, being: Being) -> None:
        """
        Save being to disk with security measures.
        
        CRITICAL: Sets file permissions (0o600) and validates paths.
        
        Args:
            being: Being instance to save
        
        Raises:
            ValueError: If being_id is invalid
            OSError: If file cannot be written
        """
        # Validate being_id
        if not self._validate_being_id(being.being_id):
            raise ValueError(f"Invalid being_id: {being.being_id} (contains path traversal or invalid characters)")
        
        being_file = self.beings_path / f"{being.being_id}.json"
        
        # Validate path is within project
        if not self._validate_path_in_project(being_file):
            raise ValueError(f"Path traversal detected: {being_file}")
        
        try:
            with open(being_file, "w", encoding="utf-8") as f:
                json.dump(being.to_dict(), f, indent=2, ensure_ascii=False)
            
            # CRITICAL: Set restrictive file permissions (0o600 = owner read/write only)
            try:
                being_file.chmod(0o600)
            except (OSError, PermissionError):
                # Ignore if permissions can't be set (e.g., on Windows)
                pass
        except (IOError, OSError, PermissionError) as e:
            raise OSError(f"Failed to save being {being.being_id}: {e}")
    
    def _load_being(self, being_id: str) -> Being:
        """
        Load being from disk with security measures.
        
        CRITICAL: Validates being_id and file paths.
        
        Args:
            being_id: Being ID to load
        
        Returns:
            Being instance
        
        Raises:
            ValueError: If being_id is invalid
            FileNotFoundError: If being file doesn't exist
            json.JSONDecodeError: If file is corrupted
            OSError: If file cannot be read
        """
        # Validate being_id
        if not self._validate_being_id(being_id):
            raise ValueError(f"Invalid being_id: {being_id} (contains path traversal or invalid characters)")
        
        being_file = self.beings_path / f"{being_id}.json"
        
        # Validate path is within project
        if not self._validate_path_in_project(being_file):
            raise ValueError(f"Path traversal detected: {being_file}")
        
        if not being_file.exists():
            raise FileNotFoundError(f"Being file not found: {being_file}")
        
        try:
            with open(being_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Corrupted being file {being_id}: {e}", e.doc, e.pos)
        except (IOError, OSError, PermissionError) as e:
            raise OSError(f"Failed to load being {being_id}: {e}")
        
        return Being.from_dict(data)
