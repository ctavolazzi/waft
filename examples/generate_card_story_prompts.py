#!/usr/bin/env python3
"""
Card-Based Story Prompt Generator

Uses playing cards to generate creative writing prompts, character traits,
plot points, and narrative elements. Each card represents a story element.
"""

import random
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import Player, generate_deckz_poker

# Card meanings for storytelling
CARD_MEANINGS = {
    "A": {"element": "Beginning", "trait": "Ambitious", "conflict": "Origin story"},
    "2": {"element": "Partnership", "trait": "Dual nature", "conflict": "Choice between two paths"},
    "3": {"element": "Growth", "trait": "Expanding", "conflict": "Three-way tension"},
    "4": {"element": "Stability", "trait": "Grounded", "conflict": "Foundation shaken"},
    "5": {"element": "Change", "trait": "Restless", "conflict": "Disruption"},
    "6": {"element": "Harmony", "trait": "Balanced", "conflict": "Seeking balance"},
    "7": {"element": "Mystery", "trait": "Secretive", "conflict": "Hidden knowledge"},
    "8": {"element": "Power", "trait": "Ambitious", "conflict": "Struggle for control"},
    "9": {"element": "Completion", "trait": "Wise", "conflict": "Near the end"},
    "10": {"element": "Transformation", "trait": "Evolving", "conflict": "Major change"},
    "J": {"element": "Youth", "trait": "Impulsive", "conflict": "Coming of age"},
    "Q": {"element": "Wisdom", "trait": "Nurturing", "conflict": "Maternal/paternal"},
    "K": {"element": "Authority", "trait": "Commanding", "conflict": "Leadership challenge"},
}

SUIT_MEANINGS = {
    "H": {"domain": "Emotions", "setting": "Heart", "theme": "Love, passion, relationships"},
    "D": {"domain": "Material", "setting": "Wealth", "theme": "Money, resources, ambition"},
    "C": {"domain": "Intellect", "setting": "Mind", "theme": "Knowledge, strategy, learning"},
    "S": {"domain": "Conflict", "setting": "Battle", "theme": "Struggle, darkness, challenge"},
}


def draw_story_cards(num_cards: int = 5) -> list[str]:
    """Draw random cards for story generation."""
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["H", "D", "C", "S"]

    cards = []
    for _ in range(num_cards):
        rank = random.choice(ranks)
        suit = random.choice(suits)
        cards.append(f"{rank}{suit}")

    return cards


def interpret_cards(cards: list[str]) -> dict[str, Any]:
    """Interpret cards as story elements."""
    story = {
        "protagonist": None,
        "antagonist": None,
        "setting": None,
        "conflict": None,
        "resolution": None,
        "theme": None,
    }

    if len(cards) >= 1:
        # First card: Protagonist
        card = cards[0]
        rank = card[:-1]
        suit = card[-1]
        story["protagonist"] = {
            "card": card,
            "trait": CARD_MEANINGS.get(rank, {}).get("trait", "Unknown"),
            "domain": SUIT_MEANINGS.get(suit, {}).get("domain", "Unknown"),
        }

    if len(cards) >= 2:
        # Second card: Antagonist/Conflict
        card = cards[1]
        rank = card[:-1]
        suit = card[-1]
        story["antagonist"] = {
            "card": card,
            "trait": CARD_MEANINGS.get(rank, {}).get("trait", "Unknown"),
            "domain": SUIT_MEANINGS.get(suit, {}).get("domain", "Unknown"),
        }
        story["conflict"] = CARD_MEANINGS.get(rank, {}).get("conflict", "Unknown")

    if len(cards) >= 3:
        # Third card: Setting
        card = cards[2]
        suit = card[-1]
        story["setting"] = SUIT_MEANINGS.get(suit, {}).get("setting", "Unknown")
        story["theme"] = SUIT_MEANINGS.get(suit, {}).get("theme", "Unknown")

    if len(cards) >= 4:
        # Fourth card: Plot point
        card = cards[3]
        rank = card[:-1]
        story["plot_point"] = CARD_MEANINGS.get(rank, {}).get("element", "Unknown")

    if len(cards) >= 5:
        # Fifth card: Resolution
        card = cards[4]
        rank = card[:-1]
        suit = card[-1]
        story["resolution"] = {
            "card": card,
            "element": CARD_MEANINGS.get(rank, {}).get("element", "Unknown"),
            "theme": SUIT_MEANINGS.get(suit, {}).get("theme", "Unknown"),
        }

    return story


