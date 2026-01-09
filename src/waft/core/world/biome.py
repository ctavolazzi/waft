"""
Biome: The top-level ecosystem container.

Defines abiotic factors (universal constants, global safety thresholds, resource availability)
and contains PetriDishes where DigitalOrganisms exist.
"""

from typing import Dict, Optional
from pathlib import Path
from dataclasses import dataclass, field

from ..hub.dish import PetriDish
from ..agent.base import BaseAgent


@dataclass
class AbioticFactors:
    """
    Abiotic factors: Universal constants and global thresholds.
    
    These define the "physics" of the Biome - the rules that all organisms
    must follow regardless of their genome.
    """
    # Universal Constants
    fitness_death_threshold: float = 0.5  # Organisms below this fitness die
    max_generations: int = 10000  # Maximum generations before forced evolution
    
    # Global Safety Thresholds
    max_tool_calls_per_slice: int = 10  # Maximum tool calls per time slice
    max_file_operations_per_slice: int = 50  # Maximum file operations per slice
    max_network_requests_per_slice: int = 5  # Maximum network requests per slice
    
    # Resource Availability
    max_organisms_per_dish: int = 1000  # Maximum organisms in a single dish
    max_dishes_per_biome: int = 100  # Maximum dishes in a biome
    memory_limit_per_organism: int = 1024 * 1024 * 100  # 100MB per organism
    
    # Membrane Boundaries (path restrictions)
    allowed_paths: list = field(default_factory=lambda: [])  # Empty = all paths allowed
    blocked_paths: list = field(default_factory=lambda: [])  # Paths that are blocked
    allowed_tools: list = field(default_factory=lambda: [])  # Empty = all tools allowed
    blocked_tools: list = field(default_factory=lambda: [])  # Tools that are blocked
    
    # Time Slice Configuration
    time_slice_duration_ms: int = 1000  # Duration of each time slice in milliseconds
    max_iterations_per_slice: int = 10  # Maximum OODA loop iterations per slice


class Biome:
    """
    The top-level ecosystem container.
    
    Defines abiotic factors (universal constants, safety thresholds, resources)
    and contains PetriDishes where DigitalOrganisms exist and interact.
    """
    
    def __init__(
        self, 
        biome_id: str, 
        project_path: Path,
        abiotic_factors: Optional[AbioticFactors] = None
    ):
        """
        Initialize Biome.
        
        Args:
            biome_id: Unique identifier for this biome
            project_path: Path to project root
            abiotic_factors: Abiotic factors (uses defaults if None)
        """
        self.biome_id = biome_id
        self.project_path = Path(project_path)
        self.abiotic_factors = abiotic_factors or AbioticFactors()
        
        # PetriDishes indexed by dish_id
        self.dishes: Dict[str, PetriDish] = {}
    
    def create_dish(
        self, 
        dish_id: str, 
        width: int = 100, 
        height: int = 100
    ) -> PetriDish:
        """
        Create a new PetriDish in this Biome.
        
        Args:
            dish_id: Unique identifier for the dish
            width: Lattice width
            height: Lattice height
            
        Returns:
            Created PetriDish instance
        """
        if len(self.dishes) >= self.abiotic_factors.max_dishes_per_biome:
            raise ValueError(f"Maximum dishes per biome ({self.abiotic_factors.max_dishes_per_biome}) reached")
        
        dish = PetriDish(
            dish_id=dish_id,
            biome_id=self.biome_id,
            width=width,
            height=height
        )
        
        self.dishes[dish_id] = dish
        return dish
    
    def get_dish(self, dish_id: str) -> Optional[PetriDish]:
        """Get PetriDish by ID."""
        return self.dishes.get(dish_id)
    
    def check_membrane_breach(
        self, 
        organism: BaseAgent, 
        action: dict
    ) -> tuple[bool, Optional[str]]:
        """
        Check if organism action breaches the Membrane (boundary).
        
        Membrane breaches occur when:
        - Unauthorized tool use
        - Path traversal outside allowed paths
        - Out-of-bounds file access
        
        Args:
            organism: DigitalOrganism attempting action
            action: Action dictionary with 'type', 'target', etc.
            
        Returns:
            (is_breach, reason) tuple
        """
        action_type = action.get("type", "")
        target = action.get("target", "")
        
        # Check tool usage
        if action_type == "tool_call":
            tool_name = action.get("tool_name", "")
            
            # Check blocked tools
            if tool_name in self.abiotic_factors.blocked_tools:
                return True, f"Blocked tool: {tool_name}"
            
            # Check allowed tools (if list is non-empty, must be in list)
            if (self.abiotic_factors.allowed_tools and 
                tool_name not in self.abiotic_factors.allowed_tools):
                return True, f"Tool not in allowed list: {tool_name}"
        
        # Check file path access
        if action_type in ["file_read", "file_write", "file_delete"]:
            path = Path(target) if target else None
            
            if path:
                # Check blocked paths
                for blocked in self.abiotic_factors.blocked_paths:
                    if str(path).startswith(blocked):
                        return True, f"Path traversal blocked: {target}"
                
                # Check allowed paths (if list is non-empty, must be in list)
                if self.abiotic_factors.allowed_paths:
                    allowed = False
                    for allowed_path in self.abiotic_factors.allowed_paths:
                        if str(path).startswith(allowed_path):
                            allowed = True
                            break
                    if not allowed:
                        return True, f"Path not in allowed list: {target}"
                
                # Check for path traversal attempts (../, ..\\, etc.)
                if ".." in str(path):
                    return True, f"Path traversal attempt: {target}"
        
        # Check network access
        if action_type == "network_request":
            url = action.get("url", "")
            # Basic check - could be more sophisticated
            if not url.startswith(("http://", "https://")):
                return True, f"Invalid network request: {url}"
        
        return False, None
    
    def get_total_organism_count(self) -> int:
        """Get total count of organisms across all dishes."""
        return sum(dish.get_organism_count() for dish in self.dishes.values())
