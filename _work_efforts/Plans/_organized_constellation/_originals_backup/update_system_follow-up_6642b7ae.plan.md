---
name: Update System Follow-up
overview: Add integration tests for the full update workflow and create user documentation for the cursor-coding-protocols update system, tracked via _pyrite work effort.
todos:
  - id: work-effort
    content: Create work effort 10.02 in _pyrite for tracking
    status: pending
  - id: integration-tests
    content: Create update-workflow.test.js with 9 integration test scenarios
    status: pending
  - id: run-tests
    content: Run integration tests and verify they pass
    status: pending
  - id: user-docs
    content: Create docs/user-guide-updates.md with commands, scenarios, troubleshooting
    status: pending
  - id: finalize
    content: Update work effort, devlog, commit and push both repos
    status: pending
---

# Update System Follow-up: Integration Tests and User Docs

## Context

The cursor-coding-protocols update system has:

- CLI interface: [scripts/cursor-protocols-cli.js](cursor-coding-protocols/scripts/cursor-protocols-cli.js)
- Component tests: [tests/update-system.test.js](cursor-coding-protocols/tests/update-system.test.js) (17 tests)
- Missing: Full workflow integration tests and end-user documentation

## Part 1: Integration Tests

### Goal

Test the complete update workflow as a user would experience it via CLI.

### New Test File

Create `tests/update-workflow.test.js` with these scenarios:

```javascript
┌─────────────────────────────────────────────────────────┐
│ Integration Test Scenarios                              │
├─────────────────────────────────────────────────────────┤
│ 1. Check → reports current version                      │
│ 2. Check → finds available update                       │
│ 3. Check → JSON output format                           │
│ 4. Install → creates backup before update               │
│ 5. Install → downloads and extracts release             │
│ 6. Install → verifies installation                      │
│ 7. Rollback → lists available backups                   │
│ 8. Rollback → restores specific backup                  │
│ 9. Full cycle: check → install → verify → rollback      │
└─────────────────────────────────────────────────────────┘
```



### Implementation Approach

- Use isolated sandbox (like existing tests)
- Test via CLI invocation (not direct class calls)
- Mock GitHub API for deterministic results
- Verify file system state at each step

## Part 2: User Documentation

### Goal

Create user-friendly docs explaining how to use the update system.

### New File

Create `docs/user-guide-updates.md` in cursor-coding-protocols:

```markdown
# Update System User Guide

## Quick Start
- Check: `node scripts/cursor-protocols-cli.js update check`
- Install: `node scripts/cursor-protocols-cli.js update install`
- Rollback: `node scripts/cursor-protocols-cli.js update rollback`

## Commands Reference
[detailed command documentation]

## Common Scenarios
- First-time setup
- Updating to latest
- Rolling back after issues
- Offline usage

## Troubleshooting
- Network errors
- Permission issues
- Backup recovery
```



## Part 3: Work Effort Tracking

Create work effort in `_pyrite`:

- Path: `_work_efforts/10-19_development/10_active/10.02_update-system-followup.md`
- Update devlog with progress

## File Changes Summary

| Location | File | Action ||----------|------|--------|| cursor-coding-protocols | `tests/update-workflow.test.js` | Create || cursor-coding-protocols | `docs/user-guide-updates.md` | Create || _pyrite | `_work_efforts/.../10.02_update-system-followup.md` | Create || _pyrite | `_work_efforts/devlog.md` | Update |

## Execution Order - Standard GitHub Workflow

### Phase 1: _pyrite (Work Effort Tracking)

```bash
cd /Users/ctavolazzi/Code/_pyrite
git checkout -b feature/update-system-followup
```



1. Create work effort file: `10.02_update-system-followup.md`
2. Update `devlog.md` with new entry
3. Commit and push:
   ```bash
      git add -A
      git commit -m "Add work effort: update system follow-up"
      git push -u origin feature/update-system-followup
   ```




4. Create PR: `gh pr create`

### Phase 2: cursor-coding-protocols (Tests and Docs)

```bash
cd /Users/ctavolazzi/Code/cursor-coding-protocols
git checkout -b feature/update-workflow-tests
```



1. Create `tests/update-workflow.test.js`
2. Run tests to verify they pass
3. Create `docs/user-guide-updates.md`
4. Commit and push:
   ```bash
      git add -A
      git commit -m "Add update workflow integration tests and user docs"
      git push -u origin feature/update-workflow-tests
   ```




5. Create PR: `gh pr create`

### Phase 3: Finalize

1. Merge PRs (after review)
2. Update _pyrite work effort status to completed