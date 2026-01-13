# Deep Game Science

**Run REAL game play with scientific method tracking - deep integration of /play-the-game with /science-bitch.**

Combines actual interactive game play (tavern scenario) with systematic scientific method tracking, capturing every dice roll, every choice, every outcome - all tracked scientifically and documented in a comprehensive PDF report.

**Use when:** You want to run REAL game play (not simulation) with complete scientific tracking, need comprehensive documentation of game play experiments, or want to prove the scientific method tool works with actual interactive scenarios.

---

## Purpose

This command provides:
- **REAL Game Play**: Actually runs the tavern scenario game (not simulation)
- **Scientific Tracking**: Every dice roll, every choice, every outcome tracked
- **Complete Scientific Method**: Full cycle from hypothesis to printed PDF
- **Comprehensive Documentation**: Beautiful PDF report with all real game play data
- **Material Output**: PDF printed to physical paper

---

## Philosophy

1. **Real Over Simulation**: Actually runs the game, not a simulation
2. **Complete Tracking**: Every roll, every check, every outcome captured
3. **Scientific Rigor**: Full scientific method cycle with real data
4. **Material Manifestation**: Digital work becomes physical (printed PDF)
5. **Trust Enables Depth**: User trust enables deeper integration

---

## Execution Steps

### Step 1: Form Hypothesis
**Purpose**: Create testable hypothesis about game play

**Actions**:
1. Form hypothesis about character skill performance
2. Define variables (investigation_skill, perception_skill)
3. Create prediction

**Output**: Hypothesis object ready for testing

---

### Step 2: Create Experiment
**Purpose**: Set up scientific experiment structure

**Actions**:
1. Create experiment manager
2. Create experiment with hypothesis
3. Set up data collection

**Output**: Experiment ready for execution

---

### Step 3: Capture Initial State (A)
**Purpose**: Save system state before experiment

**Actions**:
1. Capture initial components
2. Generate state hash
3. Save initial state

**Output**: Initial state snapshot

---

### Step 4: Run REAL Game Play
**Purpose**: Actually run the tavern scenario game

**Actions**:
1. Create character with REAL dice rolls (4d6, drop lowest)
2. Run actual tavern scenario
3. Capture every dice roll as it happens
4. Track every skill check
5. Record every game event
6. Collect data during execution (C)

**Output**: Real game play results with all data

---

### Step 5: Capture Final State (B)
**Purpose**: Save system state after experiment

**Actions**:
1. Capture final components
2. Generate state hash
3. Compare with initial state

**Output**: Final state snapshot with comparison

---

### Step 6: Analyze Results
**Purpose**: Verify/refute hypothesis with evidence

**Actions**:
1. Analyze collected data
2. Verify hypothesis
3. Calculate confidence
4. Generate conclusions

**Output**: Analysis with confidence and conclusions

---

### Step 7: Generate Comprehensive PDF
**Purpose**: Create beautiful documentation

**Actions**:
1. Build comprehensive report with:
   - Abstract briefing
   - Hypothesis and variables
   - Initial state (A)
   - REAL game play execution details
   - Data collection (C)
   - Final state (B)
   - Results and analysis
   - PROOF section (proof on paper)
2. Generate ArXiv-style academic PDF
3. Save markdown source

**Output**: Comprehensive PDF report

---

### Step 8: Print to Material World
**Purpose**: Manifest digital work as physical document

**Actions**:
1. Open PDF
2. Print PDF to default printer
3. Confirm printing

**Output**: Physical PDF on desk

---

## Complete Workflow Sequence

```
1. Form Hypothesis          → Testable hypothesis about game play
2. Create Experiment        → Scientific experiment structure
3. Capture State A          → Initial state snapshot
4. Run REAL Game Play       → Actual game with real dice rolls
5. Collect Data C           → Continuous measurements during game
6. Capture State B          → Final state snapshot
7. Analyze Results          → Verify/refute hypothesis
8. Generate PDF             → Comprehensive documentation
9. Print PDF                → Material world output
```

---

## Key Features

### REAL Game Play
- **Actual Dice Rolls**: Real random numbers, not simulated
- **Real Choices**: Actual decision points in game
- **Real Outcomes**: Actual results from real rolls
- **Real Character**: Created with real dice (4d6, drop lowest)

### Scientific Tracking
- **Every Dice Roll**: Tracked with roll, modifier, total, DC, success
- **Every Skill Check**: Type, roll, modifier, total, success, outcome
- **Every Game Event**: All events recorded with details
- **Complete Data Series**: 17+ data series collected

### Comprehensive Documentation
- **Abstract**: Complete briefing on what happened
- **Hypothesis**: Testable hypothesis with variables
- **Initial State (A)**: System state before
- **REAL Game Play**: Actual execution details
- **Data Collection (C)**: All measurements
- **Final State (B)**: System state after
- **Results**: Analysis with confidence
- **PROOF Section**: Literal proof on paper

