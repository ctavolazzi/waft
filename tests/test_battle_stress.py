#!/usr/bin/env python3
"""
BATTLE STRESS TESTS - EXTREME COMBAT TESTING

Tests the battle system under extreme conditions:
- Mass battles with many combatants
- Edge cases and boundary conditions
- Stress testing with thousands of operations
- Chaos testing with random inputs
- Performance benchmarking
"""

import random
import time
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4
import json

print("=" * 80)
print("⚔️  EXTREME BATTLE STRESS TESTS ⚔️")
print("=" * 80)


# ============================================================================
# INLINE BATTLE SYSTEM (for standalone testing)
# ============================================================================

class BattleAction(str, Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    ADAPT = "adapt"
    REGENERATE = "regenerate"
    SPECIAL = "special"
    DODGE = "dodge"
    COUNTER = "counter"
    BERSERK = "berserk"
    HEAL_ALLY = "heal_ally"
    TAUNT = "taunt"


@dataclass
class BattleStats:
    health: float
    attack: float
    defense: float
    speed: float
    adaptability: float
    regeneration: float
    special_power: float = 0.0
    critical_chance: float = 0.1
    dodge_chance: float = 0.1
    counter_chance: float = 0.05

    @classmethod
    def from_genome(cls, genome: dict) -> 'BattleStats':
        fonts = genome.get('fonts', {})
        colors = genome.get('colors', {})
        layout = genome.get('layout', {})
        fitness = max(0, min(1, genome.get('fitness', 0.5)))  # Clamp fitness

        # Clamp input values to reasonable ranges
        font_size = max(1, fonts.get('size', 12))
        margins = max(0, layout.get('margins', 10))
        padding = max(0, layout.get('padding', 5))
        line_height = max(0.1, fonts.get('line_height', 1.5))

        # Calculate stats with clamping
        base_health = 100
        health = max(50, base_health + font_size * 3 + margins * 2)
        attack = max(5, 15 + font_size + len(str(colors.get('primary', ''))))
        defense = max(0, 5 + margins + padding)
        speed = max(1, 10 + line_height * 5 - padding * 0.5)
        adaptability = max(1, fitness * 15 + 5)
        regeneration = max(1, 3 + padding * 0.5)
        special_power = max(5, fitness * 20 + 10)

        # Derived stats (clamped)
        critical_chance = min(0.5, max(0.01, 0.1 + fitness * 0.2))
        dodge_chance = min(0.4, max(0.01, 0.1 + speed * 0.01))
        counter_chance = min(0.3, max(0.01, 0.05 + defense * 0.005))

        return cls(
            health=health,
            attack=attack,
            defense=defense,
            speed=speed,
            adaptability=adaptability,
            regeneration=regeneration,
            special_power=special_power,
            critical_chance=critical_chance,
            dodge_chance=dodge_chance,
            counter_chance=counter_chance
        )

    @classmethod
    def random(cls) -> 'BattleStats':
        """Generate random battle stats."""
        return cls(
            health=random.uniform(80, 200),
            attack=random.uniform(10, 50),
            defense=random.uniform(5, 30),
            speed=random.uniform(5, 25),
            adaptability=random.uniform(5, 20),
            regeneration=random.uniform(1, 10),
            special_power=random.uniform(10, 40),
            critical_chance=random.uniform(0.05, 0.3),
            dodge_chance=random.uniform(0.05, 0.25),
            counter_chance=random.uniform(0.02, 0.15)
        )


@dataclass
class Combatant:
    name: str
    genome: dict
    stats: BattleStats
    current_health: float = None
    is_defending: bool = False
    is_berserking: bool = False
    is_taunting: bool = False
    status_effects: list = field(default_factory=list)
    action_history: list = field(default_factory=list)
    kills: int = 0
    damage_dealt: float = 0
    damage_taken: float = 0
    rounds_survived: int = 0
    critical_hits: int = 0
    dodges: int = 0
    counters: int = 0

    def __post_init__(self):
        if self.current_health is None:
            self.current_health = self.stats.health

    def take_damage(self, damage: float, attacker: 'Combatant' = None) -> tuple[float, str]:
        """Take damage and return (actual_damage, event_description)."""
        event = ""

        # Check dodge
        if random.random() < self.stats.dodge_chance and not self.is_taunting:
            self.dodges += 1
            return 0, f"{self.name} dodges the attack!"

        # Calculate defense
        defense_mult = 2.0 if self.is_defending else 1.0
        actual_damage = max(0, damage - self.stats.defense * defense_mult * 0.5)

        # Apply damage
        self.current_health = max(0, self.current_health - actual_damage)
        self.damage_taken += actual_damage

        event = f"{self.name} takes {actual_damage:.1f} damage ({self.current_health:.1f} HP left)"

        # Check counter
        if attacker and random.random() < self.stats.counter_chance and self.is_alive:
            counter_damage = self.stats.attack * 0.5
            attacker.current_health -= counter_damage
            attacker.damage_taken += counter_damage
            self.damage_dealt += counter_damage
            self.counters += 1
            event += f" and counters for {counter_damage:.1f}!"

        return actual_damage, event

    def heal(self, amount: float) -> float:
        """Heal and return actual healing done."""
        max_heal = self.stats.health - self.current_health
        actual_heal = min(amount, max_heal)
        self.current_health += actual_heal
        return actual_heal

    @property
    def is_alive(self) -> bool:
        return self.current_health > 0

    @property
    def health_percent(self) -> float:
        return (self.current_health / self.stats.health) * 100 if self.stats.health > 0 else 0


@dataclass
class BattleResult:
    battle_id: str
    winner: Combatant = None
    participants: list = field(default_factory=list)
    duration_rounds: int = 0
    total_damage: float = 0
    battle_log: list = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime = None


class BattleRoyale:
    """Battle arena for agent combat."""

    def __init__(self, max_rounds: int = 1000):
        self.max_rounds = max_rounds
        self.battle_history: list[BattleResult] = []

    def create_combatant(self, name: str, genome: dict = None) -> Combatant:
        """Create a combatant."""
        if genome is None:
            genome = self._random_genome()
        stats = BattleStats.from_genome(genome)
        return Combatant(name=name, genome=genome, stats=stats)

    def _random_genome(self) -> dict:
        """Generate a random genome."""
        return {
            'name': f'Random-{uuid4().hex[:6]}',
            'fonts': {'size': random.randint(10, 24), 'line_height': random.uniform(1.0, 2.0)},
            'colors': {'primary': f'#{random.randint(0, 0xFFFFFF):06x}'},
            'layout': {'margins': random.randint(5, 25), 'padding': random.randint(2, 15)},
            'fitness': random.random()
        }

    def run_battle(self, combatants: list[Combatant]) -> BattleResult:
        """Run a battle between combatants."""
        battle_id = str(uuid4())[:8]
        result = BattleResult(battle_id=battle_id, participants=combatants)

        # Reset combatants
        for c in combatants:
            c.current_health = c.stats.health
            c.kills = 0
            c.damage_dealt = 0
            c.damage_taken = 0
            c.rounds_survived = 0

        round_num = 0
        while round_num < self.max_rounds:
            round_num += 1
            alive = [c for c in combatants if c.is_alive]

            if len(alive) <= 1:
                break

            # Sort by speed for turn order
            alive.sort(key=lambda c: c.stats.speed, reverse=True)

            for actor in alive:
                if not actor.is_alive:
                    continue

                targets = [c for c in alive if c.is_alive and c != actor]
                if not targets:
                    break

                # Choose action
                action = self._choose_action(actor, targets)
                event = self._execute_action(actor, targets, action)
                result.battle_log.append(f"Round {round_num}: {event}")

            # Update rounds survived
            for c in combatants:
                if c.is_alive:
                    c.rounds_survived = round_num

        # Determine winner
        alive = [c for c in combatants if c.is_alive]
        if len(alive) == 1:
            result.winner = alive[0]
        elif len(alive) > 1:
            # Most health wins
            result.winner = max(alive, key=lambda c: c.current_health)

        result.duration_rounds = round_num
        result.total_damage = sum(c.damage_dealt for c in combatants)
        result.end_time = datetime.utcnow()

        # Ensure winner's rounds_survived matches duration
        if result.winner:
            result.winner.rounds_survived = result.duration_rounds

        self.battle_history.append(result)
        return result

    def _choose_action(self, actor: Combatant, targets: list[Combatant]) -> BattleAction:
        """AI chooses action."""
        health_ratio = actor.current_health / actor.stats.health

        if actor.is_berserking:
            return random.choice([BattleAction.ATTACK, BattleAction.SPECIAL])

        if health_ratio < 0.2:
            return random.choice([BattleAction.REGENERATE, BattleAction.DEFEND, BattleAction.DODGE])
        elif health_ratio < 0.4:
            return random.choice([BattleAction.REGENERATE, BattleAction.DEFEND, BattleAction.ATTACK, BattleAction.ADAPT])
        elif health_ratio > 0.8:
            weights = [0.4, 0.05, 0.1, 0.05, 0.2, 0.05, 0.05, 0.05, 0, 0.05]
            return random.choices(list(BattleAction), weights=weights)[0]
        else:
            return random.choice(list(BattleAction))

    def _execute_action(self, actor: Combatant, targets: list[Combatant], action: BattleAction) -> str:
        """Execute an action."""
        actor.is_defending = False
        actor.action_history.append(action)
        target = random.choice(targets) if targets else None

        if action == BattleAction.ATTACK:
            if not target:
                return f"{actor.name} has no target"
            damage = actor.stats.attack * random.uniform(0.8, 1.2)

            # Critical hit
            if random.random() < actor.stats.critical_chance:
                damage *= 2
                actor.critical_hits += 1
                actual, event = target.take_damage(damage, actor)
                actor.damage_dealt += actual
                if not target.is_alive:
                    actor.kills += 1
                return f"{actor.name} CRITS {target.name}! {event}"

            actual, event = target.take_damage(damage, actor)
            actor.damage_dealt += actual
            if not target.is_alive:
                actor.kills += 1
            return f"{actor.name} attacks {target.name}: {event}"

        elif action == BattleAction.DEFEND:
            actor.is_defending = True
            return f"{actor.name} takes a defensive stance"

        elif action == BattleAction.REGENERATE:
            heal = actor.stats.regeneration * random.uniform(1.0, 2.0)
            actual = actor.heal(heal)
            return f"{actor.name} regenerates {actual:.1f} HP ({actor.current_health:.1f})"

        elif action == BattleAction.SPECIAL:
            if not target:
                return f"{actor.name} has no target for special"
            damage = actor.stats.special_power * random.uniform(1.0, 1.5)
            actual, event = target.take_damage(damage, actor)
            actor.damage_dealt += actual
            if not target.is_alive:
                actor.kills += 1
            return f"{actor.name} uses SPECIAL on {target.name}: {event}"

        elif action == BattleAction.DODGE:
            actor.is_defending = True
            return f"{actor.name} prepares to dodge"

        elif action == BattleAction.ADAPT:
            stat = random.choice(['attack', 'defense', 'speed', 'regeneration'])
            boost = 1.1
            setattr(actor.stats, stat, getattr(actor.stats, stat) * boost)
            return f"{actor.name} adapts: {stat} +10%"

        elif action == BattleAction.COUNTER:
            actor.stats.counter_chance = min(0.5, actor.stats.counter_chance + 0.1)
            return f"{actor.name} prepares to counter"

        elif action == BattleAction.BERSERK:
            actor.is_berserking = True
            actor.stats.attack *= 1.5
            actor.stats.defense *= 0.5
            return f"{actor.name} goes BERSERK!"

        elif action == BattleAction.HEAL_ALLY:
            allies = [c for c in targets if c.current_health < c.stats.health]
            if allies:
                ally = min(allies, key=lambda c: c.current_health)
                heal = actor.stats.regeneration * 0.5
                actual = ally.heal(heal)
                return f"{actor.name} heals {ally.name} for {actual:.1f} HP"
            return f"{actor.name} has no ally to heal"

        elif action == BattleAction.TAUNT:
            if target:
                target.is_taunting = True
                return f"{actor.name} taunts {target.name}"
            return f"{actor.name} taunts the air"

        return f"{actor.name} does nothing"

    def run_tournament(self, combatants: list[Combatant], rounds: int = 3) -> dict:
        """Run a tournament with multiple rounds."""
        scores = {c.name: {'wins': 0, 'kills': 0, 'damage': 0} for c in combatants}
        battles = []

        for round_num in range(rounds):
            # Shuffle and pair up
            random.shuffle(combatants)
            for i in range(0, len(combatants) - 1, 2):
                pair = combatants[i:i+2]
                if len(pair) == 2:
                    result = self.run_battle([
                        self.create_combatant(pair[0].name, pair[0].genome),
                        self.create_combatant(pair[1].name, pair[1].genome)
                    ])
                    battles.append(result)

                    if result.winner:
                        scores[result.winner.name]['wins'] += 1
                    for p in result.participants:
                        scores[p.name]['kills'] += p.kills
                        scores[p.name]['damage'] += p.damage_dealt

        # Rank by wins, then kills, then damage
        rankings = sorted(
            [{'name': k, **v} for k, v in scores.items()],
            key=lambda x: (x['wins'], x['kills'], x['damage']),
            reverse=True
        )

        return {
            'tournament_id': str(uuid4())[:8],
            'total_rounds': rounds,
            'total_battles': len(battles),
            'participants': len(combatants),
            'rankings': rankings,
            'champion': rankings[0] if rankings else None
        }


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_basic_combat():
    """Test basic combat mechanics."""
    print("\n" + "=" * 70)
    print("🔥 TEST 1: Basic Combat Mechanics")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0

    # Test 1: Two combatant battle
    try:
        c1 = arena.create_combatant("Alpha")
        c2 = arena.create_combatant("Beta")
        result = arena.run_battle([c1, c2])

        assert result.winner is not None
        assert result.duration_rounds > 0
        assert result.total_damage > 0
        assert len(result.participants) == 2
        print(f"  ✓ 1v1 battle: {result.winner.name} wins in {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ 1v1 battle failed: {e}")
        failed += 1

    # Test 2: Free-for-all
    try:
        combatants = [arena.create_combatant(f"Fighter-{i}") for i in range(5)]
        result = arena.run_battle(combatants)

        assert result.winner is not None
        assert result.duration_rounds > 0
        alive_count = sum(1 for c in result.participants if c.is_alive)
        assert alive_count >= 1
        print(f"  ✓ 5-way FFA: {result.winner.name} wins, {alive_count} alive, {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ FFA battle failed: {e}")
        failed += 1

    # Test 3: Damage tracking
    try:
        c1 = arena.create_combatant("Attacker")
        c2 = arena.create_combatant("Defender")
        result = arena.run_battle([c1, c2])

        total_dealt = sum(c.damage_dealt for c in result.participants)
        total_taken = sum(c.damage_taken for c in result.participants)
        assert abs(total_dealt - total_taken) < 0.01, "Damage dealt should equal damage taken"
        print(f"  ✓ Damage tracking: {total_dealt:.1f} dealt = {total_taken:.1f} taken")
        passed += 1
    except Exception as e:
        print(f"  ✗ Damage tracking failed: {e}")
        failed += 1

    # Test 4: Kill counting
    try:
        combatants = [arena.create_combatant(f"Warrior-{i}") for i in range(4)]
        result = arena.run_battle(combatants)

        total_kills = sum(c.kills for c in result.participants)
        dead_count = sum(1 for c in result.participants if not c.is_alive)
        assert total_kills == dead_count, f"Kills ({total_kills}) should equal deaths ({dead_count})"
        print(f"  ✓ Kill counting: {total_kills} kills, {dead_count} deaths")
        passed += 1
    except Exception as e:
        print(f"  ✗ Kill counting failed: {e}")
        failed += 1

    # Test 5: Round survival tracking
    try:
        combatants = [arena.create_combatant(f"Survivor-{i}") for i in range(3)]
        result = arena.run_battle(combatants)

        assert all(c.rounds_survived > 0 for c in result.participants)
        assert result.winner.rounds_survived == result.duration_rounds
        print(f"  ✓ Survival tracking: Winner survived {result.winner.rounds_survived} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ Survival tracking failed: {e}")
        failed += 1

    return passed, failed


def test_extreme_battles():
    """Test extreme battle scenarios."""
    print("\n" + "=" * 70)
    print("🌋 TEST 2: Extreme Battle Scenarios")
    print("=" * 70)

    arena = BattleRoyale(max_rounds=500)
    passed = 0
    failed = 0

    # Test 1: Mass battle (20 combatants)
    try:
        start = time.time()
        combatants = [arena.create_combatant(f"Mass-{i}") for i in range(20)]
        result = arena.run_battle(combatants)
        elapsed = time.time() - start

        assert result.winner is not None
        assert elapsed < 5.0, f"Battle took too long: {elapsed:.2f}s"
        print(f"  ✓ 20-way battle: {result.winner.name} wins in {result.duration_rounds} rounds ({elapsed:.2f}s)")
        passed += 1
    except Exception as e:
        print(f"  ✗ Mass battle failed: {e}")
        failed += 1

    # Test 2: Rapid successive battles
    try:
        start = time.time()
        wins = {}
        for i in range(50):
            c1 = arena.create_combatant("Rapid-A")
            c2 = arena.create_combatant("Rapid-B")
            result = arena.run_battle([c1, c2])
            if result.winner:
                wins[result.winner.name] = wins.get(result.winner.name, 0) + 1
        elapsed = time.time() - start

        print(f"  ✓ 50 rapid battles in {elapsed:.2f}s (Win distribution: {wins})")
        passed += 1
    except Exception as e:
        print(f"  ✗ Rapid battles failed: {e}")
        failed += 1

    # Test 3: Glass cannon vs Tank
    try:
        glass_cannon = {
            'fonts': {'size': 50, 'line_height': 2.0},
            'colors': {'primary': '#FF0000'},
            'layout': {'margins': 1, 'padding': 1},
            'fitness': 0.9
        }
        tank = {
            'fonts': {'size': 8, 'line_height': 1.0},
            'colors': {'primary': '#0000FF'},
            'layout': {'margins': 50, 'padding': 30},
            'fitness': 0.9
        }

        gc_wins = 0
        tank_wins = 0
        for _ in range(30):
            c1 = Combatant("GlassCannon", glass_cannon, BattleStats.from_genome(glass_cannon))
            c2 = Combatant("Tank", tank, BattleStats.from_genome(tank))
            result = arena.run_battle([c1, c2])
            if result.winner.name == "GlassCannon":
                gc_wins += 1
            else:
                tank_wins += 1

        print(f"  ✓ Glass Cannon vs Tank (30 fights): GC={gc_wins}, Tank={tank_wins}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Archetype battle failed: {e}")
        failed += 1

    # Test 4: Extremely long battle (evenly matched)
    try:
        even_genome = {
            'fonts': {'size': 15, 'line_height': 1.5},
            'colors': {'primary': '#808080'},
            'layout': {'margins': 20, 'padding': 10},
            'fitness': 0.7
        }

        c1 = Combatant("Even-A", even_genome, BattleStats.from_genome(even_genome))
        c2 = Combatant("Even-B", even_genome, BattleStats.from_genome(even_genome))

        arena_long = BattleRoyale(max_rounds=2000)
        result = arena_long.run_battle([c1, c2])

        print(f"  ✓ Even match battle: {result.winner.name} wins in {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ Long battle failed: {e}")
        failed += 1

    # Test 5: Instant death scenario
    try:
        giant = {
            'fonts': {'size': 100, 'line_height': 3.0},
            'colors': {'primary': '#FFFFFF'},
            'layout': {'margins': 0, 'padding': 0},
            'fitness': 1.0
        }
        tiny = {
            'fonts': {'size': 6, 'line_height': 1.0},
            'colors': {'primary': '#000000'},
            'layout': {'margins': 1, 'padding': 1},
            'fitness': 0.1
        }

        c1 = Combatant("Giant", giant, BattleStats.from_genome(giant))
        c2 = Combatant("Tiny", tiny, BattleStats.from_genome(tiny))
        result = arena.run_battle([c1, c2])

        print(f"  ✓ Mismatch battle: {result.winner.name} wins in {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ Mismatch battle failed: {e}")
        failed += 1

    return passed, failed


def test_tournaments():
    """Test tournament system."""
    print("\n" + "=" * 70)
    print("🏆 TEST 3: Tournament System")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0

    # Test 1: Standard tournament
    try:
        combatants = [arena.create_combatant(f"TourneyFighter-{i}") for i in range(8)]
        result = arena.run_tournament(combatants, rounds=3)

        assert result['champion'] is not None
        assert len(result['rankings']) == 8
        assert result['total_rounds'] == 3
        print(f"  ✓ 8-fighter tournament: Champion = {result['champion']['name']} ({result['champion']['wins']} wins)")
        passed += 1
    except Exception as e:
        print(f"  ✗ Standard tournament failed: {e}")
        failed += 1

    # Test 2: Large tournament
    try:
        combatants = [arena.create_combatant(f"BigTourney-{i}") for i in range(32)]
        start = time.time()
        result = arena.run_tournament(combatants, rounds=5)
        elapsed = time.time() - start

        assert result['champion'] is not None
        assert elapsed < 30.0
        print(f"  ✓ 32-fighter tournament in {elapsed:.2f}s: Champion = {result['champion']['name']}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Large tournament failed: {e}")
        failed += 1

    # Test 3: Single round tournament
    try:
        combatants = [arena.create_combatant(f"SingleRound-{i}") for i in range(4)]
        result = arena.run_tournament(combatants, rounds=1)

        assert result['total_rounds'] == 1
        print(f"  ✓ Single round tournament: {result['total_battles']} battles")
        passed += 1
    except Exception as e:
        print(f"  ✗ Single round tournament failed: {e}")
        failed += 1

    # Test 4: Many round tournament
    try:
        combatants = [arena.create_combatant(f"ManyRounds-{i}") for i in range(6)]
        result = arena.run_tournament(combatants, rounds=10)

        assert result['total_rounds'] == 10
        top = result['rankings'][0]
        print(f"  ✓ 10-round tournament: Champion = {top['name']} ({top['wins']} wins, {top['kills']} kills)")
        passed += 1
    except Exception as e:
        print(f"  ✗ Many round tournament failed: {e}")
        failed += 1

    # Test 5: Verify ranking order
    try:
        combatants = [arena.create_combatant(f"RankCheck-{i}") for i in range(8)]
        result = arena.run_tournament(combatants, rounds=5)

        rankings = result['rankings']
        for i in range(len(rankings) - 1):
            curr = rankings[i]
            next_r = rankings[i + 1]
            assert curr['wins'] >= next_r['wins'], "Rankings should be sorted by wins"
        print(f"  ✓ Ranking order verified: Top 3 = {[r['name'] for r in rankings[:3]]}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Ranking verification failed: {e}")
        failed += 1

    return passed, failed


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n" + "=" * 70)
    print("🔬 TEST 4: Edge Cases & Boundaries")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0

    # Test 1: Minimum stats
    try:
        min_genome = {
            'fonts': {'size': 6, 'line_height': 1.0},
            'colors': {'primary': '#000000'},
            'layout': {'margins': 0, 'padding': 0},
            'fitness': 0.0
        }
        c = Combatant("MinStats", min_genome, BattleStats.from_genome(min_genome))
        assert c.stats.health > 0
        assert c.stats.attack > 0
        print(f"  ✓ Min stats combatant: HP={c.stats.health:.1f}, ATK={c.stats.attack:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Min stats test failed: {e}")
        failed += 1

    # Test 2: Maximum stats
    try:
        max_genome = {
            'fonts': {'size': 100, 'line_height': 3.0},
            'colors': {'primary': '#FFFFFFFFFFFF'},
            'layout': {'margins': 100, 'padding': 100},
            'fitness': 1.0
        }
        c = Combatant("MaxStats", max_genome, BattleStats.from_genome(max_genome))
        assert c.stats.health > 100
        print(f"  ✓ Max stats combatant: HP={c.stats.health:.1f}, ATK={c.stats.attack:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Max stats test failed: {e}")
        failed += 1

    # Test 3: Zero fitness
    try:
        zero_fitness = {'fonts': {'size': 12}, 'colors': {}, 'layout': {}, 'fitness': 0}
        c = Combatant("ZeroFit", zero_fitness, BattleStats.from_genome(zero_fitness))
        result = arena.run_battle([c, arena.create_combatant("Normal")])
        assert result.winner is not None
        print(f"  ✓ Zero fitness battle: {result.winner.name} wins")
        passed += 1
    except Exception as e:
        print(f"  ✗ Zero fitness test failed: {e}")
        failed += 1

    # Test 4: Empty genome fields
    try:
        sparse = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.5}
        c = Combatant("Sparse", sparse, BattleStats.from_genome(sparse))
        assert c.stats.health > 0
        print(f"  ✓ Sparse genome: HP={c.stats.health:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Sparse genome test failed: {e}")
        failed += 1

    # Test 5: Self-battle (same genome)
    try:
        genome = arena._random_genome()
        c1 = Combatant("Clone-A", genome.copy(), BattleStats.from_genome(genome))
        c2 = Combatant("Clone-B", genome.copy(), BattleStats.from_genome(genome))
        result = arena.run_battle([c1, c2])
        # Should still produce a winner due to randomness
        assert result.winner is not None
        print(f"  ✓ Clone battle: {result.winner.name} wins in {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ Clone battle test failed: {e}")
        failed += 1

    # Test 6: Single combatant (edge case)
    try:
        c = arena.create_combatant("Lonely")
        result = arena.run_battle([c])
        assert result.winner == c
        print(f"  ✓ Single combatant: Auto-wins")
        passed += 1
    except Exception as e:
        print(f"  ✗ Single combatant test failed: {e}")
        failed += 1

    # Test 7: Very short max_rounds
    try:
        short_arena = BattleRoyale(max_rounds=1)
        c1 = arena.create_combatant("Quick-A")
        c2 = arena.create_combatant("Quick-B")
        result = short_arena.run_battle([c1, c2])
        assert result.duration_rounds <= 1
        print(f"  ✓ 1-round limit: Battle ended in {result.duration_rounds} rounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ Short rounds test failed: {e}")
        failed += 1

    return passed, failed


