"""
Help - Command discovery and usage guidance.

Lists all available commands, organized by category, with brief descriptions,
usage guidance, and example strings.
"""

from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .memory import MemoryManager


class HelpManager:
    """Manages command discovery and help display."""
    
    COMMAND_CATEGORIES = {
        "Core Workflow": [
            ("phase1", "Gather all project data, create interactive dashboard. Use when starting work, need full overview."),
            ("analyze", "Analyze Phase 1 data, generate insights and action plans. Use after Phase 1, need recommendations."),
            ("resume", "Load last session summary, compare current state, continue previous work. Use when starting new session."),
            ("continue", "Reflect on current work, then continue with awareness. Use mid-work, want reflection without stopping."),
            ("proceed", "Verify context and assumptions before continuing. Use when need to check understanding before acting."),
            ("reflect", "Prompt AI to write reflective journal entries. Use when want AI to document thoughts, learnings, experiences."),
            ("checkpoint", "Document current state, progress, todos. Use when need snapshot of current situation."),
            ("verify", "Verify project state with traceable evidence. Use when need to verify project is in good state."),
            ("checkout", "Run cleanup, documentation, summary tasks. Use when ending session, want comprehensive wrap-up."),
        ],
        "Analysis & Planning": [
            ("consider", "Analysis and recommendations for decisions. Use when need structured analysis of options."),
            ("decide", "Decision matrix with mathematical calculations. Use when need quantitative decision support."),
            ("explore", "Deep exploration of codebase or concepts. Use when need thorough understanding of topic."),
        ],
        "Project Management": [
            ("orient", "Project startup process and orientation. Use when starting new project or returning after break."),
            ("spin-up", "Quick orientation and context gathering. Use when need fast project overview."),
            ("engineer", "Complete workflow from analysis to implementation. Use when want full engineering process."),
        ],
        "Utility": [
            ("visualize", "Quick interactive browser dashboard. Use when want visual representation of project state."),
            ("stats", "Session statistics (files, lines, activity). Use when want to see what was accomplished in session."),
            ("analytics", "Session analytics and historical analysis. Use when want to understand work patterns over time."),
            ("recap", "Conversation recap and session summary. Use when want summary of conversation/session."),
        ],
        "Goal Management": [
            ("goal", "Track larger goals, break into steps. Use when have larger objective, want to track progress."),
            ("next", "Identify next step based on goals. Use when want to know what to do next, need direction."),
        ],
    }
    
    USAGE_EXAMPLES = {
        "Starting Work": [
            "/orient - Get project orientation and context",
            "/phase1 - Gather all project data and create dashboard",
            "/resume - Continue from last session",
            "/goal create feature-auth \"Implement authentication system\" - Create new goal",
        ],
        "During Work": [
            "/continue - Reflect on current work and continue",
            "/proceed - Verify context and assumptions before continuing",
            "/proceed --strict - Ask questions before proceeding",
            "/checkpoint - Take snapshot of current state",
            "/next - Get next step recommendation",
            "/goal show feature-auth - View goal progress",
            "/reflect - Write in journal about current work",
        ],
        "Making Decisions": [
            "/consider - Get analysis and recommendations",
            "/decide - Use decision matrix for choices",
            "/explore - Deep dive into topic before deciding",
        ],
        "Ending Work": [
            "/checkout - Comprehensive end-of-session workflow",
            "/recap - Create conversation summary",
            "/stats - View session statistics",
            "/goal update feature-auth --step 3 --complete - Mark step complete",
        ],
        "Discovery & Learning": [
            "/help - Discover all available commands",
            "/help --category Goal - Show goal management commands",
            "/help --search reflect - Find reflection-related commands",
            "/analytics - Analyze work patterns over time",
        ],
        "Goal Workflow": [
            "/goal create api-v2 \"Build REST API v2\" - Create goal",
            "/goal list - List all goals",
            "/goal show api-v2 - View goal details",
            "/next - Get next step from active goals",
            "/next --goal api-v2 - Get next step for specific goal",
            "/next --count 3 - Get top 3 next steps",
        ],
    }
    
    def __init__(self, project_path: Path):
        """
        Initialize help manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.memory = MemoryManager(project_path)
    
    def run_help(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        command: Optional[str] = None,
        count: bool = False,
    ):
        """
        Run help command.
        
        Args:
            category: Filter by category
            search: Search commands by keyword
            command: Show details for specific command
            count: Just show command count
        """
        if count:
            self._show_count()
            return
        
        if command:
            self._show_command_details(command)
            return
        
        if category or search:
            self._show_filtered(category=category, search=search)
        else:
            self._show_all()
        
        # Always show usage examples
        self._show_usage_examples()
    
    def _show_count(self):
        """Show total command count."""
        total = sum(len(commands) for commands in self.COMMAND_CATEGORIES.values())
        
        self.console.print("\n[bold cyan]📚 Help: Command Discovery[/bold cyan]\n")
        self.console.print(f"Total Commands: {total}\n")
        
        for category, commands in self.COMMAND_CATEGORIES.items():
            self.console.print(f"  • {category}: {len(commands)} commands")
        self.console.print()
    
    def _show_all(self):
        """Show all commands organized by category."""
        self.console.print("\n[bold cyan]📚 Help: Command Discovery[/bold cyan]\n")
        
        for category, commands in self.COMMAND_CATEGORIES.items():
            self.console.print(f"[bold]{category}[/bold]")
            self.console.print("─" * 60)
            
            for i, (cmd_name, description) in enumerate(commands, 1):
                self.console.print(f"  {i}. [bold cyan]/{cmd_name}[/bold cyan]")
                self.console.print(f"     {description}\n")
        
        self.console.print()
    
    def _show_filtered(self, category: Optional[str] = None, search: Optional[str] = None):
        """Show filtered commands."""
        self.console.print("\n[bold cyan]📚 Help: Command Discovery[/bold cyan]\n")
        
        if category:
            self.console.print(f"[bold]Filter: Category = {category}[/bold]\n")
        if search:
            self.console.print(f"[bold]Filter: Search = '{search}'[/bold]\n")
        
        for cat_name, commands in self.COMMAND_CATEGORIES.items():
            if category and cat_name.lower() != category.lower():
                continue
            
            filtered_commands = []
            for cmd_name, description in commands:
                if search:
                    if search.lower() in cmd_name.lower() or search.lower() in description.lower():
                        filtered_commands.append((cmd_name, description))
                else:
                    filtered_commands.append((cmd_name, description))
            
            if filtered_commands:
                self.console.print(f"[bold]{cat_name}[/bold]")
                self.console.print("─" * 60)
                
                for i, (cmd_name, description) in enumerate(filtered_commands, 1):
                    self.console.print(f"  {i}. [bold cyan]/{cmd_name}[/bold cyan]")
                    self.console.print(f"     {description}\n")
        
        self.console.print()
    
    def _show_command_details(self, command: str):
        """Show detailed information for a specific command."""
        self.console.print(f"\n[bold cyan]📚 Help: /{command}[/bold cyan]\n")
        
        # Find command in categories
        found = False
        for category, commands in self.COMMAND_CATEGORIES.items():
            for cmd_name, description in commands:
                if cmd_name == command:
                    self.console.print(f"[bold]Category:[/bold] {category}")
                    self.console.print(f"[bold]Description:[/bold] {description}\n")
                    found = True
                    break
            if found:
                break
        
        if not found:
            self.console.print(f"[red]Command '{command}' not found.[/red]\n")
            return
        
        # Show related examples
        self.console.print("[bold]Usage Examples:[/bold]\n")
        example_found = False
        for scenario, examples in self.USAGE_EXAMPLES.items():
            for example in examples:
                if f"/{command}" in example or command in example:
                    self.console.print(f"  • {example}")
                    example_found = True
        
        if not example_found:
            self.console.print(f"  • /{command} - Run command")
        
        self.console.print()
    
    def _show_usage_examples(self):
        """Show usage examples organized by scenario."""
        self.console.print("[bold cyan]💡 Usage Examples[/bold cyan]\n")
        self.console.print("Common workflows and example command strings:\n")
        
        for scenario, examples in self.USAGE_EXAMPLES.items():
            self.console.print(f"[bold]{scenario}[/bold]")
            self.console.print("─" * 60)
            
            for example in examples:
                self.console.print(f"  • {example}")
            
            self.console.print()
        
        self.console.print("[dim]Tip: Use /help --command <name> for detailed command information[/dim]\n")
