#!/usr/bin/env python3
"""
WAFT Status Check and Documentation Generator
============================================

Checks current system status and can generate documentation at multiple
complexity levels (layman, professional, scientist) about what's happening
right now.

Usage:
    python scripts/waft_status.py                    # Status check only
    python scripts/waft_status.py --docs             # Generate all docs
    python scripts/waft_status.py --docs --level layman  # Specific level
    python scripts/waft_status.py --docs --printer-friendly
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent.parent))


def get_git_status() -> Dict[str, Any]:
    """Get comprehensive git status."""
    status = {
        "initialized": False,
        "branch": None,
        "uncommitted_files": [],
        "staged_files": [],
        "unstaged_files": [],
        "commits_ahead": 0,
        "commits_behind": 0,
        "recent_commits": [],
    }
    
    try:
        # Check if git is initialized
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode != 0:
            return status
        
        status["initialized"] = True
        
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            status["branch"] = result.stdout.strip()
        
        # Get uncommitted files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line:
                    status_code = line[:2]
                    filename = line[3:]
                    status["uncommitted_files"].append(filename)
                    if status_code[0] != " ":
                        status["staged_files"].append(filename)
                    if status_code[1] != " ":
                        status["unstaged_files"].append(filename)
        
        # Get commits ahead/behind
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                status["commits_ahead"] = int(parts[0])
                status["commits_behind"] = int(parts[1])
        
        # Get recent commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-10", "--no-decorate"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            status["recent_commits"] = [
                line.strip() for line in result.stdout.strip().split("\n") if line
            ]
    
    except Exception as e:
        print(f"Warning: Error checking git status: {e}")
    
    return status


def get_work_efforts() -> Dict[str, Any]:
    """Get work efforts status."""
    efforts = {
        "active": [],
        "recent": [],
        "completed": [],
        "count": 0,
    }
    
    work_efforts_dir = Path("_work_efforts")
    if not work_efforts_dir.exists():
        return efforts
    
    # Look for work effort directories (WE-YYMMDD-* pattern)
    for item in work_efforts_dir.iterdir():
        if item.is_dir() and item.name.startswith("WE-"):
            efforts["count"] += 1
            # Check for index file to determine status
            index_file = item / f"{item.name}_index.md"
            if index_file.exists():
                efforts["active"].append(item.name)
            else:
                efforts["recent"].append(item.name)
    
    return efforts


def get_project_health() -> Dict[str, Any]:
    """Get project health status."""
    health = {
        "pyrite_valid": False,
        "lock_exists": False,
        "structure_valid": False,
    }
    
    # Check _pyrite structure
    pyrite_dir = Path("_pyrite")
    if pyrite_dir.exists():
        health["pyrite_valid"] = True
        if (pyrite_dir / "active").exists() and (pyrite_dir / "backlog").exists():
            health["structure_valid"] = True
    
    # Check uv.lock
    if Path("uv.lock").exists():
        health["lock_exists"] = True
    
    return health


def get_recent_activity() -> Dict[str, Any]:
    """Get recent activity information."""
    activity = {
        "devlog_entries": [],
        "recent_files": [],
    }
    
    # Get recent devlog entries
    devlog = Path("_work_efforts/devlog.md")
    if devlog.exists():
        content = devlog.read_text()
        lines = content.split("\n")
        # Get last 5 entries (simple approach - look for date headers)
        recent_lines = []
        for line in reversed(lines[-100:]):  # Check last 100 lines
            if line.startswith("## ") and any(char.isdigit() for char in line):
                recent_lines.append(line)
                if len(recent_lines) >= 5:
                    break
        activity["devlog_entries"] = list(reversed(recent_lines))
    
    return activity


def check_status() -> Dict[str, Any]:
    """Perform comprehensive status check."""
    print("Checking system status...")
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "git": get_git_status(),
        "work_efforts": get_work_efforts(),
        "project_health": get_project_health(),
        "recent_activity": get_recent_activity(),
    }
    
    return status


def display_status(status: Dict[str, Any]):
    """Display status summary."""
    print("\n" + "=" * 60)
    print("WAFT System Status")
    print("=" * 60)
    print(f"Timestamp: {status['timestamp']}")
    print()
    
    # Git Status
    print("Git Status:")
    git = status["git"]
    if git["initialized"]:
        print(f"  Branch: {git['branch']}")
        print(f"  Uncommitted files: {len(git['uncommitted_files'])}")
        print(f"  Staged: {len(git['staged_files'])}, Unstaged: {len(git['unstaged_files'])}")
        print(f"  Commits ahead: {git['commits_ahead']}, behind: {git['commits_behind']}")
        if git["recent_commits"]:
            print(f"  Recent commits: {len(git['recent_commits'])}")
    else:
        print("  Git not initialized")
    print()
    
    # Work Efforts
    print("Work Efforts:")
    we = status["work_efforts"]
    print(f"  Total: {we['count']}")
    print(f"  Active: {len(we['active'])}")
    print(f"  Recent: {len(we['recent'])}")
    print()
    
    # Project Health
    print("Project Health:")
    health = status["project_health"]
    print(f"  _pyrite valid: {health['pyrite_valid']}")
    print(f"  Structure valid: {health['structure_valid']}")
    print(f"  uv.lock exists: {health['lock_exists']}")
    print()
    
    # Recent Activity
    print("Recent Activity:")
    activity = status["recent_activity"]
    print(f"  Devlog entries: {len(activity['devlog_entries'])}")
    print()
    
    print("=" * 60)


def generate_status_docs(status: Dict[str, Any], level: Optional[str] = None, printer_friendly: bool = False):
    """Generate status documentation at specified level(s)."""
    from examples.generate_waft_field_guide_printer_friendly import generate_field_guide_printer_friendly
    from examples.generate_waft_field_guide import generate_field_guide
    
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    levels = ["layman", "professional", "scientist"] if level is None else [level]
    
    for doc_level in levels:
        print(f"\nGenerating {doc_level} level status documentation...")
        
        content = format_status_content(status, doc_level)
        
        output_path = output_dir / f"WAFT_Status_{doc_level.capitalize()}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        if printer_friendly:
            output_path = output_dir / f"WAFT_Status_{doc_level.capitalize()}_{datetime.now().strftime('%Y-%m-%d')}_PrinterFriendly.pdf"
        
        if printer_friendly:
            generate_field_guide_printer_friendly(
                title="WAFT SYSTEM STATUS",
                content=content,
                output_path=output_path,
                series="STATUS REPORT",
                number=f"SR-{datetime.now().strftime('%Y%m%d')}",
                subtitle=f"Level {doc_level.capitalize()}: Current System State",
                classification="INTERNAL",
                issued_by="WAFT System",
                date=datetime.now().strftime("%B %d, %Y")
            )
        else:
            from src.waft.templates.field_guide import generate_field_guide
            generate_field_guide(
                title="WAFT SYSTEM STATUS",
                content=content,
                output_path=output_path,
                series="STATUS REPORT",
                number=f"SR-{datetime.now().strftime('%Y%m%d')}",
                subtitle=f"Level {doc_level.capitalize()}: Current System State",
                classification="INTERNAL",
                issued_by="WAFT System",
                date=datetime.now().strftime("%B %d, %Y")
            )
        
        print(f"✓ Generated: {output_path.name}")


def format_status_content(status: Dict[str, Any], level: str) -> str:
    """Format status content for specified complexity level."""
    git = status["git"]
    we = status["work_efforts"]
    health = status["project_health"]
    activity = status["recent_activity"]
    
    if level == "layman":
        return format_layman_content(status, git, we, health, activity)
    elif level == "professional":
        return format_professional_content(status, git, we, health, activity)
    else:  # scientist
        return format_scientist_content(status, git, we, health, activity)


def format_layman_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict) -> str:
    """Format status for layman audience."""
    return f"""
