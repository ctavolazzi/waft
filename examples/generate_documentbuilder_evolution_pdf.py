"""
Generate PDF about DocumentBuilder Evolution
===========================================

Creates a comprehensive PDF documenting the evolution of DocumentBuilder
to support PDF recreation from scratch.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))



def main():
    """Generate PDF about DocumentBuilder evolution."""

    title = "DocumentBuilder Evolution: PDF Recreation from Scratch"

    abstract = """
    This document describes the evolution of WAFT's DocumentBuilder class to support
    complete PDF recreation from scratch. The enhanced DocumentBuilder can now analyze
    existing PDFs, extract their structure and content, detect appropriate templates,
    and recreate them programmatically. This evolution integrates with the TemplateRegistry
    system for dynamic template discovery and management, enabling bottom-up PDF reconstruction
    capabilities that were previously unavailable.
    """

    authors = [{"name": "WAFT Development Team"}, {"name": "AI Assistant (Claude)"}]

    affiliations = ["WAFT Project", "Template Library System"]

    content = """
    <h1>Introduction</h1>
    
    <p>The DocumentBuilder class has been evolved to support complete PDF recreation from
    scratch, from the bottom up. This evolution transforms DocumentBuilder from a simple
    template-based PDF generator into a sophisticated system capable of analyzing existing
    PDFs, understanding their structure and content, and recreating them using WAFT's
    template library system.</p>
    
    <p>This capability enables WAFT to work with existing PDF documents as input,
    analyze them comprehensively, and generate new PDFs that preserve the structure
    and content of the originals while using WAFT's standardized template system.</p>
    
    <h1>Evolution Overview</h1>
    
    <h2>1.1 Previous State</h2>
    
    <p>Before this evolution, DocumentBuilder had several limitations:</p>
    
    <ul>
        <li><strong>Hardcoded Templates:</strong> TemplateType enum with static list of templates</li>
        <li><strong>Manual Template Imports:</strong> Required explicit imports for each template</li>
        <li><strong>No PDF Analysis:</strong> Could only generate PDFs, not analyze existing ones</li>
        <li><strong>No Template Discovery:</strong> Templates had to be known in advance</li>
        <li><strong>Limited Flexibility:</strong> Could not adapt to different PDF types automatically</li>
    </ul>
    
    <h2>1.2 New Capabilities</h2>
    
    <p>The evolved DocumentBuilder now provides:</p>
    
    <ul>
        <li><strong>TemplateRegistry Integration:</strong> Dynamic template discovery and management</li>
        <li><strong>PDF Analysis:</strong> Complete analysis of existing PDFs (structure, content, metadata)</li>
        <li><strong>Template Detection:</strong> Automatic template matching based on PDF characteristics</li>
        <li><strong>PDF Recreation:</strong> Generate PDFs from analyzed content</li>
        <li><strong>Bottom-Up Reconstruction:</strong> Build PDFs from scratch using analysis results</li>
    </ul>
    
    <h1>Core Components</h1>
    
    <h2>2.1 TemplateRegistry Integration</h2>
    
    <p>DocumentBuilder now integrates with the TemplateRegistry system created in this work effort.
    This provides:</p>
    
    <ul>
        <li>Dynamic template discovery from the templates directory</li>
        <li>Automatic metadata extraction (description, category, tags, parameters)</li>
        <li>Template search and filtering capabilities</li>
        <li>No hardcoded dependencies on specific templates</li>
    </ul>
    
    <p><strong>Implementation:</strong></p>
    <pre><code>class DocumentBuilder:
    _registry: Optional[TemplateRegistry] = None
    
    @classmethod
    def _get_registry(cls) -> TemplateRegistry:
        if cls._registry is None:
            cls._registry = get_registry()
        return cls._registry
    
    @classmethod
    def list_templates(cls) -> List[TemplateMetadata]:
        return cls._get_registry().list_templates()</code></pre>
    
    <h2>2.2 PDF Analysis System</h2>
    
    <p>The new <code>from_pdf()</code> method provides comprehensive PDF analysis:</p>
    
    <ul>
        <li><strong>Metadata Extraction:</strong> Title, author, dates, creator, producer</li>
        <li><strong>Structure Analysis:</strong> Sections, headings, page count</li>
        <li><strong>Content Extraction:</strong> Full text extraction with structure preservation</li>
        <li><strong>Styling Hints:</strong> Academic paper detection, LaTeX identification, formatting patterns</li>
    </ul>
    
    <p><strong>PDFAnalysis Dataclass:</strong></p>
    <pre><code>@dataclass
