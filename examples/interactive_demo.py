#!/usr/bin/env python3
"""
WAFT Interactive Demonstration - Enhanced
==========================================

This script provides an interactive terminal demonstration of WAFT's
self-documenting capabilities with custom document generation.

Run this to see:
- Existing documents in the system
- Interactive prompt for what you want to generate
- WAFT creating documents on-demand
- Assembling documents into an explorable booklet

This is WAFT documenting WAFT using WAFT.
"""

import sys
import time
import subprocess
import platform
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.reflection import ReflectionSystem
from src.waft.templates.code_documentation import generate_code_documentation
from src.waft.templates.simple_scientific import generate_simple_scientific_document
from src.waft.templates.field_guide import generate_field_guide
from src.waft.templates.personal_memo import generate_personal_memo
from src.waft.binder import Binder, DocumentEntry


# ============================================================================
# Terminal Animation Utilities
# ============================================================================

def typing_print(text: str, delay: float = 0.03, end: str = "\n"):
    """Print text with typing animation effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def blinking_cursor(duration: float = 2.0, message: str = "Thinking"):
    """Display a blinking cursor animation."""
    cursor_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0

    while time.time() < end_time:
        sys.stdout.write(f'\r{message} {cursor_chars[i % len(cursor_chars)]} ')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write('\r' + ' ' * (len(message) + 4) + '\r')
    sys.stdout.flush()


def loading_animation(message: str, duration: float = 1.5):
    """Display a loading animation with dots."""
    end_time = time.time() + duration
    dots = 0

    while time.time() < end_time:
        sys.stdout.write(f'\r{message}{"." * (dots % 4)}{" " * (3 - dots % 4)}')
        sys.stdout.flush()
        time.sleep(0.3)
        dots += 1

    sys.stdout.write(f'\r{message}... ✓\n')
    sys.stdout.flush()


def progress_step(step_num: int, total_steps: int, description: str):
    """Display a progress step."""
    print(f"\n[{step_num}/{total_steps}] {description}")
    loading_animation(f"   {description}", duration=1.0)


def open_file(file_path: Path) -> bool:
    """Open a file using the system's default application."""
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(file_path)], check=True)
        elif system == "Windows":
            subprocess.run(["start", str(file_path)], shell=True, check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(file_path)], check=True)
        return True
    except Exception as e:
        print(f"   ⚠️  Could not open file automatically: {e}")
        print(f"   📄 Please open manually: {file_path}")
        return False


# ============================================================================
# Demo Sections
# ============================================================================

def welcome_message():
    """Display welcome message with ASCII art."""
    print("\n" + "=" * 80)
    print("""
    ██╗    ██╗ █████╗ ███████╗████████╗
    ██║    ██║██╔══██╗██╔════╝╚══██╔══╝
    ██║ █╗ ██║███████║█████╗     ██║
    ██║███╗██║██╔══██║██╔══╝     ██║
    ╚███╔███╔╝██║  ██║██║        ██║
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝        ╚═╝

    World Architecture Framework & Templates
    Interactive Documentation System
    """)
    print("=" * 80)
    print()

    typing_print("Welcome to the WAFT Interactive Demonstration.", delay=0.04)
    print()
    time.sleep(0.5)
    typing_print("WAFT is a document generation framework that can observe,", delay=0.03)
    typing_print("document, and improve itself through recursive self-reflection.", delay=0.03)
    print()
    time.sleep(0.5)


def show_existing_files():
    """Display existing PDF files in the system."""
    print("\n" + "─" * 80)
    typing_print("📚 EXISTING DOCUMENTS IN SYSTEM", delay=0.05)
    print("─" * 80 + "\n")

    output_dir = Path(__file__).parent.parent / "_work_efforts"

    if output_dir.exists():
        pdf_files = sorted(output_dir.glob("*.pdf"))

        if pdf_files:
            typing_print(f"Found {len(pdf_files)} documents:", delay=0.03)
            print()
            time.sleep(0.3)

            for pdf in pdf_files[:10]:  # Show first 10
                size_kb = pdf.stat().st_size / 1024
                print(f"  📄 {pdf.name:<50} ({size_kb:>6.1f} KB)")
                time.sleep(0.1)

            if len(pdf_files) > 10:
                print(f"\n  ... and {len(pdf_files) - 10} more documents")
        else:
            typing_print("No existing documents found. Let's generate some!", delay=0.03)

    print()
    time.sleep(0.5)


