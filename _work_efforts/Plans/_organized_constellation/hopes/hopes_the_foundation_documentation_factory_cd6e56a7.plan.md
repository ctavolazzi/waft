---
name: The Foundation Documentation Factory
overview: Create DocumentEngine class as a reusable Research Documentation Library that generates SCP/Dossier-style PDFs with modular content blocks, configurable styling, and automatic redaction. The "Teleport Massive" story becomes the first use case.
todos:
  - id: add-fpdf2-dependency
    content: Add fpdf2>=2.7.0 to pyproject.toml dependencies
    status: completed
  - id: create-document-config
    content: Create DocumentConfig dataclass with fonts, watermark, redaction_style, header/footer configuration
    status: completed
  - id: create-content-blocks
    content: Create content block classes (SectionHeader, TextBlock, KeyValueBlock, LogBlock, WarningBlock, SignatureBlock)
    status: completed
  - id: create-document-engine
    content: Create DocumentEngine class with fluent API (add(), set_redactions(), render())
    status: completed
  - id: implement-redaction-engine
    content: Implement automatic redaction engine that scans content blocks for sensitive terms
    status: completed
  - id: implement-redaction-styles
    content: Implement multiple redaction styles (BLACK_BAR, BLUR, CROSS_OUT) via enum
    status: completed
  - id: implement-renderer
    content: Implement render() method that processes content blocks and generates PDF
    status: completed
  - id: create-teleport-use-case
    content: Create example use case demonstrating Teleport Massive dossier generation
    status: completed
  - id: test-pdf-generation
    content: Test PDF generation with various content block combinations
    status: pending
  - id: verify-redaction
    content: Verify redacted text is selectable under black bars and automatic term detection works
    status: pending

category: hopes
confidence: 0.63
constellation_date: 2026-01-14
---

# Implementation Plan: DocumentEngine - Research Documentation Library

## Overview

Create `DocumentEngine` class in `src/waft/foundation.py` as a **reusable, content-agnostic Research Documentation Library** that generates stylized PDF documentation. The engine uses modular content blocks, configurable styling, and automatic redaction capabilities. The "Teleport Massive" art project becomes the **first use case**, demonstrating the engine's capabilities for SCP/Dossier-style documentation.

## Technical Decisions

### PDF Library: fpdf2

**Choice**: Use `fpdf2` (not `weasyprint`)

**Rationale**:

- Better programmatic control for precise layout
- Simpler API for typewriter aesthetic
- Good font embedding support (Courier/Courier Prime)
- Better suited for text-based redaction logic
- Lighter weight than weasyprint

**Dependency**: Add `fpdf2>=2.7.0` to `pyproject.toml`

### Architecture: Modular Content Blocks

**Approach**: Content-agnostic engine with pluggable content blocks

**Rationale**:

- Separates content from rendering logic
- Enables reuse across different document types (scientific logs, legal audits, journalism)
- Allows dynamic document building via fluent API
- Makes testing easier (test blocks independently)

### Redaction Implementation

**Approach**: First-class redaction engine with multiple styles

**Styles Supported**:

- `BLACK_BAR`: Non-destructive black bars with selectable text underneath (default)
- `BLUR`: Text blurred (if PDF supports, otherwise falls back to BLACK_BAR)
- `CROSS_OUT`: Text crossed out with lines

**Method for BLACK_BAR**:

- Draw text in white (invisible) to keep it in PDF content stream (selectable)
- Draw black rectangle over the text position (visual redaction)
- Text remains in PDF but visually obscured

**Automatic Detection**: Engine scans all content blocks for `sensitive_terms` and automatically redacts them.

## File Structure

```
src/waft/
└── foundation.py          # New file: DocumentEngine + content blocks + config
```

## Implementation Details

### 1. DocumentConfig (Dataclass)

**Location**: `src/waft/foundation.py`

**Purpose**: Configuration object for document styling and behavior

**Fields**:

```python
@dataclass
class DocumentConfig:
    fonts: Dict[str, str]  # {"Header": "Courier-Bold", "Body": "Courier", "Monospace": "Courier"}
    watermark: Optional[str] = None  # "DRAFT", "CONFIDENTIAL", "TOP SECRET"
    redaction_style: RedactionStyle = RedactionStyle.BLACK_BAR
    header_text: Optional[str] = None  # "SITE-DELTA-9 // BIO-LOG"
    footer_text: Optional[str] = None  # "INTERNAL USE ONLY"
    page_margins: Tuple[float, float, float, float] = (72, 72, 72, 72)  # top, right, bottom, left
    line_spacing: float = 1.5
```

