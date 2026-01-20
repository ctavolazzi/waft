"""
Reports: Report generation for TheChronicler.

Generates hourly and daily reports on system activity.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ...brief import BriefDocument
from .storage import ObservationStorage


class ReportGenerator:
    """Generates hourly and daily reports from observations."""

    def __init__(self, storage: ObservationStorage, project_path: Path):
        """
        Initialize report generator.

        Args:
            storage: ObservationStorage instance
            project_path: Project root path
        """
        self.storage = storage
        self.project_path = project_path
        self.reports_dir = project_path / "_sentinel" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_hourly_report(self, hour: int | None = None, date: datetime | None = None) -> Path:
        """
        Generate hourly report for a specific hour.

        Args:
            hour: Hour (0-23), defaults to current hour
            date: Date, defaults to today

        Returns:
            Path to generated report
        """
        if date is None:
            date = datetime.now()
        if hour is None:
            hour = date.hour

        # Get observations for this hour
        start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=1) - timedelta(microseconds=1)

        observations = self.storage.get_observations(start, end)

        # Categorize observations
        genesis = [o for o in observations if o.get("event_type") == "genesis"]
        exodus = [o for o in observations if o.get("event_type") == "exodus"]
        mutations = [o for o in observations if o.get("event_type") == "mutation"]

        # Group by observer
        by_observer: dict[str, list[dict[str, Any]]] = {}
        for obs in observations:
            observer = obs.get("observer", "unknown")
            if observer not in by_observer:
                by_observer[observer] = []
            by_observer[observer].append(obs)

        # Generate report content
        report_time = start.strftime("%Y-%m-%d %H:00")
        title = f"Hourly Report - {report_time}"

        brief = BriefDocument(
            title=title,
            subtitle=f"Hour {hour:02d}:00 - {hour + 1:02d}:00",
            doc_id=f"HR-{start.strftime('%Y%m%d%H')}",
            include_system_status=False,
        )

        # Summary section
        brief.add_section_header("Summary", level=2)
        brief.add_text(
            f"This report covers activity from {start.strftime('%H:%M')} to "
            f"{(start + timedelta(hours=1)).strftime('%H:%M')} on {start.strftime('%B %d, %Y')}."
        )

        brief.add_table(
            ["Metric", "Count"],
            [
                ["Genesis Events (Created)", str(len(genesis))],
                ["Exodus Events (Deleted)", str(len(exodus))],
                ["Mutations (Modified)", str(len(mutations))],
                ["Total Observations", str(len(observations))],
            ],
        )

        # Genesis section
        if genesis:
            brief.add_section_header("Genesis - New Creations", level=2)
            genesis_by_observer = {}
            for obs in genesis:
                observer = obs.get("observer", "unknown")
                if observer not in genesis_by_observer:
                    genesis_by_observer[observer] = []
                genesis_by_observer[observer].append(obs)

            for observer, obs_list in genesis_by_observer.items():
                brief.add_section_header(f"{observer.title()} - {len(obs_list)} creations", level=3)
                for obs in obs_list[:20]:  # Limit to 20 per observer
                    path = obs.get("path", "unknown")
                    brief.add_text(f"• {path}")
                if len(obs_list) > 20:
                    brief.add_text(f"... and {len(obs_list) - 20} more")

        # Exodus section
        if exodus:
            brief.add_section_header("Exodus - Deletions", level=2)
            exodus_by_observer = {}
            for obs in exodus:
                observer = obs.get("observer", "unknown")
                if observer not in exodus_by_observer:
                    exodus_by_observer[observer] = []
                exodus_by_observer[observer].append(obs)

            for observer, obs_list in exodus_by_observer.items():
                brief.add_section_header(f"{observer.title()} - {len(obs_list)} deletions", level=3)
                for obs in obs_list[:20]:
                    path = obs.get("path", "unknown")
                    brief.add_text(f"• {path}")
                if len(obs_list) > 20:
                    brief.add_text(f"... and {len(obs_list) - 20} more")

        # Mutations section
        if mutations:
            brief.add_section_header("Mutations - Modifications", level=2)
            brief.add_text(f"{len(mutations)} files or components were modified during this hour.")

        # Generate PDF
        report_path = self.reports_dir / f"hourly_{start.strftime('%Y%m%d_%H00')}.pdf"
        return brief.generate(output_path=report_path)

    def generate_daily_report(self, date: datetime | None = None) -> Path:
        """
        Generate daily report for a specific date.

        Args:
            date: Date, defaults to today

        Returns:
            Path to generated report
        """
        if date is None:
            date = datetime.now()

        # Get observations for entire day
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        observations = self.storage.get_observations(start, end)

        # Categorize
        genesis = [o for o in observations if o.get("event_type") == "genesis"]
        exodus = [o for o in observations if o.get("event_type") == "exodus"]
        mutations = [o for o in observations if o.get("event_type") == "mutation"]

        # Hourly breakdown
        hourly_breakdown: dict[int, dict[str, int]] = {}
        for obs in observations:
            try:
                obs_time = datetime.fromisoformat(obs["timestamp"])
                hour = obs_time.hour
                if hour not in hourly_breakdown:
                    hourly_breakdown[hour] = {"genesis": 0, "exodus": 0, "mutation": 0}
                event_type = obs.get("event_type", "unknown")
                if event_type in hourly_breakdown[hour]:
                    hourly_breakdown[hour][event_type] += 1
            except (KeyError, ValueError):
                continue

        # Generate report
        title = f"Daily Report - {date.strftime('%B %d, %Y')}"
        brief = BriefDocument(
            title=title,
            subtitle="24-Hour Activity Summary",
            doc_id=f"DR-{date.strftime('%Y%m%d')}",
            cover_header="TELEPORT MASSIVE",
            cover_metadata={
                "OPERATIONAL MANUAL": "09-14",
                "CODENAME": "W.A.F.T.",
                "PROTOCOL": "CHRONICLER MONITORING",
            },
            cover_warning={
                "message": "RESTRICTED ACCESS. This report contains system activity data.",
                "severity": "CAUTION",
            },
            cover_signature={
                "role": "GENERATED BY",
                "name": "TheChronicler Monitoring System",
                "date": date.strftime("%Y-%m-%d"),
            },
            include_system_status=False,
        )

        # Executive summary
        brief.add_section_header("Executive Summary", level=2)
        brief.add_text(
            f"This report summarizes all system activity from {start.strftime('%B %d, %Y')} "
            f"00:00:00 to 23:59:59. The system observed {len(observations)} total events "
            f"across {len({o.get('observer', 'unknown') for o in observations})} observation sources."
        )

        brief.add_table(
            ["Metric", "Count"],
            [
                ["Genesis Events (Created)", str(len(genesis))],
                ["Exodus Events (Deleted)", str(len(exodus))],
                ["Mutations (Modified)", str(len(mutations))],
                ["Total Observations", str(len(observations))],
                ["Net Change", str(len(genesis) - len(exodus))],
            ],
        )

        # Hourly breakdown
        if hourly_breakdown:
            brief.add_section_header("Hourly Activity Breakdown", level=2)
            rows = [["Hour", "Genesis", "Exodus", "Mutations", "Total"]]
            for hour in sorted(hourly_breakdown.keys()):
                data = hourly_breakdown[hour]
                total = sum(data.values())
                rows.append(
                    [
                        f"{hour:02d}:00",
                        str(data["genesis"]),
                        str(data["exodus"]),
                        str(data["mutation"]),
                        str(total),
                    ]
                )
            brief.add_table(rows[0], rows[1:])

        # Top events by observer
        brief.add_section_header("Activity by Observer", level=2)
        by_observer: dict[str, dict[str, int]] = {}
        for obs in observations:
            observer = obs.get("observer", "unknown")
            if observer not in by_observer:
                by_observer[observer] = {"genesis": 0, "exodus": 0, "mutation": 0}
            event_type = obs.get("event_type", "unknown")
            if event_type in by_observer[observer]:
                by_observer[observer][event_type] += 1

        if by_observer:
            rows = [["Observer", "Genesis", "Exodus", "Mutations", "Total"]]
            for observer, counts in sorted(
                by_observer.items(), key=lambda x: sum(x[1].values()), reverse=True
            ):
                total = sum(counts.values())
                rows.append(
                    [
                        observer.title(),
                        str(counts["genesis"]),
                        str(counts["exodus"]),
                        str(counts["mutation"]),
                        str(total),
                    ]
                )
            brief.add_table(rows[0], rows[1:])

        # Generate PDF
        report_path = self.reports_dir / f"daily_{date.strftime('%Y%m%d')}.pdf"
        return brief.generate(output_path=report_path)
