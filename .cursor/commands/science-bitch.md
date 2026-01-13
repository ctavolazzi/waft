# Science-Bitch

**Full scientific method workflow for hypothesis testing, experimentation, and evidence-based conclusions.**

Runs the complete scientific method workflow: form hypothesis, design experiment, capture states (A & B), collect data (C), analyze results, and generate reports.

**Use when:** Need to run systematic experiments, test hypotheses, collect evidence-based data, or generate scientific reports.

---

## Purpose

This command provides:
- **Complete Scientific Method**: Full workflow from hypothesis to conclusion
- **State Capture**: Initial state (A) and final state (B) tracking
- **Data Collection**: Systematic data collection during experiments (C)
- **Hypothesis Testing**: Form, test, and verify hypotheses
- **Report Generation**: Generate field guides and project status reports
- **Evidence-Based Analysis**: Systematic analysis with traceable evidence

---

## Quick Start

### Interactive Workflow
```
/science-bitch
```

Runs the complete interactive scientific method workflow.

### Generate Field Guide
```
/science-bitch --field-guide
```

Generates comprehensive field guide PDF.

### Generate Project Status Report
```
/science-bitch --report
```

Generates project status report PDF.

### With Hypothesis
```
/science-bitch --hypothesis "Higher skill improves outcomes"
```

Starts workflow with a pre-defined hypothesis.

### Run Experiment
```
/science-bitch --run
```

Runs experiment directly.

---

## Workflow Sequence

### Phase 1: Form Hypothesis

**Purpose**: Create a testable hypothesis

**Process**:
1. Identify the question or phenomenon to investigate
2. Formulate a clear, testable hypothesis
3. Define variables (independent, dependent, control)
4. Specify what would verify or refute the hypothesis

**Output**: Hypothesis object with statement, variables, and verification plan

---

### Phase 2: Design Experiment

**Purpose**: Create experiment design based on hypothesis

**Process**:
1. Define experiment structure
2. Specify variables and their types
3. Design data collection methods
4. Plan state capture points (A and B)
5. Define success criteria

**Output**: Experiment design with variables, data collection plan, and state capture strategy

---

### Phase 3: Capture Initial State (A)

**Purpose**: Capture system state before experiment

**Process**:
1. Identify components to track
2. Capture initial state snapshot
3. Generate state hash for comparison
4. Save state to `_science/experiments/[exp_id]/state_a.json`

**Output**: Initial state snapshot with hash

---

### Phase 4: Run Experiment

**Purpose**: Execute experiment with data collection

**Process**:
1. Execute experiment according to design
2. Collect data points during execution (C)
3. Record measurements and observations
4. Track experiment progress
5. Handle errors and edge cases

**Output**: Experiment results with collected data

---

### Phase 5: Collect Data (C)

**Purpose**: Systematic data collection during experiment

**Data Collected**:
- Measurements at specified intervals
- Observations and notes
- Performance metrics
- State changes
- Error conditions
- Timestamps for all data points

**Storage**: Data saved to `_science/data/[exp_id]/`

**Output**: Data series with timestamps and metadata

---

### Phase 6: Capture Final State (B)

**Purpose**: Capture system state after experiment

**Process**:
1. Capture final state snapshot
2. Generate state hash for comparison
3. Compare with initial state (A)
4. Identify changes
5. Save state to `_science/experiments/[exp_id]/state_b.json`

**Output**: Final state snapshot with comparison to initial state

---

### Phase 7: Analyze Results

**Purpose**: Analyze experiment data and verify/refute hypothesis

**Analysis Performed**:
1. Compare states A and B
2. Analyze collected data (C)
3. Verify or refute hypothesis
4. Calculate confidence level
5. Generate conclusions
6. Identify patterns and insights

**Output**: Analysis report with:
- Hypothesis verification status
- Confidence level
- Conclusions
- Recommendations
- Evidence summary

---

### Phase 8: Generate Reports

**Purpose**: Create comprehensive documentation

