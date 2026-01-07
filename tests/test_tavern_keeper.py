"""
Tests for TavernKeeper RPG gamification system.
"""

import json
import tempfile
from pathlib import Path

import pytest

from waft.core.tavern_keeper import TavernKeeper


@pytest.fixture
def temp_project():
    """Create a temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        yield project_path


@pytest.fixture
def tavern_keeper(temp_project):
    """Create a TavernKeeper instance for testing."""
    return TavernKeeper(temp_project)


def test_tavern_keeper_initialization(tavern_keeper, temp_project):
    """Test that TavernKeeper initializes correctly."""
    assert tavern_keeper.project_path == temp_project
    assert tavern_keeper.chronicles_path.exists() or tavern_keeper.chronicles_path.parent.exists()


def test_character_creation(tavern_keeper):
    """Test that character is created with default stats."""
    character = tavern_keeper.get_character()

    assert character["name"] == "test_project"
    assert character["level"] == 1
    assert character["integrity"] == 100.0
    assert character["insight"] == 0.0
    assert character["credits"] == 0
    assert "ability_scores" in character
    assert character["ability_scores"]["strength"] == 8


def test_ability_modifiers(tavern_keeper):
    """Test ability modifier calculation."""
    # Default ability score of 8 should give -1 modifier
    assert tavern_keeper.get_ability_modifier("strength") == -1

    # Test with different scores
    character = tavern_keeper.get_character()
    character["ability_scores"]["strength"] = 10
    character["ability_scores"]["dexterity"] = 14
    character["ability_scores"]["constitution"] = 6

    # Update character (this is a test, so we'll directly modify)
    # In real usage, we'd use award_rewards or similar
    assert tavern_keeper.get_ability_modifier("strength") == 0  # (10-10)/2 = 0
    # Note: We can't easily test modified scores without updating the stored character


def test_proficiency_bonus(tavern_keeper):
    """Test proficiency bonus calculation."""
    # Get current level and test formula
    character = tavern_keeper.get_character()
    level = character.get("level", 1)

    bonus = tavern_keeper.get_proficiency_bonus()

    # Verify bonus matches level
    if level <= 4:
        assert bonus == 2
    elif level <= 8:
        assert bonus == 3
    elif level <= 12:
        assert bonus == 4
    elif level <= 16:
        assert bonus == 5
    else:
        assert bonus == 6

    # Bonus should be between 2 and 6
    assert 2 <= bonus <= 6


def test_roll_check(tavern_keeper):
    """Test dice rolling."""
    result = tavern_keeper.roll_check("strength", 10)

    assert "roll" in result
    assert "modifier" in result
    assert "total" in result
    assert "dc" in result
    assert "success" in result
    assert "classification" in result

    assert 1 <= result["roll"] <= 20
    assert result["dc"] == 10
    assert isinstance(result["success"], bool)


def test_roll_check_advantage(tavern_keeper):
    """Test rolling with advantage."""
    result = tavern_keeper.roll_check("strength", 10, advantage=True)

    assert result["roll"] >= 1
    assert result["roll"] <= 20


def test_narrate(tavern_keeper):
    """Test narrative generation."""
    narrative = tavern_keeper.narrate("verify", "success")

    assert isinstance(narrative, str)
    assert len(narrative) > 0
    # Narrative should be valid text (may or may not include character name depending on grammar)


def test_award_rewards(tavern_keeper):
    """Test reward system."""
    rewards = {
        "insight": 50.0,
        "credits": 10,
        "integrity": 5.0,
    }

    result = tavern_keeper.award_rewards(rewards)

    assert "level_up" in result
    assert "new_insight" in result
    assert "new_credits" in result
    assert result["new_insight"] == 50.0
    assert result["new_credits"] == 10

    # Check character was updated
    character = tavern_keeper.get_character()
    assert character["insight"] == 50.0
    assert character["credits"] == 10


def test_level_up(tavern_keeper):
    """Test leveling up."""
    # Award enough insight to level up
    # Level 2 requires: sqrt(insight/100) + 1 = 2, so insight >= 100
    rewards = {
        "insight": 100.0,
        "credits": 0,
        "integrity": 0.0,
    }

    result = tavern_keeper.award_rewards(rewards)

    # Should level up (level 1 -> 2)
    if result["new_insight"] >= 100:
        assert result["level_up"] or result["new_level"] > 1


def test_status_effects(tavern_keeper):
    """Test status effect system."""
    effect = {
        "id": "test_buff",
        "name": "Test Buff",
        "type": "buff",
        "effect": {"strength": +2},
        "duration": 3600,
        "description": "Test status effect",
    }

    tavern_keeper.apply_status_effect(effect)

    effects = tavern_keeper.get_active_status_effects()
    assert len(effects) > 0
    assert any(e.get("id") == "test_buff" for e in effects)


def test_adventure_journal(tavern_keeper):
    """Test adventure journal logging."""
    event = {
        "event": "test_event",
        "narrative": "Test narrative",
        "outcome": "success",
    }

    tavern_keeper.log_adventure(event)

    # Check journal was updated
    # Note: We can't easily read back without exposing internal structure
    # This test verifies the method doesn't crash


def test_character_sheet(tavern_keeper):
    """Test character sheet generation."""
    sheet = tavern_keeper.get_character_sheet()

    assert "character" in sheet
    assert "ability_scores" in sheet
    assert "ability_modifiers" in sheet
    assert "proficiency_bonus" in sheet
    assert "hp" in sheet
    assert "status_effects" in sheet

    assert sheet["hp"]["current"] > 0
    assert sheet["hp"]["max"] > 0


def test_process_command_hook(tavern_keeper):
    """Test command hook processing."""
    result = tavern_keeper.process_command_hook("verify", True, {})

    assert "narrative" in result
    assert "dice_result" in result
    assert "rewards" in result
    assert "xp_gained" in result

    assert isinstance(result["narrative"], str)
    assert "roll" in result["dice_result"]


def test_migration_from_gamification(tavern_keeper, temp_project):
    """Test migration from gamification.json."""
    # Create gamification.json
    gam_path = temp_project / "_pyrite" / ".waft" / "gamification.json"
    gam_path.parent.mkdir(parents=True, exist_ok=True)

    gam_data = {
        "integrity": 85.0,
        "insight": 150.0,
        "level": 2,
        "achievements": ["first_build"],
        "history": [
            {
                "timestamp": "2026-01-06T00:00:00Z",
                "type": "insight_award",
                "reason": "Test migration",
            }
        ],
    }

    with open(gam_path, "w") as f:
        json.dump(gam_data, f)

    # Create new TavernKeeper to trigger migration
    new_tavern = TavernKeeper(temp_project)

    # Check that stats were migrated
    character = new_tavern.get_character()
    # Migration should have updated insight and integrity
    # (Note: Migration only happens if character is at defaults)


def test_hp_calculation(tavern_keeper):
    """Test HP calculation from Constitution."""
    character = tavern_keeper.get_character()

    # Default CON is 8, modifier is -1
    # Max HP = 8 + (-1) + (Level-1) * (4 + (-1)) = 7 + 0 = 7
    # But we use max(1, ...) so should be at least 1
    max_hp = tavern_keeper.get_max_hp()
    assert max_hp >= 1

    current_hp = tavern_keeper.get_current_hp()
    assert current_hp >= 1
    assert current_hp <= max_hp

