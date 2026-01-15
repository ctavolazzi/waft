---
name: Test Mission Control UI
overview: Clean install Mission Control dependencies, document the tech stack, and test the browser UI with responsive breakpoint verification.
todos:
  - id: clean-install
    content: Delete node_modules and package-lock.json, run npm install
    status: completed
  - id: start-server
    content: Start Mission Control dev server in background
    status: completed
    dependencies:
      - clean-install
  - id: test-desktop
    content: Navigate to dashboard, take snapshot at default viewport
    status: completed
    dependencies:
      - start-server
  - id: test-responsive
    content: Test tablet (768px) and mobile (375px) breakpoints
    status: completed
    dependencies:
      - test-desktop
  - id: explore-features
    content: Click through UI to assess pending feature status
    status: completed
    dependencies:
      - test-responsive
  - id: document
    content: Summarize findings - what works, what needs work
    status: completed
    dependencies:
      - explore-features
---

# Test Mission Control Browser UI

## Tech Stack Map

```mermaid
graph TB
    subgraph backend [Backend - Node.js]
        server[server.js<br>Express + HTTP]
        ws[WebSocket Server<br>ws library]
        parser[lib/parser.js<br>Dual-format parser]
        watcher[lib/watcher.js<br>chokidar file watcher]
        logger[lib/logger.js<br>pino structured logging]
    end

    subgraph frontend [Frontend - Vanilla JS]
        html[index.html<br>Semantic HTML5]
        app[app.js<br>MissionControl class]
        events[events.js<br>EventBus + ToastManager]
        charts[charts.js<br>SVG chart generators]
        datastore[datastore.js<br>Client state]
        styles[styles.css<br>CSS Variables + Grid]
    end

    subgraph deps [Dependencies]
        express[express ^4.18.2]
        wslib[ws ^8.14.2]
        chokidar[chokidar ^3.5.3]
        graymatter[gray-matter ^4.0.3]
        chalk[chalk ^5.6.2]
        pino[pino ^10.1.0]
    end

    server --> ws
    server --> parser
    server --> watcher
    server --> logger
    ws --> app
    app --> events
    app --> charts
    app --> datastore
```

### Backend Stack
| Component | Tech | Purpose |
|-----------|------|---------|
| HTTP Server | Express 4.18 | REST API, static file serving |
| WebSocket | ws 8.14 | Real-time updates to clients |
| File Watching | chokidar 3.5 | Monitor `_work_efforts` changes |
| Frontmatter | gray-matter 4.0 | Parse YAML frontmatter in markdown |
| Logging | pino 10.1 | Structured JSON logging |
| CLI | chalk 5.6 | Colorful terminal output |

### Frontend Stack (Zero Dependencies)
| Component | Tech | Purpose |
|-----------|------|---------|
| UI | Vanilla JS (ES6+ classes) | No framework overhead |
| Styling | CSS Variables + Grid/Flexbox | Responsive, themeable |
| Fonts | JetBrains Mono, Space Grotesk | Code + UI typography |
| Events | Custom EventBus | Pub/sub with wildcards |
| Charts | Hand-rolled SVG | Donut, bar, line, sparkline, heatmap |
| State | Custom DataStore | Client-side caching |

### Data Formats Supported
- **MCP v0.3.0**: `WE-YYMMDD-xxxx` directories with `TKT-xxxx-NNN` tickets
- **Johnny Decimal**: `XX-XX_category/XX_subcategory/XX.XX_document.md`

---

## Execution Steps

### 1. Clean Install
```bash
cd /Users/ctavolazzi/Code/active/_pyrite/mcp-servers/dashboard
rm -rf node_modules package-lock.json
npm install
```

### 2. Start Server
```bash
npm run dev
```
Server runs on port 3847 (auto-finds next available if busy).

### 3. Test UI in Browser
- Navigate to http://localhost:3847
- Take snapshots at desktop, tablet (768px), and mobile (375px)
- Verify responsive CSS (TKT-fwmv-001 - completed)
- Explore pending feature areas (modals, charts, controls)

### 4. Document Findings
Report UI status, any issues, and recommendations.

---

## Key Files Reference
| File | Lines | Purpose |
|------|-------|---------|
| `server.js` | ~880 | Express server, WebSocket, REST API |
| `public/app.js` | ~2900 | Main MissionControl class |
| `public/events.js` | ~900 | EventBus, ToastManager, AnimationController |
| `public/charts.js` | ~420 | SVG chart generators |
| `public/styles.css` | - | CSS with responsive breakpoints |
| `lib/parser.js` | ~330 | Dual-format work effort parser |