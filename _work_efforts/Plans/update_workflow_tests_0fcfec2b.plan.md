---
name: Update System User Docs
overview: Create user documentation for the cursor-coding-protocols update system (Stage 1 of 3). Tests deferred to Stage 2, GitHub infrastructure to Stage 3.
todos:
  - id: verify-cli
    content: Verify CLI commands work and document actual output
    status: completed
  - id: ccp-branch
    content: Create feature branch in cursor-coding-protocols
    status: completed
  - id: create-docs
    content: Create docs/user-guide-updates.md with prerequisites and commands
    status: completed
  - id: link-readme
    content: Add link to user guide from README.md and docs/README.md
    status: completed
  - id: ccp-commit
    content: Commit and push cursor-coding-protocols changes
    status: completed
  - id: ccp-pr
    content: Create PR for cursor-coding-protocols via gh CLI
    status: completed
  - id: pyrite-branch
    content: Create feature branch in _pyrite
    status: completed
  - id: pyrite-work-effort
    content: Create work effort 10.02 via MCP (fallback to direct)
    status: completed
  - id: pyrite-devlog
    content: Update _pyrite devlog
    status: completed
  - id: memory-track
    content: Track project in user-memory knowledge graph
    status: completed
  - id: mcp-docs
    content: Create MCP-IMAGE-WORKFLOW.md in 3 locations
    status: completed
  - id: pyrite-commit
    content: Commit and push _pyrite changes
    status: completed
  - id: pyrite-pr
    content: Create PR for _pyrite via gh CLI
    status: completed
---

# 3-Stage Plan Overview

## Why 3 Stages?

Original plan had critical issues identified in review:

1. Integration tests require code changes to `update-installer.js` (no injection points for mocking)
2. GitHub infrastructure is scope creep (separate initiative)
3. CLI output didn't match documented scenarios

**Stage 1 (Current):** Documentation only - no code changes**Stage 2 (Future):** Testing infrastructure - requires code refactoring**Stage 3 (Future):** GitHub infrastructure for _pyrite - separate initiative---

# Stage 1: Update System User Documentation

## Scope

**In scope:**

- Create `docs/user-guide-updates.md` in cursor-coding-protocols
- Link from `README.md` and `docs/README.md` for discoverability
- Create MCP-IMAGE-WORKFLOW.md (3 locations)
- Track in _pyrite work effort (via Work Efforts MCP)
- Create PRs for both repos

**Explicitly out of scope:**

- Integration tests (Stage 2)
- GitHub infrastructure for _pyrite (Stage 3)

## Verified CLI Behavior

Tested 2025-12-21:

```bash
$ node scripts/cursor-protocols-cli.js update check
🔍 Checking for updates...
❌ Update check failed: GitHub API returned 404

$ node scripts/cursor-protocols-cli.js update check --json
🔍 Checking for updates...
{
  "error": "GitHub API returned 404",
  "updateAvailable": false,
  "currentVersion": "2.0.0"
}

$ node scripts/cursor-protocols-cli.js help update
Command: update
Description: Check for and install updates
Usage: cursor-protocols update <check|install|rollback> [--json] [--refresh] [--list] [version]
```

**Note:** Normal `update check` does NOT show current version. Only `--json` includes it.

## Steps

### Step 1: Create Feature Branch

```bash
cd /Users/ctavolazzi/Code/cursor-coding-protocols
git checkout -b docs/user-guide-updates
```



### Step 2: Create docs/user-guide-updates.md

**Prerequisites section (MUST INCLUDE):**

- `unzip` command available (required for extracting updates)
- `.cursor-protocols-version.json` must exist
- Note: `install.sh` creates this automatically, or run manually:
- `node scripts/version-manager.js init` (core)
- `cursor-protocols version init` (if CLI available)

**Commands to document:**

- `update check` - check for updates
- `update check --json` - JSON output with currentVersion
- ⚠️ NOTE: Output has leading `🔍 Checking for updates...` line before JSON - must strip for parsing
- `update check --refresh` - bypass cache
- `update install` - install latest (requires version init!)
- `update install [version]` - install specific version
- `update rollback --list` - list backups
- `update rollback [backup]` - restore backup

**CLI notation (consistent with existing docs):**Document BOTH formats (existing docs already use the alias):

```bash
# Full path (always works)
node scripts/cursor-protocols-cli.js update check

# With global/npm link (if configured)
cursor-protocols update check
```

**Advanced Config section (env vars):**

```bash
# Custom repository (default: ctavolazzi/cursor-coding-protocols)
export CURSOR_PROTOCOLS_UPDATE_REPO="your-org/your-fork"

# Custom API endpoint (default: https://api.github.com)
export CURSOR_PROTOCOLS_UPDATE_API="https://github.mycompany.com/api/v3"

# Cache duration in ms (default: 3600000 = 1 hour)
export CURSOR_PROTOCOLS_UPDATE_CACHE_MS="1800000"
```



### Step 3: Update README files

**3a. Root README.md** - Add to **📖 Core Documentation** table (around line 560):

