#!/usr/bin/env python3
"""
WAFT Status Check and Documentation Generator
============================================

Checks current system status and can generate documentation at multiple
complexity levels (layman, professional, scientist) about what's happening
right now.

Usage:
    python scripts/waft_status.py                    # Status check only
    python scripts/waft_status.py --docs             # Generate all docs
    python scripts/waft_status.py --docs --level layman  # Specific level
    python scripts/waft_status.py --docs --printer-friendly
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import kernel
try:
    from src.waft.core.kernel import WAFTKernel
    KERNEL_AVAILABLE = True
except ImportError:
    KERNEL_AVAILABLE = False
    WAFTKernel = None


def _validate_path_in_project(project_path: Path, file_path: Path) -> bool:
    """
    Validate file path is within project directory.
    
    Uses existing pattern from karma.py:93 and being.py:873.
    
    Args:
        project_path: Project root directory
        file_path: File path to validate
        
    Returns:
        True if path is within project, False otherwise
    """
    try:
        resolved = file_path.resolve()
        project_resolved = project_path.resolve()
        return resolved.is_relative_to(project_resolved)
    except (ValueError, OSError):
        return False


def validate_path(path: Path, project_root: Path) -> bool:
    """
    Validate path is within project root (prevent path traversal).
    
    Args:
        path: Path to validate
        project_root: Project root directory
        
    Returns:
        True if path is within project root, False otherwise
    """
    return _validate_path_in_project(project_root, path)


def calculate_moon_phase(epistemic_state: Dict[str, Any]) -> tuple[str, str]:
    """
    Calculate moon phase from epistemic vectors.
    
    Uses existing get_moon_phase function from epistemic_display module.
    Coverage = average of all epistemic vector values (0.0-1.0)
    
    Args:
        epistemic_state: Dictionary with epistemic vectors
        
    Returns:
        Tuple of (emoji, description)
    """
    try:
        from src.waft.cli.epistemic_display import get_moon_phase
    except ImportError:
        # Fallback if module not available
        def get_moon_phase(coverage: float) -> str:
            if coverage < 0.25:
                return "🌑"
            elif coverage < 0.50:
                return "🌒"
            elif coverage < 0.75:
                return "🌓"
            elif coverage < 0.90:
                return "🌔"
            else:
                return "🌕"
    
    vectors = epistemic_state.get("vectors", {})
    if not vectors:
        return "🌑", "Critical (no data)"
    
    # Calculate average coverage from all vector values
    all_values = []
    for key, value in vectors.items():
        if isinstance(value, dict):
            # Nested dict (e.g., foundation: {know: 0.6, do: 0.7})
            all_values.extend([v for v in value.values() if isinstance(v, (int, float))])
        elif isinstance(value, (int, float)):
            all_values.append(value)
    
    if not all_values:
        return "🌑", "Critical (no valid vectors)"
    
    coverage = sum(all_values) / len(all_values)
    moon_emoji = get_moon_phase(coverage)
    
    # Generate description
    if coverage < 0.25:
        desc = f"Critical ({coverage*100:.0f}% coverage)"
    elif coverage < 0.50:
        desc = f"Low ({coverage*100:.0f}% coverage)"
    elif coverage < 0.75:
        desc = f"Moderate ({coverage*100:.0f}% coverage)"
    elif coverage < 0.90:
        desc = f"Good ({coverage*100:.0f}% coverage)"
    else:
        desc = f"Excellent ({coverage*100:.0f}% coverage)"
    
    return moon_emoji, desc


def get_epistemic_state(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Get epistemic state from Empirica with graceful degradation.
    
    Includes epistemic phase calculation using kernel utilities.
    
    Args:
        project_path: Path to project root (default: current directory)
        
    Returns:
        Dictionary with epistemic state including phase, know, uncertainty, coverage, moon_phase
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    try:
        from src.waft.core.empirica import EmpiricaManager
        
        empirica = EmpiricaManager(project_path)
        
        if not empirica.is_initialized():
            return {
                "initialized": False,
                "moon_phase": "🌑",
                "moon_phase_desc": "Unknown (Empirica not initialized)",
                "knowledge_pct": None,
                "uncertainty_pct": None,
                "vectors": {},
                "message": "Empirica not initialized - epistemic state unavailable"
            }
        
        # Try to get epistemic state
        context = empirica.project_bootstrap()
        if context is None:
            # Try assess_state as fallback
            state = empirica.assess_state(include_history=False)
            if state is None:
                return {
                    "initialized": True,
                    "moon_phase": "🌑",
                    "moon_phase_desc": "Unknown (no state data)",
                    "knowledge_pct": None,
                    "uncertainty_pct": None,
                    "vectors": {},
                    "message": "Empirica initialized but no state available"
                }
            epistemic_state = state
        else:
            epistemic_state = context.get("epistemic_state", {})
        
        # Extract vectors
        vectors = epistemic_state.get("vectors", {})
        
        # Calculate moon phase using our function
        moon_emoji, moon_desc = calculate_moon_phase({"vectors": vectors})
        
        # Calculate knowledge and uncertainty percentages
        knowledge_pct = None
        uncertainty_pct = None
        
        if vectors:
            # Calculate knowledge from foundation vectors if available
            foundation = vectors.get("foundation", {})
            if isinstance(foundation, dict):
                know = foundation.get("know", 0.0)
                do = foundation.get("do", 0.0)
                context_val = foundation.get("context", 0.0)
                knowledge_pct = ((know + do + context_val) / 3.0) * 100
            
            # Get uncertainty directly
            uncertainty = vectors.get("uncertainty", None)
            if uncertainty is not None:
                uncertainty_pct = uncertainty * 100
        
        return {
            "initialized": True,
            "moon_phase": moon_emoji,
            "moon_phase_desc": moon_desc,
            "knowledge_pct": knowledge_pct,
            "uncertainty_pct": uncertainty_pct,
            "vectors": vectors,
            "message": None
        }
        
    except Exception as e:
        return {"initialized": False, "error": str(e)}


def check_pyrite_integrity(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Check _pyrite structure and Genesis files (handle missing gracefully)."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    try:
        pyrite_dir = project_path / "_pyrite"
        if not pyrite_dir.exists():
            return {"exists": False}
        
        # Validate path
        if not validate_path(pyrite_dir, project_path):
            return {"exists": False, "error": "Invalid path"}
        
        integrity = {
            "exists": True,
            "structure_valid": False,
            "genesis_files": {}
        }
        
        # Check structure
        required_dirs = ["active", "backlog", "standards", "gym_logs"]
        integrity["structure_valid"] = all(
            (pyrite_dir / d).exists() and (pyrite_dir / d).is_dir() and validate_path(pyrite_dir / d, project_path)
            for d in required_dirs
        )
        
        # Check Genesis files (may not exist yet - that's OK)
        genesis_files = {
            "state": "20.00_state.json",
            "ledger": "35.00_pyrite_ledger.json",
            "kernel": "42.00_internal_kernel.md"
        }
        
        for key, filename in genesis_files.items():
            file_path = pyrite_dir / filename
            integrity["genesis_files"][key] = {
                "exists": file_path.exists() and validate_path(file_path, project_path),
                "path": str(file_path.relative_to(project_path)) if file_path.exists() and validate_path(file_path, project_path) else None
            }
        
        return integrity
    except Exception as e:
        return {"exists": False, "error": str(e)}


def get_gamification_state(project_path: Path) -> Dict[str, Any]:
    """
    Get gamification state with graceful degradation.
    
    Args:
        project_path: Path to project root
        
    Returns:
        Dictionary with level, integrity, insight, achievements, available
    """
    try:
        from src.waft.core.gamification import GamificationManager
        
        # Validate path to gamification.json before accessing
        gamification_path = project_path / "_pyrite" / ".waft" / "gamification.json"
        if not _validate_path_in_project(project_path, gamification_path):
            return {
                "available": False,
                "level": 1,
                "integrity": 100.0,
                "insight": 0.0,
                "achievements": [],
                "message": "Path validation failed: gamification.json is outside project directory"
            }
        
        gamification = GamificationManager(project_path)
        stats = gamification.get_stats()
        
        return {
            "available": True,
            "level": stats.get("level", 1),
            "integrity": stats.get("integrity", 100.0),
            "insight": stats.get("insight", 0.0),
            "achievements": stats.get("achievements", []),
            "achievements_count": stats.get("achievements_count", 0),
            "message": None
        }
        
    except (IOError, PermissionError, json.JSONDecodeError) as e:
        return {
            "available": False,
            "level": 1,
            "integrity": 100.0,
            "insight": 0.0,
            "achievements": [],
            "message": f"Gamification data not found or corrupted - using defaults"
        }
    except Exception as e:
        # Don't expose full error to user, just indicate unavailable
        return {
            "available": False,
            "level": 1,
            "integrity": 100.0,
            "insight": 0.0,
            "achievements": [],
            "message": "Gamification data not available"
        }


def get_recent_flight_recorder_events(project_path: Path, limit: int = 10) -> List[Dict]:
    """
    Get recent events from existing TheObserver (Flight Recorder).
    
    Args:
        project_path: Path to project root
        limit: Maximum number of events to return
        
    Returns:
        List of event dictionaries
    """
    try:
        from src.waft.core.science.observer import TheObserver
        
        # Validate path to laboratory.jsonl before reading
        lab_path = project_path / "_pyrite" / "science" / "laboratory.jsonl"
        if not _validate_path_in_project(project_path, lab_path):
            return []
        
        observer = TheObserver(project_path)
        events = observer.get_laboratory_log(limit=limit)
        return events
        
    except (IOError, json.JSONDecodeError, PermissionError):
        return []  # Graceful degradation
    except Exception:
        return []  # Graceful degradation for any other errors


def get_git_status(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get comprehensive git status."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    status = {
        "initialized": False,
        "branch": None,
        "uncommitted_files": [],
        "staged_files": [],
        "unstaged_files": [],
        "commits_ahead": 0,
        "commits_behind": 0,
        "recent_commits": [],
    }
    
    try:
        # Check if git is initialized
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        if result.returncode != 0:
            return status
        
        status["initialized"] = True
        
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            status["branch"] = result.stdout.strip()
        
        # Get uncommitted files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line:
                    status_code = line[:2]
                    filename = line[3:]
                    status["uncommitted_files"].append(filename)
                    if status_code[0] != " ":
                        status["staged_files"].append(filename)
                    if status_code[1] != " ":
                        status["unstaged_files"].append(filename)
        
        # Get commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                status["commits_ahead"] = int(parts[0])
                status["commits_behind"] = int(parts[1])
        
        # Get recent commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-10", "--no-decorate"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            status["recent_commits"] = [
                line.strip() for line in result.stdout.strip().split("\n") if line
            ]
    
    except Exception as e:
        print(f"Warning: Error checking git status: {e}")
    
    return status


def get_work_efforts(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get work efforts status."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    efforts = {
        "active": [],
        "recent": [],
        "completed": [],
        "count": 0,
    }
    
    work_efforts_dir = project_path / "_work_efforts"
    if not work_efforts_dir.exists():
        return efforts
    
    # Validate path
    if not validate_path(work_efforts_dir, project_path):
        return efforts
    
    # Look for work effort directories (WE-YYMMDD-* pattern)
    try:
        for item in work_efforts_dir.iterdir():
            if item.is_dir() and item.name.startswith("WE-"):
                # Validate work effort directory name (prevent traversal)
                if ".." in item.name or not validate_path(item, project_path):
                    continue
                    
                efforts["count"] += 1
                # Check for index file to determine status
                index_file = item / f"{item.name}_index.md"
                if index_file.exists() and validate_path(index_file, project_path):
                    efforts["active"].append(item.name)
                else:
                    efforts["recent"].append(item.name)
    except Exception as e:
        print(f"Warning: Error reading work efforts: {e}")
    
    return efforts


def get_project_health(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get project health status."""
    health = {
        "pyrite_valid": False,
        "lock_exists": False,
        "structure_valid": False,
    }
    
    # Check _pyrite structure
    pyrite_dir = Path("_pyrite")
    if pyrite_dir.exists():
        health["pyrite_valid"] = True
        if (pyrite_dir / "active").exists() and (pyrite_dir / "backlog").exists():
            health["structure_valid"] = True
    
    # Check uv.lock
    if Path("uv.lock").exists():
        health["lock_exists"] = True
    
    return health


