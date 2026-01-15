---
name: Remove TinaCMS Fix Build
overview: Remove the broken TinaCMS integration to fix the build, eliminate 15 security vulnerabilities, and restore a working CI/CD pipeline.
todos:
  - id: uninstall-tinacms
    content: Run npm uninstall tinacms to remove dependency
    status: completed
  - id: update-scripts
    content: Update package.json dev/build scripts to Astro-only
    status: completed
  - id: delete-tina-dir
    content: Delete tina/ directory
    status: completed
  - id: remove-test
    content: Remove TinaCMS test from security-and-smoke.spec.ts
    status: completed
  - id: update-readme
    content: Remove TinaCMS references from README.md
    status: completed
  - id: update-developers
    content: Remove TinaCMS section from DEVELOPERS.md
    status: completed
  - id: update-devlog
    content: Add Session 6 to devlog documenting removal
    status: completed
  - id: verify-build
    content: Run npm run build to verify fix
    status: completed
  - id: verify-audit
    content: Run npm audit to confirm vulnerability reduction
    status: completed
  - id: git-commit
    content: Git add, commit with detailed message, push (no deploy)
    status: completed

category: dreads
confidence: 0.64
constellation_date: 2026-01-14
---

# Remove TinaCMS and Fix Build

## Problem

TinaCMS was added (Session 4) but never worked:
- CLI package `@tinacms/cli` was never installed
- `npm run build` fails with `tinacms: command not found`
- 15 security vulnerabilities (2 critical RCE, 11 high)
- Site works fine without it (`astro build` succeeds)

## Changes Required

### 1. Remove TinaCMS Dependency

```bash
npm uninstall tinacms
```

### 2. Update package.json Scripts

File: `package.json`

```json
// Before
"dev": "tinacms dev -c \"astro dev\"",
"build": "tinacms build && astro build",

// After
"dev": "astro dev",
"build": "astro build",
```

Keep `dev:astro` as an alias for backwards compatibility.

### 3. Delete TinaCMS Configuration

Delete directory: `tina/` (contains `config.ts`)

### 4. Remove TinaCMS Test

File: `tests/security-and-smoke.spec.ts`

Remove the test block at lines 49-65 that checks for TinaCMS admin SPA.

### 5. Update Documentation

File: `README.md`
- Update scripts table (lines 93-98) to remove TinaCMS references
- Remove "Content Management (TinaCMS)" section (lines 190-199)

File: `DEVELOPERS.md`
- Remove entire "Content Management System (TinaCMS)" section (lines 433-545)

### 6. Update Devlog

File: `_docs/devlog/2025-12-12_devlog.md`

Add Session 6 documenting TinaCMS removal with rationale.

## Verification

```bash
npm run build          # Should succeed
npm run test:unit      # Should pass (53 tests)
npm audit              # Should show 0 vulnerabilities (or significantly fewer)
```

## Git Commit

```bash
git add -A
git commit -m "chore: remove broken TinaCMS integration

- tinacms package removed (CLI was never installed, build failed)
- Eliminates 15 security vulnerabilities (2 critical, 11 high)
- Build/dev scripts reverted to Astro-only
- Documentation updated to reflect removal
- Test for TinaCMS admin removed

Site functions identically; TinaCMS was never operational."
git push
```