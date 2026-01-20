"""
Storyteller - Narrative engine that converts input into story PDFs.

Converts text, structured data, or events into narrative prose and generates PDF books.
"""

import re
from collections import Counter
from pathlib import Path
from typing import Any


class Storyteller:
    """
    Narrative engine that converts input into story PDFs.

    Extends Narrator for logging, uses PDFGenerator for output.
    """

    def __init__(
        self,
        input_data: str | dict | list,
        narrative_style: str = "medium",
        story_structure: str = "linear",  # Start simple
        pdf_style: str = "premium",
        narrator: Any | None = None,
    ):
        """
        Initialize Storyteller.

        Args:
            input_data: Text string, dict, or list of events
            narrative_style: Complexity level (simple/medium)
            story_structure: Structure template (linear/three_act)
            pdf_style: PDFGenerator style preset
            narrator: Optional Narrator instance (creates if None)
        """
        # Create or use existing Narrator
        if narrator is None:
            from ..core.tavern_keeper import Narrator, TavernKeeper

            tavern = TavernKeeper(Path.cwd())
            self.narrator = Narrator(tavern)
        else:
            self.narrator = narrator

        self.input_data = input_data
        self.narrative_style = narrative_style
        self.story_structure = story_structure
        self.pdf_style = pdf_style

        # Narrative state (for consistency)
        self.characters: dict[str, dict] = {}
        self.settings: dict[str, dict] = {}
        self.timeline: list[dict] = []

    def tell_story(
        self, output_path: Path | None = None, title: str | None = None, open_pdf: bool = False
    ) -> Path:
        """
        Generate complete narrative PDF.

        Returns:
            Path to generated PDF
        """
        # 1. Parse input
        narrative_data = self._parse_input()

        # 2. Generate narrative structure
        story_structure = self._generate_structure(narrative_data)

        # 3. Generate narrative prose
        narrative_text = self._generate_narrative(story_structure)

        # 4. Format for PDF
        formatted_content = self._format_for_pdf(narrative_text)

        # 5. Generate PDF
        from .pdf_generator import PDFGenerator

        generator = PDFGenerator.from_content(
            content=formatted_content, title=title or "Generated Story", style=self.pdf_style
        )

        return generator.save(
            output_path=output_path,
            target_pages=None,  # No limit for books
            open_pdf=open_pdf,
        )

    @classmethod
    def from_text(cls, text: str, **kwargs) -> "Storyteller":
        """Create Storyteller from text input."""
        return cls(input_data=text, **kwargs)

    @classmethod
    def from_data(cls, data: dict, **kwargs) -> "Storyteller":
        """Create Storyteller from structured data."""
        return cls(input_data=data, **kwargs)

    @classmethod
    def from_events(cls, events: list[dict], **kwargs) -> "Storyteller":
        """Create Storyteller from event list."""
        return cls(input_data=events, **kwargs)

    def _parse_input(self) -> dict[str, Any]:
        """Parse input into narrative elements."""
        if isinstance(self.input_data, str):
            return self._parse_text(self.input_data)
        elif isinstance(self.input_data, dict):
            return self._parse_structured_data(self.input_data)
        elif isinstance(self.input_data, list):
            return self._parse_events(self.input_data)
        else:
            raise ValueError(f"Unsupported input type: {type(self.input_data)}")

    def _parse_text(self, text: str) -> dict[str, Any]:
        """Extract narrative elements from text."""
        # Use ChatDistiller for basic extraction
        from .chat_distiller import ChatDistiller

        distiller = ChatDistiller()
        distilled = distiller.distill_text(text)

        # Extract characters (simple: proper nouns, repeated entities)
        characters = self._extract_characters(text)

        # Extract settings (locations mentioned)
        settings = self._extract_settings(text)

        # Extract timeline (sequence of events from ideas)
        timeline = self._extract_timeline(distilled.ideas)

        return {
            "characters": characters,
            "settings": settings,
            "timeline": timeline,
            "ideas": distilled.ideas,
            "summary": distilled.summary,
        }

    def _extract_characters(self, text: str) -> dict[str, dict]:
        """Extract characters from text (simple approach)."""
        # Find capitalized words (potential names)
        # Simple heuristic: capitalized words that appear multiple times
        words = re.findall(r"\b[A-Z][a-z]+\b", text)
        word_counts = Counter(words)

        # Filter: must appear 2+ times and not be common words
        common_words = {"The", "This", "That", "There", "When", "Where", "What"}
        characters = {}

        for word, count in word_counts.items():
            if count >= 2 and word not in common_words:
                characters[word] = {
                    "name": word,
                    "mentions": count,
                    "attributes": {},  # Will be filled from context
                }

        return characters

    def _parse_structured_data(self, data: dict) -> dict[str, Any]:
        """Parse structured data (characters, events already defined)."""
        return {
            "characters": data.get("characters", {}),
            "settings": data.get("settings", {}),
            "timeline": data.get("events", []),
            "ideas": [],
            "summary": data.get("summary", ""),
        }

    def _parse_events(self, events: list[dict]) -> dict[str, Any]:
        """Parse list of events into narrative structure."""
        # Extract characters from events
        characters = {}
        settings = {}
        timeline = []

        for event in events:
            # Add to timeline
            timeline.append(event)

            # Extract character if present
            if "character" in event:
                char_name = event["character"]
                if char_name not in characters:
                    characters[char_name] = {"name": char_name, "mentions": 0, "attributes": {}}
                characters[char_name]["mentions"] += 1

            # Extract setting if present
            if "location" in event:
                location = event["location"]
                if location not in settings:
                    settings[location] = {"name": location, "mentions": 0}
                settings[location]["mentions"] += 1

        return {
            "characters": characters,
            "settings": settings,
            "timeline": timeline,
            "ideas": [],
            "summary": f"Story with {len(events)} events",
        }

    def _extract_settings(self, text: str) -> dict[str, dict]:
        """Extract settings/locations from text (simple approach)."""
        # Find location indicators (simple patterns)
        location_patterns = [
            r"\b(?:in|at|from|to|near|around)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            r"\b(the|a|an)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        ]

        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    locations.extend([m for m in match if m and m[0].isupper()])
                else:
                    if match and match[0].isupper():
                        locations.append(match)

        location_counts = Counter(locations)

        # Filter common words and low-frequency mentions
        common_words = {"The", "This", "That", "There", "When", "Where", "What", "How", "Why"}
        settings = {}

        for location, count in location_counts.items():
            if count >= 2 and location not in common_words and len(location) > 2:
                settings[location] = {"name": location, "mentions": count}

        return settings

    def _extract_timeline(self, ideas: list) -> list[dict]:
        """Extract timeline of events from ideas."""
        timeline = []

        # Convert ideas to timeline events
        for idea in ideas:
            event = {
                "description": idea.content if hasattr(idea, "content") else str(idea),
                "category": idea.category if hasattr(idea, "category") else "event",
                "importance": idea.importance if hasattr(idea, "importance") else 0.5,
                "timestamp": idea.extracted_at if hasattr(idea, "extracted_at") else None,
            }
            timeline.append(event)

        # Sort by timestamp if available, otherwise by order
        timeline.sort(key=lambda x: x.get("timestamp") or "")

        return timeline

    def _generate_structure(self, narrative_data: dict) -> dict[str, Any]:
        """Generate story structure from narrative data."""

        if self.story_structure == "linear":
            return self._linear_structure(narrative_data)
        elif self.story_structure == "three_act":
            return self._three_act_structure(narrative_data)
        else:
            return self._linear_structure(narrative_data)  # Default

    def _linear_structure(self, data: dict) -> dict[str, Any]:
        """Simple linear structure: beginning, middle, end."""
        timeline = data["timeline"]

        # Split timeline into three parts
        total = len(timeline)
        if total == 0:
            beginning = []
            middle = []
            end = []
        else:
            beginning = timeline[: total // 3]
            middle = timeline[total // 3 : 2 * total // 3]
            end = timeline[2 * total // 3 :]

        return {
            "beginning": beginning,
            "middle": middle,
            "end": end,
            "characters": data["characters"],
            "settings": data["settings"],
        }

    def _three_act_structure(self, data: dict) -> dict[str, Any]:
        """Three-act structure: setup, confrontation, resolution."""
        timeline = data["timeline"]

        # Split into three acts
        total = len(timeline)
        if total == 0:
            act1 = []
            act2 = []
            act3 = []
        else:
            act1 = timeline[: total // 3]
            act2 = timeline[total // 3 : 2 * total // 3]
            act3 = timeline[2 * total // 3 :]

        return {
            "beginning": act1,
            "middle": act2,
            "end": act3,
            "characters": data["characters"],
            "settings": data["settings"],
        }

    def _generate_narrative(self, structure: dict) -> str:
        """Generate narrative prose from structure."""

        if self.narrative_style == "simple":
            return self._simple_narrative(structure)
        elif self.narrative_style == "medium":
            return self._medium_narrative(structure)
        else:
            return self._simple_narrative(structure)

    def _simple_narrative(self, structure: dict) -> str:
        """Simple narrative: paragraph per event."""
        paragraphs = []

        # Beginning
        paragraphs.append("# Beginning\n\n")
        for event in structure["beginning"]:
            paragraphs.append(self._event_to_prose(event))

        # Middle
        paragraphs.append("\n# Middle\n\n")
        for event in structure["middle"]:
            paragraphs.append(self._event_to_prose(event))

        # End
        paragraphs.append("\n# End\n\n")
        for event in structure["end"]:
            paragraphs.append(self._event_to_prose(event))

        return "\n\n".join(paragraphs)

    def _event_to_prose(self, event: dict) -> str:
        """Convert event to prose (simple template-based)."""
        # Use Tracery if available, fallback to simple template
        try:
            import tracery
            from tracery.modifiers import base_english

            from ..core.tavern_keeper.grammars import SUCCESS_GRAMMAR

            # Create Tracery grammar from existing grammar dict
            grammar = tracery.Grammar(SUCCESS_GRAMMAR)
            grammar.add_modifiers(base_english)

            # Generate narrative using Tracery
            narrative = grammar.flatten("#origin#")

            # Replace placeholders with event data if present
            if "location" in event:
                narrative = narrative.replace("#component#", event["location"])
            if "action" in event:
                narrative = narrative.replace("#action#", event["action"])
            if "description" in event:
                narrative = narrative.replace("#narrative#", event["description"])

            return narrative
        except (ImportError, AttributeError):
            # Fallback: simple template
            return f"{event.get('description', 'An event occurred')}."

    def _medium_narrative(self, structure: dict) -> str:
        """Medium complexity: characters, dialogue, arcs."""
        # This requires Tracery proof-of-concept first
        # For now, use simple narrative with character names
        narrative = self._simple_narrative(structure)

        # Add character references
        for char_name, char_data in structure["characters"].items():
            narrative = narrative.replace(char_name, f"**{char_name}**")

        return narrative

    def _format_for_pdf(self, narrative: str) -> str:
        """Format narrative for PDF with book-style elements."""

        # Add chapter headings if structure detected
        if "# Beginning" in narrative:
            narrative = narrative.replace("# Beginning", "## Chapter 1: Beginning")
        if "# Middle" in narrative:
            narrative = narrative.replace("# Middle", "## Chapter 2: Middle")
        if "# End" in narrative:
            narrative = narrative.replace("# End", "## Chapter 3: End")

        # Add scene breaks (double newlines)
        narrative = narrative.replace("\n\n\n", "\n\n---\n\n")

        return narrative
