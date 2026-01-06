# Incremental Commits - Proper Workflow

**Date**: 2026-01-06
**Learning**: Using _pyrite and frequent commits during development

## What I Did Wrong Initially

- Made all changes without commits
- Updated tickets only at the end
- Documented work retroactively
- Didn't use waft commands during development

## What I Should Have Done (And Now Did)

### 1. After Fixing Bug (TKT-9a6i-001)
- ✅ Committed: `cd30afb` - "fix: duplicate Project Name bug in waft info"
- ✅ Updated ticket with commit hash
- ✅ Documented in _pyrite/active/

### 2. After Creating Test Infrastructure (TKT-9a6i-004)
- ✅ Committed: `31a6ade` - "test: add test infrastructure and fixtures"
- ✅ Updated ticket with commit hash

### 3. After Adding E2E Tests (TKT-9a6i-005)
- ✅ Committed: `f1c131c` - "test: add comprehensive end-to-end tests"
- ✅ Updated ticket with commit hash

### 4. After Adding Validation Functions (TKT-9a6i-006)
- ✅ Committed: `089d445` - "feat: add validation functions"
- ✅ Committed: `[next]` - "feat: integrate validation into commands"
- ✅ Updated ticket with commit hash

### 5. After Documentation Updates
- ✅ Committed: `da6007f` - "docs: enhance README"
- ✅ Committed: `94551a1` - "docs: update CHANGELOG"

### 6. After Creating Demo & Explore Command
- ✅ Committed: `0aa5da5` - "feat: add interactive demo script"
- ✅ Committed: `0ee65f9` - "feat: add explore command"

### 7. After Process Documentation
- ✅ Committed: `e80beb5` - "docs: add development workflow questions"
- ✅ Committed: `a2cb5ed` - "docs: document work in _pyrite/active/"

## Commit Summary

**10 commits** made, each focused on a logical unit:
1. Bug fix
2. Test infrastructure
3. E2E tests
4. Validation functions
5. Validation integration
6. README update
7. CHANGELOG update
8. Demo script
9. Explore command
10. Process docs + _pyrite documentation

## Key Learnings

1. **Small, focused commits** are better than one big commit
2. **Commit after each logical unit** of work
3. **Update tickets incrementally** with commit hashes
4. **Document in _pyrite/active/** as you work, not retroactively
5. **Use waft commands** during development to verify

## Going Forward

- Make commits after each ticket completion
- Update tickets with commit hashes immediately
- Document in _pyrite/active/ as I work
- Use waft verify/info/stats during development
- Follow the workflow: spin-up → explore → draft plan → critique → finalize → begin

