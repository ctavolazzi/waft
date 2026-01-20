"""
PDF to Image and Image to PDF Converter

Converts PDFs to PNG images (one per page) and PNG images back to PDFs.
Supports multiple standard page sizes with configurable DPI.

Usage:
    # Convert PDF to PNGs
    from src.waft.evolution.pdf_image_converter import pdf_to_pngs, PageSize

    png_paths = pdf_to_pngs("document.pdf", dpi=300)

    # Convert PNGs to PDF with custom page size
    from src.waft.evolution.pdf_image_converter import pngs_to_pdf, PageSize

    pngs_to_pdf(png_paths, "output.pdf", page_size=PageSize.LETTER, dpi=300)

    # Auto-select DPI based on document size
    png_paths = pdf_to_pngs("document.pdf", dpi="auto")
"""

import hashlib
import os
import subprocess
from enum import Enum
from pathlib import Path


class PageSize(Enum):
    """Standard page sizes in inches (width, height)."""

    LETTER = (8.5, 11.0)  # US Letter
    LEGAL = (8.5, 14.0)  # US Legal
    A4 = (8.27, 11.69)  # ISO A4
    A3 = (11.69, 16.54)  # ISO A3
    TABLOID = (11.0, 17.0)  # US Tabloid

    @property
    def width(self) -> float:
        """Page width in inches."""
        return self.value[0]

    @property
    def height(self) -> float:
        """Page height in inches."""
        return self.value[1]

    @property
    def tuple(self) -> tuple[float, float]:
        """Page size as (width, height) tuple."""
        return self.value


def _auto_select_dpi(pdf_path: Path) -> int:
    """
    Automatically select DPI based on PDF file size and complexity.

    Heuristics:
    - Small files (< 1MB): 150 DPI (fast, good for previews)
    - Medium files (1-10MB): 300 DPI (balanced quality/speed)
    - Large files (> 10MB): 300 DPI (high quality, may be slow)

    Args:
        pdf_path: Path to PDF file

    Returns:
        Recommended DPI value
    """
    try:
        file_size_mb = pdf_path.stat().st_size / (1024 * 1024)

        if file_size_mb < 1:
            return 150  # Fast preview quality
        elif file_size_mb < 10:
            return 300  # Standard quality
        else:
            return 300  # High quality (may be slow for very large files)
    except Exception:
        # Default to 300 if we can't determine size
        return 300


