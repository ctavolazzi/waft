---
name: SvelteKit Visualizer Migration
overview: Migrate the Waft visualizer from static HTML generation to a modern SvelteKit application, leveraging patterns from reference repos to create a user-friendly, feature-rich development dashboard.
todos:
  - id: setup-sveltekit
    content: Initialize SvelteKit project in visualizer/ directory with TypeScript and Tailwind CSS
    status: completed
  - id: setup-fastapi
    content: Create FastAPI backend module (src/waft/api/) with CORS and base router
    status: completed
  - id: create-api-endpoints
    content: "Create API endpoints: /api/state, /api/git, /api/work-efforts, /api/empirica"
    status: completed
  - id: build-layout-components
    content: Create AppShell, Navbar, Sidebar, Footer components
    status: completed
  - id: build-card-components
    content: Create StatusCard, GitCard, HealthCard, WorkEffortsCard, GamificationCard, PyriteCard
    status: completed
  - id: create-stores
    content: Set up Svelte stores for project state, git, work efforts, empirica
    status: completed
  - id: build-main-dashboard
    content: Create main dashboard route (/) with card grid layout
    status: completed
  - id: integrate-backend
    content: Connect SvelteKit frontend to FastAPI backend with API client
    status: completed
  - id: add-real-time-updates
    content: Implement polling mechanism for auto-refresh
    status: completed
  - id: update-serve-command
    content: Update waft serve command to use FastAPI + SvelteKit build
    status: completed
---

# SvelteKit Visualizer Migration Plan

## Overview

Transform the current Python-based HTML visualizer into a modern SvelteKit application that serves as a comprehensive development dashboard. The new visualizer will integrate with all Waft systems (GitHub, MCPs, _pyrite, Empirica, work efforts) while maintaining the familiar, non-overwhelming UX.

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                    SvelteKit Frontend                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Layout  │  │  Routes  │  │ Components│ │  Stores  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↕ API
┌─────────────────────────────────────────────────────────┐
│              Python FastAPI Backend                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Visualizer│ │  Memory  │  │  GitHub  │ │ Empirica │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Project Structure

```
waft/
├── visualizer/                    # New SvelteKit app
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/       # Reusable components
│   │   │   │   ├── cards/
│   │   │   │   ├── charts/
│   │   │   │   ├── status/
│   │   │   │   └── layout/
│   │   │   ├── stores/           # Svelte stores for state
│   │   │   ├── api/              # API client
│   │   │   └── utils/            # Utilities
│   │   ├── routes/
│   │   │   ├── +layout.svelte
│   │   │   ├── +page.svelte      # Main dashboard
│   │   │   ├── git/
│   │   │   ├── work-efforts/
│   │   │   ├── empirica/
│   │   │   └── settings/
│   │   ├── app.html
│   │   └── app.d.ts
│   ├── static/
│   ├── package.json
│   ├── svelte.config.js
│   ├── vite.config.js
│   └── tsconfig.json
├── src/waft/
│   └── api/                      # New FastAPI backend
│       ├── __init__.py
│       ├── main.py               # FastAPI app
│       ├── routes/
│       │   ├── state.py          # Project state endpoint
│       │   ├── git.py            # Git status endpoint
│       │   ├── work_efforts.py   # Work efforts endpoint
│       │   └── empirica.py       # Empirica endpoint
│       └── models.py             # Pydantic models
└── pyproject.toml                # Add FastAPI dependency
```

## Implementation Phases

### Phase 1: Project Setup & Foundation

**1.1 Initialize SvelteKit Project**

- Create `visualizer/` directory in waft root
- Initialize SvelteKit with TypeScript
- Configure Vite for development
- Set up Tailwind CSS (from sveltekit-starter pattern)
- Configure path aliases (`$lib`, `$components`)

**1.2 Create FastAPI Backend**

- Add FastAPI to `pyproject.toml`
- Create `src/waft/api/` module
- Set up CORS middleware
- Create base API router structure
- Add `/api/state` endpoint (replaces current `gather_state()`)

**1.3 Design System Setup**

- Extract color scheme from current visualizer
- Create design tokens (CSS variables)
- Set up typography system
- Create base component library structure

### Phase 2: Core Components

**2.1 Layout Components** (from sveltekit-starter)

- `AppShell.svelte` - Main app container
- `Navbar.svelte` - Top navigation
- `Sidebar.svelte` - Optional sidebar navigation
- `Footer.svelte` - Footer component

**2.2 Card Components** (from current visualizer)

- `StatusCard.svelte` - Status overview card
- `GitCard.svelte` - Git status card
- `HealthCard.svelte` - Project health card
- `WorkEffortsCard.svelte` - Work efforts card
- `GamificationCard.svelte` - Gamification stats card
- `PyriteCard.svelte` - _pyrite structure card

**2.3 Status Components**

- `Badge.svelte` - Status badges (success/warning/error)
- `ProgressBar.svelte` - Progress indicators
- `StatusIndicator.svelte` - Health indicators

**2.4 Data Display Components**

- `FileList.svelte` - File listing with icons
- `CommitList.svelte` - Commit history
- `WorkEffortList.svelte` - Work effort listing
- `DevlogList.svelte` - Devlog entries

### Phase 3: State Management

**3.1 Svelte Stores**

- `projectStore.ts` - Project state (reactive)
- `gitStore.ts` - Git status
- `workEffortsStore.ts` - Work efforts
- `empiricaStore.ts` - Empirica data
- `settingsStore.ts` - User preferences

**3.2 API Client**

- `api/client.ts` - Axios/fetch wrapper
- Type-safe API methods
- Error handling
- Request/response interceptors

