#!/usr/bin/env python3
"""
Generate LaTeX Documentation for LaTeX Feature

Uses the LaTeX generator we just built to create LaTeX documentation.
Full circle: using WAFT's LaTeX generator to document WAFT's LaTeX feature!
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.latex_generator import generate_latex

def generate_latex_documentation():
    """Generate LaTeX documentation using the LaTeX generator we just built."""
    
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

**This LaTeX document was generated using WAFT's LaTeXGenerator that we just built!**
**Full circle: using WAFT to develop WAFT! 🎯**
"""

    # Generate LaTeX using the LaTeX generator we just built!
    output_dir = project_root / "_work_efforts" / "one_pagers"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    latex_path = output_dir / f"LaTeX_Feature_Documentation_{timestamp}.tex"
    
    print("📝 Generating LaTeX documentation using WAFT's LaTeXGenerator...")
    print("   (This is the LaTeX generator we just built!)")
    
    latex_path = generate_latex(
        content=content,
        title="LaTeX & Research Tools with Live Reloading",
        output_path=latex_path,
        document_class="article",
        style="clinical_standard",
        compile_pdf=False  # Don't compile, just generate .tex
    )
    
    print(f"✅ LaTeX generated: {latex_path}")
    print("\n" + "="*60)
    print("✅ LaTeX documentation generated using WAFT's LaTeXGenerator!")
    print("="*60)
    print(f"\n📝 LaTeX: {latex_path}")
    print("\nThis is the full circle: using WAFT's LaTeX generator to document WAFT's LaTeX feature! 🎯")
    print("\nTo compile to PDF:")
    print(f"  pdflatex {latex_path}")

if __name__ == "__main__":
    generate_latex_documentation()