```markdown
| `docs/user-guide-updates.md` | 🆕 User guide for the update system |
```

Insert after the `AGENTS.md` row in the table.**3b. docs/README.md** - Add to **🎯 Quick Navigation** section (around line 34):

```markdown
### Update System
**Need help with updates?**
→ Read [`user-guide-updates.md`](user-guide-updates.md)
```



### Step 4: Commit and Push

```bash
git add docs/user-guide-updates.md README.md
git commit -m "docs: Add user guide for update system"
git push -u origin docs/user-guide-updates
```



### Step 5: Create PR (gh CLI per repo guidance)

```bash
gh pr create \
  --repo ctavolazzi/cursor-coding-protocols \
  --title "docs: Add user guide for update system" \
  --body "## Summary
Adds user documentation for the update system CLI commands.

## Changes
- New: docs/user-guide-updates.md
- Updated: README.md (added link in Core Documentation table)

## Prerequisites documented
- unzip command
- .cursor-protocols-version.json (version init)"
```



### Step 6: Track in _pyrite (with proper git workflow)

**6a. Create branch:**

```bash
cd /Users/ctavolazzi/Code/_pyrite
git checkout -b docs/update-system-user-guide
```

**6b. Create work effort via MCP** (retry):

```javascript
Tool: user-work-efforts-create_work_effort
repo_path: /Users/ctavolazzi/Code/_pyrite
title: "Update System User Documentation"
category: "10-19"
subcategory: "10"
objective: "Create user documentation for cursor-coding-protocols update system"
tasks: ["Create docs/user-guide-updates.md", "Link from README.md", "Link from docs/README.md", "Create PR"]
```

If MCP fails, fall back to direct file creation.**6c. Update devlog** - Add entry to `_work_efforts/devlog.md`**6d. Track in memory** (user-memory MCP):

```javascript
Tool: user-memory-create_entities
entities: [{
  name: "UpdateSystemUserDocs",
  entityType: "WorkEffort",
  observations: [
    "Created docs/user-guide-updates.md for cursor-coding-protocols",
    "Documents update check, install, rollback commands",
    "Includes prerequisites: unzip, version init",
    "Includes advanced config: CURSOR_PROTOCOLS_UPDATE_* env vars",
    "Linked from README.md and docs/README.md"
  ]
}]
```

**6d. Commit and push _pyrite changes:**

```bash
git add -A
git commit -m "Add work effort: update system user documentation"
git push -u origin docs/update-system-user-guide
```

**6e. Create _pyrite PR:**

```bash
gh pr create \
  --repo ctavolazzi/_pyrite \
  --title "Add work effort: update system user documentation" \
  --body "Tracks the cursor-coding-protocols user docs work.

Related: ctavolazzi/cursor-coding-protocols PR (link after created)"
```



## Step 7: Create MCP Image Workflow Documentation

Create `MCP-IMAGE-WORKFLOW.md` with Mermaid diagrams documenting the image generation workflow.**Save to 3 locations:**

1. `/Users/ctavolazzi/Code/.mcp-servers/pixellab-assets/MCP-IMAGE-WORKFLOW.md`
2. `/Users/ctavolazzi/Code/_pyrite/docs/MCP-IMAGE-WORKFLOW.md`
3. `/Users/ctavolazzi/Code/cursor-coding-protocols/docs/MCP-IMAGE-WORKFLOW.md`

**Contents:**

- Overview of Pixellab and Nano-Banana MCP tools
- Mermaid flowcharts for iterative image development
- Sequence diagrams for component development with images
- Use case examples (UI design, game assets, documentation)
- Best practices and tips
- Session context and files created

---

# Stage 2: Testing Infrastructure (Future - Requires Code Changes)

When ready to tackle integration tests:

## 2.1 Refactor `update-installer.js`

- Add constructor option for custom `downloadUpdate` function
- Add constructor option for custom `extractUpdate` function
- Allow injecting mock implementations
- Add dependency injection pattern

## 2.2 Write Integration Tests

- Mock network requests (no real GitHub API calls)
- Mock extraction (no real unzip)
- Test scenarios:
- check → reports current version (JSON mode)
- install → downloads and extracts
- rollback → restores from backup

## 2.3 Update Testing Documentation

- Add to `tests/README.md`
- Document test fixtures and mocks
- CI integration notes

---

# Stage 3: GitHub Infrastructure for _pyrite (Future - Separate Initiative)

## 3.1 Repository Setup

- v0.0.1 release tag
- CHANGELOG.md (Keep a Changelog format)
- LICENSE (MIT)

## 3.2 GitHub Templates

- `.github/ISSUE_TEMPLATE/` (bug report, feature request)
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CONTRIBUTING.md`

## 3.3 CI/CD

- GitHub Actions workflow
- Markdown lint (markdownlint)
- Link check (markdown-link-check)
- Work effort validation

## 3.4 Documentation Structure

- Initialize `_docs/` with docs-maintainer MCP
- Link _docs to work efforts