# Work Effort: Clone D&D 5e Toolkit (Dungeoneer + SRD Markdown)

## Status: ✅ Completed
**Started:** 2026-01-23 19:52 PST
**Completed:** 2026-01-23 19:55 PST

## Objective

Clone and explore two D&D 5e reference repositories for potential WAFT integration:
1. **Dungeoneer VTT** - Electron virtual tabletop with P2P multiplayer
2. **dnd5e-markdown** - Full SRD in Obsidian-ready format

## Tasks

- [x] Clone Dungeoneer VTT to `_external/dungeoneer`
- [x] Clone dnd5e-markdown to `_external/dnd5e-srd`
- [x] Install Dungeoneer dependencies (`yarn install`)
- [x] Explore interesting code patterns
- [x] Document findings

## Cloned Repositories

| Repo | Location | Size | Status |
|------|----------|------|--------|
| Dungeoneer VTT | `_external/dungeoneer` | 772MB | ✅ Cloned + deps installed |
| D&D 5e SRD | `_external/dnd5e-srd` | 178MB | ✅ Cloned |

## Key Findings

### 1. P2P Chunked Transfer Pattern (Dungeoneer)

**File:** `app/server/server.js`

```javascript
const CHUNK_SIZE = 1000000; // 1MB chunks
function sendBatched(connection, key, msgString, metadata) {
    var totalLength = msgString.length;
    var chunks = Math.ceil(totalLength / CHUNK_SIZE);
    for (var i = 0; i < chunks; i++) {
        var start = i * CHUNK_SIZE;
        connection.send({
            event: key,
            data: {
                base64: msgString.substring(start, start + CHUNK_SIZE),
                chunk: i + 1,
                chunks: chunks,
                metadata: metadata,
            },
        });
    }
}
```

**Use case for WAFT:** WebRTC P2P file sharing, multiplayer features

### 2. Dynamic Lighting Geometry (Dungeoneer)

**File:** `app/mappingTool/geometry.js`

Basic 2D math utilities:
- `insideCone()` - Point-in-triangle test for cone vision
- `insideRect()` - Rectangle bounds check
- `distance()`, `angleBetween()`, `rotate()` - Vector math

**Use case for WAFT:** Map tool visualizations

### 3. Monster JSON Schema (Dungeoneer)

**File:** `data/monsters.json`

```json
{
  "name": "Aboleth",
  "size": "Large",
  "type": "Aberration",
  "armor_class": 17,
  "hit_points": 135,
  "hit_dice": "18d10",
  "speed": "10 ft., swim 40 ft.",
  "strength": 21, "dexterity": 9, "constitution": 15,
  "intelligence": 18, "wisdom": 15, "charisma": 18,
  "challenge_rating": "10",
  "special_abilities": [...],
  "actions": [...],
  "legendary_actions": [...]
}
```

**Use case for WAFT:** PDF generation, encounter builders

### 4. SRD Markdown Format (dnd5e-srd)

**File:** `compendium/bestiary/monstrosity/owlbear.md`

```markdown
---
obsidianUIMode: preview
cssclasses: json5e-monster
tags:
- monster/environment/forest
- monster/size/large
- monster/type/monstrosity
---
# Owlbear
*Large monstrosity, Unaligned*
- **Armor Class** 13 (natural armor)
- **Hit Points** 59 (`7d10 + 21`)
...
```

**Use case for WAFT:** Rules reference, Obsidian integration, PDF source data

### 5. Bestiary Organization (dnd5e-srd)

337 monster entries organized by type:
- `compendium/bestiary/aberration/`
- `compendium/bestiary/beast/`
- `compendium/bestiary/dragon/`
- `compendium/bestiary/humanoid/`
- `compendium/bestiary/monstrosity/`
- `compendium/bestiary/undead/`
- etc.

## Potential Extractions for WAFT

| Feature | Source | Priority |
|---------|--------|----------|
| Monster JSON data | dungeoneer/data/monsters.json | High |
| SRD markdown content | dnd5e-srd/compendium | High |
| CR Calculator | dungeoneer/app/js/CRCalculator.js | High |
| Encounter Module | dungeoneer/app/js/encounterModule.js | High |
| P2P chunked transfer | dungeoneer/app/server | Medium |
| Tavern Generator | dungeoneer/app/js/tavernGenerator.js | Medium |
| Random Table System | dungeoneer/app/js/randomizer.js | Medium |
| Token condition icons | dungeoneer/app/mappingTool/tokens | Low |

