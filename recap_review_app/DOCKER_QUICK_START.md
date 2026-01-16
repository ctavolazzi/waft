# Docker Quick Start

**Get the Dockerized backend running in 2 minutes!**

---

## Quick Commands

### Start Backend

```bash
cd recap_review_app
docker-compose up -d backend
```

### Start Development Backend (Hot Reload)

```bash
cd recap_review_app
docker-compose --profile dev up -d backend-dev
```

### View Logs

```bash
docker-compose logs -f backend
```

### Stop Backend

```bash
docker-compose down
```

---

## Using Makefile

```bash
# Build
make build

# Start
make up

# Start dev
make up-dev

# View logs
make logs

# Stop
make down

# Check health
make health
```

---

## Using Helper Scripts

```bash
# Start backend
./scripts/docker-start.sh

# Start development backend
./scripts/docker-start.sh --dev

# Stop backend
./scripts/docker-stop.sh
```

---

## Verify It's Working

```bash
# Check health
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","service":"recap-and-review-api","version":"1.0.0"}
```

---

## Then Start Frontend

```bash
cd recap_review_app/frontend
npm start
```

The Electron app will connect to the Dockerized backend automatically!

---

**That's it! Backend is running in Docker.** 🐳
