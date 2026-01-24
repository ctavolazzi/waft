"""
HTML Renderer for Teleport Massive Card Game.

Renders cards and decks as HTML with embedded CSS and images.
"""

from pathlib import Path
from html import escape
from typing import Optional

from ..models.card import Card, FRAME_COLORS, RARITY_COLORS
from ..models.deck import Deck


class HTMLRenderer:
    """
    Render cards and decks as HTML.
    
    Example:
        renderer = HTMLRenderer()
        
        # Render single card
        html = renderer.render_card(card)
        
        # Render deck
        html = renderer.render_deck(deck)
        
        # Save to file
        renderer.render_deck_to_file(deck, "output/deck.html")
    """
    
    # Default CSS for cards
    CARD_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Palatino Linotype', Georgia, serif; background: #0d0d15; padding: 24px; }
h1 { color: #C9A227; text-align: center; margin-bottom: 24px; }
.stats { color: #888; text-align: center; margin-bottom: 20px; font-size: 14px; }
.grid { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
.card {
  width: 250px; height: 350px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 12px; border: 1px solid #333;
  display: flex; flex-direction: column;
  color: var(--text); overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  transition: transform 0.2s;
}
.card:hover { transform: translateY(-4px); }
.header { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: rgba(0,0,0,0.2); }
.name { font-weight: bold; font-size: 14px; }
.mana { font-family: monospace; font-size: 13px; background: rgba(255,255,255,0.15); padding: 2px 6px; border-radius: 4px; }
.art { height: 130px; margin: 8px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; display: flex; align-items: center; justify-content: center; image-rendering: pixelated; }
.art img { max-height: 100%; max-width: 100%; object-fit: contain; image-rendering: pixelated; }
.type { font-size: 11px; font-style: italic; padding: 6px 12px; background: rgba(0,0,0,0.15); border-top: 1px solid rgba(255,255,255,0.1); }
.body { flex: 1; padding: 10px 12px; font-size: 11px; line-height: 1.4; overflow-y: auto; }
.rules { margin-bottom: 8px; }
.flavor { font-style: italic; opacity: 0.85; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.15); font-size: 10px; }
.footer { display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: rgba(0,0,0,0.2); }
.set { font-size: 10px; color: var(--rarity); font-weight: bold; }
.pt { background: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 13px; }
@media print {
  body { background: white; padding: 0; }
  .card { page-break-inside: avoid; box-shadow: none; border: 1px solid #000; }
  h1, .stats { display: none; }
}
"""
    
    def __init__(self, include_stats: bool = True):
        """
        Initialize HTMLRenderer.
        
        Args:
            include_stats: Whether to include deck statistics
        """
        self.include_stats = include_stats
    
    def render_card(self, card: Card) -> str:
        """
        Render a single card as HTML.
        
        Args:
            card: Card to render
            
        Returns:
            HTML string for the card
        """
        colors = card.frame_colors_dict
        rarity_color = card.rarity_color
        
        name = escape(card.name)
        mana = escape(card.mana_cost)
        type_line = escape(card.type_line)
        abilities = escape(card.abilities).replace("\\n", "<br>")
        flavor = escape(card.flavor_text)
        
        # Power/toughness
        pt_html = ""
        if card.is_creature and card.power is not None:
            pt_html = f'<div class="pt">{card.power}/{card.toughness}</div>'
        
        # Flavor text
        flavor_html = f'<div class="flavor">{flavor}</div>' if flavor else ""
        
        # Art
        art_html = ""
        if card.art_data:
            art_html = f'<img src="data:image/png;base64,{card.art_data}" alt="{name}">'
        
        return f'''<div class="card" style="--primary:{colors['primary']};--secondary:{colors['secondary']};--text:{colors['text']};--rarity:{rarity_color}">
  <div class="header"><span class="name">{name}</span><span class="mana">{mana}</span></div>
  <div class="art">{art_html}</div>
  <div class="type">{type_line}</div>
  <div class="body"><div class="rules">{abilities}</div>{flavor_html}</div>
  <div class="footer"><span class="set">{card.set_code}</span>{pt_html}</div>
</div>'''
    
    def render_deck(self, deck: Deck, title: Optional[str] = None) -> str:
        """
        Render a deck as a complete HTML page.
        
        Args:
            deck: Deck to render
            title: Optional page title
            
        Returns:
            Complete HTML page string
        """
        title = title or deck.name
        cards_html = "\n".join(self.render_card(c) for c in deck.unique_cards_list)
        
        # Stats section
        stats_html = ""
        if self.include_stats:
            stats = deck.stats
            stats_html = f'''<div class="stats">
  {stats.total_cards} cards • {stats.unique_cards} unique • 
  {stats.creatures} creatures • {stats.spells} spells • 
  {stats.lands} lands • {stats.artifacts} artifacts •
  Avg CMC: {stats.average_cmc}
</div>'''
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<style>
{self.CARD_CSS}
</style>
</head>
<body>
<h1>{escape(title)}</h1>
{stats_html}
<div class="grid">
{cards_html}
</div>
</body>
</html>'''
    
    def render_cards(self, cards: list[Card], title: str = "Cards") -> str:
        """
        Render a list of cards as HTML page.
        
        Args:
            cards: List of cards to render
            title: Page title
            
        Returns:
            Complete HTML page string
        """
        # Create temporary deck for rendering
        deck = Deck(name=title, cards=cards)
        return self.render_deck(deck, title)
    
    def render_deck_to_file(self, deck: Deck, path: Path, title: Optional[str] = None) -> Path:
        """
        Render deck to HTML file.
        
        Args:
            deck: Deck to render
            path: Output file path
            title: Optional page title
            
        Returns:
            Path to created file
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        html = self.render_deck(deck, title)
        path.write_text(html, encoding="utf-8")
        
        return path
    
    def render_cards_to_file(self, cards: list[Card], path: Path, title: str = "Cards") -> Path:
        """
        Render cards to HTML file.
        
        Args:
            cards: List of cards to render
            path: Output file path
            title: Page title
            
        Returns:
            Path to created file
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        html = self.render_cards(cards, title)
        path.write_text(html, encoding="utf-8")
        
        return path
    
    def render_decklist(self, deck: Deck) -> str:
        """
        Render deck as text decklist.
        
        Args:
            deck: Deck to render
            
        Returns:
            Text decklist string
        """
        return deck.to_decklist()


# Convenience functions
def render_card_html(card: Card) -> str:
    """Render a single card to HTML."""
    return HTMLRenderer().render_card(card)


def render_deck_html(deck: Deck, title: Optional[str] = None) -> str:
    """Render a deck to HTML."""
    return HTMLRenderer().render_deck(deck, title)
