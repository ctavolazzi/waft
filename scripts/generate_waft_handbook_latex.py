#!/usr/bin/env python3
"""
Generate WAFT Handbook using LaTeX Template System
===================================================

Inspired by LaTTe (https://github.com/raphaelreyna/latte.git) and 
LaTeX Cookbook (https://github.com/alexpovel/latex-cookbook.git).

This script:
1. Reads WAFT_FRAMEWORK_HANDBOOK.md
2. Converts it to structured JSON data
3. Uses LaTeX template (inspired by LaTTe's approach)
4. Generates beautiful PDF field guide

LaTTe Approach:
- Template: .tex file with Go templating syntax
- Data: JSON with content
- Render: Fill template with data, compile to PDF

We adapt this to Python:
- Template: LaTeX .tex file with Jinja2 templating
- Data: JSON extracted from markdown
- Render: Fill template, compile with pdflatex
"""

from pathlib import Path
import sys
import json
import re
from datetime import datetime
from typing import Dict, Any, List
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from jinja2 import Template


# LaTeX Field Guide Template (inspired by LaTTe + LaTeX Cookbook)
# Note: Using raw string and Jinja2 {% raw %} blocks for LaTeX braces
LATEX_FIELD_GUIDE_TEMPLATE = r"""
\documentclass[11pt,letterpaper]{article}

% Packages (inspired by LaTeX Cookbook)
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{tcolorbox}
\usepackage{fontspec}
\usepackage{microtype}

% Geometry (field guide style - practical margins)
\geometry{
    left=0.75in,
    right=0.75in,
    top=0.75in,
    bottom=0.75in,
    headheight=0.3in,
    footskip=0.4in
}

% Colors (field guide aesthetic)
\definecolor{fieldguideblack}{RGB}{0,0,0}
\definecolor{fieldguideyellow}{RGB}{255,255,0}
\definecolor{fieldguidered}{RGB}{204,0,0}
\definecolor{fieldguideblue}{RGB}{0,102,204}
\definecolor{fieldguideorange}{RGB}{255,153,0}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=fieldguideblue,
    urlcolor=fieldguideblue,
    citecolor=fieldguideblue,
    pdfauthor={WAFT Development Team},
    pdftitle={WAFT Framework Handbook},
    pdfsubject={Directed Evolution of Self-Modifying AI Agents}
}

% Page style (field guide header/footer)
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textsc{\textbf{${series} ${number}}}}
\fancyhead[R]{\textsc{Page \thepage}}
\fancyfoot[C]{\textsc{\textbf{${classification}}}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Title formatting (field guide style)
\titleformat{\section}
    {\Large\bfseries\color{fieldguideblack}}
    {}
    {0em}
    {}
    [\titlerule[0.4pt]]

\titleformat{\subsection}
    {\large\bfseries\color{fieldguideblack}}
    {}
    {0em}
    {}

\titleformat{\subsubsection}
    {\normalsize\bfseries\itshape\color{fieldguideblack}}
    {}
    {0em}
    {}

% Spacing
\titlespacing*{\section}{0pt}{0.3in}{0.15in}
\titlespacing*{\subsection}{0pt}{0.2in}{0.1in}
\titlespacing*{\subsubsection}{0pt}{0.15in}{0.08in}

% Custom environments (field guide boxes)
\newtcolorbox{warningbox}{
    colback=fieldguideyellow!20,
    colframe=fieldguidered,
    boxrule=3pt,
    arc=2pt,
    left=0.15in,
    right=0.15in,
    top=0.1in,
    bottom=0.1in
}

\newtcolorbox{cautionbox}{
    colback=fieldguideorange!10,
    colframe=fieldguideorange,
    boxrule=2pt,
    arc=2pt,
    left=0.15in,
    right=0.15in,
    top=0.1in,
    bottom=0.1in
}

\newtcolorbox{notebox}{
    colback=fieldguideblue!10,
    colframe=fieldguideblue,
    boxrule=2pt,
    arc=2pt,
    left=0.15in,
    right=0.15in,
    top=0.1in,
    bottom=0.1in
}

\newtcolorbox{checklistbox}{
    colback=white,
    colframe=fieldguideblack,
    boxrule=2pt,
    arc=2pt,
    left=0.15in,
    right=0.15in,
    top=0.1in,
    bottom=0.1in
}

% Code listings style
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    backgroundcolor=\color{gray!10},
    rulecolor=\color{fieldguideblack}
}

% Document metadata
\title{${title}}
{% if subtitle %}
\subtitle{${subtitle}}
{% endif %}
\author{${authors}}
\date{${date}}

\begin{document}

% Cover page (field guide style)
\begin{titlepage}
    \centering
    \vspace*{0.5in}
    
    % Series and number
    {\Large\bfseries\textsc{${series} ${number}}}
    
    \vspace{0.3in}
    
    % Title
    \begin{tcolorbox}[
        colback=white,
        colframe=fieldguideblack,
        boxrule=4pt,
        arc=0pt,
        width=0.9\textwidth,
        left=0.2in,
        right=0.2in,
        top=0.3in,
        bottom=0.3in
    ]
    \centering
    {\Huge\bfseries ${title}}
    {% if subtitle %}
    \\[0.2in]
    {\Large ${subtitle}}
    {% endif %}
    \end{tcolorbox}
    
    \vfill
    
    {% if classification %}
    \begin{tcolorbox}[
        colback=fieldguideyellow,
        colframe=fieldguidered,
        boxrule=2pt,
        width=0.7\textwidth
    ]
    \centering
    {\Large\bfseries ${classification}}
    \end{tcolorbox}
    {% endif %}
    
    \vspace{0.3in}
    
    {% if issued_by %}
    \textbf{Issued by:} ${issued_by}\\
    {% endif %}
    {% if date %}
    \textbf{Date:} ${date}
    {% endif %}
    
    \vspace{0.5in}
\end{titlepage}

\newpage
\setcounter{page}{1}

% Abstract
{% if abstract %}
\begin{abstract}
${abstract}
\end{abstract}
\vspace{0.2in}
{% endif %}

% Main content
${content}

\end{document}
"""


