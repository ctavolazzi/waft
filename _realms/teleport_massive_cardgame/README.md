# Teleport Massive Card Game (TMCG)

> A collectible card game set in the Teleport Massive universe, featuring AI-generated pixel art.

```
╔══════════════════════════════════════════════════════════════╗
║                     TELEPORT MASSIVE                         ║
║                       CARD GAME                              ║
║                                                              ║
║   "They said death was final. They must be wrong."           ║
║                                    - Aziah Calderon          ║
╚══════════════════════════════════════════════════════════════╝
```

## Features

- **Pydantic Models**: Type-safe card definitions with validation
- **AI Pixel Art**: PixelLab MCP integration for automated art generation
- **Factory Pattern**: Clean card and deck generation
- **Multiple Outputs**: HTML, PDF, print-ready formats
- **CSV/JSON Import**: Easy card data management

## Installation

```bash
cd _realms/teleport_massive_cardgame
pip install -e .
```

## Quick Start

```python
from tmcg import Card, CardGenerator, DeckBuilder

# Create a card
card = Card(
    name="Aziah Calderon",
    mana_cost="3UU",
    type_line="Legendary Creature - Human Scientist",
    abilities="When Aziah Calderon enters the battlefield, search your library for a card named 'Scint Protocol'.",
    power=3,
    toughness=4,
    rarity="mythic",
    frame_color="blue"
)

# Generate with art
generator = CardGenerator()
card_with_art = generator.generate(card, include_art=True)

# Build a deck
builder = DeckBuilder()
deck = builder.load_csv("data/cards.csv").build()

# Render to HTML
deck.render_html("output/deck.html")
```

## CLI

```bash
# Generate cards from CSV
tmcg generate --input data/cards.csv --output output/deck.html

# Generate art for a card
tmcg art --name "Aziah Calderon" --description "Female scientist with quantum energy"

# Build and preview deck
tmcg preview --input data/cards.csv
```

## Project Structure

```
teleport_massive_cardgame/
├── src/tmcg/
│   ├── models/         # Pydantic models (Card, Deck)
│   ├── generators/     # CardGenerator, ArtGenerator, DeckBuilder
│   ├── renderers/      # HTML, PDF output
│   └── cli.py          # Command line interface
├── data/               # Card data (CSV, JSON)
├── assets/art/         # Generated pixel art
├── tests/              # Test suite
└── docs/               # Documentation
```

## Card Types

| Type | Description |
|------|-------------|
| Creature | Characters with Power/Toughness |
| Instant | Fast spells |
| Sorcery | Normal spells |
| Enchantment | Persistent effects |
| Artifact | Objects and technology |
| Land | Mana sources |

## Frame Colors

| Color | Theme |
|-------|-------|
| White | Order, protection |
| Blue | Knowledge, quantum |
| Black | Death, ambition |
| Red | Chaos, destruction |
| Green | Nature, growth |
| Multicolor | Combined themes |
| Artifact | Colorless technology |

## Lore

Set in the world of Teleport Massive, where quantum teleportation has become reality. The game follows the story of Aziah Calderon, a grieving scientist determined to bring back her lost loved one, even if it means rewriting the laws of physics.

Key characters:
- **Aziah Calderon**: The protagonist, quantum scientist
- **Fai Wei**: Founder and CEO of Teleport Massive
- **SWAB/SWAE**: Mysterious artifacts from outside time

## License

MIT License - See LICENSE file

## Credits

- Pixel Art: Generated via PixelLab MCP
- Card System: Inspired by Magic: The Gathering
- Universe: Teleport Massive © 2026
