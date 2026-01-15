---
name: API + Work Effort System
overview: Restructure the work efforts system with scalable IDs (WE-YYMMDD-xxxx), then use it to build the site API architecture with comprehensive documentation, logging, and code comments.
todos:
  - id: update-mcp-server
    content: "TKT-000: Update MCP server for new WE-YYMMDD-xxxx ID format"
    status: completed
  - id: create-we-structure
    content: Create first WE folder with index.md and tickets/ subfolder
    status: completed
  - id: create-tickets
    content: Create all 8 ticket files (TKT-xxxx-001 through 008)
    status: completed
  - id: tkt-001
    content: "TKT-001: Define API endpoint schema and contracts"
    status: completed
  - id: tkt-002
    content: "TKT-002: Create /api/wiki/index.json in build script"
    status: completed
  - id: tkt-003
    content: "TKT-003: Create /api/wiki/sitemap.json endpoint"
    status: completed
  - id: tkt-004
    content: "TKT-004: Implement WikiAPI.js client module"
    status: completed
  - id: tkt-005
    content: "TKT-005: Add localStorage caching layer"
    status: completed
  - id: tkt-006
    content: "TKT-006: Create API architecture documentation"
    status: completed
  - id: tkt-007
    content: "TKT-007: Add comprehensive code comments to all files"
    status: completed
  - id: tkt-008
    content: "TKT-008: Implement debug logging system"
    status: completed

category: dreams
confidence: 0.48
constellation_date: 2026-01-14
---

# Fogsift API Architecture + Work Effort System

---

## Part 0: MCP Server Locations

### Local (Working Copy - DO NOT MOVE)

```javascript
/Users/ctavolazzi/Code/.mcp-servers/work-efforts/
├── server.js        # Main server code (will be updated)
├── package.json     # Dependencies
└── README.md
```

Cursor runs this directly via `~/.cursor/mcp.json`:

```json
{
  "work-efforts": {
    "command": "/Users/ctavolazzi/.nvm/versions/node/v22.20.0/bin/node",
    "args": ["/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js"]
  }
}
```



### Cloud (Version Control Backup)

```javascript
/Users/ctavolazzi/Code/active/_pyrite/
├── mcp-servers/
│   ├── work-efforts/
│   │   ├── server.js       # Synced copy
│   │   ├── package.json
│   │   └── README.md
│   ├── simple-tools/
│   ├── docs-maintainer/
│   └── README.md           # Installation instructions
```

**Workflow**:

1. Edit locally: `/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js`
2. Test: Restart Cursor, verify tools work
3. Backup: Copy to `_pyrite/mcp-servers/`, git push
4. Deploy elsewhere: Clone `_pyrite`, copy to local `.mcp-servers`

---

## Part 1: New ID Format

### Work Effort ID: `WE-YYMMDD-xxxx`

```javascript
WE-251227-a1b2
   │ │ │   └── 4-char random alphanumeric (a-z, 0-9)
   │ │ └── Day (27)
   │ └── Month (12)
   └── Year (25)
```



- **15 characters** total
- **Date-sortable** by filename
- **Collision-resistant**: 36^4 = 1.6M combinations per day
- **Self-documenting**: Tells you when it was created

### Ticket ID: `TKT-xxxx-NNN`

```javascript
TKT-a1b2-001
    └─┬─┘ └┬┘
  Parent   Sequence
  WE suffix
```



- References parent WE's unique suffix
- Sequential within the work effort
- Easy to trace back to parent

---

## Part 2: Folder Structure

```javascript
_work_efforts_/
├── WE-251227-a1b2_api_architecture/
│   ├── WE-251227-a1b2_index.md      # Main WE file
│   └── tickets/
│       ├── TKT-a1b2-001_define_endpoints.md
│       ├── TKT-a1b2-002_implement_wiki_api.md
│       ├── TKT-a1b2-003_create_sitemap_api.md
│       ├── TKT-a1b2-004_wiki_api_client.md
│       ├── TKT-a1b2-005_caching_layer.md
│       ├── TKT-a1b2-006_api_documentation.md
│       ├── TKT-a1b2-007_code_comments.md
│       └── TKT-a1b2-008_debug_logging.md
```

---

## Part 3: File Templates

### Work Effort Index (WE-YYMMDD-xxxx_index.md)

