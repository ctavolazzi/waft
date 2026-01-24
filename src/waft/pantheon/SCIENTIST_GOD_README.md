# Scientist God - Quick Reference

## What It Does

**Scientist God** manages the complete scientific research lifecycle with rigor that would make Chief Wiggum weep. 🔬

## Features

✅ **Hypothesis Management** - Generate, track, and test hypotheses  
✅ **Experiment Design** - Structure investigations systematically  
✅ **Evidence Collection** - Organize supporting/contradicting data  
✅ **Whitepaper Generation** - Auto-create publication-quality docs  
✅ **Oracle Integration** - Track epistemic state  
✅ **Publication Workflow** - Manage research outputs  

## Quick Start

```python
from pathlib import Path
from waft.pantheon.scientist_god import ScientistGod, EvidenceType

# Initialize
scientist = ScientistGod(project_path=Path("/your/project"))

# 1. Create hypothesis
hyp = scientist.hypothesize(
    statement="System X uses algorithm Y",
    expected_confidence=0.7
)

# 2. Design experiment
exp = scientist.design_experiment(
    hypothesis=hyp,
    name="System X Algorithm Verification",
    methodology="Inspect code, run tests, analyze performance"
)

# 3. Collect evidence
scientist.collect_evidence(
    experiment=exp,
    evidence_type=EvidenceType.SOURCE_CODE,
    location="src/system_x.py:42-67",
    content="def algorithm_y()...",
    supports=True  # Evidence supports hypothesis
)

scientist.collect_evidence(
    experiment=exp,
    evidence_type=EvidenceType.TEST_OUTPUT,
    location="pytest tests/test_algorithm.py",
    content="10 passed in 0.5s",
    supports=True
)

# 4. Generate whitepaper
wp_dir = scientist.generate_whitepaper(
    experiment=exp,
    title="System X Analysis",
    author="Your Name",
    auto_populate=True  # Auto-fill sections with evidence
)

# 5. Compile to PDF
pdf_path = scientist.compile_whitepaper(exp)

# 6. Publish
publication = scientist.publish(
    experiment=exp,
    publish_to="github"
)
```

## Evidence Types

- `SOURCE_CODE` - Verified code snippets
- `TEST_OUTPUT` - Test results (pytest, etc.)
- `TELEMETRY_DATA` - Logs, metrics, traces
- `BENCHMARK_RESULT` - Performance data
- `USER_STUDY` - User feedback/studies
- `COMPARATIVE_ANALYSIS` - Comparisons with other systems

## Integration with Whitepaper Generator

Scientist God **automatically uses** the `whitepaper_generator.py` tool:

```python
# Looks for tool at:
project_path / "tools" / "whitepaper_generator.py"

# Or specify custom path:
scientist = ScientistGod(
    project_path=Path("/project"),
    whitepaper_generator_path=Path("/custom/path/to/generator.py")
)
```

**Auto-population creates:**
- Abstract with hypothesis statement
- Evidence sections with all collected data
- Findings with confidence metrics
- Professional Typst formatting

## File Structure

Scientist God creates:

```
your-project/
└── .science/
    ├── hypotheses/
    │   └── hyp_20260124_120000.json
    ├── experiments/
    │   └── exp_20260124_120100.json
    ├── whitepapers/
    │   └── exp_20260124_120100/
    │       ├── whitepaper_config.yaml
    │       ├── sections/
    │       │   ├── 01_abstract.typ (auto-populated!)
    │       │   ├── 30_findings.typ (auto-populated!)
    │       │   └── ...
    │       └── *_COMPLETE.pdf (compiled output)
    └── publications.jsonl
```

## Status Checking

```python
# Check all scientific work
status = scientist.status()

print(status)
# {
#   "hypotheses": {
#     "total": 5,
#     "by_status": {"completed": 3, "running": 2}
#   },
#   "experiments": {
#     "total": 5,
#     "by_status": {"completed": 2, "running": 3},
#     "with_whitepapers": 2
#   },
#   "whitepapers": 2
# }
```

## With Oracle Integration

```python
from waft.core.science.oracle import TheOracle

oracle = TheOracle(project_path=Path("/project"))
scientist = ScientistGod(
    project_path=Path("/project"),
    oracle=oracle  # Pass Oracle instance
)

# Now all findings auto-log to Oracle's epistemic journal!
hyp = scientist.hypothesize("System works")
# → Logged to Oracle with confidence score

scientist.collect_evidence(...)
# → Logged to Oracle with impact assessment
```

## Real-World Example: WAFT Analysis

```python
scientist = ScientistGod(project_path=Path("/Users/you/waft"))

# Hypothesis: RPG Gym exists and works
hyp = scientist.hypothesize(
    "WAFT has a functional RPG Gym with Scint detection",
    expected_confidence=0.5  # Unsure at first
)

exp = scientist.design_experiment(
    hypothesis=hyp,
    name="RPG Gym Discovery",
    methodology="Search codebase, run tests, verify implementation"
)

# Found the evidence!
scientist.collect_evidence(
    exp, EvidenceType.SOURCE_CODE,
    "src/gym/rpg/scint.py:21-30",
    "class ScintType(Enum): SYNTAX_TEAR = auto()...",
    supports=True
)

scientist.collect_evidence(
    exp, EvidenceType.TEST_OUTPUT,
    "pytest tests/test_scint_mechanics.py",
    "5 passed in 0.23s",
    supports=True
)

# Confidence updated from evidence: 0.5 → 1.0 (2 supporting, 0 against)
print(f"Confidence: {hyp.confidence:.1%}")  # "100%"

# Generate 15-page deep-dive whitepaper
wp_dir = scientist.generate_whitepaper(
    exp, "WAFT RPG Gym Analysis", "Dr. Aria Vex"
)

# Compile and publish
scientist.compile_whitepaper(exp)
scientist.publish(exp, publish_to="github")
```

## Benefits Over Manual Process

**Before (manual):**
1. Create hypothesis in head
2. Collect evidence in random files
3. Manually write whitepaper
4. Manually track what you tested
5. Lose track of confidence levels
6. Forget what evidence you found

**After (Scientist God):**
1. `scientist.hypothesize("statement")`
2. `scientist.collect_evidence(...)`
3. `scientist.generate_whitepaper(...)` ← Auto-populated!
4. `scientist.status()` ← Always know where you are
5. Confidence auto-calculated from evidence
6. Everything tracked in `.science/`

## Why It's Not Chief Wiggum

**Chief Wiggum:** "Bake 'em away, toys!"  
**Scientist God:** "Let me rigorously verify that hypothesis with reproducible evidence."

**Chief Wiggum:** *Loses all case files*  
**Scientist God:** *Everything tracked in `.science/` with timestamps*

**Chief Wiggum:** "Close enough!"  
**Scientist God:** *Calculates exact confidence: 0.847*

**Chief Wiggum:** *No documentation*  
**Scientist God:** *Auto-generates professional whitepapers*

---

**Result:** Actual scientific rigor instead of... whatever Chief Wiggum does. 👮❌ → 🔬✅
