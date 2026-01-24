"""
ArtGenerator for Teleport Massive Card Game.

Integrates with PixelLab MCP to generate pixel art for cards.
Note: Actual PixelLab calls are made via MCP tools, not direct API.
This class provides the interface and art management.
"""

import base64
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ArtStyle(str, Enum):
    """Pixel art style presets."""
    CHARACTER = "character"  # For creature cards
    OBJECT = "object"        # For artifacts/items
    SPELL = "spell"          # For instant/sorcery effects
    LANDSCAPE = "landscape"  # For lands


class ArtSize(int, Enum):
    """Art size presets."""
    SMALL = 32
    MEDIUM = 48
    LARGE = 64
    XLARGE = 96


@dataclass
class ArtRequest:
    """Request for art generation."""
    card_name: str
    description: str
    style: ArtStyle
    size: ArtSize = ArtSize.LARGE
    
    # Character-specific
    n_directions: int = 4
    view: str = "side"
    
    # Style options
    detail: str = "high detail"
    shading: str = "detailed shading"
    outline: str = "single color black outline"


@dataclass
class ArtResult:
    """Result from art generation."""
    card_name: str
    file_path: Optional[Path] = None
    base64_data: Optional[str] = None
    pixellab_id: Optional[str] = None
    success: bool = False
    error: Optional[str] = None


