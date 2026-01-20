"""
Poker Visualization Package
===========================

Easy-to-use package for generating poker game visualizations.

Quick Start:
    from src.waft.templates.typst.poker import PokerGame
    
    game = PokerGame("My Poker Game")
    game.add_player("Alice", ["AS", "KH"])
    game.add_player("Bob", ["QD", "JD"])
    game.set_community_cards(["AC", "AD", "AH", "KS", "QS"])
    game.generate("output.pdf")
"""

from pathlib import Path
from typing import List, Optional, Literal
from .wrappers.deckz_poker import generate_deckz_poker, Player, CardFormat, GameType


class PokerGame:
    """
    Easy-to-use poker game visualization builder.
    
    Example:
        >>> game = PokerGame("Texas Hold'em Game")
        >>> game.add_player("Alice", ["AS", "KH"])
        >>> game.add_player("Bob", ["QD", "JD"])
        >>> game.set_community_cards(["AC", "AD", "AH"])
        >>> game.generate("game.pdf")
    """
    
    def __init__(
        self,
        title: str,
        game_type: GameType = "texas_holdem",
        card_format: CardFormat = "medium"
    ):
        """
        Initialize a poker game visualization.
        
        Args:
            title: Document title
            game_type: Type of poker game (default: "texas_holdem")
            card_format: Card display format (default: "medium")
        """
        self.title = title
        self.game_type = game_type
        self.card_format = card_format
        self.players: List[Player] = []
        self.community_cards: Optional[List[str]] = None
        self.content: str = ""
        self.show_rules: bool = False
    
    def add_player(self, name: str, cards: List[str]) -> "PokerGame":
        """
        Add a player to the game.
        
        Args:
            name: Player name
            cards: List of card identifiers (e.g., ["AS", "KH"])
            
        Returns:
            Self for method chaining
            
        Example:
            >>> game.add_player("Alice", ["AS", "KH"])
        """
        self.players.append(Player(name=name, cards=cards))
        return self
    
    def set_community_cards(self, cards: List[str]) -> "PokerGame":
        """
        Set community cards (for Texas Hold'em, Omaha, etc.).
        
        Args:
            cards: List of community card identifiers
            
        Returns:
            Self for method chaining
            
        Example:
            >>> game.set_community_cards(["AC", "AD", "AH", "KS", "QS"])
        """
        self.community_cards = cards
        return self
    
    def add_content(self, content: str) -> "PokerGame":
        """
        Add custom content to the document.
        
        Args:
            content: Additional Typst content
            
        Returns:
            Self for method chaining
        """
        if self.content:
            self.content += "\n\n" + content
        else:
            self.content = content
        return self
    
    def include_rules(self, include: bool = True) -> "PokerGame":
        """
        Include poker rules section.
        
        Args:
            include: Whether to include rules (default: True)
            
        Returns:
            Self for method chaining
        """
        self.show_rules = include
        return self
    
    def generate(self, output_path: Path) -> Path:
        """
        Generate the PDF.
        
        Args:
            output_path: Where to save the PDF
            
        Returns:
            Path to generated PDF
            
        Raises:
            ValueError: If validation fails
            RuntimeError: If Typst compilation fails
        """
        return generate_deckz_poker(
            title=self.title,
            content=self.content,
            output_path=Path(output_path),
            game_type=self.game_type,
            players=self.players if self.players else None,
            community_cards=self.community_cards,
            card_format=self.card_format,
            show_rules=self.show_rules
        )


# Convenience functions for common use cases

def quick_hand(
    cards: List[str],
    title: str = "Poker Hand",
    output_path: Path = Path("poker_hand.pdf"),
    card_format: CardFormat = "large"
) -> Path:
    """
    Quick function to visualize a single hand.
    
    Args:
        cards: List of card identifiers
        title: Document title
        output_path: Output PDF path
        card_format: Card display format
        
    Returns:
        Path to generated PDF
        
    Example:
        >>> quick_hand(["AS", "KS", "QS", "JS", "10S"], "Royal Flush")
    """
    game = PokerGame(title, card_format=card_format)
    game.add_player("Hand", cards)
    return game.generate(output_path)


def quick_holdem(
    players: dict,
    community_cards: List[str],
    title: str = "Texas Hold'em Game",
    output_path: Path = Path("holdem_game.pdf"),
    card_format: CardFormat = "medium"
) -> Path:
    """
    Quick function for Texas Hold'em game state.
    
    Args:
        players: Dict mapping player names to their cards
        community_cards: List of community card identifiers
        title: Document title
        output_path: Output PDF path
        card_format: Card display format
        
    Returns:
        Path to generated PDF
        
    Example:
        >>> quick_holdem(
        ...     {"Alice": ["AS", "KH"], "Bob": ["QD", "JD"]},
        ...     ["AC", "AD", "AH", "KS", "QS"]
        ... )
    """
    game = PokerGame(title, game_type="texas_holdem", card_format=card_format)
    for name, cards in players.items():
        game.add_player(name, cards)
    game.set_community_cards(community_cards)
    return game.generate(output_path)


__all__ = ["PokerGame", "quick_hand", "quick_holdem"]
