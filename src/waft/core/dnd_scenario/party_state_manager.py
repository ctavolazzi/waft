"""
Party State Manager - Party state persistence and management.

Handles loading/saving party state from realm with security validation.
"""

import json
import os
from datetime import datetime
from typing import Any

from .scenario_realm import ScenarioRealm


class PartyStateManager:
    """
    Manages party state persistence in realm.

    Features:
    - Load/save party state
    - State validation
    - Error handling
    - Path validation
    """

    def __init__(self, scenario_realm: ScenarioRealm):
        """
        Initialize Party State Manager.

        Args:
            scenario_realm: ScenarioRealm instance
        """
        self.realm = scenario_realm
        self.realm_path = scenario_realm.realm_path
        self.party_state_file = self.realm_path / "party_state.json"

    def save_party_state(self, party_state: dict[str, Any]) -> None:
        """
        Save party state to realm.

        Args:
            party_state: Party state data to save
        """
        try:
            # Validate state structure
            if not isinstance(party_state, dict):
                raise ValueError("Party state must be a dictionary")

            # Add metadata
            state_with_metadata = {
                "party_state": party_state,
                "saved_at": datetime.now().isoformat(),
                "version": "1.0.0",
            }

            # Write to temp file first (atomic operation)
            temp_file = self.party_state_file.with_suffix(".tmp")
            temp_file.write_text(json.dumps(state_with_metadata, indent=2))

            # Verify write succeeded
            if not temp_file.exists():
                raise OSError("Failed to write party state")

            # Atomic move
            temp_file.replace(self.party_state_file)

            # Set permissions (0o600)
            os.chmod(self.party_state_file, 0o600)

        except Exception as e:
            raise OSError(f"Failed to save party state: {e}")

    def load_party_state(self) -> dict[str, Any] | None:
        """
        Load party state from realm.

        Returns:
            Party state data, or None if not found
        """
        try:
            if not self.party_state_file.exists():
                return None

            # Validate path
            if not self.realm.validate_path(self.party_state_file):
                raise ValueError("Party state file path validation failed")

            # Load state
            state_data = json.loads(self.party_state_file.read_text())

            # Extract party state
            if "party_state" in state_data:
                return state_data["party_state"]
            else:
                # Legacy format (state is the dict itself)
                return state_data

        except Exception as e:
            raise OSError(f"Failed to load party state: {e}")

    def get_party_state_metadata(self) -> dict[str, Any] | None:
        """
        Get party state metadata (when saved, version, etc.).

        Returns:
            Metadata dict, or None if state doesn't exist
        """
        try:
            if not self.party_state_file.exists():
                return None

            state_data = json.loads(self.party_state_file.read_text())

            return {
                "saved_at": state_data.get("saved_at"),
                "version": state_data.get("version"),
                "file_size": self.party_state_file.stat().st_size,
            }
        except Exception:
            return None
