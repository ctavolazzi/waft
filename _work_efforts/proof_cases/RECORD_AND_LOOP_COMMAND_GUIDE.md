# /record-and-loop Command - Quick Reference

**Created**: 2026-01-14  
**Status**: ✅ Ready to Use

---

## What It Does

The `/record-and-loop` command automates the scientific method workflow:

1. **Records observations** from your experiment/test cycle
2. **Generates PDF reports** with professional formatting
3. **Prepares next iteration** with same starting conditions
4. **Opens PDFs on desktop** automatically

---

## Quick Start

### Basic Usage
```
/record-and-loop
```

**What happens:**
- AI extracts experiment context from conversation
- Records observations for all test cases
- Generates PDF report (opens on desktop)
- Prepares next iteration document (opens on desktop)

### Example
You just tested 12 variations of a title generation algorithm:

```
/record-and-loop
```

AI will:
1. Identify: "Title Generation Algorithm - Cycle 1"
2. Record observations for all 12 test cases
3. Generate: `Title_Generation_Algorithm_Cycle1_[timestamp].pdf`
4. Prepare: `Iteration2_Preparation_[timestamp].pdf`
5. Open both PDFs on your desktop

---

## Files Created

### Observations
- **Markdown**: `_work_efforts/proof_cases/[experiment_name]_observations.md`
- **PDF**: `_work_efforts/proof_cases/[Experiment_Name]_Cycle[N]_[timestamp].pdf`

### Preparation
- **Markdown**: `_work_efforts/proof_cases/iteration[N+1]_preparation.md`
- **PDF**: `_work_efforts/proof_cases/Iteration[N+1]_Preparation_[timestamp].pdf`

---

## Command Details

**Command File**: `.cursor/commands/record-and-loop.md`  
**Supporting Script**: `scripts/record_experiment_cycle.py`

**Aliases**:
- `/record-and-loop`
- `/experiment-cycle`
- `/record-observations`

---

## What Gets Documented

### Observations Document Includes:
- Experiment setup and starting conditions
- All test cases with results
- Assessments (✅ Good, ⚠️ Needs Improvement, ❌ Problem)
- Key observations and patterns
- Algorithm/approach analysis
- Recommendations for next iteration

### Preparation Document Includes:
- Same test cases (for consistency)
- Current algorithm/approach state
- Target improvements (from observations)
- Implementation plan
- Success criteria

---

## Workflow

```
Test Cycle Complete
       ↓
/record-and-loop
       ↓
Observations Recorded
       ↓
PDF Report Generated → Opens on Desktop
       ↓
Next Iteration Prepared → Opens on Desktop
       ↓
Ready for Cycle N+1
```

---

## Tips

1. **Be Specific**: Include all test cases and clear assessments
2. **Document Patterns**: Note what worked and what didn't
3. **Prioritize**: List improvements in priority order
4. **Consistency**: Keep starting conditions the same across cycles
5. **Iterate**: Use the command after each test cycle

---

## Example Output

After running `/record-and-loop`:

**Desktop Opens:**
- `Title_Generation_Algorithm_Cycle1_20260114_112714.pdf`
- `Iteration2_Preparation_20260114_112745.pdf`

**Files Created:**
- `_work_efforts/proof_cases/title_generation_experiment_observations.md`
- `_work_efforts/proof_cases/iteration2_preparation.md`

---

## Integration

This command works with:
- `/prove-it` - For proving claims
- `/study-claim` - For thorough studies
- `/checkpoint` - For status reports
- Scientific method workflow

---

**Ready to use! Just type `/record-and-loop` after completing a test cycle.**
