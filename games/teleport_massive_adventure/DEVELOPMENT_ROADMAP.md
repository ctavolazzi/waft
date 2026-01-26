# Teleport Massive: The Adventure
## Development Roadmap

---

## Current State (v0.2)

### ✅ Completed
- Clean, composable architecture (EventBus, GameState, DialogueSystem)
- Data-driven room system (JSON definitions)
- Walk-to-then-interact player controller
- 4 rooms: Lab → Lobby → Underground → Void
- Basic inventory system
- The Architect god system with event observation
- Multi-phase boss encounter
- Two endings (Merge / Stay Free)

### 📊 Metrics
- ~3,800 lines of code
- 6 core systems
- 4 scene classes
- 3 data files

---

## Phase 1: Core Polish (Foundation)
**Goal:** Make the current content feel complete and professional

### 1.1 Save/Load System
```
Priority: HIGH | Effort: MEDIUM
```
- [ ] Auto-save on room transitions
- [ ] Manual save slots (3)
- [ ] Save preview (room name, playtime, items)
- [ ] Load game menu
- [ ] "Continue" option on title screen

### 1.2 Title Screen & Menus
```
Priority: HIGH | Effort: LOW
```
- [ ] Title screen with TM logo animation
- [ ] "New Game" / "Continue" / "Options"
- [ ] Options: text speed, volume, fullscreen
- [ ] Credits screen
- [ ] "How to Play" overlay

### 1.3 Sound Design
```
Priority: HIGH | Effort: MEDIUM
```
- [ ] Ambient loops per room (lab hum, corporate, underground drip, void cosmic)
- [ ] Footstep sounds
- [ ] UI sounds (click, pickup, dialogue advance)
- [ ] Music tracks (exploration, tension, boss phases)
- [ ] Volume controls

### 1.4 Visual Polish
```
Priority: MEDIUM | Effort: MEDIUM
```
- [ ] Smooth room transitions (fade, slide, glitch)
- [ ] Item pickup animation (float up, sparkle)
- [ ] Character walk animation (4-frame cycle per direction)
- [ ] Hotspot highlight on hover
- [ ] Dialogue typewriter effect

---

## Phase 2: Puzzle Depth
**Goal:** Add meaningful gameplay beyond walk-and-talk

### 2.1 Item Combination System
```
Priority: HIGH | Effort: MEDIUM
```
```javascript
// Example: data/items.json
"combinations": [
  {
    "items": ["keycard", "artifact"],
    "result": "charged_keycard",
    "dialogue": "The artifact pulses. The keycard glows."
  }
]
```
- [ ] Drag item onto item in inventory
- [ ] Combination recipes in JSON
- [ ] Visual feedback for valid/invalid combos
- [ ] "That doesn't work" responses

### 2.2 Environmental Puzzles
```
Priority: HIGH | Effort: HIGH
```
- [ ] **Lab Terminal Puzzle**: Hack sequence (simple pattern match)
- [ ] **Lobby Security**: Distract guard to access restricted area
- [ ] **Underground Pipes**: Redirect steam to reveal hidden path
- [ ] **Void Riddles**: The Architect poses philosophical questions

### 2.3 Conditional Dialogue
```
Priority: MEDIUM | Effort: MEDIUM
```
```json
{
  "guard_default": {
    "conditions": [
      { "if": { "flag": "hasKeycard" }, "dialogueId": "guard_suspicious" },
      { "if": { "flag": "talkedToPhaseburner" }, "dialogueId": "guard_knows" },
      { "default": "guard_normal" }
    ]
  }
}
```
- [ ] NPCs react to player progress
- [ ] Multiple dialogue branches per NPC
- [ ] Relationship tracking (friendly/hostile/neutral)

---

## Phase 3: World Expansion
**Goal:** Triple the game content

### 3.1 New Areas
```
Priority: HIGH | Effort: HIGH
```

