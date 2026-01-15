# /record-and-loop - Scientific Experiment Cycle

**Records observations from experiments, generates PDF reports, and prepares for the next iteration cycle.**

Automates the scientific method workflow: observe → document → analyze → iterate. Perfect for iterative improvements, algorithm testing, and systematic experimentation.

**Use when:**
- You've completed a test cycle and want to record findings
- You need to document observations systematically
- You want to prepare for the next iteration with the same conditions
- You're running experiments and need structured documentation
- You want PDF reports that open automatically

---

## Purpose

This command provides:
- **Observation Recording**: Documents findings from test cycles
- **PDF Report Generation**: Creates professional experiment reports
- **Iteration Preparation**: Sets up next cycle with same starting conditions
- **Desktop Integration**: Opens PDFs automatically on your desktop
- **Scientific Method**: Follows observe → document → analyze → iterate pattern

---

## Execution

**Command**: `/record-and-loop` or `/experiment-cycle` or `/record-observations`

**What the AI does:**
1. **Identifies Experiment Context** - Determines what was tested/experimented on
2. **Records Observations** - Documents findings, test results, patterns
3. **Analyzes Results** - Identifies what worked, what didn't, improvements needed
4. **Generates PDF Report** - Creates professional experiment report
5. **Prepares Next Iteration** - Documents starting conditions for next cycle
6. **Opens PDFs** - Automatically opens reports on your desktop

**AI Actions:**
- Extracts experiment context from conversation
- Documents test cases/variations used
- Records observations and assessments
- Identifies patterns and improvements needed
- Creates markdown observation document
- Generates PDF with BriefDocument system
- Creates iteration preparation document
- Opens PDFs on desktop (macOS)

---

## Workflow Steps

### Step 1: Extract Experiment Context
**Purpose**: Understand what was being tested/experimented on

**Actions**:
1. Review conversation for experiment/test context
2. Identify what was being tested (algorithm, feature, system, etc.)
3. Extract test cases/variations used
4. Identify current cycle/iteration number
5. Note any specific experiment parameters

**Output**: Experiment context summary

### Step 2: Record Observations
**Purpose**: Document findings systematically

**Actions**:
1. List all test cases/variations
2. For each test case:
   - Document the input/test
   - Record the result/output
   - Assess quality (✅ Good, ⚠️ Needs Improvement, ❌ Problem)
   - Note specific issues or successes
3. Identify patterns across test cases
4. Document what worked well
5. Document what needs improvement
6. Create structured markdown document

**Output**: `_work_efforts/proof_cases/[experiment_name]_observations.md`

### Step 3: Analyze Results
**Purpose**: Identify key insights and improvements

**Actions**:
1. Analyze patterns in observations
2. Categorize findings (strengths, weaknesses, edge cases)
3. Prioritize improvements needed
4. Identify algorithm/approach strengths
5. Document recommendations for next iteration
6. Define success criteria for next cycle

**Output**: Analysis section in observations document

### Step 4: Generate PDF Report
**Purpose**: Create professional experiment report

**Actions**:
1. Read observations markdown file
2. Create BriefDocument with experiment metadata
3. Convert markdown to HTML
4. Generate PDF with cover page
5. Save to `_work_efforts/proof_cases/`
6. Open PDF on desktop (macOS: `open` command)

**Output**: `[Experiment_Name]_Cycle[N]_[timestamp].pdf` (opens automatically)

### Step 5: Prepare Next Iteration
**Purpose**: Set up next cycle with same starting conditions

**Actions**:
1. Document all test cases (same as current cycle)
2. Document current algorithm/approach state
3. List target improvements (from observations)
4. Define success criteria
5. Create implementation plan
6. Generate preparation PDF
7. Open preparation PDF on desktop

**Output**: 
- `iteration[N+1]_preparation.md`
- `Iteration[N+1]_Preparation_[timestamp].pdf` (opens automatically)

---

## File Structure

### Observations Document
**Location**: `_work_efforts/proof_cases/[experiment_name]_observations.md`

**Structure**:
```markdown
# [Experiment Name] - Experiment Observations

**Experiment Date**: YYYY-MM-DD
**Iteration**: Cycle N
**Status**: Observations Recorded - Ready for Iteration N+1

## Experiment Setup
- Starting conditions
- Test cases used
- Changes made

## Test Results: [N] Variations
[For each test case:]
- Input/Test
- Result/Output
- Assessment
- Notes

## Key Observations
- What works well
- Areas needing improvement
- Patterns identified

## Algorithm Analysis
- Current strengths
- Current weaknesses

## Recommendations for Iteration N+1
- Priority improvements
- Implementation plan

## Next Iteration Plan
- Same starting conditions
- Target improvements
- Success criteria
```

