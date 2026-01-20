"""
AI Town: A virtual town where AI characters live, chat, and socialize.

Basic implementation inspired by:
- Generative Agents paper (arXiv:2304.03442)
- ai-town repository (a16z-infra/ai-town)

Built using WAFT's tools and architecture.
"""

from .conversation import Conversation, ConversationManager
from .memory import TownMemory
from .town_agent import TownAgent
from .town_voting import TownVotingSystem, VoteType
from .town_world import TownWorld

__all__ = [
    "TownAgent",
    "TownWorld",
    "Conversation",
    "ConversationManager",
    "TownMemory",
    "TownVotingSystem",
    "VoteType",
]
