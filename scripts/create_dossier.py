#!/usr/bin/env python3
"""
Dossier Creator - Mission Sitrep Dossier
==========================================

Creates comprehensive binder-ready mission sitrep dossier with:
- TM-ARCH-009 style cover page
- Section dividers
- Mission sitrep
- Work efforts summary
- Recent activity
- System status
- Key findings
- Next steps
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument, create_brief
from src.waft.binder import Binder, DocumentEntry, BinderSection
from src.waft.evolution.pdf_generator import PDFGenerator
from src.waft.utils import escape_title_for_pdf


def gather_dossier_data(project_path: Path) -> Dict[str, Any]:
    """Gather comprehensive dossier data."""
    data = {
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
        data["git_changed"] = len(changed_files)
        data["git_files"] = changed_files[:20]
        
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        data["git_branch"] = result.stdout.strip() or "unknown"
        
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        data["git_recent_commits"] = [line for line in result.stdout.strip().split('\n') if line][:5]
    except Exception:
        data["git_changed"] = 0
        data["git_files"] = []
        data["git_branch"] = "unknown"
        data["git_recent_commits"] = []
    
    # Work efforts
    work_efforts_dir = project_path / "_work_efforts"
    if work_efforts_dir.exists():
        # Count active work efforts
        active_dir = work_efforts_dir / "active"
        if active_dir.exists():
            active_files = list(active_dir.glob("*.md"))
            data["active_work_efforts_count"] = len(active_files)
        else:
            data["active_work_efforts_count"] = 0
        
        # Recent work effort files
        recent_we = sorted(
            work_efforts_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:10]
        data["recent_work_efforts"] = [f.name for f in recent_we]
    else:
        data["active_work_efforts_count"] = 0
        data["recent_work_efforts"] = []
    
    # Recent activity (devlog)
    devlog_path = work_efforts_dir / "devlog.md"
    if devlog_path.exists():
        try:
            content = devlog_path.read_text(encoding="utf-8")
            # Extract last few entries (simple heuristic)
            lines = content.split('\n')
            recent_lines = [l for l in lines[-50:] if l.strip() and not l.startswith('#')]
            data["recent_devlog_entries"] = recent_lines[-10:]
        except Exception:
            data["recent_devlog_entries"] = []
    else:
        data["recent_devlog_entries"] = []
    
    # Recent briefs
    briefs_dir = work_efforts_dir / "briefs"
    if briefs_dir.exists():
        recent_briefs = sorted(
            briefs_dir.glob("*.pdf"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:5]
        data["recent_briefs"] = [f.name for f in recent_briefs]
    else:
        data["recent_briefs"] = []
    
    return data


def build_dossier_content(data: Dict[str, Any]) -> str:
    """Build dossier content with sections and dividers."""
    import html as html_module
    
    content_parts = []
    
    # Section 1: Mission Sitrep
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">MISSION SITREP</h1>')
    content_parts.append('<p class="section-subtitle">Current Situation and Status</p>')
    content_parts.append('</div>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Current Situation</div>
        <p><strong>Timestamp:</strong> {html_module.escape(data['timestamp'])}</p>
        <p><strong>Date:</strong> {html_module.escape(data['date'])}</p>
        <p><strong>Time:</strong> {html_module.escape(data['time'])}</p>
    </div>
    ''')
    
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Git Status</div>
        <p><strong>Branch:</strong> {html_module.escape(data['git_branch'])}</p>
        <p><strong>Changed Files:</strong> {data['git_changed']}</p>
    </div>
    ''')
    
    if data['git_recent_commits']:
        content_parts.append('<h2>Recent Commits</h2>')
        content_parts.append('<ul>')
        for commit in data['git_recent_commits'][:5]:
            content_parts.append(f'<li><code>{html_module.escape(commit[:80])}</code></li>')
        content_parts.append('</ul>')
    
    # Section 2: Work Efforts
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">WORK EFFORTS</h1>')
    content_parts.append('<p class="section-subtitle">Active Work and Progress</p>')
    content_parts.append('</div>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Active Work</div>
        <p><strong>Active Work Efforts:</strong> {data['active_work_efforts_count']}</p>
    </div>
    ''')
    
    if data['recent_work_efforts']:
        content_parts.append('<h2>Recent Work Efforts</h2>')
        content_parts.append('<ul>')
        for we in data['recent_work_efforts'][:10]:
            content_parts.append(f'<li><code>{html_module.escape(we)}</code></li>')
        content_parts.append('</ul>')
    
    # Section 3: Recent Activity
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">RECENT ACTIVITY</h1>')
    content_parts.append('<p class="section-subtitle">What\'s Been Happening</p>')
    content_parts.append('</div>')
    
    if data['recent_briefs']:
        content_parts.append('<h2>Recent Briefs</h2>')
        content_parts.append('<ul>')
        for brief in data['recent_briefs']:
            content_parts.append(f'<li><code>{html_module.escape(brief)}</code></li>')
        content_parts.append('</ul>')
    
    if data['recent_devlog_entries']:
        content_parts.append('<h2>Recent Devlog Activity</h2>')
        content_parts.append('<ul>')
        for entry in data['recent_devlog_entries'][:10]:
            if len(entry) > 100:
                entry = entry[:100] + "..."
            content_parts.append(f'<li>{html_module.escape(entry)}</li>')
        content_parts.append('</ul>')
    
    # Section 4: System Status
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">SYSTEM STATUS</h1>')
    content_parts.append('<p class="section-subtitle">System Health and Status</p>')
    content_parts.append('</div>')
    content_parts.append(f'''
    <div class="status-box">
        <div class="status-title">Repository Status</div>
        <p><strong>Branch:</strong> {html_module.escape(data['git_branch'])}</p>
        <p><strong>Uncommitted Changes:</strong> {data['git_changed']} files</p>
    </div>
    ''')
    
    if data['git_files']:
        content_parts.append('<h2>Changed Files</h2>')
        content_parts.append('<ul>')
        for file_line in data['git_files'][:15]:
            content_parts.append(f'<li><code>{html_module.escape(file_line[:80])}</code></li>')
        content_parts.append('</ul>')
    
    # Section 5: Key Findings
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">KEY FINDINGS</h1>')
    content_parts.append('<p class="section-subtitle">Important Discoveries</p>')
    content_parts.append('</div>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Recent Discoveries</div>
        <p>Key findings from recent work:</p>
        <ul>
            <li>Run-It workflow execution complete (15 phases)</li>
            <li>Security analysis: Strong overall (0 CRITICAL, 2 HIGH, 3 MEDIUM issues)</li>
            <li>Debug logging needs centralization (HIGH priority)</li>
            <li>Effort cost and will to act > time estimates (insight)</li>
            <li>Scientific method tool verified functional</li>
        </ul>
    </div>
    ''')
    
    # Section 6: Next Steps
    content_parts.append('<div class="page-break"></div>')
    content_parts.append('<div class="section-divider">')
    content_parts.append('<h1 class="section-title">NEXT STEPS</h1>')
    content_parts.append('<p class="section-subtitle">Actionable Recommendations</p>')
    content_parts.append('</div>')
    content_parts.append('''
    <div class="note">
        <div class="note-title">Recommended Actions</div>
        <ol>
            <li>Implement debug logging centralization (HIGH priority)</li>
            <li>Add debug log configuration</li>
            <li>Audit subprocess calls (MEDIUM priority)</li>
            <li>Continue Another Cycle execution if desired</li>
        </ol>
    </div>
    ''')
    
    return '\n'.join(content_parts)


def create_dossier(
    title: Optional[str] = None,
    doc_id: Optional[str] = None,
    classification: str = "INTERNAL",
    cover_header: Optional[str] = None,
    cover_metadata: Optional[Dict[str, str]] = None,
    cover_warning: Optional[Dict[str, str]] = None,
    cover_signature: Optional[Dict[str, str]] = None,
    cover_footer: Optional[str] = None,
    output_path: Optional[Path] = None,
    project_path: Optional[Path] = None
) -> Path:
    """Create comprehensive dossier document."""
    # Find project root (look for waft project indicators)
    if project_path is None:
        current = Path.cwd()
        # Look for waft project indicators
        if (current / "src" / "waft").exists() or (current / "pyproject.toml").exists():
            project_path = current
        else:
            # Try parent directories
            for parent in current.parents:
                if (parent / "src" / "waft").exists() or (parent / "pyproject.toml").exists():
                    project_path = parent
                    break
            else:
                project_path = current  # Fallback to current directory
    
    # Gather data
    print("📊 Gathering dossier data...")
    data = gather_dossier_data(project_path)
    
    # Build content
    print("📝 Building dossier content...")
    content = build_dossier_content(data)
    
    # Create brief document
    dossier_title = title or f"Mission Sitrep Dossier - {data['date']}"
    dossier_id = doc_id or f"DOSSIER-{data['date'].replace('-', '')}"
    
    doc = BriefDocument(
        title=dossier_title,
        doc_id=dossier_id,
        subtitle=f"Mission Situation Report - {data['time']}",
        classification=classification,
        cover_header=cover_header or "TELEPORT MASSIVE",
        cover_metadata=cover_metadata or {
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "REPORT_TYPE": "MISSION SITREP",
            "DATE": data['date'],
            "TIME": data['time']
        },
        cover_warning=cover_warning or {
            "message": f"MISSION SITREP - {data['git_changed']} files changed, {data['active_work_efforts_count']} active work efforts",
            "severity": "INFO"
        },
        cover_signature=cover_signature or {
            "role": "AUTHORIZED BY",
            "name": "Site-Delta-9",
            "date": data['date']
        },
        cover_footer=cover_footer or "MISSION SITREP DOSSIER - INTERNAL USE ONLY",
        include_system_status=True,
        chat_context={
            'current_task': 'Mission sitrep and status briefing',
            'recent_topics': ['Run-It workflow', 'Security analysis', 'System status', 'Work efforts'],
            'key_decisions': ['Focus on effort cost and will to act', 'Implement HIGH priority items'],
            'next_steps': ['Debug logging centralization', 'Subprocess audit']
        }
    )
    
    # Add custom content
    doc.content_blocks.append(content)
    
    # Generate PDF
    print("📄 Generating PDF...")
    if output_path:
        pdf_path = doc.generate(output_path=output_path)
    else:
        pdf_path = doc.generate()
    
    print("=" * 60)
    print("✅ Mission Sitrep Dossier Created!")
    print("=" * 60)
    print(f"📄 Output: {pdf_path}")
    print()
    print("Ready for printing and binder storage!")
    
    return pdf_path


def parse_args(args: list) -> dict:
    """Parse command line arguments."""
    kwargs = {}
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg.startswith('title:'):
            kwargs['title'] = arg[6:]
        elif arg.startswith('doc-id:'):
            kwargs['doc_id'] = arg[7:]
        elif arg.startswith('classification:'):
            kwargs['classification'] = arg[16:]
        elif arg.startswith('cover-header:'):
            kwargs['cover_header'] = arg[13:]
        elif arg.startswith('cover-metadata:'):
            try:
                kwargs['cover_metadata'] = json.loads(arg[15:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-metadata: {arg[15:]}")
        elif arg.startswith('cover-warning:'):
            try:
                kwargs['cover_warning'] = json.loads(arg[14:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-warning: {arg[14:]}")
        elif arg.startswith('cover-signature:'):
            try:
                kwargs['cover_signature'] = json.loads(arg[16:])
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON for cover-signature: {arg[16:]}")
        elif arg.startswith('cover-footer:'):
            kwargs['cover_footer'] = arg[13:]
        elif arg.startswith('output:'):
            kwargs['output_path'] = Path(arg[7:])
        elif not arg.startswith('-'):
            pass
        else:
            print(f"⚠️ Unknown option: {arg}")
        
        i += 1
    
    return kwargs


def main():
    """Main CLI entry point."""
    # Parse arguments (empty list if no args provided)
    parsed = parse_args(sys.argv[1:] if len(sys.argv) > 1 else [])
    
    try:
        # Try to find project root
        script_path = Path(__file__).resolve()
        # Script is in scripts/, project root is parent
        potential_project = script_path.parent.parent
        if (potential_project / "src" / "waft").exists():
            parsed['project_path'] = potential_project
        
        output = create_dossier(**parsed)
        print(f"\n✅ Dossier created: {output}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
