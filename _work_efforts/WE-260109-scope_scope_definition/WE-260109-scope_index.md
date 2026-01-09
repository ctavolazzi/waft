---
id: WE-260109-scope
title: "Scope Definition & Feature Consolidation"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
last_updated: 2026-01-09T00:00:00.000Z
branch: claude/explore-waft-UugBV
repository: waft
---

# WE-260109-scope: Scope Definition & Feature Consolidation

## Metadata
- **Created**: Thursday, January 9, 2026
- **Author**: Claude Audit System
- **Repository**: waft
- **Branch**: claude/explore-waft-UugBV
- **Priority**: CRITICAL

## Objective

**Answer the existential question: What IS Waft?**

Define clear scope, consolidate overlapping features, and establish what belongs in core vs plugins. This is the single most important strategic decision for the project.

## The Scope Problem

### Current State: Identity Crisis

Waft currently tries to be:
1. ✅ **Meta-framework** (environment, memory, substrate)
2. ⚠️ **Gamification system** × 2 (Integrity/Insight + full D&D RPG)
3. ⚠️ **Decision support tool** (weighted sum analysis)
4. ⚠️ **Analytics platform** (session tracking, productivity trends)
5. ⚠️ **Epistemic tracker** (Empirica integration)
6. ⚠️ **RPG game** (full D&D 5e mechanics: 1,014 LOC)
7. ⚠️ **Goal/workflow manager** × 3 (goals + workflows + compose)
8. ⚠️ **Web dashboard** (visualization)
9. ⚠️ **API server** (FastAPI routes)

**Result**: 29+ commands, 12,731 LOC, unclear value proposition

### The Audit Verdict

**Quote from Comprehensive Audit**:
> "Waft needs to **decide what it wants to be** and **ruthlessly cut everything else**. Right now it's a fascinating proof-of-concept that's too complex to maintain and too unfocused to recommend."
>
> **Grade: D+ → Potential B+ with focus**

## Tickets

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TKT-scope-001 | Define 3-sentence value proposition | open | CRITICAL |
| TKT-scope-002 | Consolidate two gamification systems into one | open | HIGH |
| TKT-scope-003 | Consolidate three task management systems | open | HIGH |
| TKT-scope-004 | Decide: Core vs Plugin architecture | open | HIGH |
| TKT-scope-005 | Reduce 29 commands to essential set (15 max) | open | HIGH |
| TKT-scope-006 | Create plugin system for optional features | open | MEDIUM |

## Key Questions (Must Answer)

### 1. What Problem Does Waft Solve?

**Current Answer**: Unclear
- Environment management? (uv already does this)
- Project scaffolding? (cookiecutter/copier do this)
- Gamification? (Unique, but is it the core?)
- All of the above? (Too broad)

**Required**: Clear, focused answer

### 2. Who Is The Target User?

