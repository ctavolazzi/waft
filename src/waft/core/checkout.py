"""
Checkout - End of session workflow orchestration.

Orchestrates comprehensive end-of-session tasks including statistics,
checkpoint creation, documentation updates, and session summaries.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .session_stats import SessionStats
from .session_analytics import SessionAnalytics, SessionRecord
from .github import GitHubManager


class CheckoutManager:
    """Manages end-of-session checkout workflow."""

    def __init__(self, project_path: Path):
        """
        Initialize checkout manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.analytics = SessionAnalytics(project_path)
        self.github = GitHubManager(project_path)

    def run_checkout(self, quick: bool = False, silent: bool = False) -> Dict[str, Any]:
        """
        Run complete checkout workflow.

        Args:
            quick: If True, skip detailed statistics
            silent: If True, minimal console output

        Returns:
            Dictionary with checkout results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "files_created": [],
            "errors": [],
        }

        if not silent:
            self.console.print("\n[bold cyan]🚪 Checkout: Ending Chat Session[/bold cyan]\n")
            self.console.print("━" * 80)

        # Phase 1: Session Statistics
        if not quick:
            stats_result = self._phase_statistics(silent)
            results["phases"]["statistics"] = stats_result
            if stats_result.get("error"):
                results["errors"].append("Statistics phase failed")

        # Phase 2: Git Status Review
        git_result = self._phase_git_review(silent)
        results["phases"]["git"] = git_result

        # Phase 3: Create Summary
        summary_result = self._phase_summary(results, silent)
        results["phases"]["summary"] = summary_result
        if summary_result.get("error"):
            results["errors"].append("Summary phase failed")

        # Phase 4: Save Analytics
        analytics_result = self._phase_analytics(results, silent)
        results["phases"]["analytics"] = analytics_result
        if analytics_result.get("error"):
            results["errors"].append("Analytics phase failed")

        # Phase 5: Final Summary
        if not silent:
            self._display_final_summary(results)

        return results

    def _phase_statistics(self, silent: bool) -> Dict[str, Any]:
        """Phase 1: Capture session statistics."""
        if not silent:
            self.console.print("\n[bold]Phase 1: Session Statistics[/bold]")

        try:
            stats = self.stats_tracker.calculate_session_stats()
            
            # Save statistics
            stats_dir = self.project_path / "_pyrite" / "phase1"
            stats_dir.mkdir(parents=True, exist_ok=True)
            stats_file = stats_dir / f"session-stats-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.json"
            stats_file.write_text(json.dumps(stats, indent=2), encoding="utf-8")

            if not silent:
                self.console.print(f"  [green]✓[/green] Files created: {stats['files']['created']}")
                self.console.print(f"  [green]✓[/green] Files modified: {stats['files']['modified']}")
                self.console.print(f"  [green]✓[/green] Lines written: {stats['code']['lines_written']:,}")
                self.console.print(f"  [green]✓[/green] Net change: {stats['code']['net_change']:+,} lines")
                self.console.print(f"  [green]✓[/green] Statistics saved: {stats_file.relative_to(self.project_path)}")

            return {
                "success": True,
                "stats_file": str(stats_file.relative_to(self.project_path)),
                "stats": stats,
            }
        except Exception as e:
            if not silent:
                self.console.print(f"  [red]✗[/red] Error: {e}")
            return {"success": False, "error": str(e)}

    def _phase_git_review(self, silent: bool) -> Dict[str, Any]:
        """Phase 2: Review git status."""
        if not silent:
            self.console.print("\n[bold]Phase 2: Git Status Review[/bold]")

        if not self.github.is_initialized():
            if not silent:
                self.console.print("  [yellow]⚠[/yellow]  Git not initialized")
            return {"success": True, "initialized": False}

        try:
            # Get git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )

            uncommitted = [line for line in result.stdout.strip().split("\n") if line.strip()]
            uncommitted_count = len(uncommitted)

            # Get branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )
            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

            if not silent:
                if uncommitted_count > 0:
                    self.console.print(f"  [yellow]⚠[/yellow]  {uncommitted_count} uncommitted files")
                    self.console.print("  [dim]💡[/dim] Suggestion: Consider committing changes")
                    self.console.print("     [dim]git add .[/dim]")
                    self.console.print(f"     [dim]git commit -m \"Session: [description]\"[/dim]")
                else:
                    self.console.print("  [green]✓[/green] No uncommitted changes")

            return {
                "success": True,
                "initialized": True,
                "branch": branch,
                "uncommitted_count": uncommitted_count,
                "uncommitted_files": uncommitted[:10],  # First 10
            }
        except Exception as e:
            if not silent:
                self.console.print(f"  [red]✗[/red] Error: {e}")
            return {"success": False, "error": str(e)}

    def _phase_summary(self, results: Dict[str, Any], silent: bool) -> Dict[str, Any]:
        """Phase 3: Create session summary."""
        if not silent:
            self.console.print("\n[bold]Phase 3: Session Summary[/bold]")

        try:
            # Get statistics if available
            stats = results["phases"].get("statistics", {}).get("stats")
            if not stats:
                # Calculate if not available
                stats = self.stats_tracker.calculate_session_stats()

            # Get git info
            git_info = results["phases"].get("git", {})

            # Create summary
            summary_dir = self.project_path / "_pyrite" / "checkout"
            summary_dir.mkdir(parents=True, exist_ok=True)
            summary_file = summary_dir / f"session-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"

            summary_content = self._generate_summary_content(stats, git_info)
            summary_file.write_text(summary_content, encoding="utf-8")

            if not silent:
                self.console.print(f"  [green]✓[/green] Summary created: {summary_file.relative_to(self.project_path)}")

            return {
                "success": True,
                "summary_file": str(summary_file.relative_to(self.project_path)),
            }
        except Exception as e:
            if not silent:
                self.console.print(f"  [red]✗[/red] Error: {e}")
            return {"success": False, "error": str(e)}

    def _generate_summary_content(self, stats: Dict[str, Any], git_info: Dict[str, Any]) -> str:
        """Generate session summary markdown content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")

        content = []
        content.append(f"# Session Summary: {date_str}\n")
        content.append(f"\n**Session End**: {timestamp}\n")
        content.append("**Status**: ✅ Complete\n")
        content.append("\n---\n\n")

        # Quick Stats
        content.append("## Quick Stats\n\n")
        content.append(f"- **Files Created**: {stats['files']['created']}\n")
        content.append(f"- **Files Modified**: {stats['files']['modified']}\n")
        content.append(f"- **Lines Written**: {stats['code']['lines_written']:,}\n")
        content.append(f"- **Net Change**: {stats['code']['net_change']:+,} lines\n")
        content.append(f"- **Total Operations**: {stats['files']['total_operations']}\n")
        content.append("\n---\n\n")

        # Top Files
        if stats.get("top_files"):
            content.append("## Top Files by Changes\n\n")
            for i, file_info in enumerate(stats["top_files"][:10], 1):
                status_icon = "✨" if file_info.get("status") == "created" else "📝"
                net = file_info.get("net", 0)
                net_str = f"+{net}" if net > 0 else str(net)
                content.append(f"{i}. {status_icon} `{file_info['file']}` ({net_str} lines)\n")
            content.append("\n---\n\n")

        # Files by Type
        if stats.get("by_type"):
            content.append("## Files by Type\n\n")
            for ext, data in sorted(stats["by_type"].items(), key=lambda x: x[1]["lines"], reverse=True):
                ext_display = ext if ext != "no-ext" else "(no ext)"
                content.append(f"- **{ext_display}**: {data['created']} created, {data['modified']} modified, {data['lines']:+,} lines\n")
            content.append("\n---\n\n")

        # Git Status
        if git_info.get("initialized"):
            content.append("## Git Status\n\n")
            content.append(f"- **Branch**: {git_info.get('branch', 'unknown')}\n")
            content.append(f"- **Uncommitted Files**: {git_info.get('uncommitted_count', 0)}\n")
            if git_info.get("uncommitted_count", 0) > 0:
                content.append("\n**Suggestion**: Consider committing changes\n")
            content.append("\n---\n\n")

        # Next Steps
        content.append("## Next Steps\n\n")
        content.append("1. Review session summary and statistics\n")
        if git_info.get("uncommitted_count", 0) > 0:
            content.append("2. Commit changes if ready\n")
        content.append("3. Start next session with `/spin-up` or `/phase1`\n")
        content.append("\n---\n\n")

        content.append(f"**Checkout Complete**: {timestamp}\n")

        return "".join(content)

    def _phase_analytics(self, results: Dict[str, Any], silent: bool) -> Dict[str, Any]:
        """Phase 4: Save session analytics for historical tracking."""
        if not silent:
            self.console.print("\n[bold]Phase 4: Analytics & Tracking[/bold]")

        try:
            # Get statistics
            stats = results["phases"].get("statistics", {}).get("stats")
            if not stats:
                stats = self.stats_tracker.calculate_session_stats()

            # Get git info
            git_info = results["phases"].get("git", {})

            # Create session record
            session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            timestamp = datetime.now().isoformat()

            # Extract commands from metadata if available
            commands = results.get("metadata", {}).get("commands", [])
            if not commands:
                # Try to infer from file patterns
                commands = []

            # Generate prompt signature
            category = self._infer_category(stats, git_info)
            prompt_signature = self.analytics.generate_prompt_signature(commands, category)

            # Create session record
            session = SessionRecord(
                session_id=session_id,
                timestamp=timestamp,
                files_created=stats["files"]["created"],
                files_modified=stats["files"]["modified"],
                files_deleted=stats["files"].get("deleted", 0),
                lines_written=stats["code"]["lines_written"],
                lines_modified=stats["code"]["lines_modified"],
                lines_deleted=stats["code"]["lines_deleted"],
                net_lines=stats["code"]["net_change"],
                commands_executed=commands,
                project_name=self.project_path.name,
                branch=git_info.get("branch", ""),
                git_commits_ahead=git_info.get("uncommitted_count", 0),
                prompt_signature=prompt_signature,
                approach_category=category,
                metadata={
                    "top_files": [f["file"] for f in stats.get("top_files", [])[:10]],
                    "file_types": stats.get("by_type", {}),
                }
            )

            # Save to analytics
            success = self.analytics.save_session(session)

            if not silent:
                if success:
                    self.console.print(f"  [green]✓[/green] Session saved: {session_id}")
                    self.console.print(f"  [green]✓[/green] Category: {category}")
                    self.console.print(f"  [green]✓[/green] Analytics database updated")
                else:
                    self.console.print("  [yellow]⚠[/yellow]  Failed to save analytics")

            return {
                "success": success,
                "session_id": session_id,
                "category": category,
            }
        except Exception as e:
            if not silent:
                self.console.print(f"  [red]✗[/red] Error: {e}")
            return {"success": False, "error": str(e)}

    def _infer_category(self, stats: Dict[str, Any], git_info: Dict[str, Any]) -> str:
        """Infer approach category from session data."""
        # Analyze file patterns to infer category
        top_files = [f["file"] for f in stats.get("top_files", [])[:5]]
        
        # Check for command files
        if any(".cursor/commands/" in f for f in top_files):
            return "command_creation"
        
        # Check for tests
        if any("test" in f.lower() for f in top_files):
            return "testing"
        
        # Check for core modules
        if any("core/" in f for f in top_files):
            return "core_development"
        
        # Check for documentation
        if any(f.endswith(".md") and "_work_efforts" in f for f in top_files):
            return "documentation"
        
        # Default
        return "general_development"

    def _display_final_summary(self, results: Dict[str, Any]):
        """Display final checkout summary."""
        self.console.print("\n[bold]Phase 4: Completion[/bold]")
        self.console.print("  [green]✓[/green] Checkout complete!\n")

        self.console.print("━" * 80)

        # Session Summary
        stats = results["phases"].get("statistics", {}).get("stats", {})
        if stats:
            summary_text = Text()
            summary_text.append("📊 Session Summary:\n", style="bold")
            summary_text.append(f"  • Files: {stats['files']['total_operations']} operations ")
            summary_text.append(f"({stats['files']['created']} created, {stats['files']['modified']} modified)\n")
            summary_text.append(f"  • Code: {stats['code']['net_change']:+,} lines net change\n")

            # Top files
            if stats.get("top_files"):
                summary_text.append("\n📁 Top Files:\n", style="bold")
                for file_info in stats["top_files"][:5]:
                    status_icon = "✨" if file_info.get("status") == "created" else "📝"
                    net = file_info.get("net", 0)
                    net_str = f"+{net}" if net > 0 else str(net)
                    summary_text.append(f"  • {status_icon} {file_info['file']} ({net_str} lines)\n", style="dim")

            # Files created
            if stats.get("top_files"):
                created_files = [f for f in stats["top_files"] if f.get("status") == "created"]
                if created_files:
                    summary_text.append("\n📋 Files Created:\n", style="bold")
                    for file_info in created_files[:10]:
                        summary_text.append(f"  • {file_info['file']}\n", style="dim")

            # Documentation
            summary_text.append("\n📚 Documentation:\n", style="bold")
            if results["phases"].get("statistics", {}).get("stats_file"):
                summary_text.append(f"  • Statistics: {results['phases']['statistics']['stats_file']}\n", style="dim")
            if results["phases"].get("summary", {}).get("summary_file"):
                summary_text.append(f"  • Summary: {results['phases']['summary']['summary_file']}\n", style="dim")

            # Next steps
            summary_text.append("\n💡 Next Steps:\n", style="bold")
            summary_text.append("  1. Review session summary and statistics\n", style="dim")
            git_info = results["phases"].get("git", {})
            if git_info.get("uncommitted_count", 0) > 0:
                summary_text.append("  2. Commit changes if ready\n", style="dim")
            summary_text.append("  3. Start next session with `/spin-up` or `/phase1`\n", style="dim")

            self.console.print(Panel(summary_text, title="✅ Session Checkout Complete", border_style="green"))

        self.console.print("\n━" * 80)
        self.console.print("\n[green]✅ Session checkout complete. Ready for next session![/green]\n")