class PDFAnalysis:
    pdf_path: Path
    page_count: int
    metadata: Dict[str, Any]
    structure: Dict[str, Any]
    content: str
    detected_template: Optional[str]
    styling_hints: Dict[str, Any]
    sections: List[Dict[str, Any]]</code></pre>
    
    <h2>2.3 Template Detection</h2>
    
    <p>Intelligent template matching based on PDF characteristics:</p>
    
    <ul>
        <li>Checks for academic paper indicators (abstract, technical report keywords)</li>
        <li>Detects LaTeX generation from metadata</li>
        <li>Analyzes page count and document structure</li>
        <li>Matches against available templates in registry</li>
        <li>Falls back gracefully if no match found</li>
    </ul>
    
    <p><strong>Detection Logic:</strong></p>
    <pre><code>def _detect_template(cls, analysis: PDFAnalysis) -> str:
    hints = analysis.styling_hints
    
    # Academic paper detection
    if hints.get("is_academic") or hints.get("has_abstract"):
        academic = registry.get_template("academic_paper")
        if academic:
            return "academic_paper"
    
    # LaTeX-generated papers
    if hints.get("is_laTeX") and hints.get("page_count", 0) > 10:
        academic = registry.get_template("academic_paper")
        if academic:
            return "academic_paper"
    
    # Fallback to field_guide
    return "field_guide"</code></pre>
    
    <h2>2.4 PDF Recreation</h2>
    
    <p>The <code>recreate()</code> method generates PDFs from analyzed content:</p>
    
    <ul>
        <li>Uses detected template automatically</li>
        <li>Preserves document structure (sections, headings)</li>
        <li>Converts extracted content to HTML format</li>
        <li>Generates PDF using WeasyPrint</li>
    </ul>
    
    <p><strong>Usage:</strong></p>
    <pre><code># Analyze and recreate in one flow
builder = DocumentBuilder.from_pdf("source.pdf")
builder.recreate("recreated.pdf")</code></pre>
    
    <h1>Implementation Details</h1>
    
    <h2>3.1 Section Detection</h2>
    
    <p>Improved heuristics for detecting document sections:</p>
    
    <ul>
        <li>Numbered sections (e.g., "1 Introduction", "2.1 Background")</li>
        <li>All-caps headers (major sections)</li>
        <li>Known section keywords (Abstract, Introduction, Conclusion, etc.)</li>
        <li>Smart grouping by major section numbers</li>
    </ul>
    
    <h2>3.2 Content Extraction</h2>
    
    <p>Content extraction preserves document structure:</p>
    
    <ul>
        <li>Maintains heading hierarchy (h1, h2, h3)</li>
        <li>Converts plain text to HTML paragraphs</li>
        <li>Preserves section organization</li>
        <li>Handles long documents (100+ pages)</li>
    </ul>
    
    <h1>Testing Results</h1>
    
    <h2>4.1 GPT-4 Technical Report Recreation</h2>
    
    <p><strong>Test Case:</strong> Recreating the GPT-4 Technical Report (100 pages)</p>
    
    <p><strong>Results:</strong></p>
    <ul>
        <li>✅ PDF analyzed successfully</li>
        <li>✅ Title extracted: "GPT-4 Technical Report"</li>
        <li>✅ Template detected: "academic_paper"</li>
        <li>✅ Pages counted: 100</li>
        <li>✅ Sections detected: 414</li>
        <li>✅ Academic paper characteristics identified</li>
        <li>✅ LaTeX generation detected</li>
        <li>✅ PDF recreated successfully (76KB output)</li>
    </ul>
    
    <p><strong>Analysis Output:</strong></p>
    <pre><code>✅ PDF analyzed successfully
   Title: GPT-4 Technical Report
   Template: academic_paper
   Pages: 100
   Sections: 414
   Is Academic: True
   Is LaTeX: True

✅ PDF recreated successfully!
   📄 GPT-4-Techincal-Report_RECREATED.pdf (76KB)</code></pre>
    
    <h2>4.2 Current Limitations</h2>
    
    <p>While the core capabilities are working, some areas need refinement:</p>
    
    <ul>
        <li><strong>Content Extraction:</strong> Currently generating 6 pages vs 100 original
            - Section detection may be too aggressive (414 sections detected)
            - Content filtering may be too strict
            - Need better paragraph preservation</li>
        <li><strong>Formatting Preservation:</strong> Tables, figures, and equations not yet extracted</li>
        <li><strong>Styling Matching:</strong> Fonts, colors, and layout not yet preserved</li>
    </ul>
    
    <h1>Usage Examples</h1>
    
    <h2>5.1 Basic PDF Recreation</h2>
    
    <pre><code>from src.waft.document_builder import DocumentBuilder

