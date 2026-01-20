#!/usr/bin/env python3
"""
The River King - New Orleans Demi-God of Gambling

Creates documentation for a demi-god who uses card visualization as their sacred tool.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import Player, generate_deckz_poker


def create_river_king_profile():
    """Create The River King's profile and sacred tool documentation."""

    # The River King's sacred hand - always the same, representing his power
    sacred_hand = ["AS", "KS", "QS", "JS", "10S"]  # Royal Flush of Spades

    # His "reading" cards - cards he uses to see fate
    reading_cards = ["AH", "KD", "QC", "JH", "10H"]  # Royal Flush of Hearts (mirror)

    content = """
# The River King
## Demi-God of Gambling, Luck, and the Mississippi

**Domain**: Gambling, Luck, Probability, Risk  
**Realm**: New Orleans, The River, All Places of Chance  
**Parent God**: The Magistrate (God of Precedent and Body of Proof)  
**Sacred Tool**: The Deck of Fates (Card Visualization System)

---

## The Legend

The River King was born from the convergence of three forces:
- The **Mississippi River** (flow, change, the passage of time)
- The **Jazz** that flows through New Orleans (improvisation, chance, syncopation)
- The **Voodoo** traditions (fate, spirits, the thin veil between worlds)

He doesn't control luck—he *reads* it. He doesn't make you win—he shows you what the cards already know.

---

## Appearance

The River King appears as:
- A tall figure in a worn velvet jacket the color of river mud
- Eyes that shift like the Mississippi—sometimes brown, sometimes gold, sometimes reflecting the cards
- Hands that move with the fluidity of a jazz pianist
- A deck of cards that seems to shuffle itself
- The faint smell of bourbon, cigar smoke, and river water

He's never far from:
- A jazz club
- A riverboat
- A back-alley game
- Anywhere people are taking chances

---

## The Sacred Tool: The Deck of Fates

The River King's power manifests through **The Deck of Fates**—a card visualization system that reveals the hidden patterns of probability and fate.

### How It Works

When The River King draws cards, they don't just show what *is*—they show what *could be*. Each card represents:

- **Ace of Spades**: The beginning, the first bet, the moment of decision
- **King of Spades**: Authority, the house, the one who sets the rules
- **Queen of Spades**: Wisdom, the one who knows the odds
- **Jack of Spades**: The wild card, the unpredictable element
- **Ten of Spades**: Completion, the final outcome, the river card

### The Royal Flush of Spades

The River King's signature hand—a Royal Flush of Spades—represents perfect alignment with fate. When this hand appears, it means:

1. **All forces are aligned** - The universe has spoken
2. **The outcome is certain** - But which outcome? That's the mystery
3. **A moment of transformation** - Something fundamental is about to change
4. **The thin veil** - The boundary between worlds is at its thinnest

### The Mirror Hand (Hearts)

The Royal Flush of Hearts is the mirror—the same power, but inverted. Where Spades show what *will* happen, Hearts show what *could have been*.

---

## Powers and Abilities

### 1. Reading the River
The River King can see probability flows like currents in the Mississippi. He doesn't change outcomes—he reads them.

### 2. The Card's Truth
Any card drawn in his presence reveals its deeper meaning:
- Not just "Ace of Spades"
- But "The moment of decision, weighted with consequence"

### 3. Luck's Current
He can sense when luck is flowing toward or away from someone. He can't control it, but he can *show* it.

### 4. The House Always Wins
He understands that probability isn't fair—it just *is*. The house edge isn't evil, it's mathematics made manifest.

### 5. The Final Bet
When someone makes their last bet, The River King is there. Not to save them, but to witness. To make sure the cards are read true.

---

## Philosophy

> "The cards don't lie. They just don't always tell you what you want to hear."

The River King believes:
- **Probability is sacred** - It's the mathematics of fate
- **Luck is real** - But it's not magic, it's statistics
- **Every bet matters** - Not because of the money, but because of the choice
- **The house edge is honest** - It's the price of the game
- **Fate is written** - But you still have to play your hand

---

## Relationship to The Magistrate

As a demi-god under The Magistrate (God of Precedent and Body of Proof), The River King maintains:

- **The Precedent of Probability**: Every game follows rules, every outcome creates precedent
- **The Body of Proof**: He collects evidence of how luck flows, how probability manifests
- **The Record of Bets**: Every wager is documented, every outcome recorded

The Magistrate provides structure; The River King provides the *flow*.

---

## Sacred Rituals

### The Shuffle
Before any important game, The River King performs The Shuffle—a ritual that ensures the cards are truly random, that fate hasn't been tampered with.

### The Reading
When someone needs to know their odds, The River King draws cards and reads them. Not fortune-telling—*probability-telling*.

### The Witness
When someone makes their final bet, The River King witnesses. He doesn't interfere. He just makes sure the cards are read true, that the outcome is honest.

---

## The Tool in Action

The Deck of Fates (this card visualization system) allows The River King to:

1. **Document Games**: Record every hand, every outcome, every moment of chance
2. **Reveal Patterns**: Show how probability flows through a session
3. **Create Precedents**: Establish how games should be documented
4. **Witness Truth**: Ensure that what happened is what's recorded

It's not just a tool—it's a *sacred artifact* that makes the invisible visible.

---

## Invocation

To call upon The River King:

> "River King, read the cards true.  
> Show me what the odds already know.  
> Let the deck speak, let fate flow.  
> Witness this moment, make it so."

But remember: He shows you the truth. He doesn't change it.

---

## Domain

The River King's influence extends to:
- All games of chance (poker, blackjack, roulette, dice)
- All places of gambling (casinos, riverboats, back alleys, online)
- All moments of risk (not just money—any bet, any chance)
- The Mississippi River and all its tributaries
- New Orleans and all cities built on chance

---

## The Paradox

The River King embodies a paradox:
- He's the god of luck, but he can't control it
- He reads fate, but he doesn't write it
- He witnesses outcomes, but he doesn't determine them
- He understands probability perfectly, but he still plays the game

This is his power: **He makes the invisible visible, but he doesn't change what's already written.**

---

*"In the end, we're all just playing the hand we're dealt. The River King just makes sure we can see the cards."*
"""

    # Create players representing The River King's power
    players = [
        Player(name="The Sacred Hand (Spades)", cards=sacred_hand),
        Player(name="The Mirror Hand (Hearts)", cards=reading_cards),
    ]

    output_path = Path("_temp_pdf_examples/the_river_king.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_deckz_poker(
        title="The River King - Demi-God of Gambling",
        content=content,
        output_path=output_path,
        players=players,
        card_format="large",
        show_rules=False,
    )

    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Creating The River King - Demi-God of Gambling")
    print("=" * 60)
    print()

    pdf_path = create_river_king_profile()

    print(f"✅ Created: {pdf_path}")
    print()
    print("The River King's sacred tool is now documented!")
    print("=" * 60)

    # Open the PDF
    import subprocess

    subprocess.run(["open", str(pdf_path)])
