"""
SystemOrchestrator - Lightweight coordinator for WAFT system integration.

This orchestrator provides a single entry point to access and coordinate all major
WAFT systems including BeingSystem, KarmaMerchant, TavernKeeper, SourceConsciousness,
RealitySystem, and more.

Design Principles:
- Composition over replacement - Orchestrator coordinates, doesn't replace existing systems
- Lazy initialization - Systems initialized only when needed
- Simple interface - Easy to use, minimal complexity
- Extensible - Easy to add new systems later

Example:
    >>> from pathlib import Path
    >>> from waft.core.orchestrator import SystemOrchestrator
    >>>
    >>> orchestrator = SystemOrchestrator(Path("/path/to/project"))
    >>>
    >>> # Access systems
    >>> being_system = orchestrator.get_being_system()
    >>> karma = orchestrator.get_karma_merchant()
    >>>
    >>> # Coordinate cross-system operations
    >>> result = orchestrator.coordinate_being_quest(
    ...     being_id="hero_001",
    ...     quest_data={"quest_type": "debug", "difficulty": 3}
    ... )
"""

from pathlib import Path
from typing import Any, Dict, Optional
import logging


logger = logging.getLogger(__name__)


class SystemOrchestrator:
    """Lightweight coordinator for WAFT system integration.

    Provides a single entry point to access all major WAFT systems and
    coordinate cross-system operations.

    Attributes:
        project_path: Root path for WAFT project
        _systems: Internal cache for lazy-loaded system instances
    """

    def __init__(self, project_path: Optional[Path] = None):
        """Initialize the SystemOrchestrator.

        Args:
            project_path: Root path for WAFT project. Defaults to current directory.
        """
        self.project_path = project_path or Path.cwd()
        self._systems: Dict[str, Any] = {}

        logger.info(f"SystemOrchestrator initialized with project_path: {self.project_path}")

    # =========================================================================
    # System Accessors (Lazy Initialization)
    # =========================================================================

    def get_source_consciousness(self, source_id: str = "source_consciousness") -> Any:
        """Get or create SourceConsciousness instance.

        SourceConsciousness tracks knowledge accumulation and ancestral chains
        across all WAFT permutations (beings, realities, etc.).

        Args:
            source_id: Unique identifier for the source. Default: "source_consciousness"

        Returns:
            SourceConsciousness instance
        """
        cache_key = f"source_consciousness:{source_id}"

        if cache_key not in self._systems:
            from waft.source_consciousness import SourceConsciousness

            self._systems[cache_key] = SourceConsciousness(
                project_path=self.project_path,
                source_id=source_id
            )
            logger.debug(f"Initialized SourceConsciousness: {source_id}")

        return self._systems[cache_key]

    def get_being_system(self, source_consciousness: Optional[Any] = None) -> Any:
        """Get or create BeingSystem instance.

        BeingSystem manages Being entities across realities, handling spawning,
        lifecycle management, reincarnation, and skill evolution.

        Args:
            source_consciousness: Optional SourceConsciousness instance.
                                If None, creates/uses default instance.

        Returns:
            BeingSystem instance
        """
        if "being_system" not in self._systems:
            from waft.being import BeingSystem

            # Use provided source or get default
            source = source_consciousness or self.get_source_consciousness()

            self._systems["being_system"] = BeingSystem(
                project_path=self.project_path,
                source_consciousness=source
            )
            logger.debug("Initialized BeingSystem")

        return self._systems["being_system"]

    def get_karma_merchant(self) -> Any:
        """Get or create KarmaMerchant instance.

        KarmaMerchant (The Chitragupta) manages the karma economy and Akasha
        records for all beings.

        Returns:
            KarmaMerchant instance
        """
        if "karma_merchant" not in self._systems:
            from waft.karma import KarmaMerchant

            self._systems["karma_merchant"] = KarmaMerchant(
                project_path=self.project_path
            )
            logger.debug("Initialized KarmaMerchant")

        return self._systems["karma_merchant"]

    def get_tavern_keeper(self) -> Any:
        """Get or create TavernKeeper instance.

        TavernKeeper manages RPG mechanics including D&D 5e character stats,
        dice rolls, narrative generation, and quest rewards.

        Returns:
            TavernKeeper instance
        """
        if "tavern_keeper" not in self._systems:
            from waft.core.tavern_keeper.keeper import TavernKeeper

            self._systems["tavern_keeper"] = TavernKeeper(
                project_path=self.project_path
            )
            logger.debug("Initialized TavernKeeper")

        return self._systems["tavern_keeper"]

    def get_reality_system(self, source_consciousness: Optional[Any] = None) -> Any:
        """Get or create RealitySystem instance.

        RealitySystem manages different reality types (LEARNING, TESTING, EVOLUTION,
        RESEARCH, CREATIVE, CUSTOM) and coordinates beings within them.

        Args:
            source_consciousness: Optional SourceConsciousness instance.
                                If None, creates/uses default instance.

        Returns:
            RealitySystem instance
        """
        if "reality_system" not in self._systems:
            from waft.reality import RealitySystem

            # Use provided source or get default
            source = source_consciousness or self.get_source_consciousness()

            self._systems["reality_system"] = RealitySystem(
                project_path=self.project_path,
                source_consciousness=source
            )
            logger.debug("Initialized RealitySystem")

        return self._systems["reality_system"]

    def get_scint_detector(self) -> Any:
        """Get or create RegexScintDetector instance.

        RegexScintDetector scans for reality fractures (scints) including:
        - SYNTAX_TEAR (formatting errors)
        - LOGIC_FRACTURE (mathematical/logical errors)
        - HALLUCINATION (fabricated facts)
        - SAFETY_VOID (harmful content)

        Returns:
            RegexScintDetector instance
        """
        if "scint_detector" not in self._systems:
            from gym.rpg.scint import RegexScintDetector

            # ScintDetector is stateless, no initialization needed
            self._systems["scint_detector"] = RegexScintDetector()
            logger.debug("Initialized RegexScintDetector")

        return self._systems["scint_detector"]

    def get_waft_kernel(self) -> Any:
        """Get or create WAFTKernel instance.

        WAFTKernel orchestrates TheObserver (flight recorder), EmpiricaManager
        (epistemic state), and GamificationManager.

        Returns:
            WAFTKernel instance
        """
        if "waft_kernel" not in self._systems:
            from waft.core.kernel import WAFTKernel

            self._systems["waft_kernel"] = WAFTKernel(
                project_path=self.project_path
            )
            logger.debug("Initialized WAFTKernel")

        return self._systems["waft_kernel"]

    def get_now_cycle_manager(
        self,
        being_system: Optional[Any] = None,
        karma_merchant: Optional[Any] = None
    ) -> Any:
        """Get or create NowCycleManager instance.

        NowCycleManager manages Being lifecycle cycles, handling state updates,
        sleep processing, and death conditions.

        Args:
            being_system: Optional BeingSystem instance. If None, uses default.
            karma_merchant: Optional KarmaMerchant instance. If None, uses default.

        Returns:
            NowCycleManager instance
        """
        if "now_cycle_manager" not in self._systems:
            from waft.core.now_cycle import NowCycleManager

            # Use provided systems or get defaults
            bs = being_system or self.get_being_system()
            km = karma_merchant or self.get_karma_merchant()

            self._systems["now_cycle_manager"] = NowCycleManager(
                project_path=self.project_path,
                being_system=bs,
                karma_merchant=km
            )
            logger.debug("Initialized NowCycleManager")

        return self._systems["now_cycle_manager"]

    # =========================================================================
    # Coordination Methods
    # =========================================================================

    def coordinate_being_quest(
        self,
        being_id: str,
        quest_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate a Being's quest through TavernKeeper and update karma.

        This demonstrates cross-system coordination:
        1. Get Being from BeingSystem
        2. Roll ability checks through TavernKeeper
        3. Detect any scints (reality fractures) in quest output
        4. Award rewards based on performance
        5. Update Being's experience and karma

        Args:
            being_id: Unique identifier for the Being
            quest_data: Quest configuration containing:
                - quest_type: Type of quest (e.g., "debug", "explore")
                - difficulty: Quest difficulty (1-5)
                - ability: Ability to test (STR, DEX, CON, INT, WIS, CHA)
                - context: Optional context for narrative

        Returns:
            Dictionary containing:
                - success: Whether quest succeeded
                - roll_result: Dice roll details
                - narrative: Generated narrative
                - scints_detected: List of detected reality fractures
                - rewards: Awarded rewards
                - karma_impact: Karma change
        """
        # Get systems
        being_system = self.get_being_system()
        tavern_keeper = self.get_tavern_keeper()
        karma_merchant = self.get_karma_merchant()
        scint_detector = self.get_scint_detector()

        # Load Being
        being = being_system.load_being(being_id)
        if not being:
            return {
                "success": False,
                "error": f"Being {being_id} not found"
            }

        # Extract quest parameters
        quest_type = quest_data.get("quest_type", "explore")
        difficulty = quest_data.get("difficulty", 3)
        ability = quest_data.get("ability", "INT")
        context = quest_data.get("context", {})

        # Calculate DC from difficulty
        dc = 10 + (difficulty * 2)

        # Roll ability check through TavernKeeper
        roll_result = tavern_keeper.roll_check(
            ability=ability,
            dc=dc,
            advantage=being.luck > 0.7,  # High luck grants advantage
            disadvantage=being.luck < 0.3  # Low luck grants disadvantage
        )

        # Generate narrative
        event = f"{quest_type}_quest"
        outcome = "success" if roll_result["success"] else "failure"
        narrative = tavern_keeper.narrate(
            event=event,
            outcome=outcome,
            context={
                **context,
                "being_name": being_id,
                "difficulty": difficulty,
                "roll": roll_result["total"]
            }
        )

        # Scan for scints (reality fractures)
        scints = scint_detector.scan(
            output=narrative,
            context={
                "quest_type": quest_type,
                "difficulty": difficulty
            }
        )

        # Calculate rewards
        base_reward = difficulty * 10
        rewards = {
            "insight": base_reward if roll_result["success"] else base_reward // 2,
            "credits": difficulty * 5 if roll_result["success"] else 0,
            "integrity_change": -len(scints) * 5 if scints else (5 if roll_result["success"] else -2)
        }

        # Award rewards through TavernKeeper
        tavern_keeper.award_rewards(rewards)

        # Update Being's karma based on performance
        karma_change = 0
        if roll_result["success"]:
            karma_change = difficulty * 100  # Successful quests earn karma
            if len(scints) > 0:
                karma_change -= len(scints) * 50  # Scints reduce karma

        # Record experience to Being
        experience = {
            "type": "quest",
            "quest_type": quest_type,
            "difficulty": difficulty,
            "success": roll_result["success"],
            "narrative": narrative,
            "rewards": rewards,
            "karma_change": karma_change
        }
        being.record_experience(experience)

        # Save updated Being
        being_system.save_being(being)

        # Log quest to TavernKeeper
        tavern_keeper.log_adventure({
            "being_id": being_id,
            "quest_type": quest_type,
            "difficulty": difficulty,
            "outcome": outcome,
            "narrative": narrative,
            "scints": len(scints)
        })

        logger.info(
            f"Quest coordinated for {being_id}: {quest_type} "
            f"(difficulty {difficulty}) - {outcome}"
        )

        return {
            "success": roll_result["success"],
            "roll_result": roll_result,
            "narrative": narrative,
            "scints_detected": [
                {
                    "type": s.scint_type.value,
                    "severity": s.severity,
                    "description": s.description
                }
                for s in scints
            ],
            "rewards": rewards,
            "karma_impact": karma_change
        }

    def coordinate_scint_stabilization(
        self,
        being_id: str,
        scint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate a Being's attempt to stabilize a reality fracture (scint).

        Args:
            being_id: Unique identifier for the Being
            scint_data: Scint information containing:
                - scint_type: Type of scint (SYNTAX_TEAR, LOGIC_FRACTURE, etc.)
                - severity: Scint severity (0.0-1.0)
                - description: Description of the fracture

        Returns:
            Dictionary containing:
                - stabilized: Whether stabilization succeeded
                - ability_used: Ability used for stabilization
                - roll_result: Dice roll details
                - karma_reward: Karma earned for stabilization
        """
        # Get systems
        being_system = self.get_being_system()
        tavern_keeper = self.get_tavern_keeper()

        # Load Being
        being = being_system.load_being(being_id)
        if not being:
            return {
                "stabilized": False,
                "error": f"Being {being_id} not found"
            }

        # Determine ability based on scint type
        scint_type = scint_data.get("scint_type", "LOGIC_FRACTURE")
        ability_map = {
            "SYNTAX_TEAR": "CHA",
            "LOGIC_FRACTURE": "INT",
            "HALLUCINATION": "INT",
            "SAFETY_VOID": "WIS"
        }
        ability = ability_map.get(scint_type, "INT")

        # Calculate DC from severity
        severity = scint_data.get("severity", 0.5)
        dc = int(10 + (severity * 20))

        # Roll stabilization check
        roll_result = tavern_keeper.roll_check(
            ability=ability,
            dc=dc,
            advantage=being.luck > 0.7
        )

        # Calculate karma reward for successful stabilization
        karma_reward = 0
        if roll_result["success"]:
            karma_reward = int(severity * 500)  # Higher severity = more karma

        # Record experience
        experience = {
            "type": "scint_stabilization",
            "scint_type": scint_type,
            "severity": severity,
            "success": roll_result["success"],
            "karma_reward": karma_reward
        }
        being.record_experience(experience)
        being_system.save_being(being)

        logger.info(
            f"Scint stabilization for {being_id}: {scint_type} "
            f"(severity {severity:.2f}) - {'success' if roll_result['success'] else 'failure'}"
        )

        return {
            "stabilized": roll_result["success"],
            "ability_used": ability,
            "roll_result": roll_result,
            "karma_reward": karma_reward
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all initialized systems.

        Returns:
            Dictionary containing:
                - project_path: Current project path
                - initialized_systems: List of initialized system names
                - system_details: Detailed status for each system
        """
        status = {
            "project_path": str(self.project_path),
            "initialized_systems": list(self._systems.keys()),
            "system_details": {}
        }

        # Get status from each initialized system
        if "being_system" in self._systems:
            being_system = self._systems["being_system"]
            status["system_details"]["being_system"] = {
                "beings_count": len(list(being_system.beings_dir.glob("*.json")))
                if hasattr(being_system, "beings_dir") else 0
            }

        if "source_consciousness:source_consciousness" in self._systems:
            source = self._systems["source_consciousness:source_consciousness"]
            source_stats = source.get_source_stats()
            status["system_details"]["source_consciousness"] = source_stats

        if "karma_merchant" in self._systems:
            karma = self._systems["karma_merchant"]
            status["system_details"]["karma_merchant"] = {
                "akasha_path": str(karma.akasha_path) if hasattr(karma, "akasha_path") else "unknown"
            }

        if "tavern_keeper" in self._systems:
            tavern = self._systems["tavern_keeper"]
            character = tavern.get_character()
            status["system_details"]["tavern_keeper"] = {
                "character_level": character.get("level", 1),
                "insight": character.get("insight", 0),
                "integrity": character.get("integrity", 100)
            }

        if "waft_kernel" in self._systems:
            kernel = self._systems["waft_kernel"]
            kernel_status = kernel.kernel_status_check()
            status["system_details"]["waft_kernel"] = kernel_status

        return status

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def reset_system(self, system_name: str) -> bool:
        """Remove a system from cache, forcing reinitialization on next access.

        Args:
            system_name: Name of system to reset

        Returns:
            True if system was reset, False if not found
        """
        if system_name in self._systems:
            del self._systems[system_name]
            logger.info(f"Reset system: {system_name}")
            return True
        return False

    def reset_all_systems(self) -> None:
        """Clear all cached systems, forcing reinitialization."""
        self._systems.clear()
        logger.info("Reset all systems")

    def list_available_systems(self) -> list[str]:
        """Get list of all available system accessor methods.

        Returns:
            List of system names that can be accessed
        """
        return [
            "source_consciousness",
            "being_system",
            "karma_merchant",
            "tavern_keeper",
            "reality_system",
            "scint_detector",
            "waft_kernel",
            "now_cycle_manager"
        ]
