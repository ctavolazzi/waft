"""
Daily Learning Server - Background daemon for collecting and reporting daily learnings.

Runs continuously, collects data throughout the day, and generates PDF reports
at a configurable trigger time (3 seconds for dev, 9 PM for production).
"""
import logging
import signal
import sys
import time
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import List

from .daily_learning.collectors import (
    EmpiricaCollector,
    ChroniclerCollector,
    SessionAnalyticsCollector,
    BaseCollector,
)
from .daily_learning.report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("DailyLearningServer")


class DailyLearningServer:
    """Background server for daily learning report generation."""

    def __init__(self, project_path: Path, dev_mode: bool = True, trigger_hour: int = 21):
        """
        Initialize the daily learning server.

        Args:
            project_path: Path to project root
            dev_mode: If True, triggers in 3 seconds for testing (default: True)
            trigger_hour: Hour to trigger report in production mode (0-23, default: 21 for 9 PM)
        """
        self.project_path = Path(project_path).resolve()
        self.running = False
        self.dev_mode = dev_mode
        self.trigger_hour = trigger_hour

        # Initialize collectors
        self.collectors: List[BaseCollector] = [
            EmpiricaCollector(self.project_path),
            ChroniclerCollector(self.project_path),
            SessionAnalyticsCollector(self.project_path),
        ]

        # Initialize report generator
        self.generator = ReportGenerator(self.project_path)

        # Calculate next trigger time
        self.next_trigger = self._calculate_next_trigger()
        logger.info(f"Server initialized. Next report trigger: {self.next_trigger}")

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

        logger.info("Daily Learning Server started.")
        logger.info(f"Mode: {'DEV (3 second trigger)' if self.dev_mode else f'PRODUCTION ({self.trigger_hour}:00 daily)'}")

        while self.running:
            now = datetime.now()

            if now >= self.next_trigger:
                self._run_daily_cycle()
                # Reset trigger for next cycle
                if self.dev_mode:
                    # After first dev run, disable dev mode for subsequent runs
                    # (or keep it enabled if you want continuous 3-second cycles)
                    # self.dev_mode = False
                    pass
                self.next_trigger = self._calculate_next_trigger()
                logger.info(f"Cycle complete. Next trigger: {self.next_trigger}")

            # Sleep briefly to prevent CPU spinning
            time.sleep(1)

    def _run_daily_cycle(self):
        """
        Run a complete daily cycle: collect data and generate report.
        """
        logger.info("Starting Daily Learning Cycle...")
        target_date = date.today()
        aggregated_data = {}

        # 1. Collect data from all collectors
        for collector in self.collectors:
            try:
                name = collector.__class__.__name__
                logger.info(f"Collecting from {name}...")
                data = collector.collect(target_date=target_date)
                aggregated_data[name] = data
                logger.info(f"✓ {name} collected {len(str(data))} bytes of data")
            except Exception as e:
                logger.error(f"Collector {name} failed: {e}", exc_info=True)
                aggregated_data[name] = {}

        # 2. Generate report
        logger.info("Generating PDF report...")
        try:
            pdf_path = self.generator.generate(aggregated_data, target_date=target_date)
            if pdf_path:
                logger.info(f"✓ Report generated successfully: {pdf_path}")
            else:
                logger.error("✗ Report generation failed (check logs above)")
        except Exception as e:
            logger.error(f"Report generation failed: {e}", exc_info=True)

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("Shutdown signal received.")
        self.stop()

    def stop(self):
        """Stop the server."""
        self.running = False
        logger.info("Server stopped.")
