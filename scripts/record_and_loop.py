#!/usr/bin/env python3
"""
Record and Loop - Scientific Experiment Cycle

Records observations from experiments, generates PDF reports, and prepares for next iteration.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.waft.brief import BriefDocument
from src.waft.utils import escape_title_for_filename
import markdown


def generate_observations_pdf(observations_file: Path, output_path: Optional[Path] = None) -> Path:
    """Generate PDF report from observations document."""
    
    # Read observations
    content = observations_file.read_text(encoding='utf-8')
    
    # Extract experiment name and cycle number
    experiment_name = "PDF Generation Improvements"
    cycle_num = "1"
    
    for line in content.split('\n'):
        if line.startswith('**Experiment Date**:'):
            # Extract date
            pass
        elif '**Iteration**:' in line:
            match = re.search(r'Cycle (\d+)', line)
            if match:
                cycle_num = match.group(1)
        elif line.startswith('# ') and 'Observations' in line:
            # Extract experiment name
            name_match = re.search(r'^# (.+?)\s*-', line)
            if name_match:
                experiment_name = name_match.group(1).strip()
    
    # Convert markdown to HTML
    try:
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'tables', 'nl2br', 'extra'],
        )
    except ImportError:
        # Basic fallback
        html_content = content.replace('\n', '<br>\n')
    
    # Generate title
    title = f"{experiment_name} - Cycle {cycle_num} Observations"
    
    # Create BriefDocument
    doc = BriefDocument(
        title=title,
        doc_id=f"OBS-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        subtitle=f"Experiment Cycle {cycle_num} - Observations Recorded",
        classification="INTERNAL",
        cover_header="EXPERIMENT OBSERVATIONS",
        cover_metadata={
            "EXPERIMENT": experiment_name,
            "CYCLE": f"Cycle {cycle_num}",
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": "Observations Recorded"
        },
        cover_footer="SCIENTIFIC METHOD - OBSERVE → DOCUMENT → ANALYZE → ITERATE",
        include_system_status=False
    )
    
    doc.content_blocks.append(html_content)
    
    # Generate PDF
    if output_path is None:
        safe_name = escape_title_for_filename(experiment_name)[:30]
        output_path = observations_file.parent / f"{safe_name}_Cycle{cycle_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    pdf_path = doc.generate(output_path=output_path)
    
    return Path(pdf_path)


def generate_preparation_pdf(preparation_file: Path, output_path: Optional[Path] = None) -> Path:
    """Generate PDF from iteration preparation document."""
    
    # Read preparation
    content = preparation_file.read_text(encoding='utf-8')
    
    # Extract iteration number
    iteration_num = "2"
    for line in content.split('\n'):
        if '**Cycle**:' in line or '**Iteration**:' in line:
            match = re.search(r'[N\+]?(\d+)', line)
            if match:
                iteration_num = match.group(1)
    
    # Convert markdown to HTML
    try:
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'tables', 'nl2br', 'extra'],
        )
    except ImportError:
        html_content = content.replace('\n', '<br>\n')
    
    # Generate title
    title = f"Iteration {iteration_num} Preparation"
    
    # Create BriefDocument
    doc = BriefDocument(
        title=title,
        doc_id=f"PREP-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        subtitle=f"Ready to Begin Cycle {iteration_num}",
        classification="INTERNAL",
        cover_header="ITERATION PREPARATION",
        cover_metadata={
            "ITERATION": f"Iteration {iteration_num}",
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "STATUS": "Ready to Begin"
        },
        cover_footer="SCIENTIFIC METHOD - PREPARE → EXECUTE → OBSERVE → ITERATE",
        include_system_status=False
    )
    
    doc.content_blocks.append(html_content)
    
    # Generate PDF
    if output_path is None:
        output_path = preparation_file.parent / f"Iteration{iteration_num}_Preparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    pdf_path = doc.generate(output_path=output_path)
    
    return Path(pdf_path)


def open_pdf_on_desktop(pdf_path: Path):
    """Open PDF on desktop (macOS)."""
    import subprocess
    import platform
    
    if platform.system() == "Darwin":  # macOS
        try:
            subprocess.run(["open", str(pdf_path)], check=False)
            print(f"  ✅ Opened PDF on desktop: {pdf_path.name}")
        except Exception as e:
            print(f"  ⚠️  Could not open PDF: {e}")
            print(f"  📄 Open manually: {pdf_path}")


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("📊 RECORD AND LOOP - Scientific Experiment Cycle")
    print("=" * 70)
    print()
    
    # Find observations file (most recent or specified)
    proof_cases_dir = project_root / "_work_efforts" / "proof_cases"
    observations_file = proof_cases_dir / "pdf_generation_improvements_observations.md"
    
    if not observations_file.exists():
        print(f"❌ Observations file not found: {observations_file}")
        print("   Please create observations document first.")
        return 1
    
    # Step 1: Generate observations PDF
    print("📄 Step 1: Generating observations PDF...")
    obs_pdf = generate_observations_pdf(observations_file)
    print(f"  ✅ Generated: {obs_pdf}")
    
    # Step 2: Create iteration 2 preparation
    print("\n📋 Step 2: Creating iteration 2 preparation...")
    prep_file = proof_cases_dir / "iteration2_preparation.md"
    
    # Read observations to extract next iteration plan
    obs_content = observations_file.read_text(encoding='utf-8')
    
    # Extract next iteration plan section
    prep_content = f"""# PDF Generation Improvements - Iteration 2 Preparation

