"""
WAFT Document Builder - Unified PDF Generation Framework
=========================================================

A simplified, composable API for generating PDFs with WAFT templates.

Philosophy:
-----------
- Single entry point: DocumentBuilder
- Fluent API: chain methods for readability
- Presets: common configurations ready to use
- Composition: build complex documents from simple blocks
- Printer-friendly: one flag, automatic conversion
- Template Registry: Dynamic template discovery and management
- PDF Analysis: Can analyze and recreate PDFs from scratch

Example:
--------
    from waft import DocumentBuilder

    # Simple document
    DocumentBuilder.field_guide(
        title="My Guide",
        content="<h2>Introduction</h2><p>Content here</p>"
    ).save("output.pdf")

    # Analyze and recreate a PDF
    builder = DocumentBuilder.from_pdf("source.pdf")
    builder.recreate("recreated.pdf")

    # With options
    DocumentBuilder.field_guide(
        title="My Guide",
        content="<h2>Introduction</h2><p>Content here</p>",
        printer_friendly=True,
        series="MANUAL",
        number="M-001"
    ).save("output.pdf")

    # Multiple documents + binder
    docs = DocumentBuilder.collection("My Project")
    docs.add(
        DocumentBuilder.field_guide(title="Guide 1", content="...")
    )
    docs.add(
        DocumentBuilder.lab_notes(title="Notes 1", content="...")
    )
    docs.save("complete_booklet.pdf")  # Auto-creates binder
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import tempfile
import re
import json

from jinja2 import Template
from weasyprint import HTML
from pypdf import PdfReader
import sys

from .templates.registry import get_registry, TemplateRegistry, TemplateMetadata
from .binder import Binder, DocumentEntry, BinderSection
from .pdf_improvements import PDFContentProcessor, PDFStylingEnhancer

# Import printer_friendly_helper with path manipulation
# This is needed because scripts/ is not in the package path
try:
    # Try relative import first (if scripts is in path)
    from scripts.printer_friendly_helper import convert_html_template_to_printer_friendly
except ImportError:
    # Fallback: add project root to path
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from scripts.printer_friendly_helper import convert_html_template_to_printer_friendly


class TemplateType(Enum):
    """Available document templates."""
    FIELD_GUIDE = "field_guide"
    LAB_NOTES = "lab_notes"
    TM_REPORT = "tm_report"
    PERSONAL_MEMO = "personal_memo"
    ACADEMIC_PAPER = "academic_paper"
    SIMPLE_SCIENTIFIC = "simple_scientific"
    ELDRITCH_JOURNAL = "eldritch_journal"
    SCREENPLAY = "screenplay"
    HEARTFELT_LETTER = "heartfelt_letter"
    INVOICE = "invoice"
    CODE_DOCS = "code_docs"
    STORYBOOK = "storybook"
    NEWSPAPER = "newspaper"


@dataclass
class PDFAnalysis:
    """Analysis results from a PDF."""
    pdf_path: Path
    page_count: int
    metadata: Dict[str, Any]
    structure: Dict[str, Any] = field(default_factory=dict)
    content: str = ""
    detected_template: Optional[str] = None
    styling_hints: Dict[str, Any] = field(default_factory=dict)
    sections: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DocumentConfig:
    """Configuration for a single document."""
    template: Union[TemplateType, str]  # Can be enum or template name
    title: str
    content: str
    output_path: Optional[Path] = None
    printer_friendly: bool = False

    # Template-specific options (with defaults)
    series: str = "FIELD GUIDE"
    number: str = "FG-001"
    subtitle: Optional[str] = None
    classification: str = "FOR OFFICIAL USE ONLY"
    issued_by: Optional[str] = None
    date: Optional[str] = None

    # Additional metadata
    author: Optional[str] = None
    description: Optional[str] = None
    
    # Page count constraints (for feedback loop)
    max_pages: Optional[int] = None
    min_pages: Optional[int] = None
    exact_pages: Optional[int] = None
    max_iterations: int = 5  # Max attempts to meet constraints


class DocumentBuilder:
    """
    Unified document builder with fluent API and PDF recreation capabilities.

    Usage:
        # Simple
        doc = DocumentBuilder.field_guide(
            title="My Guide",
            content="<h2>Intro</h2><p>Content</p>"
        )
        doc.save("output.pdf")

        # Analyze and recreate PDF
        builder = DocumentBuilder.from_pdf("source.pdf")
        builder.recreate("recreated.pdf")

        # With options
        doc = DocumentBuilder.field_guide(
            title="My Guide",
            content="<h2>Intro</h2><p>Content</p>",
            printer_friendly=True,
            series="MANUAL",
            number="M-001"
        )
        doc.save("output.pdf")

        # Collection (auto-binder)
        collection = DocumentBuilder.collection("My Project")
        collection.add(doc)
        collection.save("booklet.pdf")
    """

    # Class-level registry instance
    _registry: Optional[TemplateRegistry] = None

    def __init__(self, config: DocumentConfig):
        """Initialize with configuration."""
        self.config = config
        self._generated_path: Optional[Path] = None
        self._analysis: Optional[PDFAnalysis] = None

    @classmethod
    def _get_registry(cls) -> TemplateRegistry:
        """Get or create template registry instance."""
        if cls._registry is None:
            cls._registry = get_registry()
        return cls._registry

    @classmethod
    def list_templates(cls) -> List[TemplateMetadata]:
        """List all available templates."""
        return cls._get_registry().list_templates()

    @classmethod
    def from_pdf(cls, pdf_path: Union[str, Path]) -> "DocumentBuilder":
        """
        Create DocumentBuilder by analyzing an existing PDF.
        
        Args:
            pdf_path: Path to source PDF
            
        Returns:
            DocumentBuilder configured to recreate the PDF
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        # Analyze PDF
        analysis = cls._analyze_pdf(pdf_path)
        
        # Detect appropriate template
        template_name = cls._detect_template(analysis)
        
        # Extract content and structure
        content = cls._extract_content(analysis)
        title = cls._extract_title(analysis)
        
        # Create config
        config = DocumentConfig(
            template=template_name,
            title=title,
            content=content,
            date=analysis.metadata.get("creation_date", datetime.now().strftime("%Y-%m-%d"))
        )
        
        builder = cls(config)
        builder._analysis = analysis
        return builder

    @classmethod
    def _analyze_pdf(cls, pdf_path: Path) -> PDFAnalysis:
        """Analyze a PDF and extract structure, metadata, and content."""
        reader = PdfReader(str(pdf_path))
        
        # Extract metadata
        metadata = {}
        if reader.metadata:
            for key, value in reader.metadata.items():
                # Remove leading slash from keys
                clean_key = key.lstrip("/")
                metadata[clean_key] = str(value) if value else ""
        
        # Extract text content
        full_text = ""
        sections = []
        current_section = None
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            full_text += page_text + "\n"
            
            # Detect section headers (lines that are short and likely headers)
            lines = page_text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Heuristic: section headers are usually short, numbered, or all caps
                if (len(line) < 100 and 
                    (line[0].isdigit() or line.isupper() or 
                     any(keyword in line.lower() for keyword in ["abstract", "introduction", "conclusion", "references"]))):
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        "title": line,
                        "page": page_num,
                        "content": ""
                    }
                elif current_section:
                    current_section["content"] += line + " "
        
        if current_section:
            sections.append(current_section)
        
        # Detect styling hints
        styling_hints = {
            "page_count": len(reader.pages),
            "has_abstract": "abstract" in full_text.lower()[:500],
            "has_references": "references" in full_text.lower(),
            "is_academic": any(keyword in full_text.lower()[:1000] for keyword in 
                             ["technical report", "we report", "we present", "abstract"]),
            "is_laTeX": metadata.get("Creator", "").lower().find("latex") != -1
        }
        
        return PDFAnalysis(
            pdf_path=pdf_path,
            page_count=len(reader.pages),
            metadata=metadata,
            content=full_text,
            styling_hints=styling_hints,
            sections=sections
        )

    @classmethod
    def _detect_template(cls, analysis: PDFAnalysis) -> str:
        """Detect appropriate template based on PDF analysis."""
        hints = analysis.styling_hints
        
        # Check registry for matching templates
        registry = cls._get_registry()
        
        # Academic paper detection
        if hints.get("is_academic") or hints.get("has_abstract"):
            # Check if academic_paper template exists
            academic = registry.get_template("academic_paper")
            if academic:
                return "academic_paper"
        
        # LaTeX-generated papers often use academic format
        if hints.get("is_laTeX") and hints.get("page_count", 0) > 10:
            academic = registry.get_template("academic_paper")
            if academic:
                return "academic_paper"
        
        # Default to field_guide if available
        field_guide = registry.get_template("field_guide")
        if field_guide:
            return "field_guide"
        
        # Fallback to first available template
        templates = registry.list_templates()
        if templates:
            return templates[0].module_name
        
        return "field_guide"  # Ultimate fallback

    @classmethod
    def _extract_title(cls, analysis: PDFAnalysis) -> str:
        """Extract title from PDF analysis."""
        # Try metadata first
        title = analysis.metadata.get("Title", "").strip()
        if title:
            return title
        
        # Extract from first page
        first_page_text = analysis.content.split("\n")[:10]
        for line in first_page_text:
            line = line.strip()
            if line and len(line) < 200 and not line.lower().startswith("abstract"):
                # Likely title if it's a short line near the top
                return line
        
        # Fallback
        return analysis.pdf_path.stem.replace("_", " ").replace("-", " ").title()

    @classmethod
    def _extract_content(cls, analysis: PDFAnalysis) -> str:
        """Extract and format content from PDF analysis."""
        # Convert plain text to HTML
        html_content = "<div>\n"
        
        # For very long documents, process all sections but be smarter about it
        sections_to_process = analysis.sections
        
        # Group sections by major headings (numbered 1, 2, 3, etc.)
        major_sections = {}
        current_major = None
        
        for section in sections_to_process:
            title = section["title"].strip()
            
            # Check if this is a major section (starts with single digit)
            major_match = re.match(r'^(\d+)\s', title)
            if major_match:
                current_major = major_match.group(1)
                if current_major not in major_sections:
                    major_sections[current_major] = []
            
            if current_major:
                major_sections[current_major].append(section)
            else:
                # No major section yet, use first section as major
                if not major_sections:
                    major_sections["1"] = []
                major_sections["1"].append(section)
        
        # Process each major section
        for major_num, sections in sorted(major_sections.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
            for section in sections:
                title = section["title"].strip()
                content = section["content"].strip()
                
                # Determine heading level based on numbering
                if re.match(r'^\d+\.\d+\.\d+', title):
                    html_content += f'<h3>{title}</h3>\n'
                elif re.match(r'^\d+\.\d+', title):
                    html_content += f'<h2>{title}</h2>\n'
                else:
                    html_content += f'<h1>{title}</h1>\n'
                
                # Convert plain text paragraphs to HTML
                if content:
                    # Split content into paragraphs (look for double newlines or long sentences)
                    # First, try splitting by double newlines
                    if '\n\n' in content:
                        paragraphs = content.split('\n\n')
                    else:
                        # Split by sentence endings, but be more lenient
                        paragraphs = re.split(r'\.\s+(?=[A-Z][a-z])', content)
                    
                    for para in paragraphs:
                        para = para.strip()
                        # Clean up whitespace
                        para = re.sub(r'\s+', ' ', para)
                        para = para.replace('\n', ' ')
                        
                        if para and len(para) > 5:  # Include even short paragraphs
                            if not para.endswith(('.', '!', '?', ':')):
                                para += '.'
                            html_content += f"<p>{para}</p>\n"
        
        html_content += "</div>"
        return html_content

    def recreate(self, output_path: Optional[Path] = None) -> Path:
        """
        Recreate the analyzed PDF using the detected template.
        
        Args:
            output_path: Where to save recreated PDF
            
        Returns:
            Path to generated PDF
        """
        if not self._analysis:
            raise ValueError("No PDF analysis available. Use from_pdf() first.")
        
        output_path = output_path or self.config.output_path or Path("recreated.pdf")
        return self.generate(output_path)

    @classmethod
    def field_guide(
        cls,
        title: str,
        content: str,
        output_path: Optional[Path] = None,
        printer_friendly: bool = False,
        max_pages: Optional[int] = None,
        min_pages: Optional[int] = None,
        exact_pages: Optional[int] = None,
        **kwargs
    ) -> "DocumentBuilder":
        """
        Create a field guide document.
        
        Args:
            title: Document title
            content: HTML content
            output_path: Output PDF path
            printer_friendly: Use printer-friendly styling
            max_pages: Maximum allowed pages (triggers feedback loop)
            min_pages: Minimum required pages
            exact_pages: Exact required pages (triggers feedback loop)
            **kwargs: Additional template options
        """
        config = DocumentConfig(
            template=TemplateType.FIELD_GUIDE,
            title=title,
            content=content,
            output_path=output_path,
            printer_friendly=printer_friendly,
            max_pages=max_pages,
            min_pages=min_pages,
            exact_pages=exact_pages,
            **kwargs
        )
        return cls(config)

    @classmethod
    def lab_notes(
        cls,
        title: str,
        content: str,
        output_path: Optional[Path] = None,
        printer_friendly: bool = False,
        **kwargs
    ) -> "DocumentBuilder":
        """Create a lab notes document."""
        config = DocumentConfig(
            template=TemplateType.LAB_NOTES,
            title=title,
            content=content,
            output_path=output_path,
            printer_friendly=printer_friendly,
            **kwargs
        )
        return cls(config)

    @classmethod
    def academic_paper(
        cls,
        title: str,
        content: str,
        abstract: str = "",
        authors: List[Dict[str, str]] = None,
        affiliations: List[str] = None,
        output_path: Optional[Path] = None,
        **kwargs
    ) -> "DocumentBuilder":
        """Create an academic paper document."""
        config = DocumentConfig(
            template=TemplateType.ACADEMIC_PAPER,
            title=title,
            content=content,
            output_path=output_path,
            abstract=abstract,
            authors=authors or [],
            affiliations=affiliations or [],
            **kwargs
        )
        return cls(config)

    @classmethod
    def collection(
        cls,
        title: str,
        subtitle: Optional[str] = None,
        organization: Optional[str] = None,
        date: Optional[str] = None,
        version: Optional[str] = None,
        compiled_by: Optional[str] = None,
        cover_style: str = "professional"
    ) -> "DocumentCollection":
        """Create a document collection (auto-binder)."""
        return DocumentCollection(
            title=title,
            subtitle=subtitle,
            organization=organization,
            date=date,
            version=version,
            compiled_by=compiled_by,
            cover_style=cover_style
        )

    def generate(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate the PDF document.
        
        Args:
            output_path: Where to save PDF (uses config.output_path if not provided)
            
        Returns:
            Path to generated PDF
        """
        output_path = output_path or self.config.output_path
        if not output_path:
            output_path = Path(f"{self.config.title.lower().replace(' ', '_')}.pdf")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get template using registry
        template_str = self._get_template()
        
        # Render template
        template = Template(template_str)
        html_output = self._render_template(template)
        
        # Convert to printer-friendly if requested
        if self.config.printer_friendly:
            html_output = convert_html_template_to_printer_friendly(html_output)
        
        # Generate PDF
        HTML(string=html_output).write_pdf(output_path)
        
        # Post-process to add blank page markers
        try:
            from ..utils import process_pdf_for_blank_pages
            process_pdf_for_blank_pages(output_path)
        except Exception as e:
            print(f"⚠️  Blank page marker processing failed: {e}")
        
        self._generated_path = output_path
        return output_path

    def _render_template(self, template: Template) -> str:
        """Render template with config data."""
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            import re
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"F","location":"document_builder.py:557","message":"_render_template entry","data":{"content_length":len(self.config.content) if self.config.content else 0,"content_preview":self.config.content[:300] if self.config.content else "","content_is_html":bool(re.search(r'<[^>]+>', self.config.content)) if self.config.content else False,"has_h1":bool(re.search(r'<h1[^>]*>', self.config.content)) if self.config.content else False,"has_hr":bool(re.search(r'<hr[^>]*>', self.config.content)) if self.config.content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Process content with improved algorithms
        processed_content = self.config.content
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            import re
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"G","location":"document_builder.py:565","message":"before content processing","data":{"content_length":len(processed_content) if processed_content else 0,"content_is_html":bool(re.search(r'<[^>]+>', processed_content)) if processed_content else False,"has_h1":bool(re.search(r'<h1[^>]*>', processed_content)) if processed_content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        if processed_content:
            # If content is markdown, convert to HTML
            if not re.search(r'<[^>]+>', processed_content):
                processed_content = PDFContentProcessor.markdown_to_html(processed_content)
            else:
                # If already HTML, clean it
                processed_content = PDFContentProcessor.clean_html_content(processed_content)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            import re
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"G","location":"document_builder.py:578","message":"after content processing","data":{"processed_length":len(processed_content) if processed_content else 0,"has_h1_after":bool(re.search(r'<h1[^>]*>', processed_content)) if processed_content else False,"has_hr_after":bool(re.search(r'<hr[^>]*>', processed_content)) if processed_content else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Build template context
        context = {
            "title": self.config.title,
            "content": processed_content,
            "series": self.config.series,
            "number": self.config.number,
            "subtitle": self.config.subtitle,
            "classification": self.config.classification,
            "issued_by": self.config.issued_by,
            "date": self.config.date or datetime.now().strftime("%Y-%m-%d"),
            "author": self.config.author,
        }
        
        # Add any additional kwargs from config
        for key, value in self.config.__dict__.items():
            if key not in context and not key.startswith("_"):
                context[key] = value
        
        html_output = template.render(**context)
        
        # Apply enhanced styling (includes all formatting improvements)
        enhanced_css = PDFStylingEnhancer.get_complete_styles()
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"G","location":"document_builder.py:595","message":"before CSS injection","data":{"has_style_tag":bool('<style>' in html_output),"enhanced_css_length":len(enhanced_css) if enhanced_css else 0,"css_preview":enhanced_css[:200] if enhanced_css else ""},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # Inject CSS into HTML if not already present
        if '<style>' in html_output and enhanced_css not in html_output:
            html_output = html_output.replace('</style>', f'\n{enhanced_css}\n</style>', 1)
        elif '<style>' not in html_output:
            # Add style block if missing
            html_output = html_output.replace('<head>', f'<head>\n<style>\n{enhanced_css}\n</style>', 1)
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            import re
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"G","location":"document_builder.py:603","message":"after CSS injection","data":{"html_output_length":len(html_output) if html_output else 0,"has_enhanced_css":bool(enhanced_css in html_output) if enhanced_css else False,"has_h1_in_final":bool(re.search(r'<h1[^>]*>', html_output)) if html_output else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        # #region agent log
        with open('/Users/ctavolazzi/Code/active/waft/.cursor/debug.log', 'a') as f:
            import json
            import re
            f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"F","location":"document_builder.py:577","message":"_render_template exit","data":{"html_output_length":len(html_output) if html_output else 0,"html_output_preview":html_output[html_output.find('<div class="content">'):html_output.find('<div class="content">')+500] if html_output and '<div class="content">' in html_output else html_output[:500] if html_output else "","has_h1_in_output":bool(re.search(r'<h1[^>]*>', html_output)) if html_output else False,"has_hr_in_output":bool(re.search(r'<hr[^>]*>', html_output)) if html_output else False,"has_raw_hash":bool(re.search(r'#\s+WAFT', html_output)) if html_output else False},"timestamp":int(__import__('time').time()*1000)}) + '\n')
        # #endregion
        
        return html_output

    def save(self, output_path: Optional[Path] = None) -> Path:
        """Alias for generate() - more intuitive name."""
        return self.generate(output_path)

    def _get_template(self) -> str:
        """Get the template string for current template type using registry."""
        registry = self._get_registry()
        
        # Handle both enum and string template names
        template_name = self.config.template
        if isinstance(template_name, TemplateType):
            template_name = template_name.value
        
        # Get template metadata
        template_meta = registry.get_template(template_name)
        if not template_meta:
            # Fallback to field_guide
            template_meta = registry.get_template("field_guide")
            if not template_meta:
                raise ValueError(f"Template '{template_name}' not found and no fallback available")
        
        # Get generate function to access template constant
        generate_func = registry.get_generate_function(template_meta.name)
        if not generate_func:
            raise ValueError(f"Generate function not found for template '{template_name}'")
        
        # Import module and get template constant
        import importlib
        module = importlib.import_module(f"src.waft.templates.{template_meta.module_name}")
        
        if template_meta.template_constant:
            template_str = getattr(module, template_meta.template_constant)
            if isinstance(template_str, str):
                return template_str
        
        # Fallback: try to find template constant by convention
        for attr_name in dir(module):
            if attr_name.endswith("_TEMPLATE") and isinstance(getattr(module, attr_name), str):
                return getattr(module, attr_name)
        
        # Ultimate fallback: use field_guide
        from .templates.field_guide import FIELD_GUIDE_TEMPLATE
        return FIELD_GUIDE_TEMPLATE


class DocumentCollection:
    """
    Collection of documents that automatically creates a binder.

    Usage:
        collection = DocumentBuilder.collection("My Project")
        collection.add(DocumentBuilder.field_guide(...))
        collection.add(DocumentBuilder.lab_notes(...))
        collection.save("booklet.pdf")  # Auto-creates binder
    """

    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        organization: Optional[str] = None,
        date: Optional[str] = None,
        version: Optional[str] = None,
        compiled_by: Optional[str] = None,
        cover_style: str = "professional"
    ):
        """Initialize collection."""
        self.title = title
        self.subtitle = subtitle
        self.documents: List[DocumentBuilder] = []
        self.sections: Dict[str, List[DocumentBuilder]] = {}

        # Binder configuration
        self.binder = Binder(
            title=title,
            subtitle=subtitle,
            organization=organization or "WAFT System",
            date=date or datetime.now().strftime("%B %d, %Y"),
            version=version or "1.0",
            compiled_by=compiled_by or "WAFT System",
            cover_style=cover_style
        )

    def add(
        self,
        document: DocumentBuilder,
        section: Optional[str] = None
    ) -> "DocumentCollection":
        """Add a document to the collection."""
        self.documents.append(document)

        if section:
            if section not in self.sections:
                self.sections[section] = []
            self.sections[section].append(document)
        else:
            # Default section
            if "Documents" not in self.sections:
                self.sections["Documents"] = []
            self.sections["Documents"].append(document)

        return self

    def save(self, output_path: Path, include_dividers: bool = True) -> Path:
        """Generate all documents and create binder."""
        # Generate all documents first
        generated_paths = []

        for section_name, docs in self.sections.items():
            binder_section = self.binder.add_section(
                section_name,
                description=f"{len(docs)} document(s)"
            )

            for doc in docs:
                # Generate if not already generated
                if doc._generated_path is None:
                    # Create temp path
                    temp_path = Path("/tmp") / f"waft_doc_{id(doc)}.pdf"
                    doc.generate(temp_path)

                # Add to binder
                binder_section.add_document(DocumentEntry(
                    path=doc._generated_path,
                    title=doc.config.title,
                    author=doc.config.author,
                    date=doc.config.date or datetime.now().strftime("%B %d, %Y"),
                    description=doc.config.description
                ))
                generated_paths.append(doc._generated_path)

        # Generate binder
        self.binder.generate(output_path, include_dividers=include_dividers)

        return output_path


# Convenience functions for common patterns
def quick_field_guide(
    title: str,
    content: str,
    output: str,
    printer_friendly: bool = False
) -> Path:
    """Quick field guide generation."""
    return DocumentBuilder.field_guide(
        title=title,
        content=content,
        output_path=Path(output),
        printer_friendly=printer_friendly
    ).save()
