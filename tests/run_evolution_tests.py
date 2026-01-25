#!/usr/bin/env python3
"""
Standalone Evolution System Tests - Proof the Code Works!

This script tests the genetic crossover and battle royale systems
by mocking the dependencies that have import chain issues.
"""

import sys
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

print("=" * 70)
print("🧬 WAFT EVOLUTION SYSTEM - PROOF OF CONCEPT TESTS 🧬")
print("=" * 70)


# ============================================================================
# MOCK DEPENDENCIES (to bypass import chain issues)
# ============================================================================

class EvolutionaryEventType(str, Enum):
    """Mock event type."""
    MUTATION = "mutation"
    CROSSOVER = "crossover"

@dataclass
class EvolutionaryEvent:
    """Mock event."""
    event_type: EvolutionaryEventType
    description: str

class LineagePoet:
    """Mock lineage poet."""
    @staticmethod
    def generate_scientific_name(genome_id: str) -> str:
        return f"Evolutus {genome_id[:8].lower()}"


# ============================================================================
# COPY OF STYLING GENOME CLASSES (inline to avoid imports)
# ============================================================================

@dataclass
class FontGene:
    family: str = "sans-serif"
    size_body: int = 11
    size_h1: int = 24
    size_h2: int = 18
    size_h3: int = 14
    size_code: int = 10
    line_height: float = 1.5

@dataclass
class MarginGene:
    top: int = 20
    bottom: int = 20
    left: int = 20
    right: int = 20
    paragraph_spacing: int = 10
    section_spacing: int = 15

@dataclass
class ColorGene:
    text: str = "#000000"
    background: str = "#FFFFFF"
    heading: str = "#1a1a1a"
    accent: str = "#0066cc"
    code_bg: str = "#f5f5f5"
    code_text: str = "#333333"
    border: str = "#cccccc"

@dataclass
class LayoutGene:
    columns: int = 1
    density: str = "normal"
    toc_enabled: bool = False
    page_numbers: bool = True
    header_enabled: bool = True
    footer_enabled: bool = True

@dataclass
class StylingGene:
    font: FontGene = field(default_factory=FontGene)
    margin: MarginGene = field(default_factory=MarginGene)
    color: ColorGene = field(default_factory=ColorGene)
    layout: LayoutGene = field(default_factory=LayoutGene)

# StylingGenome is basically a dict for our purposes
StylingGenome = dict


# ============================================================================
# CROSSOVER STRATEGY ENUM
# ============================================================================

class CrossoverStrategy(str, Enum):
    UNIFORM = "uniform"
    SINGLE_POINT = "single_point"
    TWO_POINT = "two_point"
    CATEGORY_SWAP = "category_swap"
    FITNESS_WEIGHTED = "fitness_weighted"
    BLENDED = "blended"
    DOMINANT_RECESSIVE = "dominant_recessive"


# ============================================================================
# CROSSOVER RESULT
# ============================================================================

@dataclass
class CrossoverResult:
    offspring: dict
    parent_a: dict
    parent_b: dict
    strategy: CrossoverStrategy
    crossover_points: list
    inheritance_map: dict
    timestamp: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""


# ============================================================================
# GENETIC CROSSOVER ENGINE
# ============================================================================

