#!/usr/bin/env python3
"""
Typst Templates Demo Script
============================

Comprehensive demonstration of all Typst templates in WAFT.
Generates example PDFs showcasing each template with realistic content.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst import TypstCompiler, get_typst_registry


def create_demo_outputs():
    """Create demo PDFs for all available Typst templates."""
    
    output_dir = Path("_temp_pdf_examples")
    output_dir.mkdir(exist_ok=True)
    
    registry = get_typst_registry()
    compiler = TypstCompiler()
    
    print("🎨 Typst Templates Comprehensive Demo")
    print("=" * 60)
    print()
    
    templates = registry.list_templates()
    print(f"Found {len(templates)} templates to demonstrate\n")
    
    results = []
    
    # 1. Simple Compiler Demo
    print("📄 1. Direct Typst Compilation")
    print("-" * 60)
    simple_content = """
#set page(margin: 2.5cm)
#set text(size: 11pt)
#set heading(numbering: "1.")

= Typst Infrastructure Demo

== Overview

This document demonstrates the Typst infrastructure capabilities in WAFT.

== Features

- *Fast Compilation*: Single-pass compilation typically completes in under a second
- *Security Hardening*: Built-in protection against common vulnerabilities
- *Template System*: Auto-discovery of templates with unified API
- *Error Handling*: Comprehensive error messages and timeout protection

== Code Example

Here's how to use the compiler:

```python
from src.waft.templates.typst import TypstCompiler

compiler = TypstCompiler()
pdf = compiler.compile(content, Path("output.pdf"))
```

== Math Support

Typst has excellent math support:

$ E = m c^2 $

$ sum_(n=1)^oo 1/n^2 = pi^2/6 $

$ integral_0^1 x^2 "d"x = 1/3 $

== Conclusion

The Typst infrastructure is production-ready and provides a modern alternative to LaTeX.
"""
    try:
        pdf1 = compiler.compile(simple_content, output_dir / "01_direct_compilation.pdf")
        results.append(("✅", "Direct Compilation", pdf1))
        print(f"   ✅ Created: {pdf1.name}")
    except Exception as e:
        results.append(("❌", "Direct Compilation", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 2. Flow Way - Modern Report
    print("📊 2. Flow Way - Modern Report Template")
    print("-" * 60)
    try:
        flow_way = registry.get_generate_function("Flow Way")
        pdf2 = flow_way(
            title="WAFT Typst Infrastructure Report",
            subtitle="Comprehensive Template System",
            content="""
= Executive Summary

The Typst infrastructure provides a modern, secure, and efficient system for PDF generation.

== Architecture

The system consists of three main components:

1. *TypstCompiler*: Secure compilation engine with hardening
2. *TypstTemplateRegistry*: Auto-discovery and metadata extraction
3. *Template Wrappers*: Unified API layer for all templates

== Security Features

- Path validation prevents directory traversal attacks
- Content size limits prevent resource exhaustion
- Timeout protection prevents hanging processes
- Subprocess security with shell=False

== Performance

Typst compilation is significantly faster than LaTeX:

