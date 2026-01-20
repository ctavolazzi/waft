---
id: TKT-sec1-003
parent: WE-260109-sec1
title: "Delete legacy web.py (546 lines dead code)"
status: completed
priority: HIGH
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: claude
completed: 2026-01-11T00:00:00.000Z
---

# TKT-sec1-003: Delete legacy web.py (546 lines dead code)

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-sec1
- **Author**: Claude Audit System
- **Priority**: HIGH
- **Estimated Effort**: 1 ticket (simple deletion + verification)

## Description

The file `src/waft/web.py` (546 lines) is legacy code that has been **completely replaced** by the FastAPI server in `src/waft/api/main.py`. Both servers run on port 8000, but only the FastAPI version is actively used.

## Evidence

### web.py (LEGACY - 546 lines)
```python
class WaftHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Waft web dashboard."""
    # Uses Python's built-in HTTPServer
    # Inline HTML generation
    # No API structure
```

### api/main.py (CURRENT - ~200 lines)
```python
app = FastAPI(title="Waft API", version="0.0.2")
# Modern REST API
# Separate routes files
# Pydantic models
```

## Problem Impact

**Severity**: HIGH ⚠️
- **Confusion**: Two web servers in codebase
- **Maintenance**: 546 lines that don't need to exist
- **Cognitive Load**: Contributors don't know which to use
- **Tech Debt**: Legacy patterns vs modern FastAPI

## Acceptance Criteria

- [x] `src/waft/web.py` deleted
- [x] No imports of `web.py` remain in codebase
- [x] `waft serve` command uses FastAPI only
- [x] All tests pass (especially web-related tests)
- [x] Documentation updated (if web.py was mentioned)

## Implementation Plan

### Step 1: Verify No Active Usage

Search for imports and usage:
```bash
grep -r "from.*web import" src/
grep -r "import.*web" src/
grep -r "web\.serve" src/
```

### Step 2: Check main.py Command

Verify `waft serve` command uses FastAPI:
```python
# src/waft/main.py
@app.command()
def serve(...):
    # Should use: from .api.main import app
    # NOT: from .web import serve
```

### Step 3: Delete File

```bash
git rm src/waft/web.py
```

### Step 4: Update Documentation

Check these files for references to web.py:
- README.md
- docs/
- _work_efforts/WEB_DASHBOARD.md

### Step 5: Verify Tests

```bash
pytest tests/ -v
waft verify
```

## Files to Change

**Delete**:
- `src/waft/web.py` (546 lines)

**Verify** (should NOT import web.py):
- `src/waft/main.py` (check serve command)
- `src/waft/__init__.py` (check exports)

**Update** (if referenced):
- Documentation files
- Tests

## Testing Strategy

1. **Grep Search**: Ensure no imports remain
2. **Run Tests**: All tests should pass
3. **Manual Test**: `waft serve` should work (using FastAPI)
4. **Verify Dashboard**: http://localhost:8000 should load

## Benefits of Removal

- ✅ **-546 LOC**: Significant code reduction
- ✅ **Clarity**: One obvious way to serve dashboard
- ✅ **Modern**: FastAPI is standard (async, OpenAPI, Pydantic)
- ✅ **Maintainability**: Less code to maintain

## Historical Context

From audit analysis:
- web.py created early in project (BaseHTTPRequestHandler)
- FastAPI implementation added later (api/main.py)
- Both serve on port 8000
- web.py has inline HTML generation
- FastAPI has proper separation (routes, models, frontend)

## Risks

**Low Risk** - If web.py is truly legacy:
- Simply delete and verify tests pass

**Medium Risk** - If web.py still used somewhere:
- Grep search will reveal usage
- Update those locations to use FastAPI

## Completion Summary

**Completed**: 2026-01-11

All acceptance criteria met:
1. ✅ Verified no imports of web.py in codebase (grep search returned no matches)
2. ✅ Confirmed `waft serve` command (main.py:614-683) uses only FastAPI from `.api.main`
3. ✅ Deleted `src/waft/web.py` using `git rm` (546 lines removed)
4. ✅ Verified no broken imports after deletion (grep confirmed clean)
5. ✅ All documentation references are in historical/audit docs only

**Impact**:
- Removed 546 lines of dead code
- Eliminated confusion between two web server implementations
- Reduced technical debt
- Simplified codebase maintenance

## Commits

- 2026-01-11: Delete legacy web.py (546 lines dead code)
