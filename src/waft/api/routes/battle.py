"""
Battle Royale API Routes: Agent Combat and Tournament System.

Provides REST endpoints for:
- Starting battles between agents
- Running tournaments
- Battle history and statistics
- Real-time battle status via WebSocket
"""

import asyncio
import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field

from ...evolution import (
    BattleAction,
    BattleResult,
    BattleRoyale,
    BattleStats,
    BattleStatus,
    Combatant,
    StylingGene,
    StylingGenome,
    quick_battle,
)
from ..websocket import (
    emit_battle_damage,
    emit_battle_end,
    emit_battle_round,
    emit_battle_start,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Request/Response Models
# ============================================================================


class AgentConfig(BaseModel):
    """Configuration for creating a battle agent."""

    name: str = Field(..., min_length=1, max_length=50)
    # Gene modifiers that affect combat stats
    attack_modifier: float = Field(default=1.0, ge=0.5, le=2.0)
    defense_modifier: float = Field(default=1.0, ge=0.5, le=2.0)
    speed_modifier: float = Field(default=1.0, ge=0.5, le=2.0)
    # Optional custom genes
    font_size_h1: int = Field(default=24, ge=8, le=96)
    margin_top: int = Field(default=20, ge=0, le=100)
    color_contrast: float = Field(default=0.8, ge=0.0, le=1.0)


class BattleStartRequest(BaseModel):
    """Request to start a battle."""

    agents: list[AgentConfig] = Field(
        ...,
        min_length=2,
        max_length=10,
        description="List of agents to battle (2-10)",
    )
    max_rounds: int = Field(default=100, ge=10, le=1000)


class TournamentStartRequest(BaseModel):
    """Request to start a tournament."""

    agents: list[AgentConfig] = Field(
        ...,
        min_length=4,
        max_length=32,
        description="List of agents for tournament (4-32)",
    )
    rounds: int = Field(default=3, ge=1, le=10)


class CombatantResponse(BaseModel):
    """Response model for a combatant."""

    name: str
    health: float
    max_health: float
    health_percent: float
    is_alive: bool
    kills: int
    damage_dealt: float
    damage_taken: float
    rounds_survived: int
    status: str


class BattleResultResponse(BaseModel):
    """Response model for battle results."""

    battle_id: str
    winner: CombatantResponse | None
    participants: list[CombatantResponse]
    duration_rounds: int
    total_damage: float
    start_time: str
    end_time: str


class BattleStatusResponse(BaseModel):
    """Response model for in-progress battle status."""

    battle_id: str
    status: str
    current_round: int
    alive_count: int
    participants: list[CombatantResponse]


class TournamentResultResponse(BaseModel):
    """Response model for tournament results."""

    tournament_id: str
    total_rounds: int
    participants: int
    rankings: list[dict[str, Any]]
    champion: dict[str, Any] | None


class BattleHistoryResponse(BaseModel):
    """Response model for battle history."""

    total_battles: int
    total_rounds: int
    total_damage: float
    recent_battles: list[BattleResultResponse]


# ============================================================================
# In-Memory Storage
# ============================================================================

_battles: dict[str, BattleResult] = {}
_active_battles: dict[str, dict[str, Any]] = {}
_tournaments: dict[str, dict[str, Any]] = {}
_arena = BattleRoyale()


def _create_genome_from_config(config: AgentConfig) -> StylingGenome:
    """Create a StylingGenome from agent config."""
    # Create genes with modifiers affecting combat stats
    genes = StylingGene(
        name=config.name,
        description=f"Battle agent: {config.name}",
    )

    # Modify font size (affects attack)
    genes.font.size_h1 = int(config.font_size_h1 * config.attack_modifier)

    # Modify margins (affects defense)
    genes.margin.top = int(config.margin_top * config.defense_modifier)
    genes.margin.bottom = int(config.margin_top * config.defense_modifier)

    # Color contrast affects special power
    contrast_value = int(config.color_contrast * 255)
    genes.color.text = f"#{contrast_value:02x}{contrast_value:02x}{contrast_value:02x}"

    return StylingGenome.from_genes(genes)


def _combatant_to_response(combatant: Combatant) -> CombatantResponse:
    """Convert Combatant to response model."""
    return CombatantResponse(
        name=combatant.genome.scientific_name,
        health=combatant.current_health,
        max_health=combatant.stats.health,
        health_percent=combatant.health_percent,
        is_alive=combatant.is_alive,
        kills=combatant.kills,
        damage_dealt=combatant.damage_dealt,
        damage_taken=combatant.damage_taken,
        rounds_survived=combatant.rounds_survived,
        status="alive" if combatant.is_alive else "defeated",
    )


def _result_to_response(result: BattleResult) -> BattleResultResponse:
    """Convert BattleResult to response model."""
    return BattleResultResponse(
        battle_id=result.battle_id,
        winner=_combatant_to_response(result.winner) if result.winner else None,
        participants=[_combatant_to_response(c) for c in result.participants],
        duration_rounds=result.duration_rounds,
        total_damage=result.total_damage,
        start_time=result.start_time.isoformat(),
        end_time=result.end_time.isoformat(),
    )


# ============================================================================
# Battle Endpoints
# ============================================================================


@router.post("/battle/start", response_model=BattleResultResponse, status_code=201)
async def start_battle(request: BattleStartRequest, background_tasks: BackgroundTasks):
    """
    Start a battle royale between multiple agents.

    Returns battle results when complete.
    """
    # Create genomes from configs
    genomes = [_create_genome_from_config(config) for config in request.agents]

    # Set custom names
    for genome, config in zip(genomes, request.agents):
        genome.genes.name = config.name

    # Create arena with max rounds
    arena = BattleRoyale(max_rounds=request.max_rounds)

    # Run battle
    result = await arena.run_battle(genomes)

    # Store result
    _battles[result.battle_id] = result

    # Emit final WebSocket event
    try:
        await emit_battle_end(
            result.battle_id,
            result.winner.genome.scientific_name if result.winner else "No Winner",
            {
                "rounds": result.duration_rounds,
                "total_damage": result.total_damage,
                "participants": len(result.participants),
            },
        )
    except Exception as e:
        logger.warning(f"Failed to emit battle end event: {e}")

    logger.info(
        f"Battle {result.battle_id} complete: "
        f"Winner = {result.winner.genome.scientific_name if result.winner else 'None'}"
    )

    return _result_to_response(result)


@router.post("/battle/quick", response_model=BattleResultResponse)
async def quick_battle_endpoint(agent_a: AgentConfig, agent_b: AgentConfig):
    """
    Run a quick 1v1 battle between two agents.
    """
    genome_a = _create_genome_from_config(agent_a)
    genome_b = _create_genome_from_config(agent_b)

    result = await quick_battle([genome_a, genome_b])
    _battles[result.battle_id] = result

    return _result_to_response(result)


@router.get("/battle/{battle_id}", response_model=BattleResultResponse)
async def get_battle(battle_id: str):
    """Get battle results by ID."""
    if battle_id not in _battles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Battle {battle_id} not found",
        )
    return _result_to_response(_battles[battle_id])


