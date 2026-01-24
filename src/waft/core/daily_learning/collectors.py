"""
Data Collectors for Daily Learning Report.

Collects data from Empirica, TheChronicler, and SessionAnalytics.
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any

from ...core.empirica import EmpiricaManager
from ...core.chronicler.storage import ObservationStorage
from ...core.session_analytics import SessionAnalytics

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Base class for data collectors."""

    @abstractmethod
    def collect(self, target_date: date | None = None) -> dict[str, Any]:
        """
        Collects data for the specified date.

        Args:
            target_date: Date to collect data for (defaults to today)

        Returns:
            Dictionary of collected data
        """
        pass


class EmpiricaCollector(BaseCollector):
    """Collects findings, unknowns, and epistemic state from Empirica."""

    def __init__(self, project_path: Path):
        """
        Initialize Empirica collector.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.empirica = EmpiricaManager(self.project_path)

    def collect(self, target_date: date | None = None) -> dict[str, Any]:
        """
        Collect Empirica data for the target date.

        Args:
            target_date: Date to collect data for (defaults to today)

        Returns:
            Dictionary with findings, unknowns, and epistemic state
        """
        if target_date is None:
            target_date = date.today()

        logger.info(f"Collecting Empirica data for {target_date}...")

        try:
            # Get project bootstrap context (contains findings/unknowns)
            context = self.empirica.project_bootstrap()
            if not context:
                logger.warning("No Empirica context available")
                return {"findings": [], "unknowns": [], "epistemic_state": {}}

            # Extract findings and unknowns
            all_findings = context.get("findings", [])
            all_unknowns = context.get("unknowns", [])

            # Filter by date if findings/unknowns have timestamps
            # Note: Empirica findings/unknowns may not have dates, so we'll take recent ones
            findings = all_findings[-50:] if len(all_findings) > 50 else all_findings
            unknowns = all_unknowns[-50:] if len(all_unknowns) > 50 else all_unknowns

            # Get epistemic state summary
            epistemic_state = {
                "phase": context.get("phase", "UNKNOWN"),
                "findings_count": len(findings),
                "unknowns_count": len(unknowns),
            }

            # Try to get more detailed epistemic vectors if available
            if "vectors" in context:
                epistemic_state["vectors"] = context["vectors"]

            return {
                "findings": findings,
                "unknowns": unknowns,
                "epistemic_state": epistemic_state,
            }

        except Exception as e:
            logger.warning(f"Failed to collect Empirica data: {e}")
            return {"findings": [], "unknowns": [], "epistemic_state": {}}


class ChroniclerCollector(BaseCollector):
    """Collects file changes, git activity, and work effort observations from TheChronicler."""

    def __init__(self, project_path: Path):
        """
        Initialize Chronicler collector.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.storage = ObservationStorage(self.project_path)

    def collect(self, target_date: date | None = None) -> dict[str, Any]:
        """
        Collect Chronicler observations for the target date.

        Args:
            target_date: Date to collect data for (defaults to today)

        Returns:
            Dictionary with file changes, git activity, and work effort data
        """
        if target_date is None:
            target_date = date.today()

        logger.info(f"Collecting Chronicler observations for {target_date}...")

        try:
            # Get start and end of day
            start_date = datetime.combine(target_date, datetime.min.time())
            end_date = datetime.combine(target_date, datetime.max.time())

            # Get all observations for the day
            observations = self.storage.get_observations(start_date, end_date)

            # Categorize observations
            genesis = [obs for obs in observations if obs.get("event_type") == "genesis"]
            exodus = [obs for obs in observations if obs.get("event_type") == "exodus"]
            mutations = [obs for obs in observations if obs.get("event_type") == "mutation"]

            # Group by observer type
            file_observations = [
                obs for obs in observations if obs.get("observer") == "filesystem"
            ]
            git_observations = [obs for obs in observations if obs.get("observer") == "git"]
            work_effort_observations = [
                obs for obs in observations if obs.get("observer") == "work_effort"
            ]

            # Extract git commit details
            git_commits = []
            for obs in git_observations:
                if obs.get("event_type") == "mutation":  # Commits are mutations
                    git_commits.append(
                        {
                            "message": obs.get("payload", {}).get("message", ""),
                            "timestamp": obs.get("timestamp", ""),
                        }
                    )

            return {
                "file_changes": {
                    "created": len(genesis),
                    "deleted": len(exodus),
                    "modified": len(mutations),
                    "total": len(observations),
                },
                "git_activity": {
                    "commits": len(git_commits),
                    "commit_details": git_commits,
                },
                "work_efforts": {
                    "created": len([obs for obs in work_effort_observations if obs.get("event_type") == "genesis"]),
                    "updated": len([obs for obs in work_effort_observations if obs.get("event_type") == "mutation"]),
                },
            }

        except Exception as e:
            logger.warning(f"Failed to collect Chronicler data: {e}")
            return {
                "file_changes": {"created": 0, "deleted": 0, "modified": 0, "total": 0},
                "git_activity": {"commits": 0, "commit_details": []},
                "work_efforts": {"created": 0, "updated": 0},
            }


