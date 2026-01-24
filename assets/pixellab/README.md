# PixelLab Assets

AI-generated pixel art characters for the WAFT Storyteller.

## Quick Use (Sprites)

Simple south-facing sprites for UI integration:

```
sprites/
├── grok.png      # Half-orc bartender
├── bard.png      # Tavern bard with lute
└── stranger.png  # Hooded mysterious figure
```

## Full Character Data

Complete character packs with all rotations and metadata:

```
characters/
├── grok_bartender/
│   ├── rotations/     # south, east, north, west (64x64)
│   └── metadata.json  # PixelLab character data
├── tavern_bard/
│   └── ...
└── the_stranger/
    └── ...
```

## Character Details

| Character | Size | Directions | Description |
|-----------|------|------------|-------------|
| Grok | 64x64 | 4 | Half-orc bartender with green skin |
| Bard | 64x64 | 4 | Red-haired bard with lute |
| Stranger | 64x64 | 4 | Hooded figure, mysterious |

## PixelLab IDs (for animations)

- **Grok**: `eefc2491-d6ae-40f1-9e5a-3405c29c45f7`
- **Bard**: `93e6c89b-94a0-4592-90f7-d9bdeb8fc596`
- **Stranger**: `5bad8d94-e008-43d7-a821-b14756b778e5`

To add animations:
```
animate_character(character_id="...", template_animation_id="walk")
```

## Downloaded

2026-01-23 by AI assistant.
