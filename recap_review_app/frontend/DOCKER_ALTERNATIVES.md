# Docker Alternatives & Additional Resources

**Date**: 2026-01-15  
**Status**: Reference Documentation

---

## Overview

This document provides information about alternative Docker approaches and additional resources for Dockerizing Electron applications.

---

## electronuserland/builder

### Official Electron Builder Docker Image

**Image**: `electronuserland/builder:base-03.25`  
**Purpose**: Building Electron applications for distribution  
**Repository**: https://github.com/electron-userland/electron-builder

### Key Features

- ✅ Complete solution for packaging Electron apps
- ✅ Cross-platform builds (macOS, Windows, Linux)
- ✅ Native dependencies compilation
- ✅ Code signing support
- ✅ Auto-update ready
- ✅ Multiple target formats (DMG, PKG, AppImage, DEB, RPM, NSIS, MSI, etc.)

### Use Case

**Best for**: Building distributable Electron applications (not running them)

**Our Use Case**: Running Electron app in Docker (different need)

**Note**: `electronuserland/builder` is for **building** Electron apps, while our Dockerfile is for **running** Electron apps. These are complementary but different use cases.

### When to Use electronuserland/builder

- Building production distributables
- CI/CD pipelines for app distribution
- Cross-platform builds from single environment
- Code signing on CI servers
- Publishing to GitHub Releases, S3, etc.

### Example Usage

```bash
# Pull the image
docker pull electronuserland/builder:base-03.25

# Build Electron app
docker run --rm -ti \
  --env-file <(env | grep -iE 'DEBUG|NODE_|ELECTRON_|YARN_|NPM_|CI|CIRCLE|TRAVIS_TAG|TRAVIS|TRAVIS_REPO_|TRAVIS_BUILD_|TRAVIS_BRANCH|TRAVIS_PULL_REQUEST|APPVEYOR|APPVEYOR_|CSC_|GH_|GITHUB_|WIN_CERT|WIN_CERT_PW|') \
  -v ${PWD}:/project \
  -v ${PWD}/dist:/project/dist \
  -v electron-builder-cache:/root/.cache/electron-builder \
  electronuserland/builder:base-03.25
```

---

## Alternative Approaches

### 1. X11 Forwarding (Old Approach)

**What**: Mount X11 socket from host  
**Pros**: Direct display access  
**Cons**: Security risks, host dependencies, not CI/CD friendly

**Example**:
```bash
xhost +local:docker
docker run -it --rm \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  electron-app
```

**Our Choice**: ❌ Not used (security concerns)

### 2. Xvfb Virtual Display (Our Approach)

**What**: Virtual framebuffer X server inside container  
**Pros**: No host deps, secure, CI/CD friendly  
**Cons**: Requires VNC for viewing (optional)

**Example**:
```dockerfile
RUN apt-get install -y xvfb
ENV DISPLAY=:99
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & npm start"]
```

**Our Choice**: ✅ Used (modern best practice)

### 3. VNC Server (Optional Addition)

**What**: Remote desktop access to container  
**Pros**: View GUI remotely, debugging  
**Cons**: Additional setup, network access needed

**Example**:
```dockerfile
RUN apt-get install -y tigervnc-standalone-server fluxbox
CMD ["vncserver :1 && npm start"]
```

**Our Choice**: ✅ Included as optional profile

---

## GitHub Resources

### Sample Repositories

1. **electron-in-docker**
   - Repository: https://github.com/trigo-at/electron-in-docker
   - Purpose: Development workflow in Docker
   - Approach: X11 forwarding

2. **sample-electron-docker**
   - Repository: https://github.com/hungpham2511/sample-electron-docker
   - Purpose: Basic Dockerized Electron example
   - Approach: Various

3. **rpi-electron** (Our Reference)
   - Repository: https://github.com/shebson/rpi-electron
   - Purpose: Raspberry Pi Electron in Docker
   - Approach: X11 forwarding (2016)
   - **Note**: This is what we modernized!

