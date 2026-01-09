"""
Audit - Conversation audit and quality analysis.

Analyzes current conversation for quality, completeness, potential issues,
and provides recommendations for improvement.
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


class AuditManager:
    """Manages conversation audit and quality analysis."""
    
    def __init__(self, project_path: Path):
        """
        Initialize audit manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.audit_dir = project_path / "_work_efforts"
        self.audit_dir.mkdir(parents=True, exist_ok=True)
    
    def run_audit(
        self,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run audit workflow - analyze conversation quality.
        
        Args:
            output_path: Optional custom output path
            
        Returns:
            Dictionary with audit results
        """
        self.console.print("\n[bold cyan]🔍 Audit: Conversation Analysis[/bold cyan]\n")
        
        # Gather conversation data
        audit_data = self._gather_audit_data()
        
        # Analyze conversation
        analysis = self._analyze_conversation(audit_data)
        
        # Generate audit report
        audit_content = self._generate_audit_report(audit_data, analysis)
        
        # Save audit
        if output_path:
            audit_file = Path(output_path)
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            audit_file = self.audit_dir / f"AUDIT_{timestamp}.md"
        
        audit_file.write_text(audit_content, encoding="utf-8")
        
        # Display summary
        self._display_summary(analysis, audit_file)
        
        return {
            "success": True,
            "audit_file": str(audit_file.relative_to(self.project_path)),
            "analysis": analysis,
        }
    
    def _gather_audit_data(self) -> Dict[str, Any]:
        """Gather data for audit analysis."""
        import subprocess
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
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
    
    def _analyze_conversation(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze conversation for quality, completeness, and issues.
        
        This is a framework that the AI will fill in based on actual
        conversation context available to it.
        """
        analysis = {
            "quality_score": 0,
            "completeness_score": 0,
            "issues": [],
            "recommendations": [],
            "missing_info": [],
            "best_practices": {},
        }
        
        # Quality metrics (AI will assess based on conversation)
        # Framework provides structure, AI fills in actual assessment
        analysis["quality"] = {
            "clarity": 0,
            "coherence": 0,
            "completeness": 0,
            "specificity": 0,
            "actionability": 0,
        }
        
        # Issues framework
        analysis["issues"] = [
            # AI will populate based on actual conversation
        ]
        
        # Recommendations framework
        analysis["recommendations"] = [
            # AI will populate based on actual conversation
        ]
        
        # Missing information
        analysis["missing_info"] = [
            # AI will identify gaps
        ]
        
        # Best practices
        analysis["best_practices"] = {
            "code_quality": "pending",
            "documentation": "pending",
            "security": "pending",
            "maintainability": "pending",
        }
        
        return analysis
    
    def _generate_audit_report(self, audit_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate audit markdown report."""
        content = []
        content.append(f"# Conversation Audit\n\n")
        content.append(f"**Date**: {audit_data['date']}\n")
        content.append(f"**Time**: {audit_data['time']}\n")
        content.append(f"**Timestamp**: {audit_data['timestamp']}\n\n")
        content.append("---\n\n")
        
        # Executive Summary
        content.append("## Executive Summary\n\n")
        content.append("_This audit analyzes the conversation for quality, completeness, issues, and provides recommendations._\n\n")
        content.append("**Note**: This is a framework audit. The AI will analyze the actual conversation context and fill in specific findings.\n\n")
        
        # Session Information
        content.append("## Session Information\n\n")
        content.append(f"- **Date**: {audit_data['date']} {audit_data['time']}\n")
        content.append(f"- **Branch**: {audit_data['git'].get('branch', 'unknown')}\n")
        content.append(f"- **Uncommitted Files**: {audit_data['git'].get('uncommitted_count', 0)}\n\n")
        
        # Quality Analysis
        content.append("## Quality Analysis\n\n")
        content.append("### Communication Quality\n\n")
        content.append("_AI will assess based on actual conversation:_\n\n")
        content.append("- **Clarity**: _To be assessed_\n")
        content.append("- **Coherence**: _To be assessed_\n")
        content.append("- **Completeness**: _To be assessed_\n\n")
        
        # Completeness Check
        content.append("## Completeness Check\n\n")
        content.append("### Missing Information\n\n")
        content.append("_AI will identify missing context or unclear requirements._\n\n")
        
        # Issues Found
        content.append("## Issues Found\n\n")
        content.append("### High Severity\n\n")
        content.append("_AI will identify high-priority issues._\n\n")
        content.append("### Medium Severity\n\n")
        content.append("_AI will identify medium-priority issues._\n\n")
        content.append("### Low Severity\n\n")
        content.append("_AI will identify low-priority issues._\n\n")
        
        # Best Practices Review
        content.append("## Best Practices Review\n\n")
        content.append("### Code Quality\n\n")
        content.append("_AI will assess code quality based on files created/modified._\n\n")
        content.append("### Security\n\n")
        content.append("_AI will check for security considerations._\n\n")
        content.append("### Maintainability\n\n")
        content.append("_AI will assess maintainability._\n\n")
        
        # Recommendations
        content.append("## Recommendations\n\n")
        content.append("### Priority 1 (Immediate)\n\n")
        content.append("_AI will provide immediate action items._\n\n")
        content.append("### Priority 2 (Important)\n\n")
        content.append("_AI will provide important improvements._\n\n")
        content.append("### Priority 3 (Nice to Have)\n\n")
        content.append("_AI will provide optional enhancements._\n\n")
        
        # Next Steps
        content.append("## Next Steps\n\n")
        content.append("1. Review audit findings\n")
        content.append("2. Address priority recommendations\n")
        content.append("3. Continue with planned work\n")
        content.append("4. Update goals if needed\n\n")
        
        # Notes
        content.append("## Notes\n\n")
        content.append("_Add audit notes here_\n\n")
        
        return "".join(content)
    
    def _display_summary(self, analysis: Dict[str, Any], audit_file: Path):
        """Display audit summary."""
        self.console.print("[bold]🔍 Audit Summary[/bold]\n")
        self.console.print(f"  • Quality: Framework ready for AI analysis")
        self.console.print(f"  • Issues: To be identified by AI")
        self.console.print(f"  • Recommendations: To be generated by AI")
        
        self.console.print(f"\n[bold green]✅ Audit saved:[/bold green] {audit_file.relative_to(self.project_path)}\n")
        self.console.print("[dim]Note: This is a framework. The AI will analyze the actual conversation[/dim]")
        self.console.print("[dim]and fill in specific findings based on available context.[/dim]\n")
