"""
Scheduler: Manages hourly and daily report generation.

Handles 5 AM reset cycle and hourly report triggers.
"""

import threading
import time
from collections.abc import Callable
from datetime import datetime


class ChroniclerScheduler:
    """Schedules hourly and daily reports."""

    def __init__(
        self,
        on_hourly_report: Callable[[int, datetime], None],
        on_daily_report: Callable[[datetime], None],
        reset_hour: int = 5,
    ):
        """
        Initialize scheduler.

        Args:
            on_hourly_report: Callback(hour, date) for hourly reports
            on_daily_report: Callback(date) for daily reports
            reset_hour: Hour of day to reset cycle (default: 5 AM)
        """
        self.on_hourly_report = on_hourly_report
        self.on_daily_report = on_daily_report
        self.reset_hour = reset_hour

        self._running = False
        self._thread: threading.Thread | None = None
        self._last_hour: int | None = None
        self._last_date: datetime | None = None

    def start(self):
        """Start scheduler thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop scheduler thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run(self):
        """Main scheduler loop."""
        while self._running:
            now = datetime.now()
            current_hour = now.hour
            current_date = now.date()

            # Check for daily reset (5 AM)
            if current_hour == self.reset_hour:
                # Check if we've already processed this reset
                if self._last_date != current_date or self._last_hour != current_hour:
                    try:
                        # Generate daily report for previous day
                        if self._last_date:
                            prev_date = datetime.combine(self._last_date, datetime.min.time())
                            self.on_daily_report(prev_date)
                    except Exception as e:
                        print(f"Error generating daily report: {e}")

                    # Reset for new day
                    self._last_date = current_date
                    self._last_hour = current_hour
            else:
                # Check for hourly report (on the hour)
                if current_hour != self._last_hour:
                    try:
                        self.on_hourly_report(current_hour, now)
                    except Exception as e:
                        print(f"Error generating hourly report: {e}")

                    self._last_hour = current_hour
                    if self._last_date != current_date:
                        self._last_date = current_date

            # Sleep until next minute
            time.sleep(60 - now.second)

    def trigger_immediate_hourly(self):
        """Manually trigger hourly report for current hour."""
        now = datetime.now()
        self.on_hourly_report(now.hour, now)

    def trigger_immediate_daily(self):
        """Manually trigger daily report for today."""
        now = datetime.now()
        self.on_daily_report(now)
