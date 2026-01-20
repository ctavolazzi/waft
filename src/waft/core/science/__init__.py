"""
Science module for Waft's Evolutionary Code Laboratory.

The Observer: Scientific Registry for tracking agent evolution.
LineagePoet: Generates deterministic scientific names for organisms.
TamPsyche: Psychological state system for Fai Wei Tam (Davey).
TamNotebook: Research notebook with dual-mode logging.
LabEntryGenerator: Formal lab entry generator.
"""

from .lab_entry import LabEntryGenerator
from .notebook import TamNotebook
from .observer import TheObserver
from .oracle import TheOracle
from .report import ObsidianGenerator, SessionReportGenerator
from .tam_psyche import TamPsyche
from .taxonomy import LineagePoet

__all__ = [
    "TheObserver",
    "TheOracle",
    "LineagePoet",
    "SessionReportGenerator",
    "ObsidianGenerator",
    "TamPsyche",
    "TamNotebook",
    "LabEntryGenerator",
]
