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
from .two_page_generator import TwoPageGenerator
from .two_page_generator_legacy import TwoPageGeneratorLegacy
from .component_generator import ComponentPDFGenerator, FoundationComponentGenerator
from .document_evolution_engine import DocumentEvolutionEngine
from .component_evolution import ComponentEvolutionEngine, EvolvedComponent, ComponentTrait
from .user_feedback import UserFeedbackCollector, FeedbackEntry
from .pdf_image_converter import (
    pdf_to_pngs,
    pngs_to_pdf,
    convert_pdf_to_images,
    convert_images_to_pdf,
    PageSize,
)
from .pdf_metrics import PDFMetrics, PDFMetricsCollector

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
    "TwoPageGenerator",  # Main implementation (adaptive constraint enforcement)
    "TwoPageGeneratorLegacy",  # Legacy version (kept for backward compatibility)
    "ComponentPDFGenerator",  # High-level component-based generator
    "FoundationComponentGenerator",  # WAFT-integrated component generator
    "DocumentEvolutionEngine",  # Evolutionary document creator with learning
    "ComponentEvolutionEngine",  # Component trait evolution system
    "EvolvedComponent",  # Component with evolving traits
    "ComponentTrait",  # Evolving component traits
    "UserFeedbackCollector",  # User feedback collection and learning
    "FeedbackEntry",  # Individual feedback entry
    "pdf_to_pngs",
    "pngs_to_pdf",
    "convert_pdf_to_images",
    "convert_images_to_pdf",
    "PageSize",
    "PDFMetrics",  # Metrics data class
    "PDFMetricsCollector",  # Metrics collector
]

# TwoPageGenerator is the main implementation (adaptive constraint enforcement)
# TwoPageGeneratorLegacy is kept for backward compatibility
