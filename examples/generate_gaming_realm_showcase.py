#!/usr/bin/env python3
"""
Gaming and Gambling Realm Showcase

Generates a comprehensive PDF showcasing the entire realm:
- The River King
- All tools
- Example games
- Precedents
- Philosophy
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import Player, generate_deckz_poker


def generate_realm_showcase():
    """Generate comprehensive realm showcase PDF."""

    content = f"""
# Realm of Gaming and Gambling
## Complete Showcase

**Created**: {datetime.now().strftime("%Y-%m-%d")}
**Demi-God**: The River King
**Parent God**: The Magistrate
**Status**: Active

---

## The Realm

The Realm of Gaming and Gambling is a unified space for all things related to games of chance, probability, risk, and luck. It serves as the domain of The River King and houses all tools, documentation, and precedents related to card games, poker, and chance-based activities.

---

## The River King

**Demi-God of Gambling, Luck, and the Mississippi**

The River King presides over this realm, using The Deck of Fates as his sacred tool. He doesn't control luck—he *reads* it. He doesn't make you win—he shows you what the cards already know.

### Sacred Hands

The River King's power manifests through two sacred hands:

1. **The Sacred Hand (Spades)**: Perfect alignment with fate
2. **The Mirror Hand (Hearts)**: Shows what could have been

---

## Tools of the Realm

### 1. The Deck of Fates
The sacred card visualization system. Visualizes cards, hands, and game states with beautiful PDF output.

### 2. Session Recap Generator
Documents poker sessions with statistics, memorable hands, and visualizations.

### 3. Story Prompt Generator
Uses cards to generate creative writing prompts and narrative elements.

### 4. Decision Visualization
Visualizes decision options as cards for project planning.

### 5. Game Prototype Documentation
Documents new card game mechanics with visual examples.

---

## Example: A Game in the Realm

This is an example game documented using The Deck of Fates:

**Players**: Alice, Bob, Carol, Dave
**Game Type**: Texas Hold'em
**Date**: {datetime.now().strftime("%Y-%m-%d")}

The River King witnessed this game and documented it using his sacred tool.

---

## Philosophy

> "The cards don't lie. They just don't always tell you what you want to hear."

**Core Principles**:
- Probability is sacred (mathematics of fate)
- Luck is real (but it's statistics, not magic)
- Every bet matters (the choice, not just the money)
- The house edge is honest (price of the game)
- Fate is written (but you still play your hand)

---

## Precedents

The realm maintains precedents for:
- How games should be documented
- How probability should be visualized
- How luck flows through sessions
- How outcomes should be recorded

All precedents are established by The River King under the authority of The Magistrate.

---

## Integration

This realm integrates with:
- **The Pantheon**: The River King (demi-god), The Magistrate (parent god)
- **Tools**: All poker/gambling visualization systems
- **Realms**: New Orleans, Mississippi River, all places of chance
- **Systems**: Session recap, story generation, decision making

---

*"In the end, we're all just playing the hand we're dealt. The River King just makes sure we can see the cards."*
"""

    # Create example game state
    players = [
        Player(name="Alice", cards=["AS", "AD"]),
        Player(name="Bob", cards=["KS", "KD"]),
        Player(name="Carol", cards=["QS", "QD"]),
        Player(name="Dave", cards=["JS", "JD"]),
    ]

    community_cards = ["10H", "9C", "8D", "7S", "6H"]

    output_path = Path("_temp_pdf_examples/gaming_gambling_realm_showcase.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_deckz_poker(
        title="Realm of Gaming and Gambling - Complete Showcase",
        content=content,
        output_path=output_path,
        game_type="texas_holdem",
        players=players,
        community_cards=community_cards,
        card_format="medium",
        show_rules=True,
    )

    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Generating Gaming and Gambling Realm Showcase")
    print("=" * 60)
    print()

    pdf_path = generate_realm_showcase()

    print(f"✅ Generated: {pdf_path}")
    print()
    print("The Realm is now complete!")
    print("=" * 60)

    # Open the PDF
    import subprocess

    subprocess.run(["open", str(pdf_path)])
