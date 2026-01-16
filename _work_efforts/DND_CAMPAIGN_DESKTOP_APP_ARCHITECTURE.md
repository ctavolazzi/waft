# D&D Campaign Desktop App - Architecture Recommendation

**Date**: 2026-01-16
**Purpose**: Self-running, self-monitoring D&D campaign desktop application
**Status**: 🎯 Architecture Design

---

## Executive Summary

**Recommended Stack**: **Electron + SvelteKit + Python (WAFT Backend)**

**Why NOT Docker**: Docker adds unnecessary complexity for a local desktop app. Electron can bundle everything into a single executable.

**Why This Stack**:
- ✅ **Electron**: Proven desktop app framework (you already have experience)
- ✅ **SvelteKit**: Modern, fast frontend (you already have it set up)
- ✅ **Python Backend**: Your WAFT campaign system (already exists)
- ✅ **Single Executable**: Can package everything into one app
- ✅ **Self-Monitoring**: Electron can manage Python process lifecycle

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────┐
│         Electron Application                    │
│  ┌──────────────────────────────────────────┐  │
│  │  Main Process (Node.js)                   │  │
│  │  - Manages Python backend process         │  │
│  │  - IPC communication                      │  │
│  │  - Process monitoring & health checks      │  │
│  │  - Auto-restart on crashes                │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Renderer Process (SvelteKit)           │  │
│  │  - Campaign UI                            │  │
│  │  - Real-time updates                      │  │
│  │  - Campaign visualization                 │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                    ↕ IPC
┌─────────────────────────────────────────────────┐
│  Python Backend (Child Process)                 │
│  - CampaignOrchestrator                         │
│  - D&D 5e Engine                                │
│  - Being System                                  │
│  - PDF Generation                               │
│  - FastAPI Server (localhost:8000)              │
└─────────────────────────────────────────────────┘
```

---

## Architecture Details

### 1. Electron Main Process

**Responsibilities**:
- **Process Management**: Spawn and monitor Python backend
- **Health Monitoring**: Check if backend is alive, restart if needed
- **IPC Bridge**: Communication between SvelteKit and Python
- **Auto-restart**: Restart Python process on crashes
- **Resource Monitoring**: CPU, memory usage tracking

**Key Features**:
```javascript
// Main process (main.js)
const { spawn } = require('child_process');
const path = require('path');

class CampaignManager {
    constructor() {
        this.pythonProcess = null;
        this.restartCount = 0;
        this.maxRestarts = 5;
    }

    startBackend() {
        // Spawn Python backend
        const pythonPath = path.join(__dirname, 'python', 'python');
        const scriptPath = path.join(__dirname, 'backend', 'campaign_server.py');

        this.pythonProcess = spawn(pythonPath, [scriptPath], {
            stdio: ['pipe', 'pipe', 'pipe']
        });

        // Monitor process
        this.pythonProcess.on('exit', (code) => {
            if (code !== 0 && this.restartCount < this.maxRestarts) {
                this.restartCount++;
                console.log(`Backend crashed, restarting... (${this.restartCount}/${this.maxRestarts})`);
                setTimeout(() => this.startBackend(), 2000);
            }
        });

        // Health check
        setInterval(() => this.healthCheck(), 5000);
    }

    async healthCheck() {
        try {
            const response = await fetch('http://localhost:8000/api/health');
            if (!response.ok) throw new Error('Backend unhealthy');
            this.restartCount = 0; // Reset on success
        } catch (error) {
            console.error('Health check failed:', error);
            // Restart if unhealthy
            if (this.pythonProcess) {
                this.pythonProcess.kill();
                this.startBackend();
            }
        }
    }
}
```

### 2. SvelteKit Frontend

**Location**: `dnd_campaign_app/frontend/` (new directory)

**Features**:
- Campaign control panel (start/stop/pause)
- Real-time campaign visualization
- Turn-by-turn narrative display
- Character stats and progression
- Campaign state visualization
- PDF viewer for generated reports

**Tech Stack**:
- SvelteKit (you already have this)
- Tailwind CSS (already configured)
- WebSocket or polling for real-time updates

### 3. Python Backend

**Location**: `dnd_campaign_app/backend/` (new directory)

**Components**:
- **FastAPI Server**: REST API + WebSocket for real-time updates
- **CampaignOrchestrator**: Your existing campaign system
- **Self-Monitoring**: Health endpoints, metrics, logging

**Key Features**:
```python
# backend/campaign_server.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pathlib import Path

from waft.campaign.campaign_orchestrator import CampaignOrchestrator

app = FastAPI()

# CORS for Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Electron app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SelfMonitoringCampaign:
    def __init__(self):
        self.orchestrator = CampaignOrchestrator(Path.cwd())
        self.running = False
        self.metrics = {
            "turns_completed": 0,
            "errors": 0,
            "uptime": 0
        }

    async def run_campaign(self):
        """Run campaign with self-monitoring."""
        self.running = True
        try:
            # Your existing campaign logic
            await self.orchestrator.run()
        except Exception as e:
            self.metrics["errors"] += 1
            # Log error, continue if recoverable
        finally:
            self.running = False

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "running": campaign.running,
        "metrics": campaign.metrics
    }

@app.websocket("/ws/campaign")
async def campaign_websocket(websocket: WebSocket):
    """WebSocket for real-time campaign updates."""
    await websocket.accept()
    # Stream campaign events in real-time