**Prepared**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Cycle**: 2
**Status**: Ready to Begin

## Starting Conditions (Same as Cycle 1)

### System State
- **PDF Generation**: Using BriefDocument with professional cover pages
- **Code Examples**: Automatic extraction and insertion
- **Markdown Conversion**: Enhanced with syntax highlighting support
- **Title Handling**: Proper generation and escaping
- **Verdict Classification**: Dynamic based on proof results

### Test Cases (Same as Cycle 1)
1. Generate PDF from case file with multiple claims
2. Verify code examples are added automatically
3. Check markdown conversion with code blocks
4. Verify title generation and escaping
5. Test verdict-based cover page classification

## Target Improvements (From Cycle 1 Observations)

### High Priority
1. **Improve Fallback Markdown Conversion**
   - Better regex patterns for code blocks
   - Improved table conversion
   - Better header handling
   - Preserve formatting when markdown library unavailable

### Medium Priority
2. **Enhance Code Example Extraction**
   - Scan entire document for code references
   - Extract from multiple sections (not just evidence)
   - Include file paths and line numbers
   - Better code block detection

### Low Priority
3. **Better Filename Generation**
   - Smarter truncation (preserve important words)
   - Use hash for very long titles
   - Better handling of special characters in filenames

4. **Error Handling**
   - Better error messages if PDF generation fails
   - Handle PDF opening failures gracefully
   - Clear error reporting

## Implementation Plan

### Step 1: Enhance Fallback Markdown
- Improve regex patterns for code blocks
- Add table conversion regex
- Better header detection
- Preserve inline formatting

### Step 2: Improve Code Example Extraction
- Scan full document content
- Extract from all sections
- Include context (file paths, line numbers)
- Better code block formatting

### Step 3: Smarter Filename Generation
- Implement word-preserving truncation
- Add hash fallback for very long titles
- Test with various special characters

### Step 4: Error Handling
- Add try/except blocks
- Clear error messages
- Graceful degradation

## Success Criteria

### Must Have
- ✅ All current functionality works
- ✅ Fallback markdown handles common features
- ✅ Code examples extracted from all sections

### Should Have
- ✅ Better error messages
- ✅ Smarter filename generation
- ✅ Enhanced code example context

### Nice to Have
- ✅ Hash-based filenames for very long titles
- ✅ Advanced markdown features in fallback
- ✅ Code example line number extraction

## Notes

- Continue using BriefDocument for professional output
- Maintain backward compatibility
- Test with various case file formats
- Document any new utility functions created

---

**Ready to begin Iteration 2**

*Prepared: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    prep_file.write_text(prep_content, encoding='utf-8')
    print(f"  ✅ Created: {prep_file}")
    
    # Step 3: Generate preparation PDF
    print("\n📄 Step 3: Generating preparation PDF...")
    prep_pdf = generate_preparation_pdf(prep_file)
    print(f"  ✅ Generated: {prep_pdf}")
    
    # Step 4: Open PDFs on desktop
    print("\n🖥️  Step 4: Opening PDFs on desktop...")
    open_pdf_on_desktop(obs_pdf)
    open_pdf_on_desktop(prep_pdf)
    
    print("\n" + "=" * 70)
    print("✅ RECORD AND LOOP COMPLETE!")
    print("=" * 70)
    print()
    print(f"📄 Observations PDF: {obs_pdf}")
    print(f"📄 Preparation PDF: {prep_pdf}")
    print(f"📋 Observations Markdown: {observations_file}")
    print(f"📋 Preparation Markdown: {prep_file}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