| Area | Description | Key Items | NPCs |
|------|-------------|-----------|------|
| **Server Room** | TM's data center, cold and humming | Access codes, Maya's file | Maintenance Bot |
| **Executive Suite** | CEO's office, luxury meets sinister | Resignation letter, Key to vault | CEO Hologram |
| **The Between** | Liminal space, reality breaks down | Fragments of Maya | Echo of Maya |
| **Memory Archive** | Aziah's memories made physical | Photo album, Wedding ring | Younger Aziah |
| **Phaseburner Camp** | Underground community of victims | Community trust, Map | Multiple Phaseburners |

### 3.2 NPCs & Characters
```
Priority: HIGH | Effort: MEDIUM
```

| Character | Role | Location | Key Info |
|-----------|------|----------|----------|
| **Dr. Vance** | Security Chief, antagonist | Lobby/Executive | Knows about cover-up |
| **Maya (Echo)** | Wife, exists in fragments | The Between | Reveals true ending |
| **ARIA** | TM AI, helpful but conflicted | Server Room | Can be convinced to help |
| **Elder Phaseburner** | Leader of underground | Camp | Teaches about The Between |
| **CEO Hologram** | Pre-recorded, reveals TM's sins | Executive | Password to vault |

### 3.3 Side Quests
```
Priority: MEDIUM | Effort: MEDIUM
```
- [ ] **"The List"**: Find all 10 Phaseburn victim names
- [ ] **"Corporate Espionage"**: Steal TM secrets for Phaseburners
- [ ] **"Maya's Trail"**: Collect 5 memory fragments
- [ ] **"The Whistleblower"**: Find evidence to expose TM

---

## Phase 4: The Architect Integration
**Goal:** Make the god system a core gameplay element

### 4.1 Dynamic Commentary
```
Priority: HIGH | Effort: MEDIUM
```
- [ ] Architect comments appear based on player behavior patterns
- [ ] Different commentary for completionists vs speedrunners
- [ ] Meta-references to save/load abuse
- [ ] Fourth-wall breaks that acknowledge the player

### 4.2 Observation Mechanics
```
Priority: MEDIUM | Effort: HIGH
```
```javascript
// The Architect tracks and responds to:
{
  "explorationScore": 0.0-1.0,    // How much they explore
  "dialogueEngagement": 0.0-1.0,  // Do they read everything?
  "puzzlePersistence": 0.0-1.0,   // Do they give up quickly?
  "moralChoices": [],             // Track ethical decisions
  "deathCount": 0,                // How many times defeated
  "loadCount": 0                  // Save scumming detection
}
```
- [ ] Player profile influences Architect dialogue
- [ ] Boss difficulty scales with observed skill
- [ ] Secret ending for players who "break the rules"

### 4.3 Intervention System
```
Priority: LOW | Effort: MEDIUM
```
- [ ] Architect can spawn hints if player is stuck
- [ ] Architect can modify the world subtly
- [ ] "Did you notice that door wasn't there before?"
- [ ] Reality glitches that reward exploration

---

## Phase 5: Multiple Endings
**Goal:** Meaningful choices with lasting consequences

### 5.1 Ending Branches
```
Priority: HIGH | Effort: HIGH
```

| Ending | Requirement | Tone |
|--------|-------------|------|
| **Merge** | Accept Architect's offer | Bittersweet - eternal but inhuman |
| **Liberation** | Reject Architect | Hopeful - mortal but free |
| **Reunion** | Find all Maya fragments | Happy - reunited in The Between |
| **Exposure** | Complete whistleblower quest | Pyrrhic - TM falls, you're hunted |
| **Transcendence** | Break the fourth wall | Meta - become aware of being in a game |
| **Loop** | Die to Architect 10 times | Dark - trapped in cycle |

### 5.2 New Game+
```
Priority: LOW | Effort: MEDIUM
```
- [ ] Carry over some items/knowledge
- [ ] Architect remembers previous runs
- [ ] New dialogue acknowledging loops
- [ ] Hidden areas only accessible in NG+

---

## Phase 6: Technical Excellence
**Goal:** Professional-grade quality

