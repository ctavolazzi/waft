---
id: TKT-2i9f-003
parent: WE-260111-2i9f
title: "Map component relationships and dependencies"
status: completed
created: 2026-01-12T00:42:07.821Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-2i9f-003: Map component relationships and dependencies

## Metadata
- **Created**: Sunday, January 11, 2026 at 4:42:07 PM PST
- **Parent Work Effort**: WE-260111-2i9f
- **Author**: ctavolazzi

## Description
(describe what needs to be done)

## Acceptance Criteria
- [ ] (define acceptance criteria)

## Files Changed
- `ARCHITECTURE_INVESTIGATION.md`

## Implementation Notes
- 1/11/2026: **Component Relationships Mapped**:

1. **CLI → Core Managers**:
   - main.py → MemoryManager, SubstrateManager, EmpiricaManager, etc.
   - Command handlers delegate to managers

2. **Core Managers → Modules**:
   - MemoryManager → memory.py → _pyrite/ structure
   - SubstrateManager → substrate.py → Agent substrate
   - EmpiricaManager → empirica.py → Epistemic tracking

3. **Agent System**:
   - BaseAgent → AgentState, AgentConfig, EvolutionaryEvent
   - BaseAgent → TheObserver (telemetry)
   - BaseAgent → LineagePoet (scientific naming)
   - BaseAgent → ScintDetector (fitness evaluation)

4. **Evolution System**:
   - ChatDistiller → DistilledChat → IdeaGene
   - StylingGenome → FontGene, MarginGene, ColorGene, LayoutGene
   - Generators (PDF/LaTeX) → Use ChatDistiller + StylingGenome

5. **Document Generation Chain**:
   - Content → ChatDistiller → DistilledChat
   - DistilledChat + StylingGenome → Generator → Output

**Dependencies Identified**:
- External: uv, Empirica, CrewAI, WeasyPrint, FastAPI, SvelteKit
- Internal: Core managers depend on core modules
- Evolution system depends on core/science (taxonomy, observer)

**Documentation Updated**: ARCHITECTURE_INVESTIGATION.md with component relationships.
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
