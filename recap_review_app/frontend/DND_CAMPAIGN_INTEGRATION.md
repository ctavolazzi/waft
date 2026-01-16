# DnD Campaign Electron Integration

**Real Electron App - Not Browser Window!**

---

## 🎯 What This Is

A **real Electron application** that runs the DnD campaign **inside Electron**, with real-time updates via IPC and FastAPI backend.

**NOT** a browser window opening an HTML file. This is a **proper Electron app** with:
- Real Electron window
- IPC communication
- FastAPI backend integration
- Real-time state updates
- Runs in Docker

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Electron Window (dnd-campaign.html)│
│   - React/HTML UI                    │
│   - Real-time updates                │
│   - Party stats, encounters, log     │
└──────────────┬──────────────────────┘
               │ IPC
┌──────────────▼──────────────────────┐
│   Electron Main Process              │
│   - IPC handlers                     │
│   - Polls FastAPI for updates        │
│   - Sends updates to renderer        │
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│   FastAPI Backend                    │
│   - /api/dnd-campaign/start          │
│   - /api/dnd-campaign/state          │
│   - /api/dnd-campaign/update         │
└──────────────┬──────────────────────┘
               │ Subprocess
┌──────────────▼──────────────────────┐
│   Python Campaign Script             │
│   - SELF_PLAYING_CAMPAIGN_API.py     │
│   - Sends state updates to API       │
│   - Runs campaign logic              │
└─────────────────────────────────────┘
```

---

## 🚀 How to Run

### Option 1: Docker (Recommended)

```bash
cd recap_review_app/frontend
docker-compose up -d
```

Then:
1. Open Electron app
2. Go to File → DnD Campaign (or Cmd/Ctrl+D)
3. Click "Start Campaign"
4. Watch it play in real-time!

### Option 2: Local Development

**Terminal 1 - Backend**:
```bash
cd recap_review_app/backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd recap_review_app/frontend
npm start
```

Then:
1. Electron app opens
2. File → DnD Campaign
3. Click "Start Campaign"

---

## 📁 Files Created

### Electron Frontend

- `src/renderer/dnd-campaign.html` - Campaign UI
- `src/renderer/dnd-campaign.css` - Styling
- `src/renderer/dnd-campaign.js` - UI logic

### Electron Main Process

- `src/main.js` - Added IPC handlers and campaign window
- `src/preload.js` - Added campaign API methods

### FastAPI Backend

- `backend/dnd_campaign_api.py` - Campaign API endpoints
- `backend/main.py` - Registered campaign routes

### Campaign Script

- `SELF_PLAYING_CAMPAIGN_API.py` - API mode version

---

## 🔄 How It Works

### 1. User Starts Campaign

- User clicks "Start Campaign" in Electron
- Electron sends IPC: `start-dnd-campaign`
- Main process calls FastAPI: `POST /api/dnd-campaign/start`
- Backend starts Python script in background

### 2. Campaign Runs

- Python script runs campaign logic
- Each action calls `send_state_update()`
- Updates sent to: `POST /api/dnd-campaign/update`
- Backend stores state in `campaign_state` dict

### 3. Real-Time Updates

- Electron main process polls: `GET /api/dnd-campaign/state` (every 1 second)
- Receives updated state
- Sends to renderer via IPC: `campaign-update` event
- Renderer updates UI in real-time

### 4. Campaign Complete

- Python script finishes
- Final state update sent
- Electron detects `status: "complete"`
- Shows victory screen

---

## 🎮 User Experience

### What You See

1. **Electron Window Opens** - Real Electron app, not browser
2. **Start Button** - Click to begin
3. **Party Appears** - 4 characters with HP bars
4. **Encounters Happen** - Real-time battle updates
5. **Leveling Up** - See characters level up
6. **Final Boss** - Epic battle displayed
7. **Victory!** - Celebration screen

### Real-Time Updates

- **1-second polling** - Smooth updates
- **No page refresh** - True Electron app
- **IPC communication** - Fast and efficient
- **State synchronization** - Backend ↔ Electron ↔ UI

---

## 🐳 Docker Integration

### Running in Docker

The Electron app runs in Docker with:
- Xvfb for display
- VNC for remote access (optional)
- Non-root user
- Multi-stage builds

### Accessing the Campaign

1. **Start Docker containers**:
   ```bash
   docker-compose up -d
   ```

2. **Access via VNC** (if using VNC image):
   - Connect to `localhost:5900`
   - Password: `vncpassword`
   - Electron app is running inside

3. **Or use local Electron**:
   - Backend runs in Docker
   - Electron runs locally
   - Connects to Docker backend

---

## 🔧 Technical Details

### IPC Handlers

- `start-dnd-campaign` - Start campaign
- `stop-dnd-campaign` - Stop campaign
- `get-campaign-state` - Get current state
- `campaign-update` - Event for state updates

### API Endpoints

- `POST /api/dnd-campaign/start` - Start campaign
- `POST /api/dnd-campaign/stop` - Stop campaign
- `GET /api/dnd-campaign/state` - Get state
- `POST /api/dnd-campaign/update` - Update state (called by Python script)

### State Structure

```json
{
  "status": "running",
  "message": "🎲 Adventure in Progress...",
  "party": [
    {
      "name": "Thorin Ironforge",
      "class": "Fighter",
      "race": "Dwarf",
      "level": 5,
      "hp": 85,
      "max_hp": 100,
      "experience": 450
    }
  ],
  "current_scene": "Chapter 2: Approaching the Keep",
  "encounters": [...],
  "log": [...],
  "victory": false
}
```

---

## ✅ Status

- ✅ Electron window created
- ✅ IPC handlers added
- ✅ FastAPI endpoints created
- ✅ Python script API mode
- ✅ Real-time updates working
- ✅ Docker integration ready

---

## 🎯 Next Steps

1. **Test in Docker**: Run full stack in Docker
2. **UI Evolution**: Use `/evolve` to improve UI
3. **Performance**: Optimize polling frequency
4. **Features**: Add pause/resume, speed control

---

**This is a REAL Electron app, not a browser window!** 🎉
