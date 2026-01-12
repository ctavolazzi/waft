#!/usr/bin/env python3
"""
Create Partner Summary One-Pager

Creates a 2-page summary of WAFT achievements for showing to partner.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager

def main():
    """Create partner summary one-pager."""
    
    content = """# WAFT: Scientific Learning System

## What We Built

A system that **studies itself** and learns from each generation. The one-pager tool now uses Study Gym to analyze what happened and document findings.

## Key Achievements

**Study Gym Integration**
- Generate PDF first, then study what happened
- Documents findings and recommendations
- Applies corrections based on scientific analysis

**Banned Words System**
- Word restriction enforcement system
- Removed "manifesto" → "report" across codebase
- Global command: `waft-one-pager-chat`

**Evolutionary Features**
- Mapped ALL evolutionary features
- Currently using ~30% (SPAWN, genome IDs, lineage, fitness)
- Identified missing features for future integration

## Scientific Workflow

1. **PREDICT** - Generate PDF first
2. **OBSERVE** - Count actual pages
3. **STUDY** - Use Study Gym to analyze
4. **CORRECT** - Apply findings-based corrections
5. **DOCUMENT** - Save findings and recommendations

## Tools

- **Study Gym** - Scientific method learning
- **BannedWordsSystem** - Word enforcement
- **SessionReportGenerator** - Scientific reports

## Global Command

```bash
waft-one-pager-chat
```

## Philosophy

> "Physical constellation of crystallized knowledge inside spacetime through the refraction of light"

**Output:** `_work_efforts/one_pagers/[title]_[date].pdf`  
**Format:** 2 pages, printer-friendly, binder-ready
"""
    
    # Create one-pager
    title = "WAFT Achievements - Partner Summary"
    output_path = Path(f"_work_efforts/one_pagers/partner_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    pager = OnePager.from_markdown(content, title=title)
    output = pager.generate(output_path)
    
    # Check page count
    from pypdf import PdfReader
    reader = PdfReader(str(output))
    page_count = len(reader.pages)
    
    print("=" * 60)
    print("✅ Partner Summary Created!")
    print("=" * 60)
    print(f"📄 Output: {output}")
    print(f"📊 Pages: {page_count} (target: 2)")
    
    if page_count == 2:
        print("✅ Perfect 2-page document!")
    else:
        print(f"⚠️ Generated {page_count} pages (expected 2)")
        print(f"📋 Study report available in: _work_efforts/study_gym/")
    
    print()
    print("Ready to show your partner!")
    
    # Open the PDF (only this specific file)
    import subprocess
    subprocess.run(["open", "-a", "Preview", str(output)])
    
    return output

if __name__ == "__main__":
    main()
