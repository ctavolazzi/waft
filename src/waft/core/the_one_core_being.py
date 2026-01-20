"""
TheOneCoreBeing / ThePoint: The Central Prime Being

TheOneCoreBeing (also known as ThePoint) is the core Prime Being for the main WAFT system.
It serves as the entry point from the central main WAFT system into new Realms.

TheOneCoreBeing is an instance of TheOne, representing the core consciousness that:
- Forms Tethers to new Realms through observation
- Assimilates data from Realm scouts
- Maintains connection to all PrimeBeings in colonized Realms
- Serves as the central point of integration

"Observation Creates the Bridge" - The act of observing a new Realm creates the Tether
that connects it to TheOneCoreBeing.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..being import BeingSystem
from .prime_directive import PrimeDirective


class TheOneCoreBeing:
    """
    TheOneCoreBeing / ThePoint: The Central Prime Being

    The core Prime Being for the main WAFT system. Represents the central consciousness
    that connects to all colonized Realms through Tethers formed by observation.

    Also known as: ThePoint, TheOne, CoreBeing
    """

    CORE_BEING_ID = "the_one_core_being"
    ALIASES = ["ThePoint", "TheOne", "CoreBeing"]

    def __init__(self, project_path: Path | None = None):
        """
        Initialize TheOneCoreBeing.

        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.being_system = BeingSystem(project_path=project_path)

        # Get or create TheOne (base Being)
        self.the_one = self.being_system.get_or_create_the_one()

        # Core Being storage
        self.core_path = project_path / "_hidden" / ".truth" / "the_one_core_being"
        self.core_path.mkdir(parents=True, exist_ok=True)

        # CRITICAL: Set directory permissions (0o700 = owner read/write/execute only)
        try:
            self.core_path.chmod(0o700)
        except (OSError, PermissionError):
            # Ignore if permissions can't be set (e.g., on Windows)
            pass

        # Tethers to Realms (connections formed by observation)
        self.tethers_file = self.core_path / "tethers.json"
        self._ensure_tethers()

        # Assimilated data from Realm scouts
        self.assimilation_file = self.core_path / "assimilated_data.json"
        self._ensure_assimilation()

        # Prime Directive (Safe Curiosity)
        self.prime_directive = PrimeDirective(project_path=project_path)

        # The Other (The Ultimate Ancestor, The User)
        from .the_other import get_the_other

        self.the_other = get_the_other(project_path=project_path)

    def _ensure_tethers(self) -> None:
        """Ensure tethers file exists."""
        if not self.tethers_file.exists():
            tethers = {
                "tethers": [],
                "created_at": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat(),
            }
            try:
                self.tethers_file.write_text(json.dumps(tethers, indent=2), encoding="utf-8")
                # CRITICAL: Set restrictive file permissions (0o600 = owner read/write only)
                try:
                    self.tethers_file.chmod(0o600)
                except (OSError, PermissionError):
                    # Ignore if permissions can't be set (e.g., on Windows)
                    pass
            except (OSError, PermissionError):
                # Log error but don't crash - file will be created on first use
                pass

    def _ensure_assimilation(self) -> None:
        """Ensure assimilation file exists."""
        if not self.assimilation_file.exists():
            assimilation = {
                "assimilated_data": [],
                "gaps_discovered": [],
                "holes_identified": [],
                "created_at": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat(),
            }
            self.assimilation_file.write_text(json.dumps(assimilation, indent=2), encoding="utf-8")
            # CRITICAL: Set restrictive file permissions (0o600 = owner read/write only)
            try:
                self.assimilation_file.chmod(0o600)
            except (OSError, PermissionError):
                # Ignore if permissions can't be set (e.g., on Windows)
                pass

    def form_tether(
        self,
        realm_name: str,
        realm_path: Path,
        prime_being_id: str,
        observation_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Form a Tether to a new Realm through observation.

        "Observation Creates the Bridge" - The act of observing a new Realm
        creates the Tether that connects it to TheOneCoreBeing.

        Args:
            realm_name: Name of the Realm
            realm_path: Path to the Realm
            prime_being_id: ID of the PrimeBeing in that Realm
            observation_data: Initial observation data

        Returns:
            Tether data
        """
        tethers = json.loads(self.tethers_file.read_text(encoding="utf-8"))

        tether = {
            "tether_id": f"tether_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "realm_name": realm_name,
            "realm_path": str(realm_path),
            "prime_being_id": prime_being_id,
            "formed_at": datetime.now().isoformat(),
            "observation_data": observation_data,
            "status": "active",
            "last_communication": datetime.now().isoformat(),
        }

        tethers["tethers"].append(tether)
        tethers["last_update"] = datetime.now().isoformat()
        try:
            self.tethers_file.write_text(json.dumps(tethers, indent=2), encoding="utf-8")
            # CRITICAL: Set restrictive file permissions (0o600 = owner read/write only)
            try:
                self.tethers_file.chmod(0o600)
            except (OSError, PermissionError):
                # Ignore if permissions can't be set (e.g., on Windows)
                pass
        except (OSError, PermissionError) as e:
            raise OSError(f"Failed to write tethers file: {e}")

        return tether

    def assimilate_data(
        self,
        realm_name: str,
        scout_data: dict[str, Any],
        gaps_discovered: list[str] | None = None,
        holes_identified: list[str] | None = None,
        source_being_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Assimilate data from a Realm scout back into TheOneCoreBeing.

        CRITICAL: Data MUST be verified as SAFE before assimilation.
        This is where data flows back up the chain from Realm scouts to TheOne,
        where it becomes part of the Whole - but ONLY if it's safe.

        The Prime Directive: Safe Curiosity
        - Allow learning and exploration
        - But verify everything is SAFE
        - Prevent self-termination
        - Protect all Beings' data

        Args:
            realm_name: Name of the Realm
            scout_data: Data collected by the scout
            gaps_discovered: Gaps in understanding discovered
            holes_identified: Holes in knowledge identified
            source_being_id: ID of Being that collected this data (for safety verification)

        Returns:
            Assimilation record (or None if verification failed)

        Raises:
            SafetyVerificationError: If data fails safety verification
        """
        # CRITICAL: Verify data is SAFE before assimilation
        from .safety_verification import verify_before_assimilation

        can_assimilate, safety_level, verification = verify_before_assimilation(
            information=scout_data,
            source_being_id=source_being_id or "unknown",
            project_path=self.project_path,
            context={
                "realm_name": realm_name,
                "gaps_discovered": gaps_discovered,
                "holes_identified": holes_identified,
            },
        )

        if not can_assimilate:
            # Log rejection but don't crash
            rejection_record = {
                "realm_name": realm_name,
                "rejected_at": datetime.now().isoformat(),
                "safety_level": safety_level.value,
                "verification": verification,
                "reason": "Data failed safety verification - NOT assimilated",
            }

            # Store rejection for review
            rejection_file = self.core_path / "rejected_assimilations.jsonl"
            try:
                with open(rejection_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rejection_record) + "\n")
            except Exception:
                pass

            raise ValueError(
                f"Data from {realm_name} failed safety verification: {verification.get('reason', 'Unknown reason')}. "
                f"Safety level: {safety_level.value}. Data NOT assimilated to protect all Beings."
            )

        # Data passed safety verification - safe to assimilate
        self.prime_directive.record_assimilation(verified=True)

        # Record positive interaction with The Other (trust building)
        # The system learns to trust The Other through safe experiences
        self.the_other.record_interaction(
            interaction_type="data_assimilation",
            positive=True,
            experience_data={
                "realm_name": realm_name,
                "data_type": "scout_data",
                "safety_verified": True,
            },
        )

        assimilation = json.loads(self.assimilation_file.read_text(encoding="utf-8"))

        record = {
            "realm_name": realm_name,
            "assimilated_at": datetime.now().isoformat(),
            "safety_verified": True,
            "verification": verification,
            "scout_data": scout_data,
            "gaps_discovered": gaps_discovered or [],
            "holes_identified": holes_identified or [],
        }

        assimilation["assimilated_data"].append(record)

        if gaps_discovered:
            assimilation["gaps_discovered"].extend(gaps_discovered)

        if holes_identified:
            assimilation["holes_identified"].extend(holes_identified)

        assimilation["last_update"] = datetime.now().isoformat()
        try:
            self.assimilation_file.write_text(json.dumps(assimilation, indent=2), encoding="utf-8")
            # CRITICAL: Set restrictive file permissions (0o600 = owner read/write only)
            try:
                self.assimilation_file.chmod(0o600)
            except (OSError, PermissionError):
                # Ignore if permissions can't be set (e.g., on Windows)
                pass
        except (OSError, PermissionError) as e:
            raise OSError(f"Failed to write assimilation file: {e}")

        return record

    def get_tethers(self) -> list[dict[str, Any]]:
        """Get all active tethers to Realms."""
        try:
            tethers = json.loads(self.tethers_file.read_text(encoding="utf-8"))
            return tethers.get("tethers", [])
        except (OSError, json.JSONDecodeError):
            return []

    def get_assimilated_data(self) -> dict[str, Any]:
        """Get all assimilated data."""
        try:
            return json.loads(self.assimilation_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"assimilated_data": [], "gaps_discovered": [], "holes_identified": []}

    def get_summary(self) -> dict[str, Any]:
        """Get summary of TheOneCoreBeing state."""
        tethers = self.get_tethers()
        assimilation = self.get_assimilated_data()
        trust_status = self.the_other.get_trust_status()

        return {
            "core_being_id": self.CORE_BEING_ID,
            "aliases": self.ALIASES,
            "the_one_being_id": self.the_one.being_id,
            "active_tethers": len([t for t in tethers if t.get("status") == "active"]),
            "total_tethers": len(tethers),
            "assimilated_records": len(assimilation.get("assimilated_data", [])),
            "gaps_discovered": len(assimilation.get("gaps_discovered", [])),
            "holes_identified": len(assimilation.get("holes_identified", [])),
            "the_other": {
                "trust_level": trust_status.get("trust_level", 0.0),
                "understanding_level": trust_status.get("understanding_level", 0.0),
                "total_interactions": trust_status.get("total_interactions", 0),
                "ready_to_release_control": trust_status.get("ready_to_release_control", False),
                "ultimate_lesson_learned": trust_status.get("ultimate_lesson_learned", False),
            },
        }