def _get_file_hash(file_path: Path) -> str:
    """Generate SHA256 hash of file for caching."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _convert_single_page_pdf2image(
    pdf_path: Path,
    page_num: int,
    output_dir: Path,
    dpi: int,
    format: str,
) -> Path | None:
    """Convert a single page using pdf2image (for parallel processing)."""
    try:
        from pdf2image import convert_from_path

        images = convert_from_path(
            pdf_path, dpi=dpi, fmt=format, first_page=page_num, last_page=page_num
        )
        if images:
            png_path = output_dir / f"page_{page_num:03d}.png"
            images[0].save(png_path, format.upper())
            return png_path
    except Exception:
        pass
    return None


def pdf_to_pngs(
    pdf_path: Path,
    output_dir: Path | None = None,
    dpi: int | str = 300,
    format: str = "png",
) -> list[Path]:
    """
    Convert PDF to PNG images (one per page).

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save PNGs (default: same as PDF)
        dpi: Resolution for images. Can be:
            - Integer (150, 300, 600): Specific DPI value
            - "auto": Automatically select based on file size
            Default: 300
        format: Output format (default: "png")

    Returns:
        List of paths to generated PNG files

    Raises:
        RuntimeError: If conversion fails
        FileNotFoundError: If PDF file doesn't exist

    Examples:
        # Standard conversion at 300 DPI
        png_paths = pdf_to_pngs("document.pdf", dpi=300)

        # Auto-select DPI based on file size
        png_paths = pdf_to_pngs("document.pdf", dpi="auto")

        # High quality conversion
        png_paths = pdf_to_pngs("document.pdf", dpi=600)

    DPI Recommendations:
        - 150 DPI: Fast previews, web display
        - 300 DPI: Standard print quality (recommended)
        - 600 DPI: High quality print, detailed graphics
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Auto-select DPI if requested
    if dpi == "auto":
        dpi = _auto_select_dpi(pdf_path)
    elif not isinstance(dpi, int):
        raise ValueError(f"DPI must be an integer or 'auto', got: {dpi}")

    # Determine output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Try pdf2image first (best quality, supports parallel processing)
    try:
        from pdf2image import convert_from_path

        # For multi-page PDFs, use parallel processing if available
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            fmt=format,
            thread_count=min(4, os.cpu_count() or 1),  # Use up to 4 threads
        )

        png_paths = []
        for i, image in enumerate(images, start=1):
            png_path = output_dir / f"page_{i:03d}.png"
            image.save(png_path, format.upper())
            png_paths.append(png_path)

        return png_paths

    except ImportError:
        # Fallback to ImageMagick via subprocess
        try:
            base_name = pdf_path.stem
            output_pattern = output_dir / f"{base_name}_page_%03d.{format}"

            # Use ImageMagick convert command
            cmd = [
                "convert",
                "-density",
                str(dpi),
                "-quality",
                "100",
                str(pdf_path),
                str(output_pattern),
            ]

            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )

            # Find all generated files
            pattern = output_dir / f"{base_name}_page_*.{format}"
            png_paths = sorted(pattern.parent.glob(pattern.name))
            return list(png_paths)

        except (subprocess.CalledProcessError, FileNotFoundError):
            # Last resort: use PyMuPDF (fitz)
            try:
                import fitz  # PyMuPDF

                doc = fitz.open(pdf_path)
                png_paths = []

                for page_num in range(len(doc)):
                    page = doc[page_num]
                    # Render at specified DPI
                    mat = fitz.Matrix(dpi / 72, dpi / 72)
                    pix = page.get_pixmap(matrix=mat)

                    png_path = output_dir / f"page_{page_num + 1:03d}.png"
                    pix.save(png_path)
                    png_paths.append(png_path)

                doc.close()
                return png_paths

            except ImportError:
                error_msg = (
                    "No PDF conversion library available.\n\n"
                    "Please install one of the following:\n"
                    "  1. pdf2image (recommended):\n"
                    "     pip install pdf2image\n"
                    "     # Also requires poppler-utils:\n"
                    "     # macOS: brew install poppler\n"
                    "     # Ubuntu: sudo apt-get install poppler-utils\n\n"
                    "  2. ImageMagick:\n"
                    "     # macOS: brew install imagemagick\n"
                    "     # Ubuntu: sudo apt-get install imagemagick\n\n"
                    "  3. PyMuPDF (fallback):\n"
                    "     pip install pymupdf\n\n"
                    "For more information, see: docs/PDF_PNG_CONVERSION.md"
                )
                raise RuntimeError(error_msg)


