"""
Achievement System: Gamification Layer for Evolution.

Tracks accomplishments, unlocks badges, and rewards evolutionary progress.
Because evolution should feel LEGENDARY.

"Every mutation is a step toward greatness."
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4


class AchievementRarity(str, Enum):
    """Rarity levels for achievements."""
    
    COMMON = "common"           # Easy to get
    UNCOMMON = "uncommon"       # Some effort required
    RARE = "rare"               # Notable accomplishment
    EPIC = "epic"               # Significant achievement
    LEGENDARY = "legendary"     # Exceptional feat
    MYTHIC = "mythic"           # Near impossible


class AchievementCategory(str, Enum):
    """Categories of achievements."""
    
    EVOLUTION = "evolution"     # Genome evolution milestones
    COMBAT = "combat"           # Battle royale achievements
    BREEDING = "breeding"       # Genetic crossover achievements
    EXPLORATION = "exploration" # Discovering new traits
    MASTERY = "mastery"         # Skill-based achievements
    SOCIAL = "social"           # Community/sharing achievements
    SECRET = "secret"           # Hidden achievements


@dataclass
class Achievement:
    """An unlockable achievement."""
    
    id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    icon: str  # Emoji icon
    points: int  # XP value
    condition: str  # Human-readable unlock condition
    secret: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "rarity": self.rarity.value,
            "icon": self.icon,
            "points": self.points,
            "condition": self.condition,
            "secret": self.secret,
        }


@dataclass
class UnlockedAchievement:
    """Record of an unlocked achievement."""
    
    achievement: Achievement
    unlocked_at: datetime
    context: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "achievement": self.achievement.to_dict(),
            "unlocked_at": self.unlocked_at.isoformat(),
            "context": self.context,
        }


# ============================================================================
# ACHIEVEMENT DEFINITIONS
# ============================================================================

ACHIEVEMENTS: dict[str, Achievement] = {
    # Evolution Achievements
    "first_mutation": Achievement(
        id="first_mutation",
        name="First Steps",
        description="Apply your first mutation to a genome",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.COMMON,
        icon="🧬",
        points=10,
        condition="Mutate a genome once",
    ),
    "evolution_chain_5": Achievement(
        id="evolution_chain_5",
        name="Evolutionary Chain",
        description="Create a lineage of 5 generations",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.UNCOMMON,
        icon="🔗",
        points=25,
        condition="Have 5 generations in a single lineage",
    ),
    "evolution_chain_10": Achievement(
        id="evolution_chain_10",
        name="Deep Ancestry",
        description="Create a lineage of 10 generations",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.RARE,
        icon="🌳",
        points=50,
        condition="Have 10 generations in a single lineage",
    ),
    "perfect_fitness": Achievement(
        id="perfect_fitness",
        name="Perfection",
        description="Achieve a perfect fitness score of 1.0",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.LEGENDARY,
        icon="⭐",
        points=200,
        condition="Reach fitness score 1.0",
    ),
    "fitness_80": Achievement(
        id="fitness_80",
        name="High Achiever",
        description="Reach 80% fitness score",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.RARE,
        icon="📈",
        points=50,
        condition="Reach fitness score 0.8",
    ),
    "survivor": Achievement(
        id="survivor",
        name="Survivor",
        description="Have a genome survive 50 mutations without dying",
        category=AchievementCategory.EVOLUTION,
        rarity=AchievementRarity.EPIC,
        icon="🛡️",
        points=100,
        condition="50 consecutive mutations survived",
    ),
    
    # Combat Achievements
    "first_blood": Achievement(
        id="first_blood",
        name="First Blood",
        description="Win your first battle",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.COMMON,
        icon="⚔️",
        points=10,
        condition="Win a battle",
    ),
    "battle_veteran": Achievement(
        id="battle_veteran",
        name="Battle Veteran",
        description="Win 10 battles",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.UNCOMMON,
        icon="🎖️",
        points=30,
        condition="Win 10 battles",
    ),
    "champion": Achievement(
        id="champion",
        name="Champion",
        description="Win 50 battles",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.RARE,
        icon="🏆",
        points=75,
        condition="Win 50 battles",
    ),
    "legend": Achievement(
        id="legend",
        name="Legend",
        description="Win 100 battles",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.EPIC,
        icon="👑",
        points=150,
        condition="Win 100 battles",
    ),
    "godslayer": Achievement(
        id="godslayer",
        name="Godslayer",
        description="Defeat a genome with perfect fitness",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.LEGENDARY,
        icon="💀",
        points=250,
        condition="Defeat a genome with fitness 1.0",
    ),
    "flawless_victory": Achievement(
        id="flawless_victory",
        name="Flawless Victory",
        description="Win a battle without taking damage",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.EPIC,
        icon="✨",
        points=100,
        condition="Win with 100% health",
    ),
    "underdog": Achievement(
        id="underdog",
        name="Underdog",
        description="Win a battle against a genome with higher fitness",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.UNCOMMON,
        icon="🐕",
        points=35,
        condition="Beat a stronger opponent",
    ),
    "comeback_king": Achievement(
        id="comeback_king",
        name="Comeback King",
        description="Win a battle after falling below 10% health",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.RARE,
        icon="🔥",
        points=60,
        condition="Win from near death",
    ),
    "tournament_winner": Achievement(
        id="tournament_winner",
        name="Tournament Champion",
        description="Win a full tournament",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.RARE,
        icon="🥇",
        points=80,
        condition="Win a tournament",
    ),
    
    # Breeding Achievements
    "first_breed": Achievement(
        id="first_breed",
        name="Matchmaker",
        description="Perform your first genetic crossover",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.COMMON,
        icon="💕",
        points=10,
        condition="Breed two genomes",
    ),
    "prolific_breeder": Achievement(
        id="prolific_breeder",
        name="Prolific Breeder",
        description="Perform 25 crossover operations",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.UNCOMMON,
        icon="🐰",
        points=30,
        condition="25 crossover operations",
    ),
    "master_breeder": Achievement(
        id="master_breeder",
        name="Master Breeder",
        description="Perform 100 crossover operations",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.RARE,
        icon="🧪",
        points=60,
        condition="100 crossover operations",
    ),
    "super_offspring": Achievement(
        id="super_offspring",
        name="Super Offspring",
        description="Create an offspring with higher fitness than both parents",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.UNCOMMON,
        icon="🌟",
        points=40,
        condition="Offspring exceeds parents",
    ),
    "genetic_diversity": Achievement(
        id="genetic_diversity",
        name="Genetic Diversity",
        description="Use all 7 crossover strategies",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.RARE,
        icon="🧬",
        points=50,
        condition="Try all crossover strategies",
    ),
    "dynasty": Achievement(
        id="dynasty",
        name="Dynasty",
        description="Have 100 descendants from a single genome",
        category=AchievementCategory.BREEDING,
        rarity=AchievementRarity.EPIC,
        icon="👨‍👩‍👧‍👦",
        points=120,
        condition="100 descendants from one genome",
    ),
    
    # Exploration Achievements
    "trait_hunter": Achievement(
        id="trait_hunter",
        name="Trait Hunter",
        description="Discover 10 unique trait combinations",
        category=AchievementCategory.EXPLORATION,
        rarity=AchievementRarity.UNCOMMON,
        icon="🔍",
        points=25,
        condition="10 unique trait combos",
    ),
    "color_master": Achievement(
        id="color_master",
        name="Color Master",
        description="Create genomes with 50 unique color schemes",
        category=AchievementCategory.EXPLORATION,
        rarity=AchievementRarity.RARE,
        icon="🎨",
        points=45,
        condition="50 unique color schemes",
    ),
    "font_connoisseur": Achievement(
        id="font_connoisseur",
        name="Font Connoisseur",
        description="Use 20 different font combinations",
        category=AchievementCategory.EXPLORATION,
        rarity=AchievementRarity.UNCOMMON,
        icon="📝",
        points=30,
        condition="20 different fonts",
    ),
    "scint_detector": Achievement(
        id="scint_detector",
        name="SCINT Detector",
        description="Detect your first Style-Conflict-In-Need-of-Treatment",
        category=AchievementCategory.EXPLORATION,
        rarity=AchievementRarity.COMMON,
        icon="🔬",
        points=15,
        condition="Detect a SCINT",
    ),
    
    # Mastery Achievements
    "speed_demon": Achievement(
        id="speed_demon",
        name="Speed Demon",
        description="Evolve a genome to 80% fitness in under 10 generations",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.EPIC,
        icon="⚡",
        points=100,
        condition="80% fitness in <10 generations",
    ),
    "geneticist": Achievement(
        id="geneticist",
        name="Master Geneticist",
        description="Reach level 10 in the evolution system",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.RARE,
        icon="🔬",
        points=75,
        condition="Reach level 10",
    ),
    "perfectionist": Achievement(
        id="perfectionist",
        name="Perfectionist",
        description="Create 10 genomes with fitness above 0.9",
        category=AchievementCategory.MASTERY,
        rarity=AchievementRarity.EPIC,
        icon="💯",
        points=125,
        condition="10 high-fitness genomes",
    ),
    
    # Secret Achievements
    "midnight_mutator": Achievement(
        id="midnight_mutator",
        name="Midnight Mutator",
        description="Perform a mutation at exactly midnight",
        category=AchievementCategory.SECRET,
        rarity=AchievementRarity.RARE,
        icon="🌙",
        points=50,
        condition="???",
        secret=True,
    ),
    "lucky_seven": Achievement(
        id="lucky_seven",
        name="Lucky Seven",
        description="Create a genome on the 7th day with generation 7",
        category=AchievementCategory.SECRET,
        rarity=AchievementRarity.RARE,
        icon="🎰",
        points=77,
        condition="???",
        secret=True,
    ),
    "phoenix": Achievement(
        id="phoenix",
        name="Phoenix",
        description="Revive a dead genome through breeding",
        category=AchievementCategory.SECRET,
        rarity=AchievementRarity.EPIC,
        icon="🔥",
        points=100,
        condition="???",
        secret=True,
    ),
    "the_one": Achievement(
        id="the_one",
        name="The One",
        description="Create genome #1000",
        category=AchievementCategory.SECRET,
        rarity=AchievementRarity.LEGENDARY,
        icon="1️⃣",
        points=200,
        condition="???",
        secret=True,
    ),
    "god_mode": Achievement(
        id="god_mode",
        name="God Mode",
        description="Win 10 battles in a row without losing health",
        category=AchievementCategory.SECRET,
        rarity=AchievementRarity.MYTHIC,
        icon="🌌",
        points=500,
        condition="???",
        secret=True,
    ),
}


class AchievementTracker:
    """
    Tracks and manages achievement progress and unlocks.
    
    The gamification layer that makes evolution feel EPIC.
    """
    
    def __init__(self, save_path: Path | None = None):
        """
        Initialize the achievement tracker.
        
        Args:
            save_path: Optional path to persist achievements
        """
        self.save_path = save_path or Path("_pyrite/achievements.json")
        self.unlocked: dict[str, UnlockedAchievement] = {}
        self.progress: dict[str, dict[str, Any]] = {}
        self.total_points: int = 0
        self.level: int = 1
        self.callbacks: list[Callable[[UnlockedAchievement], None]] = []
        
        # Load existing achievements
        self._load()
    
    def _load(self):
        """Load achievements from disk."""
        if self.save_path.exists():
            try:
                data = json.loads(self.save_path.read_text())
                self.total_points = data.get("total_points", 0)
                self.level = data.get("level", 1)
                self.progress = data.get("progress", {})
                
                for unlock_data in data.get("unlocked", []):
                    achievement_id = unlock_data["achievement"]["id"]
                    if achievement_id in ACHIEVEMENTS:
                        self.unlocked[achievement_id] = UnlockedAchievement(
                            achievement=ACHIEVEMENTS[achievement_id],
                            unlocked_at=datetime.fromisoformat(unlock_data["unlocked_at"]),
                            context=unlock_data.get("context", {}),
                        )
            except Exception:
                pass
    
    def _save(self):
        """Save achievements to disk."""
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "total_points": self.total_points,
            "level": self.level,
            "progress": self.progress,
            "unlocked": [u.to_dict() for u in self.unlocked.values()],
        }
        self.save_path.write_text(json.dumps(data, indent=2))
    
    def unlock(
        self,
        achievement_id: str,
        context: dict[str, Any] | None = None,
    ) -> UnlockedAchievement | None:
        """
        Unlock an achievement.
        
        Args:
            achievement_id: ID of achievement to unlock
            context: Optional context about the unlock
            
        Returns:
            UnlockedAchievement if newly unlocked, None if already unlocked
        """
        if achievement_id in self.unlocked:
            return None  # Already unlocked
        
        if achievement_id not in ACHIEVEMENTS:
            return None  # Invalid achievement
        
        achievement = ACHIEVEMENTS[achievement_id]
        unlock = UnlockedAchievement(
            achievement=achievement,
            unlocked_at=datetime.utcnow(),
            context=context or {},
        )
        
        self.unlocked[achievement_id] = unlock
        self.total_points += achievement.points
        self._update_level()
        self._save()
        
        # Fire callbacks
        for callback in self.callbacks:
            try:
                callback(unlock)
            except Exception:
                pass
        
        return unlock
    
    def _update_level(self):
        """Update level based on total points."""
        # Level formula: each level requires more points
        # Level 1: 0, Level 2: 50, Level 3: 150, Level 4: 300, etc.
        points_needed = 0
        level = 1
        while self.total_points >= points_needed:
            level += 1
            points_needed += level * 50
        self.level = level - 1
    
    def get_progress(self, achievement_id: str) -> dict[str, Any]:
        """Get progress toward an achievement."""
        return self.progress.get(achievement_id, {})
    
    def update_progress(
        self,
        achievement_id: str,
        progress_data: dict[str, Any],
    ):
        """Update progress toward an achievement."""
        self.progress[achievement_id] = {
            **self.progress.get(achievement_id, {}),
            **progress_data,
        }
        self._save()
    
    def check_and_unlock(
        self,
        event_type: str,
        event_data: dict[str, Any],
    ) -> list[UnlockedAchievement]:
        """
        Check if any achievements should be unlocked based on an event.
        
        Args:
            event_type: Type of event (mutation, battle_win, breed, etc.)
            event_data: Data about the event
            
        Returns:
            List of newly unlocked achievements
        """
        unlocked = []
        
        # Mutation events
        if event_type == "mutation":
            if u := self.unlock("first_mutation", event_data):
                unlocked.append(u)
            
            # Check midnight mutator
            if datetime.now().hour == 0 and datetime.now().minute == 0:
                if u := self.unlock("midnight_mutator", event_data):
                    unlocked.append(u)
        
        # Battle events
        elif event_type == "battle_win":
            wins = self.progress.get("battle_wins", {"count": 0})["count"] + 1
            self.update_progress("battle_wins", {"count": wins})
            
            if wins >= 1:
                if u := self.unlock("first_blood", event_data):
                    unlocked.append(u)
            if wins >= 10:
                if u := self.unlock("battle_veteran", event_data):
                    unlocked.append(u)
            if wins >= 50:
                if u := self.unlock("champion", event_data):
                    unlocked.append(u)
            if wins >= 100:
                if u := self.unlock("legend", event_data):
                    unlocked.append(u)
            
            # Check flawless victory
            if event_data.get("damage_taken", 1) == 0:
                if u := self.unlock("flawless_victory", event_data):
                    unlocked.append(u)
            
            # Check underdog
            if event_data.get("winner_fitness", 0) < event_data.get("loser_fitness", 0):
                if u := self.unlock("underdog", event_data):
                    unlocked.append(u)
            
            # Check comeback king
            if event_data.get("min_health_percent", 1) < 0.1:
                if u := self.unlock("comeback_king", event_data):
                    unlocked.append(u)
            
            # Check godslayer
            if event_data.get("loser_fitness") == 1.0:
                if u := self.unlock("godslayer", event_data):
                    unlocked.append(u)
        
        # Breeding events
        elif event_type == "breed":
            breeds = self.progress.get("breed_count", {"count": 0})["count"] + 1
            self.update_progress("breed_count", {"count": breeds})
            
            if breeds >= 1:
                if u := self.unlock("first_breed", event_data):
                    unlocked.append(u)
            if breeds >= 25:
                if u := self.unlock("prolific_breeder", event_data):
                    unlocked.append(u)
            if breeds >= 100:
                if u := self.unlock("master_breeder", event_data):
                    unlocked.append(u)
            
            # Check super offspring
            offspring_fitness = event_data.get("offspring_fitness", 0)
            parent_a_fitness = event_data.get("parent_a_fitness", 1)
            parent_b_fitness = event_data.get("parent_b_fitness", 1)
            if offspring_fitness > max(parent_a_fitness, parent_b_fitness):
                if u := self.unlock("super_offspring", event_data):
                    unlocked.append(u)
            
            # Track strategies used
            strategies_used = set(self.progress.get("strategies_used", {}).get("list", []))
            strategies_used.add(event_data.get("strategy", ""))
            self.update_progress("strategies_used", {"list": list(strategies_used)})
            if len(strategies_used) >= 7:
                if u := self.unlock("genetic_diversity", event_data):
                    unlocked.append(u)
        
        # Fitness events
        elif event_type == "fitness_update":
            fitness = event_data.get("fitness", 0)
            
            if fitness >= 0.8:
                if u := self.unlock("fitness_80", event_data):
                    unlocked.append(u)
            if fitness >= 1.0:
                if u := self.unlock("perfect_fitness", event_data):
                    unlocked.append(u)
        
        # Generation events
        elif event_type == "generation":
            generation = event_data.get("generation", 0)
            
            if generation >= 5:
                if u := self.unlock("evolution_chain_5", event_data):
                    unlocked.append(u)
            if generation >= 10:
                if u := self.unlock("evolution_chain_10", event_data):
                    unlocked.append(u)
        
        # SCINT detection
        elif event_type == "scint_detected":
            if u := self.unlock("scint_detector", event_data):
                unlocked.append(u)
        
        # Tournament events
        elif event_type == "tournament_win":
            if u := self.unlock("tournament_winner", event_data):
                unlocked.append(u)
        
        return unlocked
    
    def on_unlock(self, callback: Callable[[UnlockedAchievement], None]):
        """Register a callback for when achievements are unlocked."""
        self.callbacks.append(callback)
    
    def get_all_achievements(self) -> list[Achievement]:
        """Get all achievements."""
        return list(ACHIEVEMENTS.values())
    
    def get_unlocked(self) -> list[UnlockedAchievement]:
        """Get all unlocked achievements."""
        return list(self.unlocked.values())
    
    def get_locked(self) -> list[Achievement]:
        """Get all locked achievements."""
        return [a for a in ACHIEVEMENTS.values() if a.id not in self.unlocked]
    
    def get_stats(self) -> dict[str, Any]:
        """Get achievement statistics."""
        total = len(ACHIEVEMENTS)
        unlocked = len(self.unlocked)
        
        # Points by rarity
        points_by_rarity = {}
        for achievement in ACHIEVEMENTS.values():
            rarity = achievement.rarity.value
            if rarity not in points_by_rarity:
                points_by_rarity[rarity] = {"total": 0, "earned": 0}
            points_by_rarity[rarity]["total"] += achievement.points
            if achievement.id in self.unlocked:
                points_by_rarity[rarity]["earned"] += achievement.points
        
        # Category completion
        category_completion = {}
        for category in AchievementCategory:
            cat_achievements = [a for a in ACHIEVEMENTS.values() if a.category == category]
            cat_unlocked = [a for a in cat_achievements if a.id in self.unlocked]
            category_completion[category.value] = {
                "total": len(cat_achievements),
                "unlocked": len(cat_unlocked),
                "percent": len(cat_unlocked) / len(cat_achievements) * 100 if cat_achievements else 0,
            }
        
        return {
            "total_achievements": total,
            "unlocked_achievements": unlocked,
            "completion_percent": unlocked / total * 100 if total else 0,
            "total_points": self.total_points,
            "max_points": sum(a.points for a in ACHIEVEMENTS.values()),
            "level": self.level,
            "points_by_rarity": points_by_rarity,
            "category_completion": category_completion,
        }
    
    def generate_report(self) -> str:
        """Generate achievement report."""
        stats = self.get_stats()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🏆 ACHIEVEMENT REPORT 🏆                    ║
╠══════════════════════════════════════════════════════════════╣
║  Level: {self.level} | Points: {self.total_points}/{stats['max_points']}
║  Unlocked: {stats['unlocked_achievements']}/{stats['total_achievements']} ({stats['completion_percent']:.1f}%)
║
║  RECENT UNLOCKS:
"""
        
        recent = sorted(
            self.unlocked.values(),
            key=lambda u: u.unlocked_at,
            reverse=True,
        )[:5]
        
        for unlock in recent:
            a = unlock.achievement
            report += f"║    {a.icon} {a.name} ({a.rarity.value}) +{a.points}pts\n"
        
        report += """║
║  CATEGORY PROGRESS:
"""
        
        for category, data in stats["category_completion"].items():
            bar_filled = int(data["percent"] / 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            report += f"║    {category}: [{bar}] {data['unlocked']}/{data['total']}\n"
        
        report += "╚══════════════════════════════════════════════════════════════╝"
        
        return report


# Global tracker instance
_tracker: AchievementTracker | None = None


def get_tracker() -> AchievementTracker:
    """Get the global achievement tracker."""
    global _tracker
    if _tracker is None:
        _tracker = AchievementTracker()
    return _tracker


def track_event(event_type: str, event_data: dict[str, Any]) -> list[UnlockedAchievement]:
    """
    Track an event and check for achievement unlocks.
    
    Args:
        event_type: Type of event
        event_data: Event data
        
    Returns:
        List of newly unlocked achievements
    """
    return get_tracker().check_and_unlock(event_type, event_data)