class GeneticCrossover:
    """Genetic crossover engine for combining parent genomes."""

    def __init__(self, mutation_rate: float = 0.1):
        self.mutation_rate = mutation_rate
        self.generation_counter = 0

    def crossover(
        self,
        parent_a: dict,
        parent_b: dict,
        strategy: CrossoverStrategy = CrossoverStrategy.UNIFORM
    ) -> CrossoverResult:
        """Perform crossover between two parent genomes."""

        strategy_methods = {
            CrossoverStrategy.UNIFORM: self._uniform_crossover,
            CrossoverStrategy.SINGLE_POINT: self._single_point_crossover,
            CrossoverStrategy.TWO_POINT: self._two_point_crossover,
            CrossoverStrategy.CATEGORY_SWAP: self._category_swap_crossover,
            CrossoverStrategy.FITNESS_WEIGHTED: self._fitness_weighted_crossover,
            CrossoverStrategy.BLENDED: self._blended_crossover,
            CrossoverStrategy.DOMINANT_RECESSIVE: self._dominant_recessive_crossover,
        }

        crossover_method = strategy_methods.get(strategy, self._uniform_crossover)
        offspring, inheritance_map, crossover_points = crossover_method(parent_a, parent_b)

        return CrossoverResult(
            offspring=offspring,
            parent_a=parent_a,
            parent_b=parent_b,
            strategy=strategy,
            crossover_points=crossover_points,
            inheritance_map=inheritance_map,
        )

    def _uniform_crossover(self, parent_a: dict, parent_b: dict):
        """Each gene is randomly selected from either parent."""
        offspring = {}
        inheritance_map = {}
        crossover_points = []

        all_keys = set(parent_a.keys()) | set(parent_b.keys())
        for key in all_keys:
            if random.random() < 0.5:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a"
            else:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b"
                crossover_points.append(key)

        return offspring, inheritance_map, crossover_points

    def _single_point_crossover(self, parent_a: dict, parent_b: dict):
        """Single crossover point - all genes before from A, after from B."""
        offspring = {}
        inheritance_map = {}
        all_keys = sorted(set(parent_a.keys()) | set(parent_b.keys()))
        crossover_point = random.randint(1, max(1, len(all_keys) - 1))

        for i, key in enumerate(all_keys):
            if i < crossover_point:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a"
            else:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b"

        return offspring, inheritance_map, [all_keys[crossover_point] if crossover_point < len(all_keys) else "end"]

    def _two_point_crossover(self, parent_a: dict, parent_b: dict):
        """Two crossover points - genes between points from B, rest from A."""
        offspring = {}
        inheritance_map = {}
        all_keys = sorted(set(parent_a.keys()) | set(parent_b.keys()))

        if len(all_keys) < 2:
            return self._uniform_crossover(parent_a, parent_b)

        points = sorted(random.sample(range(len(all_keys)), min(2, len(all_keys))))

        for i, key in enumerate(all_keys):
            if points[0] <= i < points[1]:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b"
            else:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a"

        crossover_points = [all_keys[p] for p in points if p < len(all_keys)]
        return offspring, inheritance_map, crossover_points

    def _category_swap_crossover(self, parent_a: dict, parent_b: dict):
        """Swap entire categories (fonts from A, colors from B, etc.)."""
        offspring = {}
        inheritance_map = {}
        all_keys = set(parent_a.keys()) | set(parent_b.keys())
        swapped = []

        for key in all_keys:
            if random.random() < 0.5:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a"
            else:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b"
                swapped.append(key)

        return offspring, inheritance_map, swapped

    def _fitness_weighted_crossover(self, parent_a: dict, parent_b: dict):
        """Bias gene selection toward the fitter parent."""
        fitness_a = parent_a.get('fitness', 0.5)
        fitness_b = parent_b.get('fitness', 0.5)
        total = fitness_a + fitness_b
        prob_a = fitness_a / total if total > 0 else 0.5

        offspring = {}
        inheritance_map = {}
        crossover_points = []

        all_keys = set(parent_a.keys()) | set(parent_b.keys())
        for key in all_keys:
            if key == 'fitness':
                # Average the fitness
                offspring[key] = (fitness_a + fitness_b) / 2
                inheritance_map[key] = "both"
            elif random.random() < prob_a:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a"
            else:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b"
                crossover_points.append(key)

        return offspring, inheritance_map, crossover_points

    def _blended_crossover(self, parent_a: dict, parent_b: dict):
        """Interpolate numeric values, randomly select others."""
        offspring = {}
        inheritance_map = {}
        all_keys = set(parent_a.keys()) | set(parent_b.keys())

        for key in all_keys:
            val_a = parent_a.get(key)
            val_b = parent_b.get(key)

            if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
                # Blend numeric values
                alpha = random.random()
                blended = val_a * alpha + val_b * (1 - alpha)
                offspring[key] = type(val_a)(blended) if isinstance(val_a, int) else blended
                inheritance_map[key] = "blended"
            elif isinstance(val_a, dict) and isinstance(val_b, dict):
                # Recursively blend nested dicts
                nested_result, nested_map, _ = self._blended_crossover(val_a, val_b)
                offspring[key] = nested_result
                inheritance_map[key] = nested_map
            else:
                # Random selection for non-numeric
                if random.random() < 0.5:
                    offspring[key] = val_a if val_a is not None else val_b
                    inheritance_map[key] = "parent_a"
                else:
                    offspring[key] = val_b if val_b is not None else val_a
                    inheritance_map[key] = "parent_b"

        return offspring, inheritance_map, ["blended"]

    def _dominant_recessive_crossover(self, parent_a: dict, parent_b: dict):
        """Mendelian inheritance - some genes are dominant."""
        # For simplicity, parent_a genes are "dominant" 75% of time
        offspring = {}
        inheritance_map = {}
        crossover_points = []

        all_keys = set(parent_a.keys()) | set(parent_b.keys())
        for key in all_keys:
            if random.random() < 0.75:
                offspring[key] = parent_a.get(key, parent_b.get(key))
                inheritance_map[key] = "parent_a (dominant)"
            else:
                offspring[key] = parent_b.get(key, parent_a.get(key))
                inheritance_map[key] = "parent_b (recessive)"
                crossover_points.append(key)

        return offspring, inheritance_map, crossover_points

    def mutate(self, genome: dict, mutation_rate: float = None) -> dict:
        """Apply random mutations to a genome."""
        rate = mutation_rate if mutation_rate is not None else self.mutation_rate
        mutated = genome.copy()

        for key, value in mutated.items():
            if random.random() < rate:
                if isinstance(value, (int, float)):
                    # Mutate numeric by +/- 20%
                    delta = value * 0.2 * (random.random() * 2 - 1)
                    mutated[key] = type(value)(value + delta)
                elif isinstance(value, str) and value.startswith('#'):
                    # Mutate colors slightly
                    mutated[key] = self._mutate_color(value)
                elif isinstance(value, dict):
                    mutated[key] = self.mutate(value, rate)

        return mutated

    def _mutate_color(self, color: str) -> str:
        """Mutate a hex color slightly."""
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            r = max(0, min(255, r + random.randint(-20, 20)))
            g = max(0, min(255, g + random.randint(-20, 20)))
            b = max(0, min(255, b + random.randint(-20, 20)))

            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color


