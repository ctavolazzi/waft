# Deckz Poker Visualization Package

Easy-to-use package for generating beautiful poker game visualizations as PDFs using the [Deckz Typst package](https://typst.app/universe/package/deckz).

## Quick Start

### Option 1: Simple Builder Class (Recommended)

```python
from src.waft.templates.typst.poker import PokerGame

game = PokerGame("My Poker Game")
game.add_player("Alice", ["AS", "KH"])
game.add_player("Bob", ["QD", "JD"])
game.set_community_cards(["AC", "AD", "AH", "KS", "QS"])
game.include_rules()
game.generate("output.pdf")
```

### Option 2: Quick Functions

```python
from src.waft.templates.typst.poker import quick_hand, quick_holdem

# Single hand
quick_hand(["AS", "KS", "QS", "JS", "10S"], "Royal Flush")

# Texas Hold'em game
quick_holdem(
    {"Alice": ["AS", "KH"], "Bob": ["QD", "JD"]},
    ["AC", "AD", "AH", "KS", "QS"]
)
```

### Option 3: Direct Function Call

```python
from src.waft.templates.typst import generate_deckz_poker, Player

players = [
    Player(name="Alice", cards=["AS", "KH"]),
    Player(name="Bob", cards=["QD", "JD"]),
]

generate_deckz_poker(
    title="Texas Hold'em Game",
    content="Game description here",
    output_path=Path("game.pdf"),
    players=players,
    community_cards=["AC", "AD", "AH", "KS", "QS"],
    show_rules=True
)
```

### Option 4: Command Line

```bash
# Simple hand
python3 scripts/generate_poker_pdf.py \
  --title "Royal Flush" \
  --output poker.pdf \
  --player "Alice:AS,KS,QS,JS,10S" \
  --format large \
  --rules

# Texas Hold'em game
python3 scripts/generate_poker_pdf.py \
  --title "Texas Hold'em Game" \
  --output game.pdf \
  --player "Alice:AS,KH" \
  --player "Bob:QD,JD" \
  --community "AC,AD,AH,KS,QS" \
  --rules
```

## Card Format

Cards use the format: **rank + suit**

- **Ranks**: `A` (Ace), `2-9`, `10`, `J` (Jack), `Q` (Queen), `K` (King)
- **Suits**: `H` (Hearts), `D` (Diamonds), `C` (Clubs), `S` (Spades)

**Examples**: `"AS"` (Ace of Spades), `"10H"` (Ten of Hearts), `"KD"` (King of Diamonds)

## Features

✅ **Texas Hold'em Support** - Full game state visualization  
✅ **Multiple Card Formats** - inline, mini, small, medium, large, square  
✅ **Poker Rules Section** - Optional hand rankings and rules documentation  
✅ **Input Validation** - Automatic validation of card identifiers  
✅ **Security** - Content sanitization to prevent code injection  
✅ **Error Handling** - Clear error messages for invalid inputs  

## Examples

See `examples/generate_poker_visualization.py` for complete examples:
- Simple hand visualization
- Texas Hold'em game state
- Poker hand rankings guide
- Complete game scenario

## API Reference

### `PokerGame` Class

Builder class for easy game construction.

```python
game = PokerGame(title, game_type="texas_holdem", card_format="medium")
game.add_player(name, cards)           # Add a player
game.set_community_cards(cards)        # Set community cards
game.add_content(text)                 # Add custom content
game.include_rules(True)               # Include rules section
game.generate(output_path)             # Generate PDF
```

### `quick_hand()` Function

Quick visualization of a single hand.

```python
quick_hand(
    cards=["AS", "KS", "QS", "JS", "10S"],
    title="Royal Flush",
    output_path=Path("hand.pdf"),
    card_format="large"
)
```

### `quick_holdem()` Function

Quick Texas Hold'em game state.

```python
quick_holdem(
    players={"Alice": ["AS", "KH"], "Bob": ["QD", "JD"]},
    community_cards=["AC", "AD", "AH", "KS", "QS"],
    title="Texas Hold'em Game",
    output_path=Path("game.pdf"),
    card_format="medium"
)
```

### `generate_deckz_poker()` Function

Full-featured function with all options.

```python
generate_deckz_poker(
    title: str,
    content: str,
    output_path: Path,
    game_type: GameType = "texas_holdem",
    players: Optional[List[Player]] = None,
    community_cards: Optional[List[str]] = None,
    card_format: CardFormat = "medium",
    show_rules: bool = False
) -> Path
```

## Card Formats

| Format | Description |
|--------|-------------|
| `inline` | Minimal inline format |
| `mini` | Smallest visual format |
| `small` | Compact format |
| `medium` | Full structured card (default) |
| `large` | Expanded with all corners |
| `square` | 1:1 format for grids |

## Game Types

Currently supported:
- **Texas Hold'em** - 2 hole cards + 5 community cards

Future support (Phase 2):
- Five Card Draw
- Omaha
- Seven Card Stud

## Security

All inputs are validated and sanitized:
- Card identifiers must match valid format
- User content is sanitized to prevent Typst injection
- Player data is validated via dataclass
- Path validation inherited from TypstCompiler

## Requirements

- Typst CLI (version 0.10.0+)
- Deckz package (automatically downloaded by Typst)

## License

Part of the WAFT project.
