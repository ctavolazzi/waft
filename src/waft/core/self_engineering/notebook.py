"""
Self-Engineering Notebook System

The system's "notebook" - journals findings, reflects on problems, and converts
insights into actionable work (scenarios, quests, work efforts).

Integrates with Empirica for epistemic tracking and decision support.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from .problem_detector import Problem


class NotebookEntryType(Enum):
    """Types of notebook entries."""

    PROBLEM_DETECTED = "problem_detected"
    DIAGNOSIS = "diagnosis"
    SOLUTION_PROPOSED = "solution_proposed"
    SOLUTION_IMPLEMENTED = "solution_implemented"
    REFLECTION = "reflection"
    INSIGHT = "insight"
    ITERATION = "iteration"


class ActionableType(Enum):
    """Types of actionable items that can be created."""

    WORK_EFFORT = "work_effort"
    SCENARIO = "scenario"
    QUEST = "quest"
    TICKET = "ticket"


@dataclass
class NotebookEntry:
    """A single notebook entry."""

    entry_id: str
    entry_type: NotebookEntryType
    timestamp: float
    title: str
    content: str
    metadata: dict[str, Any]
    related_problems: list[str] = None  # Problem IDs
    related_diagnoses: list[str] = None  # Diagnosis IDs
    actionable_type: ActionableType | None = None
    actionable_created: bool = False
    actionable_id: str | None = None  # ID of created work effort/scenario/quest

    def __post_init__(self):
        """Initialize defaults."""
        if self.related_problems is None:
            self.related_problems = []
        if self.related_diagnoses is None:
            self.related_diagnoses = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "entry_id": self.entry_id,
            "entry_type": self.entry_type.value,
            "timestamp": self.timestamp,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
            "related_problems": self.related_problems,
            "related_diagnoses": self.related_diagnoses,
            "actionable_type": self.actionable_type.value if self.actionable_type else None,
            "actionable_created": self.actionable_created,
            "actionable_id": self.actionable_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NotebookEntry":
        """Create from dictionary."""
        return cls(
            entry_id=data["entry_id"],
            entry_type=NotebookEntryType(data["entry_type"]),
            timestamp=data["timestamp"],
            title=data["title"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            related_problems=data.get("related_problems", []),
            related_diagnoses=data.get("related_diagnoses", []),
            actionable_type=ActionableType(data["actionable_type"])
            if data.get("actionable_type")
            else None,
            actionable_created=data.get("actionable_created", False),
            actionable_id=data.get("actionable_id"),
        )


@dataclass
class Reflection:
    """A reflection on findings."""

    reflection_id: str
    timestamp: float
    entry_ids: list[str]  # Notebook entry IDs being reflected on
    insights: list[str]
    patterns: list[str]
    questions: list[str]
    recommendations: list[str]
    actionable_suggestions: list[dict[str, Any]]  # Suggestions for work efforts/scenarios/quests

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Reflection":
        """Create from dictionary."""
        return cls(**data)


class NotebookManager:
    """Manages the self-engineering notebook."""

    def __init__(self, notebook_dir: Path, empirica_manager=None):
        """
        Initialize notebook manager.

        Args:
            notebook_dir: Directory for notebook files (e.g., project_root/_notebook/)
            empirica_manager: Optional EmpiricaManager for epistemic tracking
        """
        self.notebook_dir = Path(notebook_dir)
        self.notebook_dir.mkdir(parents=True, exist_ok=True)

        # Empirica integration
        self.empirica_manager = empirica_manager

        # Subdirectories
        self.entries_dir = self.notebook_dir / "entries"
        self.reflections_dir = self.notebook_dir / "reflections"
        self.actionables_dir = self.notebook_dir / "actionables"

        # Create subdirectories
        self.entries_dir.mkdir(exist_ok=True)
        self.reflections_dir.mkdir(exist_ok=True)
        self.actionables_dir.mkdir(exist_ok=True)

        # Index file
        self.index_file = self.notebook_dir / "index.json"
        self._load_index()

    def _load_index(self):
        """Load or create index."""
        if self.index_file.exists():
            with open(self.index_file) as f:
                self.index = json.load(f)
        else:
            self.index = {
                "entries": [],
                "reflections": [],
                "actionables": [],
                "last_updated": datetime.now().isoformat(),
            }
            self._save_index()

    def _save_index(self):
        """Save index."""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=2)

    def journal_problem(self, problem: Problem, context: dict[str, Any] = None) -> NotebookEntry:
        """
        Journal a detected problem.

        Args:
            problem: Detected problem
            context: Additional context

        Returns:
            Created notebook entry
        """
        entry_id = f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{problem.type.value}"

        entry = NotebookEntry(
            entry_id=entry_id,
            entry_type=NotebookEntryType.PROBLEM_DETECTED,
            timestamp=problem.timestamp,
            title=f"Problem Detected: {problem.type.value}",
            content=f"""
