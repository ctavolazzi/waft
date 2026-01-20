"""
Output Quality Validation
=========================

Functions to validate generated PDFs meet quality standards.
"""

import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from PyPDF2 import PdfReader

    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    logger.warning("PyPDF2 not available - PDF validation will be limited")


def validate_pdf_quality(pdf_path: Path, min_pages: int = 1) -> dict:
    """
    Validate PDF quality and return validation results.

    Args:
        pdf_path: Path to PDF file
        min_pages: Minimum expected page count

    Returns:
        Dictionary with validation results:
        {
            'valid': bool,
            'file_size': int,
            'page_count': int,
            'checksum': str,
            'errors': list
        }
    """
    results = {"valid": False, "file_size": 0, "page_count": 0, "checksum": None, "errors": []}

    try:
        # Check file exists
        if not pdf_path.exists():
            results["errors"].append("PDF file does not exist")
            return results

        # Check file size
        file_size = pdf_path.stat().st_size
        results["file_size"] = file_size

        if file_size == 0:
            results["errors"].append("PDF file is empty")
            return results

        # Verify PDF structure (if PyPDF2 available)
        if PYPDF2_AVAILABLE:
            try:
                reader = PdfReader(str(pdf_path))
                page_count = len(reader.pages)
                results["page_count"] = page_count

                if page_count < min_pages:
                    results["errors"].append(
                        f"PDF has {page_count} pages, expected at least {min_pages}"
                    )

            except Exception as e:
                results["errors"].append(f"PDF structure invalid: {e}")
                # Don't return here - still generate checksum

        # Generate checksum
        try:
            checksum = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            results["checksum"] = checksum
        except Exception as e:
            results["errors"].append(f"Failed to generate checksum: {e}")

        # All checks passed
        results["valid"] = len(results["errors"]) == 0

    except Exception as e:
        results["errors"].append(f"Validation error: {e}")
        logger.exception(f"PDF validation failed for {pdf_path}")

    return results
