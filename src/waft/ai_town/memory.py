"""
Memory system for AI Town agents.

Stores and retrieves conversation memories using embeddings (simplified version).
"""

import hashlib
from datetime import datetime
from typing import Any


class TownMemory:
    """
    Memory system for town agents.

    Stores conversation summaries and provides retrieval based on similarity.
    In a full implementation, this would use vector embeddings.
    """

    def __init__(self):
        self.memories: list[dict[str, Any]] = []
        self.embeddings_cache: dict[str, str] = {}  # text_hash -> embedding (simplified)

    def remember_conversation(
        self,
        agent_id: str,
        conversation_id: str,
        summary: str,
        participants: list[str],
    ):
        """
        Remember a conversation.

        Args:
            agent_id: ID of agent remembering
            conversation_id: ID of conversation
            summary: Summary of conversation
            participants: List of participant IDs
        """
        memory = {
            "agent_id": agent_id,
            "conversation_id": conversation_id,
            "summary": summary,
            "participants": participants,
            "timestamp": datetime.utcnow().isoformat(),
            "embedding_hash": self._hash_text(summary),  # Simplified - would use real embeddings
        }
        self.memories.append(memory)

        # Keep last 100 memories per agent
        agent_memories = [m for m in self.memories if m["agent_id"] == agent_id]
        if len(agent_memories) > 100:
            oldest = min(agent_memories, key=lambda m: m["timestamp"])
            self.memories.remove(oldest)

    def retrieve_memories(
        self, agent_id: str, query: str, top_k: int = 3, about_agent: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Retrieve relevant memories for an agent.

        Args:
            agent_id: ID of agent retrieving memories
            query: Query text (e.g., "What do I think about Alice?")
            top_k: Number of memories to retrieve
            about_agent: Optional agent ID to filter memories about

        Returns:
            List of relevant memories
        """
        # Filter memories for this agent
        agent_memories = [m for m in self.memories if m["agent_id"] == agent_id]

        # Filter by about_agent if specified
        if about_agent:
            agent_memories = [m for m in agent_memories if about_agent in m.get("participants", [])]

        # Simple similarity (would use vector similarity in full implementation)
        query_hash = self._hash_text(query)
        scored_memories = []
        for memory in agent_memories:
            # Simple hash-based similarity (placeholder for real embeddings)
            similarity = self._simple_similarity(query_hash, memory["embedding_hash"])
            scored_memories.append((similarity, memory))

        # Sort by similarity and return top_k
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in scored_memories[:top_k]]

    def _hash_text(self, text: str) -> str:
        """Hash text for simplified embedding (placeholder)."""
        return hashlib.sha256(text.encode()).hexdigest()

    def _simple_similarity(self, hash1: str, hash2: str) -> float:
        """Simple similarity based on hash (placeholder for real embeddings)."""
        # Count matching characters (very simplified)
        matches = sum(c1 == c2 for c1, c2 in zip(hash1, hash2, strict=False))
        return matches / max(len(hash1), len(hash2))

    def get_agent_memories(self, agent_id: str) -> list[dict[str, Any]]:
        """Get all memories for an agent."""
        return [m for m in self.memories if m["agent_id"] == agent_id]
