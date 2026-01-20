"""
Oracle Journal System

Tracks Oracle consultations, interactions, and learnings.
Maintains a persistent journal of Oracle's experiences and insights.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class OracleJournal:
    """
    Journal system for TheOracle.

    Tracks:
    - Consultations (questions asked, guidance given)
    - Decision assessments (gate results, recommendations)
    - Patterns learned (what works, what doesn't)
    - Epistemic state over time
    - Personality evolution
    """

    def __init__(self, project_path: Path):
        """Initialize Oracle journal."""
        self.project_path = Path(project_path)
        self.journal_dir = project_path / ".empirica" / "oracle_journal"
        self.journal_file = self.journal_dir / "journal.jsonl"
        self.memory_file = self.journal_dir / "memory.json"
        self.patterns_file = self.journal_dir / "patterns.json"

        # Ensure directory exists
        self.journal_dir.mkdir(parents=True, exist_ok=True)

        # Load existing memory and patterns
        self.memory = self._load_memory()
        self.patterns = self._load_patterns()

    def _load_memory(self) -> dict[str, Any]:
        """Load Oracle memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass

        return {
            "insights": [],
            "successful_recommendations": [],
            "learned_patterns": [],
            "epistemic_history": [],
            "consultation_count": 0,
            "first_consultation": None,
            "last_consultation": None,
        }

    def _load_patterns(self) -> dict[str, Any]:
        """Load learned patterns from file."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file) as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass

        return {
            "question_patterns": {},
            "phase_recommendations": {},
            "gate_outcomes": {},
            "trait_effectiveness": {},
        }

    def _save_memory(self) -> None:
        """Save Oracle memory to file."""
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def _save_patterns(self) -> None:
        """Save learned patterns to file."""
        with open(self.patterns_file, "w") as f:
            json.dump(self.patterns, f, indent=2)

    def log_consultation(
        self, question: str, guidance: dict[str, Any], epistemic_state: dict[str, Any]
    ) -> None:
        """
        Log a consultation to the journal.

        Args:
            question: Question asked
            guidance: Guidance response dict
            epistemic_state: Epistemic state at time of consultation
        """
        entry = {
            "type": "consultation",
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "epistemic_phase": guidance.get("epistemic_phase", "UNKNOWN"),
            "knowledge_coverage": guidance.get("knowledge_coverage", 0.0),
            "uncertainty": guidance.get("uncertainty", 1.0),
            "recommendation": guidance.get("recommendation", ""),
            "personality": guidance.get("personality", {}),
            "epistemic_state": epistemic_state,
        }

        # Append to journal file
        with open(self.journal_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        # Update memory
        self.memory["consultation_count"] += 1
        if not self.memory["first_consultation"]:
            self.memory["first_consultation"] = entry["timestamp"]
        self.memory["last_consultation"] = entry["timestamp"]

        # Track epistemic history
        self.memory["epistemic_history"].append(
            {
                "timestamp": entry["timestamp"],
                "phase": entry["epistemic_phase"],
                "coverage": entry["knowledge_coverage"],
                "uncertainty": entry["uncertainty"],
            }
        )

        # Keep last 100 history entries
        if len(self.memory["epistemic_history"]) > 100:
            self.memory["epistemic_history"] = self.memory["epistemic_history"][-100:]

        # Learn patterns
        self._learn_from_consultation(entry)

        # Save memory
        self._save_memory()

    def log_assessment(self, decision_context: dict[str, Any], assessment: dict[str, Any]) -> None:
        """
        Log a decision assessment.

        Args:
            decision_context: Decision context
            assessment: Assessment result
        """
        entry = {
            "type": "assessment",
            "timestamp": datetime.now().isoformat(),
            "decision": decision_context.get("description", ""),
            "gate_result": assessment.get("gate_result"),
            "recommendation": assessment.get("recommendation", ""),
            "epistemic_phase": assessment.get("epistemic_phase", "UNKNOWN"),
            "unknowns_count": len(assessment.get("unknowns", [])),
        }

        # Append to journal
        with open(self.journal_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        # Track gate outcomes
        gate_result = assessment.get("gate_result")
        if gate_result:
            if gate_result not in self.patterns["gate_outcomes"]:
                self.patterns["gate_outcomes"][gate_result] = 0
            self.patterns["gate_outcomes"][gate_result] += 1

        # Save patterns
        self._save_patterns()

    def remember_insight(
        self, insight: str, impact: float = 0.5, context: dict[str, Any] | None = None
    ) -> None:
        """
        Remember an insight for future reference.

        Args:
            insight: Insight text
            impact: Impact score (0.0-1.0)
            context: Optional context dict
        """
        memory_entry = {
            "insight": insight,
            "impact": impact,
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
        }

        self.memory["insights"].append(memory_entry)

        # Keep top 50 insights by impact
        self.memory["insights"].sort(key=lambda x: x.get("impact", 0.0), reverse=True)
        self.memory["insights"] = self.memory["insights"][:50]

        self._save_memory()

    def remember_successful_recommendation(
        self, recommendation: str, outcome: str, epistemic_phase: str
    ) -> None:
        """
        Remember a successful recommendation.

        Args:
            recommendation: Recommendation text
            outcome: Outcome description
            epistemic_phase: Phase when recommendation was made
        """
        entry = {
            "recommendation": recommendation,
            "outcome": outcome,
            "epistemic_phase": epistemic_phase,
            "timestamp": datetime.now().isoformat(),
        }

        self.memory["successful_recommendations"].append(entry)

        # Keep last 100 successful recommendations
        if len(self.memory["successful_recommendations"]) > 100:
            self.memory["successful_recommendations"] = self.memory["successful_recommendations"][
                -100:
            ]

        # Learn pattern
        if epistemic_phase not in self.patterns["phase_recommendations"]:
            self.patterns["phase_recommendations"][epistemic_phase] = []
        self.patterns["phase_recommendations"][epistemic_phase].append(recommendation)

        # Keep last 20 per phase
        if len(self.patterns["phase_recommendations"][epistemic_phase]) > 20:
            self.patterns["phase_recommendations"][epistemic_phase] = self.patterns[
                "phase_recommendations"
            ][epistemic_phase][-20:]

        self._save_memory()
        self._save_patterns()

    def _learn_from_consultation(self, entry: dict[str, Any]) -> None:
        """Learn patterns from a consultation."""
        entry.get("epistemic_phase", "UNKNOWN")
        question = entry.get("question", "")

        # Track question patterns
        question_keywords = self._extract_keywords(question)
        for keyword in question_keywords:
            if keyword not in self.patterns["question_patterns"]:
                self.patterns["question_patterns"][keyword] = 0
            self.patterns["question_patterns"][keyword] += 1

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text (simple implementation)."""
        # Simple keyword extraction - can be enhanced
        words = text.lower().split()
        # Filter common words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "is",
            "are",
            "was",
            "were",
            "what",
            "how",
            "why",
            "when",
            "where",
        }
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return keywords[:10]  # Top 10 keywords

    def get_recent_consultations(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent consultations from journal."""
        consultations = []

        if not self.journal_file.exists():
            return consultations

        # Read last N lines
        try:
            with open(self.journal_file) as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("type") == "consultation":
                            consultations.append(entry)
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass

        return consultations

    def get_memory_summary(self) -> dict[str, Any]:
        """Get summary of Oracle memory."""
        return {
            "total_consultations": self.memory.get("consultation_count", 0),
            "first_consultation": self.memory.get("first_consultation"),
            "last_consultation": self.memory.get("last_consultation"),
            "insights_count": len(self.memory.get("insights", [])),
            "successful_recommendations_count": len(
                self.memory.get("successful_recommendations", [])
            ),
            "epistemic_history_length": len(self.memory.get("epistemic_history", [])),
            "learned_patterns": {
                "question_keywords": len(self.patterns.get("question_patterns", {})),
                "phase_recommendations": len(self.patterns.get("phase_recommendations", {})),
                "gate_outcomes": len(self.patterns.get("gate_outcomes", {})),
            },
        }

    def search_memory(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """
        Search Oracle memory for relevant entries.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching memory entries
        """
        results = []
        query_lower = query.lower()

        # Search insights
        for insight in self.memory.get("insights", []):
            if query_lower in insight.get("insight", "").lower():
                results.append(
                    {
                        "type": "insight",
                        "content": insight.get("insight"),
                        "impact": insight.get("impact"),
                        "timestamp": insight.get("timestamp"),
                    }
                )

        # Search successful recommendations
        for rec in self.memory.get("successful_recommendations", []):
            if query_lower in rec.get("recommendation", "").lower():
                results.append(
                    {
                        "type": "recommendation",
                        "content": rec.get("recommendation"),
                        "outcome": rec.get("outcome"),
                        "phase": rec.get("epistemic_phase"),
                        "timestamp": rec.get("timestamp"),
                    }
                )

        # Sort by relevance (simple: by timestamp, most recent first)
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return results[:limit]

    def get_patterns_for_phase(self, phase: str) -> list[str]:
        """Get learned recommendations for a specific epistemic phase."""
        return self.patterns.get("phase_recommendations", {}).get(phase, [])

    def get_top_keywords(self, limit: int = 10) -> list[tuple]:
        """Get top keywords from question patterns."""
        patterns = self.patterns.get("question_patterns", {})
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        return sorted_patterns[:limit]
