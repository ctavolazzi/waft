"""
PDF Discovery System

Intelligently finds the most relevant PDF based on conversation context,
active files, work efforts, and epistemic state.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any


class PDFDiscovery:
    """
    Discovers and scores PDFs based on relevance to current context.

    Searches in:
    - Current directory and subdirectories
    - _work_efforts/ directories
    - _pyrite/ directories
    - _science/ directories

    Scores based on:
    - Recency (modification time)
    - Context relevance (filename/content matches conversation)
    - Active work effort association
    - Oracle epistemic state relevance
    """

    def __init__(self, project_path: Path):
        """
        Initialize PDF discovery system.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.search_directories = [
            self.project_path,
            self.project_path / "_work_efforts",
            self.project_path / "_pyrite",
            self.project_path / "_science",
        ]

    def find_relevant_pdf(self, context: dict[str, Any]) -> Path | None:
        """
        Find the most relevant PDF based on context.

        Args:
            context: Dictionary with:
                - conversation: List of conversation messages
                - active_files: List of active file paths
                - work_efforts: List of active work effort paths
                - oracle_state: Optional Oracle epistemic state

        Returns:
            Path to most relevant PDF, or None if none found
        """
        # Find all PDFs in search directories
        pdfs = self._find_all_pdfs()

        if not pdfs:
            return None

        # Score each PDF
        scored_pdfs = []
        for pdf_path in pdfs:
            score = self.score_pdf(pdf_path, context)
            if score > 0.0:  # Only include PDFs with some relevance
                scored_pdfs.append((pdf_path, score))

        if not scored_pdfs:
            return None

        # Sort by score (highest first)
        scored_pdfs.sort(key=lambda x: x[1], reverse=True)

        # Return highest scoring PDF
        return scored_pdfs[0][0]

    def _find_all_pdfs(self) -> list[Path]:
        """Find all PDF files in search directories."""
        pdfs = []

        for search_dir in self.search_directories:
            if not search_dir.exists():
                continue

            # Search recursively
            for pdf_path in search_dir.rglob("*.pdf"):
                if pdf_path.is_file():
                    pdfs.append(pdf_path)

        return pdfs

    def score_pdf(self, pdf_path: Path, context: dict[str, Any]) -> float:
        """
        Calculate relevance score for a PDF (0.0-1.0).

        Factors:
        - Recency: 1.0 - (days_old / 30) (max 30 days)
        - Context match: Filename/content keywords vs conversation
        - Work effort link: PDF in active work effort directory
        - Oracle relevance: Epistemic state alignment

        Args:
            pdf_path: Path to PDF file
            context: Context dictionary

        Returns:
            Relevance score (0.0-1.0)
        """
        score = 0.0

        # 1. Recency score (0.0-0.4)
        recency_score = self._score_recency(pdf_path)
        score += recency_score * 0.4

        # 2. Context match score (0.0-0.3)
        context_score = self._score_context_match(pdf_path, context)
        score += context_score * 0.3

        # 3. Work effort association (0.0-0.2)
        work_effort_score = self._score_work_effort_association(pdf_path, context)
        score += work_effort_score * 0.2

        # 4. Oracle relevance (0.0-0.1)
        oracle_score = self._score_oracle_relevance(pdf_path, context)
        score += oracle_score * 0.1

        return min(1.0, score)  # Cap at 1.0

    def _score_recency(self, pdf_path: Path) -> float:
        """Score based on how recent the PDF is (0.0-1.0)."""
        if not pdf_path.exists():
            return 0.0

        try:
            mtime = datetime.fromtimestamp(pdf_path.stat().st_mtime)
            age = datetime.now() - mtime
            days_old = age.days

            # Score: 1.0 for today, decreasing to 0.0 at 30 days
            if days_old < 0:
                return 1.0
            elif days_old >= 30:
                return 0.0
            else:
                return 1.0 - (days_old / 30.0)
        except Exception:
            return 0.0

    def _score_context_match(self, pdf_path: Path, context: dict[str, Any]) -> float:
        """Score based on filename/content matching conversation context."""
        # Extract keywords from conversation
        conversation = context.get("conversation", [])
        active_files = context.get("active_files", [])

        # Build keyword set from conversation
        keywords = set()
        for msg in conversation:
            if isinstance(msg, dict):
                content = msg.get("content", "") or msg.get("text", "")
            elif isinstance(msg, str):
                content = msg
            else:
                continue

            # Extract words (simple approach)
            words = re.findall(r"\b\w{4,}\b", content.lower())
            keywords.update(words)

        # Add keywords from active file names
        for file_path in active_files:
            if isinstance(file_path, (str, Path)):
                path = Path(file_path)
                # Add filename parts as keywords
                stem = path.stem.lower()
                keywords.update(re.findall(r"\b\w{4,}\b", stem))

        if not keywords:
            return 0.5  # Neutral score if no keywords

        # Check PDF filename for keyword matches
        pdf_name = pdf_path.stem.lower()
        matches = sum(1 for keyword in keywords if keyword in pdf_name)

        # Score based on match ratio
        if not keywords:
            return 0.0

        match_ratio = matches / len(keywords)
        return min(1.0, match_ratio * 2.0)  # Boost matches

    def _score_work_effort_association(self, pdf_path: Path, context: dict[str, Any]) -> float:
        """Score based on association with active work efforts."""
        work_efforts = context.get("work_efforts", [])

        if not work_efforts:
            return 0.0

        # Check if PDF is in a work effort directory
        pdf_str = str(pdf_path)
        for work_effort in work_efforts:
            if isinstance(work_effort, (str, Path)):
                work_effort_str = str(work_effort)
                if work_effort_str in pdf_str:
                    return 1.0

        return 0.0

    def _score_oracle_relevance(self, pdf_path: Path, context: dict[str, Any]) -> float:
        """Score based on Oracle epistemic state relevance."""
        oracle_state = context.get("oracle_state")

        if not oracle_state:
            return 0.0

        # Simple heuristic: if PDF name contains phase-related keywords
        phase = oracle_state.get("epistemic_phase", "").lower()
        pdf_name = pdf_path.stem.lower()

        # Map phases to keywords
        phase_keywords = {
            "data gathering": ["data", "gathering", "collect", "observation"],
            "exploration": ["explore", "experiment", "test", "try"],
            "synthesis": ["synthesis", "summary", "analysis", "findings"],
            "evolution": ["evolution", "evolve", "advance", "progress"],
            "transition": ["transition", "change", "shift"],
        }

        keywords = phase_keywords.get(phase, [])
        if not keywords:
            return 0.0

        # Check for keyword matches
        matches = sum(1 for keyword in keywords if keyword in pdf_name)
        if matches > 0:
            return min(1.0, matches / len(keywords))

        return 0.0
