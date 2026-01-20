#!/usr/bin/env python3
"""
Generate Empirica TUI Dashboard User Manual

Creates a professional PDF manual using WAFT's field guide template.
"""

from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.templates.field_guide import generate_field_guide


def generate_manual_content() -> str:
    """Generate HTML content for the manual."""
    return """
<style>
  .cover { border: none !important; }
  .warning, .caution, .note, .checklist, .procedure { border: none !important; }
  .procedure { border-left: none !important; }
  table, th, td { border-color: #bbb !important; }
  h2 {
    background: transparent !important;
    color: #000 !important;
    padding: 0.05in 0 !important;
  }
  h3 {
    border-bottom: 1px solid #999 !important;
  }
</style>

<h2>Introduction</h2>
<p>
This manual explains how to use the Empirica TUI dashboards through the WAFT command
<code>waft empirica monitor</code>. It covers prerequisites, setup, command examples,
interactive controls, and troubleshooting.
</p>

<div class="note">
    <div class="note-title">Quick Summary</div>
    The Empirica dashboards provide terminal-based visibility into epistemic state,
    CASCADE workflow progress, and snapshot memory quality.
</div>

<h2>Prerequisites</h2>
<div class="checklist">
  <ul>
    <li>Python 3.11+ installed</li>
    <li>Empirica installed: <code>pip install empirica</code></li>
    <li>WAFT project initialized: <code>waft init</code></li>
    <li>Terminal supports ANSI colors (80x24 minimum)</li>
  </ul>
</div>

<div class="caution">
    <div class="caution-title">Windows Users</div>
    Install curses support: <code>pip install windows-curses</code>
</div>

<h2>Installation &amp; Setup</h2>
<div class="procedure">
    <div class="step">Verify Empirica is installed: <code>empirica --version</code></div>
    <div class="step">Initialize Empirica in the project: <code>waft init</code></div>
    <div class="step">Create a session: <code>waft session create --ai-id claude-code</code></div>
    <div class="step">Launch the dashboard: <code>waft empirica monitor</code></div>
</div>

<h2>Basic Usage</h2>
<pre><code>waft empirica monitor
waft empirica monitor --type cascade
waft empirica monitor --type tui
waft empirica monitor --session-id &lt;SESSION_ID&gt;
waft empirica monitor --path /path/to/project
</code></pre>

<h2>Dashboard Types</h2>
<ul>
  <li><strong>Snapshot Monitor</strong>: Memory quality, compression, and reliability</li>
  <li><strong>CASCADE Monitor</strong>: PREFLIGHT to POSTFLIGHT workflow tracking</li>
  <li><strong>TUI Dashboard</strong>: Full Textual UI with activity and vectors</li>
</ul>

<table>
  <caption>Dashboard Comparison</caption>
  <tr>
    <th>Feature</th>
    <th>Snapshot Monitor</th>
    <th>CASCADE Monitor</th>
    <th>TUI Dashboard</th>
  </tr>
  <tr>
    <td>UI Library</td>
    <td>curses</td>
    <td>curses</td>
    <td>Textual</td>
  </tr>
  <tr>
    <td>Refresh</td>
    <td>Manual (r)</td>
    <td>Event-driven</td>
    <td>Auto (1-5s)</td>
  </tr>
  <tr>
    <td>Best For</td>
    <td>Memory quality</td>
    <td>Workflow tracking</td>
    <td>Full monitoring</td>
  </tr>
</table>

<h2>Interactive Commands (Snapshot Monitor)</h2>
<ul>
  <li><strong>q</strong> - Quit</li>
  <li><strong>r</strong> - Refresh</li>
  <li><strong>f</strong> - Full (toggle snapshot list)</li>
  <li><strong>e</strong> - Export snapshot JSON</li>
  <li><strong>d</strong> - Details view (vectors)</li>
</ul>

<h2>Troubleshooting</h2>
<div class="warning">
    <div class="warning-title">Common Errors</div>
    <ul>
        <li><strong>Empirica not installed</strong>: Run <code>pip install empirica</code></li>
        <li><strong>Empirica not initialized</strong>: Run <code>waft init</code></li>
        <li><strong>No module named 'textual'</strong>: Run <code>pip install textual</code></li>
        <li><strong>No module named 'curses'</strong> (Windows): Run <code>pip install windows-curses</code></li>
        <li><strong>Session not found</strong>: Check with <code>waft session status</code></li>
    </ul>
</div>

<h2>Reference</h2>
<pre><code>waft empirica monitor --type snapshot|cascade|tui
waft empirica monitor --session-id &lt;SESSION_ID&gt;
waft empirica monitor --path /path/to/project
</code></pre>

<h2>Appendix: Glossary</h2>
<table>
  <caption>Key Terms</caption>
  <tr>
    <th>Term</th>
    <th>Definition</th>
  </tr>
  <tr>
    <td>CASCADE</td>
    <td>Empirica workflow: PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT</td>
  </tr>
  <tr>
    <td>Epistemic Vectors</td>
    <td>Quantitative signals of knowledge and uncertainty</td>
  </tr>
  <tr>
    <td>Snapshot</td>
    <td>Saved epistemic state with reliability metrics</td>
  </tr>
</table>
"""


def main() -> None:
    output_dir = Path("docs/manuals")
    output_dir.mkdir(parents=True, exist_ok=True)

    content = generate_manual_content()
    output_path = output_dir / "Empirica_Dashboard_Manual.pdf"

    generate_field_guide(
        title="Empirica TUI Dashboard User Manual",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-EMPIRICA-001",
        subtitle="Monitoring Epistemic State with Terminal Dashboards",
        classification="USER MANUAL",
        issued_by="WAFT Framework",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    print(f"Manual generated: {output_path}")


if __name__ == "__main__":
    main()