@router.get("/battle/{battle_id}/summary")
async def get_battle_summary(battle_id: str):
    """Get a text summary of a battle."""
    if battle_id not in _battles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Battle {battle_id} not found",
        )

    result = _battles[battle_id]
    return {"summary": result.get_summary()}


# ============================================================================
# Tournament Endpoints
# ============================================================================


@router.post("/battle/tournament", response_model=TournamentResultResponse, status_code=201)
async def start_tournament(request: TournamentStartRequest):
    """
    Start a tournament with multiple rounds of battles.

    Agents are randomly grouped for battles, and scores are accumulated.
    """
    tournament_id = str(uuid4())[:8]

    # Create genomes
    genomes = [_create_genome_from_config(config) for config in request.agents]
    for genome, config in zip(genomes, request.agents):
        genome.genes.name = config.name

    # Run tournament
    arena = BattleRoyale()
    results = arena.run_tournament(genomes, rounds=request.rounds)

    # Store tournament
    _tournaments[tournament_id] = {
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }

    logger.info(
        f"Tournament {tournament_id} complete: "
        f"Champion = {results['champion']['name'] if results['champion'] else 'None'}"
    )

    return TournamentResultResponse(
        tournament_id=tournament_id,
        total_rounds=results["total_rounds"],
        participants=results["participants"],
        rankings=results["rankings"],
        champion=results["champion"],
    )


@router.get("/battle/tournament/{tournament_id}", response_model=TournamentResultResponse)
async def get_tournament(tournament_id: str):
    """Get tournament results by ID."""
    if tournament_id not in _tournaments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament {tournament_id} not found",
        )

    data = _tournaments[tournament_id]
    results = data["results"]

    return TournamentResultResponse(
        tournament_id=tournament_id,
        total_rounds=results["total_rounds"],
        participants=results["participants"],
        rankings=results["rankings"],
        champion=results["champion"],
    )


# ============================================================================
# History & Statistics Endpoints
# ============================================================================


@router.get("/battle/history", response_model=BattleHistoryResponse)
async def get_battle_history(limit: int = 10):
    """Get battle history with statistics."""
    battles = list(_battles.values())

    # Sort by end time (most recent first)
    battles.sort(key=lambda b: b.end_time, reverse=True)

    total_rounds = sum(b.duration_rounds for b in battles)
    total_damage = sum(b.total_damage for b in battles)

    return BattleHistoryResponse(
        total_battles=len(battles),
        total_rounds=total_rounds,
        total_damage=total_damage,
        recent_battles=[_result_to_response(b) for b in battles[:limit]],
    )


