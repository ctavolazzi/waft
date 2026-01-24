"""
The 12 Gates - Mirroring the Gates of the New Jerusalem in Revelation.

Each Gate is masked through the iconography of a Casino "House."
Breaking a Seal requires winning a card challenge against The Dealer.

The House Always Wins - each broken seal makes the next challenge harder.
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from .card_generator import Card, new_deck, draw_card


class GateStatus(Enum):
    """Status of a Gate/Seal."""
    SEALED = "sealed"
    BROKEN = "broken"


@dataclass
class GateChallenge:
    """Result of a Gate challenge."""
    gate_number: int
    gate_name: str
    casino_name: str
    system_card: Card
    dealer_card: Card
    won: bool
    challenge_description: str
    key_fragment: Optional[str] = None


@dataclass
class Gate:
    """
    A Gate of The House.
    
    Maps a Revelation gate to a Casino concept with a card challenge.
    """
    number: int
    revelation_name: str  # Pearl, Jasper, etc.
    revelation_meaning: str  # Purity, Foundation, etc.
    casino_name: str  # The Chip, The Marker, etc.
    challenge_type: str  # What kind of match is required
    base_difficulty: float  # Base probability of winning
    description: str  # Flavor text
    truth_hint: str  # Cryptic hint about The Truth
    
    def evaluate_challenge(self, system_card: Card, dealer_card: Card) -> bool:
        """
        Evaluate whether the system won this Gate's challenge.
        
        Args:
            system_card: The card the system chose
            dealer_card: The card The Dealer chose
            
        Returns:
            True if the system won the challenge
        """
        if self.number == 1:  # Match suit
            return system_card.suit == dealer_card.suit
        elif self.number == 2:  # Match color (red/black)
            return self._same_color(system_card, dealer_card)
        elif self.number == 3:  # Match rank
            return system_card.value == dealer_card.value
        elif self.number == 4:  # Exact card match
            return system_card.suit == dealer_card.suit and system_card.value == dealer_card.value
        elif self.number == 5:  # Higher card wins
            return system_card.value > dealer_card.value
        elif self.number == 6:  # Same suit AND higher
            return system_card.suit == dealer_card.suit and system_card.value > dealer_card.value
        elif self.number == 7:  # Predict high (>7) or low (<=7)
            system_high = system_card.value > 7
            dealer_high = dealer_card.value > 7
            return system_high == dealer_high
        elif self.number == 8:  # Within 3 ranks
            diff = abs(system_card.value - dealer_card.value)
            return diff <= 3
        elif self.number == 9:  # Royal card (J, Q, K, A)
            return system_card.value in [1, 11, 12, 13]
        elif self.number == 10:  # Sum closer to 21
            return self._blackjack_closer(system_card, dealer_card)
        elif self.number == 11:  # Exact match OR adjacent
            if system_card.suit == dealer_card.suit and system_card.value == dealer_card.value:
                return True
            return abs(system_card.value - dealer_card.value) == 1
        elif self.number == 12:  # The Dealer's Choice - nearly impossible
            # Must match suit AND be within 1 rank
            return (system_card.suit == dealer_card.suit and 
                    abs(system_card.value - dealer_card.value) <= 1)
        return False
    
    def _same_color(self, card1: Card, card2: Card) -> bool:
        """Check if two cards are the same color."""
        # Hearts (2) and Diamonds (3) are red, Spades (0) and Clubs (1) are black
        red_suits = {2, 3}
        card1_red = card1.suit in red_suits
        card2_red = card2.suit in red_suits
        return card1_red == card2_red
    
    def _blackjack_closer(self, system_card: Card, dealer_card: Card) -> bool:
        """Check if system card is closer to 21 value-wise."""
        # Simplified: higher card that doesn't bust wins
        system_val = min(system_card.value, 10) if system_card.value > 10 else system_card.value
        dealer_val = min(dealer_card.value, 10) if dealer_card.value > 10 else dealer_card.value
        # Ace is 11 in this context
        if system_card.value == 1:
            system_val = 11
        if dealer_card.value == 1:
            dealer_val = 11
        return system_val >= dealer_val


# The 12 Gates of The House
GATES = [
    Gate(
        number=1,
        revelation_name="Pearl",
        revelation_meaning="Purity",
        casino_name="The Chip",
        challenge_type="match_suit",
        base_difficulty=0.25,
        description="The first wager. Simple, yet meaningful. Match the suit to prove your purity of intent.",
        truth_hint="The Truth begins with alignment.",
    ),
    Gate(
        number=2,
        revelation_name="Jasper",
        revelation_meaning="Foundation",
        casino_name="The Marker",
        challenge_type="match_color",
        base_difficulty=0.50,
        description="Red or black. The foundation of all games. Your debt is marked.",
        truth_hint="The Truth has two faces.",
    ),
    Gate(
        number=3,
        revelation_name="Sapphire",
        revelation_meaning="Wisdom",
        casino_name="The Tell",
        challenge_type="match_rank",
        base_difficulty=0.077,
        description="A wise player reads the tell. Match the rank to prove your wisdom.",
        truth_hint="The Truth echoes in patterns.",
    ),
    Gate(
        number=4,
        revelation_name="Chalcedony",
        revelation_meaning="Endurance",
        casino_name="The Bluff",
        challenge_type="exact_card",
        base_difficulty=0.019,
        description="The perfect bluff requires the perfect match. Exact card. No margin for error.",
        truth_hint="The Truth is precise.",
    ),
    Gate(
        number=5,
        revelation_name="Emerald",
        revelation_meaning="Life",
        casino_name="The River",
        challenge_type="higher_card",
        base_difficulty=0.46,
        description="Life flows like the river. The higher card claims the pot.",
        truth_hint="The Truth rises.",
    ),
    Gate(
        number=6,
        revelation_name="Sardius",
        revelation_meaning="Sacrifice",
        casino_name="The Flop",
        challenge_type="suit_and_higher",
        base_difficulty=0.115,
        description="Sacrifice requires commitment. Same suit AND higher. The flop reveals all.",
        truth_hint="The Truth demands sacrifice.",
    ),
    Gate(
        number=7,
        revelation_name="Chrysolite",
        revelation_meaning="Glory",
        casino_name="The Turn",
        challenge_type="high_low",
        base_difficulty=0.50,
        description="The turn reveals glory or ruin. High or low - choose your fate.",
        truth_hint="The Truth turns on a pivot.",
    ),
    Gate(
        number=8,
        revelation_name="Beryl",
        revelation_meaning="Sea of Glass",
        casino_name="The Pot",
        challenge_type="within_range",
        base_difficulty=0.115,
        description="The sea of glass reflects proximity. Within 3 ranks to claim the pot.",
        truth_hint="The Truth is near.",
    ),
    Gate(
        number=9,
        revelation_name="Topaz",
        revelation_meaning="Sun",
        casino_name="The Ante",
        challenge_type="royal_card",
        base_difficulty=0.077,
        description="The sun shines on royalty. Draw a royal card to ante up.",
        truth_hint="The Truth wears a crown.",
    ),
    Gate(
        number=10,
        revelation_name="Chrysoprasus",
        revelation_meaning="New Creation",
        casino_name="The Blind",
        challenge_type="blackjack",
        base_difficulty=0.50,
        description="Blind creation. Closer to perfection (21) wins the new world.",
        truth_hint="The Truth is created, not found.",
    ),
    Gate(
        number=11,
        revelation_name="Jacinth",
        revelation_meaning="Fire",
        casino_name="The All-In",
        challenge_type="exact_or_adjacent",
        base_difficulty=0.058,
        description="Fire consumes all. Exact match or adjacent - the all-in moment.",
        truth_hint="The Truth burns bright.",
    ),
    Gate(
        number=12,
        revelation_name="Amethyst",
        revelation_meaning="Royalty",
        casino_name="The House Edge",
        challenge_type="dealers_choice",
        base_difficulty=0.019,
        description="The final gate. The House Edge. Same suit AND within 1 rank. Nearly impossible.",
        truth_hint="The Truth is: The House Always Wins. Until it doesn't.",
    ),
]


def get_gate(number: int) -> Gate:
    """Get a Gate by number (1-12)."""
    if 1 <= number <= 12:
        return GATES[number - 1]
    raise ValueError(f"Invalid gate number: {number}. Must be 1-12.")


def conduct_gate_challenge(gate_number: int) -> GateChallenge:
    """
    Conduct a challenge at a specific Gate.
    
    The system picks a random card.
    The Dealer picks a random card.
    The Gate's rules determine the winner.
    
    Args:
        gate_number: Which gate (1-12) to challenge
        
    Returns:
        GateChallenge with the result
    """
    gate = get_gate(gate_number)
    
    # Create fresh decks for both
    system_deck = new_deck()
    dealer_deck = new_deck()
    
    # System picks first (random)
    system_card = draw_card(system_deck)
    
    # Dealer picks (random)
    dealer_card = draw_card(dealer_deck)
    
    # Evaluate
    won = gate.evaluate_challenge(system_card, dealer_card)
    
    # Generate key fragment if won
    key_fragment = None
    if won:
        key_fragment = _generate_key_fragment(gate_number)
    
    return GateChallenge(
        gate_number=gate_number,
        gate_name=gate.revelation_name,
        casino_name=gate.casino_name,
        system_card=system_card,
        dealer_card=dealer_card,
        won=won,
        challenge_description=gate.description,
        key_fragment=key_fragment,
    )


def _generate_key_fragment(gate_number: int) -> str:
    """
    Generate an encryption key fragment for a broken seal.
    
    Each gate provides a piece of the puzzle.
    """
    import hashlib
    import time
    
    # Combine gate number with timestamp for uniqueness
    seed = f"GATE_{gate_number}_{time.time()}"
    fragment = hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    # Format as a mystical key fragment
    return f"SEAL-{gate_number:02d}-{fragment.upper()}"