**Preset Configs**:

- `DocumentConfig.classified_dossier()`: Returns pre-configured config for SCP/Dossier style
- `DocumentConfig.scientific_log()`: Returns config for scientific documentation
- `DocumentConfig.legal_audit()`: Returns config for legal documentation

### 2. RedactionStyle (Enum)

**Location**: `src/waft/foundation.py`

```python
from enum import Enum

class RedactionStyle(Enum):
    BLACK_BAR = "black_bar"
    BLUR = "blur"
    CROSS_OUT = "cross_out"
```

### 3. Content Block Classes

**Location**: `src/waft/foundation.py`

All blocks inherit from base `ContentBlock` ABC with `render(pdf, config, redaction_engine)` method.

**A. SectionHeader**

```python
class SectionHeader(ContentBlock):
    def __init__(self, title: str, level: int = 1):
        self.title = title
        self.level = level  # 1-3 for different header sizes
```

**B. TextBlock**

```python
class TextBlock(ContentBlock):
    def __init__(self, content: str, style: str = "Body"):
        self.content = content
        self.style = style  # "Body", "Monospace", "Italic"
```

**C. KeyValueBlock**

```python
class KeyValueBlock(ContentBlock):
    def __init__(self, data: Dict[str, str], label: Optional[str] = None):
        self.data = data  # {"Subject": "Specimen-D", "Genome": "001-ALPHA"}
        self.label = label  # Optional section label like "Metadata"
```

**D. LogBlock**

```python
class LogBlock(ContentBlock):
    def __init__(self, entries: List[str], timestamp_format: Optional[str] = None):
        self.entries = entries  # ["[09:04:01] INITIATING...", "[09:04:05] MEMORY LEAK..."]
        self.timestamp_format = timestamp_format  # Optional format string
```

**E. WarningBlock**

```python
class WarningBlock(ContentBlock):
    def __init__(self, text: str, severity: str = "WARNING"):
        self.text = text
        self.severity = severity  # "WARNING", "CAUTION", "CRITICAL"
```

**F. SignatureBlock**

```python
class SignatureBlock(ContentBlock):
    def __init__(self, role: str, name: str, timestamp: Optional[datetime] = None):
        self.role = role  # "AUTHORIZED BY"
        self.name = name  # "[ARCHETYPE: THE STATIC]"
        self.timestamp = timestamp or datetime.now()
```

### 4. DocumentEngine (Main Class)

**Location**: `src/waft/foundation.py`

**Dependencies**:

- `fpdf2` library
- `dataclasses` for DocumentConfig
- `enum` for RedactionStyle
- `Path` from `pathlib`
- `datetime` for timestamps
- `typing` for type hints

**Key Methods**:

1. `__init__(self, config: DocumentConfig)`

   - Initialize with DocumentConfig
   - Create empty content blocks list
   - Initialize redaction engine with empty sensitive_terms list

2. `add(self, block: ContentBlock) -> DocumentEngine`

   - Add content block to document
   - Returns self for fluent API chaining

3. `set_redactions(self, sensitive_terms: List[str]) -> DocumentEngine`

   - Set list of terms to automatically redact
   - Returns self for fluent API chaining

4. `render(self, output_path: Path) -> Path`

   - Process all content blocks
   - Apply automatic redaction to all blocks
   - Generate PDF with headers/footers/watermarks
   - Return path to generated PDF

5. `_apply_redaction(self, text: str, pdf, x: float, y: float) -> None`

   - Internal method to apply redaction based on config.redaction_style
   - Handles BLACK_BAR, BLUR, CROSS_OUT styles

6. `_render_block(self, block: ContentBlock, pdf, config: DocumentConfig) -> None`

   - Internal method to render individual content block
   - Calls block.render() with pdf, config, and redaction engine

7. `_add_header_footer(self, pdf, page_num: int, total_pages: int, config: DocumentConfig) -> None`

   - Add headers/footers based on config.header_text and config.footer_text
   - Add page numbers

8. `_add_watermark(self, pdf, config: DocumentConfig) -> None`

   - Add watermark if config.watermark is set
   - Rotate and position watermark appropriately

### Page Layout Specifications

**Page 1 - Cover**:

