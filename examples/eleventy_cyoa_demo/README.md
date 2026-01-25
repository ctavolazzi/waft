# Eleventy CYOA Demo Scenario

A simple Choose-Your-Own-Adventure scenario demonstrating the Level 1 (Eleventy CYOA) format for WAFT.

## Story Structure

```
start
├── dark_passage
│   ├── mushroom_grove (ending)
│   └── crystal_chamber (ending)
├── underground_river
│   ├── crystal_chamber (ending)
│   └── underwater_ending (ending)
└── retreat (ending)
```

## Running the Scenario

```python
from pathlib import Path
from waft.core.scenario_formats import ElevntyCYOAParser

# Load and run the scenario
scenario = ElevntyCYOAParser.load_scenario("examples/eleventy_cyoa_demo")
scenario.run_interactive()
```

## Format Specification

Each `.md` file follows the Eleventy CYOA pattern:

```yaml
---
title: Node Title
choices:
  - text: Choice description
    path: target_node_id
  - text: Another choice
    path: another_node_id
---

Markdown content goes here. Can include **formatting**, lists, etc.
```

**No choices = Ending node**

## Endings

This scenario has 5 possible endings:
1. **Cautious Explorer** - Turn back and report findings
2. **Mushroom Mystic** - Experience visions from the glowing fungi
3. **Crystal Keeper** - Discover the singing crystal chamber
4. **Depth Walker** - Find the underwater civilization
5. **Crystal Keeper** (alternate path) - Reach crystals via river route

## Why This Pattern?

- **Dead simple**: Writers can create scenarios without learning complex schemas
- **Version control friendly**: Plain text Markdown
- **AI-generatable**: LLMs can easily create valid scenarios
- **Extensible**: Can upgrade to Level 2 (Ink) or Level 3 (WAFT Native) when mechanics are needed