def get_user_request():
    """Get user input for what they want to generate."""
    print("\n" + "─" * 80)
    typing_print("💭 WHAT WOULD YOU LIKE TO SEE?", delay=0.05)
    print("─" * 80 + "\n")

    time.sleep(0.5)

    typing_print("WAFT can generate documents about any topic, in multiple formats.", delay=0.03)
    print()
    time.sleep(0.3)

    typing_print("Examples:", delay=0.03)
    print("  • 'Show me WAFT's architecture'")
    print("  • 'Create a research paper about quantum computing'")
    print("  • 'Generate a field guide for survival'")
    print("  • 'Make a technical overview of the reflection system'")
    print("  • Or just press Enter for the standard demo")
    print()
    time.sleep(0.3)

    typing_print("What would you like? ", delay=0.04, end="")
    user_input = input().strip()

    return user_input if user_input else "standard demo"


def generate_custom_booklet(user_request: str, output_dir: Path) -> Path:
    """Generate a custom booklet based on user request."""
    print("\n" + "─" * 80)
    typing_print("🔧 GENERATING CUSTOM BOOKLET", delay=0.05)
    print("─" * 80 + "\n")

    time.sleep(0.5)
    typing_print(f"Request: {user_request}", delay=0.03)
    print()
    time.sleep(0.5)

    # Analyze request
    blinking_cursor(duration=2.0, message="Analyzing request")

    request_lower = user_request.lower()

    # Create binder
    binder = Binder(
        title=f"WAFT Custom Documentation",
        subtitle=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        classification="DEMONSTRATION",
        cover_style="professional"
    )

    # Determine what to generate
    documents_to_generate = []

    if "standard" in request_lower or "demo" in request_lower:
        typing_print("Generating standard demonstration booklet...", delay=0.03)
        documents_to_generate = ["overview", "reflection", "architecture"]

    elif "architecture" in request_lower or "system" in request_lower or "waft" in request_lower:
        typing_print("Generating WAFT architecture documentation...", delay=0.03)
        documents_to_generate = ["overview", "architecture", "reflection"]

    elif "research" in request_lower or "paper" in request_lower or "scientific" in request_lower:
        typing_print("Generating research documentation...", delay=0.03)
        documents_to_generate = ["research_overview", "technical_analysis"]

    elif "field guide" in request_lower or "survival" in request_lower or "manual" in request_lower:
        typing_print("Generating field guide documentation...", delay=0.03)
        documents_to_generate = ["field_guide", "operations_memo"]

    else:
        typing_print("Generating general purpose documentation...", delay=0.03)
        documents_to_generate = ["overview", "user_guide"]

    print()
    time.sleep(0.5)

    # Generate documents
    generated_docs = []

    for i, doc_type in enumerate(documents_to_generate, 1):
        progress_step(i, len(documents_to_generate), f"Generating {doc_type.replace('_', ' ').title()}")

        doc_path = output_dir / f"demo_{doc_type}_{int(time.time())}.pdf"

        if doc_type == "overview":
            generate_overview_doc(doc_path, user_request)
        elif doc_type == "reflection":
            generate_reflection_doc(doc_path)
        elif doc_type == "architecture":
            generate_architecture_doc(doc_path)
        elif doc_type == "research_overview":
            generate_research_doc(doc_path, user_request)
        elif doc_type == "technical_analysis":
            generate_technical_doc(doc_path, user_request)
        elif doc_type == "field_guide":
            generate_field_guide_doc(doc_path, user_request)
        elif doc_type == "operations_memo":
            generate_operations_memo(doc_path, user_request)
        elif doc_type == "user_guide":
            generate_user_guide_doc(doc_path, user_request)

        generated_docs.append((doc_path, doc_type.replace('_', ' ').title()))

    # Add documents to binder
    print()
    typing_print("Assembling booklet with generated documents...", delay=0.03)
    print()
    time.sleep(0.5)

    section = binder.add_section("Generated Documentation", color="#2c3e50")

    for doc_path, doc_title in generated_docs:
        section.add_document(DocumentEntry(
            path=doc_path,
            title=doc_title,
            description=f"Generated based on request: {user_request[:50]}..."
        ))
        print(f"  ✓ Added: {doc_title}")
        time.sleep(0.2)

    # Generate final booklet
    print()
    loading_animation("Creating final booklet", duration=2.0)

    booklet_path = output_dir / f"WAFT_Custom_Booklet_{int(time.time())}.pdf"
    binder.generate(booklet_path, include_dividers=True)

    print()
    print(f"✅ Booklet created: {booklet_path.name}")
    print(f"   Size: {booklet_path.stat().st_size / 1024:.1f} KB")
    print(f"   Pages: {len(generated_docs)} documents + cover + TOC")
    print()

    return booklet_path


