"""
CardGenerator factory for Teleport Massive Card Game.

Creates cards from various data sources with validation and art integration.
"""

import csv
import json
import base64
from pathlib import Path
from typing import Optional, Union

from ..models.card import Card, Rarity, FrameColor


class CardGenerator:
    """
    Factory class for generating Card objects.
    
    Example:
        generator = CardGenerator()
        
        # From dict
        card = generator.from_dict({
            "name": "Aziah Calderon",
            "mana_cost": "3UU",
            "type_line": "Legendary Creature - Human Scientist",
            "power": 3,
            "toughness": 4,
        })
        
        # From CSV row
        card = generator.from_csv_row(row)
        
        # With art
        card = generator.with_art(card, "path/to/art.png")
    """
    
    def __init__(self, art_dir: Optional[Path] = None):
        """
        Initialize CardGenerator.
        
        Args:
            art_dir: Directory containing art files
        """
        self.art_dir = Path(art_dir) if art_dir else None
        self._art_cache: dict[str, str] = {}  # name -> base64 data
    
    def from_dict(self, data: dict) -> Card:
        """
        Create a Card from a dictionary.
        
        Args:
            data: Dictionary with card fields
            
        Returns:
            Card object
        """
        # Normalize field names (handle CSV column variations)
        normalized = self._normalize_dict(data)
        
        # Parse rarity
        rarity_str = normalized.get("rarity", "common").lower()
        rarity = Rarity(rarity_str) if rarity_str in [r.value for r in Rarity] else Rarity.COMMON
        
        # Parse frame color
        frame_str = normalized.get("frame_color", "artifact").lower()
        frame_color = FrameColor(frame_str) if frame_str in [f.value for f in FrameColor] else FrameColor.ARTIFACT
        
        # Parse power/toughness
        power = self._parse_int(normalized.get("power"))
        toughness = self._parse_int(normalized.get("toughness"))
        
        # Create card
        card = Card(
            name=normalized.get("name", "Unknown"),
            mana_cost=normalized.get("mana_cost", ""),
            type_line=normalized.get("type_line", "Unknown"),
            power=power,
            toughness=toughness,
            abilities=normalized.get("abilities", ""),
            flavor_text=normalized.get("flavor_text", ""),
            rarity=rarity,
            frame_color=frame_color,
            set_code=normalized.get("set_code", "TM"),
            art_path=normalized.get("art_path"),
            count=self._parse_int(normalized.get("count")) or 1,
        )
        
        # Load art if available
        if self.art_dir and card.name:
            card = self.with_art_from_dir(card)
        
        return card
    
    def from_csv_row(self, row: dict) -> Card:
        """
        Create a Card from a CSV row.
        
        Args:
            row: Dictionary from csv.DictReader
            
        Returns:
            Card object
        """
        return self.from_dict(row)
    
    def from_json(self, json_str: str) -> Card:
        """
        Create a Card from JSON string.
        
        Args:
            json_str: JSON string with card data
            
        Returns:
            Card object
        """
        data = json.loads(json_str)
        return self.from_dict(data)
    
    def from_file(self, path: Union[str, Path]) -> list[Card]:
        """
        Load cards from a file (CSV or JSON).
        
        Args:
            path: Path to file
            
        Returns:
            List of Card objects
        """
        path = Path(path)
        
        if path.suffix.lower() == ".csv":
            return self.from_csv(path)
        elif path.suffix.lower() == ".json":
            return self.from_json_file(path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
    
    def from_csv(self, path: Union[str, Path]) -> list[Card]:
        """
        Load cards from a CSV file.
        
        Args:
            path: Path to CSV file
            
        Returns:
            List of Card objects
        """
        path = Path(path)
        cards = []
        
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                count = self._parse_int(row.get("Count") or row.get("count")) or 1
                card = self.from_csv_row(row)
                # Add multiple copies based on count
                for _ in range(count):
                    cards.append(card.model_copy())
        
        return cards
    
    def from_json_file(self, path: Union[str, Path]) -> list[Card]:
        """
        Load cards from a JSON file.
        
        Args:
            path: Path to JSON file
            
        Returns:
            List of Card objects
        """
        path = Path(path)
        
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return [self.from_dict(d) for d in data]
        elif isinstance(data, dict) and "cards" in data:
            return [self.from_dict(d) for d in data["cards"]]
        else:
            return [self.from_dict(data)]
    
    def with_art(self, card: Card, art_path: Union[str, Path]) -> Card:
        """
        Add art to a card from file.
        
        Args:
            card: Card to add art to
            art_path: Path to art file
            
        Returns:
            Card with art_data populated
        """
        art_path = Path(art_path)
        
        if not art_path.exists():
            return card
        
        # Read and encode art
        art_data = base64.b64encode(art_path.read_bytes()).decode("utf-8")
        
        # Create new card with art
        return card.model_copy(update={
            "art_path": str(art_path),
            "art_data": art_data,
        })
    
    def with_art_from_dir(self, card: Card) -> Card:
        """
        Try to find and load art for a card from art_dir.
        
        Looks for files matching card name (normalized).
        
        Args:
            card: Card to add art to
            
        Returns:
            Card with art_data if found
        """
        if not self.art_dir or not self.art_dir.exists():
            return card
        
        # Check cache first
        if card.name in self._art_cache:
            return card.model_copy(update={"art_data": self._art_cache[card.name]})
        
        # Normalize name for file matching
        normalized_name = card.name.lower().replace(" ", "_").replace("-", "_")
        normalized_name = "".join(c for c in normalized_name if c.isalnum() or c == "_")
        
        # Try to find matching art file
        for ext in [".png", ".jpg", ".jpeg", ".gif"]:
            art_path = self.art_dir / f"{normalized_name}{ext}"
            if art_path.exists():
                card = self.with_art(card, art_path)
                self._art_cache[card.name] = card.art_data
                return card
        
        return card
    
    def _normalize_dict(self, data: dict) -> dict:
        """Normalize dictionary keys to snake_case."""
        normalized = {}
        
        # Key mappings (CSV columns -> model fields)
        mappings = {
            "name": ["name", "Name", "card_name", "CardName"],
            "mana_cost": ["mana_cost", "ManaCost", "mana", "cost", "Mana"],
            "type_line": ["type_line", "TypeLine", "type", "Type", "card_type"],
            "power": ["power", "Power", "p"],
            "toughness": ["toughness", "Toughness", "t"],
            "abilities": ["abilities", "Abilities", "rules", "Rules", "text", "Text"],
            "flavor_text": ["flavor_text", "FlavorText", "flavor", "Flavor"],
            "rarity": ["rarity", "Rarity"],
            "frame_color": ["frame_color", "FrameColor", "color", "Color"],
            "set_code": ["set_code", "SetCode", "SetSymbol", "set_symbol"],
            "art_path": ["art_path", "ArtPath", "art", "Art", "image", "Image"],
            "count": ["count", "Count", "copies", "Copies", "quantity"],
        }
        
        for target, sources in mappings.items():
            for source in sources:
                if source in data and data[source]:
                    normalized[target] = data[source]
                    break
        
        return normalized
    
    def _parse_int(self, value: Optional[str]) -> Optional[int]:
        """Safely parse integer from string."""
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None


# Convenience function
def generate_card(**kwargs) -> Card:
    """Generate a single card from keyword arguments."""
    return CardGenerator().from_dict(kwargs)
