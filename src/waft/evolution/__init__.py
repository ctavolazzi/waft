"""
WAFT Evolution System: Styling Genome and Scint Detection.

This module implements evolutionary tracking for document styling,
treating design elements (fonts, margins, colors, layouts) as genes
that evolve and improve over time.
"""

from .chat_distiller import ChatDistiller, DistilledChat, IdeaGene
from .component_evolution import ComponentEvolutionEngine, ComponentTrait, EvolvedComponent
from .component_generator import ComponentPDFGenerator, FoundationComponentGenerator
from .document_evolution_engine import DocumentEvolutionEngine
from .flexible_pdf_generator import FlexiblePDFGenerator
from .latex_generator import LaTeXGenerator, generate_latex
from .pdf_image_converter import (
    PageSize,
    convert_images_to_pdf,
    convert_pdf_to_images,
    pdf_to_pngs,
    pngs_to_pdf,
)
from .pdf_metrics import PDFMetrics, PDFMetricsCollector
from .scint_detector import Scint, ScintDetector, ScintType
from .status_components import (
    StatusComponentBuilder,
    StatusComponentType,
    create_status_components_from_status_dict,
)
from .styling_genome import (
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
)
from .two_page_generator import TwoPageGenerator
from .two_page_generator_legacy import TwoPageGeneratorLegacy
from .user_feedback import FeedbackEntry, UserFeedbackCollector

# New genetic evolution features
from .genetic_crossover import (
    CrossoverResult,
    CrossoverStrategy,
    GeneticCrossover,
    breed,
)
from .battle_royale import (
    BattleAction,
    BattleResult,
    BattleRoyale,
    BattleStats,
    BattleStatus,
    Combatant,
    quick_battle,
)
from .achievements import (
    Achievement,
    AchievementCategory,
    AchievementRarity,
    AchievementTracker,
    UnlockedAchievement,
    ACHIEVEMENTS,
    get_tracker,
    track_event,
)

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
    "FlexiblePDFGenerator",  # Flexible PDF generator (no page constraints)
    "UserFeedbackCollector",  # User feedback collection and learning
    "FeedbackEntry",  # Individual feedback entry
    "pdf_to_pngs",
    "pngs_to_pdf",
    "convert_pdf_to_images",
    "convert_images_to_pdf",
    "PageSize",
    "PDFMetrics",  # Metrics data class
    "PDFMetricsCollector",  # Metrics collector
    "LaTeXGenerator",  # LaTeX document generator
    "generate_latex",  # Quick LaTeX generation function
    "StatusComponentBuilder",  # Builder for status-specific PDF components
    "StatusComponentType",  # Status component type constants
    "create_status_components_from_status_dict",  # Create all status components from status dict
    # Genetic crossover
    "GeneticCrossover",  # Crossover engine for breeding genomes
    "CrossoverStrategy",  # Available crossover strategies
    "CrossoverResult",  # Result of crossover operation
    "breed",  # Quick function to breed two genomes
    # Battle royale
    "BattleRoyale",  # Arena for agent battles
    "BattleResult",  # Result of a battle
    "BattleStats",  # Combat stats derived from genome
    "BattleAction",  # Available battle actions
    "BattleStatus",  # Battle status enum
    "Combatant",  # Battle participant
    "quick_battle",  # Quick function to run a battle
    # Achievement system
    "Achievement",  # Achievement definition
    "AchievementCategory",  # Achievement categories
    "AchievementRarity",  # Rarity levels
    "AchievementTracker",  # Track and manage achievements
    "UnlockedAchievement",  # Record of unlocked achievement
    "ACHIEVEMENTS",  # All achievement definitions
    "get_tracker",  # Get global achievement tracker
    "track_event",  # Track event for achievements
]

# TwoPageGenerator is the main implementation (adaptive constraint enforcement)
# TwoPageGeneratorLegacy is kept for backward compatibility
