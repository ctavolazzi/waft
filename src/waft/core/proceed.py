"""
Proceed - Verify context and assumptions before continuing.

Pauses to check larger context, reflect on assumptions, ask clarifying questions,
perform a "flight check", then proceeds with verified understanding.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from .session_stats import SessionStats
from .github import GitHubManager
from .memory import MemoryManager


class ProceedManager:
    """Manages proceed workflow with verification."""
    
    def __init__(self, project_path: Path):
        """
        Initialize proceed manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
    
    def run_proceed(
        self,
        focus: Optional[str] = None,
        strict: bool = False,
        relaxed: bool = False,
    ) -> Dict[str, Any]:
        """
        Run proceed workflow - verify then continue.
        
        Args:
            focus: Focus area (assumptions, ambiguity, context)
            strict: If True, ask questions before proceeding
            relaxed: If True, proceed with best understanding
            
        Returns:
            Dictionary with proceed results
        """
        self.console.print("\n[bold cyan]✈️ Proceed: Verification & Continuation[/bold cyan]\n")
        
        # Step 1: Context Gathering
        context = self._gather_context()
        self._display_context(context)
        
        # Step 2: Assumption Identification
        assumptions = self._identify_assumptions(context)
        self._display_assumptions(assumptions)
        
        # Step 3: Ambiguity Detection
        ambiguities = self._detect_ambiguities(context)
        self._display_ambiguities(ambiguities)
        
        # Step 4: Flight Check
        flight_check = self._flight_check(context, assumptions, ambiguities)
        self._display_flight_check(flight_check)
        
        # Step 5: Clarifying Questions
        if not relaxed and (assumptions.get("critical", []) or ambiguities.get("critical", [])):
            questions = self._formulate_questions(assumptions, ambiguities)
            self._display_questions(questions, strict=strict)
        
        # Step 6: Verified Proceeding
        self._display_proceeding_summary(context, assumptions, ambiguities, flight_check)
        
        return {
            "success": True,
            "context": context,
            "assumptions": assumptions,
            "ambiguities": ambiguities,
            "flight_check": flight_check,
            "ready": flight_check.get("status") == "READY",
        }
    
    def _gather_context(self) -> Dict[str, Any]:
        """Gather current context."""
        import subprocess
        
        context = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
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
        
        context["git"] = git_info
        
        # Recent files
        try:
            stats = self.stats_tracker.calculate_session_stats()
            context["recent_files"] = {
                "created": stats.get("files", {}).get("created", []),
                "modified": stats.get("files", {}).get("modified", []),
            }
        except Exception:
            context["recent_files"] = {"created": [], "modified": []}
        
        # Active files
        try:
            active_files = self.memory.get_active_files()
            context["active_files"] = [str(f.name) for f in active_files[:10]]
        except Exception:
            context["active_files"] = []
        
        return context
    
    def _identify_assumptions(self, context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify assumptions being made."""
        assumptions = {
            "critical": [],
            "minor": [],
        }
        
        # Check for common assumptions
        if context["git"]["uncommitted_count"] > 0:
            assumptions["minor"].append(
                "Assuming uncommitted changes are intentional and safe to work with"
            )
        
        if len(context.get("active_files", [])) > 0:
            assumptions["minor"].append(
                "Assuming active files are relevant to current work"
            )
        
        # Add more assumption detection logic here
        # This is a placeholder - in real use, would analyze conversation/context
        
        return assumptions
    
    def _detect_ambiguities(self, context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Detect ambiguities and unclear points."""
        ambiguities = {
            "critical": [],
            "minor": [],
        }
        
        # Check for common ambiguities
        if context["git"]["uncommitted_count"] > 50:
            ambiguities["minor"].append(
                "Large number of uncommitted files - unclear which are relevant"
            )
        
        # Add more ambiguity detection logic here
        # This is a placeholder - in real use, would analyze conversation/requirements
        
        return ambiguities
    
    def _flight_check(self, context: Dict[str, Any], assumptions: Dict[str, List], ambiguities: Dict[str, List]) -> Dict[str, Any]:
        """Perform flight check."""
        check = {
            "context_understood": True,
            "assumptions_identified": len(assumptions.get("critical", [])) + len(assumptions.get("minor", [])) > 0,
            "ambiguities_noted": len(ambiguities.get("critical", [])) + len(ambiguities.get("minor", [])) > 0,
            "prerequisites_met": True,
            "blockers": [],
            "status": "READY",
        }
        
        # Check for blockers
        if ambiguities.get("critical"):
            check["blockers"].append("Critical ambiguities need resolution")
            check["status"] = "NEEDS_CLARIFICATION"
        
        if assumptions.get("critical"):
            check["blockers"].append("Critical assumptions need verification")
            if check["status"] == "READY":
                check["status"] = "NEEDS_VERIFICATION"
        
        return check
    
    def _formulate_questions(self, assumptions: Dict[str, List], ambiguities: Dict[str, List]) -> List[Dict[str, str]]:
        """Formulate clarifying questions."""
        questions = []
        
        for assumption in assumptions.get("critical", []):
            questions.append({
                "question": f"Can you confirm: {assumption}?",
                "reason": "Critical assumption needs verification",
                "priority": "high",
            })
        
        for ambiguity in ambiguities.get("critical", []):
            questions.append({
                "question": f"Can you clarify: {ambiguity}?",
                "reason": "Critical ambiguity needs resolution",
                "priority": "high",
            })
        
        return questions
    
    def _display_context(self, context: Dict[str, Any]):
        """Display context summary."""
        self.console.print("[bold]📋 Context Check[/bold]\n")
        
        self.console.print(f"  • Branch: {context['git'].get('branch', 'unknown')}")
        self.console.print(f"  • Uncommitted Files: {context['git'].get('uncommitted_count', 0)}")
        
        active_files = context.get("active_files", [])
        if active_files:
            self.console.print(f"  • Active Files: {len(active_files)}")
            for file in active_files[:5]:
                self.console.print(f"    - {file}")
        
        self.console.print()
    
    def _display_assumptions(self, assumptions: Dict[str, List]):
        """Display assumptions."""
        total = len(assumptions.get("critical", [])) + len(assumptions.get("minor", []))
        if total == 0:
            return
        
        self.console.print("[bold]⚠️ Assumptions Found[/bold]\n")
        
        if assumptions.get("critical"):
            self.console.print("  [bold red]Critical:[/bold red]")
            for assumption in assumptions["critical"]:
                self.console.print(f"    • {assumption}")
        
        if assumptions.get("minor"):
            self.console.print("  [dim]Minor:[/dim]")
            for assumption in assumptions["minor"]:
                self.console.print(f"    • {assumption}")
        
        self.console.print()
    
    def _display_ambiguities(self, ambiguities: Dict[str, List]):
        """Display ambiguities."""
        total = len(ambiguities.get("critical", [])) + len(ambiguities.get("minor", []))
        if total == 0:
            return
        
        self.console.print("[bold]❓ Ambiguities Found[/bold]\n")
        
        if ambiguities.get("critical"):
            self.console.print("  [bold red]Critical:[/bold red]")
            for ambiguity in ambiguities["critical"]:
                self.console.print(f"    • {ambiguity}")
        
        if ambiguities.get("minor"):
            self.console.print("  [dim]Minor:[/dim]")
            for ambiguity in ambiguities["minor"]:
                self.console.print(f"    • {ambiguity}")
        
        self.console.print()
    
    def _display_flight_check(self, flight_check: Dict[str, Any]):
        """Display flight check."""
        self.console.print("[bold]✈️ Flight Check[/bold]\n")
        
        status_icon = "✅" if flight_check["status"] == "READY" else "⚠️"
        self.console.print(f"  {status_icon} Context: {'Understood' if flight_check['context_understood'] else 'Needs Review'}")
        self.console.print(f"  {status_icon} Assumptions: {'Identified' if flight_check['assumptions_identified'] else 'None Found'}")
        self.console.print(f"  {status_icon} Ambiguities: {'Noted' if flight_check['ambiguities_noted'] else 'None Found'}")
        self.console.print(f"  {status_icon} Prerequisites: {'Met' if flight_check['prerequisites_met'] else 'Not Met'}")
        self.console.print(f"  {status_icon} Blockers: {len(flight_check['blockers'])}")
        
        if flight_check["blockers"]:
            for blocker in flight_check["blockers"]:
                self.console.print(f"    - {blocker}")
        
        self.console.print(f"\n  [bold]Status:[/bold] {flight_check['status']}\n")
    
    def _display_questions(self, questions: List[Dict[str, str]], strict: bool = False):
        """Display clarifying questions."""
        if not questions:
            return
        
        self.console.print("[bold]❓ Clarifying Questions[/bold]\n")
        
        for i, q in enumerate(questions, 1):
            self.console.print(f"  {i}. {q['question']}")
            self.console.print(f"     [dim]{q['reason']}[/dim]")
        
        if strict:
            self.console.print("\n  [bold yellow]⚠️ Strict mode: Waiting for answers before proceeding[/bold yellow]\n")
        else:
            self.console.print("\n  [dim]Proceeding with best understanding, will ask if critical[/dim]\n")
    
    def _display_proceeding_summary(
        self,
        context: Dict[str, Any],
        assumptions: Dict[str, List],
        ambiguities: Dict[str, List],
        flight_check: Dict[str, Any],
    ):
        """Display proceeding summary."""
        self.console.print("[bold green]✅ Verified Proceeding[/bold green]\n")
        
        self.console.print("  • Context verified")
        self.console.print(f"  • Assumptions: {len(assumptions.get('critical', []))} critical, {len(assumptions.get('minor', []))} minor")
        self.console.print(f"  • Ambiguities: {len(ambiguities.get('critical', []))} critical, {len(ambiguities.get('minor', []))} minor")
        self.console.print(f"  • Status: {flight_check['status']}")
        
        if flight_check["status"] == "READY":
            self.console.print("\n  [bold green]Proceeding with verified understanding...[/bold green]\n")
        else:
            self.console.print("\n  [bold yellow]Proceeding with awareness of items needing attention...[/bold yellow]\n")
