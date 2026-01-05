# Waft Web Dashboard

**Created**: 2026-01-04
**Last Updated**: 2026-01-05
**Status**: ✅ Implemented

## Overview

Added a web dashboard feature to waft that allows viewing project information through a web browser on localhost.

## New Command

### `waft serve`

Starts a web server that serves a dashboard for the current Waft project.

**Usage**:
```bash
# Start server on default port (8000)
waft serve

# Development mode with live reloading
waft serve --dev

# Custom port
waft serve --port 8080

# Custom host
waft serve --host 0.0.0.0

# For specific project
waft serve --path /path/to/project

# Combine options
waft serve --dev --port 8080
```

**Features**:
- Beautiful web dashboard with project information
- Real-time project status
- _pyrite structure visualization
- Template status
- Auto-refresh every 30 seconds (2 seconds in dev mode)
- JSON API endpoints
- **Live reloading** (with `--dev` flag): Automatically restarts server when code changes

## Endpoints

### `GET /`
Main dashboard page with HTML interface.

### `GET /api/info`
Returns project information as JSON:
```json
{
  "project_path": "/path/to/project",
  "project_name": "my-project",
  "version": "0.1.0",
  "pyrite_structure": {
    "valid": true,
    "folders": {
      "_pyrite/active": true,
      "_pyrite/backlog": true,
      "_pyrite/standards": true
    }
  },
  "uv_lock": true,
  "templates": {
    "justfile": true,
    "ci": true,
    "agents": true,
    "gitignore": true,
    "readme": true
  }
}
```

### `GET /api/structure`
Returns _pyrite structure contents:
```json
{
  "active": ["file1.md", "file2.md"],
  "backlog": ["todo.md"],
  "standards": ["coding-standards.md"]
}
```

## Dashboard Features

### Visual Design
- **Dark mode theme** - Modern dark gradient background with dark cards
- **Navigation bar** - Top navbar with brand, links, refresh button, and dev mode indicator
- Card-based layout with subtle borders
- Responsive grid and mobile-friendly design
- Status badges with color coding (dark mode optimized)
- Clean typography with high contrast

### Information Displayed
1. **Project Information**
   - Project path
   - Project name
   - Version

2. **Structure Status**
   - _pyrite structure validity
   - uv.lock status

3. **Templates**
   - List of generated templates
   - Visual indicators

4. **_pyrite Contents**
   - Files in active/
   - Files in backlog/
   - Files in standards/

## Implementation

### Files Created
- `src/waft/web.py` - Web server implementation
  - `WaftHandler` - HTTP request handler
  - `serve()` - Server startup function

### Files Modified
- `src/waft/main.py` - Added `serve` command

### Technology
- Python's built-in `http.server` (no external dependencies)
- HTML/CSS/JavaScript for dashboard
- JSON API endpoints
- `watchdog` (optional, for better file watching in dev mode)

## Usage Example

```bash
# Navigate to a Waft project
cd my_waft_project

# Start the dashboard
waft serve

# Open browser to http://localhost:8000
```

## Recent Updates

### 2026-01-05 - Live Reloading, Dark Mode & Navbar
- **Live Reloading**: Added `--dev` flag for development mode
  - Automatically restarts server when `web.py` or `main.py` changes
  - Uses `watchdog` library if available (included in dev dependencies)
  - Falls back to simple polling if watchdog not installed
  - Browser auto-refresh: 2 seconds in dev mode (vs 30 seconds in production)
- **Navigation Bar**: Added top navbar component
  - Brand logo/name on the left
  - Navigation links (Dashboard, API Info, Structure)
  - Manual refresh button
  - Dev mode badge indicator
  - Responsive design for mobile devices
- **Dark Mode Styling**: Converted dashboard to dark mode theme
  - Background: Dark gradient (#1a1a2e → #16213e → #0f3460)
  - Cards: Dark (#1e1e2e) with subtle borders
  - Text: Light colors (#e0e0e0) for high contrast
  - Accents: Blue (#7c9eff) for highlights
  - Status badges: Dark mode optimized colors
- Improved visual hierarchy and readability

## Future Enhancements

Potential improvements:
1. WebSocket support for real-time updates
2. Interactive project management
3. File editing capabilities
4. Command execution from web interface
5. Multiple project workspace view
6. Project comparison
7. Health scoring visualization
8. Dependency graph visualization
9. Theme toggle (light/dark mode switch)

## Security Notes

- Default binding to `localhost` only (not exposed to network)
- No authentication (intended for local development only)
- Read-only by default (no write operations)
- Should not be used in production without proper security

---

**Status**: ✅ Working and ready to use

