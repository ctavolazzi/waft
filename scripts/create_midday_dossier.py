#!/usr/bin/env python3
"""
Midday Dossier Creator
=======================

Creates a comprehensive midday status dossier with current system state,
work progress, and afternoon planning.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument

# ============================================================================
# Configuration Constants & Lookup Tables
# ============================================================================

# Status values lookup
WORK_EFFORT_STATUS = {
    "active": ["active", "in_progress"],
    "completed": ["completed"],
    "paused": ["paused"],
    "open": ["open"],
}

# File limits
FILE_LIMITS = {
    "git_files_display": 20,
    "git_files_list": 15,
    "work_efforts_display": 10,
    "morning_progress_items": 10,
    "morning_progress_lines": 15,
    "file_line_length": 80,
}

# Cover page configuration
COVER_CONFIG = {
    "header": "TELEPORT MASSIVE",
    "operational_manual": "09-14",
    "codename": "W.A.F.T.",
    "classification": "INTERNAL",
    "signature_role": "AUTHORIZED BY",
    "signature_name": "Site-Delta-9",
    "footer": "MIDDAY DOSSIER - INTERNAL USE ONLY",
}

# Report type configuration
REPORT_CONFIG = {
    "type": "MIDDAY DOSSIER",
    "title_prefix": "Midday Dossier",
    "subtitle_prefix": "Midday Status Report",
    "doc_id_prefix": "DOSSIER",
    "warning_severity": "INFO",
}

# Section titles
SECTION_TITLES = {
    "current_status": "Current System Status",
    "morning_progress": "Morning Progress",
    "active_work": "Active Work Efforts",
    "afternoon_planning": "Afternoon Planning",
    "recent_changes": "Recent File Changes",
}

# Note box titles
NOTE_TITLES = {
    "morning_accomplishments": "Morning Accomplishments",
    "current_work": "Current Work",
    "next_steps": "Next Steps",
    "afternoon_focus": "Afternoon Focus",
}

# Status box titles
STATUS_BOX_TITLES = {
    "timestamp": "Timestamp",
    "git_status": "Git Status",
    "afternoon_focus": "Afternoon Focus",
}

# Default fallback content
DEFAULT_CONTENT = {
    "morning_progress": [
        "Show-Me Session Overview Enhancement completed",
        "Code consolidation and cleanup",
        "Template inlining and verification",
        "Mindspace review and journal reflection",
    ],
    "next_steps": [
        "Review completed Show-Me enhancement work",
        "Consider next work effort priorities",
        "Plan afternoon focus area",
        "Continue with planned implementation work",
    ],
    "chat_context": {
        "current_task": "Midday status review and afternoon planning",
        "recent_topics": ["Show-Me enhancement", "Code consolidation", "Documentation"],
        "key_decisions": ["Show-Me work completed", "Code quality improvements"],
        "next_steps": ["Afternoon work planning", "Next work effort selection"],
    },
    "progress_intro": "Work completed today:",
    "progress_fallback_intro": "Review of work completed since morning:",
    "work_efforts_intro": "Active work efforts ({count} active):",
    "work_efforts_fallback": "No active work efforts found.",
}

# Devlog section markers
DEVLOG_MARKERS = {
    "summary": "### Summary",
    "accomplishments": "### Key Accomplishments",
    "date_prefix": "## ",
}

# Git status labels
GIT_LABELS = {"branch": "Branch:", "changed_files": "Changed Files:"}

# Abstract generation templates
ABSTRACT_TEMPLATES = {
    "dossier_intro": "This midday dossier provides a comprehensive status report as of {timestamp}. ",
    "branch_with_changes": "The current working branch is {branch} with {count} file(s) modified since the last commit. ",
    "branch_clean": "The repository is on branch {branch} with no uncommitted changes. ",
    "active_work_count": "There are currently {count} active work effort(s) in progress. ",
    "no_work_efforts": "No active work efforts are currently tracked. ",
    "morning_progress": "Significant progress has been made this morning across multiple areas of development. ",
    "morning_planning": "The morning session has been focused on planning and status review. ",
    "afternoon_focus_set": "The afternoon focus is set to: {focus}. ",
    "dossier_details": "This report details the current system state, morning accomplishments, active work efforts, and afternoon planning priorities.",
    "summary_start": "In summary, the current development state reflects active progress across the project. ",
    "morning_results": "The morning session has yielded tangible results, with multiple work items completed or advanced. ",
    "work_efforts_include": "Active work efforts include {titles}, and {additional_count} additional effort(s). ",
    "work_efforts_include_simple": "Active work efforts include {titles}. ",
    "files_modified": "With {count} file(s) currently modified, the codebase is in an active development state. ",
    "afternoon_focus": "The afternoon will be dedicated to {focus}, building upon the morning's progress. ",
    "afternoon_default": "The afternoon priorities focus on continuing active work efforts and advancing key development objectives. ",
    "summary_end": "The project maintains steady momentum with clear direction for continued development.",
}

# Work effort index file patterns
INDEX_FILE_PATTERNS = ["{we_dir_name}_index.md", "{we_id}_index.md", "index.md"]


def gather_midday_status() -> dict[str, Any]:
    """Gather comprehensive midday status information."""
    import subprocess
    from pathlib import Path

    project_path = Path.cwd()
    status = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
    }

    # Git status
    try:
        result = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, cwd=project_path
        )
        changed_files = [line for line in result.stdout.strip().split("\n") if line]
        status["git_changed"] = len(changed_files)
        status["git_files"] = changed_files[: FILE_LIMITS["git_files_display"]]
    except Exception:
        status["git_changed"] = 0
        status["git_files"] = []

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True, cwd=project_path
        )
        status["git_branch"] = result.stdout.strip() or "unknown"
    except Exception:
        status["git_branch"] = "unknown"

    # Get active work efforts
    work_efforts = []
    work_efforts_path = project_path / "_work_efforts"
    if work_efforts_path.exists():
        for we_dir in work_efforts_path.iterdir():
            if we_dir.is_dir() and we_dir.name.startswith("WE-"):
                we_id = we_dir.name.split("_")[0] if "_" in we_dir.name else we_dir.name

                # Try multiple index file patterns
                for pattern_template in INDEX_FILE_PATTERNS:
                    pattern = pattern_template.format(we_dir_name=we_dir.name, we_id=we_id)
                    index_file = we_dir / pattern
                    if index_file.exists():
                        try:
                            content = index_file.read_text()
                            content_lower = content.lower()

                            # Extract status using lookup table
                            status_val = "open"
                            for status_key, status_patterns in WORK_EFFORT_STATUS.items():
                                if any(
                                    f"status: {pattern}" in content_lower
                                    for pattern in status_patterns
                                ):
                                    status_val = status_key
                                    break

                            # Extract title
                            title = we_dir.name.replace("WE-", "").replace("_", " ").title()
                            if "title:" in content:
                                for line in content.split("\n"):
                                    if line.strip().startswith("title:"):
                                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
                                        break

                            if status_val == "active":
                                work_efforts.append(
                                    {"id": we_id, "title": title, "status": status_val}
                                )
                        except Exception:
                            pass
                        break

    status["active_work_efforts"] = work_efforts[: FILE_LIMITS["work_efforts_display"]]
    status["active_work_efforts_count"] = len(work_efforts)

    # Get recent devlog entries for morning progress
    morning_progress = []
    devlog_path = project_path / "_work_efforts" / "devlog.md"
    if devlog_path.exists():
        try:
            content = devlog_path.read_text()
            # Extract today's entries
            today = datetime.now().strftime("%Y-%m-%d")
            lines = content.split("\n")
            in_today_entry = False
            current_entry = []
            date_marker = f"{DEVLOG_MARKERS['date_prefix']}{today}"
            for i, line in enumerate(lines):
                if date_marker in line:
                    in_today_entry = True
                    current_entry = [line]
                elif in_today_entry:
                    if line.startswith(DEVLOG_MARKERS["date_prefix"]) and not line.startswith(
                        date_marker
                    ):
                        break
                    current_entry.append(line)
                    if (
                        DEVLOG_MARKERS["summary"] in line
                        or DEVLOG_MARKERS["accomplishments"] in line
                    ):
                        # Capture next few lines
                        for j in range(i + 1, min(i + 10, len(lines))):
                            if lines[j].strip() and not lines[j].startswith("##"):
                                morning_progress.append(lines[j].strip())
                            else:
                                break
            if current_entry:
                morning_progress = current_entry[: FILE_LIMITS["morning_progress_lines"]]
        except Exception:
            pass

    status["morning_progress"] = morning_progress[: FILE_LIMITS["morning_progress_items"]]

    return status


def generate_abstract(status: dict[str, Any], afternoon_focus: str | None = None) -> str:
    """Generate prose abstract summarizing the current state."""
    import html as html_module

    timestamp = status.get("timestamp", "current time")
    git_changed = status.get("git_changed", 0)
    git_branch = status.get("git_branch", "unknown")
    active_count = status.get("active_work_efforts_count", 0)
    morning_items = status.get("morning_progress", [])

    # Build abstract prose using templates
    abstract_parts = []

    abstract_parts.append(
        ABSTRACT_TEMPLATES["dossier_intro"].format(timestamp=html_module.escape(timestamp))
    )

    if git_changed > 0:
        abstract_parts.append(
            ABSTRACT_TEMPLATES["branch_with_changes"].format(
                branch=html_module.escape(git_branch), count=git_changed
            )
        )
    else:
        abstract_parts.append(
            ABSTRACT_TEMPLATES["branch_clean"].format(branch=html_module.escape(git_branch))
        )

    if active_count > 0:
        abstract_parts.append(ABSTRACT_TEMPLATES["active_work_count"].format(count=active_count))
    else:
        abstract_parts.append(ABSTRACT_TEMPLATES["no_work_efforts"])

    if morning_items:
        abstract_parts.append(ABSTRACT_TEMPLATES["morning_progress"])
    else:
        abstract_parts.append(ABSTRACT_TEMPLATES["morning_planning"])

    if afternoon_focus:
        abstract_parts.append(
            ABSTRACT_TEMPLATES["afternoon_focus_set"].format(
                focus=html_module.escape(afternoon_focus)
            )
        )

    abstract_parts.append(ABSTRACT_TEMPLATES["dossier_details"])

    return "".join(abstract_parts)


def generate_summary(status: dict[str, Any], afternoon_focus: str | None = None) -> str:
    """Generate prose summary with key takeaways and next steps."""
    import html as html_module

    git_changed = status.get("git_changed", 0)
    active_work_efforts = status.get("active_work_efforts", [])
    active_count = status.get("active_work_efforts_count", 0)
    morning_items = status.get("morning_progress", [])

    # Build summary prose using templates
    summary_parts = []

    summary_parts.append(ABSTRACT_TEMPLATES["summary_start"])

    if morning_items:
        summary_parts.append(ABSTRACT_TEMPLATES["morning_results"])

    if active_count > 0:
        work_titles = [we.get("title", "Untitled") for we in active_work_efforts[:3]]
        if work_titles:
            titles_text = ", ".join([html_module.escape(title) for title in work_titles])
            if active_count > 3:
                additional_count = active_count - len(work_titles)
                summary_parts.append(
                    ABSTRACT_TEMPLATES["work_efforts_include"].format(
                        titles=titles_text, additional_count=additional_count
                    )
                )
            else:
                summary_parts.append(
                    ABSTRACT_TEMPLATES["work_efforts_include_simple"].format(titles=titles_text)
                )
    else:
        summary_parts.append(ABSTRACT_TEMPLATES["no_work_efforts"])

    if git_changed > 0:
        summary_parts.append(ABSTRACT_TEMPLATES["files_modified"].format(count=git_changed))

    if afternoon_focus:
        summary_parts.append(
            ABSTRACT_TEMPLATES["afternoon_focus"].format(
                focus=html_module.escape(afternoon_focus.lower())
            )
        )
    else:
        summary_parts.append(ABSTRACT_TEMPLATES["afternoon_default"])

    summary_parts.append(ABSTRACT_TEMPLATES["summary_end"])

    return "".join(summary_parts)


def build_midday_content(status: dict[str, Any], afternoon_focus: str | None = None) -> str:
    """Build midday dossier content."""
    import html as html_module

    content_parts = []

    # Abstract at the top
    content_parts.append("<h2>Abstract</h2>")
    abstract_text = generate_abstract(status, afternoon_focus)
    content_parts.append(f'<p style="text-align: justify; line-height: 1.6;">{abstract_text}</p>')
    content_parts.append("")  # Spacing

    # Status Section
    content_parts.append(f"<h2>{SECTION_TITLES['current_status']}</h2>")
    content_parts.append(f"""
    <div class="status-box">
        <div class="status-title">{STATUS_BOX_TITLES["timestamp"]}</div>
        <p><strong>{html_module.escape(status["timestamp"])}</strong></p>
    </div>
    """)

    content_parts.append(f"""
    <div class="status-box">
        <div class="status-title">{STATUS_BOX_TITLES["git_status"]}</div>
        <p><strong>{GIT_LABELS["branch"]}</strong> {html_module.escape(status["git_branch"])}</p>
        <p><strong>{GIT_LABELS["changed_files"]}</strong> {status["git_changed"]}</p>
    </div>
    """)

    if status.get("git_files"):
        content_parts.append(f"<h3>{SECTION_TITLES['recent_changes']}</h3>")
        content_parts.append("<ul>")
        for file_line in status["git_files"][: FILE_LIMITS["git_files_list"]]:
            content_parts.append(
                f"<li><code>{html_module.escape(file_line[: FILE_LIMITS['file_line_length']])}</code></li>"
            )
        content_parts.append("</ul>")

    # Morning Progress Section
    content_parts.append(f"<h2>{SECTION_TITLES['morning_progress']}</h2>")
    morning_items = status.get("morning_progress", [])
    if morning_items:
        content_parts.append(f"""
        <div class="note">
            <div class="note-title">{NOTE_TITLES["morning_accomplishments"]}</div>
            <p>{DEFAULT_CONTENT["progress_intro"]}</p>
            <ul>
        """)
        for item in morning_items:
            if item.strip() and not item.startswith("#"):
                # Clean up markdown formatting
                clean_item = item.replace("**", "").replace("*", "").replace("- ", "").strip()
                if clean_item and len(clean_item) > 5:
                    content_parts.append(f"<li>{html_module.escape(clean_item[:120])}</li>")
        content_parts.append("</ul></div>")
    else:
        # Use default fallback
        content_parts.append(f"""
        <div class="note">
            <div class="note-title">{NOTE_TITLES["morning_accomplishments"]}</div>
            <p>{DEFAULT_CONTENT["progress_fallback_intro"]}</p>
            <ul>
        """)
        for item in DEFAULT_CONTENT["morning_progress"]:
            content_parts.append(f"<li>{html_module.escape(item)}</li>")
        content_parts.append("</ul></div>")

    # Active Work Section
    content_parts.append(f"<h2>{SECTION_TITLES['active_work']}</h2>")
    active_work_efforts = status.get("active_work_efforts", [])
    active_count = status.get("active_work_efforts_count", 0)
    if active_work_efforts:
        work_intro = DEFAULT_CONTENT["work_efforts_intro"].format(count=active_count)
        content_parts.append(f"""
        <div class="note">
            <div class="note-title">{NOTE_TITLES["current_work"]}</div>
            <p>{work_intro}</p>
            <ul>
        """)
        for we in active_work_efforts:
            we_id = html_module.escape(we.get("id", "unknown"))
            we_title = html_module.escape(we.get("title", "Untitled"))
            content_parts.append(f"<li><strong>{we_id}</strong>: {we_title}</li>")
        content_parts.append("</ul></div>")
    else:
        # Fallback message
        content_parts.append(f"""
        <div class="note">
            <div class="note-title">{NOTE_TITLES["current_work"]}</div>
            <p>{DEFAULT_CONTENT["work_efforts_fallback"]}</p>
        </div>
        """)

    # Afternoon Planning Section
    content_parts.append(f"<h2>{SECTION_TITLES['afternoon_planning']}</h2>")
    if afternoon_focus:
        content_parts.append(f"""
        <div class="status-box">
            <div class="status-title">{STATUS_BOX_TITLES["afternoon_focus"]}</div>
            <p><strong>{html_module.escape(afternoon_focus)}</strong></p>
        </div>
        """)

    # Next steps - use default if no custom ones provided
    next_steps = DEFAULT_CONTENT["next_steps"]
    content_parts.append(f"""
    <div class="note">
        <div class="note-title">{NOTE_TITLES["next_steps"]}</div>
        <ol>
    """)
    for i, step in enumerate(next_steps, 1):
        content_parts.append(f"<li>{html_module.escape(step)}</li>")
    content_parts.append("</ol></div>")

    # Summary at the end
    content_parts.append("")  # Spacing
    content_parts.append("<h2>Summary</h2>")
    summary_text = generate_summary(status, afternoon_focus)
    content_parts.append(f'<p style="text-align: justify; line-height: 1.6;">{summary_text}</p>')

    return "\n".join(content_parts)


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Create midday status dossier")
    parser.add_argument("--title", default=None, help="Custom title for dossier")
    parser.add_argument("--afternoon-focus", default=None, help="Afternoon focus area")
    parser.add_argument("--output", default=None, help="Output PDF path")
    args = parser.parse_args()

    # Gather status
    print("📊 Gathering midday status...")
    status = gather_midday_status()

    # Build content
    print("📝 Building dossier content...")
    content = build_midday_content(status, args.afternoon_focus)

    # Create brief document with variables from lookup tables
    title = args.title or f"{REPORT_CONFIG['title_prefix']} - {status['date']}"
    doc_id = f"{REPORT_CONFIG['doc_id_prefix']}-{status['date'].replace('-', '')}"
    subtitle = f"{REPORT_CONFIG['subtitle_prefix']} - {status['time']}"

    # Build cover metadata from configuration
    cover_metadata = {
        "OPERATIONAL MANUAL": COVER_CONFIG["operational_manual"],
        "CODENAME": COVER_CONFIG["codename"],
        "REPORT_TYPE": REPORT_CONFIG["type"],
        "DATE": status["date"],
        "TIME": status["time"],
    }

    # Build cover warning message
    warning_message = (
        f"{REPORT_CONFIG['subtitle_prefix'].upper()} - {status['git_changed']} files changed"
    )

    # Build cover signature
    cover_signature = {
        "role": COVER_CONFIG["signature_role"],
        "name": COVER_CONFIG["signature_name"],
        "date": status["date"],
    }

    # Use default chat context or customize
    chat_context = DEFAULT_CONTENT["chat_context"].copy()
    # Update with current status if available
    if status.get("active_work_efforts_count", 0) > 0:
        chat_context["recent_topics"].append(
            f"{status['active_work_efforts_count']} active work efforts"
        )

    doc = BriefDocument(
        title=title,
        doc_id=doc_id,
        subtitle=subtitle,
        classification=COVER_CONFIG["classification"],
        cover_header=COVER_CONFIG["header"],
        cover_metadata=cover_metadata,
        cover_warning={"message": warning_message, "severity": REPORT_CONFIG["warning_severity"]},
        cover_signature=cover_signature,
        cover_footer=COVER_CONFIG["footer"],
        include_system_status=True,
        chat_context=chat_context,
    )

    # Add custom content
    doc.content_blocks.append(content)

    # Generate PDF
    print("📄 Generating PDF...")
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = None

    pdf_path = doc.generate(output_path=output_path)

    print("=" * 60)
    print("✅ Midday Dossier Created!")
    print("=" * 60)
    print(f"📄 Output: {pdf_path}")
    print()
    print("Ready for review and afternoon planning!")

    return pdf_path


if __name__ == "__main__":
    main()