**3.3 Real-time Updates**

- WebSocket connection (optional, Phase 2)
- Polling mechanism for data refresh
- Optimistic UI updates

### Phase 4: Routes & Pages

**4.1 Main Dashboard** (`/`)

- Overview layout (grid of cards)
- Status summary at top
- Quick actions
- Real-time updates

**4.2 Git View** (`/git`)

- Detailed git status
- File diff viewer (future)
- Branch visualization
- Commit history timeline

**4.3 Work Efforts View** (`/work-efforts`)

- List of all work efforts
- Filter by status
- Search functionality
- Work effort detail view

**4.4 Empirica View** (`/empirica`)

- Epistemic dashboard
- Moon phase indicator
- Vector visualization
- Learning trajectory

**4.5 Settings** (`/settings`)

- Theme preferences
- Refresh intervals
- Display options

### Phase 5: Integration Points

**5.1 Python Backend Integration**

- Migrate `Visualizer.gather_state()` to FastAPI endpoint
- Create Pydantic models for all data structures
- Add error handling and validation
- Implement caching for expensive operations

**5.2 GitHub Integration**

- Use existing `GitHubManager`
- Add GitHub-specific endpoints
- Display PR status, issues, etc.

**5.3 MCP Integration** (Future)

- WebSocket connection to MCP servers
- Real-time data from MCP tools
- Work efforts MCP integration

**5.4 Empirica Integration**

- Use existing `EmpiricaManager`
- Display epistemic state
- Show learning metrics

### Phase 6: Design Patterns from Reference Repos

**6.1 From sveltekit-starter**

- Clean component structure
- TypeScript strict mode
- Tailwind CSS utility classes
- Form handling patterns

**6.2 From sveltekit-blog-starter**

- Markdown rendering (for devlog)
- Content organization
- Navigation patterns

**6.3 From sveltekit-superforms**

- Form validation patterns
- Error handling
- User feedback

**6.4 From sveltekit-pb-boilerplate**

- Authentication patterns (if needed)
- Data fetching patterns
- State management

**6.5 From svelte-vertical-timeline**

- Timeline visualization for commits/work efforts
- Chronological data display

## Key Features

### MVP Features (Phase 1-3)

1. **Dashboard Overview**

   - Project status at a glance
   - Git status summary
   - Health indicators
   - Quick navigation

2. **Real-time Updates**

   - Auto-refresh every 30 seconds
   - Manual refresh button
   - Loading states

3. **Responsive Design**

   - Mobile-friendly
   - Tablet optimized
   - Desktop enhanced

4. **Dark Mode** (from current design)

   - Maintain current color scheme
   - Smooth transitions

### Enhanced Features (Phase 4-6)

1. **Interactive Visualizations**

   - Git commit timeline
   - Work effort progress charts
   - Epistemic vector graphs

2. **Filtering & Search**

   - Filter files by type
   - Search work efforts
   - Filter git changes

3. **Export & Sharing**

   - Export dashboard as PDF
   - Shareable links
   - Screenshot functionality

4. **Keyboard Shortcuts**

   - Quick navigation
   - Refresh (R)
   - Search (Cmd/Ctrl+K)

## Technical Decisions

### Frontend Stack

- **SvelteKit**: Modern, fast, familiar
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Vite**: Fast dev server
- **Svelte Stores**: State management

### Backend Stack

- **FastAPI**: Modern Python API framework
- **Pydantic**: Data validation
- **Existing Waft modules**: Reuse current code

### Development Workflow

- **Dev Mode**: SvelteKit dev server (port 5173) + FastAPI (port 8000)
- **Production**: Build SvelteKit, serve static files from FastAPI
- **Hot Reload**: Both frontend and backend support hot reload

## File Changes

### New Files

- `visualizer/` - Entire SvelteKit application
- `src/waft/api/` - FastAPI backend module
- `src/waft/api/main.py` - FastAPI app initialization
- `src/waft/api/routes/` - API route handlers
- `src/waft/api/models.py` - Pydantic models

### Modified Files

- `src/waft/main.py` - Update `serve` command to use FastAPI
- `pyproject.toml` - Add FastAPI, uvicorn dependencies
- `src/waft/core/visualizer.py` - Keep for standalone HTML generation (backward compatibility)

### Preserved Files

- `src/waft/core/visualizer.py` - Keep `generate_html()` for standalone files
- `src/waft/web.py` - Keep for backward compatibility or remove

## Design Principles

1. **Familiar UX**: Match current visualizer's information architecture
2. **Progressive Enhancement**: Start with MVP, add features incrementally
3. **DRY**: Reusable components, shared utilities
4. **Type Safety**: TypeScript + Pydantic models
5. **Performance**: Lazy loading, code splitting, caching
6. **Accessibility**: ARIA labels, keyboard navigation
7. **Responsive**: Mobile-first design

## Testing Strategy

1. **Component Tests**: Test individual Svelte components
2. **API Tests**: Test FastAPI endpoints
3. **Integration Tests**: Test full data flow
4. **E2E Tests**: Test user workflows (optional)

## Documentation

1. **Component Documentation**: JSDoc comments
2. **API Documentation**: FastAPI auto-generated docs
3. **User Guide**: How to use the visualizer
4. **Developer Guide**: How to extend the visualizer

## Migration Path

1. **Phase 1-2**: Build alongside existing visualizer
2. **Phase 3**: Add feature flag to switch between old/new
3. **Phase 4**: Make SvelteKit default, keep old as fallback
4. **Phase 5**: Remove old visualizer (after validation period)