#!/usr/bin/env python3
"""
Generate Session Summary PDF

Uses the WAFT Template System (WeasyPrint) to create a professional PDF
from the session summary markdown content.
"""

import sys
from datetime import datetime
from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Read session summary
summary_path = Path(__file__).parent / "documents" / "SESSION_SUMMARY_2026-01-11.md"
continuation_path = Path(__file__).parent / "CONTINUATION_PROMPT.md"

if not summary_path.exists():
    print(f"❌ Error: Session summary not found: {summary_path}")
    sys.exit(1)

summary_content = summary_path.read_text(encoding="utf-8")
continuation_content = (
    continuation_path.read_text(encoding="utf-8") if continuation_path.exists() else ""
)


# Convert markdown to HTML (simple conversion)
def markdown_to_html(md_text: str) -> str:
    """Simple markdown to HTML conversion for session summary."""
    html = md_text

    # Headers
    html = html.replace("### ", "<h3>").replace("\n###", "</h3>\n")
    html = html.replace("## ", "<h2>").replace("\n##", "</h2>\n")
    html = html.replace("# ", "<h1>").replace("\n#", "</h1>\n")

    # Bold
    html = html.replace("**", "<strong>").replace("**", "</strong>")

    # Code blocks
    import re

    html = re.sub(r"```(\w+)?\n(.*?)```", r"<pre><code>\2</code></pre>", html, flags=re.DOTALL)

    # Inline code
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # Lists
    lines = html.split("\n")
    in_list = False
    result = []
    for line in lines:
        if line.strip().startswith("- "):
            if not in_list:
                result.append("<ul>")
                in_list = True
            result.append(f"<li>{line.strip()[2:]}</li>")
        elif line.strip().startswith("1. "):
            if not in_list:
                result.append("<ol>")
                in_list = True
            result.append(f"<li>{line.strip()[3:]}</li>")
        else:
            if in_list:
                result.append("</ul>" if line.strip().startswith("-") else "</ol>")
                in_list = False
            if line.strip() and not line.strip().startswith("#"):
                result.append(f"<p>{line}</p>")
            else:
                result.append(line)
    html = "\n".join(result)

    # Horizontal rules
    html = html.replace("---", "<hr>")

    return html


# Create HTML document
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WAFT Mac Shortcuts Research - Session Summary</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;

            @top-center {
                content: "WAFT Research Session Summary";
                font-family: 'Helvetica', sans-serif;
                font-size: 9pt;
                color: #666;
            }

            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Helvetica', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        @page :first {
            @top-center { content: none; }
        }

        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }

        h1 {
            font-family: 'Helvetica', sans-serif;
            font-size: 20pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            border-bottom: 3px solid #000;
            padding-bottom: 0.1in;
        }

        h2 {
            font-family: 'Helvetica', sans-serif;
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            color: #2c3e50;
        }

        h3 {
            font-family: 'Helvetica', sans-serif;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background: #f0f0f0;
            padding: 0.05in;
            border-radius: 3px;
        }

        pre {
            background: #f5f5f5;
            border-left: 4px solid #3498db;
            padding: 0.2in;
            margin: 0.2in 0;
            overflow-x: auto;
        }

        ul, ol {
            margin-left: 0.3in;
            margin-bottom: 0.2in;
        }

        li {
            margin-bottom: 0.1in;
        }

        hr {
            border: none;
            border-top: 2px solid #ccc;
            margin: 0.3in 0;
        }

        .status-badge {
            display: inline-block;
            padding: 0.05in 0.15in;
            background: #27ae60;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            font-size: 9pt;
        }
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 0.5in;">
        <h1 style="border: none; margin-top: 0;">WAFT Mac Shortcuts Research</h1>
        <h2 style="color: #666; font-size: 14pt; margin-top: 0.1in;">Session Summary</h2>
        <p style="color: #999; margin-top: 0.2in;">{{ date }}</p>
    </div>

    {{ summary_html | safe }}

    {% if continuation_html %}
    <div style="page-break-before: always; margin-top: 0.5in;">
        <h1>Continuation Prompt</h1>
        {{ continuation_html | safe }}
    </div>
    {% endif %}
</body>
</html>
"""

# Convert markdown to HTML
summary_html = markdown_to_html(summary_content)
continuation_html = markdown_to_html(continuation_content) if continuation_content else ""

# Render template
template = Template(html_template)
html_output = template.render(
    date=datetime.now().strftime("%B %d, %Y"),
    summary_html=summary_html,
    continuation_html=continuation_html,
)

# Generate PDF
output_path = Path(__file__).parent / "SESSION_SUMMARY_2026-01-11.pdf"
output_path.parent.mkdir(parents=True, exist_ok=True)

HTML(string=html_output).write_pdf(str(output_path))

print(f"✅ Generated: {output_path}")
print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
