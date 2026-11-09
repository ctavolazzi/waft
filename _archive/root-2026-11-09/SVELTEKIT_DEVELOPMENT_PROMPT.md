# SvelteKit Development UI - Continuation Prompt

Use this prompt in a new chat to continue developing the SvelteKit development UI for the Waft project.

---

## Project Context

**Waft** is an "Ambient, self-modifying Meta-Framework for Python" that orchestrates:
- **Environment** (`uv`) - Python package management
- **Memory** (`_pyrite`) - Persistent project structure (active/, backlog/, standards/)
- **Agents** (`crewai`) - AI agent capabilities (optional)
- **Epistemic Tracking** (`Empirica`) - Knowledge and learning measurement
- **Gamification** (`TavernKeeper`) - RPG mechanics for development

**Repository**: `/Users/ctavolazzi/Code/active/waft`

**Current State**: There's an existing SvelteKit visualizer project started in `visualizer/` directory with basic structure, but needs continued development.

---

## Current Implementation Status

### Backend (Python/FastAPI)
- ✅ FastAPI application in `src/waft/api/main.py`
- ✅ API routes in `src/waft/api/routes/`:
  - `state.py` - Project state endpoints
  - `git.py` - Git status and information
  - `work_efforts.py` - Work effort management
  - `empirica.py` - Epistemic tracking data
- ✅ CORS configured for `localhost:5173` and `localhost:3000`
- ✅ Static file serving support for SvelteKit build output
- ✅ Backend integrated with existing Waft managers:
  - `MemoryManager` - _pyrite structure management
  - `SubstrateManager` - Project metadata and dependencies
  - `GitHubManager` - Git operations
  - `GamificationManager` - TavernKeeper RPG mechanics
  - `EmpiricaManager` - Epistemic tracking

### Frontend (SvelteKit)
- ✅ SvelteKit project initialized in `visualizer/` directory
- ✅ TypeScript configured
- ✅ Tailwind CSS configured
- ✅ Basic structure:
  - `src/routes/+page.svelte` - Main dashboard page
  - `src/routes/+layout.svelte` - Layout wrapper
  - `src/lib/components/cards/` - Card components:
    - `StatusCard.svelte`
    - `GitCard.svelte`
    - `HealthCard.svelte`
    - `PyriteCard.svelte`
    - `GamificationCard.svelte`
    - `WorkEffortsCard.svelte`
  - `src/lib/components/layout/` - Layout components:
    - `AppShell.svelte`
    - `Navbar.svelte`
    - `Footer.svelte`
  - `src/lib/components/status/` - Status components:
    - `Badge.svelte`
    - `ProgressBar.svelte`
  - `src/lib/stores/projectStore.ts` - Svelte store for project state
  - `src/lib/api/client.ts` - API client using axios

### Existing Web Server
- ✅ `src/waft/web.py` - Simple HTTP server with HTML dashboard (legacy)
- ✅ `waft serve` command - Starts server on port 8000
- ✅ Supports `--dev` mode with live reloading
- ⚠️ **Goal**: Replace this with FastAPI + SvelteKit

---

## Development Goals

### Primary Objective
Build a modern, interactive SvelteKit development UI that:
1. **Replaces** the current simple HTML dashboard in `src/waft/web.py`
2. **Integrates** with the existing FastAPI backend (`src/waft/api/`)
3. **Displays** comprehensive project information
4. **Provides** interactive features for project management

### Key Features to Implement

1. **Dashboard Overview**
   - Project information (name, version, path)
   - Git status (branch, uncommitted changes, recent commits)
   - _pyrite structure visualization (active/, backlog/, standards/)
   - Project health indicators
   - Gamification stats (TavernKeeper insights, integrity, level)
   - Work efforts listing and status

2. **Interactive Features**
   - Real-time updates (WebSocket or polling)
   - File browsing in _pyrite structure
   - Work effort management (view, create, update)
   - Git operations (status, diff viewing)
   - Project health monitoring
   - Command execution interface (optional)

3. **UI/UX Requirements**
   - Dark mode theme (matching existing dashboard)
   - Responsive design (mobile-friendly)
   - Modern, clean interface
   - Fast loading and smooth interactions
   - Accessible components

---

## Technical Stack

### Frontend
- **SvelteKit** (v2.5.0) - Framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Svelte Stores** - State management

### Backend
- **FastAPI** - API framework
- **Python 3.10+** - Backend language
- **Existing Waft Managers** - Business logic

### Development
- **Vite** - Build tool (via SvelteKit)
- **Port 5173** - Dev server (SvelteKit)
- **Port 8000** - API server (FastAPI)

---

## Project Structure

