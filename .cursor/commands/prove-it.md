# /prove-it - Comprehensive Proof with Evidence-Based Case File

**Builds a case file with evidence to prove or disprove claims beyond reasonable doubt.**

---

## Purpose

This command provides comprehensive proof by:
1. **Running /verify checks** - Verifies all claims with evidence
2. **Running /check-assumptions** - Validates all assumptions
3. **Building a case file** - Creates detailed evidence brief
4. **Generating PDF binder** - Professional case document with verdict on cover
5. **Clear verdict** - States PROVEN, DISPROVEN, or INCONCLUSIVE

**If claims are false, states so clearly in the case brief.**

**Use when:**
- You need to prove a claim with evidence
- You want verification beyond reasonable doubt
- You need a case file documenting proof
- You want assumption validation
- You need a professional proof document

---

## Execution

**Command**: `/prove-it [claim]` or `/prove [claim]`

**What it does:**
1. Extracts claim from conversation or argument
2. Runs `/verify` checks with evidence collection
3. Runs `/check-assumptions` validation
4. Builds comprehensive case file with evidence
5. Generates PDF binder with verdict on cover
6. Opens PDF for review

**Execution Steps:**
1. Run `python3 scripts/prove_it_comprehensive.py [claim]`
2. Verification checks execute (date/time, disk space, git, templates, etc.)
3. Assumption validation runs
4. Case file built with all evidence
5. PDF generated with verdict prominently displayed
6. PDF opens automatically

**Default Claim** (if none provided):
- "All PDF templates have been fixed to remove black bars from headers"

---

## What Gets Proven

### 1. Verification Checks
- ✅ Date/Time accuracy
- ✅ Disk space availability
- ✅ Working directory verification
- ✅ Git repository state
- ✅ File existence checks
- ✅ Template verification (black bars, etc.)
- ✅ All with traceable evidence

### 2. Assumption Validation
- ✅ Extracts assumptions from claim
- ✅ Validates each assumption with evidence
- ✅ Code analysis
- ✅ File system checks
- ✅ Test results
- ✅ Confidence scoring

### 3. Evidence Collection
- ✅ All verification results documented
- ✅ Assumption validation results
- ✅ Code evidence
- ✅ File evidence
- ✅ Test evidence
- ✅ Traceable proof chains

### 4. Case File Generation
- ✅ Executive summary with verdict
- ✅ Detailed verification evidence
- ✅ Assumption validation results
- ✅ Additional evidence
- ✅ Conclusion with confidence level

### 5. PDF Binder
- ✅ Professional case brief format
- ✅ Verdict on cover page
- ✅ Confidence level displayed
- ✅ All evidence included
- ✅ Clear PROVEN/DISPROVEN/INCONCLUSIVE statement

---

## Proof Demonstrations

### Simple Proof
**File**: `scientific_method_tool/prove_it_works.py`

**What it demonstrates:**
- Basic hypothesis creation
- State capture (A & B)
- Data collection (C)
- State comparison
- Result analysis
- File persistence

**Output:**
- Step-by-step verification
- All components tested
- Files created and verified

### Real Experiment Proof
**File**: `scientific_method_tool/prove_with_real_experiment.py`

**What it demonstrates:**
- Real hypothesis about investigation skill
- Actual Being creation
- Real D&D character
- Actual tavern scenario execution
- Real data collection
- Real state comparison
- Real analysis

**Output:**
- Full experiment cycle
- Real Being decisions
- Actual fitness gains
- Verified hypothesis

---

## Example Output

```
============================================================
PROOF: Scientific Method Tool Works
============================================================

1️⃣  Creating Hypothesis...
   ✓ Hypothesis: Incrementing a counter increases its value

2️⃣  Creating Experiment Manager...
   ✓ Manager created

3️⃣  Creating Experiment...
   ✓ Experiment ID: exp_411664a5

4️⃣  Capturing Initial State (A)...
   ✓ Initial state captured: 04fe4591
   ✓ Components: ['counter', 'test_var']

5️⃣  Running Experiment...
   ✓ Experiment completed
   ✓ Results: {'initial': 10, 'final': 15, 'change': 5}

6️⃣  Verifying Data Collection (C)...
   ✓ Collected 2 data series
      - counter: 2 data points
        Values: [10, 15]
      - change: 1 data points
        Values: [5]

7️⃣  Verifying Final State (B)...
   ✓ Final state captured: 05698f80
   ✓ Components: ['counter', 'test_var']

8️⃣  Comparing States (A vs B)...
   ✓ State comparison complete
   ✓ Components changed: 0

9️⃣  Analyzing Results...
   ✓ Hypothesis verified: True
   ✓ Confidence: 90.00%

🔟 Verifying Files Saved...
   ✓ Experiment files: 1
   ✓ State files: 3
   ✓ Data files: 1

✅ PROOF COMPLETE
```

---

## Integration

This command demonstrates the scientific method tool which integrates with:
- **Self-Engineering System**: Tests self-engineering improvements
- **Being System**: Tests Being behavior hypotheses
- **D&D 5e System**: Tests gameplay mechanics
- **State Capture**: Tracks system evolution
- **Data Collection**: Monitors experimental effects

---

## Storage

All proof data is saved to:
```
scientific_method_tool/experiments/
├── experiments/          # Experiment definitions
├── states/              # State snapshots (A and B)
├── data/                # Collected data (C)
└── results_summary_*.json
```

---

## The Scientific Method Cycle

The proof demonstrates the complete cycle:
1. **Observe**: System detects patterns
2. **Hypothesize**: Form testable hypothesis
3. **Design Experiment**: Define variables
4. **Capture Initial State (A)**: Save system state before
5. **Run Experiment**: Execute with data collection
6. **Collect Data (C)**: Record all measurements during
7. **Capture Final State (B)**: Save system state after
8. **Analyze**: Compare states, analyze data, verify/refute
9. **Iterate**: Modify variables and repeat
10. **Conclude**: Draw evidence-based conclusions

---

## When to Use

**Use `/prove-it` when**:
- ✅ Want to verify the scientific method tool works
- ✅ Need to demonstrate the system to others
- ✅ Want to test the experimental framework
- ✅ Need to see the full cycle in action
- ✅ Want to verify file persistence

**Don't use `/prove-it` when**:
- ❌ Need to run actual experiments (use the tool directly)
- ❌ Need to analyze existing experiments (use analysis tools)
- ❌ Need to modify experiments (edit experiment code)

---

## Troubleshooting

**Error: ImportError**
- Solution: Ensure you're in the project root directory
- Check: `python3 -c "from scientific_method_tool import Hypothesis"`

**Error: File not found**
- Solution: Ensure proof scripts exist in `scientific_method_tool/`
- Check: `ls scientific_method_tool/prove_*.py`

**Error: Permission denied**
- Solution: Check file permissions on storage directory
- Fix: `chmod -R u+w scientific_method_tool/experiments/`

---

## Related Commands

- **`/play-the-game`**: Run D&D scenario (used in real experiment proof)
- **`/reflect`**: Reflect on proof results
- **`/analyze`**: Analyze experiment results

---

**This command proves the scientific method tool is fully functional and ready for experimental verification.**

--- End Command ---
