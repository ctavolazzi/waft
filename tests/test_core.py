import pytest
import math
from waft.core.decision_matrix import (
    Criterion, Alternative, Score, DecisionMatrix, DecisionMatrixCalculator
)

# --- Fixtures ---
@pytest.fixture
def basic_matrix():
    alts = [Alternative("A"), Alternative("B")]
    crits = [Criterion("C1", 0.5), Criterion("C2", 0.5)]
    scores = [
        Score("A", "C1", 10.0), Score("A", "C2", 5.0),
        Score("B", "C1", 5.0),  Score("B", "C2", 10.0)
    ]
    return DecisionMatrix(alts, crits, scores)

# --- Happy Path Tests ---

def test_wsm_calculation(basic_matrix):
    calc = DecisionMatrixCalculator(basic_matrix)
    results = calc.calculate_wsm()
    # A: 0.5*10 + 0.5*5 = 7.5
    # B: 0.5*5 + 0.5*10 = 7.5
    assert results["A"] == 7.5
    assert results["B"] == 7.5

def test_deterministic_tie_breaking(basic_matrix):
    # Both score 7.5. "A" should be rank 1 because "A" < "B" alphabetically.
    calc = DecisionMatrixCalculator(basic_matrix)
    results = calc.calculate_wsm()
    ranks = calc.rank_alternatives(results)
    
    assert ranks[0][0] == "A"
    assert ranks[1][0] == "B"

# --- The "Diamond Plating" Security Tests ---

def test_reject_negative_weights():
    # Attempt to inject a negative weight
    alts = [Alternative("A")]
    crits = [Criterion("C1", 1.5), Criterion("C2", -0.5)] # Sums to 1.0, but invalid!
    scores = [Score("A", "C1", 1), Score("A", "C2", 1)]
    matrix = DecisionMatrix(alts, crits, scores)
    
    with pytest.raises(ValueError, match="negative weight"):
        DecisionMatrixCalculator(matrix)

def test_reject_nan_scores():
    # Attempt to inject NaN
    alts = [Alternative("A")]
    crits = [Criterion("C1", 1.0)]
    scores = [Score("A", "C1", float('nan'))]
    matrix = DecisionMatrix(alts, crits, scores)
    
    with pytest.raises(ValueError, match="not a finite number"):
        DecisionMatrixCalculator(matrix)

def test_reject_loose_tolerance():
    # Attempt 1% error (should fail now with strict 1e-6)
    alts = [Alternative("A")]
    crits = [Criterion("C1", 0.99)] 
    scores = [Score("A", "C1", 1)]
    matrix = DecisionMatrix(alts, crits, scores)
    
    with pytest.raises(ValueError, match="sum to 1.0"):
        DecisionMatrixCalculator(matrix)
