# WAFT API & UI System

A robust local API server with SvelteKit UI for managing WAFT projects.

## Architecture

- **Backend**: FastAPI server (`src/waft/api/`) running on port 8000
- **Frontend**: SvelteKit application (`visualizer/`) running on port 8781
- **Authentication**: Bearer token-based auth with automatic handshake

## Quick Start

### Option 1: Start Everything (Recommended)

```bash
./scripts/start_waft_full.sh
```

This starts both the API server and UI automatically.

### Option 2: Start Separately

**Terminal 1 - API Server:**
```bash
./scripts/start_waft_server.sh
# Or manually:
waft serve --port 8000
```

**Terminal 2 - UI:**
```bash
./scripts/start_waft_ui.sh
# Or manually:
cd visualizer && npm run dev
```

## Access Points

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **UI Dashboard**: http://localhost:8781

## Authentication

The system uses a secure handshake mechanism:

1. **First Time**: UI automatically performs handshake on load
2. **Token Storage**: Token is stored in browser localStorage
3. **Auto-Auth**: Subsequent requests include token automatically
4. **Token File**: Server stores token in `.waft_api_token` (project root)

### Manual Handshake

```bash
curl -X POST http://localhost:8000/api/auth/handshake \
  -H "Content-Type: application/json" \
  -d '{"client_name": "My Client", "client_version": "1.0.0"}'
```

### Verify Token

```bash
curl -X GET http://localhost:8000/api/auth/verify \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## API Endpoints

### Core Endpoints

- `GET /api/health` - Health check
- `GET /api/state` - Project state
- `GET /api/git` - Git status
- `GET /api/work-efforts` - Work efforts list

### Projects (CRUD)

- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project by ID
- `GET /api/projects/stats` - Project statistics

### Authentication

- `POST /api/auth/handshake` - Perform handshake
- `GET /api/auth/verify` - Verify token
- `GET /api/auth/info` - Auth info (public)

### Other Endpoints

- `/api/decision/*` - Decision Engine
- `/api/gym/*` - Gym/RPG system
- `/api/being/*` - Being system
- `/api/campfire/*` - Campfire stories
- `/api/empirica/*` - Empirica tracking

## Development

### API Development

```bash
# Start with auto-reload
waft serve --port 8000 --dev

# Or use uvicorn directly
uvicorn src.waft.api.main:app --reload --port 8000
```

### UI Development

```bash
cd visualizer
npm install  # First time only
npm run dev
```

### Adding New API Endpoints

1. Create route file in `src/waft/api/routes/`
2. Add router to `src/waft/api/main.py`
3. Add client method in `visualizer/src/lib/api/client.ts`
4. Use in UI components

## Security Notes

- **Local Only**: This is designed for local development
- **Token File**: `.waft_api_token` has 600 permissions (owner read/write only)
- **HTTPS**: Not configured by default (local development)
- **Production**: Replace auth system with proper OAuth/JWT for production use

## Troubleshooting

### API Not Responding

1. Check if server is running: `curl http://localhost:8000/api/health`
2. Check port conflicts: `lsof -i :8000`
3. Check logs: Server outputs to console

### UI Can't Connect

1. Verify API is running on port 8000
2. Check browser console for errors
3. Verify Vite proxy config in `visualizer/vite.config.js`
4. Try manual handshake: `curl -X POST http://localhost:8000/api/auth/handshake`

### Token Issues

1. Delete `.waft_api_token` to generate new token
2. Clear browser localStorage
3. Refresh page to trigger new handshake

## Scripts

- `scripts/start_waft_server.sh` - Start API server only
- `scripts/start_waft_ui.sh` - Start UI only
- `scripts/start_waft_full.sh` - Start both (recommended)

## Next Steps

- [ ] Add CRUD operations for work efforts
- [ ] Add project creation/editing UI
- [ ] Add real-time updates via WebSockets
- [ ] Add file upload/download endpoints
- [ ] Enhance error handling and retry logic
