---
name: API + Work System v2
overview: Implement new Work Effort system with scalable IDs (WE-YYMMDD-xxxx), then use it to build the site API architecture with comprehensive documentation and debugging infrastructure.
todos:
  - id: create-we-structure
    content: Create WE-251227-xxxx folder with index.md and tickets/ subfolder
    status: pending
  - id: create-tickets
    content: Create all 8 ticket files (TKT-xxxx-001 through 008)
    status: pending
  - id: tkt-001
    content: "TKT-001: Define API endpoint schema and contracts"
    status: pending
  - id: tkt-002
    content: "TKT-002: Create /api/wiki/index.json in build script"
    status: pending
  - id: tkt-003
    content: "TKT-003: Create /api/wiki/sitemap.json endpoint"
    status: pending
  - id: tkt-004
    content: "TKT-004: Implement WikiAPI.js client module"
    status: pending
  - id: tkt-005
    content: "TKT-005: Add localStorage caching layer"
    status: pending
  - id: tkt-006
    content: "TKT-006: Create API architecture documentation"
    status: pending
  - id: tkt-007
    content: "TKT-007: Add comprehensive code comments to all files"
    status: pending
  - id: tkt-008
    content: "TKT-008: Implement debug logging system"
    status: pending

category: hopes
confidence: 0.51
constellation_date: 2026-01-14
---

# Fogsift API Architecture + Work Effort System v2

---

## Part 1: New Work Effort System

### ID Format

**Work Efforts**: `WE-YYMMDD-xxxx`
- `WE` = Work Effort prefix
- `YYMMDD` = Date created (251227 = Dec 27, 2025)
- `xxxx` = 4-character random alphanumeric (a-z, 0-9)

**Tickets**: `TKT-xxxx-NNN`
- `xxxx` = Parent WE's unique suffix
- `NNN` = Sequential number (001, 002, etc.)

### Folder Structure

```
_work_efforts_/
├── WE-251227-a1b2_api_architecture/
│   ├── WE-251227-a1b2_index.md      # Main WE file with ticket index
│   └── tickets/
│       ├── TKT-a1b2-001_define_endpoints.md
│       ├── TKT-a1b2-002_implement_wiki_api.md
│       └── TKT-a1b2-003_add_caching.md
```

### Work Effort Index Template

```markdown
---
id: WE-YYMMDD-xxxx
title: "Title Here"
status: active | paused | completed
created: 2025-12-27T09:13:45-08:00
created_by: ctavolazzi
last_updated: 2025-12-27T09:13:45-08:00
branch: feature/WE-YYMMDD-xxxx-slug
repository: fogsift
---

# WE-YYMMDD-xxxx: Title

## Objective
[What we're building and why]

## Tickets

| ID | Title | Status |
|----|-------|--------|
| TKT-xxxx-001 | Task name | pending |
| TKT-xxxx-002 | Task name | pending |

## Commits
- (populated as work progresses)

## Related
- Docs: [[link]]
- PRs: #NN
```

### Ticket Template

```markdown
---
id: TKT-xxxx-NNN
parent: WE-YYMMDD-xxxx
title: "Ticket Title"
status: pending | in_progress | completed | blocked
created: 2025-12-27T09:15:22-08:00
created_by: ctavolazzi
---

# TKT-xxxx-NNN: Title

## Description
[What needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Files Changed
- (populated when complete)

## Notes
- (implementation details, decisions)
```

---

## Part 2: Git Integration

### The Flow

```
1. PLAN      → Create Work Effort folder + index.md
2. TICKET    → Create ticket files in tickets/ subfolder
3. BRANCH    → git checkout -b feature/WE-YYMMDD-xxxx-description
4. IMPLEMENT → Code with inline comments: // TKT-xxxx-NNN: reason
5. COMMIT    → "WE-YYMMDD-xxxx/TKT-xxxx-NNN: Description"
6. UPDATE    → Mark ticket complete, list files changed
7. MERGE     → PR title: "WE-YYMMDD-xxxx: Work Effort Title"
8. CLOSE     → Mark WE complete when all tickets done
```

### Commit Message Format