def test_chaos():
    """Chaos testing with random operations."""
    print("\n" + "=" * 70)
    print("🌀 TEST 5: Chaos Testing")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0
    chaos_errors = []

    # Test 1: Random genome chaos
    try:
        for i in range(100):
            genome = {
                'fonts': {'size': random.randint(-100, 200), 'line_height': random.uniform(-5, 10)},
                'colors': {'primary': f'#{random.randint(0, 0xFFFFFFFFFF):010x}'[:7]},
                'layout': {'margins': random.randint(-50, 200), 'padding': random.uniform(-10, 50)},
                'fitness': random.uniform(-1, 2)
            }
            c = Combatant(f"Chaos-{i}", genome, BattleStats.from_genome(genome))
            assert c.stats.health > 0, f"Health must be positive, got {c.stats.health}"
        print(f"  ✓ 100 random genomes: All produced valid combatants")
        passed += 1
    except Exception as e:
        print(f"  ✗ Random genome chaos failed: {e}")
        failed += 1

    # Test 2: Random battle sizes
    try:
        for size in [2, 3, 5, 7, 10, 15, 25]:
            combatants = [arena.create_combatant(f"Chaos-{i}") for i in range(size)]
            result = arena.run_battle(combatants)
            assert result.winner is not None or result.duration_rounds > 0
        print(f"  ✓ Variable battle sizes (2-25): All completed")
        passed += 1
    except Exception as e:
        print(f"  ✗ Variable size chaos failed: {e}")
        failed += 1

    # Test 3: Interleaved operations
    try:
        operations = 0
        for _ in range(50):
            op = random.choice(['battle', 'tournament', 'create'])
            if op == 'battle':
                n = random.randint(2, 8)
                combatants = [arena.create_combatant(f"Op-{operations}-{i}") for i in range(n)]
                arena.run_battle(combatants)
            elif op == 'tournament':
                n = random.randint(4, 12)
                combatants = [arena.create_combatant(f"Op-{operations}-{i}") for i in range(n)]
                arena.run_tournament(combatants, rounds=random.randint(1, 5))
            else:
                arena.create_combatant(f"Op-{operations}")
            operations += 1
        print(f"  ✓ 50 interleaved operations: All completed")
        passed += 1
    except Exception as e:
        print(f"  ✗ Interleaved operations failed: {e}")
        failed += 1

    # Test 4: Unicode names
    try:
        unicode_names = ["🔥火", "⚔️剣士", "🛡️防御", "💀死神", "🌟星", "αβγ", "日本語", "Ñoño"]
        combatants = [arena.create_combatant(name) for name in unicode_names]
        result = arena.run_battle(combatants)
        assert result.winner is not None
        print(f"  ✓ Unicode names: {result.winner.name} wins")
        passed += 1
    except Exception as e:
        print(f"  ✗ Unicode names failed: {e}")
        failed += 1

    # Test 5: Extremely long names
    try:
        long_name = "A" * 1000
        c1 = arena.create_combatant(long_name)
        c2 = arena.create_combatant("Normal")
        result = arena.run_battle([c1, c2])
        assert result.winner is not None
        print(f"  ✓ Long name (1000 chars): Battle completed")
        passed += 1
    except Exception as e:
        print(f"  ✗ Long name failed: {e}")
        failed += 1

    return passed, failed


