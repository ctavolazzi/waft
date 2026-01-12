# Evolutionary Iteration Process

**The process WAFT should aspire to for all document generation and debugging.**

---

## Overview

The evolutionary iteration process is a core WAFT workflow that enables evidence-based debugging and continuous improvement through visual verification. The process: **Generate → Visualize → Inspect → Iterate**.

---

## The Process

### Core Workflow

```
Generate PDF → Convert to PNG → Screenshot → Inspect → Identify Issues → Fix → Repeat
```

**Key Principle**: Never fix without seeing the actual output. Visual verification is essential.

### Detailed Steps

1. **Generate Output**
   - Create PDF/document using WAFT tools
   - Save to `_work_efforts/one_pagers/` or appropriate location

2. **Convert to Visual Format**
   - Convert PDF first page to PNG using `pdf_to_pngs()`
   - Use WAFT's PDF-to-image converter (pdf2image → ImageMagick → PyMuPDF fallback)
   - Save PNG alongside PDF for easy access

3. **Visual Inspection**
   - Open PNG in browser or image viewer
   - Take screenshot if needed for documentation
   - Actually SEE what the output looks like

4. **Identify Issues**
   - Compare actual output to expectations
   - Note formatting problems, styling issues, layout problems
   - Document specific issues (e.g., "sections look bland", "Overview formatting is wrong")

5. **Make Targeted Fixes**
   - Fix specific issues identified
   - Update CSS, templates, or component rendering
   - Make precise, evidence-based changes

6. **Iterate**
   - Generate new PDF
   - Convert to PNG again
   - Compare before/after
   - Repeat until satisfied

---

## Why This Process Works

### Visual Verification
- **You can't fix what you can't see**: Code changes don't always translate to visual improvements
- **Actual output matters**: HTML/CSS can render differently than expected
- **Iterative refinement**: Each cycle improves the output incrementally

### Evidence-Based Debugging
- **Runtime evidence**: Screenshots show actual PDF output, not assumptions
- **Before/after comparison**: Visual proof of improvements
- **Targeted fixes**: Fix specific issues, not guesswork

### Rapid Feedback Loop
- **Fast iteration**: Generate → View → Fix → Repeat in minutes
- **Immediate validation**: See results immediately
- **Continuous improvement**: Each iteration builds on the last

---

## Implementation in WAFT

### Automatic PNG Conversion (v0.5.2+)

**All PDF generators now create PNG screenshots automatically:**

```python
from src.waft.evolution.pdf_generator import generate_pdf

# PNG conversion happens automatically (default: convert_to_png=True)
pdf_path = generate_pdf(
    content="# My Document\n\nContent...",
    title="My Document",
    style="clinical_standard"
)
# PNG screenshot automatically created at pdf_path.with_suffix('.png')
```

### Manual Conversion

```python
from src.waft.evolution.pdf_image_converter import pdf_to_pngs

# Convert PDF to PNG images
png_paths = pdf_to_pngs("document.pdf", dpi=300)
```

### Command Integration

**`/one-pager-preview`** command encapsulates this process:
- Generates PDF
- Converts to PNG automatically
- Opens in browser for inspection
- Enables iterative debugging

---

## Example: Blandness Cure Investigation

**Problem**: PDFs look bland and unprofessional

**Process**:
1. Generated PDF → Converted to PNG → Screenshot
2. **Identified**: Sections lack visual hierarchy, typography is generic, colors are muted
3. **Fixed**: Added section boxes, improved typography, enhanced color scheme
4. Generated new PDF → PNG → Screenshot
5. **Compared**: Before vs after
6. **Iterated**: Refined styling, added gradients, improved spacing
7. **Repeated**: Until PDF looks "cool and useful"

**Result**: Iterative improvements based on visual evidence, not assumptions

---

## Philosophy

### "See Before You Fix"
- Never fix styling without seeing the actual output
- Visual verification is mandatory
- Screenshots provide objective evidence

### "Iterate Until It's Right"
- Don't stop at first attempt
- Compare before/after
- Refine until satisfied
- Each iteration improves

### "Evidence Over Assumptions"
- Use runtime evidence (screenshots)
- Don't guess what's wrong
- Fix what you actually see
- Verify with visual proof

---

## Integration with WAFT's Evolution System

This process aligns with WAFT's core philosophy:

1. **Test → Analyze → Improve → Re-test**: The scientific method
2. **Visual Fitness Function**: Screenshots as fitness criteria
3. **Iterative Refinement**: Continuous improvement through cycles
4. **Evidence-Based**: Runtime data, not assumptions

### Connection to Study Gym

- **Hypothesis**: "This styling change will improve visual appeal"
- **Test**: Generate PDF, convert to PNG, screenshot
- **Measure**: Compare before/after screenshots
- **Learn**: Document what works, what doesn't
- **Evolve**: Apply learnings to next iteration

---

## Best Practices

1. **Always Generate PNG**: Make it automatic in generation scripts
2. **Always Screenshot**: Visual proof of changes
3. **Compare Before/After**: Track improvements visually
4. **Document Findings**: Note what works, what doesn't
5. **Iterate Systematically**: One change at a time when possible
6. **Use Evidence**: Fix based on what you see, not assumptions

---

## Future Enhancements

### Automated Comparison (Planned for v0.5.3)
- Side-by-side before/after screenshots
- Automated diff detection
- Visual regression testing

### Styling Genome Integration (Planned for v0.5.3)
- Use screenshots as fitness function
- Evolve styling based on visual appeal
- Genetic algorithm for styling optimization

### Batch Testing (Planned for v0.5.3)
- Generate multiple variants
- Compare all visually
- Select best based on criteria

---

## Related Documentation

- **PDF Generation**: [PDF Generation Guide](PDF-Generation-Guide)
- **PDF to PNG Conversion**: [PDF/PNG Conversion](PDF-PNG-Conversion)
- **Evolution System**: WAFT's core evolution philosophy
- **Study Gym**: Scientific method integration

---

**This process embodies WAFT's evolutionary philosophy: test, measure, improve, repeat. Visual verification makes the feedback loop concrete and actionable.**
