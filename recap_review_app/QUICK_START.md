# Quick Start Guide

**Get the Recap and Review app running in 5 minutes!**

---

## Step 1: Verify Prerequisites

```bash
# Check Node.js (should be 18+)
node -v

# Check npm
npm -v

# Check Python (should be 3.9+)
python3 --version
```

---

## Step 2: Install Dependencies

### Backend
```bash
cd recap_review_app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd recap_review_app/frontend
npm install
```

---

## Step 3: Start the Application

### Terminal 1 - Backend
```bash
cd recap_review_app/backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend
```bash
cd recap_review_app/frontend
npm start
```

The Electron app will open automatically! 🎉

---

## Step 4: Use the App

1. **Check API Status**: Green dot = connected, red = disconnected
2. **Select Project Path**: Click "Browse" or leave empty for current directory
3. **Generate Review**: Click "Generate Mindspace Review"
4. **View Results**: PDF opens automatically on desktop

---

## Troubleshooting

### Backend Won't Start
- Check Python version: `python3 --version`
- Activate venv: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Frontend Won't Start
- Check Node.js: `node -v` (should be 18+)
- Install dependencies: `npm install`
- Check backend is running on port 8000

### API Not Connecting
- Verify backend is running: `curl http://127.0.0.1:8000/api/health`
- Check status indicator in app (should be green)

---

## Next Steps

- Read `README.md` for full documentation
- Check `TUTORIAL_COMPLIANCE.md` for Electron tutorial alignment
- Review `ENHANCEMENTS.md` for feature list
- See `COMPLETE_FEATURES.md` for all features

---

**You're ready to go!** 🚀
