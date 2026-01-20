#!/usr/bin/env python3
"""
Generate Poker Game Visualization PDF

Simple CLI script to generate poker game visualizations using the Deckz package.
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst import Player, generate_deckz_poker


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate poker game visualization PDFs using Deckz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple hand visualization
  %(prog)s --title "Royal Flush" --output poker.pdf \\
    --player "Alice:AS,KS,QS,JS,10S"

  # Texas Hold'em game state
  %(prog)s --title "Texas Hold'em Game" --output game.pdf \\
    --player "Alice:AS,KH" --player "Bob:QD,JD" \\
    --community "AC,AD,AH,KS,QS" --rules

  # Hand rankings guide
  %(prog)s --title "Poker Hand Rankings" --output rankings.pdf \\
    --player "Royal Flush:AS,KS,QS,JS,10S" \\
    --player "Straight Flush:9H,8H,7H,6H,5H" \\
    --player "Four of a Kind:KD,KC,KH,KS,2D" \\
    --format small --rules

Card Format:
  Cards use format: rank + suit
  - Ranks: A (Ace), 2-9, 10, J (Jack), Q (Queen), K (King)
  - Suits: H (Hearts), D (Diamonds), C (Clubs), S (Spades)
  - Examples: "AS" (Ace of Spades), "10H" (Ten of Hearts), "KD" (King of Diamonds)
        """,
    )

    parser.add_argument("--title", required=True, help="Document title")

    parser.add_argument("--output", "-o", required=True, type=Path, help="Output PDF path")

    parser.add_argument(
        "--player",
        "-p",
        action="append",
        dest="players",
        metavar="NAME:CARD1,CARD2,...",
        help="Add a player with cards (can be used multiple times). Format: NAME:CARD1,CARD2,...",
    )

    parser.add_argument(
        "--community",
        "-c",
        metavar="CARD1,CARD2,...",
        help="Community cards for Texas Hold'em (comma-separated)",
    )

    parser.add_argument(
        "--game-type",
        choices=["texas_holdem", "five_card", "omaha", "seven_card_stud"],
        default="texas_holdem",
        help="Poker game type (default: texas_holdem)",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["inline", "mini", "small", "medium", "large", "square"],
        default="medium",
        dest="card_format",
        help="Card display format (default: medium)",
    )

    parser.add_argument("--rules", "-r", action="store_true", help="Include poker rules section")

    parser.add_argument("--content", help="Additional content to include in the document")

    args = parser.parse_args()

    # Parse players
    players = []
    if args.players:
        for player_str in args.players:
            try:
                name, cards_str = player_str.split(":", 1)
                cards = [c.strip().upper() for c in cards_str.split(",")]
                players.append(Player(name=name.strip(), cards=cards))
            except ValueError:
                parser.error(f"Invalid player format: {player_str}. Use NAME:CARD1,CARD2,...")

    # Parse community cards
    community_cards = None
    if args.community:
        community_cards = [c.strip().upper() for c in args.community.split(",")]

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Generate PDF
    try:
        pdf_path = generate_deckz_poker(
            title=args.title,
            content=args.content or "",
            output_path=args.output,
            game_type=args.game_type,
            players=players if players else None,
            community_cards=community_cards,
            card_format=args.card_format,
            show_rules=args.rules,
        )

        print(f"✅ Generated: {pdf_path}")
        return 0

    except ValueError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
