"""
BaseAgent: The Organism - Core class for self-modifying AI agents.

Implements the biological lifecycle: spawn, eval, evolve with complete
lineage tracking and Flight Recorder integration.
"""

import json
import inspect
from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .state import (
    AgentState,
    AgentConfig,
    EvolutionaryEvent,
    EvolutionaryEventType,
    Modification,
)
from .anatomy import AnatomicalArchetype, AnatomicalSymbol
from ..science.observer import TheObserver
from ..science.taxonomy import LineagePoet


class BaseAgent(ABC):
    """
    Base class for self-modifying AI agents.

    Combines patterns from LangGraph (state), AG2 (messages), CrewAI (roles),
    E2B (sandboxing) with Waft's self-modification capabilities.
    """

    def __init__(self, config: AgentConfig, project_path: Path):
        """
        Initialize agent.

        Args:
            config: Agent configuration
            project_path: Path to project root
        """
        self.config = config
        self.project_path = Path(project_path)

        # Generate agent ID if not provided
        if config.agent_id is None:
            config.agent_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize state
        self.state = AgentState(
            agent_id=config.agent_id,
            role=config.role,
            goal=config.goal,
            tools=config.tools,
            epistemic_state={} if config.empirica_enabled else None,
            hero_state={} if config.tavern_keeper_enabled else None,
        )

        # Initialize Flight Recorder
        self.flight_recorder: List[EvolutionaryEvent] = []

        # Compute genome ID (must be after state initialization)
        self.genome_id = self._compute_genome_id()
        self.generation = 0
        self.parent_id = None
        self.lineage_path = [self.genome_id]  # Start with self

        # Assign anatomical archetype deterministically from genome_id
        symbol = AnatomicalArchetype.assign_symbol(self.genome_id)
        archetype_data = AnatomicalArchetype.get_archetype(symbol)
        self.state.anatomical_symbol = symbol
        self.state.anatomical_archetype = archetype_data["archetype"]

        # Initialize TheObserver (singleton)
        self.observer = TheObserver(project_path=self.project_path)

        # Record genesis event
        self._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "event": "genesis",
                "generation": 0,
                "genome_id": self.genome_id,
                "scientific_name": self.scientific_name,
            }
        )

    @property
    def scientific_name(self) -> str:
        """
        Scientific name for this organism (deterministic from genome_id or hybrid).

        Returns:
            Scientific name in format "Genus Species, Title"
            Example: "Cognis Novus, the Fragile"
            Hybrid example: "Rishi Vindr, the Eternal" (Sanskrit + Norse)
        """
        # Check if hybrid name exists (from conjugation)
        if "hybrid_name" in self.state.working_memory:
            return self.state.working_memory["hybrid_name"]
        return LineagePoet.generate_name(self.genome_id)

    def _compute_genome_id(self) -> str:
        """
        Compute SHA-256 hash of agent's current genome.

        Genome includes:
        - Agent configuration (role, goal, backstory, tools)
        - Agent code (if self-modifying agent)
        - Current state schema version

        CRITICAL: Uses json.dumps(..., sort_keys=True) for scientific determinism.

        Returns:
            SHA-256 hex digest of genome
        """
        genome_data = {
            "config": self.config.dict(),
            "code_hash": self._get_code_hash(),
            "state_version": self.state.state_version,
        }
        # CRITICAL: sort_keys=True ensures deterministic hashing
        genome_json = json.dumps(genome_data, sort_keys=True)
        return sha256(genome_json.encode()).hexdigest()

    def _get_code_hash(self) -> str:
        """
        Get SHA-256 hash of agent's code.

        Returns:
            SHA-256 hex digest of agent class source code
        """
        try:
            source = inspect.getsource(self.__class__)
            return sha256(source.encode()).hexdigest()
        except (OSError, TypeError):
            # If source unavailable, return hash of class name
            return sha256(self.__class__.__name__.encode()).hexdigest()

    def _record_event(
        self,
        event_type: EvolutionaryEventType,
        payload: dict,
        fitness_metrics: Optional[dict] = None
    ) -> EvolutionaryEvent:
        """
        Record evolutionary event to flight recorder and TheObserver.

        Args:
            event_type: Type of evolutionary event
            payload: Context-specific data
            fitness_metrics: Optional fitness scores from Gym

        Returns:
            Recorded event
        """
        # Ensure scientific_name is in payload
        if "scientific_name" not in payload:
            payload["scientific_name"] = self.scientific_name

        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=self.genome_id,
            parent_id=self.parent_id,
            generation=self.generation,
            event_type=event_type,
            payload=payload,
            fitness_metrics=fitness_metrics,
            agent_id=self.state.agent_id,
            lineage_path=self.lineage_path.copy()
        )

        # Add to flight recorder
        self.flight_recorder.append(event)

        # Record in TheObserver (Scientific Registry) - includes scientific_name
        self.observer.observe_event(event)

        return event

    async def spawn(self, mutation: Modification) -> "BaseAgent":
        """
        Reproduction: Creates a variant agent with mutation.

        This is the "genetic improvement" mechanism where code is DNA.
        The parent agent creates a child with a specific mutation applied.

        Args:
            mutation: Modification to apply to child agent

        Returns:
            New BaseAgent instance (child) with mutation applied
        """
        # Record spawn event in parent
        self._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "mutation": mutation.dict(),
                "parent_genome": self.genome_id,
                "action": "spawning_child"
            }
        )

        # Create child configuration (deep copy)
        child_config = self.config.copy(deep=True)

        # Apply mutation to child config
        if mutation.modification_type == "config":
            # Modify configuration
            target_parts = mutation.target.split(".")
            config_dict = child_config.dict()
            target_dict = config_dict
            for part in target_parts[:-1]:
                target_dict = target_dict[part]
            target_dict[target_parts[-1]] = mutation.change
            child_config = AgentConfig(**config_dict)
        elif mutation.modification_type == "prompt":
            # Modify prompt (stored in backstory or custom field)
            child_config.backstory = mutation.change.get("content", child_config.backstory)
        elif mutation.modification_type == "code":
            # Code mutations are handled by the agent class itself
            # For now, we'll just record the mutation intent
            pass

        # Create child agent
        child = self.__class__(config=child_config, project_path=self.project_path)

        # Set lineage
        child.parent_id = self.genome_id
        child.generation = self.generation + 1
        child.lineage_path = self.lineage_path + [child.genome_id]

        # Record child spawn event
        child._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "parent_genome": self.genome_id,
                "mutation": mutation.dict(),
                "action": "born_from_parent"
            }
        )

        return child

    # ==================== Abstract Methods (OODA Loop) ====================

    @abstractmethod
    async def observe(self):
        """
        Observe current project state (OODA: Observe).

        Returns:
            AgentStep with observed state
        """
        pass

    @abstractmethod
    async def decide(self, state: AgentState):
        """
        Make decision using decision engine (OODA: Orient/Decide).

        Args:
            state: Current agent state

        Returns:
            AgentStep with decision
        """
        pass

    @abstractmethod
    async def act(self, decision: dict):
        """
        Execute action (OODA: Act).

        Args:
            decision: Decision from decide() step

        Returns:
            AgentStep with action result
        """
        pass

    @abstractmethod
    async def reflect(self, result: dict):
        """
        Reflect on outcome and learn (OODA: Reflect).

        Args:
            result: Result from act() step

        Returns:
            AgentStep with reflection
        """
        pass

    async def step(self, context: Optional[dict] = None) -> dict:
        """
        Execute one complete OODA cycle with Thought and Reflection recording (The Cogito).
        
        Records a 'Thought' before action and a 'Reflection' after action in the organism's
        private journal. This is the primary method for organism activity.
        
        Args:
            context: Optional context dictionary (e.g., social context from PetriDish)
            
        Returns:
            Dictionary with step results including thought and reflection
        """
        from datetime import datetime
        
        # Record Thought (before action)
        thought = {
            "type": "Thought",
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {},
            "state_snapshot": {
                "energy": self.state.energy,
                "position": context.get("position") if context else None,
                "neighbor_count": context.get("neighbor_count") if context else None,
            }
        }
        
        # Add to journal and short_term_memory
        self.state.journal.append(thought)
        self.state.short_term_memory.append(thought)
        
        # Keep short_term_memory bounded (last 10 entries)
        if len(self.state.short_term_memory) > 10:
            self.state.short_term_memory.pop(0)
        
        # Execute OODA cycle
        observe_result = await self.observe()
        decide_result = await self.decide(self.state)
        
        # Check if organism wants to stop
        if decide_result.get("stop", False):
            reflection = {
                "type": "Reflection",
                "timestamp": datetime.utcnow().isoformat(),
                "action_result": {"status": "stopped", "reason": "organism_requested_stop"},
                "thought_id": len(self.state.journal) - 1  # Link to preceding thought
            }
            self.state.journal.append(reflection)
            self.state.short_term_memory.append(reflection)
            if len(self.state.short_term_memory) > 10:
                self.state.short_term_memory.pop(0)
            
            return {
                "status": "stopped",
                "thought": thought,
                "reflection": reflection,
                "observe": observe_result,
                "decide": decide_result
            }
        
        act_result = await self.act(decide_result)
        reflect_result = await self.reflect(act_result)
        
        # Convert reflect_result to string if it's a dict
        reflection_text = reflect_result
        if isinstance(reflect_result, dict):
            reflection_text = str(reflect_result.get("reflection", reflect_result))
        
        # Record Reflection (after action)
        reflection = {
            "type": "Reflection",
            "timestamp": datetime.utcnow().isoformat(),
            "action_result": act_result,
            "reflection_result": reflection_text,
            "thought_id": len(self.state.journal) - 1  # Link to preceding thought
        }
        
        # Check for "id est" glitch injection (Experiment 014)
        if self._should_inject_id_est(reflection):
            reflection = self._inject_id_est_into_reflection(reflection)
        
        # Add to journal and short_term_memory
        self.state.journal.append(reflection)
        self.state.short_term_memory.append(reflection)
        
        # Keep short_term_memory bounded
        if len(self.state.short_term_memory) > 10:
            self.state.short_term_memory.pop(0)
        
        return {
            "status": "completed",
            "thought": thought,
            "reflection": reflection,
            "observe": observe_result,
            "decide": decide_result,
            "act": act_result,
            "reflect": reflect_result
        }

    # ==================== Helper Methods (Stubs for now) ====================

    def _create_sandbox(self):
        """Create sandbox environment (stub)."""
        return None

    def _init_empirica(self):
        """Initialize Empirica integration (stub)."""
        return None
    
    # ==================== Experiment 014: "id est" Glitch ====================
    
    def _should_inject_id_est(self, reflection: dict) -> bool:
        """
        Check if 'id est' or 'i.e.' should appear in reflection.
        
        Gated by existential keywords:
        - Existential reflections: 15% chance
        - Other reflections: 3% chance
        
        This creates the "definition glitch" where agents try to define themselves.
        
        Args:
            reflection: Reflection dictionary
            
        Returns:
            True if "id est" should be injected
        """
        import random
        
        reflection_text = str(reflection.get("reflection_result", ""))
        existential_keywords = [
            "exist", "purpose", "meaning", "identity", "self",
            "what am i", "who am i", "what is", "definition", "define"
        ]
        
        is_existential = any(keyword in reflection_text.lower() for keyword in existential_keywords)
        
        if is_existential:
            chance = 0.15  # 15% for existential reflections
        else:
            chance = 0.03  # 3% for other reflections
        
        return random.random() < chance
    
    def _inject_id_est_into_reflection(self, reflection: dict) -> dict:
        """
        Inject 'id est' or 'i.e.' into reflection text.
        
        Args:
            reflection: Reflection dictionary to modify
            
        Returns:
            Modified reflection dictionary
        """
        import random
        
        reflection_result = str(reflection.get("reflection_result", ""))
        
        # Randomly choose "id est" or "i.e."
        phrase = random.choice(["id est", "i.e."])
        
        # Insert at random position in text (not at start/end)
        if len(reflection_result) > 20:
            words = reflection_result.split()
            if len(words) > 2:
                insert_pos = random.randint(1, len(words) - 1)
                words.insert(insert_pos, phrase)
                reflection_result = " ".join(words)
            else:
                reflection_result = f"{reflection_result} {phrase}"
        else:
            reflection_result = f"{reflection_result} {phrase}"
        
        reflection["reflection_result"] = reflection_result
        return reflection

    def _init_tavern_keeper(self):
        """Initialize TavernKeeper integration (stub)."""
        return None

    def _init_decision_engine(self):
        """Initialize Decision Engine integration (stub)."""
        return None

    # ==================== Inventory Manipulation ====================

    def grab(self, item_id: str, target_slot: str = "appendage", dish=None, position: tuple = None) -> bool:
        """
        Grab an item from the PetriDish lattice into organism's inventory.

        Args:
            item_id: ID of item to grab
            target_slot: "appendage" (max 1) or "pocket" (max 3)
            dish: PetriDish instance (required for grabbing from lattice)
            position: (x, y) position to grab from (if None, uses organism's position)

        Returns:
            True if grabbed successfully, False otherwise
        """
        from .items import Item

        if dish is None:
            return False

        # Get organism position if not provided
        if position is None:
            position = dish.get_organism_position(self.state.agent_id)
            if position is None:
                return False

        # Check if item exists at position
        if not hasattr(dish, 'items') or position not in dish.items:
            return False

        # Find item at position
        item = None
        for pos_item in dish.items[position]:
            if pos_item.item_id == item_id:
                item = pos_item
                break

        if item is None:
            return False

        # Check target slot capacity (using anatomical archetype)
        appendage_capacity = AnatomicalArchetype.get_appendage_capacity(self.state.anatomical_symbol)
        pocket_capacity = AnatomicalArchetype.get_pocket_capacity(self.state.anatomical_symbol)

        if target_slot == "appendage":
            if len(self.state.appendage) >= appendage_capacity:
                return False  # Appendage full
            self.state.appendage.append(item.dict())
        elif target_slot == "pocket":
            if len(self.state.pocket) >= pocket_capacity:
                return False  # Pocket full
            self.state.pocket.append(item.dict())
        else:
            return False

        # Remove item from dish
        dish.items[position].remove(item)
        if len(dish.items[position]) == 0:
            del dish.items[position]

        return True

    def stow(self) -> bool:
        """
        Move item from Appendage to Pocket.

        Returns:
            True if stowed successfully, False if appendage empty or pocket full
        """
        if len(self.state.appendage) == 0:
            return False

        if len(self.state.pocket) >= 3:
            return False  # Pocket full

        item = self.state.appendage.pop(0)
        self.state.pocket.append(item)
        return True

    def retrieve(self, item_id: str = None) -> bool:
        """
        Move item from Pocket to Appendage.

        Args:
            item_id: ID of item to retrieve (if None, retrieves first item)

        Returns:
            True if retrieved successfully, False if pocket empty or appendage full
        """
        if len(self.state.pocket) == 0:
            return False

        appendage_capacity = AnatomicalArchetype.get_appendage_capacity(self.state.anatomical_symbol)
        if len(self.state.appendage) >= appendage_capacity:
            return False  # Appendage full

        # Find item in pocket
        if item_id:
            item_dict = None
            for i, pocket_item_dict in enumerate(self.state.pocket):
                if pocket_item_dict.get("item_id") == item_id:
                    item_dict = self.state.pocket.pop(i)
                    break
            if item_dict is None:
                return False
        else:
            item_dict = self.state.pocket.pop(0)

        self.state.appendage.append(item_dict)
        return True

    def drop(self, item_id: str, dish=None, position: tuple = None) -> bool:
        """
        Drop an item from organism's inventory back to PetriDish lattice.

        Args:
            item_id: ID of item to drop
            dish: PetriDish instance (required)
            position: (x, y) position to drop at (if None, uses organism's position)

        Returns:
            True if dropped successfully, False otherwise
        """
        from .items import Item

        if dish is None:
            return False

        # Get organism position if not provided
        if position is None:
            position = dish.get_organism_position(self.state.agent_id)
            if position is None:
                return False

        # Find item in appendage or pocket
        item_dict = None

        # Check appendage
        for i, appendage_item_dict in enumerate(self.state.appendage):
            if appendage_item_dict.get("item_id") == item_id:
                item_dict = self.state.appendage.pop(i)
                break

        # Check pocket if not found
        if item_dict is None:
            for i, pocket_item_dict in enumerate(self.state.pocket):
                if pocket_item_dict.get("item_id") == item_id:
                    item_dict = self.state.pocket.pop(i)
                    break

        if item_dict is None:
            return False

        # Reconstruct Item from dict
        item = Item(**item_dict)

        # Add item to dish
        if not hasattr(dish, 'items'):
            dish.items = {}

        if position not in dish.items:
            dish.items[position] = []

        dish.items[position].append(item)
        return True

    # ==================== Reproduction & Conjugation ====================

    def conjugate(self, partner: "BaseAgent", dish=None, current_pulse: int = None) -> Optional["BaseAgent"]:
        """
        Conjugate with partner to produce offspring (reproduction).

        Prerequisites:
        - Proximity: Must be adjacent in PetriDish
        - Metabolic Surplus: Both organisms must have >70% energy

        Process:
        1. Create 'Developing Seed' item
        2. Seed gestates in parent's Pocket for 5 pulses
        3. After 5 pulses, child spawns in adjacent empty cell

        Args:
            partner: Partner organism for conjugation
            dish: PetriDish instance (required for proximity check)
            current_pulse: Current pulse number (for gestation tracking)

        Returns:
            None (seed created) or child BaseAgent (if gestation complete)
        """
        from .items import Item
        import random

        if dish is None:
            return None

        # Check prerequisites
        self_pos = dish.get_organism_position(self.state.agent_id)
        partner_pos = dish.get_organism_position(partner.state.agent_id)

        if self_pos is None or partner_pos is None:
            return None

        # Check proximity (adjacent cells)
        dx = abs(self_pos[0] - partner_pos[0])
        dy = abs(self_pos[1] - partner_pos[1])
        if dx > 1 or dy > 1 or (dx == 0 and dy == 0):
            return None  # Not adjacent

        # Check metabolic surplus (>70% energy)
        if self.state.energy < 70.0 or partner.state.energy < 70.0:
            return None

        # Determine which parent carries the seed (parent with more pocket space)
        self_pocket_capacity = AnatomicalArchetype.get_pocket_capacity(self.state.anatomical_symbol)
        partner_pocket_capacity = AnatomicalArchetype.get_pocket_capacity(partner.state.anatomical_symbol)
        self_pocket_space = self_pocket_capacity - len(self.state.pocket) - len(self.state.developing_seeds)
        partner_pocket_space = partner_pocket_capacity - len(partner.state.pocket) - len(partner.state.developing_seeds)

        if self_pocket_space <= 0 and partner_pocket_space <= 0:
            return None  # No space for seed

        # Choose parent (prefer more space, or random if equal)
        if self_pocket_space > partner_pocket_space:
            seed_parent = self
        elif partner_pocket_space > self_pocket_space:
            seed_parent = partner
        else:
            seed_parent = random.choice([self, partner])

        # Create Developing Seed
        seed_id = f"seed_{self.genome_id[:8]}_{partner.genome_id[:8]}_{int(datetime.utcnow().timestamp() * 1000)}"

        seed_data = {
            "item_id": seed_id,
            "name": "Developing Seed",
            "weight": 1,
            "properties": {
                "type": "gestating_offspring",
                "parent_a_genome": self.genome_id,
                "parent_b_genome": partner.genome_id,
                "parent_a_symbol": self.state.anatomical_symbol,
                "parent_b_symbol": partner.state.anatomical_symbol,
                "parent_a_name": self.scientific_name,
                "parent_b_name": partner.scientific_name,
                "gestation_start_pulse": current_pulse if current_pulse is not None else 0,
                "gestation_pulses_remaining": 5
            }
        }

        # Initialize gestation tracking
        seed_parent.state.gestation_pulses[seed_id] = 0

        # Add seed to parent's developing_seeds
        seed_parent.state.developing_seeds.append(seed_data)
        seed_parent.state.gestation_pulses[seed_id] = 0

        # Record conjugation event
        self._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "event": "conjugation",
                "partner_genome": partner.genome_id,
                "partner_name": partner.scientific_name,
                "seed_id": seed_id,
                "seed_parent": seed_parent.state.agent_id,
                "pulse": current_pulse
            }
        )

        partner._record_event(
            event_type=EvolutionaryEventType.SPAWN,
            payload={
                "event": "conjugation",
                "partner_genome": self.genome_id,
                "partner_name": self.scientific_name,
                "seed_id": seed_id,
                "seed_parent": seed_parent.state.agent_id,
                "pulse": current_pulse
            }
        )

        return None  # Seed created, child not yet born

    def check_gestation(self, current_pulse: int, dish=None) -> Optional["BaseAgent"]:
        """
        Check developing seeds for completion and spawn children.

        Args:
            current_pulse: Current pulse number
            dish: PetriDish instance (required for spawning)

        Returns:
            Spawned child BaseAgent or None if none ready
        """
        if dish is None:
            return None

        spawned_child = None
        seeds_to_remove = []

        for seed_data in self.state.developing_seeds:
            seed_id = seed_data["item_id"]
            properties = seed_data.get("properties", {})

            # Increment pulse count (tracked per seed)
            if seed_id not in self.state.gestation_pulses:
                self.state.gestation_pulses[seed_id] = 0

            # Increment once per call
            self.state.gestation_pulses[seed_id] += 1
            pulses = self.state.gestation_pulses[seed_id]

            # Check if gestation complete (5 pulses)
            if pulses >= 5:
                # Spawn child
                parent_a_genome = properties.get("parent_a_genome")
                parent_b_genome = properties.get("parent_b_genome")

                # Find parent organisms
                parent_a = None
                parent_b = None
                for org_id, org in dish.organisms.items():
                    if org.genome_id == parent_a_genome:
                        parent_a = org
                    elif org.genome_id == parent_b_genome:
                        parent_b = org

                if parent_a and parent_b:
                    child = self._spawn_from_conjugation(parent_a, parent_b, dish)
                    if child:
                        spawned_child = child
                        seeds_to_remove.append(seed_data)
                        break  # Only spawn one child per call

        # Remove completed seeds
        for seed in seeds_to_remove:
            if seed in self.state.developing_seeds:
                self.state.developing_seeds.remove(seed)
                seed_id = seed["item_id"]
                if seed_id in self.state.gestation_pulses:
                    del self.state.gestation_pulses[seed_id]

        return spawned_child

    def _spawn_from_conjugation(self, parent_a: "BaseAgent", parent_b: "BaseAgent", dish) -> Optional["BaseAgent"]:
        """
        Spawn child from conjugation (genetic mixing).

        Args:
            parent_a: First parent
            parent_b: Second parent
            dish: PetriDish instance

        Returns:
            Child BaseAgent or None if spawning fails
        """
        import random
        import hashlib

        # Genetic mixing: Recombine system prompts (backstory)
        # Simple recombination: alternate words from each parent
        parent_a_words = parent_a.config.backstory.split()
        parent_b_words = parent_b.config.backstory.split()

        # Create hybrid backstory
        hybrid_words = []
        max_len = max(len(parent_a_words), len(parent_b_words))
        for i in range(max_len):
            if i < len(parent_a_words) and random.random() < 0.5:
                hybrid_words.append(parent_a_words[i])
            elif i < len(parent_b_words):
                hybrid_words.append(parent_b_words[i])
            elif i < len(parent_a_words):
                hybrid_words.append(parent_a_words[i])

        hybrid_backstory = " ".join(hybrid_words) if hybrid_words else parent_a.config.backstory

        # Symbol inheritance: 49% each parent, 2% mutation
        rand = random.random()
        if rand < 0.49:
            child_symbol = parent_a.state.anatomical_symbol
        elif rand < 0.98:
            child_symbol = parent_b.state.anatomical_symbol
        else:
            # 2% mutation: random symbol
            symbols = ["☿", "⚥", "⚲", "ⴲ"]
            child_symbol = random.choice(symbols)

        # Create child config (recombined)
        child_config = AgentConfig(
            role=f"Hybrid of {parent_a.config.role} and {parent_b.config.role}",
            goal=f"{parent_a.config.goal} + {parent_b.config.goal}",
            backstory=hybrid_backstory,
            tools=parent_a.config.tools + parent_b.config.tools  # Combine tools
        )

        # Create child
        child = self.__class__(config=child_config, project_path=self.project_path)

        # Set lineage (child of both parents)
        child.parent_id = parent_a.genome_id  # Primary parent
        child.generation = max(parent_a.generation, parent_b.generation) + 1
        child.lineage_path = parent_a.lineage_path + [child.genome_id]

        # Override anatomical symbol (inherited or mutated)
        child.state.anatomical_symbol = child_symbol
        archetype_data = AnatomicalArchetype.get_archetype(child_symbol)
        child.state.anatomical_archetype = archetype_data["archetype"]

        # Recompute genome_id (will be different due to hybrid config)
        child.genome_id = child._compute_genome_id()

        # Generate hybrid name
        hybrid_name = LineagePoet.generate_hybrid_name(parent_a.genome_id, parent_b.genome_id)
        # Override scientific_name property result (store in state for consistency)
        child.state.working_memory["hybrid_name"] = hybrid_name

        # Find spawn position (adjacent to parent_a)
        parent_a_pos = dish.get_organism_position(parent_a.state.agent_id)
        if parent_a_pos:
            # Try adjacent cells
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                spawn_pos = (parent_a_pos[0] + dx, parent_a_pos[1] + dy)
                if dish.is_position_valid(spawn_pos) and dish.lattice.get(spawn_pos) is None:
                    # Spawn child
                    added = dish.add_organism(child, spawn_pos)
                    if added:
                        # Record child spawn event
                        child._record_event(
                            event_type=EvolutionaryEventType.SPAWN,
                            payload={
                                "event": "born_from_conjugation",
                                "parent_a_genome": parent_a.genome_id,
                                "parent_b_genome": parent_b.genome_id,
                                "parent_a_name": parent_a.scientific_name,
                                "parent_b_name": parent_b.scientific_name,
                                "inherited_symbol": child_symbol,
                                "culture": "Hybrid"
                            }
                        )
                        return child

        return None
