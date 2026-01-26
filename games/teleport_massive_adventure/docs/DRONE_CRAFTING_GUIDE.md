# Drone Crafting & Upgrade System Guide

**Date:** 2026-01-25  
**Status:** ✅ Fully Functional

---

## Overview

A comprehensive crafting system that allows Aziah to upgrade their combat drone at workbenches using parts found throughout the game. The system includes level upgrades and ability enhancements.

---

## Workbenches

### Locations

1. **Lab Workbench** (`workbench_lab`)
   - Location: Lab Scene (x: 500, y: 320)
   - Description: "A workbench for upgrading and modifying drones. Tools and screens line the surface."

2. **Underground Workbench** (`workbench_underground`)
   - Location: Underground Scene (x: 500, y: 320)
   - Description: "An old workbench, still functional despite the damage. Perfect for drone modifications."

### Usage

1. **Activate your drone** (or it will auto-activate when using workbench)
2. **Approach workbench** and press `E` or click to interact
3. **Crafting UI opens** showing:
   - Current drone level and stats
   - Available parts in inventory
   - Available upgrade recipes
4. **Click "CRAFT"** on any available recipe
5. **Parts are consumed** and drone is upgraded

---

## Drone Parts

### Energy Core Module
- **Location:** Lab Scene (x: 350, y: 280)
- **Icon:** ⚡
- **Description:** "A glowing blue energy core. Essential for basic drone upgrades."
- **Used in:** Level 2, 3, 4 upgrades

### Weapon Module
- **Location:** Underground Scene (x: 400, y: 380)
- **Icon:** 🔫
- **Description:** "A red laser emitter module. Increases drone damage and burst shot effectiveness."
- **Used in:** Level 3, 4 upgrades, Burst Shot upgrade

### Shield Generator
- **Location:** Underground Scene (x: 300, y: 360)
- **Icon:** 🛡️
- **Description:** "A hexagonal shield generator module. Enhances shield mode duration and effectiveness."
- **Used in:** Level 4 upgrade, Shield Mode upgrade

---

## Upgrade Recipes

### Level Upgrades

#### Level 2 Upgrade
- **Required Parts:** 1x Energy Core
- **Bonuses:**
  - +3 damage
  - -100ms shot cooldown (faster firing)
- **Description:** "Upgrade drone to level 2. Increases damage and fire rate."

#### Level 3 Upgrade
- **Required Parts:** 1x Energy Core, 1x Weapon Module
- **Bonuses:**
  - +5 damage (total +8 from base)
  - -200ms shot cooldown (total -300ms from base)
  - +50px target range
- **Description:** "Upgrade drone to level 3. Significant damage boost and extended range."

#### Level 4 Upgrade
- **Required Parts:** 1x Energy Core, 1x Weapon Module, 1x Shield Generator
- **Bonuses:**
  - +8 damage (total +16 from base)
  - -300ms shot cooldown (total -600ms from base)
  - +100px target range (total +150px from base)
  - +1000ms shield duration
- **Description:** "Upgrade drone to level 4. Maximum power with enhanced shield capabilities."

### Ability Upgrades

#### Enhanced Burst Shot
- **Required Parts:** 1x Weapon Module
- **Bonuses:**
  - +50% damage multiplier
  - +2 projectiles (7 total instead of 5)
- **Description:** "Increases burst shot damage by 50% and adds 2 more projectiles."
- **Note:** Can be applied at any level

#### Enhanced Shield Mode
- **Required Parts:** 1x Shield Generator
- **Bonuses:**
  - +2000ms duration (5 seconds total)
  - +50% damage reduction
- **Description:** "Increases shield duration by 2 seconds and adds 50% damage reduction."
- **Note:** Can be applied at any level

---

## Stat Progression

### Base Stats (Level 1)
- **Damage:** 12 per shot
- **Shot Cooldown:** 1000ms (1 second)
- **Target Range:** 300px
- **Burst Shot:** 5 projectiles, 80% damage each
- **Shield Mode:** 3 seconds duration, no damage reduction

### Level 2 Stats
- **Damage:** 15 per shot (+3)
- **Shot Cooldown:** 900ms (-100ms)
- **Target Range:** 300px
- **Burst Shot:** 5 projectiles, 80% damage each
- **Shield Mode:** 3 seconds duration, no damage reduction

### Level 3 Stats
- **Damage:** 20 per shot (+8 total)
- **Shot Cooldown:** 700ms (-300ms total)
- **Target Range:** 350px (+50px)
- **Burst Shot:** 5 projectiles, 80% damage each
- **Shield Mode:** 3 seconds duration, no damage reduction

### Level 4 Stats
- **Damage:** 28 per shot (+16 total)
- **Shot Cooldown:** 400ms (-600ms total)
- **Target Range:** 450px (+150px total)
- **Burst Shot:** 5 projectiles, 80% damage each
- **Shield Mode:** 4 seconds duration (+1000ms), no damage reduction

### With Ability Upgrades

**Enhanced Burst Shot:**
- **Projectiles:** 7 (instead of 5)
- **Damage per projectile:** 120% base (instead of 80%)

**Enhanced Shield Mode:**
- **Duration:** 5 seconds (instead of 3)
- **Damage Reduction:** 50% (blocks half of incoming damage)

---

## Crafting UI

### Features

