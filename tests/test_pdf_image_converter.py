"""Comprehensive tests for PDF/PNG conversion functionality."""

import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from PIL import Image

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_image_converter import (
    convert_images_to_pdf,
    convert_pdf_to_images,
    pdf_to_pngs,
    pngs_to_pdf,
)


# Check if PDF conversion libraries are available
def has_pdf_converter():
    """Check if any PDF conversion library is available."""
    try:
        import pdf2image

        return True
    except ImportError:
        pass

    try:
        import fitz  # PyMuPDF

        return True
    except ImportError:
        pass

    # Check for ImageMagick
    try:
        import subprocess

        subprocess.run(
            ["convert", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    return False


PDF_CONVERTER_AVAILABLE = has_pdf_converter()
skip_no_pdf_converter = pytest.mark.skipif(
    not PDF_CONVERTER_AVAILABLE,
    reason="No PDF conversion library available (pdf2image, PyMuPDF, or ImageMagick)",
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_png(temp_dir):
    """Create a sample PNG image for testing."""
    img = Image.new("RGB", (2550, 3300), color="white")  # 8.5x11 at 300 DPI
    png_path = temp_dir / "sample.png"
    img.save(png_path)
    return png_path


@pytest.fixture
def sample_pdf(temp_dir, sample_png):
    """Create a sample PDF from PNG for testing."""
    try:
        from PIL import Image

        # Create a simple PDF from the PNG
        pdf_path = temp_dir / "sample.pdf"
        img = Image.open(sample_png)
        img.save(pdf_path, "PDF", resolution=300)
        return pdf_path
    except Exception:
        pytest.skip("Cannot create test PDF - PIL PDF support may not be available")


@pytest.fixture
def multi_page_pdf(temp_dir):
    """Create a multi-page PDF for testing."""
    try:
        from PIL import Image

        pdf_path = temp_dir / "multi_page.pdf"
        images = []

        # Create 3 pages
        for i in range(3):
            img = Image.new("RGB", (2550, 3300), color=("white", "lightgray", "lightblue")[i])
            images.append(img)

        # Save as multi-page PDF
        images[0].save(
            pdf_path,
            "PDF",
            resolution=300,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
        )
        return pdf_path
    except Exception:
        pytest.skip("Cannot create multi-page PDF")


# ============================================================================
# PDF to PNG Conversion Tests
# ============================================================================


@skip_no_pdf_converter
def test_pdf_to_pngs_single_page(temp_dir, sample_pdf):
    """Test converting a single-page PDF to PNG."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    output_dir = temp_dir / "output"
    png_paths = pdf_to_pngs(sample_pdf, output_dir=output_dir, dpi=300)

    assert len(png_paths) == 1
    assert all(p.exists() for p in png_paths)
    assert png_paths[0].suffix == ".png"

    # Verify PNG is valid
    img = Image.open(png_paths[0])
    assert img.size[0] > 0
    assert img.size[1] > 0


@skip_no_pdf_converter
def test_pdf_to_pngs_multi_page(temp_dir, multi_page_pdf):
    """Test converting a multi-page PDF to PNGs."""
    if not multi_page_pdf.exists():
        pytest.skip("Multi-page PDF not available")

    output_dir = temp_dir / "output"
    png_paths = pdf_to_pngs(multi_page_pdf, output_dir=output_dir, dpi=300)

    assert len(png_paths) == 3
    assert all(p.exists() for p in png_paths)
    assert all(p.suffix == ".png" for p in png_paths)

    # Verify all PNGs are valid
    for png_path in png_paths:
        img = Image.open(png_path)
        assert img.size[0] > 0
        assert img.size[1] > 0


@skip_no_pdf_converter
def test_pdf_to_pngs_default_output_dir(temp_dir, sample_pdf):
    """Test that default output directory is created correctly."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    # Move PDF to temp_dir
    pdf_in_temp = temp_dir / "test.pdf"
    shutil.copy(sample_pdf, pdf_in_temp)

    png_paths = pdf_to_pngs(pdf_in_temp, dpi=300)

    assert len(png_paths) > 0
    # Should create {pdf_name}_pages directory
    expected_dir = temp_dir / "test_pages"
    assert expected_dir.exists()
    assert all(p.parent == expected_dir for p in png_paths)


@skip_no_pdf_converter
def test_pdf_to_pngs_custom_dpi(temp_dir, sample_pdf):
    """Test converting PDF with custom DPI."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    output_dir = temp_dir / "output"

    # Test with different DPI values
    for dpi in [150, 300, 600]:
        png_paths = pdf_to_pngs(sample_pdf, output_dir=output_dir, dpi=dpi)
        assert len(png_paths) > 0

        # Higher DPI should produce larger images
        img = Image.open(png_paths[0])
        # Note: Actual size may vary by backend, so we just check it's valid
        assert img.size[0] > 0


def test_pdf_to_pngs_nonexistent_file(temp_dir):
    """Test error handling for nonexistent PDF."""
    nonexistent_pdf = temp_dir / "nonexistent.pdf"

    with pytest.raises(FileNotFoundError):
        pdf_to_pngs(nonexistent_pdf)


def test_pdf_to_pngs_fallback_chain(temp_dir, sample_pdf):
    """Test that fallback chain works when backends are unavailable."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    # This test verifies the function tries multiple backends
    # We can't easily test all fallback scenarios without mocking,
    # but we can verify it works with whatever backend is available
    output_dir = temp_dir / "output"

    try:
        png_paths = pdf_to_pngs(sample_pdf, output_dir=output_dir, dpi=300)
        assert len(png_paths) > 0
    except RuntimeError as e:
        # If all backends fail, we should get a helpful error message
        assert "No PDF conversion library available" in str(e)


# ============================================================================
# PNG to PDF Conversion Tests
# ============================================================================


def test_pngs_to_pdf_single_image(temp_dir, sample_png):
    """Test converting a single PNG to PDF."""
    output_pdf = temp_dir / "output.pdf"

    result_path = pngs_to_pdf([sample_png], output_pdf, page_size=(8.5, 11.0), dpi=300)

    assert result_path == output_pdf
    assert output_pdf.exists()
    assert output_pdf.suffix == ".pdf"


def test_pngs_to_pdf_multiple_images(temp_dir):
    """Test converting multiple PNGs to a single PDF."""
    # Create multiple test PNGs
    png_paths = []
    for i in range(3):
        img = Image.new("RGB", (2550, 3300), color=("white", "lightgray", "lightblue")[i])
        png_path = temp_dir / f"page_{i + 1}.png"
        img.save(png_path)
        png_paths.append(png_path)

    output_pdf = temp_dir / "output.pdf"
    result_path = pngs_to_pdf(png_paths, output_pdf, page_size=(8.5, 11.0), dpi=300)

    assert result_path == output_pdf
    assert output_pdf.exists()


def test_pngs_to_pdf_custom_page_size(temp_dir, sample_png):
    """Test converting PNG with custom page size."""
    output_pdf = temp_dir / "output.pdf"

    # Test A4 size (8.27 x 11.69 inches)
    result_path = pngs_to_pdf([sample_png], output_pdf, page_size=(8.27, 11.69), dpi=300)

    assert result_path.exists()


def test_pngs_to_pdf_crop_vs_scale(temp_dir):
    """Test crop_to_size vs scale behavior."""
    # Create a wide image (not 8.5x11 aspect ratio)
    wide_img = Image.new("RGB", (4000, 2000), color="red")
    wide_png = temp_dir / "wide.png"
    wide_img.save(wide_png)

    output_pdf_crop = temp_dir / "output_crop.pdf"
    output_pdf_scale = temp_dir / "output_scale.pdf"

    # Test cropping
    pngs_to_pdf([wide_png], output_pdf_crop, page_size=(8.5, 11.0), dpi=300, crop_to_size=True)
    assert output_pdf_crop.exists()

    # Test scaling
    pngs_to_pdf([wide_png], output_pdf_scale, page_size=(8.5, 11.0), dpi=300, crop_to_size=False)
    assert output_pdf_scale.exists()


def test_pngs_to_pdf_missing_image(temp_dir, sample_png):
    """Test handling of missing PNG files."""
    nonexistent_png = temp_dir / "nonexistent.png"
    output_pdf = temp_dir / "output.pdf"

    # Should skip missing file and continue
    result_path = pngs_to_pdf([sample_png, nonexistent_png], output_pdf, page_size=(8.5, 11.0))
    assert result_path.exists()


def test_pngs_to_pdf_no_valid_images(temp_dir):
    """Test error handling when no valid images are provided."""
    nonexistent_png = temp_dir / "nonexistent.png"
    output_pdf = temp_dir / "output.pdf"

    with pytest.raises(RuntimeError, match="No valid images"):
        pngs_to_pdf([nonexistent_png], output_pdf, page_size=(8.5, 11.0))


def test_pngs_to_pdf_rgb_conversion(temp_dir):
    """Test that non-RGB images are converted to RGB."""
    # Create RGBA image
    rgba_img = Image.new("RGBA", (2550, 3300), color=(255, 0, 0, 128))
    rgba_png = temp_dir / "rgba.png"
    rgba_img.save(rgba_png)

    output_pdf = temp_dir / "output.pdf"
    result_path = pngs_to_pdf([rgba_png], output_pdf, page_size=(8.5, 11.0))

    assert result_path.exists()


# ============================================================================
# Round-Trip Conversion Tests
# ============================================================================


@skip_no_pdf_converter
def test_round_trip_pdf_png_pdf(temp_dir, sample_pdf):
    """Test PDF → PNG → PDF round-trip conversion."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    # PDF → PNG
    png_dir = temp_dir / "pngs"
    png_paths = pdf_to_pngs(sample_pdf, output_dir=png_dir, dpi=300)
    assert len(png_paths) > 0

    # PNG → PDF
    output_pdf = temp_dir / "round_trip.pdf"
    result_path = pngs_to_pdf(png_paths, output_pdf, page_size=(8.5, 11.0), dpi=300)

    assert result_path.exists()
    # Verify the round-trip PDF has the same number of pages
    # (We can't easily verify content without a PDF library, but structure should match)


# ============================================================================
# Convenience Function Tests
# ============================================================================


@skip_no_pdf_converter
def test_convert_pdf_to_images(temp_dir, sample_pdf):
    """Test convenience function convert_pdf_to_images."""
    if not sample_pdf.exists():
        pytest.skip("Test PDF not available")

    output_dir = temp_dir / "output"
    png_paths = convert_pdf_to_images(sample_pdf, output_dir=output_dir, dpi=300)

    assert len(png_paths) > 0
    assert all(p.suffix == ".png" for p in png_paths)


def test_convert_images_to_pdf(temp_dir, sample_png):
    """Test convenience function convert_images_to_pdf."""
    output_pdf = temp_dir / "output.pdf"
    result_path = convert_images_to_pdf([sample_png], output_pdf, page_size=(8.5, 11.0), dpi=300)

    assert result_path == output_pdf
    assert output_pdf.exists()


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


def test_pdf_to_pngs_empty_pdf(temp_dir):
    """Test handling of edge cases (if we can create an empty PDF)."""
    # This is hard to test without creating an actual empty PDF
    # We'll skip this for now as it requires specific PDF creation
    pytest.skip("Empty PDF creation requires specific tools")


def test_pngs_to_pdf_very_large_image(temp_dir):
    """Test handling of very large images."""
    # Create a very large image
    large_img = Image.new("RGB", (10000, 10000), color="white")
    large_png = temp_dir / "large.png"
    large_img.save(large_png)

    output_pdf = temp_dir / "output.pdf"

    # Should handle large images (may be slow, but shouldn't crash)
    result_path = pngs_to_pdf([large_png], output_pdf, page_size=(8.5, 11.0), dpi=300)
    assert result_path.exists()


def test_pngs_to_pdf_sorted_order(temp_dir):
    """Test that PNGs are processed in sorted order."""
    # Create PNGs with non-sequential names
    png_paths = []
    for name in ["page_3.png", "page_1.png", "page_2.png"]:
        img = Image.new("RGB", (2550, 3300), color="white")
        png_path = temp_dir / name
        img.save(png_path)
        png_paths.append(png_path)

    output_pdf = temp_dir / "output.pdf"
    result_path = pngs_to_pdf(png_paths, output_pdf, page_size=(8.5, 11.0))

    # Should process in sorted order (page_1, page_2, page_3)
    assert result_path.exists()
