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

Example:
--------
    from waft import DocumentBuilder

    # Simple document
    DocumentBuilder.field_guide(
        title="My Guide",
        content="<h2>Introduction</h2><p>Content here</p>"
    ).save("output.pdf")

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
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import tempfile
import re

from jinja2 import Template
from weasyprint import HTML
from pypdf import PdfReader

from .templates.field_guide import FIELD_GUIDE_TEMPLATE
from .binder import Binder, DocumentEntry, BinderSection
from scripts.printer_friendly_helper import convert_html_template_to_printer_friendly


class TemplateType(Enum):
    """Available document templates."""
    FIELD_GUIDE = "field_guide"
    LAB_NOTES = "lab_notes"
    TM_REPORT = "tm_report"
    PERSONAL_MEMO = "personal_memo"
    SIMPLE_SCIENTIFIC = "simple_scientific"
    ELDRITCH_JOURNAL = "eldritch_journal"
    SCREENPLAY = "screenplay"
    HEARTFELT_LETTER = "heartfelt_letter"
    INVOICE = "invoice"
    CODE_DOCS = "code_docs"
    STORYBOOK = "storybook"
    NEWSPAPER = "newspaper"


@dataclass
class DocumentConfig:
    """Configuration for a single document."""
    template: TemplateType
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
    Unified document builder with fluent API.

    Usage:
        # Simple
        doc = DocumentBuilder.field_guide(
            title="My Guide",
            content="<h2>Intro</h2><p>Content</p>"
        )
        doc.save("output.pdf")

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

    def __init__(self, config: DocumentConfig):
        """Initialize with configuration."""
        self.config = config
        self._generated_path: Optional[Path] = None

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
        # TODO: Import lab_notes template when available
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
    def collection(
        cls,
        title: str,
        subtitle: Optional[str] = None,
        **binder_kwargs
    ) -> "DocumentCollection":
        """Create a document collection (auto-binder)."""
        return DocumentCollection(title, subtitle, **binder_kwargs)

    def generate(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate the PDF document with constraint-aware feedback loop.
        
        If page count constraints are specified, this will:
        1. Generate initial PDF
        2. Check page count
        3. Adjust CSS (font size, margins, spacing) if needed
        4. Regenerate and re-check
        5. Iterate until constraints are met or max iterations reached
        """
        output_path = output_path or self.config.output_path
        if not output_path:
            raise ValueError("output_path required (pass to method or save())")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if we have constraints
        has_constraints = (
            self.config.max_pages is not None or
            self.config.min_pages is not None or
            self.config.exact_pages is not None
        )

        if not has_constraints:
            # No constraints - simple generation
            return self._generate_simple(output_path)

        # Constraint-aware generation with feedback loop
        return self._generate_with_constraints(output_path)

    def _generate_simple(self, output_path: Path) -> Path:
        """Simple PDF generation without constraints."""
        # Get template
        template_str = self._get_template()

        # Convert to printer-friendly if needed
        if self.config.printer_friendly:
            template_str = convert_html_template_to_printer_friendly(template_str)

        # Render
        template = Template(template_str)
        html_output = template.render(
            title=self.config.title,
            content=self.config.content,
            series=self.config.series,
            number=self.config.number,
            subtitle=self.config.subtitle,
            classification=self.config.classification,
            issued_by=self.config.issued_by,
            date=self.config.date or datetime.now().strftime("%B %d, %Y")
        )

        # Generate PDF
        HTML(string=html_output).write_pdf(output_path)
        self._generated_path = output_path
        return output_path

    def _generate_with_constraints(self, output_path: Path) -> Path:
        """Generate PDF with constraint feedback loop."""
        # Initial CSS adjustment factors
        font_scale = 1.0
        margin_scale = 1.0
        spacing_scale = 1.0

        for iteration in range(self.config.max_iterations):
            # Get template
            template_str = self._get_template()

            # Convert to printer-friendly if needed
            if self.config.printer_friendly:
                template_str = convert_html_template_to_printer_friendly(template_str)

            # Apply CSS adjustments for constraint compliance
            template_str = self._adjust_css_for_constraints(
                template_str,
                font_scale,
                margin_scale,
                spacing_scale
            )

            # Render
            template = Template(template_str)
            html_output = template.render(
                title=self.config.title,
                content=self.config.content,
                series=self.config.series,
                number=self.config.number,
                subtitle=self.config.subtitle,
                classification=self.config.classification,
                issued_by=self.config.issued_by,
                date=self.config.date or datetime.now().strftime("%B %d, %Y")
            )

            # Generate to temp file first
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_path = Path(tmp.name)

            HTML(string=html_output).write_pdf(temp_path)

            # Check page count
            page_count = self._get_page_count(temp_path)
            constraint_met = self._check_constraints(page_count)

            if constraint_met:
                # Constraints met - move to final location
                import shutil
                shutil.move(str(temp_path), str(output_path))
                self._generated_path = output_path
                return output_path

            # Constraints not met - adjust and retry
            adjustment = self._calculate_adjustment(page_count)
            font_scale *= adjustment['font']
            margin_scale *= adjustment['margin']
            spacing_scale *= adjustment['spacing']

            # Clean up temp file for next iteration
            if temp_path.exists():
                temp_path.unlink()

        # Max iterations reached - use last attempt if it exists
        import shutil
        if temp_path.exists():
            shutil.move(str(temp_path), str(output_path))
        else:
            # Fallback: generate one more time without constraints
            return self._generate_simple(output_path)
        self._generated_path = output_path
        return output_path

    def _adjust_css_for_constraints(
        self,
        template_str: str,
        font_scale: float,
        margin_scale: float,
        spacing_scale: float
    ) -> str:
        """Adjust CSS to meet page count constraints."""
        # Adjust font sizes
        def adjust_font_size(match):
            size_str = match.group(1)
            try:
                if 'pt' in size_str:
                    size = float(size_str.replace('pt', '').strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}pt;"
                elif 'px' in size_str:
                    size = float(size_str.replace('px', '').strip())
                    new_size = size * font_scale
                    return f"font-size: {new_size:.1f}px;"
            except:
                pass
            return match.group(0)

        template_str = re.sub(
            r'font-size:\s*([0-9.]+(?:pt|px));',
            adjust_font_size,
            template_str
        )

        # Adjust margins - handle multiple margin values (e.g., "0.75in 0.5in")
        def adjust_margin_values(match):
            margin_declaration = match.group(0)
            # Extract all margin values
            margin_values = re.findall(r'([0-9.]+)in', margin_declaration)
            if margin_values:
                adjusted_values = [f"{float(v) * margin_scale:.3f}in" for v in margin_values]
                # Replace original values with adjusted ones
                result = margin_declaration
                for i, (orig, adj) in enumerate(zip(margin_values, adjusted_values)):
                    result = result.replace(f"{orig}in", adj, 1)
                return result
            return margin_declaration

        template_str = re.sub(
            r'margin:\s*([0-9.\s]+in[^;]*);',
            adjust_margin_values,
            template_str
        )

        # Adjust line-height (spacing)
        def adjust_line_height(match):
            lh_str = match.group(1)
            try:
                lh = float(lh_str)
                new_lh = lh * spacing_scale
                return f"line-height: {new_lh:.2f};"
            except:
                pass
            return match.group(0)

        template_str = re.sub(
            r'line-height:\s*([0-9.]+);',
            adjust_line_height,
            template_str
        )

        return template_str

    def _get_page_count(self, pdf_path: Path) -> int:
        """Get page count from PDF."""
        try:
            reader = PdfReader(str(pdf_path))
            return len(reader.pages)
        except Exception:
            return 0

    def _check_constraints(self, page_count: int) -> bool:
        """Check if page count meets all constraints."""
        if self.config.exact_pages is not None:
            return page_count == self.config.exact_pages

        if self.config.max_pages is not None and page_count > self.config.max_pages:
            return False

        if self.config.min_pages is not None and page_count < self.config.min_pages:
            return False

        return True

    def _calculate_adjustment(self, page_count: int) -> Dict[str, float]:
        """Calculate CSS adjustment factors based on page count vs constraints."""
        target_pages = (
            self.config.exact_pages or
            self.config.max_pages or
            self.config.min_pages or
            1
        )

        ratio = page_count / target_pages if target_pages > 0 else 1.0

        # If too many pages, reduce font/margins/spacing
        if ratio > 1.0:
            factor = 0.95  # Reduce by 5% per iteration
            return {
                'font': factor,
                'margin': factor,
                'spacing': factor
            }
        elif ratio < 0.8:
            # Too few pages - increase font/margins/spacing more aggressively
            factor = 1.10  # Increase by 10% per iteration
            return {
                'font': factor,
                'margin': factor,
                'spacing': factor
            }
        elif ratio < 1.0:
            # Close but need a bit more
            factor = 1.05
            return {
                'font': factor,
                'margin': factor,
                'spacing': factor
            }
        else:
            return {
                'font': 1.0,
                'margin': 1.0,
                'spacing': 1.0
            }

    def save(self, output_path: Optional[Path] = None) -> Path:
        """Alias for generate() - more intuitive name."""
        return self.generate(output_path)

    def _get_template(self) -> str:
        """Get the template string for current template type."""
        if self.config.template == TemplateType.FIELD_GUIDE:
            return FIELD_GUIDE_TEMPLATE
        # TODO: Add other templates
        else:
            raise NotImplementedError(
                f"Template {self.config.template.value} not yet implemented. "
                f"Available: field_guide"
            )


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
    """
    Quick field guide generation - simplest possible API.

    Example:
        quick_field_guide(
            title="My Guide",
            content="<h2>Intro</h2><p>Content</p>",
            output="guide.pdf"
        )
    """
    return DocumentBuilder.field_guide(
        title=title,
        content=content,
        printer_friendly=printer_friendly
    ).save(Path(output))


def quick_collection(
    title: str,
    documents: List[Dict[str, Any]],
    output: str,
    printer_friendly: bool = False
) -> Path:
    """
    Quick collection generation - simplest possible API.

    Example:
        quick_collection(
            title="My Booklet",
            documents=[
                {"type": "field_guide", "title": "Guide 1", "content": "..."},
                {"type": "lab_notes", "title": "Notes 1", "content": "..."}
            ],
            output="booklet.pdf"
        )
    """
    collection = DocumentBuilder.collection(title)

    for doc_config in documents:
        doc_type = doc_config.pop("type", "field_guide")
        section = doc_config.pop("section", None)

        if doc_type == "field_guide":
            doc = DocumentBuilder.field_guide(
                printer_friendly=printer_friendly,
                **doc_config
            )
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

        collection.add(doc, section=section)

    return collection.save(Path(output))
