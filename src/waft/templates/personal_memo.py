"""
Personal Memo/Notes Template
=============================

Informal personal notes, memos, diary entries from TELEPORT MASSIVE staff.
Handwritten aesthetic, personal voice, worldbuilding through character.

Features:
- Handwritten font simulation
- Informal layout
- Personal letterhead
- Sticky note style
- Coffee stain optional :)
- Character voice
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

PERSONAL_MEMO_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 1in;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #222;
        }

        /* Memo Header */
        .memo-header {
            border-bottom: 2px solid #333;
            margin-bottom: 0.3in;
            padding-bottom: 0.15in;
        }

        .from-line {
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 0.08in;
        }

        .to-line {
            margin-bottom: 0.05in;
        }

        .date-line {
            margin-bottom: 0.05in;
            font-style: italic;
            color: #666;
        }

        .re-line {
            margin-top: 0.1in;
            font-weight: bold;
        }

        /* Sticky Note Style */
        .sticky-note {
            background: #ffc;
            border: 1px solid #cc9;
            padding: 0.2in;
            margin: 0.2in 0;
            box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            font-family: 'Comic Sans MS', 'Courier New', monospace;
            font-size: 10pt;
            page-break-inside: avoid;
        }

        .sticky-note::before {
            content: "📌 ";
        }

        /* Handwritten Note */
        .handwritten {
            font-family: 'Bradley Hand', 'Comic Sans MS', cursive;
            font-size: 12pt;
            line-height: 1.8;
            color: #1a5490;
        }

        /* Personal Letterhead */
        .letterhead {
            text-align: center;
            border-bottom: 1px solid #666;
            padding-bottom: 0.15in;
            margin-bottom: 0.25in;
        }

        .letterhead-name {
            font-weight: bold;
            font-size: 14pt;
        }

        .letterhead-title {
            font-size: 10pt;
            color: #666;
        }

        .letterhead-dept {
            font-size: 9pt;
            color: #999;
            font-style: italic;
        }

        /* Section Headers */
        h2 {
            font-size: 13pt;
            font-weight: bold;
            border-bottom: 1px solid #999;
            padding-bottom: 0.05in;
            margin-top: 0.25in;
            margin-bottom: 0.12in;
        }

        h3 {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 0.18in;
            margin-bottom: 0.08in;
        }

        /* Paragraphs */
        p {
            margin-bottom: 0.15in;
            text-align: left;
        }

        /* Highlighted Text */
        .highlight {
            background: #ff9;
            padding: 0.02in 0.05in;
        }

        /* Confidential Stamp */
        .stamp {
            color: #c00;
            font-weight: bold;
            font-size: 14pt;
            text-transform: uppercase;
            border: 3px solid #c00;
            padding: 0.1in 0.2in;
            display: inline-block;
            transform: rotate(-15deg);
            opacity: 0.7;
            margin: 0.2in 0;
        }

        /* Signature */
        .signature {
            margin-top: 0.4in;
            font-family: 'Bradley Hand', cursive;
            font-size: 14pt;
        }

        /* Lists */
        ul {
            margin-left: 0.3in;
        }

        li {
            margin-bottom: 0.08in;
        }

        /* Quote/Aside */
        .aside {
            border-left: 3px solid #ccc;
            padding-left: 0.15in;
            margin: 0.15in 0;
            font-style: italic;
            color: #666;
        }

        /* PS Section */
        .ps {
            margin-top: 0.3in;
            font-style: italic;
            color: #666;
        }

        .ps::before {
            content: "P.S. ";
            font-weight: bold;
            color: #000;
        }

        /* Scribble/Strikethrough */
        .scribble {
            text-decoration: line-through;
            color: #999;
        }

        /* Underline */
        .underline {
            text-decoration: underline;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <!-- Letterhead (if formal) -->
    {% if use_letterhead %}
    <div class="letterhead">
        <div class="letterhead-name">{{ from_name }}</div>
        {% if from_title %}<div class="letterhead-title">{{ from_title }}</div>{% endif %}
        {% if department %}<div class="letterhead-dept">{{ department }}</div>{% endif %}
    </div>
    {% endif %}

    <!-- Memo Header (if memo style) -->
    {% if memo_style %}
    <div class="memo-header">
        <div class="from-line">FROM: {{ from_name }}</div>
        {% if to_name %}<div class="to-line">TO: {{ to_name }}</div>{% endif %}
        {% if date %}<div class="date-line">DATE: {{ date }}</div>{% endif %}
        {% if subject %}<div class="re-line">RE: {{ subject }}</div>{% endif %}
    </div>
    {% endif %}

    <!-- Simple header (if neither) -->
    {% if not memo_style and not use_letterhead %}
    <div style="margin-bottom: 0.3in;">
        {% if date %}<div style="float: right; color: #666;">{{ date }}</div>{% endif %}
        {% if from_name %}<div style="font-weight: bold;">{{ from_name }}</div>{% endif %}
        {% if subject %}<div style="font-style: italic; margin-top: 0.1in;">{{ subject }}</div>{% endif %}
        <div style="clear: both;"></div>
    </div>
    {% endif %}

    <!-- Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Signature -->
    {% if signature %}
    <div class="signature">
        {{ signature }}
    </div>
    {% endif %}
</body>
</html>
"""


def generate_personal_memo(
    content: str,
    output_path: Path,
    title: str = "Personal Memo",
    from_name: str = None,
    from_title: str = None,
    to_name: str = None,
    department: str = None,
    subject: str = None,
    date: str = None,
    signature: str = None,
    memo_style: bool = True,
    use_letterhead: bool = False,
) -> Path:
    """
    Generate a personal memo or note.

    Args:
        content: Main content (HTML)
        output_path: Where to save PDF
        title: Document title (for PDF metadata)
        from_name: Sender name
        from_title: Sender job title
        to_name: Recipient name
        department: Department
        subject: Subject line
        date: Date
        signature: Signature text
        memo_style: Use memo header format
        use_letterhead: Use formal letterhead

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(PERSONAL_MEMO_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        from_name=from_name,
        from_title=from_title,
        to_name=to_name,
        department=department,
        subject=subject,
        date=date,
        signature=signature,
        memo_style=memo_style,
        use_letterhead=use_letterhead,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
