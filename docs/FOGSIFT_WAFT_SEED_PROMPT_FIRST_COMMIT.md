# FogSift WAFT Seed Prompt (First Commit Only)

Use this prompt when you want a strict first-commit bootstrap for the new `FogSift/waft` repository.

```text
You are initializing the very first commit of a new repository: FogSift/waft.

Important:
- Keep this to an ultra-minimal, production-sane scaffold.
- Do not add advanced features yet.
- Prioritize clarity, testability, and philosophical fidelity.

Mission to encode:
WAFT is an evolutionary code laboratory where agents are mutable code organisms, fitness is reality-grounded, and every evolutionary step is observable.

First-commit scope (target ~8 files, +/-2 max):
1) README.md
2) pyproject.toml
3) src/waft/__init__.py
4) src/waft/core.py
5) src/waft/cli.py
6) tests/test_core.py
7) tests/test_cli.py
8) .gitignore

Core models in `src/waft/core.py`:
- AgentGenome
- EvolutionEvent
- FitnessResult

Core behavior to implement:
- `spawn_genome(parent_id: str | None, mutation: str) -> AgentGenome`
- `evaluate_fitness(seed: int, stability: float, efficiency: float, safety: float) -> FitnessResult`
- `record_event(path: str, event: EvolutionEvent) -> None`  # append JSONL
- `read_lineage(path: str) -> list[EvolutionEvent]`

CLI in `src/waft/cli.py`:
- `waft init --path .`
- `waft spawn --mutation "..."`
- `waft eval --seed 42 --stability 0.8 --efficiency 0.7 --safety 0.9`
- `waft lineage`

Rules:
- Keep code direct, simple, and explicit.
- Use only standard library unless a dependency is truly necessary.
- No web server, no database, no background jobs.
- No plugin systems, no framework abstractions.
- No "TODO architecture" placeholders.

Testing requirements:
- Deterministic fitness result for same seed/inputs.
- JSONL event recording and lineage replay works.
- CLI commands run and return expected output shape.

Output format:
1) Show final file tree.
2) Provide full contents for all created files.
3) Provide run commands:
   - install
   - test
   - demo CLI flow
4) End with:
   - "Deferred for next milestone" list (max 6 bullets).
```
