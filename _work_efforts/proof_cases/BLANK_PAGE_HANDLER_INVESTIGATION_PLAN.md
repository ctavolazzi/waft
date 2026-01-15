# CASE STUDY PLAN: Blank Page Handler Verification

**Claim**: The blank page handler is working correctly and all PDFs generated through WAFT will automatically mark blank pages with "[ THIS PAGE IS BLANK ON PURPOSE ]"

**Date**: 2026-01-14 17:00:49
**Status**: Investigation Plan

---

## Investigation Objectives

1. **Verify Handler Functionality**
   - Test blank page detection logic
   - Test marker insertion (PyMuPDF and WeasyPrint fallback)
   - Verify marker text appears correctly

2. **Verify Integration Points**
   - Check all PDF generation paths call the handler
   - Verify handler is called at correct time (post-generation)
   - Check error handling (graceful degradation)

3. **Test Real-World Scenarios**
   - Generate PDFs with intentional blank pages
   - Check existing PDFs for blank pages
   - Verify markers appear in actual output

4. **Identify Gaps**
   - Find any PDF generation paths that bypass handler
   - Check for edge cases (very small text, headers/footers only)
   - Verify handler works with all PDF styles

---

## Test Plan

### Test 1: Handler Function Test
- Create test PDF with blank pages
- Run handler manually
- Verify markers appear

### Test 2: Integration Test - PDFGenerator
- Generate PDF via PDFGenerator with blank pages
- Check if handler called
- Verify markers in output

### Test 3: Integration Test - BriefDocument
- Generate brief with blank pages
- Check if handler called
- Verify markers in output

### Test 4: Integration Test - GoldenTriangle
- Generate PDF via GoldenTriangle with blank pages
- Check if handler called
- Verify markers in output

### Test 5: Real PDF Audit
- Check recent PDFs for blank pages
- Verify if markers present
- Identify any without markers

### Test 6: Edge Cases
- PDF with only headers/footers (< 10 chars)
- PDF with whitespace only
- PDF with images but no text
- Very large PDFs

---

## Success Criteria

✅ Handler detects blank pages correctly (< 10 characters)
✅ Handler adds markers using PyMuPDF or WeasyPrint fallback
✅ All major PDF generation paths call handler
✅ Markers appear in actual generated PDFs
✅ No PDF generation paths bypass handler
✅ Error handling works (graceful degradation)

---

## Evidence Collection

- Code snippets showing handler integration
- Test PDF outputs with/without markers
- Integration point verification
- Real PDF audit results
- Edge case test results

---

## Next Steps

1. Run comprehensive tests
2. Document findings
3. Create case file with evidence
4. Provide verdict (PROVEN/DISPROVEN/INCONCLUSIVE)
