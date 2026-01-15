#!/usr/bin/env python3
"""
Example: Unified PDF Class

Demonstrates the unified PDF class that consolidates all PDF generation
approaches into one class with many methods.
"""

from pathlib import Path
from waft import PDF

def main():
    """Demonstrate unified PDF class."""
    
    print("🎯 Unified PDF Class Examples")
    print("=" * 60)
    
    # Example 1: Template-based (WeasyPrint + Jinja2)
    print("\n1. Template-based generation:")
    PDF.from_template(
        template="field_guide",
        title="My Field Guide",
        content="<h2>Introduction</h2><p>This is a field guide example.</p>"
    ).save("_work_efforts/example_template.pdf")
    print("   ✅ Generated: _work_efforts/example_template.pdf")
    
    # Example 2: Evolution-based (ChatDistiller + StylingGenome)
    print("\n2. Evolution-based generation:")
    PDF.from_content(
        content="# My Document\n\nThis is markdown content with automatic idea extraction.",
        title="My Document",
        style="clinical_standard"
    ).save("_work_efforts/example_evolution.pdf")
    print("   ✅ Generated: _work_efforts/example_evolution.pdf")
    
    # Example 3: Simple markdown
    print("\n3. Simple markdown generation:")
    PDF.from_markdown(
        "# Simple Document\n\nThis is a simple markdown document.",
        title="Simple Doc"
    ).save("_work_efforts/example_markdown.pdf")
    print("   ✅ Generated: _work_efforts/example_markdown.pdf")
    
    # Example 4: Scientific paper
    print("\n4. Scientific paper generation:")
    PDF.scientific_paper(
        title="Research Paper Example",
        abstract="This is an abstract for a research paper.",
        content="<h2>Introduction</h2><p>Research content here...</p>",
        authors=["John Doe", "Jane Smith"]
    ).save("_work_efforts/example_scientific.pdf")
    print("   ✅ Generated: _work_efforts/example_scientific.pdf")
    
    # Example 5: Two-page constraint
    print("\n5. Two-page constraint generation:")
    PDF.two_page(
        content="# Two Page Document\n\nThis content will be constrained to exactly 2 pages.",
        title="Two Page Doc",
        style="clinical_standard"
    ).save("_work_efforts/example_two_page.pdf")
    print("   ✅ Generated: _work_efforts/example_two_page.pdf")
    
    # Example 6: From file
    print("\n6. From file (auto-detect):")
    # Create a test markdown file
    test_file = Path("_work_efforts/test_example.md")
    test_file.write_text("# Test Document\n\nThis is a test markdown file.")
    PDF.from_file(
        test_file,
        style="clinical_standard"
    ).save("_work_efforts/example_from_file.pdf")
    print("   ✅ Generated: _work_efforts/example_from_file.pdf")
    
    print("\n" + "=" * 60)
    print("✅ All examples generated successfully!")
    print("\nAll PDFs saved to: _work_efforts/")

if __name__ == "__main__":
    main()
