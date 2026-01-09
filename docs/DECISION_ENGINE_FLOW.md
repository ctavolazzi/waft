# Decision Engine - Detailed Execution Flow

**Purpose**: Step-by-step breakdown of exactly what happens when you call the decision engine.

---

## Complete Execution Trace

### Example Input

```python
cli = DecisionCLI(Path('.'))
results = cli.run_decision_matrix(
    problem="How to improve dashboard?",
    alternatives=["Remove Cards", "Make Visual", "Hybrid"],
    criteria={"At-a-Glance": 0.25, "Standard": 0.20, "Clarity": 0.20, "Effort": 0.15, "Impact": 0.20},
    scores={
        "Remove Cards": {"At-a-Glance": 8, "Standard": 6, "Clarity": 9, "Effort": 9, "Impact": 7},
        "Make Visual": {"At-a-Glance": 9, "Standard": 9, "Clarity": 8, "Effort": 6, "Impact": 8},
        "Hybrid": {"At-a-Glance": 10, "Standard": 10, "Clarity": 10, "Effort": 5, "Impact": 10},
    },
    methodology="WSM"
)
```

---

## Step-by-Step Execution

### Phase 1: Input Validation (DecisionCLI.run_decision_matrix)

**Step 1.1**: Validate weights sum to 1.0
```python
total_weight = sum(criteria.values())
# total_weight = 0.25 + 0.20 + 0.20 + 0.15 + 0.20 = 1.0
if abs(total_weight - 1.0) > 0.01:  # ✓ Passes
    raise ValueError(...)
```

**Step 1.2**: Validate all alternatives have scores
```python
for alt_name, crit_scores in scores.items():
    if alt_name not in alternatives:  # ✓ All present
        raise ValueError(...)
    for crit_name, score_value in crit_scores.items():
        if crit_name not in criteria:  # ✓ All present
            raise ValueError(...)
```

**Result**: ✓ Input validated, proceed

---

### Phase 2: Data Structure Building

**Step 2.1**: Build Alternative objects
```python
alt_objects = [Alternative(name) for name in alternatives]
# Result:
# [
#   Alternative(name="Remove Cards"),
#   Alternative(name="Make Visual"),
#   Alternative(name="Hybrid")
# ]
```

**Step 2.2**: Build Criterion objects
```python
crit_objects = []
for name, weight in criteria.items():
    crit_objects.append(Criterion(name, weight, description))
# Result:
# [
#   Criterion(name="At-a-Glance", weight=0.25),
#   Criterion(name="Standard", weight=0.20),
#   Criterion(name="Clarity", weight=0.20),
#   Criterion(name="Effort", weight=0.15),
#   Criterion(name="Impact", weight=0.20)
# ]
```

**Step 2.3**: Build Score objects
```python
score_objects = []
for alt_name, crit_scores in scores.items():
    for crit_name, score_value in crit_scores.items():
        score_objects.append(Score(alt_name, crit_name, score_value))
# Result: 15 Score objects (3 alternatives × 5 criteria)
# [
#   Score("Remove Cards", "At-a-Glance", 8),
#   Score("Remove Cards", "Standard", 6),
#   Score("Remove Cards", "Clarity", 9),
#   Score("Remove Cards", "Effort", 9),
#   Score("Remove Cards", "Impact", 7),
#   Score("Make Visual", "At-a-Glance", 9),
#   ... (10 more)
# ]
```

---

### Phase 3: Matrix Creation

**Step 3.1**: Create DecisionMatrix
```python
matrix = DecisionMatrix(
    alternatives=alt_objects,      # 3 alternatives
    criteria=crit_objects,         # 5 criteria
    scores=score_objects,          # 15 scores
    methodology="WSM"
)
```

**Result**: Complete DecisionMatrix dataclass instance

---

### Phase 4: Calculator Initialization

**Step 4.1**: Create DecisionMatrixCalculator
```python
calculator = DecisionMatrixCalculator(matrix)
```

