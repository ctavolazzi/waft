#!/usr/bin/env python3
"""
Generate Comprehensive WAFT Feature Showcase PDF
================================================

Creates a single PDF booklet that demonstrates EVERY feature developed in WAFT:
- All template types (Field Guide, Lab Notes, Personal Memo, TM Report)
- Foundation V1 blocks (all types)
- Foundation V2 blocks (enhanced, Clinical Standard)
- DocumentBuilder features
- Evolution System (two-page generator, metrics, PNG conversion)
- Binder System (cover, TOC, dividers, assembly)
- Advanced features (markdown cleaning, content stats, evolutionary tracking)
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Template System
# Binder System
from src.waft.binder import Binder, DocumentEntry

# DocumentBuilder
from src.waft.document_builder import DocumentBuilder

# Evolution System
from src.waft.evolution import (
    ChatDistiller,
    ColorGene,
    FontGene,
    LayoutGene,
    MarginGene,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
    TwoPageGenerator,
)
from src.waft.foundation import (
    DocumentConfig as DocumentConfigV1,
)

# Foundation V1
from src.waft.foundation import (
    DocumentEngine as DocumentEngineV1,
)
from src.waft.foundation import (
    KeyValueBlock,
    LogBlock,
    SectionHeader,
    SignatureBlock,
    TextBlock,
    WarningBlock,
)
from src.waft.foundation_v2 import (
    DocumentConfig as DocumentConfigV2,
)

# Foundation V2
from src.waft.foundation_v2 import (
    DocumentEngine as DocumentEngineV2,
)
from src.waft.foundation_v2 import (
    MetadataRail,
    RuleBlock,
    TableBlock,
)
from src.waft.foundation_v2 import (
    SectionHeader as SectionHeaderV2,
)
from src.waft.foundation_v2 import (
    TextBlock as TextBlockV2,
)
from src.waft.templates.field_guide import generate_field_guide
from src.waft.templates.lab_notes import generate_lab_notes
from src.waft.templates.personal_memo import generate_personal_memo
from src.waft.templates.tm_report import generate_tm_report


def generate_template_documents(temp_dir: Path) -> list[Path]:
    """Generate all template system documents."""
    print("\n📄 Generating Template System Documents...")
    documents = []

    # Field Guide
    print("  - Field Guide...")
    field_guide_content = """
<h2>WAFT Template System: Field Guide</h2>

<p>This document demonstrates the Field Guide template, designed for operational manuals and survival guides.</p>

<div class="warning">
    <div class="warning-title">Warning</div>
    Field guides are critical documents. Follow all procedures exactly as written.
</div>

<div class="checklist">
    <div class="checklist-title">Template Features</div>
    <ul>
        <li>Two-column layout support</li>
        <li>Warning and caution boxes</li>
        <li>Equipment checklists</li>
        <li>Step-by-step procedures</li>
        <li>Rugged, practical aesthetic</li>
    </ul>
</div>

<h2>Usage Example</h2>

<div class="procedure">
    <div class="step">
        Use <code>DocumentBuilder.field_guide()</code> or <code>generate_field_guide()</code>
    </div>
    <div class="step">
        Provide HTML content with template-specific classes
    </div>
    <div class="step">
        Customize series, number, classification, and metadata
    </div>
</div>

<h2>Key Features</h2>

<p>The Field Guide template provides:</p>
<ul>
    <li>Professional header/footer with series numbers</li>
    <li>Classification markings</li>
    <li>Warning and caution callout boxes</li>
    <li>Checklist formatting</li>
    <li>Procedure step formatting</li>
    <li>Two-column layout capability</li>
</p>
"""

    field_guide_path = temp_dir / "template_field_guide.pdf"
    generate_field_guide(
        title="WAFT Field Guide Template",
        content=field_guide_content,
        output_path=field_guide_path,
        series="SHOWCASE",
        number="FG-001",
        subtitle="Template System Demonstration",
        classification="FEATURE SHOWCASE",
    )
    documents.append(field_guide_path)
    print(f"    ✓ Generated: {field_guide_path.name}")

    # Lab Notes
    print("  - Lab Notes...")
    lab_notes_content = """
<h2>WAFT Template System: Lab Notes</h2>

<p>This document demonstrates the Lab Notes template, designed for research documentation and scientific notebooks.</p>

<h2>Experiment: Template Feature Analysis</h2>

<h3>Objective</h3>
<p>Document all features of the Lab Notes template system.</p>

