"""Tests for gamification manager."""

import json
from pathlib import Path
from waft.core.gamification import GamificationManager


def test_gamification_manager_init(temp_project_path):
    """Test GamificationManager initialization."""
    manager = GamificationManager(temp_project_path)
    assert manager.integrity == 100.0
    assert manager.insight == 0.0
    assert manager.level == 1


def test_damage_integrity(temp_project_path):
    """Test integrity damage."""
    manager = GamificationManager(temp_project_path)
    new_integrity = manager.damage_integrity(10.0, reason="Test")
    assert new_integrity == 90.0
    assert manager.integrity == 90.0


def test_restore_integrity(temp_project_path):
    """Test integrity restoration."""
    manager = GamificationManager(temp_project_path)
    manager.damage_integrity(20.0)
    new_integrity = manager.restore_integrity(5.0, reason="Test")
    assert new_integrity == 85.0


def test_award_insight(temp_project_path):
    """Test insight awarding."""
    manager = GamificationManager(temp_project_path)
    result = manager.award_insight(100.0, reason="Test")
    assert result["new_insight"] == 100.0
    assert result["level_up"] is True
    assert manager.level > 1


def test_unlock_achievement(temp_project_path):
    """Test achievement unlocking."""
    manager = GamificationManager(temp_project_path)
    unlocked = manager.unlock_achievement("test_achievement", "Test Achievement")
    assert unlocked is True
    assert "test_achievement" in manager.achievements

    # Try to unlock again
    unlocked_again = manager.unlock_achievement("test_achievement", "Test Achievement")
    assert unlocked_again is False


def test_get_stats(temp_project_path):
    """Test stats retrieval."""
    manager = GamificationManager(temp_project_path)
    manager.award_insight(50.0)
    stats = manager.get_stats()
    assert "integrity" in stats
    assert "insight" in stats
    assert "level" in stats
    assert "achievements" in stats

