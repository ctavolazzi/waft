"""
Observers: Event observers for TheChronicler monitoring.

Each observer watches a specific aspect of the system:
- FileSystemObserver: File creation, modification, deletion
- GitObserver: Git commits, branches, changes
- WorkEffortObserver: Work effort status changes, ticket updates
"""

import json
import subprocess
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from watchdog.events import FileSystemEvent, FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = object  # Placeholder for type hints
    FileSystemEvent = object  # Placeholder for type hints


class FileSystemObserver:
    """Observes file system changes using watchdog."""

    def __init__(
        self,
        project_path: Path,
        callback: Callable[[dict[str, Any]], None],
        ignore_patterns: set[str] | None = None,
    ):
        """
        Initialize file system observer.

        Args:
            project_path: Project root to watch
            callback: Function to call with observation dict
            ignore_patterns: Set of patterns to ignore (e.g., {".git", "__pycache__"})
        """
        if not WATCHDOG_AVAILABLE:
            raise RuntimeError("watchdog not available. Install with: uv sync --extra dev")

        self.project_path = Path(project_path).resolve()
        self.callback = callback
        self.ignore_patterns = ignore_patterns or {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            ".venv",
            "venv",
            ".mypy_cache",
            ".ruff_cache",
            "*.pyc",
            ".DS_Store",
        }

        self.observer = Observer()
        self.handler = _FileSystemHandler(self.project_path, self.callback, self.ignore_patterns)
        self.observer.schedule(self.handler, str(self.project_path), recursive=True)

    def start(self):
        """Start observing file system."""
        self.observer.start()

    def stop(self):
        """Stop observing file system."""
        self.observer.stop()
        self.observer.join()

    def is_alive(self) -> bool:
        """Check if observer is running."""
        return self.observer.is_alive()