<h3>Procedure</h3>
<ol>
    <li>Generate document using <code>generate_lab_notes()</code></li>
    <li>Include structured content with headers and lists</li>
    <li>Add metadata and classification</li>
</ol>

<h3>Results</h3>
<p>The Lab Notes template provides:</p>
<ul>
    <li>Scientific notebook aesthetic</li>
    <li>Structured sections for experiments</li>
    <li>Date and metadata tracking</li>
    <li>Professional formatting</li>
</ul>

<h3>Conclusion</h3>
<p>The Lab Notes template is ideal for research documentation, experimental records, and scientific notebooks.</p>
"""

    lab_notes_path = temp_dir / "template_lab_notes.pdf"
    generate_lab_notes(
        title="WAFT Lab Notes Template",
        content=lab_notes_content,
        output_path=lab_notes_path,
        lab_id="SHOWCASE-LN-001",
        researcher="Feature Showcase Generator",
        facility="WAFT Development Lab",
        project="Template System Demonstration",
        date=datetime.now().strftime("%Y-%m-%d"),
        classification="FEATURE SHOWCASE",
    )
    documents.append(lab_notes_path)
    print(f"    ✓ Generated: {lab_notes_path.name}")

    # Personal Memo
    print("  - Personal Memo...")
    personal_memo_content = """
<h2>WAFT Template System: Personal Memo</h2>

<p>This document demonstrates the Personal Memo template, designed for staff communications and internal memos.</p>

<p>The Personal Memo template provides:</p>
<ul>
    <li>Clean, professional memo format</li>
    <li>Header fields for To/From/Subject</li>
    <li>Date and classification support</li>
    <li>Simple, readable layout</li>
</ul>

<h2>Usage</h2>
<p>Use <code>generate_personal_memo()</code> for internal communications, announcements, and staff memos.</p>
"""

    personal_memo_path = temp_dir / "template_personal_memo.pdf"
    generate_personal_memo(
        content=personal_memo_content,
        output_path=personal_memo_path,
        title="WAFT Personal Memo Template",
        from_name="Feature Showcase Generator",
        from_title="WAFT System",
        to_name="All WAFT Users",
        subject="Personal Memo Template Features",
        date=datetime.now().strftime("%B %d, %Y"),
        memo_style=True,
    )
    documents.append(personal_memo_path)
    print(f"    ✓ Generated: {personal_memo_path.name}")

    # TM Report
    print("  - TM Report...")
    tm_report_content = """
<h2>WAFT Template System: TM Report</h2>

<p>This document demonstrates the Technical Memo (TM) Report template, designed for corporate reports and technical documentation.</p>

<h2>Features</h2>
<ul>
    <li>Professional report layout</li>
    <li>Executive summary section</li>
    <li>Structured content organization</li>
    <li>Classification and metadata support</li>
</ul>

