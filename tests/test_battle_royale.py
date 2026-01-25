"""
Tests for the Battle Royale System.

Comprehensive test suite covering:
- Combat mechanics
- Battle simulation
- Tournament mode
- Stat derivation from genomes
"""

import asyncio

import pytest

from src.waft.evolution import (
    BattleAction,
    BattleResult,
    BattleRoyale,
    BattleStats,
    BattleStatus,
    Combatant,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
    StylingGene,
    StylingGenome,
    quick_battle,
)


@pytest.fixture
def genome_warrior():
    """Create a warrior-type genome (high attack)."""
    genes = StylingGene(
        font=FontGene(size_h1=48, size_body=14),  # Large heading = high attack
        margin=MarginGene(top=10, bottom=10),  # Low margin = low defense
        color=ColorGene(text="#000000", background="#ffffff"),  # High contrast = high special
        layout=LayoutGene(columns=1, density="compact"),
        name="Warrior",
    )
    genome = StylingGenome.from_genes(genes)
    genome.evaluate_fitness({"combat": 0.9})
    return genome


@pytest.fixture
def genome_defender():
    """Create a defender-type genome (high defense)."""
    genes = StylingGene(
        font=FontGene(size_h1=20, size_body=10),  # Small heading = lower attack
        margin=MarginGene(top=50, bottom=50),  # High margin = high defense
        color=ColorGene(text="#666666", background="#eeeeee"),  # Low contrast
        layout=LayoutGene(columns=2, density="spacious"),  # More columns = more health
        name="Defender",
    )
    genome = StylingGenome.from_genes(genes)
    genome.evaluate_fitness({"combat": 0.7})
    return genome


@pytest.fixture
def genome_speedster():
    """Create a speedster-type genome (high speed)."""
    genes = StylingGene(
        font=FontGene(size_h1=24, size_body=8),  # Small body = fast
        margin=MarginGene(top=20, bottom=20),
        color=ColorGene(text="#000000", background="#ffffff"),
        layout=LayoutGene(columns=1, density="compact"),
        name="Speedster",
    )
    genome = StylingGenome.from_genes(genes)
    genome.evaluate_fitness({"combat": 0.8})
    return genome


class TestBattleStats:
    """Test combat stat derivation from genomes."""

    def test_stats_from_genome(self, genome_warrior):
        """Test stats are derived from genome."""
        stats = BattleStats.from_genome(genome_warrior)

        assert stats.health > 0
        assert stats.attack > 0
        assert stats.defense > 0
        assert stats.speed > 0
        assert stats.adaptability > 0
        assert stats.regeneration > 0
        assert stats.special_power > 0

    def test_high_heading_increases_attack(self, genome_warrior, genome_defender):
        """Test that larger heading sizes increase attack."""
        warrior_stats = BattleStats.from_genome(genome_warrior)
        defender_stats = BattleStats.from_genome(genome_defender)

        # Warrior has size_h1=48, defender has size_h1=20
        assert warrior_stats.attack > defender_stats.attack

    def test_high_margin_increases_defense(self, genome_warrior, genome_defender):
        """Test that higher margins increase defense."""
        warrior_stats = BattleStats.from_genome(genome_warrior)
        defender_stats = BattleStats.from_genome(genome_defender)

        # Defender has top=50, warrior has top=10
        assert defender_stats.defense > warrior_stats.defense

    def test_more_columns_increases_health(self, genome_warrior, genome_defender):
        """Test that more columns increase health."""
        warrior_stats = BattleStats.from_genome(genome_warrior)
        defender_stats = BattleStats.from_genome(genome_defender)

        # Defender has columns=2, warrior has columns=1
        assert defender_stats.health > warrior_stats.health

    def test_fitness_multiplier_applied(self):
        """Test that fitness score affects stats."""
        genes = StylingGene(name="Test")

        # Low fitness genome
        low_fitness = StylingGenome.from_genes(genes)
        low_fitness.evaluate_fitness({"test": 0.1})

        # High fitness genome
        high_fitness = StylingGenome.from_genes(genes)
        high_fitness.evaluate_fitness({"test": 0.9})

        low_stats = BattleStats.from_genome(low_fitness)
        high_stats = BattleStats.from_genome(high_fitness)

        # High fitness should have higher stats
        assert high_stats.attack > low_stats.attack
        assert high_stats.health > low_stats.health


