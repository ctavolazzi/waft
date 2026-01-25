# Eleventy CYOA Integration with WAFT

How the Level 1 (Eleventy CYOA) scenario format integrates with WAFT's existing architecture.

## Quick Start

```python
from waft.core.scenario_formats import ElevntyCYOAParser

# Load a scenario
scenario = ElevntyCYOAParser.load_scenario("examples/eleventy_cyoa_demo")

# Run it interactively
scenario.run_interactive()
```

## Architecture Integration

### Location in Codebase

```
waft/
├── src/waft/core/
│   ├── scenario_formats/          # NEW: Format parsers
│   │   ├── __init__.py
│   │   └── eleventy_cyoa.py       # Level 1 implementation
│   ├── dnd_scenario/              # Existing Level 3 system
│   │   ├── scenario_orchestrator.py
│   │   ├── scenario_realm.py
│   │   └── ...
│   └── scenario_decision_tree.py  # ML-based choice prediction
└── examples/
    └── eleventy_cyoa_demo/         # Example scenario
        ├── start.md
        ├── dark_passage.md
        └── ...
```

### Design Principles

1. **Separation of Concerns**
   - Format parsers (`scenario_formats/`) are separate from execution logic (`dnd_scenario/`)
   - Each level has its own module/directory
   - Clean boundaries between L1/L2/L3

2. **No Breaking Changes**
   - Existing DND scenario system (`dnd_scenario/`) is untouched
   - New code is additive only
   - Both systems can coexist

3. **Extensibility**
   - Easy to add Level 2 (Ink) later: `scenario_formats/ink_parser.py`
   - Easy to add other formats: `scenario_formats/twine_parser.py`
   - Common interface pattern for all parsers

## API Reference

### `ElevntyCYOAScenario`

Main class representing a loaded scenario.

```python
from pathlib import Path
from waft.core.scenario_formats import ElevntyCYOAScenario

scenario = ElevntyCYOAScenario(Path("path/to/scenario"))

# Access nodes
start_node = scenario.get_start_node()
node = scenario.get_node("dark_passage")

# Check if it's an ending
if node.is_ending:
    print("This is an ending node")

# Run interactively
scenario.run_interactive()
```

### `ElevntyCYOAParser`

Static parser utility.

```python
from waft.core.scenario_formats import ElevntyCYOAParser

# Load scenario
scenario = ElevntyCYOAParser.load_scenario("path/to/scenario")

# Validate without running
is_valid, errors = ElevntyCYOAParser.validate_scenario("path/to/scenario")
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

### `ScenarioNode`

Represents a single node in the scenario graph.

```python
from waft.core.scenario_formats.eleventy_cyoa import ScenarioNode

# Node attributes
print(node.id)           # File stem (e.g., "start")
print(node.title)        # From YAML front matter
print(node.content)      # Markdown content
print(node.choices)      # List of Choice objects
print(node.is_ending)    # True if no choices
```

### `Choice`

Represents a single choice option.

```python
from waft.core.scenario_formats.eleventy_cyoa import Choice

choice = node.choices[0]
print(choice.text)  # Display text for player
print(choice.path)  # Node ID to navigate to
```

## Future CLI Integration

### Proposed Commands

```bash
# Run a scenario (auto-detect format)
waft scenario run path/to/scenario

# Validate scenario graph
waft scenario validate path/to/scenario

# Create new scenario from template
waft scenario new my_scenario --level 1

# List available scenarios
waft scenario list

# Convert/upgrade scenarios
waft scenario upgrade my_scenario --to-ink    # L1 → L2 (future)
```

### Implementation Plan

1. **Add CLI command**: `src/waft/cli/scenario_commands.py`
   ```python
   import click
   from waft.core.scenario_formats import ElevntyCYOAParser

   @click.group()
   def scenario():
       """Scenario management commands."""
       pass

   @scenario.command()
   @click.argument("path")
   def run(path):
       """Run a scenario interactively."""
       scenario = ElevntyCYOAParser.load_scenario(path)
       scenario.run_interactive()

   @scenario.command()
   @click.argument("path")
   def validate(path):
       """Validate scenario graph."""
       is_valid, errors = ElevntyCYOAParser.validate_scenario(path)
       if is_valid:
           click.echo("✅ Scenario is valid")
       else:
           click.echo("❌ Validation failed:")
           for error in errors:
               click.echo(f"  {error}")
   ```

2. **Register in main CLI**: `src/waft/cli/__init__.py`
   ```python
   from .scenario_commands import scenario

   cli.add_command(scenario)
   ```

3. **Add to README.md** under Commands section

## Interaction with Existing Systems

### 1. Integration with `ScenarioDecisionTree`

The ML-based decision tree from `scenario_decision_tree.py` could enhance L1 scenarios:

```python
from waft.core.scenario_formats import ElevntyCYOAScenario
from waft.core.scenario_decision_tree import ScenarioDecisionTree, ScenarioState

