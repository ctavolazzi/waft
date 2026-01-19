"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
"""

__version__ = "0.9.3"
__author__ = "Waft Team"

# Unified PDF class - single entry point for all PDF generation
from .pdf import PDF

__all__ = ["PDF"]

