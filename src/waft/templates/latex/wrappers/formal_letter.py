"""
Formal Letter LaTeX Template Wrapper
=====================================

Python wrapper for generating formal WAFT business letters using LaTeX.
Professional letter format with letterhead, signature blocks, and WAFT branding.

category: letter
tags: [latex, pdf, letter, formal, business, waft]
source: waft
"""

from pathlib import Path
from datetime import datetime
from ..compiler import LaTeXCompiler
from typing import Optional, List, Dict, Any


# LaTeX Formal Letter Template
# Uses placeholders that will be replaced by string substitution
FORMAL_LETTER_TEMPLATE = r"""\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{fontspec}
\usepackage{microtype}
\usepackage{enumitem}

% Geometry (standard business letter margins)
\geometry{
    left=1in,
    right=1in,
    top=1in,
    bottom=1in,
    headheight=0.5in,
    footskip=0.5in
}

% Colors (WAFT branding)
\definecolor{waftblue}{RGB}{0,102,204}
\definecolor{waftdark}{RGB}{0,0,0}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=waftblue,
    urlcolor=waftblue,
    citecolor=waftblue,
    pdfauthor={WAFT Development Team},
    pdftitle={WAFT Formal Letter},
    pdfsubject={Formal Business Correspondence}
}

% Page style (letterhead on first page only)
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\textsc{Page \thepage}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.4pt}

% Letterhead command
\newcommand{\letterhead}[1]{%
    \begin{center}
        \vspace*{-0.5in}
        {\Large\bfseries\textcolor{waftblue}{#1}}
        \vspace{0.1in}
        \hrule height 2pt
        \vspace{0.2in}
    \end{center}
}

% Signature block environment
\newenvironment{signatureblock}[1]{%
    \vspace{0.3in}
    \begin{flushleft}
        \vspace{0.2in}
        \hrule width 2.5in
        \vspace{0.05in}
        \textbf{#1}
}{%
    \end{flushleft}
}

% Document metadata
\title{LETTER_TITLE_PLACEHOLDER}
\author{SENDER_NAME_PLACEHOLDER}
\date{DATE_PLACEHOLDER}

\begin{document}

LETTERHEAD_PLACEHOLDER

% Date
\begin{flushright}
DATE_PLACEHOLDER
\end{flushright}

\vspace{0.2in}

% Recipient
\begin{flushleft}
RECIPIENT_BLOCK_PLACEHOLDER
\end{flushleft}

\vspace{0.2in}

SUBJECT_LINE_PLACEHOLDER

% Salutation
SALUTATION_PLACEHOLDER

\vspace{0.1in}

% Body content
BODY_CONTENT_PLACEHOLDER

% Closing
\vspace{0.2in}
CLOSING_PLACEHOLDER

SIGNATURE_BLOCK_PLACEHOLDER

ENCLOSURES_PLACEHOLDER

CC_PLACEHOLDER

\end{document}
"""


