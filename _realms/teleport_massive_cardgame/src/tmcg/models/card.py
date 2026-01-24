"""
Card model for Teleport Massive Card Game.

Pydantic-based card definition with full validation.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class CardType(str, Enum):
    """Card type enumeration."""
    CREATURE = "Creature"
    INSTANT = "Instant"
    SORCERY = "Sorcery"
    ENCHANTMENT = "Enchantment"
    ARTIFACT = "Artifact"
    LAND = "Land"
    PLANESWALKER = "Planeswalker"


class Rarity(str, Enum):
    """Card rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    MYTHIC = "mythic"


class FrameColor(str, Enum):
    """Card frame colors."""
    WHITE = "white"
    BLUE = "blue"
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    MULTICOLOR = "multicolor"
    ARTIFACT = "artifact"
    LAND = "land"


# Frame color definitions for rendering
FRAME_COLORS = {
    FrameColor.WHITE: {"primary": "#F8F6D8", "secondary": "#F0E6C8", "text": "#1a1a1a"},
    FrameColor.BLUE: {"primary": "#0A6FA3", "secondary": "#084E74", "text": "#ffffff"},
    FrameColor.BLACK: {"primary": "#2D2A24", "secondary": "#1a1714", "text": "#d4d4d4"},
    FrameColor.RED: {"primary": "#C53030", "secondary": "#9B2C2C", "text": "#ffffff"},
    FrameColor.GREEN: {"primary": "#2F6846", "secondary": "#1D4430", "text": "#ffffff"},
    FrameColor.MULTICOLOR: {"primary": "#C9A227", "secondary": "#9F7E1C", "text": "#1a1a1a"},
    FrameColor.ARTIFACT: {"primary": "#8B8589", "secondary": "#6B6569", "text": "#1a1a1a"},
    FrameColor.LAND: {"primary": "#8B7355", "secondary": "#6B5545", "text": "#ffffff"},
}

RARITY_COLORS = {
    Rarity.COMMON: "#1a1a1a",
    Rarity.UNCOMMON: "#707883",
    Rarity.RARE: "#C9A227",
    Rarity.MYTHIC: "#D35400",
}


class Card(BaseModel):
    """
    A card in the Teleport Massive Card Game.
    
    Example:
        card = Card(
            name="Aziah Calderon",
            mana_cost="3UU",
            type_line="Legendary Creature - Human Scientist",
            abilities="When Aziah Calderon enters...",
            power=3,
            toughness=4,
            rarity=Rarity.MYTHIC,
            frame_color=FrameColor.BLUE
        )
    """
    
    # Core fields
    name: str = Field(..., min_length=1, max_length=100, description="Card name")
    mana_cost: str = Field(default="", description="Mana cost (e.g., '3UU', '2WU')")
    type_line: str = Field(..., description="Card type line (e.g., 'Legendary Creature - Human Scientist')")
    
    # Stats (for creatures)
    power: Optional[int] = Field(default=None, ge=0, le=99, description="Creature power")
    toughness: Optional[int] = Field(default=None, ge=0, le=99, description="Creature toughness")
    
    # Text
    abilities: str = Field(default="", description="Card abilities/rules text")
    flavor_text: str = Field(default="", description="Flavor text (italicized)")
    
    # Metadata
    rarity: Rarity = Field(default=Rarity.COMMON, description="Card rarity")
    frame_color: FrameColor = Field(default=FrameColor.ARTIFACT, description="Frame color")
    set_code: str = Field(default="TM", max_length=5, description="Set code")
    collector_number: Optional[int] = Field(default=None, description="Collector number")
    
    # Art
    art_path: Optional[str] = Field(default=None, description="Path to art file")
    art_data: Optional[str] = Field(default=None, description="Base64 encoded art")
    
    # Generation metadata
    count: int = Field(default=1, ge=1, description="Number of copies in deck")
    
    @field_validator("mana_cost")
    @classmethod
    def validate_mana_cost(cls, v: str) -> str:
        """Validate mana cost format."""
        if not v:
            return v
        # Allow formats like: 3UU, 2WU, XUB, etc.
        pattern = r'^[0-9XWUBRG]*$'
        if not re.match(pattern, v.upper()):
            raise ValueError(f"Invalid mana cost format: {v}")
        return v.upper()
    
    @property
    def card_type(self) -> CardType:
        """Extract primary card type from type line."""
        type_lower = self.type_line.lower()
        if "creature" in type_lower:
            return CardType.CREATURE
        elif "instant" in type_lower:
            return CardType.INSTANT
        elif "sorcery" in type_lower:
            return CardType.SORCERY
        elif "enchantment" in type_lower:
            return CardType.ENCHANTMENT
        elif "artifact" in type_lower:
            return CardType.ARTIFACT
        elif "land" in type_lower:
            return CardType.LAND
        elif "planeswalker" in type_lower:
            return CardType.PLANESWALKER
        return CardType.ARTIFACT  # Default
    
    @property
    def is_creature(self) -> bool:
        """Check if card is a creature."""
        return self.card_type == CardType.CREATURE
    
    @property
    def is_legendary(self) -> bool:
        """Check if card is legendary."""
        return "legendary" in self.type_line.lower()
    
    @property
    def cmc(self) -> int:
        """Calculate converted mana cost."""
        if not self.mana_cost:
            return 0
        total = 0
        for char in self.mana_cost:
            if char.isdigit():
                total += int(char)
            elif char in "WUBRG":
                total += 1
            elif char == "X":
                pass  # X counts as 0
        return total
    
    @property
    def colors(self) -> set[str]:
        """Get colors in mana cost."""
        color_chars = set()
        for char in self.mana_cost.upper():
            if char in "WUBRG":
                color_chars.add(char)
        return color_chars
    
    @property
    def frame_colors_dict(self) -> dict:
        """Get frame color definitions."""
        return FRAME_COLORS.get(self.frame_color, FRAME_COLORS[FrameColor.ARTIFACT])
    
    @property
    def rarity_color(self) -> str:
        """Get rarity indicator color."""
        return RARITY_COLORS.get(self.rarity, RARITY_COLORS[Rarity.COMMON])
    
    def has_art(self) -> bool:
        """Check if card has art assigned."""
        return bool(self.art_path or self.art_data)
    
    def __str__(self) -> str:
        """String representation."""
        if self.is_creature and self.power is not None:
            return f"{self.name} ({self.mana_cost}) - {self.type_line} [{self.power}/{self.toughness}]"
        return f"{self.name} ({self.mana_cost}) - {self.type_line}"
    
    def __repr__(self) -> str:
        return f"Card(name='{self.name}', type='{self.type_line}', rarity={self.rarity})"


