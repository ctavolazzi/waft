# Scenario Engine Demo

**Date**: 2026-01-13  
**Status**: ✅ Working Demo

---

## Overview

This demo demonstrates a working Python implementation of the HannaCLIEngine architecture, showing:

- ✅ JSON-based scenario files
- ✅ Sequence/Choice/Container system
- ✅ Conditional choices based on container state
- ✅ Execution tracking and event logging
- ✅ PDF report generation

---

## Files

### Core Engine
- **`demo_scenario_engine.py`** - Minimal scenario engine implementation
  - `ScenarioEngine` class - Main engine
  - `ScenarioEvent` dataclass - Event tracking
  - `run_demo_scenario()` - Demo runner

### Scenario Data
- **`demo_scenario.json`** - Sample scenario: "The Mysterious Tavern"
  - 9 sequences (4 ordinary, 5 end)
  - 3 containers (inventory, clues, karma)
  - Conditional choices demonstrating container-based logic

### Demo Runner
- **`run_demo.py`** - Executes demo and generates PDF
  - Runs scenario with auto-play
  - Captures execution events
  - Generates markdown story
  - Creates PDF report

### Output
- **`scenario_engine_demo_report.pdf`** - Generated PDF showing execution

---

## Running the Demo

```bash
cd _work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine
uv run python run_demo.py
```

Or from project root:
```bash
uv run python _work_efforts/WE-260113-75vp_hannacliengine_architecture_study_python_scenario_engine/run_demo.py
```

---

## Demo Execution Flow

1. **Load Scenario**: Reads `demo_scenario.json`
2. **Initialize**: Maps sequences, creates containers
3. **Start**: Begins at `seq_001` (wake up in tavern)
4. **Auto-Play**: Automatically chooses first available option
5. **Track Events**: Records each sequence, choice, outcome
6. **Update Containers**: Tracks state changes (inventory, clues)
7. **Generate PDF**: Converts execution log to markdown → PDF

---

## Demo Scenario: "The Mysterious Tavern"

### Story Path (Auto-Play)
1. **seq_001**: Wake up → Choose A (look around) → Get mysterious note
2. **seq_002**: Read note → Choose A (look for key) → Get ornate key
3. **seq_004**: Have note + key → Choose A (go to mill) → End

### Containers Updated
- **clues**: `["mysterious_note"]`
- **inventory**: `["ornate_key"]`
- **karma**: `[]` (empty)

### Conditional Choices Demonstrated
- In `seq_003`, choice A requires `rusty_key` in inventory
- In `seq_004`, choice A requires `ornate_key` in inventory
- These choices only appear if conditions are met

---

## Architecture Highlights

### Sequence Execution
```python
engine.run_sequence("seq_001")
# → Displays text
# → Filters choices (set vs conditional)
# → Records event
```

### Choice Processing
```python
engine.make_choice("seq_001", "A")
# → Finds choice
# → Displays outcome
# → Updates containers
# → Returns next sequence ID
```

### Container System
```python
# Initialize
containers = {"inventory": [], "clues": [], "karma": []}

# Add value
containers["inventory"].append("ornate_key")

# Check condition
if "ornate_key" in containers["inventory"]:
    # Show conditional choice
```

---

## PDF Output

The generated PDF includes:
- Scenario metadata (title, author, description)
- Complete execution log with all sequences
- Choices made and outcomes
- Container state changes
- Final container state

**File**: `scenario_engine_demo_report.pdf` (15.8 KB)

---

## Next Steps

This demo proves the concept works. For full implementation:

1. **Integration with Being System**: Map Being state to containers
2. **D&D 5e Skill Checks**: Add skill check logic to choices
3. **Memory Generation**: Convert outcomes to Being memories
4. **Interactive Mode**: Allow real player input
5. **Save/Load**: Persist scenario state
6. **Multiple Beings**: Support collaborative scenarios

---

## Key Design Decisions

1. **Auto-Play for Demo**: Always chooses first option (simplifies demo)
2. **Event Tracking**: Every action recorded for PDF generation
3. **Markdown → PDF**: Uses WAFT's PDFGenerator for output
4. **Minimal Implementation**: Core concepts only, no extras

---

**Demo Status**: ✅ Working  
**PDF Generated**: ✅ Yes  
**Ready for**: Architecture review, integration planning