4. **docker-electron-chromedriver**
   - Repository: https://github.com/Mendeley/docker-electron-chromedriver
   - Purpose: Testing Electron apps with VNC
   - Approach: VNC server

5. **electron/build-images**
   - Repository: https://github.com/electron/build-images
   - Purpose: Official Electron CI build images
   - Approach: Build-focused

### Electron Builder Resources

- **electron-builder**: https://github.com/electron-userland/electron-builder
- **Documentation**: https://www.electron.build/
- **Docker Hub**: https://hub.docker.com/r/electronuserland/builder

---

## Comparison: Building vs Running

### electronuserland/builder (Building)

**Purpose**: Create distributable packages  
**Output**: DMG, PKG, AppImage, DEB, RPM, NSIS, MSI, etc.  
**Use Case**: CI/CD for app distribution  
**When**: Before shipping to users

**Example Workflow**:
```
Source Code → electronuserland/builder → Distributable Package
```

### Our Dockerfile (Running)

**Purpose**: Run Electron app in container  
**Output**: Running application  
**Use Case**: Development, testing, deployment  
**When**: During development or in production

**Example Workflow**:
```
Source Code → Our Dockerfile → Running Container
```

### Complementary Use

You can use both:

1. **Development/Testing**: Use our Dockerfile to run app
2. **Distribution**: Use electronuserland/builder to create packages

```bash
# Development: Run in Docker
docker-compose up -d electron-app

# Distribution: Build packages
docker run --rm -v ${PWD}:/project electronuserland/builder:base-03.25
```

---

## Integration Possibilities

### Option 1: Add Build Stage to Our Dockerfile

We could add a multi-stage build that uses `electronuserland/builder`:

```dockerfile
# Stage 1: Build distributable
FROM electronuserland/builder:base-03.25 AS builder
WORKDIR /app
COPY . .
RUN npm run build:dist

# Stage 2: Run application
FROM node:20-slim
# ... our current runtime setup ...
COPY --from=builder /app/dist ./dist
```

**Consideration**: This would make our Dockerfile more complex. Better to keep separate.

### Option 2: Separate Build Pipeline

Keep our runtime Dockerfile separate, use electronuserland/builder in CI/CD:

```yaml
# .github/workflows/build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Electron App
        run: |
          docker run --rm -v $PWD:/project \
            electronuserland/builder:base-03.25
```

**Consideration**: ✅ Recommended approach

---

## Recommendations

### For Our Use Case (Running Electron in Docker)

✅ **Keep our current approach**:
- Xvfb for virtual display
- Multi-stage builds
- Non-root user
- VNC optional

### For Building Distributables

✅ **Use electronuserland/builder**:
- In CI/CD pipelines
- For creating installers
- For cross-platform builds

### For Development

✅ **Use our Dockerfile**:
- Local development
- Testing
- Production deployment

---

## Additional Resources

### Articles

1. **Building a Docker-Containerized System Automation Desktop Application**
   - Covers: Node.js, Python, Electron.js integration
   - Approach: X11 forwarding (older method)

2. **How to develop an Electron app inside Docker**
   - Repository: electron-in-docker
   - Approach: Development workflow

### Tools

- **electron-builder**: Package and build Electron apps
- **electron-forge**: Alternative to electron-builder
- **electron-packager**: Simple packaging tool

---

## Summary

| Tool | Purpose | Our Use |
|------|---------|---------|
| **electronuserland/builder** | Build distributables | ❌ Different use case |
| **Our Dockerfile** | Run Electron app | ✅ Current approach |
| **Xvfb** | Virtual display | ✅ Used |
| **VNC** | Remote viewing | ✅ Optional |

**Key Insight**: `electronuserland/builder` is for **building** apps, our Dockerfile is for **running** apps. They're complementary but serve different purposes.

---

## Next Steps

1. ✅ Keep our current Dockerfile (for running)
2. ⏳ Consider adding electronuserland/builder to CI/CD (for building)
3. ⏳ Document build pipeline separately
4. ✅ Reference these resources in documentation

---

**Status**: Reference documentation complete

**Last Updated**: 2026-01-15
