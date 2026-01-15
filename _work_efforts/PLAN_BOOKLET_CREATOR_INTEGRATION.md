# Feature Evolution Plan: Booklet Creator Integration

**Date**: 2026-01-12  
**Being ID**: `being_20260112_204056_1b1c9bbd`  
**Reality**: `planning_reality`  
**Status**: Planning Complete - Ready for Execution

---

## Overview

Integrate the `booklet-creator` repository (https://github.com/chongchonghe/booklet-creator.git) into WAFT as a working prototype. The script rearranges PDF pages for booklet printing (Tabloid 11x17, folded and stapled).

**Feature Goal**: Create a functional prototype that integrates booklet-creator's page rearrangement algorithm into WAFT's PDF tool ecosystem.

---

## Feature Analysis

### Repository Analysis

**Source Repository**: `chongchonghe/booklet-creator`
- **Language**: Python
- **Dependencies**: 
  - `PyPDF2=3.0.1` (old version)
  - `numpy`
- **Core Algorithm**: Rearranges PDF pages for booklet printing
- **Output**: Creates `.booklet.pdf` file with rearranged pages

### Algorithm Understanding

The booklet-creator uses a specific page rearrangement algorithm:
- For an 8-page document, rearranges to: `4, 5, 6, 3, 2, 7, 8, 1`
- Designed for Tabloid (11x17) printing with:
  - 2 pages per sheet
  - Short-edge binding
  - Normal 'Z' layout
- Handles page ranges (start/end pages)
- Can print page order without rearranging

### Current WAFT State

**PDF Libraries**:
- ✅ `pypdf>=3.0.0` (modern version, already in dependencies)
- ✅ `numpy` (likely available, need to verify)
- ⚠️ `PyPDF2` (old, deprecated - needs migration to `pypdf`)

**Existing PDF Tools**:
- `src/waft/document_builder.py` - Uses `pypdf.PdfReader`
- `src/waft/redactor.py` - Uses `pypdf.PdfReader, PdfWriter`
- `tools/pdf_binder_organizer/` - Uses `pypdf` for PDF manipulation
- `src/waft/binder.py` - Binder system for combining PDFs

**Integration Points**:
- `tools/` directory - Natural location for PDF utilities
- `src/waft/evolution/` - PDF generation tools
- `src/waft/` - Core PDF manipulation tools

---

## Architecture

### Integration Approach

**Option 1: Standalone Tool** (Recommended for Prototype)
- Location: `tools/booklet_creator/`
- Structure:
  ```
  tools/booklet_creator/
  ├── __init__.py
  ├── booklet.py          # Core rearrangement logic
  ├── cli.py              # CLI interface
  └── README.md
  ```

**Option 2: Integrated Module**
- Location: `src/waft/booklet.py`
- Integrate with existing PDF tools
- Add to `src/waft/__init__.py` exports

**Decision**: Start with **Option 1** (standalone tool) for prototype, can migrate to Option 2 later.

### Migration Strategy

**PyPDF2 → pypdf Migration**:
- `PyPDF2.PdfReader` → `pypdf.PdfReader`
- `PyPDF2.PdfWriter` → `pypdf.PdfWriter`
- API is mostly compatible, minor adjustments needed

---

## Implementation Plan

### Phase 1: Setup & Migration (30 min)

**Task 1.1: Create Tool Directory**
- [ ] Create `tools/booklet_creator/` directory
- [ ] Add `__init__.py`
- [ ] Create `README.md` with usage instructions

**Task 1.2: Migrate Code**
- [ ] Copy `booklet.py` from repository
- [ ] Migrate `PyPDF2` → `pypdf`:
  - Replace `from PyPDF2 import PdfWriter as Writer, PdfReader as Reader`
  - Replace with `from pypdf import PdfWriter, PdfReader`
  - Update variable names if needed
- [ ] Update imports and API calls
- [ ] Test basic functionality

**Task 1.3: Dependency Check**
- [ ] Verify `numpy` is available (add to dependencies if needed)
- [ ] Verify `pypdf>=3.0.0` is available (already in pyproject.toml)
- [ ] Update `requirements.txt` or `pyproject.toml` if needed

### Phase 2: Integration & Enhancement (45 min)

**Task 2.1: Create CLI Interface**
- [ ] Create `cli.py` with Typer/Click interface
- [ ] Support command: `waft booklet <pdf_file> [options]`
- [ ] Options:
  - `--start <page>` - Starting page number
  - `--end <page>` - Ending page number
  - `--print-pages` - Print page order without rearranging
  - `--output <path>` - Custom output path
- [ ] Add help text and usage examples

**Task 2.2: Python API**
- [ ] Create clean Python API in `booklet.py`:
  ```python
  def rearrange_for_booklet(
      pdf_path: Path,
      start: int = 1,
      end: Optional[int] = None,
      output_path: Optional[Path] = None
  ) -> Path
  ```
- [ ] Return output path
- [ ] Handle errors gracefully
- [ ] Add type hints

**Task 2.3: Integration with WAFT Tools**
- [ ] Consider integration with `DocumentBuilder`:
  - Add `.booklet()` method to `DocumentBuilder`
  - Or standalone function: `waft.booklet.rearrange()`
- [ ] Integration with `Binder` system (optional):
  - Rearrange binder pages for booklet printing
- [ ] Document integration patterns

### Phase 3: Testing & Documentation (30 min)

**Task 3.1: Testing**
- [ ] Create test PDFs (4, 8, 12, 16 pages)
- [ ] Test page rearrangement algorithm
- [ ] Verify output PDFs are valid
- [ ] Test edge cases:
  - Minimum pages (4)
  - Odd page counts
  - Large documents
  - Page ranges

**Task 3.2: Documentation**
- [ ] Update `README.md` with:
  - Usage examples
  - Printer setup instructions
  - Algorithm explanation
  - Integration examples
- [ ] Add docstrings to all functions
- [ ] Create example script in `examples/`

**Task 3.3: Example Usage**
- [ ] Create `examples/create_booklet.py`:
  ```python
  from waft.booklet import rearrange_for_booklet
  from pathlib import Path
  
  # Rearrange a PDF for booklet printing
  output = rearrange_for_booklet(
      pdf_path=Path("document.pdf"),
      start=1,
      end=None
  )
  print(f"Booklet PDF created: {output}")
  ```

### Phase 4: Polish & Integration (15 min)

**Task 4.1: Error Handling**
- [ ] Validate input PDF exists
- [ ] Validate page ranges
- [ ] Handle empty PDFs
- [ ] Provide clear error messages

**Task 4.2: Output Options**
- [ ] Support custom output paths
- [ ] Preserve original filename with `.booklet` suffix (default)
- [ ] Option to overwrite or create new file

**Task 4.3: CLI Command Registration**
- [ ] Add to main WAFT CLI if applicable
- [ ] Or document as standalone tool
- [ ] Update main README with tool reference

---

## Dependencies

### Required
- ✅ `pypdf>=3.0.0` (already in `pyproject.toml`)
- ⚠️ `numpy` (need to verify/add if missing)

### Optional
- `typer` or `click` for CLI (WAFT uses `typer`)

---

## Integration Points

### 1. DocumentBuilder Integration (Future)
```python
from waft import DocumentBuilder

# Generate PDF
doc = DocumentBuilder.field_guide(title="Guide", content="...")
doc.save("guide.pdf")

# Create booklet version
from waft.booklet import rearrange_for_booklet
booklet = rearrange_for_booklet("guide.pdf")
```

### 2. Binder Integration (Future)
```python
from waft.binder import Binder

# Create binder
binder = Binder("My Binder")
binder.add_document(...)
binder.save("binder.pdf")

# Create booklet version
booklet = rearrange_for_booklet("binder.pdf")
```

### 3. CLI Integration
```bash
# Standalone command
waft booklet document.pdf

# With options
waft booklet document.pdf --start 5 --end 20 --output booklet.pdf
```

---

## Testing Strategy

### Unit Tests
- [ ] Test page rearrangement algorithm with known inputs
- [ ] Test edge cases (4 pages, odd counts, large docs)
- [ ] Test page range selection
- [ ] Test error handling

### Integration Tests
- [ ] Test with real PDFs from WAFT generation
- [ ] Test CLI interface
- [ ] Test Python API

### Manual Testing
- [ ] Print test booklet on Tabloid paper
- [ ] Verify page order is correct when folded
- [ ] Verify binding works correctly

---

## Risks & Mitigations

### Risk 1: PyPDF2 → pypdf Migration Issues
**Mitigation**: 
- Test thoroughly with sample PDFs
- Check pypdf documentation for API differences
- Handle any breaking changes gracefully

### Risk 2: Algorithm Correctness
**Mitigation**:
- Test with known page counts (4, 8, 12, 16)
- Verify against original repository behavior
- Manual testing with printed booklets

### Risk 3: Integration Complexity
**Mitigation**:
- Start with standalone tool (Option 1)
- Document integration patterns for future
- Keep API simple and focused

---

## Success Criteria

### Prototype Complete When:
- ✅ Code migrated from PyPDF2 to pypdf
- ✅ CLI interface working
- ✅ Python API functional
- ✅ Basic tests passing
- ✅ Documentation complete
- ✅ Example usage provided
- ✅ Can rearrange PDFs for booklet printing

### Future Enhancements (Post-Prototype):
- Integration with DocumentBuilder
- Integration with Binder system
- Support for different paper sizes
- Support for different binding types
- GUI interface (optional)

---

## Timeline Estimate

- **Phase 1**: 30 minutes (Setup & Migration)
- **Phase 2**: 45 minutes (Integration & Enhancement)
- **Phase 3**: 30 minutes (Testing & Documentation)
- **Phase 4**: 15 minutes (Polish & Integration)

**Total**: ~2 hours for complete prototype

---

## Next Steps After Planning

1. Review plan with user
2. Execute plan using `/evolve` command (spawns Being, executes workflow)
3. Or execute manually following this plan
4. Track execution through Being system
5. Complete evolution cycle

---

## Being Planning Record

**Being ID**: `being_20260112_204056_1b1c9bbd`  
**Reality**: `planning_reality`  
**Ancestral Chain**: `['source_consciousness', 'being_20260112_204056_1b1c9bbd']`  
**Lifetimes**: 1 (first birth)

**Planning Participation**:
- Feature specification extracted
- Repository analyzed
- Dependencies identified
- Integration points found
- Comprehensive plan created

**Skills Learned/Improved**:
- Planning: Analyzed feature requirements
- Analysis: Understood algorithm and dependencies
- Architecture: Designed integration approach

**Knowledge Gained**:
- Booklet printing page rearrangement algorithm
- PyPDF2 to pypdf migration patterns
- WAFT PDF tool ecosystem structure
- Integration patterns for new tools

---

**Plan Status**: ✅ Complete - Ready for Execution
