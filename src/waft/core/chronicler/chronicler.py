"""
TheChronicler: Self-Monitoring System

TheChronicler observes, records, and reports on all activity within the WAFT system.
Monitors genesis (creation) and exodus (deletion) of all system components.

Architecture:
- Orchestrates file system, git, and work effort observers
- Stores observations in daily folders
- Generates hourly and daily reports
- Integrates with Oracle for decision context
"""

import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .storage import ObservationStorage
from .observers import FileSystemObserver, GitObserver, WorkEffortObserver
from .reports import ReportGenerator
from .scheduler import ChroniclerScheduler
from ..science.oracle import TheOracle


class TheChronicler:
    """
    Self-monitoring system for WAFT - The Chronicler of all system activity.
    
    Observes and records:
    - File system changes (creation, modification, deletion)
    - Git repository changes (commits, status)
    - Work effort changes (new work efforts, tickets)
    
    Reports:
    - Hourly reports on the hour
    - Daily reports at 5 AM (reset cycle)
    """
    
    def __init__(
        self,
        project_path: Path,
        oracle: Optional[TheOracle] = None,
        reset_hour: int = 5
    ):
        """
        Initialize TheChronicler.
        
        Args:
            project_path: Project root path
            oracle: Optional Oracle instance for decision context
            reset_hour: Hour of day to reset cycle (default: 5 AM)
        """
        self.project_path = Path(project_path).resolve()
        self.reset_hour = reset_hour
        
        # Initialize storage
        self.storage = ObservationStorage(self.project_path)
        
        # Initialize Oracle (optional)
        self.oracle = oracle
        if self.oracle is None:
            try:
                self.oracle = TheOracle(self.project_path)
            except RuntimeError:
                # Oracle not available (Empirica not initialized)
                self.oracle = None
        
        # Initialize report generator
        self.report_generator = ReportGenerator(self.storage, self.project_path)
        
        # Observers
        self._observers = []
        self._observer_threads = []
        self._running = False
        
        # Scheduler
        self.scheduler = ChroniclerScheduler(
            on_hourly_report=self._on_hourly_report,
            on_daily_report=self._on_daily_report,
            reset_hour=reset_hour
        )
    
    def _observation_callback(self, observation: Dict[str, Any]):
        """
        Callback for all observers to store observations.
        
        Args:
            observation: Observation dictionary
        """
        # Store observation
        self.storage.store_observation(observation)
        
        # Optionally log to Oracle if significant
        if self.oracle and self._is_significant(observation):
            self._log_to_oracle(observation)
    
    def _is_significant(self, observation: Dict[str, Any]) -> bool:
        """
        Determine if observation is significant enough to log to Oracle.
        
        Args:
            observation: Observation dictionary
        
        Returns:
            True if significant
        """
        # Log work effort changes and major file changes
        observer = observation.get("observer", "")
        event_type = observation.get("event_type", "")
        
        if observer == "work_effort":
            return True
        
        if observer == "git" and event_type == "genesis":
            return True
        
        # Log significant file changes (not in ignored directories)
        if observer == "filesystem":
            path = observation.get("path", "")
            if any(part in path for part in ["src/", "_work_efforts/", "scripts/"]):
                return event_type in ["genesis", "exodus"]
        
        return False
    
    def _log_to_oracle(self, observation: Dict[str, Any]):
        """
        Log significant observation to Oracle.
        
        Args:
            observation: Observation dictionary
        """
        if not self.oracle:
            return
        
        try:
            observer = observation.get("observer", "unknown")
            event_type = observation.get("event_type", "unknown")
            path = observation.get("path", "unknown")
            
            if event_type == "genesis":
                insight = f"System genesis: {observer} detected creation of {path}"
            elif event_type == "exodus":
                insight = f"System exodus: {observer} detected deletion of {path}"
            else:
                insight = f"System mutation: {observer} detected change in {path}"
            
            self.oracle.log_insight(insight, impact=0.3)
        except Exception:
            # Don't fail if Oracle logging fails
            pass
    
    def _on_hourly_report(self, hour: int, date: datetime):
        """
        Generate hourly report.
        
        Args:
            hour: Hour (0-23)
            date: Date
        """
        try:
            report_path = self.report_generator.generate_hourly_report(hour, date)
            print(f"📊 Generated hourly report: {report_path}")
        except Exception as e:
            print(f"❌ Error generating hourly report: {e}")
    
    def _on_daily_report(self, date: datetime):
        """
        Generate daily report.
        
        Args:
            date: Date
        """
        try:
            report_path = self.report_generator.generate_daily_report(date)
            print(f"📊 Generated daily report: {report_path}")
        except Exception as e:
            print(f"❌ Error generating daily report: {e}")
    
    def start(self):
        """Start TheChronicler monitoring."""
        if self._running:
            return
        
        self._running = True
        
        # Start file system observer
        try:
            fs_observer = FileSystemObserver(
                self.project_path,
                self._observation_callback
            )
            fs_observer.start()
            self._observers.append(fs_observer)
            print("👁️  File system observer started")
        except Exception as e:
            print(f"⚠️  File system observer unavailable: {e}")
        
        # Start git observer (polling)
        git_observer = GitObserver(
            self.project_path,
            self._observation_callback
        )
        self._observers.append(git_observer)
        
        def git_poll_loop():
            while self._running:
                try:
                    git_observer.check()
                except Exception:
                    pass
                time.sleep(git_observer.poll_interval)
        
        git_thread = threading.Thread(target=git_poll_loop, daemon=True)
        git_thread.start()
        self._observer_threads.append(git_thread)
        print("👁️  Git observer started")
        
        # Start work effort observer (polling)
        we_observer = WorkEffortObserver(
            self.project_path,
            self._observation_callback
        )
        self._observers.append(we_observer)
        
        def we_poll_loop():
            while self._running:
                try:
                    we_observer.check()
                except Exception:
                    pass
                time.sleep(we_observer.poll_interval)
        
        we_thread = threading.Thread(target=we_poll_loop, daemon=True)
        we_thread.start()
        self._observer_threads.append(we_thread)
        print("👁️  Work effort observer started")
        
        # Start scheduler
        self.scheduler.start()
        print("⏰ Scheduler started (hourly reports on the hour, daily at 5 AM)")
        
        print(f"✅ TheChronicler monitoring active (reset cycle: {self.reset_hour}:00)")
    
    def stop(self):
        """Stop TheChronicler monitoring."""
        if not self._running:
            return
        
        self._running = False
        
        # Stop observers
        for observer in self._observers:
            if hasattr(observer, 'stop'):
                try:
                    observer.stop()
                except Exception:
                    pass
        
        # Stop scheduler
        self.scheduler.stop()
        
        print("🛑 TheChronicler monitoring stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get current statistics.
        
        Returns:
            Dictionary with current stats
        """
        today = datetime.now()
        genesis_count = self.storage.get_genesis_count(today)
        exodus_count = self.storage.get_exodus_count(today)
        
        return {
            "running": self._running,
            "date": today.strftime("%Y-%m-%d"),
            "genesis_count": genesis_count,
            "exodus_count": exodus_count,
            "net_change": genesis_count - exodus_count,
            "observers_active": len([o for o in self._observers if hasattr(o, 'is_alive') and o.is_alive()]),
            "oracle_available": self.oracle is not None
        }
    
    def generate_immediate_hourly_report(self):
        """Manually trigger hourly report for current hour."""
        now = datetime.now()
        self._on_hourly_report(now.hour, now)
    
    def generate_immediate_daily_report(self):
        """Manually trigger daily report for today."""
        now = datetime.now()
        self._on_daily_report(now)
