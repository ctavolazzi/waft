"""
LaTeX Template Library
======================

LaTeX template library for generating PDFs from LaTeX templates.
Auto-discovers wrapper modules and provides unified access.
"""

from pathlib import Path
from .compiler import LaTeXCompiler
from .registry import LaTeXTemplateRegistry, get_latex_registry

__all__ = [
    "LaTeXCompiler",
    "LaTeXTemplateRegistry",
    "get_latex_registry",
]