<h2>What's Happening Right Now</h2>

<p>
This report shows what the WAFT system is doing right now. Think of it like a 
health check for a computer program - we're checking to see how things are going.
</p>

<h2>Current Work Status</h2>

<p>
The system is currently working on <strong>{we['count']}</strong> different projects.
Of these, <strong>{len(we['active'])}</strong> are actively being worked on right now.
</p>

<div class="note">
    <div class="note-title">Simple Explanation</div>
    Think of work efforts like different tasks or projects. Some are being actively 
    worked on, some are waiting, and some are finished.
</div>

<h2>Code Changes</h2>

<p>
The system has <strong>{len(git['uncommitted_files'])}</strong> files that have been 
changed but not yet saved permanently. This is normal when work is in progress.
</p>

{'<div class="warning"><div class="warning-title">Attention Needed</div>There are uncommitted changes that should be saved soon.</div>' if len(git['uncommitted_files']) > 10 else ''}

<h2>System Health</h2>

<table>
    <caption>Health Check Results</caption>
    <tr>
        <th>Check</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Project Structure</td>
        <td>{'✅ Good' if health['structure_valid'] else '⚠️ Needs Attention'}</td>
    </tr>
    <tr>
        <td>Dependencies</td>
        <td>{'✅ Good' if health['lock_exists'] else '⚠️ Needs Attention'}</td>
    </tr>
