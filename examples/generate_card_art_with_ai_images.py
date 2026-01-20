#!/usr/bin/env python3
"""
Card Art with AI-Generated Images

Combines card visualization with AI image generation to create
complete mixed-media artworks. Uses MCP tools for image generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.wrappers.deckz_poker import Player, generate_deckz_poker


def generate_river_king_artwork():
    """
    Generate complete artwork combining cards with AI-generated images.

    This demonstrates the integration workflow:
    1. Generate background image (Nano-Banana/Gemini)
    2. Generate character art (PixelLab)
    3. Create card composition (deckz_poker)
    4. Document the integration process
    """

    content = f"""
# The River King: Mixed Media Artwork
## Cards + AI-Generated Images

**Created**: {Path(__file__).stat().st_mtime}
**Medium**: Playing Cards + AI Image Generation
**Tools**: Deckz Poker + Nano-Banana (Gemini) + PixelLab

---

## The Vision

Create a complete artwork of The River King using:
- **Background**: AI-generated New Orleans scene (Nano-Banana/Gemini)
- **Character**: Pixel art of The River King (PixelLab)
- **Cards**: Visual card arrangements (Deckz Poker)
- **Composition**: All elements layered together

---

## Integration Workflow

### Step 1: Generate Background Image

**Tool**: Nano-Banana (Gemini API)  
**Prompt**: 
```
New Orleans jazz club exterior at night, Mississippi River visible in background, 
neon lights reflecting on wet streets, atmospheric moody lighting, 
mystical atmosphere, cinematic composition, professional photography style
```

**Output**: Background image saved to `_temp_pdf_examples/river_king_background.png`

### Step 2: Generate Character Art

**Tool**: PixelLab  
**Action**: Create pixel art character

**Character Description**:
- Mysterious figure in worn velvet jacket (color of river mud)
- Eyes that shift like the Mississippi
- Hands moving with jazz pianist fluidity
- Deck of cards that seems to shuffle itself
- New Orleans style, pixel art, 8-directional views

**Output**: Character sprites saved to `_temp_pdf_examples/river_king_character/`

### Step 3: Create Card Composition

**Tool**: Deckz Poker Visualization  
**Purpose**: Generate card arrangements as visual elements

The cards below represent The River King's power made visible.

### Step 4: Composite Final Artwork

**Process**:
1. Load background image
2. Position character art
3. Overlay card arrangements
4. Adjust opacity and blending
5. Final composite: Mixed media artwork

---

## Card Elements

The cards represent The River King's essence:
- **Spades**: The river, the flow, time
- **Hearts**: The jazz, the passion, emotion  
- **Diamonds**: The stakes, the wealth, material
- **Clubs**: The rules, the structure, mathematics

---

## Tools Integration

### Available MCP Tools

1. **Nano-Banana (Gemini)**
   - Generate photorealistic backgrounds
   - Create atmospheric scenes
   - Style: Professional photography

2. **PixelLab**
   - Generate pixel art characters
   - Create game-style sprites
   - 8-directional character views

3. **Deckz Poker**
   - Visualize card arrangements
   - Create card compositions
   - Generate PDF with card art

### Integration Pattern

```
AI Image Generation → Card Visualization → Composition → Final Artwork
     (Nano-Banana)      (Deckz Poker)      (Layering)    (Mixed Media)
```

---

## Example Prompts

### Background (Nano-Banana)
```
New Orleans jazz club at night, Mississippi River, neon lights, 
wet streets, atmospheric, mystical, cinematic, professional photography
```

### Character (PixelLab)
```
Mysterious card dealer, velvet jacket, New Orleans style, 
pixel art, 8 directions, mystical, gambling demi-god
```

### Cards (Deckz Poker)
```
Royal Flush of Spades - The River King's sacred hand
Royal Flush of Hearts - The mirror hand
```

---

## Next Steps

To complete the artwork:

1. **Generate Background**:
   Use MCP tool: mcp_nano-banana_generate_image
   Prompt: "New Orleans jazz club at night, Mississippi River..."