- Large, bold title: "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES"
- Subtitle: "FIELD OPERATIONS DIVISION"
- Property line: "PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9"
- Operational details in structured format
- Warning block with border
- Footer: "AUTHORIZED BY: ⚲ [ARCHETYPE: THE STATIC]"
- Stamp: "INTERNAL USE ONLY"

**Page 2 - Protocol-991**:

- Header: "[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK"
- Four sections (I-IV) with roman numerals
- Redacted sections using `redact()` method
- Footer: "OFFICIAL STAMP: [ ⚲ THE STATIC - AUTHORIZED ]"
- Date: "JANUARY 09, 2026"

**Page 3 - Final Summary**:

- Header: "FOUNDATION FINAL SUMMARY: SESSION-014-RECURSION"
- Three sections (I-III) with roman numerals
- Redacted phrase in section II
- Final warning block
- Checksum at bottom

### Styling Requirements

**Fonts**:

- Primary: Courier or Courier Prime (monospaced)
- Sizes: 12pt body, 14pt headers, 10pt footers, 8pt stamps

**Colors**:

- Black text on white background
- Red for stamps/warnings (optional, or keep black for typewriter aesthetic)
- White text for redacted content (invisible but selectable)
- Black rectangles for redaction bars

**Layout**:

- Margins: 1 inch (72 points) all sides
- Line spacing: 1.5x for body text
- Page size: US Letter (8.5" x 11")
- High resolution: 300 DPI equivalent (fpdf2 default is 72 DPI, but we can scale)

### Redaction Engine Details

**Automatic Redaction Process**:

1. **Term Detection**: Engine scans all content blocks for `sensitive_terms`
2. **Position Calculation**: For each match, calculate text position in PDF
3. **Style Application**: Apply redaction based on `config.redaction_style`

**Implementation for BLACK_BAR**:

```python
def _apply_redaction_black_bar(self, pdf, text: str, x: float, y: float, width: float, height: float):
    # Save current color
    current_color = pdf.get_text_color()

    # Draw text in white (invisible but in PDF content stream)
    pdf.set_text_color(255, 255, 255)  # White
    pdf.text(x, y, text)

    # Draw black rectangle over text
    pdf.set_fill_color(0, 0, 0)  # Black
    pdf.rect(x, y - height, width, height, style='F')  # Filled rectangle

    # Restore color
    pdf.set_text_color(*current_color)
```

**Implementation for CROSS_OUT**:

```python
def _apply_redaction_cross_out(self, pdf, text: str, x: float, y: float, width: float, height: float):
    # Draw text normally
    pdf.text(x, y, text)

    # Draw diagonal lines across text
    pdf.line(x, y, x + width, y - height)
    pdf.line(x, y - height, x + width, y)
```

**Usage**:

- Set terms via `doc.set_redactions(["term1", "term2"])`
- Engine automatically redacts all occurrences in all content blocks
- Manual redaction also possible by marking text in content blocks

## Output

**Primary Output**: Generated PDF files (path specified in `render()` call)

**Example**: `_work_efforts/WAFT_DOSSIER_014.pdf` (from Teleport Massive use case)

**Features**:

- High-resolution PDF suitable for print
- Modular content blocks rendered in order
- Automatic redaction of sensitive terms
- Headers/footers based on config
- Watermarks if configured
- Stamps and authentication marks via SignatureBlock

## Dependencies to Add

**pyproject.toml**:

```toml
dependencies = [
    # ... existing dependencies ...
    "fpdf2>=2.7.0",
]
```

## Testing Considerations

1. Verify PDF generates successfully
2. Verify redacted text is selectable (copy/paste test)
3. Verify fonts render correctly (Courier/Courier Prime)
4. Verify page layout matches specifications
5. Verify headers/footers appear on all pages
6. Verify stamps render correctly

## Integration Points

**Content-Agnostic Design**:

- Engine does NOT depend on TheObserver or TavernKeeper
- Users provide content via content blocks
- Enables use cases: scientific logs, legal audits, journalism, art projects

**Helper Functions (Optional)**:

- `generate_from_observer_log(observer: TheObserver, config: DocumentConfig) -> DocumentEngine`
  - Converts Observer logs to LogBlock and KeyValueBlock content
  - Returns DocumentEngine instance ready to render

- `generate_from_tavern_narrative(tavern_keeper: TavernKeeper, config: DocumentConfig) -> DocumentEngine`
  - Converts TavernKeeper chronicles to TextBlock content
  - Returns DocumentEngine instance ready to render

