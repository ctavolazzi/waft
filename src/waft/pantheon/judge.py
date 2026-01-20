"""
Judge: God of Judgment and Evaluation

The Judge evaluates claims against the Body of Proof,
rendering judgments based on precedent and evidence.

Following "as above, so below" principles:
- As above: Pantheon god rendering celestial judgments
- So below: File-based system evaluating claims against precedent
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .magistrate import Magistrate, Precedent


class Judgment:
    """A judgment rendered by the Judge."""

    def __init__(
        self,
        claim: str,
        verdict: str,
        confidence: float,
        reasoning: str,
        relevant_precedents: list[Precedent],
        created_at: str | None = None,
    ):
        """
        Initialize a judgment.

        Args:
            claim: The claim being judged
            verdict: PROVEN/DISPROVEN/INCONCLUSIVE
            confidence: Confidence level (0.0-1.0)
            reasoning: Explanation of the judgment
            relevant_precedents: List of precedents used in judgment
            created_at: ISO timestamp when judgment was created
        """
        self.claim = claim
        self.verdict = verdict
        self.confidence = confidence
        self.reasoning = reasoning
        self.relevant_precedents = relevant_precedents
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert judgment to dictionary."""
        return {
            "claim": self.claim,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "relevant_precedents": [p.case_id for p in self.relevant_precedents],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], magistrate: Magistrate) -> "Judgment":
        """Create judgment from dictionary."""
        # Reconstruct precedents from case IDs
        precedents = []
        for case_id in data.get("relevant_precedents", []):
            precedent = magistrate.get_precedent(case_id)
            if precedent:
                precedents.append(precedent)

        return cls(
            claim=data["claim"],
            verdict=data["verdict"],
            confidence=data["confidence"],
            reasoning=data["reasoning"],
            relevant_precedents=precedents,
            created_at=data.get("created_at"),
        )


