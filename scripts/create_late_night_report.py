#!/usr/bin/env python3
"""
Late Night Report Creator
==========================

Creates a comprehensive late-night status report with deep work accomplishments,
current state, late-night insights, and tomorrow's priorities.
Perfect for late-night coding sessions and deep work reflection.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument


def gather_late_night_status() -> Dict[str, Any]:
    """Gather comprehensive late-night status information."""
    import subprocess
    from pathlib import Path
    
    project_path = Path.cwd()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    today_start = datetime(now.year, now.month, now.day)
    
    # Determine if it's actually late night (after 10 PM or before 6 AM)
    hour = now.hour
    is_late_night = hour >= 22 or hour < 6
    
    status = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "date": today,
        "time": now.strftime("%H:%M"),
        "day_of_week": now.strftime("%A"),
        "hour": hour,
        "is_late_night": is_late_night,
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
    
    # Today's commits (including late-night commits)
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
        
        # Late-night commits (after 10 PM today or before 6 AM today)
        late_night_commits = []
        for commit_line in today_commits:
            if commit_line:
                try:
                    # Get commit timestamp
                    commit_hash = commit_line.split()[0]
                    commit_time_result = subprocess.run(
                        ["git", "log", "-1", "--format=%H|%ct", commit_hash],
                        capture_output=True,
                        text=True,
                        cwd=project_path
                    )
                    if commit_time_result.stdout:
                        parts = commit_time_result.stdout.strip().split('|')
                        if len(parts) == 2:
                            commit_timestamp = int(parts[1])
                            commit_dt = datetime.fromtimestamp(commit_timestamp)
                            commit_hour = commit_dt.hour
                            if commit_hour >= 22 or commit_hour < 6:
                                late_night_commits.append(commit_line)
                except Exception:
                    pass
        
        status["late_night_commits"] = late_night_commits[:8]
        status["late_night_commits_count"] = len(late_night_commits)
    except Exception:
        status["today_commits"] = []
        status["commits_count"] = 0
        status["late_night_commits"] = []
        status["late_night_commits_count"] = 0
    
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
        
        # Late-night work efforts (modified after 10 PM or before 6 AM)
        late_night_we = []
        for we_file in today_we:
            mtime = datetime.fromtimestamp(we_file.stat().st_mtime)
            if mtime.hour >= 22 or mtime.hour < 6:
                late_night_we.append(we_file.name)
        status["late_night_work_efforts"] = late_night_we[:8]
        status["late_night_work_efforts_count"] = len(late_night_we)
    else:
        status["active_work_efforts_count"] = 0
        status["today_work_efforts"] = []
        status["today_work_efforts_count"] = 0
        status["late_night_work_efforts"] = []
        status["late_night_work_efforts_count"] = 0
    
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


def build_late_night_content(status: Dict[str, Any], insights: Optional[str] = None) -> str:
    """Build late-night report content."""
    import html as html_module
    
    content_parts = []
    
    # Header
    time_label = "Late Night" if status["is_late_night"] else "Evening"
    content_parts.append(f'<h2>Late Night Report - {status["day_of_week"]}, {status["date"]}</h2>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Report Time</div>
        <p><strong>{html_module.escape(status['timestamp'])}</strong></p>
        <p><em>Deep work session in progress</em></p>
    </div>
    ''')
    
    # Late-Night Accomplishments
    content_parts.append('<h2>Late-Night Accomplishments</h2>')
    
    accomplishments = []
    
    if status['late_night_commits_count'] > 0:
        accomplishments.append(f"🌙 {status['late_night_commits_count']} late-night commits made")
    
    if status['late_night_work_efforts_count'] > 0:
        accomplishments.append(f"🌙 {status['late_night_work_efforts_count']} work efforts updated during late-night session")
    
    if status['commits_count'] > 0:
        accomplishments.append(f"✅ {status['commits_count']} total commits today")
    
    if status['today_work_efforts_count'] > 0:
        accomplishments.append(f"✅ {status['today_work_efforts_count']} work effort files created/updated today")
    
    if status['git_changed'] > 0:
        accomplishments.append(f"📝 {status['git_changed']} files currently modified")
    
    if not accomplishments:
        accomplishments.append("🌙 Late-night session in progress - status check completed")
    
    content_parts.append('<div class="note">')
    content_parts.append('<div class="note-title">Deep Work Summary</div>')
    content_parts.append('<ul>')
    for acc in accomplishments:
        content_parts.append(f'<li>{acc}</li>')
    content_parts.append('</ul>')
    content_parts.append('</div>')
    
    # Late-Night Commits
    if status['late_night_commits']:
        content_parts.append('<h3>Late-Night Git Commits</h3>')
        content_parts.append('<ul>')
        for commit in status['late_night_commits'][:8]:
            commit_msg = commit.split(' ', 1)[1] if ' ' in commit else commit
            content_parts.append(f'<li><code>{html_module.escape(commit_msg[:70])}</code></li>')
        content_parts.append('</ul>')
    elif status['today_commits']:
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
    
    if status['late_night_work_efforts']:
        content_parts.append('<h3>Work Efforts Updated During Late-Night Session</h3>')
        content_parts.append('<ul>')
        for we_file in status['late_night_work_efforts'][:8]:
            content_parts.append(f'<li><code>{html_module.escape(we_file)}</code></li>')
        content_parts.append('</ul>')
    elif status['today_work_efforts']:
        content_parts.append('<h3>Work Efforts Created/Updated Today</h3>')
        content_parts.append('<ul>')
        for we_file in status['today_work_efforts'][:8]:
            content_parts.append(f'<li><code>{html_module.escape(we_file)}</code></li>')
        content_parts.append('</ul>')
    
    # Late-Night Insights
    content_parts.append('<h2>Late-Night Insights</h2>')
    if insights:
        content_parts.append(f'''
        <div class="status-box">
            <div class="status-title">Session Insights</div>
            <p><strong>{html_module.escape(insights)}</strong></p>
        </div>
        ''')
    
    content_parts.append('''
    <div class="note">
        <div class="note-title">Deep Work Reflection</div>
        <p>Late-night sessions often yield breakthrough insights and focused progress. Capture key learnings and decisions made during this session.</p>
        <ul>
            <li>What problems were solved?</li>
            <li>What patterns emerged?</li>
            <li>What decisions were made?</li>
            <li>What should be prioritized tomorrow?</li>
        </ul>
    </div>
    ''')
    
    # Tomorrow's Priorities
    content_parts.append('<h2>Tomorrow\'s Priorities</h2>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Next Steps</div>
        <ol>
            <li>Review late-night changes and commit if ready</li>
            <li>Update work efforts with tonight's progress</li>
            <li>Plan tomorrow's priorities based on tonight's insights</li>
            <li>Review active work efforts status</li>
            <li>Get rest - late-night work is valuable but rest is essential</li>
        </ol>
    </div>
    ''')
    
    # End of Session Notes
    content_parts.append('<h2>End of Late-Night Session Notes</h2>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Reflection</div>
        <p>Late-night work session complete. Review accomplishments, capture insights, commit changes, and prepare for tomorrow.</p>
        <p><strong>Status:</strong> Ready for rest and tomorrow's continuation</p>
        <p><em>Remember: Deep work is powerful, but sustainable pace requires rest.</em></p>
    </div>
    ''')
    
    return '\n'.join(content_parts)


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create late-night status report')
    parser.add_argument('--title', default=None, help='Custom title for report')
    parser.add_argument('--insights', default=None, help='Late-night session insights or key learnings')
    parser.add_argument('--output', default=None, help='Output PDF path')
    args = parser.parse_args()
    
    # Gather status
    print("🌙 Gathering late-night status...")
    status = gather_late_night_status()
    
    # Build content
    print("📝 Building report content...")
    content = build_late_night_content(status, args.insights)
    
    # Create brief document
    title = args.title or f"Late Night Report - {status['date']}"
    doc_id = f"LATE-NIGHT-{status['date'].replace('-', '')}"
    
    doc = BriefDocument(
        title=title,
        doc_id=doc_id,
        subtitle=f"Deep Work Session Summary - {status['time']}",
        classification="INTERNAL",
        cover_header="TELEPORT MASSIVE",
        cover_metadata={
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "REPORT_TYPE": "LATE NIGHT REPORT",
            "DATE": status['date'],
            "TIME": status['time'],
            "DAY": status['day_of_week']
        },
        cover_warning={
            "message": f"LATE NIGHT SESSION - {status['late_night_commits_count']} late-night commits, {status['git_changed']} files pending",
            "severity": "INFO"
        },
        cover_signature={
            "role": "AUTHORIZED BY",
            "name": "Site-Delta-9",
            "date": status['date']
        },
        cover_footer="LATE NIGHT REPORT - INTERNAL USE ONLY",
        include_system_status=True,
        chat_context={
            'current_task': 'Late-night status review and deep work reflection',
            'recent_topics': ['Late-night accomplishments', 'Deep work progress', 'Tomorrow priorities'],
            'key_decisions': ['Late-night status captured', 'Insights documented', 'Tomorrow priorities identified'],
            'next_steps': ['Review pending changes', 'Plan tomorrow work', 'Update work efforts', 'Get rest']
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
    print("✅ Late Night Report Created!")
    print("=" * 60)
    print(f"📄 Output: {pdf_path}")
    print()
    print("🌙 Late-night session documented. Ready for review and tomorrow planning!")
    print("💤 Remember to get rest - sustainable pace requires balance.")
    
    return pdf_path


if __name__ == "__main__":
    main()
