"""
Eldritch Horror Research Journal Template
==========================================

Academic research journal that descends into madness.
Tests typography degradation, reality-breaking layouts, corrupted text.

Features:
- Progressive degradation of formatting
- Strikethrough, scribbles, annotations
- Strange symbols and markings
- Layout that breaks down
- Increasingly unhinged content
- "The abyss stares back" aesthetic
"""

from pathlib import Path
from jinja2 import Template
from weasyprint import HTML


ELDRITCH_JOURNAL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 1in;

            @bottom-center {
                content: "Page " counter(page) " | {{ researcher }}";
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #333;
            }
        }

        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }

        /* Header */
        .journal-header {
            border-bottom: 2px solid #000;
            padding-bottom: 0.15in;
            margin-bottom: 0.3in;
        }

        .researcher-name {
            font-size: 14pt;
            font-weight: bold;
        }

        .institution {
            font-size: 10pt;
            color: #666;
            font-style: italic;
        }

        /* Entry Headers */
        .entry {
            margin: 0.3in 0;
            page-break-inside: avoid;
        }

        .entry-date {
            font-weight: bold;
            font-size: 12pt;
            border-bottom: 1px solid #333;
            padding-bottom: 0.05in;
            margin-bottom: 0.15in;
        }

        /* Progressive degradation styles */

        /* Level 1: Normal */
        .normal {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
        }

        /* Level 2: Stressed - slight degradation */
        .stressed {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            line-height: 1.8;
        }

        /* Level 3: Disturbed - noticeable issues */
        .disturbed {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            line-height: 2.0;
            letter-spacing: 1px;
        }

        /* Level 4: Unraveling - major degradation */
        .unraveling {
            font-family: 'Courier New', monospace;
            font-size: 11pt;
            line-height: 2.2;
            letter-spacing: 2px;
            word-spacing: 5px;
        }

        /* Level 5: Broken - reality breaking down */
        .broken {
            font-family: 'Courier New', monospace;
            font-size: 13pt;
            line-height: 2.5;
            letter-spacing: 3px;
            word-spacing: 8px;
            transform: rotate(-1deg);
        }

        /* Annotations and scribbles */
        .strikethrough {
            text-decoration: line-through;
            color: #666;
        }

        .handwritten {
            font-family: 'Bradley Hand', 'Comic Sans MS', cursive;
            color: #1a5490;
            font-size: 12pt;
        }

        .scribble {
            background: #fffacd;
            border: 1px dashed #999;
            padding: 0.1in;
            margin: 0.1in 0;
            font-family: 'Comic Sans MS', cursive;
            font-size: 10pt;
            transform: rotate(-2deg);
        }

        .scribble::before {
            content: "[Margin note: ";
            font-weight: bold;
        }

        .scribble::after {
            content: "]";
            font-weight: bold;
        }

        /* Warnings and symbols */
        .warning-box {
            border: 3px double #c00;
            background: #ffe;
            padding: 0.15in;
            margin: 0.2in 0;
            text-align: center;
            font-weight: bold;
            font-size: 12pt;
        }

        .symbol {
            font-size: 24pt;
            text-align: center;
            margin: 0.1in 0;
            color: #333;
        }

        /* Reality glitches */
        .glitch {
            position: relative;
            display: inline-block;
        }

        .glitch::before {
            content: attr(data-text);
            position: absolute;
            left: 2px;
            top: 0;
            color: #f0f;
            opacity: 0.3;
        }

        .glitch::after {
            content: attr(data-text);
            position: absolute;
            left: -2px;
            top: 0;
            color: #0ff;
            opacity: 0.3;
        }

        /* Repetition (madness) */
        .repeat {
            opacity: 0.7;
            font-size: 9pt;
            color: #999;
        }

        /* Corrupted text */
        .corrupted {
            font-family: 'Courier New', monospace;
            letter-spacing: 5px;
            font-size: 14pt;
            color: #000;
        }

        /* Obsessive underlining */
        .obsess {
            text-decoration: underline;
            text-decoration-style: double;
            font-weight: bold;
        }

        /* Fear/panic */
        .panic {
            font-size: 16pt;
            font-weight: bold;
            color: #c00;
            letter-spacing: 3px;
        }

        /* Whispers */
        .whisper {
            font-size: 8pt;
            color: #999;
            font-style: italic;
        }

        /* Void/emptiness */
        .void {
            color: #fff;
            background: #000;
            padding: 0.5in;
            text-align: center;
            margin: 0.2in 0;
        }

        /* Blood/stain effect */
        .stain {
            background: #8b0000;
            color: #fff;
            padding: 0.05in 0.1in;
            border-radius: 20%;
            display: inline-block;
        }

        /* Section headers */
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
        }

        /* Paragraphs */
        p {
            margin-bottom: 0.15in;
        }

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="journal-header">
        <div class="researcher-name">{{ researcher }}</div>
        <div class="institution">{{ institution }}</div>
        {% if project %}<div style="font-size: 10pt; margin-top: 0.05in;">Research Project: {{ project }}</div>{% endif %}
    </div>

    <!-- Title -->
    <h1 style="text-align: center; font-size: 18pt; margin-bottom: 0.3in;">{{ title }}</h1>

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Warning (if madness level high) -->
    {% if show_warning %}
    <div class="warning-box" style="margin-top: 0.5in;">
        ⚠ THIS JOURNAL WAS FOUND ABANDONED ⚠<br>
        READER DISCRETION ADVISED
    </div>
    {% endif %}
</body>
</html>
"""


def generate_eldritch_journal(
    title: str,
    content: str,
    output_path: Path,
    researcher: str = "Dr. [REDACTED]",
    institution: str = "Miskatonic University",
    project: str = None,
    show_warning: bool = False
) -> Path:
    """
    Generate an eldritch horror research journal.

    Args:
        title: Journal title
        content: Main content (HTML with degradation classes)
        output_path: Where to save PDF
        researcher: Researcher name
        institution: Research institution
        project: Project name
        show_warning: Show warning box at end

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(ELDRITCH_JOURNAL_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        researcher=researcher,
        institution=institution,
        project=project,
        show_warning=show_warning
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
