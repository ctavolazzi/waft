#!/usr/bin/env python3
"""
Generate WAFT Documentation for LaTeX Feature

Uses WAFT's own tools to document the LaTeX feature we just built.
This demonstrates "eating our own dog food" - using WAFT to develop WAFT.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.pdf_generator import generate_pdf, PDFGenerator
from src.waft.evolution.scientific_pdf_generator import generate_scientific_pdf
from src.waft.one_pager import create_one_pager

def generate_feature_documentation():
    """Generate comprehensive documentation using WAFT tools."""
    
    content = f"""# LaTeX & Research Tools with Live Reloading

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Branch**: `feature/latex-research-tools-live-reload`  
**Status**: ✅ Core Implementation Complete

---

## What We Built

### 1. Live Reloading Development Server

**File**: `scripts/dev_research_server.py`

A development server that automatically restarts when code changes, enabling rapid iterative development of LaTeX and research tools.

**Features**:
- Automatic server restart on file changes
- Watches `research_simulation_server.py` and `src/waft/evolution/`
- Auto-opens browser to http://localhost:8001
- Development mode indicator

**Usage**:
```bash
python3 scripts/dev_research_server.py
```

### 2. LaTeX Generator Module

**File**: `src/waft/evolution/latex_generator.py`

A complete LaTeX generation system integrated with WAFT's evolution framework.

**Integration Points**:
- **ChatDistiller**: Extracts structured ideas from content
- **StylingGenome**: Applies WAFT styling presets (clinical_standard, premium, professional)
- **StylingGenomeRegistry**: Access to style configurations

**Features**:
- Markdown to LaTeX conversion
- LaTeX character escaping
- Multiple document classes (article, report, book)
- Custom packages and preamble support
- Optional PDF compilation via pdflatex

**Usage**:
```python
from src.waft.evolution.latex_generator import generate_latex

generate_latex(
    content="# My Document\\n\\nContent here...",
    title="My Document",
    document_class="article",
    style="clinical_standard"
)
```

### 3. Research Server Integration

**New Endpoints**:
- `GET /api/report/latex` - Download research report as LaTeX
- `POST /api/export/latex` - Export any content as LaTeX

**UI Updates**:
- Added "📝 Export as LaTeX" button alongside PDF report link
- Available when simulation is complete

---

## Why This Matters

### Using WAFT to Develop WAFT

This feature demonstrates **"eating our own dog food"** - using WAFT's tools to develop WAFT features:

1. **Live Reloading**: Enables rapid iteration on LaTeX capabilities
2. **LaTeX Generation**: Adds new output format to WAFT's ecosystem
3. **Research Tools**: Enhances documentation and analysis capabilities
4. **Integration**: Works seamlessly with existing WAFT systems

### Technical Architecture

```
LaTeXGenerator
├── ChatDistiller Integration
│   └── Extracts structured ideas (concepts, decisions, insights, actions)
├── StylingGenome Integration
│   └── Applies WAFT styling presets (fonts, margins, colors)
├── Markdown to LaTeX Conversion
│   └── Headers, lists, code blocks, paragraphs
└── PDF Compilation (Optional)
    └── Uses pdflatex for PDF generation
```

---

## Next Steps

1. **Enhanced LaTeX Features**
   - Table generation from data
   - Figure/image support
   - Bibliography support
   - Custom LaTeX templates
   - Math equation support

2. **Research Tools Enhancement**
   - LaTeX export for all research reports
   - Comparative LaTeX generation
   - LaTeX template customization
   - Batch LaTeX export

3. **Development Experience**
   - Hot module reloading (no server restart)
   - WebSocket for live updates
   - Development dashboard
   - Error overlay in browser

---

## Files Created

- ✅ `scripts/dev_research_server.py` - Live reloading server
- ✅ `scripts/research_simulation_server.py` - Added dev mode and LaTeX endpoints
- ✅ `src/waft/evolution/latex_generator.py` - LaTeX generator (500+ lines)
- ✅ `src/waft/evolution/__init__.py` - Added LaTeX exports
- ✅ `_work_efforts/CHECKPOINT_2026-01-11_LATEX_RESEARCH_TOOLS_LIVE_RELOAD.md` - Documentation

---

**This documentation was generated using WAFT's PDFGenerator!**
"""

    # Generate PDF using WAFT's PDFGenerator
    output_dir = project_root / "_work_efforts" / "one_pagers"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = output_dir / f"LaTeX_Feature_Documentation_{timestamp}.pdf"
    
    print("📄 Generating PDF documentation using WAFT's PDFGenerator...")
    pdf_path = generate_pdf(
        content=content,
        title="LaTeX & Research Tools with Live Reloading",
        output_path=pdf_path,
        style="clinical_standard",
        open_pdf=False
    )
    print(f"✅ PDF generated: {pdf_path}")
    
    # Generate one-pager using WAFT's OnePager
    print("\n📋 Generating one-pager using WAFT's OnePager...")
    one_pager_path = output_dir / f"LaTeX_Feature_OnePager_{timestamp}.pdf"
    one_pager_path = create_one_pager(
        content=content,
        title="LaTeX Feature - One-Pager",
        output_path=one_pager_path
    )
    print(f"✅ One-pager generated: {one_pager_path}")
    
    # Generate scientific PDF with self-examination
    print("\n🔬 Generating scientific PDF with self-examination...")
    scientific_path = output_dir / f"LaTeX_Feature_Scientific_{timestamp}.pdf"
    scientific_path = generate_scientific_pdf(
        content=content,
        title="LaTeX Feature - Scientific Analysis",
        output_path=scientific_path,
        style="clinical_standard",
        scientific_mode=True,
        open_pdf=False
    )
    print(f"✅ Scientific PDF generated: {scientific_path}")
    
    print("\n" + "="*60)
    print("✅ All documentation generated using WAFT tools!")
    print("="*60)
    print(f"\n📄 PDF: {pdf_path}")
    print(f"📋 One-Pager: {one_pager_path}")
    print(f"🔬 Scientific: {scientific_path}")
    print("\nThis demonstrates using WAFT to develop WAFT! 🎯")

if __name__ == "__main__":
    generate_feature_documentation()
