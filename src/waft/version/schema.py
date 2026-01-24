"""
Version Schema - Data structures for VERSION.json and version-manifest.json

These schemas define the structure for tracking version state and checkpoint history.
"""

import json
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .calculator import EPOCH, EPOCH_COMMIT, EPOCH_ISO, Version, calculate_version


@dataclass
class Checkpoint:
    """A single checkpoint record."""
    
    version: str
    timestamp: str
    quarter: str  # Q0, Q1, Q2, Q3
    had_changes: bool
    checked_at: str
    commit_sha: Optional[str] = None
    report_path: Optional[str] = None
    changes: Optional[dict] = None
    
    def to_dict(self) -> dict:
        d = asdict(self)
        # Remove None values for cleaner JSON
        return {k: v for k, v in d.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Checkpoint":
        return cls(**data)


@dataclass
class VersionState:
    """
    Current version state - stored in VERSION.json
    
    This file lives at the repo root and tracks:
    - The epoch (first commit)
    - Current calculated version
    - Last checkpoint info
    """
    
    epoch: str = EPOCH_ISO
    epoch_commit: str = EPOCH_COMMIT
    current: str = ""
    last_checkpoint: Optional[dict] = None
    initialized_at: str = ""
    
    def __post_init__(self):
        if not self.current:
            self.current = str(calculate_version())
        if not self.initialized_at:
            self.initialized_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "epoch": self.epoch,
            "epoch_commit": self.epoch_commit,
            "current": self.current,
            "last_checkpoint": self.last_checkpoint,
            "initialized_at": self.initialized_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "VersionState":
        return cls(
            epoch=data.get("epoch", EPOCH_ISO),
            epoch_commit=data.get("epoch_commit", EPOCH_COMMIT),
            current=data.get("current", ""),
            last_checkpoint=data.get("last_checkpoint"),
            initialized_at=data.get("initialized_at", ""),
        )
    
    def update_current(self) -> str:
        """Update current version to now."""
        self.current = str(calculate_version())
        return self.current
    
    def set_last_checkpoint(self, checkpoint: Checkpoint):
        """Set the last checkpoint."""
        self.last_checkpoint = checkpoint.to_dict()


@dataclass
class VersionManifest:
    """
    Version history manifest - stored in version-manifest.json
    
    This file tracks all checkpoints with full history.
    """
    
    epoch: str = EPOCH_ISO
    epoch_commit: str = EPOCH_COMMIT
    checkpoints: list = field(default_factory=list)
    total_checkpoints: int = 0
    checkpoints_with_changes: int = 0
    
    def to_dict(self) -> dict:
        return {
            "epoch": self.epoch,
            "epoch_commit": self.epoch_commit,
            "checkpoints": self.checkpoints,
            "stats": {
                "total_checkpoints": self.total_checkpoints,
                "checkpoints_with_changes": self.checkpoints_with_changes,
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "VersionManifest":
        stats = data.get("stats", {})
        return cls(
            epoch=data.get("epoch", EPOCH_ISO),
            epoch_commit=data.get("epoch_commit", EPOCH_COMMIT),
            checkpoints=data.get("checkpoints", []),
            total_checkpoints=stats.get("total_checkpoints", 0),
            checkpoints_with_changes=stats.get("checkpoints_with_changes", 0),
        )
    
    def add_checkpoint(self, checkpoint: Checkpoint):
        """Add a checkpoint to the manifest."""
        self.checkpoints.append(checkpoint.to_dict())
        self.total_checkpoints += 1
        if checkpoint.had_changes:
            self.checkpoints_with_changes += 1
    
    def get_last_checkpoint(self) -> Optional[Checkpoint]:
        """Get the most recent checkpoint."""
        if not self.checkpoints:
            return None
        return Checkpoint.from_dict(self.checkpoints[-1])
    
    def get_checkpoints_for_day(self, date: datetime) -> list[Checkpoint]:
        """Get all checkpoints for a specific day."""
        date_str = date.strftime("%Y-%m-%d")
        return [
            Checkpoint.from_dict(cp)
            for cp in self.checkpoints
            if cp["timestamp"].startswith(date_str)
        ]


class VersionManager:
    """
    Manages VERSION.json and version-manifest.json files.
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.version_file = self.repo_path / "VERSION.json"
        self.manifest_file = self.repo_path / "version-manifest.json"
    
    def initialize(self, force: bool = False) -> tuple[VersionState, VersionManifest]:
        """
        Initialize VERSION.json and version-manifest.json.
        
        Args:
            force: If True, overwrite existing files
            
        Returns:
            Tuple of (VersionState, VersionManifest)
        """
        state = self.load_state() if self.version_file.exists() and not force else VersionState()
        manifest = self.load_manifest() if self.manifest_file.exists() and not force else VersionManifest()
        
        self.save_state(state)
        self.save_manifest(manifest)
        
        return state, manifest
    
    def load_state(self) -> VersionState:
        """Load VERSION.json or create default."""
        if self.version_file.exists():
            with open(self.version_file) as f:
                return VersionState.from_dict(json.load(f))
        return VersionState()
    
    def save_state(self, state: VersionState):
        """Save VERSION.json."""
        with open(self.version_file, "w") as f:
            json.dump(state.to_dict(), f, indent=2)
    
    def load_manifest(self) -> VersionManifest:
        """Load version-manifest.json or create default."""
        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                return VersionManifest.from_dict(json.load(f))
        return VersionManifest()
    
    def save_manifest(self, manifest: VersionManifest):
        """Save version-manifest.json."""
        with open(self.manifest_file, "w") as f:
            json.dump(manifest.to_dict(), f, indent=2)
    
    def get_current_commit_sha(self) -> Optional[str]:
        """Get current HEAD commit SHA."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, OSError):
            pass
        return None
    
    def create_checkpoint(self, had_changes: bool, changes: Optional[dict] = None, 
                         report_path: Optional[str] = None) -> Checkpoint:
        """
        Create a new checkpoint.
        
        Args:
            had_changes: Whether changes were detected
            changes: Optional dict of change details
            report_path: Optional path to generated report
            
        Returns:
            New Checkpoint object
        """
        now = datetime.now()
        version = calculate_version(now)
        
        checkpoint = Checkpoint(
            version=str(version),
            timestamp=now.isoformat(),
            quarter=f"Q{version.quarter}",
            had_changes=had_changes,
            checked_at=now.isoformat(),
            commit_sha=self.get_current_commit_sha(),
            report_path=report_path if had_changes else None,
            changes=changes if had_changes else None,
        )
        
        # Update state and manifest
        state = self.load_state()
        manifest = self.load_manifest()
        
        state.update_current()
        state.set_last_checkpoint(checkpoint)
        manifest.add_checkpoint(checkpoint)
        
        self.save_state(state)
        self.save_manifest(manifest)
        
        return checkpoint
    
    def get_status(self) -> dict:
        """Get current version status."""
        state = self.load_state()
        manifest = self.load_manifest()
        version = calculate_version()
        
        return {
            "current_version": str(version),
            "epoch": state.epoch,
            "epoch_commit": state.epoch_commit,
            "last_checkpoint": state.last_checkpoint,
            "total_checkpoints": manifest.total_checkpoints,
            "checkpoints_with_changes": manifest.checkpoints_with_changes,
            "version_components": version.to_dict(),
        }


if __name__ == "__main__":
    # Demo the schema
    print("=" * 50)
    print("WAFT Version Schema Demo")
    print("=" * 50)
    
    manager = VersionManager()
    
    print("\nInitializing version files...")
    state, manifest = manager.initialize()
    
    print(f"\nVERSION.json:")
    print(json.dumps(state.to_dict(), indent=2))
    
    print(f"\nversion-manifest.json:")
    print(json.dumps(manifest.to_dict(), indent=2))
    
    print("\n" + "=" * 50)
    print("Creating test checkpoint (no changes)...")
    checkpoint = manager.create_checkpoint(had_changes=False)
    print(f"Checkpoint: {checkpoint.version} at {checkpoint.checked_at}")
    
    print("\nUpdated STATUS:")
    status = manager.get_status()
    print(json.dumps(status, indent=2))
