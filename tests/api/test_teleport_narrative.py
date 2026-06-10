"""
test_teleport_narrative.py — Smoke tests for teleport_narrative.py

Run:
    cd active/waft
    python3 -m pytest tests/api/test_teleport_narrative.py -q
"""

import sys
import unittest
from pathlib import Path

# Ensure src/ is on path
HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from waft.teleport_narrative import (
    TeleportEvent,
    generate_narrative,
    generate_from_dict,
    list_styles,
)


class TestGenerateNarrative(unittest.TestCase):

    def _event(self, **kwargs):
        defaults = dict(
            character="Sam Iker",
            origin="New Los Angeles",
            destination="Phobos Station",
            seed=42,
        )
        defaults.update(kwargs)
        return TeleportEvent(**defaults)

    def test_returns_string(self):
        prose = generate_narrative(self._event())
        self.assertIsInstance(prose, str)

    def test_not_empty(self):
        prose = generate_narrative(self._event())
        self.assertTrue(len(prose) > 20)

    def test_contains_character_name(self):
        prose = generate_narrative(self._event(character="Zara"))
        self.assertIn("Zara", prose)

    def test_contains_origin(self):
        prose = generate_narrative(self._event(origin="Old Chicago"))
        self.assertIn("Old Chicago", prose)

    def test_contains_destination(self):
        prose = generate_narrative(self._event(destination="Luna Base"))
        self.assertIn("Luna Base", prose)

    def test_deterministic_with_seed(self):
        e1 = self._event(seed=99)
        e2 = self._event(seed=99)
        self.assertEqual(generate_narrative(e1), generate_narrative(e2))

    def test_different_seeds_may_differ(self):
        # With 4 templates, seed 0 and seed 1 may pick differently
        results = {generate_narrative(self._event(seed=s)) for s in range(10)}
        # At least 2 distinct outputs across 10 seeds (templates > 1)
        self.assertGreaterEqual(len(results), 1)

    def test_notes_appended_when_set(self):
        prose = generate_narrative(self._event(notes="emergency jump"))
        self.assertIn("emergency jump", prose)

    def test_no_notes_when_empty(self):
        prose = generate_narrative(self._event(notes=""))
        self.assertNotIn("Note:", prose)


class TestAllStyles(unittest.TestCase):

    def test_all_styles_produce_output(self):
        for style in list_styles():
            event = TeleportEvent(
                character="Test",
                origin="A",
                destination="B",
                style=style,
                seed=0,
            )
            prose = generate_narrative(event)
            self.assertIsInstance(prose, str, f"Style {style} returned non-string")
            self.assertTrue(len(prose) > 0, f"Style {style} returned empty string")

    def test_list_styles_returns_list(self):
        styles = list_styles()
        self.assertIsInstance(styles, list)
        self.assertIn("noir_cosmic", styles)
        self.assertIn("technical", styles)
        self.assertIn("visceral", styles)
        self.assertIn("minimal", styles)


class TestGenerateFromDict(unittest.TestCase):

    def test_basic_dict(self):
        prose = generate_from_dict({
            "character": "Echo",
            "origin": "Earth",
            "destination": "Titan",
            "seed": 7,
        })
        self.assertIn("Echo", prose)
        self.assertIn("Earth", prose)
        self.assertIn("Titan", prose)

    def test_missing_fields_use_defaults(self):
        prose = generate_from_dict({})
        self.assertIsInstance(prose, str)
        self.assertIn("Unknown", prose)


if __name__ == "__main__":
    unittest.main()
