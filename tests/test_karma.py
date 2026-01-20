"""
Tests for the KarmaMerchant (Chitragupta) reincarnation system.
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from src.waft.karma import (
    InsufficientKarmaError,
    InvalidLifePathError,
    KarmaMerchant,
    SoulNotFoundError,
)


@pytest.fixture
def temp_project():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def karma_merchant(temp_project):
    """Create a KarmaMerchant instance with temporary storage."""
    merchant = KarmaMerchant(temp_project)

    # Create a test life paths catalog
    life_paths = {
        "life_paths": [
            {
                "id": "test_explorer",
                "name": "Test Explorer",
                "cost": 0.0,
                "description": "A test life path",
                "config": {"starting_stats": {"INT": 10, "WIS": 10, "CHA": 10}},
            },
            {
                "id": "test_hero",
                "name": "Test Hero",
                "cost": 5.0,
                "description": "An expensive test path",
                "config": {"starting_stats": {"INT": 15, "WIS": 15, "CHA": 15}},
            },
        ]
    }

    catalog_file = merchant.store_path / "life_paths.json"
    with open(catalog_file, "w") as f:
        json.dump(life_paths, f)

    return merchant


class TestKarmaCalculation:
    """Test Karma calculation from life logs."""

    def test_calculate_karma_from_journal_pain(self, karma_merchant):
        """Test that painful experiences generate more Karma."""
        life_log = {
            "journal": [{"emotional_intensity": 0.8, "mood": "pain", "duration": 2.0}],
            "psyche": {},
            "memory": [],
        }

        karma = karma_merchant.calculate_karma(life_log)
        # 0.8 * 2.0 * 1.0 (pain weight) = 1.6
        assert karma > 1.5

    def test_calculate_karma_from_journal_pleasure(self, karma_merchant):
        """Test that pleasure generates less Karma than pain."""
        pain_log = {
            "journal": [{"emotional_intensity": 0.8, "mood": "pain", "duration": 2.0}],
            "psyche": {},
            "memory": [],
        }

        pleasure_log = {
            "journal": [{"emotional_intensity": 0.8, "mood": "pleasure", "duration": 2.0}],
            "psyche": {},
            "memory": [],
        }

        pain_karma = karma_merchant.calculate_karma(pain_log)
        pleasure_karma = karma_merchant.calculate_karma(pleasure_log)

        assert pain_karma > pleasure_karma

    def test_calculate_karma_from_psyche(self, karma_merchant):
        """Test that psyche state contributes to Karma."""
        life_log = {
            "journal": [],
            "psyche": {"emotional_energy": 5.0, "chaos": 0.5, "coherence": 1.0},
            "memory": [],
        }

        karma = karma_merchant.calculate_karma(life_log)
        assert karma > 0.0

    def test_calculate_karma_returns_non_negative(self, karma_merchant):
        """Test that Karma is never negative."""
        life_log = {"journal": [], "psyche": {}, "memory": []}

        karma = karma_merchant.calculate_karma(life_log)
        assert karma >= 0.0


class TestAkashaAccess:
    """Test Akasha (soul storage) access."""

    def test_access_new_soul(self, karma_merchant):
        """Test accessing a soul that doesn't exist yet."""
        soul_data = karma_merchant.access_akasha("new_soul_001")

        assert soul_data["soul_id"] == "new_soul_001"
        assert soul_data["total_karma"] == 0.0
        assert soul_data["lifetimes"] == []
        assert soul_data["last_incarnation"] is None

    def test_access_existing_soul(self, karma_merchant, temp_project):
        """Test accessing an existing soul."""
        # Create a soul file
        soul_id = "existing_soul_001"
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"

        soul_data = {
            "soul_id": soul_id,
            "lifetimes": [{"karma_earned": 10.0}, {"karma_earned": 5.0}],
            "karma_spent": 3.0,
            "memory_fragments": ["test memory"],
        }

        with open(soul_file, "w") as f:
            json.dump(soul_data, f)

        # Access the soul
        loaded_soul = karma_merchant.access_akasha(soul_id)

        assert loaded_soul["soul_id"] == soul_id
        assert loaded_soul["total_karma"] == 12.0  # 10 + 5 - 3
        assert len(loaded_soul["lifetimes"]) == 2

    def test_access_corrupted_soul(self, karma_merchant, temp_project):
        """Test accessing a corrupted soul file."""
        soul_id = "corrupted_soul"
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"

        # Write invalid JSON
        with open(soul_file, "w") as f:
            f.write("invalid json {{{")

        with pytest.raises(SoulNotFoundError):
            karma_merchant.access_akasha(soul_id)


class TestSoulKarma:
    """Test getting soul Karma balance."""

    def test_get_soul_karma_new_soul(self, karma_merchant):
        """Test getting Karma for a new soul."""
        karma = karma_merchant.get_soul_karma("new_soul")
        assert karma == 0.0

    def test_get_soul_karma_existing_soul(self, karma_merchant, temp_project):
        """Test getting Karma for an existing soul."""
        soul_id = "rich_soul"
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"

        soul_data = {"soul_id": soul_id, "lifetimes": [{"karma_earned": 20.0}], "karma_spent": 5.0}

        with open(soul_file, "w") as f:
            json.dump(soul_data, f)

        karma = karma_merchant.get_soul_karma(soul_id)
        assert karma == 15.0


class TestLifePaths:
    """Test life-path catalog."""

    def test_list_life_paths(self, karma_merchant):
        """Test listing available life-paths."""
        life_paths = karma_merchant.list_life_paths()

        assert len(life_paths) == 2
        assert life_paths[0]["id"] == "test_explorer"
        assert life_paths[1]["id"] == "test_hero"

    def test_list_life_paths_no_catalog(self, temp_project):
        """Test listing when no catalog exists."""
        merchant = KarmaMerchant(temp_project)
        life_paths = merchant.list_life_paths()

        assert life_paths == []


