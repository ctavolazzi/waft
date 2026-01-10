"""
Goal - Track larger goals, break into steps, identify next actions.

Manages larger objectives and goals, breaks them into actionable steps,
tracks progress, and identifies what to do next.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from ..logging import get_logger
from .memory import MemoryManager

logger = get_logger(__name__)


class GoalManager:
    """Manages goals and next step identification."""
    
    def __init__(self, project_path: Path):
        """
        Initialize goal manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.memory = MemoryManager(project_path)
        self.goals_dir = project_path / "_pyrite" / "goals"
        self.goals_dir.mkdir(parents=True, exist_ok=True)
        self.goals_index = self.goals_dir / "index.json"
    
    def create_goal(
        self,
        name: str,
        objective: str,
        steps: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new goal.
        
        Args:
            name: Goal name (slug)
            objective: Goal objective/description
            steps: Optional list of step descriptions
            
        Returns:
            Dictionary with goal information
        """
        goal_file = self.goals_dir / f"{name}.md"
        
        if goal_file.exists():
            self.console.print(f"[bold red]❌ Goal already exists: {name}[/bold red]")
            return {"success": False, "error": "Goal already exists"}
        
        # Create goal markdown
        content = []
        content.append(f"# Goal: {name}\n\n")
        content.append(f"**Status**: Active\n")
        content.append(f"**Created**: {datetime.now().strftime('%Y-%m-%d')}\n")
        content.append(f"**Updated**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        content.append("---\n\n")
        content.append("## Objective\n\n")
        content.append(f"{objective}\n\n")
        content.append("---\n\n")
        content.append("## Steps\n\n")
        
        if steps:
            for i, step in enumerate(steps, 1):
                content.append(f"{i}. [ ] {step}\n")
        else:
            content.append("1. [ ] Define first step\n\n")
        
        content.append("\n---\n\n")
        content.append("## Progress\n\n")
        content.append("- Completed: 0 steps\n")
        content.append("- Current: Not started\n")
        content.append("- Next: Define first step\n\n")
        content.append("---\n\n")
        content.append("## Notes\n\n")
        content.append("_Add notes here_\n")
        
        goal_file.write_text("".join(content), encoding="utf-8")
        
        # Update index
        self._update_index(name, "active")
        
        self.console.print(f"[bold green]✅ Goal created: {name}[/bold green]")
        self.console.print(f"[dim]Location: {goal_file.relative_to(self.project_path)}[/dim]\n")
        
        return {
            "success": True,
            "name": name,
            "file": str(goal_file.relative_to(self.project_path)),
        }
    
    def list_goals(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all goals.
        
        Args:
            status: Filter by status (active, completed, paused)
            
        Returns:
            List of goal dictionaries
        """
        goals = []
        
        for goal_file in self.goals_dir.glob("*.md"):
            if goal_file.name == "index.json":
                continue
            
            goal_data = self._read_goal(goal_file)
            if goal_data:
                if status is None or goal_data.get("status", "").lower() == status.lower():
                    goals.append(goal_data)
        
        return sorted(goals, key=lambda x: x.get("updated", ""), reverse=True)
    
    def show_goal(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Show goal details.
        
        Args:
            name: Goal name
            
        Returns:
            Goal dictionary or None
        """
        goal_file = self.goals_dir / f"{name}.md"
        
        if not goal_file.exists():
            self.console.print(f"[bold red]❌ Goal not found: {name}[/bold red]")
            return None
        
        goal_data = self._read_goal(goal_file)
        
        if goal_data:
            self._display_goal(goal_data)
        
        return goal_data
    
    def get_next_step(
        self,
        goal_name: Optional[str] = None,
        count: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Identify next step(s) based on goals.
        
        Args:
            goal_name: Optional specific goal name
            count: Number of next steps to return
            
        Returns:
            List of next step dictionaries
        """
        if goal_name:
            goal_data = self.show_goal(goal_name)
            if not goal_data:
                return []
            
            next_steps = self._extract_next_steps([goal_data])
        else:
            goals = self.list_goals(status="active")
            next_steps = self._extract_next_steps(goals)
        
        # Sort by priority and return top N
        next_steps.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return next_steps[:count]
    
    def _read_goal(self, goal_file: Path) -> Optional[Dict[str, Any]]:
        """Read goal from markdown file."""
        try:
            content = goal_file.read_text(encoding="utf-8")
            
            # Extract metadata
            status_match = re.search(r'\*\*Status\*\*: (\w+)', content)
            created_match = re.search(r'\*\*Created\*\*: (\d{4}-\d{2}-\d{2})', content)
            updated_match = re.search(r'\*\*Updated\*\*: (\d{4}-\d{2}-\d{2})', content)
            
            # Extract objective
            objective_match = re.search(r'## Objective\n\n(.*?)\n\n---', content, re.DOTALL)
            
            # Extract steps
            steps = []
            step_pattern = r'(\d+)\. \[([ x])\] (.+?)(?=\n\d+\.|$)'
            for match in re.finditer(step_pattern, content, re.MULTILINE | re.DOTALL):
                step_num = int(match.group(1))
                checked = match.group(2) == "x"
                step_desc = match.group(3).strip()
                # Remove trailing checkmarks and whitespace
                step_desc = re.sub(r'\s*✅\s*$', '', step_desc).strip()
                steps.append({
                    "number": step_num,
                    "completed": checked,
                    "description": step_desc,
                })
            
            # Extract progress
            progress_match = re.search(r'## Progress\n\n(.*?)\n\n---', content, re.DOTALL)
            
            return {
                "name": goal_file.stem,
                "file": str(goal_file.relative_to(self.project_path)),
                "status": status_match.group(1) if status_match else "unknown",
                "created": created_match.group(1) if created_match else "",
                "updated": updated_match.group(1) if updated_match else "",
                "objective": objective_match.group(1).strip() if objective_match else "",
                "steps": steps,
                "progress": progress_match.group(1).strip() if progress_match else "",
            }
        except Exception as e:
            return None
    
    def _extract_next_steps(self, goals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract next steps from goals."""
        next_steps = []
        
        for goal in goals:
            steps = goal.get("steps", [])
            for step in steps:
                if not step.get("completed", False):
                    next_steps.append({
                        "goal": goal.get("name", ""),
                        "step": step.get("description", ""),
                        "step_number": step.get("number", 0),
                        "priority": self._calculate_priority(goal, step),
                        "objective": goal.get("objective", ""),
                    })
                    break  # Only first incomplete step per goal
        
        return next_steps
    
    def _calculate_priority(self, goal: Dict[str, Any], step: Dict[str, Any]) -> int:
        """Calculate priority for next step (higher = more important)."""
        priority = 50  # Base priority
        
        # Higher priority for earlier steps (but not too much - want to see all goals)
        step_num = step.get("number", 999)
        priority += max(0, (20 - step_num) * 2)  # Diminishing returns
        
        # Higher priority for active goals
        if goal.get("status", "").lower() == "active":
            priority += 30
        
        # Higher priority for goals with more progress (closer to completion)
        steps = goal.get("steps", [])
        if steps:
            completed = sum(1 for s in steps if s.get("completed", False))
            total = len(steps)
            if total > 0:
                progress_ratio = completed / total
                # Higher priority for goals that are partially complete (momentum)
                if 0.3 < progress_ratio < 0.9:
                    priority += 25
        
        return priority
    
    def _display_goal(self, goal: Dict[str, Any]):
        """Display goal details."""
        self.console.print(f"\n[bold cyan]🎯 Goal: {goal['name']}[/bold cyan]\n")
        self.console.print(f"[bold]Status:[/bold] {goal.get('status', 'unknown')}")
        self.console.print(f"[bold]Objective:[/bold] {goal.get('objective', '')}\n")
        
        steps = goal.get("steps", [])
        if steps:
            table = Table(show_header=True, box=None)
            table.add_column("", width=3)
            table.add_column("Step", width=70)
            table.add_column("Status", width=10)
            
            for step in steps:
                status = "✅" if step.get("completed") else "⏸️"
                table.add_row(
                    str(step.get("number", "")),
                    step.get("description", ""),
                    status
                )
            
            self.console.print(table)
        
        progress = goal.get("progress", "")
        if progress:
            self.console.print(f"\n[bold]Progress:[/bold]")
            self.console.print(progress)
    
    def _update_index(self, name: str, status: str):
        """Update goals index."""
        if self.goals_index.exists():
            try:
                index = json.loads(self.goals_index.read_text())
            except (json.JSONDecodeError, OSError) as e:
                logger.debug(f"Could not read goals index, creating new: {e}")
                index = {}
        else:
            index = {}
        
        index[name] = {
            "status": status,
            "updated": datetime.now().isoformat(),
        }
        
        self.goals_index.write_text(json.dumps(index, indent=2), encoding="utf-8")
