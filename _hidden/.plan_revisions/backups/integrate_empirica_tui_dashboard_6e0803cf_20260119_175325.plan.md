---
name: Integrate Empirica TUI Dashboard
overview: Integrate Empirica's terminal-based dashboard (TUI) into WAFT by adding a `waft empirica monitor` command that launches Empirica's dashboard components with proper project path resolution and error handling.
todos:
  - id: "1"
    content: Create empirica_dashboard.py module with dashboard launcher functions
    status: pending
  - id: "2"
    content: Add empirica_app command group and monitor command to main.py
    status: pending
  - id: "3"
    content: Implement path resolution and Empirica validation in dashboard launcher
    status: pending
  - id: "4"
    content: Add error handling for missing dependencies and uninitialized Empirica
    status: pending
  - id: "5"
    content: Test each dashboard type (snapshot, cascade, tui) with various scenarios
    status: pending
  - id: "6"
    content: Update documentation (README.md, WAFT_SYSTEM_INTEGRATION.md)
    status: pending
---

# Integrate Empirica TUI Dashboard into WAFT

## Overview

Add a new `waft empirica monitor` command that launches Empirica's terminal-based dashboard. Empirica provides three dashboard options:

1. **Snapshot Monitor** (`snapshot_monitor.py`) - Monitors epistemic snapshot memory quality
2. **CASCADE Monitor** (`cascade_monitor.py`) - Monitors PREFLIGHT → POSTFLIGHT workflow
3. **TUI Dashboard** (`tui/dashboard.py`) - Full terminal UI dashboard with Textual

## Implementation Plan

### 1. Add Monitor Command to WAFT CLI

**File**: `src/waft/main.py`

Add a new command group for Empirica monitoring:

```python
empirica_app = typer.Typer(help="Empirica monitoring and dashboard commands")
app.add_typer(empirica_app, name="empirica")

@empirica_app.command("monitor")
def empirica_monitor(
    dashboard_type: str = typer.Option("snapshot", "--type", "-t", help="Dashboard type: snapshot, cascade, or tui"),
    session_id: Optional[str] = typer.Option(None, "--session-id", "-s", help="Session ID to monitor"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path (default: current)"),
):
    """Launch Empirica TUI dashboard for monitoring epistemic state."""
    # Implementation here
```

### 2. Create Dashboard Launcher Module

**File**: `src/waft/core/empirica_dashboard.py` (NEW)

Create a module that:

- Resolves Empirica installation path
- Validates Empirica is initialized
- Launches the appropriate dashboard
- Handles errors gracefully

**Key Functions**:

- `launch_snapshot_monitor(project_path, session_id)` - Launch snapshot monitor
- `launch_cascade_monitor(project_path)` - Launch CASCADE monitor
- `launch_tui_dashboard(project_path)` - Launch full TUI dashboard
- `find_empirica_dashboard_path(dashboard_type)` - Find dashboard script in Empirica repo

### 3. Dashboard Integration Details

**Snapshot Monitor** (`snapshot_monitor.py`):

- Monitors snapshot memory quality
- Shows compression ratios, reliability scores
- Interactive commands: q (quit), r (refresh), f (full), e (export), d (details)
- Uses curses for terminal UI

**CASCADE Monitor** (`cascade_monitor.py`):

- Monitors PREFLIGHT → POSTFLIGHT workflow
- Shows epistemic vector deltas
- Event-driven updates (no polling)
- Minimalist design for tmux integration

**TUI Dashboard** (`tui/dashboard.py`):

- Full Textual-based terminal UI
- Shows project context, activity, vectors
- Auto-refreshes every 1-5 seconds
- More comprehensive than snapshot/cascade monitors

### 4. Project Path Resolution

Ensure the dashboard runs in the correct project context:

- Use WAFT's `resolve_project_path()` function
- Change to project directory before launching dashboard
- Pass project path to Empirica dashboard if needed

### 5. Error Handling

Handle common scenarios:

- Empirica not installed → Show helpful error message
- Empirica not initialized → Prompt to run `waft init`
- No active session → Show message and allow creating one
- Dashboard script not found → Fallback to `empirica monitor` CLI command
- Terminal too small → Show warning

### 6. Dependencies

Check for required dependencies:

- `curses` (for snapshot/cascade monitors) - standard library on Unix, `windows-curses` on Windows
- `textual` (for TUI dashboard) - may need to install: `pip install textual`
- Empirica package must be installed and accessible

## Files to Modify

1. **`src/waft/main.py`**

   - Add `empirica_app` command group
   - Add `empirica monitor` command

2. **`src/waft/core/empirica_dashboard.py`** (NEW)

   - Dashboard launcher module
   - Path resolution and validation
   - Dashboard execution logic

3. **`src/waft/core/empirica.py`** (optional enhancement)

   - Add helper method to get Empirica installation path
   - Add method to check if dashboard is available

## Usage Examples

```bash
# Launch snapshot monitor (default)
waft empirica monitor

# Launch CASCADE monitor
waft empirica monitor --type cascade

# Launch full TUI dashboard
waft empirica monitor --type tui

# Monitor specific session
waft empirica monitor --session-id abc-123

# Specify project path
waft empirica monitor --path /path/to/project
```

## Testing

1. Test with Empirica initialized
2. Test with Empirica not initialized (should show helpful error)
3. Test each dashboard type (snapshot, cascade, tui)
4. Test with no active session
5. Test on different terminal sizes
6. Test error handling (missing dependencies, etc.)

## Documentation Updates

1. Update `README.md` with new command
2. Update `WAFT_SYSTEM_INTEGRATION.md` with Empirica monitor command
3. Add to CLI help text

## Future Enhancements

- Add `--auto-refresh` option for refresh interval
- Add `--export` option to export dashboard data
- Integrate with WAFT's existing dashboard command
- Add web wrapper for dashboard (convert TUI to web UI)