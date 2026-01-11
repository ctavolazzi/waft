"""
PDF to Image and Image to PDF Converter

Converts PDFs to PNG images (one per page) and PNG images back to PDFs.
Supports 8.5 x 11 inch (letter size) page format.
"""

from pathlib import Path
from typing import List, Optional, Tuple
import subprocess
import sys


def pdf_to_pngs(
    pdf_path: Path,
    output_dir: Optional[Path] = None,
    dpi: int = 300,
    format: str = "png",
) -> List[Path]:
    """
    Convert PDF to PNG images (one per page).
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save PNGs (default: same as PDF)
        dpi: Resolution for images (default: 300)
        format: Output format (default: "png")
    
    Returns:
        List of paths to generated PNG files
    
    Raises:
        RuntimeError: If conversion fails
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # Determine output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Try pdf2image first (best quality)
    try:
        from pdf2image import convert_from_path
        
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            fmt=format,
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
                "-density", str(dpi),
                "-quality", "100",
                str(pdf_path),
                str(output_pattern),
            ]
            
            result = subprocess.run(
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
                raise RuntimeError(
                    "No PDF conversion library available. Install one of:\n"
                    "  - pdf2image: pip install pdf2image\n"
                    "  - ImageMagick: brew install imagemagick (macOS)\n"
                    "  - PyMuPDF: pip install pymupdf"
                )


def pngs_to_pdf(
    png_paths: List[Path],
    output_path: Path,
    page_size: Tuple[float, float] = (8.5, 11.0),  # inches
    dpi: int = 300,
    crop_to_size: bool = True,
) -> Path:
    """
    Convert PNG images to a PDF binder (8.5 x 11 inches).
    
    Args:
        png_paths: List of PNG file paths
        output_path: Output PDF path
        page_size: Page size in inches (width, height) - default: 8.5 x 11 (letter)
        dpi: DPI for PDF (default: 300)
        crop_to_size: If True, crop images to page size; if False, scale to fit
    
    Returns:
        Path to generated PDF
    
    Raises:
        RuntimeError: If conversion fails
    """
    from PIL import Image
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert page size to pixels
    page_width = int(page_size[0] * dpi)
    page_height = int(page_size[1] * dpi)
    
    images = []
    for png_path in sorted(png_paths):
        if not Path(png_path).exists():
            print(f"Warning: PNG not found, skipping: {png_path}")
            continue
        
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
        raise RuntimeError("No valid images to convert to PDF")
    
    # Save as PDF
    images[0].save(
        output_path,
        "PDF",
        resolution=dpi,
        save_all=True,
        append_images=images[1:] if len(images) > 1 else [],
    )
    
    return output_path


def convert_pdf_to_images(
    pdf_path: Path,
    output_dir: Optional[Path] = None,
    dpi: int = 300,
) -> List[Path]:
    """
    Convenience function: Convert PDF to PNG images.
    
    Args:
        pdf_path: Path to PDF
        output_dir: Output directory (default: PDF directory + _pages)
        dpi: Resolution (default: 300)
    
    Returns:
        List of PNG file paths
    """
    return pdf_to_pngs(pdf_path, output_dir, dpi)


def convert_images_to_pdf(
    image_paths: List[Path],
    output_path: Path,
    page_size: Tuple[float, float] = (8.5, 11.0),
    dpi: int = 300,
    crop: bool = True,
) -> Path:
    """
    Convenience function: Convert PNG images to PDF.
    
    Args:
        image_paths: List of image paths
        output_path: Output PDF path
        page_size: Page size in inches (default: 8.5 x 11)
        dpi: Resolution (default: 300)
        crop: Crop to page size (default: True)
    
    Returns:
        Path to generated PDF
    """
    return pngs_to_pdf(image_paths, output_path, page_size, dpi, crop)
