"""
Chat Distiller: Extracting Ideas from Conversations as Genetic Material

This module extracts key ideas from chat conversations and treats them
as genetic material, complete with genome IDs and taxonomic classification.

The ChatDistiller:
1. Parses chat conversations (markdown, JSON, text)
2. Identifies key concepts, decisions, and insights
3. Generates genome IDs for each idea
4. Assigns scientific names using LineagePoet taxonomy
5. Structures content for 2-page PDF generation
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from ..core.science.taxonomy import LineagePoet


@dataclass
class IdeaGene:
    """
    A single idea extracted from a conversation, treated as genetic material.

    Each idea gets a unique genome ID and scientific name, enabling
    lineage tracking and evolution over time.
    """
    content: str  # The idea itself
    category: str  # "decision", "insight", "question", "action", "concept"
    context: str = ""  # Surrounding context
    importance: float = 0.5  # 0.0-1.0 importance score

    # Genetic identity
    genome_id: str = ""  # SHA-256 hash of content
    scientific_name: str = ""  # Generated from genome_id

    # Metadata
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    source_location: str = ""  # File/line reference
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Compute genome ID and scientific name after initialization."""
        if not self.genome_id:
            self.genome_id = self._compute_genome_id()
        if not self.scientific_name:
            self.scientific_name = LineagePoet.generate_name(self.genome_id)

    def _compute_genome_id(self) -> str:
        """
        Compute deterministic genome ID from idea content.

        Returns:
            SHA-256 hash of content + category
        """
        combined = f"{self.category}:{self.content}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "content": self.content,
            "category": self.category,
            "context": self.context,
            "importance": self.importance,
            "genome_id": self.genome_id,
            "scientific_name": self.scientific_name,
            "extracted_at": self.extracted_at.isoformat(),
            "source_location": self.source_location,
            "tags": self.tags,
        }


