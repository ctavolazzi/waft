# Decide

**Run mathematical decision matrix calculations using documented decision-making techniques.**

Performs multi-step complex calculations using established methodologies (Weighted Sum Model, Analytic Hierarchy Process, etc.) to help make well-calculated decisions based on data, context, and structured analysis.

**Use when:** You need to make an important decision, evaluate multiple options, or want a quantitative analysis of alternatives.

---

## Purpose

This command provides:
- **Structured Decision Analysis**: Uses documented decision-making methodologies
- **Mathematical Calculations**: Performs multi-step complex calculations
- **Interactive Data Gathering**: Asks questions to collect criteria, weights, and scores
- **Quantitative Results**: Provides calculated scores and rankings
- **Transparent Reasoning**: Shows how calculations were performed
- **Multiple Methodologies**: Supports different decision matrix techniques

---

## Philosophy

1. **Data-Driven**: Decisions based on quantitative analysis, not just intuition
2. **Structured Approach**: Uses established methodologies from decision science
3. **Transparent Process**: Shows all calculations and reasoning
4. **Interactive**: Asks questions to gather necessary data
5. **Comprehensive**: Considers multiple criteria and alternatives

---

## Decision Matrix Methodologies

### 1. Weighted Sum Model (WSM) / Simple Additive Weighting (SAW)
**Default Method** - Most commonly used

**Formula**: 
```
Total Score = Σ (Weight_i × Score_i) for all criteria
```

**Steps**:
1. Identify alternatives
2. Define criteria
3. Assign weights to criteria (sum to 1.0 or 100%)
4. Score each alternative on each criterion (typically 1-10 scale)
5. Calculate weighted scores
6. Sum weighted scores for each alternative
7. Rank alternatives by total score

**Best For**: Most general decision problems, straightforward comparisons

---

### 2. Analytic Hierarchy Process (AHP)
**Advanced Method** - Pairwise comparisons

**Steps**:
1. Structure problem hierarchically
2. Perform pairwise comparisons of criteria
3. Calculate consistency ratio
4. Derive weights from comparisons
5. Score alternatives on each criterion
6. Calculate weighted scores
7. Rank alternatives

**Best For**: Complex decisions with many criteria, when relative importance needs careful consideration

---

### 3. Weighted Product Model (WPM)
**Multiplicative Method** - Accounts for ratios

**Formula**:
```
Total Score = Π (Score_i ^ Weight_i) for all criteria
```

**Best For**: When criteria have multiplicative relationships, avoiding normalization issues

---

### 4. Best Worst Method (BWM)
**Simplified Pairwise** - Focuses on best and worst criteria

**Steps**:
1. Identify best and worst criteria
2. Compare best to all others
3. Compare all others to worst
4. Calculate optimal weights
5. Score and rank alternatives

**Best For**: When you can clearly identify best/worst criteria, faster than full AHP

---

## Execution Steps

### Phase 1: Problem Definition

1. **Understand the Decision**
   - What decision needs to be made?
   - What is the context?
   - What are the constraints?
   - What is the timeline?

2. **Identify Alternatives**
   - List all viable options
   - Include "do nothing" if relevant
   - Consider hybrid approaches
   - Ensure alternatives are mutually exclusive

### Phase 2: Criteria Development

3. **Define Evaluation Criteria**
   - What factors matter for this decision?
   - What are the success criteria?
   - What are the constraints?
   - What are the risks?

4. **Categorize Criteria** (Optional)
   - Must-have vs. nice-to-have
   - Cost vs. benefit
   - Risk vs. reward
   - Short-term vs. long-term

### Phase 3: Weighting

5. **Assign Weights to Criteria**
   - How important is each criterion relative to others?
   - Use consistent scale (1-10, percentages, or pairwise comparison)
   - Ensure weights sum to 1.0 (or normalize)
   - Consider using AHP for complex weighting

### Phase 4: Scoring

6. **Score Each Alternative**
   - Evaluate each alternative on each criterion
   - Use consistent scale (1-10 recommended)
   - Consider objective data when available
   - Document reasoning for scores