**Step 4.2**: Automatic validation (_validate_matrix)

**Check 4.2.1**: Weights sum to 1.0
```python
total_weight = sum(c.weight for c in self.matrix.criteria)
# total_weight = 0.25 + 0.20 + 0.20 + 0.15 + 0.20 = 1.0
if abs(total_weight - 1.0) > 0.01:  # ✓ Passes
    raise ValueError(...)
```

**Check 4.2.2**: All alternatives scored on all criteria
```python
for alt in self.matrix.alternatives:  # 3 alternatives
    for crit in self.matrix.criteria:  # 5 criteria
        matching_scores = [
            s for s in self.matrix.scores
            if s.alternative_name == alt.name 
            and s.criterion_name == crit.name
        ]
        if not matching_scores:  # ✓ All have scores
            raise ValueError(...)
```

**Result**: ✓ Matrix validated, calculator ready

---

### Phase 5: Calculation (WSM Method)

**Step 5.1**: Call calculate_wsm()
```python
results = calculator.calculate_wsm()
```

**Step 5.2**: For each alternative, calculate weighted sum

**Alternative: "Remove Cards"**
```python
total_score = 0.0

# Criterion: "At-a-Glance" (weight=0.25, score=8)
score_obj = Score("Remove Cards", "At-a-Glance", 8)
weighted_score = 0.25 × 8 = 2.0
total_score += 2.0  # total_score = 2.0

# Criterion: "Standard" (weight=0.20, score=6)
score_obj = Score("Remove Cards", "Standard", 6)
weighted_score = 0.20 × 6 = 1.2
total_score += 1.2  # total_score = 3.2

# Criterion: "Clarity" (weight=0.20, score=9)
score_obj = Score("Remove Cards", "Clarity", 9)
weighted_score = 0.20 × 9 = 1.8
total_score += 1.8  # total_score = 5.0

# Criterion: "Effort" (weight=0.15, score=9)
score_obj = Score("Remove Cards", "Effort", 9)
weighted_score = 0.15 × 9 = 1.35
total_score += 1.35  # total_score = 6.35

# Criterion: "Impact" (weight=0.20, score=7)
score_obj = Score("Remove Cards", "Impact", 7)
weighted_score = 0.20 × 7 = 1.4
total_score += 1.4  # total_score = 7.75

results["Remove Cards"] = 7.75
```

**Alternative: "Make Visual"**
```python
total_score = 0.0
# At-a-Glance: 0.25 × 9 = 2.25
# Standard: 0.20 × 9 = 1.8
# Clarity: 0.20 × 8 = 1.6
# Effort: 0.15 × 6 = 0.9
# Impact: 0.20 × 8 = 1.6
# Total: 2.25 + 1.8 + 1.6 + 0.9 + 1.6 = 8.15
results["Make Visual"] = 8.15
```

**Alternative: "Hybrid"**
```python
total_score = 0.0
# At-a-Glance: 0.25 × 10 = 2.5
# Standard: 0.20 × 10 = 2.0
# Clarity: 0.20 × 10 = 2.0
# Effort: 0.15 × 5 = 0.75
# Impact: 0.20 × 10 = 2.0
# Total: 2.5 + 2.0 + 2.0 + 0.75 + 2.0 = 9.25
results["Hybrid"] = 9.25
```

**Result**:
```python
{
    "Remove Cards": 7.75,
    "Make Visual": 8.15,
    "Hybrid": 9.25
}
```

---

### Phase 6: Ranking

**Step 6.1**: Call rank_alternatives()
```python
rankings = calculator.rank_alternatives(results)
```

**Step 6.2**: Sort by score descending
```python
sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)
# [
#   ("Hybrid", 9.25),
#   ("Make Visual", 8.15),
#   ("Remove Cards", 7.75)
# ]
```