@router.get("/battle/stats")
async def get_battle_stats():
    """Get aggregated battle statistics."""
    if not _battles:
        return {
            "total_battles": 0,
            "total_rounds": 0,
            "total_damage": 0,
            "avg_rounds_per_battle": 0,
            "avg_damage_per_battle": 0,
            "unique_winners": 0,
        }

    battles = list(_battles.values())

    # Calculate stats
    total_rounds = sum(b.duration_rounds for b in battles)
    total_damage = sum(b.total_damage for b in battles)
    winners = set(
        b.winner.genome.scientific_name for b in battles if b.winner
    )

    return {
        "total_battles": len(battles),
        "total_rounds": total_rounds,
        "total_damage": round(total_damage, 2),
        "avg_rounds_per_battle": round(total_rounds / len(battles), 2),
        "avg_damage_per_battle": round(total_damage / len(battles), 2),
        "unique_winners": len(winners),
        "tournaments": len(_tournaments),
    }


@router.get("/battle/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get leaderboard of top-performing agents across all battles."""
    if not _battles:
        return {"leaderboard": []}

    # Aggregate stats by agent name
    agent_stats: dict[str, dict] = {}

    for battle in _battles.values():
        for combatant in battle.participants:
            name = combatant.genome.scientific_name
            if name not in agent_stats:
                agent_stats[name] = {
                    "name": name,
                    "battles": 0,
                    "wins": 0,
                    "kills": 0,
                    "damage_dealt": 0,
                    "rounds_survived": 0,
                }

            stats = agent_stats[name]
            stats["battles"] += 1
            stats["kills"] += combatant.kills
            stats["damage_dealt"] += combatant.damage_dealt
            stats["rounds_survived"] += combatant.rounds_survived

            if battle.winner and battle.winner.genome.scientific_name == name:
                stats["wins"] += 1

    # Sort by wins, then kills, then damage
    leaderboard = sorted(
        agent_stats.values(),
        key=lambda x: (x["wins"], x["kills"], x["damage_dealt"]),
        reverse=True,
    )

    return {"leaderboard": leaderboard[:limit]}


# ============================================================================
# Combat Stats Endpoints
# ============================================================================


@router.post("/battle/preview-stats")
async def preview_combat_stats(config: AgentConfig):
    """
    Preview the combat stats that would be derived from an agent configuration.

    Useful for planning battles.
    """
    genome = _create_genome_from_config(config)
    stats = BattleStats.from_genome(genome)

    return {
        "name": config.name,
        "stats": {
            "health": round(stats.health, 2),
            "attack": round(stats.attack, 2),
            "defense": round(stats.defense, 2),
            "speed": round(stats.speed, 2),
            "adaptability": round(stats.adaptability, 2),
            "regeneration": round(stats.regeneration, 2),
            "special_power": round(stats.special_power, 2),
        },
        "modifiers_applied": {
            "attack_modifier": config.attack_modifier,
            "defense_modifier": config.defense_modifier,
            "speed_modifier": config.speed_modifier,
        },
    }


@router.get("/battle/actions")
async def list_battle_actions():
    """List all available battle actions with descriptions."""
    return {
        "actions": [
            {
                "name": "attack",
                "description": "Basic attack dealing damage based on attack stat",
            },
            {
                "name": "defend",
                "description": "Defensive stance, reduces incoming damage by 50%",
            },
            {
                "name": "adapt",
                "description": "Temporary mutation providing random stat boost",
            },
            {
                "name": "regenerate",
                "description": "Heal based on regeneration stat",
            },
            {
                "name": "special",
                "description": "Powerful special attack using special_power stat",
            },
            {
                "name": "dodge",
                "description": "Attempt to evade attacks based on speed",
            },
        ]
    }


# ============================================================================
# Admin Endpoints
# ============================================================================


@router.post("/battle/reset")
async def reset_battle_history():
    """Reset all battle history."""
    count = len(_battles)
    tournament_count = len(_tournaments)

    _battles.clear()
    _tournaments.clear()
    _active_battles.clear()

    logger.info(f"Reset battle history: {count} battles, {tournament_count} tournaments")

    return {
        "message": f"Cleared {count} battles and {tournament_count} tournaments",
        "status": "reset",
    }


@router.get("/battle/report")
async def get_arena_report():
    """Generate comprehensive arena report."""
    report = _arena.generate_battle_report()

    return {
        "report": report,
        "total_battles": len(_battles),
        "total_tournaments": len(_tournaments),
        "timestamp": datetime.now().isoformat(),
    }
