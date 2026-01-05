"""
Core modules for Waft framework.

- substrate: Environment management (uv)
- memory: Persistent structure (_pyrite)
"""

from .memory import MemoryManager
from .substrate import SubstrateManager

__all__ = ["MemoryManager", "SubstrateManager"]