**Step 6.3**: Assign ranks
```python
ranked = [(name, score, rank + 1) for rank, (name, score) in enumerate(sorted_items)]
# [
#   ("Hybrid", 9.25, 1),
#   ("Make Visual", 8.15, 2),
#   ("Remove Cards", 7.75, 3)
# ]
```

**Result**: Rankings list with explicit ranks

---

### Phase 7: Display Results

**Step 7.1**: Display criteria and weights
```
CRITERIA & WEIGHTS:
  At-a-Glance          0.25 (25%)
  Standard             0.20 (20%)
  Clarity              0.20 (20%)
  Effort               0.15 (15%)
  Impact               0.20 (20%)
```

**Step 7.2**: Display scoring matrix table
```
┌─────────────────────┬──────┬────────┬────────┬────────┬────────┬──────────┐
│ Alternative         │ At-… │ Stand… │ Clari… │ Effor… │ Impac… │ Weighted │
├─────────────────────┼──────┼────────┼────────┼────────┼────────┼──────────┤
│ Remove Cards        │    8 │      6 │      9 │      9 │      7 │     7.75 │
│ Make Visual         │    9 │      9 │      8 │      6 │      8 │     8.15 │
│ Hybrid              │   10 │     10 │     10 │      5 │     10 │     9.25 │
└─────────────────────┴──────┴────────┴────────┴────────┴────────┴──────────┘
```

**Step 7.3**: Display rankings
```
RANKINGS:
🥇 Hybrid                                    Score: 9.25
🥈 Make Visual                              Score: 8.15
🥉 Remove Cards                             Score: 7.75
```

**Step 7.4**: Display recommendation
```
RECOMMENDATION:
✅ Hybrid
   Weighted Score: 9.25
```

**Step 7.5**: Display detailed breakdown (if enabled)
```
DETAILED BREAKDOWN:

1. Hybrid (Score: 9.25)
   At-a-Glance          10/10 × 0.25 = 2.50
   Standard             10/10 × 0.20 = 2.00
   Clarity              10/10 × 0.20 = 2.00
   Effort                5/10 × 0.15 = 0.75
   Impact               10/10 × 0.20 = 2.00
```

**Step 7.6**: Sensitivity analysis (if enabled)
```
SENSITIVITY ANALYSIS:
Testing robustness by varying criterion weights...

  At-a-Glance weight -20%: Hybrid (score: 9.20)
  At-a-Glance weight +20%: Hybrid (score: 9.30)

Conclusion: Recommendation is robust across weight variations.
```

---

### Phase 8: Return Results

**Step 8.1**: Build results dictionary
```python
return {
    "problem": "How to improve dashboard?",
    "alternatives": ["Remove Cards", "Make Visual", "Hybrid"],
    "criteria": {"At-a-Glance": 0.25, ...},
    "methodology": "WSM",
    "results": {"Remove Cards": 7.75, "Make Visual": 8.15, "Hybrid": 9.25},
    "rankings": [("Hybrid", 9.25, 1), ("Make Visual", 8.15, 2), ("Remove Cards", 7.75, 3)],
    "recommendation": "Hybrid"
}
```

---

## Complete Data Transformation

```
INPUT (Python dicts)
  ↓
VALIDATION (Type & structure checks)
  ↓
DATACLASSES (Alternative, Criterion, Score)
  ↓
DECISIONMATRIX (Immutable container)
  ↓
VALIDATION (Completeness checks)
  ↓
CALCULATION (Mathematical operations)
  ↓
RESULTS (Dict[alternative: score])
  ↓
RANKING (List[(name, score, rank)])
  ↓
DISPLAY (Rich formatted output)
  ↓
OUTPUT (Structured results dict)
```

---

## Error Handling Points

1. **Input validation** → ValueError with specific message
2. **Matrix validation** → ValueError with missing data info
3. **Calculation** → ValueError if methodology unsupported
4. **Display** → Graceful degradation (no crash on display errors)

---

**Every step is traceable, every calculation is transparent, every result is interpretable.**
