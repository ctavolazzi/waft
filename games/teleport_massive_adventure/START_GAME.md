# 🎮 How to Start the Game

## ⚠️ Important: Use a Web Server

**The game MUST be run from a web server**, not by opening the HTML file directly. This is because browsers block loading local files (CORS security).

## Quick Start

### Option 1: Python HTTP Server (Recommended)

```bash
cd games/teleport_massive_adventure
python3 -m http.server 8000
```

Then open: **http://localhost:8000/index_v2.html**

### Option 2: Node.js HTTP Server

```bash
cd games/teleport_massive_adventure
npx http-server -p 8000
```

Then open: **http://localhost:8000/index_v2.html**

### Option 3: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index_v2.html`
3. Select "Open with Live Server"

## What You'll See

1. **Loading Screen** - Progress bar and loading tips
2. **Lab Scene** - Starting location with Aziah
3. **AutoPlayer Button** - Top-left corner "▶ AUTO" button
4. **Game Assets** - All sprites, objects, and UI elements

## Troubleshooting

### "Boxes moving but no assets"

This means you opened the file directly (`file://`). **Use a web server instead!**

### "404 errors in console"

Check that you're in the correct directory when starting the server:
```bash
cd games/teleport_massive_adventure
python3 -m http.server 8000
```

### "Assets not loading"

1. Check browser console (F12) for errors
2. Verify assets exist: `ls assets/characters/*/frames/*.png`
3. Make sure server is running: `curl http://localhost:8000/index_v2.html`

## AutoPlayer

Once the game loads:
1. Click **"▶ AUTO"** button (top-left)
2. Watch the automated playthrough
3. Check the log area for progress

Enjoy! 🎮
