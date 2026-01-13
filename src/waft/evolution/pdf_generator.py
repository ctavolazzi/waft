"""
Composable PDF Generator - Simple, Modular API

Provides a clean, composable interface for generating PDFs with minimal boilerplate.
Uses ChatDistiller, StylingGenome, and TwoPageGenerator under the hood.

Example:
    from src.waft.evolution.pdf_generator import PDFGenerator
    
    # Simple usage
    PDFGenerator.from_content(
        content="# My Document\n\nContent here...",
        title="My Document",
        style="clinical_standard"
    ).save("output.pdf")
    
    # With custom styling
    PDFGenerator.from_content(
        content="# My Document\n\nContent here...",
        title="My Document",
        style="clinical_standard",
        margins=(30, 30, 30, 30),
        font_size=12
    ).save("output.pdf")
    
    # From file
    PDFGenerator.from_file(
        "content.md",
        style="premium"
    ).save("output.pdf")
"""

from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Union, List
from datetime import datetime

from .chat_distiller import ChatDistiller
from .two_page_generator import TwoPageGenerator
from .golden_triangle import GoldenTriangle
from .styling_genome import (
    StylingGenome,
    StylingGenomeRegistry,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene
)


class PDFGenerator:
    """
    Composable PDF generator with presets and simple API.
    
    Reduces boilerplate by providing:
    - Preset styling configurations
    - Simple content-to-PDF pipeline
    - Automatic idea extraction
    - Flexible customization
    """
    
    # Preset configurations
    PRESETS = {
        "clinical_standard": {
            "font": {
                "family": "'Times New Roman', 'Times', serif",
                "size_body": 11,
                "size_h1": 16,
                "size_h2": 14,
                "size_h3": 12,
                "size_code": 9,
                "line_height": 1.4
            },
            "margin": {
                "top": 25.4,  # 1 inch
                "bottom": 25.4,
                "left": 25.4,
                "right": 25.4,
                "section_spacing": 12,
                "paragraph_spacing": 8
            },
            "color": {
                "text": "#000000",
                "background": "#FFFFFF",
                "heading": "#000000",
                "accent": "#000000",
                "code_bg": "#f5f5f5",
                "code_text": "#000000",
                "border": "#cccccc"
            },
            "header_font": "'Helvetica', 'Arial', sans-serif"
        },
        "premium": {
            "font": {
                "family": "'Minion Pro', 'Palatino Linotype', 'Book Antiqua', 'Palatino', serif",
                "size_body": 13,
                "size_h1": 32,
                "size_h2": 22,
                "size_h3": 17,
                "size_code": 11,
                "line_height": 1.75
            },
            "margin": {
                "top": 40,
                "bottom": 40,
                "left": 40,
                "right": 40,
                "section_spacing": 24,
                "paragraph_spacing": 12
            },
            "color": {
                "text": "#1a1a1a",
                "background": "#FFFFFF",
                "heading": "#000000",
                "accent": "#0d47a1",
                "code_bg": "#f5f7fa",
                "code_text": "#1e3a5f",
                "border": "#b0bec5"
            },
            "header_font": None  # Use same as body
        },
        "professional": {
            "font": {
                "family": "'Georgia', serif",
                "size_body": 11,
                "size_h1": 20,
                "size_h2": 16,
                "size_h3": 13,
                "size_code": 9,
                "line_height": 1.6
            },
            "margin": {
                "top": 25,
                "bottom": 25,
                "left": 25,
                "right": 25,
                "section_spacing": 14,
                "paragraph_spacing": 8
            },
            "color": {
                "text": "#1a1a1a",
                "background": "#FFFFFF",
                "heading": "#000000",
                "accent": "#2c3e50",
                "code_bg": "#f8f9fa",
                "code_text": "#333333",
                "border": "#dee2e6"
            },
            "header_font": None
        }
    }
    
    def __init__(
        self,
        content: str,
        title: str,
        styling_genome: StylingGenome,
        distilled_chat=None,
        custom_css: Optional[str] = None
    ):
        """
        Initialize PDF generator.
        
        Args:
            content: Raw content (markdown/text)
            title: Document title
            styling_genome: Styling configuration
            distilled_chat: Pre-distilled chat (optional)
            custom_css: Additional CSS to inject
        """
        self.content = content
        self.title = title
        self.styling_genome = styling_genome
        self.distilled_chat = distilled_chat
        self.custom_css = custom_css
        self._generated_path: Optional[Path] = None
        self._style: Optional[str] = None  # Store style for golden triangle
        self._metadata: Dict[str, Any] = {}  # Store metadata for component generation
    
    @classmethod
    def from_content(
        cls,
        content: str,
        title: str,
        style: str = "clinical_standard",
        output_path: Optional[Path] = None,
        registry_dir: Optional[Path] = None,
        custom_css: Optional[str] = None,
        author: Optional[Union[str, List[str]]] = None,
        subject: Optional[str] = None,
        keywords: Optional[Union[str, List[str]]] = None,
        **overrides
    ) -> "PDFGenerator":
        """
        Create PDF generator from content string.
        
        Args:
            content: Content (markdown/text)
            title: Document title
            style: Preset style name ("clinical_standard", "premium", "professional")
            output_path: Optional output path
            registry_dir: Optional styling genome registry directory
            custom_css: Optional additional CSS
            author: Optional author name(s) - string or list of strings
            subject: Optional document subject/topic
            keywords: Optional keywords - string or list of strings
            **overrides: Override preset values (e.g., font_size=12, margins=(30,30,30,30))
        
        Returns:
            PDFGenerator instance
        """
        # Get preset
        if style not in cls.PRESETS:
            raise ValueError(f"Unknown style: {style}. Available: {list(cls.PRESETS.keys())}")
        
        preset = cls.PRESETS[style].copy()
        
        # Apply overrides
        if "font_size" in overrides:
            preset["font"]["size_body"] = overrides.pop("font_size")
        if "margins" in overrides:
            margins = overrides.pop("margins")
            if margins is not None:
                if isinstance(margins, (int, float)):
                    preset["margin"]["top"] = preset["margin"]["bottom"] = preset["margin"]["left"] = preset["margin"]["right"] = margins
                elif isinstance(margins, (list, tuple)) and len(margins) == 4:
                    preset["margin"]["top"], preset["margin"]["right"], preset["margin"]["bottom"], preset["margin"]["left"] = margins
        if "line_height" in overrides:
            preset["font"]["line_height"] = overrides.pop("line_height")
        
        # Create styling genome
        registry = StylingGenomeRegistry(registry_dir=registry_dir or Path("_genetics/pdf_generator"))
        
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
        
        genome = StylingGenome.from_genes(styling_genes)
        registry.register(genome)
        
        # Distill content
        distiller = ChatDistiller()
        distilled = distiller.distill_text(content, title=title)
        
        instance = cls(
            content=content,
            title=title,
            styling_genome=genome,
            distilled_chat=distilled,
            custom_css=custom_css
        )
        # Store metadata for later use in component generation
        instance._metadata = {
            'author': author,
            'subject': subject,
            'keywords': keywords,
            'style': style
        }
        return instance
    
    @classmethod
    def from_file(
        cls,
        file_path: Union[str, Path],
        title: Optional[str] = None,
        style: str = "clinical_standard",
        output_path: Optional[Path] = None,
        **kwargs
    ) -> "PDFGenerator":
        """
        Create PDF generator from file.
        
        Args:
            file_path: Path to content file
            title: Optional title (defaults to filename)
            style: Preset style name
            output_path: Optional output path
            **kwargs: Additional arguments passed to from_content
        
        Returns:
            PDFGenerator instance
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = file_path.read_text()
        title = title or file_path.stem.replace("_", " ").title()
        
        return cls.from_content(
            content=content,
            title=title,
            style=style,
            output_path=output_path,
            **kwargs
        )
    
    def save(
        self,
        output_path: Optional[Path] = None,
        open_pdf: bool = False,
        include_all_ideas: bool = True,
        target_pages: Optional[int] = None,
        convert_to_png: bool = True,
        png_dpi: int = 300
    ) -> Path:
        """
        Generate and save PDF.
        
        Args:
            output_path: Output path (auto-generated if None)
            open_pdf: Open PDF after generation
            include_all_ideas: Include all ideas (no page limit)
            target_pages: Target page count (None = no limit)
            convert_to_png: Convert PDF to PNG images after generation (default: True for evolutionary iteration)
            png_dpi: DPI for PNG conversion (default: 300)
        
        Returns:
            Path to generated PDF
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.title)
            safe_title = safe_title.replace(' ', '_')[:50]
            output_path = Path(f"_work_efforts/session_recaps/{safe_title}_{timestamp}.pdf")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # If using golden triangle (simpler path for direct markdown→PDF)
        if self.distilled_chat is None and self.styling_genome is None:
            # Direct markdown to PDF using golden triangle
            golden_triangle = GoldenTriangle()
            
            # Get style from stored value
            style = getattr(self, '_style', 'premium')
            
            # Convert markdown to PDF
            pdf_path = golden_triangle.markdown_to_pdf(
                self.content,
                output_path,
                css=self.custom_css,
                style=style
            )
            
            self._generated_path = pdf_path
            
            # Convert to PNG if requested
            if convert_to_png:
                try:
                    from .pdf_image_converter import pdf_to_pngs
                    png_paths = pdf_to_pngs(
                        pdf_path,
                        output_dir=pdf_path.parent,
                        dpi=png_dpi,
                        format='png'
                    )
                    if png_paths:
                        import shutil
                        img_path = pdf_path.with_suffix('.png')
                        shutil.copy(png_paths[0], img_path)
                        print(f"📸 PNG screenshot saved: {img_path}")
                except Exception as e:
                    print(f"⚠️  PNG conversion failed: {e}")
            
            # Open if requested
            if open_pdf:
                import subprocess
                subprocess.run(["open", str(pdf_path)])
            
            return pdf_path
        
        # Original implementation (for backward compatibility with ChatDistiller/TwoPageGenerator)
        # Get all ideas if requested
        if include_all_ideas:
            all_ideas = self.distilled_chat.get_top_ideas(n=1000, min_importance=0.0)
            mid_point = len(all_ideas) // 2
            page_1_ideas = all_ideas[:mid_point]
            page_2_ideas = all_ideas[mid_point:]
        else:
            # Use generator's adaptive selection
            page_1_ideas = None
            page_2_ideas = None
        
        # Generate PDF
        generator = TwoPageGenerator(weasyprint_available=True, allowed_pages=target_pages or 50)
        
        if page_1_ideas is not None:
            # Direct render with all ideas
            html_content = generator._render_html(
                distilled_chat=self.distilled_chat,
                styling_genome=self.styling_genome,
                page_1_ideas=page_1_ideas,
                page_2_ideas=page_2_ideas,
            )
            
            # Inject custom CSS if provided
            if self.custom_css:
                html_content = html_content.replace('</head>', self.custom_css + '</head>')
            
            # Save HTML
            html_path = output_path.with_suffix('.html')
            html_path.write_text(html_content)
            
            # Generate PDF using golden triangle (clean HTML → PDF)
            golden_triangle = GoldenTriangle()
            golden_triangle.html_to_pdf(
                html_content,
                output_path,
                base_url=str(output_path.parent)
            )
        else:
            # Use generator's adaptive system
            result = generator.generate(
                distilled_chat=self.distilled_chat,
                styling_genome=self.styling_genome,
                output_path=output_path,
                target_pages=target_pages,
                use_component_system=False
            )
            output_path = Path(result['pdf_path'])
        
        self._generated_path = output_path
        
        # Convert to PNG if requested (evolutionary iteration process)
        if convert_to_png:
            try:
                from .pdf_image_converter import pdf_to_pngs
                png_paths = pdf_to_pngs(
                    output_path,
                    output_dir=output_path.parent,
                    dpi=png_dpi,
                    format='png'
                )
                if png_paths:
                    # Copy first page to main PNG file for easy access
                    import shutil
                    img_path = output_path.with_suffix('.png')
                    shutil.copy(png_paths[0], img_path)
                    print(f"📸 PNG screenshot saved: {img_path}")
            except Exception as e:
                # Fallback: try PyMuPDF direct conversion
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(str(output_path))
                    if len(doc) > 0:
                        page = doc[0]
                        pix = page.get_pixmap(matrix=fitz.Matrix(png_dpi/72, png_dpi/72))
                        img_path = output_path.with_suffix('.png')
                        pix.save(str(img_path))
                        doc.close()
                        print(f"📸 PNG screenshot saved: {img_path}")
                except Exception:
                    print(f"⚠️  PNG conversion failed: {e}")
        
        # Open if requested
        if open_pdf:
            import subprocess
            subprocess.run(["open", str(output_path)])
        
        return output_path
    
    def with_custom_css(self, css: str) -> "PDFGenerator":
        """Add custom CSS to the generator."""
        self.custom_css = css
        return self
    
    def with_style(self, style: str, **overrides) -> "PDFGenerator":
        """Change style preset."""
        # Recreate with new style
        return self.from_content(
            content=self.content,
            title=self.title,
            style=style,
            custom_css=self.custom_css,
            **overrides
        )


