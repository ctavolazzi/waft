# Teleport Massive: The Adventure
## Complete Game Plan - Start to Dealer

---

## 🎯 Game Overview

**Genre:** Cyberpunk Point-and-Click Adventure with Combat
**Playtime:** 20-30 minutes
**Endings:** 3 (Join, Escape, Destroy)

**Story:** Aziah, a lab technician at Teleport Massive Corp, discovers their colleague Maya has vanished into "The Between" - a glitch dimension between teleport jumps. Following her trail, Aziah uncovers the truth: The Dealer, a cosmic entity trapped in the corporation's systems, has been collecting souls. Maya beat him once. Can you?

---

## 🗺️ World Map

```
                    ┌─────────────────┐
                    │   THE VOID      │
                    │  (Final Boss)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌──────▼──────┐  ┌───▼────────┐
     │  ARCHIVES   │  │  MAINFRAME  │  │  TRANSIT   │
     │  (Puzzle)   │  │   (Boss)    │  │   HUB      │
     └──────┬──────┘  └──────┬──────┘  └─────┬──────┘
            │                │               │
            └────────────────┼───────────────┘
                             │
                    ┌────────▼────────┐
                    │    CORRIDOR     │
                    │   (Combat)      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌──────▼──────┐  ┌───▼────────┐
     │   OFFICE    │  │  SECURITY   │  │  STORAGE   │
     │  (Story)    │  │  (Combat)   │  │  (Items)   │
     └──────┬──────┘  └──────┬──────┘  └─────┬──────┘
            │                │               │
            └────────────────┼───────────────┘
                             │
                    ┌────────▼────────┐
                    │      LAB        │
                    │   (Tutorial)    │
                    └─────────────────┘
```

---

## 📍 Scene Breakdown

### ACT 1: Discovery (5-7 min)

#### Scene 1: THE LAB (Tutorial)
**Current Implementation:** ✅ Exists

**Purpose:** Tutorial, establish setting, find first clue

**Elements:**
- Aziah's workstation (Terminal) - Learn about Maya's disappearance
- SWAB Artifact - Mysterious item Maya left behind
- Security Keycard - Opens Security room
- Exit to Corridor

**Gameplay:**
1. Interact with Terminal → Learn Maya is missing, last seen in Transit Hub
2. Pick up Artifact → The Dealer's first comment
3. Pick up Keycard → Unlocks Security room
4. Exit to Corridor

**The Dealer Commentary:**
- On entering: "Another soul enters my little game. I've been keeping score, you know. For eons."
- On reading terminal: "Maya... now there's a name I haven't heard in 47 seconds. Or was it 47 years? Time is funny here."
- On picking up artifact: "Ooh, shiny! But is it useful, or just another distraction I planted?"

---

#### Scene 2: CORRIDOR
**Status:** 🔨 To Build

**Purpose:** First combat encounter, hub navigation

**Elements:**
- 2-3 Glitch Guards (enemies)
- Exits to: Lab, Office, Security, Storage
- Locked door to upper levels (needs Access Card)

**Enemies:**
| Enemy | HP | Attack | Defense | XP |
|-------|-----|--------|---------|-----|
| Glitch Guard | 40 | 8 | 3 | 25 |

**Gameplay:**
1. Enter from Lab
2. 2 Glitch Guards block path
3. Combat tutorial: Attack with spacebar/click
4. Defeat guards → 50 XP → Possibly level up
5. Choose which room to explore

**The Dealer Commentary:**
- On first combat: "Ah, violence! The universal language. Let's see your vocabulary."
- On taking damage: "Careful now. HP isn't just a number - it's your remaining moves in our game."
- On victory: "Two down. *flips card* But the deck has 52 cards, and you've only seen 2."

---

#### Scene 3: SECURITY ROOM
**Status:** 🔨 To Build

**Purpose:** Combat gauntlet, get Access Card

