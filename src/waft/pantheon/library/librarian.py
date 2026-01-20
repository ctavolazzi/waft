"""
Librarian: God of Records and Knowledge

The Librarian presides over the Library Realm, cataloging all records
from the Pantheon (precedents from Magistrate, judgments from Judge).

Following "as above, so below" principles:
- As above: Pantheon god organizing celestial knowledge
- So below: File-based system cataloging all Pantheon records
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .record_catalog import RecordCatalog, RecordEntry
from .scribe import Scribe


class Librarian:
    """
    Librarian: God of Records and Knowledge

    Presides over the Library Realm, cataloging all records from the Pantheon.
    The Librarian does not duplicate records - it catalogs metadata and relationships.

    Storage:
    - Catalog: _pantheon/library/catalog/catalog.json
    - Indexes: _pantheon/library/catalog/indexes/
    - Scripts: _pantheon/library/scripts/ (Scribe's written records)
    - Reports: _pantheon/library/reports/
    """

    def __init__(
        self,
        project_path: Path | None = None,
        magistrate: Any | None = None,
        judge: Any | None = None,
    ):
        """
        Initialize the Librarian.

        Args:
            project_path: Path to project root (default: current directory)
            magistrate: Magistrate instance (optional, for cataloging precedents)
            judge: Judge instance (optional, for cataloging judgments)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"  # Consistent with other Gods
        self.library_path = self.pantheon_path / "library"

        # Ensure library structure exists
        self.library_path.mkdir(parents=True, exist_ok=True)
        (self.library_path / "catalog").mkdir(parents=True, exist_ok=True)
        (self.library_path / "catalog" / "indexes").mkdir(parents=True, exist_ok=True)
        (self.library_path / "scripts").mkdir(parents=True, exist_ok=True)
        (self.library_path / "archives").mkdir(parents=True, exist_ok=True)
        (self.library_path / "reports").mkdir(parents=True, exist_ok=True)

        # Initialize catalog
        catalog_path = self.library_path / "catalog" / "catalog.json"
        self.catalog = RecordCatalog(catalog_path)

        # Initialize Scribe
        self.scribe = Scribe(self.library_path / "scripts")

        # Store references to other Gods (for cataloging)
        self.magistrate = magistrate
        self.judge = judge

    def catalog_precedents(self) -> int:
        """
        Catalog all precedents from Magistrate.

        Returns:
            Number of precedents cataloged
        """
        if not self.magistrate:
            return 0

        count = 0
        # Get precedents from Body of Proof
        precedents = self.magistrate.body_of_proof.precedents

        for precedent in precedents:
            entry = RecordEntry(
                record_id=precedent.case_id,
                record_type="precedent",
                source="magistrate",
                path=str(precedent.case_path),
                category=precedent.category,
                subcategory=precedent.subcategory,
                tags=precedent.tags,
                metadata={
                    "claim": precedent.claim,
                    "verdict": precedent.verdict,
                    "confidence": precedent.confidence,
                    "created_at": precedent.created_at,
                },
                created_at=precedent.created_at,
            )

            self.catalog.add_entry(entry)
            count += 1

        # Save catalog
        self.catalog.save()

        # Have Scribe write a script about this cataloging
        self.scribe.write_script(
            f"Cataloged {count} precedents from Magistrate",
            {"action": "catalog_precedents", "count": count},
        )

        return count

    def catalog_judgments(self) -> int:
        """
        Catalog all judgments from Judge.

        Returns:
            Number of judgments cataloged
        """
        if not self.judge:
            return 0

        count = 0
        # Get judgments from judgment history
        judgments = self.judge.judgment_history

        for judgment in judgments:
            entry = RecordEntry(
                record_id=f"judgment_{judgment.created_at}",
                record_type="judgment",
                source="judge",
                path=str(self.judge.judge_path / "judgments" / f"{judgment.created_at}.json"),
                category="judgment",
                tags=["judgment", judgment.verdict.lower()],
                metadata={
                    "claim": judgment.claim,
                    "verdict": judgment.verdict,
                    "confidence": judgment.confidence,
                    "reasoning": judgment.reasoning,
                    "relevant_precedents": [p.case_id for p in judgment.relevant_precedents],
                    "created_at": judgment.created_at,
                },
                created_at=judgment.created_at,
            )

            self.catalog.add_entry(entry)
            count += 1

        # Save catalog
        self.catalog.save()

        # Have Scribe write a script about this cataloging
        self.scribe.write_script(
            f"Cataloged {count} judgments from Judge",
            {"action": "catalog_judgments", "count": count},
        )

        return count

    def catalog_all(self) -> dict[str, int]:
        """
        Catalog all records from all Pantheon Gods.

        Returns:
            Dictionary with counts per source
        """
        results = {}

        if self.magistrate:
            results["precedents"] = self.catalog_precedents()

        if self.judge:
            results["judgments"] = self.catalog_judgments()

        return results

    def search(self, query: str, record_type: str | None = None) -> list[RecordEntry]:
        """
        Search catalog for records matching query.

        Args:
            query: Search query
            record_type: Optional filter by record type (precedent, judgment)

        Returns:
            List of matching RecordEntry objects
        """
        return self.catalog.search(query, record_type)

    def get_by_category(self, category: str) -> list[RecordEntry]:
        """Get all records in a category."""
        return self.catalog.get_by_category(category)

    def get_by_tag(self, tag: str) -> list[RecordEntry]:
        """Get all records with a tag."""
        return self.catalog.get_by_tag(tag)

    def get_by_type(self, record_type: str) -> list[RecordEntry]:
        """Get all records of a type."""
        return self.catalog.get_by_type(record_type)

    def generate_summary(self) -> dict[str, Any]:
        """
        Generate summary report of Library Realm.

        Returns:
            Dictionary with summary statistics
        """
        all_entries = self.catalog.get_all_entries()

        summary = {
            "total_records": len(all_entries),
            "by_type": {},
            "by_source": {},
            "by_category": {},
            "total_tags": len(self.catalog.get_all_tags()),
            "generated_at": datetime.now().isoformat(),
        }

        for entry in all_entries:
            # Count by type
            summary["by_type"][entry.record_type] = summary["by_type"].get(entry.record_type, 0) + 1

            # Count by source
            summary["by_source"][entry.source] = summary["by_source"].get(entry.source, 0) + 1

            # Count by category
            summary["by_category"][entry.category] = (
                summary["by_category"].get(entry.category, 0) + 1
            )

        # Save summary
        summary_path = self.library_path / "reports" / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        return summary
