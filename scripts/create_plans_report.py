#!/usr/bin/env python3
"""
Plans Report Creator
====================

Creates a comprehensive plans report using the science-textbook-template.
Compiles all plans from _work_efforts/Plans/ into a beautiful LaTeX textbook.
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.latex.compiler import LaTeXCompiler
from src.waft.templates.latex.content_builders import markdown_to_latex

# Try to import WeasyPrint for fallback
try:
    from weasyprint import HTML as WeasyHTML

    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


def parse_plan_file(plan_path: Path) -> dict[str, Any]:
    """Parse a plan file with YAML frontmatter."""
    content = plan_path.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if frontmatter_match:
        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
        except Exception:
            metadata = {}
        # Remove frontmatter from content
        markdown_content = content[frontmatter_match.end() :].strip()
    else:
        metadata = {}
        markdown_content = content.strip()

    # Extract title from first H1 or use filename
    title_match = re.search(r"^#\s+(.+)$", markdown_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        # Remove title from content
        markdown_content = re.sub(r"^#\s+.+$\n", "", markdown_content, count=1, flags=re.MULTILINE)
    else:
        title = metadata.get("name", plan_path.stem.replace("_", " ").title())

    return {
        "title": title,
        "metadata": metadata,
        "content": markdown_content,
        "filename": plan_path.name,
        "path": str(plan_path.relative_to(Path.cwd() / "_work_efforts" / "Plans")),
    }


def gather_all_plans(plans_dir: Path) -> list[dict[str, Any]]:
    """Gather all plan files from the Plans directory."""
    plans = []

    if not plans_dir.exists():
        print(f"⚠️  Plans directory not found: {plans_dir}")
        return plans

    # Find all .plan.md files
    plan_files = sorted(plans_dir.rglob("*.plan.md"))

    total = len(plan_files)
    print(f"📋 Found {total} plan files")

    if total > 50:
        print(f"⏳ Processing {total} plans (this may take a moment)...")
        print("   Progress: ", end="", flush=True)

    for i, plan_file in enumerate(plan_files, 1):
        try:
            plan_data = parse_plan_file(plan_file)
            plans.append(plan_data)

            # Progress indicator for large sets
            if total > 50:
                if i % 50 == 0 or i == total:
                    print(f"{i}/{total} ", end="", flush=True)
        except Exception as e:
            print(f"\n⚠️  Error parsing {plan_file.name}: {e}")

    if total > 50:
        print()  # New line after progress

    print(f"✅ Parsed {len(plans)} plans successfully")
    return plans


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "^": r"\textasciicircum{}",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "\\": r"\textbackslash{}",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def generate_latex_document(plans: list[dict[str, Any]], title: str = "Plans Report") -> str:
    """Generate LaTeX document from plans using science-textbook-template structure."""

    now = datetime.now()
    date_str = now.strftime("%B %d, %Y")

    # Start building LaTeX document
    latex_parts = []

    # Document class and packages (from template)
    latex_parts.append(r"\documentclass{book}")
    latex_parts.append("")
    latex_parts.append(f"\\title{{{escape_latex(title)}}}")
    latex_parts.append("\\newcommand{\\booksubtitle}{Comprehensive Plans Collection}")
    latex_parts.append("\\newcommand{\\booklicense}{Internal Use Only}")
    latex_parts.append("")
    latex_parts.append("\\author{W.A.F.T. System}")
    latex_parts.append(f"\\newcommand{{\\authorsubtitle}}{{{date_str}}}")
    latex_parts.append("")
    latex_parts.append("% Create convenient commands")
    latex_parts.append("\\makeatletter")
    latex_parts.append("\\newcommand{\\booktitle}{\\@title}")
    latex_parts.append("\\newcommand{\\bookauthor}{\\@author}")
    latex_parts.append("\\makeatother")
    latex_parts.append("")
    latex_parts.append("\\usepackage[utf8]{inputenc}")
    latex_parts.append("\\usepackage{fix-cm}")
    latex_parts.append("\\usepackage{tikz}")
    latex_parts.append("\\usepackage{amsmath}")
    latex_parts.append("\\usepackage{listings}")
    latex_parts.append("\\usepackage{xcolor}")
    latex_parts.append("")
    latex_parts.append("% Geometry for letter size paper (better for viewing)")
    latex_parts.append("\\usepackage[margin=.75in, paperwidth=8.5in, paperheight=11in]{geometry}")
    latex_parts.append("")
    latex_parts.append("\\renewcommand{\\contentsname}{Table of Contents}")
    latex_parts.append("\\usepackage{makeidx}")
    latex_parts.append("\\makeindex")
    latex_parts.append("")
    latex_parts.append("% Configure code listings")
    latex_parts.append("\\lstset{")
    latex_parts.append("    basicstyle=\\ttfamily\\small,")
    latex_parts.append("    breaklines=true,")
    latex_parts.append("    frame=single,")
    latex_parts.append("    backgroundcolor=\\color{gray!10}")
    latex_parts.append("}")
    latex_parts.append("")
    latex_parts.append("% Content Starts Here")
    latex_parts.append("\\begin{document}")
    latex_parts.append("\\frontmatter")
    latex_parts.append("")

    # Half Title Page
    latex_parts.append("% ---- Half Title Page ----")
    latex_parts.append("\\newgeometry{top=1.75in,bottom=.5in}")
    latex_parts.append("\\begin{titlepage}")
    latex_parts.append("\\begin{flushleft}")
    latex_parts.append("")
    latex_parts.append("% Title")
    latex_parts.append(
        f"\\textbf{{\\fontfamily{{qcs}}\\fontsize{{48}}{{54}}\\selectfont {escape_latex(title)}\\\\}}"
    )
    latex_parts.append("")
    latex_parts.append("% Draw a line 4pt high")
    latex_parts.append("\\par\\noindent\\rule{\\textwidth}{4pt}\\\\")
    latex_parts.append("")
    latex_parts.append("% Subtitle")
    latex_parts.append("\\begin{tikzpicture}")
    latex_parts.append("\\shade[bottom color=lightgray,top color=white]")
    latex_parts.append("    (0,0) rectangle (\\textwidth, 1.5)")
    latex_parts.append("    node[midway] {\\textbf{\\large \\textit{\\booksubtitle}}};")
    latex_parts.append("\\end{tikzpicture}")
    latex_parts.append("")
    latex_parts.append("% Edition Number")
    latex_parts.append("\\begin{flushright}")
    latex_parts.append(f"\\Large Generated {date_str}")
    latex_parts.append("\\end{flushright}")
    latex_parts.append("")
    latex_parts.append("\\vspace{\\fill}")
    latex_parts.append("")
    latex_parts.append("\\end{flushleft}")
    latex_parts.append("\\end{titlepage}")
    latex_parts.append("\\restoregeometry")
    latex_parts.append("")

    # Title Page
    latex_parts.append("% ---- Title Page ----")
    latex_parts.append("\\thispagestyle{empty}")
    latex_parts.append("\\newgeometry{top=1.75in,bottom=.5in}")
    latex_parts.append("\\begin{titlepage}")
    latex_parts.append("\\begin{flushleft}")
    latex_parts.append("")
    latex_parts.append("% Title")
    latex_parts.append(
        f"\\textbf{{\\fontfamily{{qcs}}\\fontsize{{48}}{{54}}\\selectfont {escape_latex(title)}\\\\}}"
    )
    latex_parts.append("")
    latex_parts.append("\\par\\noindent\\rule{\\textwidth}{4pt}\\\\")
    latex_parts.append("")
    latex_parts.append("\\begin{tikzpicture}")
    latex_parts.append("\\shade[bottom color=lightgray,top color=white]")
    latex_parts.append("    (0,0) rectangle (\\textwidth, 1.5)")
    latex_parts.append("    node[midway] {\\textbf{\\large \\textit{\\booksubtitle}}};")
    latex_parts.append("\\end{tikzpicture}")
    latex_parts.append("")
    latex_parts.append("\\begin{flushright}")
    latex_parts.append(f"\\Large Generated {date_str}")
    latex_parts.append("\\end{flushright}")
    latex_parts.append("")
    latex_parts.append("\\vspace{\\fill}")
    latex_parts.append("")
    latex_parts.append("\\textbf{\\large \\bookauthor}\\\\[3.5pt]")
    latex_parts.append("\\textbf{\\large \\textit{\\authorsubtitle}}")
    latex_parts.append("")
    latex_parts.append("\\vspace{\\fill}")
    latex_parts.append("")
    latex_parts.append("\\end{flushleft}")
    latex_parts.append("\\end{titlepage}")
    latex_parts.append("\\restoregeometry")
    latex_parts.append("")

    # Colophon
    latex_parts.append("\\thispagestyle{empty}")
    latex_parts.append("\\begin{flushleft}")
    latex_parts.append("\\vspace*{\\fill}")
    latex_parts.append("This report was typeset using \\LaTeX{} software.\\\\")
    latex_parts.append(f"Generated on {date_str}\\\\")
    latex_parts.append(f"Total Plans: {len(plans)}\\\\")
    latex_parts.append("\\vspace{\\fill}")
    latex_parts.append("\\end{flushleft}")
    latex_parts.append("")
    latex_parts.append("\\addtocounter{page}{2}")
    latex_parts.append("")

    # Preface
    latex_parts.append("\\chapter*{Preface}")
    latex_parts.append(
        f"This report contains {len(plans)} plans gathered from the work efforts system."
    )
    latex_parts.append("Each plan represents a documented intention, goal, or project outline.")
    latex_parts.append("Plans are organized chronologically and by category where applicable.")
    latex_parts.append("")

    # Table of Contents
    latex_parts.append("\\setcounter{tocdepth}{2}")
    latex_parts.append("\\tableofcontents")
    latex_parts.append("")
    latex_parts.append("\\mainmatter")
    latex_parts.append("")

    # Add each plan as a chapter
    total_plans = len(plans)
    if total_plans > 50:
        print(f"📝 Generating LaTeX for {total_plans} plans...")
        print("   Progress: ", end="", flush=True)

    for i, plan in enumerate(plans, 1):
        chapter_title = escape_latex(plan["title"])
        latex_parts.append(f"\\chapter{{{chapter_title}}}")
        latex_parts.append("")

        # Progress indicator
        if total_plans > 50 and (i % 50 == 0 or i == total_plans):
            print(f"{i}/{total_plans} ", end="", flush=True)

        # Add metadata if available
        if plan["metadata"]:
            metadata_items = []
            if "overview" in plan["metadata"]:
                metadata_items.append(
                    f"\\textbf{{Overview:}} {escape_latex(plan['metadata']['overview'])}"
                )
            if "status" in plan["metadata"]:
                metadata_items.append(
                    f"\\textbf{{Status:}} {escape_latex(str(plan['metadata']['status']))}"
                )
            if "todos" in plan["metadata"]:
                todo_count = len([t for t in plan["metadata"]["todos"] if isinstance(t, dict)])
                if todo_count > 0:
                    metadata_items.append(f"\\textbf{{Todos:}} {todo_count} items")

            if metadata_items:
                latex_parts.append("\\begin{itemize}")
                for item in metadata_items:
                    latex_parts.append(f"\\item {item}")
                latex_parts.append("\\end{itemize}")
                latex_parts.append("")

        # Convert markdown content to LaTeX
        try:
            latex_content = markdown_to_latex(plan["content"])
            # Clean up any remaining issues
            latex_content = re.sub(
                r"\\section\{", r"\\subsection{", latex_content
            )  # Demote H1 to H2
            latex_parts.append(latex_content)
        except Exception as e:
            latex_parts.append(f"% Error converting content: {e}")
            latex_parts.append(escape_latex(plan["content"][:500]))  # Fallback to escaped text

        latex_parts.append("")
        latex_parts.append("")

    # Back matter
    latex_parts.append("\\backmatter")
    latex_parts.append("")
    latex_parts.append("\\chapter*{Index of Plans}")
    latex_parts.append("\\begin{itemize}")
    for i, plan in enumerate(plans, 1):
        plan_title = escape_latex(plan["title"])
        latex_parts.append(f"\\item \\textbf{{{plan_title}}}")
        if plan.get("path"):
            latex_parts.append(f"  \\textit{{({escape_latex(plan['path'])})}}")
    latex_parts.append("\\end{itemize}")
    latex_parts.append("")
    latex_parts.append("\\end{document}")

    return "\n".join(latex_parts)


def generate_html_document(
    plans: list[dict[str, Any]], title: str = "Plans Report", fallback_reason: str | None = None
) -> str:
    """Generate HTML document from plans for WeasyPrint conversion."""
    import html as html_module

    now = datetime.now()
    date_str = now.strftime("%B %d, %Y")

    # Convert markdown to HTML (basic conversion)
    def markdown_to_html_simple(md: str) -> str:
        """Simple markdown to HTML converter."""
        html = md
        # Headers
        html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        # Bold
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        # Italic
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
        # Code blocks
        html = re.sub(r"```(\w+)?\n(.*?)```", r"<pre><code>\2</code></pre>", html, flags=re.DOTALL)
        # Inline code
        html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)
        # Paragraphs
        html = re.sub(r"\n\n+", r"</p><p>", html)
        return f"<p>{html}</p>"

    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append('<html lang="en">')
    html_parts.append("<head>")
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append(f"<title>{html_module.escape(title)}</title>")
    html_parts.append("<style>")
    html_parts.append("""
        @page {
            size: letter;
            margin: 0.75in 0.6in;
            background: #fafafa;
        }
        body {
            font-family: "Georgia", "Times New Roman", serif;
            font-size: 11pt;
            line-height: 1.7;
            max-width: 100%;
            margin: 0;
            padding: 0;
            color: #1a1a1a;
            background: #fafafa;
        }
        .title-page {
            page-break-after: always;
            text-align: center;
            padding-top: 3in;
        }
        .title-page h1 {
            font-size: 42pt;
            font-weight: bold;
            margin-bottom: 0.4in;
            border-bottom: 4pt solid #2c3e50;
            padding-bottom: 0.2in;
            color: #1a1a1a;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .title-page .subtitle {
            font-size: 16pt;
            font-style: italic;
            color: #5a6c7d;
            margin: 0.4in 0;
            background: linear-gradient(to bottom, #ffffff 0%, #f8f9fa 100%);
            padding: 0.3in;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        .title-page .date {
            font-size: 14pt;
            text-align: right;
            margin-top: 2in;
        }
        .colophon {
            page-break-after: always;
            text-align: left;
            padding-top: 4in;
        }
        .preface {
            page-break-after: always;
        }
        .preface h1 {
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 0.3in;
        }
        .toc {
            page-break-after: always;
        }
        .toc h1 {
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 0.3in;
        }
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        .toc li {
            margin: 0.1in 0;
        }
        .toc a {
            text-decoration: none;
            color: black;
        }
        .chapter {
            page-break-before: always;
            margin-top: 1in;
        }
        .chapter h1 {
            font-size: 20pt;
            font-weight: 600;
            margin-bottom: 0.35in;
            border-bottom: 3pt solid #3498db;
            padding-bottom: 0.12in;
            color: #2c3e50;
            background: linear-gradient(to right, rgba(52, 152, 219, 0.1), transparent);
            padding-left: 0.15in;
            padding-right: 0.15in;
        }
        .chapter h2 {
            font-size: 15pt;
            font-weight: 600;
            margin-top: 0.35in;
            margin-bottom: 0.25in;
            color: #34495e;
            border-bottom: 2pt solid #95a5a6;
            padding-bottom: 0.08in;
        }
        .chapter h3 {
            font-size: 13pt;
            font-weight: 600;
            margin-top: 0.25in;
            margin-bottom: 0.15in;
            color: #5a6c7d;
        }
        .metadata {
            background: linear-gradient(to bottom, #ebf5fb 0%, #ffffff 100%);
            padding: 0.25in;
            margin: 0.25in 0;
            border-left: 5pt solid #3498db;
            border-radius: 0 4px 4px 0;
            box-shadow: 0 2px 6px rgba(52, 152, 219, 0.12);
        }
        .metadata ul {
            list-style: none;
            padding-left: 0;
        }
        .metadata li {
            margin: 0.05in 0;
        }
        pre {
            background: linear-gradient(to bottom, #2c3e50 0%, #34495e 100%);
            padding: 0.2in;
            border: 1pt solid #1a1a1a;
            border-left: 5pt solid #3498db;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 9pt;
            color: #ecf0f1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            font-family: "Monaco", "Courier New", monospace;
        }
        code {
            background: #f1f3f5;
            padding: 0.03in 0.06in;
            font-family: "Monaco", "Courier New", monospace;
            font-size: 9.5pt;
            border-radius: 3px;
            color: #e74c3c;
            border: 1px solid #dee2e6;
        }
        pre code {
            background: transparent;
            padding: 0;
            border: none;
            color: #ecf0f1;
        }
        .index {
            page-break-before: always;
        }
        .index h1 {
            font-size: 20pt;
            font-weight: 600;
            margin-bottom: 0.35in;
            border-bottom: 3pt solid #3498db;
            padding-bottom: 0.12in;
            color: #2c3e50;
        }
        p {
            text-align: justify;
            orphans: 2;
            widows: 2;
            margin: 0.12in 0;
        }
        ul, ol {
            margin: 0.15in 0;
            padding-left: 0.35in;
        }
        li {
            margin-bottom: 0.08in;
            line-height: 1.6;
        }
        .index ul {
            list-style: none;
            padding-left: 0;
        }
        .index li {
            margin: 0.1in 0;
        }
    """)
    html_parts.append("</style>")
    html_parts.append("</head>")
    html_parts.append("<body>")

    # Title Page
    html_parts.append('<div class="title-page">')
    html_parts.append(f"<h1>{html_module.escape(title)}</h1>")
    html_parts.append('<div class="subtitle">Comprehensive Plans Collection</div>')
    html_parts.append(f'<div class="date">Generated {date_str}</div>')
    html_parts.append("</div>")

    # Colophon
    html_parts.append('<div class="colophon">')
    html_parts.append("<p>This report was typeset using HTML/CSS and WeasyPrint.</p>")
    html_parts.append(f"<p>Generated on {date_str}</p>")
    html_parts.append(f"<p>Total Plans: {len(plans)}</p>")
    if fallback_reason:
        html_parts.append(
            '<div style="margin-top: 0.3in; padding: 0.2in; background: #fff3cd; border: 1pt solid #ffc107; border-radius: 3pt;">'
        )
        html_parts.append(
            "<p><strong>Note:</strong> This report was generated using WeasyPrint (HTML/CSS) instead of LaTeX.</p>"
        )
        html_parts.append(f"<p><strong>Reason:</strong> {html_module.escape(fallback_reason)}</p>")
        html_parts.append(
            "<p>The report maintains the same textbook-style formatting and structure as the LaTeX version.</p>"
        )
        html_parts.append("</div>")
    html_parts.append("</div>")

    # Preface
    html_parts.append('<div class="preface">')
    html_parts.append("<h1>Preface</h1>")
    html_parts.append(
        f"<p>This report contains {len(plans)} plans gathered from the work efforts system."
    )
    html_parts.append("Each plan represents a documented intention, goal, or project outline.")
    html_parts.append("Plans are organized chronologically and by category where applicable.</p>")
    html_parts.append("</div>")

    # Table of Contents
    html_parts.append('<div class="toc">')
    html_parts.append("<h1>Table of Contents</h1>")
    html_parts.append("<ul>")
    for i, plan in enumerate(plans, 1):
        plan_title = html_module.escape(plan["title"])
        html_parts.append(f'<li><a href="#plan-{i}">{plan_title}</a></li>')
    html_parts.append("</ul>")
    html_parts.append("</div>")

    # Chapters
    total_plans = len(plans)
    if total_plans > 50:
        print(f"📝 Generating HTML for {total_plans} plans...")
        print("   Progress: ", end="", flush=True)

    for i, plan in enumerate(plans, 1):
        html_parts.append(f'<div class="chapter" id="plan-{i}">')
        html_parts.append(f"<h1>{html_module.escape(plan['title'])}</h1>")

        # Progress indicator
        if total_plans > 50 and (i % 50 == 0 or i == total_plans):
            print(f"{i}/{total_plans} ", end="", flush=True)

        # Metadata
        if plan["metadata"]:
            metadata_items = []
            if "overview" in plan["metadata"]:
                metadata_items.append(
                    f"<strong>Overview:</strong> {html_module.escape(str(plan['metadata']['overview']))}"
                )
            if "status" in plan["metadata"]:
                metadata_items.append(
                    f"<strong>Status:</strong> {html_module.escape(str(plan['metadata']['status']))}"
                )
            if "todos" in plan["metadata"]:
                todo_count = len([t for t in plan["metadata"]["todos"] if isinstance(t, dict)])
                if todo_count > 0:
                    metadata_items.append(f"<strong>Todos:</strong> {todo_count} items")

            if metadata_items:
                html_parts.append('<div class="metadata">')
                html_parts.append("<ul>")
                for item in metadata_items:
                    html_parts.append(f"<li>{item}</li>")
                html_parts.append("</ul>")
                html_parts.append("</div>")

        # Content
        try:
            html_content = markdown_to_html_simple(plan["content"])
            html_parts.append(html_content)
        except Exception as e:
            html_parts.append(f"<p>Error converting content: {html_module.escape(str(e))}</p>")
            html_parts.append(f"<pre>{html_module.escape(plan['content'][:500])}</pre>")

        html_parts.append("</div>")

    # Index
    html_parts.append('<div class="index">')
    html_parts.append("<h1>Index of Plans</h1>")
    html_parts.append("<ul>")
    for i, plan in enumerate(plans, 1):
        plan_title = html_module.escape(plan["title"])
        html_parts.append(f"<li><strong>{plan_title}</strong>")
        if plan.get("path"):
            html_parts.append(f" <em>({html_module.escape(plan['path'])})</em>")
        html_parts.append("</li>")
    html_parts.append("</ul>")
    html_parts.append("</div>")

    html_parts.append("</body>")
    html_parts.append("</html>")

    return "\n".join(html_parts)


def generate_city_plan(plans: list[dict[str, Any]], title: str = "City Plan") -> str:
    """Generate condensed City Plan - strategic overview of all plans."""
    import html as html_module
    from collections import defaultdict

    now = datetime.now()
    date_str = now.strftime("%B %d, %Y")

    # Analyze plans - extract themes and categories
    themes = defaultdict(list)
    categories = defaultdict(int)
    status_counts = defaultdict(int)

    for plan in plans:
        # Extract category from title/filename
        title_lower = plan["title"].lower()
        filename_lower = plan.get("filename", "").lower()
        text = f"{title_lower} {filename_lower}"

        # Categorize by keywords
        category = "Other"
        for keyword, cat in [
            ("api", "APIs & Integration"),
            ("ui", "User Interface"),
            ("pdf", "Document Generation"),
            ("test", "Testing & Quality"),
            ("system", "System Architecture"),
            ("workflow", "Workflows"),
            ("template", "Templates"),
            ("mcp", "MCP Servers"),
            ("dnd", "D&D System"),
            ("evolution", "Evolution System"),
            ("being", "Being System"),
            ("tavern", "Tavern Game"),
            ("latex", "LaTeX"),
            ("documentation", "Documentation"),
            ("refactor", "Refactoring"),
            ("feature", "Features"),
            ("fix", "Bug Fixes"),
        ]:
            if keyword in text:
                category = cat
                break

        categories[category] += 1
        themes[category].append(
            {
                "title": plan["title"],
                "overview": plan["metadata"].get("overview", "")[:200] if plan["metadata"] else "",
                "status": plan["metadata"].get("status", "unknown")
                if plan["metadata"]
                else "unknown",
                "todos": len([t for t in plan["metadata"].get("todos", []) if isinstance(t, dict)])
                if plan["metadata"]
                else 0,
            }
        )

        if plan["metadata"]:
            status = plan["metadata"].get("status", "unknown")
            status_counts[status] += 1

    # Generate HTML
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append('<html lang="en">')
    html_parts.append("<head>")
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append(f"<title>{html_module.escape(title)}</title>")
    html_parts.append("<style>")
    html_parts.append("""
        @page {
            size: letter;
            margin: 0.75in;
        }
        body {
            font-family: "Times New Roman", serif;
            font-size: 11pt;
            line-height: 1.6;
        }
        .title-page {
            page-break-after: always;
            text-align: center;
            padding-top: 2in;
        }
        .title-page h1 {
            font-size: 48pt;
            font-weight: bold;
            margin-bottom: 0.3in;
            border-bottom: 4pt solid black;
            padding-bottom: 0.2in;
        }
        .title-page .subtitle {
            font-size: 18pt;
            font-style: italic;
            color: #666;
            margin: 0.5in 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.3in;
            margin: 0.5in 0;
        }
        .stat-box {
            background: #f5f5f5;
            padding: 0.2in;
            border-left: 3pt solid #666;
        }
        .stat-box h3 {
            margin: 0 0 0.1in 0;
            font-size: 12pt;
        }
        .stat-box .number {
            font-size: 24pt;
            font-weight: bold;
            color: #333;
        }
        .category {
            page-break-inside: avoid;
            margin: 0.4in 0;
        }
        .category h2 {
            font-size: 16pt;
            font-weight: bold;
            border-bottom: 2pt solid #333;
            padding-bottom: 0.1in;
            margin-bottom: 0.2in;
        }
        .category .count {
            color: #666;
            font-size: 10pt;
            font-style: italic;
        }
        .plan-item {
            margin: 0.15in 0;
            padding-left: 0.2in;
            border-left: 2pt solid #ddd;
        }
        .plan-item .title {
            font-weight: bold;
            font-size: 11pt;
        }
        .plan-item .overview {
            color: #555;
            font-size: 9pt;
            margin-top: 0.05in;
        }
        .plan-item .meta {
            color: #888;
            font-size: 8pt;
            margin-top: 0.05in;
        }
    """)
    html_parts.append("</style>")
    html_parts.append("</head>")
    html_parts.append("<body>")

    # Title Page
    html_parts.append('<div class="title-page">')
    html_parts.append(f"<h1>{html_module.escape(title)}</h1>")
    html_parts.append('<div class="subtitle">Strategic Overview of All Plans</div>')
    html_parts.append(f'<div style="margin-top: 1in; font-size: 12pt;">Generated {date_str}</div>')
    html_parts.append("</div>")

    # Statistics
    html_parts.append("<h1>City Statistics</h1>")
    html_parts.append('<div class="stats">')
    html_parts.append(
        f'<div class="stat-box"><h3>Total Plans</h3><div class="number">{len(plans)}</div></div>'
    )
    html_parts.append(
        f'<div class="stat-box"><h3>Categories</h3><div class="number">{len(categories)}</div></div>'
    )
    html_parts.append(
        f'<div class="stat-box"><h3>Active</h3><div class="number">{status_counts.get("active", 0) + status_counts.get("pending", 0)}</div></div>'
    )
    html_parts.append("</div>")

    # Categories by size
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    html_parts.append("<h1>City Districts</h1>")
    html_parts.append("<p>Plans organized by category - the districts of our AI Town:</p>")

    for category, count in sorted_categories:
        html_parts.append('<div class="category">')
        html_parts.append(
            f'<h2>{html_module.escape(category)} <span class="count">({count} plans)</span></h2>'
        )

        # Show top plans in this category (limit to 5-10 most relevant)
        category_plans = themes[category][:8]  # Top 8 per category

        for plan_item in category_plans:
            html_parts.append('<div class="plan-item">')
            html_parts.append(f'<div class="title">{html_module.escape(plan_item["title"])}</div>')
            if plan_item["overview"]:
                overview_short = plan_item["overview"][:150] + (
                    "..." if len(plan_item["overview"]) > 150 else ""
                )
                html_parts.append(
                    f'<div class="overview">{html_module.escape(overview_short)}</div>'
                )
            meta_parts = []
            if plan_item["status"] != "unknown":
                meta_parts.append(f"Status: {plan_item['status']}")
            if plan_item["todos"] > 0:
                meta_parts.append(f"{plan_item['todos']} todos")
            if meta_parts:
                html_parts.append(f'<div class="meta">{" • ".join(meta_parts)}</div>')
            html_parts.append("</div>")

        if len(themes[category]) > 8:
            remaining = len(themes[category]) - 8
            html_parts.append(
                f'<div class="plan-item" style="color: #888; font-style: italic;">... and {remaining} more plans in this category</div>'
            )

        html_parts.append("</div>")

    # Summary
    html_parts.append(
        '<div style="page-break-before: always; margin-top: 0.5in; padding: 0.3in; background: #f9f9f9; border: 1pt solid #ddd;">'
    )
    html_parts.append("<h2>City Summary</h2>")
    html_parts.append(
        f"<p>This City Plan represents {len(plans)} documented plans across {len(categories)} major categories."
    )
    html_parts.append(
        "Each category represents a district of development activity in the W.A.F.T. ecosystem.</p>"
    )
    html_parts.append(
        "<p><strong>Largest Districts:</strong> "
        + ", ".join([f"{cat} ({count})" for cat, count in sorted_categories[:5]])
        + "</p>"
    )
    html_parts.append("</div>")

    html_parts.append("</body>")
    html_parts.append("</html>")

    return "\n".join(html_parts)


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create plans report using science-textbook-template"
    )
    parser.add_argument("--title", default="Plans Report", help="Report title")
    parser.add_argument("--output", default=None, help="Output PDF path")
    parser.add_argument("--plans-dir", default=None, help="Plans directory path")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of plans to include")
    parser.add_argument(
        "--city-plan",
        action="store_true",
        help="Generate condensed City Plan view (strategic overview)",
    )
    args = parser.parse_args()

    project_path = Path.cwd()

    # Determine plans directory
    if args.plans_dir:
        plans_dir = Path(args.plans_dir)
    else:
        plans_dir = project_path / "_work_efforts" / "Plans"

    # Gather plans
    print("📋 Gathering plans...")
    all_plans = gather_all_plans(plans_dir)

    if not all_plans:
        print("❌ No plans found!")
        return 1

    # Limit if requested
    if args.limit:
        all_plans = all_plans[: args.limit]
        print(f"📊 Limited to {len(all_plans)} plans")

    print(f"✅ Found {len(all_plans)} plans")

    # City Plan mode - condensed strategic overview
    if args.city_plan:
        print("🏙️  Generating City Plan (condensed strategic overview)...")
        html_content = generate_city_plan(all_plans, args.title or "City Plan")

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            now = datetime.now()
            output_dir = project_path / "_work_efforts" / "briefs"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"City_Plan_{now.strftime('%Y%m%d')}.pdf"

        # Convert HTML to PDF with WeasyPrint
        print("🔨 Converting to PDF with WeasyPrint...")
        try:
            WeasyHTML(string=html_content, base_url=str(output_path.parent)).write_pdf(
                output_path, presentational_hints=True, optimize_images=True
            )

            print("=" * 60)
            print("✅ City Plan Created!")
            print("=" * 60)
            print(f"📄 Output: {output_path}")
            print(f"📊 Plans analyzed: {len(all_plans)}")
            print(f"🏙️  Categories: {len(set([p['title'].lower() for p in all_plans]))}")
            print()
            print("Ready for review!")

            return 0
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            html_path = output_path.with_suffix(".html")
            html_path.write_text(html_content, encoding="utf-8")
            print(f"💾 HTML source saved to: {html_path}")
            return 1

    # Generate LaTeX
    print("📝 Generating LaTeX document...")
    latex_content = generate_latex_document(all_plans, args.title)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        now = datetime.now()
        output_dir = project_path / "_work_efforts" / "briefs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"Plans_Report_{now.strftime('%Y%m%d')}.pdf"

    # Try LaTeX compilation first
    print("🔨 Compiling LaTeX to PDF...")
    try:
        compiler = LaTeXCompiler()
        pdf_path = compiler.compile(
            latex_content,
            output_path,
            runs=2,  # Need 2 runs for TOC
        )

        print("=" * 60)
        print("✅ Plans Report Created!")
        print("=" * 60)
        print(f"📄 Output: {pdf_path}")
        print(f"📊 Plans included: {len(all_plans)}")
        print()
        print("Ready for review!")

        return 0
    except Exception as e:
        print(f"⚠️  LaTeX compilation failed: {e}")
        print("🔄 Falling back to WeasyPrint (HTML/CSS)...")

        if not WEASYPRINT_AVAILABLE:
            print("❌ WeasyPrint not available. Install with: pip install weasyprint")
            # Save LaTeX for debugging
            debug_path = output_path.parent / f"{output_path.stem}.tex"
            debug_path.write_text(latex_content, encoding="utf-8")
            print(f"💾 LaTeX source saved to: {debug_path}")
            return 1

        # Generate HTML and convert with WeasyPrint
        try:
            print("📝 Generating HTML document...")
            # Create fallback reason message
            error_msg = str(e)
            if "pdflatex" in error_msg.lower() or "latex compiler" in error_msg.lower():
                fallback_reason = "LaTeX compiler (pdflatex) not found on this system. Please install a LaTeX distribution (e.g., TeX Live, MiKTeX) to use LaTeX compilation."
            else:
                fallback_reason = f"LaTeX compilation failed: {error_msg}"
            html_content = generate_html_document(
                all_plans, args.title, fallback_reason=fallback_reason
            )

            # Save HTML for reference
            html_path = output_path.with_suffix(".html")
            html_path.write_text(html_content, encoding="utf-8")
            print(f"💾 HTML source saved to: {html_path}")

            # Convert HTML to PDF with WeasyPrint
            print("🔨 Converting HTML to PDF with WeasyPrint...")
            WeasyHTML(string=html_content, base_url=str(output_path.parent)).write_pdf(
                output_path, presentational_hints=True, optimize_images=True
            )

            print("=" * 60)
            print("✅ Plans Report Created!")
            print("=" * 60)
            print(f"📄 Output: {output_path}")
            print(f"📊 Plans included: {len(all_plans)}")
            print(f"💾 HTML source: {html_path}")
            print()
            print("Ready for review!")

            return 0
        except Exception as e2:
            print(f"❌ Error with WeasyPrint fallback: {e2}")
            # Save both LaTeX and HTML for debugging
            debug_path = output_path.parent / f"{output_path.stem}.tex"
            debug_path.write_text(latex_content, encoding="utf-8")
            print(f"💾 LaTeX source saved to: {debug_path}")
            if "html_content" in locals():
                html_debug_path = output_path.parent / f"{output_path.stem}.html"
                html_debug_path.write_text(html_content, encoding="utf-8")
                print(f"💾 HTML source saved to: {html_debug_path}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
