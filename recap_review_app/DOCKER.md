# Docker Setup Guide

**Docker configuration for Recap and Review application.**

---

## Quick Start

### Start Backend with Docker

```bash
cd recap_review_app
docker-compose up -d backend
```

The backend will be available at `http://localhost:8000`

### Start with Development Mode (Hot Reload)

```bash
docker-compose --profile dev up -d backend-dev
```

Backend will be available at `http://localhost:8001` with hot reload enabled.

---

## Docker Services

### Backend Service

**Production**:
- Container: `recap-review-backend`
- Port: `8000`
- Image: Built from `backend/Dockerfile`

**Development**:
- Container: `recap-review-backend-dev`
- Port: `8001`
- Image: Built from `backend/Dockerfile.dev`
- Hot reload: Enabled

---

## Commands

### Build and Start

```bash
# Build and start backend
docker-compose up -d backend

# Build and start with development mode
docker-compose --profile dev up -d backend-dev

# Build without cache
docker-compose build --no-cache backend
```

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# Development backend logs
docker-compose logs -f backend-dev
```

### Stop Services

```bash
# Stop backend
docker-compose stop backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Restart Services

```bash
# Restart backend
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend
```

---

## Volumes

### Mounted Volumes

1. **Project Root** (`../:/workspace:ro`)
   - Read-only access to WAFT project
   - Allows backend to access WAFT modules
   - Used for mindspace data gathering

2. **Output Directory** (`./backend/output:/app/output`)
   - Writable directory for generated files
   - PDFs and markdown files saved here
   - Accessible from host

---

## Environment Variables

### Backend Environment

- `PYTHONUNBUFFERED=1` - Unbuffered Python output
- `ENVIRONMENT=development` - Development mode (dev only)

### Custom Environment

Create `.env` file in `recap_review_app/`:

```env
# Backend
BACKEND_PORT=8000
PYTHONUNBUFFERED=1

# Development
ENVIRONMENT=development
```

Then use in docker-compose:
```yaml
environment:
  - ENVIRONMENT=${ENVIRONMENT:-production}
```

---

## Health Checks

The backend includes health check:

```bash
# Check health
curl http://localhost:8000/api/health

# Or via Docker
docker-compose exec backend curl http://localhost:8000/api/health
```

---

## Development Workflow

### Option 1: Docker Backend + Local Frontend

**Terminal 1 - Docker Backend**:
```bash
cd recap_review_app
docker-compose --profile dev up backend-dev
```

**Terminal 2 - Local Frontend**:
```bash
cd recap_review_app/frontend
npm start
```

### Option 2: Docker Backend + Local Frontend (Production)

**Terminal 1 - Docker Backend**:
```bash
cd recap_review_app
docker-compose up -d backend
```

**Terminal 2 - Local Frontend**:
```bash
cd recap_review_app/frontend
npm start
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Check if container is running
docker-compose ps

# Rebuild container
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8002:8000"  # Use different host port
```

### Permission Issues

```bash
# Fix output directory permissions
sudo chown -R $USER:$USER recap_review_app/backend/output
```

### Volume Mount Issues

```bash
# Check if volumes are mounted
docker-compose exec backend ls -la /workspace
docker-compose exec backend ls -la /app/output
```

---

## Building Images

### Build Backend Image

```bash
cd recap_review_app/backend
docker build -t recap-review-backend:latest .
```

### Build Development Image

```bash
cd recap_review_app/backend
docker build -f Dockerfile.dev -t recap-review-backend:dev .
```

---

## Running Containers Directly

### Run Backend Container

```bash
docker run -d \
  --name recap-review-backend \
  -p 8000:8000 \
  -v $(pwd)/../:/workspace:ro \
  -v $(pwd)/output:/app/output \
  recap-review-backend:latest
```

### Run with Environment Variables

```bash
docker run -d \
  --name recap-review-backend \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd)/../:/workspace:ro \
  -v $(pwd)/output:/app/output \
  recap-review-backend:latest
```

---

## Production Deployment

### Build for Production

```bash
# Build production image
docker build -t recap-review-backend:prod ./backend

# Tag for registry
docker tag recap-review-backend:prod your-registry/recap-review-backend:latest

# Push to registry
docker push your-registry/recap-review-backend:latest
```

### Run Production Container

```bash
docker run -d \
  --name recap-review-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /path/to/waft:/workspace:ro \
  -v /path/to/output:/app/output \
  your-registry/recap-review-backend:latest
```

---

## Docker Compose Overrides

### Development Override

Create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - ./backend:/app  # Mount for hot reload
```

This file is automatically used by docker-compose.

---

## Network Configuration

### Default Network

Services use `recap-review-network` bridge network.

### Custom Network

```yaml
networks:
  custom-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

---

## Resource Limits

### Add Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## Logging

### View Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Log Configuration

Add to docker-compose.yml:
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Cleanup

### Remove Containers

```bash
# Stop and remove
docker-compose down

# Remove volumes too
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Clean Docker System

```bash
# Remove unused containers, networks, images
docker system prune

# Remove everything (including volumes)
docker system prune -a --volumes
```

---

## Integration with Electron Frontend

The Electron frontend connects to the Dockerized backend:

1. **Backend in Docker**: `http://localhost:8000`
2. **Frontend Local**: Connects to `http://127.0.0.1:8000`
3. **No Changes Needed**: Frontend works as-is

---

## Next Steps

1. ✅ Dockerfile created
2. ✅ docker-compose.yml created
3. ✅ Development Dockerfile created
4. ⏳ Test Docker setup
5. ⏳ Add health checks
6. ⏳ Optimize image size
7. ⏳ Add multi-stage builds (optional)

---

**Docker setup complete! Ready for containerized deployment.** 🐳
