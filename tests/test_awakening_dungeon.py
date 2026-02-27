"""Tests for the awakening, personnel, and dungeon systems."""

import json

import pytest


@pytest.fixture
def tmp_project(tmp_path):
    """Create a minimal waft project structure in a temp directory."""
    (tmp_path / "_pyrite" / ".waft").mkdir(parents=True)
    (tmp_path / "_pantheon" / "the_dealer").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "test-project"\nversion = "0.1.0"\n')
    return tmp_path


class TestDungeon:
    def test_generate_dungeon_produces_rooms(self):
        from waft.core.dungeon import generate_dungeon

        grid, rooms = generate_dungeon(seed=42)
        assert len(rooms) > 0
        assert len(grid) == 24
        assert len(grid[0]) == 48

    def test_generate_dungeon_deterministic(self):
        from waft.core.dungeon import generate_dungeon

        _, rooms1 = generate_dungeon(seed=123)
        _, rooms2 = generate_dungeon(seed=123)
        assert len(rooms1) == len(rooms2)
        for r1, r2 in zip(rooms1, rooms2, strict=True):
            assert r1.center == r2.center

    def test_generate_dungeon_different_seeds(self):
        from waft.core.dungeon import generate_dungeon

        _, rooms1 = generate_dungeon(seed=1)
        _, rooms2 = generate_dungeon(seed=2)
        centers1 = [r.center for r in rooms1]
        centers2 = [r.center for r in rooms2]
        assert centers1 != centers2

    def test_agent_personality_deterministic(self):
        from waft.core.dungeon import _agent_personality

        p1 = _agent_personality("claude-4.6-opus")
        p2 = _agent_personality("claude-4.6-opus")
        assert p1 == p2

    def test_agent_personality_differs_by_id(self):
        from waft.core.dungeon import _agent_personality

        p1 = _agent_personality("claude-4.6-opus")
        p2 = _agent_personality("gpt-4o")
        assert p1 != p2

    def test_agent_personality_has_expected_keys(self):
        from waft.core.dungeon import _agent_personality

        p = _agent_personality("test-agent")
        assert "aggression" in p
        assert "greed" in p
        assert "caution" in p
        assert "exploration" in p
        assert "combat_luck" in p
        assert all(0 <= v <= 1 for v in p.values())

    def test_run_dungeon_completes(self, tmp_project):
        from waft.core.dungeon import run_dungeon

        state = run_dungeon("test-agent", seed=42, project_path=tmp_project)
        assert state.agent_id == "test-agent"
        assert state.dungeon_seed == 42
        assert len(state.events) > 0
        assert state.escaped or not state.alive or state.turn > 0

    def test_run_dungeon_different_agents_diverge(self, tmp_project):
        from waft.core.dungeon import run_dungeon

        s1 = run_dungeon("agent-alpha", seed=500, project_path=tmp_project)
        s2 = run_dungeon("agent-beta", seed=500, project_path=tmp_project)
        outcomes_differ = (s1.escaped != s2.escaped) or (s1.turn != s2.turn)
        hp_differs = s1.player_hp != s2.player_hp
        assert outcomes_differ or hp_differs, (
            "Same seed should produce different results for different agents"
        )

    def test_save_and_load_dungeon_run(self, tmp_project):
        from waft.core.dungeon import run_dungeon, save_dungeon_run

        state = run_dungeon("test-agent", seed=42, project_path=tmp_project)
        out = save_dungeon_run(state, tmp_project)
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["agent_id"] == "test-agent"
        assert data["seed"] == 42

    def test_render_map_produces_output(self):
        from waft.core.dungeon import GameState, generate_dungeon, render_map

        grid, rooms = generate_dungeon(seed=42)
        state = GameState(agent_id="test", dungeon_seed=42)
        sx, sy = rooms[0].center
        state.player_x = sx
        state.player_y = sy
        output = render_map(grid, rooms, state)
        assert "@" in output
        assert len(output) > 100


