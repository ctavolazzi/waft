# /prove-it - Prove Claims with Evidence

**Investigates claims from conversation, proves/disproves them, checks assumptions, and generates proof reports.**

---

## Purpose

This command investigates claims from the conversation and proves or disproves them by:
1. **Extracting claims** - From conversation context or explicit statement
2. **Running verification** - Checks system state, files, git status, etc.
3. **Checking assumptions** - Validates assumptions made during conversation
4. **Gathering evidence** - Searches codebase, reads files, checks implementations
5. **Building case file** - Creates comprehensive markdown case file with evidence
6. **Generating PDF report** - Creates PDF binder with verdict on cover

**If claims are false, the system will state so clearly with evidence.**

**Use when:**
- You want the AI to prove something it claimed
- You made a claim and want evidence
- You need verification of any statement
- You want to check assumptions made during conversation
- You need evidence-based confirmation with a report

---

## Execution

**Command**: `/prove-it [claim]` or `/prove [claim]`

**What it does:**
1. Extracts claim from conversation context or your explicit statement
2. Runs verification checks (date/time, disk space, git status, file existence, templates)
3. Checks assumptions made during conversation
4. Investigates codebase to gather evidence
5. Builds comprehensive case file with all evidence
6. Generates PDF report with verdict on cover
7. Opens PDF automatically (macOS/Windows/Linux)

**If no claim provided:**
- AI extracts the most recent claim from conversation context
- Or asks you to specify what to prove

**Execution:**
When you use `/prove-it [claim]`, you should:
1. Extract the claim from conversation context if not provided
2. Run: `python3 scripts/prove_it_comprehensive.py "[claim]"`
3. The script will:
   - Create case file in `_work_efforts/proof_cases/case_YYYYMMDD_HHMMSS.md`
   - Generate PDF in `_work_efforts/proof_cases/case_YYYYMMDD_HHMMSS.pdf`
   - Open the PDF automatically

---

## What Gets Proven

### 1. Claim Extraction
- ✅ AI identifies claim from conversation context
- ✅ Or uses explicit claim you provide
- ✅ Clarifies ambiguous claims

### 2. Verification Checks
- ✅ Date/Time verification
- ✅ Disk space check
- ✅ Working directory verification
- ✅ Git status check
- ✅ File existence verification
- ✅ Template verification

### 3. Assumption Checking
- ✅ Validates assumptions made during conversation
- ✅ Checks if assumptions are still valid
- ✅ Identifies invalid or outdated assumptions
- ✅ Provides evidence for each assumption

### 4. Codebase Investigation
- ✅ Searches for relevant code/files
- ✅ Reads implementations
- ✅ Checks function definitions
- ✅ Verifies actual behavior
- ✅ Examines git history if relevant

### 5. Evidence Gathering
- ✅ Code snippets as evidence
- ✅ File contents as proof
- ✅ Git commits/logs if relevant
- ✅ Test results if available
- ✅ Configuration files
- ✅ Documentation

### 6. Case File & PDF Generation
- ✅ Comprehensive markdown case file
- ✅ PDF binder with verdict on cover
- ✅ All evidence organized and presented
- ✅ Clear verdict: PROVEN/DISPROVEN/INCONCLUSIVE
- ✅ Confidence level (0-100%)

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

--- End Command ---