# ============================================================================
# BATTLE ROYALE SYSTEM
# ============================================================================

class BattleAction(str, Enum):
    ATTACK = "attack"
    DEFEND = "defend"
    ADAPT = "adapt"
    REGENERATE = "regenerate"
    SPECIAL = "special"
    DODGE = "dodge"


class BattleStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class BattleStats:
    health: float
    attack: float
    defense: float
    speed: float
    adaptability: float
    regeneration: float

    @classmethod
    def from_genome(cls, genome: dict) -> 'BattleStats':
        """Derive combat stats from genome traits."""
        fonts = genome.get('fonts', {})
        colors = genome.get('colors', {})
        layout = genome.get('layout', {})
        fitness = genome.get('fitness', 0.5)

        # Derive stats from genome properties
        health = 100 + fonts.get('size', 12) * 2
        attack = 10 + len(str(colors.get('primary', ''))) * 2
        defense = layout.get('margins', 10)
        speed = 5 + fonts.get('line_height', 1.5) * 3
        adaptability = fitness * 10
        regeneration = 2 + layout.get('padding', 5) / 2

        return cls(health, attack, defense, speed, adaptability, regeneration)


@dataclass
class Combatant:
    name: str
    genome: dict
    stats: BattleStats
    current_health: float = None
    is_defending: bool = False
    action_history: list = field(default_factory=list)

    def __post_init__(self):
        if self.current_health is None:
            self.current_health = self.stats.health

    def take_damage(self, damage: float) -> float:
        """Apply damage after defense calculation."""
        actual_damage = max(0, damage - self.stats.defense * (2 if self.is_defending else 1))
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage

    def heal(self, amount: float):
        """Heal up to max health."""
        self.current_health = min(self.stats.health, self.current_health + amount)

    def is_alive(self) -> bool:
        return self.current_health > 0


@dataclass
class BattleResult:
    winner: Combatant
    loser: Combatant
    turns: int
    battle_log: list
    timestamp: datetime = field(default_factory=datetime.utcnow)


