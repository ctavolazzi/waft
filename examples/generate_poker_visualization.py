"""
Example: Generate Poker Game Visualizations with Deckz

Demonstrates how to use the deckz_poker wrapper to generate poker game PDFs.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import (
    generate_deckz_poker,
    Player
)


def example_simple_hand():
    """Example 1: Simple hand visualization."""
    print("Generating simple hand visualization...")
    
    players = [
        Player(name="Alice", cards=["AS", "KS", "QS", "JS", "10S"]),  # Royal flush!
    ]
    
    output_path = Path("_temp_pdf_examples/poker_simple_hand.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_deckz_poker(
        title="Royal Flush Example",
        content="This is a royal flush - the highest possible hand in poker!",
        output_path=output_path,
        players=players,
        card_format="large",
        show_rules=True
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_texas_holdem():
    """Example 2: Texas Hold'em game state."""
    print("Generating Texas Hold'em game state...")
    
    players = [
        Player(name="Alice", cards=["AS", "KH"]),
        Player(name="Bob", cards=["QD", "JD"]),
        Player(name="Carol", cards=["10C", "9C"]),
        Player(name="Dave", cards=["2S", "3H"]),
    ]
    
    community_cards = ["AC", "AD", "AH", "KS", "QS"]
    
    output_path = Path("_temp_pdf_examples/poker_texas_holdem.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_deckz_poker(
        title="Texas Hold'em Game State",
        content="Example game state showing 4 players and community cards.",
        output_path=output_path,
        game_type="texas_holdem",
        players=players,
        community_cards=community_cards,
        card_format="medium",
        show_rules=True
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_hand_rankings():
    """Example 3: Poker hand rankings guide."""
    print("Generating poker hand rankings guide...")
    
    # Create examples of different hand types
    players = [
        Player(name="Royal Flush", cards=["AS", "KS", "QS", "JS", "10S"]),
        Player(name="Straight Flush", cards=["9H", "8H", "7H", "6H", "5H"]),
        Player(name="Four of a Kind", cards=["KD", "KC", "KH", "KS", "2D"]),
        Player(name="Full House", cards=["QD", "QC", "QH", "JD", "JC"]),
        Player(name="Flush", cards=["10C", "7C", "5C", "3C", "2C"]),
        Player(name="Straight", cards=["9D", "8S", "7H", "6C", "5D"]),
        Player(name="Three of a Kind", cards=["AD", "AC", "AH", "KS", "2D"]),
        Player(name="Two Pair", cards=["JD", "JC", "9H", "9S", "KD"]),
        Player(name="One Pair", cards=["10D", "10H", "KS", "QD", "2C"]),
        Player(name="High Card", cards=["AS", "KD", "QH", "JC", "9S"]),
    ]
    
    output_path = Path("_temp_pdf_examples/poker_hand_rankings.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_deckz_poker(
        title="Poker Hand Rankings Guide",
        content="Visual guide to poker hand rankings from highest to lowest.",
        output_path=output_path,
        players=players,
        card_format="small",
        show_rules=True
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def example_game_scenario():
    """Example 4: Complete game scenario."""
    print("Generating complete game scenario...")
    
    players = [
        Player(name="Alice", cards=["AS", "AD"]),  # Pocket aces!
        Player(name="Bob", cards=["KS", "KD"]),    # Pocket kings
        Player(name="Carol", cards=["QS", "QD"]),  # Pocket queens
    ]
    
    community_cards = ["AC", "KH", "QC", "10S", "9H"]
    
    output_path = Path("_temp_pdf_examples/poker_game_scenario.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = """
This is a dramatic scenario where:
- Alice has pocket aces (AS, AD) - the best starting hand
- Bob has pocket kings (KS, KD) - second best starting hand
- Carol has pocket queens (QS, QD) - third best starting hand

With the community cards (AC, KH, QC, 10S, 9H):
- Alice makes four aces (best possible hand!)
- Bob makes three kings
- Carol makes three queens

Alice wins with four of a kind!
"""
    
    pdf_path = generate_deckz_poker(
        title="Dramatic Poker Scenario",
        content=content.strip(),
        output_path=output_path,
        game_type="texas_holdem",
        players=players,
        community_cards=community_cards,
        card_format="medium",
        show_rules=False
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


def main():
    """Run all examples."""
    print("=" * 60)
    print("Deckz Poker Visualization Examples")
    print("=" * 60)
    print()
    
    try:
        # Example 1: Simple hand
        example_simple_hand()
        print()
        
        # Example 2: Texas Hold'em
        example_texas_holdem()
        print()
        
        # Example 3: Hand rankings
        example_hand_rankings()
        print()
        
        # Example 4: Game scenario
        example_game_scenario()
        print()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