def get_recent_activity(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get recent activity information."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    activity = {
        "devlog_entries": [],
        "recent_files": [],
    }
    
    try:
        # Get recent devlog entries
        devlog = project_path / "_work_efforts" / "devlog.md"
        if devlog.exists() and validate_path(devlog, project_path):
            content = devlog.read_text(encoding="utf-8")
            lines = content.split("\n")
            # Get last 5 entries (simple approach - look for date headers)
            recent_lines = []
            for line in reversed(lines[-100:]):  # Check last 100 lines
                if line.startswith("## ") and any(char.isdigit() for char in line):
                    recent_lines.append(line)
                    if len(recent_lines) >= 5:
                        break
            activity["devlog_entries"] = list(reversed(recent_lines))
    except Exception as e:
        print(f"Warning: Error reading devlog: {e}")
    
    return activity


def check_status(project_path: Optional[Path] = None, log_event: bool = True) -> Dict[str, Any]:
    """
    Perform comprehensive status check.
    
    Args:
        project_path: Project root path (default: current directory)
        log_event: Whether to log STATUS_CHECK event to flight recorder
        
    Returns:
        Dictionary with complete status information
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    print("Checking system status...")
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "git": get_git_status(project_path),
        "work_efforts": get_work_efforts(project_path),
        "project_health": get_project_health(),
        "recent_activity": get_recent_activity(project_path),
        "epistemic_state": get_epistemic_state(project_path),
        "gamification_state": get_gamification_state(project_path),
        "flight_recorder_events": get_recent_flight_recorder_events(project_path, limit=10),
        "pyrite_integrity": check_pyrite_integrity(project_path),
    }
    
    # Log STATUS_CHECK event to flight recorder
    if log_event:
        try:
            from src.waft.core.science.observer import TheObserver
            from src.waft.core.agent.state import EvolutionaryEvent, EvolutionaryEventType
            
            observer = TheObserver(project_path)
            event = EvolutionaryEvent(
                timestamp=datetime.utcnow(),
                genome_id="waft_kernel",
                event_type=EvolutionaryEventType.STATUS_CHECK,
                payload={
                    "kernel_version": "1.0",
                    "epistemic_phase": status["epistemic_state"].get("phase", "UNKNOWN"),
                    "work_efforts_count": status["work_efforts"]["count"],
                    "pyrite_valid": status["project_health"]["pyrite_valid"],
                },
                agent_id="waft_kernel"
            )
            observer.observe_event(event)
        except Exception as e:
            # Don't fail status check if event logging fails
            print(f"Warning: Could not log status check event: {e}")
    
    return status


def declare_epistemic_phase(status: Dict[str, Any]) -> str:
    """
    Determine current epistemic phase based on system state.
    
    Args:
        status: Complete status dictionary
        
    Returns:
        Epistemic phase string (e.g., "Data Gathering", "Synthesis", "Evolution")
    """
    epistemic = status.get("epistemic_state", {})
    work_efforts = status.get("work_efforts", {})
    git = status.get("git", {})
    
    # Determine phase based on activity patterns
    active_efforts = len(work_efforts.get("active", []))
    uncommitted_files = len(git.get("uncommitted_files", []))
    
    # If Empirica not initialized, use basic heuristics
    if not epistemic.get("initialized", False):
        if active_efforts > 5 or uncommitted_files > 20:
            return "Active Development"
        elif active_efforts > 0:
            return "Focused Work"
        else:
            return "Idle"
    
    # Use epistemic vectors to determine phase
    vectors = epistemic.get("vectors", {})
    uncertainty = vectors.get("uncertainty", 1.0)
    knowledge_pct = epistemic.get("knowledge_pct", 0.0)
    
    if uncertainty > 0.7 or knowledge_pct is None or knowledge_pct < 30:
        return "Data Gathering"
    elif uncertainty > 0.4 or (knowledge_pct and knowledge_pct < 60):
        return "Synthesis"
    elif active_efforts > 0:
        return "Evolution"
    else:
        return "Stable"


def display_status(status: Dict[str, Any]):
    """Display status summary."""
    print("\n" + "=" * 60)
    print("WAFT KERNEL STATUS")
    print("=" * 60)
    print(f"Timestamp: {status['timestamp']}")
    print()
    
    # Epistemic Phase
    epistemic_phase = declare_epistemic_phase(status)
    print(f"Epistemic Phase: {epistemic_phase}")
    
    # Epistemic State
    epistemic = status.get("epistemic_state", {})
    print("\nEpistemic State:")
    if epistemic.get("initialized", False):
        moon_emoji = epistemic.get("moon_phase", "🌑")
        moon_desc = epistemic.get("moon_phase_desc", "Unknown")
        print(f"  Moon Phase: {moon_emoji} ({moon_desc})")
        
        knowledge_pct = epistemic.get("knowledge_pct")
        uncertainty_pct = epistemic.get("uncertainty_pct")
        if knowledge_pct is not None:
            print(f"  Knowledge: {knowledge_pct:.1f}%")
        if uncertainty_pct is not None:
            print(f"  Uncertainty: {uncertainty_pct:.1f}%")
    else:
        message = epistemic.get("message", "Empirica not initialized")
        print(f"  {message}")
    print()
    
    # Gamification State
    gamification = status.get("gamification_state", {})
    print("Gamification:")
    if gamification.get("available", False):
        print(f"  Character Level: {gamification.get('level', 1)}")
        print(f"  Integrity Score: {gamification.get('integrity', 100.0):.1f}%")
        print(f"  Insight Points: {gamification.get('insight', 0.0):.0f}")
        achievements_count = gamification.get("achievements_count", 0)
        if achievements_count > 0:
            print(f"  Achievements: {achievements_count}")
    else:
        message = gamification.get("message", "Gamification data not available")
        print(f"  {message}")
    print()
    
    # Git Status
    print("Git Status:")
    git = status["git"]
    if git["initialized"]:
        print(f"  Branch: {git['branch']}")
        print(f"  Uncommitted files: {len(git['uncommitted_files'])}")
        print(f"  Staged: {len(git['staged_files'])}, Unstaged: {len(git['unstaged_files'])}")
        print(f"  Commits ahead: {git['commits_ahead']}, behind: {git['commits_behind']}")
        if git["recent_commits"]:
            print(f"  Recent commits: {len(git['recent_commits'])}")
    else:
        print("  Git not initialized")
    print()
    
    # Work Efforts
    print("Work Efforts:")
    we = status["work_efforts"]
    print(f"  Total: {we['count']}")
    print(f"  Active: {len(we['active'])}")
    print(f"  Recent: {len(we['recent'])}")
    print()
    
    # Project Health
    print("Project Health:")
    health = status["project_health"]
    print(f"  _pyrite valid: {health['pyrite_valid']}")
    print(f"  Structure valid: {health['structure_valid']}")
    print(f"  uv.lock exists: {health['lock_exists']}")
    
    # Pyrite Integrity
    pyrite = status.get("pyrite_integrity", {})
    if pyrite.get("exists"):
        print(f"  _pyrite structure: {'Valid' if pyrite.get('structure_valid') else 'Invalid'}")
        genesis = pyrite.get("genesis_files", {})
        genesis_count = sum(1 for f in genesis.values() if f.get("exists"))
        print(f"  Genesis files: {genesis_count}/3 present")
    print()
    
    # Flight Recorder Events
    flight_events = status.get("flight_recorder_events", [])
    if flight_events:
        print("Flight Recorder (Recent Events):")
        print(f"  Recent events: {len(flight_events)}")
        # Show last 3 events
        for event in flight_events[-3:]:
            event_type = event.get("event_type", "unknown")
            timestamp = event.get("timestamp", "unknown")
            # Format timestamp for display
            if isinstance(timestamp, str) and "T" in timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            print(f"    - {event_type} at {timestamp}")
    print()
    
    # Recent Activity
    print("Recent Activity:")
    activity = status["recent_activity"]
    print(f"  Devlog entries: {len(activity['devlog_entries'])}")
    print()
    
    print("=" * 60)


def generate_status_docs(status: Dict[str, Any], level: Optional[str] = None, printer_friendly: bool = False):
    """Generate status documentation at specified level(s)."""
    from examples.generate_waft_field_guide_printer_friendly import generate_field_guide_printer_friendly
    from examples.generate_waft_field_guide import generate_field_guide
    
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    levels = ["layman", "professional", "scientist"] if level is None else [level]
    
    for doc_level in levels:
        print(f"\nGenerating {doc_level} level status documentation...")
        
        content = format_status_content(status, doc_level)
        
        output_path = output_dir / f"WAFT_Status_{doc_level.capitalize()}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        if printer_friendly:
            output_path = output_dir / f"WAFT_Status_{doc_level.capitalize()}_{datetime.now().strftime('%Y-%m-%d')}_PrinterFriendly.pdf"
        
        if printer_friendly:
            generate_field_guide_printer_friendly(
                title="WAFT SYSTEM STATUS",
                content=content,
                output_path=output_path,
                series="STATUS REPORT",
                number=f"SR-{datetime.now().strftime('%Y%m%d')}",
                subtitle=f"Level {doc_level.capitalize()}: Current System State",
                classification="INTERNAL",
                issued_by="WAFT System",
                date=datetime.now().strftime("%B %d, %Y")
            )
        else:
            from src.waft.templates.field_guide import generate_field_guide
            generate_field_guide(
                title="WAFT SYSTEM STATUS",
                content=content,
                output_path=output_path,
                series="STATUS REPORT",
                number=f"SR-{datetime.now().strftime('%Y%m%d')}",
                subtitle=f"Level {doc_level.capitalize()}: Current System State",
                classification="INTERNAL",
                issued_by="WAFT System",
                date=datetime.now().strftime("%B %d, %Y")
            )
        
        print(f"✓ Generated: {output_path.name}")


def format_status_content(status: Dict[str, Any], level: str) -> str:
    """Format status content for specified complexity level."""
    git = status["git"]
    we = status["work_efforts"]
    health = status["project_health"]
    activity = status["recent_activity"]
    epistemic = status.get("epistemic_state", {})
    gamification = status.get("gamification_state", {})
    flight_events = status.get("flight_recorder_events", [])
    kernel = status.get("kernel", {})
    
    if level == "layman":
        return format_layman_content(status, git, we, health, activity, epistemic, gamification, kernel)
    elif level == "professional":
        return format_professional_content(status, git, we, health, activity, epistemic, gamification, flight_events, kernel)
    else:  # scientist
        return format_scientist_content(status, git, we, health, activity, epistemic, gamification, flight_events)


def format_layman_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict, epistemic: Dict, gamification: Dict, kernel: Dict) -> str:
    """Format status for layman audience."""
    # Epistemic phase
    phase = declare_epistemic_phase(status)
    
    # Epistemic state section
    epistemic_section = ""
    if epistemic.get("initialized", False):
        moon_emoji = epistemic.get("moon_phase", "🌑")
        moon_desc = epistemic.get("moon_phase_desc", "Unknown")
        knowledge_pct = epistemic.get("knowledge_pct")
        uncertainty_pct = epistemic.get("uncertainty_pct")
        
        epistemic_section = f"""