</table>

<h2>Recent Activity</h2>

<p>
The system has been active recently with <strong>{len(activity['devlog_entries'])}</strong> 
recent log entries documenting work progress.
</p>

<h2>Summary</h2>

<p>
Overall, the system is {'healthy and active' if health['structure_valid'] and len(git['uncommitted_files']) < 20 else 'needs some attention'}. 
Work is progressing on multiple projects, and the system structure is {'in good shape' if health['structure_valid'] else 'needing review'}.
</p>
"""


def format_professional_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict) -> str:
    """Format status for professional audience."""
    return f"""
<h2>System Status Report</h2>

<p><strong>Report Date:</strong> {status['timestamp']}</p>

<h2>Git Repository Status</h2>

<h3>Branch Information</h3>
<p><strong>Current Branch:</strong> {git['branch'] or 'N/A'}</p>
<p><strong>Commits Ahead:</strong> {git['commits_ahead']}</p>
<p><strong>Commits Behind:</strong> {git['commits_behind']}</p>

<h3>Uncommitted Changes</h3>
<p><strong>Total Uncommitted Files:</strong> {len(git['uncommitted_files'])}</p>
<p><strong>Staged Files:</strong> {len(git['staged_files'])}</p>
<p><strong>Unstaged Files:</strong> {len(git['unstaged_files'])}</p>

{'<div class="warning"><div class="warning-title">Warning</div>Large number of uncommitted files detected. Consider committing changes.</div>' if len(git['uncommitted_files']) > 20 else ''}

<h3>Recent Commits</h3>
<ul>
{''.join([f'<li>{commit}</li>' for commit in git['recent_commits'][:5]])}
</ul>

<h2>Work Efforts Status</h2>

<table>
    <caption>Work Efforts Breakdown</caption>
    <tr>
        <th>Category</th>
        <th>Count</th>
    </tr>
    <tr>
        <td>Total Work Efforts</td>
        <td>{we['count']}</td>
    </tr>
    <tr>
        <td>Active</td>
        <td>{len(we['active'])}</td>
    </tr>
    <tr>
        <td>Recent</td>
        <td>{len(we['recent'])}</td>
    </tr>
</table>

<h2>Project Health Metrics</h2>

<table>
    <caption>Health Check Results</caption>
    <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>_pyrite Structure</td>
        <td>{'✅ Valid' if health['pyrite_valid'] else '❌ Invalid'}</td>
        <td>{'Structure intact' if health['pyrite_valid'] else 'Missing or corrupted'}</td>
    </tr>
    <tr>
        <td>Directory Structure</td>
        <td>{'✅ Valid' if health['structure_valid'] else '❌ Invalid'}</td>
        <td>{'active/ and backlog/ exist' if health['structure_valid'] else 'Missing required directories'}</td>
    </tr>
    <tr>
        <td>Dependency Lock</td>
        <td>{'✅ Present' if health['lock_exists'] else '❌ Missing'}</td>
        <td>{'uv.lock file exists' if health['lock_exists'] else 'uv.lock not found'}</td>
    </tr>
