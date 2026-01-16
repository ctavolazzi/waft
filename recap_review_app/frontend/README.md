# Recap and Review - Electron Frontend

**Electron desktop application for mindspace documentation and review PDF generation.**

---

## Prerequisites

- **Node.js**: LTS version (18+ recommended)
- **npm**: Bundled with Node.js

**Check installation**:
```bash
node -v
npm -v
```

---

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development

```bash
npm start
# or
npm run dev
```

The Electron app will open automatically!

---

## Scripts

- `npm start` - Start the application
- `npm run dev` - Development mode (same as start)
- `npm run package` - Package app (no installer)
- `npm run dist` - Build distribution (with installer)

---

## Project Structure

```
frontend/
├── package.json          # Node.js configuration
├── src/
│   ├── main.js          # Main process (Electron)
│   ├── preload.js       # Preload script (security)
│   └── renderer/
│       ├── index.html   # UI HTML
│       ├── app.js        # UI logic
│       └── styles.css    # Styling
└── README.md
```

---

## Development

### Start Backend First

The Electron app requires the FastAPI backend to be running:

```bash
# Terminal 1 - Backend
cd ../backend
python main.py
```

### Then Start Frontend

```bash
# Terminal 2 - Frontend
npm start
```

---

## Packaging

### Using electron-builder (Current)

```bash
npm run package  # Package without installer
npm run dist     # Build with installer
```

### Using Electron Forge (Optional)

```bash
npm install --save-dev @electron-forge/cli
npx electron-forge import
npm run make     # Package
npm run publish  # Publish
```

---

## Features

- ✅ Single instance lock
- ✅ Application menu
- ✅ Progress bars
- ✅ Notifications
- ✅ Recent documents
- ✅ Dark mode support
- ✅ File dialogs
- ✅ Error handling

---

## Architecture

### Main Process (`main.js`)
- Window management
- IPC handlers
- Menu creation
- App lifecycle

### Preload Script (`preload.js`)
- Safe API exposure
- Context bridge
- Security layer

### Renderer Process (`renderer/`)
- UI logic
- User interactions
- API communication

---

## Security

- ✅ Context isolation enabled
- ✅ Node integration disabled
- ✅ Safe API exposure via contextBridge
- ✅ Preload script for IPC

---

## Troubleshooting

### App Won't Start
- Check Node.js version: `node -v` (should be 18+)
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check backend is running on port 8000

### API Not Connecting
- Verify backend is running: `curl http://127.0.0.1:8000/api/health`
- Check CORS settings in backend
- Check API_URL in main.js

### Build Errors
- Clear cache: `rm -rf node_modules dist`
- Reinstall: `npm install`
- Check electron-builder version

---

## Next Steps

1. ✅ Development setup complete
2. ⏳ Test end-to-end workflow
3. ⏳ Package for distribution
4. ⏳ Add app icon
5. ⏳ Set up auto-updater (optional)

---

**Ready for development and packaging!** ✅
