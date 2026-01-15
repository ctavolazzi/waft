"""
TheChronicler: Self-Monitoring System

TheChronicler observes, records, and reports on all activity within the WAFT system.
Monitors genesis (creation) and exodus (deletion) of all system components.

Architecture:
- Core TheChronicler class orchestrates all observers
- File system observer (watchdog)
- Git change observer
- Work effort observer
- Hourly and daily report generation
- Oracle integration for decision context
"""

from .chronicler import TheChronicler

__all__ = ["TheChronicler"]
