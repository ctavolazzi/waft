"""
WAFT RAG Module - Integration with rag-chatbot for PDF querying and knowledge retrieval.

This module provides:
- RAGChatbot: Wrapper around rag-chatbot for PDF querying
- RAGAgentMixin: BaseAgent integration for RAG capabilities
- Configuration management for models and vector stores
"""

from .chatbot import RAGChatbot
from .agent_integration import RAGAgentMixin
from .config import RAGConfig

__all__ = [
    "RAGChatbot",
    "RAGAgentMixin",
    "RAGConfig",
]
