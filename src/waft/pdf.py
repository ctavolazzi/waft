"""
Unified PDF Production Class

Single entry point for all PDF generation in WAFT. Consolidates multiple approaches
into one class with many methods instead of many classes.

This replaces:
- PDFGenerator (evolution system)
- DocumentBuilder (template system)
- DocumentEngine (Foundation V1/V2)
- TwoPageGenerator
- ScientificPDFGenerator
- ComponentPDFGenerator
- LaTeXGenerator
- FlexiblePDFGenerator

Usage:
    from waft import PDF
    
    # Template-based (WeasyPrint + Jinja2)
    PDF.from_template(
        template="field_guide",
        title="My Guide",
        content="<h2>Intro</h2><p>Content</p>"
    ).save("output.pdf")
    
    # Evolution-based (ChatDistiller + StylingGenome)
    PDF.from_content(
        content="# My Document\n\nContent...",
        title="My Document",
        style="clinical_standard"
    ).save("output.pdf")
    
    # Foundation-based (FPDF2 blocks)
    PDF.from_blocks(
        title="My Report",
        blocks=[SectionHeader("Title"), TextBlock("Content")]
    ).save("output.pdf")
    
    # Simple markdown/HTML
    PDF.from_markdown("# Title\n\nContent").save("output.pdf")
    PDF.from_html("<h1>Title</h1><p>Content</p>").save("output.pdf")
    
    # Scientific paper
    PDF.scientific_paper(
        title="Research Paper",
        abstract="Abstract text...",
        content="<h2>Introduction</h2>..."
    ).save("paper.pdf")
    
    # Two-page constraint
    PDF.two_page(
        content="# Title\n\nContent...",
        title="Two Page Doc"
    ).save("two_page.pdf")
    
    # LaTeX
    PDF.latex(
        title="LaTeX Doc",
        content="\\section{Introduction}\n\\paragraph{Content}"
    ).save("latex.pdf")
"""

from pathlib import Path
from typing import Optional, Union, List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

# Import all the underlying systems
from .document_builder import DocumentBuilder, DocumentConfig, TemplateType
from .evolution.pdf_generator import PDFGenerator
from .evolution.scientific_pdf_generator import ScientificPDFGenerator
from .evolution.two_page_generator import TwoPageGenerator
from .evolution.latex_generator import LaTeXGenerator
from .evolution.component_generator import ComponentPDFGenerator
from .foundation import DocumentEngine as FoundationV1Engine, DocumentConfig as FoundationConfig, ContentBlock
from .foundation_v2 import DocumentEngine as FoundationV2Engine, DocumentConfig as FoundationV2Config
from .evolution.golden_triangle import GoldenTriangle


@dataclass
class PDFConfig:
    """Unified configuration for PDF generation."""
    # Common options
    title: str
    content: Optional[str] = None
    output_path: Optional[Path] = None
    open_pdf: bool = False
    printer_friendly: bool = False
    
    # Template options
    template: Optional[Union[str, TemplateType]] = None
    series: str = "FIELD GUIDE"
    number: str = "FG-001"
    subtitle: Optional[str] = None
    
    # Evolution options
    style: str = "clinical_standard"  # clinical_standard, premium, professional
    author: Optional[Union[str, List[str]]] = None
    subject: Optional[str] = None
    keywords: Optional[Union[str, List[str]]] = None
    
    # Foundation options
    use_foundation_v2: bool = False
    blocks: Optional[List[ContentBlock]] = None
    
    # Two-page options
    target_pages: Optional[int] = None
    max_pages: Optional[int] = None
    min_pages: Optional[int] = None
    
    # Scientific paper options
    abstract: Optional[str] = None
    authors: Optional[List[str]] = None
    affiliations: Optional[List[str]] = None
    references: Optional[List[str]] = None
    
    # LaTeX options
    compile_latex: bool = False
    
    # Custom styling
    custom_css: Optional[str] = None
    font_size: Optional[int] = None
    margins: Optional[Union[int, Tuple[int, int, int, int]]] = None


