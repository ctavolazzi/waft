# Science-Bitch: Scientific Method Command

**Purpose**: Full scientific method workflow for hypothesis testing, experimentation, and evidence-based conclusions.

**Work Effort**: [WE-260112-az3z](../_work_efforts/WE-260112-az3z_science_bitch_command_full_scientific_method_cli/WE-260112-az3z_index.md)

---

## Quick Start

```bash
# Run full scientific method workflow
waft science-bitch

# Create new hypothesis
waft science-bitch --hypothesis "Higher skill improves outcomes"

# Run experiment
waft science-bitch --run

# Generate report
waft science-bitch --report

# Generate field guide
waft science-bitch --field-guide
```

---

## Structure

```
_science/
├── README.md              # This file
├── experiments/           # Experiment definitions and results
├── data/                  # Collected data (C)
├── reports/               # Generated reports and PDFs
└── tools/                 # Helper tools and utilities
```

---

## Scientific Method Workflow

1. **Observe**: Identify phenomenon or question
2. **Hypothesize**: Form testable hypothesis
3. **Design**: Create experiment with variables
4. **Capture State A**: Initial system state
5. **Run Experiment**: Execute with data collection
6. **Collect Data C**: Measurements during experiment
7. **Capture State B**: Final system state
8. **Analyze**: Verify/refute hypothesis
9. **Report**: Generate conclusions and documentation

---

## Integration

- **Scientific Method Tool**: `scientific_method_tool/` provides core functionality
- **PDF Generation**: Uses `waft.evolution.pdf_generator` for reports
- **Work Efforts**: Tracks progress in `WE-260112-az3z`
- **State Capture**: Captures system states before/after experiments
- **Data Collection**: Records all measurements during experiments

---

## Documentation

- **Field Guide**: `reports/field_guide.pdf` - How to use the command
- **Project Status**: `reports/project_status.pdf` - Current state and goals
- **Work Effort**: See linked work effort for tickets and progress

---

## Tools

Located in `tools/`:
- Experiment management utilities
- Data analysis helpers
- Report generation scripts
- State comparison tools

---

**Status**: ✅ Core Complete - Field Guide & Project Status PDFs Generated

**Last Updated**: 2026-01-12

---

## Generated PDFs

- **Field Guide**: `reports/field_guide.pdf` - Complete usage guide
- **Project Status**: `reports/project_status.pdf` - Current state, goals, evidence, next steps

Generate with:
```bash
waft science-bitch --field-guide
waft science-bitch --report
```
