"""
Scribe: Hand of the Librarian

The Scribe writes records into the Library Realm under the Librarian's direction.
Creates timestamped script files for audit trail.
"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


class Scribe:
    """
    Scribe: Hand of the Librarian

    Writes records into the Library Realm, creating timestamped script files
    for audit trail and record keeping.

    Storage:
    - Scripts: _pantheon/library/scripts/[timestamp]_[description].json
    """

    def __init__(self, scripts_dir: Path):
        """
        Initialize the Scribe.

        Args:
            scripts_dir: Directory where scripts are written
        """
        self.scripts_dir = Path(scripts_dir)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def write_script(
        self, description: str, data: dict[str, Any], script_type: str = "record"
    ) -> Path:
        """
        Write a script (timestamped record file).

        Args:
            description: Description of the script
            data: Data to record
            script_type: Type of script (record, catalog, archive, etc.)

        Returns:
            Path to written script file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create safe filename from description
        safe_desc = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in description)
        safe_desc = safe_desc.replace(" ", "_")[:50]  # Limit length

        filename = f"{timestamp}_{safe_desc}.json"
        script_path = self.scripts_dir / filename

        script_data = {
            "script_type": script_type,
            "description": description,
            "timestamp": timestamp,
            "iso_timestamp": datetime.now().isoformat(),
            "data": data,
        }

        script_path.write_text(json.dumps(script_data, indent=2), encoding="utf-8")

        return script_path

    def write_catalog_script(self, action: str, count: int, source: str) -> Path:
        """Write a cataloging script."""
        return self.write_script(
            f"Cataloged {count} records from {source}",
            {"action": action, "count": count, "source": source},
            script_type="catalog",
        )

    def write_record_script(
        self, record_type: str, record_id: str, metadata: dict[str, Any]
    ) -> Path:
        """Write a record script."""
        return self.write_script(
            f"Recorded {record_type}: {record_id}",
            {"record_type": record_type, "record_id": record_id, "metadata": metadata},
            script_type="record",
        )

    def write_daily_learning_report(
        self, organized_data: dict[str, Any], report_date: date, output_dir: Path
    ) -> Path:
        """
        Generates the Typst string and compiles it to PDF.

        Takes organized data from The Librarian and creates a beautiful PDF report.

        Args:
            organized_data: Organized data structure from Librarian.organize_daily_learning()
            report_date: Date for the report
            output_dir: Directory to save the PDF report

        Returns:
            Path to generated PDF report
        """
        from ...templates.typst.compiler import TypstCompiler

        filename = f"{report_date.isoformat()}_learning_report.pdf"
        output_pdf = output_dir / filename

        # Generate Typst content string
        typst_content = self._generate_typst_source(organized_data, report_date)

        # Compile using TypstCompiler (takes string, not template path)
        compiler = TypstCompiler()
        compiler.compile(
            typst_content=typst_content,
            output_path=output_pdf,
            working_dir=None,  # Use temp directory
        )

        return output_pdf

    def _generate_typst_source(self, data: dict[str, Any], report_date: date) -> str:
        """
        Constructs the Typst source code string from the organized data.

        Args:
            data: Organized data from Librarian
            report_date: Date for the report

        Returns:
            Typst source code as string
        """
        date_str = report_date.strftime("%B %d, %Y")

        # Extract sections
        learning = data.get("learning", {})
        doing = data.get("doing", {})
        activity = data.get("activity", {})
        meta = data.get("meta", {})

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
        findings = learning.get("findings", [])
        if findings:
            typst += "=== Findings\n\n"
            for i, finding in enumerate(findings[-20:], 1):  # Last 20 findings
                finding_text = (
                    finding if isinstance(finding, str) else finding.get("finding", str(finding))
                )
                impact = finding.get("impact", 0.5) if isinstance(finding, dict) else 0.5
                typst += f"{i}. {finding_text} (impact: {impact:.2f})\n\n"
        else:
            typst += "=== Findings\n\n*No findings recorded today.*\n\n"

        # Unknowns section
        unknowns = learning.get("unknowns", [])
        if unknowns:
            typst += "=== Knowledge Gaps\n\n"
            for i, unknown in enumerate(unknowns[-10:], 1):  # Last 10 unknowns
                unknown_text = (
                    unknown if isinstance(unknown, str) else unknown.get("unknown", str(unknown))
                )
                typst += f"{i}. {unknown_text}\n\n"
        else:
            typst += "=== Knowledge Gaps\n\n*No unknowns recorded today.*\n\n"

        # Epistemic state
        epistemic_state = learning.get("epistemic_state", {})
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
        file_changes = doing.get("file_changes", {})
        if file_changes:
            typst += "=== File Activity\n\n"
            typst += f"*Created:* {file_changes.get('created', 0)} files\n"
            typst += f"*Modified:* {file_changes.get('modified', 0)} files\n"
            typst += f"*Deleted:* {file_changes.get('deleted', 0)} files\n"
            typst += f"*Total changes:* {file_changes.get('total', 0)} events\n\n"

        # Git activity
        git_activity = doing.get("git_activity", {})
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
        work_efforts = doing.get("work_efforts", {})
        if work_efforts:
            typst += "\n=== Work Efforts\n\n"
            typst += f"*Created:* {work_efforts.get('created', 0)} work efforts\n"
            typst += f"*Updated:* {work_efforts.get('updated', 0)} work efforts\n\n"

        # Session metrics
        typst += "== Activity Metrics\n\n"
        session_count = activity.get("session_count", 0)
        total_time = activity.get("total_time_minutes", 0)
        typst += f"*Sessions:* {session_count}\n"
        typst += f"*Total time:* {total_time} minutes\n\n"

        # Code metrics
        code_metrics = activity.get("code", {})
        if code_metrics:
            typst += "=== Code Metrics\n\n"
            typst += f"*Lines written:* {code_metrics.get('lines_written', 0)}\n"
            typst += f"*Lines modified:* {code_metrics.get('lines_modified', 0)}\n"
            typst += f"*Lines deleted:* {code_metrics.get('lines_deleted', 0)}\n"
            typst += f"*Net lines:* {code_metrics.get('net_lines', 0)}\n\n"

        # Top commands
        commands = activity.get("commands", {})
        if commands:
            top_commands = commands.get("top_commands", [])
            if top_commands:
                typst += "=== Top Commands\n\n"
                for cmd_info in top_commands:
                    cmd = cmd_info.get("command", "unknown")
                    count = cmd_info.get("count", 0)
                    typst += f"*{cmd}:* {count} times\n"

        typst += "\n---\n\n"
        typst += f"#text(fill: gray, size: 9pt)[Generated by The Scribe for The Packrat]"

        return typst
