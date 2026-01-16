# 🐳 Dockerized Electron App - README

**Quick reference for running the Electron app in Docker**

---

## 🚀 Start the App

```bash
cd recap_review_app/frontend
docker-compose up -d electron-app
```

## 📄 View Generated PDFs

The app can automatically open PDFs when they're generated. PDFs are mounted from `../backend/output/`.

**To open a specific PDF:**
```bash
docker run -d \
  --name recap-review-electron \
  -e PDF_PATH=/app/output/recap_review.pdf \
  -v $(pwd)/../backend/output:/app/output:ro \
  recap-review-electron:latest
```

## 🔍 View with VNC (Remote Desktop)

```bash
docker-compose --profile vnc up -d electron-app-vnc
```

**Connect:**
- Host: `localhost`
- Port: `5900`
- Password: `electron`

Use any VNC client (TigerVNC, RealVNC, etc.)

## 📚 Documentation

- **Quick Start**: `DOCKER_QUICK_START.md`
- **Complete Guide**: `DOCKER_ELECTRON_GUIDE.md`
- **Architecture**: `ARCHITECTURE_COMPARISON.md`

## 🏗️ Architecture

Based on `rpi-electron` but modernized:
- ✅ Xvfb (virtual display) instead of X11 forwarding
- ✅ Node 20 + Electron 28 (vs Node 8 + Electron 1.6)
- ✅ Non-root user for security
- ✅ PDF.js viewer integrated
- ✅ Cross-platform support

---

**Ready to run!** 🎯
