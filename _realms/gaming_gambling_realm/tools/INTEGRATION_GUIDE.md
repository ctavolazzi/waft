# Card Visualization + Image Generation Integration

**Combining The Deck of Fates with AI image generation tools.**

---

## Overview

The card visualization system can be combined with image generation tools to create mixed-media artworks:

- **Cards**: Provide structure, meaning, and visual elements
- **AI Images**: Provide atmosphere, setting, and character art
- **Composition**: Layer everything together for complete artworks

---

## Available Tools

### 1. The Deck of Fates (Cards)
**Location**: `src/waft/templates/typst/wrappers/deckz_poker.py`

Visualizes cards, hands, and game states as PDFs.

### 2. Nano-Banana (Gemini) - Background Images
**MCP Tool**: `mcp_nano-banana_generate_image`

Generates photorealistic backgrounds and atmospheric scenes.

**Example Prompts**:
- "New Orleans jazz club at night, Mississippi River, neon lights, atmospheric"
- "Riverboat casino at sunset, golden hour lighting, cinematic"
- "Back alley card game, film noir style, dramatic shadows"

### 3. PixelLab - Character Art
**MCP Tool**: `mcp_pixellab_create_character`

Generates pixel art characters and sprites.

**Example**:
- "Mysterious card dealer, velvet jacket, New Orleans style, pixel art, 8 directions"

---

## Integration Workflow

### Step 1: Generate Background
```python
# Use MCP: mcp_nano-banana_generate_image
prompt = "New Orleans jazz club at night, Mississippi River, neon lights..."
# Saves to: _temp_pdf_examples/river_king_background.png
```

### Step 2: Generate Character
```python
# Use MCP: mcp_pixellab_create_character
character_description = "Mysterious card dealer, New Orleans style..."
# Creates: Character sprites in 8 directions
```

### Step 3: Create Card Composition
```python
# Use: generate_deckz_poker
# Creates: PDF with card arrangements
# Output: _temp_pdf_examples/card_composition.pdf
```

### Step 4: Composite
- Load background image
- Position character art
- Overlay card PDF (extract cards as images)
- Adjust blending and opacity
- Final mixed media artwork

---

## Example Compositions

### The River King Portrait
- **Background**: New Orleans jazz club (Nano-Banana)
- **Character**: The River King pixel art (PixelLab)
- **Cards**: Sacred hands floating (Deckz Poker)
- **Result**: Complete mixed media portrait

### Probability Visualization Art
- **Background**: Abstract mathematical space (Nano-Banana)
- **Cards**: Arranged to show probability distributions (Deckz Poker)
- **Result**: Visual representation of probability concepts

### Game Scene
- **Background**: Casino or game room (Nano-Banana)
- **Characters**: Players as pixel art (PixelLab)
- **Cards**: Actual game state (Deckz Poker)
- **Result**: Complete game scene visualization

---

## Tools Status

- ✅ **Deckz Poker**: Fully functional
- ⚠️ **Nano-Banana**: Configured, API may need model update
- ⚠️ **PixelLab**: Available via MCP

---

## Files Created

- `examples/generate_card_art_composition.py` - Card art generator
- `examples/generate_card_art_with_ai_images.py` - Integration guide
- `_temp_pdf_examples/river_king_mixed_media_art.pdf` - Example composition
- `_temp_pdf_examples/image_generation_prompts_guide.pdf` - Prompt guide

---

## Next Steps

1. Generate background images (Nano-Banana)
2. Generate character art (PixelLab)
3. Create card compositions (Deckz Poker)
4. Composite in image editing software
5. Final mixed media artworks

---

*"The cards provide structure. The images provide atmosphere. Together, they create art."*