### Phase 5: Calculation

7. **Perform Calculations**
   - Calculate weighted scores for each alternative
   - Sum (WSM) or multiply (WPM) as appropriate
   - Calculate sensitivity analysis
   - Check for consistency (AHP)

### Phase 6: Analysis

8. **Analyze Results**
   - Rank alternatives by total score
   - Identify score differences
   - Consider sensitivity to weight changes
   - Evaluate if results make sense

### Phase 7: Presentation

9. **Present Findings**
   - Show decision matrix table
   - Display calculations
   - Present rankings
   - Provide recommendations
   - Show sensitivity analysis

---

## Interactive Questions

The command will ask:

1. **Decision Context**
   - "What decision are you trying to make?"
   - "What is the context or background?"
   - "What are the constraints or requirements?"

2. **Alternatives**
   - "What are the options/alternatives you're considering?"
   - "Should we include 'do nothing' as an option?"
   - "Are there any hybrid approaches to consider?"

3. **Criteria**
   - "What criteria should we use to evaluate these alternatives?"
   - "What factors are most important?"
   - "What are the must-have vs. nice-to-have criteria?"

4. **Weights**
   - "How important is [criterion] relative to [other criterion]?"
   - "On a scale of 1-10, how important is [criterion]?"
   - "Should we use pairwise comparison (AHP) for weighting?"

5. **Scores**
   - "On a scale of 1-10, how does [alternative] perform on [criterion]?"
   - "What data supports this score?"
   - "What are the risks/concerns with this score?"

---

## Output Format

### Decision Matrix Table

```
┌──────────────┬──────┬──────┬──────┬──────┬──────────┐
│ Alternative  │ Crit1│ Crit2│ Crit3│ Total│ Rank     │
│              │(0.4) │(0.3) │(0.3) │Score │          │
├──────────────┼──────┼──────┼──────┼──────┼──────────┤
│ Option A     │  8   │  7   │  9   │ 7.8  │ 🥇 1st   │
│ Option B     │  6   │  9   │  7   │ 7.2  │ 🥈 2nd   │
│ Option C     │  9   │  5   │  8   │ 7.5  │ 🥉 3rd   │
└──────────────┴──────┴──────┴──────┴──────┴──────────┘
```

### Calculation Details

**Weighted Scores for Option A**:
- Criterion 1: 8 × 0.4 = 3.2
- Criterion 2: 7 × 0.3 = 2.1
- Criterion 3: 9 × 0.3 = 2.7
- **Total: 8.0**

### Sensitivity Analysis

Shows how results change if weights are adjusted:
- "If Criterion 1 weight increases by 10%, Option A still wins"
- "If Criterion 2 weight decreases by 20%, Option B becomes best"

### Recommendations

**Recommended Alternative**: Option A (Score: 8.0)

**Reasoning**:
- Highest total score across all criteria
- Strong performance on most important criterion (Criterion 1: 8/10)
- Balanced performance across all criteria
- Lowest risk of poor outcomes

**When to Consider Alternatives**:
- Option B: If Criterion 2 becomes more important
- Option C: If Criterion 1 becomes less important

---

## Mathematical Formulas

### Weighted Sum Model (WSM)

```
For each alternative i:
  Total_Score_i = Σ (Weight_j × Score_ij) for all criteria j

Where:
  Weight_j = weight of criterion j (Σ weights = 1.0)
  Score_ij = score of alternative i on criterion j
```

### Normalization (if needed)

```
Normalized_Score = (Raw_Score - Min_Score) / (Max_Score - Min_Score)
```

### Consistency Ratio (AHP)

```
CR = CI / RI

Where:
  CI = (λ_max - n) / (n - 1)
  λ_max = maximum eigenvalue
  n = number of criteria
  RI = random index (from table)

CR < 0.1 indicates acceptable consistency
```

---

## Use Cases

### 1. Technology Choice
**Scenario**: Choosing between frameworks/libraries

**Example**:
```
User: "Should we use FastAPI or Flask for this project? /decide"
```

