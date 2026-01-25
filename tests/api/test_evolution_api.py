"""
Tests for Evolution API Endpoints.

Comprehensive test suite for:
- Genome CRUD operations
- Crossover endpoints
- Fitness evaluation
- Population statistics
- Scint detection
"""

import pytest
from fastapi.testclient import TestClient

from src.waft.api.main import create_app
from src.waft.api.routes.evolution import _genomes


@pytest.fixture
def client(temp_project_path):
    """Create test client."""
    app = create_app(temp_project_path)
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_genomes():
    """Clear genomes before each test."""
    _genomes.clear()
    yield
    _genomes.clear()


class TestGenomeEndpoints:
    """Test genome CRUD operations."""

    def test_create_genome(self, client):
        """Test creating a new genome."""
        response = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {
                    "font": {"family": "serif", "size_body": 12},
                    "margin": {"top": 25},
                    "color": {"text": "#000000"},
                    "layout": {"columns": 1},
                    "name": "Test Genome",
                }
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "genome_id" in data
        assert data["scientific_name"]
        assert data["generation"] == 0

    def test_create_genome_with_parent(self, client):
        """Test creating genome with parent."""
        # Create parent
        parent_response = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Parent"}},
        )
        parent_id = parent_response.json()["genome_id"]

        # Create child
        child_response = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {"name": "Child"},
                "parent_id": parent_id,
            },
        )

        assert child_response.status_code == 201
        data = child_response.json()
        assert data["generation"] == 1
        assert data["parent_id"] == parent_id

    def test_create_genome_invalid_parent(self, client):
        """Test creating genome with invalid parent ID."""
        response = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {"name": "Test"},
                "parent_id": "invalid-id",
            },
        )

        assert response.status_code == 404

    def test_list_genomes(self, client):
        """Test listing genomes."""
        # Create some genomes
        for i in range(3):
            client.post(
                "/api/evolution/genomes",
                json={"genes": {"name": f"Genome {i}"}},
            )

        response = client.get("/api/evolution/genomes")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_list_genomes_with_filter(self, client):
        """Test listing genomes with generation filter."""
        # Create parent
        parent = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Parent"}},
        ).json()

        # Create children
        for i in range(2):
            client.post(
                "/api/evolution/genomes",
                json={"genes": {"name": f"Child {i}"}, "parent_id": parent["genome_id"]},
            )

        # Filter by generation
        response = client.get("/api/evolution/genomes?generation=1")
        data = response.json()

        assert len(data) == 2
        assert all(g["generation"] == 1 for g in data)

    def test_get_genome(self, client):
        """Test getting a specific genome."""
        create_response = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Test"}},
        )
        genome_id = create_response.json()["genome_id"]

        response = client.get(f"/api/evolution/genomes/{genome_id}")

        assert response.status_code == 200
        assert response.json()["genome_id"] == genome_id

    def test_get_genome_not_found(self, client):
        """Test getting non-existent genome."""
        response = client.get("/api/evolution/genomes/invalid-id")
        assert response.status_code == 404

    def test_delete_genome(self, client):
        """Test deleting a genome."""
        create_response = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Test"}},
        )
        genome_id = create_response.json()["genome_id"]

        delete_response = client.delete(f"/api/evolution/genomes/{genome_id}")
        assert delete_response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/api/evolution/genomes/{genome_id}")
        assert get_response.status_code == 404


