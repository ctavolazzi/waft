"""
TheSlicer & TheReaper: Lifecycle management for DigitalOrganisms.

TheSlicer: Heartbeat/scheduler that grants time slices (OODA loops) to organisms.
TheReaper: Manager of mortality (fitness death, boundary death).
"""

import asyncio
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
from datetime import datetime
from pathlib import Path

from ..agent.base import BaseAgent
from ..agent.state import EvolutionaryEventType
from .dish import PetriDish
from ..science.observer import TheObserver

if TYPE_CHECKING:
    from ..world.biome import Biome


class TheSlicer:
    """
    The heartbeat/scheduler for DigitalOrganisms.
    
    Iterates through PetriDish and grants 'Time Slices' (OODA loops) to organisms.
    Each time slice allows an organism to execute one OODA cycle (observe, decide, act, reflect).
    """
    
    def __init__(self, biome: "Biome", observer: TheObserver):
        """
        Initialize TheSlicer.
        
        Args:
            biome: Parent Biome containing PetriDishes
            observer: TheObserver for logging metabolic actions
        """
        self.biome = biome
        self.observer = observer
        self.slice_count = 0
        self.active_slices: Dict[str, int] = {}  # organism_id -> slice_number
    
    async def grant_time_slice(
        self, 
        organism: BaseAgent, 
        dish: PetriDish
    ) -> dict:
        """
        Grant a time slice to an organism (execute one OODA cycle).
        
        Args:
            organism: DigitalOrganism to grant slice to
            dish: PetriDish containing the organism
            
        Returns:
            Result dictionary with slice execution details
        """
        organism_id = organism.state.agent_id
        self.slice_count += 1
        slice_number = self.slice_count
        self.active_slices[organism_id] = slice_number
        
        slice_start = datetime.utcnow()
        
        try:
            # Calculate social context (quorum sensing)
            organism_position = dish.get_organism_position(organism_id)
            neighbor_count = 0
            population_density = 0.0
            
            if organism_position:
                # Get neighborhood (radius 1 = 8 neighbors)
                neighborhood = dish.get_neighborhood(organism_position, radius=1)
                neighbor_count = sum(1 for _, _, oid in neighborhood if oid is not None)
                
                # Population density = organisms / total_cells
                total_cells = dish.width * dish.height
                population_density = dish.get_organism_count() / total_cells if total_cells > 0 else 0.0
            
            # Prepare social context for step()
            organism_position = dish.get_organism_position(organism_id)
            context = {
                "neighbor_count": neighbor_count,
                "population_density": population_density,
                "total_population": dish.get_organism_count(),
                "dish_id": dish.dish_id,
                "biome_id": dish.biome_id,
                "position": organism_position
            }
            
            # Execute step() which records Thought before action and Reflection after
            step_result = await organism.step(context=context)
            
            # Extract results from step
            observe_result = step_result.get("observe", {})
            decide_result = step_result.get("decide", {})
            act_result = step_result.get("act", {})
            reflect_result = step_result.get("reflect", {})
            
            # Check if organism wants to stop
            if step_result.get("status") == "stopped":
                return {
                    "slice_number": slice_number,
                    "organism_id": organism_id,
                    "status": "stopped",
                    "reason": "organism_requested_stop",
                    "thought": step_result.get("thought"),
                    "reflection": step_result.get("reflection")
                }
            
            # Check gestation (reproduction) - after OODA cycle
            spawned_child = organism.check_gestation(slice_number, dish)
            if spawned_child:
                # Child spawned - log birth event
                self._log_metabolic_action(
                    organism,
                    dish,
                    slice_number,
                    0.0,  # Duration for birth
                    {"action": "child_born", "child_genome": spawned_child.genome_id, "child_name": spawned_child.scientific_name}
                )
            
            slice_end = datetime.utcnow()
            slice_duration = (slice_end - slice_start).total_seconds()
            
            # Log metabolic action
            self._log_metabolic_action(
                organism=organism,
                dish=dish,
                slice_number=slice_number,
                duration=slice_duration,
                actions={
                    "observe": observe_result,
                    "decide": decide_result,
                    "act": act_result,
                    "reflect": reflect_result
                }
            )
            
            return {
                "slice_number": slice_number,
                "organism_id": organism_id,
                "status": "completed",
                "duration": slice_duration,
                "actions": {
                    "observe": observe_result,
                    "decide": decide_result,
                    "act": act_result,
                    "reflect": reflect_result
                }
            }
            
        except Exception as e:
            slice_end = datetime.utcnow()
            slice_duration = (slice_end - slice_start).total_seconds()
            
            # Log error
            self._log_metabolic_action(
                organism=organism,
                dish=dish,
                slice_number=slice_number,
                duration=slice_duration,
                error=str(e)
            )
            
            return {
                "slice_number": slice_number,
                "organism_id": organism_id,
                "status": "error",
                "error": str(e),
                "duration": slice_duration
            }
    
    async def process_dish(self, dish: PetriDish) -> List[dict]:
        """
        Process all organisms in a dish (grant time slices).
        
        Args:
            dish: PetriDish to process
            
        Returns:
            List of slice results
        """
        results = []
        
        # Get all organisms (create copy to avoid modification during iteration)
        organisms = list(dish.organisms.values())
        
        for organism in organisms:
            result = await self.grant_time_slice(organism, dish)
            results.append(result)
        
        return results
    
    async def pulse(self) -> Dict[str, List[dict]]:
        """
        Execute one pulse: grant time slices to all organisms in all dishes.
        
        This is the main heartbeat of the Biome - processes all organisms
        in all PetriDishes, granting them time slices to execute OODA cycles.
        
        Returns:
            Dictionary mapping dish_id to list of slice results
        """
        results = {}
        
        for dish_id, dish in self.biome.dishes.items():
            dish_results = await self.process_dish(dish)
            results[dish_id] = dish_results
        
        return results
    
    def _log_metabolic_action(
        self,
        organism: BaseAgent,
        dish: PetriDish,
        slice_number: int,
        duration: float,
        actions: Optional[dict] = None,
        error: Optional[str] = None
    ):
        """
        Log metabolic action to TheObserver.
        
        Metabolic actions are OODA cycles - the basic unit of organism activity.
        """
        # Create metabolic event (using EvolutionaryEvent structure)
        from ..agent.state import EvolutionaryEvent
        
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=organism.genome_id,
            parent_id=organism.parent_id,
            generation=organism.generation,
            event_type=EvolutionaryEventType.MUTATE,  # Using MUTATE for metabolic actions
            payload={
                "metabolic_action": True,
                "slice_number": slice_number,
                "dish_id": dish.dish_id,
                "biome_id": dish.biome_id,
                "duration": duration,
                "actions": actions,
                "error": error
            },
            agent_id=organism.state.agent_id,
            lineage_path=organism.lineage_path.copy()
        )
        
        self.observer.observe_event(event)