@dataclass
class DistilledChat:
    """
    A chat conversation distilled into structured ideas ready for PDF generation.

    This is the processed output that feeds into the 2-page PDF generator.
    """
    title: str  # Chat title/summary
    summary: str  # Brief overview (1-2 sentences)
    ideas: List[IdeaGene]  # Extracted ideas

    # Metadata
    source_file: str = ""  # Source chat file
    distilled_at: datetime = field(default_factory=datetime.utcnow)
    total_ideas: int = 0

    # Content density metrics
    decisions_count: int = 0
    insights_count: int = 0
    actions_count: int = 0
    concepts_count: int = 0
    questions_count: int = 0

    def __post_init__(self):
        """Calculate metrics after initialization."""
        self.total_ideas = len(self.ideas)
        self.decisions_count = sum(1 for i in self.ideas if i.category == "decision")
        self.insights_count = sum(1 for i in self.ideas if i.category == "insight")
        self.actions_count = sum(1 for i in self.ideas if i.category == "action")
        self.concepts_count = sum(1 for i in self.ideas if i.category == "concept")
        self.questions_count = sum(1 for i in self.ideas if i.category == "question")

    def get_top_ideas(self, n: int = 10, min_importance: float = 0.5) -> List[IdeaGene]:
        """
        Get top N most important ideas.

        Args:
            n: Number of ideas to return
            min_importance: Minimum importance threshold

        Returns:
            List of top ideas sorted by importance
        """
        filtered = [i for i in self.ideas if i.importance >= min_importance]
        return sorted(filtered, key=lambda x: x.importance, reverse=True)[:n]

    def get_by_category(self, category: str) -> List[IdeaGene]:
        """Get all ideas in a specific category."""
        return [i for i in self.ideas if i.category == category]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "summary": self.summary,
            "source_file": self.source_file,
            "distilled_at": self.distilled_at.isoformat(),
            "total_ideas": self.total_ideas,
            "metrics": {
                "decisions": self.decisions_count,
                "insights": self.insights_count,
                "actions": self.actions_count,
                "concepts": self.concepts_count,
                "questions": self.questions_count,
            },
            "ideas": [idea.to_dict() for idea in self.ideas],
        }

    def save(self, output_path: Path):
        """Save distilled chat to JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


class ChatDistiller:
    """
    Distills chat conversations into structured ideas for 2-page PDF generation.

    Supports multiple input formats:
    - Markdown chat logs
    - JSON conversation exports
    - Plain text transcripts
    """

    # Patterns for extracting ideas from chat
    DECISION_PATTERNS = [
        r"(?:decided|decision|choose|chose|selected|going with)",
        r"(?:we will|we'll|let's|should)",
        r"(?:final|chosen|approved|accepted)",
    ]

    INSIGHT_PATTERNS = [
        r"(?:realized|discovered|learned|understood|found that)",
        r"(?:key insight|important|critical|crucial)",
        r"(?:it turns out|actually|in fact)",
    ]

    ACTION_PATTERNS = [
        r"(?:TODO|action item|next step|will do|going to)",
        r"(?:need to|must|should|have to)",
        r"(?:implement|create|build|fix|update)",
    ]

    CONCEPT_PATTERNS = [
        r"(?:concept|idea|approach|method|pattern)",
        r"(?:system|framework|architecture|design)",
        r"(?:is a|is the|represents)",
    ]

    QUESTION_PATTERNS = [
        r"(?:\?$)",
        r"(?:how|what|why|when|where|who|which)",
        r"(?:question|wondering|curious|unclear)",
    ]

    def __init__(self, importance_threshold: float = 0.3):
        """
        Initialize distiller.

        Args:
            importance_threshold: Minimum importance for extracted ideas
        """
        self.importance_threshold = importance_threshold

    def distill_markdown(self, markdown_path: Path) -> DistilledChat:
        """
        Distill a markdown chat log into structured ideas.

        Args:
            markdown_path: Path to markdown chat file

        Returns:
            DistilledChat with extracted ideas
        """
        markdown_path = Path(markdown_path)
        content = markdown_path.read_text()

        # Extract title from first heading or filename
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else markdown_path.stem

        # Extract ideas from content
        ideas = self._extract_ideas_from_text(content, str(markdown_path))

        # Generate summary from first few ideas
        summary = self._generate_summary(ideas)

        return DistilledChat(
            title=title,
            summary=summary,
            ideas=ideas,
            source_file=str(markdown_path),
        )

    def distill_text(self, text: str, title: str = "Chat Conversation") -> DistilledChat:
        """
        Distill plain text conversation into structured ideas.

        Args:
            text: Conversation text
            title: Title for the conversation

        Returns:
            DistilledChat with extracted ideas
        """
        ideas = self._extract_ideas_from_text(text, "text_input")
        summary = self._generate_summary(ideas)

        return DistilledChat(
            title=title,
            summary=summary,
            ideas=ideas,
            source_file="text_input",
        )

    def _extract_ideas_from_text(self, text: str, source: str) -> List[IdeaGene]:
        """
        Extract ideas from text content.

        Args:
            text: Text to analyze
            source: Source location

        Returns:
            List of extracted IdeaGenes
        """
        ideas = []
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()

            if not line or len(line) < 10:  # Skip very short lines
                continue

            # Determine category and importance
            category, importance = self._classify_line(line)

            if importance < self.importance_threshold:
                continue

            # Extract context (previous and next lines)
            context_lines = []
            if i > 0:
                context_lines.append(lines[i - 1].strip())
            context_lines.append(line)
            if i < len(lines) - 1:
                context_lines.append(lines[i + 1].strip())
            context = " ".join(context_lines)

            # Create idea gene
            idea = IdeaGene(
                content=line,
                category=category,
                context=context,
                importance=importance,
                source_location=f"{source}:L{i+1}",
            )

            ideas.append(idea)

        return ideas

    def _classify_line(self, line: str) -> tuple[str, float]:
        """
        Classify a line and assign importance.

        Args:
            line: Line of text

        Returns:
            Tuple of (category, importance_score)
        """
        line_lower = line.lower()

        # Check patterns for each category
        decision_score = self._pattern_score(line_lower, self.DECISION_PATTERNS)
        insight_score = self._pattern_score(line_lower, self.INSIGHT_PATTERNS)
        action_score = self._pattern_score(line_lower, self.ACTION_PATTERNS)
        concept_score = self._pattern_score(line_lower, self.CONCEPT_PATTERNS)
        question_score = self._pattern_score(line_lower, self.QUESTION_PATTERNS)

        # Select category with highest score
        scores = {
            "decision": decision_score,
            "insight": insight_score,
            "action": action_score,
            "concept": concept_score,
            "question": question_score,
        }

        category = max(scores, key=scores.get)
        importance = scores[category]

        # Boost importance for longer, more substantive lines
        if len(line) > 100:
            importance *= 1.2

        # Boost importance for lines with specific keywords
        if any(kw in line_lower for kw in ["critical", "important", "key", "must", "essential"]):
            importance *= 1.3

        # Clamp to 0.0-1.0
        importance = min(importance, 1.0)

        return category, importance

    def _pattern_score(self, text: str, patterns: List[str]) -> float:
        """
        Score text against a list of regex patterns.

        Args:
            text: Text to score
            patterns: List of regex patterns

        Returns:
            Score between 0.0 and 1.0
        """
        matches = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1

        # Normalize by number of patterns
        return min(matches / len(patterns), 1.0) if patterns else 0.0

    def _generate_summary(self, ideas: List[IdeaGene]) -> str:
        """
        Generate a brief summary from extracted ideas.

        Args:
            ideas: List of ideas

        Returns:
            Summary string (1-2 sentences)
        """
        if not ideas:
            return "Empty conversation with no extractable ideas."

        # Count by category
        categories = {}
        for idea in ideas:
            categories[idea.category] = categories.get(idea.category, 0) + 1

        # Generate summary
        top_category = max(categories, key=categories.get)
        total = len(ideas)

        summary = f"Conversation with {total} key ideas, "
        summary += f"primarily focused on {top_category}s. "

        # Add category breakdown
        breakdown = ", ".join([f"{count} {cat}" for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)])
        summary += f"Contains: {breakdown}."

        return summary
