"""
User Feedback System

Captures and learns from user feedback to guide evolution.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class FeedbackEntry:
    """A single piece of user feedback."""

    timestamp: datetime
    component_id: str | None = None  # Specific component feedback
    document_id: str | None = None  # Overall document feedback
    feedback_type: str = "general"  # "like", "dislike", "suggestion", "correction"
    message: str | None = None
    strength: float = 1.0  # 0.0-1.0, how strong the feedback is
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "component_id": self.component_id,
            "document_id": self.document_id,
            "feedback_type": self.feedback_type,
            "message": self.message,
            "strength": self.strength,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FeedbackEntry":
        """Deserialize from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            component_id=data.get("component_id"),
            document_id=data.get("document_id"),
            feedback_type=data.get("feedback_type", "general"),
            message=data.get("message"),
            strength=data.get("strength", 1.0),
            metadata=data.get("metadata", {}),
        )


class UserFeedbackCollector:
    """
    Collects and processes user feedback.

    Integrates with evolution engine to guide component development.
    """

    def __init__(self, feedback_dir: Path | None = None):
        """
        Initialize feedback collector.

        Args:
            feedback_dir: Directory for storing feedback
        """
        if feedback_dir is None:
            feedback_dir = Path("_genetics/user_feedback")
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

        self.feedback_history: list[FeedbackEntry] = []
        self._load_feedback()

    def _load_feedback(self):
        """Load feedback history from disk."""
        feedback_file = self.feedback_dir / "feedback.json"
        if feedback_file.exists():
            try:
                with open(feedback_file) as f:
                    data = json.load(f)
                    self.feedback_history = [
                        FeedbackEntry.from_dict(entry) for entry in data.get("feedback", [])
                    ]
                print(f"Loaded {len(self.feedback_history)} feedback entries")
            except Exception as e:
                print(f"Warning: Failed to load feedback: {e}")

    def _save_feedback(self):
        """Save feedback to disk."""
        feedback_file = self.feedback_dir / "feedback.json"
        data = {
            "feedback": [entry.to_dict() for entry in self.feedback_history],
            "last_updated": datetime.utcnow().isoformat(),
        }
        with open(feedback_file, "w") as f:
            json.dump(data, f, indent=2)

    def record_feedback(
        self,
        liked: bool,
        component_id: str | None = None,
        document_id: str | None = None,
        message: str | None = None,
        strength: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Record user feedback.

        Args:
            liked: True if liked, False if disliked
            component_id: Specific component that was liked/disliked
            document_id: Overall document ID
            message: Optional feedback message
            strength: How strong the feedback is (0.0-1.0)
            metadata: Additional metadata
        """
        entry = FeedbackEntry(
            timestamp=datetime.utcnow(),
            component_id=component_id,
            document_id=document_id,
            feedback_type="like" if liked else "dislike",
            message=message,
            strength=strength,
            metadata=metadata or {},
        )

        self.feedback_history.append(entry)
        self._save_feedback()

        return entry

    def record_suggestion(
        self,
        message: str,
        component_id: str | None = None,
        document_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Record a suggestion or correction."""
        entry = FeedbackEntry(
            timestamp=datetime.utcnow(),
            component_id=component_id,
            document_id=document_id,
            feedback_type="suggestion",
            message=message,
            strength=0.8,  # Suggestions are moderately strong
            metadata=metadata or {},
        )

        self.feedback_history.append(entry)
        self._save_feedback()

        return entry

    def get_recent_feedback(
        self,
        limit: int = 10,
        component_id: str | None = None,
    ) -> list[FeedbackEntry]:
        """Get recent feedback entries."""
        entries = self.feedback_history

        if component_id:
            entries = [e for e in entries if e.component_id == component_id]

        # Sort by timestamp (newest first)
        entries.sort(key=lambda e: e.timestamp, reverse=True)

        return entries[:limit]

    def get_feedback_summary(self) -> dict[str, Any]:
        """Get summary of feedback patterns."""
        if not self.feedback_history:
            return {"total": 0}

        likes = sum(1 for e in self.feedback_history if e.feedback_type == "like")
        dislikes = sum(1 for e in self.feedback_history if e.feedback_type == "dislike")
        suggestions = sum(1 for e in self.feedback_history if e.feedback_type == "suggestion")

        # Component-level feedback
        component_feedback: dict[str, dict[str, int]] = {}
        for entry in self.feedback_history:
            if entry.component_id:
                if entry.component_id not in component_feedback:
                    component_feedback[entry.component_id] = {"likes": 0, "dislikes": 0}
                if entry.feedback_type == "like":
                    component_feedback[entry.component_id]["likes"] += 1
                elif entry.feedback_type == "dislike":
                    component_feedback[entry.component_id]["dislikes"] += 1

        return {
            "total": len(self.feedback_history),
            "likes": likes,
            "dislikes": dislikes,
            "suggestions": suggestions,
            "component_feedback": component_feedback,
            "recent_count": len(self.get_recent_feedback(limit=10)),
        }
