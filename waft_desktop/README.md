# WAFT Desktop Application

**Electron desktop application for the WAFT (Wave Agent Framework & Tools) system.**

Provides a local desktop interface for managing WAFT projects, work efforts, and the complete WAFT ecosystem.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Electron Application                    │
│  ┌──────────────────────────────────────────┐  │
│  │  Main Process (Node.js)                   │  │
│  │  - Manages WAFT Python backend process    │  │
│  │  - IPC communication                      │  │
│  │  - Process monitoring & health checks     │  │
│  │  - Auto-restart on crashes                │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Renderer Process (SvelteKit)             │  │
│  │  - Project management UI                  │  │
│  │  - Work effort dashboard                  │  │
│  │  - Real-time updates                      │  │
│  │  - WAFT ecosystem visualization          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Python Backend (Child Process)          │  │
│  │  - FastAPI server (localhost:8000)       │  │
│  │  - WAFT API endpoints                     │  │
│  │  - Project management                     │  │
│  │  - Work effort operations                 │  │
│  │  - WebSocket for real-time events        │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- **Node.js**: LTS version (18+ recommended)
- **Python**: 3.10+ with WAFT installed
- **npm**: Bundled with Node.js

### Development Setup

1. **Install Electron dependencies**:
```bash
cd waft_desktop/electron
npm install
```

2. **Install Frontend dependencies**:
```bash
cd waft_desktop/frontend
npm install
```

3. **Start Development**:

**Terminal 1 - Backend (optional, Electron will auto-start it)**:
```bash
cd /path/to/waft
waft serve --port 8000
```

**Terminal 2 - Frontend Dev Server**:
```bash
cd waft_desktop/frontend
npm run dev
```

**Terminal 3 - Electron App**:
```bash
cd waft_desktop/electron
npm start
```

---

## Project Structure

```
waft_desktop/
├── electron/              # Electron main process
│   ├── main.js           # Main process entry point
│   ├── preload.js        # Preload script (security)
│   ├── package.json      # Electron dependencies
│   └── README.md         # Electron documentation
├── frontend/             # SvelteKit frontend
│   ├── src/
│   │   ├── routes/       # SvelteKit routes
│   │   ├── lib/          # Shared components
│   │   └── app.html      # App shell
│   ├── package.json      # Frontend dependencies
│   └── vite.config.js    # Vite configuration
└── README.md             # This file
```

---

## Features

- ✅ **Auto-Managed Backend**: Electron spawns and monitors WAFT backend
- ✅ **Health Monitoring**: Automatic health checks and auto-restart
- ✅ **Project Management**: Create, open, and manage WAFT projects
- ✅ **Work Effort Dashboard**: Visualize and track work efforts
- ✅ **Real-Time Updates**: WebSocket integration for live updates
- ✅ **Self-Monitoring**: Built-in health checks and metrics
- ✅ **Single Instance**: Prevents multiple app instances

---

## Development

### Backend Management

The Electron app automatically:
1. Spawns WAFT Python backend on startup
2. Monitors health every 5 seconds
3. Auto-restarts on crashes (max 5 attempts)
4. Sends status updates to frontend via IPC

### IPC API

The preload script exposes `window.electronAPI`:

```javascript
// Get backend status
const status = await window.electronAPI.backend.getStatus();

// Restart backend
await window.electronAPI.backend.restart();

// Manual health check
const healthy = await window.electronAPI.backend.healthCheck();

// Listen to events
window.electronAPI.backend.onLog((data) => {
  console.log('Backend log:', data);
});

window.electronAPI.backend.onHealth((data) => {
  console.log('Backend health:', data);
});
```

---

## Configuration

### Backend Path

The Electron app looks for WAFT in:
1. Environment variable: `WAFT_PATH`
2. Parent directory: `../` (if running from `waft_desktop/electron`)
3. Default: Current working directory

### Port Configuration

- **Backend API**: `localhost:8000` (default)
- **Frontend Dev**: `localhost:5173` (Vite default)
- **Electron**: Loads frontend from dev server or build

---

## Building

### Development Build

```bash
cd frontend
npm run build
cd ../electron
npm start
```

### Production Build

```bash
cd electron
npm run build
```

---

## Troubleshooting

### Backend Not Starting

- Check Python installation: `python3 --version`
- Check WAFT installation: `waft --version`
- Check backend logs in Electron console

### Frontend Not Loading

- Ensure frontend dev server is running: `cd frontend && npm run dev`
- Check port conflicts (5173 for Vite)
- Check Electron console for errors

### Port Conflicts

- Backend port 8000 in use: Change in `electron/main.js`
- Frontend port 5173 in use: Change in `frontend/vite.config.js`

---

**Status**: 🚧 In Development
**Version**: 0.0.1
