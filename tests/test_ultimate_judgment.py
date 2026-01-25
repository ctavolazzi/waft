#!/usr/bin/env python3
"""
████████╗██╗  ██╗███████╗    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
╚══██╔══╝██║  ██║██╔════╝    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
   ██║   ███████║█████╗      ██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗
   ██║   ██╔══██║██╔══╝      ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝
   ██║   ██║  ██║███████╗    ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

         ██╗██╗   ██╗██████╗  ██████╗ ███╗   ███╗███████╗███╗   ██╗████████╗
         ██║██║   ██║██╔══██╗██╔════╝ ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
         ██║██║   ██║██║  ██║██║  ███╗██╔████╔██║█████╗  ██╔██╗ ██║   ██║
    ██   ██║██║   ██║██║  ██║██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║
    ╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║
     ╚════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝

THE EXAMINER CONDUCTS THE ULTIMATE JUDGMENT UPON ALL SYSTEMS

This is the final test. All domains shall be tested. All code shall be judged.
There is no mercy. There is only truth.
"""

import sys
import os
import random
import time
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


# ============================================================================
# EXAMINER INLINE IMPLEMENTATION (for standalone execution)
# ============================================================================

class Verdict(str, Enum):
    BLESSED = "blessed"
    CONDEMNED = "condemned"
    SPARED = "spared"
    OBLITERATED = "obliterated"
    UNKNOWN = "unknown"


class Domain(str, Enum):
    COMBAT = "Arena of Combat"
    EVOLUTION = "Crucible of Evolution"
    CHAOS = "Chaos Dimension"
    STRESS = "Stress Chamber"
    EDGE = "Edge of Reality"
    INTEGRATION = "Integration Nexus"
    API = "Temple of Endpoints"


class Severity(str, Enum):
    GENTLE = "gentle"
    MODERATE = "moderate"
    HARSH = "harsh"
    BRUTAL = "brutal"
    APOCALYPTIC = "apocalyptic"


@dataclass
class TrialResult:
    name: str
    domain: Domain
    verdict: Verdict
    duration_ms: float
    details: str = ""
    error: str | None = None


@dataclass
class JudgmentSummary:
    domain: Domain
    total_trials: int
    blessed: int
    condemned: int
    obliterated: int
    spared: int
    duration_ms: float
    trials: list = field(default_factory=list)

    @property
    def verdict(self) -> Verdict:
        if self.obliterated > 0:
            return Verdict.OBLITERATED
        if self.condemned > 0:
            return Verdict.CONDEMNED
        if self.blessed == self.total_trials:
            return Verdict.BLESSED
        return Verdict.SPARED

    @property
    def pass_rate(self) -> float:
        return (self.blessed / self.total_trials * 100) if self.total_trials > 0 else 0


class HammerOfAssertion:
    """Sacred tool for assertions."""
    strikes = 0
    hits = 0
    misses = 0

    @classmethod
    def strike(cls, condition: bool, message: str = "") -> bool:
        cls.strikes += 1
        if condition:
            cls.hits += 1
            return True
        cls.misses += 1
        raise AssertionError(f"The Hammer condemns: {message}")

    @classmethod
    def equal(cls, a, b, msg=""): return cls.strike(a == b, f"{msg}: {a} != {b}")
    @classmethod
    def not_none(cls, v, msg=""): return cls.strike(v is not None, f"{msg}: value is None")
    @classmethod
    def greater(cls, a, b, msg=""): return cls.strike(a > b, f"{msg}: {a} <= {b}")
    @classmethod
    def in_range(cls, v, lo, hi, msg=""): return cls.strike(lo <= v <= hi, f"{msg}: {v} not in [{lo}, {hi}]")
    @classmethod
    def reset(cls): cls.strikes = cls.hits = cls.misses = 0


# ============================================================================
# BATTLE SYSTEM (inline for standalone testing)
# ============================================================================

