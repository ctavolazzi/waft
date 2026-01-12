"""
Core modules for Waft framework.

- substrate: Environment management (uv)
- memory: Persistent structure (_pyrite)
- decision_matrix: Decision-making calculations
- campfire: Storytelling orchestration
"""

from .memory import MemoryManager
from .substrate import SubstrateManager

__all__ = ["MemoryManager", "SubstrateManager"]

# Lazy imports for optional components
def get_campfire():
    """Get TheCampfire class (lazy import)."""
    from .campfire import TheCampfire
    return TheCampfire