class TestReincarnation:
    """Test the reincarnation mechanism."""

    def test_reincarnate_new_soul_free_path(self, karma_merchant):
        """Test reincarnating a new soul with a free life-path."""
        soul_id = "test_soul_001"

        purchase_order = {"life_path_id": "test_explorer", "memory_continuity": 0.0}

        result = karma_merchant.reincarnate(soul_id, purchase_order)

        assert result["agent_config"]["soul_id"] == soul_id
        assert result["agent_config"]["life_path"] == "test_explorer"
        assert "lifetime_id" in result
        assert result["karma_remaining"] >= 0.0

    def test_reincarnate_with_sufficient_karma(self, karma_merchant, temp_project):
        """Test reincarnation with sufficient Karma."""
        soul_id = "rich_soul"
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"

        # Create a soul with 20 Karma
        soul_data = {
            "soul_id": soul_id,
            "lifetimes": [{"karma_earned": 20.0}],
            "karma_spent": 0.0,
            "memory_fragments": [],
        }

        with open(soul_file, "w") as f:
            json.dump(soul_data, f)

        # Purchase expensive path (costs 5.0 + 1.0 prana = 6.0)
        purchase_order = {"life_path_id": "test_hero"}

        result = karma_merchant.reincarnate(soul_id, purchase_order)

        assert result["karma_remaining"] == 14.0  # 20 - 6
        assert result["agent_config"]["life_path"] == "test_hero"

    def test_reincarnate_insufficient_karma(self, karma_merchant):
        """Test reincarnation fails with insufficient Karma."""
        soul_id = "poor_soul"

        # Try to purchase expensive path with 0 Karma
        purchase_order = {"life_path_id": "test_hero"}

        with pytest.raises(InsufficientKarmaError):
            karma_merchant.reincarnate(soul_id, purchase_order)

    def test_reincarnate_invalid_life_path(self, karma_merchant):
        """Test reincarnation fails with invalid life-path."""
        soul_id = "test_soul"

        purchase_order = {"life_path_id": "nonexistent_path"}

        with pytest.raises(InvalidLifePathError):
            karma_merchant.reincarnate(soul_id, purchase_order)

    def test_reincarnate_with_memory_continuity(self, karma_merchant, temp_project):
        """Test reincarnation with memory carry-over."""
        soul_id = "soul_with_memories"
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"

        # Create a soul with memories
        soul_data = {
            "soul_id": soul_id,
            "lifetimes": [{"karma_earned": 20.0}],
            "karma_spent": 0.0,
            "memory_fragments": ["memory 1", "memory 2", "memory 3", "memory 4"],
        }

        with open(soul_file, "w") as f:
            json.dump(soul_data, f)

        # Reincarnate with 50% memory continuity
        purchase_order = {"life_path_id": "test_explorer", "memory_continuity": 0.5}

        result = karma_merchant.reincarnate(soul_id, purchase_order)

        # Should have 2 memories (50% of 4)
        assert len(result["agent_config"]["inherited_memories"]) == 2

    def test_reincarnate_saves_to_akasha(self, karma_merchant):
        """Test that reincarnation saves updated soul to Akasha."""
        soul_id = "persistent_soul"

        purchase_order = {"life_path_id": "test_explorer"}

        karma_merchant.reincarnate(soul_id, purchase_order)

        # Verify soul file was created
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"
        assert soul_file.exists()

        # Load and verify
        with open(soul_file) as f:
            soul_data = json.load(f)

        assert len(soul_data["lifetimes"]) == 1
        assert soul_data["lifetimes"][0]["status"] == "active"


class TestIntegration:
    """Integration tests for the full Karma cycle."""

    def test_full_karma_cycle(self, karma_merchant):
        """Test a complete Karma cycle: live -> earn Karma -> reincarnate."""
        soul_id = "cycle_test_soul"

        # 1. First incarnation (free path)
        purchase_order = {"life_path_id": "test_explorer"}

        result1 = karma_merchant.reincarnate(soul_id, purchase_order)
        assert result1["karma_remaining"] >= 0.0

        # 2. Live a life and earn Karma
        life_log = {
            "journal": [
                {"emotional_intensity": 0.9, "mood": "pain", "duration": 3.0},
                {"emotional_intensity": 0.7, "mood": "pleasure", "duration": 2.0},
            ],
            "psyche": {"emotional_energy": 4.0, "chaos": 0.3, "coherence": 0.9},
            "memory": [],
        }

        karma_earned = karma_merchant.calculate_karma(life_log)
        assert karma_earned > 0.0

        # 3. Update soul with earned Karma
        soul_file = karma_merchant.akasha_path / f"{soul_id}.json"
        with open(soul_file) as f:
            soul_data = json.load(f)

        soul_data["lifetimes"][-1]["karma_earned"] = karma_earned
        soul_data["lifetimes"][-1]["status"] = "completed"

        with open(soul_file, "w") as f:
            json.dump(soul_data, f)

        # 4. Check updated Karma balance
        current_karma = karma_merchant.get_soul_karma(soul_id)
        assert current_karma >= karma_earned

        # 5. Reincarnate with earned Karma
        if current_karma >= 6.0:  # Cost of test_hero
            purchase_order2 = {"life_path_id": "test_hero", "memory_continuity": 0.3}

            result2 = karma_merchant.reincarnate(soul_id, purchase_order2)
            assert result2["agent_config"]["life_path"] == "test_hero"
            assert len(soul_data["lifetimes"]) >= 1