class PDF:
    """
    Unified PDF production class.
    
    Single entry point for all PDF generation in WAFT. Provides methods
    for different generation approaches (template, evolution, foundation, etc.)
    instead of requiring different classes.
    """
    
    def __init__(self, config: PDFConfig):
        """Initialize with configuration."""
        self.config = config
        self._generated_path: Optional[Path] = None
        self._backend: Optional[Any] = None  # Store backend instance
    
    # ============================================================================
    # Factory Methods - Different Generation Approaches
    # ============================================================================
    
    @classmethod
    def from_template(
        cls,
        template: Union[str, TemplateType],
        title: str,
        content: str,
        output_path: Optional[Path] = None,
        printer_friendly: bool = False,
        series: str = "FIELD GUIDE",
        number: str = "FG-001",
        subtitle: Optional[str] = None,
        **kwargs
    ) -> "PDF":
        """
        Generate PDF using template system (WeasyPrint + Jinja2).
        
        Best for: Professional documents with consistent formatting.
        Uses: DocumentBuilder + Template Registry
        
        Args:
            template: Template name or TemplateType enum
            title: Document title
            content: HTML content
            output_path: Optional output path
            printer_friendly: Convert to printer-friendly (white background)
            series: Document series (e.g., "FIELD GUIDE")
            number: Document number (e.g., "FG-001")
            subtitle: Optional subtitle
            **kwargs: Additional template-specific options
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            content=content,
            output_path=output_path,
            printer_friendly=printer_friendly,
            template=template,
            series=series,
            number=number,
            subtitle=subtitle
        )
        pdf = cls(config)
        pdf._backend = "template"
        return pdf
    
    @classmethod
    def from_content(
        cls,
        content: str,
        title: str,
        style: str = "clinical_standard",
        output_path: Optional[Path] = None,
        open_pdf: bool = False,
        author: Optional[Union[str, List[str]]] = None,
        subject: Optional[str] = None,
        keywords: Optional[Union[str, List[str]]] = None,
        custom_css: Optional[str] = None,
        **overrides
    ) -> "PDF":
        """
        Generate PDF using evolution system (ChatDistiller + StylingGenome).
        
        Best for: Markdown/text content with automatic idea extraction.
        Uses: PDFGenerator + ChatDistiller + StylingGenome + TwoPageGenerator
        
        Args:
            content: Markdown or text content
            title: Document title
            style: Preset style ("clinical_standard", "premium", "professional")
            output_path: Optional output path
            open_pdf: Open PDF after generation
            author: Optional author name(s)
            subject: Optional document subject
            keywords: Optional keywords
            custom_css: Optional additional CSS
            **overrides: Override preset values (font_size, margins, line_height)
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            content=content,
            output_path=output_path,
            open_pdf=open_pdf,
            style=style,
            author=author,
            subject=subject,
            keywords=keywords,
            custom_css=custom_css
        )
        pdf = cls(config)
        pdf._backend = "evolution"
        return pdf
    
    @classmethod
    def from_blocks(
        cls,
        title: str,
        blocks: List[ContentBlock],
        use_foundation_v2: bool = False,
        output_path: Optional[Path] = None,
        **foundation_config
    ) -> "PDF":
        """
        Generate PDF using Foundation system (FPDF2 blocks).
        
        Best for: Programmatic document construction with precise control.
        Uses: DocumentEngine (Foundation V1 or V2)
        
        Args:
            title: Document title
            blocks: List of ContentBlock instances
            use_foundation_v2: Use Foundation V2 (better typography)
            output_path: Optional output path
            **foundation_config: Foundation-specific configuration
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            output_path=output_path,
            use_foundation_v2=use_foundation_v2,
            blocks=blocks
        )
        pdf = cls(config)
        pdf._backend = "foundation"
        return pdf
    
    @classmethod
    def from_markdown(
        cls,
        markdown: str,
        title: Optional[str] = None,
        style: str = "premium",
        output_path: Optional[Path] = None
    ) -> "PDF":
        """
        Generate PDF directly from markdown (simple path).
        
        Best for: Quick markdown-to-PDF conversion.
        Uses: GoldenTriangle
        
        Args:
            markdown: Markdown content
            title: Optional title (extracted from markdown if not provided)
            style: Style preset
            output_path: Optional output path
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title or "Document",
            content=markdown,
            output_path=output_path,
            style=style
        )
        pdf = cls(config)
        pdf._backend = "markdown"
        return pdf
    
    @classmethod
    def from_html(
        cls,
        html: str,
        title: Optional[str] = None,
        output_path: Optional[Path] = None
    ) -> "PDF":
        """
        Generate PDF directly from HTML (simple path).
        
        Best for: Quick HTML-to-PDF conversion.
        Uses: GoldenTriangle
        
        Args:
            html: HTML content
            title: Optional title
            output_path: Optional output path
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title or "Document",
            content=html,
            output_path=output_path
        )
        pdf = cls(config)
        pdf._backend = "html"
        return pdf
    
    @classmethod
    def scientific_paper(
        cls,
        title: str,
        content: str,
        abstract: Optional[str] = None,
        authors: Optional[List[str]] = None,
        affiliations: Optional[List[str]] = None,
        references: Optional[List[str]] = None,
        output_path: Optional[Path] = None,
        **kwargs
    ) -> "PDF":
        """
        Generate scientific paper PDF.
        
        Best for: Academic papers, research documents.
        Uses: ScientificPDFGenerator or academic_paper template
        
        Args:
            title: Paper title
            content: Paper content (HTML or markdown)
            abstract: Optional abstract
            authors: Optional list of authors
            affiliations: Optional list of affiliations
            references: Optional list of references
            output_path: Optional output path
            **kwargs: Additional options
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            content=content,
            output_path=output_path,
            abstract=abstract,
            authors=authors,
            affiliations=affiliations,
            references=references
        )
        pdf = cls(config)
        pdf._backend = "scientific"
        return pdf
    
    @classmethod
    def two_page(
        cls,
        content: str,
        title: str,
        style: str = "clinical_standard",
        output_path: Optional[Path] = None,
        **kwargs
    ) -> "PDF":
        """
        Generate PDF with strict 2-page constraint.
        
        Best for: One-pagers, summaries, executive briefs.
        Uses: TwoPageGenerator with adaptive constraint enforcement
        
        Args:
            content: Content (markdown or text)
            title: Document title
            style: Style preset
            output_path: Optional output path
            **kwargs: Additional options
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            content=content,
            output_path=output_path,
            style=style,
            target_pages=2
        )
        pdf = cls(config)
        pdf._backend = "two_page"
        return pdf
    
    @classmethod
    def latex(
        cls,
        title: str,
        content: str,
        output_path: Optional[Path] = None,
        compile_pdf: bool = False,
        **kwargs
    ) -> "PDF":
        """
        Generate PDF from LaTeX.
        
        Best for: Academic papers, complex mathematical documents.
        Uses: LaTeXGenerator
        
        Args:
            title: Document title
            content: LaTeX content
            output_path: Optional output path
            compile_pdf: Compile LaTeX to PDF (requires LaTeX installation)
            **kwargs: Additional options
        
        Returns:
            PDF instance
        """
        config = PDFConfig(
            title=title,
            content=content,
            output_path=output_path,
            compile_latex=compile_pdf
        )
        pdf = cls(config)
        pdf._backend = "latex"
        return pdf
    
    @classmethod
    def from_file(
        cls,
        file_path: Union[str, Path],
        template: Optional[Union[str, TemplateType]] = None,
        style: str = "clinical_standard",
        output_path: Optional[Path] = None,
        **kwargs
    ) -> "PDF":
        """
        Generate PDF from file (auto-detects format).
        
        Best for: Converting existing files to PDF.
        
        Args:
            file_path: Path to file (markdown, HTML, or PDF)
            template: Optional template (for markdown/HTML)
            style: Style preset (for markdown/HTML)
            output_path: Optional output path
            **kwargs: Additional options
        
        Returns:
            PDF instance
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Detect file type
        if file_path.suffix == ".pdf":
            # Analyze and recreate PDF
            return cls.from_pdf(file_path, output_path=output_path)
        elif file_path.suffix in [".md", ".markdown"]:
            # Markdown file
            content = file_path.read_text()
            title = file_path.stem.replace("_", " ").title()
            if template:
                return cls.from_template(template, title, content, output_path, **kwargs)
            else:
                return cls.from_content(content, title, style, output_path, **kwargs)
        elif file_path.suffix in [".html", ".htm"]:
            # HTML file
            content = file_path.read_text()
            title = file_path.stem.replace("_", " ").title()
            if template:
                return cls.from_template(template, title, content, output_path, **kwargs)
            else:
                return cls.from_html(content, title, output_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    @classmethod
    def from_pdf(
        cls,
        pdf_path: Union[str, Path],
        output_path: Optional[Path] = None
    ) -> "PDF":
        """
        Analyze and recreate PDF from existing PDF.
        
        Best for: PDF recreation, template detection.
        Uses: DocumentBuilder.from_pdf()
        
        Args:
            pdf_path: Path to source PDF
            output_path: Optional output path for recreated PDF
        
        Returns:
            PDF instance
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        # Use DocumentBuilder to analyze and recreate
        builder = DocumentBuilder.from_pdf(pdf_path)
        
        config = PDFConfig(
            title=builder.config.title,
            content=builder.config.content,
            output_path=output_path,
            template=builder.config.template
        )
        pdf = cls(config)
        pdf._backend = "template"
        pdf._builder = builder  # Store builder for recreation
        return pdf
    
    # ============================================================================
    # Generation Methods
    # ============================================================================
    
    def save(
        self,
        output_path: Optional[Path] = None,
        open_pdf: bool = False,
        **kwargs
    ) -> Path:
        """
        Generate and save PDF.
        
        Args:
            output_path: Output path (uses config.output_path if not provided)
            open_pdf: Open PDF after generation
            **kwargs: Backend-specific options
        
        Returns:
            Path to generated PDF
        """
        output_path = output_path or self.config.output_path
        
        # Route to appropriate backend
        if self._backend == "template":
            return self._save_template(output_path, open_pdf, **kwargs)
        elif self._backend == "evolution":
            return self._save_evolution(output_path, open_pdf, **kwargs)
        elif self._backend == "foundation":
            return self._save_foundation(output_path, open_pdf, **kwargs)
        elif self._backend == "markdown":
            return self._save_markdown(output_path, open_pdf, **kwargs)
        elif self._backend == "html":
            return self._save_html(output_path, open_pdf, **kwargs)
        elif self._backend == "scientific":
            return self._save_scientific(output_path, open_pdf, **kwargs)
        elif self._backend == "two_page":
            return self._save_two_page(output_path, open_pdf, **kwargs)
        elif self._backend == "latex":
            return self._save_latex(output_path, open_pdf, **kwargs)
        else:
            raise ValueError(f"Unknown backend: {self._backend}")
    
    def _save_template(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using template system."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.pdf")
        
        # Use storage path resolver to route to external drive if available
        from .utils import resolve_output_path
        output_path = resolve_output_path(Path(output_path))
        
        # Check if we have a builder from from_pdf()
        if hasattr(self, '_builder'):
            return self._builder.recreate(output_path)
        
        # Create new builder
        template = self.config.template or TemplateType.FIELD_GUIDE
        if isinstance(template, str):
            # Try to find template by name
            try:
                template = TemplateType[template.upper()]
            except KeyError:
                template = TemplateType.FIELD_GUIDE
        
        config = DocumentConfig(
            template=template,
            title=self.config.title,
            content=self.config.content or "",
            output_path=output_path,
            printer_friendly=self.config.printer_friendly,
            series=self.config.series,
            number=self.config.number,
            subtitle=self.config.subtitle
        )
        
        builder = DocumentBuilder(config)
        pdf_path = builder.generate(output_path)
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_evolution(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using evolution system."""
        generator = PDFGenerator.from_content(
            content=self.config.content or "",
            title=self.config.title,
            style=self.config.style,
            output_path=output_path,
            author=self.config.author,
            subject=self.config.subject,
            keywords=self.config.keywords,
            custom_css=self.config.custom_css,
            font_size=self.config.font_size,
            margins=self.config.margins
        )
        
        pdf_path = generator.save(
            output_path=output_path,
            open_pdf=open_pdf,
            **kwargs
        )
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_foundation(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using Foundation system."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.pdf")
        
        # Create Foundation config
        if self.config.use_foundation_v2:
            # Foundation V2
            foundation_config = FoundationV2Config(
                title=self.config.title,
                page_margins=(25.4, 25.4, 25.4, 25.4)  # 1 inch
            )
            engine = FoundationV2Engine(foundation_config)
        else:
            # Foundation V1
            foundation_config = FoundationConfig(
                title=self.config.title,
                page_margins=(25.4, 25.4, 25.4, 25.4)
            )
            engine = FoundationV1Engine(foundation_config)
        
        # Add blocks
        if self.config.blocks:
            for block in self.config.blocks:
                engine.add(block)
        
        pdf_path = engine.render(output_path)
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_markdown(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using markdown-to-PDF (GoldenTriangle)."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.pdf")
        
        golden_triangle = GoldenTriangle()
        pdf_path = golden_triangle.markdown_to_pdf(
            markdown_text=self.config.content or "",
            output_path=output_path,
            style=self.config.style
        )
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_html(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using HTML-to-PDF (GoldenTriangle)."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.pdf")
        
        golden_triangle = GoldenTriangle()
        pdf_path = golden_triangle.html_to_pdf(
            html=self.config.content or "",
            output_path=output_path
        )
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_scientific(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using scientific paper generator."""
        generator = ScientificPDFGenerator.from_content(
            content=self.config.content or "",
            title=self.config.title,
            abstract=self.config.abstract,
            authors=self.config.authors,
            affiliations=self.config.affiliations,
            references=self.config.references,
            style=self.config.style
        )
        
        pdf_path = generator.save(
            output_path=output_path,
            open_pdf=open_pdf,
            **kwargs
        )
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_two_page(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using two-page generator."""
        from .evolution.chat_distiller import ChatDistiller
        from .evolution.styling_genome import StylingGenome, StylingGenomeRegistry
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.pdf")
        
        # Create distilled chat from content
        distiller = ChatDistiller()
        distilled_chat = distiller.distill_text(self.config.content or "", title=self.config.title)
        
        # Create styling genome
        registry = StylingGenomeRegistry(registry_dir=Path("_genetics/pdf_generator"))
        style = self.config.style or "clinical_standard"
        if style not in PDFGenerator.PRESETS:
            style = "clinical_standard"
        preset = PDFGenerator.PRESETS[style].copy()
        
        from .evolution.styling_genome import StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
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
            name=f"{style.title()} - {self.config.title[:30]}"
        )
        styling_genome = StylingGenome.from_genes(styling_genes)
        registry.register(styling_genome)
        
        # Generate PDF
        generator = TwoPageGenerator(weasyprint_available=True, allowed_pages=2)
        result = generator.generate(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            output_path=output_path
        )
        
        pdf_path = Path(result.get("output_path", output_path))
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _save_latex(self, output_path: Optional[Path], open_pdf: bool, **kwargs) -> Path:
        """Save using LaTeX generator."""
        from .evolution.latex_generator import LaTeXGenerator
        from .evolution.chat_distiller import ChatDistiller
        from .evolution.styling_genome import StylingGenome, StylingGenomeRegistry
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.config.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/{safe_title}_{timestamp}.tex")
        
        # Create distilled chat from content
        distiller = ChatDistiller()
        distilled_chat = distiller.distill_text(self.config.content or "", title=self.config.title)
        
        # Create styling genome
        registry = StylingGenomeRegistry(registry_dir=Path("_genetics/pdf_generator"))
        style = self.config.style or "clinical_standard"
        if style not in PDFGenerator.PRESETS:
            style = "clinical_standard"
        preset = PDFGenerator.PRESETS[style].copy()
        
        from .evolution.styling_genome import StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
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
            name=f"{style.title()} - {self.config.title[:30]}"
        )
        styling_genome = StylingGenome.from_genes(styling_genes)
        registry.register(styling_genome)
        
        # Generate LaTeX
        generator = LaTeXGenerator(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome
        )
        
        latex_content = generator.generate()
        output_path.write_text(latex_content, encoding='utf-8')
        pdf_path = output_path
        
        if open_pdf:
            self._open_pdf(pdf_path)
        
        self._generated_path = pdf_path
        return pdf_path
    
    def _open_pdf(self, pdf_path: Path) -> None:
        """Open PDF in default viewer."""
        import subprocess
        import platform
        import os
        
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=False)
        elif platform.system() == "Windows":
            os.startfile(str(pdf_path))
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=False)
    
    # ============================================================================
    # Utility Methods
    # ============================================================================
    
    @property
    def path(self) -> Optional[Path]:
        """Get path to generated PDF."""
        return self._generated_path
    
    def open(self) -> None:
        """Open generated PDF."""
        if not self._generated_path:
            raise ValueError("PDF not generated yet. Call save() first.")
        self._open_pdf(self._generated_path)
    
    def print(self) -> None:
        """Print PDF to default printer."""
        if not self._generated_path:
            raise ValueError("PDF not generated yet. Call save() first.")
        
        import subprocess
        import platform
        import os
        
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["lpr", str(self._generated_path)], check=False)
        elif platform.system() == "Windows":
            os.startfile(str(self._generated_path), "print")
        else:  # Linux
            subprocess.run(["lpr", str(self._generated_path)], check=False)
