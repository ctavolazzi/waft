"""
Evolution API Routes: Genetic Crossover, Genome Management, and Population Control.

Provides REST endpoints for:
- Genome creation and management
- Genetic crossover operations
- Population statistics
- Lineage tracking
"""

import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from ...evolution import (
    ColorGene,
    CrossoverResult,
    CrossoverStrategy,
    FontGene,
    GeneticCrossover,
    LayoutGene,
    MarginGene,
    Scint,
    ScintDetector,
    ScintType,
    StylingGene,
    StylingGenome,
    StylingGenomeRegistry,
    breed,
)
from ..websocket import (
    emit_agent_crossover,
    emit_agent_spawn,
    emit_fitness_update,
    emit_generation_complete,
    emit_population_update,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================


class FontGeneModel(BaseModel):
    """Font gene configuration."""

    family: str = "sans-serif"
    size_body: int = Field(default=11, ge=6, le=72)
    size_h1: int = Field(default=24, ge=8, le=96)
    size_h2: int = Field(default=18, ge=8, le=72)
    size_h3: int = Field(default=14, ge=8, le=48)
    size_code: int = Field(default=10, ge=6, le=24)
    line_height: float = Field(default=1.5, ge=1.0, le=3.0)


class MarginGeneModel(BaseModel):
    """Margin gene configuration."""

    top: int = Field(default=20, ge=0, le=100)
    bottom: int = Field(default=20, ge=0, le=100)
    left: int = Field(default=20, ge=0, le=100)
    right: int = Field(default=20, ge=0, le=100)
    paragraph_spacing: int = Field(default=10, ge=0, le=50)
    section_spacing: int = Field(default=15, ge=0, le=100)


class ColorGeneModel(BaseModel):
    """Color gene configuration."""

    text: str = Field(default="#000000", pattern=r"^#[0-9a-fA-F]{6}$")
    background: str = Field(default="#FFFFFF", pattern=r"^#[0-9a-fA-F]{6}$")
    heading: str = Field(default="#1a1a1a", pattern=r"^#[0-9a-fA-F]{6}$")
    accent: str = Field(default="#0066cc", pattern=r"^#[0-9a-fA-F]{6}$")
    code_bg: str = Field(default="#f5f5f5", pattern=r"^#[0-9a-fA-F]{6}$")
    code_text: str = Field(default="#333333", pattern=r"^#[0-9a-fA-F]{6}$")
    border: str = Field(default="#cccccc", pattern=r"^#[0-9a-fA-F]{6}$")


class LayoutGeneModel(BaseModel):
    """Layout gene configuration."""

    columns: int = Field(default=1, ge=1, le=3)
    density: str = Field(default="normal", pattern=r"^(compact|normal|spacious)$")
    toc_enabled: bool = False
    page_numbers: bool = True
    header_enabled: bool = True
    footer_enabled: bool = True


class StylingGeneModel(BaseModel):
    """Complete styling gene configuration."""

    font: FontGeneModel = Field(default_factory=FontGeneModel)
    margin: MarginGeneModel = Field(default_factory=MarginGeneModel)
    color: ColorGeneModel = Field(default_factory=ColorGeneModel)
    layout: LayoutGeneModel = Field(default_factory=LayoutGeneModel)
    name: str = "default"
    description: str = ""


class GenomeCreateRequest(BaseModel):
    """Request to create a new genome."""

    genes: StylingGeneModel = Field(default_factory=StylingGeneModel)
    parent_id: str | None = None


class GenomeResponse(BaseModel):
    """Response containing genome data."""

    genome_id: str
    scientific_name: str
    generation: int
    parent_id: str | None
    lineage_path: list[str]
    fitness_score: float | None
    genes: dict[str, Any]
    created_at: str


class CrossoverRequest(BaseModel):
    """Request for genetic crossover."""

    parent_a_id: str
    parent_b_id: str
    strategy: str = Field(
        default="uniform",
        description="Crossover strategy: uniform, single_point, two_point, category_swap, fitness_weighted, blended, dominant_recessive",
    )


class CrossoverResponse(BaseModel):
    """Response from crossover operation."""

    offspring: GenomeResponse
    parent_a: GenomeResponse
    parent_b: GenomeResponse
    strategy: str
    crossover_points: list[str]
    inheritance_map: dict[str, str]
    notes: str


class FitnessUpdateRequest(BaseModel):
    """Request to update genome fitness."""

    metrics: dict[str, float] = Field(
        ...,
        description="Fitness metrics (e.g., {'readability': 0.8, 'density': 0.7})",
    )


class PopulationStatsResponse(BaseModel):
    """Population statistics response."""

    total_genomes: int
    max_generation: int
    best_fitness: float
    avg_fitness: float
    genomes_by_generation: dict[int, int]


class ScintResponse(BaseModel):
    """Scint (divergence) detection response."""

    scint_type: str
    divergence_score: float
    differences: dict[str, Any]
    genome_a_name: str
    genome_b_name: str
    resolved: bool


# ============================================================================
# In-Memory Storage (for demo/testing - replace with database in production)
# ============================================================================

_genomes: dict[str, StylingGenome] = {}
_crossover_engine = GeneticCrossover()
_scint_detector = ScintDetector()


def _genome_to_response(genome: StylingGenome) -> GenomeResponse:
    """Convert StylingGenome to response model."""
    return GenomeResponse(
        genome_id=genome.genome_id,
        scientific_name=genome.scientific_name,
        generation=genome.generation,
        parent_id=genome.parent_id,
        lineage_path=genome.lineage_path,
        fitness_score=genome.fitness_score,
        genes=genome.genes.to_dict(),
        created_at=genome.created_at.isoformat(),
    )


def _model_to_genes(model: StylingGeneModel) -> StylingGene:
    """Convert Pydantic model to StylingGene."""
    return StylingGene(
        font=FontGene(**model.font.model_dump()),
        margin=MarginGene(**model.margin.model_dump()),
        color=ColorGene(**model.color.model_dump()),
        layout=LayoutGene(**model.layout.model_dump()),
        name=model.name,
        description=model.description,
    )


# ============================================================================
# Genome Endpoints
# ============================================================================


@router.get("/evolution/genomes", response_model=list[GenomeResponse])
async def list_genomes(
    generation: int | None = None,
    min_fitness: float | None = None,
    limit: int = 100,
):
    """
    List all genomes with optional filtering.

    Args:
        generation: Filter by generation number
        min_fitness: Minimum fitness score filter
        limit: Maximum number of results
    """
    genomes = list(_genomes.values())

    if generation is not None:
        genomes = [g for g in genomes if g.generation == generation]

    if min_fitness is not None:
        genomes = [g for g in genomes if (g.fitness_score or 0) >= min_fitness]

    # Sort by fitness (descending) then generation
    genomes.sort(key=lambda g: (-(g.fitness_score or 0), g.generation))

    return [_genome_to_response(g) for g in genomes[:limit]]


@router.get("/evolution/genomes/{genome_id}", response_model=GenomeResponse)
async def get_genome(genome_id: str):
    """Get a specific genome by ID."""
    if genome_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome {genome_id} not found",
        )
    return _genome_to_response(_genomes[genome_id])