**Process**:
- Alternatives: FastAPI, Flask, Django
- Criteria: Performance, Learning curve, Ecosystem, Documentation
- Weights: Based on project priorities
- Scores: Based on research and experience
- Result: Calculated recommendation

---

### 2. Architecture Decision
**Scenario**: Choosing between design patterns

**Example**:
```
User: "Should we use microservices or monolith? /decide"
```

**Process**:
- Alternatives: Microservices, Monolith, Hybrid
- Criteria: Complexity, Scalability, Development speed, Maintenance
- Weights: Based on team size and requirements
- Scores: Based on project context
- Result: Quantitative recommendation

---

### 3. Feature Priority
**Scenario**: Deciding which features to build first

**Example**:
```
User: "Which feature should we prioritize? /decide"
```

**Process**:
- Alternatives: Feature A, Feature B, Feature C
- Criteria: User value, Development effort, Business impact, Risk
- Weights: Based on business priorities
- Scores: Based on estimates
- Result: Prioritized feature list

---

### 4. Resource Allocation
**Scenario**: Deciding how to allocate time/budget

**Example**:
```
User: "How should we allocate our development time? /decide"
```

**Process**:
- Alternatives: Different allocation strategies
- Criteria: Impact, Urgency, Feasibility, ROI
- Weights: Based on business goals
- Scores: Based on data
- Result: Optimal allocation

---

## Methodology Selection Guide

**Use WSM (Weighted Sum Model) when**:
- ✅ Straightforward decision with clear criteria
- ✅ Criteria are independent
- ✅ Quick decision needed
- ✅ Most common use case

**Use AHP (Analytic Hierarchy Process) when**:
- ✅ Complex decision with many criteria
- ✅ Need to carefully consider relative importance
- ✅ Want consistency checking
- ✅ Have time for pairwise comparisons

**Use WPM (Weighted Product Model) when**:
- ✅ Criteria have multiplicative relationships
- ✅ Want to avoid normalization issues
- ✅ Dealing with ratios or percentages

**Use BWM (Best Worst Method) when**:
- ✅ Can clearly identify best and worst criteria
- ✅ Want faster than AHP but more structured than WSM
- ✅ Need to reduce comparison complexity

---

## Best Practices

1. **Be Specific**: Clear alternatives and criteria
2. **Be Honest**: Realistic scores, not optimistic
3. **Be Consistent**: Use same scale throughout
4. **Be Complete**: Consider all relevant criteria
5. **Be Transparent**: Document reasoning for weights and scores
6. **Be Flexible**: Adjust if results don't make sense

---

## Advanced Features

### Sensitivity Analysis
Shows how results change with weight adjustments:
- "What if Criterion 1 is 20% more important?"
- "What if Criterion 2 is 30% less important?"
- Identifies critical weights that change the decision

### Scenario Planning
Evaluates alternatives under different scenarios:
- "How do options perform in best-case scenario?"
- "How do options perform in worst-case scenario?"
- "What if constraints change?"

### Risk-Adjusted Scoring
Incorporates uncertainty:
- Expected value calculations
- Risk-adjusted scores
- Confidence intervals

### Multi-Stakeholder Analysis
Considers different perspectives:
- Weight sets for different stakeholders
- Consensus vs. individual preferences
- Conflict resolution

---

## Example Workflow

```
User: "/decide"

AI: "What decision are you trying to make?"
User: "Should we refactor this code now or add the feature first?"

AI: "What are the alternatives you're considering?"
User: "1) Refactor now, 2) Add feature first, 3) Do both in parallel"

AI: "What criteria should we use to evaluate these?"
User: "Code quality, Time to market, Risk, Technical debt"

AI: "How important is each criterion? (weights should sum to 1.0)"
User: "Code quality: 0.3, Time to market: 0.4, Risk: 0.2, Technical debt: 0.1"

AI: "On a scale of 1-10, how does 'Refactor now' score on 'Code quality'?"
User: "9"

AI: "How does 'Refactor now' score on 'Time to market'?"
User: "4"

[... continues for all alternatives and criteria ...]

AI: [Performs calculations]

AI: [Presents decision matrix, calculations, rankings, recommendations]
```