def generate_story_prompt_pdf(
    cards: list[str], output_path: Path, title: str = "Story Prompt from Cards"
) -> Path:
    """Generate a PDF with story prompt from drawn cards."""

    story = interpret_cards(cards)

    # Build content
    content_lines = []
    content_lines.append("# Story Prompt Generator")
    content_lines.append("")
    content_lines.append("## Your Story Elements")
    content_lines.append("")

    if story.get("protagonist"):
        p = story["protagonist"]
        content_lines.append(f"### Protagonist ({p['card']})")
        content_lines.append(f"- **Trait**: {p['trait']}")
        content_lines.append(f"- **Domain**: {p['domain']}")
        content_lines.append("")

    if story.get("antagonist"):
        a = story["antagonist"]
        content_lines.append(f"### Antagonist/Conflict ({a['card']})")
        content_lines.append(f"- **Trait**: {a['trait']}")
        content_lines.append(f"- **Domain**: {a['domain']}")
        content_lines.append(f"- **Conflict Type**: {story.get('conflict', 'Unknown')}")
        content_lines.append("")

    if story.get("setting"):
        content_lines.append("### Setting")
        content_lines.append(f"- **Location**: {story['setting']}")
        content_lines.append(f"- **Theme**: {story['theme']}")
        content_lines.append("")

    if story.get("plot_point"):
        content_lines.append("### Key Plot Point")
        content_lines.append(f"- **Element**: {story['plot_point']}")
        content_lines.append("")

    if story.get("resolution"):
        r = story["resolution"]
        content_lines.append(f"### Resolution ({r['card']})")
        content_lines.append(f"- **Element**: {r['element']}")
        content_lines.append(f"- **Theme**: {r['theme']}")
        content_lines.append("")

    content_lines.append("## Writing Prompt")
    content_lines.append("")
    content_lines.append("Write a story where:")
    content_lines.append("")

    prompt_parts = []
    if story.get("protagonist"):
        p = story["protagonist"]
        prompt_parts.append(
            f"a {p['trait'].lower()} character from the {p['domain'].lower()} domain"
        )

    if story.get("conflict"):
        prompt_parts.append(f"faces {story['conflict'].lower()}")

    if story.get("setting"):
        prompt_parts.append(f"in a {story['setting'].lower()} setting")

    if story.get("theme"):
        prompt_parts.append(f"exploring themes of {story['theme'].lower()}")

    if story.get("resolution"):
        r = story["resolution"]
        prompt_parts.append(f"leading to a {r['element'].lower()} resolution")

    content_lines.append(" ".join(prompt_parts) + ".")
    content_lines.append("")

    content = "\n".join(content_lines)

    # Create a "hand" showing the cards
    players = [Player(name="Story Cards", cards=cards)]

    return generate_deckz_poker(
        title=title,
        content=content,
        output_path=output_path,
        players=players,
        card_format="large",
        show_rules=False,
    )


def example_story_prompt():
    """Generate an example story prompt."""
    print("Drawing story cards...")

    cards = draw_story_cards(5)
    print(f"Drew cards: {', '.join(cards)}")

    story = interpret_cards(cards)
    print(f"\nProtagonist: {story.get('protagonist', {}).get('trait', 'Unknown')}")
    print(f"Conflict: {story.get('conflict', 'Unknown')}")
    print(f"Setting: {story.get('setting', 'Unknown')}")

    output_path = Path("_temp_pdf_examples/story_prompt_from_cards.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_story_prompt_pdf(
        cards=cards, output_path=output_path, title="Creative Writing Prompt"
    )

    print(f"\n✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Card-Based Story Prompt Generator")
    print("=" * 60)
    print()

    example_story_prompt()

    print()
    print("=" * 60)
    print("✅ Story prompt generated!")
    print("=" * 60)