class _FileSystemHandler(FileSystemEventHandler):
    """Internal handler for file system events."""

    def __init__(
        self,
        project_path: Path,
        callback: Callable[[dict[str, Any]], None],
        ignore_patterns: set[str],
    ):
        self.project_path = project_path
        self.callback = callback
        self.ignore_patterns = ignore_patterns

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        path_str = str(path)
        rel_path = (
            path.relative_to(self.project_path) if path.is_relative_to(self.project_path) else path
        )

        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if pattern in path_str or pattern in str(rel_path):
                return True

        return False

    def _create_observation(
        self, event_type: str, path: Path, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Create observation dictionary."""
        rel_path = (
            path.relative_to(self.project_path) if path.is_relative_to(self.project_path) else path
        )

        obs = {
            "event_type": event_type,
            "observer": "filesystem",
            "path": str(rel_path),
            "absolute_path": str(path),
            "timestamp": datetime.now().isoformat(),
            "is_file": path.is_file() if path.exists() else None,
            "is_directory": path.is_dir() if path.exists() else None,
        }

        if metadata:
            obs.update(metadata)

        return obs

    def on_created(self, event: FileSystemEvent):
        """Handle file/directory creation."""
        if event.is_directory:
            return

        path = Path(event.src_path)
        if self._should_ignore(path):
            return

        try:
            stat = path.stat()
            obs = self._create_observation(
                "genesis",
                path,
                {
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                },
            )
            self.callback(obs)
        except (OSError, FileNotFoundError):
            pass

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification."""
        if event.is_directory:
            return

        path = Path(event.src_path)
        if self._should_ignore(path):
            return

        try:
            stat = path.stat()
            obs = self._create_observation(
                "mutation",
                path,
                {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                },
            )
            self.callback(obs)
        except (OSError, FileNotFoundError):
            pass

    def on_deleted(self, event: FileSystemEvent):
        """Handle file/directory deletion."""
        if event.is_directory:
            return

        path = Path(event.src_path)
        if self._should_ignore(path):
            return

        obs = self._create_observation("exodus", path)
        self.callback(obs)

    def on_moved(self, event: FileSystemEvent):
        """Handle file move/rename."""
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        dest_path = Path(event.dest_path)

        if self._should_ignore(src_path) or self._should_ignore(dest_path):
            return

        # Treat as deletion + creation
        obs_del = self._create_observation("exodus", src_path, {"moved_to": str(dest_path)})
        self.callback(obs_del)

        try:
            stat = dest_path.stat()
            obs_cre = self._create_observation(
                "genesis", dest_path, {"moved_from": str(src_path), "size": stat.st_size}
            )
            self.callback(obs_cre)
        except (OSError, FileNotFoundError):
            pass


class GitObserver:
    """Observes Git repository changes."""

    def __init__(
        self,
        project_path: Path,
        callback: Callable[[dict[str, Any]], None],
        poll_interval: int = 60,
    ):
        """
        Initialize Git observer.

        Args:
            project_path: Project root (must be git repo)
            callback: Function to call with observation dict
            poll_interval: Seconds between git status checks
        """
        self.project_path = Path(project_path)
        self.callback = callback
        self.poll_interval = poll_interval

        self._last_commit_hash: str | None = None
        self._last_status: str | None = None

    def _run_git_command(self, command: str) -> str | None:
        """Run git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + command.split(),
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        return None

    def _get_current_commit(self) -> str | None:
        """Get current commit hash."""
        return self._run_git_command("rev-parse HEAD")

    def _get_recent_commits(self, limit: int = 5) -> list:
        """Get recent commits."""
        output = self._run_git_command(f"log --oneline -n {limit} --format=%H|%s|%an|%ad")
        if not output:
            return []

        commits = []
        for line in output.split("\n"):
            parts = line.split("|", 3)
            if len(parts) >= 4:
                commits.append(
                    {"hash": parts[0], "message": parts[1], "author": parts[2], "date": parts[3]}
                )
        return commits

    def _get_status(self) -> dict[str, Any]:
        """Get git status information."""
        status_output = self._run_git_command("status --porcelain")
        branch = self._run_git_command("branch --show-current")

        if status_output:
            lines = status_output.split("\n")
            modified = [l[3:] for l in lines if l.startswith(" M")]
            added = [l[3:] for l in lines if l.startswith("A ") or l.startswith("??")]
            deleted = [l[3:] for l in lines if l.startswith("D ")]
        else:
            modified = []
            added = []
            deleted = []

        return {
            "branch": branch or "unknown",
            "modified": modified,
            "added": added,
            "deleted": deleted,
            "has_changes": bool(status_output),
        }

    def check(self):
        """Check for git changes and emit observations."""
        current_commit = self._get_current_commit()
        status = self._get_status()

        # Check for new commits
        if current_commit and current_commit != self._last_commit_hash:
            commits = self._get_recent_commits(limit=1)
            if commits:
                commit = commits[0]
                obs = {
                    "event_type": "genesis",
                    "observer": "git",
                    "commit_hash": current_commit,
                    "commit_message": commit.get("message", ""),
                    "author": commit.get("author", ""),
                    "timestamp": datetime.now().isoformat(),
                    "metadata": commit,
                }
                self.callback(obs)

            self._last_commit_hash = current_commit

        # Check for status changes
        status_str = json.dumps(status, sort_keys=True)
        if status_str != self._last_status:
            if status["has_changes"]:
                obs = {
                    "event_type": "mutation",
                    "observer": "git",
                    "status": status,
                    "timestamp": datetime.now().isoformat(),
                }
                self.callback(obs)

            self._last_status = status_str


class WorkEffortObserver:
    """Observes work effort changes."""

    def __init__(
        self,
        project_path: Path,
        callback: Callable[[dict[str, Any]], None],
        poll_interval: int = 300,
    ):
        """
        Initialize work effort observer.

        Args:
            project_path: Project root
            callback: Function to call with observation dict
            poll_interval: Seconds between checks
        """
        self.project_path = Path(project_path)
        self.callback = callback
        self.poll_interval = poll_interval

        self.work_efforts_dir = self.project_path / "_work_efforts"
        self._known_work_efforts: set[str] = set()
        self._known_tickets: set[str] = set()

    def _scan_work_efforts(self) -> set[str]:
        """Scan for work effort directories."""
        if not self.work_efforts_dir.exists():
            return set()

        work_efforts = set()
        for item in self.work_efforts_dir.iterdir():
            if item.is_dir() and item.name.startswith("WE-"):
                work_efforts.add(item.name)

        return work_efforts

    def _scan_tickets(self, work_effort_dir: Path) -> set[str]:
        """Scan for ticket files in a work effort."""
        tickets_dir = work_effort_dir / "tickets"
        if not tickets_dir.exists():
            return set()

        tickets = set()
        for ticket_file in tickets_dir.glob("TKT-*.md"):
            tickets.add(ticket_file.name)

        return tickets

    def check(self):
        """Check for work effort changes and emit observations."""
        current_work_efforts = self._scan_work_efforts()

        # Check for new work efforts (genesis)
        new_work_efforts = current_work_efforts - self._known_work_efforts
        for we_id in new_work_efforts:
            we_dir = self.work_efforts_dir / we_id
            obs = {
                "event_type": "genesis",
                "observer": "work_effort",
                "work_effort_id": we_id,
                "path": str(we_dir.relative_to(self.project_path)),
                "timestamp": datetime.now().isoformat(),
            }
            self.callback(obs)

        # Check for deleted work efforts (exodus)
        deleted_work_efforts = self._known_work_efforts - current_work_efforts
        for we_id in deleted_work_efforts:
            obs = {
                "event_type": "exodus",
                "observer": "work_effort",
                "work_effort_id": we_id,
                "timestamp": datetime.now().isoformat(),
            }
            self.callback(obs)

        self._known_work_efforts = current_work_efforts

        # Check for ticket changes in existing work efforts
        for we_id in current_work_efforts:
            we_dir = self.work_efforts_dir / we_id
            current_tickets = self._scan_tickets(we_dir)
            ticket_key = f"{we_id}:tickets"

            if ticket_key not in self._known_tickets:
                self._known_tickets.add(ticket_key)
                # Initial scan, don't emit for existing tickets
                continue

            # Check for new tickets
            for ticket_file in current_tickets:
                if ticket_file not in self._known_tickets:
                    obs = {
                        "event_type": "genesis",
                        "observer": "work_effort",
                        "work_effort_id": we_id,
                        "ticket_id": ticket_file,
                        "timestamp": datetime.now().isoformat(),
                    }
                    self.callback(obs)
                    self._known_tickets.add(ticket_file)