</table>

<h2>Recent Activity</h2>

<p><strong>Devlog Entries:</strong> {len(activity['devlog_entries'])} recent entries</p>

<h2>Analysis</h2>

<div class="note">
    <div class="note-title">Status Summary</div>
    <ul>
        <li>Git repository is {'synchronized' if git['commits_ahead'] == 0 and git['commits_behind'] == 0 else 'out of sync'}</li>
        <li>Project structure is {'healthy' if health['structure_valid'] else 'needs attention'}</li>
        <li>Work effort activity: {len(we['active'])} active efforts</li>
        <li>Uncommitted changes: {len(git['uncommitted_files'])} files</li>
    </ul>
</div>
"""


def format_scientist_content(status: Dict, git: Dict, we: Dict, health: Dict, activity: Dict) -> str:
    """Format status for scientist audience."""
    return f"""
<h2>Comprehensive System Status Analysis</h2>

<p><strong>Analysis Timestamp:</strong> {status['timestamp']}</p>
<p><strong>Analysis Depth:</strong> Research-Level</p>

<h2>Git Repository Statistical Analysis</h2>

<h3>Branch State</h3>
<table>
    <caption>Branch Metrics</caption>
    <tr>
        <th>Metric</th>
        <th>Value</th>
        <th>Analysis</th>
    </tr>
    <tr>
        <td>Current Branch</td>
        <td>{git['branch'] or 'N/A'}</td>
        <td>{'Main branch' if git['branch'] == 'main' or git['branch'] == 'master' else 'Feature branch'}</td>
    </tr>
    <tr>
        <td>Divergence (Ahead)</td>
        <td>{git['commits_ahead']}</td>
        <td>{'Synchronized' if git['commits_ahead'] == 0 else 'Local commits pending push'}</td>
    </tr>
    <tr>
        <td>Divergence (Behind)</td>
        <td>{git['commits_behind']}</td>
        <td>{'Synchronized' if git['commits_behind'] == 0 else 'Remote commits pending pull'}</td>
    </tr>
</table>

<h3>Change Set Analysis</h3>

<p><strong>Change Set Statistics:</strong></p>
<ul>
    <li>Total uncommitted files: {len(git['uncommitted_files'])}</li>
    <li>Staged files: {len(git['staged_files'])} ({len(git['staged_files'])/max(len(git['uncommitted_files']),1)*100:.1f}% of changes)</li>
    <li>Unstaged files: {len(git['unstaged_files'])} ({len(git['unstaged_files'])/max(len(git['uncommitted_files']),1)*100:.1f}% of changes)</li>
</ul>

<div class="caution">
    <div class="caution-title">Change Set Risk Assessment</div>
    {'High risk: Large number of uncommitted changes detected. Consider incremental commits.' if len(git['uncommitted_files']) > 20 else 'Low risk: Manageable number of uncommitted changes.'}
</div>

<h3>Commit History Analysis</h3>

<p><strong>Recent Commit Patterns:</strong></p>
<ul>
{''.join([f'<li>{commit}</li>' for commit in git['recent_commits'][:10]])}
</ul>

<h2>Work Efforts Statistical Analysis</h2>

<table>
    <caption>Work Efforts Distribution</caption>
    <tr>
        <th>Category</th>
        <th>Count</th>
        <th>Percentage</th>
        <th>Trend Analysis</th>
    </tr>
    <tr>
        <td>Total Work Efforts</td>
        <td>{we['count']}</td>
        <td>100%</td>
        <td>Baseline</td>
    </tr>
    <tr>
        <td>Active Efforts</td>
        <td>{len(we['active'])}</td>
        <td>{len(we['active'])/max(we['count'],1)*100:.1f}%</td>
        <td>{'High activity' if len(we['active'])/max(we['count'],1) > 0.5 else 'Moderate activity'}</td>
    </tr>
    <tr>
        <td>Recent Efforts</td>
        <td>{len(we['recent'])}</td>
        <td>{len(we['recent'])/max(we['count'],1)*100:.1f}%</td>
        <td>In progress</td>
    </tr>
