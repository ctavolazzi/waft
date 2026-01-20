#!/usr/bin/env python3
"""
WAFT Demo Walkthrough Generator
=================================

Creates a comprehensive walkthrough booklet demonstrating WAFT's PDF tools:
- Field Guide Template (with printer-friendly version)
- Binder System (combining multiple PDFs)
- Template Showcase
- Advanced Demo Features

This walkthrough uses WAFT's own tools to document itself.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from src.waft.binder import Binder, DocumentEntry
from src.waft.templates.field_guide import generate_field_guide


def create_walkthrough_intro(output_dir: Path) -> Path:
    """Create introduction walkthrough document."""

    content = """
<h2>Welcome to the WAFT PDF Tools Walkthrough</h2>

<p>
This walkthrough demonstrates WAFT's powerful PDF generation and organization tools.
You'll see how WAFT uses its own templates to document itself, creating a recursive
self-improvement loop.
</p>

<div class="note">
    <div class="note-title">What You'll Learn</div>
    <ul>
        <li>How to use the Field Guide template</li>
        <li>How to create printer-friendly versions</li>
        <li>How to combine PDFs using the Binder system</li>
        <li>How to showcase multiple templates</li>
        <li>How WAFT documents itself recursively</li>
    </ul>
</div>

<h2>Tool 1: Field Guide Template</h2>

<p>
The Field Guide template creates operational manuals with a military field manual aesthetic.
It features:
</p>

<div class="checklist">
    <div class="checklist-title">Field Guide Features</div>
    <ul>
        <li>Two-column layout support</li>
        <li>Warning and caution boxes</li>
        <li>Equipment checklists</li>
        <li>Step-by-step procedures</li>
        <li>Professional tables</li>
        <li>Rugged, practical design</li>
    </ul>
</div>

<h3>Usage Example</h3>

<pre><code>from src.waft.templates.field_guide import generate_field_guide
from pathlib import Path

generate_field_guide(
    title="My Field Guide",
    content="&lt;h2&gt;Content&lt;/h2&gt;&lt;p&gt;Your HTML here&lt;/p&gt;",
    output_path=Path("output.pdf"),
    series="FIELD GUIDE",
    number="FG-001"
)
</code></pre>

<h2>Tool 2: Printer-Friendly Conversion</h2>

<p>
WAFT includes a helper script to convert any template to printer-friendly (black and white)
versions. This is essential for:
</p>

<ul>
    <li>Cost-effective printing</li>
    <li>Professional documentation</li>
    <li>Accessibility (works with all printers)</li>
    <li>Reduced file sizes</li>
</ul>

<div class="caution">
    <div class="caution-title">Important</div>
    The printer-friendly version removes all colors and replaces them with black borders,
    white backgrounds, and text labels. All content is preserved, just optimized for
    black-and-white printing.
</div>

<h2>Tool 3: Binder System</h2>

<p>
The Binder system combines multiple PDF documents into a single, organized booklet with:
</p>

<div class="procedure">
    <div class="step">
        Cover page with title and metadata
    </div>
    <div class="step">
        Table of contents listing all sections
    </div>
    <div class="step">
        Section dividers between document groups
    </div>
    <div class="step">
        All documents merged in order
    </div>
</div>

<h3>Usage Example</h3>

<pre><code>from src.waft.binder import Binder, DocumentEntry
from pathlib import Path

binder = Binder(
    title="My Binder",
    subtitle="Document Collection"
)

section = binder.add_section("Section 1")
section.add_document(DocumentEntry(
    path=Path("doc1.pdf"),
    title="Document 1"
))

binder.generate(Path("binder.pdf"))
</code></pre>

<h2>Tool 4: Template Showcase</h2>

<p>
WAFT includes 12 professional document templates:
</p>

<table>
    <caption>Table 1: WAFT Document Templates</caption>
    <tr>
        <th>Template</th>
        <th>Use Case</th>
        <th>Status</th>
    </tr>
    <tr>
        <td><strong>Field Guide</strong></td>
        <td>Operational manuals</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Lab Notes</strong></td>
        <td>Research logs</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>TM Report</strong></td>
        <td>Technical memos</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Personal Memo</strong></td>
        <td>Staff communications</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Simple Scientific</strong></td>
        <td>Academic papers</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Eldritch Journal</strong></td>
        <td>Horror/madness themes</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Screenplay</strong></td>
        <td>Film/TV scripts</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Heartfelt Letter</strong></td>
        <td>Personal letters</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Invoice/Contract</strong></td>
        <td>Business documents</td>
        <td>✅ Production</td>
    </tr>
    <tr>
        <td><strong>Code Documentation</strong></td>
        <td>Technical docs</td>
        <td>✅ Template</td>
    </tr>
    <tr>
        <td><strong>Children's Storybook</strong></td>
        <td>Kids' books</td>
        <td>✅ Template</td>
    </tr>
    <tr>
        <td><strong>Newspaper</strong></td>
        <td>News front pages</td>
        <td>✅ Template</td>
    </tr>
