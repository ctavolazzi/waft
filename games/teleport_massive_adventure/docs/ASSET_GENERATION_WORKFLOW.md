# Asset Generation Workflow
## Using PixelLab MCP Tools Directly in Cursor

Reference: [PixelLab MCP Docs](https://api.pixellab.ai/mcp/docs)

---

## Key Insight: Non-Blocking Operations

All PixelLab MCP tools return **immediately** with job IDs. Processing happens in background (2-5 minutes).

```
1. Call create_character → Get character_id instantly
2. Queue animations immediately (no waiting!)
3. Check status later with get_character
4. Download when ready
```

---

## Available MCP Tools

| Tool | Purpose | Time |
|------|---------|------|
| `create_character` | 4 or 8 directional views | 2-5 min |
| `animate_character` | Add animation to character | 2-4 min |
| `get_character` | Check status, get download URL | Instant |
| `list_characters` | See all your characters | Instant |
| `create_topdown_tileset` | Wang tileset (16 tiles) | 3-5 min |
| `create_isometric_tile` | Single isometric tile | 1-2 min |
| `create_map_object` | Object with transparency | 1-2 min |

---

## Character Generation Calls

### 1. Create Dr. Vance (Security Chief)

```
MCP Tool: create_character
Server: user-pixellab

Arguments:
{
  "description": "Corporate security chief in dark tactical armor, stern expression, military badge on chest, gray buzzcut hair, cyberpunk style, intimidating posture",
  "name": "vance",
  "n_directions": 4,
  "size": 64,
  "proportions": {"type": "preset", "name": "heroic"},
  "outline": "single color black outline",
  "shading": "soft shading",
  "detail": "high detail",
  "view": "low top-down"
}
```

### 2. Create ARIA (AI Hologram)

```
MCP Tool: create_character
Server: user-pixellab

Arguments:
{
  "description": "AI hologram assistant, translucent blue humanoid figure, geometric circuit patterns on skin, friendly feminine face, glowing edges, digital particles around body",
  "name": "aria",
  "n_directions": 4,
  "size": 64,
  "proportions": {"type": "preset", "name": "stylized"},
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "high detail",
  "view": "low top-down"
}
```

### 3. Create Maya (Echo/Ghost)

```
MCP Tool: create_character
Server: user-pixellab

Arguments:
{
  "description": "Ghostly woman with fading transparent edges, warm amber and gold colors, sad gentle expression, flowing hair, memory fragment aesthetic, partially see-through",
  "name": "maya_echo",
  "n_directions": 4,
  "size": 64,
  "proportions": {"type": "preset", "name": "default"},
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "medium detail",
  "view": "low top-down"
}
```

### 4. Create Elder Phaseburner

```
MCP Tool: create_character
Server: user-pixellab

Arguments:
{
  "description": "Elderly figure in tattered dark robes, heavily glitched appearance with pixel distortion, wise weathered face, reality bending around them, purple energy wisps",
  "name": "elder_phaseburner",
  "n_directions": 4,
  "size": 64,
  "proportions": {"type": "preset", "name": "default"},
  "outline": "single color black outline",
  "shading": "hard shading",
  "detail": "high detail",
  "view": "low top-down"
}
```

### 5. Create CEO Hologram

```
MCP Tool: create_character
Server: user-pixellab

Arguments:
{
  "description": "Corporate executive hologram projection, expensive suit, slicked back hair, untrustworthy politician smile, blue holographic glow, slightly transparent",
  "name": "ceo_hologram",
  "n_directions": 4,
  "size": 64,
  "proportions": {"type": "preset", "name": "realistic_male"},
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "high detail",
  "view": "low top-down"
}
```

---

## Animation Calls

Once characters are created, queue animations immediately (no need to wait!):

### Walking Animation

```
MCP Tool: animate_character
Server: user-pixellab

Arguments:
{
  "character_id": "<character_id_from_create>",
  "template_animation_id": "walking",
  "action_description": "walking cautiously",
  "animation_name": "walk"
}
```

### Idle Animation

```
MCP Tool: animate_character
Server: user-pixellab

Arguments:
{
  "character_id": "<character_id_from_create>",
  "template_animation_id": "breathing-idle",
  "action_description": "standing alert",
  "animation_name": "idle"
}
```

### Available Animation Templates

```
breathing-idle      - Subtle breathing
walking             - Walk cycle
running             - Run cycle  
jumping             - Jump
falling-back-death  - Death animation
fight-stance-idle   - Combat ready
cross-punch         - Attack
drinking            - Interaction
fireball            - Special ability
flying-kick         - Action move
crouched-walking    - Stealth walk
crouching           - Crouch
backflip            - Acrobatics
```

---

## Map Object Calls

### Research Terminal

```
MCP Tool: create_map_object
Server: user-pixellab

Arguments:
{
  "description": "sci-fi research terminal with holographic display screen, blue glow, sleek futuristic design, control panels",
  "width": 96,
  "height": 96,
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "medium shading",
  "detail": "high detail"
}
```

### Artifact on Pedestal

```
MCP Tool: create_map_object
Server: user-pixellab

Arguments:
{
  "description": "glowing crystalline artifact on metal pedestal, purple cosmic energy, mysterious ancient object",
  "width": 64,
  "height": 64,
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "soft shading",
  "detail": "high detail"
}
```

### Security Keycard

```
MCP Tool: create_map_object
Server: user-pixellab

Arguments:
{
  "description": "corporate security keycard on floor, blue and white, magnetic stripe, ID photo",
  "width": 32,
  "height": 32,
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "basic shading",
  "detail": "medium detail"
}
```

### Server Rack

```
MCP Tool: create_map_object
Server: user-pixellab

Arguments:
{
  "description": "tall server rack with blinking lights, cables, futuristic data center equipment, blue LEDs",
  "width": 64,
  "height": 128,
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "medium shading",
  "detail": "high detail"
}
```

### Executive Desk

```
MCP Tool: create_map_object
Server: user-pixellab

Arguments:
{
  "description": "luxury executive desk with holographic computer display, expensive wood, corporate style",
  "width": 128,
  "height": 64,
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "soft shading",
  "detail": "high detail"
}
```

---

## Tileset Calls

### Lab Floor Tileset

```
MCP Tool: create_topdown_tileset
Server: user-pixellab

Arguments:
{
  "lower_description": "dark metallic laboratory floor with subtle grid pattern, sci-fi clean",
  "upper_description": "raised platform section with glowing blue edge lighting",
  "tile_size": {"width": 32, "height": 32},
  "view": "high top-down",
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "high detail",
  "transition_size": 0.25
}
```

### Corporate Floor Tileset

```
MCP Tool: create_topdown_tileset
Server: user-pixellab

Arguments:
{
  "lower_description": "polished dark marble floor with subtle reflection",
  "upper_description": "luxury carpet section with corporate pattern",
  "tile_size": {"width": 32, "height": 32},
  "view": "high top-down",
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "medium detail",
  "transition_size": 0.25
}
```

### Underground Tileset

```
MCP Tool: create_topdown_tileset
Server: user-pixellab

Arguments:
{
  "lower_description": "cracked concrete floor with water puddles and grime",
  "upper_description": "metal grating and exposed pipes",
  "tile_size": {"width": 32, "height": 32},
  "view": "high top-down",
  "outline": "single color outline",
  "shading": "hard shading",
  "detail": "high detail",
  "transition_size": 0.5
}
```

### Void Tileset

```
MCP Tool: create_topdown_tileset
Server: user-pixellab

Arguments:
{
  "lower_description": "cosmic void with swirling dark purple and black nebula",
  "upper_description": "floating geometric platforms with glowing edges",
  "tile_size": {"width": 32, "height": 32},
  "view": "high top-down",
  "outline": "lineless",
  "shading": "soft shading",
  "detail": "high detail",
  "transition_size": 0.0
}
```

---

## Workflow: Generate All Assets

### Step 1: Create All Characters (Batch)

Call `create_character` for each NPC. Save the `character_id` values.

```
vance_id = create_character(vance_args)
aria_id = create_character(aria_args)
maya_id = create_character(maya_args)
elder_id = create_character(elder_args)
ceo_id = create_character(ceo_args)
```

### Step 2: Queue All Animations (Immediately)

Don't wait for characters to finish - queue animations right away:

```
animate_character(vance_id, "walking")
animate_character(vance_id, "breathing-idle")
animate_character(aria_id, "breathing-idle")
animate_character(maya_id, "breathing-idle")
...
```

### Step 3: Create Map Objects

```
create_map_object(terminal_args)
create_map_object(artifact_args)
create_map_object(keycard_args)
...
```

### Step 4: Create Tilesets

```
create_topdown_tileset(lab_args)
create_topdown_tileset(corporate_args)
create_topdown_tileset(underground_args)
create_topdown_tileset(void_args)
```

### Step 5: Check Status (After 5 Minutes)

```
get_character(vance_id)  # Check if ready
get_character(aria_id)
...
```

### Step 6: Download Assets

Characters return a ZIP download URL containing all directions and animations.

---

## Checking Status

### Check Character Status

```
MCP Tool: get_character
Server: user-pixellab

Arguments:
{
  "character_id": "<character_id>",
  "include_preview": true
}
```

Returns:
- Status: completed/processing/failed
- Download URL for ZIP
- All rotation images
- Animation statuses

### Check Tileset Status

```
MCP Tool: get_topdown_tileset
Server: user-pixellab

Arguments:
{
  "tileset_id": "<tileset_id>"
}
```

---

## Cost Estimation

Based on PixelLab pricing:

| Asset | Count | Est. Credits |
|-------|-------|--------------|
| Characters (4-dir) | 5 | ~25 |
| Animations | 10 | ~20 |
| Map Objects | 20 | ~20 |
| Tilesets | 4 | ~20 |
| **Total** | | **~85 credits** |

---

## Integration with Game

Once assets are downloaded:

1. Extract ZIPs to `assets/characters/{name}/`
2. Update `index_v2.html` preload section
3. Add to room data JSON files
4. Character sprites use format: `{name}_{direction}`

Example integration:
```javascript
// In BootScene preload
const newChars = ['vance', 'aria', 'maya_echo', 'elder', 'ceo'];
const directions = ['north', 'south', 'east', 'west'];

newChars.forEach(char => {
  directions.forEach(dir => {
    this.load.image(`${char}_${dir}`, `assets/characters/${char}/${char}_${dir}.png`);
  });
});
```

---

## Quick Reference: Tool Names

When calling from Cursor MCP:

```
Server: user-pixellab

Tools:
- create_character
- animate_character
- get_character
- list_characters
- delete_character
- create_topdown_tileset
- get_topdown_tileset
- list_topdown_tilesets
- delete_topdown_tileset
- create_isometric_tile
- get_isometric_tile
- list_isometric_tiles
- delete_isometric_tile
- create_map_object
- get_map_object
```
