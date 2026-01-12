# Town Tavern Scenario

A classic D&D scenario demonstrating the D&D 5e physics engine integration with WAFT.

## Overview

You wake up in a tavern with no memory of how you got there. Your character has D&D 5e stats, and you'll need to use them to navigate the situation and uncover the mystery.

## Features

- **Character Creation**: Roll ability scores (4d6, drop lowest)
- **Skill Checks**: Perception, Investigation, Persuasion, Intelligence checks
- **Interactive Choices**: Multiple paths through the scenario
- **D&D 5e Mechanics**: Uses the physics engine we built (modifiers, proficiency, dice rolling)

## Running the Scenario

```bash
# Make sure dependencies are installed
uv sync  # or: pip install -e .

# Run the scenario
python examples/tavern_scenario.py
```

## What It Demonstrates

1. **Character Creation**: Creates a D&D 5e character with rolled stats
2. **Ability Modifiers**: Calculates and uses ability modifiers for skill checks
3. **Dice Rolling**: Uses the `d20` library for all rolls
4. **Skill Checks**: Different ability scores affect different checks
5. **Interactive Narrative**: Player choices affect the story

## Scenario Structure

1. **Wake Up**: Character wakes up in tavern
2. **First Choice**: How do you react? (4 options with different skill checks)
3. **Mystery**: A stranger approaches with a note
4. **Final Choice**: What do you do next? (3 options)

## Extending the Scenario

This is a template for creating more scenarios. You can:
- Add more choices and branches
- Include combat encounters (using `DnD5eCombat`)
- Add inventory management
- Create multiple connected scenarios
- Integrate with WAFT Being system

## Next Steps

- Add combat encounters
- Create more scenarios (old mill, town investigation, etc.)
- Integrate with Being class for persistent characters
- Add save/load functionality
- Create a scenario engine for procedural generation
