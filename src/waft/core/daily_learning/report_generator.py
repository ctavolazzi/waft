"""
Report Generator for Daily Learning Reports.

Generates Typst PDF reports from collected data.
"""
import json
import logging
from datetime import date
from pathlib import Path
from typing import Any

from ...templates.typst.compiler import TypstCompiler

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates daily learning reports as Typst PDFs."""

    def __init__(self, project_path: Path, output_dir: str | Path = "_pyrite/daily_reports"):
        """
        Initialize report generator.

        Args:
            project_path: Path to project root
            output_dir: Directory to save reports (relative to project_path)
        """
        self.project_path = Path(project_path)
        self.output_dir = self.project_path / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.compiler = TypstCompiler()

    def generate(self, data: dict[str, Any], target_date: date | None = None) -> Path | None:
        """
        Generate PDF report from collected data.

        Args:
            data: Aggregated data from all collectors
            target_date: Date for the report (defaults to today)

        Returns:
            Path to generated PDF, or None if generation failed
        """
        if target_date is None:
            target_date = date.today()

        today_str = target_date.isoformat()
        output_pdf = self.output_dir / f"{today_str}_learning_report.pdf"

        logger.info(f"Generating report for {today_str}...")

        # Generate Typst content
        typst_content = self._generate_typst_content(data, target_date)

        try:
            # Compile Typst to PDF
            self.compiler.compile(
                typst_content=typst_content,
                output_path=output_pdf,
                working_dir=None,  # Use temp directory
            )

            logger.info(f"Report generated successfully: {output_pdf}")
            return output_pdf

        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            # Save raw data as JSON backup
            json_backup = self.output_dir / f"{today_str}_data_backup.json"
            with open(json_backup, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved data backup to: {json_backup}")
            return None

    def _generate_typst_content(self, data: dict[str, Any], target_date: date) -> str:
        """
        Generate Typst source code from data.

        Args:
            data: Aggregated data from collectors
            target_date: Date for the report

        Returns:
            Typst source code as string
        """
        # Format date nicely
        date_str = target_date.strftime("%B %d, %Y")

        # Extract data from collectors
        empirica_data = data.get("EmpiricaCollector", {})
        chronicler_data = data.get("ChroniclerCollector", {})
        session_data = data.get("SessionAnalyticsCollector", {})

        # Build Typst content with WAFT border for identification
        typst = f"""#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// WAFT template border for identification
#show: s6t5-page-bordering.with(
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

#set text(font: "Times New Roman", size: 11pt)
#set heading(numbering: "1.")

= Daily Learning Report
#text(fill: gray)[{date_str}]

== What I Learned

"""
        # Findings section
        findings = empirica_data.get("findings", [])
        if findings:
            typst += "=== Findings\n\n"
            for i, finding in enumerate(findings[-20:], 1):  # Last 20 findings
                finding_text = finding if isinstance(finding, str) else finding.get("finding", str(finding))
                impact = finding.get("impact", 0.5) if isinstance(finding, dict) else 0.5
                typst += f"{i}. {finding_text} (impact: {impact:.2f})\n\n"
        else:
            typst += "=== Findings\n\n*No findings recorded today.*\n\n"

        # Unknowns section
        unknowns = empirica_data.get("unknowns", [])
        if unknowns:
            typst += "=== Knowledge Gaps\n\n"
            for i, unknown in enumerate(unknowns[-10:], 1):  # Last 10 unknowns
                unknown_text = unknown if isinstance(unknown, str) else unknown.get("unknown", str(unknown))
                typst += f"{i}. {unknown_text}\n\n"
        else:
            typst += "=== Knowledge Gaps\n\n*No unknowns recorded today.*\n\n"

        # Epistemic state
        epistemic_state = empirica_data.get("epistemic_state", {})
        if epistemic_state:
            typst += "=== Epistemic State\n\n"
            phase = epistemic_state.get("phase", "UNKNOWN")
            findings_count = epistemic_state.get("findings_count", 0)
            unknowns_count = epistemic_state.get("unknowns_count", 0)
            typst += f"*Phase:* {phase}\n"
            typst += f"*Findings:* {findings_count}\n"
            typst += f"*Unknowns:* {unknowns_count}\n\n"

        typst += "== What I Did\n\n"

        # File activity
        file_changes = chronicler_data.get("file_changes", {})
        if file_changes:
            typst += "=== File Activity\n\n"
            typst += f"*Created:* {file_changes.get('created', 0)} files\n"
            typst += f"*Modified:* {file_changes.get('modified', 0)} files\n"
            typst += f"*Deleted:* {file_changes.get('deleted', 0)} files\n"
            typst += f"*Total changes:* {file_changes.get('total', 0)} events\n\n"

        # Git activity
        git_activity = chronicler_data.get("git_activity", {})
        if git_activity:
            typst += "=== Git Activity\n\n"
            commits = git_activity.get("commits", 0)
            typst += f"*Commits:* {commits}\n\n"
            commit_details = git_activity.get("commit_details", [])
            if commit_details:
                typst += "*Recent commits:*\n\n"
                for commit in commit_details[-5:]:  # Last 5 commits
                    message = commit.get("message", "No message")
                    timestamp = commit.get("timestamp", "")
                    typst += f"- {message}\n"
                    if timestamp:
                        typst += f"  #text(fill: gray)[{timestamp}]\n"

        # Work efforts
        work_efforts = chronicler_data.get("work_efforts", {})
        if work_efforts:
            typst += "\n=== Work Efforts\n\n"
            typst += f"*Created:* {work_efforts.get('created', 0)} work efforts\n"
            typst += f"*Updated:* {work_efforts.get('updated', 0)} work efforts\n\n"

        # Session metrics
        typst += "== Activity Metrics\n\n"
        session_count = session_data.get("session_count", 0)
        total_time = session_data.get("total_time_minutes", 0)
        typst += f"*Sessions:* {session_count}\n"
        typst += f"*Total time:* {total_time} minutes\n\n"

        # Code metrics
        code_metrics = session_data.get("code", {})
        if code_metrics:
            typst += "=== Code Metrics\n\n"
            typst += f"*Lines written:* {code_metrics.get('lines_written', 0)}\n"
            typst += f"*Lines modified:* {code_metrics.get('lines_modified', 0)}\n"
            typst += f"*Lines deleted:* {code_metrics.get('lines_deleted', 0)}\n"
            typst += f"*Net lines:* {code_metrics.get('net_lines', 0)}\n\n"

        # Top commands
        commands = session_data.get("commands", {})
        if commands:
            top_commands = commands.get("top_commands", [])
            if top_commands:
                typst += "=== Top Commands\n\n"
                for cmd_info in top_commands:
                    cmd = cmd_info.get("command", "unknown")
                    count = cmd_info.get("count", 0)
                    typst += f"*{cmd}:* {count} times\n"

        typst += "\n---\n\n"
        typst += f"#text(fill: gray, size: 9pt)[Generated by Waft Daily Learning Server]"

        return typst
