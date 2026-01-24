#!/usr/bin/env python3
"""
Teleport Massive Card Generator

Generates printable MTG-style cards from CSV data.
Usage: python3 card_generator.py
"""

import csv
import base64
from pathlib import Path
from html import escape

# Map card names to art files
ART_FILES = {
    "Fai Wei": "fai_wei.png",
    "SWAB - Something Without A Beginning": "swab.png",
    "SWAE - Something Without An End": "swae.png",
}

FRAME_COLORS = {
    "white": {"primary": "#F8F6D8", "secondary": "#F0E6C8", "text": "#1a1a1a"},
    "blue": {"primary": "#0A6FA3", "secondary": "#084E74", "text": "#ffffff"},
    "black": {"primary": "#2D2A24", "secondary": "#1a1714", "text": "#d4d4d4"},
    "red": {"primary": "#C53030", "secondary": "#9B2C2C", "text": "#ffffff"},
    "green": {"primary": "#2F6846", "secondary": "#1D4430", "text": "#ffffff"},
    "multicolor": {"primary": "#C9A227", "secondary": "#9F7E1C", "text": "#1a1a1a"},
    "artifact": {"primary": "#8B8589", "secondary": "#6B6569", "text": "#1a1a1a"},
    "land": {"primary": "#8B7355", "secondary": "#6B5545", "text": "#ffffff"},
}

RARITY_COLORS = {
    "common": "#1a1a1a",
    "uncommon": "#707883",
    "rare": "#C9A227",
    "mythic": "#D35400",
}


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def get_art_data(card_name: str, art_dir: Path) -> str:
    """Get base64 encoded art if available."""
    art_file = ART_FILES.get(card_name)
    if art_file:
        art_path = art_dir / art_file
        if art_path.exists():
            data = base64.b64encode(art_path.read_bytes()).decode('utf-8')
            return f'<img src="data:image/png;base64,{data}" alt="{card_name}">'
    return ''


def card_html(card: dict, art_dir: Path) -> str:
    frame = card.get('FrameColor', 'artifact').lower()
    colors = FRAME_COLORS.get(frame, FRAME_COLORS['artifact'])
    rarity = card.get('Rarity', 'common').lower()
    rarity_color = RARITY_COLORS.get(rarity, RARITY_COLORS['common'])
    
    name = escape(card.get('Name', ''))
    mana = escape(card.get('ManaCost', ''))
    type_line = escape(card.get('TypeLine', ''))
    abilities = escape(card.get('Abilities', '')).replace('\\n', '<br>')
    flavor = escape(card.get('FlavorText', ''))
    power = card.get('Power', '')
    toughness = card.get('Toughness', '')
    
    pt_html = f'<div class="pt">{power}/{toughness}</div>' if power or toughness else ''
    flavor_html = f'<div class="flavor">{flavor}</div>' if flavor else ''
    art_html = get_art_data(card.get('Name', ''), art_dir)
    
    return f'''<div class="card" style="--primary:{colors['primary']};--secondary:{colors['secondary']};--text:{colors['text']};--rarity:{rarity_color}">
  <div class="header"><span class="name">{name}</span><span class="mana">{mana}</span></div>
  <div class="art">{art_html}</div>
  <div class="type">{type_line}</div>
  <div class="body"><div class="rules">{abilities}</div>{flavor_html}</div>
  <div class="footer"><span class="set">TM</span>{pt_html}</div>
</div>'''


def generate_html(cards: list[dict], art_dir: Path) -> str:
    cards_html = '\n'.join(card_html(c, art_dir) for c in cards)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teleport Massive Cards</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Palatino Linotype', Georgia, serif; background: #0d0d15; padding: 24px; }}
h1 {{ color: #C9A227; text-align: center; margin-bottom: 24px; }}
.grid {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
.card {{
  width: 250px; height: 350px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 12px; border: 1px solid #333;
  display: flex; flex-direction: column;
  color: var(--text); overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}}
.header {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: rgba(0,0,0,0.2); }}
.name {{ font-weight: bold; font-size: 14px; }}
.mana {{ font-family: monospace; font-size: 13px; background: rgba(255,255,255,0.15); padding: 2px 6px; border-radius: 4px; }}
.art {{ height: 130px; margin: 8px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.2); border-radius: 4px; display: flex; align-items: center; justify-content: center; image-rendering: pixelated; }}
.art img {{ max-height: 100%; max-width: 100%; object-fit: contain; image-rendering: pixelated; }}
.type {{ font-size: 11px; font-style: italic; padding: 6px 12px; background: rgba(0,0,0,0.15); border-top: 1px solid rgba(255,255,255,0.1); }}
.body {{ flex: 1; padding: 10px 12px; font-size: 11px; line-height: 1.4; overflow-y: auto; }}
.rules {{ margin-bottom: 8px; }}
.flavor {{ font-style: italic; opacity: 0.85; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.15); font-size: 10px; }}
.footer {{ display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: rgba(0,0,0,0.2); }}
.set {{ font-size: 10px; color: var(--rarity); font-weight: bold; }}
.pt {{ background: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 13px; }}
@media print {{
  body {{ background: white; padding: 0; }}
  .card {{ page-break-inside: avoid; box-shadow: none; border: 1px solid #000; }}
  h1 {{ display: none; }}
}}
</style>
</head>
<body>
<h1>Teleport Massive</h1>
<div class="grid">{cards_html}</div>
</body>
</html>'''


def main():
    here = Path(__file__).parent
    art_dir = here / "art"
    cards = read_csv(here / "teleport_massive_cards.csv")
    output = here / "deck.html"
    output.write_text(generate_html(cards, art_dir), encoding='utf-8')
    print(f"Generated {len(cards)} cards → {output}")
    print(f"Art files found: {list(art_dir.glob('*.png')) if art_dir.exists() else 'none'}")
    print(f"Open: file://{output.absolute()}")


if __name__ == "__main__":
    main()
