---
name: Deploy Script Setup
overview: Create a quick deploy script with pre-deployment checks, then push current changes and deploy to Cloudflare Pages.
todos:
  - id: commit-changes
    content: Stage and commit current changes, push to origin
    status: completed
  - id: create-deploy-script
    content: Create scripts/deploy.js with pre-deployment checks
    status: pending
    dependencies:
      - commit-changes
  - id: update-package-json
    content: Add quick-deploy npm script to package.json
    status: pending
    dependencies:
      - create-deploy-script
  - id: run-deployment
    content: Execute the deploy script to deploy to Cloudflare
    status: completed
    dependencies:
      - update-package-json

category: hopes
confidence: 0.83
constellation_date: 2026-01-14
---

# Quick Deploy Script and Cloudflare Deployment

## Current State

- Uncommitted changes: modified `_work_efforts_/00-09_site_improvements/00_ui_ux/00.00_index.md`, `dist/images/team/christopher-badge.webp`
- Untracked: `_work_efforts/`, `src/.DS_Store`, `src/images/`
- Existing deployment: `npm run deploy` runs build + `wrangler pages deploy dist --project-name fogsift`

## Plan

### Step 1: Commit Current Changes

Stage and commit the pending changes before proceeding:

```bash
git add -A
git commit -m "chore: update work efforts and team badge"
git push origin main
```



### Step 2: Create Deploy Script

Create [`scripts/deploy.js`](scripts/deploy.js) with the following pre-deployment checks:

1. **Clean git check** - Fail if uncommitted changes exist
2. **Version bump warning** - Compare current version to last deployed (warns only)
3. **Build execution** - Run `build.js` and capture any errors
4. **Critical file verification** - Ensure `dist/index.html`, `dist/styles.css`, `dist/app.js` exist
5. **Deploy to Cloudflare** - Run `wrangler pages deploy`

### Step 3: Add npm Script

Update [`package.json`](package.json) to add:

```json
"quick-deploy": "node scripts/deploy.js"
```



### Step 4: Deploy to Cloudflare

After creating the script, run it to deploy the current version.

## Script Flow Diagram

```mermaid
flowchart TD
    Start[npm run quick-deploy] --> GitCheck{Uncommitted changes?}
    GitCheck -->|Yes| Fail[Exit with error]
    GitCheck -->|No| VersionCheck{Version bumped since last deploy?}
    VersionCheck -->|No| Warn[Print warning]
    VersionCheck -->|Yes| Build
    Warn --> Build[Run build.js]
    Build --> BuildOK{Build success?}
    BuildOK -->|No| Fail
    BuildOK -->|Yes| FileCheck{Critical files exist?}
    FileCheck -->|No| Fail
    FileCheck -->|Yes| Deploy[wrangler pages deploy]
    Deploy --> Success[Print success + URL]


```