```
waft/
├── visualizer/                    # SvelteKit frontend
│   ├── src/
│   │   ├── routes/               # SvelteKit routes
│   │   │   ├── +page.svelte      # Main dashboard
│   │   │   └── +layout.svelte    # Layout wrapper
│   │   ├── lib/
│   │   │   ├── components/       # Reusable components
│   │   │   │   ├── cards/        # Card components
│   │   │   │   ├── layout/       # Layout components
│   │   │   │   └── status/       # Status components
│   │   │   ├── stores/           # Svelte stores
│   │   │   │   └── projectStore.ts
│   │   │   └── api/              # API client
│   │   │       └── client.ts
│   │   └── app.css               # Global styles
│   ├── package.json
│   └── vite.config.js
│
├── src/waft/
│   ├── api/                      # FastAPI backend
│   │   ├── main.py               # FastAPI app creation
│   │   └── routes/               # API route handlers
│   │       ├── state.py          # Project state
│   │       ├── git.py            # Git operations
│   │       ├── work_efforts.py   # Work efforts
│   │       └── empirica.py       # Epistemic tracking
│   ├── core/                     # Business logic
│   │   ├── memory.py             # MemoryManager
│   │   ├── substrate.py          # SubstrateManager
│   │   ├── github.py             # GitHubManager
│   │   ├── gamification.py      # GamificationManager
│   │   └── empirica.py           # EmpiricaManager
│   └── web.py                    # Legacy HTTP server (to be replaced)
```

---

## Integration Points

### API Endpoints Available

The FastAPI backend provides these endpoints (check `src/waft/api/routes/` for details):

- `/api/state` - Project state information
- `/api/git/*` - Git status, commits, branches
- `/api/work-efforts/*` - Work effort CRUD operations
- `/api/empirica/*` - Epistemic tracking data

### Data Models

Key data structures to work with:

1. **Project State**:
   - Project name, version, path
   - _pyrite structure status
   - Template status
   - Dependencies

2. **Git Information**:
   - Current branch
   - Uncommitted changes
   - Recent commits
   - Branch relationships

3. **Work Efforts**:
   - Active work efforts
   - Status (active, completed, paused)
   - Tickets and progress

4. **Gamification**:
   - Integrity score
   - Insight points
   - Level progression
   - TavernKeeper stats

5. **Empirica**:
   - Session data
   - Epistemic vectors
   - Learning metrics

---

## Development Workflow

### Starting Development

1. **Start FastAPI backend**:
   ```bash
   cd /Users/ctavolazzi/Code/active/waft
   waft serve --dev  # Should use FastAPI + SvelteKit when ready
   # Or run FastAPI directly if implemented
   ```

2. **Start SvelteKit dev server**:
   ```bash
   cd visualizer/
   npm install  # If needed
   npm run dev  # Runs on http://localhost:5173
   ```

3. **Development**:
   - Frontend: `visualizer/src/`
   - Backend API: `src/waft/api/`
   - Backend routes: `src/waft/api/routes/`

### Building for Production

1. **Build SvelteKit**:
   ```bash
   cd visualizer/
   npm run build  # Outputs to build/
   ```

2. **Serve with FastAPI**:
   - FastAPI should serve static files from `visualizer/build/`
   - Configured in `src/waft/api/main.py`

---

## Design Guidelines

### Color Scheme (Dark Mode)
- **Background**: Dark gradient (#1a1a2e → #16213e → #0f3460)
- **Cards**: Dark (#1e1e2e) with subtle borders (#2d2d3e)
- **Text**: Light (#e0e0e0 primary, #a0a0a0 secondary)
- **Accents**: Blue (#7c9eff) for highlights
- **Status Badges**: Dark mode optimized colors

### Component Patterns
- Use existing card components as templates
- Follow SvelteKit conventions for routing
- Use Svelte stores for shared state
- Keep components focused and reusable

---

## Key Files to Review

1. **Backend API**:
   - `src/waft/api/main.py` - FastAPI app setup
   - `src/waft/api/routes/state.py` - State endpoints
   - `src/waft/api/routes/git.py` - Git endpoints
   - `src/waft/api/routes/work_efforts.py` - Work effort endpoints

2. **Frontend**:
   - `visualizer/src/routes/+page.svelte` - Main dashboard
   - `visualizer/src/lib/stores/projectStore.ts` - State management
   - `visualizer/src/lib/api/client.ts` - API client
   - `visualizer/src/lib/components/cards/*.svelte` - Card components

3. **Legacy Reference**:
   - `src/waft/web.py` - Current HTML dashboard (reference for features)
   - `_work_efforts/WEB_DASHBOARD.md` - Dashboard documentation

---

## Next Steps

1. **Review existing code** in `visualizer/` and `src/waft/api/`
2. **Understand API endpoints** available in backend
3. **Build out dashboard** using existing components as foundation
4. **Integrate real-time updates** (polling or WebSocket)
5. **Add interactive features** (file browsing, work effort management)
6. **Test integration** between frontend and backend
7. **Replace legacy server** in `src/waft/web.py` with FastAPI + SvelteKit

---

## Questions to Consider

- Should we use WebSocket for real-time updates or polling?
- What interactive features are most valuable?
- How should we handle file editing/viewing in the UI?
- Should command execution be available in the UI?
- How to handle multiple projects/workspaces?

---

## Resources

- **Waft README**: `/Users/ctavolazzi/Code/active/waft/README.md`
- **Dashboard Docs**: `/Users/ctavolazzi/Code/active/waft/_work_efforts/WEB_DASHBOARD.md`
- **SvelteKit Docs**: https://kit.svelte.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Tailwind CSS**: https://tailwindcss.com/

---

**Start by reviewing the existing code, understanding the API structure, and then building out the dashboard features incrementally. Focus on making it a modern, interactive replacement for the current simple HTML dashboard.**
