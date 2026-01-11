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

from jinja2 import Template
from weasyprint import HTML

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
        **kwargs
    ) -> "DocumentBuilder":
        """Create a field guide document."""
        config = DocumentConfig(
            template=TemplateType.FIELD_GUIDE,
            title=title,
            content=content,
            output_path=output_path,
            printer_friendly=printer_friendly,
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
        """Generate the PDF document."""
        output_path = output_path or self.config.output_path
        if not output_path:
            raise ValueError("output_path required (pass to method or save())")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
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
