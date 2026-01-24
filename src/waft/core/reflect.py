"""
Reflect - AI Journal System.

Induces the AI to write in its journal, reflecting on current work, thoughts,
and experiences. The AI definitely needs a journal if it doesn't have one.
"""

import json
import os
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

    def __init__(
        self,
        project_path: Path,
        ai_name: Optional[str] = None,
        ai_metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize reflect manager.

        Args:
            project_path: Path to project root
            ai_name: Optional AI identifier (e.g., 'claude-code', 'cursor', 'chatgpt')
            ai_metadata: Optional AI metadata override
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)
        self.ai_name = ai_name or os.getenv("WAFT_AI_NAME") or os.getenv("AI_NAME") or "default"
        self.ai_metadata = ai_metadata or {
            "name": self.ai_name,
            "model": os.getenv("AI_MODEL") or os.getenv("MODEL_NAME"),
            "provider": os.getenv("AI_PROVIDER"),
        }

        # Journal location - placed in _pyrite/journal/ (memory layer)
        # This is appropriate as the journal is part of the AI's memory system
        self.journal_dir = project_path / "_pyrite" / "journal"
        self.journal_file = self.journal_dir / "ai-journal.md"
        self.entries_dir = self.journal_dir / "entries"
        self.archive_dir = self.journal_dir / "archive"
        self.stats_dir = self.journal_dir / "stats"
        self.index_file = self.journal_dir / "index.json"
        self.chronicles_dir = self.journal_dir / "chronicles"  # NEW: Hierarchical structure
        self.discovery_file = self.journal_dir / "discovery.json"  # NEW: Being discovery manifest

        # Journal length threshold for archiving (default: 500 lines)
        self.archive_threshold = 500

        # Archive retention policy (days to keep archives)
        self.archive_retention_days = 365  # Keep archives for 1 year

        # CRITICAL: Validate journal_dir is within project_path (security)
        self._validate_journal_path()

        # Ensure journal structure exists
        self._ensure_journal_exists()
    
    def _validate_journal_path(self):
        """Validate journal path is within project path."""
        journal_path = self.journal_dir.resolve()
        project_path = self.project_path.resolve()
        try:
            journal_path.relative_to(project_path)
        except ValueError as exc:
            raise ValueError(
                f"Journal path {journal_path} is outside project path {project_path}"
            ) from exc

    def _ensure_journal_exists(self):
        """Ensure journal directory and file exist."""
        self.journal_dir.mkdir(parents=True, exist_ok=True)
        self.entries_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.stats_dir.mkdir(parents=True, exist_ok=True)
        self.chronicles_dir.mkdir(parents=True, exist_ok=True)  # NEW: Create chronicles directory

        # CRITICAL: Set restrictive file permissions (0700 for dirs, 0600 for files)
        try:
            self.journal_dir.chmod(0o700)
            self.chronicles_dir.chmod(0o700)
        except OSError:
            pass  # Permissions may not be changeable on all systems

        # Create journal file if it doesn't exist
        if not self.journal_file.exists():
            self._create_initial_journal()

        # Initialize index if it doesn't exist
        if not self.index_file.exists():
            self._create_index()

        # Create discovery manifest if it doesn't exist
        if not self.discovery_file.exists():
            self._create_discovery_manifest()

    def _check_and_archive_if_needed(self):
        """
        Check journal length and archive if it exceeds threshold.

        If journal is too long:
        1. Extract all entries
        2. Create archive file with date
        3. Keep only recent entries in main journal (last 100 lines or 2 entries)
        4. Move old entries to archive
        """
        if not self.journal_file.exists():
            return

        # Count lines in current journal
        content = self.journal_file.read_text(encoding="utf-8")
        line_count = len(content.splitlines())

        if line_count <= self.archive_threshold:
            return  # Journal is fine, no archiving needed

        # Journal is too long - archive it
        self.console.print(
            f"\n[bold yellow]📦 Journal exceeds {self.archive_threshold} lines ({line_count} lines)[/bold yellow]"
        )
        self.console.print("[dim]Archiving old entries...[/dim]\n")

        # Extract all entries
        entries = self._extract_journal_entries(content)

        if len(entries) < 2:
            # Not enough entries to archive, just keep everything
            return

        # Create archive filename with date
        archive_date = datetime.now().strftime("%Y-%m-%d")
        archive_file = self.archive_dir / f"ai-journal-{archive_date}.md"

        # If archive file already exists for today, append timestamp
        if archive_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            archive_file = self.archive_dir / f"ai-journal-{archive_date}-{timestamp}.md"

        # Write archived entries to archive file
        archive_content = []
        archive_content.append("# AI Journal Archive\n\n")
        archive_content.append(f"**Archived**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archive_content.append(f"**Original Journal**: {self.journal_file.name}\n")
        archive_content.append(f"**Total Entries Archived**: {len(entries) - 2}\n\n")
        archive_content.append("---\n\n")

        # Archive all entries except the last 2
        for entry in entries[:-2]:
            archive_content.append(entry)
            archive_content.append("\n---\n\n")

        archive_file.write_text("".join(archive_content), encoding="utf-8")

        # Create new journal with header and last 2 entries
        new_content = []
        new_content.append("# AI Journal\n\n")
        new_content.append(
            "Reflections, thoughts, and learnings from working on the WAFT project.\n\n"
        )
        new_content.append("---\n\n")
        new_content.append(f"*Previous entries archived to: {archive_file.name}*\n\n")
        new_content.append("---\n\n")

        # Add the last 2 entries
        for entry in entries[-2:]:
            new_content.append(entry)
            new_content.append("\n---\n\n")

        # Write new journal
        self.journal_file.write_text("".join(new_content), encoding="utf-8")

        self.console.print(
            f"[bold green]✅ Archived {len(entries) - 2} entries to {archive_file.name}[/bold green]"
        )
        self.console.print(f"[dim]Kept {len(entries[-2:])} recent entries in main journal[/dim]\n")

    def _extract_journal_entries(self, content: str) -> list[str]:
        """
        Extract individual journal entries from journal content.

        Args:
            content: Full journal content

        Returns:
            List of entry strings (each entry is a complete markdown section)
        """
        entries = []

        # Pattern to match entry headers: ## YYYY-MM-DD HH:MM - Title
        # or ## Journal Entry: YYYY-MM-DD HH:MM
        pattern = r"^## (?:Journal Entry: )?(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?(?:\s+-\s+.*)?)"

        matches = list(re.finditer(pattern, content, re.MULTILINE))

        if not matches:
            # No entries found, return entire content as single entry
            return [content]

        # Extract each entry
        for i, match in enumerate(matches):
            start_pos = match.start()

            # Find end position (start of next entry or end of file)
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content)

            entry = content[start_pos:end_pos].strip()
            if entry:
                entries.append(entry)

        return entries

    def _create_index(self):
        """Create an index file for journal entries and archives."""
        payload = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "ai_name": self.ai_name,
            "journal_file": str(self.journal_file.relative_to(self.project_path)),
            "entries": [],
            "archives": [],
        }
        self.index_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _create_discovery_manifest(self):
        """Create a discovery manifest for journal structure."""
        payload = {
            "created_at": datetime.now().isoformat(),
            "ai_metadata": self.ai_metadata,
            "paths": {
                "journal_dir": str(self.journal_dir.relative_to(self.project_path)),
                "journal_file": str(self.journal_file.relative_to(self.project_path)),
                "entries_dir": str(self.entries_dir.relative_to(self.project_path)),
                "archive_dir": str(self.archive_dir.relative_to(self.project_path)),
                "stats_dir": str(self.stats_dir.relative_to(self.project_path)),
                "chronicles_dir": str(self.chronicles_dir.relative_to(self.project_path)),
                "index_file": str(self.index_file.relative_to(self.project_path)),
            },
        }
        self.discovery_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _create_initial_journal(self):
        """Create initial journal file with header."""
        header = f"""# AI Journal: {self.ai_name}

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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

        entry = {
            "timestamp": timestamp.isoformat(),
            "date": date_str,
            "time": time_str,
            "prompts": prompts,
            "context": context,
            "ai_metadata": self.ai_metadata,
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

    def _save_journal_entry(self, entry: dict[str, Any]) -> Path:
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
        content.append(f"**Timestamp**: {entry['timestamp']}\n")

        # Enhanced metadata section
        metadata = []
        if entry.get("topic"):
            metadata.append(f"**Topic**: {entry['topic']}")

        if entry["context"].get("git", {}).get("initialized"):
            branch = entry["context"]["git"].get("branch", "unknown")
            uncommitted = entry["context"]["git"].get("uncommitted_count", 0)
            metadata.append(f"**Git**: Branch `{branch}`, {uncommitted} uncommitted files")

        if entry["context"].get("stats"):
            stats = entry["context"]["stats"]
            if stats.get("files_created") or stats.get("files_modified"):
                metadata.append(
                    f"**Session**: {stats.get('files_created', 0)} created, {stats.get('files_modified', 0)} modified"
                )

        if metadata:
            content.append(" | ".join(metadata))

        content.append("\n")

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

    def search_entries(
        self,
        query: Optional[str] = None,
        topic: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, str]]:
        """Search journal entries by query, topic, or date range."""
        entries: List[Dict[str, str]] = []
        query_lower = query.lower() if query else None
        topic_lower = topic.lower() if topic else None
        try:
            start_date = datetime.strptime(date_from, "%Y-%m-%d").date() if date_from else None
        except ValueError:
            start_date = None
        try:
            end_date = datetime.strptime(date_to, "%Y-%m-%d").date() if date_to else None
        except ValueError:
            end_date = None

        if self.entries_dir.exists():
            for entry_file in sorted(self.entries_dir.glob("*.md"), reverse=True):
                content = entry_file.read_text(encoding="utf-8")
                match = re.search(
                    r"^## Journal Entry: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})",
                    content,
                    re.MULTILINE,
                )
                if match:
                    date_str, time_str = match.group(1), match.group(2)
                else:
                    date_str, time_str = "Unknown", "Unknown"

                entries.append(
                    {"date": date_str, "time": time_str, "content": content}
                )
        elif self.journal_file.exists():
            content = self.journal_file.read_text(encoding="utf-8")
            pattern = r"^## Journal Entry: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
            matches = list(re.finditer(pattern, content, re.MULTILINE))
            for i, match in enumerate(matches):
                start_pos = match.start()
                end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
                entry_content = content[start_pos:end_pos].strip()
                date_time = match.group(1).split(" ")
                date_str = date_time[0] if date_time else "Unknown"
                time_str = date_time[1] if len(date_time) > 1 else "Unknown"
                entries.append(
                    {"date": date_str, "time": time_str, "content": entry_content}
                )

        filtered = []
        for entry in entries:
            content = entry.get("content", "")
            if query_lower and query_lower not in content.lower():
                continue
            if topic_lower and topic_lower not in content.lower():
                continue
            if start_date or end_date:
                try:
                    entry_date = datetime.strptime(entry.get("date", ""), "%Y-%m-%d").date()
                except ValueError:
                    entry_date = None
                if start_date and entry_date and entry_date < start_date:
                    continue
                if end_date and entry_date and entry_date > end_date:
                    continue
            filtered.append(entry)

        return filtered[:limit]

    def cleanup_old_archives(self):
        """Remove archive files older than retention policy."""
        if not self.archive_dir.exists():
            return

        cutoff = datetime.now().timestamp() - (self.archive_retention_days * 86400)
        removed = 0
        for archive_file in self.archive_dir.glob("ai-journal-*.md"):
            if archive_file.stat().st_mtime < cutoff:
                archive_file.unlink()
                removed += 1

        if removed:
            self.console.print(
                f"[bold green]✅ Removed {removed} archives older than {self.archive_retention_days} days[/bold green]"
            )

    def display_statistics(self):
        """Display journal statistics and analytics."""
        info = self.get_journal_info()
        archive_count = len(list(self.archive_dir.glob("ai-journal-*.md"))) if self.archive_dir.exists() else 0
        journal_size = self.journal_file.stat().st_size if self.journal_file.exists() else 0

        self.console.print("\n[bold cyan]📊 Journal Statistics[/bold cyan]\n")
        self.console.print(f"  • Path: {info.get('path', 'unknown')}")
        self.console.print(f"  • Entries: {info.get('entries_count', 0)}")
        self.console.print(f"  • Archives: {archive_count}")
        self.console.print(f"  • Last Entry: {info.get('last_entry') or 'None'}")
        self.console.print(f"  • Size: {journal_size} bytes\n")
