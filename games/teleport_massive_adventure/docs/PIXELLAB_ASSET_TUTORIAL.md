# PixelLab Asset Generation Tutorial
## Complete Guide to Creating Game Assets with PixelLab MCP

**Date:** 2026-01-25  
**Game:** Teleport Massive: The Adventure

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Generating Characters](#generating-characters)
4. [Generating Map Objects](#generating-map-objects)
5. [Downloading Assets](#downloading-assets)
6. [Integrating into Game](#integrating-into-game)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This tutorial shows you how to use PixelLab's MCP (Model Context Protocol) tools to generate pixel art assets for your game, download them, and integrate them seamlessly.

**What You'll Learn:**
- How to generate character sprites with multiple directions
- How to create map objects and items
- How to download and organize assets
- How to integrate assets into Phaser.js games
- How to handle animations and naming conventions

---

## Prerequisites

### Required
- PixelLab MCP server configured (see `AGENTS.md`)
- Access to PixelLab API (free tier or higher)
- Basic knowledge of terminal/command line
- Understanding of your game's asset structure

### Tools Used
- `curl` - For downloading assets
- `unzip` - For extracting character ZIP files
- MCP tools via Cursor/Claude

---

## Generating Characters

### Step 1: Plan Your Character

Before generating, decide:
- **Name:** What will you call this character?
- **Description:** Detailed appearance description
- **Directions:** 4 (N/S/E/W) or 8 (includes diagonals)
- **Size:** Canvas size (16-128px, character is ~60% of height)
- **Style:** Shading, detail level, outline style

### Step 2: Generate Character

Use the `create_character` MCP tool:

```javascript
call_mcp_tool('user-pixellab', 'create_character', {
    'name': 'Heavy Guard',
    'description': 'large cyberpunk heavy security guard in heavy armor, bulky exoskeleton, carrying heavy weapon, intimidating presence',
    'n_directions': 4,
    'size': 64,
    'view': 'low top-down',
    'shading': 'medium shading',
    'detail': 'high detail'
});
```

**Parameters Explained:**
- `name`: Reference name (optional but helpful)
- `description`: Detailed visual description - be specific!
- `n_directions`: 4 or 8 (4 is faster, 8 is more detailed)
- `size`: Canvas size (16-128px). Character height ≈ 60% of size
- `view`: `'low top-down'`, `'high top-down'`, or `'side'`
- `shading`: `'flat'`, `'basic'`, `'medium'`, or `'detailed'`
- `detail`: `'low'`, `'medium'`, or `'high'`
- `outline`: `'single color outline'`, `'selective outline'`, or `'lineless'`

**Example Responses:**
```
✅ Character generation queued!

Character ID: 1252c1a9-d9fb-4dd7-959d-5f5f58e49a7e
Name: Heavy Guard
Status: Processing in background

Generation takes ~2-3 minutes
```

### Step 3: Check Status

Wait 2-3 minutes, then check:

```javascript
call_mcp_tool('user-pixellab', 'get_character', {
    'character_id': '1252c1a9-d9fb-4dd7-959d-5f5f58e49a7e'
});
```

**When Ready:**
- You'll get rotation image URLs
- Download ZIP link will be available
- Character metadata included

### Step 4: Add Animations (Optional)

Once character is ready, add animations:

```javascript
call_mcp_tool('user-pixellab', 'animate_character', {
    'character_id': '1252c1a9-d9fb-4dd7-959d-5f5f58e49a7e',
    'template_animation_id': 'walk',
    'action_description': 'heavy armored walk',
    'animation_name': 'walk'
});
```

**Available Animations:**
- `walk`, `walking-4-frames`, `walking-8-frames`
- `running-4-frames`, `running-6-frames`, `running-8-frames`
- `fight-stance-idle-8-frames`
- `cross-punch`, `lead-jab`, `high-kick`, `roundhouse-kick`
- `jumping-1`, `jumping-2`, `crouching`
- And many more! (See AutoPlayer.js for full list)

---

## Generating Map Objects

### Step 1: Plan Your Object

Decide:
- **Description:** What is it? Be specific about style
- **Size:** Width and height (32-400px each)
- **View:** Usually `'high top-down'` for items
- **Purpose:** Item, prop, or decoration?

### Step 2: Generate Object

```javascript
call_mcp_tool('user-pixellab', 'create_map_object', {
    'description': 'cyberpunk access card, security badge with holographic display, glowing blue edge, high-tech design, small item',
    'width': 32,
    'height': 32,
    'view': 'high top-down',
    'outline': 'single color outline',
    'shading': 'medium shading',
    'detail': 'high detail'
});
```

**Parameters:**
- `description`: Detailed visual description
- `width`: 32-400px
- `height`: 32-400px
- `view`: `'low top-down'`, `'high top-down'`, or `'side'`
- `outline`: `'single color outline'`, `'selective outline'`, or `'lineless'`
- `shading`: `'flat'`, `'basic'`, `'medium'`, or `'detailed'`
- `detail`: `'low'`, `'medium'`, or `'high'`

**Response:**
```
✅ Map object generation queued!

Object ID: 0aa08363-d735-4183-98f4-df6510c9918a
Status: Processing in background
Generation takes ~30-90 seconds
```

### Step 3: Check Status

Wait 30-90 seconds, then:

```javascript
call_mcp_tool('user-pixellab', 'get_map_object', {
    'object_id': '0aa08363-d735-4183-98f4-df6510c9918a'
});
```

**When Ready:**
- Direct download URL provided
- Image is transparent PNG
- Ready to use immediately

---

## Downloading Assets

### Characters (ZIP Download)

Characters come as ZIP files with rotations, frames, and animations:

```bash
# Download character ZIP
curl --fail -o /tmp/heavy_guard.zip \
  "https://api.pixellab.ai/mcp/characters/1252c1a9-d9fb-4dd7-959d-5f5f58e49a7e/download"

# Extract to game assets
unzip -q -o /tmp/heavy_guard.zip \
  -d games/teleport_massive_adventure/assets/characters/heavy_guard_extracted/
```

**ZIP Structure:**
```
heavy_guard_extracted/
├── rotations/
│   ├── south.png
│   ├── east.png
│   ├── north.png
│   └── west.png
├── frames/ (if available)
├── animations/
│   └── walk/
│       ├── south/frame_000.png
│       └── ...
└── metadata.json
```

**Fix File Structure:**
```bash
# Copy rotations to frames (if needed)
cp assets/characters/heavy_guard_extracted/rotations/*.png \
   assets/characters/heavy_guard_extracted/frames/

# Rename to match game convention
cd assets/characters/heavy_guard_extracted/frames/
for dir in north south east west; do
  mv ${dir}.png heavy_guard_${dir}.png
done
```

### Map Objects (Direct PNG)

Objects are single PNG files:

```bash
# Download object
curl --fail -o assets/objects/access_card.png \
  "https://api.pixellab.ai/mcp/map-objects/0aa08363-d735-4183-98f4-df6510c9918a/download"

# Create _obj version (for game)
cp assets/objects/access_card.png assets/objects/access_card_obj.png
```

**Important:** Always use `curl --fail` to detect HTTP errors properly!

---

## Integrating into Game

### Step 1: Add to Preload

In `index_v2.html` BootScene `preload()`:

```javascript
// Load enemy characters
const enemies = ['heavy_guard', 'security_drone', 'core_boss'];
const directions = ['north', 'south', 'east', 'west'];

enemies.forEach(enemy => {
    directions.forEach(dir => {
        const key = `${enemy}_${dir}`;
        const path = `assets/characters/${enemy}_extracted/frames/${enemy}_${dir}.png`;
        this.load.image(key, path);
    });
});

// Load objects
this.load.image('access_card', 'assets/objects/access_card.png');
this.load.image('access_card_obj', 'assets/objects/access_card_obj.png');
```

### Step 2: Add to Items JSON

In `data/items.json`:

```json
{
  "access_card": {
    "id": "access_card",
    "name": "Access Card",
    "description": "A high-level access card with holographic display.",
    "icon": "🔑",
    "sprite": "access_card_obj",
    "usableOn": ["upper_level_door"],
    "consumeOnUse": false
  }
}
```

### Step 3: Create NPCs (Enemies)

In your scene or room JSON:

```javascript
// Create enemy NPC
const heavyGuard = npcSystem.createNPC('heavy_guard_1', {
    name: 'Heavy Guard',
    type: 'enemy',
    x: 300,
    y: 400,
    hostile: true,
    hp: 80,
    attack: 12,
    defense: 6,
    detectionRange: 120
});

// Set patrol route
heavyGuard.setPatrolRoute([
    { x: 300, y: 400 },
    { x: 500, y: 400 },
    { x: 500, y: 500 },
    { x: 300, y: 500 }
]);

// Create sprite
const guardSprite = this.add.sprite(
    heavyGuard.x,
    heavyGuard.y,
    'heavy_guard_south'
).setScale(2).setDepth(5);
```

### Step 4: Add to Rooms JSON

In `data/rooms.json`:

```json
{
  "corridor": {
    "hotspots": [
      {
        "id": "access_card",
        "name": "Access Card",
        "position": { "x": 500, "y": 350 },
        "sprite": "access_card_obj",
        "interactions": {
          "pickup": {
            "action": "addItem",
            "item": "access_card"
          }
        }
      }
    ],
    "npcs": [
      {
        "id": "heavy_guard_1",
        "name": "Heavy Guard",
        "position": { "x": 300, "y": 400 },
        "sprite": "heavy_guard_south",
        "type": "enemy",
        "hostile": true
      }
    ]
  }
}
```

---

## Best Practices

### Character Descriptions

**✅ Good:**
```
"cyberpunk security guard with glitch effects, pixelated corruption, 
wearing tactical armor, holding energy weapon, menacing stance"
```

**❌ Bad:**
```
"guard"  // Too vague
```

**Tips:**
- Include style keywords: "cyberpunk", "sci-fi", "pixel art"
- Describe clothing/armor
- Mention weapons or tools
- Add mood/attitude: "menacing", "friendly", "intimidating"
- Specify size: "large", "small", "bulky"

### Object Descriptions

**✅ Good:**
```
"cyberpunk access card, security badge with holographic display, 
glowing blue edge, high-tech design, small item"
```

**❌ Bad:**
```
"card"  // Too vague
```

**Tips:**
- Match your game's art style
- Include size reference: "small", "large", "tall"
- Mention special effects: "glowing", "holographic", "pulsing"
- Describe materials: "metallic", "crystalline", "plastic"

### File Organization

```
assets/
├── characters/
│   ├── heavy_guard_extracted/
│   │   ├── frames/
│   │   │   ├── heavy_guard_north.png
│   │   │   ├── heavy_guard_south.png
│   │   │   ├── heavy_guard_east.png
│   │   │   └── heavy_guard_west.png
│   │   ├── rotations/ (original)
│   │   ├── animations/ (if any)
│   │   └── metadata.json
│   └── ...
└── objects/
    ├── access_card.png
    ├── access_card_obj.png
    └── ...
```

### Naming Conventions

**Characters:**
- Sprite keys: `{character_name}_{direction}` (e.g., `heavy_guard_south`)
- File names: `{character_name}_{direction}.png`

**Objects:**
- Main file: `{object_name}.png`
- Game version: `{object_name}_obj.png` (for consistency)

---

## Troubleshooting

### "Rate limit exceeded"

**Problem:** Too many jobs queued (free tier: 8 concurrent)

**Solution:**
- Wait 2-4 minutes for jobs to complete
- Check status: `get_character(character_id)`
- Upgrade subscription for more slots (Tier 2: 20, Tier 3: 30)

### "Insufficient job slots"

**Problem:** Trying to queue animation but no slots available

**Solution:**
- Wait for character generation to finish first
- Animations need 4 slots (one per direction)
- Queue animations after base character is ready

### "423 Locked" Error

**Problem:** Character still processing, ZIP not ready

**Solution:**
- Wait 2-3 more minutes
- Check status again
- Don't retry too quickly (rate limiting)

### Wrong File Structure

**Problem:** Files in `rotations/` but game expects `frames/`

**Solution:**
```bash
# Copy rotations to frames
cp assets/characters/{char}_extracted/rotations/*.png \
   assets/characters/{char}_extracted/frames/

# Rename to match convention
cd assets/characters/{char}_extracted/frames/
for dir in north south east west; do
  mv ${dir}.png {char}_${dir}.png
done
```

### Assets Not Loading

**Problem:** Game can't find sprite files

**Check:**
1. File paths in preload match actual file locations
2. File names match sprite keys exactly
3. Files exist (check with `ls`)
4. No typos in character/object names

**Debug:**
```javascript
// In preload, log what you're loading
console.log(`Loading: ${key} from ${path}`);
this.load.image(key, path);

// Check if texture exists after load
this.load.once('complete', () => {
    console.log('Textures:', this.textures.list);
});
```

### Character Looks Wrong

**Problem:** Generated character doesn't match description

**Solutions:**
- Be more specific in description
- Add style keywords matching your game
- Try different `shading` or `detail` levels
- Use `ai_freedom` parameter (100=strict, 999=creative)

---

## Complete Workflow Example

### Generate Enemy Character

```javascript
// 1. Generate
const result = call_mcp_tool('user-pixellab', 'create_character', {
    'name': 'Glitch Guard',
    'description': 'cyberpunk security guard with glitch effects, pixelated corruption, tactical armor, energy weapon',
    'n_directions': 4,
    'size': 64,
    'view': 'low top-down'
});
// Returns: character_id = 'ce370ece-d940-464f-adbf-e27781101755'

// 2. Wait 2-3 minutes

// 3. Check status
const status = call_mcp_tool('user-pixellab', 'get_character', {
    'character_id': 'ce370ece-d940-464f-adbf-e27781101755'
});

// 4. Download
curl --fail -o /tmp/glitch_guard.zip \
  "https://api.pixellab.ai/mcp/characters/ce370ece-d940-464f-adbf-e27781101755/download"

// 5. Extract
unzip -q -o /tmp/glitch_guard.zip \
  -d assets/characters/glitch_guard_extracted/

// 6. Fix structure
cp assets/characters/glitch_guard_extracted/rotations/*.png \
   assets/characters/glitch_guard_extracted/frames/
cd assets/characters/glitch_guard_extracted/frames/
for dir in north south east west; do
  mv ${dir}.png glitch_guard_${dir}.png
done

// 7. Add to game preload
// (See "Integrating into Game" section)
```

### Generate Map Object

```javascript
// 1. Generate
const result = call_mcp_tool('user-pixellab', 'create_map_object', {
    'description': 'cyberpunk health kit, medical supply box with red cross, glowing green effect',
    'width': 48,
    'height': 48,
    'view': 'high top-down'
});
// Returns: object_id = '7d2668c1-8ef1-47bc-85dd-7242a458dcee'

// 2. Wait 30-90 seconds

// 3. Check status
const status = call_mcp_tool('user-pixellab', 'get_map_object', {
    'object_id': '7d2668c1-8ef1-47bc-85dd-7242a458dcee'
});

// 4. Download
curl --fail -o assets/objects/health_kit.png \
  "https://api.pixellab.ai/mcp/map-objects/7d2668c1-8ef1-47bc-85dd-7242a458dcee/download"

// 5. Create _obj version
cp assets/objects/health_kit.png assets/objects/health_kit_obj.png

// 6. Add to game
// (See "Integrating into Game" section)
```

---

## Quick Reference

### Character Generation Checklist
- [ ] Write detailed description
- [ ] Choose directions (4 or 8)
- [ ] Set canvas size (16-128px)
- [ ] Select view angle
- [ ] Choose shading/detail level
- [ ] Generate and wait
- [ ] Download ZIP
- [ ] Extract and fix structure
- [ ] Add to preload
- [ ] Create NPC in game

### Object Generation Checklist
- [ ] Write detailed description
- [ ] Set width and height
- [ ] Choose view angle
- [ ] Generate and wait
- [ ] Download PNG
- [ ] Create _obj version
- [ ] Add to preload
- [ ] Add to items.json or rooms.json

### Integration Checklist
- [ ] Files in correct locations
- [ ] Preload code added
- [ ] Sprite keys match file names
- [ ] Items added to items.json
- [ ] NPCs created in scenes
- [ ] Test in game

---

## Resources

- **PixelLab Docs:** See `docs/PIXELLAB_ASSET_PIPELINE.md`
- **Asset Log:** See `assets/GENERATED_ASSETS.md`
- **Game Plan:** See `GAME_PLAN.md` for asset requirements
- **MCP Tools:** Available via `user-pixellab` server

---

## Tips & Tricks

1. **Batch Generation:** Queue multiple characters at once (up to 8 on free tier)
2. **Save IDs:** Keep a list of character/object IDs for easy reference
3. **Test Early:** Download one asset first to verify workflow
4. **Consistent Style:** Use similar descriptions for matching art style
5. **Animations Later:** Generate base character first, add animations after
6. **Backup Assets:** Download and save locally (assets expire after 8 hours)

---

**Happy Asset Creating! 🎨**

For questions or issues, check the troubleshooting section or review the generated assets in `assets/GENERATED_ASSETS.md`.
