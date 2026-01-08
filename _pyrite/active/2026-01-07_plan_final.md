# Final Plan - Debug Code Cleanup

**Date**: 2026-01-07 16:06 PST
**Phase**: 5 - Finalize Plan
**Work Effort**: WE-260107-3x3c
**Status**: ✅ Finalized - Ready for Implementation

---

## Objective

Remove all debug logging code (63 occurrences) that writes to `.cursor/debug.log`. This includes `#region agent log` blocks in:
- `src/waft/ui/dashboard.py` - 57 occurrences
- `src/waft/core/substrate.py` - 1 occurrence
- `src/waft/web.py` - 5 occurrences

**Goal**: Clean up code clutter, improve code quality, and remove unnecessary file I/O operations.

---

## Task Breakdown

### Ticket 1: Remove debug logging from dashboard.py
- **File**: `src/waft/ui/dashboard.py`
- **Occurrences**: 57
- **Pattern**: `# #region agent log` ... `# #endregion` blocks
- **Approach**: Remove all `#region agent log` blocks and their contents
- **Verification**: File parses correctly, no syntax errors
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 15 minutes

### Ticket 2: Remove debug logging from substrate.py
- **File**: `src/waft/core/substrate.py`
- **Occurrences**: 1
- **Pattern**: `# #region agent log` ... `# #endregion` block
- **Approach**: Remove the debug logging block (includes `import json` and `import inspect`)
- **Verification**: File parses correctly, imports removed automatically
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 5 minutes

### Ticket 3: Remove debug logging from web.py
- **File**: `src/waft/web.py`
- **Occurrences**: 5
- **Pattern**: `# #region agent log` ... `# #endregion` blocks
- **Approach**: Remove all `#region agent log` blocks
- **Note**: `json` and `time` imports at top are used legitimately elsewhere, keep them
- **Verification**: File parses correctly, no syntax errors
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 10 minutes

### Ticket 4: Verify cleanup and run tests
- **Actions**:
  1. Run `waft verify` to ensure structure is valid
  2. Run full test suite: `pytest tests/`
  3. Verify no `debug.log` references remain: `grep -r "debug.log" src/`
  4. Check for any remaining `#region agent log` blocks: `grep -r "#region agent log" src/`
  5. Check for hardcoded paths: `grep -r "/Users/ctavolazzi/Code/active/waft/.cursor/debug.log" src/`
  6. Verify no unused imports (especially in `substrate.py`)
- **Risk**: Low - verification only
- **Estimated Time**: 10 minutes

---

## Dependencies

- **None** - All tickets can be worked on independently
- **Order**: Tickets 1-3 can be done in any order, Ticket 4 must be last

---

## Success Criteria

1. ✅ All 63 debug logging occurrences removed
2. ✅ No references to `debug.log` remain in codebase
3. ✅ No hardcoded paths to `.cursor/debug.log` remain
4. ✅ All tests pass (40 tests)
5. ✅ `waft verify` passes
6. ✅ Code quality maintained (no functional changes)
7. ✅ No unused imports (especially `json` and `inspect` in `substrate.py`)

---

## Complexity Assessment

- **Overall Complexity**: Low
- **Technical Difficulty**: Trivial (find and remove)
- **Risk Level**: Low (debug code only)
- **Estimated Total Time**: 40 minutes

---

## Approach

1. **Systematic Removal**: Use search/replace to remove all `#region agent log` blocks
2. **Per-File Verification**: After each file, verify it still parses correctly
3. **Testing**: Run tests after all changes
4. **Final Check**: Comprehensive verification (debug.log references, hardcoded paths, unused imports)

---

## Implementation Notes

### Debug Code Pattern
All debug blocks follow this pattern:
```python
# #region agent log
with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
    f.write(...)
# #endregion
```

### Import Considerations
- **dashboard.py**: `time` import is used legitimately (for `time.sleep()`), keep it
- **web.py**: `json` and `time` imports are used legitimately, keep them
- **substrate.py**: `json` and `inspect` are only used in debug block, will be removed automatically

### Verification Commands
```bash
# Check for remaining debug.log references
grep -r "debug.log" src/

# Check for remaining #region blocks
grep -r "#region agent log" src/

# Check for hardcoded paths
grep -r "/Users/ctavolazzi/Code/active/waft/.cursor/debug.log" src/

# Run tests
pytest tests/

# Verify structure
waft verify
```

---

## Timeline

- **Ticket 1**: 15 minutes
- **Ticket 2**: 5 minutes
- **Ticket 3**: 10 minutes
- **Ticket 4**: 10 minutes
- **Total**: ~40 minutes

---

## Risk Mitigation

- **Low Risk**: Debug code only, not functional code
- **Safety Net**: Comprehensive test suite (40 tests)
- **Verification**: Multiple verification steps ensure nothing breaks
- **Rollback**: Git commits after each ticket for easy rollback if needed

---

**Status**: ✅ Finalized - Ready for Implementation (Phase 6: Begin)