### Preparation Document
**Location**: `_work_efforts/proof_cases/iteration[N+1]_preparation.md`

**Structure**:
```markdown
# [Experiment Name] - Iteration N+1 Preparation

**Prepared**: YYYY-MM-DD
**Cycle**: N+1
**Status**: Ready to Begin

## Starting Conditions (Same as Cycle N)
- Test cases
- Current algorithm state

## Target Improvements
- From Cycle N observations
- Priority list

## Implementation Plan
- Steps to take
- Changes to make

## Success Criteria
- Must have
- Should have
- Nice to have
```

---

## Usage Examples

### Basic Usage
```
/record-and-loop
```

**Context**: You just tested 12 variations of a title generation algorithm

**What happens**:
1. AI extracts experiment context (title generation algorithm)
2. Records observations for all 12 test cases
3. Analyzes what worked and what didn't
4. Generates PDF report
5. Prepares iteration 2 with same test cases
6. Opens both PDFs on desktop

### With Explicit Context
```
/record-and-loop
I just tested the PDF generation system with 5 different templates.
Results: 3 worked well, 2 had issues with formatting.
```

**What happens**:
1. AI uses explicit context (PDF generation, 5 templates)
2. Records observations for 5 templates
3. Documents which 3 worked and which 2 had issues
4. Generates report and prepares next iteration

### Multiple Cycles
```
/record-and-loop
This is cycle 3 of the algorithm optimization experiment.
```

**What happens**:
1. AI identifies cycle 3
2. Records observations
3. Generates "Cycle 3" report
4. Prepares "Iteration 4" document

---

## Output Files

### Generated Files
1. **Observations Markdown**: `_work_efforts/proof_cases/[experiment_name]_observations.md`
2. **Observations PDF**: `_work_efforts/proof_cases/[Experiment_Name]_Cycle[N]_[timestamp].pdf`
3. **Preparation Markdown**: `_work_efforts/proof_cases/iteration[N+1]_preparation.md`
4. **Preparation PDF**: `_work_efforts/proof_cases/Iteration[N+1]_Preparation_[timestamp].pdf`

### Desktop Integration
- Both PDFs open automatically on macOS
- PDFs are ready for review
- Markdown files available for editing

---

## Integration with Scientific Method

This command implements the scientific method workflow:

1. **Observe** → Record test results and findings
2. **Document** → Create structured observations
3. **Analyze** → Identify patterns and improvements
4. **Hypothesize** → Define improvements for next cycle
5. **Iterate** → Prepare next cycle with same conditions
6. **Repeat** → Continue until success criteria met

---

## Best Practices

### When to Use
- ✅ After completing a test cycle
- ✅ When you have multiple test cases/variations
- ✅ For iterative algorithm improvements
- ✅ For systematic experimentation
- ✅ When you need structured documentation

### What to Include
- All test cases/variations used
- Clear assessments (✅/⚠️/❌)
- Specific observations (not vague)
- Prioritized improvements
- Same starting conditions for next cycle

### Tips
- Be specific about what worked and what didn't
- Include test inputs and outputs
- Document patterns across test cases
- Prioritize improvements clearly
- Keep starting conditions consistent across cycles

---

## Technical Details

### PDF Generation
- Uses `BriefDocument` from `src.waft.brief`
- Professional cover page with metadata
- Markdown to HTML conversion
- Automatic desktop opening (macOS)

### File Naming
- Observations: `[Experiment_Name]_Cycle[N]_[timestamp].pdf`
- Preparation: `Iteration[N+1]_Preparation_[timestamp].pdf`
- Timestamp format: `YYYYMMDD_HHMMSS`

### Dependencies
- `src.waft.brief.BriefDocument`
- Markdown library (optional, has fallback)
- macOS `open` command for desktop integration

---

## Related Commands

- `/prove-it` - Prove claims with evidence
- `/study-claim` - Thorough study of claims
- `/checkpoint` - Status reports
- `/report` - Generate reports

---

**This command automates the scientific method workflow for iterative experimentation and improvement.**
