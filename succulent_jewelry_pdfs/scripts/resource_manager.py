"""
Resource Management
===================

Manages temporary files and cleanup.
"""

import atexit
import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

_temp_files: list[Path] = []


def cleanup_temp_files():
    """Clean up all temporary files."""
    for temp_file in _temp_files:
        try:
            if temp_file.exists():
                if temp_file.is_dir():
                    import shutil

                    shutil.rmtree(temp_file)
                else:
                    temp_file.unlink()
        except Exception as e:
            logger.warning(f"Failed to clean up {temp_file}: {e}")


# Register cleanup on exit
atexit.register(cleanup_temp_files)


def create_temp_dir(prefix: str = "pdf_gen_") -> Path:
    """
    Create a temporary directory that will be cleaned up on exit.

    Args:
        prefix: Prefix for temporary directory name

    Returns:
        Path to temporary directory
    """
    temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
    _temp_files.append(temp_dir)
    return temp_dir


def create_temp_file(prefix: str = "pdf_gen_", suffix: str = ".tmp") -> Path:
    """
    Create a temporary file that will be cleaned up on exit.

    Args:
        prefix: Prefix for temporary file name
        suffix: Suffix for temporary file name

    Returns:
        Path to temporary file
    """
    temp_file = Path(tempfile.mktemp(prefix=prefix, suffix=suffix))
    _temp_files.append(temp_file)
    return temp_file
