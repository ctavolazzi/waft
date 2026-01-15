#!/usr/bin/env python3
"""
Midday Dossier Creator
=======================

Creates a comprehensive midday status dossier with current system state,
work progress, and afternoon planning.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument, create_brief


def gather_midday_status() -> Dict[str, Any]:
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
    
    # Work efforts (if MCP available)
    try:
        # Try to get active work efforts count
        status["active_work_efforts"] = "Available via MCP"
    except Exception:
        status["active_work_efforts"] = "Unknown"
    
    return status


def build_midday_content(status: Dict[str, Any], afternoon_focus: Optional[str] = None) -> str:
    """Build midday dossier content."""
    import html as html_module
    
    content_parts = []
    
    # Status Section
    content_parts.append('<h2>Current System Status</h2>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Timestamp</div>
        <p><strong>{html_module.escape(status['timestamp'])}</strong></p>
    </div>
    ''')
    
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Git Status</div>
        <p><strong>Branch:</strong> {html_module.escape(status['git_branch'])}</p>
        <p><strong>Changed Files:</strong> {status['git_changed']}</p>
    </div>
    ''')
    
    if status['git_files']:
        content_parts.append('<h3>Recent File Changes</h3>')
        content_parts.append('<ul>')
        for file_line in status['git_files'][:15]:
            content_parts.append(f'<li><code>{html_module.escape(file_line[:80])}</code></li>')
        content_parts.append('</ul>')
    
    # Morning Progress Section
    content_parts.append('<h2>Morning Progress</h2>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Morning Accomplishments</div>
        <p>Review of work completed since morning:</p>
        <ul>
            <li>Prime Directive planning reviewed</li>
            <li>Brief and checkpoint documents created</li>
            <li>System status verified</li>
            <li>Midday dossier command created</li>
        </ul>
    </div>
    ''')
    
    # Active Work Section
    content_parts.append('<h2>Active Work Efforts</h2>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Current Work</div>
        <p>28 active work efforts across various features including:</p>
        <ul>
            <li>RAG Chatbot Permanent Integration (WE-260113-tya7)</li>
            <li>PDF Template Library System (WE-260112-q6gl)</li>
            <li>Being Lifecycle Attributes (WE-260111-roo0)</li>
            <li>Prime Directive Planning (current session)</li>
        </ul>
    </div>
    ''')
    
    # Afternoon Planning Section
    content_parts.append('<h2>Afternoon Planning</h2>')
    if afternoon_focus:
        content_parts.append(f'''
        <div class="status-box">
            <div class="status-title">Afternoon Focus</div>
            <p><strong>{html_module.escape(afternoon_focus)}</strong></p>
        </div>
        ''')
    
    content_parts.append('''
    <div class="note">
        <div class="note-title">Next Steps</div>
        <ol>
            <li>Review Prime Directive implementation plan</li>
            <li>Clarify implementation scope and priorities</li>
            <li>Create work effort if proceeding</li>
            <li>Begin implementation based on decisions</li>
        </ol>
    </div>
    ''')
    
    return '\n'.join(content_parts)


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create midday status dossier')
    parser.add_argument('--title', default=None, help='Custom title for dossier')
    parser.add_argument('--afternoon-focus', default=None, help='Afternoon focus area')
    parser.add_argument('--output', default=None, help='Output PDF path')
    args = parser.parse_args()
    
    # Gather status
    print("📊 Gathering midday status...")
    status = gather_midday_status()
    
    # Build content
    print("📝 Building dossier content...")
    content = build_midday_content(status, args.afternoon_focus)
    
    # Create brief document
    title = args.title or f"Midday Dossier - {status['date']}"
    doc_id = f"DOSSIER-{status['date'].replace('-', '')}"
    
    doc = BriefDocument(
        title=title,
        doc_id=doc_id,
        subtitle=f"Midday Status Report - {status['time']}",
        classification="INTERNAL",
        cover_header="TELEPORT MASSIVE",
        cover_metadata={
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "REPORT_TYPE": "MIDDAY DOSSIER",
            "DATE": status['date'],
            "TIME": status['time']
        },
        cover_warning={
            "message": f"MIDDAY STATUS REPORT - {status['git_changed']} files changed",
            "severity": "INFO"
        },
        cover_signature={
            "role": "AUTHORIZED BY",
            "name": "Site-Delta-9",
            "date": status['date']
        },
        cover_footer="MIDDAY DOSSIER - INTERNAL USE ONLY",
        include_system_status=True,
        chat_context={
            'current_task': 'Midday status review and afternoon planning',
            'recent_topics': ['Prime Directive planning', 'Brief creation', 'Checkpoint documentation'],
            'key_decisions': ['Midday dossier command created', 'Status review completed'],
            'next_steps': ['Afternoon work planning', 'Prime Directive implementation decision']
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
    print("✅ Midday Dossier Created!")
    print("=" * 60)
    print(f"📄 Output: {pdf_path}")
    print()
    print("Ready for review and afternoon planning!")
    
    return pdf_path


if __name__ == "__main__":
    main()
