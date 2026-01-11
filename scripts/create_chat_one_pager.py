#!/usr/bin/env python3
"""
Create One-Pager from Chat
==========================

Creates a 2-page one-pager PDF from the current chat session.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.one_pager import OnePager


def get_chat_summary() -> str:
    """
    Extract key information from the chat session.
    
    Creates a visual "at a glance" story-driven summary.
    """
    from datetime import datetime
    
    summary = f"""# WAFT: Scientific Learning System

## The Story

**Built** a system that studies itself. **Evolved** one-pager to use Study Gym. **Result:** Self-improving tool that learns from each generation.

## Key Achievements

**Study Gym Integration**
- Generate first, then study what happened
- Documents findings and recommendations
- Applies corrections based on analysis

**Banned Words System**
- `BannedWordsSystem` for word restrictions
- Removed "manifesto" → "report"
- Global: `waft-one-pager-chat`

**Evolutionary Features**
- Mapped ALL features (~30% used)
- Missing: MUTATE, GYM_EVAL, DEATH, SURVIVAL, Conjugate

## Scientific Workflow

1. PREDICT - Generate PDF
2. OBSERVE - Count pages
3. STUDY - Analyze with Study Gym
4. CORRECT - Apply findings
5. DOCUMENT - Save recommendations

## Tools

**Study Gym** - Scientific method learning  
**BannedWordsSystem** - Word enforcement  
**SessionReportGenerator** - Reports

```bash
waft-one-pager-chat
```

## Philosophy

> "Physical constellation of crystallized knowledge inside spacetime through the refraction of light"

**Output:** `_work_efforts/one_pagers/[title]_[date].pdf`  
**Format:** 2 pages, printer-friendly, binder-ready
"""
    
    return summary


def main():
    """Create one-pager from chat session."""
    # Get chat summary
    content = get_chat_summary()
    
    # Create one-pager
    title = f"Chat Session One-Pager - {datetime.now().strftime('%Y-%m-%d')}"
    output_path = Path(f"_work_efforts/one_pagers/chat_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    pager = OnePager.from_markdown(content, title=title)
    output = pager.generate(output_path)
    
    # Check page count
    from pypdf import PdfReader
    reader = PdfReader(str(output))
    page_count = len(reader.pages)
    
    print("=" * 60)
    print("✅ Chat One-Pager Created!")
    print("=" * 60)
    print(f"📄 Output: {output}")
    print(f"📊 Pages: {page_count} (target: 2)")
    
    if page_count == 2:
        print("✅ Perfect 2-page document!")
    else:
        print(f"⚠️ Generated {page_count} pages (expected 2)")
    
    print()
    print("Ready for printing and binder storage!")
    
    # Open the PDF (only this specific file)
    import subprocess
    subprocess.run(["open", "-a", "Preview", str(output)])


if __name__ == "__main__":
    main()