# Convenience factory functions
def creature(
    name: str,
    mana_cost: str,
    subtypes: str,
    power: int,
    toughness: int,
    abilities: str = "",
    flavor_text: str = "",
    rarity: Rarity = Rarity.COMMON,
    frame_color: FrameColor = FrameColor.ARTIFACT,
    legendary: bool = False,
) -> Card:
    """Create a creature card."""
    prefix = "Legendary " if legendary else ""
    return Card(
        name=name,
        mana_cost=mana_cost,
        type_line=f"{prefix}Creature - {subtypes}",
        power=power,
        toughness=toughness,
        abilities=abilities,
        flavor_text=flavor_text,
        rarity=rarity,
        frame_color=frame_color,
    )


def instant(
    name: str,
    mana_cost: str,
    abilities: str,
    flavor_text: str = "",
    rarity: Rarity = Rarity.COMMON,
    frame_color: FrameColor = FrameColor.ARTIFACT,
) -> Card:
    """Create an instant card."""
    return Card(
        name=name,
        mana_cost=mana_cost,
        type_line="Instant",
        abilities=abilities,
        flavor_text=flavor_text,
        rarity=rarity,
        frame_color=frame_color,
    )


def sorcery(
    name: str,
    mana_cost: str,
    abilities: str,
    flavor_text: str = "",
    rarity: Rarity = Rarity.COMMON,
    frame_color: FrameColor = FrameColor.ARTIFACT,
) -> Card:
    """Create a sorcery card."""
    return Card(
        name=name,
        mana_cost=mana_cost,
        type_line="Sorcery",
        abilities=abilities,
        flavor_text=flavor_text,
        rarity=rarity,
        frame_color=frame_color,
    )


def artifact(
    name: str,
    mana_cost: str,
    abilities: str,
    flavor_text: str = "",
    rarity: Rarity = Rarity.COMMON,
    legendary: bool = False,
) -> Card:
    """Create an artifact card."""
    prefix = "Legendary " if legendary else ""
    return Card(
        name=name,
        mana_cost=mana_cost,
        type_line=f"{prefix}Artifact",
        abilities=abilities,
        flavor_text=flavor_text,
        rarity=rarity,
        frame_color=FrameColor.ARTIFACT,
    )
