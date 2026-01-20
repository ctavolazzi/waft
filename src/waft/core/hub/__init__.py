"""
Hub module: Local spatial environments for DigitalOrganisms.

The PetriDish provides a 2D lattice for organism placement and interaction.
"""

from .dish import PetriDish
from .lifecycle import TheReaper, TheSlicer
from .viewer import PetriViewer

__all__ = ["PetriDish", "TheSlicer", "TheReaper", "PetriViewer"]