**Elements:**
- Security Chief Vex (mini-boss)
- 2 Security Drones (enemies)
- Access Card (unlocks upper levels)
- Security Logs terminal (lore about The Between incidents)

**Enemies:**
| Enemy | HP | Attack | Defense | XP |
|-------|-----|--------|---------|-----|
| Security Drone | 25 | 6 | 5 | 15 |
| Chief Vex | 80 | 12 | 6 | 50 |

**Boss Fight: Chief Vex**
- Phase 1 (100-50% HP): Normal attacks
- Phase 2 (50-0% HP): Summons 1 drone, attacks faster

**Gameplay:**
1. Use Keycard to enter
2. Fight drones
3. Boss fight with Vex
4. Victory → Access Card + Security Logs
5. Logs reveal: "The Between incidents started 3 months ago. Subject 47 (Maya) was the first to return."

**The Dealer Commentary:**
- On Vex: "Chief Vex. Loyal soldier. Never asks questions. *yawns* Predictable."
- On phase 2: "Now it's getting interesting. *leans forward*"
- On victory: "Vex was always going to lose. He didn't know he was playing."

---

#### Scene 4: OFFICE (Director's Office)
**Status:** 🔨 To Build

**Purpose:** Story exposition, character choice

**Elements:**
- Director Chen (NPC - can be hostile or ally)
- Maya's Research Notes (item)
- Director's Terminal (reveals corporate conspiracy)
- Choice: Report to Chen or steal notes

**NPC: Director Chen**
- If you report: Gives you "Official Access" badge, but warns you to stop investigating
- If you steal notes: Chen becomes hostile, you must flee

**Choice Consequences:**
| Choice | Immediate | Later Impact |
|--------|-----------|--------------|
| Report | +Official Access, Chen friendly | Chen appears in Void, tries to stop you |
| Steal | Chen hostile, must flee | Chen absent from Void |

**Gameplay:**
1. Enter office
2. Chen is present, asks what you're doing
3. Choose: "Investigating Maya" or "Just looking around"
4. If honest: Can access terminal, learn truth
5. Find Maya's notes: "The Dealer isn't evil. He's trapped. The corporation made a deal..."
6. Choice moment

**The Dealer Commentary:**
- On Chen: "Director Chen. 14 years of service. 0 original thoughts. But useful... to someone."
- On reading notes: "Maya wrote about me? *shuffles uncomfortably* What did she say?"
- On choice: "Interesting. *makes note* This will matter later."

---

#### Scene 5: STORAGE
**Status:** 🔨 To Build

**Purpose:** Resource gathering, optional puzzle

**Elements:**
- Health Kits (3x, restore 30 HP each)
- Energy Drink (buff: +5 attack for 60 seconds)
- Broken Teleporter (puzzle - optional)
- Phaseburner's ghost (optional encounter)

