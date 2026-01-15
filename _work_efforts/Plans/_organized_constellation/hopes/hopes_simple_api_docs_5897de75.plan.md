---
name: Simple API Docs
overview: Create simple, expandable API documentation for all Pyrite servers (MCP + Dashboard) with no authentication, featuring both human-readable HTML and one-click AI-copyable plain text.
todos:
  - id: html-docs
    content: Create index.html with dark theme, tool cards, and copy buttons
    status: completed
  - id: ai-txt
    content: Create ai-docs.txt plain text reference optimized for AI context
    status: completed
    dependencies:
      - html-docs
  - id: readme-update
    content: Update mcp-servers/README.md with link to docs
    status: completed
    dependencies:
      - ai-txt

category: hopes
confidence: 0.75
constellation_date: 2026-01-14
---

# Simple Pyrite API Documentation

## Goal
Create dead-simple API docs that:
- Work for humans (styled HTML)
- Work for AI (plain text copy button)
- No auth required (local servers)
- Easy to expand later

## What We're Documenting

| Server | Type | Tools/Endpoints | Auth |
|--------|------|-----------------|------|
| work-efforts | MCP (Node.js) | 7 tools | None (local) |
| simple-tools | MCP (Node.js) | 3 tools | None (local) |
| docs-maintainer | MCP (Python) | 6 tools | None (local) |
| dashboard | REST (Express) | ~10 endpoints | None (local) |

## Output Files

```
mcp-servers/
├── docs/
│   ├── index.html          # Main docs page (self-contained)
│   └── ai-docs.txt         # Plain text for AI copy
└── README.md               # Updated with docs link
```

## Design Approach

**Single HTML file** - No build step, no dependencies:
- Embedded CSS (dark theme, cyan accents)
- Vanilla JS for copy functionality
- Mobile-friendly
- Expandable sections for each server

**AI Docs Format** - Optimized for context windows:
```
PYRITE MCP SERVERS - AI REFERENCE
=================================

## work-efforts (v0.3.0)
Tools: create_work_effort, create_ticket, ...

### create_work_effort
Creates a new work effort with WE-YYMMDD-xxxx ID.
Parameters:
  - repo_path (string, required): Full path to repository
  - title (string, required): Work effort title
  ...
```

## Page Structure

1. **Header** - Title, "Copy AI Docs" button
2. **Quick Start** - Cursor config JSON (copy button)
3. **MCP Servers** - Collapsible cards for each:
   - Server name + version
   - Installation
   - Tools list with params
4. **Dashboard API** - REST endpoints reference
5. **Future: Auth Section** - Placeholder for later

## Tech Choices

- **No framework** - Just HTML/CSS/JS
- **No build** - Edit and refresh
- **Self-contained** - Single file works offline
- **Copy to clipboard** - Native Clipboard API

## Expansion Path (Later)

1. Add auth section when needed
2. Add interactive "try it" for Dashboard API
3. Add OpenAPI/Swagger export
4. Add versioned docs if APIs change significantly