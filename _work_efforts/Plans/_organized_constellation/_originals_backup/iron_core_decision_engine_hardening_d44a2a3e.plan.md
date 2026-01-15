---
name: Iron Core Decision Engine Hardening
overview: Replace existing decision_matrix.py with hardened "Iron Core" version featuring "Diamond Plating" security fixes (strict validation, immutable structures, deterministic tie-breaking), and create comprehensive security tests. Execute rampup sequence for project orientation.
todos:
  - id: rampup-proceed
    content: Execute /proceed - Verify context and assumptions for rampup sequence
    status: completed
  - id: rampup-spinup
    content: Execute /spin-up - Quick project orientation
    status: completed
  - id: rampup-analyze
    content: Execute /analyze - Initial project analysis
    status: completed
  - id: rampup-phase1
    content: Execute /phase1 - Comprehensive data gathering
    status: completed
  - id: rampup-prepare
    content: Execute /prepare - Prepare for implementation phase
    status: completed
  - id: backup-check
    content: Verify backup exists (decision_matrix_v1_backup.py)
    status: completed
  - id: replace-decision-matrix
    content: Replace src/waft/core/decision_matrix.py with hardened Iron Core version
    status: completed
  - id: replace-test-core
    content: Replace tests/test_core.py with new security test suite
    status: completed
  - id: fix-import-path
    content: Fix import path in test_core.py (use waft.core.decision_matrix not src.waft.core.decision_matrix)
    status: completed
  - id: verify-breaking-changes
    content: Document breaking changes in decision_cli.py (WPM removal, get_detailed_scores signature change)
    status: completed
  - id: run-tests
    content: Run pytest tests/test_core.py to verify security tests pass
    status: completed
  - id: rampup-recap
    content: Execute /recap - Session summary
    status: completed
---

# Iron Core Decision Engine Hardening Plan

## Overview

Replace `src/waft/core/decision_matrix.py` with hardened version featuring:

- **Diamond Plating Security**: Negative weight validation, NaN/Inf detection, strict 1e-6 tolerance
- **Immutable Data Structures**: All dataclasses frozen
- **Deterministic Tie-Breaking**: Alphabetical secondary sort
- **Comprehensive Security Tests**: New test suite in `tests/test_core.py`

## Execution Sequence

### Phase 1: Rampup (Project Orientation)

1. **Proceed** - Verify context and assumptions
2. **Spin-up** - Quick project orientation
3. **Analyze** - Initial project analysis
4. **Phase1** - Comprehensive data gathering
5. **Prepare** - Prepare for implementation phase
6. **Recap** - Session summary

### Phase 2: File Replacement

1. **Backup existing file** (for reference)

   - Create backup: `src/waft/core/decision_matrix_v1_backup.py` already exists
   - Current version will be overwritten

2. **Replace `src/waft/core/decision_matrix.py`**

   - Overwrite with new hardened implementation
   - Key changes:
     - Removed `calculate_wpm()` method (breaking change)
     - Changed `get_detailed_scores()` signature (breaking change)
     - Added negative weight validation
     - Added NaN/Inf validation
     - Stricter tolerance (1e-6 vs 1e-5)
     - Deterministic tie-breaking with alphabetical sort

3. **Create/Replace `tests/test_core.py`**

   - Replace existing test file with new security-focused tests
   - Fix import path: Use `from waft.core.decision_matrix` (not `from src.waft.core.decision_matrix`)

### Phase 3: Breaking Changes Resolution

**⚠️ BREAKING CHANGES DETECTED:**

The new `decision_matrix.py` removes methods used by `decision_cli.py`:

- `calculate_wpm()` - Used in lines 94 and 237 of `decision_cli.py`
- `get_detailed_scores(alternative_name)` - Changed signature, used in line 186

**Options:**

1. Update `decision_cli.py` to remove WPM support (recommended if WPM not needed)
2. Add WPM back to hardened version (if WPM is required)
3. Leave as-is and document breaking change (tests will fail)

**Decision needed:** Should we update `decision_cli.py` to match the new API, or add WPM back?

### Phase 4: Verification

1. Run existing tests: `pytest tests/test_core.py`
2. Verify security tests pass:

   - `test_reject_negative_weights()`
   - `test_reject_nan_scores()`
   - `test_reject_loose_tolerance()`
   - `test_deterministic_tie_breaking()`

3. Check for import errors in dependent files
4. Update documentation if needed

## Files to Modify

### Primary Files

- `src/waft/core/decision_matrix.py` - **REPLACE** with hardened version
- `tests/test_core.py` - **REPLACE** with security test suite

### Potentially Affected Files (Breaking Changes)

- `src/waft/core/decision_cli.py` - Uses removed/changed methods
  - Line 94: `calculator.calculate_wpm()`
  - Line 186: `calculator.get_detailed_scores(alt_name)`
  - Line 237: `adjusted_calc.calculate_wpm()`

## Security Enhancements (Diamond Plating)

1. **Negative Weight Prevention**
   ```python
   if c.weight < 0:
       raise ValueError(f"Criterion '{c.name}' has negative weight...")
   ```

2. **NaN/Inf Detection**
   ```python
   if not math.isfinite(c.weight):
       raise ValueError(f"Criterion '{c.name}' has invalid weight...")
   ```

3. **Strict Tolerance**
   ```python
   if not math.isclose(total_weight, 1.0, abs_tol=1e-6):
       raise ValueError(...)
   ```

4. **Deterministic Tie-Breaking**
   ```python
   sorted_items = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
   ```


## Test Coverage

New security tests verify:

- ✅ Negative weights are rejected
- ✅ NaN scores are rejected
- ✅ Loose tolerance (0.99) is rejected
- ✅ Deterministic tie-breaking (alphabetical)
- ✅ WSM calculation correctness

## Next Steps After Implementation

1. Resolve breaking changes in `decision_cli.py`
2. Run full test suite
3. Update documentation if API changes
4. Verify all dependent code works with new version