<h2>System Knowledge Status</h2>

<p>
The system's current knowledge level is <strong>{moon_emoji} {moon_desc}</strong>.
"""
        if knowledge_pct is not None:
            epistemic_section += f"<p>The system knows about <strong>{knowledge_pct:.0f}%</strong> of what it needs to know.</p>"
        if uncertainty_pct is not None:
            epistemic_section += f"<p>There's still <strong>{uncertainty_pct:.0f}%</strong> uncertainty about some things.</p>"
        epistemic_section += "</p>"
    else:
        epistemic_section = """
<h2>System Knowledge Status</h2>

<p>
Knowledge tracking is not currently available. This is normal if the system hasn't been fully set up yet.
</p>
"""
    
    # Gamification section
    gamification_section = ""
    if gamification.get("available", False):
        level = gamification.get("level", 1)
        integrity = gamification.get("integrity", 100.0)
        insight = gamification.get("insight", 0.0)
        
        gamification_section = f"""
<h2>System Progress</h2>

<p>
The system is at <strong>Level {level}</strong> with an integrity score of <strong>{integrity:.0f}%</strong>.
It has earned <strong>{insight:.0f}</strong> insight points so far.
</p>
"""
    else:
        gamification_section = """
<h2>System Progress</h2>

<p>
Progress tracking is not currently available.
</p>
"""
    
    kernel_section = ""
    if kernel:
        kernel_phase = kernel.get("epistemic_phase", phase)
        kernel_section = f"""
