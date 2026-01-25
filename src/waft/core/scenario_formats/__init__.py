"""
Scenario Format Parsers for WAFT.

Tiered scenario format system:
- Level 1: Eleventy CYOA (Markdown + YAML) - Simple branching narratives
- Level 2: Ink (reserved for future) - Branching with state
- Level 3: WAFT Native - Full ML-driven DND scenarios
"""

from .eleventy_cyoa import ElevntyCYOAParser, ElevntyCYOAScenario

__all__ = ["ElevntyCYOAParser", "ElevntyCYOAScenario"]
