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
from .door_guy import Bouncer, BouncerDecision, PortManifest, ShipManifest
from .empirica_brain import BrainCycleResult, EmpiricaBrain
from .empirica_handler import (
    CheckResult,
    EmpericaHandler,
    EmpericaHandlerError,
    GateDecision,
    Phase,
)
from .bot import Bot, BotConfig, Inventory, Journal, Port
from .meme_generator import MemeGenerator, MemeRecipe, MemeRequest, MemeStyle, MemeTemplate

__all__ = [
    "MemoryManager",
    "SubstrateManager",
    "Bouncer",
    "BouncerDecision",
    "PortManifest",
    "ShipManifest",
    "EmpiricaBrain",
    "BrainCycleResult",
    "EmpericaHandler",
    "EmpericaHandlerError",
    "CheckResult",
    "GateDecision",
    "Phase",
    "Bot",
    "BotConfig",
    "Inventory",
    "Journal",
    "Port",
    "MemeGenerator",
    "MemeRequest",
    "MemeStyle",
    "MemeTemplate",
    "MemeRecipe",
]


# Lazy imports for probe system
def get_probe():
    """Get Probe classes (lazy import)."""
    from .probe import FileSystemProbe, HTTPProbe, Probe, ProbeCollector, ServiceProbe

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
