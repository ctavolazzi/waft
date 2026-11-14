#!/usr/bin/env python3
"""Thin wrapper around waft.printer_friendly_helper, where this code lives since 2026-11-14.

It moved into the package so waft.document_builder can import it from an installed wheel.
"""

import sys
from pathlib import Path

try:
    import waft.printer_friendly_helper  # noqa: F401
except ImportError:  # run from a checkout without an install
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from waft.printer_friendly_helper import *  # noqa: E402,F401,F403