**Problem Type**: {problem.type.value}
**Severity**: {problem.severity.value}
**Description**: {problem.description}

**Context**:
{json.dumps(problem.context, indent=2)}

**Exception**: {problem.exception if problem.exception else "None"}
""".strip(),
            metadata={
                "problem_type": problem.type.value,
                "severity": problem.severity.value,
                "exception_type": type(problem.exception).__name__ if problem.exception else None,
                "exception_message": str(problem.exception) if problem.exception else None,
                **({} if context is None else context),
            },
            related_problems=[entry_id],
        )

        self._save_entry(entry)

        # Log to Empirica if available
        if self.empirica_manager and self.empirica_manager.is_initialized():
            # Log as finding with impact based on severity
            impact_map = {"critical": 0.9, "high": 0.7, "medium": 0.5, "low": 0.3}
            impact = impact_map.get(problem.severity.value.lower(), 0.5)
            finding = f"Problem detected: {problem.type.value} - {problem.description[:100]}"
            self.empirica_manager.log_finding(finding, impact=impact)

            # Log unknowns for high-severity problems
            if problem.severity.value.lower() in ["critical", "high"]:
                unknown = f"Why does {problem.type.value} occur? Root cause unknown."
                self.empirica_manager.log_unknown(unknown)

        return entry

    def journal_diagnosis(
        self, problem: Problem, diagnosis: dict[str, Any], context: dict[str, Any] = None
    ) -> NotebookEntry:
        """
        Journal a diagnosis.

        Args:
            problem: Original problem
            diagnosis: Diagnosis result (cause, confidence, explanation, solution_hint)
            context: Additional context

        Returns:
            Created notebook entry
        """
        entry_id = f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}_diagnosis"

        entry = NotebookEntry(
            entry_id=entry_id,
            entry_type=NotebookEntryType.DIAGNOSIS,
            timestamp=datetime.now().timestamp(),
            title=f"Diagnosis: {diagnosis.get('cause', 'Unknown')}",
            content=f"""
**Root Cause**: {diagnosis.get("cause", "Unknown")}
**Confidence**: {diagnosis.get("confidence", 0.0):.2f}
**Explanation**: {diagnosis.get("explanation", "No explanation provided")}

**Solution Hint**: {diagnosis.get("solution_hint", "No hint provided")}