---

## Integration with Other Commands

- **`/consider`**: Qualitative analysis (complements `/decide`)
- **`/verify`**: Verify data before decision
- **`/checkpoint`**: Document decision process
- **`/explore`**: Understand context before deciding

---

## When to Use

**Use `/decide` when**:
- ✅ Multiple viable alternatives exist
- ✅ Decision has significant impact
- ✅ Need quantitative analysis
- ✅ Want structured, documented process
- ✅ Criteria can be quantified
- ✅ Want to reduce bias in decision-making

**Don't use `/decide` when**:
- ❌ Only one viable option
- ❌ Decision is trivial
- ❌ Criteria are purely subjective/emotional
- ❌ Need immediate action (use `/consider` for quick analysis)
- ❌ Alternatives are not well-defined

---

## Mathematical Rigor

This command implements:
- ✅ Established decision science methodologies
- ✅ Peer-reviewed techniques (WSM, AHP, WPM, BWM)
- ✅ Proper normalization and weighting
- ✅ Sensitivity analysis
- ✅ Consistency checking (AHP)
- ✅ Transparent calculations

**References**:
- Saaty, T.L. (1980). The Analytic Hierarchy Process
- Triantaphyllou, E. (2000). Multi-Criteria Decision Making Methods
- Rezaei, J. (2015). Best-worst multi-criteria decision-making method

---

**This command helps make better decisions through structured, quantitative analysis using documented decision-making techniques.**

---

## Implementation Example

When executed, the command will:

1. **Ask for Decision Context**
   ```
   "What decision are you trying to make?"
   → User: "Should we refactor this code now or add the feature first?"
   
   "What is the context or background?"
   → User: "We have technical debt but also need to ship features quickly"
   ```

2. **Identify Alternatives**
   ```
   "What are the options you're considering?"
   → User: "1) Refactor now, 2) Add feature first, 3) Do both in parallel"
   
   "Should we include 'do nothing' as an option?"
   → User: "No"
   ```

3. **Define Criteria**
   ```
   "What criteria should we use to evaluate these alternatives?"
   → User: "Code quality, Time to market, Risk, Technical debt"
   
   "Any other criteria?"
   → User: "No"
   ```

4. **Assign Weights (WSM Method)**
   ```
   "How important is each criterion? (weights should sum to 1.0)"
   
   "Code quality (0-1 scale):"
   → User: "0.3"
   
   "Time to market (0-1 scale):"
   → User: "0.4"
   
   "Risk (0-1 scale):"
   → User: "0.2"
   
   "Technical debt (0-1 scale):"
   → User: "0.1"
   
   "Total: 1.0 ✓"
   ```

5. **Score Alternatives**
   ```
   "On a scale of 1-10, how does 'Refactor now' score on 'Code quality'?"
   → User: "9"
   
   "Reasoning (optional):"
   → User: "Eliminates technical debt, improves maintainability"
   
   "How does 'Refactor now' score on 'Time to market'?"
   → User: "4"
   
   "Reasoning:"
   → User: "Delays feature delivery by 2 weeks"
   
   [... continues for all alternatives and criteria ...]
   ```

6. **Perform Calculations**
   ```
   Calculating weighted scores...
   
   Option: Refactor now
   - Code quality: 9 × 0.3 = 2.7
   - Time to market: 4 × 0.4 = 1.6
   - Risk: 6 × 0.2 = 1.2
   - Technical debt: 9 × 0.1 = 0.9
   Total: 6.4
   
   Option: Add feature first
   - Code quality: 5 × 0.3 = 1.5
   - Time to market: 9 × 0.4 = 3.6
   - Risk: 7 × 0.2 = 1.4
   - Technical debt: 3 × 0.1 = 0.3
   Total: 6.8
   
   Option: Do both in parallel
   - Code quality: 7 × 0.3 = 2.1
   - Time to market: 6 × 0.4 = 2.4
   - Risk: 5 × 0.2 = 1.0
   - Technical debt: 6 × 0.1 = 0.6
   Total: 6.1
   ```

