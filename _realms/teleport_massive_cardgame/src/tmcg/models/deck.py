"""
Deck model for Teleport Massive Card Game.

A collection of cards with deck-building rules and utilities.
"""

from typing import Optional, Iterator
from pydantic import BaseModel, Field
from collections import Counter

from .card import Card, CardType, Rarity


class DeckStats(BaseModel):
    """Statistics for a deck."""
    total_cards: int = 0
    unique_cards: int = 0
    creatures: int = 0
    spells: int = 0
    lands: int = 0
    artifacts: int = 0
    average_cmc: float = 0.0
    color_distribution: dict[str, int] = Field(default_factory=dict)
    rarity_distribution: dict[str, int] = Field(default_factory=dict)
    cmc_curve: dict[int, int] = Field(default_factory=dict)


class Deck(BaseModel):
    """
    A deck of cards in the Teleport Massive Card Game.
    
    Example:
        deck = Deck(name="Quantum Control")
        deck.add(aziah_card)
        deck.add(fai_wei_card)
        print(deck.stats)
    """
    
    name: str = Field(default="Unnamed Deck", description="Deck name")
    description: str = Field(default="", description="Deck description")
    cards: list[Card] = Field(default_factory=list, description="Cards in deck")
    
    # Deck constraints
    min_size: int = Field(default=40, description="Minimum deck size")
    max_size: int = Field(default=60, description="Maximum deck size")
    max_copies: int = Field(default=4, description="Max copies of non-basic cards")
    
    # Metadata
    format: str = Field(default="standard", description="Game format")
    author: str = Field(default="", description="Deck author")
    
    def add(self, card: Card, count: int = 1) -> "Deck":
        """Add card(s) to the deck."""
        for _ in range(count):
            self.cards.append(card.model_copy())
        return self
    
    def remove(self, card_name: str, count: int = 1) -> "Deck":
        """Remove card(s) from the deck by name."""
        removed = 0
        self.cards = [
            c for c in self.cards 
            if not (c.name == card_name and (removed := removed + 1) <= count)
        ]
        return self
    
    def get_by_name(self, name: str) -> list[Card]:
        """Get all cards with given name."""
        return [c for c in self.cards if c.name == name]
    
    def get_by_type(self, card_type: CardType) -> list[Card]:
        """Get all cards of given type."""
        return [c for c in self.cards if c.card_type == card_type]
    
    def get_by_rarity(self, rarity: Rarity) -> list[Card]:
        """Get all cards of given rarity."""
        return [c for c in self.cards if c.rarity == rarity]
    
    def get_creatures(self) -> list[Card]:
        """Get all creature cards."""
        return self.get_by_type(CardType.CREATURE)
    
    def get_spells(self) -> list[Card]:
        """Get all instant and sorcery cards."""
        return [c for c in self.cards if c.card_type in (CardType.INSTANT, CardType.SORCERY)]
    
    def get_lands(self) -> list[Card]:
        """Get all land cards."""
        return self.get_by_type(CardType.LAND)
    
    @property
    def size(self) -> int:
        """Total number of cards in deck."""
        return len(self.cards)
    
    @property
    def unique_cards_list(self) -> list[Card]:
        """Get unique cards (no duplicates)."""
        seen = set()
        unique = []
        for card in self.cards:
            if card.name not in seen:
                seen.add(card.name)
                unique.append(card)
        return unique
    
    @property
    def card_counts(self) -> dict[str, int]:
        """Get count of each card by name."""
        return dict(Counter(c.name for c in self.cards))
    
    @property
    def stats(self) -> DeckStats:
        """Calculate deck statistics."""
        if not self.cards:
            return DeckStats()
        
        # Count by type
        creatures = len(self.get_creatures())
        spells = len(self.get_spells())
        lands = len(self.get_lands())
        artifacts = len(self.get_by_type(CardType.ARTIFACT))
        
        # Color distribution
        colors: Counter[str] = Counter()
        for card in self.cards:
            for color in card.colors:
                colors[color] += 1
        
        # Rarity distribution
        rarities = Counter(c.rarity.value for c in self.cards)
        
        # CMC curve (excluding lands)
        non_lands = [c for c in self.cards if c.card_type != CardType.LAND]
        cmc_curve = Counter(c.cmc for c in non_lands)
        
        # Average CMC
        avg_cmc = sum(c.cmc for c in non_lands) / len(non_lands) if non_lands else 0.0
        
        return DeckStats(
            total_cards=self.size,
            unique_cards=len(self.unique_cards_list),
            creatures=creatures,
            spells=spells,
            lands=lands,
            artifacts=artifacts,
            average_cmc=round(avg_cmc, 2),
            color_distribution=dict(colors),
            rarity_distribution=dict(rarities),
            cmc_curve=dict(sorted(cmc_curve.items())),
        )
    
    def is_valid(self) -> tuple[bool, list[str]]:
        """
        Check if deck is valid according to rules.
        Returns (is_valid, list of errors).
        """
        errors = []
        
        # Check size
        if self.size < self.min_size:
            errors.append(f"Deck has {self.size} cards, minimum is {self.min_size}")
        if self.size > self.max_size:
            errors.append(f"Deck has {self.size} cards, maximum is {self.max_size}")
        
        # Check max copies (excluding basic lands)
        for name, count in self.card_counts.items():
            card = self.get_by_name(name)[0]
            # Allow unlimited basic lands
            if "basic" in card.type_line.lower() and "land" in card.type_line.lower():
                continue
            if count > self.max_copies:
                errors.append(f"'{name}' has {count} copies, maximum is {self.max_copies}")
        
        return len(errors) == 0, errors
    
    def shuffle(self) -> "Deck":
        """Shuffle the deck (in-place)."""
        import random
        random.shuffle(self.cards)
        return self
    
    def draw(self, count: int = 1) -> list[Card]:
        """Draw cards from top of deck."""
        drawn = self.cards[:count]
        self.cards = self.cards[count:]
        return drawn
    
    def __iter__(self) -> Iterator[Card]:
        """Iterate over cards."""
        return iter(self.cards)
    
    def __len__(self) -> int:
        """Deck size."""
        return self.size
    
    def __contains__(self, card_name: str) -> bool:
        """Check if card is in deck by name."""
        return any(c.name == card_name for c in self.cards)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Deck('{self.name}', {self.size} cards)"
    
    def __repr__(self) -> str:
        return f"Deck(name='{self.name}', size={self.size}, unique={len(self.unique_cards_list)})"
    
    def to_decklist(self) -> str:
        """Export as decklist text format."""
        lines = [f"// {self.name}", f"// {self.description}" if self.description else ""]
        lines.append("")
        
        # Group by type
        for card_type in CardType:
            type_cards = self.get_by_type(card_type)
            if type_cards:
                lines.append(f"// {card_type.value}s ({len(type_cards)})")
                for name, count in sorted(Counter(c.name for c in type_cards).items()):
                    lines.append(f"{count}x {name}")
                lines.append("")
        
        return "\n".join(lines)
