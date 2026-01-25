"""
Agent Battle Royale: Competitive Fitness Evaluation Through Combat.

Pits agents against each other in simulated battles to determine
evolutionary fitness through direct competition rather than just metrics.

"In the arena of evolution, only the strongest survive."
"""

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from .styling_genome import StylingGenome


class BattleAction(str, Enum):
    """Actions an agent can take in battle."""

    ATTACK = "attack"
    DEFEND = "defend"
    ADAPT = "adapt"  # Temporary mutation
    REGENERATE = "regenerate"
    SPECIAL = "special"  # Fitness-based special move
    DODGE = "dodge"


class BattleStatus(str, Enum):
    """Status of a battle."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class BattleStats:
    """Combat statistics derived from genome."""

    health: float  # Base 100, modified by genes
    attack: float  # Base damage
    defense: float  # Damage reduction
    speed: float  # Action priority
    adaptability: float  # Mutation effectiveness
    regeneration: float  # Health recovery rate
    special_power: float  # Special move damage

    @classmethod
    def from_genome(cls, genome: StylingGenome) -> "BattleStats":
        """
        Derive battle stats from a genome's traits.

        Different gene categories contribute to different stats:
        - Font: Attack (bold = strong), Speed (smaller = faster)
        - Margin: Defense (padding = armor), Regeneration
        - Color: Special Power (contrast = intensity)
        - Layout: Health (columns = resilience), Adaptability
        """
        genes = genome.genes

        # Font-based stats
        attack = 10 + (genes.font.size_h1 / 24) * 15  # Bigger headings = stronger
        speed = 15 - (genes.font.size_body / 11) * 5  # Smaller body = faster

        # Margin-based stats
        defense = (genes.margin.top + genes.margin.bottom) / 4
        regeneration = genes.margin.paragraph_spacing / 10

        # Layout-based stats
        health = 80 + (genes.layout.columns * 20)
        adaptability = 0.5 if genes.layout.density == "compact" else 0.3

        # Color-based stats (contrast affects power)
        special_power = cls._calculate_contrast_power(
            genes.color.text, genes.color.background
        )

        # Fitness bonus
        fitness_multiplier = 1 + (genome.fitness_score or 0) * 0.5

        return cls(
            health=health * fitness_multiplier,
            attack=attack * fitness_multiplier,
            defense=defense * fitness_multiplier,
            speed=speed * fitness_multiplier,
            adaptability=adaptability,
            regeneration=regeneration * fitness_multiplier,
            special_power=special_power * fitness_multiplier,
        )

    @staticmethod
    def _calculate_contrast_power(text_color: str, bg_color: str) -> float:
        """Calculate special power from color contrast."""
        def hex_to_luminance(hex_color: str) -> float:
            r = int(hex_color[1:3], 16) / 255
            g = int(hex_color[3:5], 16) / 255
            b = int(hex_color[5:7], 16) / 255
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        try:
            lum_text = hex_to_luminance(text_color)
            lum_bg = hex_to_luminance(bg_color)
            contrast = abs(lum_text - lum_bg)
            return 15 + contrast * 30  # 15-45 range
        except Exception:
            return 20


@dataclass
class Combatant:
    """An agent participating in battle."""

    genome: StylingGenome
    stats: BattleStats
    current_health: float = field(init=False)
    is_alive: bool = True
    kills: int = 0
    damage_dealt: float = 0
    damage_taken: float = 0
    rounds_survived: int = 0
    actions_taken: list[BattleAction] = field(default_factory=list)
    temporary_buffs: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self.current_health = self.stats.health

    @property
    def health_percent(self) -> float:
        return max(0, self.current_health / self.stats.health)

    def take_damage(self, damage: float) -> float:
        """Apply damage after defense calculation."""
        actual_damage = max(0, damage - self.stats.defense * 0.5)

        # Apply temporary buffs
        if "defense_boost" in self.temporary_buffs:
            actual_damage *= 1 - self.temporary_buffs["defense_boost"]

        self.current_health -= actual_damage
        self.damage_taken += actual_damage

        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False

        return actual_damage

    def heal(self, amount: float):
        """Heal the combatant."""
        self.current_health = min(self.stats.health, self.current_health + amount)

    def choose_action(self, opponents: list["Combatant"]) -> tuple[BattleAction, "Combatant | None"]:
        """
        AI decision making for combat actions.

        Strategy based on current state and genome traits.
        """
        # Low health: prioritize defense/regeneration
        if self.health_percent < 0.3:
            if random.random() < 0.6:
                return (BattleAction.REGENERATE, None)
            if random.random() < 0.3:
                return (BattleAction.DEFEND, None)

        # High adaptability: more likely to adapt
        if random.random() < self.stats.adaptability:
            return (BattleAction.ADAPT, None)

        # Choose target (prefer weakest opponent)
        alive_opponents = [o for o in opponents if o.is_alive]
        if not alive_opponents:
            return (BattleAction.DEFEND, None)

        target = min(alive_opponents, key=lambda o: o.current_health)

        # Special attack if charged (based on damage dealt)
        if self.damage_dealt > 50 and random.random() < 0.3:
            return (BattleAction.SPECIAL, target)

        # Speed-based dodge chance
        if random.random() < self.stats.speed / 30:
            return (BattleAction.DODGE, None)

        return (BattleAction.ATTACK, target)

    def apply_buff(self, buff_type: str, value: float, duration: int = 1):
        """Apply a temporary buff."""
        self.temporary_buffs[buff_type] = value

    def clear_expired_buffs(self):
        """Clear buffs (simplified: clear all each round)."""
        self.temporary_buffs.clear()


@dataclass
class BattleRound:
    """A single round of combat."""

    round_number: int
    actions: list[dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BattleResult:
    """Result of a completed battle."""

    battle_id: str
    winner: Combatant | None
    participants: list[Combatant]
    rounds: list[BattleRound]
    duration_rounds: int
    total_damage: float
    start_time: datetime
    end_time: datetime = field(default_factory=datetime.utcnow)

    def get_summary(self) -> str:
        """Generate battle summary."""
        winner_name = self.winner.genome.scientific_name if self.winner else "No Winner"
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    BATTLE ROYALE RESULTS                      ║
╠══════════════════════════════════════════════════════════════╣
║  Battle ID: {self.battle_id}
║  Duration: {self.duration_rounds} rounds
║  Total Damage: {self.total_damage:.1f}
║
║  🏆 WINNER: {winner_name}
║
║  COMBATANTS:
"""
        for i, c in enumerate(sorted(self.participants, key=lambda x: -x.kills), 1):
            status = "👑" if c == self.winner else ("💀" if not c.is_alive else "⚔️")
            summary += f"║  {i}. {status} {c.genome.scientific_name[:20]:<20} | "
            summary += f"Kills: {c.kills} | Dmg: {c.damage_dealt:.0f} | Survived: {c.rounds_survived}r\n"

        summary += "╚══════════════════════════════════════════════════════════════╝"
        return summary