<h2>Usage</h2>
<p>Use <code>generate_tm_report()</code> for technical memos, corporate reports, and formal documentation.</p>
"""

    tm_report_path = temp_dir / "template_tm_report.pdf"
    generate_tm_report(
        title="WAFT TM Report Template",
        content=tm_report_content,
        output_path=tm_report_path,
        doc_id="SHOWCASE-TM-001",
        classification="FEATURE SHOWCASE",
        date=datetime.now().strftime("%B %d, %Y"),
        author="Feature Showcase Generator",
        department="WAFT Development",
        summary="<p>Template System Demonstration - TM Report format</p>",
    )
    documents.append(tm_report_path)
    print(f"    ✓ Generated: {tm_report_path.name}")

    return documents


def generate_foundation_v1_document(temp_dir: Path) -> Path:
    """Generate Foundation V1 document with all block types."""
    print("\n📄 Generating Foundation V1 Document...")

    config = DocumentConfigV1(
        fonts={
            "Header": ("Courier", "B"),
            "Body": ("Courier", ""),
            "Monospace": ("Courier", ""),
        },
        page_margins=(72, 72, 72, 72),  # 1 inch margins
    )

    engine = DocumentEngineV1(config)
    engine.set_title("WAFT Foundation V1 Showcase")
    engine.set_author("Feature Showcase Generator")

    # Add all block types
    engine.add(SectionHeader("Foundation V1 Block System"))
    engine.add(
        TextBlock(
            "This document demonstrates all Foundation V1 content blocks. "
            "Foundation V1 uses FPDF2 for pure Python PDF generation with a block-based API."
        )
    )

    engine.add(SectionHeader("TextBlock"))
    engine.add(
        TextBlock(
            "TextBlock is the basic content block for paragraphs and text content. "
            "It handles automatic word wrapping and page breaks."
        )
    )

    engine.add(SectionHeader("KeyValueBlock"))
    engine.add(
        KeyValueBlock(
            {
                "Technology": "FPDF2",
                "Language": "Pure Python",
                "Status": "Production",
                "Blocks Available": "6 types",
            }
        )
    )

    engine.add(SectionHeader("LogBlock"))
    engine.add(
        LogBlock(
            [
                "2026-01-11 14:00:00 - Document generation started",
                "2026-01-11 14:00:05 - All blocks added",
                "2026-01-11 14:00:10 - PDF rendering complete",
            ]
        )
    )

    engine.add(SectionHeader("WarningBlock"))
    engine.add(
        WarningBlock(
            "Foundation V1 requires manual positioning but provides full control over layout."
        )
    )

    engine.add(SectionHeader("SignatureBlock"))
    engine.add(
        SignatureBlock(
            role="WAFT System",
            name="Feature Showcase Generator",
            timestamp=datetime.now(),
        )
    )

    output_path = temp_dir / "foundation_v1_showcase.pdf"
    engine.render(output_path)
    print(f"  ✓ Generated: {output_path.name}")

    return output_path


def generate_foundation_v2_document(temp_dir: Path) -> Path:
    """Generate Foundation V2 document with enhanced blocks."""
    print("\n📄 Generating Foundation V2 Document...")

    # Use default config (will trigger font error to debug)
    config = DocumentConfigV2()
    config.title = "WAFT Foundation V2 Showcase"
    config.author = "Feature Showcase Generator"

    engine = DocumentEngineV2(config)

    # Add enhanced blocks that should work
    engine.add(SectionHeaderV2("Foundation V2 Enhanced Blocks"))
    engine.add(
        TextBlockV2(
            "Foundation V2 provides enhanced typography and professional layout blocks. "
            "This system includes advanced blocks like MetadataRail, RuleBlock, and TableBlock."
        )
    )

    engine.add(RuleBlock())

    engine.add(SectionHeaderV2("MetadataRail"))
    engine.add(
        MetadataRail(
            title="Document Metadata",
            metadata={
                "Author": "Feature Showcase Generator",
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Classification": "FEATURE SHOWCASE",
                "Version": "2.0",
            },
            style="header",
        )
    )

    engine.add(RuleBlock())

    engine.add(SectionHeaderV2("TableBlock"))
    engine.add(
        TableBlock(
            headers=["Block Type", "Description", "Status"],
            rows=[
                ["CoverPage", "Professional cover page", "Available"],
                ["MetadataRail", "Sidebar metadata display", "Available"],
                ["RuleBlock", "Horizontal rule separator", "Available"],
                ["TableBlock", "Structured data tables", "Available"],
                ["Enhanced TextBlock", "Improved typography", "Available"],
            ],
        )
    )

    engine.add(RuleBlock())
    engine.add(SectionHeaderV2("Clinical Standard Preset"))
    engine.add(
        TextBlockV2(
            "The Clinical Standard preset provides professional scientific documentation styling "
            "with Times New Roman body text, Helvetica headers, and 1-inch margins."
        )
    )

    output_path = temp_dir / "foundation_v2_showcase.pdf"
    engine.render(output_path)
    print(f"  ✓ Generated: {output_path.name}")

    return output_path


def generate_documentbuilder_showcase(temp_dir: Path) -> Path:
    """Generate DocumentBuilder showcase document."""
    print("\n📄 Generating DocumentBuilder Showcase...")

    content = """
<h2>WAFT DocumentBuilder System</h2>

<p>The DocumentBuilder provides a unified, fluent API for generating PDFs with WAFT templates.</p>

<h2>Features</h2>
<ul>
    <li>Fluent API: Chain methods for readability</li>
    <li>Presets: Common configurations ready to use</li>
    <li>Composition: Build complex documents from simple blocks</li>
    <li>Printer-friendly: One flag, automatic conversion</li>
    <li>Page constraints: exact_pages, max_pages, min_pages with feedback loops</li>
</ul>

<h2>Usage Example</h2>

<pre><code>from waft import DocumentBuilder

doc = DocumentBuilder.field_guide(
    title="My Guide",
    content="&lt;h2&gt;Introduction&lt;/h2&gt;&lt;p&gt;Content&lt;/p&gt;",
    printer_friendly=True,
    exact_pages=5
)
doc.save("output.pdf")</code></pre>

