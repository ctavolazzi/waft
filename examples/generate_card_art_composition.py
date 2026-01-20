#!/usr/bin/env python3
"""
Card Art Composition Generator

Combines card visualization with image generation concepts to create
visual art compositions. Cards become elements in larger artistic works.
"""

import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import Player, generate_deckz_poker


def create_card_art_composition(
    title: str,
    theme: str,
    card_arrangements: list[dict[str, Any]],
    art_description: str,
    output_path: Path,
) -> Path:
    """
    Create a card art composition - cards arranged as visual art elements.

    Args:
        title: Artwork title
        theme: Artistic theme
        card_arrangements: List of card arrangements (each is a "layer" or "element")
        art_description: Description of the artistic vision
        output_path: Where to save PDF
    """

    content_lines = []
    content_lines.append(f"# {title}")
    content_lines.append("")
    content_lines.append(f"**Theme**: {theme}")
    content_lines.append("**Medium**: Playing Cards + Digital Art")
    content_lines.append("")

    content_lines.append("## Artistic Vision")
    content_lines.append("")
    content_lines.append(art_description)
    content_lines.append("")

    content_lines.append("## Card Composition")
    content_lines.append("")
    content_lines.append("This artwork uses playing cards as visual elements.")
    content_lines.append("Each card arrangement represents a layer or component")
    content_lines.append("of the overall composition.")
    content_lines.append("")

    # Add arrangement descriptions
    for i, arrangement in enumerate(card_arrangements, 1):
        arrangement_name = arrangement.get("name", f"Layer {i}")
        arrangement_desc = arrangement.get("description", "")

        content_lines.append(f"### {arrangement_name}")
        content_lines.append("")
        if arrangement_desc:
            content_lines.append(arrangement_desc)
            content_lines.append("")

    content_lines.append("## Integration with Image Generation")
    content_lines.append("")
    content_lines.append("This card composition can be combined with:")
    content_lines.append("")
    content_lines.append("- **PixelLab**: Generate pixel art characters/scenes")
    content_lines.append("- **Nano-Banana (Gemini)**: Generate background images")
    content_lines.append("- **Card Overlays**: Layer cards over generated images")
    content_lines.append("- **Composition Tools**: Arrange cards in artistic patterns")
    content_lines.append("")
    content_lines.append("The cards provide structure; the images provide atmosphere.")
    content_lines.append("")

    content = "\n".join(content_lines)

    # Create players from arrangements
    players = []
    for arrangement in card_arrangements:
        if "cards" in arrangement:
            players.append(
                Player(name=arrangement.get("name", "Element"), cards=arrangement["cards"])
            )

    return generate_deckz_poker(
        title=title,
        content=content,
        output_path=output_path,
        players=players if players else None,
        card_format="large",
        show_rules=False,
    )