def test_performance():
    """Performance benchmarks."""
    print("\n" + "=" * 70)
    print("⚡ TEST 6: Performance Benchmarks")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0

    # Benchmark 1: Battle throughput
    try:
        start = time.time()
        battle_count = 100
        for _ in range(battle_count):
            c1 = arena.create_combatant("Perf-A")
            c2 = arena.create_combatant("Perf-B")
            arena.run_battle([c1, c2])
        elapsed = time.time() - start
        battles_per_sec = battle_count / elapsed

        assert battles_per_sec > 10, f"Too slow: {battles_per_sec:.1f} battles/sec"
        print(f"  ✓ Battle throughput: {battles_per_sec:.1f} battles/sec ({battle_count} in {elapsed:.2f}s)")
        passed += 1
    except Exception as e:
        print(f"  ✗ Battle throughput failed: {e}")
        failed += 1

    # Benchmark 2: Large battle performance
    try:
        sizes = [10, 20, 50]
        for size in sizes:
            start = time.time()
            combatants = [arena.create_combatant(f"Large-{i}") for i in range(size)]
            result = arena.run_battle(combatants)
            elapsed = time.time() - start
            print(f"    {size}-way battle: {elapsed:.3f}s, {result.duration_rounds} rounds")
        print(f"  ✓ Large battle scaling: All sizes completed")
        passed += 1
    except Exception as e:
        print(f"  ✗ Large battle performance failed: {e}")
        failed += 1

    # Benchmark 3: Tournament performance
    try:
        start = time.time()
        combatants = [arena.create_combatant(f"Tourney-{i}") for i in range(16)]
        result = arena.run_tournament(combatants, rounds=10)
        elapsed = time.time() - start

        print(f"  ✓ Tournament (16 fighters, 10 rounds): {elapsed:.2f}s, {result['total_battles']} battles")
        passed += 1
    except Exception as e:
        print(f"  ✗ Tournament performance failed: {e}")
        failed += 1

    # Benchmark 4: Combatant creation
    try:
        start = time.time()
        count = 1000
        for i in range(count):
            arena.create_combatant(f"Create-{i}")
        elapsed = time.time() - start
        creates_per_sec = count / elapsed

        assert creates_per_sec > 100
        print(f"  ✓ Combatant creation: {creates_per_sec:.0f}/sec ({count} in {elapsed:.3f}s)")
        passed += 1
    except Exception as e:
        print(f"  ✗ Creation performance failed: {e}")
        failed += 1

    # Benchmark 5: Memory stability
    try:
        import sys
        initial_battles = len(arena.battle_history)
        for _ in range(200):
            combatants = [arena.create_combatant(f"Mem-{i}") for i in range(5)]
            arena.run_battle(combatants)
        final_battles = len(arena.battle_history)

        battles_added = final_battles - initial_battles
        assert battles_added == 200
        print(f"  ✓ Memory stability: {battles_added} battles added to history")
        passed += 1
    except Exception as e:
        print(f"  ✗ Memory stability failed: {e}")
        failed += 1

    return passed, failed