class TestCrossoverEndpoints:
    """Test crossover operations."""

    @pytest.fixture
    def two_genomes(self, client):
        """Create two genomes for crossover tests."""
        parent_a = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Parent A"}},
        ).json()

        parent_b = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Parent B"}},
        ).json()

        return parent_a, parent_b

    def test_crossover_uniform(self, client, two_genomes):
        """Test uniform crossover."""
        parent_a, parent_b = two_genomes

        response = client.post(
            "/api/evolution/crossover",
            json={
                "parent_a_id": parent_a["genome_id"],
                "parent_b_id": parent_b["genome_id"],
                "strategy": "uniform",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["strategy"] == "uniform"
        assert data["offspring"]["genome_id"]
        assert len(data["inheritance_map"]) > 0

    def test_crossover_all_strategies(self, client, two_genomes):
        """Test all crossover strategies."""
        parent_a, parent_b = two_genomes
        strategies = [
            "uniform",
            "single_point",
            "two_point",
            "category_swap",
            "fitness_weighted",
            "blended",
            "dominant_recessive",
        ]

        for strategy in strategies:
            response = client.post(
                "/api/evolution/crossover",
                json={
                    "parent_a_id": parent_a["genome_id"],
                    "parent_b_id": parent_b["genome_id"],
                    "strategy": strategy,
                },
            )

            assert response.status_code == 200, f"Strategy {strategy} failed"
            assert response.json()["strategy"] == strategy

    def test_crossover_invalid_strategy(self, client, two_genomes):
        """Test crossover with invalid strategy."""
        parent_a, parent_b = two_genomes

        response = client.post(
            "/api/evolution/crossover",
            json={
                "parent_a_id": parent_a["genome_id"],
                "parent_b_id": parent_b["genome_id"],
                "strategy": "invalid_strategy",
            },
        )

        assert response.status_code == 400

    def test_crossover_invalid_parent(self, client, two_genomes):
        """Test crossover with invalid parent ID."""
        parent_a, _ = two_genomes

        response = client.post(
            "/api/evolution/crossover",
            json={
                "parent_a_id": parent_a["genome_id"],
                "parent_b_id": "invalid-id",
            },
        )

        assert response.status_code == 404

    def test_list_strategies(self, client):
        """Test listing available strategies."""
        response = client.get("/api/evolution/crossover/strategies")

        assert response.status_code == 200
        strategies = response.json()["strategies"]
        assert len(strategies) == 7


class TestFitnessEndpoints:
    """Test fitness evaluation."""

    def test_update_fitness(self, client):
        """Test updating genome fitness."""
        genome = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Test"}},
        ).json()

        response = client.post(
            f"/api/evolution/genomes/{genome['genome_id']}/fitness",
            json={
                "metrics": {
                    "readability": 0.8,
                    "density": 0.7,
                    "contrast": 0.9,
                }
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["fitness_score"] is not None
        assert 0 < data["fitness_score"] <= 1

    def test_update_fitness_invalid_metric(self, client):
        """Test updating fitness with invalid metric value."""
        genome = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Test"}},
        ).json()

        response = client.post(
            f"/api/evolution/genomes/{genome['genome_id']}/fitness",
            json={
                "metrics": {
                    "readability": 1.5,  # Invalid: > 1.0
                }
            },
        )

        assert response.status_code == 400

    def test_update_fitness_not_found(self, client):
        """Test updating fitness for non-existent genome."""
        response = client.post(
            "/api/evolution/genomes/invalid-id/fitness",
            json={"metrics": {"test": 0.5}},
        )

        assert response.status_code == 404


class TestPopulationEndpoints:
    """Test population statistics."""

    def test_population_stats_empty(self, client):
        """Test stats with empty population."""
        response = client.get("/api/evolution/population/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["total_genomes"] == 0

    def test_population_stats(self, client):
        """Test population statistics."""
        # Create genomes with fitness
        for i in range(5):
            genome = client.post(
                "/api/evolution/genomes",
                json={"genes": {"name": f"Genome {i}"}},
            ).json()

            client.post(
                f"/api/evolution/genomes/{genome['genome_id']}/fitness",
                json={"metrics": {"test": 0.5 + i * 0.1}},
            )

        response = client.get("/api/evolution/population/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["total_genomes"] == 5
        assert data["best_fitness"] > 0
        assert data["avg_fitness"] > 0

    def test_lineage(self, client):
        """Test getting lineage."""
        # Create lineage: grandparent -> parent -> child
        grandparent = client.post(
            "/api/evolution/genomes",
            json={"genes": {"name": "Grandparent"}},
        ).json()

        parent = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {"name": "Parent"},
                "parent_id": grandparent["genome_id"],
            },
        ).json()

        child = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {"name": "Child"},
                "parent_id": parent["genome_id"],
            },
        ).json()

        response = client.get(f"/api/evolution/population/lineage/{child['genome_id']}")

        assert response.status_code == 200
        lineage = response.json()["lineage"]
        assert len(lineage) == 3


class TestScintEndpoints:
    """Test scint detection."""

    def test_detect_scint(self, client):
        """Test scint detection between divergent genomes."""
        genome_a = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {
                    "font": {"size_body": 12},
                    "color": {"text": "#000000"},
                }
            },
        ).json()

        genome_b = client.post(
            "/api/evolution/genomes",
            json={
                "genes": {
                    "font": {"size_body": 20},
                    "color": {"text": "#ff0000"},
                }
            },
        ).json()

        response = client.post(
            f"/api/evolution/scint/detect?genome_a_id={genome_a['genome_id']}&genome_b_id={genome_b['genome_id']}"
        )

        assert response.status_code == 200
        # May or may not detect scint depending on threshold

    def test_reconcile_scint(self, client):
        """Test scint reconciliation."""
        # Create two divergent genomes with fitness
        genome_a = client.post(
            "/api/evolution/genomes",
            json={"genes": {"font": {"size_body": 12}}},
        ).json()

        client.post(
            f"/api/evolution/genomes/{genome_a['genome_id']}/fitness",
            json={"metrics": {"test": 0.9}},
        )

        genome_b = client.post(
            "/api/evolution/genomes",
            json={"genes": {"font": {"size_body": 20}}},
        ).json()

        client.post(
            f"/api/evolution/genomes/{genome_b['genome_id']}/fitness",
            json={"metrics": {"test": 0.5}},
        )

        response = client.post(
            f"/api/evolution/scint/reconcile?genome_a_id={genome_a['genome_id']}&genome_b_id={genome_b['genome_id']}&strategy=select_fittest"
        )

        assert response.status_code == 200


class TestAdminEndpoints:
    """Test admin operations."""

    def test_reset_population(self, client):
        """Test resetting population."""
        # Create some genomes
        for i in range(3):
            client.post(
                "/api/evolution/genomes",
                json={"genes": {"name": f"Genome {i}"}},
            )

        response = client.post("/api/evolution/reset")

        assert response.status_code == 200
        assert "Cleared 3" in response.json()["message"]

        # Verify empty
        list_response = client.get("/api/evolution/genomes")
        assert len(list_response.json()) == 0

    def test_evolution_report(self, client):
        """Test getting evolution report."""
        response = client.get("/api/evolution/report")

        assert response.status_code == 200
        data = response.json()
        assert "breeding_report" in data
        assert "scint_report" in data
        assert "timestamp" in data