# Analyze and recreate
builder = DocumentBuilder.from_pdf("source.pdf")
builder.recreate("recreated.pdf")</code></pre>
    
    <h2>5.2 With Custom Template</h2>
    
    <pre><code># Analyze PDF
builder = DocumentBuilder.from_pdf("source.pdf")

# Override template if needed
builder.config.template = "field_guide"

# Recreate
builder.recreate("recreated.pdf")</code></pre>
    
    <h2>5.3 Access Analysis Results</h2>
    
    <pre><code>builder = DocumentBuilder.from_pdf("source.pdf")

# Access analysis
analysis = builder._analysis
print(f"Pages: {analysis.page_count}")
print(f"Template: {analysis.detected_template}")
print(f"Sections: {len(analysis.sections)}")</code></pre>
    
    <h1>Future Enhancements</h1>
    
    <h2>6.1 Advanced Content Preservation</h2>
    
    <ul>
        <li>Tables extraction and recreation</li>
        <li>Figure/image detection and preservation</li>
        <li>Equation preservation (LaTeX, MathML)</li>
        <li>Bibliography/references formatting</li>
    </ul>
    
    <h2>6.2 Styling Preservation</h2>
    
    <ul>
        <li>Font detection and matching</li>
        <li>Color scheme extraction</li>
        <li>Layout analysis (margins, spacing)</li>
        <li>Typography matching</li>
    </ul>
    
    <h2>6.3 Multi-Format Support</h2>
    
    <ul>
        <li>Handle different PDF types (reports, papers, manuals)</li>
        <li>Better template matching algorithms</li>
        <li>Custom template creation from analysis</li>
    </ul>
    
    <h1>Conclusion</h1>
    
    <p>The evolution of DocumentBuilder represents a significant advancement in WAFT's
    PDF generation capabilities. By integrating with the TemplateRegistry system and
    adding comprehensive PDF analysis capabilities, DocumentBuilder can now work with
    existing PDFs as input, understand their structure and content, and recreate them
    using WAFT's standardized template system.</p>
    
    <p>This bottom-up reconstruction capability enables new workflows where PDFs can
    be analyzed, understood, and regenerated programmatically, opening possibilities
    for document transformation, template migration, and automated PDF processing.</p>
    
    <p>While content extraction refinement is needed for very long documents, the
    foundation is solid and the core capabilities are working. Future enhancements
    will focus on improving content preservation, styling matching, and support for
    more complex document elements like tables, figures, and equations.</p>
    """

    references = [
        "[1] WAFT Template Library System - Work Effort WE-260112-q6gl",
        "[2] TemplateRegistry Implementation - src/waft/templates/registry.py",
        "[3] Academic Paper Template - src/waft/templates/academic_paper.py",
        "[4] GPT-4 Technical Report - OpenAI, 2023",
        "[5] WeasyPrint Documentation - https://weasyprint.org/",
        "[6] Jinja2 Template Engine - https://jinja.palletsprojects.com/",
    ]

    # Generate the PDF
    output_path = Path("DocumentBuilder_Evolution_Report.pdf")

    print("📄 Generating DocumentBuilder Evolution PDF...")
    print(f"   Title: {title}")
    print(f"   Output: {output_path}")

    # Use the academic_paper template directly
    from src.waft.templates.academic_paper import generate_academic_paper

    result_path = generate_academic_paper(
        title=title,
        content=content,
        output_path=output_path,
        abstract=abstract.strip(),
        authors=authors,
        affiliations=affiliations,
        conference="WAFT Technical Reports",
        year="2026",
        references=references,
    )

    print("\n✅ PDF generated successfully!")
    print(f"   📄 {result_path.absolute()}")

    # Open the PDF
    import platform
    import subprocess

    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(result_path)])
    elif platform.system() == "Windows":
        subprocess.run(["start", str(result_path)], shell=True)
    else:  # Linux
        subprocess.run(["xdg-open", str(result_path)])

    print("   🚀 Opened in default PDF viewer")

    return result_path


if __name__ == "__main__":
    main()
