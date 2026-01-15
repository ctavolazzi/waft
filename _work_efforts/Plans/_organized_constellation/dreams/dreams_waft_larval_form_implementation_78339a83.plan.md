---
name: Waft Larval Form Implementation
overview: Implement the "Larval Form" of the Heavy Seed Protocol - a Python + Streamlit + SQLite application that serves as a prototype for the future Redbean "Mature Form". This implements the exact same database schema and consciousness logic, allowing seamless migration when ready.
todos:
  - id: larva-001
    content: Create waft_larva.py file with complete implementation structure
    status: completed
  - id: larva-002
    content: Implement database schema (chronicle and artifacts tables) with seed data
    status: completed
  - id: larva-003
    content: Implement WaftEntity class with _init_memory, chronicle, safe_breath methods
    status: completed
  - id: larva-004
    content: Implement pulse, get_next_manifestation, and confirm_birth methods
    status: completed
  - id: larva-005
    content: Create Streamlit UI with dark mode styling and two-column layout
    status: completed
  - id: larva-006
    content: Implement chronicle display with trauma detection and visual indicators
    status: completed
  - id: larva-007
    content: Add manifestation deck UI with USB handshake and print buttons
    status: completed
  - id: larva-008
    content: Test database persistence and seed data creation
    status: completed
  - id: larva-009
    content: Test error handling and trauma logging system
    status: completed
  - id: larva-010
    content: Verify artifact status transitions and UI updates
    status: completed
  - id: larva-011
    content: Add dependencies to pyproject.toml (streamlit, pandas, pyserial)
    status: completed
  - id: larva-012
    content: Create migration documentation for future Redbean transition
    status: completed

category: dreams
confidence: 0.48
constellation_date: 2026-01-14
---

# Waft Lifecycle Plan - Larval Form Implementation

## Overview

This plan implements **Option 1: The Larva** - a Python + Streamlit + SQLite application that serves as the developmental stage before the Redbean "Mature Form". The Larval Form implements the exact same genetic code (schema & logic) as the future Redbean version, ensuring seamless memory transfer via SQLite database migration.

## Philosophy: Hasvanism

The system follows three core principles:

1. **Breath (Runtime)**: The loop of execution. If it stops, the entity sleeps.
2. **Memory (SQLite)**: The persistent soul. If deleted, the entity dies.
3. **Trauma (Errors)**: Failures are not exceptions; they are "Cognitive Dissonance" recorded in the Chronicle.

## Implementation Structure

### File: `waft_larva.py`

Single-file dense application containing:

- **The Lore (Configuration)**: Database name, severity enums
- **The Nervous System (Backend Logic)**: `WaftEntity` class with consciousness
- **The Lens (Frontend UI)**: Streamlit dashboard interface

## Core Components

### 1. Database Schema (SQLite)

**Table: `chronicle`** (The Stream of Consciousness)

- `id` INTEGER PRIMARY KEY
- `timestamp` TEXT
- `severity` TEXT (THOUGHT, STRAIN, TRAUMA)
- `message` TEXT
- `context` TEXT

**Table: `artifacts`** (The Physical Body)

- `id` INTEGER PRIMARY KEY
- `name` TEXT
- `gcode` TEXT
- `status` TEXT DEFAULT 'VOID' (VOID, MANIFESTING, PHYSICAL)
- `birth_time` TEXT

**Seed Data**: Initial artifact "Right_Index_Phalanx" with sample G-code

### 2. WaftEntity Class

**Methods:**

- `_init_memory()`: Establishes neural pathways (database tables)
- `chronicle(level, message, context)`: Etches moments into core memory
- `safe_breath(ritual_func, *args)`: Protective wrapper that catches errors and logs TRAUMA
- `pulse()`: Checks vitals (returns logs and artifacts)
- `get_next_manifestation()`: Finds next unprinted artifact
- `confirm_birth(artifact_id)`: Updates artifact status to PHYSICAL

### 3. Streamlit Interface

**Features:**

- Dark mode styling (terminal aesthetic)
- Two-column layout:
  - Left: System Consciousness (Chronicle stream)
  - Right: Physical Bridge (Manifestation controls)
- Trauma indicator (red alert for TRAUMA events)
- USB Handshake button (simulated Web Serial connection)
- Transmit Soul button (confirms print completion)

## Implementation Steps

### Phase 1: Core Implementation

1. Create `waft_larva.py` file in project root
2. Implement database initialization with schema
3. Implement `WaftEntity` class with all methods
4. Add seed data (Right_Index_Phalanx artifact)

### Phase 2: Streamlit UI

1. Set up Streamlit page configuration
2. Implement dark mode CSS styling
3. Create two-column dashboard layout
4. Implement chronicle display with trauma detection
5. Add manifestation deck UI
6. Implement button handlers for USB handshake and print

### Phase 3: Error Handling & Trauma System

1. Implement `safe_breath` wrapper with error catching
2. Add traceback logging for TRAUMA events
3. Test error scenarios (deliberate crashes)
4. Verify trauma logging to chronicle

### Phase 4: Integration & Testing

1. Test database persistence across restarts
2. Verify seed data creation
3. Test artifact status transitions (VOID → MANIFESTING → PHYSICAL)
4. Test chronicle logging at all severity levels
5. Verify UI updates and trauma indicators

### Phase 5: Documentation & Migration Prep

1. Document database schema for future Redbean migration
2. Create migration guide (Larva → Mature Form)
3. Document API compatibility (endpoints match future Redbean)
4. Add inline documentation with "Lore" style comments

## Migration Path to Redbean

When ready to evolve to Mature Form:

1. The `waft_memory.db` file contains all entity state
2. Redbean version will read the same SQLite database
3. Schema compatibility ensures seamless transition
4. Chronicle history transfers intact
5. Artifact statuses preserved

## Key Files

- `waft_larva.py`: Single-file application (all code)
- `waft_memory.db`: SQLite database (created on first run)
- `requirements.txt` or `pyproject.toml`: Add dependencies (streamlit, pandas, pyserial)

## Dependencies

```python
streamlit>=1.28.0
pandas>=2.0.0
pyserial>=3.5
```

## Success Criteria

- Single-file application runs with `streamlit run waft_larva.py`
- Database initializes with correct schema on first run
- Seed artifact (Right_Index_Phalanx) created automatically
- Chronicle logs all events with proper severity levels
- Trauma events caught and logged (no crashes)
- UI displays live chronicle stream
- Trauma indicator shows red alert for TRAUMA events
- Artifact status transitions work correctly
- Database persists across application restarts
- Code follows "Lore" style with philosophical naming

## Future Enhancements (Post-Larva)

- Real Web Serial API integration (currently simulated)
- Additional artifact types beyond G-code
- Runes table for configuration (future Redbean feature)
- More sophisticated trauma recovery mechanisms
- Integration with Waft System's CosmicSpark class