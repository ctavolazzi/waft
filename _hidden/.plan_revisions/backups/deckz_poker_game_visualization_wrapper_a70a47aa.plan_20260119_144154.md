# Deckz Poker Game Visualization Wrapper

## Overview

Create a Typst template wrapper that uses the [Deckz package](https://typst.app/universe/package/deckz) to generate poker game visualizations as PDFs. This will enable generating beautiful poker game documentation, hand examples, game state diagrams, and rule guides.

## Files to Create/Modify

### 1. Create Typst Wrapper Module

**File:** `src/waft/templates/typst/wrappers/deckz_poker.py`

**Purpose:** Python wrapper for generating poker game visualizations using Deckz

**Key Features:**

- Generate individual card displays
- Render poker hands (5-card hands, Texas Hold'em, etc.)
- Display game states (multiple players, community cards, pot, etc.)
- Create poker rules documentation
- Generate example game scenarios

**Function Signature:**

```python
def generate_deckz_poker(
    title: str,
    content: str,
    output_path: Path,
    game_type: str = "texas_holdem",  # texas_holdem, five_card, omaha, etc.
    players: Optional[List[Dict]] = None,  # List of player hands
    community_cards: Optional[List[str]] = None,  # Community cards for Hold'em
    card_format: str = "medium",  # inline, mini, small, medium, large, square
    show_rules: bool = False,  # Include poker rules section
    **kwargs
) -> Path:
```

**Implementation Details:**

- Import Deckz package: `#import "@preview/deckz:0.3.1"`
- Support multiple card formats (mini, small, medium, large, square)
- Use `deckz.hand()` for player hands
- Use `deckz.deck()` for draw pile visualization
- Support Texas Hold'em layout (2 hole cards + 5 community cards)
- Support 5-card draw layout
- Include poker hand rankings visualization
- Generate game state diagrams with multiple players

### 2. Update Typst Wrappers Init

**File:** `src/waft/templates/typst/wrappers/__init__.py`

**Action:** Add export for the new wrapper (optional, since registry auto-discovers)

### 3. Example Usage Script (Optional)

**File:** `examples/generate_poker_visualization.py`

**Purpose:** Demonstrate how to use the wrapper to generate poker game PDFs

**Examples to include:**

- Simple hand visualization
- Texas Hold'em game state
- Poker hand rankings guide
- Example game scenario

## Implementation Details

### Card Format Support

The wrapper will support all Deckz card formats:

- `inline`: Minimal inline format
- `mini`: Smallest visual format
- `small`: Compact format
- `medium`: Full structured card (default)
- `large`: Expanded with all corners
- `square`: 1:1 format for grids

### Game Types Supported

1. **Texas Hold'em**: 2 hole cards per player + 5 community cards
2. **Five Card Draw**: 5 cards per player
3. **Omaha**: 4 hole cards per player + 5 community cards
4. **Seven Card Stud**: 7 cards per player (some face up)

### Layout Features

- Player positions around table
- Community cards in center
- Pot size display
- Betting rounds visualization
- Hand rankings reference

### Content Structure

The generated Typst content will include:

1. Title page with game type
2. Game state visualization (if players provided)
3. Rules section (if `show_rules=True`)
4. Hand rankings reference
5. Custom content section

## Typst Template Structure

```typst
#import "@preview/deckz:0.3.1"

#set page(margin: 1in)
#set text(font: "Roboto Slab")

= {title}

// Game state visualization
#if players:
  #game-state[
    // Render each player's hand
    #for player in players:
      #player-hand(player.name, player.cards)
    // Render community cards
    #if community_cards:
      #community-cards(..community_cards)
  ]

// Rules section
#if show_rules:
  #rules-section()

// Custom content
{content}
```

## Testing Plan

1. **Unit Tests:**

   - Test wrapper function with various parameters
   - Test card format options
   - Test different game types
   - Test edge cases (empty hands, invalid cards)

2. **Visual Tests:**

   - Generate sample PDFs for each game type
   - Verify card rendering
   - Check layout and spacing
   - Validate Typst compilation

3. **Example Scenarios:**

   - Royal flush visualization
   - Texas Hold'em full game state
   - Poker hand rankings guide
   - Example betting round

## Integration Points

- **TypstTemplateRegistry**: Auto-discovered via `generate_*` function pattern
- **TypstCompiler**: Uses existing compiler infrastructure
- **Deckz Package**: External Typst package dependency (handled by Typst)

## Success Criteria

- ✅ Wrapper module created and follows existing patterns
- ✅ Supports multiple game types (Texas Hold'em, Five Card Draw)
- ✅ Generates visually appealing poker game PDFs
- ✅ Auto-discovered by TypstTemplateRegistry
- ✅ Example usage script demonstrates capabilities
- ✅ Documentation in module docstring

## Future Enhancements (Out of Scope)

- Interactive poker game logic
- Hand evaluation and scoring
- Tournament bracket generation
- Probability calculations
- Betting strategy guides