"""
Teleport Massive: Founding Story and Initial Conditions

Creates the Teleport Massive corporation with its 2025 founding story,
founders, and initial economic conditions.
"""

from .founding_story import create_teleport_massive, get_founding_story
from .initial_conditions import get_initial_conditions, InitialConditions

__all__ = [
    "create_teleport_massive",
    "get_founding_story",
    "get_initial_conditions",
    "InitialConditions",
]
