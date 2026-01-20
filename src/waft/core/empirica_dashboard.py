"""
Empirica Dashboard Launcher - Launches Empirica's TUI dashboards from WAFT.

Supports three dashboard types:
1. Snapshot Monitor - Monitors epistemic snapshot memory quality
2. CASCADE Monitor - Monitors PREFLIGHT → POSTFLIGHT workflow
3. Full TUI Dashboard - Comprehensive terminal UI with Textual

Usage:
    from waft.core.empirica_dashboard import launch_dashboard
    launch_dashboard("snapshot")  # or "cascade" or "tui"
"""

import os
import subprocess
import sys
from pathlib import Path


def find_empirica_dashboard_path(dashboard_type: str = "snapshot") -> Path | None:
    """
    Find the path to Empirica's dashboard scripts.

    Args:
        dashboard_type: One of "snapshot", "cascade", or "tui"

    Returns:
        Path to dashboard script, or None if not found
    """
    # Map dashboard types to script paths
    dashboard_scripts = {
        "snapshot": "empirica/dashboard/snapshot_monitor.py",
        "cascade": "empirica/dashboard/cascade_monitor.py",
        "tui": "empirica/tui/dashboard.py",
    }

    script_path = dashboard_scripts.get(dashboard_type)
    if not script_path:
        return None

    # Try common Empirica installation locations
    search_paths = [
        # Development: sibling directory
        Path(__file__).parent.parent.parent.parent.parent / "empirica",
        # Development: parent's parent
        Path.cwd().parent / "empirica",
        # User's Code directory
        Path.home() / "Code" / "active" / "empirica",
        Path.home() / "Code" / "empirica",
        # Common development locations
        Path.home() / "projects" / "empirica",
        Path.home() / "dev" / "empirica",
    ]

    for base_path in search_paths:
        full_path = base_path / script_path
        if full_path.exists():
            return full_path

    return None


def find_empirica_cli() -> str | None:
    """
    Find the Empirica CLI command.

    Returns:
        Path to empirica CLI, or None if not found
    """
    import shutil

    # Try Python 3.12/3.11's empirica binary first
    for py_version in ["3.12", "3.11"]:
        empirica_path = f"/Library/Frameworks/Python.framework/Versions/{py_version}/bin/empirica"
        if os.path.exists(empirica_path) and os.access(empirica_path, os.X_OK):
            return empirica_path

    # Try system command
    empirica_cmd = shutil.which("empirica")
    if empirica_cmd:
        return empirica_cmd

    return None


def check_dashboard_dependencies(dashboard_type: str) -> dict:
    """
    Check if required dependencies for dashboard are available.

    Args:
        dashboard_type: Dashboard type to check

    Returns:
        Dict with availability status and messages
    """
    result = {"available": False, "message": "", "missing": []}

    if dashboard_type in ("snapshot", "cascade"):
        # These use curses (standard library on Unix)
        try:
            import curses

            result["available"] = True
            result["message"] = "curses available"
        except ImportError:
            result["missing"].append("curses")
            result["message"] = "curses not available (try: pip install windows-curses on Windows)"

    elif dashboard_type == "tui":
        # TUI dashboard requires textual
        try:
            import textual

            result["available"] = True
            result["message"] = "textual available"
        except ImportError:
            result["missing"].append("textual")
            result["message"] = "textual not available (install: pip install textual)"

    return result


def launch_snapshot_monitor(project_path: Path, session_id: str | None = None) -> bool:
    """
    Launch the Empirica snapshot monitor dashboard.

    Args:
        project_path: Project path for context
        session_id: Optional session ID to monitor

    Returns:
        True if launched successfully, False otherwise
    """
    dashboard_path = find_empirica_dashboard_path("snapshot")

    if dashboard_path and dashboard_path.exists():
        # Run the dashboard script directly
        cmd = [sys.executable, str(dashboard_path)]
        if session_id:
            cmd.append(session_id)

        try:
            os.chdir(project_path)
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except KeyboardInterrupt:
            return True  # User quit - that's okay

    # Fallback: try CLI command
    empirica_cli = find_empirica_cli()
    if empirica_cli:
        cmd = [empirica_cli, "monitor"]
        if session_id:
            cmd.extend(["--session-id", session_id])

        try:
            os.chdir(project_path)
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except KeyboardInterrupt:
            return True

    return False


def launch_cascade_monitor(project_path: Path) -> bool:
    """
    Launch the Empirica CASCADE monitor dashboard.

    Args:
        project_path: Project path for context

    Returns:
        True if launched successfully, False otherwise
    """
    dashboard_path = find_empirica_dashboard_path("cascade")

    if dashboard_path and dashboard_path.exists():
        cmd = [sys.executable, str(dashboard_path)]

        try:
            os.chdir(project_path)
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except KeyboardInterrupt:
            return True

    return False


def launch_tui_dashboard(project_path: Path) -> bool:
    """
    Launch the full Empirica TUI dashboard (Textual-based).

    Args:
        project_path: Project path for context

    Returns:
        True if launched successfully, False otherwise
    """
    dashboard_path = find_empirica_dashboard_path("tui")

    if dashboard_path and dashboard_path.exists():
        cmd = [sys.executable, str(dashboard_path)]

        try:
            os.chdir(project_path)
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except KeyboardInterrupt:
            return True

    return False


def launch_dashboard(
    dashboard_type: str = "snapshot",
    project_path: Path | None = None,
    session_id: str | None = None,
) -> bool:
    """
    Launch an Empirica dashboard.

    Args:
        dashboard_type: Type of dashboard ("snapshot", "cascade", or "tui")
        project_path: Project path (defaults to current directory)
        session_id: Optional session ID for snapshot monitor

    Returns:
        True if launched successfully, False otherwise
    """
    if project_path is None:
        project_path = Path.cwd()

    # Check dependencies
    deps = check_dashboard_dependencies(dashboard_type)
    if not deps["available"]:
        print(f"Error: {deps['message']}")
        return False

    # Launch appropriate dashboard
    if dashboard_type == "snapshot":
        return launch_snapshot_monitor(project_path, session_id)
    elif dashboard_type == "cascade":
        return launch_cascade_monitor(project_path)
    elif dashboard_type == "tui":
        return launch_tui_dashboard(project_path)
    else:
        print(f"Unknown dashboard type: {dashboard_type}")
        print("Available types: snapshot, cascade, tui")
        return False
