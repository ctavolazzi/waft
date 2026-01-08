"""
Session Statistics Tracker - Track files and lines per chat session.

Calculates comprehensive statistics about the current session including
files created, modified, deleted, and lines written/changed.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict


class SessionStats:
    """Tracks and calculates session statistics."""

    def __init__(self, project_path: Path):
        """
        Initialize session stats tracker.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path

    def get_git_diff_stats(self) -> Dict[str, Any]:
        """
        Get git diff statistics for modified files.

        Returns:
            Dictionary with additions, deletions, and file changes
        """
        if not (self.project_path / ".git").exists():
            return {
                "additions": 0,
                "deletions": 0,
                "files_changed": 0,
                "file_details": [],
            }

        try:
            # Get diff stats
            result = subprocess.run(
                ["git", "diff", "--numstat", "HEAD"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )

            additions = 0
            deletions = 0
            files_changed = 0
            file_details = []

            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) >= 3:
                    add = int(parts[0]) if parts[0] != "-" else 0
                    delete = int(parts[1]) if parts[1] != "-" else 0
                    filename = parts[2]

                    additions += add
                    deletions += delete
                    files_changed += 1
                    file_details.append({
                        "file": filename,
                        "additions": add,
                        "deletions": delete,
                        "net": add - delete,
                    })

            return {
                "additions": additions,
                "deletions": deletions,
                "files_changed": files_changed,
                "file_details": sorted(file_details, key=lambda x: x["net"], reverse=True),
            }
        except Exception:
            return {
                "additions": 0,
                "deletions": 0,
                "files_changed": 0,
                "file_details": [],
            }

    def get_new_files_stats(self) -> Dict[str, Any]:
        """
        Get statistics for new (untracked) files.

        Returns:
            Dictionary with new files and their line counts
        """
        if not (self.project_path / ".git").exists():
            return {
                "files": [],
                "total_lines": 0,
                "by_type": {},
            }

        try:
            # Get untracked files
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )

            new_files = []
            for line in result.stdout.strip().split("\n"):
                if line.startswith("??"):
                    filename = line[3:].strip()
                    file_path = self.project_path / filename
                    if file_path.is_file():
                        new_files.append(filename)

            # Count lines in new files
            total_lines = 0
            file_details = []
            by_type = defaultdict(lambda: {"count": 0, "lines": 0})

            for filename in new_files:
                file_path = self.project_path / filename
                try:
                    line_count = len(file_path.read_text(encoding="utf-8", errors="ignore").splitlines())
                    total_lines += line_count

                    # Get file extension
                    ext = file_path.suffix or "no-ext"
                    by_type[ext]["count"] += 1
                    by_type[ext]["lines"] += line_count

                    file_details.append({
                        "file": filename,
                        "lines": line_count,
                        "type": ext,
                    })
                except Exception:
                    pass

            return {
                "files": new_files,
                "total_lines": total_lines,
                "file_count": len(new_files),
                "by_type": dict(by_type),
                "file_details": sorted(file_details, key=lambda x: x["lines"], reverse=True),
            }
        except Exception:
            return {
                "files": [],
                "total_lines": 0,
                "file_count": 0,
                "by_type": {},
                "file_details": [],
            }

    def get_modified_files(self) -> List[str]:
        """
        Get list of modified files.

        Returns:
            List of modified file paths
        """
        if not (self.project_path / ".git").exists():
            return []

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=False,
            )

            modified = []
            for line in result.stdout.strip().split("\n"):
                if line and not line.startswith("??") and not line.startswith(" "):
                    # Modified, staged, or deleted files
                    filename = line[3:].strip()
                    if (self.project_path / filename).exists():
                        modified.append(filename)

            return modified
        except Exception:
            return []

    def calculate_session_stats(self) -> Dict[str, Any]:
        """
        Calculate comprehensive session statistics.

        Returns:
            Dictionary with all session statistics
        """
        diff_stats = self.get_git_diff_stats()
        new_files = self.get_new_files_stats()
        modified_files = self.get_modified_files()

        # Combine file details
        all_files = []
        
        # Add new files
        for file_info in new_files["file_details"]:
            all_files.append({
                "file": file_info["file"],
                "status": "created",
                "lines": file_info["lines"],
                "additions": file_info["lines"],
                "deletions": 0,
                "net": file_info["lines"],
            })

        # Add modified files
        for file_info in diff_stats["file_details"]:
            all_files.append({
                "file": file_info["file"],
                "status": "modified",
                "lines": 0,  # We don't have total lines for modified files easily
                "additions": file_info["additions"],
                "deletions": file_info["deletions"],
                "net": file_info["net"],
            })

        # Sort by net change
        all_files.sort(key=lambda x: x["net"], reverse=True)

        # Calculate totals
        total_lines_written = new_files["total_lines"] + diff_stats["additions"]
        total_lines_deleted = diff_stats["deletions"]
        net_change = total_lines_written - total_lines_deleted

        # Group by file type
        by_type = defaultdict(lambda: {"created": 0, "modified": 0, "lines": 0})
        for file_info in all_files:
            ext = Path(file_info["file"]).suffix or "no-ext"
            if file_info["status"] == "created":
                by_type[ext]["created"] += 1
            else:
                by_type[ext]["modified"] += 1
            by_type[ext]["lines"] += file_info["net"]

        return {
            "timestamp": datetime.now().isoformat(),
            "files": {
                "created": new_files["file_count"],
                "modified": len(modified_files),
                "deleted": 0,  # Hard to track without git history
                "total_operations": new_files["file_count"] + len(modified_files),
            },
            "code": {
                "lines_written": total_lines_written,
                "lines_modified": diff_stats["additions"],
                "lines_deleted": total_lines_deleted,
                "net_change": net_change,
            },
            "file_details": all_files[:20],  # Top 20 files
            "by_type": dict(by_type),
            "top_files": all_files[:10],
        }

    def format_stats(self, stats: Dict[str, Any], detailed: bool = False) -> str:
        """
        Format statistics for display.

        Args:
            stats: Statistics dictionary
            detailed: If True, show detailed breakdown

        Returns:
            Formatted string with statistics
        """
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text

        console = Console()

        # Create summary table
        summary_table = Table(show_header=False, box=None, padding=(0, 2))
        summary_table.add_column("Metric", style="bold cyan", width=25)
        summary_table.add_column("Value", style="bold", width=20)

        # Files section
        files = stats["files"]
        summary_table.add_row("📁 Files Created", f"{files['created']} files", style="green")
        summary_table.add_row("📝 Files Modified", f"{files['modified']} files", style="yellow")
        summary_table.add_row("📦 Total Operations", f"{files['total_operations']} operations", style="bold")

        summary_table.add_row("", "")  # Spacer

        # Code section
        code = stats["code"]
        summary_table.add_row("➕ Lines Written", f"{code['lines_written']:,} lines", style="green")
        summary_table.add_row("🔄 Lines Modified", f"{code['lines_modified']:,} lines", style="yellow")
        summary_table.add_row("➖ Lines Deleted", f"{code['lines_deleted']:,} lines", style="red")
        summary_table.add_row("📊 Net Change", f"{code['net_change']:+,} lines", style="bold cyan")

        # Build output
        output = Text()
        output.append("📊 Session Statistics\n\n", style="bold cyan")
        output.append(str(summary_table))

        if detailed and stats["top_files"]:
            output.append("\n\n", style="reset")
            output.append("🔝 Top Files by Changes:\n", style="bold")
            
            for i, file_info in enumerate(stats["top_files"][:10], 1):
                status_icon = "✨" if file_info["status"] == "created" else "📝"
                net = file_info["net"]
                net_str = f"+{net}" if net > 0 else str(net)
                net_style = "green" if net > 0 else "red" if net < 0 else "dim"
                output.append(f"  {i:2}. {status_icon} ", style="dim")
                output.append(f"{file_info['file']:<50} ", style="white")
                output.append(f"{net_str:>8} lines\n", style=net_style)

        if detailed and stats["by_type"]:
            output.append("\n\n", style="reset")
            output.append("📂 Files by Type:\n", style="bold")
            
            type_table = Table(show_header=True, header_style="bold", box=None)
            type_table.add_column("Type", style="cyan")
            type_table.add_column("Created", style="green", justify="right")
            type_table.add_column("Modified", style="yellow", justify="right")
            type_table.add_column("Net Lines", style="bold", justify="right")

            for ext, data in sorted(stats["by_type"].items(), key=lambda x: x[1]["lines"], reverse=True):
                ext_display = ext if ext != "no-ext" else "(no ext)"
                type_table.add_row(
                    ext_display,
                    str(data["created"]),
                    str(data["modified"]),
                    f"{data['lines']:+,}",
                )

            output.append(str(type_table))

        return str(output)