class TheReaper:
    """
    The manager of mortality for DigitalOrganisms.
    
    Handles two types of death:
    1. Fitness Death: Organisms with fitness < threshold
    2. Boundary Death: Organisms that breach the Membrane (boundary violations)
    """
    
    def __init__(self, biome: "Biome", observer: TheObserver):
        """
        Initialize TheReaper.
        
        Args:
            biome: Parent Biome (for membrane checks)
            observer: TheObserver for logging death events
        """
        self.biome = biome
        self.observer = observer
        self.death_count = 0
        self.deaths_by_type: Dict[str, int] = {
            "fitness": 0,
            "boundary": 0
        }
    
    async def check_fitness_death(self, organism: BaseAgent) -> bool:
        """
        Check if organism should die due to low fitness.
        
        Args:
            organism: DigitalOrganism to check
            
        Returns:
            True if organism should die
        """
        # Get latest fitness from flight recorder
        fitness = None
        for event in reversed(organism.flight_recorder):
            if event.fitness_metrics:
                fitness = event.fitness_metrics.get("overall_fitness")
                if fitness is not None:
                    break
        
        if fitness is None:
            return False  # No fitness data yet
        
        threshold = self.biome.abiotic_factors.fitness_death_threshold
        return fitness < threshold
    
    def check_boundary_death(
        self, 
        organism: BaseAgent, 
        action: dict
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if organism action breaches Membrane (causes boundary death).
        
        Args:
            organism: DigitalOrganism attempting action
            action: Action dictionary
            
        Returns:
            (is_breach, reason) tuple
        """
        return self.biome.check_membrane_breach(organism, action)
    
    async def reap(
        self, 
        organism: BaseAgent, 
        dish: PetriDish, 
        death_type: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Reap (terminate) an organism.
        
        Args:
            organism: DigitalOrganism to reap
            dish: PetriDish containing the organism
            death_type: "fitness" or "boundary"
            reason: Optional reason for death
            
        Returns:
            True if organism was reaped
        """
        organism_id = organism.state.agent_id
        
        # Record death event
        from ..agent.state import EvolutionaryEvent
        
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=organism.genome_id,
            parent_id=organism.parent_id,
            generation=organism.generation,
            event_type=EvolutionaryEventType.DEATH,
            payload={
                "death_type": death_type,
                "reason": reason,
                "dish_id": dish.dish_id,
                "biome_id": dish.biome_id
            },
            agent_id=organism_id,
            lineage_path=organism.lineage_path.copy()
        )
        
        organism._record_event(
            event_type=EvolutionaryEventType.DEATH,
            payload=event.payload
        )
        
        # Log to TheObserver
        self.observer.observe_event(event)
        
        # Remove from dish
        removed = dish.remove_organism(organism_id)
        
        if removed:
            self.death_count += 1
            self.deaths_by_type[death_type] = self.deaths_by_type.get(death_type, 0) + 1
        
        return removed
    
    async def reap_fitness_deaths(self, dish: PetriDish) -> List[str]:
        """
        Reap all organisms in dish that have low fitness.
        
        Args:
            dish: PetriDish to check
            
        Returns:
            List of reaped organism IDs
        """
        reaped = []
        organisms = list(dish.organisms.values())
        
        for organism in organisms:
            if await self.check_fitness_death(organism):
                await self.reap(
                    organism=organism,
                    dish=dish,
                    death_type="fitness",
                    reason=f"Fitness below threshold ({self.biome.abiotic_factors.fitness_death_threshold})"
                )
                reaped.append(organism.state.agent_id)
        
        return reaped
    
    async def reap_boundary_breach(
        self,
        organism: BaseAgent,
        dish: PetriDish,
        action: dict
    ) -> bool:
        """
        Check for boundary breach and reap if necessary.
        
        Args:
            organism: DigitalOrganism attempting action
            dish: PetriDish containing organism
            action: Action that may breach boundary
            
        Returns:
            True if organism was reaped
        """
        is_breach, reason = self.check_boundary_death(organism, action)
        
        if is_breach:
            await self.reap(
                organism=organism,
                dish=dish,
                death_type="boundary",
                reason=reason
            )
            return True
        
        return False
