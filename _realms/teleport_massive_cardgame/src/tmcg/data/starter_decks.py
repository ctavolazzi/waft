"""
Starter decks for Teleport Massive Card Game.

Pre-built decks to help players get started.
"""

from ..models.card import Card, Rarity, FrameColor, creature, instant, sorcery, artifact
from ..models.deck import Deck


# =============================================================================
# Card Definitions (matching web/src/data/cards.ts)
# =============================================================================

AZIAH_CALDERON = Card(
    name="Aziah Calderon",
    mana_cost="3UU",
    type_line="Legendary Creature - Human Scientist",
    rarity=Rarity.MYTHIC,
    power=3,
    toughness=4,
    abilities="When Aziah Calderon enters the battlefield, search your library for a card named 'Scint Protocol' and put it into your hand.",
    flavor_text="They said death was final. They said the distance between us was absolute. They must be wrong.",
    frame_color=FrameColor.BLUE,
    art_path="/art/aziah_calderon.png",
)

FAI_WEI = Card(
    name="Fai Wei",
    mana_cost="2WU",
    type_line="Legendary Creature - Human Executive",
    rarity=Rarity.RARE,
    power=2,
    toughness=3,
    abilities="At the beginning of your upkeep, scry 1. Tap: Add one mana of any color.",
    flavor_text="We're not just studying quantum mechanics—we're building the future of transportation.",
    frame_color=FrameColor.MULTICOLOR,
    art_path="/art/fai_wei.png",
)

QUANTUM_ENTANGLEMENT = Card(
    name="Quantum Entanglement",
    mana_cost="2UU",
    type_line="Instant",
    rarity=Rarity.RARE,
    abilities="Target two creatures become entangled until end of turn. Whenever one is dealt damage, the other is dealt the same amount.",
    flavor_text="Distance is an illusion.",
    frame_color=FrameColor.BLUE,
)

SCINT_PROTOCOL = Card(
    name="Scint Protocol",
    mana_cost="3U",
    type_line="Enchantment",
    rarity=Rarity.UNCOMMON,
    abilities="At the beginning of each end step, if a reality fracture occurred this turn, draw a card.",
    flavor_text="The protocol that detects tears in the fabric of existence.",
    frame_color=FrameColor.BLUE,
)

REALITY_FRACTURE = Card(
    name="Reality Fracture",
    mana_cost="1UR",
    type_line="Sorcery",
    rarity=Rarity.RARE,
    abilities="Exile target permanent. Its controller may cast it from exile until end of turn without paying its mana cost.",
    flavor_text="When space folds, anything is possible.",
    frame_color=FrameColor.MULTICOLOR,
)

TELEPORT_MASSIVE_HQ = Card(
    name="Teleport Massive HQ",
    mana_cost="",
    type_line="Land - Corporate",
    rarity=Rarity.RARE,
    abilities="Tap: Add C. 2UU, Tap: Target creature gains 'This creature can't be blocked' until end of turn.",
    flavor_text="The epicenter of quantum transportation research.",
    frame_color=FrameColor.LAND,
)

CHEN_STABILIZATION = Card(
    name="Chen Stabilization Protocol",
    mana_cost="2U",
    type_line="Enchantment",
    rarity=Rarity.UNCOMMON,
    abilities="Creatures you control have hexproof as long as they're entangled with another creature.",
    flavor_text="Dr. Chen's breakthrough made macro-scale quantum states possible.",
    frame_color=FrameColor.BLUE,
)

RESEARCH_AND_DEV = Card(
    name="Research & Development",
    mana_cost="2",
    type_line="Artifact",
    rarity=Rarity.COMMON,
    abilities="Tap, Sacrifice Research & Development: Draw two cards, then discard a card.",
    flavor_text="Where impossible ideas become inevitable realities.",
    frame_color=FrameColor.ARTIFACT,
)

SWAB = Card(
    name="SWAB - Something Without A Beginning",
    mana_cost="4",
    type_line="Legendary Artifact",
    rarity=Rarity.MYTHIC,
    abilities="SWAB has no mana cost and can't be cast. If SWAB would enter your hand from anywhere put it onto the battlefield instead.",
    flavor_text="The curved shape that always was.",
    frame_color=FrameColor.ARTIFACT,
    art_path="/art/swab.png",
)