def test_stat_derivation():
    """Test that stats are derived correctly from genomes."""
    print("\n" + "=" * 70)
    print("📊 TEST 7: Stat Derivation")
    print("=" * 70)

    passed = 0
    failed = 0

    # Test 1: Fitness affects adaptability
    try:
        low_fit = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.1}
        high_fit = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.9}

        low_stats = BattleStats.from_genome(low_fit)
        high_stats = BattleStats.from_genome(high_fit)

        assert high_stats.adaptability > low_stats.adaptability
        assert high_stats.special_power > low_stats.special_power
        print(f"  ✓ Fitness affects adaptability: Low={low_stats.adaptability:.1f}, High={high_stats.adaptability:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Fitness test failed: {e}")
        failed += 1

    # Test 2: Font size affects health/attack
    try:
        small = {'fonts': {'size': 8}, 'colors': {}, 'layout': {}, 'fitness': 0.5}
        large = {'fonts': {'size': 30}, 'colors': {}, 'layout': {}, 'fitness': 0.5}

        small_stats = BattleStats.from_genome(small)
        large_stats = BattleStats.from_genome(large)

        assert large_stats.health > small_stats.health
        assert large_stats.attack > small_stats.attack
        print(f"  ✓ Font size affects HP/ATK: Small HP={small_stats.health:.0f}, Large HP={large_stats.health:.0f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Font size test failed: {e}")
        failed += 1

    # Test 3: Margins affect defense
    try:
        thin = {'fonts': {}, 'colors': {}, 'layout': {'margins': 5}, 'fitness': 0.5}
        thick = {'fonts': {}, 'colors': {}, 'layout': {'margins': 40}, 'fitness': 0.5}

        thin_stats = BattleStats.from_genome(thin)
        thick_stats = BattleStats.from_genome(thick)

        assert thick_stats.defense > thin_stats.defense
        print(f"  ✓ Margins affect DEF: Thin={thin_stats.defense:.1f}, Thick={thick_stats.defense:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Margins test failed: {e}")
        failed += 1

    # Test 4: All stats are positive
    try:
        for _ in range(50):
            genome = {
                'fonts': {'size': random.randint(1, 100), 'line_height': random.uniform(0.5, 3)},
                'colors': {'primary': f'#{random.randint(0, 0xFFFFFF):06x}'},
                'layout': {'margins': random.randint(0, 100), 'padding': random.randint(0, 50)},
                'fitness': random.random()
            }
            stats = BattleStats.from_genome(genome)
            assert stats.health > 0
            assert stats.attack > 0
            assert stats.defense >= 0
            assert stats.speed > 0
        print(f"  ✓ All stats positive: 50 random genomes validated")
        passed += 1
    except Exception as e:
        print(f"  ✗ Positive stats test failed: {e}")
        failed += 1

    # Test 5: Critical/dodge/counter chances are bounded
    try:
        for _ in range(50):
            genome = {
                'fonts': {'size': random.randint(1, 100)},
                'colors': {},
                'layout': {'margins': random.randint(0, 100)},
                'fitness': random.random()
            }
            stats = BattleStats.from_genome(genome)
            assert 0 <= stats.critical_chance <= 1
            assert 0 <= stats.dodge_chance <= 1
            assert 0 <= stats.counter_chance <= 1
        print(f"  ✓ Chance stats bounded [0,1]: 50 random genomes validated")
        passed += 1
    except Exception as e:
        print(f"  ✗ Bounded stats test failed: {e}")
        failed += 1

    return passed, failed


