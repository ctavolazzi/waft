"""
Waft - Ambient, self-modifying Meta-Framework for Python

The "Operating System" for projects, orchestrating:
- Environment (uv)
- Memory (_pyrite)
- Agents (crewai)
"""

__version__ = "0.5.2"
__author__ = "Waft Team"

# Core orchestration
from waft.core.orchestrator import SystemOrchestrator

# Core systems
from waft.being import Being, BeingSystem
from waft.karma import KarmaMerchant
from waft.source_consciousness import SourceConsciousness
from waft.reality import Reality, RealitySystem

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
]

