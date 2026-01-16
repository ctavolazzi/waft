# Electron App - D&D Campaign Desktop App

**Main process for the desktop application.**

---

## Features

- ✅ **Python Backend Management**: Spawns and monitors Python backend process
- ✅ **Health Monitoring**: Checks backend health every 5 seconds
- ✅ **Auto-Restart**: Automatically restarts backend on crashes (max 5 attempts)
- ✅ **Process Monitoring**: Tracks backend status and metrics
- ✅ **IPC Communication**: Secure communication with renderer process
- ✅ **Single Instance**: Prevents multiple app instances

---

## Architecture

```
Electron Main Process (main.js)
  ├── BackendManager
  │   ├── Spawns Python backend
  │   ├── Monitors process health
  │   ├── Auto-restart on crashes
  │   └── Health check every 5s
  ├── Window Management
  │   ├── Creates main window
  │   └── Loads SvelteKit frontend
  └── IPC Handlers
      ├── backend-status
      ├── backend-restart
      └── backend-health-check
```

---

## Setup

```bash
npm install
```

---

## Running

### Development

```bash
npm start
# or
npm run dev
```

**Note**: Make sure SvelteKit frontend is running on `http://localhost:5173`

### Production Build

```bash
npm run build
```

---

## Backend Management

The Electron app automatically:
1. Spawns Python backend on startup
2. Monitors health every 5 seconds
3. Auto-restarts on crashes (max 5 attempts)
4. Sends status updates to frontend via IPC

---

## IPC API

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

- **API_URL**: `http://127.0.0.1:8000` (backend FastAPI server)
- **Health Check Interval**: 5 seconds
- **Max Restart Attempts**: 5
- **Restart Delay**: 2 seconds

---

## Troubleshooting

### Backend won't start
- Check Python is installed: `python3 --version`
- Check backend path is correct
- Check backend dependencies: `pip install -r backend/requirements.txt`

### Backend keeps crashing
- Check backend logs in Electron console
- Check Python backend logs
- Verify CampaignOrchestrator is available

### Health check fails
- Verify backend is running: `curl http://127.0.0.1:8000/api/health`
- Check firewall/port blocking
- Check backend logs for errors