<h2>Page Constraints</h2>
<p>The DocumentBuilder supports page constraint feedback loops:</p>
<ul>
    <li><code>exact_pages</code>: Generate exactly N pages</li>
    <li><code>max_pages</code>: Maximum allowed pages</li>
    <li><code>min_pages</code>: Minimum required pages</li>
</ul>
"""

    doc = DocumentBuilder.field_guide(
        title="WAFT DocumentBuilder Showcase",
        content=content,
        printer_friendly=False,  # Show normal styling
        series="SHOWCASE",
        number="DB-001",
    )

    output_path = temp_dir / "documentbuilder_showcase.pdf"
    doc.save(output_path)
    print(f"  ✓ Generated: {output_path.name}")

    return output_path


def generate_evolution_system_showcase(temp_dir: Path) -> Path:
    """Generate Evolution System two-page PDF with all features."""
    print("\n📄 Generating Evolution System Showcase...")

    # Create comprehensive chat content with all idea types
    chat_content = """
# WAFT Evolution System: Comprehensive Feature Demonstration

## Key Decisions

We decided to implement adaptive constraint enforcement for the two-page generator. The choice was made to use real page counting instead of estimates. We will collect comprehensive metrics for every PDF generation. The final decision was to enable PNG conversion by default for quality verification.

## Important Insights

We discovered that character-counting methods are unreliable for page estimation. The key insight is that real measurement beats estimation every time. We learned that adaptive algorithms can achieve exact page counts through iterative adjustment. It turns out that comprehensive metrics enable evolution with quality data.

## Action Items

We need to implement comprehensive testing for all PDF generation features. Next step is to create documentation for the metrics system. We must create example scripts demonstrating each feature. We should build a validation suite that checks all outputs.

## Core Concepts

The system represents a new approach to document generation with evolutionary algorithms. This is a framework for creating physical knowledge artifacts. The approach combines evolutionary algorithms with constraint satisfaction. The architecture uses genetic material for styling configuration.

## Open Questions