**Future Extensions**:

- Additional content block types (TableBlock, ImageBlock, CodeBlock)
- Template system for common document structures
- Export to other formats (HTML, Markdown)
- Batch processing for multiple documents
- Custom redaction patterns (regex-based)

## File Changes

1. **Create**: `src/waft/foundation.py` (new file, ~800-1000 lines)

   - DocumentConfig dataclass
   - RedactionStyle enum
   - ContentBlock ABC and 6 concrete block classes
   - DocumentEngine main class
   - Helper function `generate_teleport_dossier()` for first use case

2. **Update**: `pyproject.toml` (add fpdf2 dependency)

3. **Output**: `_work_efforts/WAFT_DOSSIER_014.pdf` (generated file from use case)

## Execution Steps

1. Add `fpdf2>=2.7.0` to `pyproject.toml` dependencies

2. Create `src/waft/foundation.py` with base structure:

   - Import statements (fpdf2, dataclasses, enum, typing, pathlib, datetime)
   - RedactionStyle enum
   - DocumentConfig dataclass with preset methods

3. Create ContentBlock ABC:

   - Abstract `render(pdf, config, redaction_engine)` method
   - Base class for all content blocks

4. Implement 6 content block classes:

   - SectionHeader
   - TextBlock
   - KeyValueBlock
   - LogBlock
   - WarningBlock
   - SignatureBlock

5. Implement DocumentEngine class:

   - `__init__(config)`
   - `add(block)` - fluent API
   - `set_redactions(terms)` - fluent API
   - `render(output_path)` - main rendering method
   - `_apply_redaction()` - redaction engine
   - `_render_block()` - block renderer
   - `_add_header_footer()` - page headers/footers
   - `_add_watermark()` - watermark rendering

6. Implement redaction styles:

   - BLACK_BAR (default, non-destructive)
   - CROSS_OUT (diagonal lines)
   - BLUR (placeholder, falls back to BLACK_BAR)

7. Create helper function `generate_teleport_dossier()`:

   - Uses DocumentEngine to build the 3-page dossier
   - Demonstrates all content block types
   - Outputs to `_work_efforts/WAFT_DOSSIER_014.pdf`

8. Test PDF generation:

   - Test with various content block combinations
   - Test automatic redaction
   - Test different redaction styles
   - Test fluent API chaining

9. Verify functionality:

   - Redacted text is selectable under black bars
   - All content blocks render correctly
   - Headers/footers appear on all pages
   - Watermarks render correctly
   - Teleport Massive dossier matches original requirements

## Architecture Benefits

**Content-Agnostic**: Engine doesn't know or care about "Teleport Massive" - it's just content blocks

**Reusable**: Can generate scientific logs, legal audits, journalism documents, or any structured PDF

**Extensible**: Easy to add new content block types or redaction styles

**Testable**: Each component (blocks, engine, config) can be tested independently

**Fluent API**: Clean, chainable interface for building documents programmatically

## Additional Requirements

### Migration Task

- Rewrite the generation logic for `WAFT_SPECIMEN_D_AUDIT.pdf` (or similar story artifacts) to use the new generic API
- Replace any hardcoded FPDF calls with content blocks and DocumentEngine
- Ensure the output matches the original requirements (3-page dossier with exact text)

### Portability Constraints

- Code must be clean enough to copy `foundation.py` into a totally different project (e.g., legal audit tool) and work immediately
- No dependencies on WAFT-specific code (TheObserver, TavernKeeper) in the core engine
- All WAFT-specific functionality should be in helper functions, not core classes
- Configuration-driven styling (typewriter/terminal aesthetic via DocumentConfig, not hardcoded)

### Technical Constraints

- Keep using fpdf2 (no library changes)
- Ensure non-destructive redaction (text selectable under black bars)
- Preserve typewriter/terminal aesthetic via configuration
- High-resolution output suitable for print

## Notes

- Engine is content-agnostic - "Teleport Massive" is just the first use case
- Redaction must be non-destructive (text selectable under black bars)
- Follow typewriter aesthetic (monospaced fonts, structured layout) via DocumentConfig
- Support multiple redaction styles for different use cases
- Preset configs make common use cases easy (classified_dossier, scientific_log, legal_audit)
- Code must be portable - no WAFT-specific dependencies in core engine
- All story artifacts should use the generic API, not hardcoded FPDF calls