### 6.1 Performance
```
Priority: MEDIUM | Effort: LOW
```
- [ ] Lazy load room assets
- [ ] Object pooling for particles
- [ ] Compressed audio sprites
- [ ] Preload adjacent rooms

### 6.2 Accessibility
```
Priority: MEDIUM | Effort: MEDIUM
```
- [ ] Keyboard-only navigation
- [ ] Screen reader support for dialogue
- [ ] High contrast mode
- [ ] Adjustable text size
- [ ] Colorblind-friendly UI

### 6.3 Mobile/Touch
```
Priority: LOW | Effort: HIGH
```
- [ ] Touch controls (tap to walk, tap to interact)
- [ ] Responsive UI scaling
- [ ] Virtual joystick option
- [ ] Portrait mode support

---

## Phase 7: Release Preparation
**Goal:** Ship it

### 7.1 Content Lock
- [ ] All rooms complete
- [ ] All dialogue written
- [ ] All puzzles tested
- [ ] All endings achievable

### 7.2 QA
- [ ] Playtest with 5+ people
- [ ] Fix all soft locks
- [ ] Balance puzzle difficulty
- [ ] Verify all endings work

### 7.3 Polish Pass
- [ ] Consistent art style
- [ ] Typo check all dialogue
- [ ] Smooth all transitions
- [ ] Final audio mix

### 7.4 Distribution
- [ ] itch.io page
- [ ] Trailer video
- [ ] Screenshots
- [ ] Press kit

---

## Suggested Development Order

```
IMMEDIATE (Next Session)
├── 1.2 Title Screen
├── 1.1 Save/Load
└── 2.1 Item Combinations

SHORT TERM (Next Week)
├── 1.3 Sound Design
├── 2.2 Environmental Puzzles (Lab + Lobby)
└── 3.2 Add Dr. Vance NPC

MEDIUM TERM (Next Month)
├── 3.1 Server Room + Executive Suite
├── 4.1 Dynamic Commentary
├── 2.3 Conditional Dialogue
└── 5.1 Implement 3 endings

LONG TERM (Release)
├── 3.1 The Between + Memory Archive
├── 5.2 New Game+
├── 6.2 Accessibility
└── 7.* Release prep
```

---

## Architecture Notes

### Adding a New Room
```bash
# 1. Add room data
edit data/rooms.json

# 2. Add room dialogue
edit data/dialogue.json

# 3. Create scene class
create src/scenes/NewRoomScene.js

# 4. Register in index_v2.html
# Add to scene array in Phaser config
```

### Adding a New Item
```json
// data/items.json
"new_item": {
  "id": "new_item",
  "name": "Display Name",
  "description": "What the player sees",
  "icon": "🔮",
  "usableOn": ["hotspot_id", "npc_id"]
}
```

### Adding a New NPC
```json
// data/rooms.json → room.npcs
{
  "id": "npc_id",
  "name": "NPC Name",
  "position": { "x": 300, "y": 350 },
  "sprite": "npc_south",
  "dialogue": "npc_default",
  "examineText": "Description when looked at"
}
```

---

## Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Core Polish | 1-2 weeks | 2 weeks |
| Phase 2: Puzzle Depth | 2-3 weeks | 5 weeks |
| Phase 3: World Expansion | 3-4 weeks | 9 weeks |
| Phase 4: Architect Integration | 1-2 weeks | 11 weeks |
| Phase 5: Multiple Endings | 2-3 weeks | 14 weeks |
| Phase 6: Technical | 1 week | 15 weeks |
| Phase 7: Release | 1-2 weeks | 17 weeks |

**Total: ~4 months to full release**

---

## Open Questions

1. **Art Style**: Commission more PixelLab assets or hand-draw?
2. **Scope**: Full game (~2 hours) or demo (~30 min) first?
3. **Monetization**: Free, pay-what-you-want, or fixed price?
4. **Platform**: Web-only or also desktop (Electron)?
5. **Collaboration**: Solo or bring in writer/artist/musician?

---

*"Every game is a universe. Every developer is a god. The question is: what kind of god will you be?"*
— The Architect