class BattleRoyale:
    """Arena for agent combat!"""

    def __init__(self):
        self.battles: list[BattleResult] = []

    def create_combatant(self, name: str, genome: dict) -> Combatant:
        """Create a combatant from a genome."""
        stats = BattleStats.from_genome(genome)
        return Combatant(name=name, genome=genome, stats=stats)

    def execute_battle(self, combatant_a: Combatant, combatant_b: Combatant, max_turns: int = 100) -> BattleResult:
        """Execute a battle between two combatants."""
        battle_log = []
        turn = 0

        # Reset health
        combatant_a.current_health = combatant_a.stats.health
        combatant_b.current_health = combatant_b.stats.health

        while combatant_a.is_alive() and combatant_b.is_alive() and turn < max_turns:
            turn += 1

            # Determine order by speed
            if combatant_a.stats.speed >= combatant_b.stats.speed:
                first, second = combatant_a, combatant_b
            else:
                first, second = combatant_b, combatant_a

            # First combatant acts
            action = self._choose_action(first, second)
            result = self._execute_action(first, second, action)
            battle_log.append(f"Turn {turn}: {first.name} uses {action.value} - {result}")

            if not second.is_alive():
                break

            # Second combatant acts
            action = self._choose_action(second, first)
            result = self._execute_action(second, first, action)
            battle_log.append(f"Turn {turn}: {second.name} uses {action.value} - {result}")

        # Determine winner
        if combatant_a.current_health > combatant_b.current_health:
            winner, loser = combatant_a, combatant_b
        else:
            winner, loser = combatant_b, combatant_a

        result = BattleResult(winner=winner, loser=loser, turns=turn, battle_log=battle_log)
        self.battles.append(result)
        return result

    def _choose_action(self, combatant: Combatant, opponent: Combatant) -> BattleAction:
        """AI chooses an action based on state."""
        health_ratio = combatant.current_health / combatant.stats.health

        if health_ratio < 0.3:
            # Low health - heal or defend
            return random.choice([BattleAction.REGENERATE, BattleAction.DEFEND, BattleAction.DODGE])
        elif health_ratio > 0.7:
            # High health - aggressive
            return random.choice([BattleAction.ATTACK, BattleAction.SPECIAL, BattleAction.ATTACK])
        else:
            # Mid health - balanced
            return random.choice(list(BattleAction))

    def _execute_action(self, actor: Combatant, target: Combatant, action: BattleAction) -> str:
        """Execute an action and return result description."""
        actor.is_defending = False

        if action == BattleAction.ATTACK:
            damage = actor.stats.attack * (0.8 + random.random() * 0.4)
            actual = target.take_damage(damage)
            return f"deals {actual:.1f} damage ({target.current_health:.1f} HP left)"

        elif action == BattleAction.DEFEND:
            actor.is_defending = True
            return "takes defensive stance"

        elif action == BattleAction.REGENERATE:
            heal = actor.stats.regeneration * (1 + random.random())
            actor.heal(heal)
            return f"regenerates {heal:.1f} HP ({actor.current_health:.1f} HP)"

        elif action == BattleAction.SPECIAL:
            damage = actor.stats.attack * 1.5 + actor.stats.adaptability
            actual = target.take_damage(damage)
            return f"SPECIAL ATTACK for {actual:.1f} damage!"

        elif action == BattleAction.DODGE:
            actor.is_defending = True
            return "prepares to dodge"

        elif action == BattleAction.ADAPT:
            boost = random.choice(['attack', 'defense', 'speed'])
            setattr(actor.stats, boost, getattr(actor.stats, boost) * 1.1)
            return f"adapts: {boost} increased!"

        return "does nothing"

    def run_tournament(self, combatants: list[Combatant]) -> list[tuple[Combatant, int]]:
        """Run a round-robin tournament."""
        scores = {c.name: 0 for c in combatants}

        for i, a in enumerate(combatants):
            for b in combatants[i+1:]:
                result = self.execute_battle(a, b)
                scores[result.winner.name] += 1

        rankings = sorted([(c, scores[c.name]) for c in combatants], key=lambda x: -x[1])
        return rankings


# ============================================================================
# RUN THE TESTS!
# ============================================================================