# Load L1 scenario
scenario = ElevntyCYOAScenario(Path("my_scenario"))

# Train decision tree on player behavior (future enhancement)
tree = ScenarioDecisionTree()

# Run with ML recommendations
current_node = scenario.get_start_node()
state = ScenarioState(
    sequence_id=current_node.id,
    sequence_type="ordinary",
    containers={},
    visited_sequences=[],
    choice_history=[],
    available_choices=[c.path for c in current_node.choices]
)

# Get AI recommendation
recommendation = tree.recommend_choice(state)
if recommendation:
    choice_letter, confidence = recommendation
    print(f"AI suggests: {choice_letter} (confidence: {confidence:.2f})")
```

**Status**: Not implemented, but architecture supports it

### 2. Integration with `ScenarioOrchestrator`

The orchestrator could support L1 scenarios alongside L3:

```python
from waft.core.dnd_scenario import ScenarioOrchestrator
from waft.core.scenario_formats import ElevntyCYOAParser

class EnhancedOrchestrator(ScenarioOrchestrator):
    def run_scenario(self, mode: str, scenario_path: str | None = None):
        if mode == "eleventy" and scenario_path:
            # Run L1 scenario
            scenario = ElevntyCYOAParser.load_scenario(scenario_path)
            scenario.run_interactive()
        else:
            # Existing L3 scenario logic
            super().run_scenario(mode)
```

**Status**: Possible future enhancement

### 3. Conversion to WAFT Native (L1 → L3)

Could build a converter that takes L1 scenarios and creates L3 Python code:

```python
from waft.core.scenario_formats import ElevntyCYOAParser
from waft.core.scenario_formats.converters import L1toL3Converter

# Load L1 scenario
scenario = ElevntyCYOAParser.load_scenario("my_scenario")

# Convert to L3 (WAFT Native)
converter = L1toL3Converter()
python_code = converter.convert(scenario)

# Writes Python files with DND mechanics
converter.write_to_realm("_realms/my_campaign")
```

**Status**: Not implemented, future consideration

## Testing

### Unit Tests

```python
# tests/test_eleventy_cyoa.py
import pytest
from pathlib import Path
from waft.core.scenario_formats import ElevntyCYOAParser

def test_load_valid_scenario():
    scenario = ElevntyCYOAParser.load_scenario("examples/eleventy_cyoa_demo")
    assert scenario.start_node_id == "start"
    assert len(scenario.nodes) == 7

def test_validate_broken_links():
    is_valid, errors = ElevntyCYOAParser.validate_scenario("tests/fixtures/broken_scenario")
    assert not is_valid
    assert any("broken link" in err.lower() for err in errors)

def test_ending_detection():
    scenario = ElevntyCYOAParser.load_scenario("examples/eleventy_cyoa_demo")
    retreat_node = scenario.get_node("retreat")
    assert retreat_node.is_ending
```

### Integration Tests

```python
# tests/integration/test_scenario_playthrough.py
def test_full_playthrough():
    scenario = ElevntyCYOAParser.load_scenario("examples/eleventy_cyoa_demo")

    # Simulate player choices
    current = scenario.get_start_node()
    assert current.id == "start"

    # Choice 1: Enter dark passage
    next_node = scenario.get_node(current.choices[0].path)
    assert next_node.id == "dark_passage"

    # Choice 2: Examine mushrooms
    ending = scenario.get_node(next_node.choices[0].path)
    assert ending.is_ending
    assert ending.id == "mushroom_grove"
```

## Documentation Updates

### Files to Update

1. **README.md**: Add scenario commands section
2. **CHANGELOG.md**: Document new feature
3. **docs/SCENARIO_FORMAT_SPEC.md**: ✅ Already created
4. **docs/ELEVENTY_CYOA_INTEGRATION.md**: ✅ This file

### Example README.md Addition

```markdown
## Scenario Commands

### `waft scenario run <path>`

Run an interactive scenario:

```bash
waft scenario run examples/eleventy_cyoa_demo
```

Supports multiple formats:
- **Level 1 (Eleventy CYOA)**: Simple Markdown + YAML branching
- **Level 2 (Ink)**: Coming soon
- **Level 3 (WAFT Native)**: Full DND mechanics

See [SCENARIO_FORMAT_SPEC.md](docs/SCENARIO_FORMAT_SPEC.md) for details.
```

## Example Use Cases

### 1. Quick Story Prototyping

Writers can draft branching narratives without learning Python:

```bash
mkdir my_story
cd my_story

# Create start.md
cat > start.md << 'EOF'
---
title: The Beginning
choices:
  - text: Go left
    path: left
  - text: Go right
    path: right
---

Your journey begins...
EOF

