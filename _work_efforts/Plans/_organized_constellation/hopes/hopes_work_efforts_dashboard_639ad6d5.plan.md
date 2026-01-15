---
name: Work Efforts Dashboard
overview: Build a local Express server that serves a real-time dashboard for visualizing work efforts and tickets, matching the fogsift dark theme aesthetic.
todos:
  - id: setup-package
    content: Create package.json with Express, ws, chokidar dependencies
    status: pending
  - id: build-server
    content: Build Express server with static serving, WebSocket, and file watcher
    status: pending
    dependencies:
      - setup-package
  - id: create-html
    content: Create dashboard HTML with card layout for WEs and tickets
    status: pending
    dependencies:
      - setup-package
  - id: create-css
    content: Create fogsift-themed CSS with dark mode and ASCII borders
    status: pending
    dependencies:
      - create-html
  - id: create-js
    content: Create client JS with WebSocket connection and dynamic rendering
    status: pending
    dependencies:
      - create-html
  - id: add-readme
    content: Add README with usage instructions
    status: pending
    dependencies:
      - build-server
  - id: test-dashboard
    content: Test dashboard with browser tools
    status: pending
    dependencies:
      - build-server
      - create-js
      - create-css

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Work Efforts Mission Control Dashboard

## Architecture

```mermaid
graph TB
    subgraph Server["Express Server (port 3847)"]
        Static[Static File Server]
        API[REST API]
        WS[WebSocket Server]
    end
    
    subgraph FileSystem[File System]
        WE[_work_efforts_/]
        Chokidar[chokidar watcher]
    end
    
    subgraph Client[Browser Dashboard]
        UI[Dashboard UI]
        WSClient[WebSocket Client]
    end
    
    WE --> Chokidar
    Chokidar --> WS
    WS --> WSClient
    WSClient --> UI
    API --> WE
    Static --> UI
```

## File Structure

```
mcp-servers/dashboard/
├── server.js          # Express + WebSocket + file watcher
├── package.json       # Dependencies
├── public/
│   ├── index.html     # Dashboard HTML
│   ├── styles.css     # Fogsift-themed styles
│   └── app.js         # Client-side JS
└── README.md          # Usage docs
```

## Key Implementation Details

### Server ([`mcp-servers/dashboard/server.js`](mcp-servers/dashboard/server.js))
- Express serves static files from `public/`
- `chokidar` watches `_work_efforts_/` for changes
- `ws` WebSocket broadcasts updates to connected clients
- REST endpoint `GET /api/work-efforts` returns parsed WE/ticket data
- Reuses parsing logic pattern from existing [`mcp-servers/work-efforts/server.js`](mcp-servers/work-efforts/server.js)

### Dashboard UI
- Dark theme matching fogsift tokens (bg: `#1a1412`, accent: `#fb923c`)
- ASCII-style card borders using CSS `border-style: double` or box-drawing characters
- JetBrains Mono for data display
- Status badges with semantic colors (active=orange, completed=green, blocked=red)
- Expandable WE cards showing nested tickets

### Real-time Updates
- WebSocket connection auto-reconnects
- File changes trigger full re-scan and broadcast
- UI updates without page refresh

## Dependencies

```json
{
  "express": "^4.18.2",
  "ws": "^8.14.2", 
  "chokidar": "^3.5.3"
}
```

## Commands

```bash
cd mcp-servers/dashboard && npm install
node server.js  # Starts on http://localhost:3847
```

Port 3847 chosen as memorable (looks like "DART" - dashboard art).
