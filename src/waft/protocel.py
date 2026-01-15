"""
ProtoCel: Self-Contained Evolving Cell

A ProtoCel is a self-contained cell that:
- Lives in its own folder
- Has its own API
- Can peer outside itself to observe/interact with beings
- Evolves itself based on usage patterns
- Is encapsulated but can communicate via its API
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json
import hashlib
import uuid


class ProtoCelState(Enum):
    """State of a ProtoCel."""
    CREATING = "creating"  # ProtoCel being created
    ACTIVE = "active"  # ProtoCel is active and observing
    EVOLVING = "evolving"  # ProtoCel is evolving
    SLEEPING = "sleeping"  # ProtoCel is sleeping
    ARCHIVED = "archived"  # ProtoCel is archived


class ProtoCel:
    """
    A ProtoCel - a self-contained evolving cell.
    
    ProtoCels have:
    - Own folder structure
    - Own API endpoints
    - Ability to observe beings
    - Ability to interact with beings
    - Evolution based on usage patterns
    """
    
    def __init__(
        self,
        protocel_id: str,
        project_path: Path,
        name: Optional[str] = None,
        description: Optional[str] = None,
        initial_patterns: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a ProtoCel.
        
        Args:
            protocel_id: Unique identifier for this ProtoCel
            project_path: Path to project root
            name: Optional name for the ProtoCel
            description: Optional description
            initial_patterns: Optional initial usage patterns
        """
        self.protocel_id = protocel_id
        self.project_path = Path(project_path)
        self.name = name or f"ProtoCel_{protocel_id[:8]}"
        self.description = description or "Self-contained evolving cell"
        self.created_at = datetime.now()
        self.state = ProtoCelState.CREATING
        
        # ProtoCel folder structure
        self.cell_path = self.project_path / "_hidden" / ".truth" / "protocels" / protocel_id
        self.cell_path.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories
        self.api_path = self.cell_path / "api"
        self.api_path.mkdir(exist_ok=True)
        self.observations_path = self.cell_path / "observations"
        self.observations_path.mkdir(exist_ok=True)
        self.evolution_path = self.cell_path / "evolution"
        self.evolution_path.mkdir(exist_ok=True)
        self.state_path = self.cell_path / "state.json"
        
        # Usage patterns for evolution
        self.usage_patterns = initial_patterns or {
            "being_observations": 0,
            "being_interactions": 0,
            "api_calls": 0,
            "evolution_triggers": 0,
            "patterns": {}
        }
        
        # Evolution state
        self.generation = 0
        self.fitness = 0.0
        self.mutations = []
        
        # Being interaction state
        self.observed_beings: List[str] = []
        self.interacted_beings: List[str] = []
        
        # Initialize state
        self._save_state()
        self.state = ProtoCelState.ACTIVE
    
    def _save_state(self) -> None:
        """Save ProtoCel state to disk."""
        state = {
            "protocel_id": self.protocel_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "state": self.state.value,
            "generation": self.generation,
            "fitness": self.fitness,
            "usage_patterns": self.usage_patterns,
            "observed_beings": self.observed_beings,
            "interacted_beings": self.interacted_beings,
            "mutations": self.mutations
        }
        
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def observe_being(self, being_id: str, being_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Observe a being from outside the cell.
        
        Args:
            being_id: ID of the being to observe
            being_data: Optional being data (if not provided, will fetch)
            
        Returns:
            Observation result
        """
        if being_id not in self.observed_beings:
            self.observed_beings.append(being_id)
        
        # Record observation
        observation = {
            "being_id": being_id,
            "timestamp": datetime.now().isoformat(),
            "being_data": being_data,
            "observation_type": "being_observation"
        }
        
        # Save observation
        obs_file = self.observations_path / f"obs_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{being_id[:8]}.json"
        with open(obs_file, 'w') as f:
            json.dump(observation, f, indent=2)
        
        # Update usage patterns
        self.usage_patterns["being_observations"] += 1
        if being_id not in self.usage_patterns["patterns"]:
            self.usage_patterns["patterns"][being_id] = {"observations": 0, "interactions": 0}
        self.usage_patterns["patterns"][being_id]["observations"] += 1
        
        self._save_state()
        self._check_evolution()
        
        return {
            "status": "observed",
            "being_id": being_id,
            "observation_file": str(obs_file)
        }
    
    def interact_with_being(self, being_id: str, interaction_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Interact with a being from outside the cell.
        
        Args:
            being_id: ID of the being to interact with
            interaction_type: Type of interaction
            data: Optional interaction data
            
        Returns:
            Interaction result
        """
        if being_id not in self.interacted_beings:
            self.interacted_beings.append(being_id)
        
        # Record interaction
        interaction = {
            "being_id": being_id,
            "interaction_type": interaction_type,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        # Save interaction
        int_file = self.observations_path / f"int_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{being_id[:8]}.json"
        with open(int_file, 'w') as f:
            json.dump(interaction, f, indent=2)
        
        # Update usage patterns
        self.usage_patterns["being_interactions"] += 1
        if being_id not in self.usage_patterns["patterns"]:
            self.usage_patterns["patterns"][being_id] = {"observations": 0, "interactions": 0}
        self.usage_patterns["patterns"][being_id]["interactions"] += 1
        
        self._save_state()
        self._check_evolution()
        
        return {
            "status": "interacted",
            "being_id": being_id,
            "interaction_type": interaction_type,
            "interaction_file": str(int_file)
        }
    
    def _check_evolution(self) -> None:
        """Check if ProtoCel should evolve based on usage patterns."""
        # Evolution triggers based on usage
        total_usage = (
            self.usage_patterns["being_observations"] +
            self.usage_patterns["being_interactions"] +
            self.usage_patterns["api_calls"]
        )
        
        # Evolve every 10 interactions
        if total_usage > 0 and total_usage % 10 == 0:
            self.usage_patterns["evolution_triggers"] += 1
            self.evolve()
    
    def evolve(self) -> Dict[str, Any]:
        """
        Evolve the ProtoCel based on usage patterns.
        
        Returns:
            Evolution result
        """
        if self.state == ProtoCelState.EVOLVING:
            return {"status": "already_evolving"}
        
        self.state = ProtoCelState.EVOLVING
        
        # Calculate fitness based on usage patterns
        self.fitness = self._calculate_fitness()
        
        # Generate mutation
        mutation = self._generate_mutation()
        self.mutations.append(mutation)
        self.generation += 1
        
        # Save evolution record
        evolution_record = {
            "generation": self.generation,
            "timestamp": datetime.now().isoformat(),
            "fitness": self.fitness,
            "mutation": mutation,
            "usage_patterns": self.usage_patterns.copy()
        }
        
        evo_file = self.evolution_path / f"evo_gen{self.generation}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(evo_file, 'w') as f:
            json.dump(evolution_record, f, indent=2)
        
        self.state = ProtoCelState.ACTIVE
        self._save_state()
        
        return {
            "status": "evolved",
            "generation": self.generation,
            "fitness": self.fitness,
            "mutation": mutation,
            "evolution_file": str(evo_file)
        }
    
    def _calculate_fitness(self) -> float:
        """Calculate fitness based on usage patterns."""
        # Fitness based on diversity and activity
        being_diversity = len(set(self.observed_beings + self.interacted_beings))
        total_activity = (
            self.usage_patterns["being_observations"] +
            self.usage_patterns["being_interactions"] +
            self.usage_patterns["api_calls"]
        )
        
        # Normalize fitness (0-1 scale)
        diversity_score = min(being_diversity / 10.0, 1.0)  # Max at 10 unique beings
        activity_score = min(total_activity / 100.0, 1.0)  # Max at 100 activities
        
        fitness = (diversity_score * 0.4) + (activity_score * 0.6)
        return round(fitness, 3)
    
    def _generate_mutation(self) -> Dict[str, Any]:
        """Generate a mutation based on usage patterns."""
        # Analyze patterns to determine mutation type
        most_observed = max(
            self.usage_patterns["patterns"].items(),
            key=lambda x: x[1]["observations"],
            default=(None, {})
        )
        
        mutation_type = "pattern_enhancement" if most_observed[0] else "general_improvement"
        
        mutation = {
            "type": mutation_type,
            "timestamp": datetime.now().isoformat(),
            "focus": most_observed[0] if most_observed[0] else "general",
            "changes": {
                "observation_efficiency": 1.1,  # 10% improvement
                "interaction_speed": 1.05  # 5% improvement
            }
        }
        
        return mutation
    
    def get_state(self) -> Dict[str, Any]:
        """Get current ProtoCel state."""
        return {
            "protocel_id": self.protocel_id,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "generation": self.generation,
            "fitness": self.fitness,
            "usage_patterns": self.usage_patterns,
            "observed_beings_count": len(self.observed_beings),
            "interacted_beings_count": len(self.interacted_beings),
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def load(cls, protocel_id: str, project_path: Path) -> "ProtoCel":
        """Load a ProtoCel from disk."""
        cell_path = project_path / "_hidden" / ".truth" / "protocels" / protocel_id
        state_path = cell_path / "state.json"
        
        if not state_path.exists():
            raise ValueError(f"ProtoCel {protocel_id} not found")
        
        with open(state_path, 'r') as f:
            state = json.load(f)
        
        protocel = cls(
            protocel_id=state["protocel_id"],
            project_path=project_path,
            name=state.get("name"),
            description=state.get("description"),
            initial_patterns=state.get("usage_patterns", {})
        )
        
        protocel.created_at = datetime.fromisoformat(state["created_at"])
        protocel.state = ProtoCelState(state["state"])
        protocel.generation = state.get("generation", 0)
        protocel.fitness = state.get("fitness", 0.0)
        protocel.observed_beings = state.get("observed_beings", [])
        protocel.interacted_beings = state.get("interacted_beings", [])
        protocel.mutations = state.get("mutations", [])
        
        return protocel


class ProtoCelSystem:
    """
    System for managing ProtoCels.
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize the ProtoCel System.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.protocels_path = self.project_path / "_hidden" / ".truth" / "protocels"
        self.protocels_path.mkdir(parents=True, exist_ok=True)
    
    def create_protocel(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> ProtoCel:
        """
        Create a new ProtoCel.
        
        Args:
            name: Optional name for the ProtoCel
            description: Optional description
            
        Returns:
            Created ProtoCel
        """
        protocel_id = f"protocel_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        protocel = ProtoCel(
            protocel_id=protocel_id,
            project_path=self.project_path,
            name=name,
            description=description
        )
        
        return protocel
    
    def list_protocels(self) -> List[str]:
        """List all ProtoCel IDs."""
        if not self.protocels_path.exists():
            return []
        
        protocels = []
        for item in self.protocels_path.iterdir():
            if item.is_dir() and (item / "state.json").exists():
                protocels.append(item.name)
        
        return protocels
    
    def get_protocel(self, protocel_id: str) -> ProtoCel:
        """Get a ProtoCel by ID."""
        return ProtoCel.load(protocel_id, self.project_path)