- Single-pass compilation (vs. LaTeX's multi-pass)
- Typical compilation time: < 1 second
- Efficient resource usage

== Template Categories

The registry includes templates across multiple categories:

- Academic papers (preprint, IEEE, AMS)
- Books and reports
- Letters and newsletters
- Interactive games

= Conclusion

The Typst infrastructure successfully provides a modern alternative to LaTeX with enhanced security and performance.
""",
            output_path=output_dir / "02_flow_way_report.pdf",
            authors=["WAFT Development Team", "Documentation Team"],
            affiliation="WAFT Project",
            year=2026,
            toc=True,
            toc_depth=3,
            main_color="0066CC"
        )
        results.append(("✅", "Flow Way", pdf2))
        print(f"   ✅ Created: {pdf2.name}")
    except Exception as e:
        results.append(("❌", "Flow Way", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 3. Arkheion - Academic Paper
    print("📚 3. Arkheion - Academic Paper (arXiv-style)")
    print("-" * 60)
    try:
        arkheion = registry.get_generate_function("arkheion")
        pdf3 = arkheion(
            title="Typst Template Infrastructure: A Modern Approach to Document Generation",
            content="""
= Introduction

Document generation systems have traditionally relied on LaTeX, a powerful but complex typesetting system. While LaTeX offers extensive capabilities, its multi-pass compilation, complex syntax, and steep learning curve present challenges for modern development workflows.

This paper presents the Typst template infrastructure integrated into WAFT, a comprehensive system that provides secure, efficient, and developer-friendly document generation using Typst, a modern LaTeX alternative.

== Background

LaTeX has been the de facto standard for academic and technical document generation for decades. However, several limitations have become apparent:

- *Slow Compilation*: Multi-pass compilation can be time-consuming
- *Complex Syntax*: Backslash-based commands can be difficult to read and write
- *Error Messages*: Cryptic error messages make debugging challenging
- *Package Management*: Complex package dependency resolution

Typst addresses these limitations with:

- Single-pass compilation
- Clean, readable syntax
- Clear error messages with precise locations
- Modern package management via Typst Universe

= Architecture

== TypstCompiler

The TypstCompiler provides secure compilation of Typst documents with comprehensive hardening:

- Path validation to prevent directory traversal
- Content size limits to prevent resource exhaustion
- Timeout protection to prevent hanging processes
- Subprocess security with explicit shell=False

== TypstTemplateRegistry

The registry system provides auto-discovery of template wrappers:

- Automatic scanning of wrapper modules
- Metadata extraction from docstrings
- Searchable index of all templates
- Unified API for template access

== Template Wrappers

Template wrappers provide a consistent interface:

- Standardized function signatures
- Parameter validation
- Error handling
- Documentation

= Security Analysis

== Threat Model

The compiler is designed to handle untrusted content safely:

- User-provided Typst content
- Potentially malicious file paths
- Resource exhaustion attacks
- Command injection attempts

== Security Measures

*Path Validation*: All paths are validated to ensure they're within allowed directories. Paths containing `..` are rejected, and absolute paths outside the project are blocked.

*Content Size Limits*: Default limit of 10MB prevents resource exhaustion. Configurable per-instance for different use cases.

*Timeout Protection*: Default 60-second timeout prevents hanging processes. Configurable for large documents.

*Subprocess Security*: All subprocess calls use `shell=False` with list arguments, preventing command injection.

= Performance Evaluation

== Compilation Speed

Typst's single-pass compilation provides significant speed improvements:

- Small documents (< 10 pages): < 0.5 seconds
- Medium documents (10-50 pages): < 1 second
- Large documents (50+ pages): 1-3 seconds

== Resource Usage

Typst is efficient in resource usage:

- Memory: Typically < 100MB for most documents
- CPU: Single-threaded, efficient algorithms
- Disk: Minimal temporary file usage

= Use Cases

== Academic Publishing

The infrastructure supports multiple academic paper formats:

- arXiv-style preprints (Arkheion)
- IEEE conference papers (Charged IEEE)
- AMS mathematical papers (Unequivocal AMS)

== Business Documents

Business document generation:

- Modern reports (Flow Way)
- Professional letters (Appreciated Letter)
- Department newsletters (Dashing Dept News)

== Creative Projects

Creative document generation:

- Fiction books (Wonderous Book)
- Campaign materials (D&D templates, planned)
- Interactive content (game templates)

= Conclusion

The Typst template infrastructure successfully provides a modern, secure, and efficient alternative to traditional LaTeX-based systems. With comprehensive security hardening, auto-discovery capabilities, and a unified API, it offers significant advantages for document generation workflows.

Future work includes integration of additional templates, enhanced data pipeline support, and expanded D&D 5e template integration.
""",
            output_path=output_dir / "03_arkheion_paper.pdf",
            authors=[
                {
                    "name": "WAFT Development Team",
                    "email": "dev@waft.example",
                    "affiliation": "WAFT Project",
                    "orcid": "0000-0000-0000-0000"
                },
                {
                    "name": "Documentation Team",
                    "email": "docs@waft.example",
                    "affiliation": "WAFT Project"
                }
            ],
            abstract="This paper presents the Typst template infrastructure integrated into WAFT, providing secure and unified access to multiple Typst templates. The system includes comprehensive security hardening, auto-discovery capabilities, and a unified API for document generation. We evaluate the system's performance, security features, and use cases across academic, business, and creative domains.",
            keywords=["typst", "document generation", "pdf", "templates", "security", "typesetting"],
            date="January 19, 2026",
            bibliography=None,
            include_appendices=True
        )
        results.append(("✅", "Arkheion", pdf3))
        print(f"   ✅ Created: {pdf3.name}")
    except Exception as e:
        results.append(("❌", "Arkheion", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 4. Charged IEEE - Conference Paper
    print("🔬 4. Charged IEEE - Conference Paper")
    print("-" * 60)
    try:
        ieee = registry.get_generate_function("Charged IEEE")
        pdf4 = ieee(
            title="A Secure Typst-Based Document Generation System for Modern Applications",
            content="""
I. INTRODUCTION

Document generation is a critical component of many software systems, from academic publishing to business reporting. Traditional approaches based on LaTeX, while powerful, present challenges in terms of compilation speed, syntax complexity, and security considerations.

This paper presents a secure Typst-based document generation system that addresses these challenges through comprehensive security hardening, efficient compilation, and a unified template API.

II. RELATED WORK

Previous work in document generation has focused primarily on LaTeX-based systems. While LaTeX provides extensive capabilities, its multi-pass compilation model and complex syntax present limitations for modern applications.

Typst, introduced in 2023, offers a modern alternative with single-pass compilation and cleaner syntax. However, integration into production systems requires careful consideration of security and reliability.

III. SYSTEM ARCHITECTURE

A. TypstCompiler

The TypstCompiler provides secure compilation with multiple layers of protection:

1) Path Validation: All file paths are validated to prevent directory traversal attacks. Paths containing `..` are rejected, and absolute paths are restricted to allowed directories.

