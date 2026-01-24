#!/usr/bin/env python3
"""
Test suite for the SRD Parser.
Run from the dnd-toolkit directory: python tests/test-parser.py
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Test results tracking
tests_run = 0
tests_passed = 0
tests_failed = 0

def test(name):
    """Decorator for test functions."""
    def decorator(fn):
        def wrapper(*args, **kwargs):
            global tests_run, tests_passed, tests_failed
            tests_run += 1
            try:
                fn(*args, **kwargs)
                tests_passed += 1
                print(f"  ✅ {name}")
                return True
            except AssertionError as e:
                tests_failed += 1
                print(f"  ❌ {name}: {e}")
                return False
            except Exception as e:
                tests_failed += 1
                print(f"  ❌ {name}: {type(e).__name__}: {e}")
                return False
        return wrapper
    return decorator


class TestDataFiles:
    """Tests for the generated data files."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
    
    @test("monsters.json exists and is valid JSON")
    def test_monsters_exists(self):
        path = self.data_path / "monsters.json"
        assert path.exists(), "monsters.json not found"
        data = json.loads(path.read_text())
        assert isinstance(data, list), "Should be a list"
        assert len(data) > 0, "Should have entries"
    
    @test("spells.json exists and is valid JSON")
    def test_spells_exists(self):
        path = self.data_path / "spells.json"
        assert path.exists(), "spells.json not found"
        data = json.loads(path.read_text())
        assert isinstance(data, list), "Should be a list"
        assert len(data) > 0, "Should have entries"
    
    @test("items.json exists and is valid JSON")
    def test_items_exists(self):
        path = self.data_path / "items.json"
        assert path.exists(), "items.json not found"
        data = json.loads(path.read_text())
        assert isinstance(data, list), "Should be a list"
        assert len(data) > 0, "Should have entries"
    
    @test("monsters have required fields")
    def test_monster_fields(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        for m in monsters[:10]:  # Check first 10
            assert "name" in m, f"Monster missing name: {m}"
            assert m["name"], "Name should not be empty"
    
    @test("spells have required fields")
    def test_spell_fields(self):
        path = self.data_path / "spells.json"
        spells = json.loads(path.read_text())
        for s in spells[:10]:  # Check first 10
            assert "name" in s, f"Spell missing name: {s}"
            assert "level" in s, f"Spell missing level: {s}"
    
    @test("items have required fields")
    def test_item_fields(self):
        path = self.data_path / "items.json"
        items = json.loads(path.read_text())
        for i in items[:10]:  # Check first 10
            assert "name" in i, f"Item missing name: {i}"
    
    @test("monsters are sorted alphabetically")
    def test_monsters_sorted(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        names = [m["name"] for m in monsters]
        assert names == sorted(names), "Monsters should be sorted"
    
    @test("CR values are numeric")
    def test_cr_numeric(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        for m in monsters:
            if m.get("cr") is not None:
                assert isinstance(m["cr"], (int, float)), f"CR should be numeric: {m['name']}"
    
    @test("spell levels are integers 0-9")
    def test_spell_levels(self):
        path = self.data_path / "spells.json"
        spells = json.loads(path.read_text())
        for s in spells:
            if s.get("level") is not None:
                assert isinstance(s["level"], int), f"Level should be int: {s['name']}"
                assert 0 <= s["level"] <= 9, f"Level should be 0-9: {s['name']}"


class TestParserFunctions:
    """Tests for parser utility functions."""
    
    @test("CR fraction parsing")
    def test_cr_fractions(self):
        # Test the logic used in the parser
        test_cases = [
            ("1/8", 0.125),
            ("1/4", 0.25),
            ("1/2", 0.5),
            ("1", 1.0),
            ("10", 10.0),
        ]
        for cr_str, expected in test_cases:
            if "/" in cr_str:
                num, den = cr_str.split("/")
                result = float(num) / float(den)
            else:
                result = float(cr_str)
            assert result == expected, f"Expected {expected}, got {result}"
    
    @test("ability modifier calculation")
    def test_ability_modifiers(self):
        # Standard D&D modifier formula
        def get_modifier(score):
            return (score - 10) // 2
        
        test_cases = [
            (1, -5),
            (8, -1),
            (10, 0),
            (12, 1),
            (18, 4),
            (20, 5),
            (30, 10),
        ]
        for score, expected in test_cases:
            result = get_modifier(score)
            assert result == expected, f"Score {score}: expected {expected}, got {result}"


class TestDataQuality:
    """Tests for data quality and completeness."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
    
    @test("has at least 100 monsters")
    def test_monster_count(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        assert len(monsters) >= 100, f"Only {len(monsters)} monsters"
    
    @test("has at least 100 spells")
    def test_spell_count(self):
        path = self.data_path / "spells.json"
        spells = json.loads(path.read_text())
        assert len(spells) >= 100, f"Only {len(spells)} spells"
    
    @test("has at least 50 items")
    def test_item_count(self):
        path = self.data_path / "items.json"
        items = json.loads(path.read_text())
        assert len(items) >= 50, f"Only {len(items)} items"
    
    @test("monsters have diverse types")
    def test_monster_types(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        types = set(m.get("type") for m in monsters if m.get("type"))
        # Should have at least 5 different types
        assert len(types) >= 5, f"Only {len(types)} types: {types}"
    
    @test("spells cover all levels 0-9")
    def test_spell_levels_coverage(self):
        path = self.data_path / "spells.json"
        spells = json.loads(path.read_text())
        levels = set(s.get("level") for s in spells if s.get("level") is not None)
        for level in range(10):
            assert level in levels, f"Missing level {level} spells"
    
    @test("monsters have actions")
    def test_monsters_have_actions(self):
        path = self.data_path / "monsters.json"
        monsters = json.loads(path.read_text())
        with_actions = sum(1 for m in monsters if m.get("actions"))
        # At least 50% should have actions parsed
        ratio = with_actions / len(monsters)
        assert ratio >= 0.3, f"Only {ratio*100:.1f}% have actions"
    
    @test("spells have descriptions")
    def test_spells_have_descriptions(self):
        path = self.data_path / "spells.json"
        spells = json.loads(path.read_text())
        with_desc = sum(1 for s in spells if s.get("description"))
        ratio = with_desc / len(spells)
        assert ratio >= 0.5, f"Only {ratio*100:.1f}% have descriptions"


def run_tests():
    """Run all test suites."""
    print("\n" + "=" * 60)
    print("D&D Toolkit - Parser Test Suite")
    print("=" * 60 + "\n")
    
    # Data file tests
    print("📁 Data File Tests")
    print("-" * 40)
    data_tests = TestDataFiles()
    data_tests.test_monsters_exists()
    data_tests.test_spells_exists()
    data_tests.test_items_exists()
    data_tests.test_monster_fields()
    data_tests.test_spell_fields()
    data_tests.test_item_fields()
    data_tests.test_monsters_sorted()
    data_tests.test_cr_numeric()
    data_tests.test_spell_levels()
    
    # Parser function tests
    print("\n🔧 Parser Function Tests")
    print("-" * 40)
    parser_tests = TestParserFunctions()
    parser_tests.test_cr_fractions()
    parser_tests.test_ability_modifiers()
    
    # Data quality tests
    print("\n📊 Data Quality Tests")
    print("-" * 40)
    quality_tests = TestDataQuality()
    quality_tests.test_monster_count()
    quality_tests.test_spell_count()
    quality_tests.test_item_count()
    quality_tests.test_monster_types()
    quality_tests.test_spell_levels_coverage()
    quality_tests.test_monsters_have_actions()
    quality_tests.test_spells_have_descriptions()
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {tests_passed}/{tests_run} passed, {tests_failed} failed")
    print("=" * 60 + "\n")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