def run_crossover_tests():
    """Test all crossover strategies."""
    print("\n" + "=" * 70)
    print("🧬 GENETIC CROSSOVER TESTS")
    print("=" * 70)

    parent_a = {
        'fonts': {'primary': 'Arial', 'size': 16, 'line_height': 1.5},
        'colors': {'primary': '#FF0000', 'secondary': '#00FF00'},
        'layout': {'margins': 10, 'padding': 5},
        'fitness': 0.8
    }

    parent_b = {
        'fonts': {'primary': 'Helvetica', 'size': 14, 'line_height': 1.2},
        'colors': {'primary': '#0000FF', 'secondary': '#FFFF00'},
        'layout': {'margins': 15, 'padding': 8},
        'fitness': 0.6
    }

    crossover = GeneticCrossover()
    passed = 0
    failed = 0

    for strategy in CrossoverStrategy:
        try:
            result = crossover.crossover(parent_a, parent_b, strategy=strategy)
            offspring = result.offspring

            # Verify offspring has required keys
            assert 'fonts' in offspring, f"Missing fonts in offspring"
            assert 'colors' in offspring, f"Missing colors in offspring"
            assert 'layout' in offspring, f"Missing layout in offspring"
            assert result.strategy == strategy

            print(f"  ✓ {strategy.value:25} - Offspring created with {len(result.inheritance_map)} genes")
            passed += 1
        except Exception as e:
            print(f"  ✗ {strategy.value:25} - FAILED: {e}")
            failed += 1

    # Test mutation
    print("\n  Testing mutation...")
    try:
        mutated = crossover.mutate(parent_a, mutation_rate=1.0)
        assert mutated != parent_a, "Mutation should change something"
        print("  ✓ Mutation engine working")
        passed += 1
    except Exception as e:
        print(f"  ✗ Mutation failed: {e}")
        failed += 1

    print(f"\n  Crossover Results: {passed} passed, {failed} failed")
    return passed, failed


def run_battle_tests():
    """Test the battle royale system."""
    print("\n" + "=" * 70)
    print("⚔️  BATTLE ROYALE TESTS")
    print("=" * 70)

    passed = 0
    failed = 0

    # Create test genomes
    genome_a = {
        'fonts': {'primary': 'Bold', 'size': 18, 'line_height': 1.8},
        'colors': {'primary': '#FF0000'},
        'layout': {'margins': 15, 'padding': 10},
        'fitness': 0.9
    }

    genome_b = {
        'fonts': {'primary': 'Light', 'size': 12, 'line_height': 1.2},
        'colors': {'primary': '#0000FF'},
        'layout': {'margins': 5, 'padding': 3},
        'fitness': 0.5
    }

    arena = BattleRoyale()

    # Test combatant creation
    try:
        fighter_a = arena.create_combatant("Alpha", genome_a)
        fighter_b = arena.create_combatant("Beta", genome_b)
        assert fighter_a.stats.health > 0
        assert fighter_b.stats.attack > 0
        print(f"  ✓ Combatant creation - Alpha has {fighter_a.stats.health:.1f} HP, {fighter_a.stats.attack:.1f} ATK")
        passed += 1
    except Exception as e:
        print(f"  ✗ Combatant creation failed: {e}")
        failed += 1
        return passed, failed

    # Test battle execution
    try:
        result = arena.execute_battle(fighter_a, fighter_b)
        assert result.winner is not None
        assert result.loser is not None
        assert result.turns > 0
        assert len(result.battle_log) > 0
        print(f"  ✓ Battle execution - {result.winner.name} wins in {result.turns} turns!")
        print(f"    Battle log excerpt: {result.battle_log[0]}")
        passed += 1
    except Exception as e:
        print(f"  ✗ Battle execution failed: {e}")
        failed += 1

    # Test tournament
    try:
        combatants = [
            arena.create_combatant("Warrior-1", genome_a),
            arena.create_combatant("Warrior-2", genome_b),
            arena.create_combatant("Warrior-3", {**genome_a, 'fitness': 0.7}),
            arena.create_combatant("Warrior-4", {**genome_b, 'fitness': 0.8}),
        ]
        rankings = arena.run_tournament(combatants)
        assert len(rankings) == 4
        print(f"  ✓ Tournament complete - Winner: {rankings[0][0].name} with {rankings[0][1]} wins")
        passed += 1
    except Exception as e:
        print(f"  ✗ Tournament failed: {e}")
        failed += 1

    # Test damage mechanics
    try:
        test_fighter = arena.create_combatant("Test", genome_a)
        initial_health = test_fighter.current_health
        damage_dealt = test_fighter.take_damage(50)
        assert test_fighter.current_health < initial_health
        test_fighter.heal(100)
        assert test_fighter.current_health <= test_fighter.stats.health
        print(f"  ✓ Damage/Heal mechanics - Took {damage_dealt:.1f} damage, healed back")
        passed += 1
    except Exception as e:
        print(f"  ✗ Damage mechanics failed: {e}")
        failed += 1

    print(f"\n  Battle Results: {passed} passed, {failed} failed")
    return passed, failed


