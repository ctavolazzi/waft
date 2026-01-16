# Docker Electron - Quick Start 🚀

**Get the Dockerized Electron app running in 2 minutes!**

---

## Prerequisites

✅ Docker installed and running  
✅ Docker Compose installed (optional)

---

## Quick Commands

### Start Electron App

```bash
cd recap_review_app/frontend
docker-compose up -d electron-app
```

### View Logs

```bash
docker-compose logs -f electron-app
```

### Stop App

```bash
docker-compose down
```

### Start with VNC (Remote Viewing)

```bash
docker-compose --profile vnc up -d electron-app-vnc
# Connect with VNC client: localhost:5900, password: electron
```

---

## Verify It's Working

```bash
# Check container is running
docker ps | grep recap-review-electron

# Check Electron process
docker exec recap-review-electron ps aux | grep electron

# View logs
docker logs recap-review-electron
```

---

## Open PDF Viewer

**Option 1: Set environment variable**
```bash
docker run -d \
  --name recap-review-electron \
  -e PDF_PATH=/app/output/recap_review.pdf \
  -v $(pwd)/../backend/output:/app/output:ro \
  recap-review-electron:latest
```

**Option 2: Use main app interface**
- Start the app normally
- Use the interface to select and view PDFs

---

## Architecture

```
Container
├── Xvfb (Virtual Display :99)
├── Electron App
│   ├── Main Process
│   └── Renderer (PDF Viewer)
└── PDF.js (Client-side rendering)
```

**Key Difference from Old rpi-electron:**
- ✅ Uses Xvfb (no host X server needed)
- ✅ Modern Node 20 + Electron 28
- ✅ Non-root user for security
- ✅ Multi-stage builds

---

## Troubleshooting

**Container won't start?**
```bash
docker-compose build --no-cache electron-app
docker-compose up -d electron-app
```

**PDF not loading?**
```bash
# Check PDF exists
docker exec recap-review-electron ls -la /app/output/
```

**Need help?**
See `DOCKER_ELECTRON_GUIDE.md` for detailed documentation.

---

**That's it! Your Electron app is Dockerized!** 🐳✨
