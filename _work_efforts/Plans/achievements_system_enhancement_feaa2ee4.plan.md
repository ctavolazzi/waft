---
name: Achievements System Enhancement
overview: Enhance the achievements system with a dedicated achievements page, improved floating panel, Fab Lab skill progression, and proper privacy controls with local data management.
todos:
  - id: privacy-disclaimer
    content: Create dismissible privacy disclaimer component with data export/clear controls
    status: completed
  - id: data-model
    content: Expand achievement data model with Fab Lab skills, rarity tiers, and XP values
    status: completed
  - id: panel-stability
    content: Fix floating panel stability issues (scroll lock, click-outside, mobile)
    status: completed
  - id: panel-ui
    content: Enhance panel UI with level display, stats, and improved achievement cards
    status: completed
  - id: achievements-page
    content: Create dedicated /wiki/achievements.md page with full gamification experience
    status: completed
  - id: new-achievements
    content: Add ~14 new Fab Lab skill-based achievements across 3D, laser, CNC paths
    status: completed
  - id: level-system
    content: Implement XP/level system with progress tracking and level-up celebrations
    status: completed
  - id: visual-polish
    content: Add rarity colors, holographic effects, and enhanced animations
    status: completed
---

# Achievements System Enhancement Plan

## Overview

Transform the existing achievements system into a comprehensive gamified learning experience that tracks both site interactions and Fab Lab skill progression, with a dedicated achievements page, improved floating panel, and proper privacy controls.

---

## Phase 1: Data Architecture & Privacy Controls

### 1.1 Enhanced Achievement Data Model

Expand the current `CFL.achievements` system in [`_layouts/default.html`](_layouts/default.html) (lines 418-545) to include:

- **Skill-based achievements** for Fab Lab learning paths (3D Printing, Laser Cutting, CNC, Electronics)
- **Rarity tiers**: Common, Uncommon, Rare, Epic, Legendary
- **XP/Points system** for overall progression level
- **Streak tracking** for consecutive visits/actions

### 1.2 Privacy Disclaimer Component

Create a dismissible floating disclaimer that:
- Appears on first visit (stored in localStorage)
- Explains what data is stored locally
- Provides "Clear All Data" and "Export Data" buttons
- Uses existing alert/callout components from [`_includes/components/alert.html`](_includes/components/alert.html)

```javascript
// Key storage items to document
localStorage.cflAchievements  // Unlocked achievements
localStorage.cflStats         // Click counts, pages visited
localStorage.cflPrivacyAccepted // Disclaimer dismissed
```

---

## Phase 2: Floating Panel Improvements

### 2.1 Stability Fixes

Address issues in current panel (lines 946-1143 of `default.html`):
- Add error boundaries for localStorage failures
- Fix scroll lock behavior on mobile
- Improve close-on-outside-click reliability

### 2.2 Enhanced Panel UI

- **Overall Level Display**: Show user's total XP and current level with progress bar to next level
- **Recent Achievements**: Highlight newly unlocked badges with animation
- **Quick Stats**: Use [`stat.html`](_includes/components/stat.html) component for click count, pages visited, achievements unlocked
- **Level Progress Bar**: Use [`progress.html`](_includes/components/progress.html) with animated variant

### 2.3 Improved Achievement Cards

- Add rarity border colors (gold for legendary, purple for epic, etc.)
- Show category icons more prominently
- Add hover tooltips with detailed unlock requirements
- Improve progress bar visibility for in-progress achievements

---

## Phase 3: Dedicated Achievements Page

### 3.1 Create `/wiki/achievements.md`

A full-page experience with:

**Header Section:**
- User level badge with XP progress
- Total achievements unlocked (X/Y)
- Fun title based on level ("Apprentice Maker", "Fab Lab Expert", etc.)

**Learning Paths Section (Tabs):**
Using [`tabs.html`](_includes/components/tabs.html) with these categories:
- All Achievements
- Site Explorer (page visits, interactions)
- 3D Printing Path
- Laser Cutting Path
- CNC Path
- Secret/Easter Eggs

**Achievement Grid:**
Card-based layout using enhanced achievement cards showing:
- Icon, name, description
- Progress bar for incomplete
- Unlock date for completed
- Rarity badge
- XP value

**Stats Dashboard:**
Using [`stat.html`](_includes/components/stat.html) components:
- Total XP earned
- Current streak
- Rarest achievement unlocked
- Time played (pages viewed)

**Privacy Controls Footer:**
- "Export My Data" button (JSON download)
- "Clear All Progress" button with confirmation
- Privacy explanation text

### 3.2 Add New Fab Lab Achievements

Expand from 16 to ~30 achievements:

**3D Printing Path (5 new):**
- `3d-curious` - Visit the 3D Printing wiki page
- `filament-fan` - Learn about 3 different filament types
- `slicer-starter` - Read about slicing software
- `print-pro` - Complete all 3D printing wiki pages
- `layer-legend` - Master level (complete all + quiz)

**Laser Cutting Path (5 new):**
- `beam-beginner` - Visit Laser Cutting wiki
- `material-master` - Learn about different materials
- `focus-finder` - Read about focus calibration
- `cut-champion` - Complete all laser wiki pages
- `precision-pro` - Master level

**CNC Path (4 new):**
- `mill-curious` - Visit CNC wiki
- `feeds-speeds` - Read about feeds and speeds
- `toolpath-trainee` - Learn about toolpaths
- `cnc-commander` - Complete all CNC pages

---

## Phase 4: Gamification Enhancements

### 4.1 Level System

```javascript
// XP thresholds for levels
Level 1: 0 XP - "Curious Visitor"
Level 2: 50 XP - "Apprentice Maker"
Level 3: 150 XP - "Fab Lab Regular"
Level 4: 300 XP - "Workshop Warrior"
Level 5: 500 XP - "Master Maker"
Level 6: 750 XP - "Fab Lab Legend"
```

### 4.2 XP Values by Rarity

- Common: 5 XP
- Uncommon: 15 XP
- Rare: 30 XP
- Epic: 50 XP
- Legendary: 100 XP

### 4.3 Visual Polish

- Level-up celebration animation (confetti particles)
- Achievement unlock toast enhancements
- Sound effects for different rarities (already have `CFL.sounds`)
- Holographic effect for legendary achievements using `.cfl-holo` utilities

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `_wiki/achievements.md` | Create | Dedicated achievements page |
| `_layouts/default.html` | Modify | Enhanced achievement system JS |
| `assets/css/main.css` | Modify | New achievement styles, rarity colors |
| `_includes/privacy-disclaimer.html` | Create | Floating privacy disclaimer component |

---

## Implementation Order

1. Privacy disclaimer component (establishes consent pattern)
2. Enhanced data model with new achievements
3. Floating panel improvements
4. Dedicated achievements page
5. Level system and XP calculations
6. Visual polish and animations