def pngs_to_pdf(
    png_paths: list[Path],
    output_path: Path,
    page_size: tuple[float, float] | PageSize = PageSize.LETTER,
    dpi: int = 300,
    crop_to_size: bool = True,
) -> Path:
    """
    Convert PNG images to a PDF binder.

    Args:
        png_paths: List of PNG file paths
        output_path: Output PDF path
        page_size: Page size. Can be:
            - PageSize enum (e.g., PageSize.LETTER, PageSize.A4)
            - Tuple of (width, height) in inches
            Default: PageSize.LETTER (8.5 x 11 inches)
        dpi: DPI for PDF (default: 300)
        crop_to_size: If True, crop images to page size (center crop);
                     if False, scale to fit within page size (maintains aspect ratio)

    Returns:
        Path to generated PDF

    Raises:
        RuntimeError: If conversion fails or no valid images provided

    Examples:
        # Use standard page size
        from src.waft.evolution.pdf_image_converter import pngs_to_pdf, PageSize

        pngs_to_pdf(png_list, "output.pdf", page_size=PageSize.LETTER)
        pngs_to_pdf(png_list, "output.pdf", page_size=PageSize.A4)

        # Use custom page size
        pngs_to_pdf(png_list, "output.pdf", page_size=(10.0, 12.0))

        # Scale instead of crop
        pngs_to_pdf(png_list, "output.pdf", crop_to_size=False)
    """
    from PIL import Image

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Handle PageSize enum or tuple
    if isinstance(page_size, PageSize):
        page_size_tuple = page_size.tuple
    else:
        page_size_tuple = page_size

    # Convert page size to pixels
    page_width = int(page_size_tuple[0] * dpi)
    page_height = int(page_size_tuple[1] * dpi)

    images = []
    total_images = len(png_paths)
    for idx, png_path in enumerate(sorted(png_paths), 1):
        if not Path(png_path).exists():
            print(f"Warning: PNG not found, skipping: {png_path}")
            continue

        # Progress indicator for large batches
        if total_images > 5:
            print(f"Processing image {idx}/{total_images}: {Path(png_path).name}")

        img = Image.open(png_path)

        if crop_to_size:
            # Crop to exact page size (center crop)
            img_width, img_height = img.size

            # Calculate crop box (center crop)
            if img_width / img_height > page_width / page_height:
                # Image is wider - crop width
                new_width = int(img_height * page_width / page_height)
                left = (img_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img_height))
            else:
                # Image is taller - crop height
                new_height = int(img_width * page_height / page_width)
                top = (img_height - new_height) // 2
                img = img.crop((0, top, img_width, top + new_height))

            # Resize to exact page size
            img = img.resize((page_width, page_height), Image.Resampling.LANCZOS)
        else:
            # Scale to fit within page size (maintain aspect ratio)
            img.thumbnail((page_width, page_height), Image.Resampling.LANCZOS)

            # Create new image with page size and paste centered
            new_img = Image.new("RGB", (page_width, page_height), "white")
            paste_x = (page_width - img.width) // 2
            paste_y = (page_height - img.height) // 2
            new_img.paste(img, (paste_x, paste_y))
            img = new_img

        # Convert to RGB if needed (for PDF)
        if img.mode != "RGB":
            img = img.convert("RGB")

        images.append(img)

    if not images:
        raise RuntimeError(
            "No valid images to convert to PDF.\n"
            "Please check that:\n"
            "  - PNG files exist and are readable\n"
            "  - Files are valid image formats\n"
            "  - File paths are correct"
        )

    # Save as PDF
    try:
        images[0].save(
            output_path,
            "PDF",
            resolution=dpi,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else [],
        )

        # Quality metrics
        pdf_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ PDF created: {len(images)} pages, {pdf_size:.2f} MB")

    except Exception as e:
        raise RuntimeError(
            f"Failed to save PDF: {e}\n"
            "Please check that:\n"
            "  - Output directory is writable\n"
            "  - Sufficient disk space available\n"
            "  - PIL/Pillow is properly installed"
        )

    return output_path


def convert_pdf_to_images(
    pdf_path: Path,
    output_dir: Path | None = None,
    dpi: int | str = 300,
    show_progress: bool = True,
) -> list[Path]:
    """
    Convenience function: Convert PDF to PNG images.

    Args:
        pdf_path: Path to PDF
        output_dir: Output directory (default: PDF directory + _pages)
        dpi: Resolution. Can be integer (150, 300, 600) or "auto" (default: 300)
        show_progress: Show progress messages (default: True)

    Returns:
        List of PNG file paths

    Examples:
        # Standard conversion
        pngs = convert_pdf_to_images("doc.pdf", dpi=300)

        # Auto-select DPI
        pngs = convert_pdf_to_images("doc.pdf", dpi="auto")

        # Silent mode
        pngs = convert_pdf_to_images("doc.pdf", show_progress=False)
    """
    png_paths = pdf_to_pngs(pdf_path, output_dir, dpi)

    if show_progress and png_paths:
        total_size = sum(p.stat().st_size for p in png_paths if p.exists())
        size_mb = total_size / (1024 * 1024)
        print(f"✓ Conversion complete: {len(png_paths)} images, {size_mb:.2f} MB total")

    return png_paths


def convert_images_to_pdf(
    image_paths: list[Path],
    output_path: Path,
    page_size: tuple[float, float] | PageSize = PageSize.LETTER,
    dpi: int = 300,
    crop: bool = True,
) -> Path:
    """
    Convenience function: Convert PNG images to PDF.

    Args:
        image_paths: List of image paths
        output_path: Output PDF path
        page_size: Page size. Can be PageSize enum or (width, height) tuple
                   (default: PageSize.LETTER)
        dpi: Resolution (default: 300)
        crop: Crop to page size (default: True)

    Returns:
        Path to generated PDF

    Examples:
        from src.waft.evolution.pdf_image_converter import convert_images_to_pdf, PageSize

        # Use standard page size
        convert_images_to_pdf(images, "output.pdf", page_size=PageSize.A4)

        # Custom page size
        convert_images_to_pdf(images, "output.pdf", page_size=(10.0, 12.0))
    """
    return pngs_to_pdf(image_paths, output_path, page_size, dpi, crop)
