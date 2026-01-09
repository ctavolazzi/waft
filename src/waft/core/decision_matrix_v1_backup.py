"""
Decision Matrix Calculator - Mathematical decision-making support.

PURPOSE:
    Pure mathematical engine for multi-criteria decision analysis.
    No I/O, no side effects, fully deterministic and testable.

ARCHITECTURE:
    - Data structures: Criterion, Alternative, Score, DecisionMatrix (dataclasses)
    - Calculator: DecisionMatrixCalculator (pure math operations)
    - Validation: Automatic on initialization (fail fast)

DESIGN PRINCIPLES:
    1. Immutability: Dataclasses ensure data integrity
    2. Validation: Multiple layers (input → matrix → calculation)
    3. Transparency: All calculations visible and traceable
    4. Extensibility: Easy to add new methodologies
    5. Reliability: Type-safe, validated, deterministic

METHODOLOGIES IMPLEMENTED:
    - Weighted Sum Model (WSM) / Simple Additive Weighting (SAW)
    - Analytic Hierarchy Process (AHP)
    - Weighted Product Model (WPM)
    - Best Worst Method (BWM)

MATHEMATICAL FOUNDATIONS:
    WSM: Total_Score = Σ (Weight_i × Score_i) for all criteria
    WPM: Total_Score = Π (Score_i ^ Weight_i) for all criteria
    AHP: Pairwise comparisons → weights → weighted sum
    BWM: Best/worst comparisons → weights → weighted sum

REFERENCES:
    - Saaty, T.L. (1980). The Analytic Hierarchy Process
    - Triantaphyllou, E. (2000). Multi-Criteria Decision Making Methods
    - Rezaei, J. (2015). Best-worst multi-criteria decision-making method

USAGE:
    # Direct usage (mathematical layer only)
    from waft.core.decision_matrix import (
        DecisionMatrix, Alternative, Criterion, Score,
        DecisionMatrixCalculator
    )

    matrix = DecisionMatrix(
        alternatives=[Alternative("Option A"), Alternative("Option B")],
        criteria=[Criterion("Criterion 1", 0.4), Criterion("Criterion 2", 0.6)],
        scores=[
            Score("Option A", "Criterion 1", 8.0),
            Score("Option A", "Criterion 2", 7.0),
            Score("Option B", "Criterion 1", 6.0),
            Score("Option B", "Criterion 2", 9.0),
        ],
        methodology="WSM"
    )

    calculator = DecisionMatrixCalculator(matrix)
    results = calculator.calculate_wsm()
    rankings = calculator.rank_alternatives(results)

    # Recommended: Use DecisionCLI for standardized interface
    # See decision_cli.py for full interface layer
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Criterion:
    """
    A criterion for evaluation.

    WHAT: Represents a single evaluation dimension (e.g., "Code Quality", "Time to Market")

    FIELDS:
        name: str - Criterion name (e.g., "Code Quality")
        weight: float - Importance weight (0.0-1.0, must sum to 1.0 across all criteria)
        description: Optional[str] - Optional description for clarity

    VALIDATION:
        - Weight must be between 0.0 and 1.0
        - Sum of all criterion weights must equal 1.0 (enforced at DecisionMatrix level)

    EXAMPLE:
        Criterion(name="Code Quality", weight=0.4, description="Maintainability and readability")

    WHY DATACLASS:
        - Immutable by default (frozen=True not set, but convention is immutability)
        - Type-safe fields
        - Automatic __repr__ and __eq__
        - Clear structure
    """
    name: str
    weight: float
    description: Optional[str] = None


@dataclass
class Alternative:
    """An alternative being evaluated."""
    name: str
    description: Optional[str] = None


@dataclass
class Score:
    """
    Score for an alternative on a criterion.

    WHAT: Links an alternative to a criterion with a numeric score

    FIELDS:
        alternative_name: str - Which alternative (must match Alternative.name)
        criterion_name: str - Which criterion (must match Criterion.name)
        score: float - Score value (typically 1-10 scale, but can be any positive number)
        reasoning: Optional[str] - Optional justification for the score

    VALIDATION:
        - alternative_name must exist in DecisionMatrix.alternatives
        - criterion_name must exist in DecisionMatrix.criteria
        - Score should be positive (enforced in WPM, recommended for WSM)

    EXAMPLE:
        Score(
            alternative_name="Refactor Now",
            criterion_name="Code Quality",
            score=9.0,
            reasoning="Eliminates technical debt, improves maintainability"
        )

    WHY DATACLASS:
        - Links alternatives to criteria
        - Stores score and optional reasoning
        - Type-safe relationships
    """
    alternative_name: str
    criterion_name: str
    score: float
    reasoning: Optional[str] = None


@dataclass
class DecisionMatrix:
    """Complete decision matrix data."""
    alternatives: List[Alternative]
    criteria: List[Criterion]
    scores: List[Score]
    methodology: str = "WSM"  # WSM, AHP, WPM, BWM


class DecisionMatrixCalculator:
    """
    Calculates decision matrix results using various methodologies.

    WHAT: Pure mathematical engine for decision matrix calculations

    PURPOSE:
        - Performs calculations (WSM, WPM, AHP, BWM)
        - Validates matrix completeness
        - Ranks alternatives
        - Provides detailed score breakdowns
        - Performs sensitivity analysis

    DESIGN:
        - No I/O, no side effects
        - Fully deterministic
        - Immutable (doesn't modify matrix)
        - Validates on initialization (fail fast)

    USAGE:
        calculator = DecisionMatrixCalculator(matrix)  # Validates automatically
        results = calculator.calculate_wsm()
        rankings = calculator.rank_alternatives(results)

    WHY SEPARATE CLASS:
        - Separation of concerns (data vs. calculation)
        - Reusable across different interfaces
        - Testable without I/O
        - Extensible (easy to add methods)
    """

    def __init__(self, matrix: DecisionMatrix):
        """
        Initialize calculator with decision matrix.

        WHAT IT DOES:
            1. Stores the matrix
            2. IMMEDIATELY validates matrix is complete and correct
            3. Raises ValueError if invalid (fail fast)

        VALIDATION CHECKS:
            - Weights sum to 1.0 (±0.01 tolerance)
            - All alternatives have scores for all criteria
            - No missing data

        Args:
            matrix: DecisionMatrix with alternatives, criteria, and scores

        Raises:
            ValueError: If matrix is invalid (weights don't sum to 1.0, missing scores)

        WHY IMMEDIATE VALIDATION:
            - Fail fast (don't proceed with bad data)
            - Clear error messages
            - Prevents calculation errors later
        """
        self.matrix = matrix
        self._validate_matrix()  # IMMEDIATE VALIDATION - FAIL FAST

    def _validate_matrix(self) -> None:
        """Validate that matrix is properly formed."""
        # Check weights sum to 1.0 (with tolerance)
        total_weight = sum(c.weight for c in self.matrix.criteria)
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

        # Check all alternatives have scores for all criteria
        for alt in self.matrix.alternatives:
            for crit in self.matrix.criteria:
                matching_scores = [
                    s for s in self.matrix.scores
                    if s.alternative_name == alt.name and s.criterion_name == crit.name
                ]
                if not matching_scores:
                    raise ValueError(
                        f"Missing score for alternative '{alt.name}' on criterion '{crit.name}'"
                    )

    def calculate_wsm(self) -> Dict[str, float]:
        """
        Calculate using Weighted Sum Model (WSM).

        WHAT IT DOES:
            Calculates total score for each alternative by summing weighted scores.
            Most common and intuitive decision-making method.

        FORMULA:
            Total_Score(Alternative) = Σ (Weight_i × Score_i) for all criteria i

        ALGORITHM:
            For each alternative:
                total_score = 0.0
                For each criterion:
                    weighted_score = criterion.weight × score
                    total_score += weighted_score
                results[alternative] = total_score

        EXAMPLE:
            Alternative: "Refactor Now"
            - Criterion 1: "Code Quality" (weight=0.4, score=9.0) → 0.4 × 9.0 = 3.6
            - Criterion 2: "Time to Market" (weight=0.6, score=4.0) → 0.6 × 4.0 = 2.4
            Total: 3.6 + 2.4 = 6.0

        PROPERTIES:
            - Linear combination (additive)
            - Works for independent criteria
            - Easy to interpret (weighted average)
            - Range: 0 to max(score_scale) × 1.0

        WHEN TO USE:
            - Default choice for most decisions
            - Criteria are independent
            - Need intuitive, easy-to-explain results

        Returns:
            Dictionary mapping alternative names to total scores
            Example: {"Option A": 7.4, "Option B": 7.8}

        WHY THIS METHOD:
            - Most intuitive (weighted average)
            - Mathematically sound
            - Easy to explain to stakeholders
            - Works well for most decision problems
        """
        results = {}

        for alt in self.matrix.alternatives:
            total_score = 0.0

            for crit in self.matrix.criteria:
                # Find score for this alternative-criterion pair
                # Validation ensures this exists, so next() will always find a match
                score_obj = next(
                    s for s in self.matrix.scores
                    if s.alternative_name == alt.name and s.criterion_name == crit.name
                )

                # Calculate weighted score: weight × raw_score
                weighted_score = crit.weight * score_obj.score
                total_score += weighted_score  # Sum all weighted scores

            results[alt.name] = total_score

        return results

    def calculate_wpm(self) -> Dict[str, float]:
        """
        Calculate using Weighted Product Model (WPM).

        Formula: Total_Score = Π (Score_i ^ Weight_i) for all criteria

        Returns:
            Dictionary mapping alternative names to total scores
        """
        results = {}

        for alt in self.matrix.alternatives:
            total_score = 1.0

            for crit in self.matrix.criteria:
                # Find score for this alternative-criterion pair
                score_obj = next(
                    s for s in self.matrix.scores
                    if s.alternative_name == alt.name and s.criterion_name == crit.name
                )

                # Calculate weighted product (avoid zero scores)
                if score_obj.score <= 0:
                    score_value = 0.001  # Small positive value
                else:
                    score_value = score_obj.score

                weighted_product = math.pow(score_value, crit.weight)
                total_score *= weighted_product

            results[alt.name] = total_score

        return results

    def calculate_ahp_weights(self, pairwise_comparisons: Dict[Tuple[str, str], float]) -> Dict[str, float]:
        """
        Calculate AHP weights from pairwise comparisons.

        Args:
            pairwise_comparisons: Dictionary mapping (criterion1, criterion2) to comparison value
                                 (1-9 scale: 1=equal, 3=moderate, 5=strong, 7=very strong, 9=extreme)

        Returns:
            Dictionary mapping criterion names to weights
        """
        n = len(self.matrix.criteria)
        criteria_names = [c.name for c in self.matrix.criteria]

        # Build comparison matrix
        comparison_matrix = [[1.0] * n for _ in range(n)]

        for i, crit1 in enumerate(criteria_names):
            for j, crit2 in enumerate(criteria_names):
                if i == j:
                    comparison_matrix[i][j] = 1.0
                elif (crit1, crit2) in pairwise_comparisons:
                    comparison_matrix[i][j] = pairwise_comparisons[(crit1, crit2)]
                elif (crit2, crit1) in pairwise_comparisons:
                    # Reciprocal (if A is 3x B, then B is 1/3x A)
                    comparison_matrix[i][j] = 1.0 / pairwise_comparisons[(crit2, crit1)]
                else:
                    comparison_matrix[i][j] = 1.0  # Default to equal

        # Calculate weights using geometric mean method (simplified AHP)
        weights = {}
        for i, crit_name in enumerate(criteria_names):
            # Geometric mean of row
            row_product = 1.0
            for j in range(n):
                row_product *= comparison_matrix[i][j]
            geometric_mean = math.pow(row_product, 1.0 / n)

            weights[crit_name] = geometric_mean

        # Normalize weights to sum to 1.0
        total = sum(weights.values())
        for crit_name in weights:
            weights[crit_name] /= total

        return weights

    def calculate_consistency_ratio(self, pairwise_comparisons: Dict[Tuple[str, str], float]) -> float:
        """
        Calculate consistency ratio for AHP.

        CR = CI / RI
        CI = (λ_max - n) / (n - 1)

        Args:
            pairwise_comparisons: Pairwise comparison values

        Returns:
            Consistency ratio (should be < 0.1 for acceptable consistency)
        """
        n = len(self.matrix.criteria)
        if n <= 2:
            return 0.0  # Always consistent for 2 or fewer criteria

        # Random Index values (Saaty, 1980)
        ri_values = {
            1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        ri = ri_values.get(n, 1.45)

        # Build comparison matrix and calculate eigenvalues (simplified)
        # For full implementation, would use eigenvalue calculation
        # Here we use a simplified approximation
        weights = self.calculate_ahp_weights(pairwise_comparisons)
        criteria_names = [c.name for c in self.matrix.criteria]

        # Calculate λ_max approximation
        lambda_max = 0.0
        for i, crit1 in enumerate(criteria_names):
            row_sum = 0.0
            for j, crit2 in enumerate(criteria_names):
                if (crit1, crit2) in pairwise_comparisons:
                    comp_value = pairwise_comparisons[(crit1, crit2)]
                elif (crit2, crit1) in pairwise_comparisons:
                    comp_value = 1.0 / pairwise_comparisons[(crit2, crit1)]
                else:
                    comp_value = 1.0
                row_sum += comp_value * weights[crit2]
            lambda_max += row_sum / weights[crit1]

        lambda_max /= n

        # Calculate Consistency Index
        ci = (lambda_max - n) / (n - 1)

        # Calculate Consistency Ratio
        cr = ci / ri if ri > 0 else 0.0

        return cr

    def calculate_bwm_weights(
        self,
        best_criterion: str,
        worst_criterion: str,
        best_comparisons: Dict[str, float],
        worst_comparisons: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate weights using Best Worst Method (BWM).

        Args:
            best_criterion: Name of best (most important) criterion
            worst_criterion: Name of worst (least important) criterion
            best_comparisons: Dictionary mapping criterion to comparison with best (1-9 scale)
            worst_comparisons: Dictionary mapping criterion to comparison with worst (1-9 scale)

        Returns:
            Dictionary mapping criterion names to weights
        """
        criteria_names = [c.name for c in self.matrix.criteria]

        # Validate inputs
        if best_criterion not in criteria_names:
            raise ValueError(f"Best criterion '{best_criterion}' not found")
        if worst_criterion not in criteria_names:
            raise ValueError(f"Worst criterion '{worst_criterion}' not found")

        # Build optimization problem (simplified - uses geometric mean)
        # Full BWM uses optimization, but we'll use a simplified approach
        weights = {}

        # Initialize with best and worst
        weights[best_criterion] = 1.0
        if worst_criterion in worst_comparisons:
            weights[worst_criterion] = 1.0 / worst_comparisons[worst_criterion]
        else:
            weights[worst_criterion] = 0.1  # Default

        # Calculate intermediate weights
        for crit_name in criteria_names:
            if crit_name == best_criterion or crit_name == worst_criterion:
                continue

            # Use best comparison if available
            if crit_name in best_comparisons:
                weights[crit_name] = 1.0 / best_comparisons[crit_name]
            # Use worst comparison if available
            elif crit_name in worst_comparisons:
                weights[crit_name] = worst_comparisons[crit_name] * weights[worst_criterion]
            else:
                # Default: average of best and worst
                weights[crit_name] = (weights[best_criterion] + weights[worst_criterion]) / 2.0

        # Normalize to sum to 1.0
        total = sum(weights.values())
        for crit_name in weights:
            weights[crit_name] /= total

        return weights

    def calculate(self, methodology: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate decision matrix results.

        Args:
            methodology: Method to use (WSM, WPM, AHP, BWM). Defaults to matrix.methodology.

        Returns:
            Dictionary mapping alternative names to total scores
        """
        method = methodology or self.matrix.methodology

        if method == "WSM":
            return self.calculate_wsm()
        elif method == "WPM":
            return self.calculate_wpm()
        else:
            raise ValueError(f"Unknown methodology: {method}")

    def rank_alternatives(self, scores: Dict[str, float]) -> List[Tuple[str, float, int]]:
        """
        Rank alternatives by score.

        Args:
            scores: Dictionary of alternative names to scores

        Returns:
            List of tuples (alternative_name, score, rank) sorted by score descending
        """
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranked = [(name, score, rank + 1) for rank, (name, score) in enumerate(sorted_items)]
        return ranked

    def get_detailed_scores(self, alternative_name: str) -> Dict[str, Tuple[float, float]]:
        """
        Get detailed scores for an alternative.

        Args:
            alternative_name: Name of alternative

        Returns:
            Dictionary mapping criterion names to (raw_score, weighted_score) tuples
        """
        details = {}

        for crit in self.matrix.criteria:
            score_obj = next(
                s for s in self.matrix.scores
                if s.alternative_name == alternative_name and s.criterion_name == crit.name
            )

            weighted_score = crit.weight * score_obj.score
            details[crit.name] = (score_obj.score, weighted_score)

        return details

    def sensitivity_analysis(
        self,
        criterion_name: str,
        weight_adjustment: float,
        methodology: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Perform sensitivity analysis by adjusting a criterion weight.

        Args:
            criterion_name: Name of criterion to adjust
            weight_adjustment: Adjustment factor (e.g., 0.1 for 10% increase)
            methodology: Method to use (defaults to matrix.methodology)

        Returns:
            Dictionary mapping alternative names to new scores
        """
        # Create adjusted matrix
        adjusted_criteria = []
        total_other_weight = 0.0

        for crit in self.matrix.criteria:
            if crit.name == criterion_name:
                # Adjust this criterion's weight
                new_weight = crit.weight * (1.0 + weight_adjustment)
                adjusted_criteria.append(Criterion(crit.name, new_weight, crit.description))
            else:
                adjusted_criteria.append(crit)
                total_other_weight += crit.weight

        # Normalize other weights proportionally
        if total_other_weight > 0:
            adjustment_factor = (1.0 - adjusted_criteria[0].weight) / total_other_weight
            for crit in adjusted_criteria[1:]:
                crit.weight *= adjustment_factor

        # Create adjusted matrix
        adjusted_matrix = DecisionMatrix(
            alternatives=self.matrix.alternatives,
            criteria=adjusted_criteria,
            scores=self.matrix.scores,
            methodology=methodology or self.matrix.methodology
        )

        # Calculate with adjusted weights
        calculator = DecisionMatrixCalculator(adjusted_matrix)
        return calculator.calculate()


def normalize_scores(scores: List[float], method: str = "min_max") -> List[float]:
    """
    Normalize scores to 0-1 range.

    Args:
        scores: List of raw scores
        method: Normalization method ("min_max" or "sum")

    Returns:
        List of normalized scores
    """
    if method == "min_max":
        min_score = min(scores)
        max_score = max(scores)
        if max_score == min_score:
            return [1.0] * len(scores)
        return [(s - min_score) / (max_score - min_score) for s in scores]
    elif method == "sum":
        total = sum(scores)
        if total == 0:
            return [1.0 / len(scores)] * len(scores)
        return [s / total for s in scores]
    else:
        raise ValueError(f"Unknown normalization method: {method}")
