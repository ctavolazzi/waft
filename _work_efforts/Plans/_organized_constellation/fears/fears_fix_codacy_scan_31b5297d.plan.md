---
category: fears
confidence: 0.40
constellation_date: 2026-01-14
original_file: fix_codacy_scan_31b5297d.plan.md
---

# Fix Codacy Security Scan Failure

## Problem

The Codacy Security Scan GitHub Action fails with `java.nio.charset.MalformedInputException` because binary files (`.woff2` fonts, `.ico` icons) in the committed `.next/` build directory cannot be read as UTF-8.

## Solution

Remove build artifacts from git tracking and add defensive exclusions.

## Files to Modify

### 1. Update `.gitignore`

Add entries to prevent future commits of build artifacts:

```javascript
# Build outputs
**/.next/
**/node_modules/
**/venv/
**/.venv/

# Binary files that shouldn't be tracked
*.woff2
*.ico
```



### 2. Create `.codacy.yml`

Add at repo root for defense-in-depth:

```yaml
exclude_paths:
    - "archive/**"
    - "**/.next/**"
    - "**/node_modules/**"
    - "**/venv/**"
    - "**/*.woff2"
    - "**/*.ico"
    - "**/*.map"
```



### 3. Remove tracked build artifacts from git

Files to untrack (not delete locally):

- `archive/NovaSystem-Streamlined-root-20251207/novasystem_modern_ui/.next/` (contains 8 binary files causing the error)
- `archive/NovaSystem-Streamlined-root-20251207/venv/`
- `archive/nova-mvp-root-20251207/backend/venv/`

Commands:

```bash
git rm -r --cached archive/NovaSystem-Streamlined-root-20251207/novasystem_modern_ui/.next/
git rm -r --cached archive/NovaSystem-Streamlined-root-20251207/venv/
git rm -r --cached archive/nova-mvp-root-20251207/backend/venv/
```



### 4. Commit locally

```bash
git add .gitignore .codacy.yml
git commit -m "fix: remove build artifacts causing Codacy scan failure"
```