def generate_overview_doc(output_path: Path, request: str):
    """Generate system overview document."""
    content = f"""
<h2>System Overview</h2>
<p>This document provides an overview of WAFT's capabilities in response to your request:
<strong>"{request}"</strong></p>

<h2>What is WAFT?</h2>
<p>WAFT (World Architecture Framework & Templates) is a self-documenting document generation
system that can observe and document its own structure.</p>

<h2>Key Capabilities</h2>
<ul>
    <li><strong>12 Professional Templates</strong> - From academic papers to creative writing</li>
    <li><strong>Self-Observation</strong> - Reflection system analyzes the codebase</li>
    <li><strong>Document Assembly</strong> - Binder system creates multi-document collections</li>
    <li><strong>Recursive Improvement</strong> - Documentation drives development</li>
</ul>

<h2>The Recursive Loop</h2>
<p>WAFT demonstrates systems-level self-awareness by documenting itself using its own
templates, creating a feedback loop for continuous improvement.</p>

<div class="callout note">
<strong>This Document</strong><br>
This overview was generated by WAFT in response to your specific request,
demonstrating the system's ability to create custom documentation on demand.
</div>
"""

    generate_code_documentation(
        title="WAFT System Overview",
        content=content,
        output_path=output_path,
        project="WAFT Interactive Demo",
        version="1.0"
    )


def generate_reflection_doc(output_path: Path):
    """Generate reflection system documentation."""
    waft_root = Path(__file__).parent.parent / "src/waft"
    reflector = ReflectionSystem(waft_root=waft_root)
    report = reflector.reflect()

    content = f"""
<h2>Reflection System Analysis</h2>
<p>WAFT has analyzed its own codebase and generated this report.</p>

<h2>Code Metrics</h2>
<ul>
    <li><strong>Files Analyzed:</strong> {report.metrics.get('total_files', 'N/A')}</li>
    <li><strong>Functions Found:</strong> {report.metrics.get('total_functions', 'N/A')}</li>
    <li><strong>Classes Found:</strong> {report.metrics.get('total_classes', 'N/A')}</li>
    <li><strong>Documentation Coverage:</strong> {report.metrics.get('documentation_coverage', 0):.1f}%</li>
</ul>

<h2>How It Works</h2>
<p>The reflection system uses Python's AST (Abstract Syntax Tree) to analyze the
codebase and identify documentation gaps.</p>

<div class="callout tip">
<strong>Meta-Documentation</strong><br>
This analysis was performed by WAFT observing itself - demonstrating recursive
self-documentation in action.
</div>
"""

    generate_code_documentation(
        title="WAFT Reflection Report",
        content=content,
        output_path=output_path,
        project="Self-Analysis",
        version="1.0"
    )


