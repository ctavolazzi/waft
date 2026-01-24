# Work Effort: TMCG Core System

## Status: 🟢 Active
**ID:** WE-260120-0001
**Started:** 2026-01-20 12:36
**Last Updated:** 2026-01-20 12:36

---

## Objective

Build the core system for Teleport Massive Card Game (TMCG) including:
- Card data models
- Card generation factory
- Deck building system
- Art generation integration (PixelLab)
- HTML/PDF output rendering

---

## Background

Successfully proved PixelLab MCP integration works for generating pixel art. Now building a proper, production-ready card game system.

---

## Tasks

- [x] Create project structure and README
- [x] Build `Card` class (Pydantic model) - Complete in `models/card.py`
- [ ] Build `CardGenerator` factory class
- [x] Build `Deck` class - Complete in `models/deck.py` + `data/decks.ts`
- [x] Build `DeckBuilder` class - Enhanced web UI with save/load
- [x] Build `ArtGenerator` (PixelLab integration) - Demonstrated with Aziah art
- [ ] Build `HTMLRenderer` for card output
- [ ] Migrate existing card data from CSV
- [ ] Create CLI interface
- [ ] Test end-to-end pipeline
- [x] **BONUS**: Created starter decks (Python + TypeScript)
- [x] **BONUS**: Added localStorage persistence for user decks
- [x] **BONUS**: Expanded card set to 20 cards

---

## Architecture

```
tmcg/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── card.py          # Card Pydantic model
│   ├── deck.py          # Deck class
│   └── enums.py         # Card types, rarities, colors
├── generators/
│   ├── __init__.py
│   ├── card_generator.py    # CardGenerator factory
│   ├── art_generator.py     # PixelLab integration
│   └── deck_builder.py      # DeckBuilder
├── renderers/
│   ├── __init__.py
│   ├── html_renderer.py     # HTML card output
│   └── pdf_renderer.py      # PDF export
├── data/
│   ├── __init__.py
│   └── loader.py            # CSV/JSON data loading
└── cli.py                   # Command line interface
```

---

## Progress

### 2026-01-20 12:36 - Started
- Created project structure
- Planning architecture
- Beginning implementation

### 2026-01-20 13:45 - Auto-Work Session (Phase 1)
- **Fixed broken art**: Generated Aziah Calderon pixel art using PixelLab MCP (saved to `web/public/art/aziah_calderon.png`)
- **Expanded card set**: Added 8 new cards (tm-013 to tm-020), expanding set from 12 to 20 cards
  - Quantum Observer (uncommon creature)
  - Probability Collapse (rare instant)
  - Scint Detector (uncommon artifact)
  - Entangled Souls (rare sorcery)
  - Lab Assistant (common creature)
  - Recursive Timeline (rare enchantment)
  - Corporate Security (common creature)
  - Dr. Chen's Discovery (uncommon instant)
- **Updated home page stats**: Changed card count from 12 to 20, card types from 5 to 6

### 2026-01-20 13:55 - Auto-Work Session (Phase 2)
- **Created Deck data structure** (`web/src/data/decks.ts`):
  - `Deck` interface with full metadata
  - `DeckEntry` and `DeckStats` types
  - `DeckConstraints` for validation
  - Utility functions: `calculateStats()`, `validateDeck()`, `exportDecklist()`, `cloneDeck()`
  
- **Created 2 Starter Decks**:
  1. **Quantum Control** (44 cards) - Blue control, Aziah-focused
  2. **The Vibration** (44 cards) - Multicolor combo
  
- **Added localStorage persistence**:
  - `saveDeck()`, `getSavedDecks()`, `deleteSavedDeck()`
  - Full CRUD for user's saved decks
  
- **Enhanced Deck Builder UI**:
  - "Browse Starter Decks" button with modal
  - "My Decks" browser with load/delete
  - Save button (persists to localStorage)
  - Deck statistics display
  
- **Created Python starter decks** (`src/tmcg/data/starter_decks.py`):
  - Card definitions matching TypeScript
  - `create_quantum_control_deck()`, `create_the_vibration_deck()`
  - `get_starter_deck()`, `list_starter_decks()` utilities

**Note**: Server running in production mode (`next start`) - changes require rebuild to display

---

## Notes

- Based on successful PixelLab MCP integration proof
- Using Pydantic for data validation
- Following factory pattern for card generation
- HTML output with embedded base64 art

---

## Related

- Case File: `_work_efforts/proof_cases/CASE_PIXELLAB_INTEGRATION_20260120.md`
- Celebration: `_pyrite/journal/celebrations/PIXELLAB_MCP_INTEGRATION_20260120.md`
- Original cards: `_realms/bureaucracy_realm/corporations/teleport_massive_20250701/cards/`