SWAE = Card(
    name="SWAE - Something Without An End",
    mana_cost="4",
    type_line="Legendary Artifact",
    rarity=Rarity.MYTHIC,
    abilities="SWAE can't leave the battlefield. At the beginning of your upkeep, you may pay 2. If you don't, SWAE deals 1 damage to you.",
    flavor_text="The sharp edge that always will be.",
    frame_color=FrameColor.ARTIFACT,
    art_path="/art/swae.png",
)

THE_VIBRATION = Card(
    name="The Vibration",
    mana_cost="XUB",
    type_line="Sorcery",
    rarity=Rarity.MYTHIC,
    abilities="The Vibration can't be countered. Exile X target permanents. Return them to the battlefield under their owners' control at the beginning of the next end step.",
    flavor_text="The oscillation between existence and nonexistence.",
    frame_color=FrameColor.MULTICOLOR,
)

GRIEVING_SCIENTIST = Card(
    name="Grieving Scientist",
    mana_cost="1U",
    type_line="Creature - Human Scientist",
    rarity=Rarity.COMMON,
    power=1,
    toughness=2,
    abilities="When Grieving Scientist enters the battlefield, look at the top two cards of your library. Put one into your hand and the other into your graveyard.",
    flavor_text="Loss fuels the greatest discoveries.",
    frame_color=FrameColor.BLUE,
)

QUANTUM_OBSERVER = Card(
    name="Quantum Observer",
    mana_cost="2U",
    type_line="Creature - Human Scientist",
    rarity=Rarity.UNCOMMON,
    power=2,
    toughness=2,
    abilities="Flash. When Quantum Observer enters the battlefield, you may tap or untap target permanent.",
    flavor_text="The act of observation changes everything.",
    frame_color=FrameColor.BLUE,
)

LAB_ASSISTANT = Card(
    name="Lab Assistant",
    mana_cost="U",
    type_line="Creature - Human Scientist",
    rarity=Rarity.COMMON,
    power=1,
    toughness=1,
    abilities="When Lab Assistant enters the battlefield, draw a card, then discard a card.",
    flavor_text="Every breakthrough starts with someone willing to fetch coffee.",
    frame_color=FrameColor.BLUE,
)

CORPORATE_SECURITY = Card(
    name="Corporate Security",
    mana_cost="2W",
    type_line="Creature - Human Soldier",
    rarity=Rarity.COMMON,
    power=2,
    toughness=3,
    abilities="Vigilance. Teleport Massive creatures you control have ward 1.",
    flavor_text="Protecting secrets more valuable than gold.",
    frame_color=FrameColor.WHITE,
)

SCINT_DETECTOR = Card(
    name="Scint Detector",
    mana_cost="2",
    type_line="Artifact",
    rarity=Rarity.UNCOMMON,
    abilities="Tap: Look at the top card of your library. You may put it into your graveyard. If a card was put into a graveyard from anywhere this turn, draw a card instead.",
    flavor_text="It measures the tears between moments.",
    frame_color=FrameColor.ARTIFACT,
)

RECURSIVE_TIMELINE = Card(
    name="Recursive Timeline",
    mana_cost="3U",
    type_line="Enchantment",
    rarity=Rarity.RARE,
    abilities="At the beginning of your upkeep, exile the top card of your library. You may play it this turn. At the beginning of your end step, if you didn't play a card exiled this way, put it on the bottom of your library.",
    flavor_text="She's lived this moment before. And she will again.",
    frame_color=FrameColor.BLUE,
)

DR_CHENS_DISCOVERY = Card(
    name="Dr. Chen's Discovery",
    mana_cost="2UU",
    type_line="Instant",
    rarity=Rarity.UNCOMMON,
    abilities="Draw three cards. If you control an entangled creature, draw four cards instead.",
    flavor_text="The stabilization protocol changed everything we thought we knew.",
    frame_color=FrameColor.BLUE,
)

PROBABILITY_COLLAPSE = Card(
    name="Probability Collapse",
    mana_cost="1UU",
    type_line="Instant",
    rarity=Rarity.RARE,
    abilities="Counter target spell. Its controller reveals cards from the top of their library until they reveal a spell with the same mana value, then may cast it without paying its mana cost.",
    flavor_text="Every possibility exists until we choose to look.",
    frame_color=FrameColor.BLUE,
)

