---
name: Foundation Stress Test & Calibration
overview: Create comprehensive unit tests for TheFoundation/DocumentEngine and a calibration artifact script that generates a stress-test PDF to verify visual integrity, redaction correctness, and pagination stability.
todos:
  - id: test-suite
    content: Create tests/test_foundation.py with comprehensive unit tests for DocumentConfig, all block types, redaction logic, empty/null states, and integration tests
    status: completed
  - id: calibration-script
    content: Create src/waft/verify_foundation.py that generates WAFT_CALIBRATION_REPORT.pdf with kitchen sink page, redaction torture test, pagination stress test, and selectability verification
    status: completed
  - id: run-tests
    content: Execute pytest tests/test_foundation.py -v to verify all tests pass
    status: completed
  - id: run-calibration
    content: Execute python src/waft/verify_foundation.py to generate calibration PDF and verify output
    status: completed

category: dreams
confidence: 0.62
constellation_date: 2026-01-14
---

# Foundation Stress Test & Calibration Plan

## Overview
Create comprehensive testing infrastructure to verify TheFoundation and DocumentEngine reliability through unit tests and visual calibration artifacts.

## Task A: Unit Test Suite (`tests/test_foundation.py`)

### Test Structure
Create pytest test suite covering:

1. **Configuration Validation Tests**
   - Test `DocumentConfig` initialization with valid fonts
   - Test `DocumentConfig.classified_dossier()` preset
   - Test `DocumentConfig.scientific_log()` preset
   - Test `DocumentConfig.legal_audit()` preset
   - Test invalid font configurations (if validation exists)
   - Test margin configurations
   - Test watermark and header/footer text

2. **Block Rendering Tests**
   - Test `SectionHeader` rendering (levels 1, 2, 3)
   - Test `TextBlock` rendering (Body, Monospace styles)
   - Test `KeyValueBlock` rendering (with and without label)
   - Test `LogBlock` rendering (empty, single entry, multiple entries)
   - Test `WarningBlock` rendering (WARNING, CAUTION, CRITICAL severities)
   - Test `SignatureBlock` rendering (with and without timestamp)
   - Test empty `TextBlock` (whitespace-only content)
   - Test `None` header_text in config

3. **Redaction Logic Tests**
   - Test `AutoRedactor` with simple string matching
   - Test case-insensitive matching ("Project Stargate" vs "project stargate")
   - Test overlapping terms (e.g., "TAM" and "Fai Wei Tam")
   - Test multiple occurrences of same term
   - Test redaction in `TextBlock`
   - Test redaction in `KeyValueBlock` values
   - Test redaction in `LogBlock` entries
   - Test redaction in `SectionHeader`
   - Test empty sensitive terms list (no redaction)
   - Test term at start/end of text
   - Test term spanning word boundaries

4. **Empty/Null State Tests**
   - Test empty `LogBlock` entries list
   - Test `TextBlock` with empty string
   - Test `TextBlock` with only whitespace
   - Test `KeyValueBlock` with empty dict
   - Test `DocumentConfig` with `None` header_text
   - Test `DocumentConfig` with `None` footer_text
   - Test `DocumentConfig` with `None` watermark

5. **DocumentEngine Integration Tests**
   - Test `DocumentEngine.add()` fluent API
   - Test `DocumentEngine.add_sensitive_terms()` fluent API
   - Test `DocumentEngine.render()` generates valid PDF
   - Test pagination (blocks spanning multiple pages)
   - Test header/footer on all pages
   - Test watermark on all pages
   - Test page numbering

6. **TheFoundation Integration Tests**
   - Test `TheFoundation` initialization
   - Test `TheFoundation.generate_dossier()` generates PDF
   - Test output path creation
   - Test default vs custom output paths

### Test Implementation Details
- Use `temp_dir` fixture from `conftest.py` for PDF output
- Use `pytest.raises()` for validation error tests
- Verify PDF files are created and non-empty
- Use `Path.exists()` and `Path.stat().st_size` for file validation
- Mock FPDF if needed for isolated unit tests (optional)

## Task B: Calibration Artifact Script (`src/waft/verify_foundation.py`)

### Script Purpose
Generate `WAFT_CALIBRATION_REPORT.pdf` that stress-tests all visual and functional aspects.

### Content Requirements

1. **Kitchen Sink Page (Page 1)**
   - Include every block type on single page:
     - `SectionHeader` (level 1)
     - `SectionHeader` (level 2)
     - `SectionHeader` (level 3)
     - `TextBlock` (Body style)
     - `TextBlock` (Monospace style)
     - `KeyValueBlock` (with label)
     - `KeyValueBlock` (without label)
     - `LogBlock` (multiple entries)
     - `WarningBlock` (WARNING severity)
     - `WarningBlock` (CAUTION severity)
     - `WarningBlock` (CRITICAL severity)
     - `SignatureBlock` (with timestamp)
   - Add instruction: "SELECT THIS TEXT TO VERIFY REDACTION -> [TOP SECRET PASSWORD]"
     - Where "TOP SECRET PASSWORD" is a sensitive term that should be redacted but selectable

2. **Redaction Torture Test (Page 2)**
   - Text block containing "Project Stargate" exactly 50 times
   - Text block with sensitive term at end of line (to test line break handling)
   - `KeyValueBlock` with sensitive term in value:
     - Key: "CLASSIFIED PROJECT"
     - Value: "Project Stargate is the codename for..."
   - `LogBlock` with entries containing sensitive terms:
     - "[09:00:01] Initializing Project Stargate protocol"
     - "[09:00:02] Project Stargate status: ACTIVE"
     - etc.
   - Test overlapping terms: Add both "Project Stargate" and "Stargate" as sensitive terms

3. **Pagination Stress Test (Page 3+)**
   - `LogBlock` with exactly 100 entries
   - Each entry formatted: `"[HH:MM:SS] Entry N: [content]"`
   - Verify headers/footers persist across page breaks
   - Verify margins are consistent
   - Verify watermark appears on all pages

4. **Selectability Verification**
   - On Page 1, include explicit instruction:
     - "VERIFICATION: Select the redacted text below. The text '[TOP SECRET PASSWORD]' should be selectable (white text) even though it appears black."
   - Include a `TextBlock` with: "Password: [TOP SECRET PASSWORD]"
   - Add "TOP SECRET PASSWORD" to sensitive terms

### Script Implementation
- Use `DocumentConfig.classified_dossier()` for styling
- Set sensitive terms: `["Project Stargate", "Stargate", "TOP SECRET PASSWORD"]`
- Generate PDF to `_work_efforts/WAFT_CALIBRATION_REPORT.pdf`
- Print success message with file path and size
- Handle errors gracefully with clear messages

### Script Structure
```python
def generate_calibration_report(output_path: Optional[Path] = None) -> Path:
    """Generate comprehensive calibration PDF."""
    # Setup config and engine
    # Add all test content
    # Render PDF
    # Return path
```

## File Locations
- **Unit Tests**: `tests/test_foundation.py`
- **Calibration Script**: `src/waft/verify_foundation.py`

## Execution Commands
1. Run unit tests: `pytest tests/test_foundation.py -v`
2. Run calibration script: `python src/waft/verify_foundation.py`

## Expected Outputs
- Test results: pytest output showing all tests passing
- Calibration PDF: `_work_efforts/WAFT_CALIBRATION_REPORT.pdf` (multi-page PDF)

## Dependencies
- `pytest` (already in project)
- `fpdf2` (already used by foundation.py)
- Standard library: `Path`, `tempfile`, `datetime`