**Puzzle: Broken Teleporter**
- Find 3 power cells hidden in boxes
- Arrange in correct sequence (clue in Maya's notes)
- Success: Teleports to secret area with bonus XP and lore

**Optional: Phaseburner's Ghost**
- Maya's old colleague who didn't survive The Between
- Warns you about The Dealer: "Don't trust his games. Don't play his rules."
- Gives cryptic hint about third ending

**The Dealer Commentary:**
- On entering: "The storage room. Where corporations hide their mistakes. And I've seen a lot of mistakes."
- On Phaseburner: "*silence* ...He shouldn't be able to speak to you. Interesting."

---

### ACT 2: Descent (7-10 min)

#### Scene 6: UPPER CORRIDOR
**Status:** 🔨 To Build

**Purpose:** Combat gauntlet, path choice

**Elements:**
- 4 Glitch Guards
- 1 Heavy Guard (tougher enemy)
- Three exits: Archives, Mainframe, Transit Hub

**Enemies:**
| Enemy | HP | Attack | Defense | XP |
|-------|-----|--------|---------|-----|
| Heavy Guard | 60 | 10 | 8 | 35 |

**The Dealer Commentary:**
- "The upper floors. Where decisions are made. Where destinies are... dealt."
- "Three doors. Three paths. All lead to me eventually."

---

#### Scene 7: ARCHIVES
**Status:** 🔨 To Build

**Purpose:** Major puzzle, lore dump

**Elements:**
- Archive Terminal (encrypted - puzzle)
- The Architect (NPC - mysterious figure)
- Void Key Fragment 1/3

**Puzzle: Archive Decryption**
1. Find 4 data fragments scattered in archives
2. Each fragment has a number/symbol
3. Enter correct sequence: MAYA-0047-BETWEEN
4. Success: Unlocks full truth about The Dealer

**NPC: The Architect**
- Created the teleportation system
- Made the original deal with The Dealer
- Offers choice: "Help me trap him forever" or "Help me free us both"

**Lore Revealed:**
- The Dealer was a human: Dr. Marcus Vale, lead researcher
- He got stuck in The Between during the first teleport test
- The corporation exploited his condition instead of saving him
- He's been "dealing" with teleporters ever since, collecting data on consciousness

**The Dealer Commentary:**
- On entering: "The Archives. My memory palace. Or is it my prison?"
- On Architect: "Him. *cards stop shuffling* We have history."
- On truth reveal: "...You know now. Does knowing change anything?"

---

#### Scene 8: MAINFRAME
**Status:** 🔨 To Build

**Purpose:** Boss fight, Void Key Fragment

**Elements:**
- CORE (Boss - AI defense system)
- Void Key Fragment 2/3
- Emergency Shutdown option (skips fight but has consequences)

**Boss Fight: CORE**
- HP: 150
- Phases:
  1. (100-70%): Laser attacks, dodge by moving
  2. (70-40%): Summons 2 drones, area attacks
  3. (40-0%): Desperate mode, rapid attacks, but defense drops

**Alternative: Emergency Shutdown**
- Skip the fight
- But: Lose all XP from this fight, and CORE appears in Void as an enemy

**The Dealer Commentary:**
- "CORE. The machine that thinks it's alive. Or the alive thing that thinks it's a machine?"
- On victory: "Impressive. You fight like someone who wants to survive."
- On shutdown: "Taking shortcuts? *marks in Ledger* I'll remember that."

---

#### Scene 9: TRANSIT HUB
**Status:** 🔨 To Build

**Purpose:** Point of no return, final preparation

**Elements:**
- Active Teleporter (leads to The Void)
- Void Key Fragment 3/3
- Maya's Final Message (recording)
- Vendor Terminal (spend XP on upgrades before final fight)

**Maya's Final Message:**
"If you're hearing this, you've come further than anyone except me. The Dealer isn't what you think. He's not evil - he's desperate. He's been playing this game for so long because it's the only way he can interact with anyone. The way to beat him isn't through combat. It's through choice. When you face him, remember: you have three options. Join his game forever. Escape and leave him behind. Or... flip the table. End the game entirely. I chose to escape. But maybe... maybe he deserves better. - Maya"

**Vendor Upgrades:**
| Upgrade | Cost | Effect |
|---------|------|--------|
| HP Boost | 50 XP | +25 Max HP |
| Attack Up | 40 XP | +5 Attack |
| Defense Up | 40 XP | +3 Defense |
| Critical Edge | 60 XP | +10% Crit Chance |

**The Dealer Commentary:**
- "The Transit Hub. The last station before The Between."
- On hearing Maya's message: "*long pause* She... remembered me."
- "Are you ready? The next door leads to my table. No more practice rounds."

---

### ACT 3: The Dealer (8-12 min)

#### Scene 10: THE VOID (Final Boss)
**Status:** ✅ Partially Exists (VoidScene.js)

**Purpose:** Final confrontation, three endings

**Layout:**
```
        ┌──────────────────────────────────┐
        │                                  │
        │      THE INFINITE TABLE          │
        │      ═══════════════════         │
        │                                  │
        │         [THE DEALER]             │
        │                                  │
        │    ♠  ♥  ♦  ♣  (floating)       │
        │                                  │
        │                                  │
        │          [AZIAH]                 │
        │                                  │
        │   [JOIN]  [ESCAPE]  [DESTROY]    │
        │                                  │
        └──────────────────────────────────┘
```

**The Confrontation:**

**Phase 1: The Wager**
- The Dealer offers a game: "One hand. Winner takes all."
- Player can accept or refuse
- If accept: Card game mini-game (skill-based)
- If refuse: Combat begins

**Phase 2: Combat (if refused or lost card game)**
- The Dealer has 3 phases:

| Phase | HP Range | Abilities |
|-------|----------|-----------|
| Amused | 100-70% | Card throws (ranged), teleports |
| Impressed | 70-40% | Summons past players as ghosts, area denial |
| Desperate | 40-0% | All-out attacks, dialogue changes to pleading |

**Phase 3: The Choice**
- When Dealer reaches 0 HP, he doesn't die
- Instead, three options appear:

---

## 🎭 The Three Endings

### Ending 1: JOIN THE GAME
**Trigger:** Choose "Join" or lose to The Dealer

**Scene:**
- Aziah takes a seat at the table
- The Dealer smiles genuinely for the first time
- "Finally. A partner. The game goes on."
- Aziah becomes the new observer, dealing cards to future players
- Credits show glimpses of endless card games

**The Dealer's Line:** "Welcome to eternity. It's not so bad once you stop counting the days."

**Stats Screen:**
- "You chose to stay"
- "The Dealer has a new partner"
- "The game continues..."

---

### Ending 2: ESCAPE THE BETWEEN
**Trigger:** Choose "Escape" after defeating The Dealer

**Scene:**
- A portal opens behind Aziah
- The Dealer watches, resigned
- "Go then. Maya did the same. Everyone leaves eventually."
- Aziah steps through, returns to the real world
- The lab is empty. Maya's gone. But Aziah is free.
- Credits show Aziah in the outside world, haunted by memories

**The Dealer's Line:** "Don't look back. It's better if you don't look back."

**Stats Screen:**
- "You escaped"
- "The Dealer remains alone"
- "Freedom has its price"

---

### Ending 3: FLIP THE TABLE
**Trigger:** Choose "Destroy" after defeating The Dealer

**Requirements:** Must have found at least 2/3 Void Key Fragments

**Scene:**
- Aziah approaches the table
- The Dealer tenses: "What are you-"
- Aziah flips the Infinite Table
- Everything shatters: cards, chips, the void itself
- The Dealer screams - then laughs, then cries
- "You... you actually did it. I'm free. I'm finally free."
- Dr. Marcus Vale's human form flickers into existence
- "Thank you. I'd forgotten what it felt like to end."
- The void collapses. Aziah wakes up in the lab.
- Maya is there. "You did it. You actually ended the game."

**The Dealer's Final Line:** "Every game has to end. Thank you for playing mine."

**Stats Screen:**
- "You ended the game"
- "Dr. Marcus Vale is at peace"
- "Maya remembers"
- "THE TRUE ENDING"

---

## 📊 Progression Balance

### Recommended Level Progression
| Scene | Recommended Level | XP Available |
|-------|-------------------|--------------|
| Lab | 1 | 0 |
| Corridor | 1-2 | 50 |
| Security | 2-3 | 115 |
| Office | 3 | 25 (optional) |
| Storage | 3 | 30 (optional) |
| Upper Corridor | 3-4 | 140 |
| Archives | 4 | 50 (puzzle) |
| Mainframe | 4-5 | 150 |
| Transit | 5 | 0 (shopping) |
| The Void | 5-6 | Final fight |

**Total Available XP:** ~560
**XP to Level 6:** 500
**Player should reach Level 5-6 by The Dealer**

### Dealer Fight Balance
| Difficulty | Dealer HP | Attack | Defense |
|------------|-----------|--------|---------|
| Easy | 200 | 15 | 8 |
| Normal | 300 | 20 | 12 |
| Hard | 400 | 28 | 15 |
| Nightmare | 500 | 35 | 20 |

---

## 🔧 Implementation Checklist

### Core Systems ✅
- [x] StatsSystem (HP, XP, Level)
- [x] CollisionSystem (Hitboxes)
- [x] CombatSystem (Damage, XP rewards)
- [x] DialogueSystem
- [x] InventorySystem
- [x] The Dealer (Commentary)
- [x] Stats HUD

### Scenes To Build
- [x] Lab Scene (Tutorial)
- [ ] Corridor Scene (Combat intro)
- [ ] Security Scene (Mini-boss)
- [ ] Office Scene (Story choice)
- [ ] Storage Scene (Resources)
- [ ] Upper Corridor (Hub)
- [ ] Archives Scene (Puzzle)
- [ ] Mainframe Scene (Boss)
- [ ] Transit Hub (Final prep)
- [x] Void Scene (Final boss - needs completion)

### Enemies To Create
- [ ] Glitch Guard (basic)
- [ ] Heavy Guard (tank)
- [ ] Security Drone (fast)
- [ ] Chief Vex (mini-boss)
- [ ] CORE (boss)
- [ ] Past Players (ghosts)
- [ ] The Dealer (final boss combat)

### NPCs To Create
- [x] Aziah (player)
- [ ] Director Chen
- [ ] The Architect
- [ ] Phaseburner's Ghost
- [ ] Maya (endings)

### Items To Add
- [x] SWAB Artifact
- [x] Security Keycard
- [ ] Access Card
- [ ] Maya's Notes
- [ ] Health Kit
- [ ] Energy Drink
- [ ] Void Key Fragments (3)
- [ ] Official Access Badge

### Puzzles To Design
- [ ] Broken Teleporter (Storage)
- [ ] Archive Decryption
- [ ] Card Game Mini-game (Dealer)

---

## 🎮 Control Scheme

### Movement
- **WASD / Arrow Keys:** Move
- **Click:** Move to location (point-and-click)

### Combat
- **Space / Click Enemy:** Attack
- **E:** Special ability (unlocked at Level 3)
- **Q:** Use item from hotbar

### Interaction
- **E:** Interact with objects/NPCs
- **I:** Open inventory
- **ESC:** Pause menu

---

## 🎵 Audio Plan (Future)

### Music Tracks
1. **Lab Theme:** Ambient electronic, curious
2. **Combat Theme:** Tense, rhythmic
3. **Boss Theme:** Intense, driving
4. **The Void Theme:** Eerie, card-shuffle sounds
5. **Ending Themes:** 3 variations (melancholic, hopeful, triumphant)

### Sound Effects
- Card shuffle (Dealer commentary)
- Damage taken/dealt
- Level up fanfare
- Item pickup
- Door open/close
- Teleporter activation

---

## 📝 Next Steps (Priority Order)

### Phase 1: Combat Loop
1. Create Glitch Guard enemy
2. Build Corridor scene with combat
3. Test combat balance

### Phase 2: Progression
4. Build Security scene (mini-boss)
5. Build Office scene (story choice)
6. Build Storage scene (resources)

### Phase 3: Mid-Game
7. Build Upper Corridor
8. Build Archives (puzzle)
9. Build Mainframe (boss)

### Phase 4: Finale
10. Build Transit Hub
11. Complete Void Scene (Dealer fight)
12. Implement three endings

### Phase 5: Polish
13. Balance pass
14. Add missing dialogue
15. Bug fixes
16. Optional: Audio

---

*"Every great game has a plan. But the best players know when to deviate from it."*
— The Dealer
