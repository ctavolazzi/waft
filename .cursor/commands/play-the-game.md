# /play-the-game - Run the Town Tavern Scenario

**Launch the interactive D&D 5e tavern scenario and play the game.**

---

## Purpose

This command runs the Town Tavern scenario - an interactive D&D 5e adventure where you wake up in a tavern with no memory of how you got there. You'll create a character, make skill checks, and navigate through an engaging narrative using the D&D 5e physics engine we built.

**Use when:**
- You want to test the D&D 5e system in action
- You want to play an interactive scenario
- You want to see how the physics engine works with real gameplay
- You want to demonstrate the system to others

---

## Execution

**Command**: `/play-the-game` or `/play` or `/tavern`

**What it does:**
1. Runs the `examples/tavern_scenario.py` script
2. Creates a D&D 5e character with rolled ability scores
3. Presents an interactive narrative with choices
4. Uses real D&D mechanics (skill checks, dice rolling, modifiers)
5. Demonstrates the physics engine in action

**Execution Steps:**
1. Run `python3 examples/tavern_scenario.py`
2. Follow the interactive prompts
3. Make choices that affect the story
4. Experience D&D 5e mechanics in action

---

## Gameplay

### Character Creation
- Roll ability scores (4d6, drop lowest)
- Calculate starting HP (hit die + CON modifier)
- Display character stats (AC, modifiers, proficiency)

### Interactive Choices
You'll be presented with multiple choices:
1. **Stand up slowly** - Perception check (WIS)
2. **Check your pockets** - Investigation check (INT)
3. **Ask the bartender** - Persuasion check (CHA)
4. **Try to remember** - Intelligence check (INT)

### Skill Checks
Each choice triggers a skill check using your character's ability modifiers:
- Roll d20
- Add ability modifier
- Compare to difficulty class (DC)
- Different outcomes based on success/failure

### Narrative
The story adapts based on your choices and roll results, leading to:
- Discovery of clues
- Interaction with NPCs
- Mysterious notes and encounters
- Multiple ending paths

---

## Features Demonstrated

1. **D&D 5e Physics Engine**:
   - Ability modifier calculation
   - Proficiency bonus
   - Skill checks
   - Dice rolling with `d20` library

2. **Character System**:
   - Character creation
   - Stat management
   - HP tracking
   - AC calculation

3. **Interactive Narrative**:
   - Player choices
   - Branching storylines
   - Dynamic outcomes based on rolls

---

## Requirements

- Python 3.10+
- `d20` library (already in dependencies)
- `rich` library (for console formatting)
- Dependencies installed: `uv sync` or `pip install -e .`

---

## Example Output

```
╔════════════════════════════════════════╗
║  TOWN TAVERN SCENARIO                  ║
║  A D&D 5e Adventure                    ║
╚════════════════════════════════════════╝

Creating Your Character...

What is your name? [Adventurer]: 

Rolling ability scores (4d6, drop lowest)...
  STR: 15  DEX: 13  CON: 14
  INT: 12  WIS: 10  CHA: 11

Character Created!
  Name: Adventurer
  Level: 1
  HP: 17/17
  AC: 11
  STR Modifier: +2
  Proficiency Bonus: +2

You wake up with a pounding headache...
[Interactive narrative continues]
```

---

## Troubleshooting

**Error: ModuleNotFoundError: No module named 'd20'**
- Solution: Install dependencies with `uv sync` or `pip install -e .`

**Error: ModuleNotFoundError: No module named 'rich'**
- Solution: Install rich: `pip install rich` or ensure all dependencies are installed

**Script not found**
- Solution: Ensure you're in the project root directory

---

## Integration

This scenario demonstrates:
- How to use the D&D 5e module (`waft.core.dnd5e`)
- Character creation patterns
- Skill check implementation
- Interactive narrative structure

You can use this as a template for creating more scenarios or integrating with the WAFT Being system.

---

## Future Enhancements

- Save/load character state
- Multiple scenarios
- Combat encounters
- Integration with WAFT Being class
- Persistent character progression
- Multi-player support

---

**Enjoy your adventure in the Town Tavern!**
