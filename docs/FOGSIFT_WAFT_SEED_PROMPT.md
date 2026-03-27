# FogSift WAFT Seed Prompt (Core Only)

Use this prompt to bootstrap the new `FogSift/waft` repository with only foundational WAFT philosophy and core architecture.

```text
You are helping initialize the new WAFT repository from zero.

Goal:
Create a minimal, clean foundation that captures WAFT's core philosophy and core elements only. Do not implement advanced modules yet.

Core philosophy to encode:
1) WAFT is an evolutionary code laboratory.
2) Agents are mutable code organisms (code as DNA).
3) Fitness is measured through reality-grounded evaluation, not vibes.
4) Every mutation and evaluation must be observable and auditable.
5) Build additively: small, testable increments over speculative abstractions.

Core elements to include now:
- README with mission, philosophy, and first-run instructions.
- Minimal Python package layout under `src/waft/`.
- Core domain models:
  - AgentGenome (identity + mutable code/config reference)
  - EvolutionEvent (spawn/mutate/eval/survive/death records)
  - FitnessResult (stability/efficiency/safety scores + total fitness)
- A tiny "substrate" interface showing how an agent mutation is represented.
- A tiny "gym" interface showing how fitness is evaluated.
- A local "flight recorder" that writes append-only JSONL lineage events.
- One CLI entrypoint with just a few commands:
  - `waft init`
  - `waft spawn`
  - `waft eval`
  - `waft lineage`
- Basic tests that prove:
  - events are recorded,
  - fitness output is deterministic for seeded inputs,
  - lineage can be replayed.

Constraints:
- Keep implementation direct and minimal.
- Prefer single-file implementations per feature area until size justifies splitting.
- No placeholder enterprise architecture.
- No web UI yet.
- No external services required for first run.
- Keep dependencies lean.

Deliverables:
1) File tree of proposed initial scaffold.
2) Initial implementation of the core files.
3) A short "What is intentionally deferred" section.
4) Exact commands to run tests and a minimal demo flow.
```
