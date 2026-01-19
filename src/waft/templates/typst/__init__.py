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