</table>

<h2>Project Health Deep Analysis</h2>

<table>
    <caption>Health Metrics with Risk Assessment</caption>
    <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Risk Level</th>
        <th>Recommendation</th>
    </tr>
    <tr>
        <td>_pyrite Structure</td>
        <td>{'✅ Valid' if health['pyrite_valid'] else '❌ Invalid'}</td>
        <td>{'Low' if health['pyrite_valid'] else 'High'}</td>
        <td>{'No action needed' if health['pyrite_valid'] else 'Run waft init to repair'}</td>
    </tr>
    <tr>
        <td>Directory Structure</td>
        <td>{'✅ Valid' if health['structure_valid'] else '❌ Invalid'}</td>
        <td>{'Low' if health['structure_valid'] else 'High'}</td>
        <td>{'No action needed' if health['structure_valid'] else 'Verify _pyrite structure'}</td>
    </tr>
    <tr>
        <td>Dependency Lock</td>
        <td>{'✅ Present' if health['lock_exists'] else '❌ Missing'}</td>
        <td>{'Low' if health['lock_exists'] else 'Medium'}</td>
        <td>{'No action needed' if health['lock_exists'] else 'Run uv sync to generate lock'}</td>
    </tr>
</table>

<h2>Activity Pattern Analysis</h2>

<p><strong>Recent Activity Metrics:</strong></p>
<ul>
    <li>Devlog entries in recent period: {len(activity['devlog_entries'])}</li>
    <li>Activity level: {'High' if len(activity['devlog_entries']) >= 3 else 'Moderate' if len(activity['devlog_entries']) >= 1 else 'Low'}</li>
</ul>

<h2>Predictive Indicators</h2>

<div class="note">
    <div class="note-title">System Trajectory Analysis</div>
    <ul>
        <li><strong>Development Velocity:</strong> {'High' if len(git['recent_commits']) >= 5 else 'Moderate' if len(git['recent_commits']) >= 2 else 'Low'}</li>
        <li><strong>Work Distribution:</strong> {len(we['active'])} active efforts indicate {'focused development' if len(we['active']) <= 3 else 'parallel development'}</li>
        <li><strong>Change Management:</strong> {len(git['uncommitted_files'])} uncommitted files suggest {'incremental development' if len(git['uncommitted_files']) < 10 else 'batch development pattern'}</li>
    </ul>
</div>

<h2>Research-Level Insights</h2>

<div class="highlight-box">
    <h3>Key Observations</h3>
    <ul>
        <li>System state indicates {'stable development' if health['structure_valid'] and len(git['uncommitted_files']) < 15 else 'active development with potential risk'}</li>
        <li>Work effort distribution shows {'balanced workload' if 0.3 <= len(we['active'])/max(we['count'],1) <= 0.7 else 'concentrated or distributed workload'}</li>
        <li>Git activity pattern suggests {'regular commit cadence' if len(git['recent_commits']) >= 3 else 'irregular or new development cycle'}</li>
    </ul>
</div>
"""


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check WAFT system status and optionally generate documentation'
    )
    parser.add_argument('--docs', action='store_true', help='Generate status documentation')
    parser.add_argument('--level', choices=['layman', 'professional', 'scientist'], help='Documentation level (requires --docs)')
    parser.add_argument('--printer-friendly', action='store_true', help='Generate printer-friendly versions')
    parser.add_argument('--focus', help='Focus on specific area')
    
    args = parser.parse_args()
    
    # Check status
    status = check_status()
    
    # Display status
    display_status(status)
    
    # Generate docs if requested
    if args.docs:
        generate_status_docs(status, level=args.level, printer_friendly=args.printer_friendly)
        print("\n✓ Status documentation generated")
    
    print()


if __name__ == '__main__':
    main()
