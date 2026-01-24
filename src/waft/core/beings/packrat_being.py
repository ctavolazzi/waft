"""
The Packrat Being - A timeful Being that collects research and learning data.

The Packrat is a rickety, mole-like creature with large spectacles, carrying
everything it's ever learned "just in case" and making noise as it works.

NOW: The Packrat uses PocketBase API instead of files - it's a microservice!
"""
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Any

from ...being import Being, BeingSystem
from ...reality import RealitySystem, RealityType
from ..daily_learning.collectors import (
    EmpiricaCollector,
    ChroniclerCollector,
    SessionAnalyticsCollector,
)
from ..realms.server import RealmServer
from ..inventory.client import PocketBaseInventory

logger = logging.getLogger("ThePackrat")


class PackratBeing:
    """
    A specific embodiment of a Being focused on collection.

    Wraps a generic Being instance for lifecycle management.
    The Packrat collects data throughout the day and takes it to
    The Librarian and The Scribe for organization and report generation.
    """

    def __init__(self, project_path: Path, realm_path: Path):
        """
        Initialize The Packrat Being.

        NOW: Starts PocketBase server and uses API instead of files!

        Args:
            project_path: Path to project root
            realm_path: Path to Daily Learning Realm
        """
        self.project_path = Path(project_path).resolve()
        self.realm_path = Path(realm_path).resolve()

        # Start RealmServer (PocketBase server for this Realm)
        self.realm_server = RealmServer(
            realm_name="daily_learning_realm",
            project_path=self.project_path,
            lazy=False,  # Start immediately - this is Packrat's home
        )
        
        # CRITICAL: Start server (bootstrap runs automatically if needed)
        if not self.realm_server.start():
            raise RuntimeError(
                f"Failed to start Daily Learning Realm server on port {self.realm_server.port}.\n"
                f"Check logs: {self.realm_server.realm_path / 'pocketbase.log'}\n"
                f"If port is in use, run: pkill pocketbase"
            )

        # Wait a moment for server to be fully ready
        import time
        time.sleep(1)

        # Initialize PocketBase client (will authenticate with bootstrapped admin)
        try:
            self.inventory = PocketBaseInventory(
                base_url=self.realm_server.base_url,
                admin_email=self.realm_server.config["admin_email"],
                admin_password=self.realm_server.config["admin_password"],
            )
        except Exception as e:
            logger.error(f"Failed to connect to PocketBase API: {e}")
            logger.error(f"Server may not be ready. Check: {self.realm_server.base_url}/_/")
            raise

        # Create Reality for Daily Learning Realm
        reality_system = RealitySystem(project_path=self.project_path)
        reality = reality_system.create_reality(
            reality_type=RealityType.LEARNING,
            configuration={
                "realm_name": "daily_learning_realm",
                "realm_path": str(self.realm_path),
                "special": True,
                "purpose": "daily_learning_collection",
                "port": self.realm_server.port,
            },
        )
        self.reality_id = reality.reality_id

        # Spawn the underlying Being
        being_system = BeingSystem(project_path=self.project_path)
        self.being: Being = being_system.spawn_being(
            reality_id=self.reality_id,
            parent_being_id=None,  # Spawns from TheOne
            initial_skills={
                "data_collection": 50.0,
                "research": 40.0,
                "organization": 30.0,
                "memory": 60.0,  # Hoarder trait - high memory
                "api_communication": 40.0,  # NEW: API skills
            },
        )

        # Set custom name and personality
        self.being.custom_name = "The Packrat"
        self.being.personality = {
            "hoarder": True,
            "curious": True,
            "noisy": True,
            "collaborative": True,
            "networked": True,  # NEW: Works via API
        }
        being_system.save_being(self.being)

        # Tools initialized with project_path
        self.tools = {
            "empirica": EmpiricaCollector(self.project_path),
            "chronicler": ChroniclerCollector(self.project_path),
            "session": SessionAnalyticsCollector(self.project_path),
        }

        self.make_noise("spawned", "I have arrived! My spectacles are polished. My server is running!")
        self.make_noise("spawned", f"Backpack API: {self.realm_server.base_url}/_/")

    def make_noise(self, action_type: str, message: str):
        """
        Logs activity with character flavor.

        Args:
            action_type: Type of action (spawned, collecting, hoarding, visiting, resting, error)
            message: Message to log
        """
        emojis = {
            "spawned": "🐣",
            "collecting": "🔍",
            "hoarding": "🎒",
            "visiting": "🏛️",
            "resting": "💤",
            "error": "🤕",
        }
        icon = emojis.get(action_type, "🐀")
        logger.info(f"{icon} [The Packrat]: {message}")

    def collect_data(self, target_date: date | None = None):
        """
        The main loop activity. Goes out and finds things.

        Args:
            target_date: Date to collect data for (defaults to today)
        """
        self.make_noise("collecting", "*sniffs air* Searching for data scraps...")
        findings_count = 0

        for name, tool in self.tools.items():
            try:
                data = tool.collect(target_date=target_date)
                if data:
                    self._add_to_backpack(name, data)
                    findings_count += 1
            except Exception as e:
                self.make_noise("error", f"*trips over tail* Oof! Failed to collect from {name}: {e}")

        # Skill progression
        if findings_count > 0:
            # Update Being's data_collection skill
            current_skill = self.being.skills.get("data_collection", 50.0)
            self.being.skills["data_collection"] = min(100.0, current_skill + 0.5)
            self.make_noise("hoarding", f"Stashed data from {findings_count} sources. Backpack heavier.")

    def get_backpack_data(self) -> dict[str, Any]:
        """
        Get all backpack data from PocketBase API.

        Returns:
            Dictionary with same structure as old backpack (for compatibility)
        """
        # Fetch latest items from each source
        backpack_data = {
            "metadata": {
                "being_id": self.being.being_id,
                "spawned_at": datetime.now().isoformat(),
                "noise_level": "high",
                "collection_count": 0,
            },
            "data": {},
        }

        for source in ["empirica", "chronicler", "session"]:
            items = self.inventory.get_items(source=source, limit=100)
            backpack_data["data"][source] = [
                {
                    "collected_at": item.get("collected_at", ""),
                    "content": item.get("payload", {}),
                }
                for item in items
            ]
            backpack_data["metadata"]["collection_count"] += len(items)

        return backpack_data

    def visit_library(self, librarian, scribe) -> Path:
        """
        The climax of the day. Handing over the goods.

        NOW: Librarian reads from PocketBase API, Library Realm starts lazily!

        Args:
            librarian: Librarian instance
            scribe: Scribe instance

        Returns:
            Path to generated PDF report
        """
        self.make_noise("visiting", "Walking to the Library Realm... hope The Librarian likes this haul.")

        # Get backpack data from API
        backpack_data = self.get_backpack_data()

        # 1. The Librarian organizes (reads from API)
        try:
            organized_data = librarian.organize_daily_learning(backpack_data, inventory_client=self.inventory)
            # Update organization skill
            current_skill = self.being.skills.get("organization", 30.0)
            self.being.skills["organization"] = min(100.0, current_skill + 0.2)
            self.make_noise("visiting", "The Librarian nodded approvingly. Organizing complete.")
        except Exception as e:
            self.make_noise("error", f"The Librarian scolded me: {e}")
            raise

        # 2. The Scribe writes (Passing reports_dir dynamically)
        try:
            report_dir = self.realm_path / "reports"
            report_dir.mkdir(exist_ok=True)

            report_path = scribe.write_daily_learning_report(
                organized_data=organized_data,
                report_date=datetime.now().date(),
                output_dir=report_dir,
            )
            # Update research skill
            current_skill = self.being.skills.get("research", 40.0)
            self.being.skills["research"] = min(100.0, current_skill + 0.5)

            # Save Being with updated skills
            being_system = BeingSystem(project_path=self.project_path)
            being_system.save_being(self.being)

            self.make_noise("visiting", f"The Scribe handed me a scroll! It is here: {report_path}")
            return report_path
        except Exception as e:
            self.make_noise("error", f"The Scribe ran out of ink: {e}")
            raise

    def shutdown(self):
        """Shutdown Packrat and close connections."""
        self.make_noise("resting", "Closing connections...")
        if hasattr(self, "inventory"):
            self.inventory.close()
        # Note: We keep the RealmServer running (it's Packrat's home)
        # Server will be stopped by PackratServer if needed