- **Drone Info Panel:** Shows current level, damage, cooldown, range
- **Available Parts:** Lists all drone parts in inventory
- **Available Upgrades:** Shows recipes you can craft
- **Recipe Details:** Name, description, required parts
- **CRAFT Button:** Crafts the upgrade (consumes parts)
- **Close Button:** Closes UI (or press ESC)

### UI Layout

```
┌─────────────────────────────────────┐
│   DRONE UPGRADE WORKBENCH           │
├─────────────────────────────────────┤
│ Current Drone Level: 2              │
│ Damage: 15 | Cooldown: 900ms        │
├─────────────────────────────────────┤
│ Available Parts:                    │
│ ⚡ Energy Core 🔫 Weapon Module      │
├─────────────────────────────────────┤
│ Available Upgrades:                 │
│ ┌─────────────────────────────────┐ │
│ │ Drone Level 3                   │ │
│ │ Upgrade to level 3...           │ │
│ │ Required: energy_core,          │ │
│ │          weapon_module          │ │
│ │ [CRAFT]                          │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## Gameplay Flow

### Early Game
1. **Find Energy Core** in Lab Scene
2. **Acquire Combat Drone** (if not already have it)
3. **Activate drone** (auto-activates when acquired)
4. **Use Lab Workbench** to upgrade to Level 2

### Mid Game
1. **Find Weapon Module** in Underground Scene
2. **Use Underground Workbench** to upgrade to Level 3
3. **Optional:** Craft Enhanced Burst Shot upgrade

### Late Game
1. **Find Shield Generator** in Underground Scene
2. **Use workbench** to upgrade to Level 4
3. **Optional:** Craft Enhanced Shield Mode upgrade

---

## Technical Details

### CraftingSystem Class

**Location:** `src/core/CraftingSystem.js`

**Key Methods:**
- `canCraft(recipeId, inventory)` - Check if recipe can be crafted
- `craft(recipeId, inventory, drone)` - Execute crafting
- `getAvailableRecipes(inventory, drone)` - Get craftable recipes
- `getDroneInfo(drone)` - Get current drone stats

### Integration Points

- **InteractionSystem:** Handles workbench interactions
- **CombatDrone:** Receives upgrades and applies stat bonuses
- **GameState:** Manages inventory and part consumption
- **EventBus:** Emits `drone:upgraded` events

### Upgrade Application

Upgrades are applied immediately when crafted:
- **Level upgrades:** Set drone level and add stat bonuses
- **Ability upgrades:** Modify ability properties (multipliers, counts, durations)

---

## PixelLab Assets

### Generated Assets

1. **Energy Core** (`energy_core_obj.png`)
   - ID: `86fef39f-e357-4d65-b748-428f41581601`
   - Blue glowing geometric design
   - 32×32px

2. **Weapon Module** (`weapon_module_obj.png`)
   - ID: `52a5c5c5-0777-4e12-8e09-de3c0a50679d`
   - Dark metallic object with red laser beam
   - 32×32px

3. **Shield Generator** (`shield_generator_obj.png`)
   - ID: `18988585-a21b-4c04-93ef-d41c6dfa89f6`
   - Hexagonal blue energy field
   - 32×32px

4. **Workbench** (`workbench_obj.png`)
   - Placeholder created (64×64px)
   - Simple table with tools/screens
   - *Note: PixelLab generation hit rate limit, placeholder used*

### Asset Locations

- **Parts:** `assets/objects/energy_core_obj.png`, `weapon_module_obj.png`, `shield_generator_obj.png`
- **Workbench:** `assets/objects/workbench_obj.png`

---

## Future Enhancements

### Possible Additions
- [ ] More upgrade tiers (Level 5, 6, etc.)
- [ ] Specialized upgrade paths (offense vs defense)
- [ ] Part combinations for unique upgrades
- [ ] Visual effects for upgraded drone
- [ ] Upgrade preview (shows stat changes before crafting)
- [ ] Part crafting (combine basic parts into advanced ones)

---

## Troubleshooting

### "Drone not available"
- **Cause:** Drone not acquired or initialized
- **Fix:** Make sure you have the combat drone item in inventory

### "Missing required parts"
- **Cause:** Don't have all parts needed for recipe
- **Fix:** Collect the required parts first

### "Already at this level"
- **Cause:** Trying to craft an upgrade you already have
- **Fix:** Check available recipes - only shows upgrades you can make

### Parts not appearing in inventory
- **Cause:** Parts not picked up or inventory not updated
- **Fix:** Make sure you've collected the parts from their locations

---

## Code Reference

### Key Files

- `src/core/CraftingSystem.js` - Crafting logic and recipes
- `src/core/CombatDrone.js` - Drone stats and upgrade application
- `src/core/InteractionSystem.js` - Workbench interaction and UI
- `data/rooms.json` - Workbench and part locations
- `data/items.json` - Part item definitions

### Key Methods

```javascript
// Check if can craft
craftingSystem.canCraft('drone_level_2', inventory)

// Craft upgrade
craftingSystem.craft('drone_level_2', inventory, drone)

// Get available recipes
craftingSystem.getAvailableRecipes(inventory, drone)

// Get drone info
craftingSystem.getDroneInfo(drone)
```

---

**Last Updated:** 2026-01-25  
**Version:** 1.0
