"""
PetriDish: The local spatial environment for DigitalOrganisms.

Implements a 2D coordinate grid (lattice) where organisms occupy cells.
Provides spatial organization and neighborhood queries.
"""

from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from pathlib import Path

# DigitalOrganism is BaseAgent
from ..agent.base import BaseAgent
from ..agent.items import Item


@dataclass
class Cell:
    """A cell in the PetriDish lattice."""
    position: Tuple[int, int]
    organism_id: Optional[str] = None
    occupied: bool = False


class PetriDish:
    """
    The local spatial environment for DigitalOrganisms.
    
    Maintains a 2D coordinate grid (lattice) where organisms occupy cells.
    Provides spatial organization and neighborhood queries for organism interaction.
    """
    
    def __init__(self, dish_id: str, biome_id: str, width: int = 100, height: int = 100):
        """
        Initialize PetriDish.
        
        Args:
            dish_id: Unique identifier for this dish
            biome_id: Identifier of parent Biome
            width: Lattice width (default: 100)
            height: Lattice height (default: 100)
        """
        self.dish_id = dish_id
        self.biome_id = biome_id
        self.width = width
        self.height = height
        
        # Organisms indexed by organism_id
        self.organisms: Dict[str, BaseAgent] = {}
        
        # Lattice: (x, y) -> organism_id (or None if empty)
        self.lattice: Dict[Tuple[int, int], Optional[str]] = {}
        
        # Items: (x, y) -> List[Item] (items can exist in cells)
        self.items: Dict[Tuple[int, int], List[Item]] = {}
        
        # Initialize empty lattice
        for x in range(width):
            for y in range(height):
                self.lattice[(x, y)] = None
    
    def add_item(self, item: Item, position: Tuple[int, int]) -> bool:
        """
        Add item to PetriDish at specified position.
        
        Args:
            item: Item to add
            position: (x, y) coordinates in lattice
            
        Returns:
            True if added successfully, False if position invalid
        """
        x, y = position
        
        # Validate position
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        # Add item
        if position not in self.items:
            self.items[position] = []
        self.items[position].append(item)
        
        return True
    
    def get_items_at(self, position: Tuple[int, int]) -> List[Item]:
        """
        Get items at specified position.
        
        Args:
            position: (x, y) coordinates
            
        Returns:
            List of items at position (empty list if none)
        """
        return self.items.get(position, [])
    
    def add_organism(self, organism: BaseAgent, position: Tuple[int, int]) -> bool:
        """
        Add organism to PetriDish at specified position.
        
        Args:
            organism: DigitalOrganism (BaseAgent instance)
            position: (x, y) coordinates in lattice
            
        Returns:
            True if added successfully, False if position occupied
        """
        x, y = position
        
        # Validate position
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        # Check if position is occupied
        if self.lattice[position] is not None:
            return False
        
        # Add organism
        organism_id = organism.state.agent_id
        self.organisms[organism_id] = organism
        self.lattice[position] = organism_id
        
        return True
    
    def remove_organism(self, organism_id: str) -> bool:
        """
        Remove organism from PetriDish.
        
        Args:
            organism_id: Identifier of organism to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        if organism_id not in self.organisms:
            return False
        
        # Find and clear position in lattice
        for position, oid in self.lattice.items():
            if oid == organism_id:
                self.lattice[position] = None
                break
        
        # Remove from organisms dict
        del self.organisms[organism_id]
        
        return True
    
    def get_organism_position(self, organism_id: str) -> Optional[Tuple[int, int]]:
        """
        Get position of organism in lattice.
        
        Args:
            organism_id: Identifier of organism
            
        Returns:
            (x, y) position or None if not found
        """
        for position, oid in self.lattice.items():
            if oid == organism_id:
                return position
        return None
    
    def get_neighborhood(
        self, 
        position: Tuple[int, int], 
        radius: int = 1
    ) -> List[Tuple[int, int, Optional[str]]]:
        """
        Get neighborhood around position (Moore neighborhood).
        
        Args:
            position: (x, y) center position
            radius: Neighborhood radius (default: 1, gives 8 neighbors)
            
        Returns:
            List of (x, y, organism_id) tuples for neighboring cells
        """
        x, y = position
        neighborhood = []
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue  # Skip center cell
                
                nx, ny = x + dx, y + dy
                
                # Check bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    organism_id = self.lattice.get((nx, ny))
                    neighborhood.append((nx, ny, organism_id))
        
        return neighborhood
    
    def get_empty_cell(self) -> Optional[Tuple[int, int]]:
        """
        Find an empty cell in the lattice.
        
        Returns:
            (x, y) position of empty cell or None if full
        """
        for position, organism_id in self.lattice.items():
            if organism_id is None:
                return position
        return None
    
    def get_organism_count(self) -> int:
        """Get count of organisms in dish."""
        return len(self.organisms)
    
    def is_position_valid(self, position: Tuple[int, int]) -> bool:
        """Check if position is within lattice bounds."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
