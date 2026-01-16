#!/usr/bin/env python3
"""
Evening Report Creator
======================

Creates a comprehensive evening status report with daily accomplishments,
current state, and tomorrow's priorities.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument


def gather_evening_status() -> Dict[str, Any]:
    """Gather comprehensive evening status information."""
    import subprocess
    from pathlib import Path
    
    project_path = Path.cwd()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    today_start = datetime(now.year, now.month, now.day)
    
    status = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "date": today,
        "time": now.strftime("%H:%M"),
        "day_of_week": now.strftime("%A"),
    }
    
    # Git status
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        changed_files = [line for line in result.stdout.strip().split('\n') if line]
        status["git_changed"] = len(changed_files)
        status["git_files"] = changed_files[:20]  # First 20 files
    except Exception:
        status["git_changed"] = 0
        status["git_files"] = []
    
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        status["git_branch"] = result.stdout.strip() or "unknown"
    except Exception:
        status["git_branch"] = "unknown"
    
    # Today's commits
    try:
        result = subprocess.run(
            ["git", "log", "--since", today_start.isoformat(), "--oneline"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        today_commits = [line for line in result.stdout.strip().split('\n') if line]
        status["today_commits"] = today_commits[:10]  # Last 10 commits
        status["commits_count"] = len(today_commits)
    except Exception:
        status["today_commits"] = []
        status["commits_count"] = 0
    
    # Work efforts
    work_efforts_dir = project_path / "_work_efforts"
    if work_efforts_dir.exists():
        # Count active work efforts
        active_dir = work_efforts_dir / "active"
        if active_dir.exists():
            active_files = list(active_dir.glob("*.md"))
            status["active_work_efforts_count"] = len(active_files)
        else:
            status["active_work_efforts_count"] = 0
        
        # Recent work effort files (today)
        all_we = sorted(
            work_efforts_dir.rglob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        today_we = [f for f in all_we if datetime.fromtimestamp(f.stat().st_mtime).date() == now.date()]
        status["today_work_efforts"] = [f.name for f in today_we[:10]]
        status["today_work_efforts_count"] = len(today_we)
    else:
        status["active_work_efforts_count"] = 0
        status["today_work_efforts"] = []
        status["today_work_efforts_count"] = 0
    
    # Recent activity (devlog)
    devlog_path = work_efforts_dir / "devlog.md"
    if devlog_path.exists():
        try:
            devlog_content = devlog_path.read_text()
            # Get last 500 chars for recent activity
            status["recent_devlog"] = devlog_content[-500:] if len(devlog_content) > 500 else devlog_content
        except Exception:
            status["recent_devlog"] = ""
    else:
        status["recent_devlog"] = ""
    
    return status


def build_evening_content(status: Dict[str, Any], tomorrow_focus: Optional[str] = None) -> str:
    """Build evening report content."""
    import html as html_module
    
    content_parts = []
    
    # Header
    content_parts.append(f'<h2>Evening Report - {status["day_of_week"]}, {status["date"]}</h2>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Report Time</div>
        <p><strong>{html_module.escape(status['timestamp'])}</strong></p>
    </div>
    ''')
    
    # Today's Accomplishments
    content_parts.append('<h2>Today\'s Accomplishments</h2>')
    
    accomplishments = []
    
    if status['commits_count'] > 0:
        accomplishments.append(f"✅ {status['commits_count']} git commits made")
    
    if status['today_work_efforts_count'] > 0:
        accomplishments.append(f"✅ {status['today_work_efforts_count']} work effort files created/updated")
    
    if status['git_changed'] > 0:
        accomplishments.append(f"✅ {status['git_changed']} files currently modified")
    
    if not accomplishments:
        accomplishments.append("📋 Day in review - status check completed")
    
    content_parts.append('<div class="note">')
    content_parts.append('<div class="note-title">Daily Summary</div>')
    content_parts.append('<ul>')
    for acc in accomplishments:
        content_parts.append(f'<li>{acc}</li>')
    content_parts.append('</ul>')
    content_parts.append('</div>')
    
    # Today's Commits
    if status['today_commits']:
        content_parts.append('<h3>Today\'s Git Commits</h3>')
        content_parts.append('<ul>')
        for commit in status['today_commits'][:8]:
            commit_msg = commit.split(' ', 1)[1] if ' ' in commit else commit
            content_parts.append(f'<li><code>{html_module.escape(commit_msg[:70])}</code></li>')
        content_parts.append('</ul>')
    
    # Current System Status
    content_parts.append('<h2>Current System Status</h2>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Git Status</div>
        <p><strong>Branch:</strong> {html_module.escape(status['git_branch'])}</p>
        <p><strong>Uncommitted Changes:</strong> {status['git_changed']} files</p>
    </div>
    ''')
    
    if status['git_files']:
        content_parts.append('<h3>Pending File Changes</h3>')
        content_parts.append('<ul>')
        for file_line in status['git_files'][:15]:
            content_parts.append(f'<li><code>{html_module.escape(file_line[:80])}</code></li>')
        content_parts.append('</ul>')
    
    # Active Work Efforts
    content_parts.append('<h2>Active Work Efforts</h2>')
    content_parts.append(f'''
    <div class="note">
        <div class="note-title">Current Work</div>
        <p><strong>{status['active_work_efforts_count']}</strong> active work efforts in progress</p>
    </div>
    ''')
    
    if status['today_work_efforts']:
        content_parts.append('<h3>Work Efforts Created/Updated Today</h3>')
        content_parts.append('<ul>')
        for we_file in status['today_work_efforts'][:8]:
            content_parts.append(f'<li><code>{html_module.escape(we_file)}</code></li>')
        content_parts.append('</ul>')
    
    # Tomorrow's Priorities
    content_parts.append('<h2>Tomorrow\'s Priorities</h2>')
    if tomorrow_focus:
        content_parts.append(f'''
        <div class="status-box">
            <div class="status-title">Primary Focus</div>
            <p><strong>{html_module.escape(tomorrow_focus)}</strong></p>
        </div>
        ''')
    
    content_parts.append('''
    <div class="note">
        <div class="note-title">Next Steps</div>
        <ol>
            <li>Review pending changes and commit if ready</li>
            <li>Update work efforts with today's progress</li>
            <li>Plan tomorrow's priorities</li>
            <li>Review active work efforts status</li>
        </ol>
    </div>
    ''')
    
    # End of Day Notes
    content_parts.append('<h2>End of Day Notes</h2>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Reflection</div>
        <p>Today\'s work session complete. Review accomplishments, commit changes, and prepare for tomorrow.</p>
        <p><strong>Status:</strong> Ready for next session</p>
    </div>
    ''')
    
    return '\n'.join(content_parts)


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create evening status report')
    parser.add_argument('--title', default=None, help='Custom title for report')
    parser.add_argument('--tomorrow-focus', default=None, help='Tomorrow\'s primary focus area')
    parser.add_argument('--output', default=None, help='Output PDF path')
    args = parser.parse_args()
    
    # Gather status
    print("🌙 Gathering evening status...")
    status = gather_evening_status()
    
    # Build content
    print("📝 Building report content...")
    content = build_evening_content(status, args.tomorrow_focus)
    
    # Create brief document
    title = args.title or f"Evening Report - {status['date']}"
    doc_id = f"EVENING-{status['date'].replace('-', '')}"
    
    doc = BriefDocument(
        title=title,
        doc_id=doc_id,
        subtitle=f"End of Day Summary - {status['time']}",
        classification="INTERNAL",
        cover_header="TELEPORT MASSIVE",
        cover_metadata={
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "REPORT_TYPE": "EVENING REPORT",
            "DATE": status['date'],
            "TIME": status['time'],
            "DAY": status['day_of_week']
        },
        cover_warning={
            "message": f"END OF DAY REPORT - {status['commits_count']} commits today, {status['git_changed']} files pending",
            "severity": "INFO"
        },
        cover_signature={
            "role": "AUTHORIZED BY",
            "name": "Site-Delta-9",
            "date": status['date']
        },
        cover_footer="EVENING REPORT - INTERNAL USE ONLY",
        include_system_status=True,
        chat_context={
            'current_task': 'Evening status review and tomorrow planning',
            'recent_topics': ['Daily accomplishments', 'Work progress', 'Tomorrow priorities'],
            'key_decisions': ['End of day status captured', 'Tomorrow priorities identified'],
            'next_steps': ['Review pending changes', 'Plan tomorrow work', 'Update work efforts']
        }
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
    print("✅ Evening Report Created!")
    print("=" * 60)
    print(f"📄 Output: {pdf_path}")
    print()
    print("Ready for review and tomorrow planning!")
    
    return pdf_path


if __name__ == "__main__":
    main()