def example_river_king_portrait():
    """Create a card art composition for The River King."""
    print("Generating River King card art composition...")

    title = "The River King's Portrait in Cards"
    theme = "New Orleans, Gambling, The Mississippi"

    art_description = """
This composition visualizes The River King through card arrangements.
Each card represents an aspect of his domain:

- **Spades**: The river, the flow, the passage of time
- **Hearts**: The passion, the jazz, the emotion
- **Diamonds**: The wealth, the stakes, the material
- **Clubs**: The power, the structure, the rules

The cards are arranged to suggest his presence—not a literal portrait,
but a representation of his essence through the medium he commands.
"""

    card_arrangements = [
        {
            "name": "The River (Spades)",
            "description": "Flowing spades represent the Mississippi—constant, powerful, ever-changing.",
            "cards": ["AS", "KS", "QS", "JS", "10S", "9S", "8S"],
        },
        {
            "name": "The Jazz (Hearts)",
            "description": "Hearts pulse with the rhythm of New Orleans jazz—improvisation, syncopation, soul.",
            "cards": ["AH", "KH", "QH", "JH", "10H"],
        },
        {
            "name": "The Stakes (Diamonds)",
            "description": "Diamonds glitter with the wealth at risk—every bet, every wager, every chance.",
            "cards": ["AD", "KD", "QD", "JD", "10D"],
        },
        {
            "name": "The Rules (Clubs)",
            "description": "Clubs stand for the structure—the house edge, the mathematics, the truth.",
            "cards": ["AC", "KC", "QC", "JC", "10C"],
        },
    ]

    output_path = Path("_temp_pdf_examples/river_king_card_art.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = create_card_art_composition(
        title=title,
        theme=theme,
        card_arrangements=card_arrangements,
        art_description=art_description,
        output_path=output_path,
    )

    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_probability_visualization():
    """Create card art that visualizes probability concepts."""
    print("Generating probability visualization art...")

    title = "Probability as Art"
    theme = "Mathematics, Chance, Visual Representation"

    art_description = """
This composition visualizes probability concepts through card arrangements.
Each arrangement represents a different probability distribution:

- **Rare Events**: Few cards, widely spaced (low probability)
- **Common Events**: Many cards, tightly grouped (high probability)
- **Distribution Curves**: Cards arranged in bell curve patterns
- **Randomness**: Cards scattered to show true randomness

The cards become a visual language for understanding probability.
"""

    card_arrangements = [
        {
            "name": "Rare Event (Royal Flush)",
            "description": "Just 4 cards—the rarest of hands. Spaced far apart to show rarity.",
            "cards": ["AS", "KS", "QS", "JS", "10S"],
        },
        {
            "name": "Common Event (One Pair)",
            "description": "Many cards clustered together—the most common outcome.",
            "cards": ["AH", "AD", "KS", "QD", "JC", "10H", "9S", "8C", "7D"],
        },
        {
            "name": "Probability Distribution",
            "description": "Cards arranged to show how probability is distributed across outcomes.",
            "cards": ["2H", "3D", "4C", "5S", "6H", "7D", "8C", "9S", "10H"],
        },
    ]

    output_path = Path("_temp_pdf_examples/probability_card_art.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = create_card_art_composition(
        title=title,
        theme=theme,
        card_arrangements=card_arrangements,
        art_description=art_description,
        output_path=output_path,
    )

    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_combined_with_images():
    """Create a composition that's designed to be combined with generated images."""
    print("Generating card composition for image integration...")

    title = "Cards + Generated Art: The River King's Domain"
    theme = "Mixed Media: Cards + AI-Generated Images"

    art_description = """
This composition is designed to be layered with AI-generated images:

**Layer 1 (Background)**: AI-generated image of New Orleans at night
- Jazz club exterior
- Mississippi River in background
- Neon lights reflecting on wet streets
- Generated using: Nano-Banana (Gemini) or PixelLab

**Layer 2 (Midground)**: Card arrangements (this PDF)
- Cards floating above the scene
- Representing probability flows
- The River King's presence made visible

**Layer 3 (Foreground)**: Additional card elements
- Individual cards as focal points
- Highlighting key moments
- Creating depth and composition

**Integration Method**:
1. Generate background image (Nano-Banana: "New Orleans jazz club at night, Mississippi River, neon lights")
2. Generate character art (PixelLab: "Mysterious figure in velvet jacket, card dealer")
3. Overlay this card composition
4. Composite in image editing software
5. Final artwork: Mixed media card + AI art
"""

    card_arrangements = [
        {
            "name": "Probability Flows",
            "description": "Cards arranged to show how luck flows through the scene.",
            "cards": ["AS", "KS", "QS", "JS", "10S"],
        },
        {
            "name": "The Sacred Hand",
            "description": "The River King's signature hand, floating above the scene.",
            "cards": ["AH", "KH", "QH", "JH", "10H"],
        },
    ]

    content = f"""
# {title}

**Theme**: {theme}

## Artistic Vision

{art_description}

## Card Composition

This PDF contains the card elements that will be composited with generated images.

### Integration Workflow

1. **Generate Background Image**
   - Use Nano-Banana (Gemini): "New Orleans jazz club exterior at night, Mississippi River in background, neon lights, wet streets, atmospheric"
   - Or use PixelLab: Create pixel art scene

2. **Generate Character Art**
   - Use PixelLab: "Mysterious card dealer character, velvet jacket, New Orleans style, pixel art"
   - Or use Nano-Banana: "The River King, demi-god of gambling, New Orleans, mystical"

3. **Composite This Card PDF**
   - Extract card images from this PDF
   - Layer over background
   - Position cards to create composition

4. **Final Artwork**
   - Mixed media: AI-generated images + card visualization
   - Cards provide structure and meaning
   - Images provide atmosphere and setting

## Card Elements

The cards below represent the visual elements that will be integrated.
"""

    players = [
        Player(name="Probability Flows", cards=["AS", "KS", "QS", "JS", "10S"]),
        Player(name="The Sacred Hand", cards=["AH", "KH", "QH", "JH", "10H"]),
    ]

    output_path = Path("_temp_pdf_examples/card_art_with_images.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_deckz_poker(
        title=title,
        content=content,
        output_path=output_path,
        players=players,
        card_format="large",
        show_rules=False,
    )

    print(f"✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Card Art Composition Generator")
    print("=" * 60)
    print()

    example_river_king_portrait()
    print()

    example_probability_visualization()
    print()

    example_combined_with_images()
    print()

    print("=" * 60)
    print("✅ All card art compositions generated!")
    print("=" * 60)
    print()
    print("💡 Next Step: Use image generation tools to create backgrounds")
    print("   and composite with these card arrangements!")
    print("=" * 60)

    # Open PDFs
    import subprocess

    subprocess.run(["open", "_temp_pdf_examples/river_king_card_art.pdf"])
    subprocess.run(["open", "_temp_pdf_examples/probability_card_art.pdf"])
    subprocess.run(["open", "_temp_pdf_examples/card_art_with_images.pdf"])
