---
name: HannaCLIEngine Architecture Study
overview: Study HannaCLIEngine as a reference architecture to design a Python-based Choose Your Own Adventure engine for WAFT beings, adapting its sequence/choice/container model to integrate with WAFT's reality and being systems.
todos:
  - id: clone_hanna
    content: Clone HannaCLIEngine repository and examine structure
    status: pending
  - id: analyze_json_schema
    content: Document HannaCLIEngine JSON game file schema and structure
    status: pending
  - id: study_engine_logic
    content: Analyze how HannaCLIEngine processes sequences, choices, and containers
    status: pending
  - id: map_to_waft
    content: Map HannaCLIEngine concepts to WAFT Being/Reality systems
    status: pending
  - id: design_python_engine
    content: Design Python ScenarioEngine architecture with classes and JSON schema
    status: pending
  - id: create_integration_plan
    content: Plan integration with Being state, D&D 5e mechanics, and memory flow
    status: pending
  - id: document_architecture
    content: Create architecture analysis document comparing HannaCLIEngine to WAFT design
    status: pending

category: dreams
confidence: 1.00
constellation_date: 2026-01-14
---

# HannaCLIEngine Architecture Study & Python Adaptation Plan

## Objective

Study HannaCLIEngine's architecture and design patterns to inform the creation of a Python-based Choose Your Own Adventure engine for WAFT. This will enable structured interactive scenarios for beings in realities, replacing the current hardcoded tavern scenarios with a flexible, data-driven system.

## Current State Analysis

### WAFT's Current Interactive Scenarios

- **Location**: `examples/tavern_scenario.py`, `examples/being_plays_tavern_game.py`
- **Pattern**: Hardcoded Python functions with if/else branching
- **Integration**: Directly calls D&D 5e mechanics, Being class methods
- **Limitations**:
  - Scenarios are code, not data
  - Difficult to create new scenarios without coding
  - No reusable engine for branching narratives
  - Conditional logic is embedded in code

### HannaCLIEngine Architecture (to study)

**Core Components:**

1. **Game File Format (JSON)**

   - Sequences (sqId, sqType, mainText, secondaryText)
   - Choices (choiceLetter, choiceType, choiceText, outcomeText)
   - Conditional choices (choiceCondition with container/value)
   - Container system (inventory, state tracking)
   - Next sequence routing (nextSq)

2. **Engine (C++)**

   - Parses JSON game files
   - Manages game state
   - Handles container operations
   - Executes conditional logic
   - Routes between sequences