class ArtGenerator:
    """
    Art generation manager for card art.
    
    This class manages art requests, caching, and storage.
    Actual generation is done via PixelLab MCP tools.
    
    Example:
        generator = ArtGenerator(art_dir=Path("assets/art"))
        
        # Check if art exists
        if not generator.has_art("Aziah Calderon"):
            # Request would be made via MCP
            request = generator.create_request(
                card_name="Aziah Calderon",
                description="Female scientist with quantum energy",
                style=ArtStyle.CHARACTER
            )
            print(f"Generate with: {request}")
        
        # Load existing art
        art_data = generator.load_art("Fai Wei")
    """
    
    def __init__(self, art_dir: Path):
        """
        Initialize ArtGenerator.
        
        Args:
            art_dir: Directory for storing art files
        """
        self.art_dir = Path(art_dir)
        self.art_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, str] = {}  # name -> base64
        
        # Pre-load existing art
        self._scan_existing_art()
    
    def _scan_existing_art(self) -> None:
        """Scan art directory for existing files."""
        for ext in ["*.png", "*.jpg", "*.jpeg", "*.gif"]:
            for path in self.art_dir.glob(ext):
                name = path.stem.replace("_", " ").title()
                self._cache[name] = self._path_to_base64(path)
    
    def _path_to_base64(self, path: Path) -> str:
        """Convert file to base64 string."""
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    
    def _normalize_name(self, name: str) -> str:
        """Normalize card name to filename."""
        return name.lower().replace(" ", "_").replace("-", "_")
    
    def has_art(self, card_name: str) -> bool:
        """Check if art exists for a card."""
        if card_name in self._cache:
            return True
        
        normalized = self._normalize_name(card_name)
        for ext in [".png", ".jpg", ".jpeg", ".gif"]:
            if (self.art_dir / f"{normalized}{ext}").exists():
                return True
        
        return False
    
    def load_art(self, card_name: str) -> Optional[str]:
        """
        Load art for a card as base64.
        
        Args:
            card_name: Name of the card
            
        Returns:
            Base64 encoded art data, or None
        """
        if card_name in self._cache:
            return self._cache[card_name]
        
        normalized = self._normalize_name(card_name)
        for ext in [".png", ".jpg", ".jpeg", ".gif"]:
            path = self.art_dir / f"{normalized}{ext}"
            if path.exists():
                data = self._path_to_base64(path)
                self._cache[card_name] = data
                return data
        
        return None
    
    def save_art(self, card_name: str, data: bytes, ext: str = ".png") -> Path:
        """
        Save art data to file.
        
        Args:
            card_name: Name of the card
            data: Raw image data
            ext: File extension
            
        Returns:
            Path to saved file
        """
        normalized = self._normalize_name(card_name)
        path = self.art_dir / f"{normalized}{ext}"
        path.write_bytes(data)
        
        # Update cache
        self._cache[card_name] = base64.b64encode(data).decode("utf-8")
        
        return path
    
    def save_art_base64(self, card_name: str, base64_data: str, ext: str = ".png") -> Path:
        """
        Save base64 art data to file.
        
        Args:
            card_name: Name of the card
            base64_data: Base64 encoded image data
            ext: File extension
            
        Returns:
            Path to saved file
        """
        data = base64.b64decode(base64_data)
        return self.save_art(card_name, data, ext)
    
    def create_request(
        self,
        card_name: str,
        description: str,
        style: ArtStyle,
        size: ArtSize = ArtSize.LARGE,
        **kwargs
    ) -> ArtRequest:
        """
        Create an art generation request.
        
        This request can be used with PixelLab MCP tools.
        
        Args:
            card_name: Name of the card
            description: Visual description for generation
            style: Art style preset
            size: Art size preset
            **kwargs: Additional options
            
        Returns:
            ArtRequest object
        """
        return ArtRequest(
            card_name=card_name,
            description=description,
            style=style,
            size=size,
            n_directions=kwargs.get("n_directions", 4),
            view=kwargs.get("view", "side"),
            detail=kwargs.get("detail", "high detail"),
            shading=kwargs.get("shading", "detailed shading"),
            outline=kwargs.get("outline", "single color black outline"),
        )
    
    def get_pixellab_params(self, request: ArtRequest) -> dict:
        """
        Convert request to PixelLab MCP parameters.
        
        Args:
            request: ArtRequest object
            
        Returns:
            Dictionary of parameters for PixelLab MCP tools
        """
        if request.style == ArtStyle.CHARACTER:
            return {
                "description": request.description,
                "name": request.card_name,
                "size": request.size.value,
                "n_directions": request.n_directions,
                "view": request.view,
                "detail": request.detail,
                "shading": request.shading,
                "outline": request.outline,
            }
        else:
            return {
                "description": request.description,
                "width": request.size.value,
                "height": request.size.value,
                "view": "high top-down",
                "detail": request.detail,
                "shading": request.shading,
            }
    
    def list_available_art(self) -> list[str]:
        """List all cards with available art."""
        return list(self._cache.keys())
    
    def list_missing_art(self, card_names: list[str]) -> list[str]:
        """List cards that need art."""
        return [name for name in card_names if not self.has_art(name)]
    
    def get_art_stats(self) -> dict:
        """Get statistics about art collection."""
        files = list(self.art_dir.glob("*.png")) + list(self.art_dir.glob("*.jpg"))
        total_size = sum(f.stat().st_size for f in files)
        
        return {
            "total_files": len(files),
            "total_size_kb": round(total_size / 1024, 2),
            "cached_cards": len(self._cache),
            "art_dir": str(self.art_dir),
        }


# Convenience function
def generate_art_description(card) -> str:
    """
    Generate a visual description for a card's art.
    
    Args:
        card: Card object
        
    Returns:
        Description string for art generation
    """
    from ..models.card import CardType
    
    base_desc = card.name
    
    if card.card_type == CardType.CREATURE:
        # Extract creature type from type line
        if " - " in card.type_line:
            subtypes = card.type_line.split(" - ")[1]
            base_desc = f"{subtypes} character"
    elif card.card_type == CardType.ARTIFACT:
        base_desc = f"Artifact object: {card.name}"
    elif card.card_type in (CardType.INSTANT, CardType.SORCERY):
        base_desc = f"Magical effect: {card.name}"
    elif card.card_type == CardType.LAND:
        base_desc = f"Location: {card.name}"
    
    # Add color theme
    color_themes = {
        "W": "white, light, holy",
        "U": "blue, arcane, water",
        "B": "dark, shadowy, death",
        "R": "red, fire, chaos",
        "G": "green, nature, growth",
    }
    
    colors = []
    for c in card.colors:
        if c in color_themes:
            colors.append(color_themes[c])
    
    if colors:
        base_desc += f", {', '.join(colors)} themed"
    
    return base_desc
