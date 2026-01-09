"""
PygameBiomeEngine: Real-time Pygame visualization of the Biome.

Renders the PetriDish lattice in a dedicated Pygame window with:
- Linnaean symbols (☿, ⚥, ⚲, ⴲ) as organism icons
- Color-coding by culture (Sanskrit=Gold, Norse=Blue, Latin=Red, Cyber=Green)
- Real-time updates on every pulse
"""

import pygame
import sys
from typing import Dict, Tuple, Optional, TYPE_CHECKING
from pathlib import Path

from .dish import PetriDish
from ..agent.base import BaseAgent
from ..science.taxonomy import LineagePoet

if TYPE_CHECKING:
    from ..world.biome import Biome

# Initialize Pygame
pygame.init()

# Color definitions (RGB)
COLORS = {
    "background": (20, 20, 30),
    "grid": (40, 40, 50),
    "sanskrit": (255, 215, 0),  # Gold
    "norse": (70, 130, 180),    # Steel Blue
    "latin": (220, 20, 60),      # Crimson Red
    "cyber": (50, 205, 50),      # Lime Green
    "text": (255, 255, 255),
    "sidebar": (30, 30, 40)
}

# Symbol font size
SYMBOL_SIZE = 24


class PygameBiomeEngine:
    """
    Pygame-based real-time visualization of the Biome.
    
    Creates a dedicated window that renders PetriDish lattices with organisms,
    updating in real-time on every pulse.
    """
    
    def __init__(
        self,
        width: int = 1200,
        height: int = 800,
        cell_size: int = 8,
        title: str = "WAFT Biome Engine"
    ):
        """
        Initialize Pygame Biome Engine.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            cell_size: Size of each lattice cell in pixels
            title: Window title
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.title = title
        
        # Create window
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Fonts
        self.font_small = pygame.font.Font(None, 16)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 24)
        self.symbol_font = pygame.font.Font(None, SYMBOL_SIZE)
        
        # Sidebar width
        self.sidebar_width = 250
        
        # Grid area
        self.grid_width = width - self.sidebar_width
        self.grid_height = height
        
        # Running state
        self.running = True
        self.pulse_count = 0
    
    def _get_culture_color(self, genome_id: str) -> Tuple[int, int, int]:
        """
        Get color for organism's culture.
        
        Args:
            genome_id: Organism's genome_id
            
        Returns:
            RGB color tuple
        """
        if len(genome_id) < 2:
            return COLORS["text"]
        
        first_byte_hex = genome_id[:2]
        first_byte = int(first_byte_hex, 16)
        
        if 0x00 <= first_byte <= 0x3F:  # Sanskrit
            return COLORS["sanskrit"]
        elif 0x40 <= first_byte <= 0x7F:  # Norse
            return COLORS["norse"]
        elif 0x80 <= first_byte <= 0xBF:  # Latin
            return COLORS["latin"]
        else:  # Cyber/Tech
            return COLORS["cyber"]
    
    def render_dish(self, dish: PetriDish, offset_x: int = 0, offset_y: int = 0):
        """
        Render a PetriDish to the screen.
        
        Args:
            dish: PetriDish to render
            offset_x: X offset for positioning
            offset_y: Y offset for positioning
        """
        # Calculate visible area
        max_cells_x = self.grid_width // self.cell_size
        max_cells_y = self.grid_height // self.cell_size
        
        # Draw grid background
        for x in range(min(max_cells_x, dish.width)):
            for y in range(min(max_cells_y, dish.height)):
                rect = pygame.Rect(
                    offset_x + x * self.cell_size,
                    offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, COLORS["grid"], rect)
                pygame.draw.rect(self.screen, COLORS["background"], rect, 1)
        
        # Draw organisms
        for organism_id, organism in dish.organisms.items():
            position = dish.get_organism_position(organism_id)
            if position is None:
                continue
            
            x, y = position
            
            # Check if visible
            if x >= max_cells_x or y >= max_cells_y:
                continue
            
            # Get symbol and color
            symbol = organism.state.anatomical_symbol
            color = self._get_culture_color(organism.genome_id)
            
            # Draw symbol
            symbol_surface = self.symbol_font.render(symbol, True, color)
            symbol_rect = symbol_surface.get_rect()
            symbol_rect.center = (
                offset_x + x * self.cell_size + self.cell_size // 2,
                offset_y + y * self.cell_size + self.cell_size // 2
            )
            self.screen.blit(symbol_surface, symbol_rect)
        
        # Draw items (if any)
        for position, items in dish.items.items():
            if not items:
                continue
            
            x, y = position
            if x >= max_cells_x or y >= max_cells_y:
                continue
            
            # Draw item indicator (small dot)
            item_x = offset_x + x * self.cell_size + self.cell_size - 3
            item_y = offset_y + y * self.cell_size + 3
            pygame.draw.circle(self.screen, (200, 200, 200), (item_x, item_y), 2)
    
    def render_sidebar(self, dish: PetriDish):
        """
        Render sidebar with statistics.
        
        Args:
            dish: PetriDish to get stats from
        """
        sidebar_x = self.grid_width
        y = 20
        
        # Background
        sidebar_rect = pygame.Rect(sidebar_x, 0, self.sidebar_width, self.height)
        pygame.draw.rect(self.screen, COLORS["sidebar"], sidebar_rect)
        
        # Title
        title = self.font_large.render("Biome Stats", True, COLORS["text"])
        self.screen.blit(title, (sidebar_x + 10, y))
        y += 40
        
        # Pulse count
        pulse_text = self.font_medium.render(f"Pulse: {self.pulse_count}", True, COLORS["text"])
        self.screen.blit(pulse_text, (sidebar_x + 10, y))
        y += 30
        
        # Population
        pop_count = dish.get_organism_count()
        pop_text = self.font_medium.render(f"Population: {pop_count}", True, COLORS["text"])
        self.screen.blit(pop_text, (sidebar_x + 10, y))
        y += 30
        
        # Energy average
        if pop_count > 0:
            total_energy = sum(org.state.energy for org in dish.organisms.values())
            avg_energy = total_energy / pop_count
            energy_text = self.font_medium.render(f"Energy Avg: {avg_energy:.1f}%", True, COLORS["text"])
            self.screen.blit(energy_text, (sidebar_x + 10, y))
            y += 30
        
        # Culture distribution
        y += 20
        culture_title = self.font_medium.render("Cultures:", True, COLORS["text"])
        self.screen.blit(culture_title, (sidebar_x + 10, y))
        y += 25
        
        culture_dist = self._get_culture_distribution(dish)
        for culture, count in sorted(culture_dist.items()):
            culture_text = self.font_small.render(f"  {culture}: {count}", True, COLORS["text"])
            self.screen.blit(culture_text, (sidebar_x + 10, y))
            y += 20
        
        # Symbol distribution
        y += 10
        symbol_title = self.font_medium.render("Archetypes:", True, COLORS["text"])
        self.screen.blit(symbol_title, (sidebar_x + 10, y))
        y += 25
        
        symbol_dist = self._get_symbol_distribution(dish)
        for symbol, count in sorted(symbol_dist.items()):
            symbol_text = self.font_small.render(f"  {symbol}: {count}", True, COLORS["text"])
            self.screen.blit(symbol_text, (sidebar_x + 10, y))
            y += 20
    
    def _get_culture_distribution(self, dish: PetriDish) -> Dict[str, int]:
        """Get culture distribution in dish."""
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
        """Get anatomical symbol distribution in dish."""
        distribution = {}
        
        for organism in dish.organisms.values():
            symbol = organism.state.anatomical_symbol
            distribution[symbol] = distribution.get(symbol, 0) + 1
        
        return distribution
    
    def update(self, dish: PetriDish):
        """
        Update display with current dish state.
        
        Args:
            dish: PetriDish to render
        """
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Clear screen
        self.screen.fill(COLORS["background"])
        
        # Render dish
        self.render_dish(dish)
        
        # Render sidebar
        self.render_sidebar(dish)
        
        # Update display
        pygame.display.flip()
    
    def pulse(self, dish: PetriDish):
        """
        Advance one pulse and update display.
        
        Args:
            dish: PetriDish to render
        """
        self.pulse_count += 1
        self.update(dish)
    
    def close(self):
        """Close the Pygame window."""
        pygame.quit()
    
    def is_running(self) -> bool:
        """Check if window is still running."""
        return self.running