```

---

## Why This Architecture?

### ✅ Advantages

1. **Single Executable**: Electron can bundle Python runtime
   - Use `pyinstaller` or `cx_Freeze` to create Python executable
   - Bundle with Electron app
   - One `.app` (macOS) or `.exe` (Windows) file

2. **Self-Monitoring Built-in**:
   - Electron monitors Python process
   - Python exposes health endpoints
   - Auto-restart on failures
   - Metrics and logging

3. **Real-time Updates**:
   - WebSocket for live campaign events
   - SvelteKit reactive UI
   - No page refreshes needed

4. **Leverages Existing Code**:
   - Your CampaignOrchestrator
   - Your SvelteKit setup
   - Your Electron experience

5. **Cross-Platform**:
   - Electron works on macOS, Windows, Linux
   - Python backend is cross-platform
   - Single codebase

### ❌ Why NOT Docker

1. **Overkill**: Docker adds containerization overhead
2. **Complexity**: Need Docker runtime, more moving parts
3. **Distribution**: Users need Docker installed
4. **Performance**: Native processes are faster
5. **Desktop Integration**: Electron integrates better with OS

---

## Implementation Plan

### Phase 1: Backend API (1-2 days)
1. Create FastAPI server wrapper around CampaignOrchestrator
2. Add WebSocket support for real-time events
3. Add health monitoring endpoints
4. Add metrics collection

### Phase 2: Electron App (2-3 days)
1. Create Electron app structure
2. Implement Python process management
3. Add health monitoring and auto-restart
4. Set up IPC between main and renderer

### Phase 3: SvelteKit Frontend (2-3 days)
1. Create campaign UI in SvelteKit
2. Connect to backend via WebSocket
3. Real-time campaign visualization
4. Control panel (start/stop/pause)

### Phase 4: Packaging (1 day)
1. Bundle Python with PyInstaller
2. Package Electron app
3. Create installers (macOS/Windows)
4. Test standalone executable

---

## Alternative: Tauri (Lighter Option)

If Electron feels too heavy, consider **Tauri**:

**Tauri Stack**: Tauri + SvelteKit + Python Backend

**Advantages**:
- ✅ Much smaller bundle size (~10MB vs ~150MB)
- ✅ Better performance (Rust backend)
- ✅ Better security model
- ✅ Native OS integration

**Trade-offs**:
- ⚠️ Less mature ecosystem
- ⚠️ Rust knowledge helpful (but not required)
- ⚠️ Smaller community

**Recommendation**: Start with Electron (you have experience), migrate to Tauri later if needed.

---

## Project Structure

```
dnd_campaign_app/
├── frontend/                 # SvelteKit app
│   ├── src/
│   │   ├── routes/
│   │   │   └── +page.svelte  # Campaign UI
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── CampaignViewer.svelte
│   │   │   │   ├── ControlPanel.svelte
│   │   │   │   └── StatsPanel.svelte
│   │   │   └── stores/
│   │   │       └── campaignStore.ts
│   │   └── app.html
│   └── package.json
│
├── electron/                 # Electron main process
│   ├── main.js              # Main process
│   ├── preload.js           # Preload script
│   └── package.json
│
├── backend/                  # Python backend
│   ├── campaign_server.py   # FastAPI server
│   ├── campaign_manager.py   # Campaign orchestration
│   └── requirements.txt
│
├── python/                   # Bundled Python runtime
│   └── (PyInstaller output)
│
└── build/                    # Build outputs
    ├── mac/
    ├── win/
    └── linux/
```

---

## Self-Monitoring Features

### 1. Process Health
- **Heartbeat**: Backend sends heartbeat every 5 seconds
- **Health Endpoint**: `/api/health` returns status
- **Auto-restart**: Electron restarts Python on failure
- **Max Restarts**: Limit restarts to prevent loops

### 2. Campaign Monitoring
- **Turn Tracking**: Monitor turn progression
- **Error Detection**: Catch and log errors
- **Performance Metrics**: Track response times
- **Resource Usage**: Monitor CPU/memory

### 3. UI Indicators
- **Status Badge**: Green (running), Yellow (paused), Red (error)
- **Metrics Display**: Turns, errors, uptime
- **Log Viewer**: Real-time log display
- **Alert System**: Notifications for errors

---

## Next Steps

1. **Create Project Structure**: Set up directories
2. **Backend First**: Get FastAPI server running with campaign
3. **Electron Wrapper**: Add Electron to manage Python process
4. **SvelteKit UI**: Build campaign visualization
5. **Self-Monitoring**: Add health checks and auto-restart
6. **Packaging**: Create executable

**Recommendation**: Start with backend API, then add Electron wrapper, then build UI.

---

## Questions to Consider

1. **Campaign Duration**: How long should campaigns run?
   - Unlimited until completion?
   - Time-based limits?
   - Turn-based limits?

2. **User Interaction**: Should users be able to intervene?
   - Pause/resume?
   - Make choices?
   - Or fully automated?

3. **Persistence**: Save campaign state?
   - Resume after app restart?
   - Multiple campaigns?

4. **Distribution**: How to distribute?
   - App Store?
   - Direct download?
   - Auto-updates?

---

**This architecture gives you a self-contained, self-monitoring desktop app that runs D&D campaigns automatically. Ready to start building?**
