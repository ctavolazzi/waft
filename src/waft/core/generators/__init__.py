"""
Procedural World Generators
===========================

Fantasy content generators for the AI Storyteller.
Inspired by Donjon, Eigengrau's Generator, and tabletop RPG random tables.

Generators:
- NameGenerator: Fantasy names (characters, taverns, places)
- NPCGenerator: Characters with personalities and secrets
- TavernGenerator: Complete tavern environments
- DungeonGenerator: Five-room dungeon structures
- WorldManager: Orchestrates all generators and maintains state
"""

from .names import NameGenerator
from .npcs import NPCGenerator, NPC
from .tavern import TavernGenerator, Tavern
from .dungeon import DungeonGenerator, Dungeon
from .world import WorldManager

__all__ = [
    "NameGenerator",
    "NPCGenerator",
    "NPC",
    "TavernGenerator",
    "Tavern",
    "DungeonGenerator",
    "Dungeon",
    "WorldManager",
]
