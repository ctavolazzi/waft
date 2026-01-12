"""
Data Collection System

Collects data during experiments (C) for analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path


@dataclass
class DataPoint:
    """A single data point collected during an experiment."""
    timestamp: str
    metric_name: str
    value: Any
    unit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "metric_name": self.metric_name,
            "value": self.value,
            "unit": self.unit,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataPoint":
        """Create from dictionary."""
        return cls(
            timestamp=data["timestamp"],
            metric_name=data["metric_name"],
            value=data["value"],
            unit=data.get("unit"),
            metadata=data.get("metadata", {})
        )


@dataclass
class DataSeries:
    """A series of data points for a single metric."""
    metric_name: str
    unit: Optional[str] = None
    data_points: List[DataPoint] = field(default_factory=list)
    
    def add_point(self, value: Any, metadata: Optional[Dict[str, Any]] = None):
        """Add a data point to the series."""
        point = DataPoint(
            timestamp=datetime.now().isoformat(),
            metric_name=self.metric_name,
            value=value,
            unit=self.unit,
            metadata=metadata or {}
        )
        self.data_points.append(point)
    
    def get_values(self) -> List[Any]:
        """Get all values from data points."""
        return [dp.value for dp in self.data_points]
    
    def get_timestamps(self) -> List[str]:
        """Get all timestamps from data points."""
        return [dp.timestamp for dp in self.data_points]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "unit": self.unit,
            "data_points": [dp.to_dict() for dp in self.data_points]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSeries":
        """Create from dictionary."""
        return cls(
            metric_name=data["metric_name"],
            unit=data.get("unit"),
            data_points=[DataPoint.from_dict(dp) for dp in data.get("data_points", [])]
        )


class DataCollector:
    """Collects data during experiments."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize data collector.
        
        Args:
            storage_path: Optional path to store collected data
        """
        self.storage_path = storage_path
        if self.storage_path:
            self.storage_path = Path(storage_path)
            self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.series: Dict[str, DataSeries] = {}
    
    def create_series(self, metric_name: str, unit: Optional[str] = None) -> DataSeries:
        """
        Create a new data series.
        
        Args:
            metric_name: Name of the metric
            unit: Optional unit of measurement
        
        Returns:
            DataSeries instance
        """
        series = DataSeries(metric_name=metric_name, unit=unit)
        self.series[metric_name] = series
        return series
    
    def record(self, metric_name: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        """
        Record a data point.
        
        Args:
            metric_name: Name of the metric
            value: Value to record
            metadata: Optional metadata
        """
        if metric_name not in self.series:
            self.create_series(metric_name)
        
        self.series[metric_name].add_point(value, metadata)
    
    def record_fitness(self, fitness: float, being_id: Optional[str] = None):
        """Record fitness value."""
        metadata = {"being_id": being_id} if being_id else {}
        self.record("fitness", fitness, metadata)
    
    def record_decision(self, decision_type: str, success: bool, metadata: Optional[Dict[str, Any]] = None):
        """Record a decision."""
        metadata = metadata or {}
        metadata.update({
            "decision_type": decision_type,
            "success": success
        })
        self.record("decisions", {"type": decision_type, "success": success}, metadata)
    
    def record_skill_level(self, skill_name: str, level: float):
        """Record skill level."""
        self.record(f"skill_{skill_name}", level)
    
    def get_series(self, metric_name: str) -> Optional[DataSeries]:
        """Get a data series by name."""
        return self.series.get(metric_name)
    
    def get_all_series(self) -> Dict[str, DataSeries]:
        """Get all data series."""
        return self.series.copy()
    
    def save(self, experiment_id: str):
        """Save collected data to file."""
        if not self.storage_path:
            return
        
        filename = f"data_{experiment_id}.json"
        filepath = self.storage_path / filename
        
        data = {
            "experiment_id": experiment_id,
            "series": {name: series.to_dict() for name, series in self.series.items()}
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    
    def load(self, experiment_id: str) -> bool:
        """Load collected data from file."""
        if not self.storage_path:
            return False
        
        filename = f"data_{experiment_id}.json"
        filepath = self.storage_path / filename
        
        if not filepath.exists():
            return False
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.series = {
            name: DataSeries.from_dict(series_data)
            for name, series_data in data.get("series", {}).items()
        }
        
        return True
    
    def clear(self):
        """Clear all collected data."""
        self.series = {}
