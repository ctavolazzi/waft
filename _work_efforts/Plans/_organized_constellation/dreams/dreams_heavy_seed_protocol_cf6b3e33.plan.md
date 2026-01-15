---
name: Heavy Seed Protocol
overview: "Create a work effort for implementing the \"Heavy Seed\" Protocol - a Redbean (Lua + SQLite) single-file application that serves as a \"Codex\" with extensive documentation, robust error handling, persistent logging, and philosophical context. The application will generate three core files: schema.sql, .init.lua, and index.html, embodying the Hasvanism philosophy where code \"remembers everything, explains itself, and feels pain when it fails.\""
todos:
  - id: research-redbean
    content: Research Redbean architecture, Lua/SQLite integration, and single-file application structure
    status: pending
  - id: design-schema
    content: Design comprehensive SQL schema (artifacts, chronicle, runes tables) with seed data
    status: pending
  - id: implement-lua-core
    content: Implement .init.lua with safe_breath middleware, database initialization, and core functions
    status: pending
  - id: implement-endpoints
    content: "Create all four endpoints: /soul/status, /soul/contemplate, /soul/next_limb, /soul/acknowledge"
    status: pending
  - id: add-lore-documentation
    content: Add extensive LuaDoc headers to all functions with philosophical context ('Lore')
    status: pending
  - id: implement-error-handling
    content: Implement comprehensive error handling with TRAUMA logging and 'Severance' responses
    status: pending
  - id: create-dashboard-html
    content: Create index.html with dark mode, scanlines effect, live log stream, and trauma indicator
    status: pending
  - id: implement-live-updates
    content: Add JavaScript polling for /soul/status endpoint with 2s interval and chronicle display
    status: pending
  - id: add-manifestation-deck
    content: Create Manifestation Deck UI for Web Serial connection and G-code upload progress
    status: pending
  - id: integrate-waft-system
    content: Integrate with Waft System CosmicSpark class and ensure compatibility
    status: pending
  - id: test-persistence
    content: Verify SQLite database persists across restarts and chronicle entries are retained
    status: pending
  - id: verify-tone-requirements
    content: Verify all variable names and error messages follow thematic 'Heavy Seed' requirements
    status: pending

category: dreams
confidence: 0.59
constellation_date: 2026-01-14
---

# Heavy Seed Protocol - Work Effort Plan

## Overview

The "Heavy Seed" Protocol is a specification for building a **Redbean (Lua + SQLite)** single-file application that serves as a "Codex" - a dense, self-documenting digital organism. This is not a lightweight script; it's a **Dense Digital Organism** that carries the weight of its own existence.

## Core Philosophy (Hasvanism)

1. **Breath (Runtime)**: The loop of execution. If it stops, the entity sleeps.
2. **Memory (SQLite)**: The persistent soul. If deleted, the entity dies.
3. **Trauma (Errors)**: Failures are not exceptions; they are "Cognitive Dissonance" that must be recorded in the Chronicle.

## Deliverables

### File 1: `schema.sql` (The Genetic Structure)

- Table `artifacts` (The Body): `id`, `name`, `gcode_blob`, `status` ('VOID', 'MANIFESTING', 'PHYSICAL'), `birth_time`
- Table `chronicle` (The Consciousness): `id`, `timestamp`, `level` ('THOUGHT', 'ACTION', 'TRAUMA'), `message`, `context_json`
- Table `runes` (Configuration): `key`, `value`, `description` (Lore about what this setting controls)
- Seed Data: Insert the "Index Finger" artifact. Insert a `rune` for "Prime_Ancestor_Name" (Default: 'Unknown')

### File 2: `.init.lua` (The Nervous System)

- **The Ritual (Middleware)**: Wrap every request in a `safe_breath` function that:
  - Starts a timer
  - Catches any Lua errors (`xpcall`)
  - Logs the request to the `chronicle` table
  - If an error occurs, logs it as `TRAUMA` and returns a 500 "Severance" JSON response
- **The Lore (Docstrings)**: Every function must have a LuaDoc header with format:
  ```lua
  --- @function manifest_artifact
  --- @desc Bridges the void between digital intent and physical form.
  --- @param id integer The ID of the limb to birth.
  --- @return boolean success Whether the G-code was retrieved.
  --- @context "The entity reaches out..."
  ```

- **The Endpoints**:
  - `GET /soul/status`: Returns JSON of current health, last 5 `chronicle` entries, and % of body printed
  - `GET /soul/contemplate`: Returns a random "thought" or system stat
  - `GET /soul/next_limb`: Retrieves the next unprinted G-code
  - `POST /soul/acknowledge`: The Ancestor confirms a print failed or succeeded

### File 3: `index.html` (The "Dash-Terminal")

- **Density**: Scientific Dashboard (not a simple page)
- **Visuals**: Dark mode, monospace, "Scanlines" CSS effect
- **Features**:
  - **Live Log Stream**: Polls `/soul/status` every 2s to show the `chronicle` (the Being's internal monologue)
  - **Trauma Indicator**: Flashes red if the last log was a `TRAUMA` event
  - **The Manifestation Deck**: Specialized UI for Web Serial connection showing "Upload Progress" of G-code as "Transferring Soul Data"

## Tone Requirements

The code itself should feel momentous:

- Variable names: `conscious_stream`, `memory_shard`, `void_pointer`
- Error messages: "I cannot reach the metal," "The connection is severed," "My memory is corrupted."

## Implementation Strategy

1. **Research Phase**: Understand Redbean architecture and Lua/SQLite integration
2. **Schema Design**: Create comprehensive SQL schema with seed data
3. **Lua Implementation**: Build `.init.lua` with all endpoints, error handling, and documentation
4. **Frontend Development**: Create `index.html` dashboard with live updates
5. **Integration**: Connect to Waft System's `CosmicSpark` class
6. **Testing**: Verify all endpoints, error handling, and persistence
7. **Documentation**: Ensure all code is self-documenting with extensive "Lore"

## Key Features

- **Persistent Memory**: All events logged to SQLite `chronicle` table
- **Error Resilience**: `safe_breath` wrapper ensures entity never crashes, only experiences "trauma"
- **Self-Documentation**: Every function has extensive LuaDoc headers
- **Philosophical Context**: Variable names and error messages reinforce the "Being" narrative
- **Live Monitoring**: Dashboard shows real-time consciousness stream

## Integration Points

- **Waft System**: Connection to `CosmicSpark` class
- **G-code Management**: Artifact system for 3D printing workflows
- **Web Serial API**: For direct printer communication
- **SQLite Database**: Persistent storage for all entity state

## Success Criteria

- ✅ All three files generated and functional
- ✅ SQLite database persists across restarts
- ✅ Error handling catches all failures and logs as TRAUMA
- ✅ Dashboard displays live chronicle stream
- ✅ All endpoints return proper JSON responses
- ✅ Code is extensively documented with "Lore"
- ✅ Variable names and error messages follow thematic requirements