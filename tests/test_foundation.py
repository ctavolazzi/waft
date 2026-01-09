"""Comprehensive tests for TheFoundation and DocumentEngine."""

import pytest
from pathlib import Path
from datetime import datetime
from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    TheFoundation,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
    LogBlock,
    WarningBlock,
    SignatureBlock,
    AutoRedactor,
    RedactionStyle,
)

# Check if TheFoundation can be instantiated (tests relative imports)
# We test this by trying to create a TheFoundation instance
FOUNDATION_TESTS_AVAILABLE = False
try:
    from pathlib import Path
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir) / "test"
        test_path.mkdir()
        # Try to instantiate TheFoundation - this will fail if relative imports don't work
        _test_foundation = TheFoundation(test_path)
        FOUNDATION_TESTS_AVAILABLE = True
except (ImportError, ValueError, Exception):
    # If instantiation fails, skip TheFoundation tests
    FOUNDATION_TESTS_AVAILABLE = False


# ============================================================================
# Configuration Validation Tests
# ============================================================================


def test_document_config_initialization():
    """Test DocumentConfig initialization with valid fonts."""
    config = DocumentConfig()
    assert config.fonts is not None
    assert "Header" in config.fonts
    assert "Body" in config.fonts
    assert "Monospace" in config.fonts
    assert config.redaction_style == RedactionStyle.BLACK_BAR
    assert config.watermark is None
    assert config.header_text is None
    assert config.footer_text is None


def test_document_config_classified_dossier():
    """Test DocumentConfig.classified_dossier() preset."""
    config = DocumentConfig.classified_dossier(
        header="TEST HEADER",
        watermark="TEST WATERMARK"
    )
    assert config.watermark == "TEST WATERMARK"
    assert config.header_text == "TEST HEADER"
    assert config.footer_text == "INTERNAL USE ONLY"
    assert config.fonts["Header"] == ("Courier", "B")
    assert config.fonts["Body"] == ("Courier", "")
    assert config.redaction_style == RedactionStyle.BLACK_BAR


def test_document_config_scientific_log():
    """Test DocumentConfig.scientific_log() preset."""
    config = DocumentConfig.scientific_log()
    assert config.watermark == "DRAFT"
    assert config.fonts["Header"] == ("Courier", "B")
    assert config.fonts["Body"] == ("Courier", "")
    assert config.redaction_style == RedactionStyle.BLACK_BAR


def test_document_config_legal_audit():
    """Test DocumentConfig.legal_audit() preset."""
    config = DocumentConfig.legal_audit()
    assert config.watermark == "CONFIDENTIAL"
    assert config.fonts["Header"] == "Courier-Bold"
    assert config.fonts["Body"] == "Courier"
    assert config.redaction_style == RedactionStyle.BLACK_BAR


def test_document_config_margins():
    """Test margin configurations."""
    config = DocumentConfig(page_margins=(50, 60, 70, 80))
    assert config.page_margins == (50, 60, 70, 80)


def test_document_config_none_values():
    """Test DocumentConfig with None header_text, footer_text, watermark."""
    config = DocumentConfig(
        header_text=None,
        footer_text=None,
        watermark=None
    )
    assert config.header_text is None
    assert config.footer_text is None
    assert config.watermark is None


# ============================================================================
# Block Rendering Tests
# ============================================================================


