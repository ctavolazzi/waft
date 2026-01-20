#!/usr/bin/env python3
"""
Create Book - Simple DnD Storybook Generator
==============================================

A simple command-line tool to create beautiful D&D-style storybooks
using the WAFT Storyteller system.

Usage:
    python scripts/create_book.py "My Book Title" --content "Chapter content here..."
    python scripts/create_book.py "Adventure Book" --file story.txt
    python scripts/create_book.py "Campaign Book" --demo
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.pantheon.storyteller import Storyteller


def create_sample_chapters() -> list[dict[str, Any]]:
    """Create sample chapters for demo book."""
    return [
        {
            "title": "Chapter 1: The Beginning",
            "content": """
            In a world where magic flows through every stone and tree,
            a group of adventurers gathered at the ancient tavern known
            as The Wandering Star. The tavern keeper, a wise old dwarf
            named Thorgrim, had seen many heroes come and go.

            Tonight was different. The stars aligned in a way that hadn't
            been seen in a thousand years. The adventurers felt a pull,
            a calling to something greater than themselves.

            As they sat around the fire, sharing stories and ale, a
            mysterious figure entered the tavern. Cloaked in shadows
            and carrying an ancient tome, the stranger approached their table.

            "I have been waiting for you," the figure said, placing the
            tome on the table. "Your destiny begins tonight."
            """,
            "read_aloud": [
                "The tavern door creaks open, and a chill wind follows the mysterious figure inside. All eyes turn to the newcomer."
            ],
            "sidebar": {
                "title": "The Wandering Star",
                "content": "This ancient tavern has stood for over five hundred years, serving adventurers from all corners of the realm.",
            },
        },
        {
            "title": "Chapter 2: The Quest",
            "content": """
            The tome opened of its own accord, revealing a map of the
            realm marked with glowing runes. The adventurers leaned in,
            their eyes wide with wonder and anticipation.

            "The Dark Lord has awakened," the stranger explained. "Only
            you can stop him. But first, you must gather the three
            artifacts of power: the Sword of Light, the Shield of Truth,
            and the Crown of Wisdom."

            The quest was clear. The adventurers looked at each other,
            knowing that their lives would never be the same. They had
            trained for this moment, and now it was time to prove their worth.

            Thorgrim the tavern keeper approached, placing a small pouch
            on the table. "Take this," he said. "It contains provisions
            for your journey. May the stars guide you."
            """,
            "read_aloud": [
                "The map glows brighter as you touch it, and you feel a surge of energy flow through your body."
            ],
            "characters": ["Thorgrim", "The Stranger"],
            "settings": ["The Wandering Star Tavern"],
        },
        {
            "title": "Chapter 3: The Journey Begins",
            "content": """
            With the map in hand and provisions secured, the adventurers
            set out at dawn. The path led them through the Whispering Woods,
            where ancient trees seemed to watch their every move.

            As they traveled deeper into the forest, they encountered
            their first challenge: a bridge guarded by a riddle-speaking
            troll. The troll, named Grom, was not hostile but demanded
            they answer his riddle before crossing.

            "What has roots as nobody sees, is taller than trees, up, up
            it goes, and yet never grows?" Grom asked, his voice rumbling
            like thunder.

            After a moment of thought, one of the adventurers answered:
            "A mountain!" Grom smiled, a rare sight, and allowed them
            to pass.

            The journey had truly begun, and the adventurers knew that
            greater challenges lay ahead.
            """,
            "read_aloud": [
                "The troll's eyes gleam with intelligence as he poses his riddle, and you realize this is no ordinary encounter."
            ],
            "monsters": [
                {
                    "name": "Grom the Bridge Troll",
                    "size": "Large",
                    "type": "giant",
                    "alignment": "neutral",
                    "armor_class": 15,
                    "hit_points": "84 (8d10 + 40)",
                    "speed": "30 ft.",
                    "ability_scores": {
                        "str": 18,
                        "dex": 8,
                        "con": 16,
                        "int": 12,
                        "wis": 14,
                        "cha": 10,
                    },
                    "description": "A wise old troll who guards the bridge, more interested in riddles than combat.",
                    "actions": [
                        {
                            "name": "Club",
                            "description": "Melee Weapon Attack: +6 to hit, reach 10 ft., one target. Hit: 13 (2d6 + 6) bludgeoning damage.",
                        }
                    ],
                }
            ],
            "characters": ["Grom"],
            "settings": ["Whispering Woods", "The Bridge"],
        },
    ]


def parse_chapters_from_file(file_path: Path) -> list[dict[str, Any]]:
    """
    Parse chapters from a text file.

    Supports:
    - Markdown with ## headers for chapters
    - YAML frontmatter for chapter metadata
    - Read-aloud text in > blockquotes
    - Sidebars in <!-- sidebar: title --> blocks
    """
    content = file_path.read_text(encoding="utf-8")

    chapters = []
    current_chapter = None
    current_content = []
    current_read_aloud = []
    current_sidebar = None
    current_metadata = {}

    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check for chapter header (## or #)
        if line.startswith("##"):
            # Save previous chapter
            if current_chapter:
                chapter_data = {"title": current_chapter, "content": "\n\n".join(current_content)}
                if current_read_aloud:
                    chapter_data["read_aloud"] = current_read_aloud
                if current_sidebar:
                    chapter_data["sidebar"] = current_sidebar
                if current_metadata:
                    chapter_data.update(current_metadata)
                chapters.append(chapter_data)

            # Start new chapter
            current_chapter = line.lstrip("#").strip()
            current_content = []
            current_read_aloud = []
            current_sidebar = None
            current_metadata = {}
            i += 1
            continue

        # Check for YAML frontmatter (--- blocks)
        if line == "---" and i == 0:
            i += 1
            frontmatter_lines = []
            while i < len(lines) and lines[i].strip() != "---":
                frontmatter_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # Skip closing ---
            # Parse simple YAML (key: value)
            for fm_line in frontmatter_lines:
                if ":" in fm_line:
                    key, value = fm_line.split(":", 1)
                    current_metadata[key.strip()] = value.strip().strip("\"'")
            continue

        # Check for read-aloud text (> blockquote)
        if line.startswith(">"):
            read_aloud_text = line[1:].strip()
            if read_aloud_text:
                current_read_aloud.append(read_aloud_text)
            i += 1
            continue

        # Check for sidebar (HTML comment style)
        if "<!-- sidebar:" in line or "<!--sidebar:" in line:
            # Extract sidebar title and content
            match = re.search(r"sidebar:\s*(.+?)\s*-->", line, re.IGNORECASE)
            if match:
                sidebar_title = match.group(1)
                # Get next lines until closing or next section
                sidebar_content = []
                i += 1
                while i < len(lines) and not (
                    lines[i].strip().startswith("<!--") or lines[i].strip().startswith("##")
                ):
                    if lines[i].strip() and not lines[i].strip().startswith("-->"):
                        sidebar_content.append(lines[i].strip())
                    i += 1
                current_sidebar = {"title": sidebar_title, "content": "\n\n".join(sidebar_content)}
            else:
                i += 1
            continue

        # Regular content
        if current_chapter and line:
            current_content.append(line)
        elif not current_chapter and line:
            # Content before first chapter - create chapter 1
            if not current_chapter:
                current_chapter = "Chapter 1"
            current_content.append(line)

        i += 1

    # Add last chapter
    if current_chapter:
        chapter_data = {"title": current_chapter, "content": "\n\n".join(current_content)}
        if current_read_aloud:
            chapter_data["read_aloud"] = current_read_aloud
        if current_sidebar:
            chapter_data["sidebar"] = current_sidebar
        if current_metadata:
            chapter_data.update(current_metadata)
        chapters.append(chapter_data)

    # If no chapters found, treat entire file as one chapter
    if not chapters:
        chapters.append({"title": "Chapter 1", "content": content})

    return chapters


def create_book(
    title: str,
    chapters: list[dict[str, Any]] | None = None,
    author: str | None = None,
    output_path: Path | None = None,
    include_monsters: bool = True,
    include_read_aloud: bool = True,
    template_style: str = "dnd",
) -> Path:
    """
    Create a DnD-style storybook.

    Args:
        title: Book title
        chapters: List of chapter dicts (or None for demo)
        author: Author name (default: "WAFT Storyteller")
        output_path: Output PDF path (auto-generated if None)
        include_monsters: Include monster stat blocks
        include_read_aloud: Format read-aloud text boxes

    Returns:
        Path to generated PDF
    """
    print(f"\n📚 Creating book: {title}")
    print("=" * 60)

    # Initialize Storyteller
    storyteller = Storyteller()

    # Use demo chapters if none provided
    if chapters is None:
        print("📖 Using demo chapters...")
        chapters = create_sample_chapters()

    print(f"📑 Found {len(chapters)} chapters")

    # Show chapter summary
    for i, ch in enumerate(chapters, 1):
        has_read_aloud = bool(ch.get("read_aloud"))
        has_sidebar = bool(ch.get("sidebar"))
        has_monsters = bool(ch.get("monsters"))
        features = []
        if has_read_aloud:
            features.append("read-aloud")
        if has_sidebar:
            features.append("sidebar")
        if has_monsters:
            features.append("monsters")
        feature_str = f" ({', '.join(features)})" if features else ""
        print(f"   {i}. {ch.get('title', f'Chapter {i}')}{feature_str}")

    # Create the storybook based on template style
    print("\n✨ Generating PDF...")
    story = None
    try:
        if template_style == "field-guide":
            from scripts.evolve_book_template import generate_field_guide_storybook_latex

            final_path = generate_field_guide_storybook_latex(
                title=title, chapters=chapters, author=author, output_path=output_path
            )
        elif template_style == "academic":
            from scripts.evolve_book_template import generate_academic_storybook_latex

            final_path = generate_academic_storybook_latex(
                title=title, chapters=chapters, author=author, output_path=output_path
            )
        else:  # dnd (default)
            # Initialize Storyteller
            storyteller = Storyteller()
            story = storyteller.create_storybook(
                title=title,
                chapters=chapters,
                author=author,
                story_type="storybook",
                include_monsters=include_monsters,
                include_read_aloud=include_read_aloud,
            )
            # Move to custom output path if specified
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                import shutil

                shutil.copy2(story.story_path, output_path)
                final_path = output_path
            else:
                final_path = story.story_path
    except RuntimeError as e:
        if "LaTeX compiler" in str(e) or "pdflatex" in str(e).lower():
            print("\n" + "=" * 60)
            print("⚠️  LaTeX Required")
            print("=" * 60)
            print("\nThe storybook template requires LaTeX to be installed.")
            print("\nTo install LaTeX:")
            print("  macOS:  brew install --cask mactex")
            print("  Linux:  sudo apt-get install texlive-full")
            print("  Or:     Install BasicTeX (smaller, ~100MB)")
            print("\n" + "=" * 60)
        raise
    except Exception as e:
        print(f"\n❌ Error generating book: {e}")
        import traceback

        traceback.print_exc()
        raise

    print("=" * 60)
    print(f"✅ Book created: {final_path}")
    print(f"   Size: {final_path.stat().st_size / 1024:.1f} KB")
    if template_style == "dnd" and story:
        print(f"   Story ID: {story.story_id}")
    print()

    return final_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create a D&D-style storybook PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create book with demo content
  python scripts/create_book.py "My Adventure Book" --demo

  # Create book from text file
  python scripts/create_book.py "Campaign Book" --file story.txt

  # Create book with inline content
  python scripts/create_book.py "My Story" --content "Chapter 1 content here..."

  # Specify output location
  python scripts/create_book.py "My Book" --demo --output books/my_book.pdf
        """,
    )

    parser.add_argument("title", help="Book title")

    parser.add_argument("--content", help="Chapter content (will create single chapter)")

    parser.add_argument(
        "--file",
        type=Path,
        help="Text file with chapters (use ## headers for chapters). Also supports JSON/YAML files.",
    )

    parser.add_argument("--demo", action="store_true", help="Use demo content (3 sample chapters)")

    parser.add_argument(
        "--author", default="WAFT Storyteller", help="Author name (default: WAFT Storyteller)"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output PDF path (default: auto-generated in _pantheon/storyteller/storybooks/)",
    )

    parser.add_argument("--no-monsters", action="store_true", help="Exclude monster stat blocks")

    parser.add_argument(
        "--no-read-aloud", action="store_true", help="Exclude read-aloud text boxes"
    )

    parser.add_argument(
        "--template",
        choices=["dnd", "field-guide", "academic"],
        default="dnd",
        help="Template style (default: dnd)",
    )

    args = parser.parse_args()

    # Determine chapters source
    chapters = None

    if args.demo:
        chapters = create_sample_chapters()
    elif args.file:
        if not args.file.exists():
            print(f"❌ Error: File not found: {args.file}")
            return 1
        print(f"📄 Reading chapters from: {args.file}")

        # Check file extension for JSON/YAML
        file_ext = args.file.suffix.lower()
        if file_ext == ".json":
            import json

            data = json.loads(args.file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                chapters = data
            elif isinstance(data, dict) and "chapters" in data:
                chapters = data["chapters"]
            else:
                print(
                    "❌ Error: JSON file must contain a list of chapters or a dict with 'chapters' key"
                )
                return 1
        elif file_ext in [".yaml", ".yml"]:
            try:
                import yaml

                data = yaml.safe_load(args.file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    chapters = data
                elif isinstance(data, dict) and "chapters" in data:
                    chapters = data["chapters"]
                else:
                    print(
                        "❌ Error: YAML file must contain a list of chapters or a dict with 'chapters' key"
                    )
                    return 1
            except ImportError:
                print("⚠️  Warning: PyYAML not installed. Install with: pip install pyyaml")
                print("   Falling back to text parsing...")
                chapters = parse_chapters_from_file(args.file)
        else:
            chapters = parse_chapters_from_file(args.file)
    elif args.content:
        chapters = [{"title": "Chapter 1", "content": args.content}]
    else:
        # Default to demo
        print("ℹ️  No content specified, using demo chapters...")
        chapters = create_sample_chapters()

    # Create the book
    try:
        pdf_path = create_book(
            title=args.title,
            chapters=chapters,
            author=args.author,
            output_path=args.output,
            include_monsters=not args.no_monsters,
            include_read_aloud=not args.no_read_aloud,
            template_style=args.template,
        )

        print(f"🎉 Success! Your book is ready: {pdf_path}")
        return 0

    except Exception as e:
        print(f"\n❌ Error creating book: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
