# TheOracle Calculation Display Enhancement - Continuation Prompt

**Date**: 2026-01-19  
**Status**: ⚠️ **IN PROGRESS** - Calculation display implemented, needs testing and completion

---

## Context

User wants to see TheOracle calculating its thoughts step-by-step, showing actual mathematical formulas and reasoning process (similar to Empirica's epistemic mode). The goal is to make the thinking process transparent and visible in real-time.

---

## What Was Done

### 1. Enhanced Step-by-Step Thinking Display

**Location**: `src/waft/core/science/oracle_thinking.py`

**Changes**:
- Added `CALCULATE` step to show mathematical calculations
- Enhanced each step to show:
  - Status messages ("Assessing...", "Calculating...")
  - Actual formulas being used
  - Intermediate calculation values
  - Decision logic reasoning

**Example Output**:
```
📊 PREFLIGHT...
   Assessing epistemic state...
   💭 Retrieving current epistemic vectors from Empirica...
   ✓ Assessment complete
      💭 Calculated: know=0.00 (from foundation vectors), uncertainty=1.00 (from meta vector)
      KNOW: 0% (Low)
      UNCERTAINTY: 100% (High)
      → INVESTIGATE REQUIRED

🧮 CALCULATE...
   Extracting epistemic vectors...
   💭 From epistemic_state.vectors: foundation.know = 0.000, vectors.uncertainty = 1.000
   ✓ Calculation complete
   Calculating coverage and phase...
   💭 Formula: coverage = know(0.000) × (1 - uncertainty(1.000)) = 0.000 × 0.000 = 0.000. Phase logic: know(0.00) < 0.3 AND uncertainty(1.00) > 0.5

✅ CHECK...
   Evaluating decision gate...
   💭 Inputs: 0 findings, 0 unknowns, uncertainty=1.000
   Calculating confidence...
   💭 Step 1: base_confidence = min(1.0, findings(0) × 0.1) = min(1.0, 0.000) = 0.000. Step 2: confidence = 0.000 × (1 - uncertainty(1.000)) = 0.000 × 0.000 = 0.000
   Evaluating decision logic...
   💭 Decision tree: Special case: uncertainty(1.000) >= 0.99 AND no findings/unknowns → PROCEED (fallback mode)
   ✓ Decision gate evaluated
      Findings: 0, Unknowns: 0
      CONFIDENCE: 0%
      → DECISION: PROCEED
```

### 2. Added Calculation Formulas to Thinking Callbacks

**Location**: `src/waft/core/science/oracle.py`

**Changes**:
- `_empirica_preflight()`: Shows vector extraction and calculation
- `_empirica_check()`: Shows confidence calculation step-by-step
- `provide_guidance()`: Shows coverage and phase calculation formulas
- Added `show_calculation` parameter to `get_epistemic_phase()`

**Formulas Displayed**:
- **Coverage**: `coverage = know × (1 - uncertainty)`
- **Confidence**: `base_confidence = min(1.0, findings × 0.1)`, then `confidence = base_confidence × (1 - uncertainty)`
- **Phase Logic**: Shows actual thresholds being evaluated (e.g., `know < 0.3 AND uncertainty > 0.5`)
- **Decision Logic**: Shows which condition triggered the decision

### 3. Enhanced Main CLI Display

**Location**: `src/waft/main.py`

**Changes**:
- Added immediate feedback with status spinners
- Shows thinking steps in real-time
- Displays full calculation dashboard after thinking

### 4. TheOracle Fallback Fix (Previous Work)

**Location**: `src/waft/core/science/oracle.py`

**Changes**:
- Added `_answer_question_without_epistemic_state()` method
- Modified `_generate_recommendation()` to use fallback when phase is UNKNOWN
- Updated CHECK decision logic to allow PROCEED for fallback answers

---

## Current State

### ✅ Completed
- Calculation formulas added to thinking callbacks
- Step-by-step thinking display enhanced
- CALCULATE step added to workflow
- Decision logic reasoning displayed
- Immediate feedback with status spinners

### ⚠️ Issues
- **Empirica CLI timeouts**: Commands are timing out (5-10 second timeouts)
- **Testing blocked**: Can't fully test the calculation display due to timeouts
- **Performance**: Initialization takes too long before user sees feedback

### 📋 Still TODO
1. **Fix Empirica CLI timeouts** - Commands hanging/timing out
2. **Test calculation display** - Verify all formulas show correctly
3. **Optimize initialization** - Show feedback immediately, don't wait for Empirica
4. **Complete release notes** - Finish CHANGELOG.md and RELEASE_NOTES_v0.9.4.md
5. **Commit changes** - Commit Oracle fix, version bump, bootstrap script

---

## Files Modified

1. `src/waft/core/science/oracle.py`
   - Added calculation thinking callbacks
   - Enhanced `_empirica_check()` to show formulas
   - Modified `get_epistemic_phase()` to return calculation details
   - Added `_answer_question_without_epistemic_state()` (previous fix)

2. `src/waft/core/science/oracle_thinking.py`
   - Added `CALCULATE` step icon and display
   - Enhanced all steps to show thinking/calculations
   - Reduced delay for faster feedback

3. `src/waft/main.py`
   - Added status spinners for immediate feedback
   - Enhanced question handling to show step-by-step thinking
   - Added calculation dashboard display

4. `scripts/bootstrap_epistemic_state.py` (NEW)
   - Bootstrap script to initialize epistemic state

5. `pyproject.toml` & `src/waft/__init__.py`
   - Version bumped to 0.9.4

---

## Key Formulas Being Displayed

### Coverage Calculation
```
coverage = know × (1 - uncertainty)
Example: coverage = 0.000 × (1 - 1.000) = 0.000 × 0.000 = 0.000
```

### Confidence Calculation
```
Step 1: base_confidence = min(1.0, findings_count × 0.1)
Step 2: confidence = base_confidence × (1 - uncertainty)
Example: base_confidence = min(1.0, 0 × 0.1) = 0.000
         confidence = 0.000 × (1 - 1.000) = 0.000
```

### Phase Determination
```
if know < 0.3 AND uncertainty > 0.5 → "Data Gathering"
if know < 0.6 AND uncertainty > 0.3 → "Exploration"
if know > 0.6 AND uncertainty < 0.3 → "Synthesis"
if know > 0.8 AND uncertainty < 0.2 → "Evolution"
else → "Transition"
```

### Decision Logic
```
if uncertainty >= 0.99 AND no findings/unknowns → PROCEED (fallback)
if confidence >= 0.7 AND uncertainty < 0.3 → PROCEED
if confidence < 0.3 OR uncertainty > 0.7 → HALT
if unknowns > findings → BRANCH
else → REVISE
```

---

## Testing

**To test the calculation display:**
```bash
# Test with a question (should show step-by-step calculations)
python3 -m src.waft.main oracle "What should be documented in the version release notes?"

# Expected output:
# - Immediate feedback (no long wait)
# - Step-by-step thinking with formulas
# - Calculation details for each step
# - Decision logic reasoning
```

**Known Issues:**
- Empirica CLI commands timing out (5-10 seconds)
- May need to increase timeout or handle timeouts gracefully
- Initialization takes time before first output appears

---

## Next Steps

1. **Fix Empirica CLI timeouts**
   - Increase timeout values
   - Add graceful timeout handling
   - Show progress even during timeouts

2. **Optimize initialization**
   - Show "Initializing..." immediately
   - Don't block on Empirica CLI calls
   - Use async/background processing if needed

3. **Complete release documentation**
   - Finish CHANGELOG.md entry for v0.9.4
   - Create RELEASE_NOTES_v0.9.4.md
   - Document Oracle fix and calculation display

4. **Commit and push**
   - Commit all changes
   - Push to GitHub
   - Tag release if appropriate

---

## Related Files

- `ORACLE_FIX_SUMMARY.md` - Previous fix documentation
- `V0.9.4_VERSION_UPDATE_SUMMARY.md` - Version update summary
- `scripts/bootstrap_epistemic_state.py` - Bootstrap script

---

## Notes

- User wants to see calculations happening in real-time
- Similar to Empirica's epistemic mode showing vector calculations
- Goal is transparency in the reasoning process
- Current implementation shows formulas but needs testing due to CLI timeouts
