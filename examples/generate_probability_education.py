#!/usr/bin/env python3
"""
Probability Education with Cards

Uses card visualization to teach probability concepts visually.
Each example demonstrates a probability concept with actual card combinations.
"""

import sys
import random
from pathlib import Path
from typing import List, Dict, Any
from itertools import combinations

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import (
    generate_deckz_poker,
    Player
)


def calculate_hand_probability(hand_type: str) -> Dict[str, Any]:
    """Calculate probability of getting a specific hand type."""
    # Total possible 5-card hands from 52-card deck
    total_hands = 2598960  # C(52,5)
    
    probabilities = {
        "royal_flush": {"count": 4, "probability": 4 / total_hands, "odds": "649,739:1"},
        "straight_flush": {"count": 36, "probability": 36 / total_hands, "odds": "72,192:1"},
        "four_of_a_kind": {"count": 624, "probability": 624 / total_hands, "odds": "4,164:1"},
        "full_house": {"count": 3744, "probability": 3744 / total_hands, "odds": "693:1"},
        "flush": {"count": 5108, "probability": 5108 / total_hands, "odds": "508:1"},
        "straight": {"count": 10200, "probability": 10200 / total_hands, "odds": "254:1"},
        "three_of_a_kind": {"count": 54912, "probability": 54912 / total_hands, "odds": "46:1"},
        "two_pair": {"count": 123552, "probability": 123552 / total_hands, "odds": "20:1"},
        "one_pair": {"count": 1098240, "probability": 1098240 / total_hands, "odds": "1.37:1"},
        "high_card": {"count": 1302540, "probability": 1302540 / total_hands, "odds": "0.995:1"},
    }
    
    return probabilities.get(hand_type, {})


def generate_probability_lesson(
    concept: str,
    examples: List[Dict[str, Any]],
    output_path: Path
) -> Path:
    """Generate a probability education PDF."""
    
    content_lines = []
    content_lines.append(f"# Probability Education: {concept}")
    content_lines.append("")
    content_lines.append("## Concept Overview")
    content_lines.append("")
    
    if concept == "Hand Probabilities":
        content_lines.append("This lesson demonstrates the probability of different poker hands.")
        content_lines.append("Each hand type has a specific probability based on mathematics.")
        content_lines.append("")
        content_lines.append("### Key Insight")
        content_lines.append("")
        content_lines.append("Probability isn't about luck—it's about mathematics. The cards don't")
        content_lines.append("care about your feelings. They follow the laws of probability.")
        content_lines.append("")
    
    elif concept == "Conditional Probability":
        content_lines.append("Conditional probability: What's the chance of something happening")
        content_lines.append("given that something else has already happened?")
        content_lines.append("")
        content_lines.append("### Example: Drawing Cards")
        content_lines.append("")
        content_lines.append("If you already have two aces, what's the probability of getting")
        content_lines.append("another ace? The deck has changed—fewer cards, fewer aces.")
        content_lines.append("")
    
    elif concept == "Expected Value":
        content_lines.append("Expected value: The average outcome if you repeat an action many times.")
        content_lines.append("")
        content_lines.append("### Example: Betting")
        content_lines.append("")
        content_lines.append("If you bet $10 with a 10% chance to win $100, your expected value is:")
        content_lines.append("(0.10 × $100) + (0.90 × $0) = $10")
        content_lines.append("")
        content_lines.append("Over many bets, you'll average $10 per bet. But any single bet")
        content_lines.append("could win $100 or lose $10.")
        content_lines.append("")
    
    # Add examples
    if examples:
        content_lines.append("## Visual Examples")
        content_lines.append("")
        
        for i, example in enumerate(examples, 1):
            example_name = example.get("name", f"Example {i}")
            example_desc = example.get("description", "")
            example_prob = example.get("probability", "")
            
            content_lines.append(f"### {example_name}")
            content_lines.append("")
            if example_desc:
                content_lines.append(example_desc)
                content_lines.append("")
            if example_prob:
                content_lines.append(f"**Probability**: {example_prob}")
                content_lines.append("")
    
    # Add mathematical explanation
    content_lines.append("## The Mathematics")
    content_lines.append("")
    content_lines.append("Probability = (Number of favorable outcomes) / (Total number of outcomes)")
    content_lines.append("")
    content_lines.append("For poker hands:")
    content_lines.append("- Total 5-card hands from 52 cards: 2,598,960")
    content_lines.append("- Each hand type has a specific count")
    content_lines.append("- Probability = Count / 2,598,960")
    content_lines.append("")
    
    content = "\n".join(content_lines)
    
    # Create players from examples
    players = []
    for example in examples:
        if "cards" in example:
            players.append(Player(
                name=example.get("name", "Example"),
                cards=example["cards"]
            ))
    
    return generate_deckz_poker(
        title=f"Probability Education: {concept}",
        content=content,
        output_path=output_path,
        players=players if players else None,
        card_format="medium",
        show_rules=False
    )


