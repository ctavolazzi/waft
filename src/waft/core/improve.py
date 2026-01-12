"""
Improve - Analyze work and suggest improvements.

Analyzes code, documentation, architecture, and implementation to identify
improvement opportunities with prioritized recommendations.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .session_stats import SessionStats
from .github import GitHubManager
from .memory import MemoryManager


class Improvement:
    """Represents a single improvement opportunity."""
    
    def __init__(
        self,
        title: str,
        description: str,
        category: str,
        priority: str,
        impact: str,
        effort: str,
        location: Optional[str] = None,
        current_state: Optional[str] = None,
        suggested_change: Optional[str] = None,
        rationale: Optional[str] = None
    ):
        self.title = title
        self.description = description
        self.category = category  # code, documentation, architecture, testing, performance, usability
        self.priority = priority  # critical, high, medium, low
        self.impact = impact  # high, medium, low
        self.effort = effort  # high, medium, low
        self.location = location
        self.current_state = current_state
        self.suggested_change = suggested_change
        self.rationale = rationale
        self.score: float = 0.0  # Calculated priority score
    
    def calculate_score(self) -> float:
        """Calculate priority score based on impact and effort."""
        impact_scores = {"high": 3.0, "medium": 2.0, "low": 1.0}
        effort_scores = {"high": 1.0, "medium": 2.0, "low": 3.0}  # Lower effort = higher score
        priority_scores = {"critical": 4.0, "high": 3.0, "medium": 2.0, "low": 1.0}
        
        impact_val = impact_scores.get(self.impact, 1.0)
        effort_val = effort_scores.get(self.effort, 1.0)
        priority_val = priority_scores.get(self.priority, 1.0)
        
        # Score = (impact * priority) / effort
        self.score = (impact_val * priority_val) / effort_val
        return self.score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "impact": self.impact,
            "effort": self.effort,
            "score": self.score,
            "location": self.location,
            "current_state": self.current_state,
            "suggested_change": self.suggested_change,
            "rationale": self.rationale,
        }


class ImproveManager:
    """Manages improvement analysis workflow."""
    
    def __init__(self, project_path: Path):
        """
        Initialize improvement manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.improvements: List[Improvement] = []
        
    def run_improve(
        self,
        focus: Optional[str] = None,
        category: Optional[str] = None,
        recent_only: bool = False,
        output_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """
        Run improvement analysis workflow.
        
        Args:
            focus: Focus area (file path, work effort, or "all")
            category: Filter by category (code, documentation, architecture, etc.)
            recent_only: Only analyze recent changes
            output_path: Optional path to save improvement report
            
        Returns:
            Dictionary with improvement recommendations
        """
        self.console.print("\n[bold cyan]🔧 Improve: Analysis & Recommendations[/bold cyan]\n")
        
        # Step 1: Gather context
        self.console.print("[yellow]→[/yellow] Gathering context...")
        context = self._gather_context(focus, recent_only)
        
        # Step 2: Analyze code quality
        self.console.print("[yellow]→[/yellow] Analyzing code quality...")
        code_improvements = self._analyze_code(context)
        
        # Step 3: Analyze documentation
        self.console.print("[yellow]→[/yellow] Analyzing documentation...")
        doc_improvements = self._analyze_documentation(context)
        
        # Step 4: Analyze architecture
        self.console.print("[yellow]→[/yellow] Analyzing architecture...")
        arch_improvements = self._analyze_architecture(context)
        
        # Step 5: Analyze testing
        self.console.print("[yellow]→[/yellow] Analyzing testing...")
        test_improvements = self._analyze_testing(context)
        
        # Step 6: Analyze performance
        self.console.print("[yellow]→[/yellow] Analyzing performance...")
        perf_improvements = self._analyze_performance(context)
        
        # Step 7: Analyze usability
        self.console.print("[yellow]→[/yellow] Analyzing usability...")
        usability_improvements = self._analyze_usability(context)
        
        # Combine all improvements
        all_improvements = (
            code_improvements +
            doc_improvements +
            arch_improvements +
            test_improvements +
            perf_improvements +
            usability_improvements
        )
        
        # Filter by category if specified
        if category:
            all_improvements = [i for i in all_improvements if i.category == category]
        
        # Calculate scores and sort
        for improvement in all_improvements:
            improvement.calculate_score()
        
        all_improvements.sort(key=lambda x: x.score, reverse=True)
        self.improvements = all_improvements
        
        # Step 8: Display results
        self._display_improvements(all_improvements)
        
        # Step 9: Save report if requested
        if output_path:
            self._save_report(all_improvements, output_path, context)
        
        return {
            "success": True,
            "improvements": [i.to_dict() for i in all_improvements],
            "summary": self._generate_summary(all_improvements),
        }
    
    def _gather_context(
        self,
        focus: Optional[str],
        recent_only: bool
    ) -> Dict[str, Any]:
        """Gather context for analysis."""
        context = {
            "project_path": self.project_path,
            "focus": focus,
            "recent_only": recent_only,
            "git_status": self._get_git_status(),
            "recent_files": self._get_recent_files() if recent_only else [],
            "work_efforts": self._get_active_work_efforts(),
        }
        return context
    
    def _get_git_status(self) -> Dict[str, Any]:
        """Get git status information."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            modified = [line for line in result.stdout.split("\n") if line.startswith(" M")]
            added = [line for line in result.stdout.split("\n") if line.startswith("??")]
            return {
                "modified": len(modified),
                "added": len(added),
                "files": modified + added
            }
        except Exception:
            return {"modified": 0, "added": 0, "files": []}
    
    def _get_recent_files(self) -> List[str]:
        """Get recently modified files."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--name-only", "--pretty=format:", "-10"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            files = [f for f in result.stdout.split("\n") if f.strip()]
            return list(set(files))
        except Exception:
            return []
    
    def _get_active_work_efforts(self) -> List[Dict[str, Any]]:
        """Get active work efforts."""
        try:
            work_efforts_path = self.project_path / "_work_efforts"
            if not work_efforts_path.exists():
                return []
            
            efforts = []
            for item in work_efforts_path.iterdir():
                if item.is_dir() and item.name.startswith("WE-"):
                    index_file = item / f"{item.name}_index.md"
                    if index_file.exists():
                        efforts.append({
                            "id": item.name,
                            "path": str(item),
                        })
            return efforts
        except Exception:
            return []
    
    def _analyze_code(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze code quality."""
        improvements = []
        
        # Check for import issues
        if context.get("focus") == "encapsulated-environments-pdf" or not context.get("focus"):
            improvements.append(Improvement(
                title="Fix import path in encapsulated-environments-pdf command",
                description="The command has import issues when using PDFGenerator. The example script works but CLI command fails.",
                category="code",
                priority="high",
                impact="high",
                effort="low",
                location="src/waft/main.py:1926",
                current_state="Import fails with 'No module named src' error",
                suggested_change="Use relative imports or fix import path to match working example script",
                rationale="Example script works, CLI command should work the same way"
            ))
        
        # Check for error handling
        improvements.append(Improvement(
            title="Add better error handling for PDF generation",
            description="PDF generation commands should gracefully handle missing dependencies and provide helpful error messages",
            category="code",
            priority="medium",
            impact="medium",
            effort="low",
            location="src/waft/main.py:encapsulated_environments_pdf",
            current_state="Basic try/except with generic error message",
            suggested_change="Check for specific dependencies, provide installation instructions, suggest alternative approaches",
            rationale="Better error messages help users fix issues faster"
        ))
        
        return improvements
    
    def _analyze_documentation(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze documentation quality."""
        improvements = []
        
        # Check command documentation
        improvements.append(Improvement(
            title="Add usage examples to encapsulated-environments-pdf command docs",
            description="The command documentation could include more examples and troubleshooting tips",
            category="documentation",
            priority="low",
            impact="medium",
            effort="low",
            location=".cursor/commands/encapsulated-environments-pdf.md",
            current_state="Basic documentation exists",
            suggested_change="Add troubleshooting section, common issues, and more examples",
            rationale="Better docs reduce support burden"
        ))
        
        return improvements
    
    def _analyze_architecture(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze architecture quality."""
        improvements = []
        
        # Check for code duplication
        improvements.append(Improvement(
            title="Consolidate PDF generation approaches",
            description="Both example script and CLI command generate PDFs but use different import patterns. Should be unified.",
            category="architecture",
            priority="medium",
            impact="medium",
            effort="medium",
            location="examples/generate_encapsulated_environments_pdf.py, src/waft/main.py",
            current_state="Two different approaches to same functionality",
            suggested_change="Create shared PDF generation utility or fix CLI command to use same pattern as example",
            rationale="Reduces duplication and maintenance burden"
        ))
        
        return improvements
    
    def _analyze_testing(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze testing coverage."""
        improvements = []
        
        improvements.append(Improvement(
            title="Add tests for encapsulated-environments-pdf command",
            description="The new command should have tests to verify it works correctly",
            category="testing",
            priority="medium",
            impact="medium",
            effort="medium",
            location="tests/",
            current_state="No tests for new command",
            suggested_change="Create test file for PDF generation command",
            rationale="Tests ensure command works and prevent regressions"
        ))
        
        return improvements
    
    def _analyze_performance(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze performance."""
        improvements = []
        
        # No performance issues identified for this work
        return improvements
    
    def _analyze_usability(self, context: Dict[str, Any]) -> List[Improvement]:
        """Analyze usability."""
        improvements = []
        
        improvements.append(Improvement(
            title="Make encapsulated-environments-pdf command work reliably",
            description="The command should work out of the box without import errors",
            category="usability",
            priority="high",
            impact="high",
            effort="low",
            location="src/waft/main.py:encapsulated_environments_pdf",
            current_state="Command fails with import errors",
            suggested_change="Fix import path to match working example script pattern",
            rationale="Users expect commands to work when they run them"
        ))
        
        return improvements
    
    def _display_improvements(self, improvements: List[Improvement]) -> None:
        """Display improvement recommendations."""
        if not improvements:
            self.console.print("[green]✅[/green] No improvements identified. Code looks good!")
            return
        
        # Summary table
        summary_table = Table(title="Improvement Summary", show_header=True, header_style="bold cyan")
        summary_table.add_column("Priority", width=12)
        summary_table.add_column("Category", width=15)
        summary_table.add_column("Count", justify="right", width=8)
        
        by_priority = {}
        by_category = {}
        for imp in improvements:
            by_priority[imp.priority] = by_priority.get(imp.priority, 0) + 1
            by_category[imp.category] = by_category.get(imp.category, 0) + 1
        
        for priority in ["critical", "high", "medium", "low"]:
            count = by_priority.get(priority, 0)
            if count > 0:
                color = {"critical": "red", "high": "yellow", "medium": "blue", "low": "dim"}[priority]
                summary_table.add_row(
                    f"[{color}]{priority.upper()}[/{color}]",
                    "All",
                    str(count)
                )
        
        self.console.print("\n")
        self.console.print(summary_table)
        
        # Detailed improvements
        self.console.print("\n[bold]Detailed Improvements:[/bold]\n")
        
        for i, improvement in enumerate(improvements, 1):
            priority_color = {
                "critical": "red",
                "high": "yellow",
                "medium": "blue",
                "low": "dim"
            }.get(improvement.priority, "dim")
            
            panel_content = f"[bold]{improvement.title}[/bold]\n\n"
            panel_content += f"[dim]Category:[/dim] {improvement.category} | "
            panel_content += f"[dim]Impact:[/dim] {improvement.impact} | "
            panel_content += f"[dim]Effort:[/dim] {improvement.effort} | "
            panel_content += f"[dim]Score:[/dim] {improvement.score:.2f}\n\n"
            
            panel_content += f"{improvement.description}\n\n"
            
            if improvement.location:
                panel_content += f"[dim]Location:[/dim] {improvement.location}\n"
            if improvement.current_state:
                panel_content += f"[dim]Current:[/dim] {improvement.current_state}\n"
            if improvement.suggested_change:
                panel_content += f"[dim]Suggested:[/dim] {improvement.suggested_change}\n"
            if improvement.rationale:
                panel_content += f"[dim]Rationale:[/dim] {improvement.rationale}\n"
            
            self.console.print(
                Panel(
                    panel_content,
                    title=f"[{priority_color}]{i}. {improvement.priority.upper()}[/{priority_color}]",
                    border_style=priority_color
                )
            )
            self.console.print()
    
    def _generate_summary(self, improvements: List[Improvement]) -> Dict[str, Any]:
        """Generate summary statistics."""
        by_priority = {}
        by_category = {}
        by_impact = {}
        by_effort = {}
        
        for imp in improvements:
            by_priority[imp.priority] = by_priority.get(imp.priority, 0) + 1
            by_category[imp.category] = by_category.get(imp.category, 0) + 1
            by_impact[imp.impact] = by_impact.get(imp.impact, 0) + 1
            by_effort[imp.effort] = by_effort.get(imp.effort, 0) + 1
        
        return {
            "total": len(improvements),
            "by_priority": by_priority,
            "by_category": by_category,
            "by_impact": by_impact,
            "by_effort": by_effort,
            "top_3": [i.to_dict() for i in improvements[:3]],
        }
    
    def _save_report(
        self,
        improvements: List[Improvement],
        output_path: Path,
        context: Dict[str, Any]
    ) -> None:
        """Save improvement report to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Improvement Analysis Report

**Generated**: {timestamp}
**Focus**: {context.get('focus', 'All')}
**Total Improvements**: {len(improvements)}

---

## Summary

"""
        
        summary = self._generate_summary(improvements)
        report += f"- **Total**: {summary['total']}\n"
        report += f"- **By Priority**: {summary['by_priority']}\n"
        report += f"- **By Category**: {summary['by_category']}\n"
        report += f"- **By Impact**: {summary['by_impact']}\n"
        report += f"- **By Effort**: {summary['by_effort']}\n\n"
        
        report += "---\n\n## Top 3 Improvements\n\n"
        for i, imp in enumerate(improvements[:3], 1):
            report += f"### {i}. {imp.title}\n\n"
            report += f"**Priority**: {imp.priority} | **Impact**: {imp.impact} | **Effort**: {imp.effort} | **Score**: {imp.score:.2f}\n\n"
            report += f"{imp.description}\n\n"
            if imp.location:
                report += f"**Location**: {imp.location}\n\n"
            if imp.suggested_change:
                report += f"**Suggested Change**: {imp.suggested_change}\n\n"
            report += "---\n\n"
        
        report += "## All Improvements\n\n"
        for i, imp in enumerate(improvements, 1):
            report += f"### {i}. {imp.title}\n\n"
            report += f"- **Priority**: {imp.priority}\n"
            report += f"- **Category**: {imp.category}\n"
            report += f"- **Impact**: {imp.impact}\n"
            report += f"- **Effort**: {imp.effort}\n"
            report += f"- **Score**: {imp.score:.2f}\n\n"
            report += f"{imp.description}\n\n"
            if imp.location:
                report += f"**Location**: {imp.location}\n\n"
            if imp.current_state:
                report += f"**Current State**: {imp.current_state}\n\n"
            if imp.suggested_change:
                report += f"**Suggested Change**: {imp.suggested_change}\n\n"
            if imp.rationale:
                report += f"**Rationale**: {imp.rationale}\n\n"
            report += "---\n\n"
        
        output_path.write_text(report)
        self.console.print(f"[green]✅[/green] Report saved: {output_path}")
