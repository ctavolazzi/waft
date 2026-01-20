#!/usr/bin/env python3
"""
Poker Session Recap Generator

Generates beautiful PDF recaps of poker sessions with hand visualizations,
statistics, and memorable moments using the deckz_poker wrapper.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import (
    generate_deckz_poker,
    Player
)


class PokerSession:
    """Represents a poker session with hands, players, and outcomes."""
    
    def __init__(
        self,
        date: str,
        game_type: str = "texas_holdem",
        players: List[str] = None,
        hands: List[Dict[str, Any]] = None,
        buy_in: float = 0.0,
        notes: str = ""
    ):
        self.date = date
        self.game_type = game_type
        self.players = players or []
        self.hands = hands or []
        self.buy_in = buy_in
        self.notes = notes
    
    def add_hand(
        self,
        hand_number: int,
        players: List[Player],
        community_cards: Optional[List[str]] = None,
        winner: Optional[str] = None,
        pot_size: float = 0.0,
        notes: str = ""
    ):
        """Add a hand to the session."""
        self.hands.append({
            "hand_number": hand_number,
            "players": players,
            "community_cards": community_cards,
            "winner": winner,
            "pot_size": pot_size,
            "notes": notes
        })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate session statistics."""
        if not self.hands:
            return {}
        
        wins = {}
        total_pots = {}
        
        for hand in self.hands:
            if hand.get("winner"):
                winner = hand["winner"]
                wins[winner] = wins.get(winner, 0) + 1
                total_pots[winner] = total_pots.get(winner, 0.0) + hand.get("pot_size", 0.0)
        
        return {
            "total_hands": len(self.hands),
            "wins_by_player": wins,
            "total_pots_by_player": total_pots,
            "most_wins": max(wins.items(), key=lambda x: x[1])[0] if wins else None,
            "biggest_pot": max((h.get("pot_size", 0.0) for h in self.hands), default=0.0)
        }


def generate_poker_session_recap(
    session: PokerSession,
    output_path: Path,
    include_rules: bool = False
) -> Path:
    """
    Generate a PDF recap of a poker session.
    
    Args:
        session: PokerSession object with session data
        output_path: Where to save the PDF
        include_rules: Whether to include poker rules section
        
    Returns:
        Path to generated PDF
    """
    # Build content
    content_lines = []
    
    # Session header
    content_lines.append(f"# Poker Session Recap")
    content_lines.append("")
    content_lines.append(f"**Date**: {session.date}")
    content_lines.append(f"**Game Type**: {session.game_type.replace('_', ' ').title()}")
    content_lines.append(f"**Players**: {', '.join(session.players)}")
    content_lines.append(f"**Total Hands**: {len(session.hands)}")
    content_lines.append("")
    
    # Statistics
    stats = session.get_statistics()
    if stats:
        content_lines.append("## Session Statistics")
        content_lines.append("")
        if stats.get("most_wins"):
            content_lines.append(f"**Most Wins**: {stats['most_wins']} ({stats['wins_by_player'][stats['most_wins']]} hands)")
        if stats.get("biggest_pot"):
            content_lines.append(f"**Biggest Pot**: ${stats['biggest_pot']:.2f}")
        content_lines.append("")
        
        if stats.get("wins_by_player"):
            content_lines.append("### Win Summary")
            content_lines.append("")
            for player, wins in sorted(stats["wins_by_player"].items(), key=lambda x: x[1], reverse=True):
                content_lines.append(f"- {player}: {wins} wins")
            content_lines.append("")
    
    # Memorable hands section
    if session.hands:
        content_lines.append("## Memorable Hands")
        content_lines.append("")
        
        # Find interesting hands (big pots, special hands, etc.)
        memorable_hands = []
        for hand in session.hands:
            if hand.get("pot_size", 0) > 50 or hand.get("notes"):
                memorable_hands.append(hand)
        
        if not memorable_hands and session.hands:
            # If no specific memorable hands, show last 3 hands
            memorable_hands = session.hands[-3:]
        
        for hand in memorable_hands:
            content_lines.append(f"### Hand #{hand['hand_number']}")
            content_lines.append("")
            if hand.get("pot_size"):
                content_lines.append(f"**Pot**: ${hand['pot_size']:.2f}")
            if hand.get("winner"):
                content_lines.append(f"**Winner**: {hand['winner']}")
            if hand.get("notes"):
                content_lines.append(f"**Notes**: {hand['notes']}")
            content_lines.append("")
    
    # Session notes
    if session.notes:
        content_lines.append("## Session Notes")
        content_lines.append("")
        content_lines.append(session.notes)
        content_lines.append("")
    
    content = "\n".join(content_lines)
    
    # Collect all players and hands for visualization
    all_players = []
    all_community_cards = []
    
    # Use the most recent hand for the main visualization
    if session.hands:
        last_hand = session.hands[-1]
        all_players = last_hand.get("players", [])
        all_community_cards = last_hand.get("community_cards")
    
    # Generate PDF
    return generate_deckz_poker(
        title=f"Poker Session - {session.date}",
        content=content,
        output_path=output_path,
        game_type=session.game_type,
        players=all_players if all_players else None,
        community_cards=all_community_cards,
        card_format="medium",
        show_rules=include_rules
    )


def example_session():
    """Generate an example poker session recap."""
    print("Generating example poker session recap...")
    
    # Create a sample session
    session = PokerSession(
        date="2026-01-19",
        game_type="texas_holdem",
        players=["Alice", "Bob", "Carol", "Dave"],
        buy_in=20.0,
        notes="Great session! Lots of action and memorable hands."
    )
    
    # Add some hands
    session.add_hand(
        hand_number=1,
        players=[
            Player(name="Alice", cards=["AS", "AD"]),
            Player(name="Bob", cards=["KS", "KD"]),
            Player(name="Carol", cards=["QS", "QD"]),
        ],
        community_cards=["AC", "KH", "QC", "10S", "9H"],
        winner="Alice",
        pot_size=45.0,
        notes="Alice flopped quad aces!"
    )
    
    session.add_hand(
        hand_number=15,
        players=[
            Player(name="Alice", cards=["10H", "9H"]),
            Player(name="Bob", cards=["8C", "7C"]),
            Player(name="Dave", cards=["6D", "5D"]),
        ],
        community_cards=["7H", "6H", "5H", "4H", "3H"],
        winner="Alice",
        pot_size=120.0,
        notes="Alice made a straight flush on the river!"
    )
    
    session.add_hand(
        hand_number=23,
        players=[
            Player(name="Bob", cards=["JS", "JC"]),
            Player(name="Carol", cards=["JD", "JH"]),
        ],
        community_cards=["10C", "9D", "8S", "7C", "6H"],
        winner="Bob",
        pot_size=35.0,
        notes="Bob's jacks held up against Carol's jacks (better kicker)"
    )
    
    # Generate recap
    output_path = Path("_temp_pdf_examples/poker_session_recap_example.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pdf_path = generate_poker_session_recap(
        session=session,
        output_path=output_path,
        include_rules=True
    )
    
    print(f"✅ Generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Poker Session Recap Generator")
    print("=" * 60)
    print()
    
    example_session()
    
    print()
    print("=" * 60)
    print("✅ Example session recap generated!")
    print("=" * 60)
