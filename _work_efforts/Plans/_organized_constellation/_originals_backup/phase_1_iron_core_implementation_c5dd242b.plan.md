---
name: Phase 1 Iron Core Implementation
overview: Replace the existing 621-line decision_matrix.py with a simpler, test-driven implementation. Backup the existing file for future AHP/BWM harvesting, create the new Iron Core with WSM/WPM only, add comprehensive tests, and fix API compatibility issues.
todos:
  - id: backup-existing
    content: Rename decision_matrix.py to decision_matrix_v1_backup.py
    status: pending
  - id: create-iron-core
    content: Create new decision_matrix.py with simpler WSM/WPM implementation
    status: pending
  - id: fix-api-compat
    content: Update decision_cli.py to use Score.value instead of Score.score
    status: pending
  - id: check-workflow
    content: Verify workflow_decision.py compatibility
    status: pending
  - id: create-tests
    content: Create tests/test_core.py with provided test suite
    status: pending
  - id: fix-test-issues
    content: Fix any test issues (e.g., dummy matrix in test_ranking_logic)
    status: pending
  - id: run-tests
    content: Run pytest to verify all tests pass
    status: pending
---

# Phase 1: The Iron Core - Execution Plan

## Objective

Establish a trusted, test-verified mathematical foundation for the decision matrix calculator by replacing the complex existing implementation with a simpler, test-driven version.

## Steps

### 1. Backup Existing Implementation

- **File:** `src/waft/core/decision_matrix.py` → `src/waft/core/decision_matrix_v1_backup.py`
- **Reason:** Preserve AHP/BWM logic for Phase 4, maintain rollback capability
- **Action:** Rename file (no deletion)

### 2. Create New Iron Core

- **File:** `src/waft/core/decision_matrix.py` (new file)
- **Content:** Use the provided simpler implementation with:
- `Criterion` (frozen dataclass with weight validation)
- `Alternative` (frozen dataclass)
- `Score` (frozen dataclass with `value` field, not `score`)
- `DecisionMatrix` (container)
- `DecisionMatrixCalculator` (WSM/WPM only, strict validation)
- **Key differences from existing:**
- Uses `frozen=True` for immutability
- `Score.value` instead of `Score.score` (API change)
- Simpler validation (weights sum to 1.0 with `math.isclose`)
- WSM/WPM only (no AHP/BWM)
- Optimized lookup using dict maps

### 3. Fix API Compatibility

- **File:** `src/waft/core/decision_cli.py`
- **Issue:** Line 83 uses `Score(alt_name, crit_name, score_value)` which expects `score` field
- **Fix:** Update to use `value` field: `Score(alt_name, crit_name, score_value)` → `Score(alt_name, crit_name, score_value)` (field name change in Score dataclass)
- **Also check:** `workflow_decision.py` for any Score usage

### 4. Create Test Suite

- **File:** `tests/test_core.py` (new file)
- **Content:** Use provided test code with:
- `test_wsm_calculation` - Verify WSM math
- `test_validation_weights_must_sum_to_one` - Verify weight validation
- `test_validation_missing_score` - Verify completeness check
- `test_ranking_logic` - Verify ranking algorithm
- **Note:** The `test_ranking_logic` test may need adjustment since it creates a dummy matrix - we'll need to create a valid minimal matrix instead

### 5. Verify Implementation

- **Command:** `pytest tests/test_core.py -v`
- **Expected:** All tests pass (green)
- **If failures:** Fix issues before proceeding

## Files to Modify

1. **Rename:** `src/waft/core/decision_matrix.py` → `src/waft/core/decision_matrix_v1_backup.py`
2. **Create:** `src/waft/core/decision_matrix.py` (new simpler version)
3. **Update:** `src/waft/core/decision_cli.py` (fix Score field name: `score` → `value`)
4. **Check:** `src/waft/core/workflow_decision.py` (verify no direct Score usage)
5. **Create:** `tests/test_core.py` (new test file)

## API Compatibility Notes

The new `Score` dataclass uses `value` instead of `score`:

- **Old:** `Score(alt_name, crit_name, score_value)` → accesses `score_obj.score`
- **New:** `Score(alt_name, crit_name, score_value)` → accesses `score_obj.value`

This requires updating `decision_cli.py` line 83 and any code that accesses `score_obj.score`.

## Risk Mitigation

- **Backup preserved:** Original file renamed, not deleted
- **Tests first:** Verify math before integration
- **API fix:** Update dependent code immediately
- **Rollback:** Can restore from backup if needed

## Success Criteria

- ✅ All tests pass (`pytest tests/test_core.py`)
- ✅ No import errors in dependent modules
- ✅ `decision_cli.py` works with new API
- ✅ Backup file exists for future reference