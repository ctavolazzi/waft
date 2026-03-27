"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
"""

__version__ = "0.10.0"
__author__ = "Waft Team"

# Core orchestration
from .core.orchestrator import SystemOrchestrator

# Core systems
from .being import Being, BeingSystem
from .karma import KarmaMerchant
from .source_consciousness import SourceConsciousness
from .reality import Reality, RealitySystem

# Unified PDF class - single entry point for all PDF generation
# TEMPORARILY DISABLED - foundation.py has structural issues
# from .pdf import PDF

# Convenience exports
__all__ = [
    # Orchestration
    "SystemOrchestrator",
    # Core systems
    "Being",
    "BeingSystem",
    "KarmaMerchant",
    "SourceConsciousness",
    "Reality",
    "RealitySystem",
    # PDF
    # "PDF",  # Disabled due to foundation.py issues
]