How should we handle edge cases in page counting? What is the best approach for handling very long content? Why does the system sometimes need multiple iterations? How can we improve the fitness evaluation algorithm?
"""

    # Distill chat
    distiller = ChatDistiller()
    distilled = distiller.distill_text(chat_content, title="WAFT Evolution System Showcase")

    print(f"  - Extracted {distilled.total_ideas} ideas")
    print(f"    Decisions: {distilled.decisions_count}, Insights: {distilled.insights_count}")
    print(f"    Actions: {distilled.actions_count}, Concepts: {distilled.concepts_count}")
    print(f"    Questions: {distilled.questions_count}")

    # Create styling genome
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/chat_one_pagers"))
    styling_genes = StylingGene(
        font=FontGene(
            family="sans-serif", size_body=11, size_h1=18, size_h2=14, size_h3=12, line_height=1.6
        ),
        margin=MarginGene(
            top=20, bottom=20, left=20, right=20, section_spacing=12, paragraph_spacing=8
        ),
        color=ColorGene(
            text="#000000",
            background="#FFFFFF",
            accent="#0066cc",
            heading="#1a1a1a",
            code_bg="#f5f5f5",
            code_text="#333333",
        ),
        layout=LayoutGene(columns=1, density="normal"),
        name="Feature Showcase Genome",
    )
    genome = StylingGenome.from_genes(styling_genes)
    registry.register(genome)

    # Generate with all features
    generator = TwoPageGenerator(weasyprint_available=True)
    output_path = temp_dir / "evolution_system_showcase.pdf"

    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=2,
        convert_to_png=True,
        png_dpi=300,
        collect_metrics=True,
        metrics_dir=Path("_pyrite/metrics/pdf"),
    )

    print(f"  ✓ Generated: {output_path.name}")
    print(f"    Pages: {result['page_count']}/2")
    print(f"    Fitness: {result['fitness_metrics']['overall']:.3f}")
    print(f"    PNG conversion: {'✓' if result.get('png_paths') else '✗'}")
    print(f"    Metrics collected: {'✓' if result.get('metrics') else '✗'}")

    return output_path


def main():
    """Generate comprehensive feature showcase PDF."""
    print("=" * 70)
    print("🔬 WAFT Comprehensive Feature Showcase PDF Generator")
    print("=" * 70)
    print()

    # Create temp directory for intermediate files
    temp_dir = Path("_work_efforts/showcase_temp")
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Generate all documents
        all_documents = []

        # Template System documents
        template_docs = generate_template_documents(temp_dir)
        all_documents.extend(template_docs)

        # Foundation V1
        foundation_v1_doc = generate_foundation_v1_document(temp_dir)
        all_documents.append(foundation_v1_doc)

        # Foundation V2
        foundation_v2_doc = generate_foundation_v2_document(temp_dir)
        all_documents.append(foundation_v2_doc)

        # DocumentBuilder
        documentbuilder_doc = generate_documentbuilder_showcase(temp_dir)
        all_documents.append(documentbuilder_doc)

        # Evolution System
        evolution_doc = generate_evolution_system_showcase(temp_dir)
        all_documents.append(evolution_doc)

        # Assemble binder
        print("\n📚 Assembling Binder...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"_work_efforts/comprehensive_feature_showcase_{timestamp}.pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        binder = Binder(
            title="WAFT Comprehensive Feature Showcase",
            subtitle="Complete Demonstration of All PDF Generation Features",
            classification="FEATURE SHOWCASE",
            organization="WAFT Development Team",
            date=datetime.now().strftime("%B %d, %Y"),
            version="1.0",
            compiled_by="Feature Showcase Generator",
            cover_style="professional",
        )

        # Section 1: Template System
        section1 = binder.add_section(
            "Section 1: Template System",
            description="All template types: Field Guide, Lab Notes, Personal Memo, TM Report",
            color="#3498db",
        )
        for doc_path in template_docs:
            section1.add_document(
                DocumentEntry(
                    path=doc_path,
                    title=doc_path.stem.replace("_", " ").title(),
                    description="Template system demonstration",
                )
            )

        # Section 2: Foundation V1
        section2 = binder.add_section(
            "Section 2: Foundation V1", description="Block-based API with FPDF2", color="#2ecc71"
        )
        section2.add_document(
            DocumentEntry(
                path=foundation_v1_doc,
                title="Foundation V1 Showcase",
                description="All Foundation V1 block types",
            )
        )

        # Section 3: Foundation V2
        section3 = binder.add_section(
            "Section 3: Foundation V2",
            description="Enhanced blocks with Clinical Standard preset",
            color="#9b59b6",
        )
        section3.add_document(
            DocumentEntry(
                path=foundation_v2_doc,
                title="Foundation V2 Showcase",
                description="Enhanced typography and professional blocks",
            )
        )

        # Section 4: DocumentBuilder
        section4 = binder.add_section(
            "Section 4: DocumentBuilder",
            description="Unified fluent API for PDF generation",
            color="#e74c3c",
        )
        section4.add_document(
            DocumentEntry(
                path=documentbuilder_doc,
                title="DocumentBuilder Showcase",
                description="Fluent API and page constraints",
            )
        )

        # Section 5: Evolution System
        section5 = binder.add_section(
            "Section 5: Evolution System",
            description="Two-page generator with adaptive constraints, metrics, and PNG conversion",
            color="#f39c12",
        )
        section5.add_document(
            DocumentEntry(
                path=evolution_doc,
                title="Evolution System Showcase",
                description="Adaptive constraint enforcement, styling genomes, metrics collection",
            )
        )

        # Generate binder
        binder.generate(output_path, include_dividers=True)

        print()
        print("=" * 70)
        print("✅ Comprehensive Feature Showcase PDF Generated!")
        print("=" * 70)
        print(f"📄 Output: {output_path}")
        print(f"📊 Total documents: {len(all_documents)}")
        print("📚 Sections: 5")
        print()
        print("Features demonstrated:")
        print("  ✓ All template types (Field Guide, Lab Notes, Personal Memo, TM Report)")
        print("  ✓ Foundation V1 blocks (all 6 types)")
        print("  ✓ Foundation V2 blocks (enhanced, Clinical Standard)")
        print("  ✓ DocumentBuilder (fluent API, page constraints)")
        print("  ✓ Evolution System (two-page generator, metrics, PNG conversion)")
        print("  ✓ Binder System (cover, TOC, dividers, assembly)")
        print()

        # Open PDF
        import subprocess

        try:
            subprocess.run(["open", "-a", "Preview", str(output_path)], check=False)
            print("📖 PDF opened in Preview")
        except Exception as e:
            print(f"⚠️  Could not open PDF automatically: {e}")

    finally:
        # Cleanup temp directory (optional - keep for debugging)
        # shutil.rmtree(temp_dir, ignore_errors=True)
        pass


if __name__ == "__main__":
    main()
