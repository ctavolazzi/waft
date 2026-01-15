# Science-Bitch Field Guide

**Version**: 1.0  
**Date**: 2026-01-14

---

## Overview

Science-Bitch is a command-line tool that implements the full scientific method workflow for hypothesis testing, experimentation, and evidence-based conclusions.

---

## Quick Start

```bash
# Run full interactive workflow
waft science-bitch

# Generate field guide (this document)
waft science-bitch --field-guide

# Generate project status report
waft science-bitch --report
```

---

## Scientific Method Workflow

### 1. Form Hypothesis

Create a testable hypothesis with:
- **Statement**: What you're testing
- **Prediction**: Expected outcome
- **Variables**: Independent, dependent, and control variables

### 2. Design Experiment

Design an experiment that:
- Tests your hypothesis
- Controls for confounding variables
- Collects measurable data

### 3. Capture Initial State (A)

Before running the experiment:
- Capture system state
- Record baseline measurements
- Document initial conditions

### 4. Run Experiment

Execute the experiment:
- Use controlled variables
- Collect data during execution
- Record all measurements

### 5. Collect Data (C)

During the experiment:
- Record all measurements
- Track dependent variables
- Note any observations

### 6. Capture Final State (B)

After the experiment:
- Capture final system state
- Compare with initial state
- Identify changes

### 7. Analyze Results

Analyze collected data:
- Verify or refute hypothesis
- Calculate confidence
- Draw conclusions

### 8. Generate Report

Create documentation:
- Experiment report
- Analysis results
- Recommendations

---

## Command Options

### `waft science-bitch`

Run full interactive workflow:
1. Form hypothesis interactively
2. Design experiment
3. Run experiment
4. Analyze results
5. Generate report

### `waft science-bitch --field-guide`

Generate this field guide as PDF.

### `waft science-bitch --report`

Generate project status report PDF.

---

## File Structure

```
_science/
├── README.md              # Overview and quick start
├── experiments/           # Experiment definitions
├── data/                  # Collected data (C)
├── reports/               # Generated reports
│   ├── field_guide.pdf    # This guide
│   ├── project_status.pdf # Status report
│   └── experiment_*.md    # Experiment reports
└── tools/                  # Helper utilities
```

---

## Integration

- **Scientific Method Tool**: Core functionality from `scientific_method_tool/`
- **PDF Generation**: Uses `waft.evolution.pdf_generator`
- **Work Effort**: Tracked in `WE-260112-az3z`
- **State Capture**: Automatic state snapshots
- **Data Collection**: Comprehensive data recording

---

## Best Practices

1. **Clear Hypotheses**: Make hypotheses specific and testable
2. **Control Variables**: Keep control variables constant
3. **Multiple Trials**: Run multiple experiments for reliability
4. **Document Everything**: Record all observations
5. **Analyze Thoroughly**: Don't skip the analysis step

---

## Troubleshooting

**Command not found**: Ensure you're in the project root and dependencies are installed.

**Import errors**: Run `uv pip install jinja2 weasyprint markdown`

**PDF generation fails**: Check that WeasyPrint is installed and working.

---

## Examples

See `scientific_method_tool/example_usage.py` for complete examples.

---

**For more information, see the work effort: WE-260112-az3z**

