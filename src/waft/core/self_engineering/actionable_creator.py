"""
Actionable Creator: Converts notebook findings into work efforts, scenarios, quests.

Takes notebook entries and reflections and creates actionable work items.

Integrates with Empirica for decision support and epistemic tracking.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from .notebook import NotebookEntry, Reflection


class ActionableCreator:
    """Creates actionable items from notebook findings."""

    def __init__(
        self,
        project_path: Path,
        work_efforts_dir: Path,
        scenarios_dir: Path,
        quests_dir: Path,
        empirica_manager=None,
    ):
        """
        Initialize actionable creator.

        Args:
            project_path: Project root path
            work_efforts_dir: Directory for work efforts (e.g., _work_efforts/)
            scenarios_dir: Directory for scenarios (e.g., examples/)
            quests_dir: Directory for quests (e.g., src/gym/rpg/dungeons/)
            empirica_manager: Optional EmpiricaManager for decision support
        """
        self.project_path = Path(project_path)
        self.work_efforts_dir = Path(work_efforts_dir)
        self.scenarios_dir = Path(scenarios_dir)
        self.quests_dir = Path(quests_dir)
        self.empirica_manager = empirica_manager

    def create_work_effort_from_entry(
        self, entry: NotebookEntry, use_empirica: bool = True
    ) -> dict[str, Any]:
        """
        Create a work effort from a notebook entry.

        Args:
            entry: Notebook entry to convert
            use_empirica: Whether to use Empirica for decision support

        Returns:
            Work effort metadata (for MCP work-efforts server)
        """
        # Check with Empirica if operation is safe to proceed
        if use_empirica and self.empirica_manager and self.empirica_manager.is_initialized():
            gate_result = self.empirica_manager.check_submit(
                {
                    "type": "work_effort_creation",
                    "scope": "medium",
                    "description": f"Create work effort from {entry.entry_type.value}",
                    "severity": entry.metadata.get("severity", "medium"),
                }
            )

            if gate_result == "HALT":
                # Operation requires approval - return None or raise
                return {
                    "id": None,
                    "status": "HALT",
                    "message": "Empirica gate: Operation requires human approval",
                }
            elif gate_result == "BRANCH":
                # Need investigation first
                return {
                    "id": None,
                    "status": "BRANCH",
                    "message": "Empirica gate: Need investigation before creating work effort",
                }

        # Generate work effort ID
        work_effort_id = f"WE-{datetime.now().strftime('%y%m%d')}-{entry.entry_id[-4:]}"

        # Determine priority from severity
        priority_map = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}
        priority = priority_map.get(entry.metadata.get("severity", "medium").lower(), "MEDIUM")

        # Use Empirica epistemic state to inform priority if available
        if use_empirica and self.empirica_manager and self.empirica_manager.is_initialized():
            epistemic_context = self.empirica_manager.project_bootstrap()
            if epistemic_context:
                # Adjust priority based on epistemic state
                uncertainty = (
                    epistemic_context.get("epistemic_state", {})
                    .get("vectors", {})
                    .get("uncertainty", 0.5)
                )
                # Higher uncertainty = higher priority (need to learn more)
                if uncertainty > 0.7 and priority == "MEDIUM":
                    priority = "HIGH"

        # Create work effort structure
        work_effort_data = {
            "id": work_effort_id,
            "title": entry.title.replace("Problem Detected: ", "").replace("Diagnosis: ", ""),
            "status": "open",
            "priority": priority,
            "created": datetime.now().isoformat(),
            "created_by": "self_engineering_system",
            "last_updated": datetime.now().isoformat(),
            "branch": "main",
            "repository": "waft",
            "objective": entry.content,
            "source": {
                "notebook_entry": entry.entry_id,
                "entry_type": entry.entry_type.value,
                "timestamp": entry.timestamp,
            },
        }

        return work_effort_data

    def create_scenario_from_entry(self, entry: NotebookEntry) -> dict[str, Any]:
        """
        Create a D&D scenario from a notebook entry.

        Args:
            entry: Notebook entry to convert

        Returns:
            Scenario metadata and code structure
        """
        scenario_id = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Extract scenario elements from entry
        problem_type = entry.metadata.get("problem_type", "unknown")
        description = entry.content

        scenario_data = {
            "scenario_id": scenario_id,
            "title": entry.title.replace("Problem Detected: ", "").replace("Diagnosis: ", ""),
            "description": description,
            "problem_type": problem_type,
            "source_entry": entry.entry_id,
            "created": datetime.now().isoformat(),
            "template": "tavern_scenario",  # Default template
            "metadata": {
                "severity": entry.metadata.get("severity", "medium"),
                "entry_type": entry.entry_type.value,
            },
        }

        return scenario_data

    def create_quest_from_entry(self, entry: NotebookEntry) -> dict[str, Any]:
        """
        Create a D&D quest from a notebook entry.

        Args:
            entry: Notebook entry to convert

        Returns:
            Quest data (for JSON quest file)
        """
        quest_id = f"quest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Map severity to difficulty (1-10)
        difficulty_map = {"critical": 9, "high": 7, "medium": 5, "low": 3}
        difficulty = difficulty_map.get(entry.metadata.get("severity", "medium").lower(), 5)

        quest_data = {
            "name": entry.title.replace("Problem Detected: ", "").replace("Diagnosis: ", ""),
            "difficulty": difficulty,
            "description": entry.content[:500],  # Truncate for quest description
            "win_condition": "problem_resolved",  # Default win condition
            "loot_table": {"xp": difficulty * 10, "karma": difficulty * 5},
            "metadata": {
                "source_entry": entry.entry_id,
                "entry_type": entry.entry_type.value,
                "severity": entry.metadata.get("severity", "medium"),
            },
        }

        return quest_data

    def create_from_reflection(self, reflection: Reflection) -> list[dict[str, Any]]:
        """
        Create actionable items from reflection suggestions.

        Args:
            reflection: Reflection with actionable suggestions

        Returns:
            List of created actionable items
        """
        created = []

        for suggestion in reflection.actionable_suggestions:
            # Find the source entry
            entry_id = suggestion.get("source_entry")
            if not entry_id:
                continue

            # Load entry (would need notebook manager reference)
            # For now, create based on suggestion

            if suggestion["type"] == "work_effort":
                created.append(
                    {
                        "type": "work_effort",
                        "title": suggestion["title"],
                        "description": suggestion["description"],
                        "priority": suggestion.get("priority", "MEDIUM"),
                    }
                )

            elif suggestion["type"] == "scenario":
                created.append(
                    {
                        "type": "scenario",
                        "title": suggestion["title"],
                        "description": suggestion["description"],
                    }
                )

            elif suggestion["type"] == "quest":
                created.append(
                    {
                        "type": "quest",
                        "title": suggestion["title"],
                        "description": suggestion["description"],
                    }
                )

        return created
