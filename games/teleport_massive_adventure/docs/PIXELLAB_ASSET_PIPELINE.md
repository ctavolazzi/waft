# PixelLab Asset Pipeline
## Automated Art Generation for Teleport Massive

Reference: [PixelLab API v2](https://api.pixellab.ai/v2/llms.txt)

---

## Available Endpoints We'll Use

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| `/create-character-with-4-directions` | Generate character facing N/S/E/W | NPCs, player |
| `/create-character-with-8-directions` | 8 directional views | Detailed characters |
| `/characters/animations` | Animate existing character | Walk, idle, attack |
| `/create-image-pixflux` | Single sprite/object | Items, props |
| `/map-objects` | Objects with transparency | Furniture, pickups |
| `/create-tileset` | Wang tileset (16-23 tiles) | Room backgrounds |
| `/create-isometric-tile` | Isometric tiles | Optional iso view |

---

## Character Generation

### Creating a New NPC

```javascript
// Example: Generate Dr. Vance (Security Chief)
const response = await fetch('https://api.pixellab.ai/v2/create-character-with-4-directions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    description: "Corporate security chief in dark tactical suit, stern expression, badge on chest, short gray hair, cyberpunk style",
    image_size: { width: 64, height: 64 },
    outline: "medium",
    shading: "soft",
    detail: "high",
    view: "side",
    no_background: true
  })
});

const { character_id, background_job_id } = await response.json();
```

### Animation Templates Available

From the API docs, these animation templates are available:
- `breathing-idle` - Subtle idle animation
- `walking` - Walk cycle
- `running` - Run cycle
- `jumping` - Jump animation
- `falling-back-death` - Death animation
- `fight-stance-idle-8-frames` - Combat ready
- `cross-punch` - Attack
- `drinking` - Interaction
- `fireball` - Special ability
- `flying-kick` - Action move

### Animating a Character

```javascript
// Add walk animation to existing character
const animResponse = await fetch('https://api.pixellab.ai/v2/characters/animations', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    character_id: "abc-123-character-id",
    template_animation_id: "walking",
    action_description: "walking cautiously through dark corridor",
    directions: ["south", "north", "east", "west"]
  })
});
```

---

## Characters Needed

### Priority 1 (Core Story)

| Character | Description | Animations |
|-----------|-------------|------------|
| **Dr. Vance** | Security Chief, antagonist. Dark tactical suit, stern, badge, gray hair. | idle, walking, pointing |
| **ARIA** | TM AI hologram. Blue translucent figure, geometric, friendly. | idle, talking, glitching |
| **Maya (Echo)** | Aziah's wife, fragmented. Fading edges, warm colors, sad expression. | idle, reaching, fading |
| **Elder Phaseburner** | Leader of underground. Heavily glitched, robes, wise. | idle, talking, phasing |
| **CEO Hologram** | Pre-recorded executive. Expensive suit, slick, untrustworthy. | talking, gesturing |

### Priority 2 (World Building)

| Character | Description | Animations |
|-----------|-------------|------------|
| **Maintenance Bot** | Server room robot. Boxy, utilitarian, helpful. | idle, working |
| **Phaseburner NPCs** (3-5) | Various victims. Glitchy, diverse, sympathetic. | idle, talking |
| **TM Employees** (2-3) | Background characters. Corporate casual, oblivious. | idle, walking |

---

## Map Objects Needed

### Using `/map-objects` endpoint

```javascript
// Example: Generate research terminal
const objResponse = await fetch('https://api.pixellab.ai/v2/map-objects', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    description: "sci-fi research terminal with holographic display, blue glow, sleek design",
    image_size: { width: 96, height: 96 },
    view: "high top-down",
    outline: "medium",
    shading: "soft",
    detail: "high"
  })
});
```

### Objects by Room

#### Lab
- Research terminal (96x96)
- Strange artifact on pedestal (64x64)
- Photo frame (32x32)
- Lab equipment / beakers (48x48)
- Door (64x96)

#### Lobby
- Reception desk (128x64)
- TM holographic logo (96x64)
- Security checkpoint (64x64)
- Keycard on floor (32x32)
- Maintenance hatch (64x48)

#### Underground
- Damaged terminal (64x64)
- Steam pipes (various)
- Debris piles (48x48)
- Makeshift shelter (96x64)
- Portal (80x80)

#### Server Room (New)
- Server racks (64x128) x3
- Cooling unit (48x64)
- Access panel (32x32)
- Data cables (decorative)

#### Executive Suite (New)
- Executive desk (128x64)
- Holographic conference table (160x80)
- Art pieces (48x64)
- Vault door (64x96)
- Trophy case (48x64)

#### The Between (New)
- Memory fragments (32x32) x5
- Floating platforms (64x32)
- Reality tears (48x64)
- Maya's silhouette (64x64)

---

## Tilesets

### Using `/create-tileset` endpoint

```javascript
// Example: Lab floor tileset
const tileResponse = await fetch('https://api.pixellab.ai/v2/tilesets', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    lower_description: "dark metallic floor with subtle grid pattern, sci-fi laboratory",
    upper_description: "raised platform section with glowing edge trim",
    tile_size: { width: 32, height: 32 },
    view: "high top-down",
    outline: "thin",
    shading: "soft",
    transition_size: 0.5
  })
});
```

### Tilesets Needed

| Tileset | Lower | Upper | Style |
|---------|-------|-------|-------|
| Lab Floor | Dark metal grid | Raised platforms | Clean, high-tech |
| Corporate | Polished marble | Carpet sections | Luxury |
| Underground | Cracked concrete | Grating/pipes | Industrial decay |
| Server Room | Cable floor | Server platforms | Data center |
| Void | Cosmic void | Floating geometry | Abstract, purple |
| The Between | Fragmented reality | Memory paths | Dreamlike |

---

## Asset Generation Script

```javascript
// scripts/generate_assets.js
const PIXELLAB_TOKEN = process.env.PIXELLAB_API_TOKEN;
const BASE_URL = 'https://api.pixellab.ai/v2';

async function generateCharacter(name, description, size = 64) {
  console.log(`Generating character: ${name}`);
  
  const response = await fetch(`${BASE_URL}/create-character-with-4-directions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${PIXELLAB_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      description,
      image_size: { width: size, height: size },
      outline: 'medium',
      shading: 'soft',
      detail: 'high',
      view: 'side'
    })
  });
  
  const data = await response.json();
  console.log(`  Job ID: ${data.background_job_id}`);
  console.log(`  Character ID: ${data.character_id}`);
  
  return data;
}