**Report Types**:

#### Field Guide
- Complete usage guide
- Workflow documentation
- Examples and best practices
- Command reference

#### Project Status Report
- Current project state
- Goals and objectives
- Evidence collected
- Next steps
- Progress tracking

**Output**: PDF reports in `_science/reports/`

---

## Complete Execution Sequence

```
1. Form Hypothesis          → Create testable hypothesis
2. Design Experiment        → Plan experiment structure
3. Capture State A          → Initial state snapshot
4. Run Experiment           → Execute with data collection
5. Collect Data C           → Systematic measurements
6. Capture State B          → Final state snapshot
7. Analyze Results          → Verify/refute hypothesis
8. Generate Reports            → Create documentation
```

---

## Command Options

### Interactive Workflow (Default)
```
/science-bitch
```

Runs complete interactive workflow with prompts for each phase.

### Generate Field Guide
```
/science-bitch --field-guide
```

Generates comprehensive field guide PDF showing how to use the command.

**Output**: `_science/reports/field_guide.pdf`

### Generate Project Status Report
```
/science-bitch --report
```

Generates project status report PDF with current state, goals, and progress.

**Output**: `_science/reports/project_status.pdf`

### With Pre-Defined Hypothesis
```
/science-bitch --hypothesis "Your hypothesis statement here"
```

Starts workflow with a hypothesis already defined.

### Run Experiment Directly
```
/science-bitch --run
```

Runs experiment without interactive prompts (uses existing hypothesis/design).

### Specify Project Path
```
/science-bitch --path /path/to/project
```

Runs command in specified project directory (default: current directory).

---

## Usage Examples

### Example 1: Full Interactive Workflow
```
/science-bitch
```

**What it does**:
1. Prompts for hypothesis formation
2. Guides through experiment design
3. Captures initial state (A)
4. Runs experiment with data collection (C)
5. Captures final state (B)
6. Analyzes results
7. Generates report

**Output**: Complete experiment with analysis and report

### Example 2: Generate Field Guide
```
/science-bitch --field-guide
```

**What it does**:
- Generates comprehensive field guide PDF
- Documents all workflow phases
- Provides examples and best practices
- Includes command reference

**Output**: `_science/reports/field_guide.pdf`

### Example 3: Generate Status Report
```
/science-bitch --report
```

**What it does**:
- Generates project status report PDF
- Shows current state and goals
- Documents evidence collected
- Lists next steps

**Output**: `_science/reports/project_status.pdf`

### Example 4: Hypothesis-Driven Experiment
```
/science-bitch --hypothesis "Increasing iteration count improves fitness scores"
```

**What it does**:
- Starts with pre-defined hypothesis
- Skips hypothesis formation phase
- Proceeds directly to experiment design
- Runs complete workflow

**Output**: Experiment results testing the specified hypothesis

---

## Scientific Method Cycle

The command implements the complete scientific method:

1. **Observe**: Identify phenomenon or question
2. **Hypothesize**: Form testable hypothesis
3. **Design**: Create experiment with variables
4. **Capture State A**: Initial system state
5. **Run Experiment**: Execute with data collection
6. **Collect Data C**: Measurements during experiment
7. **Capture State B**: Final system state
8. **Analyze**: Verify/refute hypothesis
9. **Report**: Generate conclusions and documentation
10. **Iterate**: Modify variables and repeat

---

## File Structure

```
_science/
├── README.md                    # Overview and quick start
├── experiments/                 # Experiment definitions and results
│   ├── [exp_id]/               # Individual experiment
│   │   ├── experiment.json     # Experiment definition
│   │   ├── state_a.json        # Initial state (A)
│   │   ├── state_b.json        # Final state (B)
│   │   └── results.json        # Experiment results
├── data/                        # Collected data (C)
│   └── [exp_id]/               # Data for each experiment
│       └── data_series.json   # Collected measurements
├── reports/                     # Generated reports
│   ├── field_guide.pdf         # Usage guide
│   ├── field_guide.md          # Source markdown
│   ├── project_status.pdf      # Status report
│   └── project_status.md       # Source markdown
└── tools/                       # Helper utilities
    ├── generate_field_guide_pdf.py
    └── generate_status_pdf.py
```

