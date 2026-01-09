"""
Decision Engine API endpoints.

Exposes the hardened Decision Engine to web clients via FastAPI.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ...core.decision_matrix import DecisionMatrixCalculator
from ...core.input_transformer import InputTransformer
from ..models import (
    DecisionRequest, DecisionResponse, RankingItem, AlternativeAnalysis,
    DetailedScore, SensitivityWarning
)

router = APIRouter()


@router.get("/health")
async def get_health():
    """
    Health check endpoint for Decision Engine.
    
    Returns:
        Health status with version and core information
    """
    return {
        "status": "ok",
        "version": "1.0",
        "core": "diamond_plated",
        "engine": "iron_core"
    }


@router.post("/analyze", response_model=DecisionResponse)
async def analyze_decision(request: DecisionRequest):
    """
    Analyze a decision using the Decision Engine.
    
    Accepts a DecisionRequest, processes it through InputTransformer
    (the Gateway/Airlock), runs calculations, and returns structured results.
    
    Args:
        request: DecisionRequest with problem, alternatives, criteria, scores
    
    Returns:
        DecisionResponse with rankings, analysis, and sensitivity warnings
    
    Raises:
        HTTPException: If input data is invalid or calculation fails
    """
    try:
        # Convert Pydantic model to dict for InputTransformer
        # InputTransformer expects a specific format
        raw_data = {
            'alternatives': request.alternatives,
            'criteria': request.criteria,
            'scores': request.scores,
            'methodology': request.methodology
        }
        
        # Pass through InputTransformer (Gateway/Airlock)
        matrix = InputTransformer.transform_input(raw_data)
        
        # Create calculator and run analysis
        calculator = DecisionMatrixCalculator(matrix)
        
        # Calculate WSM results
        results = calculator.calculate_wsm()
        
        # Get rankings
        rankings_raw = calculator.rank_alternatives(results)
        
        # Get detailed scores
        detailed_scores = calculator.get_detailed_scores()
        
        # Build response
        rankings = [
            RankingItem(rank=rank, name=name, score=score)
            for name, score, rank in rankings_raw
        ]
        
        # Build detailed analysis
        detailed_analysis = []
        for alt_name, score, rank in rankings_raw:
            alt_scores = detailed_scores.get(alt_name, {})
            detailed_items = []
            
            for crit_name, raw_score in alt_scores.items():
                # Find criterion weight
                crit = next(c for c in matrix.criteria if c.name == crit_name)
                weighted_score = crit.weight * raw_score
                
                detailed_items.append(DetailedScore(
                    criterion_name=crit_name,
                    raw_score=raw_score,
                    weighted_score=weighted_score,
                    weight=crit.weight
                ))
            
            detailed_analysis.append(AlternativeAnalysis(
                name=alt_name,
                total_score=score,
                rank=rank,
                detailed_scores=detailed_items
            ))
        
        # Run sensitivity analysis if requested
        sensitivity_warnings = []
        is_robust = True
        
        if request.show_sensitivity and len(matrix.criteria) > 1:
            sensitivity_result = _run_sensitivity_analysis(matrix, calculator, rankings_raw)
            sensitivity_warnings = sensitivity_result['warnings']
            is_robust = sensitivity_result['is_robust']
        
        return DecisionResponse(
            problem=request.problem,
            methodology=request.methodology,
            rankings=rankings,
            recommendation=rankings[0].name if rankings else None,
            detailed_analysis=detailed_analysis,
            sensitivity_warnings=sensitivity_warnings,
            is_robust=is_robust
        )
        
    except ValueError as e:
        # Input validation errors from InputTransformer or Calculator
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def _run_sensitivity_analysis(
    matrix: Any,
    calculator: DecisionMatrixCalculator,
    original_rankings: list
) -> Dict[str, Any]:
    """
    Run sensitivity analysis - check if winner changes when highest weight criterion is reduced.
    
    Returns:
        Dict with 'warnings' list and 'is_robust' boolean
    """
    from ...core.decision_matrix import DecisionMatrix, Criterion
    
    if len(matrix.criteria) < 2:
        return {'warnings': [], 'is_robust': True}
    
    # Find criterion with highest weight
    highest_crit = max(matrix.criteria, key=lambda c: c.weight)
    crit_name = highest_crit.name
    crit_weight = highest_crit.weight
    
    # Original winner
    original_winner = original_rankings[0][0] if original_rankings else None
    
    # Calculate what happens if highest weight is reduced by 20%
    reduced_weight = crit_weight * 0.8
    remaining_weight = 1.0 - reduced_weight
    
    # Distribute remaining weight proportionally to other criteria
    other_criteria = [c for c in matrix.criteria if c.name != crit_name]
    other_total = sum(c.weight for c in other_criteria)
    
    if other_total > 0:
        # Rebuild criteria with adjusted weights
        crit_objects = []
        for crit in matrix.criteria:
            if crit.name == crit_name:
                crit_objects.append(
                    Criterion(crit.name, reduced_weight, crit.description)
                )
            else:
                # Proportional distribution
                adjusted_weight = crit.weight * (remaining_weight / other_total)
                crit_objects.append(
                    Criterion(crit.name, adjusted_weight, crit.description)
                )
        
        # Create adjusted matrix and calculate
        adjusted_matrix = DecisionMatrix(
            matrix.alternatives,
            crit_objects,
            matrix.scores,
            methodology="WSM"
        )
        adjusted_calc = DecisionMatrixCalculator(adjusted_matrix)
        adjusted_results = adjusted_calc.calculate_wsm()
        adjusted_rankings = adjusted_calc.rank_alternatives(adjusted_results)
        new_winner = adjusted_rankings[0][0] if adjusted_rankings else None
        
        warnings = []
        is_robust = True
        
        if new_winner != original_winner:
            is_robust = False
            warnings.append(SensitivityWarning(
                criterion_name=crit_name,
                original_weight=crit_weight,
                reduced_weight=reduced_weight,
                original_winner=original_winner,
                new_winner=new_winner,
                warning=f"If '{crit_name}' becomes less important, '{new_winner}' would win instead of '{original_winner}'."
            ))
        
        return {'warnings': warnings, 'is_robust': is_robust}
    
    return {'warnings': [], 'is_robust': True}
