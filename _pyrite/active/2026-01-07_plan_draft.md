# Draft Plan - Debug Code Cleanup

**Date**: 2026-01-07 16:06 PST
**Phase**: 3 - Draft Plan
**Work Effort**: WE-260107-3x3c

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
- **Lines**: 434-437, 441-444, 449-452, 458-461, 463-466, 473-476, 481-484, 489-492, 496-499, 506-509, 513-516, 522-525, 528-531, 538-541, 554-557, 560-563, 566-569, 574-577, 579-582, 595-598
- **Approach**: Remove all `#region agent log` blocks and their contents
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 15 minutes

### Ticket 2: Remove debug logging from substrate.py
- **File**: `src/waft/core/substrate.py`
- **Occurrences**: 1
- **Pattern**: `# #region agent log` ... `# #endregion` block
- **Lines**: 26-32
- **Approach**: Remove the debug logging block
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 5 minutes

### Ticket 3: Remove debug logging from web.py
- **File**: `src/waft/web.py`
- **Occurrences**: 5
- **Pattern**: `# #region agent log` ... `# #endregion` blocks
- **Lines**: 26-30, 33-36, 38-41, 43-46
- **Approach**: Remove all `#region agent log` blocks
- **Risk**: Low - debug code only, not functional code
- **Estimated Time**: 10 minutes

### Ticket 4: Verify cleanup and run tests
- **Actions**:
  - Run `waft verify` to ensure structure is valid
  - Run full test suite: `pytest tests/`
  - Verify no `debug.log` references remain: `grep -r "debug.log" src/`
  - Check for any remaining `#region agent log` blocks
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
3. ✅ All tests pass (40 tests)
4. ✅ `waft verify` passes
5. ✅ Code quality maintained (no functional changes)

---

## Complexity Assessment

- **Overall Complexity**: Low
- **Technical Difficulty**: Trivial (find and remove)
- **Risk Level**: Low (debug code only)
- **Estimated Total Time**: 40 minutes

---

## Approach

1. **Systematic Removal**: Use search/replace to remove all `#region agent log` blocks
2. **Verification**: After each file, verify it still functions
3. **Testing**: Run tests after all changes
4. **Final Check**: Verify no debug.log references remain

---

## Notes

- Debug logging was added for development/debugging purposes
- All blocks follow the same pattern: `# #region agent log` ... `# #endregion`
- The debug.log file writes are not needed for production
- Removing this code will improve readability and reduce file I/O overhead

---

## Critique & Refinements

### Issues Identified

1. **Unused Imports** ⚠️
   - `substrate.py`: `import json` and `import inspect` are only used inside the debug block
   - These should be removed after debug block removal
   - `web.py` and `dashboard.py`: `json` and `time` are used legitimately elsewhere, keep imports

2. **Import Location** ⚠️
   - In `substrate.py`, `json` and `inspect` are imported inside the debug block (lines 27-28)
   - These will be automatically removed when the block is removed
   - No action needed - they're part of the debug block

3. **Verification Enhancement** ✅
   - Add check for unused imports after cleanup
   - Verify no hardcoded paths to `/Users/ctavolazzi/Code/active/waft/.cursor/debug.log` remain

### Plan Refinements

1. **After each file cleanup**:
   - Verify file still parses correctly (syntax check)
   - Check for any broken references

2. **Enhanced verification** (Ticket 4):
   - Check for unused imports: `ruff check --select F401` or manual review
   - Verify no hardcoded debug.log paths remain
   - Check for any remaining `#region agent log` patterns

### Assumptions Validated

- ✅ Debug code is not functional - safe to remove
- ✅ All blocks follow same pattern - easy to remove systematically
- ✅ No dependencies on debug.log file - safe to remove writes
- ✅ Tests will catch any issues - good safety net

### Gaps Addressed

- ✅ Added import cleanup check
- ✅ Added hardcoded path check
- ✅ Enhanced verification steps

---

**Status**: ✅ Critique Complete - Plan Refined and Ready for Finalization