<h2>WAFT Kernel Status</h2>

<p>
The WAFT Kernel is the central intelligence overseeing agent breeding in this 
directed evolution laboratory. It's like the brain of the system, making sure 
everything runs smoothly.
</p>

<p>
<strong>Current Phase:</strong> {kernel_phase}
</p>
"""
    
    return f"""
<h2>What's Happening Right Now</h2>

<p>
This report shows what the WAFT system is doing right now. Think of it like a 
health check for a computer program - we're checking to see how things are going.
</p>
{kernel_section}
{epistemic_section}
{gamification_section}

<h2>Current Work Status</h2>

<p>
The system is currently working on <strong>{we['count']}</strong> different projects.
Of these, <strong>{len(we['active'])}</strong> are actively being worked on right now.
</p>

<div class="note">
    <div class="note-title">Simple Explanation</div>
    Think of work efforts like different tasks or projects. Some are being actively 
    worked on, some are waiting, and some are finished.
</div>

<h2>Code Changes</h2>

<p>
The system has <strong>{len(git['uncommitted_files'])}</strong> files that have been 
changed but not yet saved permanently. This is normal when work is in progress.
</p>

{'<div class="warning"><div class="warning-title">Attention Needed</div>There are uncommitted changes that should be saved soon.</div>' if len(git['uncommitted_files']) > 10 else ''}

