"""
Reflect - AI Journal System.

Induces the AI to write in its journal, reflecting on current work, thoughts,
and experiences. The AI definitely needs a journal if it doesn't have one.

Enhanced with search, statistics, analytics, and improved integration.
"""

import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .github import GitHubManager
from .memory import MemoryManager
from .session_stats import SessionStats


class ReflectManager:
    """Manages AI journal and reflection entries."""

    def __init__(self, project_path: Path):
        """
        Initialize reflect manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.console = Console()
        self.stats_tracker = SessionStats(project_path)
        self.github = GitHubManager(project_path)
        self.memory = MemoryManager(project_path)

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

        # Check if journal needs archiving
        self._check_and_archive_if_needed()

    def _validate_journal_path(self):
        """
        CRITICAL: Validate journal_dir is within project_path (prevent path traversal).

        Raises:
            ValueError: If journal_dir escapes project_path
        """
        try:
            resolved_journal = self.journal_dir.resolve()
            resolved_project = self.project_path.resolve()

            if not resolved_journal.is_relative_to(resolved_project):
                raise ValueError(
                    f"Security violation: journal_dir ({self.journal_dir}) "
                    f"is not within project_path ({self.project_path})"
                )
        except (ValueError, OSError) as e:
            raise ValueError(f"Failed to validate journal path: {e}")

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

    def _create_initial_journal(self):
        """Create initial journal file with header."""
        header = f"""# AI Journal

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Purpose**: Reflective journal for AI assistant thoughts, learnings, and experiences

---

This journal captures the AI's reflections on its work, thoughts, learnings, and experiences.
Entries are appended chronologically, providing a record of the AI's cognitive journey.

---