# Convenience functions
def generate_pdf(
    content: str,
    title: str,
    output_path: Optional[Path] = None,
    style: str = "clinical_standard",
    convert_to_png: bool = True,
    png_dpi: int = 300,
    open_pdf: bool = False,
    **kwargs
) -> Path:
    """
    Quick function to generate a PDF.
    
    Example:
        generate_pdf(
            content="# My Doc\n\nContent...",
            title="My Document",
            style="clinical_standard",
            open_pdf=True
        )
    """
    generator = PDFGenerator.from_content(
        content=content,
        title=title,
        style=style,
        **kwargs
    )
    return generator.save(
        output_path=output_path,
        open_pdf=open_pdf,
        convert_to_png=convert_to_png,
        png_dpi=png_dpi
    )


def generate_pdf_from_file(
    file_path: Union[str, Path],
    output_path: Optional[Path] = None,
    style: str = "clinical_standard",
    open_pdf: bool = False,
    convert_to_png: bool = True,
    png_dpi: int = 300,
    **kwargs
) -> Path:
    """
    Quick function to generate PDF from file.
    
    Example:
        generate_pdf_from_file(
            "content.md",
            style="premium",
            open_pdf=True
        )
    """
    generator = PDFGenerator.from_file(
        file_path=file_path,
        style=style,
        **kwargs
    )
    return generator.save(
        output_path=output_path,
        open_pdf=open_pdf,
        convert_to_png=convert_to_png,
        png_dpi=png_dpi
    )
