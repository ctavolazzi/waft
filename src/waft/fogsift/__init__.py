"""
FogSift Modular Pet Device - Creature System

Software simulation for the FogSift tamagotchi-style device.
"""

from .creature import FogSiftCreature, LifeStage, Element
from .simulation import run_simulation

__all__ = ["FogSiftCreature", "LifeStage", "Element", "run_simulation"]
