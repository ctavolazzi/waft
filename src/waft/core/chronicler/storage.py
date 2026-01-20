"""
Storage: Observation persistence for TheChronicler.

Manages daily observation folders and JSONL storage.
"""

import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any


class ObservationStorage:
    """Manages storage of observations in daily folders."""

    def __init__(self, project_path: Path):
        """
        Initialize observation storage.

        Args:
            project_path: Project root path
        """
        self.project_path = Path(project_path)
        self.observations_dir = self.project_path / "_chronicler" / "observations"
        self.observations_dir.mkdir(parents=True, exist_ok=True)

        self._lock = Lock()
        self._current_day_dir: Path | None = None
        self._current_day: str | None = None

    def get_day_dir(self, date: datetime | None = None) -> Path:
        """
        Get or create directory for a specific day.

        Args:
            date: Date to get directory for (defaults to today)

        Returns:
            Path to day directory
        """
        if date is None:
            date = datetime.now()

        day_str = date.strftime("%Y-%m-%d")

        # Cache current day directory
        if day_str == self._current_day:
            return self._current_day_dir

        day_dir = self.observations_dir / day_str
        day_dir.mkdir(parents=True, exist_ok=True)

        self._current_day = day_str
        self._current_day_dir = day_dir

        return day_dir

    def store_observation(self, observation: dict[str, Any], date: datetime | None = None) -> Path:
        """
        Store an observation in JSONL format.

        Args:
            observation: Observation data dictionary
            date: Date for observation (defaults to now)

        Returns:
            Path to stored observation file
        """
        if date is None:
            date = datetime.now()

        day_dir = self.get_day_dir(date)
        hour = date.strftime("%H")

        # Store in hourly files
        observation_file = day_dir / f"observations_{hour}.jsonl"

        # Add timestamp if not present
        if "timestamp" not in observation:
            observation["timestamp"] = date.isoformat()

        with self._lock:
            with open(observation_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(observation) + "\n")

        return observation_file

    def get_observations(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        event_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve observations within a date range.

        Args:
            start_date: Start of date range (defaults to today)
            end_date: End of date range (defaults to today)
            event_type: Filter by event type (genesis, exodus, mutation)

        Returns:
            List of observation dictionaries
        """
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if end_date is None:
            end_date = datetime.now()

        observations = []

        # Iterate through date range
        current_date = start_date
        while current_date <= end_date:
            day_dir = self.get_day_dir(current_date)

            if not day_dir.exists():
                current_date = self._next_day(current_date)
                continue

            # Read all hourly files for this day
            for hour_file in sorted(day_dir.glob("observations_*.jsonl")):
                with open(hour_file, encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            obs = json.loads(line)
                            obs_date = datetime.fromisoformat(obs["timestamp"])

                            # Filter by date range
                            if start_date <= obs_date <= end_date:
                                # Filter by event type if specified
                                if event_type is None or obs.get("event_type") == event_type:
                                    observations.append(obs)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue

            current_date = self._next_day(current_date)

        return sorted(observations, key=lambda x: x.get("timestamp", ""))

    def _next_day(self, date: datetime) -> datetime:
        """Get next day from date."""
        from datetime import timedelta

        return date + timedelta(days=1)

    def get_genesis_count(self, date: datetime | None = None) -> int:
        """Get count of genesis events (creations) for a day."""
        if date is None:
            date = datetime.now()

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        observations = self.get_observations(start, end, event_type="genesis")
        return len(observations)

    def get_exodus_count(self, date: datetime | None = None) -> int:
        """Get count of exodus events (deletions) for a day."""
        if date is None:
            date = datetime.now()

        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        observations = self.get_observations(start, end, event_type="exodus")
        return len(observations)
