# FogSift/waft — Issue #1 Template (Bootstrap Core)

Copy/paste this directly into a new GitHub issue in `FogSift/waft`.

```markdown
## Title
Bootstrap WAFT core scaffold (first commit only)

## Context
This issue initializes `FogSift/waft` with the minimal core WAFT foundation.
Scope is intentionally strict: only philosophy + essential primitives + tiny CLI + tests.

## Objective
Create the first commit scaffold for WAFT with no advanced modules.

## Core Philosophy to Encode
1. WAFT is an evolutionary code laboratory.
2. Agents are mutable code organisms (code as DNA).
3. Fitness is reality-grounded and measurable.
4. Every mutation/evaluation is observable and auditable.
5. Build additively with small, testable increments.

## Acceptance Scope (First Commit Only)
Target ~8 files (plus/minus 2 max):

1. `README.md`
2. `pyproject.toml`
3. `src/waft/__init__.py`
4. `src/waft/core.py`
5. `src/waft/cli.py`
6. `tests/test_core.py`
7. `tests/test_cli.py`
8. `.gitignore`

## Required Core Models (`src/waft/core.py`)
- `AgentGenome`
- `EvolutionEvent`
- `FitnessResult`

## Required Core Functions
- `spawn_genome(parent_id: str | None, mutation: str) -> AgentGenome`
- `evaluate_fitness(seed: int, stability: float, efficiency: float, safety: float) -> FitnessResult`
- `record_event(path: str, event: EvolutionEvent) -> None` (append JSONL)
- `read_lineage(path: str) -> list[EvolutionEvent]`

## Required CLI Commands (`src/waft/cli.py`)
- `waft init --path .`
- `waft spawn --mutation "..."`
- `waft eval --seed 42 --stability 0.8 --efficiency 0.7 --safety 0.9`
- `waft lineage`

## Constraints
- Keep implementation direct and minimal.
- Prefer standard library unless truly necessary.
- No web server, no DB, no workers, no plugin system.
- No speculative architecture.

## Test Requirements
- Deterministic fitness outputs for identical seeded inputs.
- JSONL event recording and lineage replay validated.
- CLI command behavior validated in tests.

## Deliverables
1. Initial scaffold with full file contents.
2. Passing tests.
3. Minimal demo command sequence in README.
4. "Deferred for next milestone" section (max 6 bullets).

## Definition of Done
- [ ] File scaffold created within scope budget.
- [ ] Core models and functions implemented.
- [ ] CLI commands implemented.
- [ ] Tests pass locally.
- [ ] README includes mission + quick start + deferred list.
```