"""
        self.journal_file.write_text(header, encoding="utf-8")

    def run_reflect(
        self, prompt: str | None = None, topic: str | None = None, save_entry: bool = True
    ) -> dict[str, Any]:
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
            self.console.print("\n[bold green]✅ Journal entry written[/bold green]")
            self.console.print(f"[dim]Location: {entry_path.relative_to(self.project_path)}[/dim]")

            # Check if journal needs archiving after adding new entry
            self._check_and_archive_if_needed()
        else:
            self.console.print(
                "\n[bold yellow]⚠️[/bold yellow] Entry not saved (use --save to save)"
            )

        # Display entry summary
        self._display_entry_summary(entry)

        return {
            "success": True,
            "entry": entry,
            "journal_path": str(self.journal_file.relative_to(self.project_path)),
            "context": context,
        }

    def _gather_context(self) -> dict[str, Any]:
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
                    uncommitted = [
                        line for line in result.stdout.strip().split("\n") if line.strip()
                    ]
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

    def _get_recent_entries(self, limit: int = 3) -> list[dict[str, str]]:
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
        pattern = r"^## Journal Entry: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})"

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
            summary_lines = [
                line.strip()
                for line in entry_content.split("\n")[:5]
                if line.strip() and not line.strip().startswith("#")
            ]
            summary = " ".join(summary_lines[:3])[:200]  # First 200 chars

            entries.append(
                {
                    "date": date_str,
                    "summary": summary,
                }
            )

        return entries[-limit:] if entries else []

    def _generate_reflection_prompts(
        self, context: dict[str, Any], custom_prompt: str | None, topic: str | None
    ) -> dict[str, str]:
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
            prompts["what_doing"] = (
                "What am I doing right now? What tasks, features, or work am I engaged in?"
            )

        # What I'm Thinking
        prompts["what_thinking"] = (
            "What am I thinking about? What thoughts, concerns, or ideas are on my mind?"
        )

        # What I'm Learning
        prompts["what_learning"] = (
            "What am I learning? What new insights, discoveries, or realizations have I had?"
        )

        # Patterns I Notice
        prompts["patterns"] = (
            "What patterns do I notice in my work? Are there recurring themes, approaches, or behaviors?"
        )

        # Questions I Have
        prompts["questions"] = (
            "What questions do I have? What uncertainties, curiosities, or things I want to explore?"
        )

        # How I Feel
        prompts["feelings"] = (
            "How do I feel about this work? What's my emotional or experiential state?"
        )

        # What I'd Do Differently
        prompts["differently"] = (
            "What would I do differently? What improvements, adjustments, or changes would I make?"
        )

        # Meta-Reflection
        prompts["meta"] = (
            "What am I thinking about my own thinking? Any meta-cognitive observations?"
        )

        return prompts

    def _display_reflection_prompts(self, prompts: dict[str, str], context: dict[str, Any]):
        """Display reflection prompts to induce AI reflection."""
        self.console.print("[bold]📝 Reflection Prompts[/bold]\n")

        if "custom" in prompts:
            self.console.print(
                Panel(prompts["custom"], title="Custom Reflection Prompt", border_style="cyan")
            )
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
        self, prompts: dict[str, str], context: dict[str, Any]
    ) -> dict[str, Any]:
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
            "sections": {},
        }

        # Create section placeholders based on prompts
        if "custom" in prompts:
            entry["sections"]["reflection"] = (
                "[AI should write reflection here in response to custom prompt]"
            )
        else:
            for key, prompt in prompts.items():
                if key != "custom":
                    section_name = key.replace("_", " ").title()
                    entry["sections"][section_name] = f"[AI should reflect on: {prompt}]"

        return entry

    def _save_journal_entry(self, entry: dict[str, Any]) -> Path:
        """
        Save journal entry to file with dual-write strategy (hierarchical + legacy).

        NEW: Writes to hierarchical chronicle structure (YYYY/MM/DD/HH/entries.md)
        LEGACY: Also writes to flat structure for backward compatibility

        Args:
            entry: Journal entry dictionary

        Returns:
            Path to saved entry (chronicle path)
        """
        # Parse timestamp
        timestamp = datetime.fromisoformat(entry["timestamp"])

        # Build markdown content with enhanced metadata
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
        for section_name, section_content in entry["sections"].items():
            content.append(f"### {section_name}\n")
            content.append(f"{section_content}\n\n")

        content.append("---\n")
        content_text = "".join(content)

        # NEW: Write to hierarchical chronicle structure
        chronicle_path = self._get_chronicle_path(timestamp)
        chronicle_path.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set restrictive permissions on directory
        try:
            chronicle_path.chmod(0o700)
        except OSError:
            pass

        chronicle_entries_file = chronicle_path / "entries.md"

        # Append to hour-level entries.md
        try:
            with open(chronicle_entries_file, "a", encoding="utf-8") as f:
                f.write(content_text)

            # CRITICAL: Set restrictive permissions on file (0600)
            try:
                chronicle_entries_file.chmod(0o600)
            except OSError:
                pass
        except OSError as e:
            self.console.print(f"[bold red]Error writing to chronicle: {e}[/bold red]")
            # Fall back to legacy structure if chronicle write fails

        # Update hour-level index.json
        self._update_hour_index(chronicle_path, entry)

        # LEGACY: Also append to main journal file (backward compatibility)
        try:
            with open(self.journal_file, "a", encoding="utf-8") as f:
                f.write(content_text)
        except OSError as e:
            self.console.print(
                f"[bold yellow]Warning: Could not write to legacy journal: {e}[/bold yellow]"
            )

        # LEGACY: Also save as individual entry file
        entry_file = self.entries_dir / f"{entry['date']}-{entry['time'].replace(':', '')}.md"
        try:
            entry_file.write_text(content_text, encoding="utf-8")
            # CRITICAL: Set restrictive permissions
            try:
                entry_file.chmod(0o600)
            except OSError:
                pass
        except OSError as e:
            self.console.print(
                f"[bold yellow]Warning: Could not write legacy entry file: {e}[/bold yellow]"
            )

        # Update master index
        self._update_index(entry)

        return chronicle_entries_file

    def _display_entry_summary(self, entry: dict[str, Any]):
        """Display summary of created entry."""
        self.console.print("\n[bold]📋 Entry Summary[/bold]\n")
        self.console.print(f"  • Date: {entry['date']} {entry['time']}")
        self.console.print(f"  • Sections: {len(entry['sections'])}")

        if entry["sections"]:
            self.console.print("\n[bold]Sections:[/bold]")
            for section_name in entry["sections"].keys():
                self.console.print(f"  - {section_name}")

        self.console.print(
            "\n[dim]Note: The AI should now write its reflection in response to the prompts.[/dim]"
        )
        self.console.print(
            "[dim]The entry structure has been created - the AI should fill it with thoughtful reflection.[/dim]\n"
        )

    def get_journal_info(self) -> dict[str, Any]:
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
            # Count entries - match both formats:
            # "## Journal Entry: YYYY-MM-DD HH:MM" or "## YYYY-MM-DD HH:MM - Title"
            entries = re.findall(
                r"^## (?:Journal Entry: )?(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)",
                content,
                re.MULTILINE,
            )
            info["entries_count"] = len(entries)

            # Get last entry date - find all matches and get the last one
            all_matches = list(
                re.finditer(
                    r"^## (?:Journal Entry: )?(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)",
                    content,
                    re.MULTILINE,
                )
            )
            if all_matches:
                info["last_entry"] = all_matches[-1].group(1)

        return info

    def _create_index(self):
        """Create initial journal index for fast lookups."""
        index = {
            "created": datetime.now().isoformat(),
            "entries": [],
            "tags": {},
            "topics": {},
            "stats": {
                "total_entries": 0,
                "first_entry": None,
                "last_entry": None,
            },
        }
        self.index_file.write_text(json.dumps(index, indent=2), encoding="utf-8")

    def _get_chronicle_path(self, timestamp: datetime) -> Path:
        """
        Generate YYYY/MM/DD/HH path for entry with CRITICAL security validation.

        This method implements the hierarchical chronicling structure while preventing
        path traversal attacks through comprehensive validation.

        Args:
            timestamp: Datetime for the entry

        Returns:
            Path to chronicle directory (YYYY/MM/DD/HH)

        Raises:
            ValueError: If timestamp components are invalid or path traversal detected
        """
        # CRITICAL: Validate timestamp components
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour

        if not (1900 <= year <= 2100):
            raise ValueError(f"Invalid year: {year} (must be 1900-2100)")
        if not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month} (must be 1-12)")
        if not (1 <= day <= 31):
            raise ValueError(f"Invalid day: {day} (must be 1-31)")
        if not (0 <= hour <= 23):
            raise ValueError(f"Invalid hour: {hour} (must be 0-23)")

        # Build path using formatted strings (safe - no user input)
        chronicle_path = (
            self.journal_dir
            / "chronicles"
            / f"{year:04d}"
            / f"{month:02d}"
            / f"{day:02d}"
            / f"{hour:02d}"
        )

        # CRITICAL: Resolve and validate path stays within journal_dir
        # This prevents symlink attacks and path traversal
        try:
            resolved_path = chronicle_path.resolve()
            resolved_journal_dir = self.journal_dir.resolve()

            if not resolved_path.is_relative_to(resolved_journal_dir):
                raise ValueError(
                    f"Path traversal detected: {chronicle_path} "
                    f"resolves outside journal_dir {resolved_journal_dir}"
                )
        except (ValueError, OSError) as e:
            raise ValueError(f"Failed to validate chronicle path: {e}")

        return chronicle_path

    def _create_discovery_manifest(self):
        """
        Create discovery.json manifest for Being discovery mechanism.

        This file enables Beings to discover and understand the journal structure
        through probing mechanisms.
        """
        manifest = {
            "journal_path": str(self.journal_dir.relative_to(self.project_path)),
            "structure": "hierarchical",
            "format": "markdown",
            "entry_types": ["structured", "simple", "being"],
            "time_segmentation": {
                "levels": ["year", "month", "day", "hour"],
                "format": "YYYY/MM/DD/HH",
            },
            "discovery_hints": [
                "Look for _pyrite/journal/chronicles/",
                "Entries organized by time: YYYY/MM/DD/HH/entries.md",
                "Master index at _pyrite/journal/index.json",
                "Discovery manifest at _pyrite/journal/discovery.json",
            ],
            "last_updated": datetime.now().isoformat(),
        }

        self.discovery_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        # CRITICAL: Set restrictive permissions (0600)
        try:
            self.discovery_file.chmod(0o600)
        except OSError:
            pass  # Permissions may not be changeable on all systems

    def _update_hour_index(self, chronicle_path: Path, entry: dict[str, Any]):
        """
        Update hour-level index.json for hierarchical chronicle structure.

        Args:
            chronicle_path: Path to chronicle directory (YYYY/MM/DD/HH)
            entry: Journal entry dictionary
        """
        hour_index_file = chronicle_path / "index.json"

        try:
            if hour_index_file.exists():
                hour_index = json.loads(hour_index_file.read_text(encoding="utf-8"))
            else:
                hour_index = {
                    "hour": entry["time"].split(":")[0],
                    "date": entry["date"],
                    "entries": [],
                    "entry_count": 0,
                }
        except (json.JSONDecodeError, FileNotFoundError):
            hour_index = {
                "hour": entry["time"].split(":")[0],
                "date": entry["date"],
                "entries": [],
                "entry_count": 0,
            }

        entry_id = f"{entry['date']}-{entry['time'].replace(':', '')}"
        entry_info = {
            "id": entry_id,
            "timestamp": entry["timestamp"],
            "format": self._detect_entry_format(entry),
        }

        hour_index["entries"].append(entry_info)
        hour_index["entry_count"] = len(hour_index["entries"])
        hour_index["last_updated"] = datetime.now().isoformat()

        hour_index_file.write_text(json.dumps(hour_index, indent=2), encoding="utf-8")

        # CRITICAL: Set restrictive permissions (0600)
        try:
            hour_index_file.chmod(0o600)
        except OSError:
            pass

    def _detect_entry_format(self, entry: dict[str, Any]) -> str:
        """
        Detect entry format: structured, simple, or being.

        Args:
            entry: Journal entry dictionary

        Returns:
            Format string: "structured", "simple", or "being"
        """
        if entry.get("being_id"):
            return "being"
        elif entry.get("sections") and len(entry.get("sections", {})) > 1:
            return "structured"
        else:
            return "simple"

    def _update_index(self, entry: dict[str, Any]):
        """Update journal index with new entry."""
        if not self.index_file.exists():
            self._create_index()

        try:
            index = json.loads(self.index_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            index = self._create_index()

        entry_id = f"{entry['date']}-{entry['time'].replace(':', '')}"
        entry_info = {
            "id": entry_id,
            "date": entry["date"],
            "time": entry["time"],
            "timestamp": entry["timestamp"],
            "topic": entry.get("context", {}).get("topic"),
            "sections": list(entry.get("sections", {}).keys()),
        }

        index["entries"].append(entry_info)
        index["stats"]["total_entries"] = len(index["entries"])

        if not index["stats"]["first_entry"]:
            index["stats"]["first_entry"] = entry["timestamp"]
        index["stats"]["last_entry"] = entry["timestamp"]

        # Update topics
        if entry_info["topic"]:
            if entry_info["topic"] not in index["topics"]:
                index["topics"][entry_info["topic"]] = []
            index["topics"][entry_info["topic"]].append(entry_id)

        self.index_file.write_text(json.dumps(index, indent=2), encoding="utf-8")

    def search_entries(
        self,
        query: str | None = None,
        topic: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search journal entries.

        Args:
            query: Text search query
            topic: Filter by topic
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        results = []

        # Search main journal
        if self.journal_file.exists():
            content = self.journal_file.read_text(encoding="utf-8")
            entries = self._extract_journal_entries(content)

            for entry_text in entries:
                entry_data = self._parse_entry(entry_text)
                if not entry_data:
                    continue

                # Apply filters
                if topic and entry_data.get("topic") != topic:
                    continue

                if date_from and entry_data.get("date") < date_from:
                    continue

                if date_to and entry_data.get("date") > date_to:
                    continue

                if query and query.lower() not in entry_text.lower():
                    continue

                results.append(entry_data)

                if len(results) >= limit:
                    break

        # Search archives
        if len(results) < limit:
            for archive_file in sorted(self.archive_dir.glob("*.md"), reverse=True):
                try:
                    archive_content = archive_file.read_text(encoding="utf-8")
                    archive_entries = self._extract_journal_entries(archive_content)

                    for entry_text in archive_entries:
                        entry_data = self._parse_entry(entry_text)
                        if not entry_data:
                            continue

                        # Apply filters
                        if topic and entry_data.get("topic") != topic:
                            continue

                        if date_from and entry_data.get("date") < date_from:
                            continue

                        if date_to and entry_data.get("date") > date_to:
                            continue

                        if query and query.lower() not in entry_text.lower():
                            continue

                        results.append(entry_data)

                        if len(results) >= limit:
                            break
                except Exception:
                    continue

                if len(results) >= limit:
                    break

        return results[:limit]

    def _parse_entry(self, entry_text: str) -> dict[str, Any] | None:
        """Parse a journal entry text into structured data."""
        # Extract date/time
        date_match = re.search(
            r"^## (?:Journal Entry: )?(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2}))?",
            entry_text,
            re.MULTILINE,
        )
        if not date_match:
            return None

        date_str = date_match.group(1)
        time_str = date_match.group(2) or "00:00"

        # Extract sections
        sections = {}
        section_pattern = r"^### (.+?)\n(.*?)(?=^### |^---|$)"
        for match in re.finditer(section_pattern, entry_text, re.MULTILINE | re.DOTALL):
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_name] = section_content

        return {
            "date": date_str,
            "time": time_str,
            "timestamp": f"{date_str}T{time_str}:00",
            "sections": sections,
            "content": entry_text,
        }

    def get_statistics(self) -> dict[str, Any]:
        """
        Get comprehensive journal statistics.

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_entries": 0,
            "entries_by_date": defaultdict(int),
            "entries_by_topic": defaultdict(int),
            "total_words": 0,
            "average_entry_length": 0,
            "first_entry": None,
            "last_entry": None,
            "archive_count": 0,
            "archive_size_mb": 0,
        }

        # Count entries in main journal
        if self.journal_file.exists():
            content = self.journal_file.read_text(encoding="utf-8")
            entries = self._extract_journal_entries(content)
            stats["total_entries"] = len(entries)

            for entry_text in entries:
                entry_data = self._parse_entry(entry_text)
                if entry_data:
                    stats["entries_by_date"][entry_data["date"]] += 1
                    stats["total_words"] += len(entry_text.split())

                    if not stats["first_entry"]:
                        stats["first_entry"] = entry_data["timestamp"]
                    stats["last_entry"] = entry_data["timestamp"]

        # Count archives
        archive_files = list(self.archive_dir.glob("*.md"))
        stats["archive_count"] = len(archive_files)

        total_size = sum(f.stat().st_size for f in archive_files if f.exists())
        stats["archive_size_mb"] = round(total_size / (1024 * 1024), 2)

        if stats["total_entries"] > 0:
            stats["average_entry_length"] = stats["total_words"] // stats["total_entries"]

        return stats

    def display_statistics(self):
        """Display journal statistics in a formatted table."""
        stats = self.get_statistics()

        table = Table(title="📊 Journal Statistics", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="dim")
        table.add_column("Value", justify="right")

        table.add_row("Total Entries", str(stats["total_entries"]))
        table.add_row("Total Words", f"{stats['total_words']:,}")
        table.add_row("Average Entry Length", f"{stats['average_entry_length']} words")
        table.add_row("Archive Files", str(stats["archive_count"]))
        table.add_row("Archive Size", f"{stats['archive_size_mb']} MB")

        if stats["first_entry"]:
            table.add_row("First Entry", stats["first_entry"][:10])
        if stats["last_entry"]:
            table.add_row("Last Entry", stats["last_entry"][:10])

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

    def cleanup_old_archives(self):
        """Remove archive files older than retention policy."""
        cutoff_date = datetime.now() - timedelta(days=self.archive_retention_days)
        removed_count = 0

        for archive_file in self.archive_dir.glob("*.md"):
            try:
                file_time = datetime.fromtimestamp(archive_file.stat().st_mtime)
                if file_time < cutoff_date:
                    archive_file.unlink()
                    removed_count += 1
            except Exception:
                continue

        if removed_count > 0:
            self.console.print(f"[dim]Cleaned up {removed_count} old archive files[/dim]\n")

        return removed_count