---

## Integration

This command integrates with:
- **Scientific Method Tool**: `scientific_method_tool/` provides core functionality
- **PDF Generation**: Uses `waft.evolution.pdf_generator` for reports
- **Work Efforts**: Tracks progress in `WE-260112-az3z`
- **State Capture**: Captures system states before/after experiments
- **Data Collection**: Records all measurements during experiments

---

## When to Use

**Use `/science-bitch` when**:
- ✅ Need to test a hypothesis systematically
- ✅ Want to run controlled experiments
- ✅ Need evidence-based conclusions
- ✅ Want to track state changes (A → B)
- ✅ Need systematic data collection
- ✅ Want to generate scientific reports
- ✅ Need to verify or refute a hypothesis

**Don't use `/science-bitch` when**:
- ❌ Just need quick testing (use direct testing)
- ❌ Don't need systematic approach
- ❌ Hypothesis is already verified
- ❌ Just need data collection (use data tools directly)
- ❌ Time-constrained (full workflow takes time)

---

## Output Summary

After completion, provides:
1. **Hypothesis**: Testable hypothesis statement
2. **Experiment Design**: Complete experiment structure
3. **State Snapshots**: Initial (A) and final (B) states
4. **Collected Data**: All measurements (C)
5. **Analysis**: Hypothesis verification/refutation with confidence
6. **Report**: Comprehensive documentation (if requested)

---

## Best Practices

1. **Clear Hypotheses**: Formulate specific, testable hypotheses
2. **Systematic Design**: Plan experiments carefully
3. **Complete State Capture**: Capture all relevant components
4. **Thorough Data Collection**: Collect data at appropriate intervals
5. **Careful Analysis**: Verify all claims with evidence
6. **Document Everything**: Generate reports for future reference
7. **Iterate**: Refine hypotheses and experiments based on results

---

## Implementation Details

### CLI Command
The command wraps the `waft science-bitch` CLI command:
- **Location**: `src/waft/main.py` (line 2144)
- **Manager**: `src/waft/core/science_bitch.py`
- **Work Effort**: `WE-260112-az3z`

### Execution
When `/science-bitch` is executed:
1. AI reads this command file
2. Executes `waft science-bitch` with appropriate options
3. Processes results and displays output
4. Generates reports if requested

### Options Mapping
- `/science-bitch` → `waft science-bitch` (interactive)
- `/science-bitch --field-guide` → `waft science-bitch --field-guide`
- `/science-bitch --report` → `waft science-bitch --report`
- `/science-bitch --hypothesis "..."` → `waft science-bitch --hypothesis "..."`
- `/science-bitch --run` → `waft science-bitch --run`

---

## Related Commands

- **`/hypothesis`**: Form and verify hypotheses (complementary workflow)
- **`/prove-it`**: Prove scientific method tool works
- **`/verify`**: Verify claims with evidence
- **`/analyze`**: Analyze data and generate insights

---

## Troubleshooting

**Error: Command not found**
- Solution: Ensure you're in a project with `waft` installed
- Check: `waft --help` should show `science-bitch` command

**Error: ImportError**
- Solution: Ensure scientific_method_tool is available
- Check: `python3 -c "from scientific_method_tool import Hypothesis"`

**Error: Permission denied**
- Solution: Check file permissions on `_science/` directory
- Fix: `chmod -R u+w _science/`

**Error: State capture failed**
- Solution: Ensure components exist and are accessible
- Check: Verify component paths and permissions

---

**This command provides a complete scientific method workflow from hypothesis formation through experiment execution, data collection, state tracking, analysis, and reporting - perfect for systematic hypothesis testing and evidence-based conclusions.**

---

End Command ---
