---
id: TKT-2i9f-001
parent: WE-260111-2i9f
title: "Read and analyze root README.md"
status: completed
created: 2026-01-12T00:42:07.817Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-2i9f-001: Read and analyze root README.md

## Metadata
- **Created**: Sunday, January 11, 2026 at 4:42:07 PM PST
- **Parent Work Effort**: WE-260111-2i9f
- **Author**: ctavolazzi

## Description
(describe what needs to be done)

## Acceptance Criteria
- [ ] (define acceptance criteria)

## Files Changed
- `README.md`

## Implementation Notes
- 1/11/2026: Starting investigation from README.md entry point.

**Key Findings from README:**

1. **Core Purpose**: WAFT is "A Python framework for directed evolution of self-modifying AI agents" - the goal is to observe a "God-Head" agent emerge from evolutionary process.

2. **Three Core Pillars**:
   - **The Substrate**: Agents that write their own Python source code (DNA)
   - **The Physics**: Scint System (Reality Fracture Detection) as fitness function
   - **The Flight Recorder**: Telemetry system for phylogenetic trees

3. **Main Entry Points**:
   - CLI commands via `waft` command (installed via `uv tool install waft`)
   - Main commands: `new`, `verify`, `evolve`, `sync`, `add`, `init`, `info`, `serve`
   - Empirica commands: `session`, `finding log`, `unknown log`, `check`, `assess`
   - Gamification commands: `dashboard`, `stats`, `character`, `chronicle`, `observe`

4. **Project Structure**:
   - `_pyrite/` - Memory structure (active, backlog, standards, gym_logs)
   - `src/agents.py` - Agent definitions
   - `pyproject.toml` - uv project config
   - Uses `uv` package manager and `just` task runner

5. **Key Documentation References**:
   - `docs/AI_SDK_VISION.md` - Complete vision and architecture
   - `docs/designs/002_agent_interface.md` - BaseAgent specification
   - `docs/research/evolutionary_architecture.md` - Scientific doctrine
   - `docs/research/state_of_art_2026.md` - Research synthesis

**Next Steps**: Trace CLI entry point to understand command structure and module organization.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
