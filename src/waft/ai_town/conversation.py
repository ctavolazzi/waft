"""
Conversation system for AI Town.

Agents can have conversations with each other, with memory and context.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversationMessage:
    """A message in a conversation."""

    agent_id: str
    agent_name: str
    content: str
    timestamp: float
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Conversation:
    """A conversation between agents."""

    conversation_id: str
    participants: list[str]  # Agent IDs
    messages: list[ConversationMessage] = field(default_factory=list)
    started_at: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    ended_at: float | None = None
    summary: str | None = None

    def add_message(self, agent_id: str, agent_name: str, content: str):
        """Add a message to the conversation."""
        message = ConversationMessage(
            agent_id=agent_id,
            agent_name=agent_name,
            content=content,
            timestamp=datetime.utcnow().timestamp(),
        )
        self.messages.append(message)
        return message

    def end(self, summary: str | None = None):
        """End the conversation."""
        self.ended_at = datetime.utcnow().timestamp()
        self.summary = summary

    def is_active(self) -> bool:
        """Check if conversation is still active."""
        return self.ended_at is None

    def get_duration(self) -> float:
        """Get conversation duration in seconds."""
        end = self.ended_at or datetime.utcnow().timestamp()
        return end - self.started_at


class ConversationManager:
    """Manages conversations in the town."""

    def __init__(self):
        self.conversations: dict[str, Conversation] = {}
        self.active_conversations: dict[str, str] = {}  # agent_id -> conversation_id

    def start_conversation(self, agent_ids: list[str], agent_names: dict[str, str]) -> Conversation:
        """Start a new conversation between agents."""
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            conversation_id=conversation_id,
            participants=agent_ids,
        )
        self.conversations[conversation_id] = conversation

        # Mark agents as in conversation
        for agent_id in agent_ids:
            self.active_conversations[agent_id] = conversation_id

        return conversation

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        """Get a conversation by ID."""
        return self.conversations.get(conversation_id)

    def get_agent_conversation(self, agent_id: str) -> Conversation | None:
        """Get the active conversation for an agent."""
        conversation_id = self.active_conversations.get(agent_id)
        if conversation_id:
            return self.conversations.get(conversation_id)
        return None

    def end_conversation(self, conversation_id: str, summary: str | None = None):
        """End a conversation."""
        conversation = self.conversations.get(conversation_id)
        if conversation:
            conversation.end(summary)
            # Remove from active conversations
            for agent_id in list(self.active_conversations.keys()):
                if self.active_conversations[agent_id] == conversation_id:
                    del self.active_conversations[agent_id]

    def add_message(
        self, conversation_id: str, agent_id: str, agent_name: str, content: str
    ) -> ConversationMessage | None:
        """Add a message to a conversation."""
        conversation = self.conversations.get(conversation_id)
        if conversation and conversation.is_active():
            return conversation.add_message(agent_id, agent_name, content)
        return None

    def get_conversation_summary(self, conversation_id: str) -> str:
        """Generate a summary of a conversation."""
        conversation = self.conversations.get(conversation_id)
        if not conversation or not conversation.messages:
            return "Empty conversation"

        # Simple summary - could be enhanced with LLM
        participants = ", ".join([msg.agent_name for msg in conversation.messages[:3]])
        message_count = len(conversation.messages)
        return f"Conversation between {participants} with {message_count} messages"
