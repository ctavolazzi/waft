---
name: Fix CI Lock Sync
overview: Sync package-lock.json with package.json to fix the GitHub Actions CI failure, and create a work effort to document the fix.
todos:
  - id: work-effort
    content: Create work effort 30.01_ci_lockfile_sync.md in infrastructure
    status: completed
  - id: npm-install
    content: Run npm install to sync package-lock.json
    status: completed
  - id: devlog
    content: Update devlog with fix details
    status: completed
  - id: commit
    content: Commit and push changes
    status: completed

category: dreads
confidence: 0.70
constellation_date: 2026-01-14
---

# Fix CI Lock File Sync

## Problem

The GitHub Actions workflow (`playwright-e2e.yml`) fails because `npm ci` requires `package.json` and `package-lock.json` to be in sync. Errors show version mismatches like:

- `recma-jsx@0.3.0` in lock file vs `recma-jsx@1.0.1` required

## Solution: Clean Slate Regeneration

### 1. Create Work Effort

Create a new work effort at `_work_efforts/10-19_development/10_active/10.16_ci_lockfile_sync.md` to document this fix.

**Verified:** 10.16 is the next available number (10.13-10.15 already exist).

### 2. Delete Stale Dependencies

Remove both stale lock file AND node_modules for cleanest regeneration:

```bash
rm package-lock.json
rm -rf node_modules
```

**Verified:** node_modules exists (486 items), package-lock.json exists (379KB).

### 3. Regenerate Fresh Lock File

Install dependencies fresh to create a clean lock file:

```bash
npm install
```

### 4. Verify No Errors

Check for peer dependency warnings or errors in the npm output.

### 5. Update Devlog

Add entry to [`_docs/devlog/2025-12-14_devlog.md`](_docs/devlog/2025-12-14_devlog.md) documenting the fix.

### 6. Commit and Push

Commit the regenerated `package-lock.json` and work effort:

```bash
git add package-lock.json _work_efforts/ _docs/devlog/
git commit -m "fix: regenerate package-lock.json for CI compatibility"
git push
```

### 7. Verify CI

The next CI run should pass. The workflow at [`.github/workflows/playwright-e2e.yml`](.github/workflows/playwright-e2e.yml) will use `npm ci` successfully.

## Files Changed

- `package-lock.json` (deleted and regenerated)
- `node_modules/` (deleted and reinstalled - not committed)
- `_work_efforts/10-19_development/10_active/10.16_ci_lockfile_sync.md` (new)
- `_docs/devlog/2025-12-14_devlog.md` (updated)

## Verified Facts

- CI workflow uses `npm ci` (line 28 of `.github/workflows/playwright-e2e.yml`)
- Devlog `2025-12-14_devlog.md` exists
- Work effort number 10.16 is available (10.13-10.15 already taken)
- node_modules: 486 items
- package-lock.json: 379KB