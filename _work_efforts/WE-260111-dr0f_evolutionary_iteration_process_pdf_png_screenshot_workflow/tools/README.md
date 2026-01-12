# WE-260111-dr0f Tooling

**Work Effort**: Evolutionary Iteration Process - PDF PNG Screenshot Workflow  
**Purpose**: Tools for working on this work effort

---

## Available Tools

### 1. `compare_pngs.py` - PNG Comparison Tool
**Status**: 🚧 To be created (TKT-dr0f-003)

Compare two PNG images and generate:
- Side-by-side HTML view
- Diff image (highlighting differences)
- Metrics report (similarity score, differences)

**Usage**:
```bash
python tools/compare_pngs.py before.png after.png --output comparison.html
```

### 2. `generate_test_pdfs.py` - Test PDF Generator
**Status**: ✅ Available

Generate test PDFs with different styling for comparison testing.

**Usage**:
```bash
python tools/generate_test_pdfs.py --count 5 --output test_outputs/
```

### 3. `batch_compare.py` - Batch Comparison Tool
**Status**: 🚧 To be created (TKT-dr0f-005)

Compare multiple PDF/PNG pairs in batch.

**Usage**:
```bash
python tools/batch_compare.py --input test_outputs/ --output batch_results/
```

### 4. `fitness_calculator.py` - Visual Appeal Fitness
**Status**: 🚧 To be created (TKT-dr0f-004)

Calculate fitness score based on visual appeal metrics.

**Usage**:
```bash
python tools/fitness_calculator.py image.png --metrics contrast,balance,readability
```

---

## Work Effort Status Tracker

### Quick Status Check
```bash
python tools/status.py
```

Shows:
- Ticket completion status
- Files changed per ticket
- Next steps
- Blockers

---

## Data Generation Tools

### Generate Test Data
```bash
# Generate test PDFs with PNGs
python tools/generate_test_pdfs.py --count 10

# Compare all generated PDFs
python tools/batch_compare.py --input test_outputs/

# Calculate fitness scores
python tools/fitness_calculator.py test_outputs/*.png
```

### Play and Experiment
```bash
# Interactive comparison tool
python tools/interactive_compare.py

# Visual fitness explorer
python tools/fitness_explorer.py
```

---

## Hypothesis Generation Tools

### Generate Hypothesis from Data
```bash
# Analyze comparison results and generate hypothesis
python tools/hypothesis_generator.py --data batch_results/ --output hypothesis.md
```

### Test Hypothesis
```bash
# Run hypothesis tests
python tools/test_hypothesis.py hypothesis.md --iterations 10
```

---

## Next Steps

1. Create `compare_pngs.py` (TKT-dr0f-003)
2. Create `batch_compare.py` (TKT-dr0f-005)
3. Create `fitness_calculator.py` (TKT-dr0f-004)
4. Create hypothesis generation tools
5. Create interactive exploration tools

---

**These tools enable the evolutionary iteration process: Generate → Visualize → Compare → Iterate → Evolve**
