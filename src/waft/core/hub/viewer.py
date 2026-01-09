"""
PetriViewer: Real-time Lattice Renderer for the Multiverse.

Renders the PetriDish lattice as a 2D ASCII grid with ANSI colors,
showing organisms, items, and a sidebar with population statistics.
"""

import os
from typing import Dict, Tuple, Optional
from ..hub.dish import PetriDish
from ..agent.base import BaseAgent
from ..agent.items import Item
from ..science.taxonomy import LineagePoet


class PetriViewer:
    """
    Real-time renderer for PetriDish lattice visualization.
    
    Generates ASCII art with ANSI colors showing:
    - Organisms by anatomical symbol (☿, ⚥, ⚲, ⴲ)
    - Items (Scint-Shards as '·', Void-Stones as '■')
    - Culture-based colors (Sanskrit=Yellow, Norse=Blue, Latin=Red, Cyber=Green)
    - Sidebar with population stats
    """
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Culture colors
    SANSKRIT_COLOR = "\033[93m"  # Yellow
    NORSE_COLOR = "\033[94m"     # Blue
    LATIN_COLOR = "\033[91m"     # Red
    CYBER_COLOR = "\033[92m"     # Green
    DEFAULT_COLOR = "\033[37m"   # White
    
    # Item symbols
    SCINT_SHARD = "·"
    VOID_STONE = "■"
    DEFAULT_ITEM = "○"
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize PetriViewer.
        
        Args:
            use_colors: Whether to use ANSI colors (default: True)
        """
        self.use_colors = use_colors and os.getenv("TERM") != "dumb"
    
    def _get_culture_color(self, genome_id: str) -> str:
        """
        Get ANSI color code for organism's culture.
        
        Args:
            genome_id: Organism's genome_id
            
        Returns:
            ANSI color code string
        """
        if not self.use_colors:
            return ""
        
        if len(genome_id) < 2:
            return self.DEFAULT_COLOR
        
        first_byte_hex = genome_id[:2]
        first_byte = int(first_byte_hex, 16)
        
        if 0x00 <= first_byte <= 0x3F:  # Sanskrit
            return self.SANSKRIT_COLOR
        elif 0x40 <= first_byte <= 0x7F:  # Norse
            return self.NORSE_COLOR
        elif 0x80 <= first_byte <= 0xBF:  # Latin
            return self.LATIN_COLOR
        else:  # Cyber/Tech
            return self.CYBER_COLOR
    
    def _get_item_symbol(self, item: Item) -> str:
        """
        Get symbol for item.
        
        Args:
            item: Item instance
            
        Returns:
            Symbol character
        """
        name_lower = item.name.lower()
        if "scint" in name_lower or "shard" in name_lower:
            return self.SCINT_SHARD
        elif "void" in name_lower or "stone" in name_lower:
            return self.VOID_STONE
        else:
            return self.DEFAULT_ITEM
    
    def render(self, dish: PetriDish, sidebar: bool = True) -> str:
        """
        Render PetriDish as ASCII grid with colors.
        
        Args:
            dish: PetriDish to render
            sidebar: Whether to include sidebar (default: True)
            
        Returns:
            Formatted string with ASCII grid and optional sidebar
        """
        lines = []
        
        # Header
        lines.append(f"{self.BOLD}PetriDish: {dish.dish_id}{self.RESET}")
        lines.append(f"Size: {dish.width}×{dish.height}")
        lines.append("")
        
        # Render grid
        grid_lines = []
        
        # Add coordinate labels for first row
        header = "   " + "".join([str(x % 10) if x < 10 else " " for x in range(dish.width)])
        grid_lines.append(header)
        
        for y in range(dish.height):
            row = [f"{y:2d} "]  # Row label
            for x in range(dish.width):
                pos = (x, y)
                
                # Check for organism
                organism_id = dish.lattice.get(pos)
                if organism_id and organism_id in dish.organisms:
                    organism = dish.organisms[organism_id]
                    symbol = organism.state.anatomical_symbol
                    color = self._get_culture_color(organism.genome_id)
                    row.append(f"{color}{symbol}{self.RESET}")
                # Check for items
                elif pos in dish.items and len(dish.items[pos]) > 0:
                    item = dish.items[pos][0]  # Show first item
                    symbol = self._get_item_symbol(item)
                    row.append(symbol)
                else:
                    row.append(" ")  # Empty cell
            
            grid_lines.append("".join(row))
        
        lines.extend(grid_lines)
        lines.append("")
        
        # Sidebar
        if sidebar:
            sidebar_lines = self._generate_sidebar(dish)
            lines.extend(sidebar_lines)
        
        return "\n".join(lines)
    
    def _generate_sidebar(self, dish: PetriDish) -> list:
        """
        Generate sidebar with population statistics.
        
        Args:
            dish: PetriDish to analyze
            
        Returns:
            List of sidebar lines
        """
        lines = []
        lines.append(f"{self.BOLD}━━━ SIDEBAR ━━━{self.RESET}")
        
        # Population Count
        pop_count = dish.get_organism_count()
        lines.append(f"Population: {pop_count}")
        
        # Energy Average
        if pop_count > 0:
            total_energy = sum(org.state.energy for org in dish.organisms.values())
            avg_energy = total_energy / pop_count
            lines.append(f"Energy Avg: {avg_energy:.1f}%")
        else:
            lines.append("Energy Avg: N/A")
        
        # Latest Birth Event
        latest_birth = self._get_latest_birth(dish)
        if latest_birth:
            lines.append(f"Latest Birth: {latest_birth}")
        else:
            lines.append("Latest Birth: None")
        
        # Culture Distribution
        culture_dist = self._get_culture_distribution(dish)
        if culture_dist:
            lines.append("")
            lines.append("Cultures:")
            for culture, count in culture_dist.items():
                lines.append(f"  {culture}: {count}")
        
        # Anatomical Distribution
        symbol_dist = self._get_symbol_distribution(dish)
        if symbol_dist:
            lines.append("")
            lines.append("Archetypes:")
            for symbol, count in symbol_dist.items():
                lines.append(f"  {symbol}: {count}")
        
        lines.append(f"{self.BOLD}━━━━━━━━━━━━━━━━{self.RESET}")
        
        return lines
    
    def _get_latest_birth(self, dish: PetriDish) -> Optional[str]:
        """
        Get latest birth event from organisms.
        
        Args:
            dish: PetriDish to check
            
        Returns:
            Scientific name of most recently spawned organism or None
        """
        if not dish.organisms:
            return None
        
        # Find organism with highest generation (most recent)
        latest = max(dish.organisms.values(), key=lambda o: o.generation)
        return latest.scientific_name
    
    def _get_culture_distribution(self, dish: PetriDish) -> Dict[str, int]:
        """
        Get culture distribution in dish.
        
        Args:
            dish: PetriDish to analyze
            
        Returns:
            Dictionary mapping culture names to counts
        """
        distribution = {}
        
        for organism in dish.organisms.values():
            if len(organism.genome_id) < 2:
                continue
            
            first_byte_hex = organism.genome_id[:2]
            first_byte = int(first_byte_hex, 16)
            culture = LineagePoet._get_culture_name(first_byte)
            
            distribution[culture] = distribution.get(culture, 0) + 1
        
        return distribution
    
    def _get_symbol_distribution(self, dish: PetriDish) -> Dict[str, int]:
        """
        Get anatomical symbol distribution in dish.
        
        Args:
            dish: PetriDish to analyze
            
        Returns:
            Dictionary mapping symbols to counts
        """
        distribution = {}
        
        for organism in dish.organisms.values():
            symbol = organism.state.anatomical_symbol
            distribution[symbol] = distribution.get(symbol, 0) + 1
        
        return distribution
    
    def clear_screen(self):
        """Clear terminal screen."""
        if self.use_colors:
            # Use ANSI escape code for clearing screen (works better than os.system)
            print("\033[2J\033[H", end="", flush=True)
