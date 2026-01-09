"""
Items: Objects that organisms can interact with in the multiverse.

Items can be held in the Appendage (1 slot) or Pocket (3 slots).
Items can exist in PetriDish lattice cells for foraging.
"""

import hashlib
from typing import Dict, Any
from pydantic import BaseModel, Field


class Item(BaseModel):
    """
    An item that can be held by an organism or placed in the PetriDish.
    
    Items have deterministic IDs based on their properties for consistency.
    """
    item_id: str = Field(description="Deterministic hash identifier")
    name: str = Field(description="Item name (e.g., 'Scint-Shard', 'Void-Stone')")
    weight: int = Field(description="Item weight (affects energy consumption)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Item-specific properties")
    
    @classmethod
    def create(cls, name: str, weight: int = 1, properties: Dict[str, Any] = None) -> "Item":
        """
        Create a new item with deterministic ID.
        
        Args:
            name: Item name
            weight: Item weight
            properties: Optional item properties
            
        Returns:
            Item instance with deterministic item_id
        """
        if properties is None:
            properties = {}
        
        # Generate deterministic ID from name and properties
        item_data = {
            "name": name,
            "weight": weight,
            "properties": properties
        }
        item_json = str(sorted(item_data.items()))
        item_id = hashlib.sha256(item_json.encode()).hexdigest()[:16]
        
        return cls(
            item_id=item_id,
            name=name,
            weight=weight,
            properties=properties
        )