## Deep Dive: Extractable Code Patterns

### CR Calculator (`CRCalculator.js`)

Complete Challenge Rating calculation from DMG:

```javascript
// CR table with HP ranges, damage ranges, AC, save DC, attack bonus
var table = [
  { cr: "0", minHP: 1, maxHP: 6, profBonus: 2, ac: 13, minDmg: 0, maxDmg: 1, saveDc: 13, attack_bonus: 3 },
  { cr: "1/8", minHP: 7, maxHP: 35, profBonus: 2, ac: 13, minDmg: 2, maxDmg: 3, saveDc: 13, attack_bonus: 3 },
  // ... up to CR 30
  { cr: "30", minHP: 806, maxHP: 850, profBonus: 9, ac: 19, minDmg: 303, maxDmg: 320, saveDc: 23, attack_bonus: 14 },
]

// Calculate CR from stats
function calculateCR(ac, hp, attackBonus, predictedDmg, saveDc) {
  // Find defensive CR from HP, adjust by AC difference
  // Find offensive CR from damage, adjust by attack bonus
  // Average them for final CR
}
```

### Encounter Module (`encounterModule.js`)

Full XP-based encounter difficulty system:

```javascript
// XP by CR index (0=CR0, 1=CR1/8, 2=CR1/4, 3=CR1/2, 4+=CR1+)
xpByCR: [10, 25, 50, 100, 200, 450, 700, 1100, 1800, 2300, ...]

// Party size multipliers
function getMultiplierForCreatureNumber(count, partySize) {
  var values = [1, 1.5, 2, 2.5, 3, 4];  // Based on monster count
  // Adjust up for small parties (≤2), down for large parties (≥5)
}

// Difficulty thresholds per level
table: [
  [50, 75, 100],      // Level 1: Easy, Medium, Hard
  [100, 150, 200],    // Level 2
  // ... up to level 20
]

// Returns "Trivial", "Easy", "Medium", "Hard", "Deadly", "2x Deadly"
function getEncounterDifficultyString(xpValue, allLevels)
```

### Tavern Generator (`tavernGenerator.js`)

Template-based generation with placeholder system:

```javascript
// Placeholders: _name, _adjective, _tavern, _profession, _unique
// _material, _vegetables, _2vegetables, _meat, _fish, etc.

// Example template: "The _adjective _common_animal _tavern"
// Becomes: "The Prancing Pony Inn"

// Wealth tiers affect: interior, flooring, menu prices, drinks
// Menu generated with food items + drinks at wealth-appropriate prices
// Rumors generated with NPC rumormongers
```

### Random Table System (`randomizer.js`)

Probability-weighted random tables with chaining:

```javascript
{
  "tables": {
    "Adventuring_gear": [
      { "content": "Abacus", "probability": 0.01, "followup_table": "" },
      { "content": "Acid (vial)", "probability": 0.01, "followup_table": "" },
      // Tables can chain via followup_table for nested rolls
    ]
  }
}
```

## Asset Inventory

| Asset | Location | Count | Format |
|-------|----------|-------|--------|
| Monsters | dungeoneer/data/monsters.json | ~300 | JSON |
| Spells | dungeoneer/data/spells.json | ~300 | JSON |
| Items | dungeoneer/data/items.json | ~200 | JSON |
| Conditions | dungeoneer/data/conditions.json | 15 | JSON |
| Condition Icons | dungeoneer/app/mappingTool/tokens/conditions/ | 18 | PNG |
| SRD Monsters | dnd5e-srd/compendium/bestiary/ | 337 | Markdown |
| SRD Spells | dnd5e-srd/compendium/spells/ | ~300 | Markdown |
| SRD Classes | dnd5e-srd/compendium/classes/ | 11 | Markdown |
| SRD Races | dnd5e-srd/compendium/races/ | 10 | Markdown |

## Next Steps

1. Extract CR Calculator for homebrew monster validation
2. Port Encounter Module XP tables to Python for PDF generators
3. Use SRD markdown as source for Obsidian-style PDF generation
4. Consider adapting tavern generator for session prep tools

## Notes

- Dungeoneer uses PeerJS for WebRTC P2P (hosted signaling server)
- SRD content is public domain (Unlicense)
- Both repos are read-only references (not modifying originals)
- Generator data files are 100KB+ JSON with extensive word lists