def parse_markdown_to_json(markdown_path: Path) -> Dict[str, Any]:
    """Parse WAFT handbook markdown into structured JSON data."""
    content = markdown_path.read_text(encoding='utf-8')
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    metadata = {}
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # Simple YAML parsing (basic)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == 'authors':
                    # Handle list format
                    if value.startswith('['):
                        metadata[key] = [{'name': value.strip('[]').strip()}]
                    else:
                        metadata[key] = [{'name': value}]
                else:
                    metadata[key] = value
        content = content[frontmatter_match.end():]
    
    # Extract title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = metadata.get('title', title_match.group(1) if title_match else 'WAFT Framework Handbook')
    
    # Extract abstract
    abstract_match = re.search(r'^## Abstract\s*\n\n(.+?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    abstract = metadata.get('abstract', abstract_match.group(1).strip() if abstract_match else '')
    
    # Convert markdown sections to LaTeX
    latex_content = convert_markdown_to_latex(content)
    
    return {
        'title': title,
        'subtitle': metadata.get('subtitle', 'A Comprehensive Guide to Directed Evolution of Self-Modifying AI Agents'),
        'abstract': abstract,
        'authors': ', '.join([a.get('name', 'WAFT Development Team') for a in metadata.get('authors', [{'name': 'WAFT Development Team'}])]),
        'date': metadata.get('year', datetime.now().strftime('%Y')),
        'series': 'FIELD GUIDE',
        'number': 'FG-WAFT-001',
        'classification': 'FOR OFFICIAL USE ONLY',
        'issued_by': 'WAFT Development Team',
        'content': latex_content
    }


def convert_markdown_to_latex(markdown: str) -> str:
    """Convert markdown content to LaTeX format."""
    latex = markdown
    
    # Remove frontmatter and title (already handled)
    latex = re.sub(r'^---\n.*?\n---\n', '', latex, flags=re.DOTALL)
    latex = re.sub(r'^#\s+.*?\n\n', '', latex, flags=re.MULTILINE)
    latex = re.sub(r'^## Abstract\s*\n\n.*?(?=\n##|\Z)', '', latex, flags=re.DOTALL)
    
    # Headers
    latex = re.sub(r'^##\s+(.+)$', r'\\section{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^###\s+(.+)$', r'\\subsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^####\s+(.+)$', r'\\subsubsection{\1}', latex, flags=re.MULTILINE)
    
    # Bold
    latex = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex)
    
    # Italic
    latex = re.sub(r'\*(.+?)\*', r'\\textit{\1}', latex)
    
    # Code blocks
    latex = re.sub(
        r'```(\w+)?\n(.*?)```',
        lambda m: f'\\begin{{lstlisting}}\n{m.group(2)}\\end{{lstlisting}}',
        latex,
        flags=re.DOTALL
    )
    
    # Inline code
    latex = re.sub(r'`([^`]+)`', r'\\texttt{\1}', latex)
    
    # Lists
    # Unordered lists
    latex = re.sub(r'^-\s+(.+)$', r'\\item \1', latex, flags=re.MULTILINE)
    # Wrap consecutive items in itemize
    lines = latex.split('\n')
    result = []
    in_list = False
    for i, line in enumerate(lines):
        if line.strip().startswith('\\item'):
            if not in_list:
                result.append('\\begin{itemize}')
                in_list = True
            result.append(line)
        else:
            if in_list:
                result.append('\\end{itemize}')
                in_list = False
            result.append(line)
    if in_list:
        result.append('\\end{itemize}')
    latex = '\n'.join(result)
    
    # Tables (basic markdown table to LaTeX)
    latex = convert_markdown_tables_to_latex(latex)
    
    # Horizontal rules
    latex = re.sub(r'^---\s*$', r'\\hrule', latex, flags=re.MULTILINE)
    
    # Paragraphs (double newline = paragraph break)
    latex = re.sub(r'\n\n+', r'\n\n', latex)
    
    return latex