def generate_formal_letter(
    title: str,
    content: str,
    output_path: Path,
    # Letter metadata
    date: Optional[str] = None,
    sender_name: str = "WAFT Development Team",
    sender_title: Optional[str] = None,
    sender_organization: str = "WAFT Framework",
    sender_address: Optional[str] = None,
    sender_city_state_zip: Optional[str] = None,
    sender_email: Optional[str] = None,
    sender_phone: Optional[str] = None,
    # Recipient
    recipient_name: Optional[str] = None,
    recipient_title: Optional[str] = None,
    recipient_organization: Optional[str] = None,
    recipient_address: Optional[str] = None,
    recipient_city_state_zip: Optional[str] = None,
    # Letter content
    subject: Optional[str] = None,
    salutation: Optional[str] = None,
    closing: Optional[str] = None,
    # Signature
    signature_name: Optional[str] = None,
    signature_title: Optional[str] = None,
    signature_organization: Optional[str] = None,
    signature_email: Optional[str] = None,
    signature_phone: Optional[str] = None,
    # Letterhead
    letterhead: Optional[str] = None,
    # Additional
    enclosures: Optional[str] = None,
    cc: Optional[str] = None,
    **kwargs
) -> Path:
    """
    Generate PDF using Formal Letter LaTeX template.

    Args:
        title: Document title (used for PDF metadata)
        content: Main letter body content (markdown or plain text)
        output_path: Where to save PDF
        date: Letter date (defaults to current date)
        sender_name: Sender's name
        sender_title: Sender's title/position
        sender_organization: Sender's organization
        sender_address: Sender's street address
        sender_city_state_zip: Sender's city, state, zip
        sender_email: Sender's email
        sender_phone: Sender's phone
        recipient_name: Recipient's name
        recipient_title: Recipient's title/position
        recipient_organization: Recipient's organization
        recipient_address: Recipient's street address
        recipient_city_state_zip: Recipient's city, state, zip
        subject: Letter subject line
        salutation: Letter salutation (defaults to "Dear [recipient_name],")
        closing: Letter closing (defaults to "Sincerely,")
        signature_name: Name for signature block
        signature_title: Title for signature block
        signature_organization: Organization for signature block
        signature_email: Email for signature block
        signature_phone: Phone for signature block
        letterhead: Letterhead text (if None, uses sender_organization)
        enclosures: List of enclosures
        cc: List of CC recipients
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Set defaults
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")
    
    if letterhead is None:
        letterhead = sender_organization or "WAFT Framework"
    
    if signature_name is None:
        signature_name = sender_name
    
    if signature_title is None:
        signature_title = sender_title
    
    if signature_organization is None:
        signature_organization = sender_organization
    
    if signature_email is None:
        signature_email = sender_email
    
    if signature_phone is None:
        signature_phone = sender_phone
    
    # Convert markdown content to LaTeX (simple conversion)
    body_content = _markdown_to_latex(content)
    
    # Build LaTeX document by replacing placeholders
    latex_content = FORMAL_LETTER_TEMPLATE
    
    # Basic metadata
    latex_content = latex_content.replace("LETTER_TITLE_PLACEHOLDER", _escape_latex(title))
    latex_content = latex_content.replace("SENDER_NAME_PLACEHOLDER", _escape_latex(sender_name))
    latex_content = latex_content.replace("DATE_PLACEHOLDER", _escape_latex(date))
    
    # Letterhead
    if letterhead:
        letterhead_latex = f"\\letterhead{{{_escape_latex(letterhead)}}}"
    else:
        letterhead_latex = ""
    latex_content = latex_content.replace("LETTERHEAD_PLACEHOLDER", letterhead_latex)
    
    # Recipient block
    recipient_lines = []
    if recipient_name:
        recipient_lines.append(f"\\textbf{{{_escape_latex(recipient_name)}}}\\\\")
    if recipient_title:
        recipient_lines.append(f"{_escape_latex(recipient_title)}\\\\")
    if recipient_organization:
        recipient_lines.append(f"{_escape_latex(recipient_organization)}\\\\")
    if recipient_address:
        recipient_lines.append(f"{_escape_latex(recipient_address)}\\\\")
    if recipient_city_state_zip:
        recipient_lines.append(_escape_latex(recipient_city_state_zip))
    recipient_block = "\n".join(recipient_lines) if recipient_lines else ""
    latex_content = latex_content.replace("RECIPIENT_BLOCK_PLACEHOLDER", recipient_block)
    
    # Subject line
    if subject:
        subject_latex = f"\\textbf{{Subject: {_escape_latex(subject)}}}\n\\vspace{{0.15in}}"
    else:
        subject_latex = ""
    latex_content = latex_content.replace("SUBJECT_LINE_PLACEHOLDER", subject_latex)
    
    # Salutation
    if salutation:
        salutation_latex = _escape_latex(salutation)
    else:
        salutation_latex = f"Dear {_escape_latex(recipient_name or 'Sir or Madam')},"
    latex_content = latex_content.replace("SALUTATION_PLACEHOLDER", salutation_latex)
    
    # Body content
    latex_content = latex_content.replace("BODY_CONTENT_PLACEHOLDER", body_content)
    
    # Closing
    if closing:
        closing_latex = f"{_escape_latex(closing)},"
    else:
        closing_latex = "Sincerely,"
    latex_content = latex_content.replace("CLOSING_PLACEHOLDER", closing_latex)
    
    # Signature block
    if signature_name:
        signature_lines = [f"\\begin{{signatureblock}}{{{_escape_latex(signature_name)}}}"]
        if signature_title:
            signature_lines.append(f"{_escape_latex(signature_title)}\\\\")
        if signature_organization:
            signature_lines.append(f"{_escape_latex(signature_organization)}\\\\")
        if signature_email:
            signature_lines.append(f"{_escape_latex(signature_email)}\\\\")
        if signature_phone:
            signature_lines.append(_escape_latex(signature_phone))
        signature_lines.append("\\end{signatureblock}")
        signature_block = "\n".join(signature_lines)
    else:
        signature_block = ""
    latex_content = latex_content.replace("SIGNATURE_BLOCK_PLACEHOLDER", signature_block)
    
    # Enclosures
    if enclosures:
        enclosures_latex = f"\\vspace{{0.2in}}\n\\begin{{flushleft}}\n\\textit{{Enclosures: {_escape_latex(enclosures)}}}\n\\end{{flushleft}}"
    else:
        enclosures_latex = ""
    latex_content = latex_content.replace("ENCLOSURES_PLACEHOLDER", enclosures_latex)
    
    # CC
    if cc:
        cc_latex = f"\\vspace{{0.1in}}\n\\begin{{flushleft}}\n\\textit{{cc: {_escape_latex(cc)}}}\n\\end{{flushleft}}"
    else:
        cc_latex = ""
    latex_content = latex_content.replace("CC_PLACEHOLDER", cc_latex)
    
    # Compile to PDF
    compiler = LaTeXCompiler(compiler="pdflatex")
    pdf_path = compiler.compile(
        latex_content,
        output_path,
        working_dir=output_path.parent,
        runs=2
    )
    
    return pdf_path


def _escape_latex(text: Optional[str]) -> str:
    """Escape LaTeX special characters."""
    if text is None:
        return ""
    
    # LaTeX special characters that need escaping
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "^": r"\textasciicircum{}",
        "_": r"\_",
        "~": r"\textasciitilde{}",
    }
    
    result = str(text)
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    
    return result


def _markdown_to_latex(markdown: str) -> str:
    """
    Convert markdown to LaTeX (simple conversion).
    
    Handles:
    - Paragraphs (double newline)
    - Bold (**text**)
    - Italic (*text*)
    - Line breaks
    """
    if not markdown:
        return ""
    
    lines = markdown.split("\n")
    latex_lines = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_paragraph:
                latex_lines.append("")
                latex_lines.append("")
                in_paragraph = False
            continue
        
        # Convert markdown to LaTeX
        # Bold: **text** -> \textbf{text}
        import re
        line = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', line)
        # Italic: *text* -> \textit{text}
        line = re.sub(r'\*(.*?)\*', r'\\textit{\1}', line)
        
        # Escape LaTeX special characters
        line = _escape_latex(line)
        
        latex_lines.append(line)
        in_paragraph = True
    
    return "\n".join(latex_lines)
