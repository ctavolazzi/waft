---
id: TKT-2i9f-002
parent: WE-260111-2i9f
title: "Identify main entry points and core modules"
status: in_progress
created: 2026-01-12T00:42:07.819Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-2i9f-002: Identify main entry points and core modules

## Metadata
- **Created**: Sunday, January 11, 2026 at 4:42:07 PM PST
- **Parent Work Effort**: WE-260111-2i9f
- **Author**: ctavolazzi

## Description
(describe what needs to be done)

## Acceptance Criteria
- [ ] (define acceptance criteria)

## Files Changed
- `src/waft/main.py`
- `ARCHITECTURE_INVESTIGATION.md`

## Implementation Notes
- 1/11/2026: **Main Entry Point Identified**: `src/waft/main.py`

**Key Findings**:

1. **CLI Framework**: Typer
   - Main app: `app = typer.Typer(name="waft")`
   - Entry: `main()` → `app()`

2. **Core Managers** (Orchestration Layer):
   - MemoryManager - `_pyrite/` memory system
   - SubstrateManager - Agent substrate
   - EmpiricaManager - Epistemic tracking
   - GamificationManager - D&D gamification
   - GitHubManager - GitHub integration
   - TavernKeeper - Narrative system

3. **Module Structure**:
   - `core/` - Core orchestration (managers, agents, science, decision)
   - `evolution/` - Evolution system (PDF, LaTeX, document generation)
   - `templates/` - Document templates
   - `api/` - FastAPI web API
   - `cli/` - CLI display components
   - `ui/` - UI components

4. **Command Structure**:
   - Main commands: new, verify, evolve, sync, add, init, info, serve, decide
   - Sub-commands: session, finding, unknown, goal, github, journal, analytics
   - Gamification: dashboard, stats, character, chronicle, observe

**Documentation Created**: `ARCHITECTURE_INVESTIGATION.md` with initial findings.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