2) Content Size Limits: Default limit of 10MB prevents resource exhaustion. This is configurable per-instance.

3) Timeout Protection: Default 60-second timeout prevents hanging processes.

4) Subprocess Security: All subprocess calls use shell=False with list arguments.

B. Template Registry

The registry system provides auto-discovery of template wrappers through:

1) Module Scanning: Automatic discovery of Python modules in the wrappers directory.

2) Metadata Extraction: Extraction of template metadata from module docstrings.

3) Search Capabilities: Full-text search across names, descriptions, and tags.

C. Template Wrappers

Template wrappers provide a unified API for all templates, ensuring consistent behavior and error handling.

IV. SECURITY ANALYSIS

A. Threat Model

The system is designed to handle untrusted content, including user-provided Typst code and file paths.

B. Security Measures

Path validation prevents directory traversal. Content size limits prevent resource exhaustion. Timeout protection prevents denial of service. Subprocess security prevents command injection.

V. PERFORMANCE EVALUATION

Typst's single-pass compilation provides significant speed improvements over LaTeX. Typical compilation times are under one second for most documents.

VI. USE CASES

The system supports multiple use cases including academic publishing, business documents, and creative projects.

VII. CONCLUSION

The Typst-based document generation system successfully provides a secure, efficient, and developer-friendly alternative to traditional LaTeX-based approaches.
""",
            output_path=output_dir / "04_ieee_paper.pdf",
            authors=[
                {
                    "name": "Research Team",
                    "department": "Computer Science",
                    "organization": "WAFT Research Lab",
                    "location": "San Francisco, CA",
                    "email": "research@waft.example"
                }
            ],
            abstract="This paper presents a secure Typst-based document generation system with comprehensive security hardening, efficient compilation, and unified template API. The system addresses limitations of traditional LaTeX-based approaches through modern design principles and security-first architecture.",
            index_terms=["Document Generation", "Typst", "Security", "PDF", "Templates"],
            paper_size="us-letter",
            bibliography=None,
            figure_supplement="Figure"
        )
        results.append(("✅", "Charged IEEE", pdf4))
        print(f"   ✅ Created: {pdf4.name}")
    except Exception as e:
        results.append(("❌", "Charged IEEE", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 5. Unequivocal AMS - Math Paper
    print("🔢 5. Unequivocal AMS - Mathematical Paper")
    print("-" * 60)
    try:
        ams = registry.get_generate_function("Unequivocal AMS")
        pdf5 = ams(
            title="Mathematical Foundations of Document Generation Systems",
            content="""
