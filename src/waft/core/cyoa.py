"""
CYOA Engine - Choose Your Own Adventure
========================================

A simple, elegant CYOA engine inspired by Raymond Camden's Eleventy pattern.
Stories are defined as Markdown files with YAML front matter.

Format:
```markdown
---
title: Start of the Story
choices:
  - text: This is choice one
    path: one
  - text: This is choice two
    path: two
---

This is the story content in Markdown.
```

If no `choices` are provided, it's "The End."
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Regex to extract YAML front matter
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class Choice:
    """A single choice option."""
    text: str
    path: str


@dataclass
class Page:
    """A single page/scene in the story."""
    id: str  # Filename without extension
    title: str
    content: str  # Markdown content
    choices: list[Choice] = field(default_factory=list)
    # Visual novel fields
    scene: str | None = None  # Background scene (tavern, forest, crypt, etc.)
    speaker: str | None = None  # Character speaking
    mood: str | None = None  # Atmosphere (warm, dark, mysterious, danger)
    portrait: str | None = None  # Character portrait position/image

    @property
    def is_ending(self) -> bool:
        """True if this page has no choices (The End)."""
        return len(self.choices) == 0


@dataclass
class Story:
    """A complete CYOA story."""
    name: str
    pages: dict[str, Page]  # id -> Page
    start_page: str = "start"

    def get_page(self, page_id: str) -> Page | None:
        """Get a page by ID."""
        return self.pages.get(page_id)

    def validate(self) -> list[str]:
        """
        Validate story integrity.
        Returns list of errors (empty if valid).
        """
        errors = []

        # Check start page exists
        if self.start_page not in self.pages:
            errors.append(f"Start page '{self.start_page}' not found")

        # Check all choice paths point to valid pages
        for page_id, page in self.pages.items():
            for choice in page.choices:
                if choice.path not in self.pages:
                    errors.append(f"Page '{page_id}' has broken link to '{choice.path}'")

        return errors

    def get_graph(self) -> dict:
        """
        Get story as a graph for visualization.
        Returns dict with nodes and edges.
        """
        nodes = []
        edges = []

        for page_id, page in self.pages.items():
            nodes.append({
                "id": page_id,
                "title": page.title,
                "is_ending": page.is_ending,
                "is_start": page_id == self.start_page,
            })
            for choice in page.choices:
                edges.append({
                    "from": page_id,
                    "to": choice.path,
                    "text": choice.text,
                })

        return {"nodes": nodes, "edges": edges}


def parse_page(file_path: Path) -> Page:
    """
    Parse a Markdown file with YAML front matter into a Page.

    Args:
        file_path: Path to the .md file

    Returns:
        Parsed Page object
    """
    content = file_path.read_text(encoding="utf-8")
    page_id = file_path.stem  # Filename without extension

    # Extract front matter
    match = FRONT_MATTER_RE.match(content)
    if match:
        front_matter_str = match.group(1)
        body = content[match.end():]
        try:
            front_matter = yaml.safe_load(front_matter_str) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path}: {e}")
    else:
        front_matter = {}
        body = content

    # Extract fields
    title = front_matter.get("title", page_id.replace("_", " ").replace("-", " ").title())

    # Parse choices
    choices = []
    for choice_data in front_matter.get("choices", []):
        if isinstance(choice_data, dict) and "text" in choice_data and "path" in choice_data:
            choices.append(Choice(
                text=choice_data["text"],
                path=choice_data["path"],
            ))

    # Visual novel fields
    scene = front_matter.get("scene")
    speaker = front_matter.get("speaker")
    mood = front_matter.get("mood")
    portrait = front_matter.get("portrait")

    return Page(
        id=page_id,
        title=title,
        content=body.strip(),
        choices=choices,
        scene=scene,
        speaker=speaker,
        mood=mood,
        portrait=portrait,
    )


def load_story(story_dir: Path | str, start_page: str = "start") -> Story:
    """
    Load a complete story from a directory of Markdown files.

    Args:
        story_dir: Directory containing .md files (Path or string)
        start_page: ID of the starting page (default: "start")

    Returns:
        Loaded Story object
    """
    if isinstance(story_dir, str):
        story_dir = Path(story_dir)

    if not story_dir.exists():
        raise FileNotFoundError(f"Story directory not found: {story_dir}")

    pages = {}
    for md_file in story_dir.glob("*.md"):
        page = parse_page(md_file)
        pages[page.id] = page

    if not pages:
        raise ValueError(f"No .md files found in {story_dir}")

    return Story(
        name=story_dir.name,
        pages=pages,
        start_page=start_page,
    )


def load_all_stories(stories_root: Path | str) -> dict[str, Story]:
    """
    Load all stories from a root directory.
    Each subdirectory is treated as a separate story.

    Args:
        stories_root: Root directory containing story subdirectories

    Returns:
        Dict mapping story name to Story object
    """
    if isinstance(stories_root, str):
        stories_root = Path(stories_root)

    stories = {}

    if not stories_root.exists():
        return stories

    for story_dir in stories_root.iterdir():
        if story_dir.is_dir() and not story_dir.name.startswith("."):
            try:
                story = load_story(story_dir)
                stories[story.name] = story
            except (ValueError, FileNotFoundError) as e:
                # Skip invalid story directories
                print(f"Warning: Could not load story from {story_dir}: {e}")

    return stories


# ============================================================================
# CLI Player (for testing)
# ============================================================================

def play_story_cli(story: Story) -> None:
    """
    Play a story in the terminal (for testing).
    """
    current_page = story.get_page(story.start_page)

    if not current_page:
        print(f"Error: Start page '{story.start_page}' not found!")
        return

    print(f"\n{'=' * 60}")
    print(f"  {story.name.upper()}")
    print(f"{'=' * 60}\n")

    while current_page:
        print(f"\n## {current_page.title}\n")
        print(current_page.content)
        print()

        if current_page.is_ending:
            print("\n--- THE END ---\n")
            break

        print("\nWhat do you choose?\n")
        for i, choice in enumerate(current_page.choices, 1):
            print(f"  [{i}] {choice.text}")
        print()

        while True:
            try:
                choice_num = int(input("Enter choice number: "))
                if 1 <= choice_num <= len(current_page.choices):
                    break
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nGoodbye!")
                return

        chosen = current_page.choices[choice_num - 1]
        current_page = story.get_page(chosen.path)

        if not current_page:
            print(f"\nError: Page '{chosen.path}' not found!")
            break


if __name__ == "__main__":
    # Quick test
    import sys

    if len(sys.argv) > 1:
        story_path = Path(sys.argv[1])
        story = load_story(story_path)
        errors = story.validate()
        if errors:
            print("Story validation errors:")
            for e in errors:
                print(f"  - {e}")
        else:
            play_story_cli(story)
    else:
        print("Usage: python -m waft.core.cyoa <story_directory>")
