# D&D Campaign Desktop App

**Self-running, self-monitoring D&D campaign desktop application**

---

## Architecture

```
Electron App (Main Process)
  ├── Spawns Python Backend (child process)
  ├── Monitors health (auto-restart on crash)
  └── IPC bridge to SvelteKit UI

SvelteKit Frontend (Renderer)
  ├── Campaign visualization
  ├── Real-time updates (WebSocket)
  └── Control panel

Python Backend (Child Process)
  ├── FastAPI server (localhost:8000)
  ├── CampaignOrchestrator
  ├── Self-monitoring endpoints
  └── WebSocket for real-time events
```

---

## Quick Start

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Electron Setup

```bash
cd electron
npm install
```

### 4. Run Development

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
python campaign_server.py
```

**Terminal 2 - Electron**:
```bash
cd electron
npm start
```

---

## Project Structure

```
dnd_campaign_desktop_app/
├── backend/              # Python FastAPI server
│   ├── campaign_server.py
│   ├── campaign_manager.py
│   └── requirements.txt
├── frontend/             # SvelteKit UI
│   ├── src/
│   └── package.json
├── electron/             # Electron main process
│   ├── main.js
│   ├── preload.js
│   └── package.json
└── README.md
```

---

## Features

- ✅ Self-running campaigns
- ✅ Self-monitoring (health checks, auto-restart)
- ✅ Real-time campaign visualization
- ✅ Turn-by-turn narrative display
- ✅ Character stats and progression
- ✅ PDF generation for campaign booklets