# Create endings
cat > left.md << 'EOF'
---
title: The Left Path
---

You chose wisely. The end.
EOF

cat > right.md << 'EOF'
---
title: The Right Path
---

You chose poorly. The end.
EOF

# Validate and run
waft scenario validate .
waft scenario run .
```

### 2. AI-Generated Content

LLMs can easily generate valid L1 scenarios:

```python
from anthropic import Anthropic
from waft.core.scenario_formats import ElevntyCYOAParser

client = Anthropic()

prompt = """Generate a 5-node CYOA scenario about exploring a haunted house.
Use the Eleventy CYOA format (Markdown + YAML front matter).
Create: start.md, hallway.md, basement.md, attic.md, escape.md"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": prompt}]
)

# Parse generated content, save to files
# Then validate
is_valid, errors = ElevntyCYOAParser.validate_scenario("haunted_house")
```

### 3. Decision Tree Documentation

Technical writers can create interactive troubleshooting guides:

```yaml
---
title: Server Not Starting
choices:
  - text: Check if port 8080 is available
    path: check_port
  - text: Review application logs
    path: check_logs
---

Your server failed to start. What do you want to check first?
```

## Performance Considerations

### Scenario Loading

- **L1 scenarios load fast**: Simple file I/O + YAML parsing
- **No database required**: Pure filesystem-based
- **Validation is cheap**: O(n) graph traversal where n = nodes

### Memory Footprint

```python
# Rough estimate for a 100-node scenario:
# - 100 markdown files (~1KB each) = 100KB
# - Parsed nodes in memory = ~200KB
# - Total: < 1MB for typical scenario
```

### Comparison to L3

| Metric | L1 (Eleventy) | L3 (WAFT Native) |
|--------|--------------|------------------|
| **Load Time** | <100ms | ~500ms (DB queries) |
| **Memory** | ~1MB per 100 nodes | ~10MB (party state, ML models) |
| **Startup** | Instant | Moderate (Realm initialization) |
| **Validation** | Fast (graph check) | Complex (schema + mechanics) |

## Migration Strategy

If you want to replace existing WAFT scenarios with L1 format:

### Option 1: Keep Both Systems

**Recommended**: L1 and L3 serve different purposes.

- Use L1 for: Story drafts, simple narratives, AI content
- Use L3 for: Full RPG campaigns, ML-driven gameplay

### Option 2: Gradual Migration

1. Identify simple scenarios in existing DND system
2. Convert to L1 Markdown format
3. Keep complex scenarios in L3
4. Use L2 (Ink) as middle ground when ready

### Option 3: Hybrid Approach

L1 scenarios could trigger L3 encounters:

```yaml
---
title: The Dragon's Lair
choices:
  - text: Fight the dragon
    path: encounter:dragon_battle  # Triggers L3 encounter
  - text: Sneak past
    path: sneak_path
---

You enter the dragon's lair...
```

**Status**: Not implemented, possible future feature

## Benefits for WAFT

1. **Lower Barrier to Entry**
   - Non-programmers can create content
   - Markdown is familiar to most writers
   - AI can generate valid scenarios trivially

2. **Rapid Prototyping**
   - Draft story flow in minutes
   - Validate graph structure instantly
   - Iterate without restarting Python

3. **Version Control Friendly**
   - Plain text Markdown
   - Easy to diff and review
   - Git-friendly

4. **Complements Existing Systems**
   - Doesn't replace L3 (WAFT Native)
   - Adds new use cases
   - Enables gradual complexity scaling

## Future Enhancements

### 1. Visual Scenario Editor

Web-based editor for creating L1 scenarios:
- Node graph visualization
- Markdown editor with live preview
- Drag-and-drop choice connections
- One-click validation

### 2. Scenario Analytics

Track player behavior across playthroughs:
- Most common paths
- Dead-end frequency
- Average session length
- Choice popularity heatmap

### 3. L1 → L2 → L3 Pipeline

Automated upgrade tools:
```bash
waft scenario upgrade my_scenario --to-ink    # L1 → L2
waft scenario upgrade my_scenario --to-native # L2 → L3
```

### 4. Scenario Marketplace

Share and discover scenarios:
```bash
waft scenario install "mysteries/haunted-mansion"
waft scenario publish my_scenario
```

## Conclusion

The Eleventy CYOA integration provides:
- ✅ **Minimal implementation** (~200 LOC)
- ✅ **Zero breaking changes** to existing code
- ✅ **Clear use case** (rapid prototyping)
- ✅ **Extensible architecture** for L2/L3
- ✅ **AI-friendly format** for generation

**Next Steps**:
1. Add CLI commands (`waft scenario run/validate`)
2. Write comprehensive tests
3. Update README.md
4. Consider L2 (Ink) integration
5. Gather user feedback

---

*Last updated: 2026-01-24*
