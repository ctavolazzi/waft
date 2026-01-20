"""
D&D 5e Physics Engine for WAFT Beings

This module provides the core algorithms and data structures for D&D 5e mechanics,
serving as the "physics engine" and "biology" for WAFT Being agents.

Modules:
- stats: Core mathematical algorithms (modifiers, AC, proficiency)
- dice: Dice rolling wrapper (uses d20 library)
- character: Character dataclass with state management
- combat: Combat mechanics (attack rolls, saving throws)
- adapter: Adapter pattern for 4-stat to 6-stat conversion
"""

from .adapter import StatsAdapter
from .character import DnD5eCharacter
from .combat import DnD5eCombat
from .dice import DnDRoller
from .stats import ArmorType, DnD5eStats

__all__ = [
    "DnD5eStats",
    "ArmorType",
    "DnDRoller",
    "DnD5eCharacter",
    "DnD5eCombat",
    "StatsAdapter",
]