```markdown
---
id: WE-251227-a1b2
title: "API Architecture"
status: active
created: 2025-12-27T09:13:45-08:00
created_by: ctavolazzi
last_updated: 2025-12-27T09:13:45-08:00
branch: feature/WE-251227-a1b2-api-architecture
repository: fogsift
---

# WE-251227-a1b2: API Architecture

## Metadata
- **Created**: Friday, December 27, 2025 at 9:13:45 AM PST
- **Author**: ctavolazzi
- **Repository**: fogsift
- **Branch**: feature/WE-251227-a1b2-api-architecture

## Objective
Create a clean, API-driven data layer for dynamic wiki content with proper
caching, documentation, and debugging infrastructure.

## Tickets

| ID | Title | Status |
|----|-------|--------|
| TKT-a1b2-001 | Define API endpoint schema | pending |
| TKT-a1b2-002 | Create /api/wiki/index.json | pending |
| TKT-a1b2-003 | Create /api/wiki/sitemap.json | pending |
| TKT-a1b2-004 | Implement WikiAPI.js client | pending |
| TKT-a1b2-005 | Add localStorage caching | pending |
| TKT-a1b2-006 | Create API documentation | pending |
| TKT-a1b2-007 | Add code comments to all files | pending |
| TKT-a1b2-008 | Implement debug logging | pending |

## Commits
- (populated as work progresses)

## Related
- Docs: [[architecture.02_api_architecture]]
- PRs: (to be added)
```



### Ticket Template (TKT-xxxx-NNN_description.md)

```markdown
---
id: TKT-a1b2-001
parent: WE-251227-a1b2
title: "Define API Endpoint Schema"
status: pending
created: 2025-12-27T09:15:22-08:00
created_by: ctavolazzi
assigned_to: null
---

# TKT-a1b2-001: Define API Endpoint Schema

## Metadata
- **Created**: Friday, December 27, 2025 at 9:15:22 AM PST
- **Parent Work Effort**: WE-251227-a1b2 (API Architecture)
- **Author**: ctavolazzi

## Description
Document all API endpoints, their request/response contracts, and error codes.

## Acceptance Criteria
- [ ] All endpoints documented with URL, method, response shape
- [ ] TypeScript interfaces defined for all responses
- [ ] Error codes and messages specified
- [ ] Example requests/responses provided

## Files Changed
- (populated when complete)

## Implementation Notes
- (decisions, blockers, context)

## Commits
- (populated as work progresses)
```

---

## Part 4: Git Integration

### The Flow

```javascript
1. PLAN      → Create WE folder + index.md with objective
2. TICKET    → Create ticket files in tickets/ subfolder
3. BRANCH    → git checkout -b feature/WE-YYMMDD-xxxx-description
4. IMPLEMENT → Code with inline comments: // TKT-xxxx-NNN: reason
5. COMMIT    → "WE-YYMMDD-xxxx/TKT-xxxx-NNN: Description"
6. UPDATE    → Mark ticket complete, list files changed
7. MERGE     → PR title: "WE-YYMMDD-xxxx: Work Effort Title"
8. CLOSE     → Mark WE complete when all tickets done
```



### Commit Message Format

```javascript
WE-251227-a1b2/TKT-a1b2-001: Define API endpoint schema

- Document /api/wiki/index.json contract
- Document /api/wiki/sitemap.json contract
- Add TypeScript interfaces
- Specify error codes

Refs: TKT-a1b2-001
Part of: WE-251227-a1b2 (API Architecture)
```



### Branch Naming

```javascript
feature/WE-251227-a1b2-api-architecture
```

---

## Part 5: API Architecture (First Work Effort)

### Endpoints

```javascript
dist/api/
├── wiki/
│   ├── index.json      # Full wiki structure
│   └── sitemap.json    # JD-numbered sitemap data
├── articles.json       # Field notes content
└── meta.json           # Site version, build date
```



### Data Flow

```javascript
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
│  (build-time)     │                    │  (build-time)     │
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



### Debug Logging System

```javascript
// src/js/debug.js
const Debug = {
    enabled: false,
    prefix: '[FOGSIFT]',

    log(module, message, data) {
        if (!this.enabled) return;
        console.log(`${this.prefix}[${module}]`, message, data || '');
    },

    api(endpoint, status, duration) {
        if (!this.enabled) return;
        console.log(`${this.prefix}[API] ${endpoint} → ${status} (${duration}ms)`);
    },

    // Activate from console: Debug.enable()
    enable() { this.enabled = true; localStorage.setItem('debug', '1'); },
    disable() { this.enabled = false; localStorage.removeItem('debug'); }
};
```

---

## Part 6: Files to Create/Modify

### New Files

- `_work_efforts_/WE-YYMMDD-xxxx_api_architecture/WE-YYMMDD-xxxx_index.md`
- `_work_efforts_/WE-YYMMDD-xxxx_api_architecture/tickets/TKT-xxxx-001_define_endpoints.md`
- (+ 7 more ticket files)
- `src/js/wiki-api.js` - Client API module
- `src/js/debug.js` - Debug logging system
- `_docs/20-29_development/architecture_category/architecture.02_api_architecture.md`

### Modified Files

- `/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js` - Update for new ID format
- `scripts/build.js` - Add API JSON generation
- All `src/js/*.js` - Add comprehensive file headers
- All `src/css/*.css` - Add file role documentation

---

## Execution Order

1. **TKT-000**: Update MCP server for new ID format (prerequisite)
2. **Create WE**: Generate first work effort folder + index