def generate_architecture_doc(output_path: Path):
    """Generate architecture documentation."""
    content = """
<h2>System Architecture</h2>
<p>WAFT is built on three core systems working in harmony.</p>

<h2>Core Components</h2>

<h3>1. Template System</h3>
<p>12 diverse document generators covering academic, business, technical, and creative formats.</p>

<h3>2. Reflection System</h3>
<p>Uses AST analysis to observe the codebase and identify documentation needs.</p>

<h3>3. Binder System</h3>
<p>Assembles multiple documents into cohesive collections with covers, TOCs, and dividers.</p>

<h2>Data Flow</h2>
<pre>
User Request
    ↓
Template Selection
    ↓
Content Generation
    ↓
PDF Rendering (WeasyPrint)
    ↓
Document Assembly (Binder)
    ↓
Final Output
</pre>

<h2>Technology Stack</h2>
<ul>
    <li><strong>WeasyPrint</strong> - HTML/CSS to PDF conversion</li>
    <li><strong>Jinja2</strong> - Template engine</li>
    <li><strong>pypdf</strong> - PDF manipulation</li>
    <li><strong>AST</strong> - Python code analysis</li>
</ul>
"""

    generate_code_documentation(
        title="WAFT Architecture",
        content=content,
        output_path=output_path,
        project="System Design",
        version="1.0"
    )


def generate_research_doc(output_path: Path, request: str):
    """Generate research paper style document."""
    content = f"""
<h2>Abstract</h2>
<p>This research document explores the concepts related to "{request}"
in the context of self-documenting systems and recursive improvement.</p>

<h2>Introduction</h2>
<p>Modern software systems face the challenge of maintaining up-to-date
documentation as the system evolves. WAFT addresses this through
recursive self-documentation.</p>

<h2>Methodology</h2>
<p>The system employs AST-based code analysis combined with template-driven
document generation to create a feedback loop of observation and documentation.</p>

<h2>Results</h2>
<p>WAFT successfully demonstrates the ability to observe and document its own
structure, creating a foundation for continuous self-improvement through documentation.</p>

<h2>Discussion</h2>
<p>This approach represents a novel method of maintaining system documentation
through automated self-observation and generation.</p>
"""

    generate_simple_scientific_document(
        title="Self-Documenting Systems: A Case Study",
        content=content,
        output_path=output_path,
        authors=["WAFT System"],
        abstract="An exploration of recursive self-documentation in software systems.",
        date=datetime.now().strftime("%Y-%m-%d")
    )


def generate_technical_doc(output_path: Path, request: str):
    """Generate technical analysis document."""
    content = f"""
<h2>Technical Analysis</h2>
<p>Analysis generated in response to: <em>{request}</em></p>

<h2>System Components</h2>
<p>WAFT consists of modular components that work together to achieve
recursive self-documentation.</p>

<h2>Implementation Details</h2>
<ul>
    <li>Python 3.10+ for modern language features</li>
    <li>Type hints for code clarity</li>
    <li>AST-based static analysis</li>
    <li>Template-driven document generation</li>
</ul>

<h2>Performance Characteristics</h2>
<p>Document generation typically completes in under 2 seconds per document,
with binder assembly adding minimal overhead.</p>

<div class="callout note">
<strong>Scalability</strong><br>
The system scales linearly with codebase size and document complexity.
</div>
"""

    generate_code_documentation(
        title="Technical Analysis",
        content=content,
        output_path=output_path,
        project="WAFT",
        version="1.0"
    )


def generate_field_guide_doc(output_path: Path, request: str):
    """Generate field guide style document."""
    content = f"""
<h2>Purpose</h2>
<p>This field guide provides operational procedures for WAFT system usage.</p>

<h2>Quick Start</h2>
<ol>
    <li>Import the required template</li>
    <li>Prepare your content</li>
    <li>Generate the document</li>
    <li>Optionally assemble into booklet</li>
</ol>

<h2>Safety Procedures</h2>
<div style="border: 2px solid #c00; padding: 10px; margin: 10px 0; background: #fee;">
<strong>⚠️  WARNING</strong><br>
Always verify generated documents before distribution.
</div>

<h2>Operational Notes</h2>
<p>WAFT can generate documents on-demand based on user requests,
as demonstrated by this field guide created in response to: "{request}"</p>
"""

    generate_field_guide(
        title="WAFT Operations Manual",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-DEMO-001"
    )


