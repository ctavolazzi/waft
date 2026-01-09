"""
Continue Work - Reflect on current work and continue with improved awareness.

Pauses to deeply reflect on current work, approach, and progress, then continues
with improved awareness and potentially adjusted direction.

Note: Module named 'continue_work' because 'continue' is a Python keyword.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .session_stats import SessionStats
from .github import GitHubManager
from .gamification import GamificationManager
from .substrate import SubstrateManager
from .memory import MemoryManager


class ContinueManager:
    """Manages continue workflow - reflecting on current work and continuing."""
    
    def __init__(self, project_path: Path):
        """
        Initialize continue manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.gamification = GamificationManager(project_path)
        self.substrate = SubstrateManager(project_path)
        self.memory = MemoryManager(project_path)
    
    def run_continue(
        self,
        deep: bool = False,
        focus: Optional[str] = None,
        save: bool = False
    ) -> Dict[str, Any]:
        """
        Run continue workflow - reflect and continue with awareness.
        
        Args:
            deep: Whether to perform deep reflection
            focus: Focus area ("approach", "patterns", "quality", None for all)
            save: Whether to save reflection to file
            
        Returns:
            Dictionary with reflection results
        """
        self.console.print("\n[bold cyan]🌊 Continue: Reflecting on Current Work[/bold cyan]\n")
        
        # Capture current state
        current_state = self._capture_current_state()
        
        # Deep reflection
        reflection = self._reflect_on_work(current_state, deep, focus)
        
        # Meta-cognitive analysis
        meta_analysis = self._meta_cognitive_analysis(reflection, deep)
        
        # Generate insights
        insights = self._generate_insights(reflection, meta_analysis)
        
        # Adjusted continuation
        continuation = self._adjusted_continuation(reflection, insights)
        
        # Display reflection report
        self._display_reflection_report(
            current_state, reflection, meta_analysis, insights, continuation
        )
        
        # Save if requested
        if save:
            self._save_reflection(current_state, reflection, insights, continuation)
        
        return {
            "success": True,
            "current_state": current_state,
            "reflection": reflection,
            "meta_analysis": meta_analysis,
            "insights": insights,
            "continuation": continuation,
        }
    
    def _capture_current_state(self) -> Dict[str, Any]:
        """
        Capture current work state.
        
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
                    git_info["uncommitted_files"] = uncommitted[:20]  # Limit to 20
                    git_info["uncommitted_count"] = len(uncommitted)
            except Exception:
                pass
        
        # Recent session stats
        try:
            current_stats = self.stats_tracker.calculate_session_stats()
        except Exception:
            current_stats = {}
        
        # Project health
        try:
            integrity = self.gamification.get_integrity()
        except Exception:
            integrity = 100.0
        
        # Active files (from _pyrite/active/)
        active_files = []
        active_dir = self.project_path / "_pyrite" / "active"
        if active_dir.exists():
            active_files = [f.name for f in active_dir.glob("*.md")][:10]
        
        return {
            "git": git_info,
            "stats": current_stats,
            "integrity": integrity,
            "active_files": active_files,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _reflect_on_work(
        self,
        current_state: Dict[str, Any],
        deep: bool,
        focus: Optional[str]
    ) -> Dict[str, Any]:
        """
        Reflect on current work.
        
        Args:
            current_state: Current state information
            deep: Whether to perform deep reflection
            focus: Focus area or None for all
            
        Returns:
            Dictionary with reflection analysis
        """
        reflection = {
            "what": {},
            "why": {},
            "how": {},
            "effectiveness": {},
            "patterns": [],
            "insights": [],
        }
        
        # What am I doing?
        uncommitted = current_state["git"].get("uncommitted_files", [])
        stats = current_state.get("stats", {})
        
        # Identify what's being worked on from uncommitted files
        work_items = []
        if uncommitted:
            # Group by type/area
            code_files = [f for f in uncommitted if f.endswith(('.py', '.js', '.ts'))]
            doc_files = [f for f in uncommitted if f.endswith(('.md', '.txt'))]
            config_files = [f for f in uncommitted if any(f.endswith(ext) for ext in ('.toml', '.json', '.yaml', '.yml'))]
            
            if code_files:
                work_items.append({
                    "type": "Code",
                    "files": code_files[:5],
                    "count": len(code_files)
                })
            if doc_files:
                work_items.append({
                    "type": "Documentation",
                    "files": doc_files[:5],
                    "count": len(doc_files)
                })
            if config_files:
                work_items.append({
                    "type": "Configuration",
                    "files": config_files[:5],
                    "count": len(config_files)
                })
        
        reflection["what"] = {
            "files": uncommitted[:10],
            "work_items": work_items,
            "stats": {
                "files_created": stats.get("files", {}).get("created", 0),
                "files_modified": stats.get("files", {}).get("modified", 0),
                "lines_written": stats.get("code", {}).get("lines_written", 0),
            }
        }
        
        # Why am I doing it? (infer from context)
        # This would ideally come from conversation context or work efforts
        reflection["why"] = {
            "inferred_purpose": "Continuing development work",
            "context": "Active development session",
        }
        
        # How am I doing it? (analyze approach)
        approach_indicators = []
        if len(doc_files) > len(code_files):
            approach_indicators.append("Documentation-first approach")
        if code_files and doc_files:
            approach_indicators.append("Code and documentation together")
        if stats.get("files", {}).get("created", 0) > stats.get("files", {}).get("modified", 0):
            approach_indicators.append("Creating new files")
        else:
            approach_indicators.append("Modifying existing files")
        
        reflection["how"] = {
            "methodology": " ".join(approach_indicators) if approach_indicators else "Standard development",
            "efficiency": "Good" if current_state["git"]["uncommitted_count"] < 50 else "Many changes",
            "quality": "High" if current_state["integrity"] >= 90 else "Needs attention",
        }
        
        # Is it working? (effectiveness)
        reflection["effectiveness"] = {
            "progress": "Good" if stats.get("code", {}).get("lines_written", 0) > 0 else "Starting",
            "direction": "On track",
            "quality": "High" if current_state["integrity"] >= 90 else "Moderate",
        }
        
        # Patterns (if deep reflection)
        if deep or focus in (None, "patterns"):
            patterns = self._identify_patterns(current_state, stats)
            reflection["patterns"] = patterns
        
        return reflection
    
    def _identify_patterns(
        self,
        current_state: Dict[str, Any],
        stats: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Identify patterns in current work.
        
        Args:
            current_state: Current state
            stats: Session statistics
            
        Returns:
            List of pattern dictionaries
        """
        patterns = []
        
        # Pattern: Documentation alongside code
        uncommitted = current_state["git"].get("uncommitted_files", [])
        doc_files = [f for f in uncommitted if f.endswith('.md')]
        code_files = [f for f in uncommitted if f.endswith('.py')]
        
        if doc_files and code_files:
            patterns.append({
                "pattern": "Documentation alongside code",
                "observation": f"{len(doc_files)} doc files, {len(code_files)} code files",
                "insight": "Good practice - keeps code and docs in sync"
            })
        
        # Pattern: Creating new files vs modifying
        files_created = stats.get("files", {}).get("created", 0)
        files_modified = stats.get("files", {}).get("modified", 0)
        
        if files_created > files_modified * 2:
            patterns.append({
                "pattern": "Creating new files",
                "observation": f"{files_created} created vs {files_modified} modified",
                "insight": "Expanding codebase with new functionality"
            })
        elif files_modified > files_created * 2:
            patterns.append({
                "pattern": "Modifying existing files",
                "observation": f"{files_modified} modified vs {files_created} created",
                "insight": "Iterating on existing code"
            })
        
        # Pattern: High integrity
        if current_state["integrity"] >= 90:
            patterns.append({
                "pattern": "Maintaining high integrity",
                "observation": f"Integrity: {current_state['integrity']:.0f}%",
                "insight": "Good practices being maintained"
            })
        
        return patterns
    
    def _meta_cognitive_analysis(
        self,
        reflection: Dict[str, Any],
        deep: bool
    ) -> Dict[str, Any]:
        """
        Perform meta-cognitive analysis (thinking about thinking).
        
        Args:
            reflection: Reflection results
            deep: Whether to perform deep analysis
            
        Returns:
            Dictionary with meta-analysis
        """
        meta = {
            "thinking_about_thinking": [],
            "evaluation_of_evaluation": {},
            "understanding_of_understanding": {},
        }
        
        # Think about the thinking
        if reflection.get("how", {}).get("methodology"):
            meta["thinking_about_thinking"].append(
                f"Current methodology: {reflection['how']['methodology']}. "
                f"This approach is {'effective' if reflection['effectiveness']['progress'] == 'Good' else 'needs evaluation'}."
            )
        
        # Evaluate the evaluation
        meta["evaluation_of_evaluation"] = {
            "reflection_quality": "Good" if reflection.get("patterns") else "Basic",
            "awareness_level": "High" if deep else "Moderate",
            "insight_depth": "Deep" if deep else "Surface",
        }
        
        # Understand the understanding
        meta["understanding_of_understanding"] = {
            "clarity": "Clear" if reflection.get("what") else "Unclear",
            "purpose_understanding": "Understood" if reflection.get("why") else "Needs clarification",
            "approach_understanding": "Understood" if reflection.get("how") else "Needs analysis",
        }
        
        return meta
    
    def _generate_insights(
        self,
        reflection: Dict[str, Any],
        meta_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate insights from reflection.
        
        Args:
            reflection: Reflection results
            meta_analysis: Meta-cognitive analysis
            
        Returns:
            List of insight dictionaries
        """
        insights = []
        
        # Insight from patterns
        patterns = reflection.get("patterns", [])
        if patterns:
            for pattern in patterns[:3]:
                insights.append({
                    "insight": pattern.get("insight", ""),
                    "meaning": f"Pattern '{pattern.get('pattern', '')}' indicates {pattern.get('observation', '')}",
                    "action": "Continue this pattern if effective"
                })
        
        # Insight from effectiveness
        effectiveness = reflection.get("effectiveness", {})
        if effectiveness.get("progress") == "Good":
            insights.append({
                "insight": "Current approach is working well",
                "meaning": "Progress is good, quality is maintained",
                "action": "Continue with current approach"
            })
        
        # Insight from methodology
        methodology = reflection.get("how", {}).get("methodology", "")
        if "Documentation" in methodology:
            insights.append({
                "insight": "Documentation-first approach is effective",
                "meaning": "Keeping code and docs in sync improves maintainability",
                "action": "Continue documenting thoroughly"
            })
        
        return insights
    
    def _adjusted_continuation(
        self,
        reflection: Dict[str, Any],
        insights: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate adjusted continuation plan.
        
        Args:
            reflection: Reflection results
            insights: Generated insights
            
        Returns:
            Dictionary with continuation plan
        """
        continuation = {
            "insights_to_apply": [],
            "course_adjustments": [],
            "continue_with": [],
            "next_steps": [],
        }
        
        # Insights to apply
        for insight in insights[:3]:
            continuation["insights_to_apply"].append({
                "insight": insight.get("insight", ""),
                "how_to_apply": insight.get("action", "")
            })
        
        # Course adjustments
        effectiveness = reflection.get("effectiveness", {})
        if effectiveness.get("quality") != "High":
            continuation["course_adjustments"].append({
                "adjustment": "Focus on quality",
                "why": "Quality needs attention",
                "how": "Review code, add tests, improve documentation"
            })
        
        # Continue with
        continuation["continue_with"].append("Current systematic approach")
        continuation["continue_with"].append("Comprehensive documentation")
        
        # Next steps
        uncommitted = reflection.get("what", {}).get("files", [])
        if uncommitted:
            continuation["next_steps"].append({
                "action": f"Continue working on {len(uncommitted)} uncommitted file(s)",
                "why": "Work in progress needs completion",
                "reflection": "Current work is on track, continue systematically"
            })
        
        return continuation
    
    def _display_reflection_report(
        self,
        current_state: Dict[str, Any],
        reflection: Dict[str, Any],
        meta_analysis: Dict[str, Any],
        insights: List[Dict[str, str]],
        continuation: Dict[str, Any]
    ):
        """Display comprehensive reflection report."""
        self.console.print("=" * 90)
        
        # Current Work State
        self.console.print("\n[bold]📋 Current Work State[/bold]\n")
        
        what = reflection.get("what", {})
        work_items = what.get("work_items", [])
        
        self.console.print("[bold]What's Being Worked On:[/bold]")
        if work_items:
            for item in work_items:
                self.console.print(f"  • {item['type']}: {item['count']} file(s)")
                for file in item.get("files", [])[:3]:
                    self.console.print(f"    - {file}")
        else:
            uncommitted = current_state["git"].get("uncommitted_files", [])
            if uncommitted:
                self.console.print(f"  • {len(uncommitted)} uncommitted file(s)")
                for file in uncommitted[:5]:
                    self.console.print(f"    - {file}")
        
        stats = what.get("stats", {})
        if stats:
            self.console.print("\n[bold]Progress Made:[/bold]")
            if stats.get("files_created", 0) > 0:
                self.console.print(f"  • Files Created: {stats['files_created']}")
            if stats.get("files_modified", 0) > 0:
                self.console.print(f"  • Files Modified: {stats['files_modified']}")
            if stats.get("lines_written", 0) > 0:
                self.console.print(f"  • Lines Written: {stats['lines_written']:,}")
        
        self.console.print("\n" + "=" * 90)
        
        # Reflection Analysis
        self.console.print("\n[bold]🔍 Reflection Analysis[/bold]\n")
        
        how = reflection.get("how", {})
        self.console.print("[bold]Current Approach:[/bold]")
        self.console.print(f"  • Methodology: {how.get('methodology', 'Standard development')}")
        self.console.print(f"  • Efficiency: {how.get('efficiency', 'Unknown')}")
        self.console.print(f"  • Quality: {how.get('quality', 'Unknown')}")
        self.console.print(f"  • Direction: {reflection.get('effectiveness', {}).get('direction', 'Unknown')}")
        
        patterns = reflection.get("patterns", [])
        if patterns:
            self.console.print("\n[bold]Patterns Identified:[/bold]")
            for pattern in patterns:
                self.console.print(f"  • {pattern.get('pattern', '')}: {pattern.get('observation', '')}")
                self.console.print(f"    [dim]→ {pattern.get('insight', '')}[/dim]")
        
        if insights:
            self.console.print("\n[bold]Insights:[/bold]")
            for i, insight in enumerate(insights[:3], 1):
                self.console.print(f"  {i}. {insight.get('insight', '')}")
                self.console.print(f"     [dim]→ {insight.get('meaning', '')}[/dim]")
                self.console.print(f"     [dim]→ Action: {insight.get('action', '')}[/dim]")
        
        self.console.print("\n" + "=" * 90)
        
        # Reflection Questions
        self.console.print("\n[bold]❓ Reflection Questions[/bold]\n")
        
        self.console.print("[bold]What am I doing?[/bold]")
        work_summary = []
        if work_items:
            for item in work_items:
                work_summary.append(f"{item['type'].lower()} work ({item['count']} files)")
        if work_summary:
            self.console.print(f"  {' '.join(work_summary)}")
        else:
            self.console.print("  Continuing development work")
        
        self.console.print("\n[bold]Why am I doing it?[/bold]")
        why = reflection.get("why", {})
        self.console.print(f"  {why.get('inferred_purpose', 'Continuing project development')}")
        
        self.console.print("\n[bold]How am I doing it?[/bold]")
        self.console.print(f"  {how.get('methodology', 'Standard development approach')}")
        
        self.console.print("\n[bold]Is it working?[/bold]")
        effectiveness = reflection.get("effectiveness", {})
        self.console.print(f"  Progress: {effectiveness.get('progress', 'Unknown')}")
        self.console.print(f"  Quality: {effectiveness.get('quality', 'Unknown')}")
        self.console.print(f"  Direction: {effectiveness.get('direction', 'Unknown')}")
        
        self.console.print("\n[bold]Should I adjust?[/bold]")
        adjustments = continuation.get("course_adjustments", [])
        if adjustments:
            for adj in adjustments:
                self.console.print(f"  • {adj.get('adjustment', '')}: {adj.get('why', '')}")
                self.console.print(f"    [dim]→ {adj.get('how', '')}[/dim]")
        else:
            self.console.print("  ✅ Current approach is working well")
            self.console.print("  💡 Continue with current methodology")
        
        self.console.print("\n" + "=" * 90)
        
        # Adjusted Continuation
        self.console.print("\n[bold]🎯 Adjusted Continuation[/bold]\n")
        
        insights_to_apply = continuation.get("insights_to_apply", [])
        if insights_to_apply:
            self.console.print("[bold]Insights to Apply:[/bold]")
            for insight in insights_to_apply:
                self.console.print(f"  • {insight.get('insight', '')}")
                self.console.print(f"    [dim]→ {insight.get('how_to_apply', '')}[/dim]")
        
        continue_with = continuation.get("continue_with", [])
        if continue_with:
            self.console.print("\n[bold]Continue With:[/bold]")
            for item in continue_with:
                self.console.print(f"  • ✅ {item}")
        
        next_steps = continuation.get("next_steps", [])
        if next_steps:
            self.console.print("\n[bold]Next Steps (with awareness):[/bold]")
            for i, step in enumerate(next_steps[:5], 1):
                self.console.print(f"  {i}. {step.get('action', '')}")
                if step.get("why"):
                    self.console.print(f"     [dim]→ Why: {step['why']}[/dim]")
                if step.get("reflection"):
                    self.console.print(f"     [dim]→ Reflection: {step['reflection']}[/dim]")
        
        self.console.print("\n" + "=" * 90)
        self.console.print("\n[bold green]✅ Reflection Complete - Continue with improved awareness[/bold green]\n")
    
    def _save_reflection(
        self,
        current_state: Dict[str, Any],
        reflection: Dict[str, Any],
        insights: List[Dict[str, str]],
        continuation: Dict[str, Any]
    ) -> Path:
        """
        Save reflection to file.
        
        Args:
            current_state: Current state
            reflection: Reflection results
            insights: Generated insights
            continuation: Continuation plan
            
        Returns:
            Path to saved reflection file
        """
        continue_dir = self.project_path / "_pyrite" / "continue"
        continue_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        reflection_file = continue_dir / f"continue-{timestamp}.md"
        
        content = []
        content.append(f"# Continue Reflection: {timestamp}\n\n")
        content.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        content.append("---\n\n")
        
        content.append("## Current Work State\n\n")
        what = reflection.get("what", {})
        content.append(f"- Files: {len(what.get('files', []))}\n")
        content.append(f"- Files Created: {what.get('stats', {}).get('files_created', 0)}\n")
        content.append(f"- Lines Written: {what.get('stats', {}).get('lines_written', 0):,}\n\n")
        
        content.append("## Reflection\n\n")
        content.append(f"### What: {reflection.get('what', {}).get('work_items', [{}])[0].get('type', 'Development') if reflection.get('what', {}).get('work_items') else 'Development'}\n\n")
        content.append(f"### Why: {reflection.get('why', {}).get('inferred_purpose', 'Continuing work')}\n\n")
        content.append(f"### How: {reflection.get('how', {}).get('methodology', 'Standard approach')}\n\n")
        
        if insights:
            content.append("## Insights\n\n")
            for i, insight in enumerate(insights, 1):
                content.append(f"{i}. {insight.get('insight', '')}\n")
                content.append(f"   - {insight.get('meaning', '')}\n")
                content.append(f"   - Action: {insight.get('action', '')}\n\n")
        
        if continuation.get("next_steps"):
            content.append("## Next Steps\n\n")
            for i, step in enumerate(continuation["next_steps"], 1):
                content.append(f"{i}. {step.get('action', '')}\n")
                if step.get("why"):
                    content.append(f"   - Why: {step['why']}\n")
                if step.get("reflection"):
                    content.append(f"   - Reflection: {step['reflection']}\n\n")
        
        reflection_file.write_text("".join(content), encoding="utf-8")
        
        return reflection_file
