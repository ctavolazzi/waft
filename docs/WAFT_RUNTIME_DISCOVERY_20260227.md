# WAFT Runtime Discovery - 2026-02-27

This document is the dated discovery snapshot.

For the maintained reference, see:
- `docs/CLI_RUNTIME_REFERENCE.md`

## CLI Root Entrypoint

- Console script wiring:
  - `pyproject.toml`: `waft = "waft.main:main"`
- Runtime entry:
  - `src/waft/main.py` -> `main()` -> Typer `app()`

## Command Reality Check: `awaken` and `personnel`

- No registered Typer commands or handlers for:
  - `waft awaken`
  - `waft awaken list`
  - `waft personnel list`
- Search scope used:
  - `src/waft/main.py`
  - `src/waft/cli/*`
  - markdown/scripts scanned for literal command usage
- Practical conclusion:
  - These commands are not present in current WAFT CLI state in this repo snapshot (v0.9.4 lineage).

## `waft dnd-scenario` Entrypoint and Syntax

- Handler:
  - `src/waft/main.py` -> `dnd_scenario(...)` (Typer command `dnd-scenario`)
- Supported flags (from handler signature):
  - Mode flags:
    - `--encounter`
    - `--explore`
    - `--lore`
    - `--resume`
  - State flags:
    - `--party-state`
    - `--crystallize`
    - `--restore-initial`
  - Experiment flags:
    - `--experiment`
    - `--iteration`
  - Science flags:
    - `--science`
    - `--hypothesis`
    - `--iterations`
- Orchestration route:
  - `src/waft/core/dnd_scenario/scenario_orchestrator.py` -> `run_scenario()`
  - Routing branches into encounter/explore/lore/resume handlers.
- Example calls:
  - `waft dnd-scenario --encounter`
  - `waft dnd-scenario --experiment exp_001 --iteration 1 --encounter`
  - `waft dnd-scenario --party-state`

## `waft serve` on Port 5051

- Handler:
  - `src/waft/main.py` -> `serve(...)`
- Syntax:
  - `waft serve --port 5051`
  - optional: `waft serve --port 5051 --host 0.0.0.0 --dev`
- Runtime path:
  - `serve()` imports `create_app` from `src/waft/api/main.py`
  - launches via `uvicorn.run(app, host=..., port=...)`

## Storyteller API Route Map

- Router registration:
  - `src/waft/api/main.py` includes storyteller router with prefix `/api`
- Story router:
  - `src/waft/api/routes/storyteller.py` with `APIRouter(prefix="/story")`
- Effective endpoints:
  - `POST /api/story/start`
  - `POST /api/story/action`
  - `GET /api/story/session/{session_id}`
  - `GET /api/story/world/{session_id}`
  - `GET /api/story/npcs/{session_id}`
  - `POST /api/story/generate-location/{session_id}`
  - `GET /api/story/sprites/{name}`
  - `GET /api/story/play`
- Runtime core:
  - `src/waft/core/storyteller.py`
  - key entrypoints: `get_storyteller()`, `Storyteller.start_game`, `take_action`

## Deterministic-First Scenario Notes

Important caveat: no explicit `--seed` flag is present for `dnd-scenario` in current command surface.

Randomness sources observed in:
- `src/waft/core/dnd_scenario/party_manager.py`
- `src/waft/core/dnd_scenario/encounter_generator.py`
- `src/waft/core/dnd_scenario/scenario_orchestrator.py`

Reproducibility flow (same starting state, not strict RNG determinism):
1. `waft dnd-scenario --encounter` (initial run and realm creation)
2. `waft dnd-scenario --crystallize`
3. `waft dnd-scenario --experiment exp_first --iteration 1 --encounter`
4. `waft dnd-scenario --restore-initial`
5. `waft dnd-scenario --experiment exp_first --iteration 2 --encounter`

## Artifact Persistence Map

- Realm root:
  - `_realms/dnd_scenario_realm/`
- Scenario history:
  - `_realms/dnd_scenario_realm/scenario_history.json`
- Party state:
  - `_realms/dnd_scenario_realm/party_state.json`
- Encounter logs:
  - `_realms/dnd_scenario_realm/encounters/*_encounter.json`
- Lore files:
  - `_realms/dnd_scenario_realm/lore/{locations,npcs,events}/*.md`
- Crystallized snapshots:
  - `_realms/dnd_scenario_realm/crystallized_state/manifest_*.json`
  - plus encrypted/hash/hmac/version files in same state bundle
- Restore backups:
  - `_hidden/.state_backups/backup_*` (from `realm_state_preserver.py`)

## Follow-Up Candidates

- Add `--seed` to `waft dnd-scenario` for strict reproducibility.
- Add CLI smoke tests that assert `awaken` and `personnel` availability status (expected missing, unless intentionally added).
- Add endpoint contract tests for storyteller routes under `/api/story/*`.
