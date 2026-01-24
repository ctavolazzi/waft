# Deep Analyze: WAFT App (2026-01-20)

## Scope and Method
Focused local analysis of the WAFT repo using targeted file reads and structural review of key subsystems:
- CLI entrypoint (`src/waft/main.py`)
- Empirica integration (`src/waft/core/empirica.py`)
- TheOracle (epistemic intelligence) (`src/waft/core/science/oracle.py`)
- Science-Bitch scientific workflow (`src/waft/core/science_bitch.py`)
- TavernKeeper gamification core (`src/waft/core/tavern_keeper/keeper.py`)

## Entry Points and CLI Architecture
WAFT exposes a Typer-based CLI with a central app in `src/waft/main.py`. The module defines the `waft` command, wires subcommands, and provides utilities like command hooks via TavernKeeper.

Key observations:
- The CLI uses Typer with sub-apps and rich console output.
- Central helper `_process_tavern_hook` handles post-command narrative, dice rolls, and reward display.
- The CLI entry point is `main()` (Typer app invocation).

## Core Systems

### Empirica Integration
`EmpiricaManager` provides CLI/API integration for epistemic tracking:
- Resolves the appropriate `empirica` CLI binary (prefers Python 3.12/3.11).
- Supports a Python API manager where available.
- Performs project initialization checks and readiness validation.

### TheOracle (Epistemic Intelligence)
`TheOracle` enforces Empirica readiness, loads a personality profile, and provides:
- Epistemic state retrieval (`get_epistemic_state`)
- Logging of findings/unknowns
- Decision assessment gates
- Reflection and guidance generation

### Science-Bitch (Scientific Method)
`ScienceBitchManager` orchestrates a full scientific workflow:
- Creates `_science` directories and captures extensive context (git state, system state).
- Uses `scientific_method_tool` for experiment management and analysis.

### TavernKeeper (Gamification / Narrative)
`TavernKeeper` manages RPG-style progression and narrative:
- Stores persistent state in `_pyrite/.waft/chronicles.json` (TinyDB preferred, JSON fallback).
- Integrates optional dependencies like `tinydb`, `d20`, `tracery`.
- Uses Empirica to log character progression.

## Data and Storage
- Empirica data stored under `.empirica/` and in git notes.
- Gamification state in `_pyrite/.waft/`.
- Scientific method artifacts in `_science/`.

## Patterns and Algorithms
- Manager pattern: EmpiricaManager, ScienceBitchManager, TheOracle.
- CLI-first workflows with rich output and `typer.Exit` for error handling.
- Optional dependency fallback behavior (TinyDB/d20/tracery).
- State-capture pattern in Science-Bitch: gather git/system/environment/project state snapshots.

## Risks and Unknowns
- Runtime error encountered in `waft oracle`: `name 'Any' is not defined`. This suggests a missing import or annotation evaluation error in the Oracle path; requires targeted critique and fix.
- Large code surface area with many subsystems; further deep analysis could map module relationships and dependency graph.

## Next Steps
1. Run critique focusing on Oracle runtime error and dependency fallbacks.
2. Validate assumptions and create verification trace.
3. Apply fixes in respond-to-critique if warranted.
