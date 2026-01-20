"""
Typst Template Library
======================

Typst template library for generating PDFs from Typst templates.
Auto-discovers wrapper modules and provides unified access.
"""

from pathlib import Path
from .compiler import TypstCompiler
from .registry import TypstTemplateRegistry, get_typst_registry, TypstTemplateMetadata

__all__ = [
    "TypstCompiler",
    "TypstTemplateRegistry",
    "get_typst_registry",
    "TypstTemplateMetadata",
]

# Export worldbuilding functions
from .wrappers.worldbuild_iso import generate_worldbuild_iso, generate_worldbuild_with_symbols
from .wrappers.worldbuild_yagenda import (
    generate_worldbuild_agenda,
    generate_worldbuild_event_schedule,
    generate_worldbuild_council_meeting
)
from .wrappers.worldbuild_quill import (
    generate_worldbuild_quantum_circuit,
    generate_worldbuild_magical_circuit,
    generate_worldbuild_tequila_circuit
)

# Export poker visualization functions
from .wrappers.deckz_poker import generate_deckz_poker, Player

__all__.extend([
    "TypstCompiler",
    "TypstTemplateRegistry",
    "get_typst_registry",
    "TypstTemplateMetadata",
    "generate_worldbuild_iso",
    "generate_worldbuild_with_symbols",
    "generate_worldbuild_agenda",
    "generate_worldbuild_event_schedule",
    "generate_worldbuild_council_meeting",
    "generate_worldbuild_quantum_circuit",
    "generate_worldbuild_magical_circuit",
    "generate_worldbuild_tequila_circuit",
    "generate_deckz_poker",
    "Player",
])