@router.post("/evolution/genomes", response_model=GenomeResponse, status_code=201)
async def create_genome(request: GenomeCreateRequest):
    """
    Create a new genome.

    If parent_id is provided, creates as child of that genome.
    """
    genes = _model_to_genes(request.genes)

    parent = None
    if request.parent_id:
        if request.parent_id not in _genomes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent genome {request.parent_id} not found",
            )
        parent = _genomes[request.parent_id]

    genome = StylingGenome.from_genes(genes, parent=parent)
    _genomes[genome.genome_id] = genome

    # Emit WebSocket event
    try:
        import asyncio

        asyncio.create_task(
            emit_agent_spawn(
                {
                    "genome_id": genome.genome_id,
                    "scientific_name": genome.scientific_name,
                    "generation": genome.generation,
                    "parent_id": genome.parent_id,
                }
            )
        )
    except Exception as e:
        logger.warning(f"Failed to emit spawn event: {e}")

    logger.info(f"Created genome: {genome.scientific_name} (Gen {genome.generation})")
    return _genome_to_response(genome)


@router.delete("/evolution/genomes/{genome_id}", status_code=204)
async def delete_genome(genome_id: str):
    """Delete a genome."""
    if genome_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome {genome_id} not found",
        )
    del _genomes[genome_id]
    logger.info(f"Deleted genome: {genome_id}")