**Current Answer**: Unclear
- Solo developers? (Don't need 29 commands)
- Teams? (Too quirky with RPG mechanics)
- Python beginners? (Too complex)
- Python experts? (Would they use this?)

**Required**: Specific persona(s)

### 3. What Is The Core Value?

**Current Answer**: Unclear
- The _pyrite memory structure?
- The gamification?
- The RPG mechanics?
- The integration layer?

**Required**: 1-2 core features that differentiate Waft

## Overlapping Systems (Must Consolidate)

### Gamification (2 Systems!)

| System | LOC | Features |
|--------|-----|----------|
| **GamificationManager** | 303 | Integrity, Insight, Level, Achievements |
| **TavernKeeper (RPG)** | 1,014 | STR/DEX/CON/INT/WIS/CHA, HP, d20 rolls, chronicles, quests |

**Question**: Why two? Pick one or integrate.

### Task Management (3 Systems!)

| System | LOC | Purpose |
|--------|-----|---------|
| **GoalManager** | 310 | Track goals, break into steps |
| **WorkflowManager** | 246 | Run command sequences |
| **ComposeManager** | 246 | Compose commands from natural language |

**Question**: Why three overlapping systems? Consolidate.

### Context Restoration (5 Commands!)

- `waft checkout`
- `waft resume`
- `waft continue`
- `waft proceed`
- `waft reflect`

**Question**: Do we need 5 commands that do similar things?

## Proposed Scope Options

### Option 1: Focused Meta-Framework

**Core**:
- Environment management (uv wrapper)
- Memory structure (_pyrite/)
- Simple gamification (integrity/insight only)
- Project scaffolding

**Plugin**:
- RPG mechanics (waft-tavern)
- Decision engine (waft-decide)
- Session analytics (waft-analytics)
- Empirica integration (waft-empirica)

**Commands**: ~12

### Option 2: Gamified Dev Tool

**Core**:
- Gamification (choose ONE system)
- Session tracking
- Project management
- Simple memory structure

**Plugin**:
- RPG mechanics (optional)
- Decision engine
- Advanced analytics

**Commands**: ~15

### Option 3: Current (Status Quo)

**Core**: Everything (29+ commands)

**Plugin**: Nothing

**Result**: Unmaintainable, unfocused, Grade D+

## Success Criteria

- [ ] **Value proposition** defined in 3 sentences or less
- [ ] **Target user** clearly identified
- [ ] **Core features** (< 5) identified
- [ ] **Plugin features** identified
- [ ] **Gamification** consolidated to ONE system
- [ ] **Task management** consolidated to ONE system
- [ ] **Commands** reduced to 15 or fewer
- [ ] **Architecture** supports core + plugins
- [ ] **Documentation** reflects new focus
- [ ] **Team alignment** on direction

## Decision Framework

For each feature, ask:

1. **Is this core to Waft's value proposition?**
   - YES → Keep in core
   - NO → Move to plugin or remove

2. **Would users use Waft if this was missing?**
   - YES → Essential, keep
   - NO → Nice-to-have, plugin or remove

3. **Does this overlap with another feature?**
   - YES → Consolidate or remove
   - NO → OK to keep (if passes #1 and #2)

4. **Does this add more complexity than value?**
   - YES → Remove or simplify
   - NO → OK to keep

## Impact Assessment

### Scenario: Choose Option 1 (Focused Meta-Framework)

**Before**:
- Commands: 29
- LOC: 12,731
- Gamification: 2 systems
- Task Management: 3 systems
- Focus: Unclear
- Grade: D+

**After**:
- Commands: ~12
- LOC: ~6,000 (core), ~6,000 (plugins)
- Gamification: 1 simple system (integrity/insight)
- Task Management: 1 system
- Focus: Clear
- Grade: B+

**Plugins Available**:
- `waft-tavern`: Full RPG mechanics (for those who want it)
- `waft-analytics`: Advanced session analytics
- `waft-decide`: Decision matrix engine
- `waft-empirica`: Empirica integration

**User Experience**:
```bash
# Minimal install (core only)
pip install waft

# With RPG mechanics
pip install waft[tavern]

# Full experience
pip install waft[all]
```

## Philosophy

**From Audit**:
> "Waft is simultaneously impressive and concerning. It needs to **decide what it wants to be** and **ruthlessly cut everything else**."

**Key Principle**: **Focus = Power**

Better to do 3-5 things excellently than 15 things mediocrely.

## Related

- Audit Report: "THE TAVERNKEEPER QUESTION"
- Audit Report: "Scope Explosion Evidence"
- Audit Finding: "Swiss Army Chainsaw" anti-pattern
- Audit Finding: "Second System Effect"

## Dependencies

- This work effort BLOCKS all feature work
- Must be decided before architecture refactoring completes
- Informs what tests need to be written

## Notes

This is the **most important work effort**. All other work is tactical. This is strategic.

Without answering "What is Waft?", we can't make good decisions about what to keep, what to remove, or what to build next.

The audit made it clear: Waft is suffering from severe scope creep. The path forward requires courage to cut features and focus on core value.

**Remember**: You can always add features later (as plugins). You can rarely recover from lack of focus.
