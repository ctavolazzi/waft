"""
Evolving Story - Story that evolves over time with agent direction.

Orchestrates story evolution through agent decisions, maintains state,
and generates PDFs at each generation.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .narrative_decisions import DecisionValidator, NarrativeDecision
from .story_state import Character, Event, StoryState
from .storyteller import Storyteller


class EvolvingStory:
    """
    Story that evolves over time through agent decisions.

    Maintains story state, tracks evolution history, and generates
    PDF snapshots at each generation.
    """

    def __init__(
        self,
        story_id: str | None = None,
        title: str = "Untitled Story",
        initial_state: StoryState | None = None,
    ):
        """
        Initialize evolving story.

        Args:
            story_id: Unique story identifier (auto-generated if None)
            title: Story title
            initial_state: Initial story state (creates empty if None)
        """
        self.story_id = story_id or f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.title = title

        if initial_state:
            self.state = initial_state
            self.state.story_id = self.story_id
            self.state.title = self.title
        else:
            self.state = StoryState(story_id=self.story_id, title=self.title, generation=0)

        self.evolution_history: list[dict[str, Any]] = []
        self.decision_history: list[NarrativeDecision] = []

    @classmethod
    def from_seed(
        cls, seed_text: str, title: str | None = None, story_id: str | None = None
    ) -> "EvolvingStory":
        """
        Create evolving story from seed text.

        Args:
            seed_text: Initial story text
            title: Story title (extracted from text if None)
            story_id: Story identifier (auto-generated if None)
        """
        # Use Storyteller to parse initial text
        storyteller = Storyteller.from_text(seed_text, narrative_style="simple")
        narrative_data = storyteller._parse_input()

        # Create initial state
        state = StoryState(
            story_id=story_id or f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=title or "Untitled Story",
            generation=0,
            summary=narrative_data.get("summary", ""),
        )

        # Add characters
        for char_name, char_data in narrative_data.get("characters", {}).items():
            character = Character(
                name=char_name,
                role=char_data.get("role"),
                attributes=char_data.get("attributes", {}),
                mentions=char_data.get("mentions", 0),
            )
            state.add_character(character)

        # Add initial events from timeline
        for event_data in narrative_data.get("timeline", []):
            event = Event(
                event_id=f"event_{uuid.uuid4()}",
                timestamp=datetime.utcnow(),
                description=event_data.get("description", ""),
                character=event_data.get("character"),
                location=event_data.get("location"),
                category=event_data.get("category", "event"),
                importance=event_data.get("importance", 0.5),
                narrative_text=event_data.get("description", ""),
            )
            state.add_event(event)

        # Set initial narrative text
        state.narrative_text = seed_text

        return cls(story_id=state.story_id, title=state.title, initial_state=state)

    @classmethod
    def from_structured_data(
        cls, data: dict[str, Any], story_id: str | None = None
    ) -> "EvolvingStory":
        """Create evolving story from structured data."""
        state = StoryState.from_dict(data)
        if story_id:
            state.story_id = story_id
        return cls(story_id=state.story_id, title=state.title, initial_state=state)

    def get_current_state(self) -> StoryState:
        """Get current story state for agent observation."""
        return self.state

    def apply_decision(self, decision: NarrativeDecision) -> bool:
        """
        Apply a narrative decision to the story.

        Args:
            decision: Narrative decision to apply

        Returns:
            True if decision was applied, False if validation failed
        """
        # Validate decision
        is_valid, errors = DecisionValidator.validate_decision(decision, self.state)

        if not is_valid:
            print(f"Decision validation failed: {errors}")
            return False

        # Check coherence
        coherence = DecisionValidator.check_coherence(decision, self.state)
        if coherence < 0.3:
            print(f"Decision coherence too low: {coherence}")
            return False

        # Apply decision based on type
        self.state.generation += 1
        decision.generation = self.state.generation

        # Convert decision to event
        event = decision.to_event()
        self.state.add_event(event)

        # Update narrative text
        if decision.narrative_text:
            self.state.narrative_text += f"\n\n{decision.narrative_text}"
        else:
            self.state.narrative_text += f"\n\n{decision.description}"

        # Update characters if needed
        if decision.decision_type.value == "character_development" and decision.character:
            if decision.character in self.state.characters:
                char = self.state.characters[decision.character]
                if decision.narrative_text:
                    char.arc = decision.narrative_text

        # Update world state if needed
        if decision.decision_type.value == "world_event":
            if decision.location:
                if "locations" not in self.state.world_state:
                    self.state.world_state["locations"] = {}
                self.state.world_state["locations"][decision.location] = decision.description

        # Record decision
        self.decision_history.append(decision)
        self.evolution_history.append(
            {
                "generation": self.state.generation,
                "decision": decision.dict(),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Update coherence score
        self.state.coherence_score = coherence

        return True

    def generate_pdf(
        self, generation: int | None = None, output_path: Path | None = None, open_pdf: bool = False
    ) -> Path:
        """
        Generate PDF snapshot of current story state.

        Args:
            generation: Generation number (uses current if None)
            output_path: Output path (auto-generated if None)
            open_pdf: Open PDF after generation

        Returns:
            Path to generated PDF
        """
        gen = generation if generation is not None else self.state.generation

        if output_path is None:
            output_dir = Path("_stories") / self.story_id
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"generation_{gen:03d}.pdf"

        # Convert story state to narrative format for Storyteller
        # Create structured data from state
        storyteller_data = {
            "characters": {
                name: {
                    "name": char.name,
                    "role": char.role,
                    "attributes": char.attributes,
                    "mentions": char.mentions,
                }
                for name, char in self.state.characters.items()
            },
            "settings": self.state.world_state.get("locations", {}),
            "events": [
                {
                    "character": event.character,
                    "action": event.description,
                    "time": event.timestamp.isoformat(),
                    "description": event.narrative_text or event.description,
                }
                for event in self.state.timeline
            ],
            "summary": self.state.summary or f"Story evolution through {gen} generations",
        }

        # Generate PDF using Storyteller
        storyteller = Storyteller.from_data(
            storyteller_data, narrative_style="medium", story_structure="linear"
        )

        # Override narrative text with current state
        storyteller.input_data = self.state.narrative_text

        pdf_path = storyteller.tell_story(
            output_path=output_path, title=f"{self.title} - Generation {gen}", open_pdf=open_pdf
        )

        return pdf_path

    def save_state(self, file_path: Path | None = None) -> Path:
        """
        Save story state to JSON file.

        Args:
            file_path: Path to save (auto-generated if None)

        Returns:
            Path to saved file
        """
        if file_path is None:
            output_dir = Path("_stories") / self.story_id
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / "current_state.json"

        data = {
            "story_id": self.story_id,
            "title": self.title,
            "state": self.state.dict(),
            "evolution_history": self.evolution_history,
            "saved_at": datetime.utcnow().isoformat(),
        }

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        return file_path

    @classmethod
    def load_state(cls, file_path: Path) -> "EvolvingStory":
        """
        Load story state from JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            EvolvingStory instance
        """
        with open(file_path) as f:
            data = json.load(f)

        story = cls(
            story_id=data["story_id"],
            title=data["title"],
            initial_state=StoryState.from_dict(data["state"]),
        )

        story.evolution_history = data.get("evolution_history", [])

        return story

    def get_evolution_history(self) -> list[dict[str, Any]]:
        """Get evolution history."""
        return self.evolution_history.copy()

    def get_summary(self) -> str:
        """Get story summary."""
        return f"""
Story: {self.title}
ID: {self.story_id}
Generation: {self.state.generation}
Characters: {len(self.state.characters)}
Events: {len(self.state.timeline)}
Coherence: {self.state.coherence_score:.2f}
        """.strip()
