---
id: WE-260109-arch
title: "Architecture Refactoring"
status: open
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
last_updated: 2026-01-09T00:00:00.000Z
branch: claude/explore-waft-UugBV
repository: waft
---

# WE-260109-arch: Architecture Refactoring

## Metadata
- **Created**: Thursday, January 9, 2026
- **Author**: Claude Audit System
- **Repository**: waft
- **Branch**: claude/explore-waft-UugBV
- **Priority**: HIGH

## Objective

Refactor core architecture to improve maintainability, testability, and reduce technical debt. Primary focus: break up the 1,957-line main.py monolith and remove code duplication.

## Audit Context

Comprehensive audit revealed severe architecture debt:
- **main.py**: 1,957 lines (single file)
- **29+ commands** in one file
- **Duplicated code**: Moon phase calculation repeated 3+ times
- **Magic numbers**: Insight/integrity values hardcoded everywhere
- **No logging system**: print() statements throughout library code
- **Inconsistent error handling**: bool returns, exceptions, silent failures

## Tickets

| ID | Title | Status | Priority | Effort |
|----|-------|--------|----------|--------|
| TKT-arch-001 | Split main.py into command modules | open | HIGH | 3 |
| TKT-arch-002 | Extract and centralize moon phase calculation | open | MEDIUM | 1 |
| TKT-arch-003 | Create constants module for magic numbers | open | MEDIUM | 1 |
| TKT-arch-004 | Implement centralized logging system | open | HIGH | 2 |
| TKT-arch-005 | Standardize error handling patterns | open | MEDIUM | 2 |
| TKT-arch-006 | Replace print() with logging in library code | open | HIGH | 2 |

## Problem Statement

### Current Architecture Issues

**1. main.py Monolith** (1,957 lines):
- Single Responsibility Principle violated
- Hard to navigate and understand
- Difficult to test individual commands
- High cognitive load for contributors

**2. Code Duplication**:
- Moon phase calculation: 3+ occurrences
- Integrity checks: Repeated patterns
- Error handling: Inconsistent patterns

**3. No Logging Infrastructure**:
- `print()` used throughout
- No debug levels
- No log rotation
- No structured logging

**4. Magic Numbers Everywhere**:
```python
gamification.award_insight(50.0, reason="...")  # Why 50?
gamification.award_insight(10.0, reason="...")  # Why 10?
gamification.damage_integrity(10.0, reason="...") # Why 10?
```

## Success Criteria

- [ ] main.py split into < 500 lines per file
- [ ] Commands organized by domain (project, empirica, gamification, etc.)
- [ ] Zero code duplication (DRY principle)
- [ ] All magic numbers replaced with named constants
- [ ] Centralized logging system implemented
- [ ] Zero print() statements in library code (CLI output OK)
- [ ] Consistent error handling across all modules
- [ ] All existing tests pass
- [ ] Test coverage increases by 10%+

## Architecture Vision

### Proposed Structure

```
src/waft/
├── main.py                    # CLI entry point (< 200 lines)
├── commands/                  # Command modules
│   ├── __init__.py
│   ├── project.py            # new, init, verify, info
│   ├── empirica.py           # session, finding, unknown, check, assess
│   ├── gamification.py       # stats, level, achievements, dashboard
│   ├── tavern.py             # character, chronicle, roll, quests
│   ├── analytics.py          # analytics sessions/trends
│   └── decision.py           # decide
├── core/                      # Business logic (unchanged)
│   ├── ...
├── constants.py              # Named constants
├── logging_config.py         # Logging setup
└── utils/                    # Shared utilities
    ├── moon_phase.py         # Moon phase calculation
    ├── error_handling.py     # Standard error patterns
    └── ...
```

### Benefits

1. **Maintainability**: Smaller files, clearer organization
2. **Testability**: Each command module independently testable
3. **Discoverability**: New contributors can find code easily
4. **Modularity**: Commands can be enabled/disabled
5. **Debugging**: Proper logging makes issues traceable
6. **Consistency**: Standard patterns across codebase

## Impact Assessment

**Before**:
- main.py: 1,957 lines
- Commands: All in one file
- Logging: print() everywhere
- Constants: Magic numbers
- Duplication: High

**After**:
- main.py: < 200 lines
- Commands: ~300 lines each, 6 files
- Logging: Structured, configurable
- Constants: Named, documented
- Duplication: None

**Code Quality Improvement**: +2 letter grades (D+ → B-)

## Dependencies

- No blocking dependencies
- Can be done in parallel with security fixes (WE-260109-sec1)
- Should be done before feature work continues

## Related

- Audit Report: "Architecture Debt" section
- Previous: WE-260107-3x3c (debug code cleanup - similar spirit)
- Pattern: Follow separation of concerns principle

## Notes

This refactoring is essential for long-term maintainability. The current architecture doesn't scale beyond ~30 commands, and we're already there. Breaking up main.py will make all future work easier.

The goal is NOT to change functionality, but to reorganize code for clarity and maintainability. All existing tests should pass without modification after refactoring.
