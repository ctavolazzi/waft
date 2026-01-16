# Setup Guide: Recap and Review Full Stack Application

## Quick Start

### 1. Backend Setup

```bash
cd recap_review_app/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd recap_review_app/frontend
npm install
```

### 3. Run the Application

**Terminal 1 - Start Backend**:
```bash
cd recap_review_app/backend
source venv/bin/activate
python main.py
# Or: uvicorn main:app --reload --port 8000
```

**Terminal 2 - Start Frontend**:
```bash
cd recap_review_app/frontend
npm run dev
```

The Electron app will open automatically!

---

## Testing the Command

You can also test the command directly:

```bash
cd /Users/ctavolazzi/Code/active/waft
python3 -m waft recap-and-review
```

This will:
1. Capture current mindspace
2. Generate markdown document
3. Generate PDF (if dependencies available)
4. Open PDF on desktop

---

## Dependencies

### Backend
- Python 3.9+
- FastAPI
- Uvicorn
- WeasyPrint (for PDF generation)
- Markdown

### Frontend
- Node.js 18+
- Electron
- Axios

---

## Troubleshooting

### PDF Generation Not Working

If PDF generation fails, install:
```bash
# macOS
brew install cairo pango gdk-pixbuf libffi

# Then reinstall weasyprint
pip install --upgrade weasyprint
```

### API Not Connecting

1. Check backend is running on port 8000
2. Check CORS settings in `backend/main.py`
3. Verify API health: `curl http://127.0.0.1:8000/api/health`

### Electron App Not Opening

1. Check Node.js version: `node --version` (should be 18+)
2. Reinstall dependencies: `npm install`
3. Check for errors in terminal

---

## Next Steps

1. ✅ Command created: `/recap-and-review`
2. ✅ Full stack app structure created
3. ⏳ Test command functionality
4. ⏳ Test full stack app
5. ⏳ Add file browser dialog
6. ⏳ Enhance UI/UX
7. ⏳ Package for distribution

---

**The application is ready for testing!**
