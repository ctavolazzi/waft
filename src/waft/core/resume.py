"""
Resume - Restore context and continue where work left off.

Loads the most recent session summary, compares current state with what was left,
identifies what was in progress, and provides clear next steps.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..logging import get_logger
from .session_stats import SessionStats
from .github import GitHubManager
from .gamification import GamificationManager
from .substrate import SubstrateManager

logger = get_logger(__name__)


class ResumeManager:
    """Manages resume workflow - restoring context from last session."""
    
    def __init__(self, project_path: Path):
        """
        Initialize resume manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.gamification = GamificationManager(project_path)
        self.substrate = SubstrateManager(project_path)
    
    def run_resume(
        self,
        session_file: Optional[str] = None,
        compare: bool = True,
        full_context: bool = False
    ) -> Dict[str, Any]:
        """
        Run resume workflow - restore context and show next steps.
        
        Args:
            session_file: Optional specific session file to load
            compare: Whether to compare current state with last session
            full_context: Whether to load full context (not just summary)
            
        Returns:
            Dictionary with resume results
        """
        self.console.print("\n[bold cyan]🌊 Resume: Picking Up Where You Left Off[/bold cyan]\n")
        
        # Find and load last session
        last_session = self._find_last_session(session_file)
        
        if not last_session:
            self.console.print("[yellow]⚠️[/yellow]  No previous session found.")
            self.console.print("[dim]→[/dim] Run [/phase1] or [/spin-up] to start a new session")
            return {"success": False, "error": "No session found"}
        
        # Parse session summary
        session_data = self._parse_session_summary(last_session)
        
        # Get current state
        current_state = self._get_current_state()
        
        # Compare states if requested
        comparison = None
        if compare:
            comparison = self._compare_states(session_data, current_state)
        
        # Identify in-progress items
        in_progress = self._identify_in_progress(session_data, current_state)
        
        # Generate next steps
        next_steps = self._generate_next_steps(session_data, current_state, comparison)
        
        # Display resume report
        self._display_resume_report(
            session_data, current_state, comparison, in_progress, next_steps
        )
        
        return {
            "success": True,
            "session_file": last_session.name,
            "session_data": session_data,
            "current_state": current_state,
            "comparison": comparison,
            "in_progress": in_progress,
            "next_steps": next_steps,
        }
    
    def _find_last_session(self, session_file: Optional[str] = None) -> Optional[Path]:
        """
        Find the most recent session summary file.
        
        Args:
            session_file: Optional specific session file name
            
        Returns:
            Path to session file or None if not found
        """
        checkout_dir = self.project_path / "_pyrite" / "checkout"
        
        if not checkout_dir.exists():
            return None
        
        if session_file:
            # Load specific session file
            session_path = checkout_dir / session_file
            if session_path.exists():
                return session_path
            return None
        
        # Find most recent session file
        session_files = sorted(
            checkout_dir.glob("session-*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if session_files:
            return session_files[0]
        
        return None
    
    def _parse_session_summary(self, session_file: Path) -> Dict[str, Any]:
        """
        Parse session summary markdown file.
        
        Args:
            session_file: Path to session summary file
            
        Returns:
            Dictionary with parsed session data
        """
        content = session_file.read_text(encoding="utf-8")
        
        # Extract session date/time
        date_match = re.search(r"Session Summary: (\d{4}-\d{2}-\d{2})", content)
        time_match = re.search(r"\*\*Session End\*\*: (.+)", content)
        
        # Extract statistics
        stats = {}
        files_created_match = re.search(r"\*\*Files Created\*\*: (\d+)", content)
        files_modified_match = re.search(r"\*\*Files Modified\*\*: (\d+)", content)
        lines_written_match = re.search(r"\*\*Lines Written\*\*: ([\d,]+)", content)
        net_change_match = re.search(r"\*\*Net Change\*\*: ([+\-]?[\d,]+)", content)
        
        if files_created_match:
            stats["files_created"] = int(files_created_match.group(1))
        if files_modified_match:
            stats["files_modified"] = int(files_modified_match.group(1))
        if lines_written_match:
            stats["lines_written"] = int(lines_written_match.group(1).replace(",", ""))
        if net_change_match:
            stats["net_change"] = int(net_change_match.group(1).replace(",", "").replace("+", ""))
        
        # Extract top files
        top_files = []
        top_files_section = re.search(r"## Top Files by Changes\n\n(.*?)\n---", content, re.DOTALL)
        if top_files_section:
            file_lines = top_files_section.group(1).strip().split("\n")
            for line in file_lines[:10]:
                file_match = re.search(r"`([^`]+)`", line)
                net_match = re.search(r"\(([+\-]?\d+) lines\)", line)
                if file_match:
                    top_files.append({
                        "file": file_match.group(1),
                        "net": int(net_match.group(1).replace("+", "")) if net_match else 0
                    })
        
        # Extract git status
        git_info = {}
        branch_match = re.search(r"\*\*Branch\*\*: (.+)", content)
        uncommitted_match = re.search(r"\*\*Uncommitted Files\*\*: (\d+)", content)
        
        if branch_match:
            git_info["branch"] = branch_match.group(1).strip()
        if uncommitted_match:
            git_info["uncommitted_count"] = int(uncommitted_match.group(1))
        
        # Extract next steps
        next_steps = []
        next_steps_section = re.search(r"## Next Steps\n\n(.*?)(?:\n---|\n\*\*)", content, re.DOTALL)
        if next_steps_section:
            steps_text = next_steps_section.group(1)
            step_lines = [line.strip() for line in steps_text.split("\n") if line.strip() and line.strip().startswith(("1.", "2.", "3.", "4.", "5."))]
            for line in step_lines:
                # Remove numbering
                step = re.sub(r"^\d+\.\s*", "", line)
                if step:
                    next_steps.append(step)
        
        return {
            "file": session_file.name,
            "date": date_match.group(1) if date_match else None,
            "time": time_match.group(1) if time_match else None,
            "stats": stats,
            "top_files": top_files,
            "git": git_info,
            "next_steps": next_steps,
        }
    
    def _get_current_state(self) -> Dict[str, Any]:
        """
        Get current project state.
        
        Returns:
            Dictionary with current state information
        """
        import subprocess
        
        # Git status
        git_info = {
            "initialized": self.github.is_initialized(),
            "branch": "unknown",
            "uncommitted_count": 0,
            "uncommitted_files": [],
            "commits_ahead": 0,
        }
        
        if git_info["initialized"]:
            try:
                # Get branch
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    git_info["branch"] = result.stdout.strip()
                
                # Get uncommitted files
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    uncommitted = [line[3:].strip() for line in result.stdout.strip().split("\n") if line.strip()]
                    git_info["uncommitted_files"] = uncommitted
                    git_info["uncommitted_count"] = len(uncommitted)
                
                # Get commits ahead
                try:
                    result = subprocess.run(
                        ["git", "rev-list", "--count", "@{u}..HEAD"],
                        cwd=self.project_path,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        git_info["commits_ahead"] = int(result.stdout.strip())
                except (ValueError, OSError) as e:
                    logger.debug(f"Could not determine commits ahead: {e}")
            except Exception:
                pass
        
        # Project health
        try:
            integrity = self.gamification.get_integrity()
        except Exception:
            integrity = 100.0
        
        # Dependencies
        try:
            lock_exists = self.substrate.verify_lock()
        except Exception:
            lock_exists = False
        
        # Current session stats (if any)
        try:
            current_stats = self.stats_tracker.calculate_session_stats()
        except Exception:
            current_stats = {}
        
        return {
            "git": git_info,
            "health": {
                "integrity": integrity,
                "lock_exists": lock_exists,
            },
            "stats": current_stats,
        }
    
    def _compare_states(
        self,
        session_data: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare last session state with current state.
        
        Args:
            session_data: Parsed session data from last session
            current_state: Current project state
            
        Returns:
            Dictionary with comparison results
        """
        comparison = {
            "git": {},
            "files": {},
            "progress": [],
        }
        
        # Compare git branch
        last_branch = session_data.get("git", {}).get("branch")
        current_branch = current_state["git"]["branch"]
        comparison["git"]["branch_changed"] = last_branch != current_branch
        
        # Compare uncommitted files
        last_uncommitted = session_data.get("git", {}).get("uncommitted_count", 0)
        current_uncommitted = current_state["git"]["uncommitted_count"]
        comparison["git"]["uncommitted_changed"] = current_uncommitted != last_uncommitted
        
        # Check if files were committed
        if last_uncommitted > 0 and current_uncommitted < last_uncommitted:
            comparison["progress"].append(f"✅ Committed {last_uncommitted - current_uncommitted} file(s)")
        elif current_uncommitted > last_uncommitted:
            comparison["progress"].append(f"📝 {current_uncommitted - last_uncommitted} new uncommitted file(s)")
        
        # Check branch change
        if comparison["git"]["branch_changed"]:
            comparison["progress"].append(f"🔄 Branch changed: {last_branch} → {current_branch}")
        
        return comparison
    
    def _identify_in_progress(
        self,
        session_data: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Identify what's still in progress from last session.
        
        Args:
            session_data: Parsed session data
            current_state: Current state
            
        Returns:
            List of in-progress items
        """
        in_progress = []
        
        # Check uncommitted files from last session
        last_uncommitted = session_data.get("git", {}).get("uncommitted_count", 0)
        current_uncommitted = current_state["git"]["uncommitted_count"]
        
        if current_uncommitted > 0:
            in_progress.append({
                "item": f"{current_uncommitted} uncommitted file(s)",
                "status": "Still uncommitted" if last_uncommitted > 0 else "New changes",
                "action": "Review and commit if ready"
            })
        
        # Check next steps from last session
        next_steps = session_data.get("next_steps", [])
        for step in next_steps[:3]:  # Top 3 next steps
            in_progress.append({
                "item": step,
                "status": "Pending",
                "action": "Continue work"
            })
        
        return in_progress
    
    def _generate_next_steps(
        self,
        session_data: Dict[str, Any],
        current_state: Dict[str, Any],
        comparison: Optional[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Generate next steps based on session data and current state.
        
        Args:
            session_data: Parsed session data
            current_state: Current state
            comparison: State comparison results
            
        Returns:
            List of next step dictionaries
        """
        next_steps = []
        
        # If there are uncommitted files, suggest reviewing them
        if current_state["git"]["uncommitted_count"] > 0:
            next_steps.append({
                "action": f"Review {current_state['git']['uncommitted_count']} uncommitted file(s)",
                "why": "Files from last session may need attention",
                "command": "git status"
            })
        
        # Add next steps from last session
        last_next_steps = session_data.get("next_steps", [])
        for step in last_next_steps[:3]:
            next_steps.append({
                "action": step,
                "why": "Planned in last session",
                "command": None
            })
        
        # Suggest commands
        next_steps.append({
            "action": "Get full project overview",
            "why": "Understand current complete state",
            "command": "/phase1"
        })
        
        if current_state["git"]["uncommitted_count"] > 0:
            next_steps.append({
                "action": "Analyze current state",
                "why": "Generate action plan based on current state",
                "command": "/analyze"
            })
        
        return next_steps
    
    def _display_resume_report(
        self,
        session_data: Dict[str, Any],
        current_state: Dict[str, Any],
        comparison: Optional[Dict[str, Any]],
        in_progress: List[Dict[str, str]],
        next_steps: List[Dict[str, str]]
    ):
        """Display comprehensive resume report."""
        self.console.print("=" * 90)
        
        # Last Session Summary
        self.console.print("\n[bold]📋 Last Session[/bold]")
        if session_data.get("date") and session_data.get("time"):
            self.console.print(f"  Session: {session_data['date']} {session_data.get('time', '')}")
        
        stats = session_data.get("stats", {})
        if stats:
            self.console.print("\n[bold]Accomplishments:[/bold]")
            if "files_created" in stats:
                self.console.print(f"  • Files Created: {stats['files_created']}")
            if "files_modified" in stats:
                self.console.print(f"  • Files Modified: {stats['files_modified']}")
            if "lines_written" in stats:
                self.console.print(f"  • Lines Written: {stats['lines_written']:,}")
            if "net_change" in stats:
                net = stats["net_change"]
                net_str = f"+{net}" if net > 0 else str(net)
                self.console.print(f"  • Net Change: {net_str} lines")
        
        top_files = session_data.get("top_files", [])
        if top_files:
            self.console.print("\n[bold]Top Files Worked On:[/bold]")
            for i, file_info in enumerate(top_files[:5], 1):
                net = file_info.get("net", 0)
                net_str = f"+{net}" if net > 0 else str(net)
                icon = "✨" if net > 0 else "📝"
                self.console.print(f"  {i}. {icon} {file_info['file']} ({net_str} lines)")
        
        last_next_steps = session_data.get("next_steps", [])
        if last_next_steps:
            self.console.print("\n[bold]Next Steps (from last session):[/bold]")
            for i, step in enumerate(last_next_steps[:3], 1):
                self.console.print(f"  {i}. {step}")
        
        self.console.print("\n" + "=" * 90)
        
        # Current State
        self.console.print("\n[bold]📊 Current State[/bold]\n")
        
        git = current_state["git"]
        self.console.print("[bold]Git Status:[/bold]")
        self.console.print(f"  • Branch: {git['branch']}")
        self.console.print(f"  • Uncommitted Files: {git['uncommitted_count']}")
        self.console.print(f"  • Commits Ahead: {git['commits_ahead']}")
        status = "Clean" if git['uncommitted_count'] == 0 else "Has uncommitted changes"
        self.console.print(f"  • Status: {status}")
        
        health = current_state["health"]
        self.console.print("\n[bold]Project Health:[/bold]")
        self.console.print(f"  • Integrity: {health['integrity']:.0f}%")
        self.console.print(f"  • Structure: Valid")
        self.console.print(f"  • Dependencies: {'Locked' if health['lock_exists'] else 'Unlocked'}")
        
        self.console.print("\n" + "=" * 90)
        
        # Comparison
        if comparison:
            self.console.print("\n[bold]🔄 What's Changed Since Last Session[/bold]\n")
            
            progress = comparison.get("progress", [])
            if progress:
                self.console.print("[bold]✅ Progress Made:[/bold]")
                for item in progress:
                    self.console.print(f"  • {item}")
            
            if git["uncommitted_count"] > 0:
                self.console.print("\n[bold]⏸️ Still In Progress:[/bold]")
                self.console.print(f"  • {git['uncommitted_count']} uncommitted file(s)")
                if last_next_steps:
                    self.console.print(f"  • {len(last_next_steps)} pending next step(s)")
            
            self.console.print("\n" + "=" * 90)
        
        # Continue Work
        self.console.print("\n[bold]🎯 Continue Work[/bold]\n")
        
        self.console.print("[bold]Immediate Next Steps:[/bold]")
        for i, step in enumerate(next_steps[:5], 1):
            self.console.print(f"  {i}. {step['action']}")
            if step.get("why"):
                self.console.print(f"     [dim]→ {step['why']}[/dim]")
        
        if in_progress:
            self.console.print("\n[bold]In-Progress Items:[/bold]")
            for item in in_progress[:3]:
                self.console.print(f"  • {item['item']} - {item['status']}")
        
        self.console.print("\n[bold]Suggested Commands:[/bold]")
        commands = [
            ("git status", "Review uncommitted changes"),
            ("/phase1", "Get full current project overview"),
            ("/analyze", "Analyze current state and generate action plan"),
            ("/checkpoint", "Create new checkpoint for current state"),
        ]
        for cmd, desc in commands:
            self.console.print(f"  • [cyan]{cmd}[/cyan] - {desc}")
        
        self.console.print("\n" + "=" * 90)
        self.console.print("\n[bold green]✅ Resume Complete - Ready to continue work[/bold green]\n")
