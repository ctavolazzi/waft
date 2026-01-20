# Realm of Gaming and Gambling

**Status**: Active  
**Created**: 2026-01-19  
**Demi-God**: The River King  
**Parent God**: The Magistrate  
**Sacred Tool**: The Deck of Fates

---

## Overview

The Realm of Gaming and Gambling is a unified space for all things related to games of chance, probability, risk, and luck. It serves as the domain of The River King, demi-god of gambling, and houses all tools, documentation, and precedents related to card games, poker, and chance-based activities.

---

## Structure

```
gaming_gambling_realm/
├── games/          # Documented poker games and card game sessions
├── sessions/       # Poker session recaps and game logs
├── tools/          # Gambling tools and utilities
├── readings/       # Sacred readings by The River King
├── precedents/     # Game rules and precedents established
└── realm_manifest.json
```

---

## The River King

**Demi-God of Gambling, Luck, and the Mississippi**

The River King presides over this realm, using The Deck of Fates (the deckz_poker visualization system) as his sacred tool to:
- Document games and outcomes
- Reveal probability patterns
- Create precedents for game documentation
- Witness and record moments of chance

See `_pantheon/river_king/` for full documentation.

---

## Tools

### 1. The Deck of Fates (deckz_poker)
**Location**: `src/waft/templates/typst/wrappers/deckz_poker.py`

The sacred tool of The River King. Visualizes cards, hands, and game states.

**Usage**:
```python
from src.waft.templates.typst.wrappers.deckz_poker import generate_deckz_poker, Player

players = [Player(name="Alice", cards=["AS", "KH"])]
generate_deckz_poker(
    title="Game Title",
    content="Game description",
    output_path=Path("game.pdf"),
    players=players
)
```

### 2. Session Recap Generator
**Location**: `examples/generate_poker_session_recap.py`

Documents poker sessions with statistics, memorable hands, and visualizations.

### 3. Story Prompt Generator
**Location**: `examples/generate_card_story_prompts.py`

Uses cards to generate creative writing prompts and narrative elements.

### 4. Decision Visualization
**Location**: `examples/generate_decision_cards.py`

Visualizes decision options as cards for project planning and choice analysis.

### 5. Game Prototype Documentation
**Location**: `examples/generate_card_game_prototype.py`

Documents new card game mechanics with visual examples.

---

## Precedents

The realm maintains precedents for:
- How games should be documented
- How probability should be visualized
- How luck flows through sessions
- How outcomes should be recorded

See `precedents/` directory for established rules.

---

## Philosophy

> "The cards don't lie. They just don't always tell you what you want to hear."

**Core Principles**:
- Probability is sacred (mathematics of fate)
- Luck is real (but it's statistics, not magic)
- Every bet matters (the choice, not just the money)
- The house edge is honest (price of the game)
- Fate is written (but you still play your hand)

---

## Integration

- **Pantheon**: The River King (demi-god)
- **Parent God**: The Magistrate (provides structure, precedent, proof)
- **Tools**: All poker/gambling visualization tools
- **Realm**: New Orleans, Mississippi River, all places of chance

---

## Usage Examples

### Document a Poker Session
```python
from examples.generate_poker_session_recap import PokerSession, generate_poker_session_recap

session = PokerSession(date="2026-01-19", players=["Alice", "Bob"])
session.add_hand(hand_number=1, players=[...], winner="Alice")
generate_poker_session_recap(session, Path("session.pdf"))
```

### Generate Story Prompt
```python
from examples.generate_card_story_prompts import draw_story_cards, generate_story_prompt_pdf

cards = draw_story_cards(5)
generate_story_prompt_pdf(cards, Path("story.pdf"))
```

### Visualize Decision
```python
from examples.generate_decision_cards import visualize_decision_outcomes

options = [{"name": "Option A", "description": "..."}, ...]
visualize_decision_outcomes("Which option?", options, Path("decision.pdf"))
```

---

## Status

✅ **Active** - All tools operational  
✅ **The River King** - Presiding demi-god  
✅ **Sacred Tool** - The Deck of Fates functional  
✅ **Precedents** - Being established  
✅ **Documentation** - Complete
