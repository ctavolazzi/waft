"""
Core modules for Waft framework.

- substrate: Environment management (uv)
- memory: Persistent structure (_pyrite)
- decision_matrix: Decision-making calculations
- campfire: Storytelling orchestration
- probe: Testing and exploration tool (pokey stick)
"""

from .memory import MemoryManager
from .substrate import SubstrateManager

__all__ = ["MemoryManager", "SubstrateManager"]

# Lazy imports for probe system
def get_probe():
    """Get Probe classes (lazy import)."""
    from .probe import Probe, HTTPProbe, FileSystemProbe, ServiceProbe, ProbeCollector
    return {
        "Probe": Probe,
        "HTTPProbe": HTTPProbe,
        "FileSystemProbe": FileSystemProbe,
        "ServiceProbe": ServiceProbe,
        "ProbeCollector": ProbeCollector,
    }

# Lazy imports for optional components
def get_campfire():
    """Get TheCampfire class (lazy import)."""
    from .campfire import TheCampfire
    return TheCampfire

