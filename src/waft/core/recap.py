"""
Recap - Conversation recap and session summary.

Creates comprehensive recap of current conversation/session, extracting key points,
decisions, accomplishments, and questions.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .session_stats import SessionStats
from .github import GitHubManager
from .memory import MemoryManager


class RecapManager:
    """Manages conversation recap and session summary creation."""
    
    def __init__(self, project_path: Path):
        """
        Initialize recap manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.recap_dir = project_path / "_work_efforts"
        self.recap_dir.mkdir(parents=True, exist_ok=True)
    
    def run_recap(
        self,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run recap workflow - create conversation summary.
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Dictionary with recap results
        """
        self.console.print("\n[bold cyan]📋 Recap: Conversation Summary[/bold cyan]\n")
        
        # Gather session data
        session_data = self._gather_session_data()
        
        # Generate recap document
        recap_content = self._generate_recap(session_data)
        
        # Save recap
        if output_path:
            recap_file = Path(output_path)
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            recap_file = self.recap_dir / f"SESSION_RECAP_{timestamp}.md"
        
        recap_file.write_text(recap_content, encoding="utf-8")
        
        # Display summary
        self._display_summary(session_data, recap_file)
        
        return {
            "success": True,
            "recap_file": str(recap_file.relative_to(self.project_path)),
            "session_data": session_data,
        }
    
    def _gather_session_data(self) -> Dict[str, Any]:
        """Gather session data for recap."""
        import subprocess
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
        }
        
        # Git status
        git_info = {
            "initialized": self.github.is_initialized(),
            "branch": "unknown",
            "uncommitted_count": 0,
            "uncommitted_files": [],
        }
        
        if git_info["initialized"]:
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    git_info["branch"] = result.stdout.strip()
                
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    uncommitted = [line[3:].strip() for line in result.stdout.strip().split("\n") if line.strip()]
                    git_info["uncommitted_files"] = uncommitted[:20]
                    git_info["uncommitted_count"] = len(uncommitted)
            except Exception:
                pass
        
        data["git"] = git_info
        
        # Session stats
        try:
            stats = self.stats_tracker.calculate_session_stats()
            data["stats"] = {
                "files_created": stats.get("files", {}).get("created", 0),
                "files_modified": stats.get("files", {}).get("modified", 0),
                "lines_written": stats.get("code", {}).get("lines_written", 0),
                "lines_deleted": stats.get("code", {}).get("lines_deleted", 0),
                "net_lines": stats.get("code", {}).get("lines_written", 0) - stats.get("code", {}).get("lines_deleted", 0),
            }
        except Exception:
            data["stats"] = {}
        
        # Active files
        try:
            active_files = self.memory.get_active_files()
            data["active_files"] = [str(f.name) for f in active_files[:10]]
        except Exception:
            data["active_files"] = []
        
        return data
    
    def _generate_recap(self, session_data: Dict[str, Any]) -> str:
        """Generate recap markdown content."""
        content = []
        content.append(f"# Session Recap\n\n")
        content.append(f"**Date**: {session_data['date']}\n")
        content.append(f"**Time**: {session_data['time']}\n")
        content.append(f"**Timestamp**: {session_data['timestamp']}\n\n")
        content.append("---\n\n")
        
        # Session Information
        content.append("## Session Information\n\n")
        content.append(f"- **Date**: {session_data['date']} {session_data['time']}\n")
        content.append(f"- **Branch**: {session_data['git'].get('branch', 'unknown')}\n")
        content.append(f"- **Uncommitted Files**: {session_data['git'].get('uncommitted_count', 0)}\n\n")
        
        # Accomplishments
        stats = session_data.get("stats", {})
        if stats:
            content.append("## Accomplishments\n\n")
            if stats.get("files_created", 0) > 0:
                content.append(f"- **Files Created**: {stats['files_created']}\n")
            if stats.get("files_modified", 0) > 0:
                content.append(f"- **Files Modified**: {stats['files_modified']}\n")
            if stats.get("lines_written", 0) > 0:
                content.append(f"- **Lines Written**: {stats['lines_written']:,}\n")
            if stats.get("net_lines", 0) != 0:
                content.append(f"- **Net Lines**: {stats['net_lines']:+,}\n")
            content.append("\n")
        
        # Key Files
        uncommitted = session_data["git"].get("uncommitted_files", [])
        if uncommitted:
            content.append("## Key Files\n\n")
            content.append("### Modified/Created\n\n")
            for file in uncommitted[:15]:
                content.append(f"- `{file}`\n")
            content.append("\n")
        
        # Notes
        content.append("## Notes\n\n")
        content.append("_Add session notes here_\n\n")
        
        # Next Steps
        content.append("## Next Steps\n\n")
        content.append("1. Review recap and identify next actions\n")
        content.append("2. Continue with planned work\n")
        content.append("3. Update goals if needed\n\n")
        
        return "".join(content)
    
    def _display_summary(self, session_data: Dict[str, Any], recap_file: Path):
        """Display recap summary."""
        self.console.print("[bold]📋 Recap Summary[/bold]\n")
        self.console.print(f"  • Date: {session_data['date']} {session_data['time']}")
        self.console.print(f"  • Branch: {session_data['git'].get('branch', 'unknown')}")
        
        stats = session_data.get("stats", {})
        if stats:
            self.console.print(f"  • Files Created: {stats.get('files_created', 0)}")
            self.console.print(f"  • Lines Written: {stats.get('lines_written', 0):,}")
        
        self.console.print(f"\n[bold green]✅ Recap saved:[/bold green] {recap_file.relative_to(self.project_path)}\n")