def generate_operations_memo(output_path: Path, request: str):
    """Generate operations memo."""
    content = f"""
TO: Demo Participant
FROM: WAFT System
RE: Custom Documentation Request

This memo confirms receipt of your documentation request:
"{request}"

WAFT has processed this request and generated appropriate
documentation using its template system.

The documents have been assembled into an explorable booklet
for your review.

Thank you for participating in this demonstration.
"""

    generate_personal_memo(
        content=content,
        output_path=output_path,
        from_name="WAFT System",
        to_name="Demo Participant",
        subject="Documentation Request Processed"
    )


def generate_user_guide_doc(output_path: Path, request: str):
    """Generate user guide document."""
    content = f"""
<h2>User Guide</h2>
<p>Welcome to the WAFT user guide, generated based on: "{request}"</p>

<h2>Getting Started</h2>
<p>WAFT makes it easy to generate professional documents from templates.</p>

<h2>Available Templates</h2>
<ul>
    <li>Scientific Papers</li>
    <li>Field Guides</li>
    <li>Technical Documentation</li>
    <li>Business Documents</li>
    <li>Personal Correspondence</li>
    <li>And 7 more...</li>
</ul>

<h2>Creating Your First Document</h2>
<pre>
from src.waft.templates import generate_code_documentation

generate_code_documentation(
    title="My Document",
    content="Content here...",
    output_path=Path("output.pdf")
)
</pre>

<div class="callout tip">
<strong>Pro Tip</strong><br>
Use the Binder system to combine multiple documents into collections.
</div>
"""

    generate_code_documentation(
        title="WAFT User Guide",
        content=content,
        output_path=output_path,
        project="Documentation",
        version="1.0"
    )


# ============================================================================
# Main Demo Flow
# ============================================================================

def main():
    """Run the interactive demonstration."""
    try:
        # 1. Welcome
        welcome_message()

        # 2. Show existing files
        show_existing_files()

        # 3. Get user request
        user_request = get_user_request()

        # 4. Generate custom booklet
        output_dir = Path(__file__).parent.parent / "_work_efforts"
        output_dir.mkdir(exist_ok=True)

        booklet_path = generate_custom_booklet(user_request, output_dir)

        # 5. Open booklet
        print("\n" + "─" * 80)
        typing_print("📖 OPENING YOUR CUSTOM BOOKLET", delay=0.05)
        print("─" * 80 + "\n")

        time.sleep(0.5)
        typing_print("Your personalized documentation booklet is ready!", delay=0.03)
        print()
        time.sleep(0.3)

        typing_print("This booklet was:", delay=0.03)
        print("  ✓ Generated based on your specific request")
        print("  ✓ Created using WAFT's template system")
        print("  ✓ Assembled into a cohesive collection")
        print("  ✓ Ready to explore")
        print()
        time.sleep(0.5)

        typing_print("Opening booklet...", delay=0.03)
        print()
        open_file(booklet_path)

        # 6. Closing
        print("\n" + "=" * 80)
        print()
        typing_print("🎉 DEMONSTRATION COMPLETE", delay=0.05)
        print()
        print("=" * 80)
        print()

        typing_print("What you just experienced:", delay=0.03)
        print()
        time.sleep(0.3)

        print("  ✅ Interactive document generation")
        print("  ✅ Custom content based on your request")
        print("  ✅ Multi-document booklet assembly")
        print("  ✅ WAFT documenting itself using its own tools")
        print()
        time.sleep(0.5)

        typing_print("This is the recursive loop in action.", delay=0.04)
        typing_print("A system that documents itself can observe itself improving.", delay=0.04)
        print()
        time.sleep(0.5)

        print("─" * 80)
        print()
        print(f"📄 Your booklet: {booklet_path}")
        print("📁 All documents: _work_efforts/")
        print("📖 Verification: WHAT_WE_HAVE_HERE.md")
        print()
        print("=" * 80)
        print()

    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("\nDemonstration interrupted by user.")
        print("\n" + "=" * 80 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
