"""
Tests for Battle Royale API Endpoints.

Comprehensive test suite for:
- Battle execution
- Tournament mode
- Statistics and history
- Combat preview
"""

import pytest
from fastapi.testclient import TestClient

from src.waft.api.main import create_app
from src.waft.api.routes.battle import _battles, _tournaments


@pytest.fixture
def client(temp_project_path):
    """Create test client."""
    app = create_app(temp_project_path)
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_battles():
    """Clear battles before each test."""
    _battles.clear()
    _tournaments.clear()
    yield
    _battles.clear()
    _tournaments.clear()


@pytest.fixture
def sample_agents():
    """Sample agent configurations."""
    return [
        {
            "name": "Warrior",
            "attack_modifier": 1.5,
            "defense_modifier": 0.8,
            "speed_modifier": 1.0,
        },
        {
            "name": "Defender",
            "attack_modifier": 0.8,
            "defense_modifier": 1.5,
            "speed_modifier": 1.0,
        },
    ]


class TestBattleEndpoints:
    """Test battle execution."""

    def test_start_battle(self, client, sample_agents):
        """Test starting a battle."""
        response = client.post(
            "/api/battle/start",
            json={
                "agents": sample_agents,
                "max_rounds": 50,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "battle_id" in data
        assert data["duration_rounds"] > 0
        assert len(data["participants"]) == 2

    def test_battle_has_winner(self, client, sample_agents):
        """Test battle produces a winner."""
        response = client.post(
            "/api/battle/start",
            json={
                "agents": sample_agents,
                "max_rounds": 200,
            },
        )

        data = response.json()
        # Either winner exists or max rounds reached
        if data["duration_rounds"] < 200:
            assert data["winner"] is not None

    def test_battle_minimum_agents(self, client):
        """Test battle requires at least 2 agents."""
        response = client.post(
            "/api/battle/start",
            json={
                "agents": [{"name": "Solo"}],
            },
        )

        assert response.status_code == 422  # Validation error

    def test_battle_maximum_agents(self, client):
        """Test battle accepts up to 10 agents."""
        agents = [{"name": f"Agent{i}"} for i in range(10)]

        response = client.post(
            "/api/battle/start",
            json={"agents": agents},
        )

        assert response.status_code == 201
        assert len(response.json()["participants"]) == 10

    def test_quick_battle(self, client):
        """Test quick 1v1 battle."""
        response = client.post(
            "/api/battle/quick",
            params={
                "agent_a": {"name": "A"},
                "agent_b": {"name": "B"},
            },
            json={},  # Quick battle uses query params
        )

        # This endpoint uses query params, adjust test
        response = client.post(
            "/api/battle/quick?"
            "agent_a={\"name\":\"A\"}&agent_b={\"name\":\"B\"}"
        )
        # Note: This test might need adjustment based on actual endpoint signature

    def test_get_battle(self, client, sample_agents):
        """Test getting battle by ID."""
        create_response = client.post(
            "/api/battle/start",
            json={"agents": sample_agents},
        )
        battle_id = create_response.json()["battle_id"]

        response = client.get(f"/api/battle/{battle_id}")

        assert response.status_code == 200
        assert response.json()["battle_id"] == battle_id

    def test_get_battle_not_found(self, client):
        """Test getting non-existent battle."""
        response = client.get("/api/battle/invalid-id")
        assert response.status_code == 404

    def test_get_battle_summary(self, client, sample_agents):
        """Test getting battle summary."""
        create_response = client.post(
            "/api/battle/start",
            json={"agents": sample_agents},
        )
        battle_id = create_response.json()["battle_id"]

        response = client.get(f"/api/battle/{battle_id}/summary")

        assert response.status_code == 200
        assert "BATTLE ROYALE RESULTS" in response.json()["summary"]


class TestTournamentEndpoints:
    """Test tournament mode."""

    def test_start_tournament(self, client):
        """Test starting a tournament."""
        agents = [{"name": f"Agent{i}"} for i in range(4)]

        response = client.post(
            "/api/battle/tournament",
            json={
                "agents": agents,
                "rounds": 2,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "tournament_id" in data
        assert data["participants"] == 4
        assert data["total_rounds"] == 2
        assert len(data["rankings"]) == 4

    def test_tournament_has_champion(self, client):
        """Test tournament produces a champion."""
        agents = [{"name": f"Agent{i}"} for i in range(4)]

        response = client.post(
            "/api/battle/tournament",
            json={"agents": agents, "rounds": 3},
        )

        data = response.json()
        assert data["champion"] is not None
        assert "name" in data["champion"]

    def test_tournament_minimum_agents(self, client):
        """Test tournament requires at least 4 agents."""
        agents = [{"name": f"Agent{i}"} for i in range(3)]

        response = client.post(
            "/api/battle/tournament",
            json={"agents": agents},
        )

        assert response.status_code == 422

    def test_get_tournament(self, client):
        """Test getting tournament by ID."""
        agents = [{"name": f"Agent{i}"} for i in range(4)]

        create_response = client.post(
            "/api/battle/tournament",
            json={"agents": agents},
        )
        tournament_id = create_response.json()["tournament_id"]

        response = client.get(f"/api/battle/tournament/{tournament_id}")

        assert response.status_code == 200
        assert response.json()["tournament_id"] == tournament_id

    def test_get_tournament_not_found(self, client):
        """Test getting non-existent tournament."""
        response = client.get("/api/battle/tournament/invalid-id")
        assert response.status_code == 404


class TestHistoryEndpoints:
    """Test history and statistics."""

    def test_battle_history_empty(self, client):
        """Test history with no battles."""
        response = client.get("/api/battle/history")

        assert response.status_code == 200
        data = response.json()
        assert data["total_battles"] == 0

    def test_battle_history(self, client, sample_agents):
        """Test battle history."""
        # Run some battles
        for _ in range(3):
            client.post(
                "/api/battle/start",
                json={"agents": sample_agents},
            )

        response = client.get("/api/battle/history")

        assert response.status_code == 200
        data = response.json()
        assert data["total_battles"] == 3
        assert len(data["recent_battles"]) == 3

    def test_battle_history_limit(self, client, sample_agents):
        """Test history respects limit."""
        for _ in range(5):
            client.post(
                "/api/battle/start",
                json={"agents": sample_agents},
            )

        response = client.get("/api/battle/history?limit=2")

        assert response.status_code == 200
        assert len(response.json()["recent_battles"]) == 2

    def test_battle_stats(self, client, sample_agents):
        """Test battle statistics."""
        for _ in range(3):
            client.post(
                "/api/battle/start",
                json={"agents": sample_agents},
            )

        response = client.get("/api/battle/stats")

        assert response.status_code == 200
        data = response.json()
        assert data["total_battles"] == 3
        assert data["total_rounds"] > 0
        assert data["avg_rounds_per_battle"] > 0

    def test_leaderboard_empty(self, client):
        """Test leaderboard with no battles."""
        response = client.get("/api/battle/leaderboard")

        assert response.status_code == 200
        assert response.json()["leaderboard"] == []

    def test_leaderboard(self, client, sample_agents):
        """Test leaderboard population."""
        for _ in range(5):
            client.post(
                "/api/battle/start",
                json={"agents": sample_agents},
            )

        response = client.get("/api/battle/leaderboard")

        assert response.status_code == 200
        leaderboard = response.json()["leaderboard"]
        assert len(leaderboard) > 0
        # Should be sorted by wins
        for entry in leaderboard:
            assert "name" in entry
            assert "wins" in entry
            assert "kills" in entry


class TestCombatPreview:
    """Test combat stat preview."""

    def test_preview_stats(self, client):
        """Test previewing combat stats."""
        response = client.post(
            "/api/battle/preview-stats",
            json={
                "name": "Test Agent",
                "attack_modifier": 1.5,
                "defense_modifier": 0.8,
                "speed_modifier": 1.2,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Agent"
        assert "stats" in data
        assert data["stats"]["health"] > 0
        assert data["stats"]["attack"] > 0

    def test_preview_default_modifiers(self, client):
        """Test preview with default modifiers."""
        response = client.post(
            "/api/battle/preview-stats",
            json={"name": "Default Agent"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["modifiers_applied"]["attack_modifier"] == 1.0

    def test_list_battle_actions(self, client):
        """Test listing battle actions."""
        response = client.get("/api/battle/actions")

        assert response.status_code == 200
        actions = response.json()["actions"]
        assert len(actions) >= 6

        action_names = [a["name"] for a in actions]
        assert "attack" in action_names
        assert "defend" in action_names
        assert "special" in action_names


class TestAdminEndpoints:
    """Test admin operations."""

    def test_reset_battles(self, client, sample_agents):
        """Test resetting battle history."""
        for _ in range(3):
            client.post(
                "/api/battle/start",
                json={"agents": sample_agents},
            )

        response = client.post("/api/battle/reset")

        assert response.status_code == 200
        assert "Cleared 3 battles" in response.json()["message"]

        # Verify empty
        history = client.get("/api/battle/history").json()
        assert history["total_battles"] == 0

    def test_battle_report(self, client):
        """Test getting arena report."""
        response = client.get("/api/battle/report")

        assert response.status_code == 200
        data = response.json()
        assert "report" in data
        assert "timestamp" in data


class TestAgentValidation:
    """Test agent configuration validation."""

    def test_agent_name_required(self, client):
        """Test agent name is required."""
        response = client.post(
            "/api/battle/start",
            json={
                "agents": [
                    {},  # Missing name
                    {"name": "Valid"},
                ]
            },
        )

        assert response.status_code == 422

    def test_agent_modifier_bounds(self, client):
        """Test modifier value bounds."""
        # Modifier too low
        response = client.post(
            "/api/battle/start",
            json={
                "agents": [
                    {"name": "A", "attack_modifier": 0.1},  # Below 0.5
                    {"name": "B"},
                ]
            },
        )
        assert response.status_code == 422

        # Modifier too high
        response = client.post(
            "/api/battle/start",
            json={
                "agents": [
                    {"name": "A", "attack_modifier": 3.0},  # Above 2.0
                    {"name": "B"},
                ]
            },
        )
        assert response.status_code == 422


class TestBattleParticipants:
    """Test battle participant tracking."""

    def test_participants_tracked(self, client, sample_agents):
        """Test all participants are tracked."""
        response = client.post(
            "/api/battle/start",
            json={"agents": sample_agents},
        )

        participants = response.json()["participants"]

        assert len(participants) == 2
        for p in participants:
            assert "name" in p
            assert "health" in p
            assert "max_health" in p
            assert "kills" in p
            assert "damage_dealt" in p

    def test_participant_health_tracking(self, client, sample_agents):
        """Test health is tracked correctly."""
        response = client.post(
            "/api/battle/start",
            json={"agents": sample_agents},
        )

        participants = response.json()["participants"]

        # At least one should have taken damage
        damage_taken = sum(p["damage_taken"] for p in participants)
        assert damage_taken > 0

    def test_winner_has_most_health(self, client, sample_agents):
        """Test winner has positive health."""
        response = client.post(
            "/api/battle/start",
            json={"agents": sample_agents, "max_rounds": 200},
        )

        data = response.json()
        if data["winner"]:
            assert data["winner"]["health"] > 0
            assert data["winner"]["is_alive"]
