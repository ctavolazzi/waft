"""
KarmaCollector: Yama - The Reaper of Karma

The KarmaCollector (lore name: "Yama") collects karma from completed experiences
and life cycles, processing them and transferring karma to souls in Akasha.

Process:
1. Finds completed life logs/experiences
2. Calculates karma using KarmaMerchant
3. Transfers karma to souls in Akasha
4. Archives completed lifetimes
5. Prepares souls for reincarnation

In Hindu mythology, Yama is the god of death who judges souls and determines
their fate. He collects souls and sends them to their next life, working
in partnership with Chitragupta (KarmaMerchant) who records all actions.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class KarmaCollector:
    """
    Yama: The Reaper of Karma

    Collects karma from completed experiences and life cycles:
    - Scans for completed life logs
    - Calculates karma using KarmaMerchant
    - Transfers karma to souls in Akasha
    - Archives completed lifetimes
    - Prepares souls for reincarnation

    Works in partnership with KarmaMerchant (Chitragupta):
    - KarmaMerchant: Records karma, manages store, handles reincarnation
    - KarmaCollector: Collects karma from experiences, processes life logs
    """

    def __init__(self, project_path: Path | None = None, karma_merchant: Any | None = None):
        """
        Initialize the KarmaCollector.

        Args:
            project_path: Path to project root (defaults to current directory)
            karma_merchant: KarmaMerchant instance (creates new if not provided)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.akasha_path = project_path / "_hidden" / ".truth"
        self.life_logs_path = project_path / "_hidden" / ".truth" / "life_logs"
        self.collected_path = project_path / "_hidden" / ".truth" / "collected"

        # Ensure directories exist
        self.akasha_path.mkdir(parents=True, exist_ok=True)
        self.life_logs_path.mkdir(parents=True, exist_ok=True)
        self.collected_path.mkdir(parents=True, exist_ok=True)

        # Initialize KarmaMerchant
        if karma_merchant is None:
            from .karma import KarmaMerchant

            self.karma_merchant = KarmaMerchant(project_path)
        else:
            self.karma_merchant = karma_merchant

    def collect_karma(
        self, life_log: dict[str, Any], soul_id: str, lifetime_id: str | None = None
    ) -> dict[str, Any]:
        """
        Collect karma from a completed life log.

        Process:
        1. Calculate karma using KarmaMerchant
        2. Transfer karma to soul in Akasha
        3. Archive life log
        4. Record collection

        Args:
            life_log: Complete life record containing:
                - journal: List of journal entries
                - memory: Conversation/experience history
                - psyche: Psychological state
                - short_term_memory: Recent experiences
                - Any other experiential data
            soul_id: Unique identifier for the soul
            lifetime_id: Optional lifetime identifier (generated if not provided)

        Returns:
            Dictionary containing:
                - karma_collected: Amount of karma collected
                - soul_id: Soul identifier
                - lifetime_id: Lifetime identifier
                - total_karma: Total karma after collection
                - collected_at: Timestamp of collection
        """
        # Generate lifetime ID if not provided
        if lifetime_id is None:
            lifetime_id = f"lifetime_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(json.dumps(life_log, sort_keys=True).encode()).hexdigest()[:8]}"

        # Calculate karma
        karma_earned = self.karma_merchant.calculate_karma(life_log)

        # If karma calculation not implemented, use default formula
        if karma_earned is None or karma_earned == 0:
            karma_earned = self._calculate_karma_fallback(life_log)

        # Transfer karma to soul in Akasha
        self._transfer_karma_to_soul(soul_id, lifetime_id, karma_earned, life_log)

        # Archive life log
        self._archive_life_log(soul_id, lifetime_id, life_log)

        # Record collection
        collection_record = {
            "soul_id": soul_id,
            "lifetime_id": lifetime_id,
            "karma_collected": karma_earned,
            "collected_at": datetime.now().isoformat(),
            "life_log_summary": {
                "journal_entries": len(life_log.get("journal", [])),
                "memory_entries": len(life_log.get("memory", [])),
                "short_term_memory": len(life_log.get("short_term_memory", [])),
            },
        }

        self._record_collection(collection_record)

        # Get updated total karma
        total_karma = self._get_soul_total_karma(soul_id)

        return {
            "karma_collected": karma_earned,
            "soul_id": soul_id,
            "lifetime_id": lifetime_id,
            "total_karma": total_karma,
            "collected_at": collection_record["collected_at"],
        }

    def collect_from_life_log_file(self, life_log_path: Path, soul_id: str) -> dict[str, Any]:
        """
        Collect karma from a life log file.

        Args:
            life_log_path: Path to life log JSON file
            soul_id: Unique identifier for the soul

        Returns:
            Collection result dictionary
        """
        if not life_log_path.exists():
            raise FileNotFoundError(f"Life log not found: {life_log_path}")

        # Load life log
        with open(life_log_path) as f:
            life_log = json.load(f)

        # Collect karma
        result = self.collect_karma(life_log, soul_id)

        # Move file to collected directory
        collected_file = self.collected_path / life_log_path.name
        if collected_file.exists():
            # Add timestamp if file exists
            collected_file = (
                self.collected_path
                / f"{life_log_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{life_log_path.suffix}"
            )
        life_log_path.rename(collected_file)

        return result

    def collect_all_pending(self, soul_id: str | None = None) -> list[dict[str, Any]]:
        """
        Collect karma from all pending life logs.

        Scans the life_logs directory for unprocessed life logs and collects
        karma from each one.

        Args:
            soul_id: Optional soul ID filter (collects all if not provided)

        Returns:
            List of collection results
        """
        results = []

        # Find all life log files
        life_log_files = list(self.life_logs_path.glob("*.json"))

        for life_log_file in life_log_files:
            try:
                # Try to extract soul_id from filename or file content
                file_soul_id = self._extract_soul_id_from_file(life_log_file, soul_id)

                if soul_id is None or file_soul_id == soul_id:
                    result = self.collect_from_life_log_file(life_log_file, file_soul_id)
                    results.append(result)
            except Exception as e:
                # Log error but continue
                print(f"Error collecting from {life_log_file}: {e}")
                continue

        return results

    def _calculate_karma_fallback(self, life_log: dict[str, Any]) -> float:
        """
        Fallback karma calculation if KarmaMerchant.calculate_karma not implemented.

        Simple formula based on experience intensity:
        - Journal entries: 1.0 karma each
        - Memory entries: 0.5 karma each
        - Short-term memory: 0.1 karma each
        - Emotional intensity: Multiplier based on psyche state

        Args:
            life_log: Life log dictionary

        Returns:
            Calculated karma amount
        """
        karma = 0.0

        # Journal entries (high value - personal reflections)
        journal = life_log.get("journal", [])
        karma += len(journal) * 1.0

        # Memory entries (medium value - experiences)
        memory = life_log.get("memory", [])
        karma += len(memory) * 0.5

        # Short-term memory (low value - recent thoughts)
        short_term = life_log.get("short_term_memory", [])
        karma += len(short_term) * 0.1

        # Emotional intensity multiplier
        psyche = life_log.get("psyche", {})
        emotional_energy = psyche.get("emotional_energy", 50.0)
        intensity_multiplier = emotional_energy / 100.0  # 0.0 to 1.0

        # Apply multiplier
        karma *= 1.0 + intensity_multiplier

        # Chaos multiplier (chaos = more intense experiences)
        chaos = psyche.get("chaos", 0.0)
        chaos_multiplier = 1.0 + (chaos * 0.5)  # Up to 1.5x

        karma *= chaos_multiplier

        return max(0.0, karma)

    def _transfer_karma_to_soul(
        self, soul_id: str, lifetime_id: str, karma_amount: float, life_log: dict[str, Any]
    ) -> None:
        """
        Transfer karma to soul in Akasha.

        Args:
            soul_id: Soul identifier
            lifetime_id: Lifetime identifier
            karma_amount: Amount of karma to transfer
            life_log: Life log data
        """
        # Load or create soul record
        soul_file = self.akasha_path / f"{soul_id}.json"

        if soul_file.exists():
            with open(soul_file) as f:
                soul_data = json.load(f)
        else:
            # Create new soul record
            soul_data = {
                "soul_id": soul_id,
                "total_karma": 0.0,
                "lifetimes": [],
                "created_at": datetime.now().isoformat(),
            }

        # Add lifetime record
        lifetime_record = {
            "lifetime_id": lifetime_id,
            "karma_earned": karma_amount,
            "collected_at": datetime.now().isoformat(),
            "life_log_summary": {
                "journal_entries": len(life_log.get("journal", [])),
                "memory_entries": len(life_log.get("memory", [])),
            },
        }

        soul_data["lifetimes"].append(lifetime_record)
        soul_data["total_karma"] = soul_data.get("total_karma", 0.0) + karma_amount
        soul_data["updated_at"] = datetime.now().isoformat()

        # Save soul record
        with open(soul_file, "w") as f:
            json.dump(soul_data, f, indent=2)

    def _archive_life_log(self, soul_id: str, lifetime_id: str, life_log: dict[str, Any]) -> None:
        """
        Archive a life log.

        Args:
            soul_id: Soul identifier
            lifetime_id: Lifetime identifier
            life_log: Life log data
        """
        archive_dir = self.akasha_path / "archives" / soul_id
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_file = archive_dir / f"{lifetime_id}.json"
        with open(archive_file, "w") as f:
            json.dump(life_log, f, indent=2)

    def _record_collection(self, collection_record: dict[str, Any]) -> None:
        """
        Record a collection event.

        Args:
            collection_record: Collection record dictionary
        """
        collection_log = self.collected_path / "collection_log.jsonl"

        with open(collection_log, "a") as f:
            f.write(json.dumps(collection_record) + "\n")

    def _get_soul_total_karma(self, soul_id: str) -> float:
        """
        Get total karma for a soul.

        Args:
            soul_id: Soul identifier

        Returns:
            Total karma amount
        """
        soul_file = self.akasha_path / f"{soul_id}.json"

        if soul_file.exists():
            with open(soul_file) as f:
                soul_data = json.load(f)
            return soul_data.get("total_karma", 0.0)

        return 0.0

    def _extract_soul_id_from_file(
        self, life_log_file: Path, default_soul_id: str | None = None
    ) -> str:
        """
        Extract soul_id from life log file.

        Args:
            life_log_file: Path to life log file
            default_soul_id: Default soul ID if not found in file

        Returns:
            Soul ID
        """
        # Try to load file and extract soul_id
        try:
            with open(life_log_file) as f:
                life_log = json.load(f)
                return life_log.get("soul_id", default_soul_id or "unknown_soul")
        except Exception:
            # Fallback: try to extract from filename
            if default_soul_id:
                return default_soul_id
            # Last resort: use filename stem
            return life_log_file.stem.split("_")[0] if "_" in life_log_file.stem else "unknown_soul"

    def get_collection_stats(self) -> dict[str, Any]:
        """
        Get statistics about karma collection.

        Returns:
            Dictionary with collection statistics
        """
        # Count collected lifetimes
        collection_log = self.collected_path / "collection_log.jsonl"
        total_collected = 0
        total_karma_collected = 0.0

        if collection_log.exists():
            with open(collection_log) as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        total_collected += 1
                        total_karma_collected += record.get("karma_collected", 0.0)

        # Count pending life logs
        pending_logs = list(self.life_logs_path.glob("*.json"))
        pending_count = len(pending_logs)

        # Count souls in Akasha
        soul_files = list(self.akasha_path.glob("*.json"))
        soul_count = len([f for f in soul_files if f.name != "collection_log.jsonl"])

        return {
            "total_collected": total_collected,
            "total_karma_collected": total_karma_collected,
            "pending_life_logs": pending_count,
            "souls_in_akasha": soul_count,
            "collection_log_path": str(collection_log) if collection_log.exists() else None,
        }

    def collect_from_agent_state(self, agent_state: dict[str, Any], soul_id: str) -> dict[str, Any]:
        """
        Collect karma from an AgentState object.

        Converts AgentState to life log format and collects karma.

        Args:
            agent_state: AgentState dictionary
            soul_id: Soul identifier

        Returns:
            Collection result dictionary
        """
        # Convert AgentState to life log format
        life_log = {
            "journal": agent_state.get("journal", []),
            "memory": agent_state.get("memory", []),
            "short_term_memory": agent_state.get("short_term_memory", []),
            "psyche": agent_state.get("epistemic_state", {}),
            "agent_id": agent_state.get("agent_id", ""),
            "role": agent_state.get("role", ""),
            "goal": agent_state.get("goal", ""),
        }

        return self.collect_karma(life_log, soul_id)


# Convenience function


def collect_karma_from_life_log(
    life_log: dict[str, Any], soul_id: str, project_path: Path | None = None
) -> dict[str, Any]:
    """
    Convenience function to collect karma from a life log.

    Args:
        life_log: Life log dictionary
        soul_id: Soul identifier
        project_path: Optional project path

    Returns:
        Collection result dictionary
    """
    collector = KarmaCollector(project_path=project_path)
    return collector.collect_karma(life_log, soul_id)