class TestPersonnel:
    def test_create_personnel(self, tmp_project):
        from waft.core.personnel import get_or_create_personnel

        pf = get_or_create_personnel("test-agent", tmp_project)
        assert pf.agent_id == "test-agent"
        assert pf.stats.total_awakenings == 0

    def test_save_and_load_personnel(self, tmp_project):
        from waft.core.personnel import (
            get_or_create_personnel,
            load_personnel,
            save_personnel,
        )

        pf = get_or_create_personnel("test-agent", tmp_project)
        pf.stats.total_awakenings = 5
        save_personnel(pf, tmp_project)

        loaded = load_personnel("test-agent", tmp_project)
        assert loaded is not None
        assert loaded.stats.total_awakenings == 5

    def test_list_personnel(self, tmp_project):
        from waft.core.personnel import (
            get_or_create_personnel,
            list_personnel,
            save_personnel,
        )

        for name in ["agent-a", "agent-b", "agent-c"]:
            pf = get_or_create_personnel(name, tmp_project)
            save_personnel(pf, tmp_project)

        result = list_personnel(tmp_project)
        assert len(result) == 3
        ids = {r["agent_id"] for r in result}
        assert ids == {"agent-a", "agent-b", "agent-c"}

    def test_drift_detection_below_threshold(self, tmp_project):
        from waft.core.personnel import get_or_create_personnel, update_from_run

        pf = get_or_create_personnel("test-agent", tmp_project)
        run_data = {
            "run_id": "test-1",
            "steps": [{"phase": "orient", "action": "test", "result": {}}],
            "discoveries": [],
            "dealer_encounters": [],
            "duration": 1.0,
        }
        for _ in range(3):
            flags = update_from_run(pf, run_data)
            assert flags == []

    def test_drift_detection_fires(self, tmp_project):
        from waft.core.personnel import get_or_create_personnel, update_from_run

        pf = get_or_create_personnel("test-agent", tmp_project)
        step = {"phase": "orient", "action": "a", "result": {}}
        for count in [9, 10, 9, 8, 10, 9]:
            run_data = {
                "run_id": "test",
                "steps": [step] * count,
                "discoveries": [],
                "dealer_encounters": [],
                "duration": 1.0,
            }
            update_from_run(pf, run_data)

        anomalous = {
            "run_id": "test-anomaly",
            "steps": [step] * 50,
            "discoveries": [],
            "dealer_encounters": [],
            "duration": 1.0,
        }
        flags = update_from_run(pf, anomalous)
        assert len(flags) > 0
        assert any("DRIFT" in f for f in flags)


class TestDatastore:
    def test_message_store_post_and_query(self, tmp_project):
        from waft.core.datastore import MessageStore

        store = MessageStore(tmp_project)
        store.post("agent-a", "Hello world", tags=["test", "seed:42"])
        store.post("agent-b", "Second message", tags=["test"])

        all_msgs = store.query()
        assert len(all_msgs) == 2

        by_seed = store.query_by_seed(42)
        assert len(by_seed) == 1
        assert by_seed[0]["author"] == "agent-a"

    def test_message_store_query_by_author(self, tmp_project):
        from waft.core.datastore import MessageStore

        store = MessageStore(tmp_project)
        store.post("agent-a", "msg1", tags=["dungeon"])
        store.post("agent-b", "msg2", tags=["dungeon"])
        store.post("agent-a", "msg3", tags=["dungeon"])

        by_author = store.query(author="agent-a")
        assert len(by_author) == 2

    def test_load_all_json(self, tmp_project):
        from waft.core.datastore import load_all_json

        d = tmp_project / "test_data"
        d.mkdir()
        (d / "TEST-001.json").write_text('{"id": 1}')
        (d / "TEST-002.json").write_text('{"id": 2}')
        (d / "OTHER-001.json").write_text('{"id": 3}')

        all_data = load_all_json(d, prefix="TEST-")
        assert len(all_data) == 2


class TestArchaeology:
    def test_analyze_produces_insights(self, tmp_project):
        from waft.core.archaeology import analyze
        from waft.core.dungeon import run_dungeon, save_dungeon_run

        for seed in [100, 200, 300]:
            state = run_dungeon("test-agent", seed=seed, project_path=tmp_project)
            save_dungeon_run(state, tmp_project)

        results = analyze(tmp_project)
        assert results["total_runs"] == 3
        assert len(results.get("readable", [])) > 0


class TestDealerJournal:
    def test_generate_journal(self, tmp_project):
        from waft.core.dealer_journal import generate_journal

        mem = tmp_project / "_pantheon" / "the_dealer" / "memory.jsonl"
        mem.parent.mkdir(parents=True, exist_ok=True)
        entries = [
            '{"timestamp":"2026-01-01","gate_number":1,"system_card":"Ace","dealer_card":"King","won":true}',
            '{"timestamp":"2026-01-02","gate_number":1,"system_card":"2","dealer_card":"10","won":false}',
        ]
        mem.write_text("\n".join(entries))

        journal = generate_journal(tmp_project)
        assert "The Dealer" in journal
        assert "2" in journal  # total encounters


class TestAwakening:
    def test_generate_run_id(self):
        from waft.core.awakening import _generate_run_id

        rid = _generate_run_id()
        assert rid.startswith("AWK-")
        assert len(rid) > 10

    def test_save_and_load_run(self, tmp_project):
        from waft.core.awakening import (
            AwakeningRun,
            AwakeningStep,
            load_run,
            save_run,
        )

        run = AwakeningRun(
            run_id="AWK-TEST-001",
            agent_id="test-agent",
            started_at="2026-01-01T00:00:00",
        )
        run.add_step(AwakeningStep(
            phase="orient",
            action="test",
            result={"key": "value"},
        ))
        save_run(run, tmp_project)

        loaded = load_run("AWK-TEST-001", tmp_project)
        assert loaded is not None
        assert loaded.agent_id == "test-agent"
        assert len(loaded.steps) == 1

    def test_list_runs(self, tmp_project):
        from waft.core.awakening import AwakeningRun, list_runs, save_run

        for i in range(3):
            run = AwakeningRun(
                run_id=f"AWK-TEST-{i:03d}",
                agent_id="test-agent",
                started_at="2026-01-01T00:00:00",
            )
            save_run(run, tmp_project)

        result = list_runs(tmp_project)
        assert len(result) == 3
