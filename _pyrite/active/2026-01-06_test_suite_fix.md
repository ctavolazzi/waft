# Test Suite Fix

**Date**: 2026-01-06
**Issue**: 5 test errors in `full_waft_project` fixture

## Problem

The `full_waft_project` fixture in `tests/conftest.py` was creating `.github/workflows/ci.yml` as a directory, then trying to write to it as a file, causing `IsADirectoryError`.

## Root Cause

```python
# WRONG - creates ci.yml as a directory
(temp_project_path / ".github" / "workflows" / "ci.yml").mkdir(parents=True)
(temp_project_path / ".github" / "workflows" / "ci.yml").write_text("# CI workflow")
```

## Fix

```python
# CORRECT - create parent directory, then write file
(temp_project_path / ".github" / "workflows").mkdir(parents=True)
(temp_project_path / ".github" / "workflows" / "ci.yml").write_text("# CI workflow")
```

Same fix applied to `src/agents.py` path.

## Result

- ✅ All 40 tests now passing
- ✅ Fixed 5 errors in fixture setup
- ✅ Verified with `waft verify` and `waft info`

## Files Changed

- `tests/conftest.py` - Fixed `full_waft_project` fixture


