# WAFT Desktop - Quick Start Guide

**Get the WAFT Desktop app running in 3 steps!**

---

## Step 1: Install Dependencies

```bash
cd waft_desktop/electron
npm install

cd ../frontend
npm install
```

---

## Step 2: Start Development

### Option A: Use the Startup Script (Recommended)

```bash
cd waft_desktop
./START_DEV.sh
```

This will:
- Start the SvelteKit frontend dev server (port 5173)
- Launch the Electron app
- Electron will automatically spawn the WAFT backend

### Option B: Manual Start (3 Terminals)

**Terminal 1 - Frontend**:
```bash
cd waft_desktop/frontend
npm run dev
```

**Terminal 2 - Electron**:
```bash
cd waft_desktop/electron
npm start
```

**Terminal 3 - Backend (Optional, Electron auto-starts it)**:
```bash
cd /path/to/waft
waft serve --port 8000
```

---

## Step 3: Use the App!

The Electron app will open automatically. You'll see:

- **Backend Status**: Running/Stopped indicator
- **Health Status**: Healthy/Unhealthy indicator
- **System Information**: PID, port, uptime
- **Backend Controls**: Restart button
- **Backend Logs**: Real-time log output

---

## What's Happening?

1. **Electron** spawns the WAFT Python backend as a child process
2. **Backend** runs FastAPI server on `localhost:8000`
3. **Frontend** (SvelteKit) runs on `localhost:5173` (dev mode)
4. **Electron** loads the frontend and provides IPC bridge
5. **Health checks** run every 5 seconds automatically

---

## Troubleshooting

### Backend Not Starting

- Check WAFT is installed: `waft --version`
- Check Python is available: `python3 --version`
- Check Electron console for errors (View → Toggle Developer Tools)

### Frontend Not Loading

- Ensure frontend dev server is running: `cd frontend && npm run dev`
- Check port 5173 is available
- Check Electron console for errors

### Port Conflicts

- Backend port 8000: Change in `electron/main.js` (line ~15)
- Frontend port 5173: Change in `frontend/vite.config.js`

---

## Next Steps

- Add project management UI
- Add work effort dashboard
- Add project creation/opening
- Add real-time updates via WebSocket

---

**Ready to build!** 🚀
