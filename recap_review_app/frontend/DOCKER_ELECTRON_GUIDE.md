# Dockerized Electron App with PDF Viewer

**Modern Implementation Based on rpi-electron Architecture**

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Comparison: Old vs Modern](#comparison-old-vs-modern)
3. [Quick Start](#quick-start)
4. [Step-by-Step Setup](#step-by-step-setup)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## 🏗️ Architecture Overview

### Modern Dockerized Electron Architecture

```
┌─────────────────────────────────────┐
│     Docker Container                │
│  ┌──────────────────────────────┐  │
│  │  Xvfb (Virtual Framebuffer)   │  │
│  │  Display: :99                 │  │
│  └──────────────────────────────┘  │
│           │                         │
│  ┌──────────────────────────────┐  │
│  │  Electron App                │  │
│  │  - Main Process (Node.js)    │  │
│  │  - Renderer (Chromium)       │  │
│  └──────────────────────────────┘  │
│           │                         │
│  ┌──────────────────────────────┐  │
│  │  PDF.js Viewer               │  │
│  │  - PDF rendering             │  │
│  │  - Navigation controls       │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Key Components

1. **Xvfb (X Virtual Framebuffer)**
   - Provides virtual display for headless environments
   - No need for X11 server on host
   - Better for containerized environments

2. **Electron Runtime**
   - Main process: Node.js environment
   - Renderer process: Chromium-based UI
   - Secure IPC communication

3. **PDF.js Integration**
   - Client-side PDF rendering
   - No server-side dependencies
   - Full PDF viewing capabilities

---

## 🔄 Comparison: Old vs Modern

### Original rpi-electron (2016)

**Architecture:**
- X11 forwarding to host display
- Required X server on host
- Direct display access
- Raspberry Pi specific

**Dockerfile:**
```dockerfile
FROM resin/rpi-raspbian
# X11 forwarding setup
# xhost local:root
# docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY
```

**Limitations:**
- ❌ Requires X server on host
- ❌ Platform-specific (Raspberry Pi)
- ❌ Security concerns (xhost)
- ❌ Old dependencies (Node 8, Electron 1.6)

### Modern Implementation (2024-2025)

**Architecture:**
- Xvfb virtual framebuffer
- No host X server required
- Cross-platform (Linux, macOS, Windows)
- Modern dependencies

**Dockerfile:**
```dockerfile
FROM node:20-slim
# Xvfb for headless display
# No host dependencies
```

**Advantages:**
- ✅ No host X server needed
- ✅ Cross-platform compatible
- ✅ Better security (non-root user)
- ✅ Modern tooling (Node 20, Electron 28)
- ✅ Multi-stage builds
- ✅ PDF viewer integrated

---

## 🚀 Quick Start

### Prerequisites

- Docker installed and running
- Docker Compose (optional but recommended)
- Generated PDF files in `../backend/output/`

### Start Electron App

```bash
cd recap_review_app/frontend
docker-compose up -d electron-app
```

### View with VNC (Optional)

```bash
docker-compose --profile vnc up -d electron-app-vnc
# Connect with VNC client to localhost:5900
# Password: electron
```

---

## 📝 Step-by-Step Setup

### Step 1: Understand the Architecture

The modern implementation uses:

1. **Xvfb** instead of X11 forwarding
   - Virtual display server inside container
   - No host dependencies
   - Better for CI/CD and cloud environments

2. **Multi-stage Docker build**
   - Builder stage: Install dependencies
   - Runtime stage: Minimal production image

3. **Non-root user**
   - Security best practice
   - Electron runs as user `electron` (UID 1000)

### Step 2: Build the Docker Image

```bash
cd recap_review_app/frontend

# Build standard image
docker build -t recap-review-electron:latest -f Dockerfile .

# Or build VNC version
docker build -t recap-review-electron:vnc -f Dockerfile.vnc .
```

**What happens:**
1. Builder stage installs Node dependencies
2. Runtime stage adds Electron dependencies and Xvfb
3. Creates non-root user
4. Sets up display environment

### Step 3: Run the Container

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d electron-app
```

**Option B: Using Docker directly**

```bash
docker run -d \
  --name recap-review-electron \
  -e DISPLAY=:99 \
  -v $(pwd)/../backend/output:/app/output:ro \
  recap-review-electron:latest
```

### Step 4: Verify It's Running

```bash
# Check container status
docker ps | grep recap-review-electron

# View logs
docker logs recap-review-electron

# Check if Electron process is running
docker exec recap-review-electron ps aux | grep electron
```

### Step 5: Access the PDF Viewer

The Electron app will start and can:
- Display the main Recap and Review interface
- Open PDF viewer when PDF path is provided
- View generated PDFs from the backend

**To open PDF viewer directly:**

```bash
# Set PDF path environment variable
docker run -d \
  --name recap-review-electron \
  -e DISPLAY=:99 \
  -e PDF_PATH=/app/output/recap_review.pdf \
  -v $(pwd)/../backend/output:/app/output:ro \
  recap-review-electron:latest
```

---

## 📖 Usage Guide

### Basic Usage

1. **Start the container:**
   ```bash
   docker-compose up -d electron-app
   ```

2. **Generate a PDF** (if not already generated):
   ```bash
   # In another terminal, generate PDF via backend
   cd ../backend
   # Use the API or CLI to generate recap review PDF
   ```

3. **View the PDF:**
   - The Electron app will display the main interface
   - Use the PDF viewer to open generated PDFs
   - Or set `PDF_PATH` environment variable to auto-open

### VNC Access (Remote Viewing)

For remote viewing or debugging:

1. **Start VNC version:**
   ```bash
   docker-compose --profile vnc up -d electron-app-vnc
   ```

2. **Connect with VNC client:**
   - Host: `localhost`
   - Port: `5900`
   - Password: `electron`

3. **View the Electron app:**
   - You'll see the full desktop environment
   - Electron app running in Fluxbox window manager
   - Can interact with the UI remotely

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISPLAY` | X display number | `:99` |
| `PDF_PATH` | Path to PDF file to open | None |
| `NODE_ENV` | Node environment | `production` |
| `VNC_PASSWORD` | VNC access password (VNC mode) | `electron` |

### Volume Mounts

**Output Directory:**
```yaml
volumes:
  - ../backend/output:/app/output:ro
```

This mounts the backend output directory so the Electron app can access generated PDFs.

---

## 🔧 Troubleshooting

### Issue: Container exits immediately

**Check logs:**
```bash
docker logs recap-review-electron
```

**Common causes:**
- Missing dependencies
- Display server not starting
- Permission issues

**Solution:**
```bash
# Rebuild with no cache
docker-compose build --no-cache electron-app
docker-compose up -d electron-app
```

### Issue: PDF not loading

**Check:**
1. PDF file exists in mounted volume
2. File path is correct
3. File permissions allow reading

**Solution:**
```bash
# Verify PDF exists
docker exec recap-review-electron ls -la /app/output/

# Check file permissions
docker exec recap-review-electron stat /app/output/recap_review.pdf
```

### Issue: Display errors

**Error:** `Cannot connect to X server`

**Solution:**
- Ensure Xvfb is running: `docker exec recap-review-electron pgrep Xvfb`
- Check DISPLAY environment: `docker exec recap-review-electron echo $DISPLAY`
- Restart container: `docker-compose restart electron-app`

### Issue: VNC connection fails

**Check:**
1. VNC server is running: `docker exec recap-review-electron-vnc pgrep vncserver`
2. Port 5900 is accessible: `netstat -an | grep 5900`
3. Firewall allows connection

**Solution:**
```bash
# Restart VNC container
docker-compose --profile vnc restart electron-app-vnc

# Check VNC logs
docker logs recap-review-electron-vnc
```

---

## ⚙️ Advanced Configuration

### Custom Display Resolution

Edit `Dockerfile`:
```dockerfile
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 & sleep 2 && npm start"]
```

### Enable GPU Acceleration (if available)

Add to `docker-compose.yml`:
```yaml
devices:
  - /dev/dri:/dev/dri
environment:
  - LIBGL_ALWAYS_SOFTWARE=0
```

### Custom PDF Viewer Settings

Edit `src/renderer/pdf-viewer.html`:
- Change default zoom level
- Modify toolbar buttons
- Adjust color scheme

### Development Mode

For development with hot reload:

```yaml
volumes:
  - .:/app
environment:
  - NODE_ENV=development
```

---

## 📚 Architecture Deep Dive

### Why Xvfb Instead of X11?

**X11 Forwarding (Old):**
- Requires X server on host
- Security concerns (xhost)
- Platform-specific
- Complex setup

**Xvfb (Modern):**
- Self-contained in container
- No host dependencies
- Better security
- Simpler setup
- Works in CI/CD

### Security Considerations

1. **Non-root user:**
   - Electron runs as `electron` user (UID 1000)
   - Reduces attack surface

2. **Read-only mounts:**
   - Output directory mounted read-only
   - Prevents accidental modifications

3. **Minimal base image:**
   - `node:20-slim` base
   - Only necessary dependencies

4. **No network exposure:**
   - No ports exposed by default
   - VNC only when explicitly enabled

### Performance Optimization

1. **Multi-stage builds:**
   - Smaller final image
   - Faster builds with caching

2. **Layer optimization:**
   - Dependencies installed first
   - Source code copied last

3. **Minimal runtime:**
   - Only production dependencies
   - No dev tools in production

---

## 🎯 Next Steps

1. ✅ **Docker setup complete**
2. ✅ **PDF viewer integrated**
3. ⏳ **Test with generated PDFs**
4. ⏳ **Customize viewer UI**
5. ⏳ **Add more PDF features** (annotations, search, etc.)

---

## 📖 References

- [Original rpi-electron](https://github.com/shebson/rpi-electron)
- [Electron Docker Best Practices](https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci)
- [PDF.js Documentation](https://mozilla.github.io/pdf.js/)
- [Xvfb Documentation](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)

---

**Status**: ✅ **Dockerized Electron App Ready!**

The app is now containerized with modern best practices, includes a PDF viewer, and is ready to run when you get back from your run! 🏃‍♂️
