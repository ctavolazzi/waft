---
id: WE-260116-fikx
title: "Death Encounter System: D&D Saving Throws and Being vs Death"
status: active
created: 2026-01-17T04:34:45.629Z
created_by: ctavolazzi
last_updated: 2026-01-17T04:34:45.629Z
branch: feature/WE-260116-fikx-death_encounter_system_d_d_saving_throws_and_being_vs_death
repository: waft
---

# WE-260116-fikx: Death Encounter System: D&D Saving Throws and Being vs Death

## Metadata
- **Created**: Friday, January 16, 2026 at 8:34:45 PM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260116-fikx-death_encounter_system_d_d_saving_throws_and_being_vs_death

## Objective
Implement dramatic death system where beings get a final chance through CON saving throws when Will to Live reaches 0.0, then fight Death in narrative encounters that generate PDFs. Includes HP stat (optional for physical beings), decay system managed by God of Rot, and complete encounter generation.

## Tickets

| ID | Title | Status |
|----|-------|--------|
| TKT-fikx-001 | Add optional HP stat to Being class (has_physical_form flag) | ✅ completed |
| TKT-fikx-002 | Implement CON saving throw when Will to Live hits 0.0 | ✅ completed |
| TKT-fikx-003 | Create decay system for Will to Live, Stamina, and HP | pending |
| TKT-fikx-004 | Add God of Rot entity to Pantheon | pending |
| TKT-fikx-005 | Create Death entity with combat stats | pending |
| TKT-fikx-006 | Implement Being vs Death encounter generator | pending |
| TKT-fikx-007 | Generate encounter markdown documents | pending |
| TKT-fikx-008 | Convert encounter markdown to PDF | pending |
| TKT-fikx-009 | Integrate encounter system with death processing | pending |
| TKT-fikx-010 | Link encounters to death tombstones in Akasha | pending |

## Implementation Progress

**Phase 1: Foundation (✅ Complete)**
- ✅ Optional HP stat with `has_physical_form` flag
- ✅ CON saving throw when Will to Live hits 0.0
- ✅ Near-death experience system (restores Will to Live to 1.0 on success)
- ✅ Empirica integration for epistemic tracking (deaths, near-death experiences)

**Phase 2: Decay System (Pending)**
- ⏳ Decay rates for Will to Live, Stamina, HP
- ⏳ God of Rot entity

**Phase 3: Death Encounters (Pending)**
- ⏳ Death entity with combat stats
- ⏳ Encounter generator
- ⏳ Markdown → PDF conversion

## Empirica Integration

**Status**: ✅ Complete - All three systems integrated

**Death Encounter System:**
- Logs near-death experiences (saving throw successes) to Empirica
- Logs deaths with impact scores (0.8)
- Logs unknowns about death patterns for first-time deaths
- Tracks epistemic learning about death mechanics

**TheOracle:**
- Logs all consultations as findings (impact: 0.3)
- Logs decision assessments with gate results
- Tracks HALT/BRANCH/REVISE decisions as unknowns
- Enhances epistemic intelligence with usage tracking

**prove-it Scripts:**
- Logs proof experiment results to Empirica
- Tracks verified/refuted hypotheses as findings
- Logs refuted hypotheses as unknowns for investigation
- Measures learning from proof demonstrations

## Commits
- Phase 1: HP stat and saving throw implementation
- Empirica integration: Death system, Oracle, prove-it

## Related
- Docs: (to be linked)
- PRs: (to be added)