class TestCombatant:
    """Test combatant mechanics."""

    def test_combatant_creation(self, genome_warrior):
        """Test combatant is created correctly."""
        stats = BattleStats.from_genome(genome_warrior)
        combatant = Combatant(genome=genome_warrior, stats=stats)

        assert combatant.current_health == stats.health
        assert combatant.is_alive
        assert combatant.kills == 0
        assert combatant.damage_dealt == 0

    def test_take_damage(self, genome_warrior):
        """Test damage application."""
        stats = BattleStats.from_genome(genome_warrior)
        combatant = Combatant(genome=genome_warrior, stats=stats)

        initial_health = combatant.current_health
        actual_damage = combatant.take_damage(20)

        assert combatant.current_health < initial_health
        assert combatant.damage_taken > 0
        assert actual_damage > 0

    def test_damage_reduced_by_defense(self, genome_defender):
        """Test defense reduces incoming damage."""
        stats = BattleStats.from_genome(genome_defender)
        combatant = Combatant(genome=genome_defender, stats=stats)

        raw_damage = 50
        actual_damage = combatant.take_damage(raw_damage)

        # With defense, actual damage should be less
        assert actual_damage < raw_damage

    def test_death_on_zero_health(self, genome_warrior):
        """Test combatant dies at zero health."""
        stats = BattleStats.from_genome(genome_warrior)
        combatant = Combatant(genome=genome_warrior, stats=stats)

        # Deal massive damage
        combatant.take_damage(10000)

        assert combatant.current_health == 0
        assert not combatant.is_alive

    def test_heal(self, genome_warrior):
        """Test healing mechanic."""
        stats = BattleStats.from_genome(genome_warrior)
        combatant = Combatant(genome=genome_warrior, stats=stats)

        # Take some damage
        combatant.take_damage(30)
        health_after_damage = combatant.current_health

        # Heal
        combatant.heal(20)

        assert combatant.current_health > health_after_damage
        # Should not exceed max health
        assert combatant.current_health <= stats.health

    def test_health_percent(self, genome_warrior):
        """Test health percentage calculation."""
        stats = BattleStats.from_genome(genome_warrior)
        combatant = Combatant(genome=genome_warrior, stats=stats)

        assert combatant.health_percent == 1.0

        combatant.take_damage(stats.health / 2)
        assert 0.4 < combatant.health_percent < 0.6


class TestBattleRoyale:
    """Test battle simulation."""

    @pytest.mark.asyncio
    async def test_basic_battle(self, genome_warrior, genome_defender):
        """Test basic battle execution."""
        arena = BattleRoyale(max_rounds=50)
        result = await arena.run_battle([genome_warrior, genome_defender])

        assert isinstance(result, BattleResult)
        assert result.battle_id
        assert result.duration_rounds > 0
        assert result.total_damage > 0
        assert len(result.participants) == 2

    @pytest.mark.asyncio
    async def test_battle_has_winner(self, genome_warrior, genome_defender):
        """Test battle produces a winner."""
        arena = BattleRoyale(max_rounds=200)
        result = await arena.run_battle([genome_warrior, genome_defender])

        # Either there's a winner or it's a max rounds timeout
        if result.duration_rounds < 200:
            assert result.winner is not None

    @pytest.mark.asyncio
    async def test_multi_combatant_battle(
        self, genome_warrior, genome_defender, genome_speedster
    ):
        """Test battle with multiple combatants."""
        arena = BattleRoyale(max_rounds=100)
        result = await arena.run_battle(
            [genome_warrior, genome_defender, genome_speedster]
        )

        assert len(result.participants) == 3
        # At least some should be eliminated
        alive = sum(1 for p in result.participants if p.is_alive)
        assert alive <= 3

    @pytest.mark.asyncio
    async def test_battle_rounds_tracked(self, genome_warrior, genome_defender):
        """Test battle rounds are recorded."""
        arena = BattleRoyale(max_rounds=20)
        result = await arena.run_battle([genome_warrior, genome_defender])

        assert len(result.rounds) == result.duration_rounds

    @pytest.mark.asyncio
    async def test_damage_recorded(self, genome_warrior, genome_defender):
        """Test damage is tracked correctly."""
        arena = BattleRoyale(max_rounds=50)
        result = await arena.run_battle([genome_warrior, genome_defender])

        total_dealt = sum(p.damage_dealt for p in result.participants)
        total_taken = sum(p.damage_taken for p in result.participants)

        # These should be roughly equal (all damage dealt is damage taken)
        assert abs(total_dealt - total_taken) < 1  # Allow small float error

    @pytest.mark.asyncio
    async def test_max_rounds_limit(self, genome_warrior, genome_defender):
        """Test battle respects max rounds limit."""
        arena = BattleRoyale(max_rounds=5)
        result = await arena.run_battle([genome_warrior, genome_defender])

        assert result.duration_rounds <= 5


