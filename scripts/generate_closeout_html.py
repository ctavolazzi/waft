#!/usr/bin/env python3
"""
Generate Closeout HTML Report
=============================

Creates a beautiful HTML closeout report inspired by the show_me design.
Uses the same dark theme, typography, and layout patterns.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_closeout_html(
    accomplishments: List[str] = None,
    failures: List[str] = None,
    planned: List[str] = None,
    unplanned: List[str] = None,
    errors: List[Dict[str, str]] = None,
    oversights: List[str] = None,
    lessons: List[str] = None,
    next_steps: List[str] = None,
    metrics: Dict[str, Any] = None,
    recommendations: List[str] = None,
    session_focus: str = "Session work",
    timestamp: str = None,
    output_path: Optional[Path] = None
) -> Path:
    """
    Generate HTML closeout report using show_me design inspiration.
    
    Args:
        accomplishments: List of completed items
        failures: List of incomplete items
        planned: List of planned items
        unplanned: List of unplanned items
        errors: List of dicts with 'error', 'cause', 'fix', 'status'
        oversights: List of things missed
        lessons: List of lessons learned
        next_steps: List of next steps
        metrics: Dict of metrics (files_created, files_modified, etc.)
        recommendations: List of recommendations
        session_focus: Brief description of session
        timestamp: Timestamp string (defaults to now)
        output_path: Output file path (defaults to _work_efforts/showcase_documents/)
    
    Returns:
        Path to generated HTML file
    """
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if output_path is None:
        output_path = Path("_work_efforts/showcase_documents") / f"CLOSEOUT_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Default values
    accomplishments = accomplishments or []
    failures = failures or []
    planned = planned or []
    unplanned = unplanned or []
    errors = errors or []
    oversights = oversights or []
    lessons = lessons or []
    next_steps = next_steps or []
    metrics = metrics or {}
    recommendations = recommendations or []
    
    # Generate HTML content sections
    html_content = generate_closeout_content(
        accomplishments, failures, planned, unplanned, errors,
        oversights, lessons, next_steps, metrics, recommendations,
        session_focus, timestamp
    )
    
    # Use show_me WAFT HTML template
    from scripts.show_me import generate_waft_html
    
    full_html = generate_waft_html(
        html_content=html_content,
        title="Session Closeout Report",
        timestamp=timestamp,
        session_history=None
    )
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return output_path


def generate_closeout_content(
    accomplishments: List[str],
    failures: List[str],
    planned: List[str],
    unplanned: List[str],
    errors: List[Dict[str, str]],
    oversights: List[str],
    lessons: List[str],
    next_steps: List[str],
    metrics: Dict[str, Any],
    recommendations: List[str],
    session_focus: str,
    timestamp: str
) -> str:
    """Generate the HTML content for closeout report."""
    
    content = f"""
<div id='abstract'></div>
<div class="header-section">
<div class="header-meta">
<div class="meta-item"><span class="meta-label">Generated:</span> {timestamp}</div>
<div class="meta-item"><span class="meta-label">Session Focus:</span> {session_focus}</div>
</div>
</div>

<div class="abstract-section-header">
<h2>Abstract</h2>
<button class="abstract-copy-btn" onclick="copyAbstract()" title="Copy abstract to clipboard">
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 2C3.44772 2 3 2.44772 3 3V11C3 11.5523 3.44772 12 4 12H5V13C5 13.5523 5.44772 14 6 14H13C13.5523 14 14 13.5523 14 13V6C14 5.44772 13.5523 5 13 5H12V3C12 2.44772 11.5523 2 11 2H4Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
<path d="M6 5H11C11.5523 5 12 5.44772 12 6V11H6V5Z" stroke="currentColor" stroke-width="1.2" fill="none"/>
</svg>
</button>
</div>

<div class="abstract-box" id="abstract-content">
<strong>Session Summary:</strong> {session_focus}

<strong>{len(accomplishments)} accomplishments</strong> completed. <strong>{len(failures)} items</strong> not completed. <strong>{len(errors)} errors</strong> encountered and resolved. <strong>{len(lessons)} lessons</strong> learned. <strong>{len(next_steps)} next steps</strong> identified.
</div>

## Quick Stats

<div class="stats-grid">
<div class="stat-card">
<span class="stat-value">{len(accomplishments)}</span>
<span class="stat-label">Accomplished</span>
</div>
<div class="stat-card">
<span class="stat-value">{len(failures)}</span>
<span class="stat-label">Not Completed</span>
</div>
<div class="stat-card">
<span class="stat-value">{len(errors)}</span>
<span class="stat-label">Errors Fixed</span>
</div>
<div class="stat-card">
<span class="stat-value">{len(lessons)}</span>
<span class="stat-label">Lessons Learned</span>
</div>
</div>

## Everything Accomplished ✅

<div class="content-card">
<ul>
"""
    
    for acc in accomplishments:
        content += f"<li>✅ {acc}</li>\n"
    
    content += """</ul>
</div>

## Everything Failed To Do ❌