= Introduction

Document generation systems can be modeled mathematically as functions mapping content to formatted output. Let $D$ be the set of all documents, $T$ be the set of templates, and $F: D times T arrow.r "PDF"$ be the generation function.

We analyze the properties of $F$ and establish conditions for security and efficiency. The function $F: D times T arrow.r PDF$ maps documents and templates to PDF output.

= Main Results

== Theorem 1: Compilation Complexity

For a document $d in D$ with $n$ elements, Typst compilation has time complexity $O(n)$ in the single-pass model, compared to $O(k cdot n)$ for LaTeX's $k$-pass model.

*Proof.* Typst processes each element exactly once, while LaTeX requires multiple passes for cross-references and table of contents generation. $square$

== Theorem 2: Security Properties

The path validation function $V: Path to bool$ satisfies:

1. $V(p) = false$ if $p$ contains `..`
2. $V(p) = false$ if $p$ is absolute and outside allowed directories
3. $V(p) = true$ for relative paths within project

*Proof.* By construction of the validation algorithm. $square$

== Corollary 3: Path Traversal Prevention

The system prevents path traversal attacks: for any path $p$ with $.. in p$, we have $V(p) = false$.

= Applications

== Academic Publishing

The system supports multiple academic formats with consistent mathematical notation support.

== Technical Documentation

Mathematical documentation benefits from Typst's native math support and clean syntax.

= Conclusion

The mathematical foundations provide a rigorous basis for secure and efficient document generation.
""",
            output_path=output_dir / "05_ams_math.pdf",
            authors=[
                {
                    "name": "Mathematician",
                    "department": "Mathematics",
                    "organization": "WAFT University",
                    "location": "Cambridge, MA",
                    "email": "math@waft.example",
                    "url": "www.waft.example/~math"
                }
            ],
            abstract="We establish mathematical foundations for document generation systems, analyzing compilation complexity and security properties. Our results show that Typst's single-pass model provides optimal complexity while maintaining security guarantees.",
            paper_size="us-letter",
            bibliography=None
        )
        results.append(("✅", "Unequivocal AMS", pdf5))
        print(f"   ✅ Created: {pdf5.name}")
    except Exception as e:
        results.append(("❌", "Unequivocal AMS", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 6. Wonderous Book - Fiction
    print("📖 6. Wonderous Book - Fiction Book")
    print("-" * 60)
    try:
        book = registry.get_generate_function("Wonderous Book")
        pdf6 = book(
            title="The Typst Chronicles",
            content="""
= Chapter 1: The Discovery

In a world dominated by LaTeX, a new system emerged. Typst, they called it. Clean syntax, fast compilation, and a promise of something better.

Dr. Sarah Chen first encountered Typst on a rainy Tuesday afternoon. She was struggling with yet another LaTeX compilation error when a colleague mentioned this new typesetting system.

"Try Typst," he said. "It's different."

= Chapter 2: The Learning Curve

Sarah dove into Typst with the enthusiasm of a researcher discovering a new tool. The syntax was clean, the error messages helpful, and the compilation was fast—almost too fast to believe.

She wrote her first paper in Typst, and it compiled on the first try. No multiple passes, no cryptic errors, just clean, beautiful output.

= Chapter 3: The Integration

As Sarah's use of Typst grew, she began to see its potential for larger projects. She integrated it into her research workflow, building templates and automating document generation.

The WAFT project took notice. They saw the potential for a comprehensive Typst infrastructure—secure, efficient, and developer-friendly.

= Chapter 4: The Future

Today, Typst is transforming how we think about document generation. From academic papers to business reports, from books to newsletters, Typst is making typesetting accessible to everyone.

And Sarah? She's still writing, still discovering, still pushing the boundaries of what's possible with modern typesetting.

= Epilogue

The story of Typst is still being written. With each new template, each new feature, we're building the future of document generation.

