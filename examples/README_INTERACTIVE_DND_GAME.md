# 🎲 Interactive D&D Game

A complete, playable D&D 5e adventure game built with WAFT tools!

## Features

### ✨ Core Gameplay
- **Character Creation**: Roll ability scores (4d6, drop lowest) and create your character
- **Combat System**: Turn-based combat with real dice rolling using the `d20` library
- **Interactive Choices**: Make decisions that affect your adventure
- **Shop System**: Buy weapons, armor, and consumables
- **Save/Load**: Save your progress and continue later

### 🎯 D&D 5e Mechanics
- **Real Dice Rolling**: Uses `DnDRoller` with the `d20` library
- **Combat Resolution**: Uses `DnD5eCombat` for attack rolls, damage, and healing
- **Character Stats**: Full D&D 5e character with ability scores, modifiers, AC, HP
- **Equipment System**: Equip weapons and armor that affect combat
- **Leveling**: Gain XP and level up after encounters

### 🛠️ Tools Used
- `DnD5eCharacter` - Character state management
- `DnDRoller` - Dice rolling (d20 library)
- `DnD5eCombat` - Combat mechanics
- `DnD5eStats` - Ability modifiers and calculations
- `Rich` - Beautiful console output
- `ArmorType` - Armor system

## How to Play

### Installation

```bash
# Make sure dependencies are installed
uv sync  # or: pip install -e .
```

### Running the Game

```bash
python examples/interactive_dnd_game.py
```

### Gameplay

1. **Create Your Character**
   - Enter your character's name
   - Roll ability scores (automatic)
   - View your starting stats

2. **Explore the World**
   - Choose actions: explore, shop, rest, combat, character sheet, save, quit
   - Make choices that affect your adventure
   - Discover encounters and treasures

3. **Combat**
   - Turn-based combat with enemies
   - Roll attack rolls and damage
   - Use strategy to defeat foes
   - Gain XP and gold from victories

4. **Shop**
   - Buy weapons (swords, daggers)
   - Buy armor (leather, chain mail, shields)
   - Buy consumables (healing potions, rations)
   - Equipment affects your combat effectiveness

5. **Rest**
   - Recover HP between encounters
   - Prepare for the next adventure

6. **Save Your Progress**
   - Save your game at any time
   - Load your saved game on next play

## Game Commands

| Command | Description |
|---------|-------------|
| `explore` | Explore the area and discover encounters |
| `shop` | Visit the shop to buy equipment |
| `rest` | Rest to recover HP |
| `character` | View your character sheet |
| `combat` | Start a combat encounter |
| `save` | Save your game progress |
| `quit` | Exit the game (with option to save) |

## Combat System

### Player Actions
- **Attack**: Roll to hit against enemy AC, deal damage on success
- **Flee**: Attempt to escape combat (DEX check)

### Combat Flow
1. Player turn: Choose action (attack/flee)
2. Roll attack roll (d20 + STR modifier + proficiency)
3. If hit, roll damage dice
4. Critical hits (natural 20) deal double damage
5. Enemy turn: Enemy attacks player
6. Repeat until one side is defeated

### Victory Rewards
- Experience points (XP)
- Gold pieces (gp)
- Level up after multiple encounters

## Shop Items

| Item | Cost | Effect |
|------|------|--------|
| Longsword | 15 gp | 1d8 damage weapon |
| Dagger | 2 gp | 1d4 damage weapon |
| Shield | 10 gp | +2 AC |
| Leather Armor | 10 gp | AC 11 |
| Chain Mail | 75 gp | AC 16 |
| Healing Potion | 50 gp | 2d4+2 healing |
| Rations | 5 gp | 1 day of food |

## Enemies

| Enemy | AC | HP | Damage | XP |
|-------|----|----|--------|-----|
| Goblin | 15 | 7 | 1d6 | 50 |
| Orc | 13 | 15 | 1d12+3 | 100 |
| Skeleton | 13 | 13 | 1d6+2 | 50 |
| Bandit | 12 | 11 | 1d6 | 25 |
| Wolf | 13 | 11 | 2d4+2 | 50 |

## Character Sheet

Your character sheet shows:
- **Ability Scores**: STR, DEX, CON, INT, WIS, CHA (with modifiers)
- **Combat Stats**: HP, AC, Level, Proficiency Bonus
- **Equipment**: Current weapon and armor
- **Resources**: Gold and inventory

## Save System

- Save files are stored as `dnd_game_save.json` in the examples directory
- Saves include: character stats, gold, inventory, story log, encounters completed
- Load your saved game when starting a new session

## Example Session

```
🎲 CHARACTER CREATION 🎲

What is your character's name? [Adventurer]: Thorin

Rolling ability scores (4d6, drop lowest)...
  STR: 15  DEX: 12  CON: 14
  INT: 10  WIS: 13  CHA: 11

✓ Character Created!
  Name: Thorin
  Level: 1
  HP: 12/12
  AC: 10
  Proficiency Bonus: +2

🎮 WELCOME TO THE ADVENTURE! 🎮

You find yourself in a small town. What would you like to do?

What do you do? [explore/shop/rest/character/combat/save/quit]: explore

You explore the area...

┌─────────────────────────────────────────┐
│ You discover an ancient ruin with       │
│ mysterious markings.                    │
└─────────────────────────────────────────┘

Would you like to investigate further? [y/N]: y

⚔️  COMBAT: Skeleton ⚔️

Enemy: Skeleton (AC 13, HP 13)
You: Thorin (AC 10, HP 12/12)

--- Round 1 ---

Your turn!
Action: [attack/flee]: attack
✓ You hit for 8 damage! (Skeleton HP: 5/13)

Skeleton's turn!
✗ Skeleton hits you for 4 damage! (Your HP: 8/12)

--- Round 2 ---

Your turn!
Action: [attack/flee]: attack
✓ You hit for 6 damage! (Skeleton HP: -1/13)

🎉 VICTORY! You defeated the Skeleton! 🎉

+ Gained 50 XP
+ Found 12 gp
```

## Extending the Game

The game is built with modular components that can be easily extended:

- **Add new enemies**: Edit `CombatEncounter.ENEMIES`
- **Add shop items**: Edit `Shop.ITEMS`
- **Add story events**: Extend the `explore` action
- **Add new locations**: Create new game areas
- **Add quests**: Implement a quest system
- **Add spells**: Implement spellcasting for spellcasters

## Technical Details

### Architecture
- **GameState**: Manages character, inventory, gold, story log
- **CombatEncounter**: Handles combat mechanics
- **Shop**: Manages shop interactions
- **Save/Load**: JSON-based persistence

### Dependencies
- `d20` - Dice rolling library
- `rich` - Beautiful terminal output
- WAFT D&D 5e modules - Character, combat, dice systems

## Credits

Built using:
- WAFT D&D 5e Physics Engine
- `d20` dice rolling library
- `rich` console library
- D&D 5e System Reference Document (SRD)

Enjoy your adventure! 🎲⚔️🛡️
