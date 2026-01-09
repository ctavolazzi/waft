import math
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from .tracing import get_tracer, SpanStatus

# ==========================================
# 1. Immutable Data Structures
# ==========================================

@dataclass(frozen=True)
class Criterion:
    """
    Represents a single evaluation criterion.
    Immutable.
    """
    name: str
    weight: float
    description: Optional[str] = None

@dataclass(frozen=True)
class Alternative:
    """
    Represents an option being evaluated.
    Immutable.
    """
    name: str
    description: Optional[str] = None

@dataclass(frozen=True)
class Score:
    """
    Represents the score of an alternative for a specific criterion.
    Immutable.
    """
    alternative_name: str
    criterion_name: str
    value: float  # Using 'value' for clarity
    reasoning: Optional[str] = None

@dataclass(frozen=True)
class DecisionMatrix:
    """
    The container for the entire decision problem.
    Immutable once created.
    """
    alternatives: List[Alternative]
    criteria: List[Criterion]
    scores: List[Score]
    methodology: str = "WSM"

# ==========================================
# 2. The Mathematical Engine
# ==========================================

class DecisionMatrixCalculator:
    """
    Pure mathematical engine.
    Includes 'Diamond Plated' validation to prevent exploits.
    """

    def __init__(self, matrix: DecisionMatrix):
        self.matrix = matrix
        self._validate_matrix()

    def _validate_matrix(self):
        """
        Gatekeeper Method: Ensures the matrix is mathematically valid and secure.
        """
        # 1. Check for Negative Weights (Exploit Prevention)
        for c in self.matrix.criteria:
            if c.weight < 0:
                raise ValueError(f"Criterion '{c.name}' has negative weight: {c.weight}. Weights must be non-negative.")
            if not math.isfinite(c.weight):
                 raise ValueError(f"Criterion '{c.name}' has invalid weight: {c.weight}.")

        # 2. Check Weights sum to 1.0 (High Precision)
        total_weight = sum(c.weight for c in self.matrix.criteria)
        if not math.isclose(total_weight, 1.0, abs_tol=1e-6):
            raise ValueError(f"Criterion weights must sum to 1.0. Current sum: {total_weight:.6f}")

        # 3. Check for Finite Scores (NaN/Inf Prevention)
        for s in self.matrix.scores:
            if not math.isfinite(s.value):
                raise ValueError(f"Score for '{s.alternative_name}' on '{s.criterion_name}' is not a finite number.")

        # 4. Check Completeness (No Missing Data)
        existing_scores = {(s.alternative_name, s.criterion_name) for s in self.matrix.scores}
        for alt in self.matrix.alternatives:
            for crit in self.matrix.criteria:
                if (alt.name, crit.name) not in existing_scores:
                    raise ValueError(f"Missing score for Alternative '{alt.name}' on Criterion '{crit.name}'")

    def calculate_wsm(self) -> Dict[str, float]:
        """
        Weighted Sum Model (WSM).
        Formula: Score = Sum(Weight * Value)
        """
        tracer = get_tracer()
        span = tracer.start_span("decision_matrix.calculate_wsm", "core", data={
            "num_alternatives": len(self.matrix.alternatives),
            "num_criteria": len(self.matrix.criteria),
            "num_scores": len(self.matrix.scores)
        })

        try:
            results = {alt.name: 0.0 for alt in self.matrix.alternatives}
            weight_map = {c.name: c.weight for c in self.matrix.criteria}

            for score_obj in self.matrix.scores:
                if score_obj.alternative_name in results:
                    weight = weight_map.get(score_obj.criterion_name, 0.0)
                    results[score_obj.alternative_name] += weight * score_obj.value

            tracer.end_span(span, SpanStatus.SUCCESS, output_data={"results": results})
            return results
        except Exception as e:
            tracer.end_span(span, SpanStatus.ERROR, error=e)
            raise

    def rank_alternatives(self, scores: Dict[str, float]) -> List[Tuple[str, float, int]]:
        """
        Sorts alternatives deterministically.
        Primary Sort: Score (Descending)
        Secondary Sort: Name (Ascending) - Breaks ties alphabetically
        """
        tracer = get_tracer()
        span = tracer.start_span("decision_matrix.rank_alternatives", "core",
                                data={"scores": scores})

        try:
            # Sort key: (-score, name).
            # Negative score makes Python sort descending for float.
            # Name sorts ascending for string.
            sorted_items = sorted(scores.items(), key=lambda item: (-item[1], item[0]))

            ranked_results = []
            for rank, (name, score) in enumerate(sorted_items, start=1):
                ranked_results.append((name, score, rank))

            tracer.end_span(span, SpanStatus.SUCCESS,
                           output_data={"rankings": [(name, score, rank) for name, score, rank in ranked_results]})
            return ranked_results
        except Exception as e:
            tracer.end_span(span, SpanStatus.ERROR, error=e)
            raise

    def get_detailed_scores(self) -> Dict[str, Dict[str, float]]:
        """
        Helper for UI to get the breakdown of scores.
        """
        details = {alt.name: {} for alt in self.matrix.alternatives}
        for s in self.matrix.scores:
             if s.alternative_name in details:
                 details[s.alternative_name][s.criterion_name] = s.value
        return details
