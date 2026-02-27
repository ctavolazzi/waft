"""
Card generator adapter for playingcards.

Encapsulates the playingcards dependency behind small helpers.
"""

from playingcards import Card as PlayingCard
from playingcards import Deck as PlayingDeck

Card = PlayingCard
Deck = PlayingDeck


def new_deck(shuffle: bool = True) -> PlayingDeck:
    """Create a new deck, shuffled by default."""
    deck = PlayingDeck()
    if shuffle:
        deck.shuffle()
    return deck


def draw_card(deck: PlayingDeck) -> PlayingCard:
    """Draw a single card from a deck."""
    return deck.draw_card()


def draw_hand(deck: PlayingDeck, count: int):
    """Draw a hand of cards from a deck."""
    return deck.draw_n(count)


def create_card(value: int, suit: int) -> PlayingCard:
    """Create a specific card by value and suit."""
    return PlayingCard(value=value, suit=suit)
