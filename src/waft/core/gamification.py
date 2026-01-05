"""
Gamification Manager - Constructivist Sci-Fi theme.

Manages Integrity (structural stability), Insight (verified knowledge),
Moon Phase (epistemic clock), and Leveling system.
"""

import json
import math
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class GamificationManager:
    """Manages gamification system with Constructivist Sci-Fi terminology."""
    
    def __init__(self, project_path: Path):
        """
        Initialize the GamificationManager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.data_path = project_path / "_pyrite" / ".waft" / "gamification.json"
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load gamification data from file."""
        if self.data_path.exists():
            try:
                with open(self.data_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default data
        return {
            "integrity": 100.0,
            "insight": 0.0,
            "level": 1,
            "achievements": [],
            "history": [],
            "created_at": datetime.now().isoformat(),
        }
    
    def _save_data(self) -> None:
        """Save gamification data to file."""
        self._data["updated_at"] = datetime.now().isoformat()
        with open(self.data_path, "w") as f:
            json.dump(self._data, f, indent=2)
    
    @property
    def integrity(self) -> float:
        """Get current integrity value."""
        return self._data.get("integrity", 100.0)
    
    @property
    def insight(self) -> float:
        """Get current insight value."""
        return self._data.get("insight", 0.0)
    
    @property
    def level(self) -> int:
        """Calculate current level from insight."""
        insight = self.insight
        if insight <= 0:
            return 1
        # Level = sqrt(Insight / 100)
        level = int(math.sqrt(insight / 100)) + 1
        return max(1, level)
    
    @property
    def achievements(self) -> List[str]:
        """Get list of unlocked achievements."""
        return self._data.get("achievements", [])
    
    def damage_integrity(self, amount: float, reason: str = "") -> float:
        """
        Decrease integrity (e.g., from errors, failed tests).
        
        Args:
            amount: Amount to decrease (positive number)
            reason: Optional reason for damage
            
        Returns:
            New integrity value
        """
        current = self.integrity
        new_integrity = max(0.0, current - amount)
        self._data["integrity"] = new_integrity
        
        # Log to history
        self._data.setdefault("history", []).append({
            "timestamp": datetime.now().isoformat(),
            "type": "integrity_damage",
            "amount": -amount,
            "reason": reason,
            "integrity_before": current,
            "integrity_after": new_integrity,
        })
        
        self._save_data()
        return new_integrity
    
    def restore_integrity(self, amount: float, reason: str = "") -> float:
        """
        Increase integrity (e.g., from successful operations).
        
        Args:
            amount: Amount to increase (positive number)
            reason: Optional reason for restoration
            
        Returns:
            New integrity value
        """
        current = self.integrity
        new_integrity = min(100.0, current + amount)
        self._data["integrity"] = new_integrity
        
        # Log to history
        self._data.setdefault("history", []).append({
            "timestamp": datetime.now().isoformat(),
            "type": "integrity_restore",
            "amount": amount,
            "reason": reason,
            "integrity_before": current,
            "integrity_after": new_integrity,
        })
        
        self._save_data()
        return new_integrity
    
    def award_insight(self, amount: float, reason: str = "") -> Dict[str, Any]:
        """
        Award insight (verified knowledge).
        
        Args:
            amount: Amount of insight to award
            reason: Optional reason for award
            
        Returns:
            Dictionary with level_up flag and new values
        """
        old_level = self.level
        old_insight = self.insight
        
        new_insight = old_insight + amount
        self._data["insight"] = new_insight
        
        new_level = self.level
        level_up = new_level > old_level
        
        # Log to history
        self._data.setdefault("history", []).append({
            "timestamp": datetime.now().isoformat(),
            "type": "insight_award",
            "amount": amount,
            "reason": reason,
            "insight_before": old_insight,
            "insight_after": new_insight,
            "level_before": old_level,
            "level_after": new_level,
            "level_up": level_up,
        })
        
        self._save_data()
        
        return {
            "level_up": level_up,
            "old_level": old_level,
            "new_level": new_level,
            "old_insight": old_insight,
            "new_insight": new_insight,
        }
    
    def unlock_achievement(self, achievement_id: str, achievement_name: str) -> bool:
        """
        Unlock an achievement.
        
        Args:
            achievement_id: Unique achievement identifier
            achievement_name: Display name of achievement
            
        Returns:
            True if newly unlocked, False if already unlocked
        """
        achievements = self.achievements
        if achievement_id in achievements:
            return False
        
        achievements.append(achievement_id)
        self._data["achievements"] = achievements
        
        # Log to history
        self._data.setdefault("history", []).append({
            "timestamp": datetime.now().isoformat(),
            "type": "achievement_unlocked",
            "achievement_id": achievement_id,
            "achievement_name": achievement_name,
        })
        
        self._save_data()
        return True
    
    def get_achievement_status(self) -> Dict[str, bool]:
        """
        Get status of all achievements (locked/unlocked).
        
        Returns:
            Dictionary mapping achievement_id to unlocked status
        """
        unlocked = set(self.achievements)
        
        # Define all achievements
        all_achievements = {
            "first_build": "🌱 First Build",
            "constructor": "🏗️ Constructor",
            "goal_achiever": "🎯 Goal Achiever",
            "knowledge_architect": "🧠 Knowledge Architect",
            "perfect_integrity": "💎 Perfect Integrity",
            "level_10": "🚀 Level 10",
            "master_constructor": "🏆 Master Constructor",
            "epistemic_master": "🌙 Epistemic Master",
        }
        
        return {
            achievement_id: achievement_id in unlocked
            for achievement_id in all_achievements.keys()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get current stats.
        
        Returns:
            Dictionary with all current stats
        """
        return {
            "integrity": self.integrity,
            "insight": self.insight,
            "level": self.level,
            "achievements_count": len(self.achievements),
            "achievements": self.achievements,
        }
    
    def get_insight_to_next_level(self) -> float:
        """
        Calculate insight needed to reach next level.
        
        Returns:
            Insight points needed
        """
        current_level = self.level
        next_level = current_level + 1
        
        # Insight for level N = (N-1)^2 * 100
        insight_for_next = (next_level - 1) ** 2 * 100
        insight_needed = insight_for_next - self.insight
        
        return max(0.0, insight_needed)
    
    def check_achievements(self, stats: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Check and unlock achievements based on current stats.
        
        Args:
            stats: Optional stats dictionary (uses current if not provided)
            
        Returns:
            List of newly unlocked achievement IDs
        """
        if stats is None:
            stats = self.get_stats()
        
        newly_unlocked = []
        
        # Check achievements
        insight = stats.get("insight", self.insight)
        level = stats.get("level", self.level)
        integrity = stats.get("integrity", self.integrity)
        
        # First Build - checked externally (when project created)
        # Constructor - checked externally (when 10 projects created)
        # Goal Achiever - checked externally (when 10 goals completed)
        # Knowledge Architect - checked externally (when 50 findings logged)
        
        # Perfect Integrity
        if integrity >= 100.0:
            if self.unlock_achievement("perfect_integrity", "💎 Perfect Integrity"):
                newly_unlocked.append("perfect_integrity")
        
        # Level 10
        if level >= 10:
            if self.unlock_achievement("level_10", "🚀 Level 10"):
                newly_unlocked.append("level_10")
        
        return newly_unlocked