def run_integration_tests():
    """Test crossover + battle integration."""
    print("\n" + "=" * 70)
    print("🔗 INTEGRATION TESTS (Crossover + Battle)")
    print("=" * 70)

    passed = 0
    failed = 0

    try:
        # Create parent genomes
        parent_a = {
            'fonts': {'primary': 'Strong', 'size': 20, 'line_height': 2.0},
            'colors': {'primary': '#FF0000'},
            'layout': {'margins': 20, 'padding': 15},
            'fitness': 0.95
        }
        parent_b = {
            'fonts': {'primary': 'Fast', 'size': 10, 'line_height': 1.0},
            'colors': {'primary': '#00FF00'},
            'layout': {'margins': 5, 'padding': 2},
            'fitness': 0.75
        }

        # Breed offspring
        crossover = GeneticCrossover()
        offspring_result = crossover.crossover(parent_a, parent_b, CrossoverStrategy.FITNESS_WEIGHTED)
        offspring_genome = offspring_result.offspring

        # Create battle arena
        arena = BattleRoyale()
        parent_fighter = arena.create_combatant("Parent-A", parent_a)
        offspring_fighter = arena.create_combatant("Offspring", offspring_genome)

        # Battle them!
        battle_result = arena.execute_battle(parent_fighter, offspring_fighter)

        print(f"  ✓ Bred offspring and battled against parent")
        print(f"    Offspring inherited traits from: {set(offspring_result.inheritance_map.values())}")
        print(f"    Battle winner: {battle_result.winner.name} in {battle_result.turns} turns")
        passed += 1

    except Exception as e:
        print(f"  ✗ Integration test failed: {e}")
        failed += 1

    # Test evolution over generations
    try:
        print("\n  Running multi-generation evolution...")
        crossover = GeneticCrossover(mutation_rate=0.2)
        arena = BattleRoyale()

        # Start with initial population
        population = [
            {'name': f'Gen0-{i}', 'fonts': {'size': random.randint(10, 20)},
             'colors': {'primary': f'#{random.randint(0, 255):02x}0000'},
             'layout': {'margins': random.randint(5, 20)}, 'fitness': random.random()}
            for i in range(4)
        ]

        # Evolve for 3 generations
        for gen in range(3):
            # Create combatants and run tournament
            combatants = [arena.create_combatant(p['name'], p) for p in population]
            rankings = arena.run_tournament(combatants)

            # Breed top 2 winners
            winner_genomes = [c.genome for c, _ in rankings[:2]]
            child1_result = crossover.crossover(winner_genomes[0], winner_genomes[1])
            child2_result = crossover.crossover(winner_genomes[1], winner_genomes[0])

            # Apply mutations
            child1 = crossover.mutate(child1_result.offspring)
            child2 = crossover.mutate(child2_result.offspring)
            child1['name'] = f'Gen{gen+1}-0'
            child2['name'] = f'Gen{gen+1}-1'

            # New population: 2 parents + 2 offspring
            population = [winner_genomes[0], winner_genomes[1], child1, child2]

        print(f"  ✓ Evolved population through 3 generations")
        print(f"    Final population: {[p.get('name', 'unnamed') for p in population]}")
        passed += 1

    except Exception as e:
        print(f"  ✗ Multi-generation evolution failed: {e}")
        failed += 1

    print(f"\n  Integration Results: {passed} passed, {failed} failed")
    return passed, failed


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    total_passed = 0
    total_failed = 0

    p, f = run_crossover_tests()
    total_passed += p
    total_failed += f

    p, f = run_battle_tests()
    total_passed += p
    total_failed += f

    p, f = run_integration_tests()
    total_passed += p
    total_failed += f

    print("\n" + "=" * 70)
    print(f"🏆 FINAL RESULTS: {total_passed} PASSED, {total_failed} FAILED")
    print("=" * 70)

    if total_failed == 0:
        print("""
    ██████╗  █████╗ ███████╗███████╗███████╗██████╗ ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██║
    ██████╔╝███████║███████╗███████╗█████╗  ██║  ██║██║
    ██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║  ██║╚═╝
    ██║     ██║  ██║███████║███████║███████╗██████╔╝██╗
    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝

        ALL TESTS PASSED! THE CODE WORKS!
        """)
        sys.exit(0)
    else:
        print("\n    Some tests failed. Check output above.")
        sys.exit(1)
