#!/usr/bin/env python3
"""
Decision Visualization with Cards

Uses playing cards to visualize decision outcomes, scenarios, and choices.
Each card represents a different option or outcome.
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


def visualize_decision_outcomes(
    decision: str,
    options: List[Dict[str, Any]],
    output_path: Path
) -> Path:
    """
    Visualize decision options as cards.
    
    Args:
        decision: The decision question
        options: List of dicts with 'name', 'description', 'card' (optional)
        output_path: Where to save PDF
    """
    # Map options to cards if not provided
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["H", "D", "C", "S"]
    
    players = []
    content_lines = []
    
    content_lines.append(f"# Decision: {decision}")
    content_lines.append("")
    content_lines.append("## Your Options")
    content_lines.append("")
    
    for i, option in enumerate(options):
        # Assign card if not provided
        if "card" not in option:
            rank_idx = i % len(ranks)
            suit_idx = (i // len(ranks)) % len(suits)
            card = f"{ranks[rank_idx]}{suits[suit_idx]}"
        else:
            card = option["card"]
        
        option_name = option.get("name", f"Option {i+1}")
        option_desc = option.get("description", "")
        
        players.append(Player(name=option_name, cards=[card]))
        
        content_lines.append(f"### {option_name} ({card})")
        if option_desc:
            content_lines.append(option_desc)
        content_lines.append("")
    
    content = "\n".join(content_lines)
    
    return generate_deckz_poker(
        title=f"Decision: {decision}",
        content=content,
        output_path=output_path,
        players=players,
        card_format="medium",
        show_rules=False
    )


def example_decision():
    """Generate an example decision visualization."""
    print("Generating decision visualization...")
    
    decision = "Which project should we prioritize next?"
    
    options = [
        {
            "name": "Build Poker Tools",
            "description": "Expand the poker visualization system with more features. High impact, medium effort.",
            "card": "AS"  # Ace of Spades - best option
        },
        {
            "name": "Create Story Generator",
            "description": "Build a card-based story prompt system. Creative, fun, medium effort.",
            "card": "KH"  # King of Hearts - creative option
        },
        {
            "name": "Tournament Bracket System",
            "description": "Create tournament management with visual brackets. High complexity, high value.",
            "card": "QD"  # Queen of Diamonds - valuable option
        },
        {
            "name": "Hand Analysis Tool",
            "description": "Build poker hand strength calculator. Technical, useful, low effort.",
            "card": "JC"  # Jack of Clubs - technical option
        },
    ]
    
    output_path = Path("_temp_pdf_examples/decision_visualization.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = visualize_decision_outcomes(
        decision=decision,
        options=options,
        output_path=output_path
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Decision Visualization with Cards")
    print("=" * 60)
    print()
    
    example_decision()
    
    print()
    print("=" * 60)
    print("✅ Decision visualization generated!")
    print("=" * 60)
