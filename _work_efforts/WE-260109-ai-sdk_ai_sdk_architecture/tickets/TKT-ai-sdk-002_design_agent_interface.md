---
id: TKT-ai-sdk-002
parent: WE-260109-ai-sdk
title: "Design Agent base class and interface"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
depends_on: [TKT-ai-sdk-001]
---

# TKT-ai-sdk-002: Design Agent base class and interface

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-ai-sdk
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 3 tickets
- **Depends On**: TKT-ai-sdk-001 (vision document)

## Problem Statement

There's no Agent base class or interface for AI agents to use Waft. The codebase has CrewAI templates but no Waft-native agent interface.

**Current State**:
- ✅ CrewAI templates exist (`src/agents.py` in projects)
- ❌ No Waft Agent base class
- ❌ No agent lifecycle management
- ❌ No integration with Waft's decision engine, analytics, or gamification

## Acceptance Criteria

- [ ] Agent base class designed (`src/waft/core/agent.py`)
- [ ] Agent lifecycle defined (observe, decide, act, reflect)
- [ ] Integration with decision engine
- [ ] Integration with session analytics
- [ ] Integration with TavernKeeper (personality)
- [ ] Integration with Empirica (epistemic tracking)
- [ ] Example agent implementation
- [ ] Documentation complete

## Design Requirements

### Agent Interface

```python
class WaftAgent:
    """Base class for self-modifying AI agents."""
    
    def observe(self) -> ProjectState:
        """Observe current project state."""
        pass
    
    def decide(self, state: ProjectState) -> Decision:
        """Make decision using decision engine."""
        pass
    
    def act(self, decision: Decision) -> ActionResult:
        """Execute action (potentially modifying code)."""
        pass
    
    def reflect(self, result: ActionResult) -> Reflection:
        """Reflect on outcome and learn."""
        pass
    
    def run_cycle(self):
        """Execute one observe-decide-act-reflect cycle."""
        pass
```

### Integration Points

1. **Decision Engine**: Agents use `DecisionMatrix` for reasoning
2. **Session Analytics**: Agents log actions for learning
3. **TavernKeeper**: Agents have personality (ability scores, chronicles)
4. **Empirica**: Agents track epistemic state
5. **Gamification**: Agents earn insight/integrity

## Implementation Steps

1. **Design Phase**
   - Design Agent base class interface
   - Define lifecycle methods
   - Design integration points
   - Design state management

2. **Implementation Phase**
   - Implement base class
   - Implement lifecycle methods
   - Integrate with existing systems
   - Add error handling

3. **Example Phase**
   - Create example agent (e.g., `RefactorAgent`)
   - Demonstrate usage
   - Write tests

4. **Documentation Phase**
   - Document Agent interface
   - Document lifecycle
   - Document integration points
   - Create usage examples

## Deliverables

- `src/waft/core/agent.py` - Agent base class
- `src/waft/core/agent_example.py` - Example implementation
- `docs/AGENT_INTERFACE.md` - Documentation
- Tests for Agent class

## Dependencies

- TKT-ai-sdk-001 (vision document must exist first)

## Notes

This is the foundation for all agent implementations. Design carefully - changes here will affect all agents.
