"""
Devlog Manager - Categorized, timestamped devlog entry management.

Transforms devlog from single-file to categorized, organized, timestamped entry files
based on update source and category.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from .github import GitHubManager
from .session_stats import SessionStats


class DevlogManager:
    """Manages categorized devlog entries with source and category tracking."""

    # Source types
    SOURCE_COMMAND = "command"
    SOURCE_SCRIPT = "script"
    SOURCE_API = "api"
    SOURCE_BEING = "being"
    SOURCE_WORKFLOW = "workflow"
    SOURCE_MANUAL = "manual"

    # Categories
    CATEGORY_FEATURE = "feature"
    CATEGORY_BUGFIX = "bugfix"
    CATEGORY_REFACTOR = "refactor"
    CATEGORY_DOCUMENTATION = "documentation"
    CATEGORY_RESEARCH = "research"
    CATEGORY_MAINTENANCE = "maintenance"

    def __init__(self, project_path: Path):
        """
        Initialize devlog manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.devlog_dir = project_path / "_work_efforts" / "devlog"
        self.legacy_devlog = project_path / "_work_efforts" / "devlog.md"
        self.index_file = self.devlog_dir / "index.json"

        # Directory structure
        self.by_source_dir = self.devlog_dir / "by_source"
        self.by_category_dir = self.devlog_dir / "by_category"
        self.by_date_dir = self.devlog_dir / "by_date"

        # Subdirectories for sources
        self.source_dirs = {
            self.SOURCE_COMMAND: self.by_source_dir / "command",
            self.SOURCE_SCRIPT: self.by_source_dir / "script",
            self.SOURCE_API: self.by_source_dir / "api",
            self.SOURCE_BEING: self.by_source_dir / "being",
            self.SOURCE_WORKFLOW: self.by_source_dir / "workflow",
            self.SOURCE_MANUAL: self.by_source_dir / "manual",
        }

        # Subdirectories for categories
        self.category_dirs = {
            self.CATEGORY_FEATURE: self.by_category_dir / "feature",
            self.CATEGORY_BUGFIX: self.by_category_dir / "bugfix",
            self.CATEGORY_REFACTOR: self.by_category_dir / "refactor",
            self.CATEGORY_DOCUMENTATION: self.by_category_dir / "documentation",
            self.CATEGORY_RESEARCH: self.by_category_dir / "research",
            self.CATEGORY_MAINTENANCE: self.by_category_dir / "maintenance",
        }

        self.github = GitHubManager(project_path)
        self.stats_tracker = SessionStats(project_path)

        # Ensure directory structure exists
        self._ensure_structure()

        # Load index
        self.index = self._load_index()

    def _ensure_structure(self):
        """Ensure all directory structure exists."""
        self.devlog_dir.mkdir(parents=True, exist_ok=True)
        self.by_source_dir.mkdir(exist_ok=True)
        self.by_category_dir.mkdir(exist_ok=True)
        self.by_date_dir.mkdir(exist_ok=True)

        for dir_path in self.source_dirs.values():
            dir_path.mkdir(exist_ok=True)

        for dir_path in self.category_dirs.values():
            dir_path.mkdir(exist_ok=True)

    def _load_index(self) -> dict[str, Any]:
        """Load index from JSON file."""
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except (json.JSONDecodeError, OSError):
                return {"entries": [], "last_updated": None}
        return {"entries": [], "last_updated": None}

    def _save_index(self):
        """Save index to JSON file."""
        self.index["last_updated"] = datetime.now().isoformat()
        self.index_file.write_text(json.dumps(self.index, indent=2))

    def _detect_source(self) -> str:
        """
        Automatically detect source of devlog entry.

        Returns:
            Source type (command, script, api, being, workflow, manual)
        """
        import inspect

        # Check call stack for source detection
        frame = inspect.currentframe()
        try:
            # Go up 2 frames (skip _detect_source and write_entry)
            caller_frame = frame.f_back.f_back if frame.f_back else None
            if caller_frame:
                filename = caller_frame.f_code.co_filename

                # Check if from .cursor/commands/
                if ".cursor/commands/" in filename:
                    return self.SOURCE_COMMAND

                # Check if from scripts/
                if "/scripts/" in filename:
                    return self.SOURCE_SCRIPT

                # Check if from API routes
                if "/api/" in filename or "router" in filename.lower():
                    return self.SOURCE_API

                # Check if from Being system
                if "being" in filename.lower():
                    return self.SOURCE_BEING

                # Check if from workflow commands
                if any(cmd in filename.lower() for cmd in ["version-bake", "evolve", "workflow"]):
                    return self.SOURCE_WORKFLOW
        finally:
            del frame

        # Default to manual if can't detect
        return self.SOURCE_MANUAL

    def _detect_category(self, content: str) -> str:
        """
        Detect category from content analysis.

        Args:
            content: Entry content

        Returns:
            Category type
        """
        content_lower = content.lower()

        # Feature indicators
        if any(word in content_lower for word in ["feature", "add", "implement", "new", "create"]):
            return self.CATEGORY_FEATURE

        # Bugfix indicators
        if any(word in content_lower for word in ["fix", "bug", "error", "issue", "correct"]):
            return self.CATEGORY_BUGFIX

        # Refactor indicators
        if any(
            word in content_lower for word in ["refactor", "restructure", "reorganize", "cleanup"]
        ):
            return self.CATEGORY_REFACTOR

        # Documentation indicators
        if any(word in content_lower for word in ["document", "doc", "readme", "guide", "manual"]):
            return self.CATEGORY_DOCUMENTATION

        # Research indicators
        if any(
            word in content_lower
            for word in ["research", "investigate", "analyze", "study", "explore"]
        ):
            return self.CATEGORY_RESEARCH

        # Default to maintenance
        return self.CATEGORY_MAINTENANCE

    def _get_entry_path(
        self, source: str, category: str, timestamp: datetime
    ) -> tuple[Path, Path, Path]:
        """
        Generate entry file paths for all three organization schemes.

        Args:
            source: Source type
            category: Category type
            timestamp: Entry timestamp

        Returns:
            Tuple of (by_source_path, by_category_path, by_date_path)
        """
        timestamp_str = timestamp.strftime("%Y-%m-%d_%H%M%S")
        filename = f"{timestamp_str}_{source}_{category}.md"

        by_source_path = self.source_dirs[source] / filename
        by_category_path = self.category_dirs[category] / filename
        date_dir = self.by_date_dir / timestamp.strftime("%Y-%m-%d")
        date_dir.mkdir(exist_ok=True)
        by_date_path = date_dir / filename

        return by_source_path, by_category_path, by_date_path

    def _get_context(self) -> dict[str, Any]:
        """Get context metadata for entry."""
        context = {}

        # Git branch
        if self.github.is_initialized():
            status = self.github.get_status()
            context["git_branch"] = status.get("branch")

        # Session stats
        stats = self.stats_tracker.calculate_session_stats()
        context["session_stats"] = {
            "files_created": stats.get("files_created", 0),
            "files_modified": stats.get("files_modified", 0),
        }

        return context

    def write_entry(
        self,
        content: str,
        source: str | None = None,
        category: str | None = None,
        metadata: dict[str, Any] | None = None,
        title: str | None = None,
    ) -> dict[str, Any]:
        """
        Write categorized devlog entry.

        Args:
            content: Entry content
            source: Source type (auto-detected if None)
            category: Category type (auto-detected if None)
            metadata: Additional metadata
            title: Entry title (auto-generated if None)

        Returns:
            Dictionary with entry info (paths, timestamp, etc.)
        """
        # Auto-detect source and category if not provided
        if source is None:
            source = self._detect_source()
        if category is None:
            category = self._detect_category(content)

        # Generate timestamp
        timestamp = datetime.now()

        # Get context
        context = self._get_context()
        if metadata:
            context.update(metadata)

        # Generate title if not provided
        if title is None:
            # Extract first line or generate from timestamp
            lines = content.strip().split("\n")
            if lines and lines[0].strip():
                title = lines[0].strip()
                # Remove markdown headers if present
                title = re.sub(r"^#+\s*", "", title)
            else:
                title = f"Entry {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

        # Generate file paths
        by_source_path, by_category_path, by_date_path = self._get_entry_path(
            source, category, timestamp
        )

        # Build entry content
        entry_content = f"""# Devlog Entry

**Timestamp**: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
**Source**: {source}
**Category**: {category}
**Title**: {title}

## Context
{json.dumps(context, indent=2)}

## Content

{content}
"""

        # Write to all three locations (symlinks would be better, but files work)
        by_source_path.write_text(entry_content)
        by_category_path.write_text(entry_content)
        by_date_path.write_text(entry_content)

        # Update index
        entry_info = {
            "timestamp": timestamp.isoformat(),
            "source": source,
            "category": category,
            "title": title,
            "paths": {
                "by_source": str(by_source_path.relative_to(self.project_path)),
                "by_category": str(by_category_path.relative_to(self.project_path)),
                "by_date": str(by_date_path.relative_to(self.project_path)),
            },
        }
        self.index["entries"].append(entry_info)
        self._save_index()

        # Also append to legacy devlog.md for backward compatibility
        self._append_to_legacy_devlog(title, content, timestamp, source, category)

        return entry_info

    def _append_to_legacy_devlog(
        self, title: str, content: str, timestamp: datetime, source: str, category: str
    ):
        """Append entry to legacy devlog.md for backward compatibility."""
        if not self.legacy_devlog.exists():
            self.legacy_devlog.write_text("# Development Log\n\n")

        entry = f"""
## {timestamp.strftime("%Y-%m-%d")} - {title}

**Time**: {timestamp.strftime("%H:%M:%S")}
**Source**: {source}
**Category**: {category}

{content}

---
"""
        # Append to end of file
        with open(self.legacy_devlog, "a", encoding="utf-8") as f:
            f.write(entry)

    def get_recent_entries(
        self,
        limit: int = 5,
        source: str | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get recent devlog entries.

        Args:
            limit: Maximum number of entries to return
            source: Filter by source type
            category: Filter by category

        Returns:
            List of entry dictionaries
        """
        entries = self.index.get("entries", [])

        # Filter by source and category if specified
        if source:
            entries = [e for e in entries if e.get("source") == source]
        if category:
            entries = [e for e in entries if e.get("category") == category]

        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return entries[:limit]

    def migrate_legacy_devlog(self) -> dict[str, Any]:
        """
        Migrate existing devlog.md to new categorized structure.

        Returns:
            Migration summary
        """
        if not self.legacy_devlog.exists():
            return {"migrated": 0, "errors": []}

        content = self.legacy_devlog.read_text()
        entries = []
        errors = []

        # Parse legacy devlog entries (format: ## YYYY-MM-DD - Title)
        pattern = r"##\s+(\d{4}-\d{2}-\d{2})\s+-\s+(.+?)(?=##|\Z)"
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            date_str = match.group(1)
            rest = match.group(2).strip()

            # Extract title (first line)
            lines = rest.split("\n")
            title = lines[0].strip() if lines else "Untitled Entry"

            # Extract content (rest)
            content_text = "\n".join(lines[1:]).strip()

            # Try to parse timestamp from entry
            timestamp = None
            time_match = re.search(r"\*\*Time\*\*:\s*(\d{2}:\d{2}:\d{2})", content_text)
            if time_match:
                try:
                    timestamp = datetime.strptime(
                        f"{date_str} {time_match.group(1)}", "%Y-%m-%d %H:%M:%S"
                    )
                except ValueError:
                    pass

            if timestamp is None:
                timestamp = datetime.strptime(date_str, "%Y-%m-%d")

            # Try to extract source and category from content
            source_match = re.search(r"\*\*Source\*\*:\s*(\w+)", content_text)
            category_match = re.search(r"\*\*Category\*\*:\s*(\w+)", content_text)

            source = source_match.group(1) if source_match else self._detect_category(content_text)
            category = (
                category_match.group(1) if category_match else self._detect_category(content_text)
            )

            # Create entry
            try:
                entry_info = self.write_entry(
                    content=content_text,
                    source=source,
                    category=category,
                    title=title,
                )
                entries.append(entry_info)
            except Exception as e:
                errors.append({"entry": title, "error": str(e)})

        return {
            "migrated": len(entries),
            "errors": errors,
            "entries": entries,
        }
