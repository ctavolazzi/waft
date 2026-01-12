# /prove-it - Prove Scientific Method Tool Works

**Demonstrates that the scientific method tool is fully functional.**

---

## Purpose

This command proves that the scientific method tool works by running demonstration experiments that show:
1. Initial state capture (A)
2. Data collection during experiments (C)
3. Final state capture (B)
4. State comparison
5. Result analysis
6. File persistence

**Use when:**
- You want to verify the scientific method tool works
- You want to demonstrate the system to others
- You want to test the experimental framework
- You want to see the full scientific method cycle in action

---

## Execution

**Command**: `/prove-it` or `/prove`

**What it does:**
1. Runs simple proof demonstration
2. Runs real D&D experiment proof
3. Shows all captured states (A & B)
4. Shows collected data (C)
5. Displays analysis results
6. Verifies file persistence

**Execution Steps:**
1. Run `python3 scientific_method_tool/prove_it_works.py` (simple proof)
2. Run `python3 scientific_method_tool/prove_with_real_experiment.py` (real experiment)
3. Display results and verification

---

## What Gets Proven

### 1. State Capture (A & B)
- ✅ Initial state captured before experiment
- ✅ Final state captured after experiment
- ✅ State hashes for comparison
- ✅ Components tracked

### 2. Data Collection (C)
- ✅ Data points collected during experiment
- ✅ Data series with timestamps
- ✅ Multiple metrics tracked
- ✅ Data persisted to files

### 3. Experiment Execution
- ✅ Experiments run successfully
- ✅ Real Being and D&D character integration
- ✅ Hypothesis testing works
- ✅ Results captured

### 4. Analysis
- ✅ Hypothesis verification/refutation
- ✅ Confidence scoring
- ✅ Conclusions generated
- ✅ Recommendations provided

### 5. File Persistence
- ✅ Experiment files saved
- ✅ State files saved (initial & final)
- ✅ Data files saved
- ✅ All data recoverable

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