def example_hand_probabilities():
    """Generate probability lesson for poker hands."""
    print("Generating hand probabilities lesson...")
    
    examples = [
        {
            "name": "Royal Flush (Rarest)",
            "description": "The rarest hand. Only 4 possible combinations out of 2,598,960 total hands.",
            "cards": ["AS", "KS", "QS", "JS", "10S"],
            "probability": "1 in 649,739 (0.000154%)"
        },
        {
            "name": "Four of a Kind",
            "description": "Four cards of the same rank. Much more common than a royal flush.",
            "cards": ["AH", "AD", "AC", "AS", "KH"],
            "probability": "1 in 4,164 (0.024%)"
        },
        {
            "name": "Full House",
            "description": "Three of a kind plus a pair. A strong but achievable hand.",
            "cards": ["KH", "KD", "KC", "QS", "QD"],
            "probability": "1 in 693 (0.144%)"
        },
        {
            "name": "One Pair (Most Common)",
            "description": "Just one pair. The most common hand type in poker.",
            "cards": ["AH", "AD", "KS", "QD", "JC"],
            "probability": "1 in 1.37 (42.26%)"
        },
    ]
    
    output_path = Path("_temp_pdf_examples/probability_hand_odds.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_probability_lesson(
        concept="Hand Probabilities",
        examples=examples,
        output_path=output_path
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_conditional_probability():
    """Generate conditional probability lesson."""
    print("Generating conditional probability lesson...")
    
    examples = [
        {
            "name": "Starting Hand: Two Aces",
            "description": "You're dealt two aces. What are your odds now?",
            "cards": ["AS", "AD"]
        },
        {
            "name": "After Flop: Still Two Aces",
            "description": "The flop doesn't help. You still have two aces, but now there are fewer cards left.",
            "cards": ["AS", "AD", "KH", "QC", "JD"]
        },
        {
            "name": "Probability Changes",
            "description": "With 47 cards remaining and 2 aces left, probability of getting another ace: 2/47 = 4.26%",
            "cards": ["AS", "AD", "KH", "QC", "JD", "AC"]
        },
    ]
    
    content = """
# Conditional Probability: How Cards Change Odds

## The Concept

Conditional probability asks: "What's the probability of X, given that Y has already happened?"

In poker, every card dealt changes the probabilities for all remaining cards.

## Example: Drawing Aces

### Starting Situation
You're dealt two aces. Great hand! But what are your odds of improving?

### After the Flop
Three community cards are dealt. They don't help you. Now:
- **Cards remaining**: 47 (52 - 2 hole cards - 3 flop cards)
- **Aces remaining**: 2 (4 total - 2 in your hand)
- **Probability of getting another ace**: 2/47 = 4.26%

### The Key Insight
The probability changed! It's no longer 4/52 (7.69%) because:
1. You already have 2 aces
2. 5 cards are already dealt
3. The deck has changed

## Mathematical Formula

P(A | B) = P(A and B) / P(B)

Where:
- A = Event you're interested in (getting an ace)
- B = Condition that's already happened (you have 2 aces, flop is dealt)

## Real-World Application

This is why card counting works in blackjack:
- As cards are dealt, the composition of the remaining deck changes
- High cards remaining = better odds for player
- Low cards remaining = better odds for house

The cards don't have memory, but the deck composition does change!
"""
    
    output_path = Path("_temp_pdf_examples/probability_conditional.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    players = [
        Player(name="Your Hand", cards=["AS", "AD"]),
        Player(name="After Flop", cards=["AS", "AD", "KH", "QC", "JD"]),
    ]
    
    pdf_path = generate_deckz_poker(
        title="Conditional Probability: How Cards Change Odds",
        content=content,
        output_path=output_path,
        players=players,
        card_format="medium",
        show_rules=False
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_expected_value():
    """Generate expected value lesson."""
    print("Generating expected value lesson...")
    
    content = """
# Expected Value: The Mathematics of Betting

## What is Expected Value?

Expected Value (EV) = The average outcome if you repeat an action many, many times.

## Formula

EV = (Probability of Win × Value if Win) + (Probability of Loss × Value if Loss)

## Example 1: Simple Bet

**Bet**: $10  
**Win**: 20% chance to win $50  
**Lose**: 80% chance to lose $10

**Calculation**:
- EV = (0.20 × $50) + (0.80 × -$10)
- EV = $10 + (-$8)
- EV = $2

**Meaning**: Over many bets, you'll average a $2 profit per bet.

## Example 2: Poker Tournament

**Situation**: Final table, 3 players left
- 1st place: $10,000 (33% chance)
- 2nd place: $5,000 (33% chance)  
- 3rd place: $2,500 (33% chance)

**Your Expected Value**:
- EV = (0.33 × $10,000) + (0.33 × $5,000) + (0.33 × $2,500)
- EV = $3,333 + $1,667 + $833
- EV = $5,833

**Meaning**: Your "average" finish is worth $5,833, even though you'll only get one of the three prizes.

## Example 3: The House Edge

**Game**: Roulette (American)
- Bet $10 on red
- Win: 18/38 chance to win $10 (get $20 back)
- Lose: 20/38 chance to lose $10

**Your EV**:
- EV = (18/38 × $10) + (20/38 × -$10)
- EV = $4.74 + (-$5.26)
- EV = -$0.52

**Meaning**: Every $10 bet costs you $0.52 on average. That's the house edge.

## Key Insight

Expected value tells you what will happen *on average* over many repetitions. But any single bet could win big or lose everything. That's the difference between probability (long-term) and luck (short-term).

## The River King's Wisdom

> "The house edge isn't evil—it's mathematics. The cards don't care about your feelings. They follow the laws of probability. But you still have to play your hand."
"""
    
    output_path = Path("_temp_pdf_examples/probability_expected_value.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Show a "betting scenario" with cards
    players = [
        Player(name="Your Hand", cards=["AS", "KH"]),
        Player(name="Opponent", cards=["QD", "JC"]),
    ]
    community_cards = ["10H", "9S", "8C"]
    
    pdf_path = generate_deckz_poker(
        title="Expected Value: The Mathematics of Betting",
        content=content,
        output_path=output_path,
        players=players,
        community_cards=community_cards,
        card_format="small",
        show_rules=False
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Probability Education with Cards")
    print("=" * 60)
    print()
    
    example_hand_probabilities()
    print()
    
    example_conditional_probability()
    print()
    
    example_expected_value()
    print()
    
    print("=" * 60)
    print("✅ All probability lessons generated!")
    print("=" * 60)
    
    # Open all PDFs
    import subprocess
    subprocess.run(["open", "_temp_pdf_examples/probability_hand_odds.pdf"])
    subprocess.run(["open", "_temp_pdf_examples/probability_conditional.pdf"])
    subprocess.run(["open", "_temp_pdf_examples/probability_expected_value.pdf"])
