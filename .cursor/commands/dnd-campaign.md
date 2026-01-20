# /dnd-campaign - Launch D&D Campaign

**Purpose:** Launch a full D&D 5e campaign session with interactive gameplay, quest generation, and story progression

**Usage:** `/dnd-campaign [options]`

**Options:**
- `--mode [interactive|web|scenario]` - Campaign mode (default: interactive)
- `--new-party` - Create a new party (force new party creation)
- `--location [name]` - Start at specific location
- `--quest [quest_id]` - Start with specific quest active

---

## Overview

The D&D Campaign command launches a complete D&D 5e campaign experience using the WAFT D&D infrastructure:

- **Interactive Mode**: Full interactive CLI campaign with party management, combat, exploration, and quests
- **Web Mode**: Launch the web-based D&D game UI (FastAPI + HTML)
- **Scenario Mode**: Run AI-driven scenario generation with quest PDF creation

**Perfect for:**
- Starting a new D&D campaign session
- Continuing an existing campaign
- Generating quest PDFs from scenarios
- Interactive gameplay with party management

---

## Quick Start

### Interactive Campaign
```
/dnd-campaign
```

Launches an interactive CLI campaign with:
- Party creation/loading
- Combat encounters
- Exploration scenarios
- Quest management
- Story progression

### Web-Based Game
```
/dnd-campaign --mode web
```

Launches the web UI at http://localhost:8003 with:
- Character creation
- Turn-based combat
- Shop system
- Quest system
- Multiple locations
- Save/load functionality
- Spellcasting

### Scenario Generation
```
/dnd-campaign --mode scenario
```

Runs AI-driven scenario generation:
- Encounter scenarios
- Exploration scenarios
- Lore scenarios
- Quest PDF generation

---

## Campaign Modes

### Interactive Mode (Default)

Full-featured CLI campaign with:
- **Party Management**: Create or load party of adventurers
- **Combat System**: Turn-based combat with D&D 5e rules
- **Exploration**: Discover locations, NPCs, and events
- **Quest System**: Accept and complete quests
- **Story Progression**: Dynamic narrative generation

**Features:**
- Real-time dice rolling (d20 library)
- Character sheets with full stats
- Equipment and inventory management
- Level progression
- Save/load game state

### Web Mode

Browser-based D&D game with modern UI:
- **FastAPI Backend**: RESTful API for game state
- **HTML/CSS/JS Frontend**: Responsive web interface
- **Real-time Updates**: Live game state synchronization
- **Multiple Systems**: Combat, shop, quests, locations, spells

**Access:** http://localhost:8003

**Features:**
- Character creation with stat rolling
- Turn-based combat with visual feedback
- Shop with weapons, armor, consumables
- Quest system with objectives tracking
- Travel between locations
- Detailed inventory management
- Spellcasting system
- Save/load functionality

### Scenario Mode

AI-driven scenario generation for quest creation:
- **Encounter Scenarios**: Combat encounters with party
- **Exploration Scenarios**: Location discovery and events
- **Lore Scenarios**: NPCs, history, and world-building
- **Quest PDFs**: Generate quest booklets using Typst templates

**Output:**
- Scenario results (JSON)
- Quest markdown
- Quest PDFs (if Typst available)
- Party state updates

---

## Campaign Features

### Party System

- **Party Members**: Create adventurers as Beings
- **Character Stats**: Full D&D 5e character sheets
- **Party State**: Persistent party state management
- **Load/Save**: Continue campaigns across sessions

### Combat System

- **D&D 5e Rules**: Attack rolls, saving throws, damage
- **Turn-Based**: Player and enemy turns
- **Dice Rolling**: Real dice mechanics (d20 library)
- **Critical Hits**: Natural 20s deal double damage
- **Fleeing**: DEX checks to escape combat

### Quest System

- **Quest Types**: Combat, exploration, delivery quests
- **Objectives**: Track quest progress
- **Rewards**: XP, gold, items
- **Quest PDFs**: Generate quest booklets

### Locations

- **Multiple Areas**: Town, Forest, Cave, Ruins
- **Location Events**: Area-specific encounters
- **Travel System**: Move between locations
- **Location History**: Track visited areas

### Equipment & Inventory

- **Weapons**: Swords, daggers with damage dice
- **Armor**: Leather, chain mail with AC bonuses
- **Consumables**: Healing potions, rations
- **Equipment Effects**: Stats affect combat

### Spellcasting

