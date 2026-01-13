# Science-Bitch: A Comprehensive Research Guide

**A Complete Scientific Method Workflow Tool for Hypothesis Testing, Experimentation, and Evidence-Based Research**

---

**Version**: 1.0  
**Date**: 2026-01-12  
**Author**: WAFT Research Team  
**Document Type**: Research Booklet

---

## Executive Summary

Science-Bitch is a comprehensive command-line tool that implements the complete scientific method workflow for systematic hypothesis testing, controlled experimentation, and evidence-based conclusions. This research booklet provides a complete guide to understanding, using, and extending the Science-Bitch system.

### Key Features

- **Complete Scientific Method Implementation**: Full workflow from hypothesis formation to conclusion
- **State Capture System**: Automatic tracking of system states before (A) and after (B) experiments
- **Systematic Data Collection**: Comprehensive data collection during experiments (C)
- **Hypothesis Testing Framework**: Structured approach to forming, testing, and verifying hypotheses
- **Automated Report Generation**: Professional PDF reports with full documentation
- **Evidence-Based Analysis**: Systematic analysis with traceable evidence chains

---

## Table of Contents

1. [Introduction](#introduction)
2. [Scientific Method Overview](#scientific-method-overview)
3. [Architecture and Design](#architecture-and-design)
4. [Workflow Phases](#workflow-phases)
5. [State Capture System](#state-capture-system)
6. [Data Collection Framework](#data-collection-framework)
7. [Hypothesis Testing](#hypothesis-testing)
8. [Report Generation](#report-generation)
9. [Integration with WAFT](#integration-with-waft)
10. [Use Cases and Examples](#use-cases-and-examples)
11. [Best Practices](#best-practices)
12. [Technical Implementation](#technical-implementation)
13. [Future Directions](#future-directions)
14. [Conclusion](#conclusion)

---

## 1. Introduction

### What is Science-Bitch?

Science-Bitch is a command-line tool that provides a structured, systematic approach to scientific research and experimentation. It implements the complete scientific method workflow, from initial hypothesis formation through experiment execution, data collection, analysis, and report generation.

### Why Science-Bitch?

Traditional research workflows often lack:
- **Systematic State Tracking**: No clear before/after snapshots
- **Structured Data Collection**: Ad-hoc data recording
- **Evidence Chains**: Difficult to trace conclusions back to data
- **Automated Documentation**: Manual report generation

Science-Bitch addresses these gaps by providing:
- **Automatic State Capture**: System snapshots at key points (A and B)
- **Structured Data Collection**: Systematic measurement recording (C)
- **Traceable Evidence**: Complete chains from hypothesis to conclusion
- **Automated Reports**: Professional PDF documentation

### Target Audience

- **Researchers**: Scientists conducting systematic experiments
- **Developers**: Engineers testing hypotheses about code/system behavior
- **Data Scientists**: Analysts needing structured experimentation workflows
- **Students**: Learners practicing the scientific method
- **Teams**: Groups needing standardized research processes

---

## 2. Scientific Method Overview

### The Scientific Method

The scientific method is a systematic approach to understanding the natural world through observation, hypothesis formation, experimentation, and analysis. Science-Bitch implements this complete cycle:

```
1. Observe      → Identify phenomenon or question
2. Hypothesize  → Form testable hypothesis
3. Design       → Create experiment with variables
4. Capture A    → Initial system state
5. Run          → Execute experiment
6. Collect C    → Data during experiment
7. Capture B    → Final system state
8. Analyze      → Verify/refute hypothesis
9. Report       → Generate conclusions
10. Iterate     → Refine and repeat
```

### Key Concepts

#### Hypothesis

A **hypothesis** is a testable statement that predicts the outcome of an experiment. It must be:
- **Specific**: Clear and unambiguous
- **Testable**: Can be verified or refuted
- **Falsifiable**: Can be proven wrong
- **Measurable**: Has quantifiable outcomes

#### Variables

- **Independent Variable**: What you change or control
- **Dependent Variable**: What you measure (the outcome)
- **Control Variables**: What you keep constant

#### State Capture

- **State A**: Initial system state before experiment
- **State B**: Final system state after experiment
- **State Comparison**: Identifies changes and effects

#### Data Collection (C)

- **Systematic Measurements**: Recorded at specified intervals
- **Observations**: Qualitative notes and observations
- **Metrics**: Performance and behavior metrics
- **Timestamps**: All data points timestamped

---

## 3. Architecture and Design

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Science-Bitch CLI                      │
│              (src/waft/main.py)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            ScienceBitchManager                           │
│         (src/waft/core/science_bitch.py)                │
└─────┬──────────────┬──────────────┬─────────────────────┘
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│Hypothesis│  │Experiment│  │   State  │
│  System  │  │  Design  │  │  Capture │
└──────────┘  └──────────┘  └──────────┘
      │              │              │
      └──────────────┴──────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Data Collection (C)                        │
│         Systematic measurement recording                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Analysis & Reporting                       │
│    PDF Generation (waft.evolution.pdf_generator)        │
└─────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. ScienceBitchManager

The main manager class that orchestrates the entire workflow:

```python
class ScienceBitchManager:
    def __init__(self, project_path: Path)
    def run_interactive(self) -> Dict[str, Any]
    def generate_field_guide(self) -> Optional[Path]
    def generate_project_status_report(self) -> Optional[Path]
    def _create_field_guide_content(self) -> str
    def _create_project_status_content(self) -> str
```

#### 2. Scientific Method Tool

Core functionality from `scientific_method_tool/`:
- Hypothesis formation and validation
- Experiment design
- Data collection frameworks
- Analysis tools

#### 3. PDF Generation

Uses `waft.evolution.pdf_generator`:
- Professional formatting
- Multiple style presets
- Markdown to HTML conversion
- Comprehensive documentation

#### 4. State Capture

Automatic system state snapshots:
- File system state
- Configuration state
- Code state
- Data state

---

## 4. Workflow Phases

### Phase 1: Form Hypothesis

**Purpose**: Create a testable hypothesis

**Process**:
1. Identify the question or phenomenon
2. Formulate clear, testable hypothesis
3. Define variables (independent, dependent, control)
4. Specify verification criteria

**Example**:
```
Hypothesis: "Increasing the number of iterations in the genetic algorithm 
will improve fitness scores by at least 10%."

Variables:
- Independent: Number of iterations
- Dependent: Fitness score
- Control: Algorithm parameters, input data

Verification: If fitness increases by ≥10%, hypothesis is verified.
```

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

**Example**:
```
Experiment Design:
- Run algorithm with iterations: [10, 50, 100, 200]
- Measure fitness score for each
- Capture state before (A) and after (B)
- Collect data during execution (C)
- Compare results
```

**Output**: Experiment design with variables, data collection plan, and state capture strategy

---

### Phase 3: Capture Initial State (A)

**Purpose**: Capture system state before experiment

**Process**:
1. Identify components to track
2. Capture initial state snapshot
3. Generate state hash for comparison
4. Save state to `_science/experiments/[exp_id]/state_a.json`

**Components Captured**:
- File system structure
- Configuration files
- Code versions
- Data files
- System metrics

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

**Example Data Points**:
```json
{
  "timestamp": "2026-01-12T15:30:00Z",
  "iteration": 50,
  "fitness_score": 0.85,
  "execution_time_ms": 1234,
  "observations": "Convergence improving"
}
```

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

**Comparison**:
- File changes (added, modified, deleted)
- Configuration changes
- Code changes
- Data changes
- Metric changes

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

**Analysis Output**:
- Hypothesis verification status (verified/refuted/uncertain)
- Confidence level (0.0-1.0)
- Conclusions
- Recommendations
- Evidence summary

**Example Analysis**:
```
Hypothesis: "Increasing iterations improves fitness by ≥10%"

Results:
- 10 iterations: fitness = 0.70
- 50 iterations: fitness = 0.75 (+7%)
- 100 iterations: fitness = 0.82 (+17%)
- 200 iterations: fitness = 0.85 (+21%)

Conclusion: Hypothesis VERIFIED
Confidence: 0.95
Evidence: Clear positive correlation, 100+ iterations show >10% improvement
```

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

#### Experiment Report
- Hypothesis and design
- State snapshots (A and B)
- Collected data (C)
- Analysis results
- Conclusions

**Output**: PDF reports in `_science/reports/`

---

## 5. State Capture System

### Overview

The state capture system provides automatic snapshots of system state at key points in the experiment workflow. This enables:
- **Before/After Comparison**: Clear view of what changed
- **Reproducibility**: Can restore to initial state
- **Change Tracking**: Identifies all modifications
- **Evidence Chain**: Links changes to experiment results

### State Components

#### File System State
- Directory structure
- File contents (for key files)
- File metadata (size, modified time)
- File hashes (for change detection)

#### Configuration State
- Environment variables
- Configuration files
- Settings and parameters
- System configuration

#### Code State
- Source code versions
- Dependencies
- Build artifacts
- Test results

#### Data State
- Input data
- Output data
- Intermediate data
- Data schemas

### State Comparison

The system compares State A (initial) and State B (final) to identify:

**File Changes**:
- Added files
- Modified files
- Deleted files
- Renamed files

**Configuration Changes**:
- Modified settings
- New parameters
- Removed parameters

**Code Changes**:
- Modified source files
- New dependencies
- Updated versions

**Data Changes**:
- New data files
- Modified data
- Data schema changes

### Implementation

```python
def capture_state(state_id: str) -> Dict[str, Any]:
    """Capture current system state."""
    state = {
        "timestamp": datetime.now().isoformat(),
        "state_id": state_id,
        "files": capture_file_system(),
        "config": capture_configuration(),
        "code": capture_code_state(),
        "data": capture_data_state(),
        "hash": generate_state_hash()
    }
    return state
```

---

## 6. Data Collection Framework

### Overview

The data collection framework provides systematic recording of measurements, observations, and metrics during experiment execution.

### Data Types

#### Measurements
- Quantitative values
- Timestamped
- Units specified
- Precision recorded

#### Observations
- Qualitative notes
- Timestamped
- Context provided
- Categorized

#### Metrics
- Performance metrics
- System metrics
- Application metrics
- Custom metrics

#### Events
- Significant events
- Error conditions
- State transitions
- Milestones

### Data Collection Process

1. **Define Collection Points**: Where to collect data
2. **Specify Intervals**: How often to collect
3. **Record Measurements**: Capture values
4. **Store Data**: Save to structured format
5. **Timestamp Everything**: All data points timestamped

### Data Storage

Data is stored in structured JSON format:

```json
{
  "experiment_id": "exp_20260112_001",
  "data_points": [
    {
      "timestamp": "2026-01-12T15:30:00Z",
      "type": "measurement",
      "name": "fitness_score",
      "value": 0.85,
      "unit": "normalized",
      "context": "iteration_100"
    },
    {
      "timestamp": "2026-01-12T15:30:05Z",
      "type": "observation",
      "category": "convergence",
      "note": "Algorithm converging steadily",
      "context": "iteration_100"
    }
  ]
}
```

### Analysis Integration

Collected data (C) is integrated with state snapshots (A and B) for comprehensive analysis:
- **Temporal Analysis**: How values change over time
- **Correlation Analysis**: Relationships between variables
- **Statistical Analysis**: Means, variances, distributions
- **Pattern Recognition**: Identifying trends and patterns

---

## 7. Hypothesis Testing

### Hypothesis Formation

A good hypothesis has:
- **Clear Statement**: Unambiguous prediction
- **Testable**: Can be verified or refuted
- **Falsifiable**: Can be proven wrong
- **Measurable**: Has quantifiable outcomes
- **Specific**: Not too broad or vague

### Hypothesis Structure

```
If [independent variable] is [changed],
then [dependent variable] will [expected outcome],
because [rationale].
```

### Verification Process

1. **Define Criteria**: What constitutes verification?
2. **Run Experiment**: Execute according to design
3. **Collect Data**: Systematic data collection
4. **Analyze Results**: Compare to criteria
5. **Verify/Refute**: Determine outcome
6. **Calculate Confidence**: Assess certainty

### Confidence Levels

- **High (0.8-1.0)**: Strong evidence, clear results
- **Medium (0.5-0.8)**: Moderate evidence, some uncertainty
- **Low (0.0-0.5)**: Weak evidence, high uncertainty

### Example Hypothesis Testing

**Hypothesis**: "Using caching improves response time by at least 50%"

**Test**:
- Run with caching: response_time = 100ms
- Run without caching: response_time = 250ms
- Improvement: 60%

**Result**: VERIFIED (60% > 50% threshold)
**Confidence**: 0.95 (high - clear improvement)

---

## 8. Report Generation

### Report Types

#### Field Guide
Comprehensive usage guide covering:
- Command overview
- Workflow phases
- Examples
- Best practices
- Troubleshooting

#### Project Status Report
Current project state including:
- Goals and objectives
- Progress tracking
- Evidence collected
- Next steps
- Recommendations

#### Experiment Report
Complete experiment documentation:
- Hypothesis and design
- State snapshots (A and B)
- Collected data (C)
- Analysis results
- Conclusions

### PDF Generation

Reports are generated using `waft.evolution.pdf_generator`:

**Features**:
- Professional formatting
- Multiple style presets (clinical_standard, premium, professional)
- Markdown to HTML conversion
- Comprehensive documentation
- Beautiful typography

**Style Presets**:
- **clinical_standard**: Academic/research style
- **premium**: High-end publication style
- **professional**: Business/professional style

### Report Structure

1. **Title Page**: Document title, version, date
2. **Table of Contents**: Navigation
3. **Executive Summary**: Key findings
4. **Main Content**: Detailed sections
5. **Appendices**: Supporting data
6. **References**: Citations and sources

---

## 9. Integration with WAFT

### WAFT Ecosystem

Science-Bitch integrates with the broader WAFT ecosystem:

#### PDF Generation
- Uses `waft.evolution.pdf_generator`
- Leverages styling genomes
- Professional formatting
- Multiple output formats

#### Work Efforts System
- Tracks progress in `WE-260112-az3z`
- Links to work effort documentation
- Progress tracking
- Status updates

#### Scientific Method Tool
- Core functionality from `scientific_method_tool/`
- Hypothesis framework
- Experiment design
- Analysis tools

#### State Management
- System state capture
- Change tracking
- Reproducibility support

### Command Integration

Science-Bitch is accessible via:
- **CLI**: `waft science-bitch`
- **Cursor Command**: `/science-bitch`
- **Python API**: `ScienceBitchManager`

---

## 10. Use Cases and Examples

### Use Case 1: Algorithm Performance Testing

**Scenario**: Testing if a new algorithm improves performance

**Workflow**:
1. **Hypothesis**: "New algorithm reduces execution time by 30%"
2. **Design**: Compare old vs new algorithm on test dataset
3. **Capture A**: Initial codebase state
4. **Run**: Execute both algorithms
5. **Collect C**: Record execution times
6. **Capture B**: Final state
7. **Analyze**: Compare performance metrics
8. **Report**: Generate performance analysis

**Result**: Algorithm verified to reduce time by 35%

---

### Use Case 2: Configuration Optimization

**Scenario**: Finding optimal configuration parameters

**Workflow**:
1. **Hypothesis**: "Parameter X=0.8 optimizes accuracy"
2. **Design**: Test X values [0.5, 0.6, 0.7, 0.8, 0.9]
3. **Capture A**: Initial configuration
4. **Run**: Test each parameter value
5. **Collect C**: Record accuracy for each
6. **Capture B**: Final configuration
7. **Analyze**: Identify optimal value
8. **Report**: Configuration recommendations

**Result**: X=0.8 provides best accuracy (0.92)

---

### Use Case 3: Code Refactoring Impact

**Scenario**: Measuring impact of code refactoring

**Workflow**:
1. **Hypothesis**: "Refactoring improves maintainability without performance loss"
2. **Design**: Compare before/after metrics
3. **Capture A**: Pre-refactoring state
4. **Run**: Execute refactored code
5. **Collect C**: Performance and maintainability metrics
6. **Capture B**: Post-refactoring state
7. **Analyze**: Compare metrics
8. **Report**: Refactoring impact analysis

**Result**: Maintainability improved, performance maintained

---

## 11. Best Practices

### Hypothesis Formation

1. **Be Specific**: Clear, unambiguous statements
2. **Make Testable**: Can be verified or refuted
3. **Define Variables**: Clear independent/dependent variables
4. **Set Criteria**: What constitutes verification?

### Experiment Design

1. **Control Variables**: Keep constants constant
2. **Multiple Trials**: Run multiple experiments
3. **Randomization**: Reduce bias
4. **Blinding**: When appropriate

### State Capture

1. **Capture Everything**: Don't miss important components
2. **Use Hashes**: For change detection
3. **Document Context**: Include relevant information
4. **Version Control**: Track state versions

### Data Collection

1. **Systematic**: Consistent collection methods
2. **Timestamped**: All data points timestamped
3. **Categorized**: Organize by type
4. **Complete**: Don't skip data points

### Analysis

1. **Thorough**: Don't rush analysis
2. **Evidence-Based**: All conclusions supported
3. **Statistical**: Use appropriate methods
4. **Documented**: Clear reasoning

### Reporting

1. **Complete**: Include all relevant information
2. **Clear**: Easy to understand
3. **Professional**: Well-formatted
4. **Reproducible**: Others can follow

---

## 12. Technical Implementation

### Command Structure

```bash
# Interactive workflow
waft science-bitch

# Generate field guide
waft science-bitch --field-guide

# Generate project status report
waft science-bitch --report

# With hypothesis
waft science-bitch --hypothesis "Your hypothesis"

# Run experiment
waft science-bitch --run
```

### File Structure

```
_science/
├── README.md                    # Overview
├── SUMMARY.md                   # Summary
├── experiments/                 # Experiment definitions
│   └── [exp_id]/               # Individual experiment
│       ├── experiment.json     # Experiment definition
│       ├── state_a.json        # Initial state (A)
│       ├── state_b.json        # Final state (B)
│       └── results.json        # Experiment results
├── data/                        # Collected data (C)
│   └── [exp_id]/               # Data for each experiment
│       └── data_series.json   # Collected measurements
├── reports/                     # Generated reports
│   ├── field_guide.pdf         # Usage guide
│   ├── field_guide.md          # Source markdown
│   ├── project_status.pdf       # Status report
│   └── project_status.md       # Source markdown
└── tools/                       # Helper utilities
    ├── generate_field_guide_pdf.py
    └── generate_status_pdf.py
```

### Code Structure

```
src/waft/
├── main.py                      # CLI entry point
└── core/
    └── science_bitch.py         # ScienceBitchManager

scientific_method_tool/
├── hypothesis.py                # Hypothesis framework
├── experiment.py                # Experiment design
└── analysis.py                  # Analysis tools
```

### Dependencies

- **typer**: CLI framework
- **rich**: Terminal formatting
- **weasyprint**: PDF generation
- **markdown**: Markdown processing
- **jinja2**: Template rendering

---

## 13. Future Directions

### Planned Enhancements

1. **Visual Analytics**: Charts and graphs in reports
2. **Statistical Analysis**: Built-in statistical tests
3. **Machine Learning Integration**: ML-based hypothesis generation
4. **Collaborative Features**: Team experiment sharing
5. **Version Control Integration**: Git-based state tracking
6. **Cloud Storage**: Remote experiment storage
7. **Real-Time Monitoring**: Live experiment tracking
8. **Automated Hypothesis Generation**: AI-assisted hypothesis formation

### Research Areas

1. **Reproducibility**: Improving experiment reproducibility
2. **Scalability**: Handling large-scale experiments
3. **Integration**: Better ecosystem integration
4. **Usability**: Improving user experience
5. **Performance**: Optimizing execution speed

---

## 14. Conclusion

Science-Bitch provides a comprehensive, systematic approach to scientific research and experimentation. By implementing the complete scientific method workflow with automatic state capture, systematic data collection, and professional report generation, it enables researchers to conduct rigorous, evidence-based research with full traceability.

### Key Benefits

- **Systematic Approach**: Structured workflow ensures completeness
- **Evidence-Based**: All conclusions traceable to data
- **Reproducible**: State capture enables reproduction
- **Professional**: High-quality documentation
- **Integrated**: Works with WAFT ecosystem

### Getting Started

1. Install dependencies: `pip install -e .`
2. Run field guide: `waft science-bitch --field-guide`
3. Form hypothesis: `waft science-bitch --hypothesis "Your hypothesis"`
4. Run experiment: `waft science-bitch --run`
5. Generate report: `waft science-bitch --report`

### Resources

- **Work Effort**: `WE-260112-az3z_science_bitch_command_full_scientific_method_cli`
- **Source Code**: `src/waft/core/science_bitch.py`
- **Documentation**: `_science/README.md`
- **Examples**: `scientific_method_tool/example_usage.py`

---

## Appendices

### Appendix A: Command Reference

```bash
# Full workflow
waft science-bitch

# Generate field guide
waft science-bitch --field-guide

# Generate status report
waft science-bitch --report

# With hypothesis
waft science-bitch --hypothesis "Statement"

# Run experiment
waft science-bitch --run

# Specify path
waft science-bitch --path /path/to/project
```

### Appendix B: File Formats

#### Experiment Definition (experiment.json)
```json
{
  "experiment_id": "exp_20260112_001",
  "hypothesis": "Statement",
  "variables": {
    "independent": "...",
    "dependent": "...",
    "control": "..."
  },
  "design": "...",
  "created_at": "2026-01-12T15:00:00Z"
}
```

#### State Snapshot (state_a.json / state_b.json)
```json
{
  "state_id": "state_a",
  "timestamp": "2026-01-12T15:00:00Z",
  "files": {...},
  "config": {...},
  "code": {...},
  "data": {...},
  "hash": "..."
}
```

#### Data Series (data_series.json)
```json
{
  "experiment_id": "exp_20260112_001",
  "data_points": [
    {
      "timestamp": "2026-01-12T15:30:00Z",
      "type": "measurement",
      "name": "fitness_score",
      "value": 0.85
    }
  ]
}
```

### Appendix C: Troubleshooting

**Command not found**
- Ensure you're in project root
- Check: `waft --help` shows `science-bitch`

**Import errors**
- Install dependencies: `pip install -e .`
- Check: `python3 -c "from waft.core.science_bitch import ScienceBitchManager"`

**PDF generation fails**
- Install WeasyPrint: `pip install weasyprint`
- Check system dependencies (Cairo, Pango)

**State capture fails**
- Check file permissions
- Verify component paths
- Ensure write access to `_science/`

---

**End of Research Booklet**

*This document was generated using Science-Bitch and WAFT PDF generation tools.*
