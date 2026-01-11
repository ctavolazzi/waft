"""
WAFT Evolution System: Styling Genome and Scint Detection.

This module implements evolutionary tracking for document styling,
treating design elements (fonts, margins, colors, layouts) as genes
that evolve and improve over time.
"""

from .styling_genome import (
    StylingGenome,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
    StylingGenomeRegistry,
)
from .scint_detector import ScintDetector, Scint, ScintType

__all__ = [
    "StylingGenome",
    "StylingGene",
    "FontGene",
    "MarginGene",
    "ColorGene",
    "LayoutGene",
    "StylingGenomeRegistry",
    "ScintDetector",
    "Scint",
    "ScintType",
]
