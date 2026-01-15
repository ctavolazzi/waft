#!/usr/bin/env python3
"""
Generate Research PDF: eBook-Template Analysis & WAFT PDF Systems Comparison

Creates a comprehensive research document comparing eBook-Template with WAFT's PDF systems.
"""

from pathlib import Path
from datetime import datetime
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.academic_paper import generate_academic_paper
import markdown


def generate_research_pdf():
    """Generate comprehensive research PDF about eBook-Template analysis."""
    
    # Read the analysis document
    analysis_path = project_root / "_work_efforts" / "WE-260112-q6gl_pdf_template_library_system" / "EBOCK_TEMPLATE_ANALYSIS.md"
    analysis_content = analysis_path.read_text()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        analysis_content,
        extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
    )
    
    # Enhance HTML with better styling
    html_content = f"""
    <div class="research-content">
    {html_content}
    </div>
    
    <style>
    .research-content {{
        font-family: 'Georgia', 'Times New Roman', serif;
        line-height: 1.7;
        color: #1a1a1a;
    }}
    .research-content h1 {{
        font-size: 24pt;
        font-weight: bold;
        margin-top: 0.5in;
        margin-bottom: 0.3in;
        color: #2c3e50;
        border-bottom: 2px solid #2c3e50;
        padding-bottom: 0.1in;
    }}
    .research-content h2 {{
        font-size: 18pt;
        font-weight: bold;
        margin-top: 0.4in;
        margin-bottom: 0.2in;
        color: #34495e;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 0.05in;
    }}
    .research-content h3 {{
        font-size: 14pt;
        font-weight: bold;
        margin-top: 0.3in;
        margin-bottom: 0.15in;
        color: #34495e;
    }}
    .research-content p {{
        margin-bottom: 0.15in;
        text-align: justify;
    }}
    .research-content table {{
        border-collapse: collapse;
        width: 100%;
        margin: 0.3in 0;
        font-size: 10pt;
    }}
    .research-content th, .research-content td {{
        border: 1px solid #dee2e6;
        padding: 0.1in;
        text-align: left;
    }}
    .research-content th {{
        background-color: #f8f9fa;
        font-weight: bold;
        color: #2c3e50;
    }}
    .research-content code {{
        font-family: 'Courier New', monospace;
        font-size: 9pt;
        background-color: #f8f9fa;
        padding: 2px 6px;
        border-radius: 3px;
        color: #e83e8c;
    }}
    .research-content pre {{
        background-color: #f8f9fa;
        padding: 0.2in;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 9pt;
        border-left: 4px solid #2c3e50;
        margin: 0.2in 0;
    }}
    .research-content pre code {{
        background-color: transparent;
        padding: 0;
        color: #333;
    }}
    .research-content ul, .research-content ol {{
        margin-left: 0.3in;
        margin-bottom: 0.15in;
    }}
    .research-content li {{
        margin-bottom: 0.05in;
    }}
    .research-content hr {{
        border: none;
        border-top: 2px solid #dee2e6;
        margin: 0.4in 0;
    }}
    .research-content blockquote {{
        border-left: 4px solid #2c3e50;
        padding-left: 0.2in;
        margin-left: 0;
        font-style: italic;
        color: #555;
    }}
    </style>
    """
    
    # Generate PDF
    output_dir = project_root / "_work_efforts" / "showcase_documents"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = output_dir / f"eBook_Template_Research_Analysis_{timestamp}.pdf"
    
    print(f"Generating research PDF: {pdf_path}")
    
    generate_academic_paper(
        title="eBook-Template Repository Analysis: A Comparative Study of Multi-Format Document Generation Systems",
        content=html_content,
        output_path=pdf_path,
        abstract="""This research document provides a comprehensive analysis of the eBook-Template repository, 
        comparing its Asciidoctor-based multi-format eBook generation approach with WAFT's Python-native PDF 
        template system. The analysis examines architectural differences, feature comparisons, integration 
        opportunities, and provides actionable recommendations for both systems. Key findings reveal that while 
        eBook-Template excels at multi-format output (PDF, ePub, Kindle), WAFT provides superior template 
        diversity and Python integration. The research identifies complementary strengths and proposes 
        integration strategies for enhanced document generation capabilities.""",
        authors=[
            {"name": "WAFT Research Team"},
            {"name": "AI Assistant (Claude)"}
        ],
        conference="WAFT Research",
        year="2026",
        references=[
            "eBook-Template Repository: https://github.com/akosma/eBook-Template",
            "Asciidoctor Documentation: https://asciidoctor.org/",
            "WAFT Template System: src/waft/templates/",
            "WAFT DocumentBuilder: src/waft/document_builder.py",
            "WAFT Template Registry: src/waft/templates/registry.py"
        ],
        page_numbers=True
    )
    
    print(f"✅ Research PDF generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    pdf_path = generate_research_pdf()
    print(f"\n📄 Research PDF ready: {pdf_path}")
    print(f"   Location: {pdf_path.relative_to(project_root)}")
