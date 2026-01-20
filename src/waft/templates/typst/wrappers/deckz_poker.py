"""
Deckz Poker Game Visualization Typst Template Wrapper
======================================================

Python wrapper for generating poker game visualizations using the Deckz Typst package.
Supports Texas Hold'em game states, hand visualizations, and poker rules documentation.

Category: game
Tags: [typst, poker, cards, deckz, visualization]
Source: typst-universe
"""

import re
from pathlib import Path
from typing import Literal, List, Optional
from dataclasses import dataclass

from ..compiler import TypstCompiler


# Type aliases for type safety
CardFormat = Literal["inline", "mini", "small", "medium", "large", "square"]
GameType = Literal["texas_holdem", "five_card", "omaha", "seven_card_stud"]

# Deckz card identifier format: rank (A, 2-9, 10, J, Q, K) + suit (H, D, C, S)
# Pattern: 10 followed by suit, OR single rank character followed by suit
CARD_IDENTIFIER_PATTERN = re.compile(r'^(10|[A2-9JQK])[HDCS]$')


def _validate_card_identifier(card: str) -> bool:
    """
    Validate card identifier matches Deckz format.
    
    Valid format: rank (A, 2-9, 10, J, Q, K) + suit (H=Hearts, D=Diamonds, C=Clubs, S=Spades)
    Special case: "back" for card back (face down)
    Examples: "AS", "10H", "KD", "2C", "back"
    
    Args:
        card: Card identifier string
        
    Returns:
        True if valid, False otherwise
    """
    if not card or not isinstance(card, str):
        return False
    card_upper = card.upper()
    # Allow "back" for card backs
    if card_upper == "BACK":
        return True
    return bool(CARD_IDENTIFIER_PATTERN.match(card_upper))


def _sanitize_typst_content(content: str) -> str:
    """
    Sanitize user-provided content to prevent Typst code injection.
    
    Escapes special Typst characters and wraps content in raw text block.
    
    Args:
        content: User-provided content string
        
    Returns:
        Sanitized content safe for embedding in Typst template
    """
    if not content:
        return ""
    
    # Escape special Typst characters that could cause issues
    # Note: We'll use Typst's raw text syntax to safely embed content
    # This prevents any Typst commands from being executed
    escaped = content.replace("\\", "\\\\")  # Escape backslashes first
    escaped = escaped.replace("\"", "\\\"")  # Escape quotes
    
    # Return as raw text block to prevent any Typst interpretation
    return escaped


def _sanitize_typst_string(text: str) -> str:
    """
    Sanitize a string for safe embedding in Typst string literals.
    
    Args:
        text: String to sanitize
        
    Returns:
        Sanitized string safe for Typst string literals
    """
    if not text:
        return ""
    
    # Escape special characters for Typst strings
    escaped = text.replace("\\", "\\\\")  # Escape backslashes first
    escaped = escaped.replace("\"", "\\\"")  # Escape quotes
    escaped = escaped.replace("\n", " ")  # Replace newlines with spaces
    escaped = escaped.replace("\r", "")  # Remove carriage returns
    
    return escaped


