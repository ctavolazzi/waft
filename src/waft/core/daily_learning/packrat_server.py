"""
Packrat Server - Orchestrates The Packrat Being's daily learning cycle.

Manages The Packrat Being, coordinates with The Librarian and The Scribe,
and handles the trigger schedule (3 seconds for dev, 9 PM for production).
"""
import logging
import signal
import sys
import time
from datetime import datetime, timedelta, date
from pathlib import Path

from ..beings.packrat_being import PackratBeing
from ..realms.server import RealmServer
from ...pantheon.library.librarian import Librarian
from ...pantheon.library.scribe import Scribe

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PackratServer")


class PackratServer:
    """Server that orchestrates The Packrat Being's daily learning cycle."""

    def __init__(self, project_path: Path, dev_mode: bool = True, trigger_hour: int = 21):
        """
        Initialize the Packrat Server.

        Args:
            project_path: Path to project root
            dev_mode: If True, triggers in 3 seconds for testing (default: True)
            trigger_hour: Hour to trigger report in production mode (0-23, default: 21 for 9 PM)
        """
        self.project_path = Path(project_path).resolve()
        self.running = False
        self.dev_mode = dev_mode
        self.trigger_hour = trigger_hour

        # Setup Realm
        self.realm_path = self.project_path / "_realms" / "daily_learning_realm"
        self.realm_path.mkdir(parents=True, exist_ok=True)
        (self.realm_path / "reports").mkdir(exist_ok=True)

        # Summon Entities with correct paths
        self.packrat = PackratBeing(project_path=self.project_path, realm_path=self.realm_path)
        self.librarian = Librarian(project_path=self.project_path)

        # Scribe points to scripts dir (for stashing intermediate scripts if needed)
        library_path = self.project_path / "_pantheon" / "library"
        self.scribe = Scribe(scripts_dir=library_path / "scripts")

        # Library Realm server (lazy - only starts when Packrat visits)
        self.library_realm_server = None

        # Calculate next trigger time
        self.next_trigger = self._calculate_next_trigger()
        logger.info(f"Packrat Server initialized. Next report trigger: {self.next_trigger}")

    def _calculate_next_trigger(self) -> datetime:
        """
        Calculate the next trigger time based on mode.

        Returns:
            Next trigger datetime
        """
        if self.dev_mode:
            # DEV MODE: Trigger in 3 seconds
            return datetime.now() + timedelta(seconds=3)

        # PRODUCTION: Trigger at set hour (default: 9 PM)
        now = datetime.now()
        target = now.replace(hour=self.trigger_hour, minute=0, second=0, microsecond=0)
        if target <= now:
            # If trigger hour passed, schedule for tomorrow
            target += timedelta(days=1)
        return target

    def start(self):
        """Start the server loop."""
        self.running = True
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        logger.info("Packrat Server Active. The Packrat is awake.")
        logger.info(f"Mode: {'DEV (3 second trigger)' if self.dev_mode else f'PRODUCTION ({self.trigger_hour}:00 daily)'}")
        logger.info(f"Next report trigger: {self.next_trigger}")

        while self.running:
            now = datetime.now()

            if now >= self.next_trigger:
                self._run_daily_cycle()
                # Reset trigger for next cycle
                if self.dev_mode:
                    # After first dev run, keep dev mode enabled for continuous 3-second cycles
                    # (or set to False if you want it to switch to production after first run)
                    pass
                self.next_trigger = self._calculate_next_trigger()
                logger.info(f"Cycle complete. The Packrat is napping until {self.next_trigger}")

            # Sleep briefly to prevent CPU spinning
            time.sleep(1)

    def _run_daily_cycle(self):
        """
        Run a complete daily cycle: collect data and generate report.
        """
        self.packrat.make_noise("resting", "Waking up for the big haul!")

        # 1. Final Sweep - collect data for today
        target_date = date.today()
        self.packrat.collect_data(target_date=target_date)

        # 2. Visit Pantheon
        try:
            pdf_path = self.packrat.visit_library(self.librarian, self.scribe)
            logger.info(f"Daily Cycle Success. Report: {pdf_path}")
        except Exception as e:
            logger.error(f"Daily Cycle Failed: {e}", exc_info=True)

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        self.packrat.make_noise("tired", "Going to sleep now. Bye bye.")
        logger.info("Shutdown signal received.")
        self.stop()

    def stop(self):
        """Stop the server and clean up Realm servers."""
        self.running = False

        # Stop Library Realm if running
        if self.library_realm_server and self.library_realm_server.is_running():
            self.library_realm_server.stop()

        # Packrat's RealmServer stays running (it's Packrat's home)
        # But we can close the inventory client
        if hasattr(self.packrat, "shutdown"):
            self.packrat.shutdown()

        logger.info("Server stopped.")
