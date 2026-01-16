"""
Beings System: Timeful Agents in Realities

Beings are timeful, dynamic entities that exist in realities, learn skills, and evolve.
They move a lot, change things rapidly, and collect evidence that may influence
the timeless Entities in the Pantheon.

Unlike Entities (which are timeless Forces that Bind Reality Together), Beings are:
- **Timeful**: They move a lot and change things rapidly
- **Dynamic**: Constantly learning, evolving, and adapting
- **Evidence Collectors**: They gather evidence that may prove Entities need to change
- **Explorers**: They spawn into realities, learn through experience, evolve through
  natural selection, and pass memories/lessons upward

Beings have:
- Skills (learned abilities)
- Memories (experiences)
- Lessons (what worked/didn't work)
- Fitness (evolutionary success)
- Lifecycle attributes (will_to_live, luck, decision_fatigue, pleasure, pain)
- Personality and goals
- Sleep state

**Contrast with Entities**: See `src/waft/pantheon/README.md` for the timeless nature
of Pantheon Entities (Forces that Bind Reality Together).
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
    A Being - a timeful, dynamic entity that exists in realities, learns skills, and evolves.
    
    Beings are timeful agents that move a lot, change things rapidly, and collect evidence.
    Unlike Entities (timeless Forces that Bind Reality Together), Beings are dynamic explorers
    that constantly evolve and adapt.
    
    Beings have:
    - Skills (learned abilities with levels)
    - Memories (experiences)
    - Lessons (what worked/didn't work)
    - Fitness (evolutionary success)
    - Lineage (ancestral chain)
    - Lifecycle attributes (will_to_live, luck, decision_fatigue, pleasure, pain)
    - Personality and goals
    - Sleep state
    
    The evidence collected by Beings may influence the timeless Entities in the Pantheon,
    proving that Aspects of Creation need to change.
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
        recent_experiences: Optional[List[Dict[str, Any]]] = None,
        # Naming
        custom_name: Optional[str] = None
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
            custom_name: Optional custom name (e.g., "Bob") - overrides scientific name
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
        
        # Energy system (INNATE to all beings)
        # Energy capacity is derived from Karma (bidirectional relationship)
        self.energy: float = 100.0  # Current energy (0.0-100.0)
        self.energy_capacity: float = 100.0  # Max energy (derived from Karma)
        self.energy_well: float = 100.0  # Energy Well/Source (related to Karma)
        self.energy_regeneration_rate: float = 2.0  # Energy restored per cycle
        self._initialize_energy_from_karma()  # Initialize from Karma if available
        
        # Harm/Help tracking (for pain/pleasure calculation)
        self.recent_harm_events: List[Any] = []  # List of Harm objects
        self.recent_help_events: List[Any] = []  # List of Help objects
        
        # Alignment tracking
        self.current_alignment_score: float = 0.5  # Current alignment (0.0-1.0)
        self.alignment_history: List[Dict[str, Any]] = []  # History of alignment scores
        
        # Empirica integration (for first Being only - when parent_being_id is None)
        self.empirica_session_id: Optional[str] = None
        self.empirica_manager: Optional[Any] = None
        self._is_first_being = parent_being_id is None
        
        # Naming
        self.custom_name: Optional[str] = custom_name
        
        # Purpose system
        self.purpose_being_id: Optional[str] = None  # Link to Purpose Being
        self.purpose: Optional[Dict[str, Any]] = None  # Purpose object (direct)
    
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
    
    @property
    def scientific_name(self) -> str:
        """
        Generate scientific name from being_id using LineagePoet.
        
        Uses being_id as genome seed to generate deterministic scientific name.
        Format: "Genus Species, Title" (e.g., "Cognis Novus, the Fragile")
        
        Returns:
            Scientific name based on being_id hash
        """
        from .core.science.taxonomy import LineagePoet
        import hashlib
        
        # Generate genome_id from being_id (deterministic)
        # Use being_id as seed for hash-based naming
        genome_id = hashlib.sha256(self.being_id.encode()).hexdigest()
        return LineagePoet.generate_name(genome_id)
    
    @property
    def display_name(self) -> str:
        """
        Get display name for this being.
        
        Priority:
        1. custom_name (if user set one, e.g., "Bob")
        2. scientific_name (deterministic from hash)
        3. being_id (fallback)
        
        Returns:
            Display name to use
        """
        if self.custom_name:
            return self.custom_name
        return self.scientific_name
    
    def set_custom_name(self, name: str) -> None:
        """
        Set a custom name for this being (e.g., "Bob").
        
        This overrides the scientific name for display purposes.
        The scientific name is still available via scientific_name property.
        
        Args:
            name: Custom name to use
        """
        self.custom_name = name
    
    def get_purpose(self, being_system: Optional["BeingSystem"] = None) -> Optional[Dict[str, Any]]:
        """
        Get the purpose of this being.
        
        Args:
            being_system: Optional BeingSystem instance (to avoid circular import)
        
        Returns:
            Purpose dict if set, or None if no purpose
        """
        # If purpose is set directly, return it
        if self.purpose is not None:
            return self.purpose
        
        # If purpose_being_id is set, load Purpose Being and return its purpose
        if self.purpose_being_id:
            try:
                # Use provided being_system or create new one
                if being_system is None:
                    being_system = BeingSystem(project_path=Path.cwd())
                purpose_being = being_system._load_being(self.purpose_being_id)
                return purpose_being.purpose
            except Exception:
                # Purpose Being not found or error loading
                return None
        
        return None
    
    def set_purpose(self, purpose: Dict[str, Any]) -> None:
        """
        Set purpose directly on this being.
        
        Args:
            purpose: Purpose dict to set
        """
        self.purpose = purpose
        self.purpose_being_id = None  # Clear linked purpose being
    
    def imbue_with_purpose(self, purpose_being: "Being") -> None:
        """
        Imbue this being with a Purpose Being's purpose.
        
        Links this being to the Purpose Being, so this being's purpose
        comes from the Purpose Being.
        
        Args:
            purpose_being: Purpose Being to link to
        """
        self.purpose_being_id = purpose_being.being_id
        self.purpose = None  # Clear direct purpose (use linked instead)
    
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
    
    def _initialize_energy_from_karma(self) -> None:
        """
        Initialize energy capacity from Karma (bidirectional relationship).
        
        Karma → Energy Capacity: More karma = larger energy pool
        Formula: energy_capacity = base_capacity + (karma_balance / 100.0) * capacity_multiplier
        """
        base_capacity = 100.0
        capacity_multiplier = 50.0  # Each 100 karma = +50 energy capacity
        
        # Try to get karma balance
        karma_balance = 0.0
        if self.soul_id:
            try:
                from .karma import KarmaMerchant
                from pathlib import Path
                karma_merchant = KarmaMerchant(project_path=Path.cwd())
                akasha_data = karma_merchant.access_akasha(self.soul_id)
                if akasha_data and isinstance(akasha_data, dict):
                    karma_balance = akasha_data.get("karma_balance", akasha_data.get("total_karma", 0.0))
            except Exception:
                # KarmaMerchant not available or error
                pass
        
        # Calculate energy capacity from karma
        self.energy_capacity = base_capacity + (karma_balance / 100.0) * capacity_multiplier
        self.energy_well = self.energy_capacity  # Energy Well = capacity
        self.energy = min(self.energy, self.energy_capacity)  # Clamp current energy to capacity
    
    def update_energy_from_karma(self) -> None:
        """
        Update energy capacity from current Karma balance.
        
        Called when karma changes to update energy capacity.
        """
        self._initialize_energy_from_karma()
    
    def consume_energy(self, amount: float) -> float:
        """
        Consume energy for an action.
        
        Args:
            amount: Energy to consume
        
        Returns:
            Actual energy consumed (may be less if depleted)
        """
        actual_consumption = min(amount, self.energy)
        self.energy = max(0.0, self.energy - actual_consumption)
        return actual_consumption
    
    def regenerate_energy(self, amount: Optional[float] = None) -> float:
        """
        Regenerate energy (called each cycle).
        
        Args:
            amount: Amount to regenerate (defaults to energy_regeneration_rate)
        
        Returns:
            Actual energy regenerated
        """
        if amount is None:
            amount = self.energy_regeneration_rate
        
        old_energy = self.energy
        self.energy = min(self.energy_capacity, self.energy + amount)
        
        return self.energy - old_energy
    
    def get_energy_ratio(self) -> float:
        """
        Get energy as a ratio of capacity (0.0-1.0).
        
        Returns:
            Energy ratio
        """
        if self.energy_capacity == 0:
            return 0.0
        return self.energy / self.energy_capacity
    
    def is_energy_depleted(self) -> bool:
        """
        Check if energy is depleted (below 10% threshold).
        
        Returns:
            True if energy is critically low
        """
        return self.energy < (self.energy_capacity * 0.1)
    
    def generate_karma_from_energy(self, energy_spent: float) -> float:
        """
        Generate karma from energy expenditure (bidirectional relationship).
        
        Energy Spent → Karma: Energy expenditure generates karma
        Formula: karma_generated = energy_spent * karma_conversion_rate
        
        Args:
            energy_spent: Amount of energy spent
        
        Returns:
            Karma generated
        """
        karma_conversion_rate = 0.1  # Each 1.0 energy = 0.1 karma
        return energy_spent * karma_conversion_rate
    
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
        
        Enhanced to include Harm/Help events and alignment information.
        
        Args:
            memory_content: Content of memory
            memory_type: Type of memory
            metadata: Additional metadata (can include harm_events, help_events, alignment_score)
            
        Returns:
            Memory record
        """
        memory = {
            "content": memory_content,
            "type": memory_type,
            "recorded_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # Include Harm/Help events if available
        if self.recent_harm_events:
            memory["metadata"]["harm_events"] = [
                harm.to_dict() for harm in self.recent_harm_events
            ]
        if self.recent_help_events:
            memory["metadata"]["help_events"] = [
                help_event.to_dict() for help_event in self.recent_help_events
            ]
        
        # Include alignment information
        memory["metadata"]["alignment_score"] = self.current_alignment_score
        memory["metadata"]["pleasure"] = self.pleasure
        memory["metadata"]["pain"] = self.pain
        
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
        
        Enhanced to include alignment patterns and Harm/Help learning.
        
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
        
        # Include alignment information for learning
        lesson_record["metadata"]["alignment_score"] = self.current_alignment_score
        lesson_record["metadata"]["pleasure"] = self.pleasure
        lesson_record["metadata"]["pain"] = self.pain
        
        self.lessons_learned.append(lesson_record)
        
        # Learn from alignment patterns
        self._learn_from_alignment_patterns()
        
        return lesson_record
    
    def _learn_from_alignment_patterns(self) -> None:
        """
        Learn from alignment history to update personality/goals.
        
        Beings learn which actions create Alignment vs. Misalignment,
        and personality/goals evolve based on what creates Pleasure (Alignment).
        """
        if len(self.alignment_history) < 5:
            # Need at least 5 data points to learn patterns
            return
        
        # Analyze recent alignment history
        recent_history = self.alignment_history[-20:]  # Last 20 cycles
        
        # Calculate average alignment
        avg_alignment = sum(h["alignment_score"] for h in recent_history) / len(recent_history)
        
        # Calculate average pleasure/pain
        avg_pleasure = sum(h.get("pleasure", 0.0) for h in recent_history if "pleasure" in h) / len(recent_history)
        avg_pain = sum(h.get("pain", 0.0) for h in recent_history if "pain" in h) / len(recent_history)
        
        # If alignment consistently creates pleasure, being learns to seek alignment
        if avg_alignment > 0.7 and avg_pleasure > 0.5:
            # High alignment = high pleasure - being learns to maintain this
            # Adjust personality/goals to favor alignment-seeking behaviors
            if "alignment_seeking" not in self.personality:
                self.personality["alignment_seeking"] = 0.5
            self.personality["alignment_seeking"] = min(1.0, self.personality["alignment_seeking"] + 0.1)
        
        # If misalignment consistently creates pain, being learns to avoid it
        if avg_alignment < 0.3 and avg_pain > 0.5:
            # Low alignment = high pain - being learns to avoid this
            if "misalignment_avoidance" not in self.personality:
                self.personality["misalignment_avoidance"] = 0.5
            self.personality["misalignment_avoidance"] = min(1.0, self.personality["misalignment_avoidance"] + 0.1)
        
        # Update goals based on what creates alignment
        # If certain goals consistently lead to alignment, prioritize them
        if avg_alignment > 0.6:
            # High alignment - being learns which goals/actions create this
            # This is a simplified learning mechanism
            # In full implementation, would track which specific goals/actions led to alignment
            pass
    
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
        experience: Optional[Dict[str, Any]] = None,
        harm_events: Optional[List[Any]] = None,
        help_events: Optional[List[Any]] = None,
        alignment_score: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Calculate pleasure and pain from multiple sources:
        1. Harm/Help events (subjective interpretation)
        2. Alignment score (Arrow of Intent alignment)
        3. Personality-goal-experience alignment (existing)
        
        Modulated by Stamina (capacity to feel).
        
        Args:
            personality: Personality traits dict (defaults to self.personality)
            goals: Lifetime goals list (defaults to self.goals)
            experience: Experience dict from current cycle (defaults to recent_experiences)
            harm_events: List of Harm objects (defaults to self.recent_harm_events)
            help_events: List of Help objects (defaults to self.recent_help_events)
            alignment_score: Alignment score (defaults to self.current_alignment_score)
        
        Returns:
            (pleasure, pain) tuple (0.0-1.0 each), modulated by Stamina
        """
        from .core.personality_alignment import PersonalityAlignment
        from .core.alignment import AlignmentSystem
        
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
                experience = {"type": "neutral", "intensity": 0.0, "description": ""}
        
        if harm_events is None:
            harm_events = self.recent_harm_events
        if help_events is None:
            help_events = self.recent_help_events
        if alignment_score is None:
            alignment_score = self.current_alignment_score
        
        # Initialize systems
        personality_alignment = PersonalityAlignment()
        alignment_system = AlignmentSystem()
        
        # 1. Calculate base pleasure/pain from personality-goal-experience alignment
        base_pleasure, base_pain = personality_alignment.calculate_alignment(
            personality, goals, experience
        )
        
        # 2. Add pleasure/pain from Harm/Help events (subjective interpretation)
        harm_pain = 0.0
        help_pleasure = 0.0
        
        # Process harm events
        for harm in harm_events or []:
            # Calculate alignment between source and target (this being)
            # For now, use a simple interpretation based on harm severity
            # In full implementation, would use Arrow of Intent alignment
            interpreted_pain = harm.severity
            if not harm.intentional:
                # Unintentional harm causes less pain
                interpreted_pain *= 0.7
            harm_pain += interpreted_pain
        
        # Process help events
        for help_event in help_events or []:
            # Calculate alignment between source and target (this being)
            interpreted_pleasure = help_event.benefit
            if help_event.intentional:
                # Intentional help causes more pleasure
                interpreted_pleasure *= 1.2
            help_pleasure += interpreted_pleasure
        
        # Clamp harm/help contributions
        harm_pain = min(1.0, harm_pain)
        help_pleasure = min(1.0, help_pleasure)
        
        # 3. Add pleasure/pain from Alignment score
        alignment_pleasure = alignment_system.alignment_to_pleasure(alignment_score)
        alignment_pain = alignment_system.alignment_to_pain(alignment_score)
        
        # Combine all sources (weighted average)
        total_pleasure = (
            base_pleasure * 0.4 +
            help_pleasure * 0.3 +
            alignment_pleasure * 0.3
        )
        total_pain = (
            base_pain * 0.4 +
            harm_pain * 0.3 +
            alignment_pain * 0.3
        )
        
        # Clamp to 0.0-1.0
        total_pleasure = max(0.0, min(1.0, total_pleasure))
        total_pain = max(0.0, min(1.0, total_pain))
        
        # 4. Modulate by Stamina (capacity to feel)
        stamina_ratio = self.get_stamina_ratio()
        # Low stamina = reduced capacity to feel (numbness)
        # High stamina = full capacity to feel
        stamina_modifier = stamina_ratio * 0.5 + 0.5  # Maps [0.0, 1.0] to [0.5, 1.0]
        
        effective_pleasure = total_pleasure * stamina_modifier
        effective_pain = total_pain * stamina_modifier
        
        return (effective_pleasure, effective_pain)
    
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
    
    def _think_with_empirica(self, decision_type: str) -> Optional[str]:
        """
        Use Empirica to think about the decision (only for first Being).
        
        Args:
            decision_type: Type of decision being considered
        
        Returns:
            Gate result (PROCEED/HALT/BRANCH/REVISE) or None if Empirica not available
        """
        if not self._is_first_being or not self.empirica_manager or not self.empirica_session_id:
            return None
        
        try:
            # Use Empirica check gate to assess decision
            operation = {
                "type": "decision",
                "scope": "medium",
                "decision_type": decision_type,
                "being_state": {
                    "stamina_ratio": self.get_stamina_ratio(),
                    "will_to_live": self.will_to_live,
                    "personality_type": self.personality_type,
                    "decision_fatigue": self.decision_fatigue
                }
            }
            
            gate_result = self.empirica_manager.check_submit(operation)
            return gate_result
        except Exception:
            # If Empirica hangs or fails, just proceed without gate
            return None
    
    def _empirica_preflight(self, decision_type: str) -> bool:
        """
        Submit preflight assessment to Empirica before making decision.
        
        Args:
            decision_type: Type of decision being considered
        
        Returns:
            True if preflight submitted successfully, False otherwise
        """
        if not self._is_first_being or not self.empirica_manager or not self.empirica_session_id:
            return False
        
        try:
            # Calculate epistemic vectors based on being state
            vectors = {
                "engagement": min(1.0, self.will_to_live / 100.0),
                "foundation": {
                    "know": min(1.0, sum(self.skills.values()) / (len(self.skills) * 100.0) if self.skills else 0.0),
                    "do": min(1.0, self.stamina / 100.0),
                    "context": min(1.0, len(self.memories) / 10.0)  # Normalize to 0-1
                },
                "comprehension": {
                    "clarity": min(1.0, self.get_stamina_ratio()),
                    "coherence": min(1.0, (self.will_to_live + self.stamina) / 200.0),
                    "signal": min(1.0, len(self.lessons_learned) / 5.0),
                    "density": min(1.0, sum(self.skills.values()) / 500.0 if self.skills else 0.0)
                },
                "execution": {
                    "state": min(1.0, self.stamina / 100.0),
                    "change": 0.5,  # Default - will be updated postflight
                    "completion": 0.0,  # Will be updated postflight
                    "impact": 0.5  # Default - will be updated postflight
                },
                "uncertainty": max(0.0, 1.0 - (sum(self.skills.values()) / 500.0 if self.skills else 1.0))
            }
            
            reasoning = f"Considering {decision_type} decision. Stamina: {self.stamina:.1f}/{self.stamina_max:.1f}, Will to live: {self.will_to_live:.1f}, Fatigue: {self.decision_fatigue}/{self.decision_quota_max}"
            
            return self.empirica_manager.submit_preflight(
                self.empirica_session_id,
                vectors,
                reasoning
            )
        except Exception:
            # If Empirica hangs or fails, just continue without preflight
            return False
    
    def _empirica_postflight(self, decision_type: str, experience: Dict[str, Any]) -> bool:
        """
        Submit postflight assessment to Empirica after making decision.
        
        Args:
            decision_type: Type of decision that was made
            experience: Experience data from the decision
        
        Returns:
            True if postflight submitted successfully, False otherwise
        """
        if not self._is_first_being or not self.empirica_manager or not self.empirica_session_id:
            return False
        
        # Calculate epistemic vectors based on decision outcome
        success = experience.get("quality") in ["excellent", "good"]
        impact = experience.get("intensity", 0.5)
        
        vectors = {
            "engagement": min(1.0, self.will_to_live / 100.0),
            "foundation": {
                "know": min(1.0, sum(self.skills.values()) / (len(self.skills) * 100.0) if self.skills else 0.0),
                "do": min(1.0, self.stamina / 100.0),
                "context": min(1.0, len(self.memories) / 10.0)
            },
            "comprehension": {
                "clarity": min(1.0, self.get_stamina_ratio()),
                "coherence": min(1.0, (self.will_to_live + self.stamina) / 200.0),
                "signal": min(1.0, len(self.lessons_learned) / 5.0),
                "density": min(1.0, sum(self.skills.values()) / 500.0 if self.skills else 0.0)
            },
            "execution": {
                "state": min(1.0, self.stamina / 100.0),
                "change": 0.3 if success else 0.1,  # Positive change if successful
                "completion": 1.0 if success else 0.5,  # Completed if successful
                "impact": impact
            },
            "uncertainty": max(0.0, 1.0 - (sum(self.skills.values()) / 500.0 if self.skills else 1.0))
        }
        
        reasoning = f"Completed {decision_type} decision. Quality: {experience.get('quality', 'unknown')}, Stamina remaining: {self.stamina:.1f}, Mistakes: {len(experience.get('mistakes', []))}"
        
        return self.empirica_manager.submit_postflight(
            self.empirica_session_id,
            vectors,
            reasoning
        )
    
    def _empirica_log_finding(self, finding: str, impact: float = 0.5) -> bool:
        """
        Log a finding to Empirica.
        
        Args:
            finding: Description of the finding
            impact: Impact score (0.0-1.0)
        
        Returns:
            True if logged successfully, False otherwise
        """
        if not self._is_first_being or not self.empirica_manager:
            return False
        return self.empirica_manager.log_finding(finding, impact)
    
    def _empirica_log_unknown(self, unknown: str) -> bool:
        """
        Log an unknown to Empirica.
        
        Args:
            unknown: Description of what needs investigation
        
        Returns:
            True if logged successfully, False otherwise
        """
        if not self._is_first_being or not self.empirica_manager:
            return False
        return self.empirica_manager.log_unknown(unknown)
    
    def make_decision(self, decision_type: str, stamina_cost: float = 5.0) -> Dict[str, Any]:
        """
        Make a decision (decrements fatigue, consumes stamina, returns experience).
        
        When stamina is depleted, actions become sluggish, shitty, and make mistakes.
        For the first Being, uses Empirica for epistemic thinking.
        
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
        
        # Empirica preflight (for first Being) - non-blocking, continue if fails
        try:
            self._empirica_preflight(decision_type)
        except Exception:
            pass  # Continue even if preflight fails
        
        # Empirica check gate (for first Being) - non-blocking, continue if fails
        try:
            gate_result = self._think_with_empirica(decision_type)
        except Exception:
            gate_result = None  # Continue without gate if it fails
        if gate_result == "HALT":
            # Being decides to halt - log unknown and rest instead
            self._empirica_log_unknown(f"Decision {decision_type} halted by Empirica gate")
            decision_type = "rest"  # Fallback to rest
        elif gate_result == "BRANCH":
            # Being decides to branch - log finding
            self._empirica_log_finding(f"Decision {decision_type} requires branching investigation", impact=0.6)
        elif gate_result == "REVISE":
            # Being decides to revise - log finding
            self._empirica_log_finding(f"Decision {decision_type} needs revision", impact=0.4)
        
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
        
        # Empirica postflight (for first Being) - non-blocking
        try:
            self._empirica_postflight(decision_type, experience)
        except Exception:
            pass  # Continue even if postflight fails
        
        # Log findings/unknowns based on experience quality - non-blocking
        try:
            if experience.get("stamina_depleted"):
                self._empirica_log_unknown(f"Stamina depleted during {decision_type} - performance degraded")
            if experience.get("quality") == "excellent":
                self._empirica_log_finding(f"Excellent execution of {decision_type}", impact=0.7)
        except Exception:
            pass  # Continue even if logging fails
        
        return {
            "decision_type": decision_type,
            "experience": experience,
            "decision_fatigue_remaining": self.decision_fatigue,
            "stamina_remaining": self.stamina,
            "stamina_depleted": stamina_depleted,
            "empirica_gate": gate_result if self._is_first_being else None
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
            # Naming
            "custom_name": self.custom_name,
            # Purpose system
            "purpose_being_id": self.purpose_being_id,
            "purpose": self.purpose,
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
            recent_experiences=data.get("recent_experiences"),
            # Naming
            custom_name=data.get("custom_name")
        )
        
        # Purpose system (set after initialization to avoid __init__ signature issues)
        being.purpose_being_id = data.get("purpose_being_id")
        being.purpose = data.get("purpose")
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
    
    # TheOne Being ID - root ancestor for all Beings
    THE_ONE_BEING_ID = "the_one"
    
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
    
    def get_or_create_the_one(self) -> Being:
        """
        Get or create TheOne Being - the root ancestor for all Beings.
        
        TheOne is a special Being entity that serves as the root ancestor.
        All new Beings will be descendants of TheOne, ensuring a unified lineage.
        
        Returns:
            TheOne Being instance
        """
        # Check if TheOne exists
        the_one_file = self.beings_path / f"{self.THE_ONE_BEING_ID}.json"
        
        if the_one_file.exists():
            # Load existing TheOne
            return self._load_being(self.THE_ONE_BEING_ID)
        
        # Create Genesis Reality for TheOne
        from .reality import RealitySystem, RealityType
        reality_system = RealitySystem(project_path=self.project_path, source_consciousness=self.source)
        
        # Create Genesis Reality (will generate unique ID)
        genesis_reality = reality_system.create_reality(
            reality_type=RealityType.LEARNING,  # Use LEARNING if GENESIS doesn't exist
            configuration={"special": True, "purpose": "genesis"},
            source_id=self.source.source_id
        )
        genesis_reality_id = genesis_reality.reality_id
        
        # Create TheOne Being
        the_one = Being(
            being_id=self.THE_ONE_BEING_ID,
            reality_id=genesis_reality_id,
            parent_being_id=None,  # Spawns from Source
            source_id=self.source.source_id,
            lifetimes=1,  # First Being
            custom_name="TheOne"
        )
        
        # Set ancestral chain: [source_consciousness, the_one]
        the_one.ancestral_chain = [self.source.source_id, self.THE_ONE_BEING_ID]
        
        # Save TheOne
        self._save_being(the_one)
        
        # Register TheOne as permutation of source
        self.source.register_permutation(
            permutation_id=self.THE_ONE_BEING_ID,
            permutation_type="being",
            parent_id=None,
            metadata={
                "reality_id": genesis_reality_id,
                "special": True,
                "purpose": "root_ancestor"
            }
        )
        
        # Initialize CelestialBody and Guardian Beings
        try:
            from .prime_directive import (
                CelestialBody,
                MaintenanceStaff,
                SecurityTeam,
                Curator,
                PRIME_DIRECTIVE_BEING_IDS
            )
            
            # Initialize CelestialBody (Heart, Mind, Body, Spirit)
            celestial_body = CelestialBody(
                project_path=self.project_path,
                the_one_being_id=self.THE_ONE_BEING_ID
            )
            
            # Create Guardian Beings
            maintenance_staff = MaintenanceStaff(
                being_id=PRIME_DIRECTIVE_BEING_IDS["maintenance_staff"],
                reality_id=genesis_reality_id,
                project_path=self.project_path,
                parent_being_id=self.THE_ONE_BEING_ID
            )
            self._save_being(maintenance_staff)
            
            security_team = SecurityTeam(
                being_id=PRIME_DIRECTIVE_BEING_IDS["security_team"],
                reality_id=genesis_reality_id,
                project_path=self.project_path,
                parent_being_id=self.THE_ONE_BEING_ID
            )
            self._save_being(security_team)
            
            curator = Curator(
                being_id=PRIME_DIRECTIVE_BEING_IDS["curator"],
                reality_id=genesis_reality_id,
                project_path=self.project_path,
                parent_being_id=self.THE_ONE_BEING_ID
            )
            self._save_being(curator)
            
            # Record initialization in CelestialBody
            celestial_body.record_cycle({
                "type": "initialization",
                "event": "CelestialBody and Guardian Beings created",
                "guardian_beings": list(PRIME_DIRECTIVE_BEING_IDS.values()),
            })
            
            # Add reference to Prime Directive
            celestial_body.heart.add_reference(
                reference_type="being",
                reference_id=self.THE_ONE_BEING_ID,
                description="TheOne Being - root ancestor with CelestialBody"
            )
            
        except ImportError:
            # Prime Directive module not available - continue without it
            pass
        
        return the_one
    
    def _validate_being_id(self, being_id: str) -> bool:
        """
        Validate being_id is safe for file system use.
        
        Rejects:
        - IDs with path traversal (.., /, \\)
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
        
        All new Beings are descendants of TheOne, ensuring a unified lineage.
        
        Args:
            reality_id: Reality to spawn into
            parent_being_id: Optional parent being ID
            initial_skills: Optional initial skills
            
        Returns:
            Created Being instance
        """
        # Get or create TheOne (root ancestor)
        the_one = self.get_or_create_the_one()
        
        # If parent_being_id is None (spawning from Source), set parent to TheOne
        if parent_being_id is None:
            parent_being_id = the_one.being_id
        
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
        # Check if parent had custom_name to inherit
        custom_name = None
        if parent_being_id:
            try:
                parent = self._load_being(parent_being_id)
                # Optionally inherit custom name (or let user set new one)
                # For now, don't inherit - each being gets fresh name
                pass
            except Exception:
                pass
        
        being = Being(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            skills=skills,
            custom_name=custom_name
        )
        
        # Set lifetimes: increment from parent if reincarnated, or 1 if first birth
        if parent_being_id:
            # Reincarnation: parent's lifetimes + 1
            being.lifetimes = parent_lifetimes + 1
        else:
            # First birth: this is lifetime 1
            being.lifetimes = 1

            # Initialize Empirica for the first Being (optional - Being works without it)
            try:
                from .core.empirica import EmpiricaManager
                empirica_manager = EmpiricaManager(project_path=self.project_path)

                # Check if Empirica is initialized, initialize if needed
                if not empirica_manager.is_initialized():
                    # Try to initialize Empirica (may fail if not installed)
                    initialized = empirica_manager.initialize()
                    if not initialized:
                        # Empirica not available - Being works without it
                        pass
                    else:
                        # Create Empirica session for this Being
                        session_id = empirica_manager.create_session(
                            ai_id=being_id,
                            session_type="being_lifecycle"
                        )
                        if session_id:
                            being.empirica_manager = empirica_manager
                            being.empirica_session_id = session_id
                else:
                    # Empirica already initialized - create session
                    session_id = empirica_manager.create_session(
                        ai_id=being_id,
                        session_type="being_lifecycle"
                    )
                    if session_id:
                        being.empirica_manager = empirica_manager
                        being.empirica_session_id = session_id
            except (ImportError, Exception):
                # Empirica not available or failed - Being works without it
                pass
        
        # Build ancestral chain - always include TheOne
        if parent_being_id:
            parent_chain = self.source.get_ancestral_chain(parent_being_id)
            # Ensure TheOne is in the chain (should be, but verify)
            if self.THE_ONE_BEING_ID not in parent_chain:
                # Insert TheOne after source_consciousness
                if self.source.source_id in parent_chain:
                    source_idx = parent_chain.index(self.source.source_id)
                    parent_chain.insert(source_idx + 1, self.THE_ONE_BEING_ID)
                else:
                    # If source not in chain, prepend both
                    parent_chain = [self.source.source_id, self.THE_ONE_BEING_ID] + parent_chain[1:]
            being.ancestral_chain = parent_chain + [being_id]
        else:
            # Shouldn't happen now (parent is always TheOne), but handle gracefully
            being.ancestral_chain = [self.source.source_id, self.THE_ONE_BEING_ID, being_id]
        
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
        
        # Add reference to Prime Directive
        try:
            from .prime_directive import CelestialBody
            celestial_body = CelestialBody(project_path=self.project_path)
            celestial_body.heart.add_reference(
                reference_type="being",
                reference_id=being.being_id,
                description=f"Being {being.being_id} spawned in reality {reality_id}"
            )
        except ImportError:
            # Prime Directive module not available
            pass
        
        # Generate character sheet .txt (default, automatic)
        # Only generates .txt by default - .md and .pdf are on-demand
        try:
            from ..evolution.being_character_sheet_generator import generate_character_sheet_txt
            generate_character_sheet_txt(being, project_path=self.project_path)
        except (ImportError, Exception):
            # Character sheet generation optional - Being works without it
            pass
        
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
    
    def reincarnate_being(
        self,
        dead_being_id: str,
        reality_id: Optional[str] = None,
        use_karma: bool = True,
        purchase_order: Optional[Dict[str, Any]] = None
    ) -> Being:
        """
        Reincarnate a dead (ARCHIVED) Being into a new lifetime.
        
        This bridges the death → rebirth cycle. The Being's soul (via soul_id)
        can use accumulated Karma to purchase a life-path, or simply reincarnate
        with inherited skills.
        
        Process:
        1. Load the archived Being
        2. Verify it's dead (ARCHIVED state)
        3. Optionally use KarmaMerchant if available and use_karma=True
        4. Spawn new Being with parent_being_id pointing to dead Being
        5. New Being's lifetimes = dead Being's lifetimes + 1
        
        Args:
            dead_being_id: ID of the archived/dead Being to reincarnate
            reality_id: Reality to spawn into (defaults to dead Being's reality)
            use_karma: Whether to attempt Karma-based reincarnation (default: True)
            purchase_order: Optional purchase order for KarmaMerchant
                          (life_path_id, class, experience_packages, memory_continuity)
        
        Returns:
            New Being instance (reincarnated)
        
        Raises:
            ValueError: If Being is not archived/dead
        """
        # Load the dead Being
        dead_being = self._load_being(dead_being_id)
        
        # Verify it's dead
        if dead_being.state != BeingState.ARCHIVED:
            raise ValueError(
                f"Being {dead_being_id} is not dead (state: {dead_being.state.value}). "
                "Only ARCHIVED Beings can be reincarnated."
            )
        
        # Use reality from dead Being if not specified
        if reality_id is None:
            reality_id = dead_being.reality_id
        
        # Try Karma-based reincarnation if requested
        if use_karma and dead_being.soul_id:
            try:
                from .karma import KarmaMerchant
                karma_merchant = KarmaMerchant(project_path=self.project_path)
                
                # Check if reincarnate is implemented
                if hasattr(karma_merchant, 'reincarnate') and callable(karma_merchant.reincarnate):
                    # Try to access Akasha to check Karma
                    akasha_data = karma_merchant.access_akasha(dead_being.soul_id)
                    
                    if akasha_data and isinstance(akasha_data, dict):
                        karma_balance = akasha_data.get("karma_balance", akasha_data.get("total_karma", 0.0))
                        
                        # If we have Karma and a purchase order, use Karma-based reincarnation
                        if karma_balance > 0 and purchase_order:
                            try:
                                reincarnation_result = karma_merchant.reincarnate(
                                    dead_being.soul_id,
                                    purchase_order
                                )
                                
                                # If reincarnate returns agent_config, use it
                                if reincarnation_result and "agent_config" in reincarnation_result:
                                    agent_config = reincarnation_result["agent_config"]
                                    
                                    # Spawn with purchased configuration
                                    new_being = self.spawn_being(
                                        reality_id=reality_id,
                                        parent_being_id=dead_being_id,
                                        initial_skills=agent_config.get("skills", {})
                                    )
                                    
                                    # Apply other config if present
                                    if "personality" in agent_config:
                                        new_being.personality = agent_config["personality"]
                                    if "personality_type" in agent_config:
                                        new_being.personality_type = agent_config["personality_type"]
                                    if "goals" in agent_config:
                                        new_being.goals = agent_config["goals"]
                                    
                                    # Inherit soul_id for continuity
                                    new_being.soul_id = dead_being.soul_id
                                    
                                    self._save_being(new_being)
                                    return new_being
                            except Exception:
                                # Karma reincarnation failed, fall through to simple reincarnation
                                pass
            except (ImportError, AttributeError, Exception):
                # KarmaMerchant not available or not fully implemented, fall through
                pass
        
        # Fallback: Simple reincarnation (inherit skills with mutation)
        # This is the basic evolutionary mechanism
        new_being = self.spawn_being(
            reality_id=reality_id,
            parent_being_id=dead_being_id
        )
        
        # Inherit soul_id for continuity across lifetimes
        if dead_being.soul_id:
            new_being.soul_id = dead_being.soul_id
        
        # Inherit some memories/lessons based on memory_continuity if specified
        if purchase_order and "memory_continuity" in purchase_order:
            continuity = purchase_order["memory_continuity"]
            if 0.0 < continuity <= 1.0:
                # Carry over a percentage of memories
                num_memories = int(len(dead_being.memories) * continuity)
                new_being.memories = dead_being.memories[-num_memories:] if num_memories > 0 else []
                
                # Carry over some lessons
                num_lessons = int(len(dead_being.lessons_learned) * continuity)
                new_being.lessons_learned = dead_being.lessons_learned[-num_lessons:] if num_lessons > 0 else []
        
        self._save_being(new_being)
        return new_being
    
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
    
    def save_being(self, being: Being) -> None:
        """
        Save a Being to disk.
        
        Public API for saving beings (wraps _save_being).
        
        CRITICAL: Sets file permissions (0o600) and validates paths.
        
        Args:
            being: Being instance to save
        
        Raises:
            ValueError: If being_id is invalid
            OSError: If file cannot be written
        """
        self._save_being(being)
    
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
    
    def get_user_feedback(
        self,
        sentiment: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get user feedback from The One Being.
        
        Retrieves memories with type "user_feedback" from The One Being,
        optionally filtered by sentiment ("love" or "hate").
        
        Args:
            sentiment: Optional filter by sentiment ("love" or "hate")
            limit: Optional limit on number of feedback items to return
        
        Returns:
            List of feedback memory dicts with metadata
        """
        the_one = self.get_or_create_the_one()
        
        # Filter memories for user feedback
        feedback_memories = [
            mem for mem in the_one.memories
            if mem.get("type") == "user_feedback"
        ]
        
        # Filter by sentiment if specified
        if sentiment:
            feedback_memories = [
                mem for mem in feedback_memories
                if mem.get("metadata", {}).get("sentiment") == sentiment
            ]
        
        # Sort by most recent first
        feedback_memories.sort(
            key=lambda x: x.get("recorded_at", ""),
            reverse=True
        )
        
        # Apply limit if specified
        if limit:
            feedback_memories = feedback_memories[:limit]
        
        return feedback_memories
    
    def record_user_feedback(
        self,
        content: str,
        sentiment: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record user feedback to The One Being.
        
        Args:
            content: Feedback content/description
            sentiment: "love" or "hate"
            context: Optional additional context metadata
        
        Returns:
            Recorded memory dict
        """
        the_one = self.get_or_create_the_one()
        
        # Update Being's emotional state
        if sentiment == "love":
            the_one.pleasure = min(100.0, the_one.pleasure + 5.0)
        elif sentiment == "hate":
            the_one.pain = min(100.0, the_one.pain + 5.0)
        
        # Record memory
        memory = the_one.record_memory(
            memory_content=content,
            memory_type="user_feedback",
            metadata={
                "sentiment": sentiment,
                "context": context or {},
                "influence_weight": 1.0 if sentiment == "love" else -1.0,
                "recorded_at": datetime.now().isoformat()
            }
        )
        
        # Save Being
        self._save_being(the_one)
        
        return memory
