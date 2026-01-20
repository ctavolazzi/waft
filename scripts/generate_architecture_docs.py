#!/usr/bin/env python3
"""
Generate Architecture Documentation using WAFT Tools

Uses WAFT's own tools to document the architecture investigation.
Demonstrates "using WAFT to develop WAFT" practice.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.latex_generator import generate_latex
from src.waft.evolution.pdf_generator import generate_pdf
from src.waft.one_pager import create_one_pager


def generate_architecture_documentation():
    """Generate architecture documentation using WAFT tools."""

    # Read the architecture investigation document
    investigation_path = (
        project_root
        / "_work_efforts"
        / "WE-260111-2i9f_app_architecture_investigation_from_readme_entry_point"
        / "ARCHITECTURE_INVESTIGATION.md"
    )

    if not investigation_path.exists():
        print(f"❌ Architecture investigation not found: {investigation_path}")
        return

    content = investigation_path.read_text()

    # Add header with investigation metadata
    full_content = f"""# WAFT Architecture Investigation

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Work Effort**: WE-260111-2i9f
**Entry Point**: README.md
**Status**: 🔍 Investigation Complete

---

{content}

---

## Investigation Summary

This architecture investigation started from the README.md entry point and traced through:
1. ✅ CLI entry point (main.py)
2. ✅ Core module structure
3. ✅ Component relationships
4. ✅ Design patterns
5. ✅ Data flow patterns

**Key Findings**:
- WAFT is a self-modifying AI SDK with evolutionary architecture
- Three core pillars: Substrate, Physics (Scint System), Flight Recorder
- Manager pattern for orchestration
- Genome pattern for genetic material representation
- Generator pattern for document generation
- Complete lineage tracking for scientific research

**Documentation Generated Using WAFT Tools**:
- PDFGenerator for PDF documentation
- LaTeXGenerator for LaTeX documentation
- OnePager for 2-page summary

This demonstrates "using WAFT to develop WAFT" - documenting architecture with WAFT's own tools!
"""

    output_dir = project_root / "_work_efforts" / "one_pagers"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("📄 Generating architecture documentation using WAFT tools...\n")

    # 1. Generate PDF
    print("1️⃣ Generating PDF using PDFGenerator...")
    pdf_path = output_dir / f"WAFT_Architecture_Investigation_{timestamp}.pdf"
    pdf_path = generate_pdf(
        content=full_content,
        title="WAFT Architecture Investigation",
        output_path=pdf_path,
        style="clinical_standard",
        open_pdf=False,
    )
    print(f"   ✅ PDF: {pdf_path}\n")

    # 2. Generate LaTeX
    print("2️⃣ Generating LaTeX using LaTeXGenerator...")
    latex_path = output_dir / f"WAFT_Architecture_Investigation_{timestamp}.tex"
    latex_path = generate_latex(
        content=full_content,
        title="WAFT Architecture Investigation",
        output_path=latex_path,
        document_class="article",
        style="clinical_standard",
        compile_pdf=False,
    )
    print(f"   ✅ LaTeX: {latex_path}\n")

    # 3. Generate one-pager
    print("3️⃣ Generating one-pager using OnePager...")
    one_pager_path = output_dir / f"WAFT_Architecture_OnePager_{timestamp}.pdf"
    one_pager_path = create_one_pager(
        content=full_content, title="WAFT Architecture - One-Pager", output_path=one_pager_path
    )
    print(f"   ✅ One-Pager: {one_pager_path}\n")

    print("=" * 60)
    print("✅ Architecture documentation generated using WAFT tools!")
    print("=" * 60)
    print(f"\n📄 PDF: {pdf_path}")
    print(f"📝 LaTeX: {latex_path}")
    print(f"📋 One-Pager: {one_pager_path}")
    print("\nAll documentation generated using WAFT's own tools! 🎯")


if __name__ == "__main__":
    generate_architecture_documentation()
