---
name: Mission Control Dashboard
overview: Build a local dashboard that monitors work efforts across multiple repositories, designed to scale from one repo to many agents working in parallel across the codebase.
todos:
  - id: fix-mcp-server
    content: Fix _work_efforts_ -> _work_efforts in MCP server.js (2 occurrences)
    status: pending
  - id: create-package
    content: Create package.json with express, ws, chokidar
    status: pending
  - id: create-config
    content: Create config.json with _pyrite as first repo
    status: pending
    dependencies:
      - create-package
  - id: build-server
    content: Build Express server with multi-repo file watching and WebSocket
    status: pending
    dependencies:
      - create-package
      - create-config
  - id: create-html
    content: Create dashboard HTML with repo tabs and WE card layout
    status: pending
    dependencies:
      - create-package
  - id: create-css
    content: Create fogsift-themed CSS (dark mode, ASCII borders, monospace)
    status: pending
    dependencies:
      - create-html
  - id: create-client-js
    content: Create client JS with WebSocket and dynamic rendering
    status: pending
    dependencies:
      - create-html
  - id: add-readme
    content: Add README with setup and usage instructions
    status: pending
    dependencies:
      - build-server
  - id: test-dashboard
    content: Test dashboard in browser, verify real-time updates
    status: pending
    dependencies:
      - build-server
      - create-client-js
      - create-css

category: hopes
confidence: 0.75
constellation_date: 2026-01-14
---

# Mission Control Dashboard

## Vision

A central dashboard to monitor AI agent progress across multiple Cursor windows, repositories, and workflows - starting with one repo, designed for many.

```
┌─────────────────────────────────────────────────────────────────┐
│  MISSION CONTROL                              ● 3 repos active  │
├─────────────────────────────────────────────────────────────────┤
│  _pyrite          fogsift           cursor-coding-protocols     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                │
│  │ WE-a1b2  │     │ WE-c3d4  │     │ WE-e5f6  │                │
│  │ ████░░░░ │     │ ████████ │     │ ██░░░░░░ │                │
│  │ 2/5 tkts │     │ DONE     │     │ 1/4 tkts │                │
│  └──────────┘     └──────────┘     └──────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture

```mermaid
graph TB
    subgraph Dashboard["Mission Control (Express :3847)"]
        Static[Static Files]
        API[REST API]
        WS[WebSocket Hub]
        Config[config.json]
    end
    
    subgraph Watchers[File Watchers]
        W1[chokidar: _pyrite]
        W2[chokidar: fogsift]
        W3[chokidar: repo-n]
    end
    
    subgraph Repos[Repositories]
        R1[_pyrite/_work_efforts/]
        R2[fogsift/_work_efforts/]
        R3[repo-n/_work_efforts/]
    end
    
    Config --> W1
    Config --> W2
    Config --> W3
    R1 --> W1
    R2 --> W2
    R3 --> W3
    W1 --> WS
    W2 --> WS
    W3 --> WS
    WS --> Browser[Browser Clients]
    API --> Browser
```

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Folder name | `_work_efforts/` | Match existing disk structure |
| Database | None (files are truth) | No sync issues, markdown is portable |
| Multi-repo | Config-driven | Add repos via `config.json`, no restart needed |
| Framework | Express.js | Simple, JS ecosystem consistency |

## File Structure

```
mcp-servers/dashboard/
├── server.js           # Express + WebSocket + multi-repo watchers
├── package.json        
├── config.json         # Repo paths to monitor
├── public/
│   ├── index.html      # Dashboard shell
│   ├── styles.css      # Fogsift dark theme
│   └── app.js          # Client: WS connection, rendering
└── README.md
```

## Config Format

```json
{
  "repos": [
    {
      "name": "_pyrite",
      "path": "/Users/ctavolazzi/Code/active/_pyrite",
      "color": "#fb923c"
    }
  ],
  "port": 3847
}
```

Start with one repo. Add more by editing config (hot-reload support).

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/repos` | GET | List configured repos |
| `/api/repos/:name/work-efforts` | GET | Get all WEs for a repo |
| `/api/config` | GET/POST | Read/update config |

## WebSocket Events

```javascript
// Server -> Client
{ type: "update", repo: "_pyrite", data: {...} }
{ type: "repo_added", repo: "fogsift" }

// Client -> Server  
{ type: "subscribe", repos: ["_pyrite", "fogsift"] }
```

## UI Components

1. **Repo Switcher** - Tabs or sidebar for each repo
2. **Work Effort Cards** - Expandable cards with progress bars
3. **Ticket List** - Nested under each WE with status badges
4. **Activity Feed** - Real-time log of file changes (optional v2)

## Styling (Fogsift Dark)

```css
:root {
  --bg: #1a1412;
  --bg-card: #0f0b09;
  --text: #f5f0e6;
  --accent: #fb923c;
  --border: #3d2e26;
  --font-mono: 'JetBrains Mono', monospace;
}
```

## MVP Scope (v1)

- [x] Single repo to start (config supports multiple)
- [x] Real-time file watching
- [x] Work effort + ticket visualization
- [x] Status badges and progress indication
- [ ] ~~Settings UI~~ (v2)
- [ ] ~~Activity feed~~ (v2)

## Bug Fix Required

Update [`mcp-servers/work-efforts/server.js`](mcp-servers/work-efforts/server.js) lines 104 and 418:
```javascript
// Change from:
const workEffortsDir = path.join(repoPath, '_work_efforts_');
// To:
const workEffortsDir = path.join(repoPath, '_work_efforts');
```

## Commands

```bash
cd mcp-servers/dashboard
npm install
node server.js
# Open http://localhost:3847
```