# ============================================================================
# Crossover Endpoints
# ============================================================================


@router.post("/evolution/crossover", response_model=CrossoverResponse)
async def perform_crossover(request: CrossoverRequest):
    """
    Perform genetic crossover between two parent genomes.

    Strategies:
    - uniform: Random selection of each gene
    - single_point: Single crossover point
    - two_point: Two crossover points
    - category_swap: Swap entire categories (font, margin, etc.)
    - fitness_weighted: Bias toward fitter parent
    - blended: Interpolate numeric values
    - dominant_recessive: Mendelian inheritance simulation
    """
    if request.parent_a_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent A genome {request.parent_a_id} not found",
        )
    if request.parent_b_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent B genome {request.parent_b_id} not found",
        )

    parent_a = _genomes[request.parent_a_id]
    parent_b = _genomes[request.parent_b_id]

    # Parse strategy
    try:
        strategy = CrossoverStrategy(request.strategy)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid strategy: {request.strategy}. Valid options: {[s.value for s in CrossoverStrategy]}",
        )

    # Perform crossover
    result = _crossover_engine.crossover(parent_a, parent_b, strategy)

    # Store offspring
    _genomes[result.offspring.genome_id] = result.offspring

    # Emit WebSocket event
    try:
        import asyncio

        asyncio.create_task(
            emit_agent_crossover(
                parent_a.genome_id,
                parent_b.genome_id,
                result.offspring.genome_id,
            )
        )
    except Exception as e:
        logger.warning(f"Failed to emit crossover event: {e}")

    logger.info(
        f"Crossover: {parent_a.scientific_name} x {parent_b.scientific_name} -> {result.offspring.scientific_name}"
    )

    return CrossoverResponse(
        offspring=_genome_to_response(result.offspring),
        parent_a=_genome_to_response(result.parent_a),
        parent_b=_genome_to_response(result.parent_b),
        strategy=result.strategy.value,
        crossover_points=result.crossover_points,
        inheritance_map=result.inheritance_map,
        notes=result.notes,
    )


@router.get("/evolution/crossover/strategies")
async def list_crossover_strategies():
    """List all available crossover strategies with descriptions."""
    return {
        "strategies": [
            {
                "name": "uniform",
                "description": "Random selection of each gene from either parent",
            },
            {
                "name": "single_point",
                "description": "All genes before crossover point from parent A, after from parent B",
            },
            {
                "name": "two_point",
                "description": "Genes between two points from parent B, rest from parent A",
            },
            {
                "name": "category_swap",
                "description": "Randomly select entire categories (font, margin, color, layout) from each parent",
            },
            {
                "name": "fitness_weighted",
                "description": "Bias gene selection toward the fitter parent",
            },
            {
                "name": "blended",
                "description": "Interpolate numeric values between parents",
            },
            {
                "name": "dominant_recessive",
                "description": "Simulate Mendelian inheritance with dominant/recessive traits",
            },
        ]
    }


# ============================================================================
# Fitness Endpoints
# ============================================================================


@router.post("/evolution/genomes/{genome_id}/fitness", response_model=GenomeResponse)
async def update_fitness(genome_id: str, request: FitnessUpdateRequest):
    """
    Update a genome's fitness score based on evaluation metrics.

    Metrics should be values between 0.0 and 1.0.
    """
    if genome_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome {genome_id} not found",
        )

    genome = _genomes[genome_id]

    # Validate metrics
    for key, value in request.metrics.items():
        if not 0.0 <= value <= 1.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Metric '{key}' must be between 0.0 and 1.0, got {value}",
            )

    # Evaluate fitness
    fitness = genome.evaluate_fitness(request.metrics)

    # Emit WebSocket event
    try:
        import asyncio

        asyncio.create_task(
            emit_fitness_update(genome_id, fitness, request.metrics)
        )
    except Exception as e:
        logger.warning(f"Failed to emit fitness event: {e}")

    logger.info(f"Updated fitness for {genome.scientific_name}: {fitness:.3f}")
    return _genome_to_response(genome)


# ============================================================================
# Population Endpoints
# ============================================================================


