#!/usr/bin/env python3
"""
WAFT Demo Session Booklet Generator

Creates a printable PDF booklet documenting the demo session,
including the meta-cognitive explanation and demo structure.
"""

from pathlib import Path
from datetime import datetime
from jinja2 import Template

try:
    from weasyprint import HTML
except ImportError:
    raise ImportError("WeasyPrint required. Install with: pip install weasyprint")


DEMO_BOOKLET_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WAFT Meta-Cognitive Demonstration</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
            
            @top-center {
                content: "WAFT Meta-Cognitive Demonstration";
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #666;
            }
            
            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #666;
            }
        }
        
        @page :first {
            @top-center { content: none; }
        }
        
        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }
        
        .cover {
            text-align: center;
            padding-top: 2in;
        }
        
        .cover h1 {
            font-size: 28pt;
            font-weight: bold;
            margin-bottom: 0.5in;
            letter-spacing: 2px;
        }
        
        .cover .subtitle {
            font-size: 16pt;
            color: #333;
            margin-bottom: 1in;
        }
        
        .cover .date {
            font-size: 12pt;
            color: #666;
            margin-top: 1.5in;
        }
        
        h1 {
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            border-bottom: 2px solid #000;
            padding-bottom: 0.1in;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
        }
        
        .demo-structure {
            background: #f5f5f5;
            padding: 0.2in;
            margin: 0.2in 0;
            border-left: 4px solid #000;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            white-space: pre-wrap;
        }
        
        .highlight {
            background: #ffffcc;
            padding: 0.05in;
        }
        
        .meta-cognition {
            background: #e8f4f8;
            padding: 0.2in;
            margin: 0.2in 0;
            border-left: 4px solid #0066cc;
        }
        
        ul, ol {
            margin-left: 0.3in;
            margin-top: 0.1in;
        }
        
        li {
            margin-bottom: 0.1in;
        }
        
        code {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background: #f0f0f0;
            padding: 0.05in;
        }
        
        .footer-note {
            margin-top: 0.5in;
            padding-top: 0.2in;
            border-top: 1px solid #ccc;
            font-size: 9pt;
            color: #666;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="cover">
        <h1>WAFT</h1>
        <div class="subtitle">Meta-Cognitive Demonstration</div>
        <div class="subtitle" style="font-size: 14pt; margin-top: 0.3in;">
            World Architecture Framework & Templates
        </div>
        <div class="date">
            {{ date }}
        </div>
    </div>
    
    <h1>Introduction</h1>
    <p>
        This booklet documents a demonstration of WAFT's meta-cognitive capabilities.
        WAFT is a self-documenting, self-modifying meta-framework that tracks its own
        work and enables continuity across AI sessions through epistemic memory.
    </p>
    
    <h2>What You Witnessed</h2>
    <ul>
        <li><strong>Basic file organization</strong> - Simple folder cleanup (2022 ChatGPT level)</li>
        <li><strong>Work effort management system</strong> - The _pyrite system for tracking intellectual labor</li>
        <li><strong>Epistemic memory</strong> - How WAFT remembers what it knows</li>
        <li><strong>Meta-cognitive perspective-taking</strong> - How AI systems can "wear" previous perspectives</li>
        <li><strong>Recursive self-improvement foundation</strong> - The basis for continuous enhancement</li>
    </ul>
    
    <h1>Demo Structure</h1>
    <p>The demonstration created the following folder structure:</p>
    <div class="demo-structure">{{ demo_structure }}</div>
    
    <h1>Meta-Cognition: The Core Concept</h1>
    
    <div class="meta-cognition">
        <h2>Why _pyrite?</h2>
        <p>
            So that WAFT can track on its own what it knows and what it doesn't.
        </p>
        <p>
            The work efforts ticketing system acts as a sort of <strong>rudimentary epistemic
            memory</strong> - a journal that any LLM can pick up and wear like a pair of glasses
            to see how the previous AI saw its world.
        </p>
        <p>
            <strong>This is perspective taking.</strong>
        </p>
        <p>
            This is a very, very, very basic, very very very simple form of LLM
            meta-cognition across architectures using a work efforts and journaling
            system to track "thoughts" or <strong>intellectual labor quanta</strong> in the form of text
            in the WAFT system, which can self-modify and recursively self-improve based
            on external and internal feedback.
        </p>
    </div>
    
    <h2>How It Works</h2>
    <ol>
        <li><strong>Work Efforts</strong>: Track discrete units of intellectual labor</li>
        <li><strong>Journaling</strong>: Record thoughts, learnings, and observations</li>
        <li><strong>Perspective Taking</strong>: New AI instances can "put on" the previous AI's
            perspective by reading the work efforts and journals</li>
    </ol>
    
    <h2>Why It Matters</h2>
    <p>This enables:</p>
    <ul>
        <li><strong>Continuity</strong>: Knowledge persists across AI sessions</li>
        <li><strong>Self-Awareness</strong>: System knows what it knows</li>
        <li><strong>Recursive Improvement</strong>: System can improve based on its own observations</li>
        <li><strong>Meta-Cognition</strong>: Thinking about thinking</li>
    </ul>
    
    <h2>The Recursive Loop</h2>
    <ol>
        <li>AI does work → Creates work effort</li>
        <li>AI reflects → Writes journal entry</li>
        <li>AI documents → Records what it learned</li>
        <li>Next AI reads → Understands previous context</li>
        <li>Next AI continues → Builds on previous knowledge</li>
        <li>Cycle repeats → Continuous improvement</li>
    </ol>
    
    <h1>Intellectual Labor Quanta</h1>
    <p>
        Each work effort, journal entry, or documentation piece represents a
        <span class="highlight"><strong>quantum of intellectual labor</strong></span> - a discrete unit of thought and work
        that can be tracked, measured, and built upon.
    </p>
    
    <h1>Cross-Architecture Meta-Cognition</h1>
    <p>
        This system works across different AI architectures because it's based on
        <strong>text</strong> - the universal interface. Any LLM can read and understand:
    </p>
    <ul>
        <li>Work effort descriptions</li>
        <li>Journal entries</li>
        <li>Documentation</li>
        <li>Status updates</li>
    </ul>
    <p>
        This creates a form of <strong>perspective-taking</strong> where one AI can understand
        how another AI (or a previous version of itself) saw the world.
    </p>
    
    <h1>Next Steps</h1>
    <p>
        The demo folder structure created during this demonstration can serve as a
        <strong>jumping off point for full installation of the WAFT system</strong>. The organized
        structure, tools folder, and _pyrite system provide the foundation for:
    </p>
    <ul>
        <li>Organic system growth and expansion</li>
        <li>Work effort tracking and management</li>
        <li>Epistemic memory development</li>
        <li>Recursive self-improvement</li>
    </ul>
    
    <div class="footer-note">
        <p>Generated by WAFT - World Architecture Framework & Templates</p>
        <p>This is WAFT tracking its own work, understanding its own state,</p>
        <p>and enabling future AI instances to continue where this one left off.</p>
    </div>
</body>
</html>
"""


def generate_demo_structure_tree(demo_dir: Path, prefix: str = "", is_last: bool = True, root_name: str = None) -> str:
    """Generate a text tree representation of the demo structure."""
    if root_name is None:
        root_name = demo_dir.name if demo_dir.name else "demo_output"
    
    # For root, use the provided name
    if prefix == "":
        name = root_name
    else:
        name = demo_dir.name
    
    connector = "└── " if is_last else "├── "
    result = f"{prefix}{connector}{name}/\n"
    
    if demo_dir.is_dir():
        children = sorted([p for p in demo_dir.iterdir() if p.name != ".gitkeep" and not p.name.endswith('.pdf')])
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            extension = "    " if is_last else "│   "
            result += generate_demo_structure_tree(child, prefix + extension, is_last_child, root_name)
    
    return result


def generate_demo_booklet(demo_dir: Path, output_path: Path) -> Path:
    """
    Generate a PDF booklet documenting the demo session.
    
    Args:
        demo_dir: Path to the demo output directory
        output_path: Path where the PDF should be saved
        
    Returns:
        Path to the generated PDF
    """
    # Read meta-cognition explanation if available
    meta_cog_file = demo_dir / "tools" / "meta_cognition_explanation.md"
    meta_cog_content = ""
    if meta_cog_file.exists():
        meta_cog_content = meta_cog_file.read_text()
    
    # Generate structure tree
    demo_structure = generate_demo_structure_tree(demo_dir)
    
    # Render template
    template = Template(DEMO_BOOKLET_TEMPLATE)
    html_content = template.render(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        demo_structure=demo_structure,
        meta_cognition_content=meta_cog_content
    )
    
    # Generate PDF
    HTML(string=html_content).write_pdf(str(output_path))
    
    return output_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_dir = Path(sys.argv[1])
    else:
        demo_dir = Path(__file__).parent.parent / "demo_output"
    
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = demo_dir / "WAFT_Demo_Booklet.pdf"
    
    if not demo_dir.exists():
        print(f"Error: Demo directory not found: {demo_dir}")
        sys.exit(1)
    
    print(f"Generating demo booklet...")
    print(f"  Demo directory: {demo_dir}")
    print(f"  Output: {output_path}")
    
    pdf_path = generate_demo_booklet(demo_dir, output_path)
    print(f"✅ Booklet generated: {pdf_path}")
    
    # Try to open the PDF
    try:
        import platform
        import subprocess
        
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=True)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=True)
        print(f"✅ PDF opened")
    except Exception as e:
        print(f"⚠️  Could not open PDF automatically: {e}")
        print(f"   Please open manually: {pdf_path}")