And it's just getting started.
""",
            output_path=output_dir / "06_wonderous_book.pdf",
            author="WAFT Storyteller",
            paper_size="iso-b5",
            dedication="For all who seek better ways to create",
            publishing_info="WAFT Publishing House\n123 Story Lane\nNarrative City, NC 12345\n\nISBN: 978-0-000000-00-0"
        )
        results.append(("✅", "Wonderous Book", pdf6))
        print(f"   ✅ Created: {pdf6.name}")
    except Exception as e:
        results.append(("❌", "Wonderous Book", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 7. Appreciated Letter - Business Letter
    print("✉️  7. Appreciated Letter - Business Letter")
    print("-" * 60)
    try:
        letter = registry.get_generate_function("Appreciated Letter")
        pdf7 = letter(
            content="""
Dear Typst Community,

I am writing to express our excitement about the Typst template infrastructure we've built for WAFT. This system represents a significant step forward in making modern typesetting accessible to developers and content creators.

The infrastructure includes:

- Comprehensive security hardening
- Auto-discovery of templates
- Unified API across all templates
- Support for 10+ official Typst templates

We believe this system will help more people discover and use Typst for their document generation needs. The combination of Typst's excellent design and our infrastructure's security and developer experience features creates a powerful tool for creating beautiful documents.

We're excited to see how the community uses this infrastructure and look forward to contributing more templates and features in the future.

Thank you for your continued support of Typst and the open-source community.

Best regards,
""",
            output_path=output_dir / "07_business_letter.pdf",
            sender="WAFT Development Team\n123 Innovation Drive\nTech City, TC 12345\nUnited States",
            recipient="Typst Community\nOpen Source Foundation\n456 Collaboration Ave\nCommunity Town, CT 67890",
            date="January 19, 2026",
            subject="Introduction of WAFT Typst Infrastructure",
            name="WAFT Development Team\nProject Lead"
        )
        results.append(("✅", "Appreciated Letter", pdf7))
        print(f"   ✅ Created: {pdf7.name}")
    except Exception as e:
        results.append(("❌", "Appreciated Letter", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 8. Dashing Dept News - Newsletter
    print("📰 8. Dashing Dept News - Newsletter")
    print("-" * 60)
    try:
        newsletter = registry.get_generate_function("Dashing Dept News")
        pdf8 = newsletter(
            title="WAFT Department Newsletter",
            content="""
= Major Milestone: Typst Infrastructure Complete

We're excited to announce the completion of our comprehensive Typst template infrastructure! This system provides secure, efficient document generation with support for 10+ templates.

== New Features

- Auto-discovery of templates
- Security hardening
- Unified API
- Comprehensive documentation

== Upcoming Events

- Template showcase webinar: February 1st
- Community template contest: February 15th
- Documentation sprint: March 1st

== Team Spotlight

Our development team has been working tirelessly to bring you this infrastructure. Special thanks to everyone who contributed!

== Technical Deep Dive

The infrastructure uses a three-layer architecture:

1. TypstCompiler for secure compilation
2. TypstTemplateRegistry for auto-discovery
3. Template wrappers for unified API

This design ensures security, performance, and developer experience.

= Community Contributions

We've received amazing contributions from the community! Thank you to everyone who has tested, reported issues, and suggested improvements.

= Looking Ahead

We're planning several exciting features:

- Additional template integrations
- Enhanced data pipeline support
- D&D 5e template expansion
- Performance optimizations

Stay tuned for more updates!
""",
            output_path=output_dir / "08_newsletter.pdf",
            edition="January 2026\nVolume 1, Issue 1",
            hero_image=None,
            publication_info="WAFT Department of Documentation\n123 Documentation Drive\nInfo City, IC 12345\n\nFor inquiries: newsletter at waft.example"
        )
        results.append(("✅", "Dashing Dept News", pdf8))
        print(f"   ✅ Created: {pdf8.name}")
    except Exception as e:
        results.append(("❌", "Dashing Dept News", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # 9. Advanced Example - Complex Document
    print("🎯 9. Advanced Example - Complex Multi-Section Document")
    print("-" * 60)
    try:
        advanced_content = """
#set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2cm, left: 2cm, right: 2cm),
    numbering: "1",
    header: [
        #set text(size: 9pt)
        #align(right)[#counter(page)]
    ],
    footer: [
        #set text(size: 9pt)
        #align(center)[WAFT Typst Infrastructure]
    ]
)
#set text(size: 11pt)
#set par(leading: 1.4em)
#set heading(numbering: "1.")
#show heading: set text(size: 1.2em)
#set par(first-line-indent: 1em)