<h2>System Health</h2>

<table>
    <caption>Health Check Results</caption>
    <tr>
        <th>Check</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Project Structure</td>
        <td>{'✅ Good' if health['structure_valid'] else '⚠️ Needs Attention'}</td>
    </tr>
    <tr>
        <td>Dependencies</td>
        <td>{'✅ Good' if health['lock_exists'] else '⚠️ Needs Attention'}</td>
    </tr>
</table>

<h2>Recent Activity</h2>

<p>
The system has been active recently with <strong>{len(activity['devlog_entries'])}</strong> 
recent log entries documenting work progress.
</p>

<h2>Summary</h2>

<p>
Overall, the system is {'healthy and active' if health['structure_valid'] and len(git['uncommitted_files']) < 20 else 'needs some attention'}. 
Work is progressing on multiple projects, and the system structure is {'in good shape' if health['structure_valid'] else 'needing review'}.
</p>
"""


def format_professional_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict, epistemic: Dict, gamification: Dict, flight_events: List, kernel: Dict) -> str:
    """Format status for professional audience."""
    kernel_section = ""
    if kernel:
        phase = kernel.get("epistemic_phase", "Unknown")
        epi_state = kernel.get("epistemic_state", {})
        moon = epi_state.get("moon_phase", "🌑")
        know = epi_state.get("knowledge_percentage", 0)
        uncertainty = epi_state.get("uncertainty_percentage", 0)
        systems = kernel.get("systems", {})
        kernel_section = f"""
