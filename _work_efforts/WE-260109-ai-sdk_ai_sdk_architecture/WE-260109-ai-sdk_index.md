---
id: WE-260109-ai-sdk
title: "AI SDK Architecture & Vision Alignment"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
last_updated: 2026-01-09T00:00:00.000Z
branch: main
repository: waft
---

# WE-260109-ai-sdk: AI SDK Architecture & Vision Alignment

## Metadata
- **Created**: Thursday, January 9, 2026
- **Author**: Claude Audit System
- **Repository**: waft
- **Branch**: main
- **Priority**: CRITICAL

## Executive Summary

**CRITICAL REVELATION**: Waft is intended to become a **self-modifying AI SDK**, not just a Python meta-framework. This completely reframes the entire codebase audit.

### The Gap

**Current State**: 
- ✅ Foundation built (80%) - substrate, memory, managers
- ✅ Intelligence layer built (60%) - analytics, empirica, decision engine
- ✅ Personality layer built (90%) - TavernKeeper, gamification
- ❌ **Agent layer NOT built (0%)** ← THE CRITICAL GAP

**Vision**: Self-modifying AI SDK where agents can:
- Observe project state
- Make decisions using the decision engine
- Modify code safely
- Learn from experience
- Adapt behavior over time

## Component Reinterpretation

| Component | Audit Initially Saw | AI SDK Reality | Status |
|-----------|---------------------|----------------|--------|
| `_pyrite/` structure | File organization | Agent persistent memory | ✅ Built |
| Session analytics (473 LOC) | Unnecessary complexity | Training data pipeline | ✅ Built (data collection) |
| Empirica integration | Unclear dependency | Epistemic state tracking | ✅ Built |
| Decision matrix (800 LOC) | Over-engineered | AI reasoning framework | ✅ Built |
| TavernKeeper (1,014 LOC) | Scope creep | Agent personality engine | ✅ Built |
| 2 gamification systems | Redundant | Dual reward signals | ✅ Built |
| 5 context commands | Too many | Context primitives | ✅ Built |
| 3 task systems | Overlapping | Planning hierarchy | ✅ Built |
| **Agent Interface** | **Missing** | **Base Agent class** | ❌ **NOT BUILT** |
| **Self-Mod Engine** | **Missing** | **Code modification** | ❌ **NOT BUILT** |
| **Learning System** | **Missing** | **Adapt from experience** | ❌ **NOT BUILT** |

## The Real Problem

**Not**: "Too much scope"  
**But**: "Missing the core AI agent layer"

All the infrastructure is there, but there's no:
1. **Agent base class** - No way for AI agents to use Waft
2. **Self-modification engine** - No safe code modification capabilities
3. **Learning system** - No adaptation from experience (session analytics collects but doesn't learn)
4. **Safety constraints** - No validation for self-modification
5. **Examples** - No concrete agent implementations

## Work Effort Scope

This work effort will:
1. Define the AI SDK vision document (what "self-modifying" means)
2. Design the Agent interface (base class, lifecycle, capabilities)
3. Design the self-modification engine (safe code changes, rollback)
4. Design the learning system (how agents adapt from experience)
5. Map existing components to AI SDK roles
6. Identify implementation gaps
7. Create roadmap to v1.0

## Success Criteria

- [ ] Vision document written and approved
- [ ] Agent interface designed and documented
- [ ] Self-modification engine architecture designed
- [ ] Learning system architecture designed
- [ ] Component mapping complete
- [ ] Gap analysis complete
- [ ] Implementation roadmap created

## Related Work Efforts

- **WE-260109-sec1**: Security fixes (CRITICAL for AI agents executing code)
- **WE-260109-arch**: Architecture refactoring (organize for agent primitives)
- **WE-260109-scope**: Scope definition (reframed by AI SDK vision)

## Notes

This work effort BLOCKS all other strategic work. Without the AI SDK vision document, features continue to look like scope creep when they're actually foundational AI SDK components.

**Key Question**: What does "self-modifying" mean specifically?
- Code generation/modification?
- Parameter tuning?
- Prompt evolution?
- Architecture changes?
- All of the above?

**Answer Required**: Before proceeding with implementation.
