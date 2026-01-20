"""
Empirica Dashboard Launcher - Handles launching Empirica's terminal-based dashboards.

Provides integration for:
- Snapshot Monitor (curses-based)
- CASCADE Monitor (curses-based)
- TUI Dashboard (Textual-based)
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


def launch_empirica_dashboard(
    project_path: Path,
    dashboard_type: str = "snapshot",
    session_id: Optional[str] = None
) -> None:
    """
    Main entry point for launching Empirica dashboard.
    
    Args:
        project_path: Path to project root
        dashboard_type: Type of dashboard (snapshot, cascade, or tui)
        session_id: Optional session ID to monitor
        
    Raises:
        ImportError: If Empirica or dependencies not installed
        FileNotFoundError: If dashboard script not found
        ValueError: If validation fails
        PermissionError: If cannot access files
    """
    # Validate inputs
    if dashboard_type not in ["snapshot", "cascade", "tui"]:
        raise ValueError(f"Invalid dashboard type: {dashboard_type}. Must be snapshot, cascade, or tui")
    
    # Validate project path (security: prevent path traversal)
    project_path = _validate_project_path(project_path)
    
    # Validate Empirica setup
    _validate_empirica_setup(project_path)
    
    # Validate session if provided
    if session_id:
        _validate_session(session_id, project_path)
    
    # Check dependencies
    _check_dependencies(dashboard_type)
    
    # Launch appropriate dashboard
    with _change_directory(project_path):
        if dashboard_type == "snapshot":
            launch_snapshot_monitor(project_path, session_id)
        elif dashboard_type == "cascade":
            launch_cascade_monitor(project_path)
        elif dashboard_type == "tui":
            launch_tui_dashboard(project_path)


def _validate_project_path(project_path: Path) -> Path:
    """
    Validate and resolve project path, preventing path traversal attacks.
    
    Args:
        project_path: Path to validate
        
    Returns:
        Resolved Path object
        
    Raises:
        ValueError: If path is invalid or contains traversal sequences
        PermissionError: If path cannot be accessed
    """
    # Check for path traversal sequences in original path (before resolution)
    original_str = str(project_path)
    if ".." in original_str:
        raise ValueError(f"Invalid project path: path traversal sequences not allowed: {project_path}")
    
    # Resolve to absolute path
    try:
        resolved = project_path.resolve()
    except (OSError, PermissionError) as e:
        raise PermissionError(f"Cannot access project path: {project_path} - {e}")
    
    # Validate path exists and is a directory
    if not resolved.exists():
        raise ValueError(f"Project path does not exist: {resolved}")
    
    if not resolved.is_dir():
        raise ValueError(f"Project path is not a directory: {resolved}")
    
    # Check read permissions
    if not os.access(resolved, os.R_OK):
        raise PermissionError(f"Cannot read project path: {resolved}")
    
    return resolved


def _validate_empirica_setup(project_path: Path) -> None:
    """
    Validate Empirica initialized and project context.
    
    Args:
        project_path: Path to project root
        
    Raises:
        ValueError: If Empirica not initialized
    """
    # Check for .empirica directory
    empirica_dir = project_path / ".empirica"
    if not empirica_dir.exists():
        raise ValueError(
            "Empirica not initialized in this project. "
            "Run 'waft init' to initialize Empirica."
        )
    
    # Check for config file
    empirica_config = empirica_dir / "config.yaml"
    if not empirica_config.exists():
        raise ValueError(
            "Empirica configuration not found. "
            "Run 'waft init' to initialize Empirica."
        )


def _check_dependencies(dashboard_type: str) -> None:
    """
    Check for required dependencies before launching dashboard.
    
    Args:
        dashboard_type: Type of dashboard (snapshot, cascade, or tui)
        
    Raises:
        ImportError: If required dependencies not available
    """
    if dashboard_type in ["snapshot", "cascade"]:
        # Check for curses
        try:
            import curses
        except ImportError:
            try:
                import windows_curses as curses
            except ImportError:
                raise ImportError(
                    "curses not available. Install with:\n"
                    "  Unix: Already included in standard library\n"
                    "  Windows: pip install windows-curses"
                )
    elif dashboard_type == "tui":
        try:
            import textual
        except ImportError:
            raise ImportError(
                "textual not available. Install with: pip install textual"
            )


def _find_empirica_package() -> Optional[Path]:
    """
    Find Empirica package location (handles both pip install and source).
    
    Returns:
        Path to Empirica package, or None if not found
    """
    try:
        import empirica
        return Path(empirica.__file__).parent
    except ImportError:
        # Try to find via CLI command
        empirica_cmd = shutil.which("empirica")
        if empirica_cmd:
            return Path(empirica_cmd).parent
    return None


def _validate_session(session_id: str, project_path: Path) -> bool:
    """
    Validate session exists before monitoring.
    
    Args:
        session_id: Session ID to validate
        project_path: Path to project root
        
    Returns:
        True if session exists
        
    Raises:
        ValueError: If session not found
    """
    # Try using EmpiricaManager if available
    try:
        from .empirica import EmpiricaManager
        empirica = EmpiricaManager(project_path)
        
        # Check if we can query sessions
        # EmpiricaManager doesn't have a direct session validation method,
        # so we'll check the database file directly
        sessions_db = project_path / ".empirica" / "sessions" / "sessions.db"
        if sessions_db.exists():
            # Basic validation - session ID format check
            # Full validation would require querying the database
            if not session_id or len(session_id) < 3:
                raise ValueError(f"Invalid session ID format: {session_id}")
            return True
        else:
            raise ValueError("No sessions database found. Create a session first with 'waft session create'")
    except ImportError:
        # EmpiricaManager not available - skip validation
        return True
    except Exception as e:
        raise ValueError(f"Error validating session: {e}")


@contextmanager
def _change_directory(path: Path):
    """Context manager to temporarily change working directory."""
    old_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_cwd)


def launch_snapshot_monitor(project_path: Path, session_id: Optional[str]) -> None:
    """
    Launch snapshot monitor via import.
    
    Args:
        project_path: Path to project root
        session_id: Optional session ID to monitor
    """
    # Find Empirica package
    empirica_package = _find_empirica_package()
    if not empirica_package:
        raise FileNotFoundError(
            "Empirica package not found. Install with: pip install empirica"
        )
    
    # Try to import snapshot_monitor
    try:
        # Add Empirica package to path if needed
        empirica_parent = empirica_package.parent
        if str(empirica_parent) not in sys.path:
            sys.path.insert(0, str(empirica_parent))
        
        # Try different import paths
        try:
            from empirica.dashboard.snapshot_monitor import main as snapshot_main
        except ImportError:
            try:
                from empirica.snapshot_monitor import main as snapshot_main
            except ImportError:
                # Try direct file import
                snapshot_file = empirica_package / "dashboard" / "snapshot_monitor.py"
                if not snapshot_file.exists():
                    snapshot_file = empirica_package / "snapshot_monitor.py"
                
                if snapshot_file.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("snapshot_monitor", snapshot_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        snapshot_main = module.main
                    else:
                        raise FileNotFoundError(f"Could not load snapshot_monitor from {snapshot_file}")
                else:
                    raise FileNotFoundError(
                        f"snapshot_monitor.py not found in Empirica package at {empirica_package}"
                    )
        
        # Launch with project path and optional session ID
        if session_id:
            snapshot_main(project_path=str(project_path), session_id=session_id)
        else:
            snapshot_main(project_path=str(project_path))
            
    except ImportError as e:
        error_msg = str(e)
        if "auto_tracker" in error_msg:
            raise ImportError(
                f"Failed to import snapshot_monitor: {error_msg}\n"
                "This may be an Empirica version or dependency issue.\n"
                "Try: pip install --upgrade empirica\n"
                "Or check Empirica's documentation for required dependencies."
            )
        raise ImportError(
            f"Failed to import snapshot_monitor: {error_msg}\n"
            "Make sure Empirica is properly installed: pip install empirica"
        )


def launch_cascade_monitor(project_path: Path) -> None:
    """
    Launch CASCADE monitor via import.
    
    Args:
        project_path: Path to project root
    """
    # Find Empirica package
    empirica_package = _find_empirica_package()
    if not empirica_package:
        raise FileNotFoundError(
            "Empirica package not found. Install with: pip install empirica"
        )
    
    # Try to import cascade_monitor
    try:
        # Add Empirica package to path if needed
        empirica_parent = empirica_package.parent
        if str(empirica_parent) not in sys.path:
            sys.path.insert(0, str(empirica_parent))
        
        # Try different import paths
        try:
            from empirica.dashboard.cascade_monitor import main as cascade_main
        except ImportError:
            try:
                from empirica.cascade_monitor import main as cascade_main
            except ImportError:
                # Try direct file import
                cascade_file = empirica_package / "dashboard" / "cascade_monitor.py"
                if not cascade_file.exists():
                    cascade_file = empirica_package / "cascade_monitor.py"
                
                if cascade_file.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("cascade_monitor", cascade_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        cascade_main = module.main
                    else:
                        raise FileNotFoundError(f"Could not load cascade_monitor from {cascade_file}")
                else:
                    raise FileNotFoundError(
                        f"cascade_monitor.py not found in Empirica package at {empirica_package}"
                    )
        
        # Launch with project path
        cascade_main(project_path=str(project_path))
        
    except ImportError as e:
        error_msg = str(e)
        if "auto_tracker" in error_msg:
            raise ImportError(
                f"Failed to import cascade_monitor: {error_msg}\n"
                "This may be an Empirica version or dependency issue.\n"
                "Try: pip install --upgrade empirica\n"
                "Or check Empirica's documentation for required dependencies."
            )
        raise ImportError(
            f"Failed to import cascade_monitor: {error_msg}\n"
            "Make sure Empirica is properly installed: pip install empirica"
        )


def launch_tui_dashboard(project_path: Path) -> None:
    """
    Launch full TUI dashboard via import.
    
    Args:
        project_path: Path to project root
    """
    # Find Empirica package
    empirica_package = _find_empirica_package()
    if not empirica_package:
        raise FileNotFoundError(
            "Empirica package not found. Install with: pip install empirica"
        )
    
    # Try to import TUI dashboard
    try:
        # Add Empirica package to path if needed
        empirica_parent = empirica_package.parent
        if str(empirica_parent) not in sys.path:
            sys.path.insert(0, str(empirica_parent))
        
        # Import TUI dashboard - it's a Textual app
        try:
            from empirica.tui.dashboard import EmpiricaDashboard
        except ImportError:
            # Try alternative import path
            try:
                from empirica.dashboard.tui.dashboard import EmpiricaDashboard
            except ImportError:
                # Try direct file import
                tui_file = empirica_package / "tui" / "dashboard.py"
                if not tui_file.exists():
                    tui_file = empirica_package / "dashboard" / "tui" / "dashboard.py"
                
                if tui_file.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("tui_dashboard", tui_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        EmpiricaDashboard = module.EmpiricaDashboard
                    else:
                        raise FileNotFoundError(f"Could not load TUI dashboard from {tui_file}")
                else:
                    raise FileNotFoundError(
                        f"tui/dashboard.py not found in Empirica package at {empirica_package}"
                    )
        
        # Apply patches to fix known bugs in Empirica dashboard
        _patch_empirica_dashboard(EmpiricaDashboard)
        
        # Import Textual's run function
        from textual.app import App
        
        # Launch Textual app with project path
        # EmpiricaDashboard is a Textual App, so we run it using Textual's run method
        app = EmpiricaDashboard()
        app.run()
        
    except ImportError as e:
        raise ImportError(
            f"Failed to import TUI dashboard: {e}\n"
            "Make sure Empirica is properly installed: pip install empirica"
        )


def _patch_empirica_dashboard(dashboard_class):
    """
    Patch EmpiricaDashboard to fix known bugs:
    1. Timezone-aware vs naive datetime subtraction
    2. Timestamp column type mismatch (REAL Unix timestamp vs ISO string)
    """
    from datetime import datetime, timezone
    from empirica.tui.dashboard import ActivityPanel, VectorsPanel, CommandsLog
    
    # Patch ActivityPanel.update_activity
    original_activity = ActivityPanel.update_activity
    
    def patched_update_activity(self):
        """Patched version that handles timezone and timestamp issues."""
        try:
            from empirica.data.session_database import SessionDatabase
            from rich.text import Text
            from rich.panel import Panel
            
            db = SessionDatabase()
            cursor = db.conn.cursor()
            
            # Get active session
            cursor.execute("""
                SELECT session_id, ai_id, start_time, project_id
                FROM sessions
                WHERE end_time IS NULL
                ORDER BY start_time DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            
            if row:
                session_id = row['session_id']
                ai_id = row['ai_id']
                start_time = row['start_time']
                
                # Calculate session duration - FIX: Handle timezone-aware datetimes
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    # Make datetime.now() timezone-aware if start_dt is
                    if start_dt.tzinfo is not None:
                        now_dt = datetime.now(timezone.utc)
                        # Convert start_dt to UTC if needed
                        if start_dt.tzinfo != timezone.utc:
                            start_dt = start_dt.astimezone(timezone.utc)
                    else:
                        now_dt = datetime.now()
                    duration = now_dt - start_dt
                    duration_str = str(duration).split('.')[0]  # Remove microseconds
                except (ValueError, AttributeError) as e:
                    duration_str = "N/A"
                
                # Get latest reflex for phase information - FIX: Handle REAL timestamp
                cursor.execute("""
                    SELECT phase, round, timestamp
                    FROM reflexes
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                """, (session_id,))
                
                reflex_row = cursor.fetchone()
                
                content = Text()
                content.append("🆔 Session: ", style="bold cyan")
                content.append(f"{session_id[:8]}... ", style="yellow")
                content.append(f"(AI: {ai_id})\n", style="green")
                
                content.append("⏱️  Duration: ", style="bold cyan")
                content.append(f"{duration_str}\n", style="white")
                
                if reflex_row:
                    phase = reflex_row['phase']
                    # sqlite3.Row doesn't have .get(), use try/except or check keys
                    try:
                        round_num = reflex_row['round']
                    except (KeyError, IndexError):
                        try:
                            round_num = reflex_row['round_num']
                        except (KeyError, IndexError):
                            round_num = 'N/A'
                    timestamp_val = reflex_row['timestamp']
                    
                    # FIX: Handle both REAL (Unix timestamp) and ISO string formats
                    try:
                        if isinstance(timestamp_val, (int, float)):
                            # Unix timestamp (REAL)
                            reflex_time = datetime.fromtimestamp(timestamp_val, tz=timezone.utc)
                        else:
                            # ISO string
                            reflex_time = datetime.fromisoformat(str(timestamp_val).replace('Z', '+00:00'))
                        
                        # Make datetime.now() timezone-aware if reflex_time is
                        if reflex_time.tzinfo is not None:
                            now_dt = datetime.now(timezone.utc)
                            if reflex_time.tzinfo != timezone.utc:
                                reflex_time = reflex_time.astimezone(timezone.utc)
                        else:
                            now_dt = datetime.now()
                        
                        time_in_phase = now_dt - reflex_time
                        time_str = str(time_in_phase).split('.')[0]
                    except (ValueError, TypeError, OSError) as e:
                        time_str = "N/A"
                    
                    content.append("🎯 Phase: ", style="bold cyan")
                    content.append(f"{phase} ", style="magenta bold")
                    content.append(f"(Round {round_num})\n", style="white")
                    
                    content.append("⏰ Time in Phase: ", style="bold cyan")
                    content.append(f"{time_str}", style="white")
                else:
                    content.append("🎯 Phase: ", style="bold cyan")
                    content.append("No reflexes yet", style="dim")
            else:
                content = Text("No active session", style="dim italic")
            
            db.close()
            
            self.update(Panel(content, title="[bold]CURRENT ACTIVITY[/bold]", border_style="green"))
            
        except Exception as e:
            from rich.panel import Panel
            self.update(Panel(f"Error: {e}", title="[bold red]ERROR[/bold red]", border_style="red"))
    
    # Replace the method
    ActivityPanel.update_activity = patched_update_activity
    
    # Patch VectorsPanel.update_vectors
    original_vectors = VectorsPanel.update_vectors
    
    def patched_update_vectors(self):
        """Patched version that handles timestamp issues in epistemic queries."""
        try:
            from empirica.data.session_database import SessionDatabase
            from rich.table import Table
            from rich.panel import Panel
            
            db = SessionDatabase()
            cursor = db.conn.cursor()
            
            # Get active session
            cursor.execute("""
                SELECT session_id FROM sessions
                WHERE end_time IS NULL
                ORDER BY start_time DESC
                LIMIT 1
            """)
            
            session_row = cursor.fetchone()
            
            if session_row:
                session_id = session_row['session_id']
                
                # Get latest two reflexes for delta calculation - FIX: Handle REAL timestamp
                cursor.execute("""
                    SELECT engagement, know, context, uncertainty, timestamp
                    FROM reflexes
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 2
                """, (session_id,))
                
                rows = cursor.fetchall()
                
                if rows:
                    latest = rows[0]
                    previous = rows[1] if len(rows) > 1 else None
                    
                    # Build vector display
                    table = Table(show_header=True, header_style="bold cyan")
                    table.add_column("Vector", style="cyan")
                    table.add_column("Current", style="white", justify="right")
                    if previous:
                        table.add_column("Previous", style="dim", justify="right")
                        table.add_column("Δ", style="yellow", justify="right")
                    
                    vectors = ['engagement', 'know', 'context', 'uncertainty']
                    for vec in vectors:
                        current_val = latest[vec] if latest[vec] is not None else 0.0
                        row_data = [vec.capitalize(), f"{current_val:.2f}"]
                        
                        if previous:
                            prev_val = previous[vec] if previous[vec] is not None else 0.0
                            delta = current_val - prev_val
                            delta_str = f"{delta:+.2f}" if delta != 0 else "0.00"
                            row_data.extend([f"{prev_val:.2f}", delta_str])
                        
                        table.add_row(*row_data)
                    
                    self.update(Panel(table, title="[bold]EPISTEMIC VECTORS[/bold]", border_style="blue"))
                else:
                    self.update(Panel("[dim]No epistemic data yet[/dim]", title="[bold]EPISTEMIC VECTORS[/bold]"))
            else:
                self.update(Panel("[dim]No active session[/dim]", title="[bold]EPISTEMIC VECTORS[/bold]"))
            
            db.close()
            
        except Exception as e:
            from rich.panel import Panel
            self.update(Panel(f"Error: {e}", title="[bold red]ERROR[/bold red]", border_style="red"))
    
    VectorsPanel.update_vectors = patched_update_vectors
    
    # Patch CommandsLog.update_log
    original_log = CommandsLog.update_log
    
    def patched_update_log(self):
        """Patched version that handles timestamp issues in log queries."""
        try:
            from empirica.data.session_database import SessionDatabase
            from rich.text import Text
            from rich.panel import Panel
            
            db = SessionDatabase()
            cursor = db.conn.cursor()
            
            # Get recent findings and unknowns - FIX: Use created_timestamp column (REAL Unix timestamp)
            # The actual column name is created_timestamp, not timestamp or created_at
            cursor.execute("""
                SELECT 'FINDING' as type, finding as message, created_timestamp as timestamp
                FROM project_findings
                UNION ALL
                SELECT 'UNKNOWN' as type, unknown as message, created_timestamp as timestamp
                FROM project_unknowns
                WHERE is_resolved = 0
                ORDER BY timestamp DESC
                LIMIT 5
            """)
            
            rows = cursor.fetchall()
            
            if rows:
                content = Text()
                for row in rows:
                    event_type = row['type']
                    message = row['message']
                    # sqlite3.Row doesn't have .get(), access directly
                    try:
                        timestamp_val = row['timestamp']
                    except (KeyError, IndexError):
                        timestamp_val = None
                    
                    # FIX: Handle both REAL and ISO string timestamps
                    try:
                        if timestamp_val is None:
                            time_str = "N/A"
                        elif isinstance(timestamp_val, (int, float)):
                            # Unix timestamp
                            timestamp = datetime.fromtimestamp(timestamp_val, tz=timezone.utc)
                            time_str = timestamp.strftime("%H:%M:%S")
                        else:
                            # ISO string
                            timestamp = datetime.fromisoformat(str(timestamp_val).replace('Z', '+00:00'))
                            time_str = timestamp.strftime("%H:%M:%S")
                    except (ValueError, TypeError, OSError):
                        time_str = "N/A"
                    
                    # Color based on type
                    type_style = "green" if event_type == "FINDING" else "yellow"
                    
                    content.append(f"{time_str} ", style="dim")
                    content.append(f"[{event_type}] ", style=type_style)
                    content.append(f"{message[:60]}...\n" if len(message) > 60 else f"{message}\n")
                
                self.update(Panel(content, title="[bold]RECENT ACTIVITY[/bold]", border_style="blue"))
            else:
                self.update(Panel("No recent activity", title="[bold]RECENT ACTIVITY[/bold]", border_style="dim"))
            
            db.close()
            
        except Exception as e:
            self.update(Panel(f"Error: {e}", title="[bold red]ERROR[/bold red]", border_style="red"))
    
    CommandsLog.update_log = patched_update_log