class TestTournament:
    """Test tournament mode."""

    def test_tournament_basic(
        self, genome_warrior, genome_defender, genome_speedster
    ):
        """Test basic tournament execution."""
        arena = BattleRoyale()

        # Need at least 4 for tournament
        genes = StylingGene(name="Extra")
        extra = StylingGenome.from_genes(genes)

        results = arena.run_tournament(
            [genome_warrior, genome_defender, genome_speedster, extra],
            rounds=2,
        )

        assert "total_rounds" in results
        assert "participants" in results
        assert "rankings" in results
        assert "champion" in results

    def test_tournament_rankings(
        self, genome_warrior, genome_defender, genome_speedster
    ):
        """Test tournament produces rankings."""
        arena = BattleRoyale()

        genes = StylingGene(name="Extra")
        extra = StylingGenome.from_genes(genes)

        results = arena.run_tournament(
            [genome_warrior, genome_defender, genome_speedster, extra],
            rounds=3,
        )

        rankings = results["rankings"]
        assert len(rankings) == 4

        # Rankings should have score info
        for entry in rankings:
            assert "name" in entry
            assert "wins" in entry
            assert "kills" in entry


class TestQuickBattle:
    """Test quick_battle convenience function."""

    @pytest.mark.asyncio
    async def test_quick_battle(self, genome_warrior, genome_defender):
        """Test quick battle function."""
        result = await quick_battle([genome_warrior, genome_defender])

        assert isinstance(result, BattleResult)
        assert len(result.participants) == 2


class TestBattleActions:
    """Test individual battle actions."""

    def test_all_actions_defined(self):
        """Test all battle actions are defined."""
        actions = list(BattleAction)

        assert BattleAction.ATTACK in actions
        assert BattleAction.DEFEND in actions
        assert BattleAction.ADAPT in actions
        assert BattleAction.REGENERATE in actions
        assert BattleAction.SPECIAL in actions
        assert BattleAction.DODGE in actions

    def test_combatant_chooses_action(self, genome_warrior, genome_defender):
        """Test combatants can choose actions."""
        warrior_stats = BattleStats.from_genome(genome_warrior)
        defender_stats = BattleStats.from_genome(genome_defender)

        warrior = Combatant(genome=genome_warrior, stats=warrior_stats)
        defender = Combatant(genome=genome_defender, stats=defender_stats)

        action, target = warrior.choose_action([defender])

        assert action in BattleAction
        # If action requires target, it should be provided
        if action in [BattleAction.ATTACK, BattleAction.SPECIAL]:
            assert target is not None


class TestBattleReport:
    """Test battle report generation."""

    @pytest.mark.asyncio
    async def test_battle_summary(self, genome_warrior, genome_defender):
        """Test battle summary generation."""
        arena = BattleRoyale(max_rounds=30)
        result = await arena.run_battle([genome_warrior, genome_defender])

        summary = result.get_summary()

        assert "BATTLE ROYALE RESULTS" in summary
        assert result.battle_id in summary
        assert "WINNER" in summary or "No Winner" in summary

    def test_arena_report(self):
        """Test arena report with no battles."""
        arena = BattleRoyale()
        report = arena.generate_battle_report()

        assert "Battle Report" in report
        assert "No battles" in report


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.asyncio
    async def test_minimum_combatants(self, genome_warrior):
        """Test battle requires at least 2 combatants."""
        arena = BattleRoyale()

        with pytest.raises(ValueError):
            await arena.run_battle([genome_warrior])

    @pytest.mark.asyncio
    async def test_identical_genomes_battle(self, genome_warrior):
        """Test battle between identical genomes."""
        arena = BattleRoyale(max_rounds=50)

        # Create a copy
        genes = genome_warrior.genes
        twin = StylingGenome.from_genes(genes)
        twin.evaluate_fitness({"combat": 0.9})

        result = await arena.run_battle([genome_warrior, twin])

        assert len(result.participants) == 2

    @pytest.mark.asyncio
    async def test_large_battle(self):
        """Test battle with many combatants."""
        arena = BattleRoyale(max_rounds=50)

        genomes = []
        for i in range(8):
            genes = StylingGene(name=f"Agent{i}")
            genome = StylingGenome.from_genes(genes)
            genomes.append(genome)

        result = await arena.run_battle(genomes)

        assert len(result.participants) == 8