- **Spell List**: Firebolt, Healing Word, Magic Missile, Cure Wounds
- **Level Requirements**: Spells require character level
- **Combat Spells**: Cast in combat for damage/healing
- **Spell Effects**: Damage dice and healing dice

---

## Integration

The campaign system integrates with:

- **D&D 5e Core**: `DnD5eCharacter`, `DnDRoller`, `DnD5eCombat`
- **Scenario System**: `ScenarioRealm`, `ScenarioOrchestrator`
- **Quest System**: `QuestPDFGenerator` with Typst templates
- **Party System**: `PartyManager`, `PartyStateManager`
- **Being System**: Party members as Beings
- **Brief System**: Quest PDF generation

---

## Technical Details

### Interactive Mode

**Script**: `examples/interactive_dnd_game.py`
**Dependencies**: `d20`, `rich`, WAFT D&D core

### Web Mode

**Backend**: `examples/dnd_game_server.py` (FastAPI)
**Frontend**: `examples/dnd_game_ui.html`
**Port**: 8003
**Dependencies**: FastAPI, WAFT D&D core

### Scenario Mode

**Modules**: `src/waft/core/dnd_scenario/`
**Output**: `_realms/dnd_scenario_realm/`
**Dependencies**: Scenario orchestrator, quest PDF generator

---

## Usage Examples

### Example 1: Start Interactive Campaign

```
/dnd-campaign
```

**Output**:
- Party creation/loading
- Interactive game loop
- Combat, exploration, quests

### Example 2: Launch Web Game

```
/dnd-campaign --mode web
```

**Output**:
- FastAPI server starts on port 8003
- Browser opens automatically
- Web UI ready for gameplay

### Example 3: Generate Scenario Quest

```
/dnd-campaign --mode scenario --new-party
```

**Output**:
- New party created
- Scenario executed
- Quest PDF generated

### Example 4: Continue Campaign

```
/dnd-campaign --mode web
```

**Output**:
- Loads existing game state
- Continues from last save
- All progress preserved

---

## Campaign Flow

### Interactive Mode Flow

```
1. Initialize Campaign
   ├─> Load or create party
   ├─> Initialize scenario realm
   └─> Load quest system

2. Game Loop
   ├─> Display options (explore/shop/rest/combat/quests)
   ├─> Player chooses action
   ├─> Execute action
   │   ├─> Combat: Turn-based battle
   │   ├─> Explore: Random events
   │   ├─> Shop: Buy equipment
   │   ├─> Rest: Recover HP
   │   └─> Quests: Manage objectives
   ├─> Update game state
   └─> Repeat

3. Save Progress
   └─> Save game state to file
```

### Web Mode Flow

```
1. Start Server
   ├─> FastAPI server on port 8003
   └─> Open browser

2. Character Creation
   ├─> Enter character name
   ├─> Roll ability scores
   └─> Create character

3. Gameplay
   ├─> Explore locations
   ├─> Combat encounters
   ├─> Shop for equipment
   ├─> Accept/complete quests
   ├─> Cast spells
   └─> Save progress

4. Continue Session
   └─> Load saved game
```

### Scenario Mode Flow

```
1. Initialize Scenario
   ├─> Create/load party
   ├─> Initialize orchestrator
   └─> Setup quest generator

2. Run Scenario
   ├─> Select mode (encounter/explore/lore)
   ├─> Execute scenario
   ├─> Generate quest markdown
   └─> Compile quest PDF

3. Save Results
   ├─> Scenario results (JSON)
   ├─> Quest markdown
   └─> Quest PDF (if Typst available)
```

---

## Philosophy

The D&D Campaign command provides:
- **Complete Experience**: Full D&D 5e gameplay
- **Multiple Interfaces**: CLI, web, and scenario modes
- **Persistent State**: Save and continue campaigns
- **Quest Integration**: Generate quest PDFs
- **Flexible Play**: Choose your preferred mode

It's designed to be:
- **Easy to Start**: Simple command launches everything
- **Feature-Rich**: All D&D systems integrated
- **Persistent**: Save progress across sessions
- **Extensible**: Easy to add new features

---

## Future Enhancements

- Multiplayer support
- Advanced spell system
- More character classes
- Campaign story arcs
- NPC relationship system
- World map navigation
- Advanced quest chains
- Character progression trees

---

**Created to provide a complete D&D 5e campaign experience using WAFT infrastructure.**

---

End Command ---