**Original Problem**: {problem.description}
""".strip(),
            metadata={
                "cause": diagnosis.get("cause"),
                "confidence": diagnosis.get("confidence", 0.0),
                **({} if context is None else context),
            },
            related_problems=[entry_id],
        )

        self._save_entry(entry)

        # Log diagnosis to Empirica if available
        if self.empirica_manager and self.empirica_manager.is_initialized():
            # Log as finding (diagnosis is a discovery)
            confidence = diagnosis.get("confidence", 0.0)
            finding = (
                f"Diagnosed: {diagnosis.get('cause', 'Unknown')} (confidence: {confidence:.2f})"
            )
            impact = min(0.9, 0.5 + confidence * 0.4)  # Impact based on confidence
            self.empirica_manager.log_finding(finding, impact=impact)

        return entry

    def journal_reflection(
        self,
        entries: list[NotebookEntry],
        insights: list[str] = None,
        patterns: list[str] = None,
        questions: list[str] = None,
        use_empirica: bool = True,
    ) -> Reflection:
        """
        Journal a reflection on findings.

        Args:
            entries: Notebook entries to reflect on
            insights: Key insights
            patterns: Patterns noticed
            questions: Questions raised

        Returns:
            Created reflection
        """
        reflection_id = f"reflection_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        reflection = Reflection(
            reflection_id=reflection_id,
            timestamp=datetime.now().timestamp(),
            entry_ids=[e.entry_id for e in entries],
            insights=insights or [],
            patterns=patterns or [],
            questions=questions or [],
            recommendations=[],
            actionable_suggestions=[],
        )

        # Generate actionable suggestions based on entries
        for entry in entries:
            if entry.entry_type == NotebookEntryType.PROBLEM_DETECTED:
                # Suggest work effort for high-severity problems
                if entry.metadata.get("severity") in ["critical", "high"]:
                    reflection.actionable_suggestions.append(
                        {
                            "type": "work_effort",
                            "title": f"Fix: {entry.title}",
                            "description": entry.content,
                            "priority": entry.metadata.get("severity", "medium"),
                            "source_entry": entry.entry_id,
                        }
                    )

            elif entry.entry_type == NotebookEntryType.DIAGNOSIS:
                # Suggest scenario or quest for interesting diagnoses
                if entry.metadata.get("confidence", 0.0) > 0.7:
                    reflection.actionable_suggestions.append(
                        {
                            "type": "scenario",
                            "title": f"Scenario: {entry.metadata.get('cause', 'Unknown Issue')}",
                            "description": f"Explore the problem: {entry.content}",
                            "source_entry": entry.entry_id,
                        }
                    )

        self._save_reflection(reflection)

        # Log reflection insights to Empirica if available and enabled
        if use_empirica and self.empirica_manager and self.empirica_manager.is_initialized():
            # Get epistemic state to inform reflection
            self.empirica_manager.project_bootstrap()

            # Log insights as findings
            for insight in insights or []:
                self.empirica_manager.log_finding(f"Insight: {insight}", impact=0.6)

            # Log patterns as findings (patterns are discoveries)
            for pattern in patterns or []:
                self.empirica_manager.log_finding(f"Pattern: {pattern}", impact=0.5)

            # Log questions as unknowns
            for question in questions or []:
                self.empirica_manager.log_unknown(question)

        return reflection

    def _save_entry(self, entry: NotebookEntry):
        """Save notebook entry."""
        entry_file = self.entries_dir / f"{entry.entry_id}.json"
        with open(entry_file, "w") as f:
            json.dump(entry.to_dict(), f, indent=2)

        # Update index
        if entry.entry_id not in self.index["entries"]:
            self.index["entries"].append(entry.entry_id)
        self._save_index()

    def _save_reflection(self, reflection: Reflection):
        """Save reflection."""
        reflection_file = self.reflections_dir / f"{reflection.reflection_id}.json"
        with open(reflection_file, "w") as f:
            json.dump(reflection.to_dict(), f, indent=2)

        # Update index
        if reflection.reflection_id not in self.index["reflections"]:
            self.index["reflections"].append(reflection.reflection_id)
        self._save_index()

    def get_entries(self, entry_type: NotebookEntryType | None = None) -> list[NotebookEntry]:
        """Get all entries, optionally filtered by type."""
        entries = []
        for entry_id in self.index["entries"]:
            entry_file = self.entries_dir / f"{entry_id}.json"
            if entry_file.exists():
                with open(entry_file) as f:
                    data = json.load(f)
                    entry = NotebookEntry.from_dict(data)
                    if entry_type is None or entry.entry_type == entry_type:
                        entries.append(entry)

        return sorted(entries, key=lambda e: e.timestamp, reverse=True)

    def get_reflections(self) -> list[Reflection]:
        """Get all reflections."""
        reflections = []
        for reflection_id in self.index["reflections"]:
            reflection_file = self.reflections_dir / f"{reflection_id}.json"
            if reflection_file.exists():
                with open(reflection_file) as f:
                    data = json.load(f)
                    reflections.append(Reflection.from_dict(data))

        return sorted(reflections, key=lambda r: r.timestamp, reverse=True)

    def _sanitize_for_json(self, data: Any) -> Any:
        """Sanitize data for JSON serialization (convert exceptions, etc.)."""
        if isinstance(data, dict):
            return {k: self._sanitize_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_for_json(item) for item in data]
        elif isinstance(data, Exception):
            return {
                "type": type(data).__name__,
                "message": str(data),
                "args": [str(arg) for arg in data.args] if hasattr(data, "args") else [],
            }
        elif hasattr(data, "__dict__"):
            # Try to convert objects to dict
            try:
                return self._sanitize_for_json(data.__dict__)
            except:
                return str(data)
        else:
            # Check if it's JSON serializable
            try:
                json.dumps(data)
                return data
            except (TypeError, ValueError):
                return str(data)

    def mark_actionable_created(
        self, entry_id: str, actionable_type: ActionableType, actionable_id: str
    ):
        """Mark that an actionable item was created from an entry."""
        entry_file = self.entries_dir / f"{entry_id}.json"
        if entry_file.exists():
            with open(entry_file) as f:
                data = json.load(f)

            entry = NotebookEntry.from_dict(data)
            entry.actionable_created = True
            entry.actionable_type = actionable_type
            entry.actionable_id = actionable_id

            with open(entry_file, "w") as f:
                json.dump(entry.to_dict(), f, indent=2)