= Comprehensive Typst Infrastructure Guide

#align(center)[
  *A Complete Reference for Document Generation*
  
  #v(0.5em)
  January 2026
]

== Introduction

This document demonstrates advanced Typst features and the capabilities of the WAFT Typst infrastructure. We'll explore various document elements, formatting options, and integration patterns.

== Document Structure

=== Sections and Subsections

Typst provides a clean hierarchy for document organization. Sections are numbered automatically, and you can reference them easily.

=== Lists and Enumerations

*Unordered lists* are great for:
- Bullet points
- Feature lists
- Quick notes

*Numbered lists* work well for:
1. Step-by-step instructions
2. Ordered sequences
3. Prioritized items

=== Code Blocks

Typst supports syntax highlighting for code:

```python
from src.waft.templates.typst import TypstCompiler

compiler = TypstCompiler()
pdf = compiler.compile(content, Path("output.pdf"))
```

== Mathematical Content

Typst excels at mathematical typesetting:

*Inline math*: The equation $E = m c^2$ is Einstein's famous mass-energy equivalence.

*Block equations*:

$ sum_(n=1)^oo 1/n^2 = pi^2/6 $

$ int_0^1 x^2 dx = 1/3 $

$ (a + b)^2 = a^2 + 2ab + b^2 $

== Tables

#table(
    columns: 3,
    stroke: 1pt,
    align: center,
    [*Template*], [*Category*], [*Use Case*],
    [Flow Way], [Report], [Modern documents],
    [Arkheion], [Preprint], [Academic papers],
    [IEEE], [Paper], [Conference papers],
    [AMS], [Paper], [Math papers],
    [Book], [Book], [Fiction books],
    [Letter], [Letter], [Business letters],
)

== Figures and Images

#figure(
    rect(width: 100%, height: 2cm, fill: rgb("0066CC")),
    caption: [Example figure with custom styling]
)

== Advanced Formatting

=== Custom Styling

You can customize almost everything in Typst:

- Fonts and sizes
- Colors and fills
- Spacing and margins
- Page layouts

=== Grid Layouts

#grid(
    columns: 2,
    gutter: 1cm,
    [*Left Column*: This is the left column content with some text to demonstrate the grid layout system.],
    [*Right Column*: This is the right column content showing how Typst handles multi-column layouts elegantly.],
)

== Conclusion

The Typst infrastructure provides a powerful, secure, and efficient system for document generation. With support for multiple templates, comprehensive security features, and excellent performance, it's an ideal choice for modern document generation workflows.

== References

1. Typst Documentation: https://typst.app/docs/
2. Typst Universe: https://typst.app/universe/
3. WAFT Documentation: See project README
"""
        pdf9 = compiler.compile(advanced_content, output_dir / "09_advanced_document.pdf")
        results.append(("✅", "Advanced Document", pdf9))
        print(f"   ✅ Created: {pdf9.name}")
    except Exception as e:
        results.append(("❌", "Advanced Document", str(e)))
        print(f"   ❌ Failed: {e}")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    print()
    
    successful = [r for r in results if r[0] == "✅"]
    failed = [r for r in results if r[0] == "❌"]
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print()
    
    if successful:
        print("Generated PDFs:")
        total_size = 0
        for status, name, pdf_path in successful:
            if isinstance(pdf_path, Path) and pdf_path.exists():
                size = pdf_path.stat().st_size
                total_size += size
                print(f"  {status} {name:25} {pdf_path.name:30} ({size:,} bytes)")
        print()
        print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
        print()
        print(f"📁 All PDFs saved to: {output_dir.absolute()}")
    
    if failed:
        print("\nFailed generations:")
        for status, name, error in failed:
            print(f"  {status} {name}: {error}")
    
    print()
    print("🎉 Demo complete! Check the PDFs to see all templates in action.")
    
    return output_dir


if __name__ == "__main__":
    output_dir = create_demo_outputs()
    
    # Open all PDFs
    print("\n📂 Opening all generated PDFs...")
    import subprocess
    for pdf_file in sorted(output_dir.glob("*.pdf")):
        print(f"   Opening {pdf_file.name}...")
        subprocess.run(["open", str(pdf_file)], check=False)
        import time
        time.sleep(0.5)