@router.get("/evolution/population/stats", response_model=PopulationStatsResponse)
async def get_population_stats():
    """Get population statistics."""
    if not _genomes:
        return PopulationStatsResponse(
            total_genomes=0,
            max_generation=0,
            best_fitness=0.0,
            avg_fitness=0.0,
            genomes_by_generation={},
        )

    genomes = list(_genomes.values())
    fitness_scores = [g.fitness_score for g in genomes if g.fitness_score is not None]

    # Count by generation
    gen_counts: dict[int, int] = {}
    for g in genomes:
        gen_counts[g.generation] = gen_counts.get(g.generation, 0) + 1

    return PopulationStatsResponse(
        total_genomes=len(genomes),
        max_generation=max(g.generation for g in genomes),
        best_fitness=max(fitness_scores) if fitness_scores else 0.0,
        avg_fitness=sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0.0,
        genomes_by_generation=gen_counts,
    )


@router.get("/evolution/population/lineage/{genome_id}")
async def get_lineage(genome_id: str):
    """Get the full lineage (ancestry) of a genome."""
    if genome_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome {genome_id} not found",
        )

    genome = _genomes[genome_id]
    lineage = []

    for ancestor_id in genome.lineage_path:
        if ancestor_id in _genomes:
            lineage.append(_genome_to_response(_genomes[ancestor_id]))

    return {"genome_id": genome_id, "lineage": lineage}


# ============================================================================
# Scint Detection Endpoints
# ============================================================================


@router.post("/evolution/scint/detect", response_model=ScintResponse | None)
async def detect_scint(genome_a_id: str, genome_b_id: str):
    """
    Detect styling divergence (scint) between two genomes.

    Returns None if no significant divergence detected.
    """
    if genome_a_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome A {genome_a_id} not found",
        )
    if genome_b_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome B {genome_b_id} not found",
        )

    genome_a = _genomes[genome_a_id]
    genome_b = _genomes[genome_b_id]

    scint = _scint_detector.detect(genome_a, genome_b)

    if scint is None:
        return None

    return ScintResponse(
        scint_type=scint.scint_type.value,
        divergence_score=scint.divergence_score,
        differences={k: str(v) for k, v in scint.differences.items()},
        genome_a_name=genome_a.scientific_name,
        genome_b_name=genome_b.scientific_name,
        resolved=scint.resolved,
    )


@router.post("/evolution/scint/reconcile")
async def reconcile_scint(
    genome_a_id: str,
    genome_b_id: str,
    strategy: str = "select_fittest",
):
    """
    Reconcile a scint between two genomes.

    Strategies:
    - select_fittest: Choose genome with higher fitness
    - select_a: Choose genome A
    - select_b: Choose genome B
    - merge: Merge best genes from both (uses genetic crossover)
    """
    if genome_a_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome A {genome_a_id} not found",
        )
    if genome_b_id not in _genomes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genome B {genome_b_id} not found",
        )

    genome_a = _genomes[genome_a_id]
    genome_b = _genomes[genome_b_id]

    # Detect scint
    scint = _scint_detector.detect(genome_a, genome_b)
    if scint is None:
        return {"message": "No scint detected between these genomes"}

    # Reconcile
    winner = _scint_detector.reconcile_scint(scint, strategy)

    return {
        "strategy": strategy,
        "winner": _genome_to_response(winner),
        "scint_resolved": scint.resolved,
    }


# ============================================================================
# Admin Endpoints
# ============================================================================


@router.post("/evolution/reset")
async def reset_population():
    """Reset the entire population (clear all genomes)."""
    count = len(_genomes)
    _genomes.clear()
    _crossover_engine.crossover_history.clear()
    _scint_detector.detected_scints.clear()

    logger.info(f"Reset population: cleared {count} genomes")
    return {"message": f"Cleared {count} genomes", "status": "reset"}


@router.get("/evolution/report")
async def get_evolution_report():
    """Generate comprehensive evolution report."""
    breeding_report = _crossover_engine.generate_breeding_report()
    scint_report = _scint_detector.generate_scint_report()

    return {
        "population_size": len(_genomes),
        "breeding_report": breeding_report,
        "scint_report": scint_report,
        "timestamp": datetime.now().isoformat(),
    }
