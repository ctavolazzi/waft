#!/usr/bin/env python3
"""
Card Game Prototype Documentation

Visualize and document card game mechanics, rules, and gameplay.
Perfect for game designers prototyping new card games.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import (
    generate_deckz_poker,
    Player
)


def document_card_game(
    game_name: str,
    rules: str,
    example_hands: List[Dict[str, Any]],
    output_path: Path
) -> Path:
    """
    Document a card game with visual examples.
    
    Args:
        game_name: Name of the game
        rules: Game rules description
        example_hands: List of example hands/scenarios
        output_path: Where to save PDF
    """
    content_lines = []
    content_lines.append(f"# {game_name}")
    content_lines.append("")
    content_lines.append("## Game Rules")
    content_lines.append("")
    content_lines.append(rules)
    content_lines.append("")
    
    if example_hands:
        content_lines.append("## Example Hands")
        content_lines.append("")
        
        players = []
        for i, hand in enumerate(example_hands):
            hand_name = hand.get("name", f"Example Hand {i+1}")
            hand_desc = hand.get("description", "")
            hand_cards = hand.get("cards", [])
            
            if hand_cards:
                players.append(Player(name=hand_name, cards=hand_cards))
                content_lines.append(f"### {hand_name}")
                if hand_desc:
                    content_lines.append(hand_desc)
                content_lines.append("")
    
    content = "\n".join(content_lines)
    
    return generate_deckz_poker(
        title=f"{game_name} - Game Documentation",
        content=content,
        output_path=output_path,
        players=players if players else None,
        card_format="medium",
        show_rules=False
    )


def example_game_prototype():
    """Generate example card game documentation."""
    print("Generating card game prototype documentation...")
    
    game_name = "Memory Palace"
    rules = """
**Memory Palace** is a card game that tests memory and pattern recognition.

## Setup
- Use a standard 52-card deck
- Deal 5 cards to each player
- Place remaining cards face down as draw pile

## Gameplay
1. Players take turns playing cards from their hand
2. When a card is played, all players must remember the sequence
3. If a player can't recall the sequence, they draw a penalty card
4. First player to empty their hand wins

## Special Rules
- **Pairs**: Playing two of the same rank allows you to challenge another player
- **Sequences**: Playing three consecutive cards gives you an extra turn
- **Memory Challenge**: Any player can challenge the sequence at any time
    """
    
    example_hands = [
        {
            "name": "Starting Hand",
            "description": "A typical starting hand with mixed suits and ranks.",
            "cards": ["AS", "7H", "KD", "3C", "10S"]
        },
        {
            "name": "Pair Opportunity",
            "description": "This hand contains a pair (Kings) that can be used for a challenge.",
            "cards": ["KH", "KD", "5C", "9S", "2H"]
        },
        {
            "name": "Sequence Potential",
            "description": "This hand has three consecutive cards (7, 8, 9) for an extra turn.",
            "cards": ["7D", "8C", "9H", "AS", "KD"]
        },
    ]
    
    output_path = Path("_temp_pdf_examples/card_game_prototype.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = document_card_game(
        game_name=game_name,
        rules=rules,
        example_hands=example_hands,
        output_path=output_path
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Card Game Prototype Documentation")
    print("=" * 60)
    print()
    
    example_game_prototype()
    
    print()
    print("=" * 60)
    print("✅ Game prototype documentation generated!")
    print("=" * 60)