def convert_markdown_tables_to_latex(markdown: str) -> str:
    """Convert markdown tables to LaTeX table format."""
    # Find markdown tables
    table_pattern = r'\|(.+)\|\n\|[-\s\|]+\|\n((?:\|.+\|\n?)+)'
    
    def table_replacer(match):
        header_row = match.group(1)
        data_rows = match.group(2)
        
        # Parse header
        headers = [h.strip() for h in header_row.split('|') if h.strip()]
        
        # Parse data rows
        rows = []
        for row in data_rows.strip().split('\n'):
            if row.strip():
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    rows.append(cells)
        
        # Build LaTeX table
        latex_table = '\\begin{longtable}{' + 'l' * len(headers) + '}\n'
        latex_table += '\\toprule\n'
        latex_table += ' & '.join([f'\\textbf{{{h}}}' for h in headers]) + ' \\\\\n'
        latex_table += '\\midrule\n'
        latex_table += '\\endfirsthead\n'
        latex_table += '\\midrule\n'
        for row in rows:
            latex_table += ' & '.join(row) + ' \\\\\n'
        latex_table += '\\bottomrule\n'
        latex_table += '\\end{longtable}\n'
        
        return latex_table
    
    return re.sub(table_pattern, table_replacer, markdown, flags=re.MULTILINE)


def generate_latex_from_template(template_str: str, data: Dict[str, Any]) -> str:
    """Fill LaTeX template with data using Jinja2."""
    # Use custom delimiters to avoid conflicts with LaTeX braces
    # Use [[var]] instead of {{var}} to avoid LaTeX brace conflicts
    template_str = template_str.replace('${', '{{').replace('}}', '}}')
    # But we need to be careful - only replace ${} that are variables
    # For now, let's use a simpler approach: use Jinja2 with escaped braces
    from jinja2 import Environment, BaseLoader
    env = Environment(loader=BaseLoader())
    # Use different delimiters
    env.variable_start_string = '[['
    env.variable_end_string = ']]'
    env.block_start_string = '{%'
    env.block_end_string = '%}'
    
    # Convert our ${} syntax to [[ ]] syntax
    import re
    template_str = re.sub(r'\$\{(\w+)\}', r'[[\1]]', template_str)
    
    template = env.from_string(template_str)
    return template.render(**data)


def compile_latex_to_pdf(tex_path: Path, output_dir: Path) -> Path:
    """Compile LaTeX file to PDF using pdflatex."""
    pdf_path = output_dir / f"{tex_path.stem}.pdf"
    
    # Run pdflatex (may need multiple passes for references)
    for _ in range(2):
        result = subprocess.run(
            ['pdflatex', '-output-directory', str(output_dir), str(tex_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"LaTeX compilation error:\n{result.stderr}")
            return None
    
    return pdf_path if pdf_path.exists() else None


def main():
    """Main execution: Generate WAFT Handbook PDF using LaTeX."""
    project_root = Path(__file__).parent.parent
    handbook_md = project_root / "WAFT_FRAMEWORK_HANDBOOK.md"
    output_dir = project_root / "_work_efforts" / "waft_handbook_latex"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("📚 Generating WAFT Handbook using LaTeX Template System")
    print(f"   Source: {handbook_md}")
    print(f"   Output: {output_dir}")
    
    # Step 1: Parse markdown to JSON
    print("\n1️⃣  Parsing markdown to structured data...")
    data = parse_markdown_to_json(handbook_md)
    json_path = output_dir / "handbook_data.json"
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"   ✅ Data saved to: {json_path}")
    
    # Step 2: Generate LaTeX from template
    print("\n2️⃣  Generating LaTeX from template...")
    latex_content = generate_latex_from_template(LATEX_FIELD_GUIDE_TEMPLATE, data)
    tex_path = output_dir / "waft_handbook.tex"
    tex_path.write_text(latex_content, encoding='utf-8')
    print(f"   ✅ LaTeX saved to: {tex_path}")
    
    # Step 3: Compile to PDF
    print("\n3️⃣  Compiling LaTeX to PDF...")
    pdf_path = compile_latex_to_pdf(tex_path, output_dir)
    
    if pdf_path and pdf_path.exists():
        print(f"   ✅ PDF generated: {pdf_path}")
        print(f"\n🎉 WAFT Handbook PDF ready!")
        print(f"   📄 {pdf_path}")
        
        # Try to open PDF
        try:
            import platform
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', str(pdf_path)])
            elif platform.system() == 'Linux':
                subprocess.run(['xdg-open', str(pdf_path)])
            elif platform.system() == 'Windows':
                subprocess.run(['start', str(pdf_path)], shell=True)
        except Exception as e:
            print(f"   ⚠️  Could not auto-open PDF: {e}")
    else:
        print("   ❌ PDF compilation failed. Check LaTeX errors above.")
        print("   💡 Tip: You can manually compile the .tex file with pdflatex")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
