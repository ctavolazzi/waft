"""
Calibration Artifact Generator for TheFoundation/DocumentEngine.

Generates WAFT_CALIBRATION_REPORT.pdf that stress-tests all visual and functional
aspects of the PDF generation system, including redaction, pagination, and layout.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
    LogBlock,
    WarningBlock,
    SignatureBlock,
)


def generate_calibration_report(output_path: Optional[Path] = None) -> Path:
    """
    Generate comprehensive calibration PDF.

    Args:
        output_path: Optional output path (defaults to _work_efforts/WAFT_CALIBRATION_REPORT.pdf)

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        # Default to _work_efforts in current directory or project root
        work_efforts_dir = Path("_work_efforts")
        work_efforts_dir.mkdir(parents=True, exist_ok=True)
        output_path = work_efforts_dir / "WAFT_CALIBRATION_REPORT.pdf"

    # Configure for Site-Delta-9 dossier style
    config = DocumentConfig.classified_dossier(
        header="SITE-DELTA-9 // CALIBRATION TEST",
        watermark="CALIBRATION ARTIFACT",
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for automatic redaction
    engine.add_sensitive_terms([
        "Project Stargate",
        "Stargate",  # Overlapping term test
        "TOP SECRET PASSWORD",
    ])

    # ========================================================================
    # PAGE 1: KITCHEN SINK PAGE
    # ========================================================================
    engine.add(SectionHeader("CALIBRATION REPORT: KITCHEN SINK PAGE", level=1))
    engine.add(TextBlock("This page contains every single block type to verify they render correctly."))

    # Section Headers (all levels)
    engine.add(SectionHeader("Level 1 Header", level=1))
    engine.add(SectionHeader("Level 2 Header", level=2))
    engine.add(SectionHeader("Level 3 Header", level=3))

    # Text Blocks (different styles)
    engine.add(TextBlock("This is a Body style text block with normal formatting.", style="Body"))
    engine.add(TextBlock("This is a Monospace style text block for code/logs.", style="Monospace"))

    # KeyValue Blocks (with and without label)
    engine.add(KeyValueBlock(
        {
            "Test Key 1": "Test Value 1",
            "Test Key 2": "Test Value 2",
            "Test Key 3": "Test Value 3",
        },
        label="Metadata Section"
    ))
    engine.add(KeyValueBlock(
        {
            "Unlabeled Key 1": "Unlabeled Value 1",
            "Unlabeled Key 2": "Unlabeled Value 2",
        }
    ))

    # Log Block
    engine.add(LogBlock([
        "[09:00:01] First log entry",
        "[09:00:02] Second log entry",
        "[09:00:03] Third log entry",
        "[09:00:04] Fourth log entry",
    ]))

    # Warning Blocks (all severities)
    engine.add(WarningBlock("This is a WARNING severity block.", severity="WARNING"))
    engine.add(WarningBlock("This is a CAUTION severity block.", severity="CAUTION"))
    engine.add(WarningBlock("This is a CRITICAL severity block.", severity="CRITICAL"))

    # Signature Block
    engine.add(SignatureBlock(
        role="CALIBRATION TESTER",
        name="Test System",
        timestamp=datetime.now()
    ))

    # Selectability Verification Section
    engine.add(SectionHeader("SELECTABILITY VERIFICATION", level=2))
    engine.add(TextBlock(
        "VERIFICATION: Select the redacted text below. The text '[TOP SECRET PASSWORD]' "
        "should be selectable (white text) even though it appears black."
    ))
    engine.add(TextBlock("SELECT THIS TEXT TO VERIFY REDACTION -> [TOP SECRET PASSWORD]"))
    engine.add(TextBlock("Password: [TOP SECRET PASSWORD]"))

    # ========================================================================
    # PAGE 2: REDACTION TORTURE TEST
    # ========================================================================
    engine.add(SectionHeader("REDACTION TORTURE TEST", level=1))

    # Text block with "Project Stargate" exactly 50 times
    stargate_text = "Project Stargate " * 50
    engine.add(TextBlock(
        f"This section contains the sensitive term 'Project Stargate' exactly 50 times: {stargate_text}"
    ))

    # Text block with sensitive term at end of line (to test line break handling)
    engine.add(TextBlock(
        "This is a long line of text that should wrap, and at the end we have Project Stargate. "
        "This tests whether redaction works correctly when terms appear at line boundaries."
    ))

    # KeyValueBlock with sensitive term in value
    engine.add(KeyValueBlock({
        "CLASSIFIED PROJECT": "Project Stargate is the codename for a highly classified operation.",
        "STATUS": "Project Stargate is currently active.",
        "LOCATION": "Project Stargate facility is located at a secure site.",
    }))

    # LogBlock with entries containing sensitive terms
    engine.add(LogBlock([
        "[09:00:01] Initializing Project Stargate protocol",
        "[09:00:02] Project Stargate status: ACTIVE",
        "[09:00:03] Project Stargate systems online",
        "[09:00:04] Project Stargate monitoring enabled",
        "[09:00:05] Project Stargate data collection started",
        "[09:00:06] Project Stargate security check passed",
        "[09:00:07] Project Stargate backup completed",
        "[09:00:08] Project Stargate report generated",
        "[09:00:09] Project Stargate session ended",
        "[09:00:10] Project Stargate logs archived",
    ]))

    # Test overlapping terms
    engine.add(SectionHeader("OVERLAPPING TERMS TEST", level=2))
    engine.add(TextBlock(
        "This tests overlapping sensitive terms. We have 'Project Stargate' and 'Stargate' "
        "both as sensitive terms. The word 'Stargate' appears in 'Project Stargate', so we "
        "need to ensure redaction handles this correctly."
    ))
    engine.add(TextBlock(
        "Standalone Stargate reference. Project Stargate reference. Another Stargate mention."
    ))

    # ========================================================================
    # PAGE 3+: PAGINATION STRESS TEST
    # ========================================================================
    engine.add(SectionHeader("PAGINATION STRESS TEST", level=1))
    engine.add(TextBlock(
        "This section contains a LogBlock with exactly 100 entries to verify that headers, "
        "footers, and margins persist correctly across page breaks."
    ))

    # Generate 100 log entries
    log_entries = []
    for i in range(1, 101):
        hour = 9 + (i // 60)
        minute = i % 60
        second = (i * 3) % 60
        timestamp = f"[{hour:02d}:{minute:02d}:{second:02d}]"
        log_entries.append(f"{timestamp} Entry {i:03d}: This is log entry number {i} for pagination testing")

    engine.add(LogBlock(log_entries))

    # ========================================================================
    # FINAL VERIFICATION SECTION
    # ========================================================================
    engine.add(SectionHeader("FINAL VERIFICATION CHECKLIST", level=1))
    engine.add(TextBlock(
        "Please verify the following:\n\n"
        "1. All block types render correctly on Page 1 (Kitchen Sink)\n"
        "2. Redaction works for all 50 occurrences of 'Project Stargate' on Page 2\n"
        "3. Redaction works in KeyValueBlock values\n"
        "4. Redaction works in LogBlock entries\n"
        "5. Overlapping terms ('Project Stargate' and 'Stargate') are handled correctly\n"
        "6. Headers and footers appear on all pages\n"
        "7. Watermark appears on all pages\n"
        "8. Page numbering is correct\n"
        "9. Margins are consistent across pages\n"
        "10. Redacted text is selectable (white text under black bar)"
    ))

    engine.add(WarningBlock(
        "This is a calibration artifact. Do not use in production without verification.",
        severity="WARNING"
    ))

    engine.add(SignatureBlock(
        role="CALIBRATION SYSTEM",
        name="Automated Test Generator",
        timestamp=datetime.now()
    ))

    # Render PDF
    output_path = engine.render(output_path)
    return output_path


if __name__ == "__main__":
    """Generate calibration report when run as script."""
    try:
        output_path = generate_calibration_report()
        file_size_kb = output_path.stat().st_size / 1024
        print(f"✅ Calibration report generated successfully!")
        print(f"   📄 File: {output_path}")
        print(f"   📊 Size: {file_size_kb:.1f} KB")
        print(f"   ✅ All stress tests included:")
        print(f"      - Kitchen Sink page (all block types)")
        print(f"      - Redaction torture test (50 occurrences)")
        print(f"      - Pagination stress test (100 log entries)")
        print(f"      - Selectability verification")
    except Exception as e:
        print(f"❌ Error generating calibration report: {e}")
        raise
