# One-Pager Preview

**Generate one-pager PDF, convert to PNG screenshot, and open in browser for visual inspection.**

---

## Purpose

This command generates a one-pager PDF from the current chat session, converts the first page to a PNG screenshot, and opens it in the browser so you can visually inspect the formatting and iterate on improvements.

**Use when:**
- You want to see what the PDF actually looks like
- Debugging formatting issues
- Iterating on document structure and styling
- Need visual feedback on PDF output

---

## Execution

**Command**: `/one-pager-preview` or `/preview-pdf`

**What it does:**
1. Generates one-pager PDF using `scripts/generate_chat_one_pager.py` with `open_in_browser=True`
2. Automatically converts first page of PDF to PNG using WAFT's PDF-to-image converter
3. Opens PNG in browser for visual inspection
4. Prints paths to both PDF and PNG files

**Execution Steps:**
1. Run `python3 scripts/generate_chat_one_pager.py` (script already has `open_in_browser=True` enabled)
2. Script generates PDF
3. Script converts PDF first page to PNG automatically
4. Script opens PNG in browser
5. You can now see the actual PDF output and iterate

---

## Workflow

```
Generate PDF → Convert to PNG → Open in Browser → Inspect → Iterate
```

**Iteration Loop:**
1. Run `/one-pager-preview`
2. View PNG screenshot in browser
3. Identify formatting issues
4. Fix code/styling
5. Run `/one-pager-preview` again
6. Compare before/after
7. Repeat until satisfied

---

## Technical Details

**Script**: `scripts/generate_chat_one_pager.py`
- Uses `OnePager.from_components()` with WAFT's document component system
- Includes: Title, Abstract, Attribution, Sections, Quote components
- Generates PDF using WeasyPrint

**PDF to PNG Conversion**:
- Uses `src.waft.evolution.pdf_image_converter.pdf_to_pngs()`
- Fallback chain: pdf2image → ImageMagick → PyMuPDF
- Saves PNG in same directory as PDF
- Opens PNG file in default browser

**Output Files**:
- PDF: `_work_efforts/one_pagers/Chat_One_Pager_{timestamp}.pdf`
- PNG: `_work_efforts/one_pagers/Chat_One_Pager_{timestamp}.png`

---

## Integration

**Related Commands**:
- `/one-pager-chat` - Generate one-pager without preview
- `/one-pager` - General one-pager generation

**Related Tools**:
- `OnePager` class in `src/waft/one_pager.py`
- `ComponentBuilder` in `src/waft/evolution/document_components.py`
- PDF image converter in `src/waft/evolution/pdf_image_converter.py`

---

## Example Usage

```
/one-pager-preview
```

**Output**:
```
📄 Generating one-pager with sections and variables...
📝 Title: WAFT Self-Testing & Verification Session
📊 Sections: 8
📋 Variables: 3
💾 Output: /path/to/Chat_One_Pager_20260111_182749.pdf
📸 Screenshot saved: /path/to/Chat_One_Pager_20260111_182749.png
✅ One-Pager Generated!
```

---

## Notes

- PNG screenshot is automatically generated and opened
- First page only (one-pagers are 2 pages, but preview shows page 1)
- Browser opens automatically for visual inspection
- Use this for iterative design and formatting improvements
