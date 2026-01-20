"""
Pydantic models for Decision Engine API.

These models define the contract for HTTP requests/responses.
Data still passes through InputTransformer for final validation.
"""


from pydantic import BaseModel, Field


class AlternativeInput(BaseModel):
    """Alternative input - can be string or object with description."""

    name: str
    description: str | None = None


class CriterionInput(BaseModel):
    """Criterion input - can be weight or object with weight and description."""

    weight: float = Field(..., ge=0.0, le=1.0, description="Criterion weight (0.0-1.0)")
    description: str | None = None


class DecisionRequest(BaseModel):
    """
    Request model for decision analysis.

    Mirrors the structure required by InputTransformer.
    Pydantic handles HTTP JSON validation, InputTransformer handles final security checks.
    """

    problem: str = Field(..., description="Description of the decision problem")
    alternatives: list[str | dict[str, str]] = Field(
        ..., description="List of alternatives (strings or objects with name/description)"
    )
    criteria: dict[str, float | dict[str, float | str]] = Field(
        ..., description="Dictionary mapping criterion names to weights or weight objects"
    )
    scores: dict[str, dict[str, float | int | str]] = Field(
        ..., description="Nested dict: {alternative_name: {criterion_name: score}}"
    )
    methodology: str = Field(default="WSM", description="Calculation method (WSM only)")
    show_details: bool = Field(default=True, description="Include detailed breakdown")
    show_sensitivity: bool = Field(default=True, description="Include sensitivity analysis")


class RankingItem(BaseModel):
    """Single ranking result."""

    rank: int
    name: str
    score: float


class DetailedScore(BaseModel):
    """Detailed score for a single alternative-criterion pair."""

    criterion_name: str
    raw_score: float
    weighted_score: float
    weight: float


class AlternativeAnalysis(BaseModel):
    """Detailed analysis for a single alternative."""

    name: str
    total_score: float
    rank: int
    detailed_scores: list[DetailedScore]


class SensitivityWarning(BaseModel):
    """Sensitivity analysis warning."""

    criterion_name: str
    original_weight: float
    reduced_weight: float
    original_winner: str
    new_winner: str
    warning: str


class DecisionResponse(BaseModel):
    """
    Response model for decision analysis.

    Contains rankings, detailed analysis, and sensitivity warnings.
    """

    problem: str
    methodology: str
    rankings: list[RankingItem]
    recommendation: str
    detailed_analysis: list[AlternativeAnalysis]
    sensitivity_warnings: list[SensitivityWarning] = Field(default_factory=list)
    is_robust: bool = Field(
        default=True, description="Whether recommendation is robust to weight changes"
    )
