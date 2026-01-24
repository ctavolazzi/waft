# D&D Toolkit Tests & Demos

## Quick Start

### Browser Tests
Open `test-runner.html` in your browser to run the JavaScript test suite:
```bash
open tests/test-runner.html
```

### Python Tests
Run the parser test suite from the command line:
```bash
cd _tools/dnd-toolkit
python3 tests/test-parser.py
```

### Interactive Demo
Open `demos/demo.html` for an interactive demonstration:
```bash
open demos/demo.html
```

## Test Files

### `tests/test-runner.html`
Browser-based JavaScript test suite that verifies:
- Data loading (monsters, spells, items JSON)
- Utility functions (modifiers, CR formatting, capitalization)
- SRD browser functions (search, filtering)
- Homebrew creator (form data, export formats)
- Card export (JSON structure, truncation)

**Tests:** 20+ individual tests
**Run time:** ~1-2 seconds

### `tests/test-parser.py`
Python test suite for the SRD parser that verifies:
- Data file existence and validity
- Required fields in each data type
- Data sorting and formatting
- Parser function correctness
- Data quality metrics (counts, coverage)

**Tests:** 18 tests
**Run time:** ~10 seconds

## Demo Files

### `demos/demo.html`
Interactive showcase of toolkit features:
- Live monster/spell/item display examples
- Card export format demonstration
- Data statistics display
- Random monster generator
- Sample card download

### `demos/sample-homebrew.json`
Example homebrew content showing proper JSON structure:
- 2 custom monsters (Shadow Stalker, Crystal Golem)
- 3 custom spells (Arcane Tether, Temporal Echo, Whispers of the Void)
- 3 custom items (Cloak of Shifting Shadows, Blade of the Storm, Potion of Arcane Sight)

## Test Coverage

| Component | Browser Tests | Python Tests |
|-----------|---------------|--------------|
| Data Loading | ✅ | ✅ |
| Monster Parser | ❌ | ✅ |
| Spell Parser | ❌ | ✅ |
| Item Parser | ❌ | ✅ |
| Search/Filter | ✅ | ❌ |
| Homebrew Forms | ✅ | ❌ |
| Card Export | ✅ | ❌ |
| Utility Functions | ✅ | ✅ |

## Expected Results

### Browser Tests
```
✓ Monsters JSON loads successfully
✓ Spells JSON loads successfully
✓ Items JSON loads successfully
✓ Monster data has required fields
✓ Spell data has required fields
✓ getModifier calculates correctly
✓ formatCR handles fractions
... (20+ tests total)
```

### Python Tests
```
✅ monsters.json exists and is valid JSON
✅ spells.json exists and is valid JSON
✅ items.json exists and is valid JSON
✅ monsters have required fields
✅ spells have required fields
✅ items have required fields
✅ monsters are sorted alphabetically
✅ CR values are numeric
✅ spell levels are integers 0-9
✅ CR fraction parsing
✅ ability modifier calculation
✅ has at least 100 monsters
✅ has at least 100 spells
✅ has at least 50 items
✅ monsters have diverse types
✅ spells cover all levels 0-9
✅ monsters have actions
✅ spells have descriptions

Results: 18/18 passed, 0 failed
```

## Adding New Tests

### Browser Tests
Add tests in `test-runner.html` using the test framework:
```javascript
test('Test name', 'group-name', async () => {
    // Your test code
    assert(condition, 'Error message');
    assertEqual(actual, expected, 'Error message');
    assertExists(value, 'Error message');
});
```

### Python Tests
Add tests in `test-parser.py` using the decorator:
```python
class TestNewFeature:
    @test("descriptive test name")
    def test_something(self):
        assert condition, "Error message"
```