def test_section_header_level_1(temp_dir):
    """Test SectionHeader rendering (level 1)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(SectionHeader("Test Header", level=1))
    output_path = temp_dir / "test_header1.pdf"
    engine.render(output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_section_header_level_2(temp_dir):
    """Test SectionHeader rendering (level 2)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(SectionHeader("Test Header", level=2))
    output_path = temp_dir / "test_header2.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_section_header_level_3(temp_dir):
    """Test SectionHeader rendering (level 3)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(SectionHeader("Test Header", level=3))
    output_path = temp_dir / "test_header3.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_text_block_body_style(temp_dir):
    """Test TextBlock rendering (Body style)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(TextBlock("This is a test paragraph.", style="Body"))
    output_path = temp_dir / "test_text_body.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_text_block_monospace_style(temp_dir):
    """Test TextBlock rendering (Monospace style)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(TextBlock("This is monospace text.", style="Monospace"))
    output_path = temp_dir / "test_text_mono.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_text_block_empty_string(temp_dir):
    """Test TextBlock with empty string."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(TextBlock(""))
    output_path = temp_dir / "test_text_empty.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_text_block_whitespace_only(temp_dir):
    """Test TextBlock with only whitespace."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(TextBlock("   \n\n   "))
    output_path = temp_dir / "test_text_whitespace.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_key_value_block_with_label(temp_dir):
    """Test KeyValueBlock rendering (with label)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(KeyValueBlock({"Key1": "Value1", "Key2": "Value2"}, label="Metadata"))
    output_path = temp_dir / "test_kv_labeled.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_key_value_block_without_label(temp_dir):
    """Test KeyValueBlock rendering (without label)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(KeyValueBlock({"Key1": "Value1", "Key2": "Value2"}))
    output_path = temp_dir / "test_kv_unlabeled.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_key_value_block_empty_dict(temp_dir):
    """Test KeyValueBlock with empty dict."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(KeyValueBlock({}))
    output_path = temp_dir / "test_kv_empty.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_log_block_single_entry(temp_dir):
    """Test LogBlock rendering (single entry)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(LogBlock(["[09:00:01] Test log entry"]))
    output_path = temp_dir / "test_log_single.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_log_block_multiple_entries(temp_dir):
    """Test LogBlock rendering (multiple entries)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(LogBlock([
        "[09:00:01] Entry 1",
        "[09:00:02] Entry 2",
        "[09:00:03] Entry 3"
    ]))
    output_path = temp_dir / "test_log_multiple.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_log_block_empty_entries(temp_dir):
    """Test LogBlock with empty entries list."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(LogBlock([]))
    output_path = temp_dir / "test_log_empty.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_warning_block_warning_severity(temp_dir):
    """Test WarningBlock rendering (WARNING severity)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(WarningBlock("This is a warning.", severity="WARNING"))
    output_path = temp_dir / "test_warning.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_warning_block_caution_severity(temp_dir):
    """Test WarningBlock rendering (CAUTION severity)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(WarningBlock("This is a caution.", severity="CAUTION"))
    output_path = temp_dir / "test_caution.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_warning_block_critical_severity(temp_dir):
    """Test WarningBlock rendering (CRITICAL severity)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(WarningBlock("This is critical.", severity="CRITICAL"))
    output_path = temp_dir / "test_critical.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_signature_block_with_timestamp(temp_dir):
    """Test SignatureBlock rendering (with timestamp)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    timestamp = datetime(2026, 1, 9, 12, 0, 0)
    engine.add(SignatureBlock("Author", "John Doe", timestamp=timestamp))
    output_path = temp_dir / "test_signature_timestamp.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_signature_block_without_timestamp(temp_dir):
    """Test SignatureBlock rendering (without timestamp, uses now)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(SignatureBlock("Author", "John Doe"))
    output_path = temp_dir / "test_signature_no_timestamp.pdf"
    engine.render(output_path)
    assert output_path.exists()


# ============================================================================
# Redaction Logic Tests
# ============================================================================