7. **Present Results**
   ```
   ┌─────────────────────┬──────────┬──────────┬──────┬──────────┬──────────┐
   │ Alternative         │ Code Q   │ Time     │ Risk │ Tech Debt│ Total    │
   │                     │ (0.3)    │ (0.4)    │(0.2) │ (0.1)    │ Score    │
   ├─────────────────────┼──────────┼──────────┼──────┼──────────┼──────────┤
   │ Add feature first   │ 5 (1.5)  │ 9 (3.6)  │ 7(1.4)│ 3 (0.3)  │ 6.8 🥇  │
   │ Refactor now        │ 9 (2.7)  │ 4 (1.6)  │ 6(1.2)│ 9 (0.9)  │ 6.4 🥈  │
   │ Do both in parallel │ 7 (2.1)  │ 6 (2.4)  │ 5(1.0)│ 6 (0.6)  │ 6.1 🥉  │
   └─────────────────────┴──────────┴──────────┴──────┴──────────┴──────────┘
   
   Recommended: Add feature first (Score: 6.8)
   
   Reasoning:
   - Highest total score (6.8)
   - Strong performance on most important criterion (Time to market: 9/10)
   - Acceptable trade-offs on other criteria
   - Lowest risk of missing deadlines
   
   Sensitivity Analysis:
   - If "Time to market" weight increases by 20%: Still wins (7.0 vs 6.0)
   - If "Code quality" weight increases by 30%: "Refactor now" becomes best (7.0 vs 6.8)
   ```

---

## Code Integration

The command uses standardized modules:

### Core Modules

1. **`waft.core.decision_matrix`** - Mathematical calculations
   - `DecisionMatrixCalculator` - Main calculator class
   - `calculate_wsm()` - Weighted Sum Model
   - `calculate_wpm()` - Weighted Product Model
   - `calculate_ahp_weights()` - AHP weight calculation
   - `calculate_consistency_ratio()` - AHP consistency checking
   - `calculate_bwm_weights()` - Best Worst Method
   - `sensitivity_analysis()` - Weight adjustment analysis

2. **`waft.core.decision_cli`** - Standardized CLI interface ⭐
   - `DecisionCLI` - Reusable CLI handler
   - `run_decision_matrix()` - Standardized calculation workflow
   - Consistent output formatting
   - Built-in sensitivity analysis

### Standardized Usage

**Recommended Approach** (via DecisionCLI):
```python
from waft.core.decision_cli import DecisionCLI
from pathlib import Path

cli = DecisionCLI(Path('.'))

results = cli.run_decision_matrix(
    problem="What should we do next?",
    alternatives=["Option A", "Option B", "Option C"],
    criteria={
        "Criterion 1": 0.4,
        "Criterion 2": 0.6,
    },
    scores={
        "Option A": {"Criterion 1": 8.0, "Criterion 2": 7.0},
        "Option B": {"Criterion 1": 6.0, "Criterion 2": 9.0},
        "Option C": {"Criterion 1": 7.0, "Criterion 2": 8.0},
    },
    methodology="WSM",
    show_details=True,
    show_sensitivity=True
)
```

**Direct Usage** (for advanced cases):
```python
from waft.core.decision_matrix import (
    DecisionMatrix, Alternative, Criterion, Score,
    DecisionMatrixCalculator
)

# Create matrix
matrix = DecisionMatrix(
    alternatives=[
        Alternative("Option A"),
        Alternative("Option B"),
    ],
    criteria=[
        Criterion("Criterion 1", 0.4),
        Criterion("Criterion 2", 0.6),
    ],
    scores=[
        Score("Option A", "Criterion 1", 8.0),
        Score("Option A", "Criterion 2", 7.0),
        Score("Option B", "Criterion 1", 6.0),
        Score("Option B", "Criterion 2", 9.0),
    ],
    methodology="WSM"
)

# Calculate
calculator = DecisionMatrixCalculator(matrix)
results = calculator.calculate_wsm()
rankings = calculator.rank_alternatives(results)
```

---

**This command helps make better decisions through structured, quantitative analysis using documented decision-making techniques.**
