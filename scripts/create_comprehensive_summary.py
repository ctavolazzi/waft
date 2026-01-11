#!/usr/bin/env python3
"""
Create Comprehensive WAFT Summary One-Pager

Creates a 2-page summary covering everything achieved today.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager

def main():
    """Create comprehensive summary one-pager."""
    
    content = """# WAFT: Scientific Learning System

## What is WAFT?

WAFT (Workflow Automation Framework & Tools) is a scientific learning system that studies itself and evolves through the Scientific Method. Today we transformed the one-pager tool to use Study Gym for self-improvement.

## Today's Achievements

**Study Gym Integration**
- One-pager generates first, then studies what happened
- Scientific Method: PREDICT → OBSERVE → STUDY → CORRECT → DOCUMENT
- Every generation creates study report with findings and recommendations
- System learns from each generation and documents patterns

**Banned Words System**
- Created `BannedWordsSystem` for word restriction enforcement
- Removed "manifesto" → "report" across entire codebase
- Renamed `ManifestoGenerator` → `SessionReportGenerator`
- Global command: `waft-one-pager-chat` works from anywhere

**Evolutionary Features Inventory**
- Mapped ALL evolutionary features in WAFT
- Currently using ~30% (SPAWN, genome IDs, lineage, fitness, names)
- Missing: MUTATE, GYM_EVAL, DEATH, SURVIVAL, Conjugate, selection mechanisms

## How It Works

**Scientific Workflow:**
1. **PREDICT** - Generate PDF with raw content
2. **OBSERVE** - Count actual pages
3. **STUDY** - Use Study Gym to analyze:
   - Record observations (page count, word count, metrics)
   - Form hypotheses (what caused the page count)
   - Document findings and conclusions
   - Generate recommendations
4. **CORRECT** - Apply corrections based on study findings
5. **DOCUMENT** - Save complete study report

**Study Reports:** `_work_efforts/study_gym/study_YYYYMMDD_HHMMSS_report.md`
Contains observations, hypotheses, findings, conclusions, recommendations.

## Tools Created

- **Study Gym** - Scientific method learning (OBSERVE → QUESTION → HYPOTHESIZE → TEST → ANALYZE → CONCLUDE)
- **BannedWordsSystem** - Word restriction enforcement
- **SessionReportGenerator** - Scientific reports, phylogenetic trees
- **One-Pager System** - 2-page printable documents with Study Gym integration

## Key Innovation

Instead of word count heuristics, we now:
- Generate first (see what actually happens)
- Study the result (understand why)
- Document findings (learn from it)
- Apply corrections (improve iteratively)

This creates a self-improving system that builds knowledge over time.

## Global Commands

```bash
waft-one-pager-chat  # Create one-pager from chat session
```

## Philosophy

> "Physical constellation of crystallized knowledge inside spacetime through the refraction of light"

WAFT creates printable, binder-ready documents as physical knowledge artifacts.

## Output & Format

- **Location:** `_work_efforts/one_pagers/[title]_[date].pdf`
- **Format:** 2 pages (front/back), printer-friendly, binder-ready
- **Study Data:** `_work_efforts/study_gym/` (all generations documented)

## What's Next

Pattern analysis, predictive models, auto-correction, full WAFT evolutionary ecosystem integration.
"""
    
    # Create one-pager
    title = "WAFT Development Summary - 2026-01-11"
    output_path = Path(f"_work_efforts/one_pagers/waft_comprehensive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    pager = OnePager.from_markdown(content, title=title)
    output = pager.generate(output_path)
    
    # Check page count
    from pypdf import PdfReader
    reader = PdfReader(str(output))
    page_count = len(reader.pages)
    
    print("=" * 60)
    print("✅ Comprehensive WAFT Summary Created!")
    print("=" * 60)
    print(f"📄 Output: {output}")
    print(f"📊 Pages: {page_count} (target: 2)")
    
    if page_count == 2:
        print("✅ Perfect 2-page document!")
    else:
        print(f"⚠️ Generated {page_count} pages (expected 2)")
        print(f"📋 Study report with recommendations: _work_efforts/study_gym/")
    
    print()
    print("Ready for printing and review!")
    
    # Open the PDF (only this specific file)
    import subprocess
    subprocess.run(["open", "-a", "Preview", str(output)])
    
    return output

if __name__ == "__main__":
    main()
