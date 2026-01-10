"""Centralized logging infrastructure for Waft.

Provides consistent logging across all modules with proper formatting
and level management.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Get a logger for the specified module.

    Args:
        name: Logger name, typically __name__ from calling module
        level: Optional logging level (defaults to INFO)

    Returns:
        Configured logger instance

    Example:
        >>> from waft.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Operation completed")
    """
    logger = logging.getLogger(f"waft.{name}")

    # Only configure if this logger hasn't been configured yet
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Set level
        logger.setLevel(level or logging.INFO)

    return logger


def get_file_logger(
    name: str,
    log_file: Path,
    level: Optional[int] = None
) -> logging.Logger:
    """Get a logger that writes to a file.

    Args:
        name: Logger name
        log_file: Path to log file
        level: Optional logging level (defaults to DEBUG)

    Returns:
        Configured logger instance with file handler
    """
    logger = logging.getLogger(f"waft.{name}.file")

    if not logger.handlers:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(log_file)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # File loggers typically use DEBUG level
        logger.setLevel(level or logging.DEBUG)

    return logger


def configure_root_logger(level: int = logging.INFO) -> None:
    """Configure the root Waft logger.

    Args:
        level: Logging level for root logger
    """
    root_logger = logging.getLogger("waft")
    root_logger.setLevel(level)

    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
