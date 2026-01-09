"""
Science module for Waft's Evolutionary Code Laboratory.

The Observer: Scientific Registry for tracking agent evolution.
LineagePoet: Generates deterministic scientific names for organisms.
TamPsyche: Psychological state system for Fai Wei Tam (Davey).
TamNotebook: Research notebook with dual-mode logging.
LabEntryGenerator: Formal lab entry generator.
"""

from .observer import TheObserver
from .taxonomy import LineagePoet
from .report import ManifestoGenerator, ObsidianGenerator
from .tam_psyche import TamPsyche
from .notebook import TamNotebook
from .lab_entry import LabEntryGenerator

__all__ = [
    "TheObserver",
    "LineagePoet",
    "ManifestoGenerator",
    "ObsidianGenerator",
    "TamPsyche",
    "TamNotebook",
    "LabEntryGenerator",
]
