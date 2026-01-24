"""
Version Calculator - Epoch-based versioning for WAFT

Calculates version from repo's first commit timestamp.
Version format: v{Years}.{Months}.{Days}.{Hour}.{Quarter}

Epoch: January 4, 2026 @ 4:19:05 PM PST (first commit)
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import json
from pathlib import Path

# The epoch - first commit of the waft repository
EPOCH = datetime(2026, 1, 4, 16, 19, 5)  # Jan 4, 2026 @ 4:19:05 PM
EPOCH_COMMIT = "18ac1b40d0856fb028c385e8c9bf0ef5cdccf77c"
EPOCH_ISO = "2026-01-04T16:19:05-08:00"


@dataclass
class Version:
    """Represents a WAFT version with time-based components."""
    
    years: int
    months: int
    days: int
    hour: int
    quarter: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Format as v{Y}.{M}.{D}.{H}.{Q}"""
        return f"v{self.years}.{self.months}.{self.days}.{self.hour}.{self.quarter}"
    
    def __repr__(self) -> str:
        return f"Version({self})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": str(self),
            "years": self.years,
            "months": self.months,
            "days": self.days,
            "hour": self.hour,
            "quarter": self.quarter,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Version":
        """Create Version from dictionary."""
        return cls(
            years=data["years"],
            months=data["months"],
            days=data["days"],
            hour=data["hour"],
            quarter=data["quarter"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
    
    @classmethod
    def from_timestamp(cls, ts: Optional[datetime] = None) -> "Version":
        """Calculate version from a timestamp (defaults to now)."""
        ts = ts or datetime.now()
        return calculate_version(ts)
    
    def quarter_start(self) -> datetime:
        """Get the start time of this quarter."""
        minute = self.quarter * 15
        return self.timestamp.replace(minute=minute, second=0, microsecond=0)
    
    def quarter_end(self) -> datetime:
        """Get the end time of this quarter."""
        minute = (self.quarter + 1) * 15 - 1
        return self.timestamp.replace(minute=minute, second=59, microsecond=999999)
    
    def is_same_quarter(self, other: "Version") -> bool:
        """Check if two versions are in the same quarter."""
        return (
            self.years == other.years
            and self.months == other.months
            and self.days == other.days
            and self.hour == other.hour
            and self.quarter == other.quarter
        )
    
    def total_quarters_since_epoch(self) -> int:
        """Calculate total quarters elapsed since epoch."""
        total_days = self.years * 365 + self.months * 30 + self.days
        total_hours = total_days * 24 + self.hour
        total_quarters = total_hours * 4 + self.quarter
        return total_quarters


def calculate_version(ts: Optional[datetime] = None) -> Version:
    """
    Calculate the current WAFT version based on time since epoch.
    
    Args:
        ts: Timestamp to calculate version for (defaults to now)
        
    Returns:
        Version object with all components
        
    Example:
        >>> v = calculate_version()
        >>> print(v)  # e.g., v0.0.16.14.0
    """
    ts = ts or datetime.now()
    
    if ts < EPOCH:
        # Before epoch - return v0.0.0.0.0
        return Version(0, 0, 0, 0, 0, ts)
    
    delta = ts - EPOCH
    total_days = delta.days
    
    # Calculate year/month/day components
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    
    # Time components from the timestamp
    hour = ts.hour
    quarter = ts.minute // 15  # 0-3 for Q0-Q3
    
    return Version(years, months, days, hour, quarter, ts)


def get_quarter_boundaries(ts: Optional[datetime] = None) -> tuple[datetime, datetime]:
    """
    Get the start and end times of the current quarter.
    
    Args:
        ts: Timestamp to get boundaries for (defaults to now)
        
    Returns:
        Tuple of (quarter_start, quarter_end)
        
    Example:
        >>> start, end = get_quarter_boundaries()
        >>> # If now is 14:12, returns (14:00:00, 14:14:59)
    """
    ts = ts or datetime.now()
    quarter = ts.minute // 15
    
    start_minute = quarter * 15
    end_minute = start_minute + 14
    
    start = ts.replace(minute=start_minute, second=0, microsecond=0)
    end = ts.replace(minute=end_minute, second=59, microsecond=999999)
    
    return start, end


def time_until_next_quarter(ts: Optional[datetime] = None) -> timedelta:
    """
    Calculate time remaining until the next quarter checkpoint.
    
    Args:
        ts: Current timestamp (defaults to now)
        
    Returns:
        timedelta until next quarter
        
    Example:
        >>> remaining = time_until_next_quarter()
        >>> print(f"{remaining.seconds // 60}m {remaining.seconds % 60}s")
    """
    ts = ts or datetime.now()
    current_quarter = ts.minute // 15
    next_quarter_minute = (current_quarter + 1) * 15
    
    if next_quarter_minute >= 60:
        # Next quarter is in the next hour
        next_checkpoint = ts.replace(
            hour=ts.hour + 1 if ts.hour < 23 else 0,
            minute=0,
            second=0,
            microsecond=0
        )
        if ts.hour == 23:
            next_checkpoint = next_checkpoint + timedelta(days=1)
    else:
        next_checkpoint = ts.replace(
            minute=next_quarter_minute,
            second=0,
            microsecond=0
        )
    
    return next_checkpoint - ts


def format_countdown(td: timedelta) -> str:
    """Format a timedelta as a human-readable countdown."""
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}m {seconds}s"


# Convenience functions for common operations

def current_version() -> Version:
    """Get the current version."""
    return calculate_version()


def version_string() -> str:
    """Get the current version as a string."""
    return str(calculate_version())


def days_since_epoch(ts: Optional[datetime] = None) -> int:
    """Calculate days since epoch."""
    ts = ts or datetime.now()
    return (ts - EPOCH).days if ts >= EPOCH else 0


def quarters_today() -> list[Version]:
    """Get all quarter versions for today."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    versions = []
    for hour in range(24):
        for quarter in range(4):
            ts = today.replace(hour=hour, minute=quarter * 15)
            if ts <= datetime.now():
                versions.append(calculate_version(ts))
    return versions


if __name__ == "__main__":
    # Demo the version calculator
    print("=" * 50)
    print("WAFT Version Calculator Demo")
    print("=" * 50)
    print(f"\nEpoch: {EPOCH.isoformat()}")
    print(f"Epoch Commit: {EPOCH_COMMIT}")
    print()
    
    now = datetime.now()
    v = calculate_version(now)
    
    print(f"Current Time: {now.isoformat()}")
    print(f"Current Version: {v}")
    print(f"Days Since Epoch: {days_since_epoch()}")
    print()
    
    start, end = get_quarter_boundaries()
    remaining = time_until_next_quarter()
    
    print(f"Quarter Boundaries:")
    print(f"  Start: {start.strftime('%H:%M:%S')}")
    print(f"  End:   {end.strftime('%H:%M:%S')}")
    print(f"  Next Checkpoint In: {format_countdown(remaining)}")
    print()
    
    print("Version Components:")
    print(f"  Years:   {v.years}")
    print(f"  Months:  {v.months}")
    print(f"  Days:    {v.days}")
    print(f"  Hour:    {v.hour}")
    print(f"  Quarter: Q{v.quarter} (:{v.quarter * 15:02d}-:{v.quarter * 15 + 14:02d})")
    print()
    
    print(f"Total Quarters Since Epoch: {v.total_quarters_since_epoch()}")
