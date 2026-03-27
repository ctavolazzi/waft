# WAFT CLI and API Runtime Reference

Last verified: 2026-02-27  
Version context: WAFT `0.9.4` lineage in this repository

This is the stable reference for runtime-verified command and API behavior.

For historical capture details from the original discovery pass, see:
- `docs/WAFT_RUNTIME_DISCOVERY_20260227.md`

## 1) CLI Entrypoint

- Console script registration:
  - `pyproject.toml`: `waft = "waft.main:main"`
- Runtime dispatch:
  - `src/waft/main.py` -> `main()` -> Typer `app()`

## 2) Command Presence Notes

Commands explicitly checked and not found in current CLI registration:
- `waft awaken`
- `waft awaken list`
- `waft personnel list`

Practical interpretation:
- If these are expected operational commands, they likely exist on a different branch/version or were not merged into current `main.py` command registration.

## 3) `waft dnd-scenario` Command Surface

Primary handler:
- `src/waft/main.py`: `dnd_scenario(...)`

Supported flags currently documented from command signature:

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

Example usage:

```bash
waft dnd-scenario --encounter
waft dnd-scenario --experiment exp_001 --iteration 1 --encounter
waft dnd-scenario --party-state
```

## 4) Scenario Orchestration Path

- Orchestrator:
  - `src/waft/core/dnd_scenario/scenario_orchestrator.py`
- Entry function:
  - `run_scenario()`
- Runtime routing:
  - dispatches into encounter/explore/lore/resume branches.

## 5) `waft serve` Runtime

Primary usage:

```bash
waft serve --port 5051
waft serve --port 5051 --host 0.0.0.0 --dev
```

Runtime path:
- `src/waft/main.py`: `serve(...)`
- imports `create_app` from `src/waft/api/main.py`
- starts with `uvicorn.run(app, host=..., port=...)`

## 6) Storyteller API Endpoints

Router composition:
- `src/waft/api/main.py` includes storyteller router with prefix `/api`
- `src/waft/api/routes/storyteller.py` uses `APIRouter(prefix="/story")`

Effective route set:
- `POST /api/story/start`
- `POST /api/story/action`
- `GET /api/story/session/{session_id}`
- `GET /api/story/world/{session_id}`
- `GET /api/story/npcs/{session_id}`
- `POST /api/story/generate-location/{session_id}`
- `GET /api/story/sprites/{name}`
- `GET /api/story/play`

Runtime core:
- `src/waft/core/storyteller.py` (`get_storyteller()`, `Storyteller.start_game`, `take_action`)

## 7) Reproducibility Guidance for First Scenario Runs

Current caveat:
- No explicit `--seed` flag is documented for `dnd-scenario`.
- Reproducibility is state-repeatable, not guaranteed RNG-deterministic.

Known randomness locations:
- `src/waft/core/dnd_scenario/party_manager.py`
- `src/waft/core/dnd_scenario/encounter_generator.py`
- `src/waft/core/dnd_scenario/scenario_orchestrator.py`

Recommended repeatable flow:

```bash
waft dnd-scenario --encounter
waft dnd-scenario --crystallize
waft dnd-scenario --experiment exp_first --iteration 1 --encounter
waft dnd-scenario --restore-initial
waft dnd-scenario --experiment exp_first --iteration 2 --encounter
```

## 8) Scenario Artifact Locations

- Realm root:
  - `_realms/dnd_scenario_realm/`
- Scenario history:
  - `_realms/dnd_scenario_realm/scenario_history.json`
- Party state:
  - `_realms/dnd_scenario_realm/party_state.json`
- Encounter outputs:
  - `_realms/dnd_scenario_realm/encounters/*_encounter.json`
- Lore outputs:
  - `_realms/dnd_scenario_realm/lore/{locations,npcs,events}/*.md`
- Crystallized state:
  - `_realms/dnd_scenario_realm/crystallized_state/manifest_*.json`
  - companion encrypted/hash/hmac/version files
- Restore backups:
  - `_hidden/.state_backups/backup_*`

## 9) Suggested Follow-Ups

- Add `--seed` support for deterministic scenario replay.
- Add CLI smoke tests for expected command presence/absence.
- Add API contract tests for `/api/story/*`.