<h2>WAFT Kernel Operational State</h2>

<h3>Kernel Identity</h3>
<p><strong>Identity:</strong> {kernel.get('identity', 'N/A')}</p>
<p><strong>Mission:</strong> {kernel.get('mission', 'N/A')}</p>
<p><strong>Epistemic Phase:</strong> {phase}</p>

<h3>Epistemic State</h3>
<p><strong>Moon Phase:</strong> {moon}</p>
<p><strong>Knowledge:</strong> {know:.0f}%</p>
<p><strong>Uncertainty:</strong> {uncertainty:.0f}%</p>

<h3>System Integration</h3>
<table>
    <tr>
        <th>System</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Flight Recorder</td>
        <td>{'✅ Operational' if systems.get('flight_recorder', {}).get('operational') else '❌ Not operational'}</td>
    </tr>
    <tr>
        <td>Empirica</td>
        <td>{'✅ Initialized' if systems.get('empirica', {}).get('initialized') else '❌ Not initialized'}</td>
    </tr>
    <tr>
        <td>Gamification</td>
        <td>Level {systems.get('gamification', {}).get('level', 1)}, Integrity: {systems.get('gamification', {}).get('integrity', 0):.0f}%</td>
    </tr>
</table>
"""
    
    return f"""
<h2>System Status Report</h2>

<p><strong>Report Date:</strong> {status['timestamp']}</p>
{kernel_section}

<h2>Git Repository Status</h2>

<h3>Branch Information</h3>
<p><strong>Current Branch:</strong> {git['branch'] or 'N/A'}</p>
<p><strong>Commits Ahead:</strong> {git['commits_ahead']}</p>
<p><strong>Commits Behind:</strong> {git['commits_behind']}</p>

<h3>Uncommitted Changes</h3>
<p><strong>Total Uncommitted Files:</strong> {len(git['uncommitted_files'])}</p>
<p><strong>Staged Files:</strong> {len(git['staged_files'])}</p>
<p><strong>Unstaged Files:</strong> {len(git['unstaged_files'])}</p>

{'<div class="warning"><div class="warning-title">Warning</div>Large number of uncommitted files detected. Consider committing changes.</div>' if len(git['uncommitted_files']) > 20 else ''}

<h3>Recent Commits</h3>
<ul>
{''.join([f'<li>{commit}</li>' for commit in git['recent_commits'][:5]])}
</ul>

<h2>Work Efforts Status</h2>

<table>
    <caption>Work Efforts Breakdown</caption>
    <tr>
        <th>Category</th>
        <th>Count</th>
    </tr>
    <tr>
        <td>Total Work Efforts</td>
        <td>{we['count']}</td>
    </tr>
    <tr>
        <td>Active</td>
        <td>{len(we['active'])}</td>
    </tr>
    <tr>
        <td>Recent</td>
        <td>{len(we['recent'])}</td>
    </tr>
</table>

<h2>Project Health Metrics</h2>

<table>
    <caption>Health Check Results</caption>
    <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>_pyrite Structure</td>
        <td>{'✅ Valid' if health['pyrite_valid'] else '❌ Invalid'}</td>
        <td>{'Structure intact' if health['pyrite_valid'] else 'Missing or corrupted'}</td>
    </tr>
    <tr>
        <td>Directory Structure</td>
        <td>{'✅ Valid' if health['structure_valid'] else '❌ Invalid'}</td>
        <td>{'active/ and backlog/ exist' if health['structure_valid'] else 'Missing required directories'}</td>
    </tr>
    <tr>
        <td>Dependency Lock</td>
        <td>{'✅ Present' if health['lock_exists'] else '❌ Missing'}</td>
        <td>{'uv.lock file exists' if health['lock_exists'] else 'uv.lock not found'}</td>
    </tr>
</table>

<h2>Recent Activity</h2>

<p><strong>Devlog Entries:</strong> {len(activity['devlog_entries'])} recent entries</p>

<h2>Analysis</h2>

<div class="note">
    <div class="note-title">Status Summary</div>
    <ul>
        <li>Git repository is {'synchronized' if git['commits_ahead'] == 0 and git['commits_behind'] == 0 else 'out of sync'}</li>
        <li>Project structure is {'healthy' if health['structure_valid'] else 'needs attention'}</li>
        <li>Work effort activity: {len(we['active'])} active efforts</li>
        <li>Uncommitted changes: {len(git['uncommitted_files'])} files</li>
    </ul>
</div>
"""


def format_scientist_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict, epistemic: Dict, gamification: Dict, flight_events: List) -> str:
    """Format status for scientist audience."""
    # Epistemic analysis
    epistemic_section = ""
    if epistemic.get("initialized", False):
        moon_emoji = epistemic.get("moon_phase", "🌑")
        moon_desc = epistemic.get("moon_phase_desc", "Unknown")
        knowledge_pct = epistemic.get("knowledge_pct")
        uncertainty_pct = epistemic.get("uncertainty_pct")
        vectors = epistemic.get("vectors", {})
        
        epistemic_section = f"""
<h2>Epistemic State Deep Analysis</h2>

<h3>Moon Phase Indicator</h3>
<p><strong>Current Phase:</strong> {moon_emoji} ({moon_desc})</p>
"""
        if knowledge_pct is not None:
            epistemic_section += f"<p><strong>Knowledge Coverage:</strong> {knowledge_pct:.2f}%</p>"
        if uncertainty_pct is not None:
            epistemic_section += f"<p><strong>Uncertainty Level:</strong> {uncertainty_pct:.2f}%</p>"
        
        if vectors:
            epistemic_section += """
