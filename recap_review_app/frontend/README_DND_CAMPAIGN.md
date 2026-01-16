# DnD Campaign in Electron - README

**Real Electron App - Not Browser Window!**

---

## 🎯 What This Is

A **complete Electron application** that runs the self-playing DnD campaign **inside Electron** with real-time updates.

**Key Points**:
- ✅ **Real Electron window** (not browser)
- ✅ **IPC communication** (not HTTP polling from renderer)
- ✅ **FastAPI backend** integration
- ✅ **Real-time updates** via polling
- ✅ **Docker support** for full stack

---

## 🚀 Quick Start

### Option 1: Script (Easiest)

```bash
cd recap_review_app/frontend
./run_dnd_campaign.sh
```

### Option 2: Manual

**Terminal 1**:
```bash
cd recap_review_app/backend
uvicorn main:app --reload --port 8000
```

**Terminal 2**:
```bash
cd recap_review_app/frontend
DND_CAMPAIGN=1 npm start
```

### Option 3: From Menu

1. Start Electron normally: `npm start`
2. Go to **File → DnD Campaign** (or `Cmd/Ctrl+D`)
3. Click **"Start Campaign"**

---

## 🏗️ How It Works

### Architecture Flow

```
User clicks "Start Campaign"
    ↓
Electron Renderer → IPC → Electron Main Process
    ↓
Main Process → HTTP → FastAPI Backend
    ↓
Backend → Subprocess → Python Script
    ↓
Python Script → HTTP → Backend (state updates)
    ↓
Backend → HTTP → Main Process (polling)
    ↓
Main Process → IPC → Renderer (updates)
    ↓
UI Updates in Real-Time!
```

### Components

1. **Electron Renderer** (`dnd-campaign.html/js`)
   - UI display
   - Button handlers
   - Real-time UI updates

2. **Electron Main Process** (`main.js`)
   - IPC handlers
   - HTTP client (axios)
   - State polling (1s interval)
   - IPC events to renderer

3. **FastAPI Backend** (`dnd_campaign_api.py`)
   - REST API endpoints
   - State management
   - Process management
   - State storage

4. **Python Script** (`SELF_PLAYING_CAMPAIGN_API.py`)
   - Campaign logic
   - State updates via HTTP
   - Same game, API mode

---

## 📊 State Flow

### Starting Campaign

1. User clicks "Start Campaign"
2. Renderer → Main: `start-dnd-campaign` IPC
3. Main → Backend: `POST /api/dnd-campaign/start`
4. Backend starts Python script
5. Main starts polling loop

### During Campaign

1. Python script runs campaign
2. Each action calls `send_state_update()`
3. Updates sent to: `POST /api/dnd-campaign/update`
4. Backend stores in `campaign_state` dict
5. Main polls: `GET /api/dnd-campaign/state` (every 1s)
6. Main sends IPC: `campaign-update` event
7. Renderer updates UI

### Campaign Complete

1. Python script finishes
2. Final state update sent
3. Main detects `status: "complete"`
4. Victory screen shown

---

## 🎮 User Experience

### What You See

- **Real Electron Window** - Native OS window
- **Beautiful UI** - D&D themed with gradients
- **Party Display** - 4 characters with HP bars
- **Current Scene** - Where the party is
- **Encounters** - All battles fought
- **Campaign Log** - Real-time event stream
- **Victory Screen** - When complete

### Real-Time Updates

- **1-second polling** - Smooth updates
- **No page refresh** - True Electron app
- **IPC events** - Fast communication
- **State sync** - Backend ↔ Electron ↔ UI

---

## 🐳 Docker

### Full Stack

```bash
cd recap_review_app
docker-compose -f docker-compose.yml -f frontend/docker-compose.yml up -d
```

### Backend Only

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
1. Backend running: `curl http://localhost:8000/api/health`
2. API URL correct: Check `API_URL` in main.js
3. Script exists: `SELF_PLAYING_CAMPAIGN_API.py`

### "No updates showing"

**Check**:
1. Backend receiving updates: Check logs
2. IPC working: Check DevTools console
3. Polling active: Check network tab

### "Docker issues"

**Check**:
1. Containers on same network
2. Service names match (`backend`)
3. Ports exposed (`8000:8000`)

---

## 📝 Files

- `src/renderer/dnd-campaign.html` - UI
- `src/renderer/dnd-campaign.js` - Logic
- `src/renderer/dnd-campaign.css` - Styling
- `src/main.js` - IPC handlers
- `backend/dnd_campaign_api.py` - API
- `SELF_PLAYING_CAMPAIGN_API.py` - Script

---

## ✅ Status

**COMPLETE** - Real Electron app integration ready!

---

**This is a REAL Electron app, not a browser window!** 🎉