class Judge:
    """
    Judge: God of Judgment and Evaluation

    Evaluates claims against the Body of Proof (from Magistrate),
    rendering judgments based on precedent and evidence.

    Storage:
    - Judgments: _pantheon/judge/judgments/*.json
    - Judgment History: _pantheon/judge/judgment_history.json
    """

    def __init__(
        self, project_path: Path | None = None, magistrate: Magistrate | None = None
    ):
        """
        Initialize the Judge.

        Args:
            project_path: Path to project root (default: current directory)
            magistrate: Magistrate instance (default: creates new one)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.judge_path = self.pantheon_path / "judge"
        self.judgments_path = self.judge_path / "judgments"

        # Create directory structure
        self.judge_path.mkdir(parents=True, exist_ok=True)
        self.judgments_path.mkdir(parents=True, exist_ok=True)

        # Magistrate (provides Body of Proof)
        if magistrate is None:
            self.magistrate = Magistrate(project_path=project_path)
        else:
            self.magistrate = magistrate

        # Judgment history
        self.judgment_history: list[Judgment] = []
        self._load_judgment_history()

    def _load_judgment_history(self):
        """Load judgment history from disk."""
        history_file = self.judge_path / "judgment_history.json"

        if history_file.exists():
            try:
                with open(history_file, encoding="utf-8") as f:
                    data = json.load(f)
                    self.judgment_history = [
                        Judgment.from_dict(j, self.magistrate) for j in data.get("judgments", [])
                    ]
            except Exception as e:
                print(f"Error loading judgment history: {e}")
                self.judgment_history = []

    def _save_judgment_history(self):
        """Save judgment history to disk."""
        history_file = self.judge_path / "judgment_history.json"

        data = {
            "judgments": [j.to_dict() for j in self.judgment_history],
            "total_count": len(self.judgment_history),
            "updated_at": datetime.now().isoformat(),
        }

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _find_relevant_precedents(
        self,
        claim: str,
        category: str | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[Precedent]:
        """
        Find relevant precedents for a claim.

        Args:
            claim: The claim to find precedents for
            category: Optional category filter
            tags: Optional tags to match
            limit: Maximum number of precedents to return

        Returns:
            List of relevant precedents, sorted by relevance
        """
        # Start with all precedents
        candidates = list(self.magistrate.body_of_proof.precedents)

        # Filter by category if provided
        if category:
            category_precedents = self.magistrate.get_precedents_by_category(category)
            candidates = [p for p in candidates if p in category_precedents]

        # Filter by tags if provided
        if tags:
            tag_precedents = []
            for tag in tags:
                tag_precedents.extend(self.magistrate.get_precedents_by_tag(tag))
            if tag_precedents:
                candidates = [p for p in candidates if p in tag_precedents]

        # If no filters, search by claim text
        if not category and not tags:
            candidates = self.magistrate.search_precedents(claim)

        # Score and sort by relevance
        scored = []
        claim_lower = claim.lower()

        for precedent in candidates:
            score = 0.0

            # Base score from confidence
            if precedent.confidence:
                score += precedent.confidence * 0.3

            # Claim similarity (simple keyword matching)
            if precedent.claim:
                claim_words = set(claim_lower.split())
                precedent_words = set(precedent.claim.lower().split())
                common_words = claim_words.intersection(precedent_words)
                if claim_words:
                    similarity = len(common_words) / len(claim_words)
                    score += similarity * 0.4

            # Tag match boost
            if tags and precedent.tags:
                matching_tags = set(tags).intersection(set(precedent.tags))
                if matching_tags:
                    score += (len(matching_tags) / max(len(tags), len(precedent.tags))) * 0.3

            scored.append((score, precedent))

        # Sort by score (descending) and return top N
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:limit]]

    def evaluate_claim(
        self,
        claim: str,
        category: str | None = None,
        tags: list[str] | None = None,
        context: str | None = None,
    ) -> Judgment:
        """
        Evaluate a claim against the Body of Proof.

        Args:
            claim: The claim to evaluate
            category: Optional category to focus on
            tags: Optional tags to consider
            context: Optional additional context

        Returns:
            Judgment with verdict, confidence, and reasoning
        """
        # Find relevant precedents
        relevant_precedents = self._find_relevant_precedents(claim, category, tags)

        if not relevant_precedents:
            # No precedents found - inconclusive
            reasoning = "No relevant precedents found in Body of Proof. Cannot render judgment."
            judgment = Judgment(
                claim=claim,
                verdict="INCONCLUSIVE",
                confidence=0.0,
                reasoning=reasoning,
                relevant_precedents=[],
            )
            self._save_judgment(judgment)
            return judgment

        # Evaluate against precedents
        supporting = []
        contradicting = []
        neutral = []

        for precedent in relevant_precedents:
            verdict = (precedent.verdict or "").upper()
            confidence = precedent.confidence or 0.5

            if "PROVEN" in verdict:
                supporting.append((precedent, confidence))
            elif "DISPROVEN" in verdict:
                contradicting.append((precedent, confidence))
            else:
                neutral.append((precedent, confidence))

        # Calculate weighted scores
        supporting_weight = sum(conf for _, conf in supporting)
        contradicting_weight = sum(conf for _, conf in contradicting)
        neutral_weight = sum(conf for _, conf in neutral)

        total_weight = supporting_weight + contradicting_weight + neutral_weight

        if total_weight == 0:
            # All precedents have no confidence
            reasoning = f"Found {len(relevant_precedents)} relevant precedents, but none have sufficient confidence."
            judgment = Judgment(
                claim=claim,
                verdict="INCONCLUSIVE",
                confidence=0.0,
                reasoning=reasoning,
                relevant_precedents=relevant_precedents,
            )
            self._save_judgment(judgment)
            return judgment

        # Determine verdict
        if supporting_weight > contradicting_weight * 1.5:
            # Strong support
            verdict = "PROVEN"
            confidence = min(0.95, supporting_weight / total_weight)
            reasoning = f"Claim is PROVEN based on {len(supporting)} supporting precedents (weight: {supporting_weight:.2f}) vs {len(contradicting)} contradicting (weight: {contradicting_weight:.2f})."
        elif contradicting_weight > supporting_weight * 1.5:
            # Strong contradiction
            verdict = "DISPROVEN"
            confidence = min(0.95, contradicting_weight / total_weight)
            reasoning = f"Claim is DISPROVEN based on {len(contradicting)} contradicting precedents (weight: {contradicting_weight:.2f}) vs {len(supporting)} supporting (weight: {supporting_weight:.2f})."
        else:
            # Mixed or inconclusive
            verdict = "INCONCLUSIVE"
            confidence = (
                abs(supporting_weight - contradicting_weight) / total_weight
                if total_weight > 0
                else 0.0
            )
            reasoning = f"Claim is INCONCLUSIVE. Mixed evidence: {len(supporting)} supporting (weight: {supporting_weight:.2f}), {len(contradicting)} contradicting (weight: {contradicting_weight:.2f}), {len(neutral)} neutral (weight: {neutral_weight:.2f})."

        # Add context if provided
        if context:
            reasoning += f" Context: {context}"

        # Add precedent details
        if relevant_precedents:
            precedent_ids = [p.case_id for p in relevant_precedents[:3]]
            reasoning += f" Key precedents: {', '.join(precedent_ids)}"

        judgment = Judgment(
            claim=claim,
            verdict=verdict,
            confidence=confidence,
            reasoning=reasoning,
            relevant_precedents=relevant_precedents,
        )

        self._save_judgment(judgment)
        return judgment

    def _save_judgment(self, judgment: Judgment):
        """Save a judgment to disk."""
        # Save individual judgment file
        judgment_id = f"judgment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        judgment_file = self.judgments_path / f"{judgment_id}.json"

        with open(judgment_file, "w", encoding="utf-8") as f:
            json.dump(judgment.to_dict(), f, indent=2)

        # Add to history
        self.judgment_history.append(judgment)

        # Save history
        self._save_judgment_history()

    def get_judgment_history(
        self,
        verdict: str | None = None,
        min_confidence: float | None = None,
        limit: int | None = None,
    ) -> list[Judgment]:
        """
        Get judgment history with optional filters.

        Args:
            verdict: Filter by verdict (PROVEN/DISPROVEN/INCONCLUSIVE)
            min_confidence: Minimum confidence threshold
            limit: Maximum number of judgments to return

        Returns:
            List of judgments matching criteria
        """
        judgments = self.judgment_history.copy()

        # Filter by verdict
        if verdict:
            verdict_upper = verdict.upper()
            judgments = [j for j in judgments if verdict_upper in j.verdict.upper()]

        # Filter by confidence
        if min_confidence is not None:
            judgments = [j for j in judgments if j.confidence >= min_confidence]

        # Sort by date (newest first)
        judgments.sort(key=lambda j: j.created_at, reverse=True)

        # Limit
        if limit:
            judgments = judgments[:limit]

        return judgments

    def get_judgment_summary(self) -> dict[str, Any]:
        """Get summary of all judgments."""
        total = len(self.judgment_history)

        verdicts = {"PROVEN": 0, "DISPROVEN": 0, "INCONCLUSIVE": 0}
        for judgment in self.judgment_history:
            verdict = judgment.verdict.upper()
            if "PROVEN" in verdict:
                verdicts["PROVEN"] += 1
            elif "DISPROVEN" in verdict:
                verdicts["DISPROVEN"] += 1
            else:
                verdicts["INCONCLUSIVE"] += 1

        avg_confidence = (
            sum(j.confidence for j in self.judgment_history) / total if total > 0 else 0.0
        )

        return {
            "total_judgments": total,
            "verdicts": verdicts,
            "average_confidence": avg_confidence,
            "body_of_proof_size": len(self.magistrate.body_of_proof.precedents),
        }