@dataclass
class Player:
    """Player data structure with validation."""
    name: str
    cards: List[str]  # Card identifiers (e.g., ["AS", "KH"])
    
    def __post_init__(self):
        """Validate player data after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Player name must be a non-empty string")
        if not self.cards or not isinstance(self.cards, list):
            raise ValueError("Player cards must be a non-empty list")
        # Validate all card identifiers
        for card in self.cards:
            if not _validate_card_identifier(card):
                raise ValueError(
                    f"Invalid card identifier: {card}. "
                    f"Card must match format: rank (A, 2-9, 10, J, Q, K) + suit (H, D, C, S). "
                    f"Example: 'AS', '10H', 'KD'"
                )


def generate_deckz_poker(
    title: str,
    content: str,
    output_path: Path,
    game_type: GameType = "texas_holdem",
    players: Optional[List[Player]] = None,
    community_cards: Optional[List[str]] = None,
    card_format: CardFormat = "medium",
    show_rules: bool = False,
    **kwargs
) -> Path:
    """
    Generate PDF using Deckz package for poker game visualizations.
    
    This function creates poker game visualizations including hands, game states,
    and optional rules documentation using the Deckz Typst package.
    
    Card Identifier Format:
        Cards must match Deckz format: rank + suit
        - Ranks: A (Ace), 2-9, 10, J (Jack), Q (Queen), K (King)
        - Suits: H (Hearts), D (Diamonds), C (Clubs), S (Spades)
        - Examples: "AS" (Ace of Spades), "10H" (Ten of Hearts), "KD" (King of Diamonds)
    
    Args:
        title: Document title
        content: Custom content (Typst markup) - will be sanitized
        output_path: Where to save the PDF
        game_type: Type of poker game (default: "texas_holdem")
        players: List of Player objects with name and cards (optional)
        community_cards: List of community card identifiers for Hold'em (optional)
        card_format: Card display format (default: "medium")
        show_rules: Include poker rules section (default: False)
        **kwargs: Additional template parameters (unused for now)
        
    Returns:
        Path to generated PDF
        
    Raises:
        ValueError: If card identifiers are invalid or player structure is invalid
        RuntimeError: If Typst compilation fails (from TypstCompiler)
    """
    # Validate game type
    valid_game_types = ["texas_holdem", "five_card", "omaha", "seven_card_stud"]
    if game_type not in valid_game_types:
        raise ValueError(
            f"Invalid game_type: {game_type}. "
            f"Must be one of: {', '.join(valid_game_types)}"
        )
    
    # Validate card format
    valid_formats = ["inline", "mini", "small", "medium", "large", "square"]
    if card_format not in valid_formats:
        raise ValueError(
            f"Invalid card_format: {card_format}. "
            f"Must be one of: {', '.join(valid_formats)}"
        )
    
    # Validate community cards if provided
    if community_cards:
        for card in community_cards:
            if not _validate_card_identifier(card):
                raise ValueError(
                    f"Invalid community card identifier: {card}. "
                    f"Card must match format: rank (A, 2-9, 10, J, Q, K) + suit (H, D, C, S). "
                    f"Example: 'AS', '10H', 'KD'"
                )
    
    # Sanitize title and content
    sanitized_title = _sanitize_typst_string(title)
    sanitized_content = _sanitize_typst_content(content)
    
    # Build Typst content
    typst_content = _build_typst_content(
        title=sanitized_title,
        content=sanitized_content,
        game_type=game_type,
        players=players,
        community_cards=community_cards,
        card_format=card_format,
        show_rules=show_rules
    )
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content, output_path)
    
    return pdf_path


def _build_typst_content(
    title: str,
    content: str,
    game_type: GameType,
    players: Optional[List[Player]],
    community_cards: Optional[List[str]],
    card_format: CardFormat,
    show_rules: bool
) -> str:
    """Build Typst content string for poker game visualization."""
    
    # Start with imports and page setup
    typst_lines = [
        '#import "@preview/deckz:0.3.1"',
        '',
        '#set page(margin: 1in)',
        '#set text(font: "Roboto Slab")',
        '',
        f'= {title}',
        ''
    ]
    
    # Add game state visualization if players provided
    if players:
        typst_lines.append('== Game State')
        typst_lines.append('')
        
        # Render community cards if provided (for Texas Hold'em)
        if community_cards and game_type == "texas_holdem":
            typst_lines.append('=== Community Cards')
            typst_lines.append('')
            # Format cards as positional arguments for deckz.hand()
            cards_args = ', '.join([f'"{card.upper()}"' for card in community_cards])
            typst_lines.append(f'#deckz.hand({cards_args}, format: "{card_format}")')
            typst_lines.append('')
        
        # Render each player's hand
        typst_lines.append('=== Player Hands')
        typst_lines.append('')
        for i, player in enumerate(players, 1):
            sanitized_name = _sanitize_typst_string(player.name)
            typst_lines.append(f'*{sanitized_name}*:')
            typst_lines.append('')
            # Format cards as positional arguments for deckz.hand()
            cards_args = ', '.join([f'"{card.upper()}"' for card in player.cards])
            typst_lines.append(f'#deckz.hand({cards_args}, format: "{card_format}")')
            typst_lines.append('')
    
    # Add rules section if requested
    if show_rules:
        typst_lines.extend(_build_rules_section())
    
    # Add custom content
    if content:
        typst_lines.append('== Additional Content')
        typst_lines.append('')
        # Use raw text block to safely embed user content
        typst_lines.append('```')
        typst_lines.append(content)
        typst_lines.append('```')
        typst_lines.append('')
    
    return '\n'.join(typst_lines)


def _build_rules_section() -> List[str]:
    """Build poker rules documentation section."""
    return [
        '== Poker Hand Rankings',
        '',
        'Poker hands are ranked from highest to lowest:',
        '',
        '1. *Royal Flush*: A, K, Q, J, 10, all of the same suit',
        '2. *Straight Flush*: Five cards in sequence, all of the same suit',
        '3. *Four of a Kind*: Four cards of the same rank',
        '4. *Full House*: Three of a kind plus a pair',
        '5. *Flush*: Five cards of the same suit, not in sequence',
        '6. *Straight*: Five cards in sequence, not all of the same suit',
        '7. *Three of a Kind*: Three cards of the same rank',
        '8. *Two Pair*: Two different pairs',
        '9. *One Pair*: Two cards of the same rank',
        '10. *High Card*: Highest card when no other hand is made',
        '',
        '== Texas Hold\'em Rules',
        '',
        'Texas Hold\'em is played with:',
        '',
        '- Each player receives 2 hole cards (face down)',
        '- 5 community cards are dealt face up in the center',
        '- Players make the best 5-card hand using any combination of their 2 hole cards and the 5 community cards',
        '- Betting rounds occur before the flop (first 3 community cards), after the flop, after the turn (4th card), and after the river (5th card)',
        ''
    ]
