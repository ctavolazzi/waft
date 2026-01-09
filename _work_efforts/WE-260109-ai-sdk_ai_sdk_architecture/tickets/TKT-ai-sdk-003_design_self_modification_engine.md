---
id: TKT-ai-sdk-003
parent: WE-260109-ai-sdk
title: "Design self-modification engine for safe code changes"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
depends_on: [TKT-ai-sdk-001, TKT-ai-sdk-002]
---

# TKT-ai-sdk-003: Design self-modification engine for safe code changes

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-ai-sdk
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 5 tickets (complex, safety-critical)
- **Depends On**: TKT-ai-sdk-001, TKT-ai-sdk-002

## Problem Statement

Agents need to modify code safely, but there's no self-modification engine. This is the core capability that makes Waft a "self-modifying" SDK.

**Current State**:
- ❌ No code modification capabilities
- ❌ No safety constraints
- ❌ No rollback mechanism
- ❌ No validation system

## Acceptance Criteria

- [ ] Self-modification engine designed (`src/waft/core/self_mod.py`)
- [ ] Safety constraints defined (what can be modified, what can't)
- [ ] Rollback mechanism implemented
- [ ] Validation system (syntax, tests, etc.)
- [ ] Approval workflow (for risky changes)
- [ ] Change tracking (git integration)
- [ ] Example modifications (add function, refactor, etc.)
- [ ] Documentation complete

## Design Requirements

### Safety Model

**Allowed Modifications** (no approval):
- Add new functions/methods
- Add new files
- Update comments/docstrings
- Format code (black, ruff)

**Requires Approval**:
- Delete functions/files
- Modify existing function signatures
- Change imports
- Modify core framework code

**Forbidden**:
- Delete entire files
- Modify git history
- Modify system files outside project

### Modification Engine

```python
class SelfModificationEngine:
    """Safe code modification engine."""
    
    def modify_code(
        self,
        file_path: Path,
        modification: Modification,
        safety_level: SafetyLevel
    ) -> ModificationResult:
        """Apply code modification with safety checks."""
        pass
    
    def validate_modification(
        self,
        modification: Modification
    ) -> ValidationResult:
        """Validate modification before applying."""
        pass
    
    def rollback(
        self,
        modification_id: str
    ) -> RollbackResult:
        """Rollback a modification."""
        pass
```

### Integration Points

1. **Git**: Track all modifications in git
2. **Tests**: Run tests before/after modification
3. **Linting**: Validate syntax
4. **Decision Engine**: Use for approval decisions
5. **Session Analytics**: Log all modifications

## Implementation Steps

1. **Design Phase**
   - Design safety model
   - Design modification engine interface
   - Design validation system
   - Design rollback mechanism

2. **Implementation Phase**
   - Implement modification engine
   - Implement safety constraints
   - Implement validation
   - Implement rollback
   - Integrate with git

3. **Testing Phase**
   - Test safe modifications
   - Test approval workflow
   - Test rollback
   - Test edge cases

4. **Documentation Phase**
   - Document safety model
   - Document modification engine
   - Document usage examples
   - Document best practices

## Deliverables

- `src/waft/core/self_mod.py` - Self-modification engine
- `src/waft/core/safety.py` - Safety constraints
- `docs/SELF_MODIFICATION.md` - Documentation
- Tests for modification engine

## Dependencies

- TKT-ai-sdk-001 (vision document)
- TKT-ai-sdk-002 (agent interface)
- WE-260109-sec1 (security fixes - CRITICAL for this)

## Notes

**CRITICAL**: This is safety-critical code. Agents modifying code could break projects. Design carefully with extensive validation and rollback capabilities.

**Security**: Must address all security concerns from WE-260109-sec1 before implementing.
