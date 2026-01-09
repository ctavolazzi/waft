"""
Agent module for Waft's Evolutionary Code Laboratory.

The Organism: BaseAgent and related models for agent evolution.
"""

from .state import (
    AgentState,
    AgentConfig,
    Message,
    MessageRole,
    ToolDefinition,
    EvolutionaryEvent,
    EvolutionaryEventType,
    Modification,
)
from .base import BaseAgent
from .items import Item
from .anatomy import AnatomicalArchetype, AnatomicalSymbol

__all__ = [
    "BaseAgent",
    "AgentState",
    "AgentConfig",
    "Message",
    "MessageRole",
    "ToolDefinition",
    "EvolutionaryEvent",
    "EvolutionaryEventType",
    "Modification",
    "Item",
    "AnatomicalArchetype",
    "AnatomicalSymbol",
]