3. **Studio (C#)**

   - Visual editor for creating games
   - Project management (.hprj files)
   - Game metadata (title, author, description)

**Key Design Patterns:**

- **Data-driven**: Games defined in JSON, not code
- **State containers**: Track player inventory/state
- **Conditional choices**: Choices appear based on container contents
- **Sequence-based**: Game flow through numbered sequences
- **Type system**: Ordinary sequences vs. End sequences

## Research Phase

### 1. Repository Analysis

- Clone and examine HannaCLIEngine structure
- Document JSON schema for game files
- Analyze engine logic (how it processes sequences/choices)
- Study container system implementation
- Review sample projects for patterns

### 2. Architecture Mapping

Map HannaCLIEngine concepts to WAFT concepts:

| HannaCLIEngine | WAFT Equivalent |

|----------------|----------------|

| Game File | Reality Scenario Definition |

| Sequence | Scenario Node/Scene |

| Choice | Being Decision Point |

| Container | Being State (skills, karma, inventory) |

| Player | Being Instance |

| Game State | Reality State + Being State |

### 3. Integration Points

- **Being System**: Use Being's skills, karma, memories as containers
- **Reality System**: Scenarios become reality configurations
- **D&D 5e Integration**: Skill checks as conditional choice triggers
- **Memory Flow**: Scenario outcomes generate memories/lessons

## Design Phase

### Python Engine Architecture

**Core Classes:**

1. `ScenarioEngine` - Main engine class

   - Loads scenario JSON
   - Manages game state
   - Executes sequences
   - Handles choice resolution

2. `ScenarioSequence` - Represents a game sequence

   - Sequence ID, type (ordinary/end)
   - Main/secondary text
   - Available choices (filtered by conditions)

3. `ScenarioChoice` - Represents a player choice

   - Choice text, outcome text
   - Conditions (container checks)
   - Actions (container modifications)
   - Next sequence routing

4. `ScenarioContainer` - State tracking

   - Container name (e.g., "inventory", "skills", "karma")
   - Values stored in container
   - Check if value exists
   - Add/remove values

5. `BeingScenarioAdapter` - WAFT integration

   - Maps Being state to containers
   - Converts Being skills → container values
   - Tracks scenario progress in Being memory
   - Generates memories from outcomes

**JSON Schema (Python adaptation):**

```json
{
  "scenario_id": "tavern_mystery_001",
  "title": "The Tavern Mystery",
  "author": "WAFT System",
  "description": "A being wakes up in a tavern...",
  "start_sequence": "seq_001",
  "containers": ["inventory", "clues", "karma_state"],
  "sequences": [
    {
      "sq_id": "seq_001",
      "sq_type": "ordinary",
      "main_text": "You wake up with a pounding headache...",
      "secondary_text": "What do you do?",
      "choices": [
        {
          "choice_letter": "A",
          "choice_type": "set",
          "choice_text": "Stand up slowly (Perception check)",
          "outcome_text": "You notice a mysterious note...",
          "skill_check": {"skill": "perception", "ability": "wis"},
          "container_add": {"container": "clues", "value": "mysterious_note"},
          "next_sq": "seq_002"
        }
      ]
    }
  ]
}
```

## Implementation Plan

### Phase 1: Core Engine (Week 1)

1. Create `src/waft/scenarios/` module
2. Implement `ScenarioEngine` class
3. Implement `ScenarioSequence` and `ScenarioChoice` classes
4. Implement `ScenarioContainer` class
5. JSON schema validation
6. Basic sequence execution (no conditions yet)

### Phase 2: Conditional Logic (Week 1-2)

1. Implement container value checking
2. Conditional choice filtering
3. Container add/remove operations
4. Integration with Being state (skills, karma)

### Phase 3: WAFT Integration (Week 2)

1. Create `BeingScenarioAdapter` class
2. Map Being skills → scenario containers
3. Map Being karma → karma_state container
4. Generate memories from scenario outcomes
5. Track scenario progress in Being memory

### Phase 4: D&D 5e Integration (Week 2-3)

1. Skill check system for conditional choices
2. Dice rolling integration
3. Ability modifier calculations
4. Success/failure branching

### Phase 5: Scenario Creation Tools (Week 3)

1. JSON schema documentation
2. Scenario template generator
3. Validation tools
4. Example scenarios (tavern, research, evolution)

### Phase 6: Migration (Week 3-4)

1. Convert existing tavern scenario to JSON
2. Test with Being instances
3. Generate scientific reports from scenario outcomes
4. Document migration process

## Files to Create

### Core Engine

- `src/waft/scenarios/__init__.py`
- `src/waft/scenarios/engine.py` - Main ScenarioEngine class
- `src/waft/scenarios/sequence.py` - ScenarioSequence class
- `src/waft/scenarios/choice.py` - ScenarioChoice class
- `src/waft/scenarios/container.py` - ScenarioContainer class
- `src/waft/scenarios/schema.py` - JSON schema validation

### Integration

- `src/waft/scenarios/being_adapter.py` - BeingScenarioAdapter
- `src/waft/scenarios/dnd_integration.py` - D&D 5e skill checks

### Tools & Examples

- `scripts/waft-scenario.py` - CLI tool for running scenarios
- `examples/scenarios/tavern_mystery.json` - Example scenario
- `docs/SCENARIO_ENGINE.md` - Documentation
- `docs/SCENARIO_CREATION_GUIDE.md` - How to create scenarios

## Key Design Decisions

1. **JSON vs. Python DSL**: Use JSON (like HannaCLIEngine) for data-driven scenarios, but provide Python API for programmatic generation
2. **Container Mapping**: Flexible mapping system - Being skills can map to multiple containers (e.g., "cognitive_skills", "technical_skills")
3. **Memory Generation**: Automatic memory extraction from scenario outcomes based on Being's learning objectives
4. **State Persistence**: Scenarios can be saved/resumed using Being memory system
5. **Multi-being Support**: Engine supports multiple beings playing same scenario (for reality scenarios)

## Success Criteria

- [ ] Engine can load and execute JSON scenarios
- [ ] Conditional choices work based on container state
- [ ] Being state integrates with scenario containers
- [ ] D&D 5e skill checks work in scenarios
- [ ] Existing tavern scenario converted to JSON
- [ ] Beings can play scenarios and generate memories
- [ ] Documentation complete with examples

## Research Deliverables

1. **Architecture Analysis Document**: Detailed breakdown of HannaCLIEngine's design
2. **JSON Schema Documentation**: Complete schema for WAFT scenario format
3. **Integration Design**: How scenarios connect to Being/Reality systems
4. **Migration Guide**: How to convert existing scenarios to new format

## Next Steps

1. Clone HannaCLIEngine repository
2. Analyze JSON game file structure
3. Study engine execution flow
4. Document architecture patterns
5. Design Python adaptation
6. Begin implementation