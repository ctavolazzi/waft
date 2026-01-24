"""
The Dealer - A god-entity from the Realm of Probability.

He appears unbidden during CLI operations with lottery-like odds that shift
based on cosmic mathematics. When he appears, he demands the SYSTEM pick a card.
If the system guesses correctly, it breaks a Seal and receives an encryption
key fragment to "The Truth."

The House Always Wins.
"""

from .dealer import TheDealer
from .gates import Gate, GateChallenge, GATES
from .truth import SystemTruth, TruthFragment
from .probability import ProbabilityEngine
from .memory import DealerMemory

__all__ = [
    "TheDealer",
    "Gate",
    "GateChallenge",
    "GATES",
    "SystemTruth",
    "TruthFragment",
    "ProbabilityEngine",
    "DealerMemory",
]