<div class="content-card">
<ul>
"""
    
    for fail in failures:
        content += f"<li>❌ {fail}</li>\n"
    
    content += """</ul>
</div>

## Everything Planned 📋

<div class="content-card">
<ul>
"""
    
    for plan in planned:
        content += f"<li>📋 {plan}</li>\n"
    
    content += """</ul>
</div>

## Everything Failed To Plan For ⚠️

<div class="content-card">
<ul>
"""
    
    for unplan in unplanned:
        content += f"<li>⚠️ {unplan}</li>\n"
    
    content += """</ul>
</div>

## Errors and Mistakes 🔴

<div class="content-card">
<table>
<thead>
<tr>
<th>Error</th>
<th>Cause</th>
<th>Fix</th>
<th>Status</th>
</tr>
</thead>
<tbody>
"""
    
    for error in errors:
        error_text = error.get('error', 'N/A')
        cause = error.get('cause', 'N/A')
        fix = error.get('fix', 'N/A')
        status = error.get('status', 'N/A')
        content += f"<tr><td>{error_text}</td><td>{cause}</td><td>{fix}</td><td>{status}</td></tr>\n"
    
    content += """</tbody>
</table>
</div>

## Oversights 👁️

<div class="content-card">
<ul>
"""
    
    for oversight in oversights:
        content += f"<li>👁️ {oversight}</li>\n"
    
    content += """</ul>
</div>

## Lessons Learned 📚

<div class="content-card">
<ul>
"""
    
    for lesson in lessons:
        content += f"<li>📚 {lesson}</li>\n"
    
    content += """</ul>
</div>

## Next Steps 🎯

<div class="content-card">
<ol>
"""
    
    for step in next_steps:
        content += f"<li>{step}</li>\n"
    
    content += """</ol>
</div>

## Metrics & Statistics 📊

<div class="content-card">
<table>
<thead>
<tr>
<th>Metric</th>
<th>Value</th>
</tr>
</thead>
<tbody>
"""
    
    for key, value in metrics.items():
        content += f"<tr><td><strong>{key.replace('_', ' ').title()}</strong></td><td>{value}</td></tr>\n"
    
    content += """</tbody>
</table>
</div>

## Recommendations 💡

<div class="content-card">
<ul>
"""
    
    for rec in recommendations:
        content += f"<li>💡 {rec}</li>\n"
    
    content += """</ul>
</div>

## Conclusion

<div class="abstract-box">
<p><strong>Session Summary:</strong> {session_focus}</p>
<p>This session resulted in <strong>{len(accomplishments)} accomplishments</strong>, with <strong>{len(failures)} items</strong> not completed. <strong>{len(errors)} errors</strong> were encountered and resolved. <strong>{len(lessons)} key lessons</strong> were learned for future improvement.</p>
<p><strong>Key Achievement:</strong> The session successfully addressed the primary objectives while identifying areas for continued development.</p>
<p><strong>Key Learning:</strong> {lessons[0] if lessons else 'Continuous improvement through reflection and documentation.'}</p>
</div>
"""
    
    return content


if __name__ == "__main__":
    # Example usage
    from pathlib import Path
    
    print("=" * 80)
    print("Generating Closeout HTML Report")
    print("=" * 80)
    print()
    
    # Example data
    html_path = generate_closeout_html(
        accomplishments=[
            "Added copy button to Abstract section",
            "Created /thank-you command",
            "Implemented subtle, chill SVG icon design",
            "Added visual feedback for copy action"
        ],
        failures=[
            "Full closeout automation (needs session analysis)",
            "PDF generation from HTML (can be added)"
        ],
        planned=[
            "Copy button implementation",
            "Thank you command creation"
        ],
        unplanned=[
            "User requested HTML closeout report",
            "Design inspiration from show_me"
        ],
        errors=[
            {
                "error": "Markdown vs HTML structure",
                "cause": "Mixed markdown and HTML in header",
                "fix": "Used raw HTML for flex container",
                "status": "✅ Fixed"
            }
        ],
        oversights=[
            "Didn't initially show progress as requested",
            "Could have created preview earlier"
        ],
        lessons=[
            "User feedback is critical - 'keep showing me' was important",
            "Preview files help demonstrate features before full integration",
            "Subtle design matters - low opacity creates better UX"
        ],
        next_steps=[
            "Test copy button in actual show_me output",
            "Consider adding copy buttons to other sections",
            "Add keyboard shortcut support"
        ],
        metrics={
            "files_created": 2,
            "files_modified": 2,
            "lines_added": 80,
            "features_completed": 1
        },
        recommendations=[
            "Use HTML closeout reports for visual documentation",
            "Continue using show_me design patterns for consistency",
            "Add more interactive elements to closeout reports"
        ],
        session_focus="Abstract Copy Button & Closeout HTML Report",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    print(f"✅ Generated: {html_path}")
    print(f"   Size: {html_path.stat().st_size / 1024:.1f} KB")
    print()
    print("=" * 80)
    print("To open the HTML, run:")
    print(f"   open {html_path}")
    print("=" * 80)
