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
from .chat_distiller import ChatDistiller, DistilledChat, IdeaGene
from .two_page_generator import TwoPageGenerator as TwoPageGeneratorV1
from .two_page_generator_v2 import TwoPageGeneratorV2
from .pdf_image_converter import (
    pdf_to_pngs,
    pngs_to_pdf,
    convert_pdf_to_images,
    convert_images_to_pdf,
)

# V2 is the default (evolved with TRUE constraint enforcement)
# V1 is kept for backward compatibility
TwoPageGenerator = TwoPageGeneratorV2

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
    "ChatDistiller",
    "DistilledChat",
    "IdeaGene",
    "TwoPageGenerator",  # Default: V2 (evolved)
    "TwoPageGeneratorV1",  # Legacy version
    "TwoPageGeneratorV2",  # Explicit V2 access
    "pdf_to_pngs",
    "pngs_to_pdf",
    "convert_pdf_to_images",
    "convert_images_to_pdf",
]
