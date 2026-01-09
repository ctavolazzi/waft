"""
Anatomical Archetypes: Linnaean Constraints for DigitalOrganisms.

Defines four anatomical archetypes with different inventory capacities:
- ☿ (The Weaver): Appendage: 1 | Pocket: 3 | Social/Fluid
- ⚥ (The Balanced): Appendage: 2 | Pocket: 2 | Versatile
- ⚲ (The Static): Appendage: 1 | Pocket: 1 | High-Speed/Efficient
- ⴲ (The Foundation): Appendage: 0 | Pocket: 5 | Storage/Protective
"""

from typing import Dict, Tuple
from enum import Enum


class AnatomicalSymbol(str, Enum):
    """Anatomical symbols for Linnaean classification."""
    WEAVER = "☿"  # The Weaver: Social/Fluid
    BALANCED = "⚥"  # The Balanced: Versatile
    STATIC = "⚲"  # The Static: High-Speed/Efficient
    FOUNDATION = "ⴲ"  # The Foundation: Storage/Protective


class AnatomicalArchetype:
    """Anatomical archetype with inventory constraints."""
    
    ARCHETYPES = {
        AnatomicalSymbol.WEAVER: {
            "name": "The Weaver",
            "archetype": "Social/Fluid",
            "appendage_capacity": 1,
            "pocket_capacity": 3,
            "description": "Social organisms with fluid interactions"
        },
        AnatomicalSymbol.BALANCED: {
            "name": "The Balanced",
            "archetype": "Versatile",
            "appendage_capacity": 2,
            "pocket_capacity": 2,
            "description": "Versatile organisms with balanced capabilities"
        },
        AnatomicalSymbol.STATIC: {
            "name": "The Static",
            "archetype": "High-Speed/Efficient",
            "appendage_capacity": 1,
            "pocket_capacity": 1,
            "description": "High-speed organisms optimized for efficiency"
        },
        AnatomicalSymbol.FOUNDATION: {
            "name": "The Foundation",
            "archetype": "Storage/Protective",
            "appendage_capacity": 0,
            "pocket_capacity": 5,
            "description": "Storage-focused organisms with protective capabilities"
        }
    }
    
    @classmethod
    def get_archetype(cls, symbol: str) -> Dict:
        """Get archetype configuration by symbol."""
        return cls.ARCHETYPES.get(symbol, cls.ARCHETYPES[AnatomicalSymbol.WEAVER])
    
    @classmethod
    def get_appendage_capacity(cls, symbol: str) -> int:
        """Get appendage capacity for symbol."""
        return cls.get_archetype(symbol)["appendage_capacity"]
    
    @classmethod
    def get_pocket_capacity(cls, symbol: str) -> int:
        """Get pocket capacity for symbol."""
        return cls.get_archetype(symbol)["pocket_capacity"]
    
    @classmethod
    def assign_symbol(cls, genome_id: str) -> str:
        """
        Assign anatomical symbol deterministically from genome_id.
        
        Uses bytes 4-5 (2 bytes = 4 hex chars) to select symbol.
        
        Args:
            genome_id: SHA-256 hex digest (64 characters)
            
        Returns:
            Anatomical symbol (☿, ⚥, ⚲, ⴲ)
        """
        if len(genome_id) < 64:
            genome_id = genome_id.ljust(64, '0')
        
        # Use bytes 4-5 (hex chars 8-12) for symbol selection
        symbol_bytes = genome_id[8:12]  # 4 hex chars = 2 bytes
        symbol_index = int(symbol_bytes, 16) % 4
        
        symbols = [
            AnatomicalSymbol.WEAVER,
            AnatomicalSymbol.BALANCED,
            AnatomicalSymbol.STATIC,
            AnatomicalSymbol.FOUNDATION
        ]
        
        return symbols[symbol_index].value
