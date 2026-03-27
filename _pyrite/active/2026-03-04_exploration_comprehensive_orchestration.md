# 2026-03-04 Exploration - Comprehensive Orchestration

## Objective
Map current Waft execution surfaces and integration points relevant to new-environment oracle bootstrap.

## Architecture Notes
- API composition is centralized in `src/waft/api/main.py` with route registration under `/api/*`.
- Pantheon oracle-cycle route is active:
  - `src/waft/api/routes/pantheon_oracle_cycle.py`
  - mounted at `/api/pantheon/oracle-cycle/*`
- UI exists and depends on that route:
  - `src/waft/pantheon/ui/oracle_cycle.html`
  - `src/waft/pantheon/ui/oracle_cycle_app.mjs`

## Key Behavioral Finding
- Planned CLI/module invocation (`waft.pantheon.oracle_cycle`) is not currently importable in this repo state.
- Oracle-cycle operation is currently API-first and artifact persistence writes under:
  - `<WAFT_PROJECT_PATH>/_pantheon/oracle_cycle/runs`

## External-Drive Experiment Finding
- Existing run artifact confirmed in EasyStore experiment path:
  - `/Volumes/Easystore/waft-experiments/20260304_oracle_cycle_bootstrap/_pantheon/oracle_cycle/runs/20260304_082101.json`

## Risks
1. Operator confusion due to mismatch between documented module command and runtime entrypoint.
2. Output path mismatch vs pre-created `oracle_runs/` operator expectation.
3. Limited local disk headroom in workspace environment (15Gi available).

## Opportunity
- Introduce a stable CLI alias in Waft that internally dispatches to existing oracle-cycle logic while preserving deterministic artifact output controls.