</table>

<h2>The Recursive Loop</h2>

<div class="highlight-box">
    <h3>WAFT Documenting WAFT</h3>
    <p>
        This walkthrough itself demonstrates WAFT's recursive capabilities:
    </p>
    <ol>
        <li><strong>WAFT generates this walkthrough</strong> using its Field Guide template</li>
        <li><strong>WAFT creates a printer-friendly version</strong> using the helper script</li>
        <li><strong>WAFT combines everything</strong> using the Binder system</li>
        <li><strong>WAFT documents the process</strong> in this very document</li>
    </ol>
    <p>
        This creates a feedback loop where WAFT improves by understanding itself better.
    </p>
</div>

<h2>Next Steps</h2>

<div class="procedure">
    <div class="step">
        Review the generated walkthrough booklet
    </div>
    <div class="step">
        Check out the printer-friendly version
    </div>
    <div class="step">
        Explore the individual template examples
    </div>
    <div class="step">
        Try creating your own documents using WAFT templates
    </div>
</div>

<div class="note">
    <div class="note-title">Remember</div>
    WAFT's tools are designed to work together. Use templates to generate documents,
    use the binder to organize them, and use the printer-friendly helper to optimize
    for printing. All while WAFT tracks its work in the _pyrite system.
</div>
    """

    output_path = output_dir / "WAFT_Demo_Walkthrough_Intro.pdf"

    generate_field_guide(
        title="WAFT DEMO WALKTHROUGH",
        content=content,
        output_path=output_path,
        series="WALKTHROUGH",
        number="WT-001",
        subtitle="Introduction to WAFT PDF Tools",
        classification="DEMONSTRATION",
        issued_by="WAFT Documentation Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def create_printer_friendly_walkthrough(output_dir: Path) -> Path:
    """Create printer-friendly version of walkthrough."""

    # Import printer-friendly template
    from examples.generate_waft_field_guide_printer_friendly import (
        generate_field_guide_printer_friendly,  # We'll use similar content structure
    )

    content = """
<h2>Welcome to the WAFT PDF Tools Walkthrough</h2>

<p>
This walkthrough demonstrates WAFT's powerful PDF generation and organization tools.
You'll see how WAFT uses its own templates to document itself, creating a recursive
self-improvement loop.
</p>

<div class="note">
    <div class="note-title">What You'll Learn</div>
    <ul>
        <li>How to use the Field Guide template</li>
        <li>How to create printer-friendly versions</li>
        <li>How to combine PDFs using the Binder system</li>
        <li>How to showcase multiple templates</li>
        <li>How WAFT documents itself recursively</li>
    </ul>
</div>

<h2>Tool 1: Field Guide Template</h2>

<p>
The Field Guide template creates operational manuals with a military field manual aesthetic.
It features two-column layout, warning boxes, checklists, procedures, and professional tables.
</p>

<h2>Tool 2: Printer-Friendly Conversion</h2>

<p>
WAFT includes a helper script to convert any template to printer-friendly (black and white)
versions. This is essential for cost-effective printing, professional documentation,
accessibility, and reduced file sizes.
</p>

<div class="caution">
    <div class="caution-title">Important</div>
    The printer-friendly version removes all colors and replaces them with black borders,
    white backgrounds, and text labels. All content is preserved, just optimized for
    black-and-white printing.
</div>

<h2>Tool 3: Binder System</h2>

<p>
The Binder system combines multiple PDF documents into a single, organized booklet with
cover page, table of contents, section dividers, and all documents merged in order.
</p>

<h2>Tool 4: Template Showcase</h2>

<p>
WAFT includes 12 professional document templates for various use cases including
field guides, lab notes, technical memos, personal memos, academic papers, and more.
</p>

<h2>The Recursive Loop</h2>

<div class="note">
    <div class="note-title">WAFT Documenting WAFT</div>
    This walkthrough itself demonstrates WAFT's recursive capabilities:
    <ol>
        <li>WAFT generates this walkthrough using its Field Guide template</li>
        <li>WAFT creates a printer-friendly version using the helper script</li>
        <li>WAFT combines everything using the Binder system</li>
        <li>WAFT documents the process in this very document</li>
    </ol>
    This creates a feedback loop where WAFT improves by understanding itself better.
