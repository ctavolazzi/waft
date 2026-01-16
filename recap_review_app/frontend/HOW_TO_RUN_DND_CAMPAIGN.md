# How to Run DnD Campaign in Electron

**Real Electron App - Not Browser Window!**

---

## 🎯 Quick Start

### Option 1: Docker (Recommended)

```bash
cd recap_review_app/frontend
./run_dnd_campaign.sh
```

This will:
1. Start backend in Docker
2. Open Electron app
3. Automatically open DnD Campaign window
4. Click "Start Campaign" to begin!

### Option 2: Local Development

**Terminal 1 - Backend**:
```bash
cd recap_review_app/backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Electron**:
```bash
cd recap_review_app/frontend
DND_CAMPAIGN=1 npm start
```

Then:
1. Electron opens with DnD Campaign window
2. Click "Start Campaign"
3. Watch it play!

---

## 🎮 Using the App

### From Main Window

1. Open Electron app (normal mode)
2. Go to **File → DnD Campaign** (or press `Cmd/Ctrl+D`)
3. Campaign window opens
4. Click **"Start Campaign"**
5. Watch the game play in real-time!

### Direct Campaign Mode

Run with `DND_CAMPAIGN=1` to open campaign window directly:

```bash
DND_CAMPAIGN=1 npm start
```

---

## 🏗️ Architecture

```
Electron Window (dnd-campaign.html)
    ↕ IPC
Electron Main Process
    ↕ HTTP
FastAPI Backend (port 8000)
    ↕ Subprocess
Python Campaign Script (SELF_PLAYING_CAMPAIGN_API.py)
```

### Flow

1. **User clicks "Start Campaign"** in Electron
2. **Electron → Main Process**: IPC `start-dnd-campaign`
3. **Main Process → Backend**: HTTP `POST /api/dnd-campaign/start`
4. **Backend → Python**: Starts `SELF_PLAYING_CAMPAIGN_API.py`
5. **Python → Backend**: Sends state updates via `POST /api/dnd-campaign/update`
6. **Main Process → Backend**: Polls `GET /api/dnd-campaign/state` (every 1 second)
7. **Main Process → Renderer**: Sends updates via IPC `campaign-update` event
8. **Renderer**: Updates UI in real-time

---

## ✅ What You'll See

### Real Electron Window

- **Not a browser** - Real Electron app
- **Native window** - OS-native window controls
- **Smooth updates** - No page refreshes
- **IPC communication** - Fast and efficient

### Real-Time Display

- **Party Members**: 4 characters with HP bars
- **Current Scene**: Where the party is now
- **Encounters**: All battles fought
- **Campaign Log**: Real-time event stream
- **Victory Screen**: When campaign completes

---

## 🐳 Docker Setup

### Full Stack in Docker

```bash
cd recap_review_app

# Start everything
docker-compose -f docker-compose.yml -f frontend/docker-compose.yml up -d

# Access Electron via VNC (if using VNC image)
# Connect to localhost:5900
```

### Backend Only in Docker

```bash
cd recap_review_app
docker-compose up -d backend

# Run Electron locally
cd frontend
DND_CAMPAIGN=1 npm start
```

---

## 🔧 Troubleshooting

### "Campaign not starting"

**Check**:
1. Backend is running: `curl http://localhost:8000/api/health`
2. API URL is correct: Check `API_URL` in main.js
3. Python script exists: Check `SELF_PLAYING_CAMPAIGN_API.py`

### "No updates showing"

**Check**:
1. Backend is receiving updates: Check backend logs
2. IPC is working: Check Electron DevTools console
3. Polling is active: Check network tab for `/api/dnd-campaign/state` requests

### "Docker connection issues"

**Check**:
1. Containers are on same network: `docker network ls`
2. Service names match: `backend` in docker-compose
3. Ports are exposed: `8000:8000` in docker-compose

---

## 📝 Files

### Electron
- `src/renderer/dnd-campaign.html` - Campaign UI
- `src/renderer/dnd-campaign.js` - UI logic
- `src/renderer/dnd-campaign.css` - Styling
- `src/main.js` - IPC handlers
- `src/preload.js` - API bridge

### Backend
- `backend/dnd_campaign_api.py` - API endpoints
- `backend/main.py` - Route registration

### Campaign
- `SELF_PLAYING_CAMPAIGN_API.py` - API mode script

---

## 🎯 Next: Evolve the UI

Once it's working, use `/evolve` to improve the UI:

```bash
waft evolve --target recap_review_app/frontend/src/renderer/dnd-campaign.html
```

---

**This is a REAL Electron app running the game inside Electron!** 🎉
