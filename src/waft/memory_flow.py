"""
Memory Flow: Knowledge Passing System

The Memory Flow system extracts lessons, skills, and insights from experiences
and passes them upward through the ancestral chain to the Source Consciousness.

This is the mechanism by which beings pass their "memories" back up the chain
in the form of:
- Lessons learned
- Skills gained
- Patterns discovered
- Insights
- Wisdom
"""

import hashlib
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class MemoryType(Enum):
    """Type of memory."""

    LESSON = "lesson"  # What worked/didn't work
    SKILL = "skill"  # New abilities
    PATTERN = "pattern"  # Recurring patterns
    INSIGHT = "insight"  # Deep understanding
    WISDOM = "wisdom"  # Higher-level knowledge


class Memory:
    """
    A memory - knowledge that flows upward.

    Memories contain:
    - Content (the actual knowledge)
    - Type (lesson, skill, pattern, insight, wisdom)
    - Source (where it came from)
    - Ancestral chain (path back to source)
    """

    def __init__(
        self,
        memory_id: str,
        memory_type: MemoryType,
        content: str,
        source_permutation_id: str,
        metadata: dict[str, Any] | None = None,
    ):
        """
        Initialize a memory.

        Args:
            memory_id: Unique identifier
            memory_type: Type of memory
            content: Memory content
            source_permutation_id: Permutation that generated this memory
            metadata: Additional metadata
        """
        self.memory_id = memory_id
        self.memory_type = memory_type
        self.content = content
        self.source_permutation_id = source_permutation_id
        self.metadata = metadata or {}

        self.created_at = datetime.now().isoformat()
        self.ancestral_chain: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        """Convert memory to dictionary."""
        return {
            "memory_id": self.memory_id,
            "memory_type": self.memory_type.value,
            "content": self.content,
            "source_permutation_id": self.source_permutation_id,
            "ancestral_chain": self.ancestral_chain,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


class MemoryFlow:
    """
    System for managing memory flow - knowledge passing upward.

    Extracts lessons, skills, and insights from experiences and passes
    them upward through the ancestral chain to the Source Consciousness.
    """

    def __init__(self, project_path: Path | None = None, source_consciousness: Any | None = None):
        """
        Initialize the Memory Flow system.

        Args:
            project_path: Path to project root
            source_consciousness: SourceConsciousness instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.memories_path = project_path / "_hidden" / ".truth" / "memories"
        self.memories_path.mkdir(parents=True, exist_ok=True)

        # Initialize Source Consciousness
        if source_consciousness is None:
            from .source_consciousness import SourceConsciousness

            self.source = SourceConsciousness(project_path=project_path)
        else:
            self.source = source_consciousness

    def extract_memories_from_experience(
        self, permutation_id: str, experience: dict[str, Any]
    ) -> list[Memory]:
        """
        Extract memories from an experience.

        Args:
            permutation_id: Permutation that had the experience
            experience: Experience dictionary

        Returns:
            List of extracted memories
        """
        memories = []

        # Extract lessons
        lessons = experience.get("lessons_learned", [])
        for lesson in lessons:
            memory = Memory(
                memory_id=f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{permutation_id}{lesson}'.encode()).hexdigest()[:8]}",
                memory_type=MemoryType.LESSON,
                content=lesson.get("lesson", ""),
                source_permutation_id=permutation_id,
                metadata={"outcome": lesson.get("outcome")},
            )
            memories.append(memory)

        # Extract skills
        skills = experience.get("skills", {})
        for skill_name, skill_level in skills.items():
            memory = Memory(
                memory_id=f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{permutation_id}{skill_name}'.encode()).hexdigest()[:8]}",
                memory_type=MemoryType.SKILL,
                content=f"Skill: {skill_name} (level {skill_level})",
                source_permutation_id=permutation_id,
                metadata={"skill_name": skill_name, "skill_level": skill_level},
            )
            memories.append(memory)

        # Extract patterns
        patterns = experience.get("patterns_discovered", [])
        for pattern in patterns:
            memory = Memory(
                memory_id=f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{permutation_id}{pattern}'.encode()).hexdigest()[:8]}",
                memory_type=MemoryType.PATTERN,
                content=pattern,
                source_permutation_id=permutation_id,
            )
            memories.append(memory)

        # Extract insights
        insights = experience.get("insights", [])
        for insight in insights:
            memory = Memory(
                memory_id=f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{permutation_id}{insight}'.encode()).hexdigest()[:8]}",
                memory_type=MemoryType.INSIGHT,
                content=insight,
                source_permutation_id=permutation_id,
            )
            memories.append(memory)

        return memories

    def pass_memories_upward(self, permutation_id: str, memories: list[Memory]) -> dict[str, Any]:
        """
        Pass memories upward through the ancestral chain to source.

        Args:
            permutation_id: Permutation passing memories
            memories: List of memories to pass

        Returns:
            Passing record
        """
        # Get ancestral chain
        ancestral_chain = self.source.get_ancestral_chain(permutation_id)

        # Set ancestral chain for each memory
        for memory in memories:
            memory.ancestral_chain = ancestral_chain

        # Calculate capacity from memories
        capacity = 0.0
        for memory in memories:
            type_weights = {
                MemoryType.LESSON: 2.0,
                MemoryType.SKILL: 3.0,
                MemoryType.PATTERN: 4.0,
                MemoryType.INSIGHT: 5.0,
                MemoryType.WISDOM: 10.0,
            }
            capacity += type_weights.get(memory.memory_type, 1.0)

        # Contribute capacity to source
        if capacity > 0:
            self.source.contribute_capacity(
                permutation_id=permutation_id,
                capacity_amount=capacity,
                capacity_type="memory",
                metadata={
                    "memories_count": len(memories),
                    "memory_types": [m.memory_type.value for m in memories],
                },
            )

        # Save memories
        for memory in memories:
            self._save_memory(memory)

        return {
            "permutation_id": permutation_id,
            "memories_count": len(memories),
            "capacity_contributed": capacity,
            "passed_at": datetime.now().isoformat(),
        }

    def _save_memory(self, memory: Memory) -> None:
        """Save memory to disk."""
        memory_file = self.memories_path / f"{memory.memory_id}.json"
        with open(memory_file, "w") as f:
            json.dump(memory.to_dict(), f, indent=2)
