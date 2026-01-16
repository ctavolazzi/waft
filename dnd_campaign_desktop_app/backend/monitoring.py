"""
Monitoring Data Collection System

Collects first-time startup data and runtime metrics for the D&D Campaign Desktop App.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import platform
import sys
import time
import os
from dataclasses import dataclass, asdict
from enum import Enum


class EventType(Enum):
    """Types of events to monitor."""
    FIRST_STARTUP = "first_startup"
    BACKEND_START = "backend_start"
    BACKEND_READY = "backend_ready"
    BACKEND_ERROR = "backend_error"
    HEALTH_CHECK = "health_check"
    CAMPAIGN_CREATED = "campaign_created"
    CAMPAIGN_STARTED = "campaign_started"
    CAMPAIGN_COMPLETED = "campaign_completed"
    ELECTRON_START = "electron_start"
    ELECTRON_READY = "electron_ready"
    RESTART = "restart"
    SHUTDOWN = "shutdown"


@dataclass
class SystemInfo:
    """System information snapshot."""
    platform: str
    platform_version: str
    architecture: str
    python_version: str
    node_version: Optional[str] = None
    cpu_count: int = 0
    memory_total: Optional[int] = None  # bytes


@dataclass
class StartupEvent:
    """First-time startup event data."""
    event_id: str
    event_type: str
    timestamp: str
    system_info: Dict[str, Any]
    startup_time_ms: float
    backend_start_time_ms: Optional[float] = None
    electron_start_time_ms: Optional[float] = None
    health_check_passed: bool = False
    errors: List[str] = field(default_factory=list)
    features_accessed: List[str] = field(default_factory=list)


@dataclass
class RuntimeMetric:
    """Runtime performance metric."""
    metric_id: str
    metric_type: str
    timestamp: str
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class MonitoringCollector:
    """
    Collects monitoring data for the D&D Campaign Desktop App.

    Features:
    - First-time startup data collection
    - Runtime metrics tracking
    - System information capture
    - Performance monitoring
    - Error tracking
    """

    def __init__(self, project_path: Path, component: str = "backend"):
        """
        Initialize monitoring collector.

        Args:
            project_path: Path to project root
            component: Component name ("backend", "electron", "frontend")
        """
        self.project_path = Path(project_path)
        self.component = component
        self.monitoring_dir = self.project_path / "_pyrite" / ".waft" / "monitoring"
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)

        self.startup_data_file = self.monitoring_dir / "startup_data.json"
        self.metrics_file = self.monitoring_dir / "metrics.jsonl"
        self.events_file = self.monitoring_dir / "events.jsonl"

        self.start_time = time.time()
        self.is_first_startup = not self.startup_data_file.exists()
        self.startup_data: Optional[StartupEvent] = None

    def get_system_info(self) -> SystemInfo:
        """Collect system information."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_total = memory.total
            cpu_count = psutil.cpu_count()
        except ImportError:
            memory_total = None
            cpu_count = os.cpu_count() or 0

        # Try to get Node.js version
        node_version = None
        try:
            import subprocess
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                node_version = result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return SystemInfo(
            platform=platform.system(),
            platform_version=platform.version(),
            architecture=platform.machine(),
            python_version=sys.version.split()[0],
            node_version=node_version,
            cpu_count=cpu_count,
            memory_total=memory_total
        )

    def record_first_startup(self, backend_start_time: Optional[float] = None,
                           electron_start_time: Optional[float] = None,
                           health_check_passed: bool = False,
                           errors: Optional[List[str]] = None) -> StartupEvent:
        """
        Record first-time startup data.

        Args:
            backend_start_time: Backend startup time in milliseconds
            electron_start_time: Electron startup time in milliseconds
            health_check_passed: Whether health check passed
            errors: List of error messages

        Returns:
            StartupEvent with collected data
        """
        if not self.is_first_startup:
            # Load existing startup data
            if self.startup_data_file.exists():
                with open(self.startup_data_file, 'r') as f:
                    data = json.load(f)
                    return StartupEvent(**data)
            return None

        startup_time_ms = (time.time() - self.start_time) * 1000

        system_info = self.get_system_info()

        event = StartupEvent(
            event_id=f"startup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            event_type=EventType.FIRST_STARTUP.value,
            timestamp=datetime.now().isoformat(),
            system_info=asdict(system_info),
            startup_time_ms=startup_time_ms,
            backend_start_time_ms=backend_start_time,
            electron_start_time_ms=electron_start_time,
            health_check_passed=health_check_passed,
            errors=errors or [],
            features_accessed=[]
        )

        # Save startup data
        with open(self.startup_data_file, 'w') as f:
            json.dump(asdict(event), f, indent=2)

        self.startup_data = event
        return event

    def record_event(self, event_type: EventType, metadata: Optional[Dict[str, Any]] = None):
        """
        Record a runtime event.

        Args:
            event_type: Type of event
            metadata: Additional event metadata
        """
        event = {
            "event_id": f"{event_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "event_type": event_type.value,
            "timestamp": datetime.now().isoformat(),
            "component": self.component,
            "metadata": metadata or {}
        }

        # Append to events file (JSONL format)
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def record_metric(self, metric_type: str, value: float, unit: str = "ms",
                     metadata: Optional[Dict[str, Any]] = None):
        """
        Record a performance metric.

        Args:
            metric_type: Type of metric (e.g., "health_check_duration", "api_response_time")
            value: Metric value
            unit: Unit of measurement
            metadata: Additional metadata
        """
        metric = RuntimeMetric(
            metric_id=f"metric_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
            value=value,
            unit=unit,
            metadata=metadata or {}
        )

        # Append to metrics file (JSONL format)
        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(asdict(metric)) + '\n')

    def record_error(self, error_type: str, error_message: str,
                    stack_trace: Optional[str] = None):
        """
        Record an error event.

        Args:
            error_type: Type of error
            error_message: Error message
            stack_trace: Optional stack trace
        """
        self.record_event(
            EventType.BACKEND_ERROR,
            metadata={
                "error_type": error_type,
                "error_message": error_message,
                "stack_trace": stack_trace
            }
        )

    def record_feature_access(self, feature_name: str):
        """
        Record that a feature was accessed.

        Args:
            feature_name: Name of the feature
        """
        if self.startup_data:
            if feature_name not in self.startup_data.features_accessed:
                self.startup_data.features_accessed.append(feature_name)
                # Update startup data file
                with open(self.startup_data_file, 'w') as f:
                    json.dump(asdict(self.startup_data), f, indent=2)

        self.record_event(
            EventType.CAMPAIGN_CREATED if feature_name == "campaign_create" else None,
            metadata={"feature": feature_name}
        )

    def get_startup_data(self) -> Optional[Dict[str, Any]]:
        """Get first-time startup data if available."""
        if self.startup_data_file.exists():
            with open(self.startup_data_file, 'r') as f:
                return json.load(f)
        return None

    def is_first_startup(self) -> bool:
        """Check if this is the first startup."""
        return self.is_first_startup


# Global instance (will be initialized in campaign_server.py)
monitoring: Optional[MonitoringCollector] = None


def init_monitoring(project_path: Path, component: str = "backend") -> MonitoringCollector:
    """
    Initialize global monitoring collector.

    Args:
        project_path: Path to project root
        component: Component name

    Returns:
        MonitoringCollector instance
    """
    global monitoring
    monitoring = MonitoringCollector(project_path, component)
    return monitoring


def get_monitoring() -> Optional[MonitoringCollector]:
    """Get global monitoring collector."""
    return monitoring