class SessionAnalyticsCollector(BaseCollector):
    """Collects session metrics from SessionAnalytics."""

    def __init__(self, project_path: Path):
        """
        Initialize SessionAnalytics collector.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.analytics = SessionAnalytics(self.project_path)

    def collect(self, target_date: date | None = None) -> dict[str, Any]:
        """
        Collect SessionAnalytics data for the target date.

        Args:
            target_date: Date to collect data for (defaults to today)

        Returns:
            Dictionary with session metrics
        """
        if target_date is None:
            target_date = date.today()

        logger.info(f"Collecting SessionAnalytics data for {target_date}...")

        try:
            # Get start and end of day
            start_date = datetime.combine(target_date, datetime.min.time())
            end_date = datetime.combine(target_date, datetime.max.time())

            # Get sessions for the day
            sessions = self.analytics.get_sessions(start_date=start_date, end_date=end_date)

            # Aggregate metrics
            total_time = sum(
                s.duration_seconds for s in sessions if s.duration_seconds is not None
            )
            total_files_created = sum(s.files_created for s in sessions)
            total_files_modified = sum(s.files_modified for s in sessions)
            total_files_deleted = sum(s.files_deleted for s in sessions)
            total_lines_written = sum(s.lines_written for s in sessions)
            total_lines_modified = sum(s.lines_modified for s in sessions)
            total_lines_deleted = sum(s.lines_deleted for s in sessions)

            # Collect all commands
            all_commands = []
            for session in sessions:
                if session.commands_executed:
                    all_commands.extend(session.commands_executed)

            # Get top commands (simple frequency count)
            command_counts: dict[str, int] = {}
            for cmd in all_commands:
                # Extract base command (first word)
                base_cmd = cmd.split()[0] if cmd else "unknown"
                command_counts[base_cmd] = command_counts.get(base_cmd, 0) + 1

            top_commands = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:10]

            return {
                "session_count": len(sessions),
                "total_time_minutes": int(total_time / 60) if total_time else 0,
                "files": {
                    "created": total_files_created,
                    "modified": total_files_modified,
                    "deleted": total_files_deleted,
                },
                "code": {
                    "lines_written": total_lines_written,
                    "lines_modified": total_lines_modified,
                    "lines_deleted": total_lines_deleted,
                    "net_lines": total_lines_written - total_lines_deleted,
                },
                "commands": {
                    "total_executed": len(all_commands),
                    "top_commands": [{"command": cmd, "count": count} for cmd, count in top_commands],
                },
            }

        except Exception as e:
            logger.warning(f"Failed to collect SessionAnalytics data: {e}")
            return {
                "session_count": 0,
                "total_time_minutes": 0,
                "files": {"created": 0, "modified": 0, "deleted": 0},
                "code": {"lines_written": 0, "lines_modified": 0, "lines_deleted": 0, "net_lines": 0},
                "commands": {"total_executed": 0, "top_commands": []},
            }