<h3>Epistemic Vectors (13 Dimensions)</h3>
<table>
    <tr>
        <th>Vector</th>
        <th>Value</th>
        <th>Analysis</th>
    </tr>
"""
            for key, value in vectors.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            epistemic_section += f"<tr><td>{key}.{sub_key}</td><td>{sub_value:.3f}</td><td>{'High' if sub_value > 0.7 else 'Moderate' if sub_value > 0.4 else 'Low'}</td></tr>"
                elif isinstance(value, (int, float)):
                    epistemic_section += f"<tr><td>{key}</td><td>{value:.3f}</td><td>{'High' if value > 0.7 else 'Moderate' if value > 0.4 else 'Low'}</td></tr>"
            epistemic_section += "</table>"
    else:
        message = epistemic.get("message", "Empirica not initialized")
        epistemic_section = f"""
<h2>Epistemic State Analysis</h2>

<p><strong>Status:</strong> {message}</p>
<p><strong>Impact:</strong> Epistemic tracking unavailable - using heuristic phase detection</p>
"""
    
    # Gamification analysis
    gamification_section = ""
    if gamification.get("available", False):
        level = gamification.get("level", 1)
        integrity = gamification.get("integrity", 100.0)
        insight = gamification.get("insight", 0.0)
        achievements = gamification.get("achievements", [])
        
        gamification_section = f"""
<h2>Gamification Statistical Analysis</h2>

<table>
    <caption>Gamification Metrics</caption>
    <tr>
        <th>Metric</th>
        <th>Value</th>
        <th>Analysis</th>
    </tr>
    <tr>
        <td>Character Level</td>
        <td>{level}</td>
        <td>{'High' if level >= 5 else 'Moderate' if level >= 3 else 'Low'}</td>
    </tr>
    <tr>
        <td>Integrity Score</td>
        <td>{integrity:.2f}%</td>
        <td>{'Excellent' if integrity >= 90 else 'Good' if integrity >= 70 else 'Needs Attention'}</td>
    </tr>
    <tr>
        <td>Insight Points</td>
        <td>{insight:.0f}</td>
        <td>Accumulated knowledge points</td>
    </tr>
    <tr>
        <td>Achievements Unlocked</td>
        <td>{len(achievements)}</td>
        <td>Milestones reached</td>
    </tr>
</table>
"""
    else:
        message = gamification.get("message", "Gamification data not available")
        gamification_section = f"""
<h2>Gamification Analysis</h2>

<p><strong>Status:</strong> {message}</p>
"""
    
    # Flight Recorder analysis
    flight_section = ""
    if flight_events:
        # Analyze event types
        event_types = {}
        for event in flight_events:
            event_type = event.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        flight_section = f"""
<h2>Flight Recorder Event Analysis</h2>

<h3>Recent Events Summary</h3>
<p><strong>Total Events Retrieved:</strong> {len(flight_events)}</p>

<h3>Event Type Distribution</h3>
<table>
    <tr>
        <th>Event Type</th>
        <th>Count</th>
        <th>Percentage</th>
    </tr>
"""
        for event_type, count in event_types.items():
            pct = (count / len(flight_events)) * 100
            flight_section += f"<tr><td>{event_type}</td><td>{count}</td><td>{pct:.1f}%</td></tr>"
        flight_section += "</table>"
        
        # Show recent events
        flight_section += """
<h3>Recent Event Details</h3>
<ul>
"""
        for event in flight_events[-5:]:
            event_type = event.get("event_type", "unknown")
            timestamp = event.get("timestamp", "unknown")
            genome_id = event.get("genome_id", "")[:16] if event.get("genome_id") else "N/A"
            generation = event.get("generation", "N/A")
            flight_section += f"<li><strong>{event_type}</strong> - Generation {generation} - Genome: {genome_id} - {timestamp}</li>"
        flight_section += "</ul>"
    
    return f"""
<h2>Comprehensive System Status Analysis</h2>

<p><strong>Analysis Timestamp:</strong> {status['timestamp']}</p>
<p><strong>Analysis Depth:</strong> Research-Level</p>
{epistemic_section}
{gamification_section}
{flight_section}

<h2>Git Repository Statistical Analysis</h2>

<h3>Branch State</h3>
<table>
    <caption>Branch Metrics</caption>
    <tr>
        <th>Metric</th>
        <th>Value</th>
        <th>Analysis</th>
    </tr>
    <tr>
        <td>Current Branch</td>
        <td>{git['branch'] or 'N/A'}</td>
        <td>{'Main branch' if git['branch'] == 'main' or git['branch'] == 'master' else 'Feature branch'}</td>
    </tr>
    <tr>
        <td>Divergence (Ahead)</td>
        <td>{git['commits_ahead']}</td>
        <td>{'Synchronized' if git['commits_ahead'] == 0 else 'Local commits pending push'}</td>
    </tr>
    <tr>
        <td>Divergence (Behind)</td>
        <td>{git['commits_behind']}</td>
        <td>{'Synchronized' if git['commits_behind'] == 0 else 'Remote commits pending pull'}</td>
    </tr>
</table>

<h3>Change Set Analysis</h3>

