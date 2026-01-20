"""
Time Manager: Manage simulation time progression

Handles time advancement, date calculations, and time-based events.
"""

from datetime import datetime, timedelta
from enum import Enum


class TimeUnit(Enum):
    """Time units for simulation."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class TimeManager:
    """
    Manages simulation time progression.

    Tracks:
    - Current simulation date
    - Time unit (daily, weekly, monthly)
    - Tick count
    - Time-based event scheduling
    """

    def __init__(self, start_date: datetime, time_unit: TimeUnit = TimeUnit.DAILY):
        """
        Initialize time manager.

        Args:
            start_date: Starting simulation date
            time_unit: Time unit for each tick
        """
        self.start_date = start_date
        self.current_date = start_date
        self.time_unit = time_unit
        self.tick_count = 0

    def tick(self) -> datetime:
        """
        Advance time by one unit.

        Returns:
            New current date
        """
        self.tick_count += 1

        if self.time_unit == TimeUnit.DAILY:
            self.current_date += timedelta(days=1)
        elif self.time_unit == TimeUnit.WEEKLY:
            self.current_date += timedelta(weeks=1)
        elif self.time_unit == TimeUnit.MONTHLY:
            # Approximate month as 30 days
            self.current_date += timedelta(days=30)
        elif self.time_unit == TimeUnit.QUARTERLY:
            self.current_date += timedelta(days=90)
        elif self.time_unit == TimeUnit.YEARLY:
            self.current_date += timedelta(days=365)

        return self.current_date

    def get_days_since_start(self) -> int:
        """Get number of days since simulation start."""
        delta = self.current_date - self.start_date
        return delta.days

    def get_months_since_start(self) -> int:
        """Get approximate number of months since simulation start."""
        return self.get_days_since_start() // 30

    def is_month_end(self) -> bool:
        """Check if current date is end of month."""
        # Check if next day would be in a different month
        next_day = self.current_date + timedelta(days=1)
        return next_day.month != self.current_date.month

    def is_quarter_end(self) -> bool:
        """Check if current date is end of quarter."""
        return self.current_date.month in [3, 6, 9, 12] and self.is_month_end()

    def is_year_end(self) -> bool:
        """Check if current date is end of year."""
        return self.current_date.month == 12 and self.is_month_end()

    def to_dict(self) -> dict:
        """Convert time manager to dictionary."""
        return {
            "start_date": self.start_date.isoformat(),
            "current_date": self.current_date.isoformat(),
            "time_unit": self.time_unit.value,
            "tick_count": self.tick_count,
            "days_since_start": self.get_days_since_start(),
            "months_since_start": self.get_months_since_start(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimeManager":
        """Create TimeManager from dictionary."""
        manager = cls(
            start_date=datetime.fromisoformat(data["start_date"]),
            time_unit=TimeUnit(data["time_unit"]),
        )
        manager.current_date = datetime.fromisoformat(data["current_date"])
        manager.tick_count = data.get("tick_count", 0)
        return manager
