#!/usr/bin/env python3
"""
Simple Field Guide Example - Using New DocumentBuilder API
===========================================================

This demonstrates how much simpler document generation is with the new API.

BEFORE (old way):
-----------------
    from src.waft.templates.field_guide import generate_field_guide
    from src.waft.binder import Binder, DocumentEntry
    from pathlib import Path
    from datetime import datetime
    
    # Generate individual PDFs
    level1 = generate_field_guide(
        title="WAFT FIELD GUIDE",
        content=content1,
        output_path=Path("level1.pdf"),
        series="FIELD GUIDE",
        number="FG-001",
        subtitle="Level 1",
        classification="PUBLIC",
        issued_by="WAFT Team",
        date=datetime.now().strftime("%B %d, %Y")
    )
    
    level2 = generate_field_guide(...)
    level3 = generate_field_guide(...)
    
    # Create binder manually
    binder = Binder(...)
    section = binder.add_section(...)
    section.add_document(DocumentEntry(...))
    binder.generate(...)

AFTER (new way):
----------------
    from waft import DocumentBuilder
    
    # Simple single document
    DocumentBuilder.field_guide(
        title="WAFT Field Guide",
        content="<h2>Intro</h2><p>Content</p>"
    ).save("guide.pdf")
    
    # With printer-friendly
    DocumentBuilder.field_guide(
        title="WAFT Field Guide",
        content="<h2>Intro</h2><p>Content</p>",
        printer_friendly=True
    ).save("guide_pf.pdf")
    
    # Collection (auto-binder)
    collection = DocumentBuilder.collection("WAFT Guides")
    collection.add(DocumentBuilder.field_guide(title="Level 1", content="..."))
    collection.add(DocumentBuilder.field_guide(title="Level 2", content="..."))
    collection.save("complete_booklet.pdf")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.document_builder import DocumentBuilder, quick_field_guide, quick_collection


def example_simple_document():
    """Example: Single document, simplest possible."""
    print("Example 1: Simple Document")
    print("-" * 60)
    
    quick_field_guide(
        title="Quick Guide",
        content="<h2>Introduction</h2><p>This is a simple guide.</p>",
        output="_work_efforts/showcase_documents/example_simple.pdf"
    )
    
    print("✅ Generated: example_simple.pdf")
    print()


def example_with_options():
    """Example: Document with custom options."""
    print("Example 2: Document with Options")
    print("-" * 60)
    
    DocumentBuilder.field_guide(
        title="Custom Guide",
        content="<h2>Custom</h2><p>With custom options.</p>",
        series="MANUAL",
        number="M-001",
        subtitle="Custom Subtitle",
        classification="PUBLIC",
        printer_friendly=False
    ).save("_work_efforts/showcase_documents/example_custom.pdf")
    
    print("✅ Generated: example_custom.pdf")
    print()


def example_printer_friendly():
    """Example: Printer-friendly version."""
    print("Example 3: Printer-Friendly")
    print("-" * 60)
    
    DocumentBuilder.field_guide(
        title="Printer-Friendly Guide",
        content="<h2>Intro</h2><p>Black and white version.</p>",
        printer_friendly=True
    ).save("_work_efforts/showcase_documents/example_printer_friendly.pdf")
    
    print("✅ Generated: example_printer_friendly.pdf")
    print()


def example_collection():
    """Example: Collection with auto-binder."""
    print("Example 4: Collection (Auto-Binder)")
    print("-" * 60)
    
    collection = DocumentBuilder.collection(
        title="Example Collection",
        subtitle="Multiple Documents"
    )
    
    # Add documents
    collection.add(
        DocumentBuilder.field_guide(
            title="Document 1",
            content="<h2>First Document</h2><p>Content here.</p>"
        ),
        section="Section 1"
    )
    
    collection.add(
        DocumentBuilder.field_guide(
            title="Document 2",
            content="<h2>Second Document</h2><p>More content.</p>",
            printer_friendly=True
        ),
        section="Section 2"
    )
    
    collection.save("_work_efforts/showcase_documents/example_collection.pdf")
    
    print("✅ Generated: example_collection.pdf (with auto-binder)")
    print()


def example_quick_collection():
    """Example: Quick collection API."""
    print("Example 5: Quick Collection API")
    print("-" * 60)
    
    quick_collection(
        title="Quick Collection",
        documents=[
            {
                "type": "field_guide",
                "title": "Guide 1",
                "content": "<h2>Guide 1</h2><p>Content</p>",
                "section": "Guides"
            },
            {
                "type": "field_guide",
                "title": "Guide 2",
                "content": "<h2>Guide 2</h2><p>Content</p>",
                "section": "Guides",
                "printer_friendly": True
            }
        ],
        output="_work_efforts/showcase_documents/example_quick_collection.pdf"
    )
    
    print("✅ Generated: example_quick_collection.pdf")
    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("WAFT DocumentBuilder - Simple Examples")
    print("=" * 60)
    print()
    
    # Ensure output directory exists
    Path("_work_efforts/showcase_documents").mkdir(parents=True, exist_ok=True)
    
    try:
        example_simple_document()
        example_with_options()
        example_printer_friendly()
        example_collection()
        example_quick_collection()
        
        print("=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        print()
        print("Generated files:")
        print("  - example_simple.pdf")
        print("  - example_custom.pdf")
        print("  - example_printer_friendly.pdf")
        print("  - example_collection.pdf")
        print("  - example_quick_collection.pdf")
        print()
        print("All files saved to: _work_efforts/showcase_documents/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