ENTANGLED_SOULS = Card(
    name="Entangled Souls",
    mana_cost="3UB",
    type_line="Sorcery",
    rarity=Rarity.RARE,
    abilities="Choose two target creatures. Until end of turn, whenever one of them dies, return the other to its owner's hand. If both would die simultaneously, return both to the battlefield under your control.",
    flavor_text="Connected across any distance, even death.",
    frame_color=FrameColor.MULTICOLOR,
)


# =============================================================================
# Starter Decks
# =============================================================================

def create_quantum_control_deck() -> Deck:
    """
    Create the 'Quantum Control' starter deck.
    
    Theme: Blue-focused control deck centered around Aziah Calderon and
    the quantum mechanics of Teleport Massive. Uses entanglement, observation,
    and reality manipulation to control the game.
    
    Strategy: Control the board early with cheap scientists, draw cards,
    and win with powerful mythic finishers.
    """
    deck = Deck(
        name="Quantum Control",
        description="The official starter deck. Control the board with quantum mechanics and finish with legendary scientists.",
        author="Teleport Massive",
        format="standard",
    )
    
    # Creatures (16)
    deck.add(AZIAH_CALDERON, 1)
    deck.add(FAI_WEI, 1)
    deck.add(GRIEVING_SCIENTIST, 4)
    deck.add(QUANTUM_OBSERVER, 4)
    deck.add(LAB_ASSISTANT, 4)
    deck.add(CORPORATE_SECURITY, 2)
    
    # Instants (8)
    deck.add(QUANTUM_ENTANGLEMENT, 2)
    deck.add(PROBABILITY_COLLAPSE, 2)
    deck.add(DR_CHENS_DISCOVERY, 4)
    
    # Sorceries (4)
    deck.add(REALITY_FRACTURE, 2)
    deck.add(ENTANGLED_SOULS, 2)
    
    # Enchantments (6)
    deck.add(SCINT_PROTOCOL, 2)
    deck.add(CHEN_STABILIZATION, 2)
    deck.add(RECURSIVE_TIMELINE, 2)
    
    # Artifacts (6)
    deck.add(RESEARCH_AND_DEV, 2)
    deck.add(SWAB, 1)
    deck.add(SWAE, 1)
    deck.add(SCINT_DETECTOR, 2)
    
    # Lands (4)
    deck.add(TELEPORT_MASSIVE_HQ, 4)
    
    return deck


def create_the_vibration_deck() -> Deck:
    """
    Create 'The Vibration' starter deck.
    
    Theme: Multicolor deck focused on The Vibration mythic and
    reality-bending effects. Exiles and returns permanents for value.
    """
    deck = Deck(
        name="The Vibration",
        description="An aggressive deck that bends reality to win. Center your strategy around The Vibration.",
        author="Teleport Massive",
        format="standard",
    )
    
    # Creatures (18)
    deck.add(FAI_WEI, 2)
    deck.add(GRIEVING_SCIENTIST, 4)
    deck.add(QUANTUM_OBSERVER, 4)
    deck.add(LAB_ASSISTANT, 4)
    deck.add(CORPORATE_SECURITY, 4)
    
    # The Vibration & Support (8)
    deck.add(THE_VIBRATION, 2)
    deck.add(QUANTUM_ENTANGLEMENT, 4)
    deck.add(REALITY_FRACTURE, 2)
    
    # Card Advantage (8)
    deck.add(RESEARCH_AND_DEV, 4)
    deck.add(DR_CHENS_DISCOVERY, 4)
    
    # Enchantments (4)
    deck.add(SCINT_PROTOCOL, 2)
    deck.add(RECURSIVE_TIMELINE, 2)
    
    # Lands (6)
    deck.add(TELEPORT_MASSIVE_HQ, 4)
    
    return deck


# Convenience dictionary
STARTER_DECKS = {
    "quantum-control": create_quantum_control_deck,
    "the-vibration": create_the_vibration_deck,
}


def get_starter_deck(name: str) -> Deck:
    """Get a starter deck by name."""
    if name not in STARTER_DECKS:
        raise ValueError(f"Unknown starter deck: {name}. Available: {list(STARTER_DECKS.keys())}")
    return STARTER_DECKS[name]()


def list_starter_decks() -> list[str]:
    """List available starter deck names."""
    return list(STARTER_DECKS.keys())
