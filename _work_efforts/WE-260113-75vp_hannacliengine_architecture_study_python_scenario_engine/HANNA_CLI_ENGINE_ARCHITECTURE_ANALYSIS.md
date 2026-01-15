# HannaCLIEngine Architecture Analysis

**Date**: 2026-01-13  
**Work Effort**: WE-260113-75vp  
**Status**: Research Phase Complete

---

## Overview

HannaCLIEngine is a Choose Your Own Adventure (CYOA) game engine written in C++ that processes JSON game files. It's paired with Hanna-Studio, a C# GUI editor for creating games. The engine is designed to be simple, data-driven, and focused on branching narratives with conditional choices.

**Repository**: `DeanEncoded/HannaCLIEngine`  
**Language**: C++ (Engine), C# (Studio)  
**Last Updated**: ~2 years ago (inactive)

---

## Core Architecture

### Two-Component System

1. **HannaCLIEngine (C++)** - Runtime engine that executes games
2. **Hanna-Studio (C#)** - Visual editor for creating games

### Engine Execution Flow

```
1. Load JSON game file
2. Parse metadata (title, author, description, start sequence)
3. Map sequence IDs to indexes
4. Initialize containers (empty vectors)
5. Start game from startSq
6. Run sequence → Display choices → Process choice → Next sequence
```

---

## JSON Game File Structure

### Top-Level Structure

```json
{
  "gameTitle": "Game Title",
  "gameAuthor": "Author Name",
  "gameDesc": "Game Description",
  "startSq": "sequence_id_01",
  "gameContainers": ["inventory", "weapons", "friends"],
  "sequences": [...]
}
```

### Sequence Structure

```json
{
  "sqId": "unique_sequence_id",
  "sqType": "ordinary" | "end",
  "mainText": "Primary narrative text displayed to player",
  "secondaryText": "Secondary text (e.g., 'What do you do?')",
  "choices": [...]
}
```

**Sequence Types:**
- **ordinary**: Has choices, continues game flow
- **end**: Displays text and ends game

### Choice Structure

```json
{
  "choiceLetter": "A",
  "choiceType": "set" | "conditional",
  "choiceText": "Text displayed as choice option",
  "outcomeText": "Text displayed after choice is made",
  "choiceCondition": {
    "container": "inventory",
    "value": "sword"
  },
  "containerAdd": {
    "container": "inventory",
    "value": "key"
  },
  "nextSq": "sequence_id_02"
}
```

**Choice Types:**
- **set**: Always displayed
- **conditional**: Only displayed if `choiceCondition.value` exists in `choiceCondition.container`

---

## Container System

### Concept

Containers are named collections (vectors) that store string values. They track game state and enable conditional choices.

### Implementation

```cpp
std::map<std::string, std::vector<std::string>> gameContainers;
```

**Example:**
- Container: `"inventory"` → Values: `["sword", "key", "potion"]`
- Container: `"weapons"` → Values: `["pistol", "knife"]`

### Operations

1. **Initialize**: Empty vectors created for each container in `gameContainers`
2. **Add Value**: When choice with `containerAdd` is made, value is pushed to container
3. **Check Condition**: Loop through container vector to find matching value

### Conditional Choice Logic

```cpp
// Check if value exists in container
for (int o = 0; o < gameContainers[conditionContainer].size(); o++) {
    if (gameContainers[conditionContainer][o] == conditionValue) {
        // Display choice
    }
}
```

---

## Engine Processing Logic

### Sequence Execution (`runSequence`)

1. **Clear screen** (unless debug mode)
2. **Display sequence ID** (debug mode only)
3. **Display mainText**
4. **Display secondaryText**
5. **Process choices**:
   - Loop through all choices
   - If `choiceType == "set"`: Always display
   - If `choiceType == "conditional"`: Check container condition
   - Build `validChoiceLetters` array
6. **If `sqType == "end"`**: Display "THE END" and exit
7. **Otherwise**: Call `makeChoice(choices)`

### Choice Processing (`makeChoice`)

1. **Validate input**: Check if user input matches `validChoiceLetters`
2. **Display outcomeText**
3. **Process containerAdd**: Add value to container if specified
4. **Navigate to nextSq**: Recursively call `runSequence(nextSq)`

### Key Design Patterns

1. **Recursive Navigation**: `runSequence` calls itself via `nextSq`
2. **State Tracking**: Containers persist across sequences
3. **Conditional Filtering**: Choices filtered at display time
4. **Letter Mapping**: Choices mapped to letters (a, b, c, d)

---

## Data Structures

### Engine State

```cpp
// Metadata
std::string gameTitle, gameAuthor, gameDesc, startSq;

// Sequence management
std::map<std::string, int> sequenceMapper;  // sqId → index
nlohmann::json sequences;                   // All sequences

// Container system
std::map<std::string, std::vector<std::string>> gameContainers;

// Choice management
std::map<std::string, int> choiceMapper;    // "a" → 0, "b" → 1, etc.
std::vector<std::string> validChoiceLetters;

// Debug
bool debug = false;
std::string currentSequenceId;
```

---

## Key Insights for WAFT Adaptation

### Strengths

1. **Simple, data-driven**: Games defined in JSON, not code
2. **Flexible containers**: Can represent inventory, state, flags, etc.
3. **Conditional choices**: Enables branching based on state
4. **Clear separation**: Engine vs. Editor

### Limitations

1. **No container disposal**: Can't remove values (planned feature)
2. **Single condition**: Only one condition per choice (planned: multiple)
3. **String-based**: All values are strings
4. **No save/load**: No persistence mechanism
5. **Windows-only**: Uses Windows-specific console functions

### WAFT Integration Opportunities

1. **Being State as Containers**:
   - Being skills → `"cognitive_skills"` container
   - Being karma → `"karma_state"` container
   - Being memories → `"memories"` container

2. **D&D 5e Integration**:
   - Skill checks as conditional choice triggers
   - Ability scores as container values
   - Dice rolls determine choice availability

3. **Memory Generation**:
   - Scenario outcomes → Being memories
   - Container state changes → Learning events
   - Sequence completion → Experience points

4. **Reality System**:
   - Scenarios as reality configurations
   - Multiple beings playing same scenario
   - Shared containers for collaborative scenarios

---

## Python Adaptation Design

### Proposed JSON Schema

```json
{
  "scenario_id": "tavern_mystery_001",
  "title": "The Tavern Mystery",
  "author": "WAFT System",
  "description": "A being wakes up in a tavern...",
  "start_sequence": "seq_001",
  "containers": ["inventory", "clues", "karma_state", "skills"],
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
          "skill_check": {
            "skill": "perception",
            "ability": "wis",
            "dc": 15,
            "success_sq": "seq_002",
            "failure_sq": "seq_003"
          },
          "container_add": {
            "container": "clues",
            "value": "mysterious_note"
          },
          "next_sq": "seq_002"
        }
      ]
    }
  ]
}
```

### Key Differences from HannaCLIEngine

1. **Skill Checks**: Added `skill_check` property for D&D 5e integration
2. **Success/Failure Branching**: Different sequences based on skill check results
3. **Container Types**: Support for different value types (not just strings)
4. **Being Integration**: Containers map to Being state automatically

---

## Next Steps

1. ✅ Clone and examine HannaCLIEngine structure
2. ⏳ Document complete JSON schema (with examples)
3. ⏳ Analyze engine execution flow in detail
4. ⏳ Map concepts to WAFT Being/Reality systems
5. ⏳ Design Python ScenarioEngine architecture
6. ⏳ Plan integration with Being state and D&D 5e
7. ⏳ Create architecture comparison document

---

## References

- **Repository**: https://github.com/DeanEncoded/HannaCLIEngine
- **Engine Code**: `HannaCLIEngine/game.cpp`, `HannaCLIEngine/HannaCLIEngine.h`
- **Studio Code**: `Hanna-Studio/` (C# project)
- **Sample Project**: `sample-projects/Multiple-Protagonists.hprj`

---

**Analysis Complete**: 2026-01-13 00:30 PST