</div>

<h2>Next Steps</h2>

<div class="procedure">
    <div class="step">
        Review the generated walkthrough booklet
    </div>
    <div class="step">
        Check out the printer-friendly version
    </div>
    <div class="step">
        Explore the individual template examples
    </div>
    <div class="step">
        Try creating your own documents using WAFT templates
    </div>
</div>
    """

    output_path = output_dir / "WAFT_Demo_Walkthrough_Intro_PrinterFriendly.pdf"

    generate_field_guide_printer_friendly(
        title="WAFT DEMO WALKTHROUGH",
        content=content,
        output_path=output_path,
        series="WALKTHROUGH",
        number="WT-001",
        subtitle="Introduction to WAFT PDF Tools (Printer Friendly)",
        classification="DEMONSTRATION",
        issued_by="WAFT Documentation Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def generate_complete_walkthrough_booklet(output_dir: Path) -> Path:
    """Generate complete walkthrough booklet with all demos."""

    print("=" * 80)
    print("WAFT Demo Walkthrough Generator")
    print("=" * 80)
    print()

    # Generate intro documents
    print("Generating walkthrough introduction...")
    intro_path = create_walkthrough_intro(output_dir)

    print("Generating printer-friendly walkthrough...")
    intro_pf_path = create_printer_friendly_walkthrough(output_dir)

    # Check if demo files exist
    demo_files = []
    demo_dir = Path("demo_output")
    if demo_dir.exists():
        demo_booklet = demo_dir / "WAFT_Demo_Booklet.pdf"
        if demo_booklet.exists():
            demo_files.append(demo_booklet)

    advanced_demo_dir = Path("advanced_demo_output")
    if advanced_demo_dir.exists():
        advanced_booklet = advanced_demo_dir / "WAFT_Advanced_Demo_Booklet.pdf"
        if advanced_booklet.exists():
            demo_files.append(advanced_booklet)

    # Create binder
    print("\nAssembling complete walkthrough booklet...")
    binder = Binder(
        title="WAFT Demo Walkthrough",
        subtitle="Complete Guide to WAFT PDF Tools",
        organization="WAFT Documentation Team",
        date=datetime.now().strftime("%B %d, %Y"),
        version="1.0",
        compiled_by="WAFT System",
        cover_style="professional",
    )

    # Add sections
    intro_section = binder.add_section(
        "Introduction", description="Overview of WAFT PDF tools", color="#000000"
    )
    intro_section.add_document(
        DocumentEntry(
            path=intro_path,
            title="WAFT Demo Walkthrough - Introduction",
            author="WAFT Documentation Team",
            date=datetime.now().strftime("%B %d, %Y"),
            description="Introduction to WAFT's PDF generation and organization tools",
        )
    )

    if intro_pf_path.exists():
        intro_section.add_document(
            DocumentEntry(
                path=intro_pf_path,
                title="WAFT Demo Walkthrough - Introduction (Printer Friendly)",
                author="WAFT Documentation Team",
                date=datetime.now().strftime("%B %d, %Y"),
                description="Printer-friendly version of the introduction",
            )
        )

    # Add demo files if they exist
    if demo_files:
        demo_section = binder.add_section(
            "Demo Examples",
            description="Example demonstrations of WAFT capabilities",
            color="#333333",
        )

        for demo_file in demo_files:
            demo_section.add_document(
                DocumentEntry(
                    path=demo_file,
                    title=demo_file.stem.replace("_", " ").title(),
                    author="WAFT System",
                    date=datetime.now().strftime("%B %d, %Y"),
                    description=f"Demo example: {demo_file.name}",
                )
            )

    # Generate binder
    output_path = output_dir / "WAFT_Complete_Demo_Walkthrough.pdf"
    binder.generate(output_path, include_dividers=True)

    print(f"\n✓ Complete walkthrough booklet generated: {output_path}")
    print(f"  Size: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"  Sections: {len(binder.sections)}")
    print(f"  Documents: {sum(len(s.documents) for s in binder.sections)}")

    return output_path


if __name__ == "__main__":
    output_dir = Path("_work_efforts/showcase_documents")
    output_dir.mkdir(parents=True, exist_ok=True)

    generate_complete_walkthrough_booklet(output_dir)

    print()
    print("=" * 80)
    print("Walkthrough generation complete!")
    print("=" * 80)
