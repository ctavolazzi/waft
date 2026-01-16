"""
LaTeX Content Builders
=====================

Functions to format content for LaTeX templates.
Similar to build_dnd_scenario_content() pattern from D&D template.
"""

import re
from typing import Dict, Any, Optional


def markdown_to_latex(markdown: str) -> str:
    """
    Convert basic markdown to LaTeX.
    
    Args:
        markdown: Markdown content
        
    Returns:
        LaTeX formatted content
    """
    latex = markdown
    
    # Headers
    latex = re.sub(r'^# (.+)$', r'\\section{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^## (.+)$', r'\\subsection{\1}', latex, flags=re.MULTILINE)
    latex = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', latex, flags=re.MULTILINE)
    
    # Bold
    latex = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', latex)
    latex = re.sub(r'__(.+?)__', r'\\textbf{\1}', latex)
    
    # Italic
    latex = re.sub(r'\*(.+?)\*', r'\\textit{\1}', latex)
    latex = re.sub(r'_(.+?)_', r'\\textit{\1}', latex)
    
    # Code blocks
    latex = re.sub(r'```(\w+)?\n(.*?)```', r'\\begin{verbatim}\n\2\n\\end{verbatim}', latex, flags=re.DOTALL)
    
    # Inline code
    latex = re.sub(r'`(.+?)`', r'\\texttt{\1}', latex)
    
    # Links
    latex = re.sub(r'\[(.+?)\]\((.+?)\)', r'\\href{\2}{\1}', latex)
    
    # Lists (basic)
    lines = latex.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^[-*]\s+', line):
            if not in_list:
                result_lines.append('\\begin{itemize}')
                in_list = True
            content = re.sub(r'^[-*]\s+', '', line)
            result_lines.append(f'\\item {content}')
        elif re.match(r'^\d+\.\s+', line):
            if not in_list:
                result_lines.append('\\begin{enumerate}')
                in_list = True
            content = re.sub(r'^\d+\.\s+', '', line)
            result_lines.append(f'\\item {content}')
        else:
            if in_list:
                result_lines.append('\\end{itemize}' if 'itemize' in result_lines[-2] else '\\end{enumerate}')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('\\end{itemize}')
    
    return '\n'.join(result_lines)


def html_to_latex(html: str) -> str:
    """
    Convert basic HTML to LaTeX.
    
    Args:
        html: HTML content
        
    Returns:
        LaTeX formatted content
    """
    latex = html
    
    # Remove HTML tags and convert to LaTeX
    latex = re.sub(r'<h1>(.+?)</h1>', r'\\section{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<h2>(.+?)</h2>', r'\\subsection{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<h3>(.+?)</h3>', r'\\subsubsection{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<strong>(.+?)</strong>', r'\\textbf{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<em>(.+?)</em>', r'\\textit{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<code>(.+?)</code>', r'\\texttt{\1}', latex, flags=re.DOTALL)
    latex = re.sub(r'<p>(.+?)</p>', r'\1\n\n', latex, flags=re.DOTALL)
    latex = re.sub(r'<br\s*/?>', r'\n', latex)
    
    # Remove remaining HTML tags
    latex = re.sub(r'<[^>]+>', '', latex)
    
    # Decode HTML entities
    latex = latex.replace('&nbsp;', ' ')
    latex = latex.replace('&amp;', '&')
    latex = latex.replace('&lt;', '<')
    latex = latex.replace('&gt;', '>')
    latex = latex.replace('&quot;', '"')
    
    return latex.strip()


def build_assignment_content(
    title: str,
    content: str,
    author: str = "Author",
    course: Optional[str] = None,
    date: Optional[str] = None,
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for Assignment template.
    
    Args:
        title: Document title
        content: Main content (markdown or HTML)
        author: Author name
        course: Course name (optional)
        date: Date (optional)
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_essay_content(
    title: str,
    content: str,
    author: str = "Author",
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for Essay template.
    
    Args:
        title: Document title
        content: Main content (markdown or HTML)
        author: Author name
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_neurips2025_content(
    title: str,
    content: str,
    authors: Optional[str] = None,
    abstract: Optional[str] = None,
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for NeurIPS 2025 template.
    
    Args:
        title: Paper title
        content: Main content (markdown or HTML)
        authors: Author names (optional)
        abstract: Abstract text (optional)
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_presentation_content(
    title: str,
    content: str,
    author: str = "Author",
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for Presentation/Beamer template.
    
    Args:
        title: Presentation title
        content: Main content (markdown or HTML)
        author: Author name
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_cv_content(
    name: str,
    content: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for CV template.
    
    Args:
        name: Full name
        content: CV content (markdown or HTML)
        email: Email address (optional)
        phone: Phone number (optional)
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_thesis_content(
    title: str,
    content: str,
    author: str = "Author",
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for Thesis template.
    
    Args:
        title: Thesis title
        content: Main content (markdown or HTML)
        author: Author name
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content


def build_report_content(
    title: str,
    content: str,
    author: str = "Author",
    **kwargs
) -> str:
    """
    Build LaTeX content formatted for Report template.
    
    Args:
        title: Report title
        content: Main content (markdown or HTML)
        author: Author name
        **kwargs: Additional parameters
        
    Returns:
        LaTeX formatted content string
    """
    # Convert content to LaTeX
    if content.startswith('<'):
        latex_content = html_to_latex(content)
    else:
        latex_content = markdown_to_latex(content)
    
    return latex_content
