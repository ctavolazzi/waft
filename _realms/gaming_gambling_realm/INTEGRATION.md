# Gaming and Gambling Realm - Integration Guide

**Complete integration of all poker, gambling, and card visualization systems.**

---

## What's Included

### 1. The River King (Demi-God)
- **Location**: `_pantheon/river_king/`
- **Role**: Presides over the realm, uses The Deck of Fates
- **Powers**: Reads probability, witnesses games, documents outcomes

### 2. The Deck of Fates (Sacred Tool)
- **Location**: `src/waft/templates/typst/wrappers/deckz_poker.py`
- **Purpose**: Card visualization and game documentation
- **Status**: Active, fully functional

### 3. Tools and Generators
- **Session Recaps**: `examples/generate_poker_session_recap.py`
- **Story Prompts**: `examples/generate_card_story_prompts.py`
- **Decision Visualization**: `examples/generate_decision_cards.py`
- **Game Prototyping**: `examples/generate_card_game_prototype.py`
- **Realm Showcase**: `examples/generate_gaming_realm_showcase.py`

### 4. Example PDFs
All generated in `_temp_pdf_examples/`:
- `poker_simple_hand.pdf`
- `poker_texas_holdem.pdf`
- `poker_hand_rankings.pdf`
- `poker_game_scenario.pdf`
- `poker_session_recap_example.pdf`
- `story_prompt_from_cards.pdf`
- `decision_visualization.pdf`
- `card_game_prototype.pdf`
- `the_river_king.pdf`
- `gaming_gambling_realm_showcase.pdf`

---

## Quick Start

### Document a Poker Session
```python
from examples.generate_poker_session_recap import PokerSession, generate_poker_session_recap
from pathlib import Path

session = PokerSession(
    date="2026-01-19",
    players=["Alice", "Bob", "Carol"]
)
session.add_hand(
    hand_number=1,
    players=[Player(name="Alice", cards=["AS", "KH"])],
    winner="Alice",
    pot_size=45.0
)
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

options = [
    {"name": "Option A", "description": "..."},
    {"name": "Option B", "description": "..."}
]
visualize_decision_outcomes("Which option?", options, Path("decision.pdf"))
```

---

## Realm Structure

```
_realms/gaming_gambling_realm/
├── games/              # Documented games
├── sessions/           # Session recaps
├── tools/              # Gambling tools
├── readings/           # Sacred readings by The River King
├── precedents/         # Established rules
├── realm_manifest.json # Realm metadata
└── README.md           # This file
```

---

## Philosophy

The realm operates under The River King's philosophy:

> "The cards don't lie. They just don't always tell you what you want to hear."

**Principles**:
- Probability is sacred
- Luck is real (statistics, not magic)
- Every bet matters
- The house edge is honest
- Fate is written, but you still play your hand

---

## Integration Points

- **Pantheon**: The River King (demi-god), The Magistrate (parent god)
- **Tools**: All visualization and documentation tools
- **Realms**: New Orleans, Mississippi River, all places of chance
- **Systems**: Session recap, story generation, decision making

---

## Status

✅ **Realm Created**  
✅ **The River King** - Active demi-god  
✅ **Sacred Tool** - The Deck of Fates operational  
✅ **All Tools** - Functional  
✅ **Precedents** - Established  
✅ **Documentation** - Complete

---

*"In the end, we're all just playing the hand we're dealt. The River King just makes sure we can see the cards."*
