"""
Storyteller: God of Narrative and Story Creation

The Storyteller weaves narratives from raw data, events, and ideas,
generating storybooks, campaign materials, and adventure modules
using the D&D 5e LaTeX template for authentic book styling.

Following "as above, so below" principles:
- As above: Pantheon god weaving the threads of narrative
- So below: File-based system generating story PDFs from structured data
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..evolution.storyteller import Storyteller as StorytellerEngine
from ..templates.dnd5e_latex import generate_storybook_latex


class Story:
    """A story created by the Storyteller."""

    def __init__(
        self,
        story_id: str,
        title: str,
        story_path: Path,
        story_type: str = "adventure",
        chapters: list[dict[str, Any]] | None = None,
        characters: list[str] | None = None,
        settings: list[str] | None = None,
        created_at: str | None = None,
    ):
        """
        Initialize a story.

        Args:
            story_id: Unique identifier for the story
            story_path: Path to the story PDF
            title: Story title
            story_type: Type of story (adventure, campaign, storybook, etc.)
            chapters: List of chapter data
            characters: List of character names
            settings: List of setting/location names
            created_at: ISO timestamp when story was created
        """
        self.story_id = story_id
        self.story_path = story_path
        self.title = title
        self.story_type = story_type
        self.chapters = chapters or []
        self.characters = characters or []
        self.settings = settings or []
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert story to dictionary."""
        return {
            "story_id": self.story_id,
            "story_path": str(self.story_path),
            "title": self.title,
            "story_type": self.story_type,
            "chapters": self.chapters,
            "characters": self.characters,
            "settings": self.settings,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Story":
        """Create story from dictionary."""
        return cls(
            story_id=data["story_id"],
            story_path=Path(data["story_path"]),
            title=data["title"],
            story_type=data.get("story_type", "adventure"),
            chapters=data.get("chapters", []),
            characters=data.get("characters", []),
            settings=data.get("settings", []),
            created_at=data.get("created_at"),
        )


class Storyteller:
    """
    Storyteller: God of Narrative and Story Creation

    Generates storybooks, campaign materials, and adventure modules
    using the D&D 5e LaTeX template for authentic book styling.

    Storage:
    - Stories: _pantheon/storyteller/stories/*.json
    - Story Catalog: _pantheon/storyteller/story_catalog.json
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize the Storyteller.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        # Use storage path resolver for augmented content (routes to external drive if available)
        from ..utils import get_storage_path

        # Resolve paths (routes to external drive if available)
        storyteller_rel = Path("_pantheon") / "storyteller"
        self.storyteller_path = get_storage_path(storyteller_rel, self.project_path)
        self.stories_path = get_storage_path(storyteller_rel / "stories", self.project_path)
        self.storybooks_path = get_storage_path(storyteller_rel / "storybooks", self.project_path)

        # Create directory structure
        self.storyteller_path.mkdir(parents=True, exist_ok=True)
        self.stories_path.mkdir(parents=True, exist_ok=True)
        self.storybooks_path.mkdir(parents=True, exist_ok=True)

        # Story catalog
        self.story_catalog: list[Story] = []
        self._load_story_catalog()

    def _load_story_catalog(self):
        """Load story catalog from disk."""
        catalog_file = self.storyteller_path / "story_catalog.json"

        if catalog_file.exists():
            try:
                with open(catalog_file, encoding="utf-8") as f:
                    data = json.load(f)
                    self.story_catalog = [Story.from_dict(s) for s in data.get("stories", [])]
            except Exception as e:
                print(f"Error loading story catalog: {e}")
                self.story_catalog = []

    def _save_story_catalog(self):
        """Save story catalog to disk."""
        catalog_file = self.storyteller_path / "story_catalog.json"

        data = {
            "stories": [s.to_dict() for s in self.story_catalog],
            "total_count": len(self.story_catalog),
            "updated_at": datetime.now().isoformat(),
        }

        with open(catalog_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create_storybook(
        self,
        title: str,
        chapters: list[dict[str, Any]],
        author: str | None = None,
        story_type: str = "storybook",
        include_monsters: bool = False,
        include_read_aloud: bool = True,
    ) -> Story:
        """
        Create a storybook using D&D 5e LaTeX template.

        Args:
            title: Storybook title
            chapters: List of chapter dicts with 'title', 'content', optional 'read_aloud', 'sidebar', 'monsters'
            author: Author name (default: "WAFT Storyteller")
            story_type: Type of story (storybook, adventure, campaign, etc.)
            include_monsters: Include monster stat blocks if present
            include_read_aloud: Format read-aloud text boxes

        Returns:
            Story object
        """
        # Generate story ID
        story_id = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Generate PDF
        output_path = self.storybooks_path / f"{story_id}.pdf"

        pdf_path = generate_storybook_latex(
            title=title,
            chapters=chapters,
            output_path=output_path,
            author=author,
            include_monsters=include_monsters,
            include_read_aloud=include_read_aloud,
        )

        # Extract characters and settings from chapters
        characters = []
        settings = []
        for chapter in chapters:
            # Extract from content (simple heuristic)
            content = chapter.get("content", "")
            # Could use NLP here, but for now just track what's provided
            if "characters" in chapter:
                characters.extend(chapter["characters"])
            if "settings" in chapter:
                settings.extend(chapter["settings"])

        # Create Story object
        story = Story(
            story_id=story_id,
            title=title,
            story_path=pdf_path,
            story_type=story_type,
            chapters=chapters,
            characters=list(set(characters)),  # Deduplicate
            settings=list(set(settings)),  # Deduplicate
        )

        # Save story metadata
        story_file = self.stories_path / f"{story_id}.json"
        with open(story_file, "w", encoding="utf-8") as f:
            json.dump(story.to_dict(), f, indent=2, ensure_ascii=False)

        # Add to catalog
        self.story_catalog.append(story)
        self._save_story_catalog()

        return story

    def create_story_from_engine(
        self,
        input_data: str | dict | list,
        title: str | None = None,
        narrative_style: str = "medium",
        story_structure: str = "linear",
        use_latex: bool = True,
    ) -> Story:
        """
        Create a story using the Storyteller engine, then format as storybook.

        Args:
            input_data: Text, dict, or list of events
            title: Story title (default: generated)
            narrative_style: Complexity level (simple/medium)
            story_structure: Structure template (linear/three_act)
            use_latex: Use LaTeX template (True) or standard PDF (False)

        Returns:
            Story object
        """
        # Use Storyteller engine to generate narrative
        storyteller_engine = StorytellerEngine(
            input_data=input_data, narrative_style=narrative_style, story_structure=story_structure
        )

        # Parse input
        narrative_data = storyteller_engine._parse_input()

        # Generate structure
        story_structure_data = storyteller_engine._generate_structure(narrative_data)

        # Convert to chapters format
        chapters = []

        # Beginning
        if story_structure_data.get("beginning"):
            chapters.append(
                {
                    "title": "Chapter 1: Beginning",
                    "content": "\n\n".join(
                        [
                            storyteller_engine._event_to_prose(e)
                            for e in story_structure_data["beginning"]
                        ]
                    ),
                    "read_aloud": [],  # Could extract from events
                }
            )

        # Middle
        if story_structure_data.get("middle"):
            chapters.append(
                {
                    "title": "Chapter 2: Middle",
                    "content": "\n\n".join(
                        [
                            storyteller_engine._event_to_prose(e)
                            for e in story_structure_data["middle"]
                        ]
                    ),
                    "read_aloud": [],
                }
            )

        # End
        if story_structure_data.get("end"):
            chapters.append(
                {
                    "title": "Chapter 3: End",
                    "content": "\n\n".join(
                        [storyteller_engine._event_to_prose(e) for e in story_structure_data["end"]]
                    ),
                    "read_aloud": [],
                }
            )

        # Generate title if not provided
        if title is None:
            title = narrative_data.get("summary", "Generated Story")
            if not title or len(title) < 5:
                title = f"Story {datetime.now().strftime('%Y-%m-%d')}"

        # Create storybook
        if use_latex:
            return self.create_storybook(title=title, chapters=chapters, story_type="storybook")
        else:
            # Use standard PDF generation
            output_path = (
                self.storybooks_path / f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            pdf_path = storyteller_engine.tell_story(output_path=output_path, title=title)

            story = Story(
                story_id=f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title=title,
                story_path=pdf_path,
                story_type="storybook",
                chapters=chapters,
                characters=list(story_structure_data.get("characters", {}).keys()),
                settings=list(story_structure_data.get("settings", {}).keys()),
            )

            # Save story metadata
            story_file = self.stories_path / f"{story.story_id}.json"
            with open(story_file, "w", encoding="utf-8") as f:
                json.dump(story.to_dict(), f, indent=2, ensure_ascii=False)

            # Add to catalog
            self.story_catalog.append(story)
            self._save_story_catalog()

            return story

    def get_story(self, story_id: str) -> Story | None:
        """Get story by ID."""
        for story in self.story_catalog:
            if story.story_id == story_id:
                return story
        return None

    def list_stories(
        self,
        story_type: str | None = None,
        character: str | None = None,
        setting: str | None = None,
    ) -> list[Story]:
        """
        List stories with optional filters.

        Args:
            story_type: Filter by story type
            character: Filter by character name
            setting: Filter by setting name

        Returns:
            List of matching stories
        """
        stories = self.story_catalog

        if story_type:
            stories = [s for s in stories if s.story_type == story_type]

        if character:
            stories = [s for s in stories if character in s.characters]

        if setting:
            stories = [s for s in stories if setting in s.settings]

        return stories

    def get_story_summary(self) -> dict[str, Any]:
        """Get summary of all stories."""
        return {
            "total_stories": len(self.story_catalog),
            "by_type": {
                story_type: len([s for s in self.story_catalog if s.story_type == story_type])
                for story_type in set(s.story_type for s in self.story_catalog)
            },
            "total_characters": len(
                set(char for story in self.story_catalog for char in story.characters)
            ),
            "total_settings": len(
                set(setting for story in self.story_catalog for setting in story.settings)
            ),
            "recent_stories": [
                s.to_dict()
                for s in sorted(self.story_catalog, key=lambda x: x.created_at, reverse=True)[:5]
            ],
        }
