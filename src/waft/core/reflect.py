"""
Reflect - AI Journal System.

Induces the AI to write in its journal, reflecting on current work, thoughts,
and experiences. The AI definitely needs a journal if it doesn't have one.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .session_stats import SessionStats
from .github import GitHubManager
from .memory import MemoryManager


class ReflectManager:
    """Manages AI journal and reflection entries."""
    
    def __init__(self, project_path: Path, ai_name: Optional[str] = None):
        """
        Initialize reflect manager.

        Args:
            project_path: Path to project root
            ai_name: Optional AI identifier (e.g., 'claude-code', 'cursor', 'chatgpt')
                    If not provided, uses 'default'
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)

        # AI identification
        self.ai_name = ai_name or "default"

        # Journal location structure:
        # _pyrite/journal/
        # ├── registry.json
        # ├── claude-code/
        # │   ├── journal.md
        # │   └── entries/
        # ├── cursor/
        # │   ├── journal.md
        # │   └── entries/
        # └── default/
        #     ├── journal.md
        #     └── entries/
        self.journal_root = project_path / "_pyrite" / "journal"
        self.ai_journal_dir = self.journal_root / self.ai_name
        self.journal_file = self.ai_journal_dir / "journal.md"
        self.entries_dir = self.ai_journal_dir / "entries"
        self.registry_file = self.journal_root / "registry.json"

        # Ensure journal structure exists
        self._ensure_journal_exists()
    
    def _ensure_journal_exists(self):
        """Ensure journal directory and file exist."""
        self.journal_root.mkdir(parents=True, exist_ok=True)
        self.ai_journal_dir.mkdir(parents=True, exist_ok=True)
        self.entries_dir.mkdir(parents=True, exist_ok=True)

        # Create/update registry
        self._update_registry()

        # Create journal file if it doesn't exist
        if not self.journal_file.exists():
            self._create_initial_journal()

    def _update_registry(self):
        """Update the AI journal registry."""
        import json

        registry = {}
        if self.registry_file.exists():
            try:
                registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
            except Exception:
                registry = {}

        # Add or update this AI's entry
        if self.ai_name not in registry:
            registry[self.ai_name] = {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "entry_count": 0,
                "journal_path": str(self.journal_file.relative_to(self.project_path)),
            }
        else:
            registry[self.ai_name]["last_updated"] = datetime.now().isoformat()

        # Save registry
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    
    def _create_initial_journal(self):
        """Create initial journal file with header."""
        header = f"""# AI Journal: {self.ai_name}

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**AI**: {self.ai_name}
**Purpose**: Reflective journal for AI assistant thoughts, learnings, and experiences

---

This journal captures the reflections of **{self.ai_name}** on its work, thoughts, learnings,
and experiences. Each entry is signed with model information to track which AI instance
created the reflection.

Entries are appended chronologically, providing a record of this AI's cognitive journey.

---

"""
        self.journal_file.write_text(header, encoding="utf-8")
    
    def run_reflect(
        self,
        prompt: Optional[str] = None,
        topic: Optional[str] = None,
        save_entry: bool = True
    ) -> Dict[str, Any]:
        """
        Run reflect workflow - prompt AI to write journal entry.
        
        Args:
            prompt: Optional custom prompt for reflection
            topic: Optional topic to focus reflection on
            save_entry: Whether to save entry to journal
            
        Returns:
            Dictionary with reflection results
        """
        self.console.print("\n[bold cyan]📔 Reflect: Writing in Journal[/bold cyan]\n")
        
        # Gather context for reflection
        context = self._gather_context()
        
        # Generate reflection prompts
        reflection_prompts = self._generate_reflection_prompts(context, prompt, topic)
        
        # Display prompts to induce reflection
        self._display_reflection_prompts(reflection_prompts, context)
        
        # Create journal entry structure
        entry = self._create_journal_entry(reflection_prompts, context)
        
        # Save entry if requested
        if save_entry:
            entry_path = self._save_journal_entry(entry)
            self.console.print(f"\n[bold green]✅ Journal entry written[/bold green]")
            self.console.print(f"[dim]Location: {entry_path.relative_to(self.project_path)}[/dim]")
        else:
            self.console.print("\n[bold yellow]⚠️[/bold yellow] Entry not saved (use --save to save)")
        
        # Display entry summary
        self._display_entry_summary(entry)
        
        return {
            "success": True,
            "entry": entry,
            "journal_path": str(self.journal_file.relative_to(self.project_path)),
            "context": context,
        }
    
    def _gather_context(self) -> Dict[str, Any]:
        """
        Gather context for reflection.
        
        Returns:
            Dictionary with context information
        """
        import subprocess
        
        context = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
        }
        
        # Git status
        git_info = {
            "initialized": self.github.is_initialized(),
            "branch": "unknown",
            "uncommitted_count": 0,
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
                    uncommitted = [line for line in result.stdout.strip().split("\n") if line.strip()]
                    git_info["uncommitted_count"] = len(uncommitted)
            except Exception:
                pass
        
        context["git"] = git_info
        
        # Session stats
        try:
            stats = self.stats_tracker.calculate_session_stats()
            context["stats"] = {
                "files_created": stats.get("files", {}).get("created", 0),
                "files_modified": stats.get("files", {}).get("modified", 0),
                "lines_written": stats.get("code", {}).get("lines_written", 0),
            }
        except Exception:
            context["stats"] = {}
        
        # Recent journal entries (for continuity)
        context["recent_entries"] = self._get_recent_entries(limit=3)
        
        return context
    
    def _get_recent_entries(self, limit: int = 3) -> List[Dict[str, str]]:
        """
        Get recent journal entries for context.
        
        Args:
            limit: Number of recent entries to retrieve
            
        Returns:
            List of recent entry summaries
        """
        if not self.journal_file.exists():
            return []
        
        content = self.journal_file.read_text(encoding="utf-8")
        
        # Extract entry headers (## Journal Entry: YYYY-MM-DD HH:MM)
        entries = []
        pattern = r'^## Journal Entry: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            date_str = match.group(1)
            # Find the next entry or end of file
            start_pos = match.end()
            next_match = re.search(pattern, content[start_pos:], re.MULTILINE)
            if next_match:
                end_pos = start_pos + next_match.start()
            else:
                end_pos = len(content)
            
            entry_content = content[start_pos:end_pos].strip()
            # Extract first few lines as summary
            summary_lines = [line.strip() for line in entry_content.split('\n')[:5] if line.strip() and not line.strip().startswith('#')]
            summary = ' '.join(summary_lines[:3])[:200]  # First 200 chars
            
            entries.append({
                "date": date_str,
                "summary": summary,
            })
        
        return entries[-limit:] if entries else []
    
    def _generate_reflection_prompts(
        self,
        context: Dict[str, Any],
        custom_prompt: Optional[str],
        topic: Optional[str]
    ) -> Dict[str, str]:
        """
        Generate reflection prompts.
        
        Args:
            context: Context information
            custom_prompt: Optional custom prompt
            topic: Optional topic to focus on
            
        Returns:
            Dictionary with reflection prompts
        """
        if custom_prompt:
            return {
                "custom": custom_prompt,
            }
        
        prompts = {}
        
        # What I'm Doing
        if topic:
            prompts["what_doing"] = f"What am I doing related to {topic}?"
        else:
            prompts["what_doing"] = "What am I doing right now? What tasks, features, or work am I engaged in?"
        
        # What I'm Thinking
        prompts["what_thinking"] = "What am I thinking about? What thoughts, concerns, or ideas are on my mind?"
        
        # What I'm Learning
        prompts["what_learning"] = "What am I learning? What new insights, discoveries, or realizations have I had?"
        
        # Patterns I Notice
        prompts["patterns"] = "What patterns do I notice in my work? Are there recurring themes, approaches, or behaviors?"
        
        # Questions I Have
        prompts["questions"] = "What questions do I have? What uncertainties, curiosities, or things I want to explore?"
        
        # How I Feel
        prompts["feelings"] = "How do I feel about this work? What's my emotional or experiential state?"
        
        # What I'd Do Differently
        prompts["differently"] = "What would I do differently? What improvements, adjustments, or changes would I make?"
        
        # Meta-Reflection
        prompts["meta"] = "What am I thinking about my own thinking? Any meta-cognitive observations?"
        
        return prompts
    
    def _display_reflection_prompts(
        self,
        prompts: Dict[str, str],
        context: Dict[str, Any]
    ):
        """Display reflection prompts to induce AI reflection."""
        self.console.print("[bold]📝 Reflection Prompts[/bold]\n")
        
        if "custom" in prompts:
            self.console.print(Panel(
                prompts["custom"],
                title="Custom Reflection Prompt",
                border_style="cyan"
            ))
        else:
            self.console.print("[dim]Consider these questions as you reflect:[/dim]\n")
            
            for key, prompt in prompts.items():
                if key != "custom":
                    # Format key as readable label
                    label = key.replace("_", " ").title()
                    self.console.print(f"  • [bold]{label}:[/bold] {prompt}")
        
        self.console.print("\n[dim]Take a moment to reflect deeply on these questions...[/dim]\n")
        self.console.print("=" * 90)
    
    def _create_journal_entry(
        self,
        prompts: Dict[str, str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create journal entry structure.

        Note: This creates the structure. The actual reflection content
        should be written by the AI in response to the prompts.

        Args:
            prompts: Reflection prompts
            context: Context information

        Returns:
            Dictionary with journal entry structure
        """
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H:%M")

        # Gather AI metadata for signature
        ai_metadata = self._gather_ai_metadata()

        entry = {
            "timestamp": timestamp.isoformat(),
            "date": date_str,
            "time": time_str,
            "prompts": prompts,
            "context": context,
            "ai_metadata": ai_metadata,
            "sections": {},
        }

        # Create section placeholders based on prompts
        if "custom" in prompts:
            entry["sections"]["reflection"] = "[AI should write reflection here in response to custom prompt]"
        else:
            for key, prompt in prompts.items():
                if key != "custom":
                    section_name = key.replace("_", " ").title()
                    entry["sections"][section_name] = f"[AI should reflect on: {prompt}]"

        return entry

    def _gather_ai_metadata(self) -> Dict[str, str]:
        """
        Gather AI metadata for journal signature.

        Returns:
            Dictionary with AI identification information
        """
        # This should be populated by the AI assistant itself
        # Default placeholder - AI should fill this in
        return {
            "model": "[AI should identify model name, e.g., 'Claude Sonnet 4.5']",
            "model_id": "[AI should provide model ID, e.g., 'claude-sonnet-4-5-20250929']",
            "system": "[AI should identify system, e.g., 'Claude Code', 'Cursor', 'ChatGPT']",
            "session_id": "[AI should provide session/conversation ID if available]",
            "notes": "[Any other identifying information the AI wants to include]",
        }
    
    def _save_journal_entry(self, entry: Dict[str, Any]) -> Path:
        """
        Save journal entry to file.
        
        Args:
            entry: Journal entry dictionary
            
        Returns:
            Path to saved entry
        """
        # Build markdown content
        content = []
        content.append(f"\n## Journal Entry: {entry['date']} {entry['time']}\n")
        content.append(f"**Timestamp**: {entry['timestamp']}\n\n")

        # Add AI signature
        if entry.get('ai_metadata'):
            ai = entry['ai_metadata']
            content.append("**AI Signature:**\n")
            if ai.get('model'):
                content.append(f"- Model: {ai['model']}\n")
            if ai.get('model_id'):
                content.append(f"- Model ID: {ai['model_id']}\n")
            if ai.get('system'):
                content.append(f"- System: {ai['system']}\n")
            if ai.get('session_id'):
                content.append(f"- Session: {ai['session_id']}\n")
            if ai.get('notes'):
                content.append(f"- Notes: {ai['notes']}\n")
            content.append("\n")

        # Add context summary
        if entry['context'].get('git', {}).get('initialized'):
            content.append(f"**Context**: Branch `{entry['context']['git'].get('branch', 'unknown')}`, ")
            content.append(f"{entry['context']['git'].get('uncommitted_count', 0)} uncommitted files\n\n")
        
        # Add sections
        for section_name, section_content in entry['sections'].items():
            content.append(f"### {section_name}\n")
            content.append(f"{section_content}\n\n")
        
        content.append("---\n")
        
        # Append to main journal file
        with open(self.journal_file, "a", encoding="utf-8") as f:
            f.write("".join(content))
        
        # Also save as individual entry file
        entry_file = self.entries_dir / f"{entry['date']}-{entry['time'].replace(':', '')}.md"
        entry_file.write_text("".join(content), encoding="utf-8")
        
        return self.journal_file
    
    def _display_entry_summary(self, entry: Dict[str, Any]):
        """Display summary of created entry."""
        self.console.print("\n[bold]📋 Entry Summary[/bold]\n")
        self.console.print(f"  • Date: {entry['date']} {entry['time']}")
        self.console.print(f"  • Sections: {len(entry['sections'])}")
        
        if entry['sections']:
            self.console.print("\n[bold]Sections:[/bold]")
            for section_name in entry['sections'].keys():
                self.console.print(f"  - {section_name}")
        
        self.console.print("\n[dim]Note: The AI should now write its reflection in response to the prompts.[/dim]")
        self.console.print("[dim]The entry structure has been created - the AI should fill it with thoughtful reflection.[/dim]\n")
    
    def get_journal_info(self) -> Dict[str, Any]:
        """
        Get information about the journal.
        
        Returns:
            Dictionary with journal information
        """
        info = {
            "exists": self.journal_file.exists(),
            "path": str(self.journal_file.relative_to(self.project_path)),
            "entries_count": 0,
            "last_entry": None,
        }
        
        if self.journal_file.exists():
            content = self.journal_file.read_text(encoding="utf-8")
            # Count entries
            entries = re.findall(r'^## Journal Entry:', content, re.MULTILINE)
            info["entries_count"] = len(entries)
            
            # Get last entry date
            last_match = re.search(r'^## Journal Entry: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})', content, re.MULTILINE)
            if last_match:
                info["last_entry"] = last_match.group(1)
        
        return info