<p><strong>Change Set Statistics:</strong></p>
<ul>
    <li>Total uncommitted files: {len(git['uncommitted_files'])}</li>
    <li>Staged files: {len(git['staged_files'])} ({len(git['staged_files'])/max(len(git['uncommitted_files']),1)*100:.1f}% of changes)</li>
    <li>Unstaged files: {len(git['unstaged_files'])} ({len(git['unstaged_files'])/max(len(git['uncommitted_files']),1)*100:.1f}% of changes)</li>
</ul>

<div class="caution">
    <div class="caution-title">Change Set Risk Assessment</div>
    {'High risk: Large number of uncommitted changes detected. Consider incremental commits.' if len(git['uncommitted_files']) > 20 else 'Low risk: Manageable number of uncommitted changes.'}
</div>

<h3>Commit History Analysis</h3>

<p><strong>Recent Commit Patterns:</strong></p>
<ul>
{''.join([f'<li>{commit}</li>' for commit in git['recent_commits'][:10]])}
</ul>

<h2>Work Efforts Statistical Analysis</h2>

<table>
    <caption>Work Efforts Distribution</caption>
    <tr>
        <th>Category</th>
        <th>Count</th>
        <th>Percentage</th>
        <th>Trend Analysis</th>
    </tr>
    <tr>
        <td>Total Work Efforts</td>
        <td>{we['count']}</td>
        <td>100%</td>
        <td>Baseline</td>
    </tr>
    <tr>
        <td>Active Efforts</td>
        <td>{len(we['active'])}</td>
        <td>{len(we['active'])/max(we['count'],1)*100:.1f}%</td>
        <td>{'High activity' if len(we['active'])/max(we['count'],1) > 0.5 else 'Moderate activity'}</td>
    </tr>
    <tr>
        <td>Recent Efforts</td>
        <td>{len(we['recent'])}</td>
        <td>{len(we['recent'])/max(we['count'],1)*100:.1f}%</td>
        <td>In progress</td>
    </tr>
</table>

<h2>Project Health Deep Analysis</h2>

<table>
    <caption>Health Metrics with Risk Assessment</caption>
    <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Risk Level</th>
        <th>Recommendation</th>
    </tr>
    <tr>
        <td>_pyrite Structure</td>
        <td>{'✅ Valid' if health['pyrite_valid'] else '❌ Invalid'}</td>
        <td>{'Low' if health['pyrite_valid'] else 'High'}</td>
        <td>{'No action needed' if health['pyrite_valid'] else 'Run waft init to repair'}</td>
    </tr>
    <tr>
        <td>Directory Structure</td>
        <td>{'✅ Valid' if health['structure_valid'] else '❌ Invalid'}</td>
        <td>{'Low' if health['structure_valid'] else 'High'}</td>
        <td>{'No action needed' if health['structure_valid'] else 'Verify _pyrite structure'}</td>
    </tr>
    <tr>
        <td>Dependency Lock</td>
        <td>{'✅ Present' if health['lock_exists'] else '❌ Missing'}</td>
        <td>{'Low' if health['lock_exists'] else 'Medium'}</td>
        <td>{'No action needed' if health['lock_exists'] else 'Run uv sync to generate lock'}</td>
    </tr>
</table>

<h2>Activity Pattern Analysis</h2>

<p><strong>Recent Activity Metrics:</strong></p>
<ul>
    <li>Devlog entries in recent period: {len(activity['devlog_entries'])}</li>
    <li>Activity level: {'High' if len(activity['devlog_entries']) >= 3 else 'Moderate' if len(activity['devlog_entries']) >= 1 else 'Low'}</li>
</ul>

<h2>Predictive Indicators</h2>

<div class="note">
    <div class="note-title">System Trajectory Analysis</div>
    <ul>
        <li><strong>Development Velocity:</strong> {'High' if len(git['recent_commits']) >= 5 else 'Moderate' if len(git['recent_commits']) >= 2 else 'Low'}</li>
        <li><strong>Work Distribution:</strong> {len(we['active'])} active efforts indicate {'focused development' if len(we['active']) <= 3 else 'parallel development'}</li>
        <li><strong>Change Management:</strong> {len(git['uncommitted_files'])} uncommitted files suggest {'incremental development' if len(git['uncommitted_files']) < 10 else 'batch development pattern'}</li>
    </ul>
</div>

<h2>Research-Level Insights</h2>

<div class="highlight-box">
    <h3>Key Observations</h3>
    <ul>
        <li>System state indicates {'stable development' if health['structure_valid'] and len(git['uncommitted_files']) < 15 else 'active development with potential risk'}</li>
        <li>Work effort distribution shows {'balanced workload' if 0.3 <= len(we['active'])/max(we['count'],1) <= 0.7 else 'concentrated or distributed workload'}</li>
        <li>Git activity pattern suggests {'regular commit cadence' if len(git['recent_commits']) >= 3 else 'irregular or new development cycle'}</li>
    </ul>
</div>
"""


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check WAFT system status and optionally generate documentation'
    )
    parser.add_argument('--docs', action='store_true', help='Generate status documentation')
    parser.add_argument('--level', choices=['layman', 'professional', 'scientist'], help='Documentation level (requires --docs)')
    parser.add_argument('--printer-friendly', action='store_true', help='Generate printer-friendly versions')
    parser.add_argument('--focus', help='Focus on specific area')
    
    args = parser.parse_args()
    
    # Determine project path
    project_path = Path.cwd()
    
    # Check status
    status = check_status(project_path=project_path, log_event=True)
    
    # Display status
    display_status(status)
    
    # Generate docs if requested
    if args.docs:
        generate_status_docs(status, level=args.level, printer_friendly=args.printer_friendly)
        print("\n✓ Status documentation generated")
    
    print()


if __name__ == '__main__':
    main()
