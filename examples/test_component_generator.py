#!/usr/bin/env python3
"""
Test ComponentPDFGenerator

Simple test script to demonstrate the component-based PDF generator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import ComponentPDFGenerator


def main():
    """Test the component generator."""
    # Sample content
    content = """
    WAFT (Wide-Area Functional Taxonomy) is an evolutionary code laboratory.
    It allows AI agents to modify their own code and evolve through generations.

    The system has three pillars:
    1. The Substrate: Code is DNA - agents can mutate their own source code
    2. The Physics: Scint Gym evaluates agents through error handling tests
    3. The Flight Recorder: Complete lineage tracking for scientific analysis

    Agents evolve through generations, with successful mutations surviving
    and unsuccessful ones being discarded. The system produces phylogenetic
    trees showing the evolution of code over time.
    """

    # Initialize generator
    generator = ComponentPDFGenerator(
        project_path=Path("."),
        default_allowed_pages=2,
    )

    # Generate PDF
    print("Generating component-based PDF...")
    result = generator.generate_one_pager(
        content=content,
        title="WAFT: The Evolutionary Code Laboratory",
        allowed_pages=2,
        author="WAFT Research Team",
    )

    if result["success"]:
        print("✅ Success!")
        print(f"📄 PDF: {result['pdf_path']}")
        print(f"📊 Pages: {result['page_count']}/{result['target_pages']}")
        print(
            f"🎯 Learning: {result['learning_summary'].get('successful', 0)}/{result['learning_summary'].get('total_tests', 0)} successful"
        )
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