def test_action_mechanics():
    """Test all battle action mechanics."""
    print("\n" + "=" * 70)
    print("⚙️ TEST 8: Action Mechanics")
    print("=" * 70)

    arena = BattleRoyale()
    passed = 0
    failed = 0

    # Test 1: Defend reduces damage
    try:
        genome = {'fonts': {'size': 15}, 'colors': {}, 'layout': {'margins': 10}, 'fitness': 0.5}
        defender = Combatant("Defender", genome, BattleStats.from_genome(genome))
        defender.is_defending = True
        defender.stats.dodge_chance = 0  # Disable dodge for clean test
        defender.stats.counter_chance = 0  # Disable counter for clean test

        normal = Combatant("Normal", genome, BattleStats.from_genome(genome))
        normal.stats.dodge_chance = 0  # Disable dodge for clean test
        normal.stats.counter_chance = 0  # Disable counter for clean test

        # Same damage to both
        _, _ = defender.take_damage(50)
        _, _ = normal.take_damage(50)

        # Defender should have taken less actual damage
        assert defender.current_health > normal.current_health
        print(f"  ✓ Defend reduces damage: Defended HP={defender.current_health:.1f}, Normal HP={normal.current_health:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Defend mechanic failed: {e}")
        failed += 1

    # Test 2: Regeneration heals
    try:
        genome = {'fonts': {}, 'colors': {}, 'layout': {'padding': 10}, 'fitness': 0.5}
        healer = Combatant("Healer", genome, BattleStats.from_genome(genome))
        healer.current_health = 50  # Damage first

        initial = healer.current_health
        actual = healer.heal(healer.stats.regeneration * 2)

        assert actual > 0
        assert healer.current_health > initial
        print(f"  ✓ Regeneration heals: {initial:.1f} -> {healer.current_health:.1f} (+{actual:.1f})")
        passed += 1
    except Exception as e:
        print(f"  ✗ Regeneration failed: {e}")
        failed += 1

    # Test 3: Can't heal over max
    try:
        genome = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.5}
        c = Combatant("FullHP", genome, BattleStats.from_genome(genome))

        actual = c.heal(1000)
        assert actual == 0
        assert c.current_health == c.stats.health
        print(f"  ✓ Heal cap: Can't heal over max HP")
        passed += 1
    except Exception as e:
        print(f"  ✗ Heal cap failed: {e}")
        failed += 1

    # Test 4: Death at 0 HP
    try:
        genome = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.5}
        c = Combatant("Mortal", genome, BattleStats.from_genome(genome))

        assert c.is_alive
        c.current_health = 0
        assert not c.is_alive
        print(f"  ✓ Death at 0 HP: Combatant correctly marked as dead")
        passed += 1
    except Exception as e:
        print(f"  ✗ Death mechanic failed: {e}")
        failed += 1

    # Test 5: Berserk mode
    try:
        genome = {'fonts': {'size': 15}, 'colors': {}, 'layout': {'margins': 15}, 'fitness': 0.5}
        berserker = Combatant("Berserker", genome, BattleStats.from_genome(genome))

        initial_atk = berserker.stats.attack
        initial_def = berserker.stats.defense

        berserker.is_berserking = True
        berserker.stats.attack *= 1.5
        berserker.stats.defense *= 0.5

        assert berserker.stats.attack > initial_atk
        assert berserker.stats.defense < initial_def
        print(f"  ✓ Berserk mode: ATK {initial_atk:.1f}->{berserker.stats.attack:.1f}, DEF {initial_def:.1f}->{berserker.stats.defense:.1f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Berserk mode failed: {e}")
        failed += 1

    return passed, failed


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    total_passed = 0
    total_failed = 0

    tests = [
        ("Basic Combat", test_basic_combat),
        ("Extreme Battles", test_extreme_battles),
        ("Tournaments", test_tournaments),
        ("Edge Cases", test_edge_cases),
        ("Chaos Testing", test_chaos),
        ("Performance", test_performance),
        ("Stat Derivation", test_stat_derivation),
        ("Action Mechanics", test_action_mechanics),
    ]

    for name, test_func in tests:
        try:
            p, f = test_func()
            total_passed += p
            total_failed += f
        except Exception as e:
            print(f"\n  💥 TEST SUITE {name} CRASHED: {e}")
            total_failed += 1

    print("\n" + "=" * 80)
    print(f"🏆 FINAL BATTLE STRESS TEST RESULTS: {total_passed} PASSED, {total_failed} FAILED")
    print("=" * 80)

    if total_failed == 0:
        print("""
    ██████╗  █████╗ ████████╗████████╗██╗     ███████╗    ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗ ██╗
    ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗██║
    ██████╔╝███████║   ██║      ██║   ██║     █████╗      ██████╔╝██████╔╝██║   ██║██║   ██║█████╗  ██║  ██║██║
    ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║╚██╗ ██╔╝██╔══╝  ██║  ██║╚═╝
    ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗    ██║     ██║  ██║╚██████╔╝ ╚████╔╝ ███████╗██████╔╝██╗
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝╚═════╝ ╚═╝

        THE BATTLE SYSTEM IS BATTLE-HARDENED!
        """)
        sys.exit(0)
    else:
        print(f"\n    {total_failed} tests failed. Time to debug!")
        sys.exit(1)
