"""
LaTeX Generator for WAFT

Generates LaTeX documents from content, integrating with WAFT's evolution system.
Supports scientific paper format, research reports, and documentation.

Usage:
    from src.waft.evolution.latex_generator import LaTeXGenerator
    
    generator = LaTeXGenerator.from_content(
        content="# My Document\n\nContent here...",
        title="My Document",
        document_class="article"
    )
    generator.save("output.tex")
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import re

from .chat_distiller import ChatDistiller, DistilledChat
from .styling_genome import StylingGenome, StylingGenomeRegistry


class LaTeXGenerator:
    """
    Generate LaTeX documents from content using WAFT's evolution system.
    
    Integrates with:
    - ChatDistiller: Extract structured ideas from content
    - StylingGenome: Apply styling configurations
    - Research tools: Scientific paper format support
    """
    
    def __init__(
        self,
        distilled_chat: DistilledChat,
        styling_genome: Optional[StylingGenome] = None,
        document_class: str = "article",
        packages: Optional[List[str]] = None,
        custom_preamble: Optional[str] = None
    ):
        self.distilled_chat = distilled_chat
        # Create default styling genome if not provided
        if styling_genome is None:
            from .pdf_generator import PDFGenerator
            preset = PDFGenerator.PRESETS["clinical_standard"].copy()
            from .styling_genome import StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
            styling_genes = StylingGene(
                font=FontGene(**preset["font"]),
                margin=MarginGene(**preset["margin"]),
                color=ColorGene(**preset["color"]),
                layout=LayoutGene(columns=1, density="normal", toc_enabled=False, page_numbers=True, header_enabled=True, footer_enabled=True),
                name="Clinical Standard"
            )
            styling_genome = StylingGenome.from_genes(styling_genes)
        
        self.styling_genome = styling_genome
        self.document_class = document_class
        self.packages = packages or self._default_packages()
        self.custom_preamble = custom_preamble
        self._generated_path: Optional[Path] = None
    
    @classmethod
    def from_content(
        cls,
        content: str,
        title: str,
        document_class: str = "article",
        style: str = "clinical_standard",
        packages: Optional[List[str]] = None,
        custom_preamble: Optional[str] = None
    ) -> "LaTeXGenerator":
        """Create LaTeX generator from markdown content."""
        # Distill content to extract ideas
        distiller = ChatDistiller()
        distilled_chat = distiller.distill_text(content, title=title)
        
        # Get styling genome from PDFGenerator presets (same approach)
        from .pdf_generator import PDFGenerator
        if style not in PDFGenerator.PRESETS:
            raise ValueError(f"Unknown style: {style}. Available: {list(PDFGenerator.PRESETS.keys())}")
        
        preset = PDFGenerator.PRESETS[style].copy()
        
        # Create styling genome from preset
        from .styling_genome import StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
        
        styling_genes = StylingGene(
            font=FontGene(**preset["font"]),
            margin=MarginGene(**preset["margin"]),
            color=ColorGene(**preset["color"]),
            layout=LayoutGene(
                columns=1,
                density="normal",
                toc_enabled=False,
                page_numbers=True,
                header_enabled=True,
                footer_enabled=True
            ),
            name=f"{style.title()} - {title[:30]}"
        )
        
        styling_genome = StylingGenome.from_genes(styling_genes)
        
        return cls(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            document_class=document_class,
            packages=packages,
            custom_preamble=custom_preamble
        )
    
    def _default_packages(self) -> List[str]:
        """Default LaTeX packages for scientific documents."""
        return [
            "amsmath",
            "amsfonts",
            "amssymb",
            "geometry",
            "graphicx",
            "hyperref",
            "xcolor",
            "booktabs",
            "longtable",
            "enumitem",
            "fancyhdr",
            "titlesec",
        ]
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        # LaTeX special characters that need escaping
        replacements = {
            '\\': r'\textbackslash{}',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '~': r'\textasciitilde{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def _markdown_to_latex(self, markdown: str) -> str:
        """Convert markdown to LaTeX."""
        lines = markdown.split('\n')
        latex_lines = []
        in_list = False
        list_type = None
        
        for line in lines:
            # Headers
            if line.startswith('# '):
                latex_lines.append(r'\section{' + self._escape_latex(line[2:].strip()) + '}')
                in_list = False
            elif line.startswith('## '):
                latex_lines.append(r'\subsection{' + self._escape_latex(line[3:].strip()) + '}')
                in_list = False
            elif line.startswith('### '):
                latex_lines.append(r'\subsubsection{' + self._escape_latex(line[4:].strip()) + '}')
                in_list = False
            # Lists
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                if not in_list:
                    latex_lines.append(r'\begin{itemize}')
                    in_list = True
                    list_type = 'itemize'
                item_text = line.strip()[2:].strip()
                latex_lines.append(r'\item ' + self._escape_latex(item_text))
            elif line.strip().startswith(tuple(f'{i}. ' for i in range(1, 100))):
                if not in_list or list_type != 'enumerate':
                    if in_list:
                        latex_lines.append(r'\end{' + list_type + '}')
                    latex_lines.append(r'\begin{enumerate}')
                    in_list = True
                    list_type = 'enumerate'
                # Extract number and text
                match = re.match(r'^\s*(\d+)\.\s*(.*)', line.strip())
                if match:
                    item_text = match.group(2)
                    latex_lines.append(r'\item ' + self._escape_latex(item_text))
            # Code blocks
            elif line.strip().startswith('```'):
                if '```' in line and not line.strip().endswith('```'):
                    latex_lines.append(r'\begin{verbatim}')
                else:
                    latex_lines.append(r'\end{verbatim}')
            # Horizontal rule
            elif line.strip() == '---' or line.strip() == '***':
                latex_lines.append(r'\hline')
                in_list = False
            # Empty line
            elif not line.strip():
                if in_list:
                    # Don't close list on single empty line
                    pass
                else:
                    latex_lines.append('')
            # Regular paragraph
            else:
                if in_list:
                    latex_lines.append(r'\end{' + list_type + '}')
                    in_list = False
                escaped = self._escape_latex(line.strip())
                if escaped:
                    latex_lines.append(escaped)
        
        # Close any open list
        if in_list:
            latex_lines.append(r'\end{' + list_type + '}')
        
        return '\n'.join(latex_lines)
    
    def _generate_preamble(self) -> str:
        """Generate LaTeX document preamble."""
        preamble = f"\\documentclass[{self._get_document_options()}]{{{self.document_class}}}\n\n"
        
        # Add packages
        for package in self.packages:
            preamble += f"\\usepackage{{{package}}}\n"
        
        # Geometry settings from styling genome
        margin = self.styling_genome.genes.margin
        preamble += f"\\geometry{{"
        preamble += f"left={margin.left}mm,"
        preamble += f"right={margin.right}mm,"
        preamble += f"top={margin.top}mm,"
        preamble += f"bottom={margin.bottom}mm"
        preamble += f"}}\n\n"
        
        # Hyperref settings
        preamble += r"\hypersetup{"
        preamble += r"colorlinks=true,"
        preamble += r"linkcolor=blue,"
        preamble += r"urlcolor=blue,"
        preamble += r"citecolor=blue"
        preamble += r"}\n\n"
        
        # Custom preamble if provided
        if self.custom_preamble:
            preamble += self.custom_preamble + "\n\n"
        
        # Title formatting
        font = self.styling_genome.genes.font
        preamble += f"\\setlength{{\\parindent}}{{0pt}}\n"
        preamble += f"\\setlength{{\\parskip}}{{{font.line_height}em}}\n"
        preamble += f"\\renewcommand{{\\baselinestretch}}{{{font.line_height}}}\n\n"
        
        # Title format
        preamble += r"\titleformat{\section}"
        preamble += r"{\Large\bfseries}{\thesection}{1em}{}\n"
        preamble += r"\titleformat{\subsection}"
        preamble += r"{\large\bfseries}{\thesubsection}{1em}{}\n\n"
        
        return preamble
    
    def _get_document_options(self) -> str:
        """Get document class options."""
        options = []
        
        # Font size from styling genome
        font = self.styling_genome.genes.font
        if font.size_body <= 10:
            options.append("10pt")
        elif font.size_body <= 11:
            options.append("11pt")
        else:
            options.append("12pt")
        
        # Paper size (assuming letter for now)
        options.append("letterpaper")
        
        return ",".join(options)
    
    def _generate_content(self) -> str:
        """Generate LaTeX document content from distilled chat."""
        content = []
        
        # Title
        content.append(r"\begin{document}")
        content.append(r"\maketitle")
        content.append("")
        
        # Abstract if available
        if self.distilled_chat.summary:
            content.append(r"\begin{abstract}")
            content.append(self._escape_latex(self.distilled_chat.summary))
            content.append(r"\end{abstract}")
            content.append("")
        
        # Main content from ideas
        ideas = self.distilled_chat.ideas
        
        if ideas:
            # Group ideas by category for better structure
            concepts = [idea for idea in ideas if idea.category == "concept"]
            decisions = [idea for idea in ideas if idea.category == "decision"]
            insights = [idea for idea in ideas if idea.category == "insight"]
            actions = [idea for idea in ideas if idea.category == "action"]
            
            # Concepts section
            if concepts:
                content.append(r"\section{Key Concepts}")
                for idea in concepts:
                    content.append(self._escape_latex(idea.content))
                    content.append("")
            
            # Decisions section
            if decisions:
                content.append(r"\section{Decisions}")
                content.append(r"\begin{itemize}")
                for idea in decisions:
                    content.append(r"\item " + self._escape_latex(idea.content))
                content.append(r"\end{itemize}")
                content.append("")
            
            # Insights section
            if insights:
                content.append(r"\section{Insights}")
                for idea in insights:
                    content.append(self._escape_latex(idea.content))
                    content.append("")
            
            # Actions section
            if actions:
                content.append(r"\section{Actions}")
                content.append(r"\begin{itemize}")
                for idea in actions:
                    content.append(r"\item " + self._escape_latex(idea.content))
                content.append(r"\end{itemize}")
                content.append("")
        else:
            # Fallback: use summary and all ideas
            if self.distilled_chat.summary:
                content.append(r"\section{Summary}")
                content.append(self._escape_latex(self.distilled_chat.summary))
                content.append("")
            
            # Add all ideas as a general section
            if ideas:
                content.append(r"\section{Content}")
                for idea in ideas:
                    content.append(self._escape_latex(idea.content))
                    content.append("")
        
        # End document
        content.append(r"\end{document}")
        
        return "\n".join(content)
    
    def generate(self) -> str:
        """Generate complete LaTeX document."""
        latex = []
        
        # Preamble
        latex.append(self._generate_preamble())
        
        # Title info
        latex.append(f"\\title{{{self._escape_latex(self.distilled_chat.title)}}}")
        latex.append(f"\\author{{WAFT Document Generator}}")
        latex.append(f"\\date{{\\today}}")
        latex.append("")
        
        # Content
        latex.append(self._generate_content())
        
        return "\n".join(latex)
    
    def save(self, output_path: Optional[Path] = None, compile_pdf: bool = False) -> Path:
        """Save LaTeX document to file."""
        if output_path is None:
            # Generate default path
            safe_title = re.sub(r'[^\w\s-]', '', self.distilled_chat.title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            output_path = Path(f"{safe_title}.tex")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate LaTeX
        latex_content = self.generate()
        output_path.write_text(latex_content, encoding='utf-8')
        
        self._generated_path = output_path
        
        # Compile to PDF if requested
        if compile_pdf:
            self._compile_pdf(output_path)
        
        return output_path
    
    def _compile_pdf(self, tex_path: Path) -> Path:
        """Compile LaTeX to PDF using pdflatex."""
        import subprocess
        
        pdf_path = tex_path.with_suffix('.pdf')
        
        try:
            # Run pdflatex (may need multiple passes for references)
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', str(tex_path)],
                cwd=str(tex_path.parent),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Compiled LaTeX to PDF: {pdf_path}")
                return pdf_path
            else:
                print(f"⚠️  LaTeX compilation warnings (PDF may still be generated):")
                print(result.stderr)
                if pdf_path.exists():
                    return pdf_path
                else:
                    raise RuntimeError("PDF not generated despite compilation attempt")
        except FileNotFoundError:
            raise RuntimeError(
                "pdflatex not found. Install a LaTeX distribution:\n"
                "  - macOS: brew install --cask mactex\n"
                "  - Linux: sudo apt-get install texlive-full\n"
                "  - Windows: Install MiKTeX or TeX Live"
            )


def generate_latex(
    content: str,
    title: str,
    output_path: Optional[Path] = None,
    document_class: str = "article",
    style: str = "clinical_standard",
    compile_pdf: bool = False
) -> Path:
    """
    Quick function to generate LaTeX from content.
    
    Args:
        content: Markdown content
        title: Document title
        output_path: Output file path (default: {title}.tex)
        document_class: LaTeX document class (default: article)
        style: WAFT style preset (default: clinical_standard)
        compile_pdf: Whether to compile to PDF (requires pdflatex)
    
    Returns:
        Path to generated .tex file (or .pdf if compile_pdf=True)
    """
    generator = LaTeXGenerator.from_content(
        content=content,
        title=title,
        document_class=document_class,
        style=style
    )
    
    return generator.save(output_path=output_path, compile_pdf=compile_pdf)
