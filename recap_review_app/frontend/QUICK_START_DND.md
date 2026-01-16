# Quick Start: DnD Campaign in Electron

**Run the game in a REAL Electron window!**

---

## 🚀 Fastest Way

```bash
cd recap_review_app/frontend
./run_dnd_campaign.sh
```

**That's it!** Electron opens with the campaign window.

---

## 🎮 What Happens

1. **Backend starts** (in Docker or locally)
2. **Electron opens** with DnD Campaign window
3. **Click "Start Campaign"**
4. **Watch it play** in real-time!

---

## 📋 Manual Steps

### 1. Start Backend

```bash
cd recap_review_app/backend
uvicorn main:app --reload --port 8000
```

### 2. Start Electron

```bash
cd recap_review_app/frontend
DND_CAMPAIGN=1 npm start
```

### 3. Play!

- Click "Start Campaign"
- Watch the party fight!
- See encounters happen
- Watch leveling up
- See final boss battle
- Victory!

---

## 🐳 Docker Way

```bash
cd recap_review_app

# Start backend
docker-compose up -d backend

# Start Electron (local, connects to Docker backend)
cd frontend
DND_CAMPAIGN=1 npm start
```

---

## ✅ Verification

### Check Backend

```bash
curl http://localhost:8000/api/health
```

Should return: `{"status": "healthy", ...}`

### Check Campaign API

```bash
curl http://localhost:8000/api/dnd-campaign/state
```

Should return campaign state.

---

## 🎯 That's It!

**Real Electron app. Real-time updates. Real game playing itself!**

🎲 **Enjoy!** 🎲