```
WE-251227-a1b2/TKT-a1b2-001: Add API endpoint schema

- Define /api/wiki/index.json contract
- Add TypeScript interfaces for responses
- Document error codes

Refs: TKT-a1b2-001
Part of: WE-251227-a1b2 (API Architecture)
```

### Branch Naming

```
feature/WE-251227-a1b2-api-architecture     # Main WE branch
feature/WE-251227-a1b2-api-architecture/TKT-001  # Optional: per-ticket branch
```

---

## Part 3: First Work Effort - API Architecture

### WE-251227-xxxx: Site API Architecture

**Objective**: Create a clean, API-driven data layer for dynamic wiki content with proper caching, documentation, and debugging infrastructure.

### Tickets

| ID | Title | Description |
|----|-------|-------------|
| TKT-xxxx-001 | Define API endpoint schema | Document all endpoints, request/response contracts |
| TKT-xxxx-002 | Create /api/wiki/index.json | Build script generates wiki index as JSON |
| TKT-xxxx-003 | Create /api/wiki/sitemap.json | JD-formatted sitemap data endpoint |
| TKT-xxxx-004 | Implement WikiAPI.js module | Client-side module with loadIndex(), loadSitemap() |
| TKT-xxxx-005 | Add localStorage caching | Cache API responses with TTL |
| TKT-xxxx-006 | Create API architecture docs | Full documentation in _docs/ |
| TKT-xxxx-007 | Add code comments to all files | Comprehensive headers explaining role in system |
| TKT-xxxx-008 | Implement debug logging system | Toggleable Debug module with API/component logging |

### API Endpoints (Final)

```
dist/api/
├── wiki/
│   ├── index.json      # Full wiki structure (from src/wiki/index.json)
│   └── sitemap.json    # JD-numbered sitemap data
├── articles.json       # Field notes content
└── meta.json           # Site version, build date, etc.
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│              SINGLE SOURCE OF TRUTH                          │
│              src/wiki/index.json                             │
└─────────────────────────────┬───────────────────────────────┘
                              │
              npm run build   │
                              ▼
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────────┐                    ┌───────────────────┐
│  Static HTML      │                    │  /api/*.json      │
│  (build-time)     │                    │  (also build-time)│
└───────────────────┘                    └─────────┬─────────┘
                                                   │
                                                   ▼
                                         ┌───────────────────┐
                                         │  WikiAPI.js       │
                                         │  (client module)  │
                                         │  - loadIndex()    │
                                         │  - loadSitemap()  │
                                         │  - cache layer    │
                                         └─────────┬─────────┘
                                                   │
                                                   ▼
                                         ┌───────────────────┐
                                         │  Components       │
                                         │  - JD Sitemap     │
                                         │  - Wiki Nav       │
                                         │  - Search (future)│
                                         └───────────────────┘
```

---

## Part 4: Files to Create/Modify

### New Files
- `_work_efforts_/WE-251227-xxxx_api_architecture/WE-251227-xxxx_index.md`
- `_work_efforts_/WE-251227-xxxx_api_architecture/tickets/TKT-xxxx-001_define_endpoints.md`
- (+ 7 more ticket files)
- `src/js/wiki-api.js` - Client API module
- `src/js/debug.js` - Debug logging system
- `_docs/20-29_development/architecture_category/architecture.02_api_architecture.md`

### Modified Files
- `scripts/build.js` - Add API JSON generation
- All `src/js/*.js` - Add comprehensive file headers
- All `src/css/*.css` - Add file role documentation

---

## Execution Order

1. **Create WE folder structure** with index.md
2. **Create all 8 ticket files** with acceptance criteria
3. **Execute tickets sequentially** (001 through 008)
4. **Each ticket completion** includes:
   - Code changes with `// TKT-xxxx-NNN:` comments
   - Commit with proper format
   - Ticket updated with files changed
   - WE index updated

---

## Summary

- **ID Format**: `WE-YYMMDD-xxxx` (short, unique, sortable)
- **Full metadata**: Inside files (timestamps, author, context)
- **Git integration**: IDs in commits, branches, PRs
- **First WE**: API Architecture with 8 tickets
- **Outcome**: Clean API layer + documentation + debug tooling