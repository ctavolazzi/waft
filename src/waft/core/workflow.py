"""
Compose - Command sequence composition and command creation.

Parse natural language to extract and execute command sequences.
Turn commonly used sequences into reusable commands.
Gives control over command composition.
"""

import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .memory import MemoryManager


class ComposeManager:
    """Manages command composition and command creation from sequences."""
    
    def __init__(self, project_path: Path):
        """
        Initialize compose manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.memory = MemoryManager(project_path)
        self.commands_dir = project_path / ".cursor" / "commands"
        self.commands_dir.mkdir(parents=True, exist_ok=True)
    
    def run_compose(
        self,
        input_text: Optional[str] = None,
        create_command: Optional[str] = None,
        command_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Compose and execute command sequence, optionally create new command.
        
        Args:
            input_text: Natural language command sequence
            create_command: If provided, create new command with this name
            command_name: Name for command being created
            
        Returns:
            Dictionary with execution results
        """
        if not input_text:
            self.console.print("[bold red]❌ Must provide command sequence[/bold red]")
            return {"success": False, "error": "Missing input"}
        
        # Parse natural language
        sequence = self._parse_natural_language(input_text)
        if not sequence:
            return {"success": False, "error": "Failed to parse sequence"}
        
        # Execute sequence
        results = self._execute_sequence(sequence)
        
        # Create command if requested
        if create_command and results.get("success"):
            self._create_command_from_sequence(create_command, sequence, input_text)
        
        return results
    
    def _parse_natural_language(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse natural language to extract command sequence.
        
        Uses simple pattern matching to extract command names.
        AI can interpret more complex phrases naturally.
        
        Args:
            text: Natural language input
            
        Returns:
            Parsed workflow dictionary or None
        """
        # Known command names
        known_commands = [
            "proceed", "spin-up", "analyze", "phase1", "phase2",
            "recap", "continue", "reflect", "checkpoint", "verify",
            "checkout", "resume", "orient", "explore", "consider",
            "decide", "goal", "next", "help", "setup", "workflow",
            "prepare", "visualize", "stats", "analytics"
        ]
        
        steps = []
        
        # Simple extraction: look for /command patterns
        command_pattern = r'/(\w+(?:-\w+)*)'
        matches = re.findall(command_pattern, text.lower())
        
        for match in matches:
            # Normalize command name
            cmd_name = match.replace("-", "-")
            if cmd_name in known_commands:
                steps.append({
                    "command": cmd_name,
                    "params": {},
                })
        
        # Also look for natural language patterns
        # "proceed to X" means "proceed then X"
        # "X and Y" means "X then Y"
        # "X then Y" means "X then Y"
        
        # Extract phase numbers from "phase2", "phase 2", "move on to phase2"
        phase_match = re.search(r'phase\s*(\d+)', text.lower())
        if phase_match:
            # Find "prepare" command and add phase param
            for i, step in enumerate(steps):
                if step["command"] == "prepare":
                    steps[i]["params"]["phase"] = int(phase_match.group(1))
        
        if not steps:
            return None
        
        return {
            "name": "parsed-workflow",
            "description": f"Parsed from: {text[:50]}...",
            "steps": steps,
        }
    
    def _load_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Load named workflow from file."""
        workflow_file = self.workflows_dir / f"{name}.yaml"
        
        if not workflow_file.exists():
            return None
        
        try:
            content = workflow_file.read_text(encoding="utf-8")
            return yaml.safe_load(content)
        except Exception as e:
            self.console.print(f"[bold red]❌ Error loading workflow: {e}[/bold red]")
            return None
    
    def _save_workflow(self, workflow: Dict[str, Any], name: str):
        """Save workflow to file."""
        workflow_file = self.workflows_dir / f"{name}.yaml"
        
        try:
            workflow["name"] = name
            workflow["created"] = datetime.now().isoformat()
            content = yaml.dump(workflow, default_flow_style=False)
            workflow_file.write_text(content, encoding="utf-8")
            self.console.print(f"[dim]💾 Saved workflow: {name}[/dim]")
        except Exception as e:
            self.console.print(f"[bold red]❌ Error saving workflow: {e}[/bold red]")
    
    def _execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow steps."""
        self.console.print(f"\n[bold cyan]🔄 Workflow: {workflow.get('name', 'unnamed')}[/bold cyan]\n")
        
        steps = workflow.get("steps", [])
        if not steps:
            self.console.print("[bold red]❌ No steps in workflow[/bold red]")
            return {"success": False, "error": "No steps"}
        
        results = []
        
        for i, step in enumerate(steps, 1):
            cmd_name = step.get("command")
            params = step.get("params", {})
            
            self.console.print(f"[bold]Step {i}/{len(steps)}:[/bold] {cmd_name}")
            
            # Note: Actual command execution would call the command managers
            # For now, we'll just document what would be executed
            results.append({
                "step": i,
                "command": cmd_name,
                "params": params,
                "status": "pending",  # Would be "success" or "failed" in real execution
            })
            
            self.console.print(f"  [dim]Would execute: waft {cmd_name} with params {params}[/dim]\n")
        
        self.console.print(f"[bold green]✅ Workflow execution plan created[/bold green]")
        self.console.print(f"[dim]Note: Actual command execution not yet implemented[/dim]\n")
        
        return {
            "success": True,
            "workflow": workflow.get("name"),
            "steps": len(steps),
            "results": results,
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all saved workflows."""
        workflows = []
        
        for workflow_file in self.workflows_dir.glob("*.yaml"):
            try:
                content = workflow_file.read_text(encoding="utf-8")
                workflow = yaml.safe_load(content)
                workflows.append({
                    "name": workflow.get("name", workflow_file.stem),
                    "description": workflow.get("description", ""),
                    "steps": len(workflow.get("steps", [])),
                    "created": workflow.get("created", ""),
                })
            except Exception:
                continue
        
        return sorted(workflows, key=lambda x: x.get("created", ""), reverse=True)
    
    def show_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Show workflow details."""
        workflow = self._load_workflow(name)
        
        if not workflow:
            self.console.print(f"[bold red]❌ Workflow not found: {name}[/bold red]")
            return None
        
        self.console.print(f"\n[bold cyan]📋 Workflow: {name}[/bold cyan]\n")
        self.console.print(f"[bold]Description:[/bold] {workflow.get('description', '')}\n")
        
        steps = workflow.get("steps", [])
        if steps:
            table = Table(show_header=True)
            table.add_column("Step", width=5)
            table.add_column("Command", width=20)
            table.add_column("Parameters", width=40)
            
            for i, step in enumerate(steps, 1):
                params_str = str(step.get("params", {})) if step.get("params") else ""
                table.add_row(
                    str(i),
                    step.get("command", ""),
                    params_str[:40] + "..." if len(params_str) > 40 else params_str
                )
            
            self.console.print(table)
            self.console.print()
        
        return workflow