2. **Generate Character**:
   Use MCP tool: mcp_pixellab_create_character
   Character description: "Mysterious card dealer..."

3. **Composite**:
   - Use image editing software
   - Layer: Background → Character → Cards
   - Adjust blending and opacity
   - Final mixed media artwork

---

*"The cards provide structure. The images provide atmosphere. Together, they create art."*
"""

    # Create card composition
    players = [
        Player(name="The Sacred Hand (Spades)", cards=["AS", "KS", "QS", "JS", "10S"]),
        Player(name="The Mirror Hand (Hearts)", cards=["AH", "KD", "QC", "JH", "10H"]),
        Player(name="The Stakes (Diamonds)", cards=["AD", "KD", "QD", "JD", "10D"]),
        Player(name="The Rules (Clubs)", cards=["AC", "KC", "QC", "JC", "10C"]),
    ]

    output_path = Path("_temp_pdf_examples/river_king_mixed_media_art.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_deckz_poker(
        title="The River King: Mixed Media Artwork",
        content=content,
        output_path=output_path,
        players=players,
        card_format="large",
        show_rules=False,
    )

    return pdf_path


def generate_image_prompts_guide():
    """Generate a guide with prompts for image generation tools."""

    content = """
# Image Generation Prompts for Card Art

## Background Images (Nano-Banana/Gemini)

### New Orleans Jazz Club
```
New Orleans jazz club exterior at night, Mississippi River visible in background, 
neon lights reflecting on wet streets, atmospheric moody lighting, 
mystical atmosphere, cinematic composition, professional photography style, 
warm colors, depth of field, bokeh effects
```

### Riverboat Casino
```
Mississippi River riverboat casino at sunset, New Orleans skyline in distance,
golden hour lighting, steam rising from river, atmospheric, cinematic,
professional photography, warm tones, dramatic sky
```

### Back Alley Game
```
Dark back alley in New Orleans, single light source from window,
card game in progress, mysterious atmosphere, film noir style,
high contrast, dramatic shadows, cinematic composition
```

## Character Art (PixelLab)

### The River King - Pixel Art
```
Mysterious card dealer character, worn velvet jacket color of river mud,
eyes that shift colors, hands moving fluidly, deck of cards,
New Orleans style, pixel art, 8-directional views, mystical demi-god,
gambling theme, atmospheric
```

### Card Spirits - Pixel Art
```
Small pixel art spirits made of playing cards, floating, ethereal,
New Orleans voodoo style, mystical, animated, 4-directional views
```

## Integration Workflow

1. Generate background image
2. Generate character art
3. Create card composition (this system)
4. Composite all elements
5. Final mixed media artwork

## Tools

- **Nano-Banana**: Photorealistic backgrounds
- **PixelLab**: Pixel art characters and sprites
- **Deckz Poker**: Card visualizations
- **Image Editor**: Compositing and layering
"""

    output_path = Path("_temp_pdf_examples/image_generation_prompts_guide.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf_path = generate_deckz_poker(
        title="Image Generation Prompts for Card Art",
        content=content,
        output_path=output_path,
        players=None,
        card_format="medium",
        show_rules=False,
    )

    return pdf_path


if __name__ == "__main__":
    print("=" * 60)
    print("Card Art with AI-Generated Images")
    print("=" * 60)
    print()

    pdf1 = generate_river_king_artwork()
    print(f"✅ Generated: {pdf1}")
    print()

    pdf2 = generate_image_prompts_guide()
    print(f"✅ Generated: {pdf2}")
    print()

    print("=" * 60)
    print("✅ Card art compositions ready for image integration!")
    print("=" * 60)
    print()
    print("💡 Use MCP tools to generate images:")
    print("   - Nano-Banana: Background images")
    print("   - PixelLab: Character art")
    print("   - Then composite with these card PDFs")
    print("=" * 60)

    # Open PDFs
    import subprocess

    subprocess.run(["open", str(pdf1)])
    subprocess.run(["open", str(pdf2)])
