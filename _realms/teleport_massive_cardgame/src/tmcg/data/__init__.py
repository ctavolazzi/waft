"""
Data module for Teleport Massive Card Game.

Contains card data, starter decks, and data loading utilities.
"""

from .starter_decks import (
    STARTER_DECKS,
    get_starter_deck,
    list_starter_decks,
    create_quantum_control_deck,
    create_the_vibration_deck,
)

__all__ = [
    "STARTER_DECKS",
    "get_starter_deck", 
    "list_starter_decks",
    "create_quantum_control_deck",
    "create_the_vibration_deck",
]