### Material Output
- **PDF Generated**: Beautiful ArXiv-style academic paper
- **PDF Opened**: Automatically opened for viewing
- **PDF Printed**: Sent to printer automatically

---

## Usage Examples

### Basic Execution
```
/deep-game-science
```

Runs complete workflow: hypothesis → experiment → REAL game play → analysis → PDF → print

### With Custom Hypothesis
```
/deep-game-science --hypothesis "Higher charisma improves social outcomes"
```

Starts with custom hypothesis

### With Custom Choices
```
/deep-game-science --choices "2,y,1"
```

Uses custom game play choices (Investigation, read note, investigate)

---

## Integration

This command integrates:
- **`/play-the-game`**: Actually runs the tavern scenario
- **`/science-bitch`**: Scientific method workflow
- **PDF Generation**: Academic paper template
- **Printing**: Material world output

---

## When to Use

**Use `/deep-game-science` when**:
- ✅ Want REAL game play (not simulation)
- ✅ Need complete scientific tracking
- ✅ Want comprehensive documentation
- ✅ Need proof on paper
- ✅ Want material output (printed PDF)
- ✅ Testing scientific method with real scenarios

**Don't use `/deep-game-science` when**:
- ❌ Just need quick game play (use `/play-the-game`)
- ❌ Just need scientific method (use `/science-bitch`)
- ❌ Don't need real game play (use simulation)
- ❌ Don't need printed output

---

## Output

After completion, provides:
1. **Experiment Results**: Fitness gained, dice rolls, skill checks, events
2. **Analysis**: Hypothesis verification with confidence
3. **PDF Report**: Comprehensive documentation (70-80KB)
4. **Printed PDF**: Physical document on desk
5. **Markdown Source**: Source markdown for PDF

---

## Technical Details

### Experiment Script
- **Location**: `experiments/deep_tavern_science_experiment.py`
- **Dependencies**: scientific_method_tool, waft.being, waft.core.dnd5e, examples.tavern_scenario
- **Execution**: `python3 experiments/deep_tavern_science_experiment.py`

### PDF Generation
- **Template**: ArXiv-style academic paper
- **Location**: `_science/reports/Deep_Tavern_Science_Experiment_*.pdf`
- **Size**: ~70-80KB
- **Format**: Two-column academic layout

### Printing
- **Method**: `lpr` command (macOS)
- **Platform**: Auto-detects and uses appropriate method
- **Output**: Default printer

---

## Example Output

```
======================================================================
🔬 DEEP TAVERN SCIENCE EXPERIMENT
REAL Game Play with Scientific Method
======================================================================

Step 1: Form Hypothesis
   ✓ Hypothesis: Higher investigation and perception skills improve...
   ✓ Prediction: Characters with investigation skill > 40...

Step 2: Create Experiment
   ✓ Experiment ID: exp_c0cc4f15

Step 3: Capture Initial State (A)
   ✓ State hash: e0fdd0613af2ca5d...
   ✓ Components: ['investigation_skill', 'perception_skill', ...]

Step 4: Run REAL Experiment (Actual Game Play)
   🎲 Creating Character with Real Dice Rolls...
   🎮 Running REAL Tavern Scenario...
   ✓ Fitness gained: 16.0
   ✓ Events: 5
   ✓ Dice rolls: 1
   ✓ Skill checks: 1
   ✓ Successful checks: 0

Step 5: Verify Data Collection (C)
   ✓ fitness: 2 data points
   ✓ dice_roll: 1 data points
   ✓ skill_check_success: 1 data points
   ... (17 total data series)

Step 6: Verify Final State (B)
   ✓ State hash: 0926b5be0f91589e...

Step 7: Analyze Results
   ✓ Verified: True
   ✓ Confidence: 64.0%
   ✓ Conclusions: Hypothesis VERIFIED...

Step 8: Generate Comprehensive PDF Report
   📄 Generating comprehensive PDF report...
   → Generating ArXiv-style academic PDF...
   ✅ PDF generated: _science/reports/Deep_Tavern_Science_Experiment_*.pdf

   🖨️  Printing PDF to material world...
   ✅ PDF sent to printer!

======================================================================
✅ DEEP EXPERIMENT COMPLETE!
======================================================================
```

---

## Related Commands

- **`/play-the-game`**: Run tavern scenario (game play only)
- **`/science-bitch`**: Scientific method workflow (without game play)
- **`/prove-it`**: Prove scientific method tool works
- **`/reflect`**: Reflect on experiment results

---

## The Difference

This command goes **deeper** than simulation:
- **Simulation**: Approximates game play
- **Deep Game Science**: Actually runs the game with real dice rolls

This is the REAL integration - not simulation, but actual game play tracked scientifically.

---

**This command combines REAL game play with scientific method tracking, generating comprehensive documentation and printing it to the material world - proving the system works with actual interactive scenarios.**

--- End Command ---