class BattleRoyale:
    """
    The Battle Royale Arena.

    Runs competitive evolution battles between agents,
    using their genomic traits as combat statistics.
    """

    def __init__(
        self,
        max_rounds: int = 100,
        event_callback: Callable[[str, dict], None] | None = None,
    ):
        """
        Initialize the battle arena.

        Args:
            max_rounds: Maximum rounds before forced end
            event_callback: Optional callback for real-time events
        """
        self.max_rounds = max_rounds
        self.event_callback = event_callback
        self.battle_history: list[BattleResult] = []

    async def run_battle(
        self,
        genomes: list[StylingGenome],
        battle_id: str | None = None,
    ) -> BattleResult:
        """
        Run a battle royale between multiple genomes.

        Args:
            genomes: List of genomes to battle
            battle_id: Optional battle identifier

        Returns:
            BattleResult with winner and statistics
        """
        if len(genomes) < 2:
            raise ValueError("Need at least 2 combatants for battle")

        battle_id = battle_id or str(uuid4())[:8]
        start_time = datetime.utcnow()

        # Create combatants
        combatants = [
            Combatant(genome=g, stats=BattleStats.from_genome(g))
            for g in genomes
        ]

        # Emit battle start
        await self._emit_event(
            "battle_start",
            {
                "battle_id": battle_id,
                "participants": [
                    {
                        "name": c.genome.scientific_name,
                        "health": c.stats.health,
                        "fitness": c.genome.fitness_score,
                    }
                    for c in combatants
                ],
            },
        )

        rounds: list[BattleRound] = []
        round_number = 0

        # Main battle loop
        while self._count_alive(combatants) > 1 and round_number < self.max_rounds:
            round_number += 1
            round_actions = await self._execute_round(
                combatants, round_number, battle_id
            )
            rounds.append(BattleRound(round_number=round_number, actions=round_actions))

            # Small delay for real-time feel
            await asyncio.sleep(0.05)

        # Determine winner
        alive = [c for c in combatants if c.is_alive]
        winner = max(alive, key=lambda c: c.current_health) if alive else None

        # Calculate total damage
        total_damage = sum(c.damage_dealt for c in combatants)

        result = BattleResult(
            battle_id=battle_id,
            winner=winner,
            participants=combatants,
            rounds=rounds,
            duration_rounds=round_number,
            total_damage=total_damage,
            start_time=start_time,
        )

        # Emit battle end
        await self._emit_event(
            "battle_end",
            {
                "battle_id": battle_id,
                "winner": winner.genome.scientific_name if winner else None,
                "rounds": round_number,
                "total_damage": total_damage,
            },
        )

        self.battle_history.append(result)
        return result

    async def _execute_round(
        self,
        combatants: list[Combatant],
        round_number: int,
        battle_id: str,
    ) -> list[dict[str, Any]]:
        """Execute a single round of combat."""
        actions = []

        # Sort by speed (faster acts first)
        turn_order = sorted(
            [c for c in combatants if c.is_alive],
            key=lambda c: -c.stats.speed,
        )

        for combatant in turn_order:
            if not combatant.is_alive:
                continue

            combatant.rounds_survived = round_number
            combatant.clear_expired_buffs()

            # Get opponents
            opponents = [c for c in combatants if c != combatant and c.is_alive]
            if not opponents:
                break

            # Choose and execute action
            action, target = combatant.choose_action(opponents)
            combatant.actions_taken.append(action)

            action_result = await self._execute_action(
                combatant, action, target, battle_id
            )
            actions.append(action_result)

        # Emit round complete
        await self._emit_event(
            "battle_round",
            {
                "battle_id": battle_id,
                "round": round_number,
                "alive_count": self._count_alive(combatants),
                "actions": actions,
            },
        )

        return actions

    async def _execute_action(
        self,
        actor: Combatant,
        action: BattleAction,
        target: Combatant | None,
        battle_id: str,
    ) -> dict[str, Any]:
        """Execute a combat action."""
        result = {
            "actor": actor.genome.scientific_name,
            "action": action.value,
            "target": target.genome.scientific_name if target else None,
        }

        if action == BattleAction.ATTACK and target:
            # Calculate damage
            damage = actor.stats.attack * (0.8 + random.random() * 0.4)
            actual_damage = target.take_damage(damage)
            actor.damage_dealt += actual_damage

            result["damage"] = actual_damage
            result["target_health"] = target.current_health

            # Check for kill
            if not target.is_alive:
                actor.kills += 1
                result["kill"] = True
                await self._emit_event(
                    "battle_death",
                    {
                        "battle_id": battle_id,
                        "victim": target.genome.scientific_name,
                        "killer": actor.genome.scientific_name,
                    },
                )

        elif action == BattleAction.DEFEND:
            actor.apply_buff("defense_boost", 0.5)
            result["buff"] = "defense +50%"

        elif action == BattleAction.REGENERATE:
            heal_amount = actor.stats.regeneration * 5
            actor.heal(heal_amount)
            result["heal"] = heal_amount

        elif action == BattleAction.ADAPT:
            # Temporary stat boost based on adaptability
            boost_type = random.choice(["attack", "defense", "speed"])
            boost_value = 0.3 * actor.stats.adaptability
            actor.apply_buff(f"{boost_type}_boost", boost_value)
            result["adaptation"] = f"{boost_type} +{boost_value:.0%}"

        elif action == BattleAction.SPECIAL and target:
            # High damage special attack
            damage = actor.stats.special_power * (1 + random.random())
            actual_damage = target.take_damage(damage)
            actor.damage_dealt += actual_damage

            result["damage"] = actual_damage
            result["special"] = True

            if not target.is_alive:
                actor.kills += 1
                result["kill"] = True

        elif action == BattleAction.DODGE:
            actor.apply_buff("dodge", 0.8)
            result["status"] = "dodging"

        return result

    def _count_alive(self, combatants: list[Combatant]) -> int:
        """Count alive combatants."""
        return sum(1 for c in combatants if c.is_alive)

    async def _emit_event(self, event_type: str, data: dict):
        """Emit event through callback if available."""
        if self.event_callback:
            try:
                self.event_callback(event_type, data)
            except Exception:
                pass

    def run_tournament(
        self,
        genomes: list[StylingGenome],
        rounds: int = 3,
    ) -> dict[str, Any]:
        """
        Run a tournament with multiple battle rounds.

        Args:
            genomes: All participating genomes
            rounds: Number of tournament rounds

        Returns:
            Tournament results with rankings
        """
        # Track wins and scores
        scores: dict[str, dict] = {
            g.genome_id: {
                "name": g.scientific_name,
                "wins": 0,
                "kills": 0,
                "damage": 0,
                "survived_rounds": 0,
            }
            for g in genomes
        }

        # Run tournament rounds
        for round_num in range(rounds):
            # Shuffle for random matchups
            shuffled = genomes.copy()
            random.shuffle(shuffled)

            # Battle in groups
            group_size = min(4, len(shuffled))
            for i in range(0, len(shuffled), group_size):
                group = shuffled[i : i + group_size]
                if len(group) >= 2:
                    result = asyncio.run(self.run_battle(group))

                    # Update scores
                    for combatant in result.participants:
                        gid = combatant.genome.genome_id
                        if gid in scores:
                            if combatant == result.winner:
                                scores[gid]["wins"] += 1
                            scores[gid]["kills"] += combatant.kills
                            scores[gid]["damage"] += combatant.damage_dealt
                            scores[gid]["survived_rounds"] += combatant.rounds_survived

        # Rank by wins, then kills, then damage
        rankings = sorted(
            scores.values(),
            key=lambda x: (x["wins"], x["kills"], x["damage"]),
            reverse=True,
        )

        return {
            "total_rounds": rounds,
            "participants": len(genomes),
            "rankings": rankings,
            "champion": rankings[0] if rankings else None,
        }

    def generate_battle_report(self) -> str:
        """Generate report of all battles."""
        if not self.battle_history:
            return "# Battle Report\n\nNo battles have been fought yet."

        total_battles = len(self.battle_history)
        total_rounds = sum(b.duration_rounds for b in self.battle_history)
        total_damage = sum(b.total_damage for b in self.battle_history)

        report = f"""# Battle Royale Report

## Overall Statistics
- **Total Battles**: {total_battles}
- **Total Rounds**: {total_rounds}
- **Total Damage Dealt**: {total_damage:.0f}
- **Average Battle Length**: {total_rounds / total_battles:.1f} rounds

## Recent Battles
"""

        for battle in self.battle_history[-5:]:
            winner_name = battle.winner.genome.scientific_name if battle.winner else "Draw"
            report += f"""
### Battle {battle.battle_id}
- **Winner**: {winner_name}
- **Rounds**: {battle.duration_rounds}
- **Participants**: {len(battle.participants)}
"""

        return report


# Convenience function for quick battles
async def quick_battle(genomes: list[StylingGenome]) -> BattleResult:
    """
    Run a quick battle between genomes.

    Args:
        genomes: List of genomes to battle

    Returns:
        BattleResult
    """
    arena = BattleRoyale()
    return await arena.run_battle(genomes)