async function checkJobStatus(jobId) {
  const response = await fetch(`${BASE_URL}/background-jobs/${jobId}`, {
    headers: { 'Authorization': `Bearer ${PIXELLAB_TOKEN}` }
  });
  return response.json();
}

async function downloadCharacterZip(characterId, outputPath) {
  const response = await fetch(`${BASE_URL}/characters/${characterId}/zip`, {
    headers: { 'Authorization': `Bearer ${PIXELLAB_TOKEN}` }
  });
  
  const buffer = await response.arrayBuffer();
  require('fs').writeFileSync(outputPath, Buffer.from(buffer));
  console.log(`Downloaded: ${outputPath}`);
}

// Character definitions
const CHARACTERS = [
  {
    name: 'vance',
    description: 'Corporate security chief in dark tactical armor, stern expression, badge, gray buzzcut hair, cyberpunk military style'
  },
  {
    name: 'aria',
    description: 'AI hologram assistant, blue translucent humanoid figure, geometric patterns, friendly feminine appearance, glowing edges'
  },
  {
    name: 'maya_echo',
    description: 'Ghostly woman with fading edges, warm amber colors, sad gentle expression, partially transparent, memory fragment'
  },
  {
    name: 'elder_phaseburner',
    description: 'Elderly figure in tattered robes, heavily glitched appearance, wise expression, reality distortion around them'
  },
  {
    name: 'ceo_hologram',
    description: 'Corporate executive hologram, expensive suit, slick hair, untrustworthy smile, blue holographic projection'
  }
];

// Run generation
async function main() {
  for (const char of CHARACTERS) {
    await generateCharacter(char.name, char.description);
    // Wait between requests to avoid rate limiting
    await new Promise(r => setTimeout(r, 2000));
  }
}

main().catch(console.error);
```

---

## MCP Integration

We already have the PixelLab MCP server configured. We can call it directly:

```javascript
// Using MCP server (already configured in .cursor/mcp.json)
// Tools available:
// - create_character (4 or 8 directions)
// - animate_character
// - get_character
// - list_characters
// - create_isometric_tile
// - create_map_object
// - create_topdown_tileset
```

---

## Batch Generation Plan

### Phase 1: Core Characters (5 credits each = 25 credits)
1. Dr. Vance
2. ARIA
3. Maya Echo
4. Elder Phaseburner
5. CEO Hologram

### Phase 2: Character Animations (2 credits each = 30 credits)
- Each character: idle + walking = 10 animations
- Priority characters only

### Phase 3: Map Objects (1-2 credits each = ~30 credits)
- Lab objects (5)
- Lobby objects (5)
- Underground objects (5)
- New room objects (15)

### Phase 4: Tilesets (5 credits each = 30 credits)
- 6 distinct tilesets

### Estimated Total: ~115 credits

---

## Directory Structure

```
assets/
├── characters/
│   ├── aziah/           # Existing
│   ├── guard/           # Existing
│   ├── phaseburner/     # Existing
│   ├── architect/       # Existing
│   ├── vance/           # NEW
│   ├── aria/            # NEW
│   ├── maya_echo/       # NEW
│   ├── elder/           # NEW
│   └── ceo/             # NEW
├── objects/
│   ├── lab/
│   ├── lobby/
│   ├── underground/
│   ├── server_room/
│   ├── executive/
│   └── between/
├── tilesets/
│   ├── lab/
│   ├── corporate/
│   ├── underground/
│   ├── server/
│   ├── void/
│   └── between/
└── ui/
    ├── icons/
    └── buttons/
```

---

## Style Consistency

To maintain visual consistency across all generated assets:

```json
{
  "style_defaults": {
    "outline": "medium",
    "shading": "soft", 
    "detail": "high",
    "view": "side",
    "color_palette": "cyberpunk (blue, purple, teal accents on dark backgrounds)"
  },
  "character_sizes": {
    "standard": { "width": 64, "height": 64 },
    "large": { "width": 96, "height": 96 },
    "boss": { "width": 128, "height": 128 }
  },
  "object_sizes": {
    "small": { "width": 32, "height": 32 },
    "medium": { "width": 64, "height": 64 },
    "large": { "width": 96, "height": 96 }
  }
}
```

---

## Next Steps

1. **Get API token** from https://pixellab.ai/account
2. **Test single character** generation
3. **Batch generate** priority characters
4. **Add animations** to characters
5. **Generate objects** room by room
6. **Create tilesets** for backgrounds
7. **Integrate** into game asset loader