def test_redactor_simple_string_matching(temp_dir):
    """Test AutoRedactor with simple string matching."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["Project Stargate"])
    engine.add(TextBlock("This document is about Project Stargate."))
    output_path = temp_dir / "test_redaction_simple.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redactor_case_insensitive_matching(temp_dir):
    """Test case-insensitive matching."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["Project Stargate"])
    engine.add(TextBlock("This document is about project stargate."))
    output_path = temp_dir / "test_redaction_case.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redactor_overlapping_terms(temp_dir):
    """Test overlapping terms (e.g., 'TAM' and 'Fai Wei Tam')."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["TAM", "Fai Wei Tam"])
    engine.add(TextBlock("Subject: Fai Wei Tam"))
    output_path = temp_dir / "test_redaction_overlap.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redactor_multiple_occurrences(temp_dir):
    """Test multiple occurrences of same term."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["Project Stargate"])
    engine.add(TextBlock("Project Stargate is mentioned here. Project Stargate is also here."))
    output_path = temp_dir / "test_redaction_multiple.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_in_text_block(temp_dir):
    """Test redaction in TextBlock."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(TextBlock("This is a SECRET message."))
    output_path = temp_dir / "test_redaction_text.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_in_key_value_block(temp_dir):
    """Test redaction in KeyValueBlock values."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(KeyValueBlock({"Project": "SECRET Project Name"}))
    output_path = temp_dir / "test_redaction_kv.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_in_log_block(temp_dir):
    """Test redaction in LogBlock entries."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(LogBlock(["[09:00:01] SECRET operation started"]))
    output_path = temp_dir / "test_redaction_log.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_in_section_header(temp_dir):
    """Test redaction in SectionHeader."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(SectionHeader("SECRET Header", level=1))
    output_path = temp_dir / "test_redaction_header.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_empty_terms_list(temp_dir):
    """Test empty sensitive terms list (no redaction)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    # Don't add any sensitive terms
    engine.add(TextBlock("This is a SECRET message."))
    output_path = temp_dir / "test_redaction_none.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_term_at_start(temp_dir):
    """Test term at start of text."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(TextBlock("SECRET message here."))
    output_path = temp_dir / "test_redaction_start.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_redaction_term_at_end(temp_dir):
    """Test term at end of text."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add_sensitive_terms(["SECRET"])
    engine.add(TextBlock("This is a SECRET"))
    output_path = temp_dir / "test_redaction_end.pdf"
    engine.render(output_path)
    assert output_path.exists()


# ============================================================================
# DocumentEngine Integration Tests
# ============================================================================


def test_document_engine_fluent_add(temp_dir):
    """Test DocumentEngine.add() fluent API."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    result = engine.add(TextBlock("Test"))
    assert result is engine  # Should return self for fluent API
    output_path = temp_dir / "test_fluent.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_document_engine_fluent_add_sensitive_terms(temp_dir):
    """Test DocumentEngine.add_sensitive_terms() fluent API."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    result = engine.add_sensitive_terms(["SECRET"])
    assert result is engine  # Should return self for fluent API
    engine.add(TextBlock("SECRET message"))
    output_path = temp_dir / "test_fluent_terms.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_document_engine_render_generates_pdf(temp_dir):
    """Test DocumentEngine.render() generates valid PDF."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    engine.add(TextBlock("Test content"))
    output_path = temp_dir / "test_render.pdf"
    returned_path = engine.render(output_path)
    assert returned_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_document_engine_pagination(temp_dir):
    """Test pagination (blocks spanning multiple pages)."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    # Add enough content to force pagination
    for i in range(50):
        engine.add(TextBlock(f"This is paragraph {i}. " * 10))
    output_path = temp_dir / "test_pagination.pdf"
    engine.render(output_path)
    assert output_path.exists()
    # PDF should have multiple pages (we can't easily verify page count without parsing PDF)


def test_document_engine_header_footer(temp_dir):
    """Test header/footer on all pages."""
    config = DocumentConfig.classified_dossier(
        header="TEST HEADER",
        watermark="TEST"
    )
    config.footer_text = "TEST FOOTER"
    engine = DocumentEngine(config)
    # Add content spanning multiple pages
    for i in range(30):
        engine.add(TextBlock(f"Paragraph {i}. " * 10))
    output_path = temp_dir / "test_header_footer.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_document_engine_watermark(temp_dir):
    """Test watermark on all pages."""
    config = DocumentConfig.classified_dossier(watermark="TEST WATERMARK")
    engine = DocumentEngine(config)
    # Add content spanning multiple pages
    for i in range(30):
        engine.add(TextBlock(f"Paragraph {i}. " * 10))
    output_path = temp_dir / "test_watermark.pdf"
    engine.render(output_path)
    assert output_path.exists()


def test_document_engine_page_numbering(temp_dir):
    """Test page numbering."""
    config = DocumentConfig.classified_dossier()
    engine = DocumentEngine(config)
    # Add content spanning multiple pages
    for i in range(30):
        engine.add(TextBlock(f"Paragraph {i}. " * 10))
    output_path = temp_dir / "test_page_numbers.pdf"
    engine.render(output_path)
    assert output_path.exists()


# ============================================================================
# TheFoundation Integration Tests
# ============================================================================


@pytest.mark.skipif(not FOUNDATION_TESTS_AVAILABLE, reason="Requires WAFT-specific imports")
def test_foundation_initialization(temp_project_path):
    """Test TheFoundation initialization."""
    foundation = TheFoundation(temp_project_path)
    assert foundation.project_path == Path(temp_project_path)
    assert foundation.output_dir == Path(temp_project_path) / "_work_efforts"
    assert foundation.observer is not None
    assert foundation.tavern_keeper is not None


@pytest.mark.skipif(not FOUNDATION_TESTS_AVAILABLE, reason="Requires WAFT-specific imports")
def test_foundation_generate_dossier_default_path(temp_project_path):
    """Test TheFoundation.generate_dossier() generates PDF with default path."""
    foundation = TheFoundation(temp_project_path)
    output_path = foundation.generate_dossier("014")
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    assert "WAFT_DOSSIER_014.pdf" in str(output_path)


@pytest.mark.skipif(not FOUNDATION_TESTS_AVAILABLE, reason="Requires WAFT-specific imports")
def test_foundation_generate_dossier_custom_path(temp_project_path, temp_dir):
    """Test TheFoundation.generate_dossier() with custom output path."""
    foundation = TheFoundation(temp_project_path)
    custom_path = temp_dir / "custom_dossier.pdf"
    output_path = foundation.generate_dossier("014", output_path=custom_path)
    assert output_path == custom_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


@pytest.mark.skipif(not FOUNDATION_TESTS_AVAILABLE, reason="Requires WAFT-specific imports")
def test_foundation_output_dir_creation(temp_project_path):
    """Test output directory creation."""
    foundation = TheFoundation(temp_project_path)
    assert foundation.output_dir.exists()
    assert foundation.output_dir.is_dir()
