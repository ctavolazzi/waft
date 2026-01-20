#!/usr/bin/env python3
"""
Prior Efforts Tracker - Track evolution attempts and prior efforts for work efforts.

Simple tool to log and track attempts, iterations, and prior efforts
that Beings can use to learn from history.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class PriorEffortsTracker:
    """
    Track prior efforts, iterations, and evolution attempts.

    Simple JSON-based tracking for work effort evolution history.
    """

    def __init__(self, work_effort_path: Path):
        """
        Initialize tracker.

        Args:
            work_effort_path: Path to work effort directory
        """
        self.work_effort_path = Path(work_effort_path)
        self.tools_dir = self.work_effort_path / "tools"
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.efforts_file = self.tools_dir / "prior_efforts.json"
        self._efforts: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Load prior efforts from disk."""
        if self.efforts_file.exists():
            try:
                with open(self.efforts_file) as f:
                    self._efforts = json.load(f)
            except (OSError, json.JSONDecodeError):
                self._efforts = []
        else:
            self._efforts = []

    def _save(self) -> None:
        """Save prior efforts to disk."""
        try:
            with open(self.efforts_file, "w") as f:
                json.dump(self._efforts, f, indent=2)
        except OSError:
            pass  # Graceful degradation

    def log_attempt(
        self,
        attempt_id: str,
        description: str,
        approach: str,
        status: str = "attempted",
        outcome: str | None = None,
        lessons_learned: list[str] | None = None,
        files_created: list[str] | None = None,
        files_modified: list[str] | None = None,
        errors_encountered: list[str] | None = None,
        being_id: str | None = None,
        generation: int | None = None,
    ) -> None:
        """
        Log a prior effort/attempt.

        Args:
            attempt_id: Unique identifier for this attempt
            description: What was attempted
            approach: How it was attempted
            status: attempted | succeeded | failed | partial
            outcome: What happened
            lessons_learned: What was learned from this attempt
            files_created: Files created during attempt
            files_modified: Files modified during attempt
            errors_encountered: Errors or issues encountered
            being_id: ID of Being that made this attempt
            generation: Generation number if part of evolution
        """
        effort = {
            "attempt_id": attempt_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "approach": approach,
            "status": status,
            "outcome": outcome,
            "lessons_learned": lessons_learned or [],
            "files_created": files_created or [],
            "files_modified": files_modified or [],
            "errors_encountered": errors_encountered or [],
            "being_id": being_id,
            "generation": generation,
        }

        self._efforts.append(effort)
        self._save()

    def get_prior_efforts(
        self,
        status: str | None = None,
        being_id: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get prior efforts, optionally filtered.

        Args:
            status: Filter by status (attempted | succeeded | failed | partial)
            being_id: Filter by being_id
            limit: Limit number of results

        Returns:
            List of effort dictionaries
        """
        efforts = self._efforts

        if status:
            efforts = [e for e in efforts if e.get("status") == status]

        if being_id:
            efforts = [e for e in efforts if e.get("being_id") == being_id]

        # Sort by timestamp (newest first)
        efforts = sorted(efforts, key=lambda x: x.get("timestamp", ""), reverse=True)

        if limit:
            efforts = efforts[:limit]

        return efforts

    def get_lessons_learned(self) -> list[str]:
        """Get all lessons learned from prior efforts."""
        lessons = []
        for effort in self._efforts:
            lessons.extend(effort.get("lessons_learned", []))
        return list(set(lessons))  # Unique lessons

    def get_common_errors(self) -> list[str]:
        """Get common errors encountered."""
        errors = []
        for effort in self._efforts:
            errors.extend(effort.get("errors_encountered", []))

        # Count frequency
        from collections import Counter

        error_counts = Counter(errors)
        return [error for error, count in error_counts.most_common(10)]

    def get_statistics(self) -> dict[str, Any]:
        """Get statistics about prior efforts."""
        total = len(self._efforts)
        if total == 0:
            return {
                "total_attempts": 0,
                "succeeded": 0,
                "failed": 0,
                "partial": 0,
                "unique_beings": 0,
                "total_lessons": 0,
                "total_errors": 0,
            }

        status_counts = {}
        being_ids = set()
        total_lessons = 0
        total_errors = 0

        for effort in self._efforts:
            status = effort.get("status", "attempted")
            status_counts[status] = status_counts.get(status, 0) + 1

            if effort.get("being_id"):
                being_ids.add(effort["being_id"])

            total_lessons += len(effort.get("lessons_learned", []))
            total_errors += len(effort.get("errors_encountered", []))

        success_rate = (status_counts.get("succeeded", 0) / total * 100) if total > 0 else 0

        return {
            "total_attempts": total,
            "succeeded": status_counts.get("succeeded", 0),
            "failed": status_counts.get("failed", 0),
            "partial": status_counts.get("partial", 0),
            "attempted": status_counts.get("attempted", 0),
            "unique_beings": len(being_ids),
            "total_lessons": total_lessons,
            "total_errors": total_errors,
            "success_rate": success_rate,
        }

    def export_markdown(self, output_path: Path | None = None) -> str:
        """
        Export prior efforts as markdown report.

        Args:
            output_path: Optional path to save markdown file

        Returns:
            Markdown string
        """
        stats = self.get_statistics()
        efforts = self.get_prior_efforts()
        lessons = self.get_lessons_learned()
        common_errors = self.get_common_errors()

        md = f"""# Prior Efforts Report

**Generated**: {datetime.now().isoformat()}
**Work Effort**: {self.work_effort_path.name}

## Statistics

- **Total Attempts**: {stats["total_attempts"]}
- **Succeeded**: {stats["succeeded"]}
- **Failed**: {stats["failed"]}
- **Partial**: {stats["partial"]}
- **Success Rate**: {stats["success_rate"]:.1f}%
- **Unique Beings**: {stats["unique_beings"]}
- **Total Lessons Learned**: {stats["total_lessons"]}
- **Total Errors Encountered**: {stats["total_errors"]}

## Lessons Learned

"""

        for lesson in lessons:
            md += f"- {lesson}\n"

        md += "\n## Common Errors\n\n"
        for error in common_errors:
            md += f"- {error}\n"

        md += "\n## Prior Efforts\n\n"

        for effort in efforts:
            md += f"### {effort['attempt_id']} - {effort['description']}\n\n"
            md += f"**Status**: {effort['status']}\n"
            md += f"**Timestamp**: {effort['timestamp']}\n"
            md += f"**Approach**: {effort['approach']}\n"

            if effort.get("outcome"):
                md += f"**Outcome**: {effort['outcome']}\n"

            if effort.get("being_id"):
                md += f"**Being ID**: {effort['being_id']}\n"

            if effort.get("generation"):
                md += f"**Generation**: {effort['generation']}\n"

            if effort.get("lessons_learned"):
                md += "\n**Lessons Learned**:\n"
                for lesson in effort["lessons_learned"]:
                    md += f"- {lesson}\n"

            if effort.get("errors_encountered"):
                md += "\n**Errors**:\n"
                for error in effort["errors_encountered"]:
                    md += f"- {error}\n"

            if effort.get("files_created"):
                md += f"\n**Files Created**: {', '.join(effort['files_created'])}\n"

            if effort.get("files_modified"):
                md += f"\n**Files Modified**: {', '.join(effort['files_modified'])}\n"

            md += "\n---\n\n"

        if output_path:
            with open(output_path, "w") as f:
                f.write(md)

        return md


def main():
    """CLI interface for prior efforts tracker."""
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Usage: prior_efforts_tracker.py <work_effort_path> [command]")
        print("\nCommands:")
        print("  list - List all prior efforts")
        print("  stats - Show statistics")
        print("  lessons - Show lessons learned")
        print("  errors - Show common errors")
        print("  export - Export markdown report")
        sys.exit(1)

    work_effort_path = Path(sys.argv[1])
    tracker = PriorEffortsTracker(work_effort_path)

    command = sys.argv[2] if len(sys.argv) > 2 else "list"

    if command == "list":
        efforts = tracker.get_prior_efforts()
        print(f"\nPrior Efforts ({len(efforts)} total):\n")
        for effort in efforts:
            print(f"  {effort['attempt_id']}: {effort['description']} [{effort['status']}]")

    elif command == "stats":
        stats = tracker.get_statistics()
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    elif command == "lessons":
        lessons = tracker.get_lessons_learned()
        print(f"\nLessons Learned ({len(lessons)} total):\n")
        for lesson in lessons:
            print(f"  - {lesson}")

    elif command == "errors":
        errors = tracker.get_common_errors()
        print("\nCommon Errors:\n")
        for error in errors:
            print(f"  - {error}")

    elif command == "export":
        output_path = work_effort_path / "tools" / "prior_efforts_report.md"
        tracker.export_markdown(output_path)
        print(f"\nExported to: {output_path}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
