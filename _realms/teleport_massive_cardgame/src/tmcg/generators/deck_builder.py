"""
DeckBuilder for Teleport Massive Card Game.

Fluent interface for building decks from various sources.
"""

from pathlib import Path
from typing import Optional, Union, Callable

from ..models.card import Card, CardType, Rarity
from ..models.deck import Deck
from .card_generator import CardGenerator


class DeckBuilder:
    """
    Fluent builder for creating Decks.
    
    Example:
        deck = (DeckBuilder()
            .name("Quantum Control")
            .description("Blue control deck featuring Aziah Calderon")
            .load_csv("data/cards.csv")
            .filter(lambda c: c.frame_color == FrameColor.BLUE)
            .add(aziah_card, count=1)
            .add(island_card, count=20)
            .build())
    """
    
    def __init__(self, art_dir: Optional[Path] = None):
        """
        Initialize DeckBuilder.
        
        Args:
            art_dir: Directory containing art files for cards
        """
        self._name = "Unnamed Deck"
        self._description = ""
        self._author = ""
        self._format = "standard"
        self._cards: list[Card] = []
        self._min_size = 40
        self._max_size = 60
        self._max_copies = 4
        self._generator = CardGenerator(art_dir=art_dir)
    
    def name(self, name: str) -> "DeckBuilder":
        """Set deck name."""
        self._name = name
        return self
    
    def description(self, desc: str) -> "DeckBuilder":
        """Set deck description."""
        self._description = desc
        return self
    
    def author(self, author: str) -> "DeckBuilder":
        """Set deck author."""
        self._author = author
        return self
    
    def format(self, fmt: str) -> "DeckBuilder":
        """Set deck format."""
        self._format = fmt
        return self
    
    def min_size(self, size: int) -> "DeckBuilder":
        """Set minimum deck size."""
        self._min_size = size
        return self
    
    def max_size(self, size: int) -> "DeckBuilder":
        """Set maximum deck size."""
        self._max_size = size
        return self
    
    def max_copies(self, copies: int) -> "DeckBuilder":
        """Set maximum copies per card."""
        self._max_copies = copies
        return self
    
    def add(self, card: Card, count: int = 1) -> "DeckBuilder":
        """
        Add a card to the deck.
        
        Args:
            card: Card to add
            count: Number of copies
        """
        for _ in range(count):
            self._cards.append(card.model_copy())
        return self
    
    def add_many(self, cards: list[Card]) -> "DeckBuilder":
        """
        Add multiple cards to the deck.
        
        Args:
            cards: List of cards to add
        """
        self._cards.extend(c.model_copy() for c in cards)
        return self
    
    def load_csv(self, path: Union[str, Path]) -> "DeckBuilder":
        """
        Load cards from a CSV file.
        
        Args:
            path: Path to CSV file
        """
        cards = self._generator.from_csv(path)
        self._cards.extend(cards)
        return self
    
    def load_json(self, path: Union[str, Path]) -> "DeckBuilder":
        """
        Load cards from a JSON file.
        
        Args:
            path: Path to JSON file
        """
        cards = self._generator.from_json_file(path)
        self._cards.extend(cards)
        return self
    
    def load_file(self, path: Union[str, Path]) -> "DeckBuilder":
        """
        Load cards from a file (auto-detect format).
        
        Args:
            path: Path to file
        """
        cards = self._generator.from_file(path)
        self._cards.extend(cards)
        return self
    
    def filter(self, predicate: Callable[[Card], bool]) -> "DeckBuilder":
        """
        Filter cards by predicate.
        
        Args:
            predicate: Function that returns True for cards to keep
        """
        self._cards = [c for c in self._cards if predicate(c)]
        return self
    
    def filter_by_type(self, card_type: CardType) -> "DeckBuilder":
        """Filter cards by type."""
        return self.filter(lambda c: c.card_type == card_type)
    
    def filter_by_rarity(self, rarity: Rarity) -> "DeckBuilder":
        """Filter cards by rarity."""
        return self.filter(lambda c: c.rarity == rarity)
    
    def filter_by_color(self, color: str) -> "DeckBuilder":
        """Filter cards by color in mana cost."""
        return self.filter(lambda c: color.upper() in c.colors)
    
    def filter_by_cmc(self, min_cmc: int = 0, max_cmc: int = 99) -> "DeckBuilder":
        """Filter cards by converted mana cost."""
        return self.filter(lambda c: min_cmc <= c.cmc <= max_cmc)
    
    def remove(self, card_name: str, count: int = 1) -> "DeckBuilder":
        """
        Remove cards by name.
        
        Args:
            card_name: Name of card to remove
            count: Number of copies to remove
        """
        removed = 0
        new_cards = []
        for card in self._cards:
            if card.name == card_name and removed < count:
                removed += 1
            else:
                new_cards.append(card)
        self._cards = new_cards
        return self
    
    def clear(self) -> "DeckBuilder":
        """Remove all cards."""
        self._cards = []
        return self
    
    def sort_by_name(self) -> "DeckBuilder":
        """Sort cards by name."""
        self._cards.sort(key=lambda c: c.name)
        return self
    
    def sort_by_cmc(self) -> "DeckBuilder":
        """Sort cards by converted mana cost."""
        self._cards.sort(key=lambda c: (c.cmc, c.name))
        return self
    
    def sort_by_type(self) -> "DeckBuilder":
        """Sort cards by type."""
        type_order = {t: i for i, t in enumerate(CardType)}
        self._cards.sort(key=lambda c: (type_order.get(c.card_type, 99), c.name))
        return self
    
    def with_art(self, art_dir: Union[str, Path]) -> "DeckBuilder":
        """
        Load art for all cards from directory.
        
        Args:
            art_dir: Directory containing art files
        """
        self._generator.art_dir = Path(art_dir)
        self._cards = [self._generator.with_art_from_dir(c) for c in self._cards]
        return self
    
    def build(self) -> Deck:
        """
        Build the final Deck.
        
        Returns:
            Deck object with all configured cards
        """
        deck = Deck(
            name=self._name,
            description=self._description,
            cards=self._cards,
            min_size=self._min_size,
            max_size=self._max_size,
            max_copies=self._max_copies,
            format=self._format,
            author=self._author,
        )
        return deck
    
    def build_validated(self) -> tuple[Deck, list[str]]:
        """
        Build deck and return validation errors.
        
        Returns:
            Tuple of (Deck, list of validation errors)
        """
        deck = self.build()
        _, errors = deck.is_valid()
        return deck, errors
    
    @property
    def card_count(self) -> int:
        """Current number of cards."""
        return len(self._cards)
    
    @property
    def preview(self) -> str:
        """Preview of current deck state."""
        lines = [
            f"Deck: {self._name}",
            f"Cards: {len(self._cards)}",
            "",
            "Card breakdown:",
        ]
        
        from collections import Counter
        counts = Counter(c.name for c in self._cards)
        for name, count in sorted(counts.items()):
            lines.append(f"  {count}x {name}")
        
        return "\n".join(lines)


# Convenience function
def build_deck(
    name: str,
    cards: list[Card],
    description: str = "",
) -> Deck:
    """Quick way to build a deck from cards."""
    return (DeckBuilder()
        .name(name)
        .description(description)
        .add_many(cards)
        .build())