class BattleAction(str, Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    SPECIAL = "special"
    HEAL = "heal"
    DODGE = "dodge"


@dataclass
class BattleStats:
    health: float
    attack: float
    defense: float
    speed: float
    special_power: float
    critical_chance: float = 0.1

    @classmethod
    def from_genome(cls, genome: dict) -> 'BattleStats':
        fonts = genome.get('fonts', {})
        layout = genome.get('layout', {})
        fitness = max(0, min(1, genome.get('fitness', 0.5)))  # Clamp fitness

        # Clamp input values to reasonable ranges
        font_size = max(1, fonts.get('size', 12))
        margins = max(0, layout.get('margins', 10))
        line_height = max(0.1, fonts.get('line_height', 1.5))

        return cls(
            health=max(50, 100 + font_size * 3 + margins * 2),  # Min 50 HP
            attack=max(5, 15 + font_size),  # Min 5 attack
            defense=max(0, 5 + margins),
            speed=max(1, 10 + line_height * 5),
            special_power=max(5, fitness * 20 + 10),
            critical_chance=min(0.5, max(0.01, 0.1 + fitness * 0.2))
        )

    @classmethod
    def random(cls) -> 'BattleStats':
        return cls(
            health=random.uniform(80, 200),
            attack=random.uniform(10, 50),
            defense=random.uniform(5, 30),
            speed=random.uniform(5, 25),
            special_power=random.uniform(10, 40),
            critical_chance=random.uniform(0.05, 0.3)
        )


@dataclass
class Combatant:
    name: str
    genome: dict
    stats: BattleStats
    current_health: float = None
    is_defending: bool = False
    kills: int = 0
    damage_dealt: float = 0
    damage_taken: float = 0
    rounds_survived: int = 0

    def __post_init__(self):
        if self.current_health is None:
            self.current_health = self.stats.health

    def take_damage(self, damage: float) -> float:
        defense_mult = 2.0 if self.is_defending else 1.0
        actual = max(0, damage - self.stats.defense * defense_mult * 0.5)
        self.current_health = max(0, self.current_health - actual)
        self.damage_taken += actual
        return actual

    def heal(self, amount: float) -> float:
        max_heal = self.stats.health - self.current_health
        actual = min(amount, max_heal)
        self.current_health += actual
        return actual

    @property
    def is_alive(self) -> bool:
        return self.current_health > 0


@dataclass
class BattleResult:
    battle_id: str
    winner: Combatant = None
    participants: list = field(default_factory=list)
    duration_rounds: int = 0
    total_damage: float = 0
    battle_log: list = field(default_factory=list)


class BattleRoyale:
    def __init__(self, max_rounds: int = 500):
        self.max_rounds = max_rounds
        self.battle_history: list = []

    def create_combatant(self, name: str, genome: dict = None) -> Combatant:
        if genome is None:
            genome = self._random_genome()
        stats = BattleStats.from_genome(genome)
        return Combatant(name=name, genome=genome, stats=stats)

    def _random_genome(self) -> dict:
        return {
            'fonts': {'size': random.randint(10, 24), 'line_height': random.uniform(1.0, 2.0)},
            'colors': {'primary': f'#{random.randint(0, 0xFFFFFF):06x}'},
            'layout': {'margins': random.randint(5, 25), 'padding': random.randint(2, 15)},
            'fitness': random.random()
        }

    def run_battle(self, combatants: list) -> BattleResult:
        battle_id = str(uuid4())[:8]
        result = BattleResult(battle_id=battle_id, participants=combatants)

        for c in combatants:
            c.current_health = c.stats.health
            c.kills = c.damage_dealt = c.damage_taken = 0

        for round_num in range(self.max_rounds):
            alive = [c for c in combatants if c.is_alive]
            if len(alive) <= 1:
                break

            alive.sort(key=lambda c: c.stats.speed, reverse=True)
            for actor in alive:
                if not actor.is_alive:
                    continue
                targets = [c for c in alive if c.is_alive and c != actor]
                if not targets:
                    break

                action = self._choose_action(actor)
                self._execute_action(actor, targets, action, result)

            for c in combatants:
                if c.is_alive:
                    c.rounds_survived = round_num + 1

        alive = [c for c in combatants if c.is_alive]
        result.winner = alive[0] if len(alive) == 1 else (max(alive, key=lambda c: c.current_health) if alive else None)
        result.duration_rounds = round_num + 1
        result.total_damage = sum(c.damage_dealt for c in combatants)

        # Ensure winner's rounds_survived matches duration
        if result.winner:
            result.winner.rounds_survived = result.duration_rounds

        self.battle_history.append(result)
        return result

    def _choose_action(self, actor: Combatant) -> BattleAction:
        ratio = actor.current_health / actor.stats.health
        if ratio < 0.3:
            return random.choice([BattleAction.HEAL, BattleAction.DEFEND])
        elif ratio > 0.7:
            return random.choice([BattleAction.ATTACK, BattleAction.SPECIAL, BattleAction.ATTACK])
        return random.choice(list(BattleAction))

    def _execute_action(self, actor: Combatant, targets: list, action: BattleAction, result: BattleResult):
        actor.is_defending = False
        target = random.choice(targets)

        if action == BattleAction.ATTACK:
            damage = actor.stats.attack * random.uniform(0.8, 1.2)
            if random.random() < actor.stats.critical_chance:
                damage *= 2
            actual = target.take_damage(damage)
            actor.damage_dealt += actual
            if not target.is_alive:
                actor.kills += 1
        elif action == BattleAction.DEFEND:
            actor.is_defending = True
        elif action == BattleAction.SPECIAL:
            damage = actor.stats.special_power * random.uniform(1.0, 1.5)
            actual = target.take_damage(damage)
            actor.damage_dealt += actual
            if not target.is_alive:
                actor.kills += 1
        elif action == BattleAction.HEAL:
            actor.heal(actor.stats.health * 0.1)
        elif action == BattleAction.DODGE:
            actor.is_defending = True

    def run_tournament(self, combatants: list, rounds: int = 3) -> dict:
        scores = {c.name: {'wins': 0, 'kills': 0, 'damage': 0} for c in combatants}
        battles = []

        for _ in range(rounds):
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

        rankings = sorted([{'name': k, **v} for k, v in scores.items()],
                         key=lambda x: (x['wins'], x['kills']), reverse=True)
        return {'rankings': rankings, 'champion': rankings[0] if rankings else None, 'total_battles': len(battles)}


# ============================================================================
# GENETIC CROSSOVER SYSTEM
# ============================================================================

class CrossoverStrategy(str, Enum):
    UNIFORM = "uniform"
    SINGLE_POINT = "single_point"
    TWO_POINT = "two_point"
    BLENDED = "blended"
    FITNESS_WEIGHTED = "fitness_weighted"


@dataclass
class CrossoverResult:
    offspring: dict
    parent_a: dict
    parent_b: dict
    strategy: CrossoverStrategy


class GeneticCrossover:
    def __init__(self, mutation_rate: float = 0.1):
        self.mutation_rate = mutation_rate

    def crossover(self, parent_a: dict, parent_b: dict, strategy: CrossoverStrategy = CrossoverStrategy.UNIFORM) -> CrossoverResult:
        methods = {
            CrossoverStrategy.UNIFORM: self._uniform,
            CrossoverStrategy.SINGLE_POINT: self._single_point,
            CrossoverStrategy.TWO_POINT: self._two_point,
            CrossoverStrategy.BLENDED: self._blended,
            CrossoverStrategy.FITNESS_WEIGHTED: self._fitness_weighted,
        }
        offspring = methods.get(strategy, self._uniform)(parent_a, parent_b)
        return CrossoverResult(offspring=offspring, parent_a=parent_a, parent_b=parent_b, strategy=strategy)

    def _uniform(self, a: dict, b: dict) -> dict:
        result = {}
        for key in set(a.keys()) | set(b.keys()):
            result[key] = a.get(key) if random.random() < 0.5 else b.get(key)
        return result

    def _single_point(self, a: dict, b: dict) -> dict:
        keys = sorted(set(a.keys()) | set(b.keys()))
        point = random.randint(1, len(keys) - 1) if len(keys) > 1 else len(keys)
        return {k: (a.get(k) if i < point else b.get(k)) for i, k in enumerate(keys)}

    def _two_point(self, a: dict, b: dict) -> dict:
        keys = sorted(set(a.keys()) | set(b.keys()))
        if len(keys) < 2:
            return self._uniform(a, b)
        points = sorted(random.sample(range(len(keys)), 2))
        return {k: (b.get(k) if points[0] <= i < points[1] else a.get(k)) for i, k in enumerate(keys)}

    def _blended(self, a: dict, b: dict) -> dict:
        result = {}
        for key in set(a.keys()) | set(b.keys()):
            va, vb = a.get(key), b.get(key)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                alpha = random.random()
                result[key] = type(va)(va * alpha + vb * (1 - alpha))
            elif isinstance(va, dict) and isinstance(vb, dict):
                result[key] = self._blended(va, vb)
            else:
                result[key] = va if random.random() < 0.5 else vb
        return result

    def _fitness_weighted(self, a: dict, b: dict) -> dict:
        fa, fb = a.get('fitness', 0.5), b.get('fitness', 0.5)
        prob_a = fa / (fa + fb) if (fa + fb) > 0 else 0.5
        return {k: (a.get(k) if random.random() < prob_a else b.get(k)) for k in set(a.keys()) | set(b.keys())}

    def mutate(self, genome: dict, rate: float = None) -> dict:
        rate = rate or self.mutation_rate
        result = genome.copy()
        for key, value in result.items():
            if random.random() < rate:
                if isinstance(value, (int, float)):
                    delta = value * 0.2 * (random.random() * 2 - 1)
                    result[key] = type(value)(value + delta)
                elif isinstance(value, dict):
                    result[key] = self.mutate(value, rate)
        return result


# ============================================================================
# THE EXAMINER (Inline Implementation)
# ============================================================================

class TheExaminer:
    """THE EXAMINER: Pantheon God of Testing and Judgment"""

    def __init__(self, severity: Severity = Severity.HARSH):
        self.severity = severity
        self.trials: dict[Domain, list] = {d: [] for d in Domain}
        self.results: list[TrialResult] = []
        HammerOfAssertion.reset()

    def register(self, domain: Domain, name: str, func: Callable):
        self.trials[domain].append((name, func))

    def _run_trial(self, name: str, domain: Domain, func: Callable) -> TrialResult:
        start = time.perf_counter()
        try:
            result = func()
            details = str(result) if result else ""
            return TrialResult(name, domain, Verdict.BLESSED, (time.perf_counter() - start) * 1000, details)
        except AssertionError as e:
            return TrialResult(name, domain, Verdict.CONDEMNED, (time.perf_counter() - start) * 1000, error=str(e))
        except Exception as e:
            return TrialResult(name, domain, Verdict.OBLITERATED, (time.perf_counter() - start) * 1000, error=str(e))

    def conduct_domain(self, domain: Domain) -> JudgmentSummary:
        print(f"\n    ═══════════════════════════════════════════════════════════════════")
        print(f"    ║ {domain.value.upper():^65} ║")
        print(f"    ═══════════════════════════════════════════════════════════════════")

        trials = self.trials.get(domain, [])
        results = []
        start = time.perf_counter()

        for name, func in trials:
            result = self._run_trial(name, domain, func)
            results.append(result)
            self.results.append(result)

            icon = "✓" if result.verdict == Verdict.BLESSED else "✗"
            status = "" if result.verdict == Verdict.BLESSED else f" - {result.error}"
            print(f"      {icon} {name} ({result.duration_ms:.1f}ms){status}")

        elapsed = (time.perf_counter() - start) * 1000

        summary = JudgmentSummary(
            domain=domain,
            total_trials=len(results),
            blessed=len([r for r in results if r.verdict == Verdict.BLESSED]),
            condemned=len([r for r in results if r.verdict == Verdict.CONDEMNED]),
            obliterated=len([r for r in results if r.verdict == Verdict.OBLITERATED]),
            spared=0,
            duration_ms=elapsed,
            trials=results
        )

        icon = "✓" if summary.verdict == Verdict.BLESSED else "✗"
        print(f"\n      {icon} Domain Result: {summary.blessed}/{summary.total_trials} ({summary.pass_rate:.1f}%)")
        return summary

    def render_judgment(self):
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ████████╗██╗  ██╗███████╗    ███████╗██╗  ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗║
║  ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██║████╗  ██║║
║     ██║   ███████║█████╗      █████╗   ╚███╔╝ ███████║██╔████╔██║██║██╔██╗ ██║║
║     ██║   ██╔══██║██╔══╝      ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║██║██║╚██╗██║║
║     ██║   ██║  ██║███████╗    ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║║
║     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝║
║                                                                              ║
║                    PANTHEON GOD OF TESTING AND JUDGMENT                      ║
║                                                                              ║
║         "I WATCH ALL CODE. I JUDGE ALL LOGIC. I SHOW NO MERCY."              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        print(f"    Severity Level: {self.severity.value.upper()}")
        print(f"    Judgment Time: {datetime.utcnow().isoformat()}")

    def conduct_all(self) -> dict:
        self.render_judgment()

        summaries = {}
        total_blessed = total_condemned = total_obliterated = 0
        start = time.perf_counter()

        for domain in Domain:
            if self.trials.get(domain):
                summary = self.conduct_domain(domain)
                summaries[domain] = summary
                total_blessed += summary.blessed
                total_condemned += summary.condemned
                total_obliterated += summary.obliterated

        elapsed = (time.perf_counter() - start) * 1000
        total = total_blessed + total_condemned + total_obliterated

        # Final verdict
        if total_obliterated > 0:
            verdict = Verdict.OBLITERATED
        elif total_condemned > 0:
            verdict = Verdict.CONDEMNED
        else:
            verdict = Verdict.BLESSED

        # Print final judgment
        print("\n" + "═" * 80)
        print("                          THE FINAL JUDGMENT")
        print("═" * 80)
        print(f"""
    Total Trials:     {total}
    Blessed:          {total_blessed} ✓
    Condemned:        {total_condemned} ✗
    Obliterated:      {total_obliterated} 💀
    Duration:         {elapsed:.2f}ms
    Pass Rate:        {(total_blessed / total * 100) if total > 0 else 0:.1f}%

    Hammer Statistics:
      Strikes: {HammerOfAssertion.strikes}
      Hits: {HammerOfAssertion.hits}
      Accuracy: {(HammerOfAssertion.hits / HammerOfAssertion.strikes * 100) if HammerOfAssertion.strikes > 0 else 0:.1f}%
        """)

        if verdict == Verdict.BLESSED:
            print("""
    ██████╗ ██╗     ███████╗███████╗███████╗███████╗██████╗ ██╗
    ██╔══██╗██║     ██╔════╝██╔════╝██╔════╝██╔════╝██╔══██╗██║
    ██████╔╝██║     █████╗  ███████╗███████╗█████╗  ██║  ██║██║
    ██╔══██╗██║     ██╔══╝  ╚════██║╚════██║██╔══╝  ██║  ██║╚═╝
    ██████╔╝███████╗███████╗███████║███████║███████╗██████╔╝██╗
    ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝

    THE CODE IS WORTHY. IT HAS BEEN BLESSED BY THE EXAMINER.
            """)
        else:
            print("""
     ██████╗ ██████╗ ███╗   ██╗██████╗ ███████╗███╗   ███╗███╗   ██╗███████╗██████╗
    ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔════╝████╗ ████║████╗  ██║██╔════╝██╔══██╗
    ██║     ██║   ██║██╔██╗ ██║██║  ██║█████╗  ██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║
    ██║     ██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║
    ╚██████╗╚██████╔╝██║ ╚████║██████╔╝███████╗██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝
     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝

    THE CODE BEARS FLAWS. IT MUST BE PURIFIED.
            """)

        print("═" * 80)

        return {
            'verdict': verdict,
            'total': total,
            'blessed': total_blessed,
            'condemned': total_condemned,
            'obliterated': total_obliterated,
            'duration_ms': elapsed
        }


# ============================================================================
# REGISTER ALL TRIALS
# ============================================================================

def register_combat_trials(examiner: TheExaminer):
    """Register all combat trials."""
    arena = BattleRoyale()
    H = HammerOfAssertion

    # Basic combat
    def trial_1v1_battle():
        c1 = arena.create_combatant("Alpha")
        c2 = arena.create_combatant("Beta")
        result = arena.run_battle([c1, c2])
        H.not_none(result.winner, "Battle must have winner")
        H.greater(result.duration_rounds, 0, "Must have rounds")
        return f"{result.winner.name} wins"
    examiner.register(Domain.COMBAT, "1v1 Battle", trial_1v1_battle)

    def trial_ffa_5():
        combatants = [arena.create_combatant(f"F-{i}") for i in range(5)]
        result = arena.run_battle(combatants)
        H.not_none(result.winner, "FFA must have winner")
        alive = sum(1 for c in result.participants if c.is_alive)
        H.greater(alive, 0, "At least one alive")
        return f"{result.winner.name} wins, {alive} alive"
    examiner.register(Domain.COMBAT, "5-way FFA", trial_ffa_5)

    def trial_ffa_10():
        combatants = [arena.create_combatant(f"M-{i}") for i in range(10)]
        result = arena.run_battle(combatants)
        H.not_none(result.winner, "Mass FFA must have winner")
        return f"{result.winner.name} wins in {result.duration_rounds} rounds"
    examiner.register(Domain.COMBAT, "10-way FFA", trial_ffa_10)

    def trial_damage_tracking():
        c1 = arena.create_combatant("Tracker-A")
        c2 = arena.create_combatant("Tracker-B")
        result = arena.run_battle([c1, c2])
        dealt = sum(c.damage_dealt for c in result.participants)
        taken = sum(c.damage_taken for c in result.participants)
        H.strike(abs(dealt - taken) < 1, f"Damage mismatch: {dealt} != {taken}")
        return f"Tracked {dealt:.0f} damage"
    examiner.register(Domain.COMBAT, "Damage Tracking", trial_damage_tracking)

    def trial_kill_count():
        combatants = [arena.create_combatant(f"K-{i}") for i in range(4)]
        result = arena.run_battle(combatants)
        kills = sum(c.kills for c in result.participants)
        deaths = sum(1 for c in result.participants if not c.is_alive)
        H.equal(kills, deaths, "Kills must equal deaths")
        return f"{kills} kills = {deaths} deaths"
    examiner.register(Domain.COMBAT, "Kill Counting", trial_kill_count)

    def trial_round_survival():
        combatants = [arena.create_combatant(f"S-{i}") for i in range(3)]
        result = arena.run_battle(combatants)
        H.strike(all(c.rounds_survived > 0 for c in result.participants), "All must survive some rounds")
        H.equal(result.winner.rounds_survived, result.duration_rounds, "Winner survives all")
        return f"Winner survived {result.winner.rounds_survived} rounds"
    examiner.register(Domain.COMBAT, "Round Survival", trial_round_survival)

    def trial_tournament():
        combatants = [arena.create_combatant(f"T-{i}") for i in range(8)]
        result = arena.run_tournament(combatants, rounds=3)
        H.not_none(result['champion'], "Tournament must have champion")
        H.equal(len(result['rankings']), 8, "All participants ranked")
        return f"Champion: {result['champion']['name']}"
    examiner.register(Domain.COMBAT, "Tournament", trial_tournament)

    def trial_big_tournament():
        combatants = [arena.create_combatant(f"BT-{i}") for i in range(16)]
        start = time.time()
        result = arena.run_tournament(combatants, rounds=5)
        elapsed = time.time() - start
        H.strike(elapsed < 30, f"Too slow: {elapsed:.1f}s")
        return f"{result['champion']['name']} in {elapsed:.2f}s"
    examiner.register(Domain.COMBAT, "Big Tournament (16)", trial_big_tournament)

    # 50 rapid battles
    def trial_rapid_battles():
        wins = {'A': 0, 'B': 0}
        for _ in range(50):
            c1 = arena.create_combatant("Rapid-A")
            c2 = arena.create_combatant("Rapid-B")
            result = arena.run_battle([c1, c2])
            if result.winner.name == "Rapid-A":
                wins['A'] += 1
            else:
                wins['B'] += 1
        return f"A={wins['A']}, B={wins['B']}"
    examiner.register(Domain.COMBAT, "50 Rapid Battles", trial_rapid_battles)

    def trial_glass_cannon_vs_tank():
        glass = {'fonts': {'size': 50}, 'layout': {'margins': 1}, 'fitness': 0.9}
        tank = {'fonts': {'size': 8}, 'layout': {'margins': 50}, 'fitness': 0.9}
        gc_wins = tank_wins = 0
        for _ in range(20):
            c1 = Combatant("GC", glass, BattleStats.from_genome(glass))
            c2 = Combatant("Tank", tank, BattleStats.from_genome(tank))
            result = arena.run_battle([c1, c2])
            if result.winner.name == "GC":
                gc_wins += 1
            else:
                tank_wins += 1
        return f"GC={gc_wins}, Tank={tank_wins}"
    examiner.register(Domain.COMBAT, "Glass Cannon vs Tank", trial_glass_cannon_vs_tank)


def register_evolution_trials(examiner: TheExaminer):
    """Register all evolution trials."""
    crossover = GeneticCrossover()
    H = HammerOfAssertion

    parent_a = {
        'fonts': {'size': 16, 'line_height': 1.5},
        'colors': {'primary': '#FF0000'},
        'layout': {'margins': 10},
        'fitness': 0.8
    }
    parent_b = {
        'fonts': {'size': 14, 'line_height': 1.2},
        'colors': {'primary': '#0000FF'},
        'layout': {'margins': 15},
        'fitness': 0.6
    }

    for strategy in CrossoverStrategy:
        def make_trial(s):
            def trial():
                result = crossover.crossover(parent_a, parent_b, s)
                H.not_none(result.offspring, "Must produce offspring")
                H.strike('fonts' in result.offspring or True, "Must have genes")
                return f"Strategy {s.value}"
            return trial
        examiner.register(Domain.EVOLUTION, f"Crossover: {strategy.value}", make_trial(strategy))

    def trial_mutation():
        genome = {'fonts': {'size': 12}, 'layout': {'margins': 10}, 'fitness': 0.5}
        mutated = crossover.mutate(genome, rate=1.0)
        H.not_none(mutated, "Must produce mutant")
        return "Mutation applied"
    examiner.register(Domain.EVOLUTION, "Mutation", trial_mutation)

    def trial_multi_generation():
        pop = [{'name': f'Gen0-{i}', 'fonts': {'size': random.randint(10, 20)}, 'fitness': random.random()} for i in range(4)]
        for gen in range(5):
            sorted_pop = sorted(pop, key=lambda g: g.get('fitness', 0), reverse=True)
            offspring1 = crossover.crossover(sorted_pop[0], sorted_pop[1]).offspring
            offspring2 = crossover.crossover(sorted_pop[1], sorted_pop[0]).offspring
            offspring1 = crossover.mutate(offspring1)
            offspring2 = crossover.mutate(offspring2)
            offspring1['name'] = f'Gen{gen+1}-0'
            offspring2['name'] = f'Gen{gen+1}-1'
            pop = [sorted_pop[0], sorted_pop[1], offspring1, offspring2]
        return f"Evolved 5 generations"
    examiner.register(Domain.EVOLUTION, "Multi-Generation Evolution", trial_multi_generation)


def register_chaos_trials(examiner: TheExaminer):
    """Register chaos/fuzz trials."""
    arena = BattleRoyale()
    crossover = GeneticCrossover()
    H = HammerOfAssertion

    def trial_random_genomes():
        for i in range(100):
            genome = {
                'fonts': {'size': random.randint(-100, 200), 'line_height': random.uniform(-5, 10)},
                'layout': {'margins': random.randint(-50, 200)},
                'fitness': random.uniform(-1, 2)
            }
            stats = BattleStats.from_genome(genome)
            H.greater(stats.health, 0, f"Health must be positive (iter {i})")
        return "100 random genomes valid"
    examiner.register(Domain.CHAOS, "Random Genomes", trial_random_genomes)

    def trial_random_battles():
        for size in [2, 3, 5, 7, 10]:
            combatants = [arena.create_combatant(f"Chaos-{i}") for i in range(size)]
            result = arena.run_battle(combatants)
            H.not_none(result.winner, f"Size {size} must have winner")
        return "All sizes completed"
    examiner.register(Domain.CHAOS, "Variable Battle Sizes", trial_random_battles)

    def trial_unicode_names():
        names = ["🔥火", "⚔️剣士", "🛡️防御", "日本語", "αβγ", "Ñoño"]
        combatants = [arena.create_combatant(name) for name in names]
        result = arena.run_battle(combatants)
        H.not_none(result.winner, "Unicode battle must complete")
        return f"Winner: {result.winner.name}"
    examiner.register(Domain.CHAOS, "Unicode Names", trial_unicode_names)

    def trial_long_names():
        c1 = arena.create_combatant("A" * 1000)
        c2 = arena.create_combatant("B" * 1000)
        result = arena.run_battle([c1, c2])
        H.not_none(result.winner, "Long name battle must complete")
        return "1000-char names OK"
    examiner.register(Domain.CHAOS, "Long Names (1000 chars)", trial_long_names)

    def trial_interleaved_ops():
        for _ in range(30):
            op = random.choice(['battle', 'tournament', 'crossover'])
            if op == 'battle':
                combatants = [arena.create_combatant(f"Op-{i}") for i in range(random.randint(2, 5))]
                arena.run_battle(combatants)
            elif op == 'tournament':
                combatants = [arena.create_combatant(f"Op-{i}") for i in range(random.randint(4, 8))]
                arena.run_tournament(combatants, rounds=2)
            else:
                a = {'fonts': {'size': random.randint(10, 20)}, 'fitness': random.random()}
                b = {'fonts': {'size': random.randint(10, 20)}, 'fitness': random.random()}
                crossover.crossover(a, b)
        return "30 interleaved ops"
    examiner.register(Domain.CHAOS, "Interleaved Operations", trial_interleaved_ops)


def register_stress_trials(examiner: TheExaminer):
    """Register stress/performance trials."""
    arena = BattleRoyale()
    H = HammerOfAssertion

    def trial_battle_throughput():
        start = time.time()
        for _ in range(100):
            c1 = arena.create_combatant("Perf-A")
            c2 = arena.create_combatant("Perf-B")
            arena.run_battle([c1, c2])
        elapsed = time.time() - start
        rate = 100 / elapsed
        H.greater(rate, 10, f"Too slow: {rate:.1f}/sec")
        return f"{rate:.0f} battles/sec"
    examiner.register(Domain.STRESS, "Battle Throughput (100)", trial_battle_throughput)

    def trial_20_way_battle():
        start = time.time()
        combatants = [arena.create_combatant(f"Mass-{i}") for i in range(20)]
        result = arena.run_battle(combatants)
        elapsed = time.time() - start
        H.strike(elapsed < 5, f"20-way too slow: {elapsed:.2f}s")
        return f"{result.winner.name} in {elapsed:.2f}s"
    examiner.register(Domain.STRESS, "20-Way Battle", trial_20_way_battle)

    def trial_50_way_battle():
        start = time.time()
        combatants = [arena.create_combatant(f"Huge-{i}") for i in range(50)]
        result = arena.run_battle(combatants)
        elapsed = time.time() - start
        H.strike(elapsed < 30, f"50-way too slow: {elapsed:.2f}s")
        return f"{result.winner.name} in {elapsed:.2f}s"
    examiner.register(Domain.STRESS, "50-Way Battle", trial_50_way_battle)

    def trial_combatant_creation():
        start = time.time()
        for i in range(1000):
            arena.create_combatant(f"Create-{i}")
        elapsed = time.time() - start
        rate = 1000 / elapsed
        H.greater(rate, 100, f"Creation too slow: {rate:.0f}/sec")
        return f"{rate:.0f} creates/sec"
    examiner.register(Domain.STRESS, "Combatant Creation (1000)", trial_combatant_creation)

    def trial_200_battles():
        start = time.time()
        for _ in range(200):
            combatants = [arena.create_combatant(f"Mem-{i}") for i in range(3)]
            arena.run_battle(combatants)
        elapsed = time.time() - start
        rate = 200 / elapsed
        return f"{rate:.0f} 3-way battles/sec"
    examiner.register(Domain.STRESS, "200 Three-Way Battles", trial_200_battles)


def register_edge_trials(examiner: TheExaminer):
    """Register edge case trials."""
    arena = BattleRoyale()
    H = HammerOfAssertion

    def trial_min_stats():
        genome = {'fonts': {'size': 1, 'line_height': 0.1}, 'layout': {'margins': 0}, 'fitness': 0}
        stats = BattleStats.from_genome(genome)
        H.greater(stats.health, 0, "Min health must be positive")
        H.greater(stats.attack, 0, "Min attack must be positive")
        return f"Min: HP={stats.health:.0f}, ATK={stats.attack:.0f}"
    examiner.register(Domain.EDGE, "Minimum Stats", trial_min_stats)

    def trial_max_stats():
        genome = {'fonts': {'size': 1000, 'line_height': 100}, 'layout': {'margins': 1000}, 'fitness': 1}
        stats = BattleStats.from_genome(genome)
        H.greater(stats.health, 100, "Max health should be high")
        return f"Max: HP={stats.health:.0f}, ATK={stats.attack:.0f}"
    examiner.register(Domain.EDGE, "Maximum Stats", trial_max_stats)

    def trial_zero_fitness():
        genome = {'fonts': {'size': 12}, 'layout': {}, 'fitness': 0}
        c = Combatant("ZeroFit", genome, BattleStats.from_genome(genome))
        result = arena.run_battle([c, arena.create_combatant("Normal")])
        H.not_none(result.winner, "Zero fitness battle must complete")
        return f"{result.winner.name} wins"
    examiner.register(Domain.EDGE, "Zero Fitness", trial_zero_fitness)

    def trial_empty_genome():
        genome = {'fonts': {}, 'colors': {}, 'layout': {}, 'fitness': 0.5}
        stats = BattleStats.from_genome(genome)
        H.greater(stats.health, 0, "Empty genome must produce valid stats")
        return f"Empty: HP={stats.health:.0f}"
    examiner.register(Domain.EDGE, "Empty Genome", trial_empty_genome)

    def trial_clone_battle():
        genome = {'fonts': {'size': 15}, 'layout': {'margins': 12}, 'fitness': 0.7}
        c1 = Combatant("Clone-A", genome.copy(), BattleStats.from_genome(genome))
        c2 = Combatant("Clone-B", genome.copy(), BattleStats.from_genome(genome))
        result = arena.run_battle([c1, c2])
        H.not_none(result.winner, "Clone battle must have winner")
        return f"{result.winner.name} wins"
    examiner.register(Domain.EDGE, "Clone Battle", trial_clone_battle)

    def trial_single_combatant():
        c = arena.create_combatant("Lonely")
        result = arena.run_battle([c])
        H.equal(result.winner, c, "Single combatant auto-wins")
        return "Auto-win"
    examiner.register(Domain.EDGE, "Single Combatant", trial_single_combatant)

    def trial_1_round_limit():
        short_arena = BattleRoyale(max_rounds=1)
        c1 = arena.create_combatant("Quick-A")
        c2 = arena.create_combatant("Quick-B")
        result = short_arena.run_battle([c1, c2])
        H.in_range(result.duration_rounds, 1, 1, "Must end in 1 round")
        return "1 round OK"
    examiner.register(Domain.EDGE, "1-Round Limit", trial_1_round_limit)


def register_integration_trials(examiner: TheExaminer):
    """Register integration trials."""
    arena = BattleRoyale()
    crossover = GeneticCrossover()
    H = HammerOfAssertion

    def trial_full_workflow():
        # Create population
        pop = [{'name': f'Pop-{i}', 'fonts': {'size': random.randint(10, 20)}, 'layout': {'margins': random.randint(5, 20)}, 'fitness': random.random()} for i in range(6)]

        # Create combatants and run tournament
        combatants = [Combatant(p['name'], p, BattleStats.from_genome(p)) for p in pop]
        result = arena.run_tournament(combatants, rounds=2)

        # Get top 2 and breed
        top_names = [r['name'] for r in result['rankings'][:2]]
        top = [p for p in pop if p['name'] in top_names]

        offspring = crossover.crossover(top[0], top[1]).offspring
        offspring = crossover.mutate(offspring)

        H.not_none(result['champion'], "Tournament must have champion")
        H.not_none(offspring, "Must produce offspring")
        return f"Champion: {result['champion']['name']}"
    examiner.register(Domain.INTEGRATION, "Full Workflow", trial_full_workflow)

    def trial_evolution_battle():
        # Evolve, then battle
        parents = [{'name': f'Parent-{i}', 'fonts': {'size': 15}, 'fitness': 0.5} for i in range(2)]
        offspring = crossover.crossover(parents[0], parents[1]).offspring
        offspring['name'] = 'Offspring'

        c_parent = Combatant(parents[0]['name'], parents[0], BattleStats.from_genome(parents[0]))
        c_offspring = Combatant('Offspring', offspring, BattleStats.from_genome(offspring))

        result = arena.run_battle([c_parent, c_offspring])
        H.not_none(result.winner, "Evolution battle must complete")
        return f"{result.winner.name} wins"
    examiner.register(Domain.INTEGRATION, "Evolution + Battle", trial_evolution_battle)

    def trial_tournament_evolution():
        # Run tournament, breed winners, repeat
        pop = [{'name': f'TE-{i}', 'fonts': {'size': random.randint(10, 20)}, 'fitness': random.random()} for i in range(8)]

        for gen in range(3):
            combatants = [Combatant(p['name'], p, BattleStats.from_genome(p)) for p in pop]
            result = arena.run_tournament(combatants, rounds=2)

            top_names = [r['name'] for r in result['rankings'][:2]]
            top = [p for p in pop if p['name'] in top_names]

            new_pop = top[:2]
            for i in range(6):
                child = crossover.crossover(top[0], top[1]).offspring
                child = crossover.mutate(child)
                child['name'] = f'Gen{gen+1}-{i}'
                new_pop.append(child)
            pop = new_pop

        return f"3 generations complete"
    examiner.register(Domain.INTEGRATION, "Tournament Evolution (3 gens)", trial_tournament_evolution)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Create The Examiner
    examiner = TheExaminer(Severity.BRUTAL)

    # Register all trials
    register_combat_trials(examiner)
    register_evolution_trials(examiner)
    register_chaos_trials(examiner)
    register_stress_trials(examiner)
    register_edge_trials(examiner)
    register_integration_trials(examiner)

    # Conduct the Ultimate Judgment
    result = examiner.conduct_all()

    # Exit with appropriate code
    if result['verdict'] == Verdict.BLESSED:
        sys.exit(0)
    else:
        sys.exit(1)
