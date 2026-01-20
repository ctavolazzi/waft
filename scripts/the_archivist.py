#!/usr/bin/env python3
"""
The Archivist - PDF Archive Management System
=============================================

A Being who keeps things tidy. Minimal effort, maximum results.
Like an old guy keeping things in case we need them again someday.

Responsibilities:
- Archive daily PDFs into organized collections
- Generate morning reports of daily work
- Keep project from bloating with unorganized files
- Maintain archive index for easy retrieval
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.waft.brief import BriefDocument


class TheArchivist:
    """
    The Archivist - A Being who keeps things tidy.

    Minimal effort, maximum results.
    """

    def __init__(self, project_path: Path):
        """Initialize The Archivist."""
        self.project_path = project_path
        self.archive_path = project_path / "_archive"
        self.archive_path.mkdir(parents=True, exist_ok=True)

        # Archive structure
        self.daily_archive = self.archive_path / "daily"
        self.daily_archive.mkdir(exist_ok=True)

        self.reports_path = self.archive_path / "reports"
        self.reports_path.mkdir(exist_ok=True)

        self.index_path = self.archive_path / "archive_index.json"

    def collect_todays_pdfs(self, date: str | None = None) -> list[Path]:
        """Collect all PDFs from today."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Find all PDFs modified today
        pdfs = []
        for pdf_path in self.project_path.rglob("*.pdf"):
            try:
                mtime = datetime.fromtimestamp(pdf_path.stat().st_mtime)
                if mtime.strftime("%Y-%m-%d") == date:
                    pdfs.append(pdf_path)
            except Exception:
                continue

        return sorted(pdfs, key=lambda p: p.stat().st_mtime, reverse=True)

    def archive_daily_pdfs(self, date: str | None = None) -> dict[str, Any]:
        """Archive today's PDFs into organized collection."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        date_archive = self.daily_archive / date
        date_archive.mkdir(parents=True, exist_ok=True)

        pdfs = self.collect_todays_pdfs(date)

        archived = []
        for pdf in pdfs:
            # Skip if already in archive
            if pdf.parent == date_archive:
                continue

            # Copy to archive
            dest = date_archive / pdf.name
            if not dest.exists():
                shutil.copy2(pdf, dest)
                archived.append(
                    {
                        "original": str(pdf.relative_to(self.project_path)),
                        "archived": str(dest.relative_to(self.project_path)),
                        "size_kb": pdf.stat().st_size / 1024,
                    }
                )

        # Update index
        self._update_index(date, archived)

        return {
            "date": date,
            "archived_count": len(archived),
            "archived_files": archived,
            "archive_path": str(date_archive.relative_to(self.project_path)),
        }

    def generate_morning_report(self, date: str | None = None) -> Path:
        """Generate morning report of today's PDFs."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        pdfs = self.collect_todays_pdfs(date)

        # Organize by category
        briefs = [p for p in pdfs if "brief" in p.name.lower() or "briefs" in str(p.parent)]
        proofs = [p for p in pdfs if "proof" in p.name.lower() or "proof_cases" in str(p.parent)]
        studies = [p for p in pdfs if "study" in p.name.lower() or "self_studies" in str(p.parent)]
        work_efforts = [
            p
            for p in pdfs
            if "_work_efforts" in str(p.parent) and p not in briefs and p not in proofs
        ]
        other = [
            p
            for p in pdfs
            if p not in briefs and p not in proofs and p not in studies and p not in work_efforts
        ]

        # Build report content
        report_content = self._build_report_content(
            date, briefs, proofs, studies, work_efforts, other
        )

        # Generate PDF
        doc = BriefDocument(
            title=f"Morning Archive Report - {date}",
            doc_id=f"ARCHIVE-{date.replace('-', '')}",
            subtitle="Daily PDF Collection & Archive",
            classification="INTERNAL",
            cover_header="THE ARCHIVIST",
            cover_metadata={"DATE": date, "TOTAL_PDFS": str(len(pdfs)), "ARCHIVED": "Yes"},
            cover_warning={
                "message": f"Daily Archive - {len(pdfs)} documents collected",
                "severity": "INFO",
            },
            cover_footer="DAILY ARCHIVE REPORT",
            include_system_status=False,
        )

        doc.content_blocks.append(report_content)

        report_path = self.reports_path / f"morning_report_{date.replace('-', '')}.pdf"
        pdf_path = doc.generate(output_path=report_path)

        return pdf_path

    def _build_report_content(
        self,
        date: str,
        briefs: list[Path],
        proofs: list[Path],
        studies: list[Path],
        work_efforts: list[Path],
        other: list[Path],
    ) -> str:
        """Build report content HTML."""
        content = []

        content.append(f"<h2>Morning Archive Report - {date}</h2>")
        content.append(f"<p><strong>Date:</strong> {date}</p>")
        content.append(
            f"<p><strong>Total PDFs Collected:</strong> {len(briefs) + len(proofs) + len(studies) + len(work_efforts) + len(other)}</p>"
        )
        content.append("")

        # Briefs
        if briefs:
            content.append("<h3>📋 Briefs & Session Reports</h3>")
            content.append("<ul>")
            for pdf in briefs:
                size_kb = pdf.stat().st_size / 1024
                rel_path = pdf.relative_to(self.project_path)
                content.append(
                    f"<li><strong>{pdf.name}</strong> ({size_kb:.1f} KB)<br><code>{rel_path}</code></li>"
                )
            content.append("</ul>")
            content.append("")

        # Proofs
        if proofs:
            content.append("<h3>🔍 Proof Cases & Verification</h3>")
            content.append("<ul>")
            for pdf in proofs:
                size_kb = pdf.stat().st_size / 1024
                rel_path = pdf.relative_to(self.project_path)
                content.append(
                    f"<li><strong>{pdf.name}</strong> ({size_kb:.1f} KB)<br><code>{rel_path}</code></li>"
                )
            content.append("</ul>")
            content.append("")

        # Studies
        if studies:
            content.append("<h3>🔬 Studies & Research</h3>")
            content.append("<ul>")
            for pdf in studies:
                size_kb = pdf.stat().st_size / 1024
                rel_path = pdf.relative_to(self.project_path)
                content.append(
                    f"<li><strong>{pdf.name}</strong> ({size_kb:.1f} KB)<br><code>{rel_path}</code></li>"
                )
            content.append("</ul>")
            content.append("")

        # Work Efforts
        if work_efforts:
            content.append("<h3>📁 Work Efforts Documents</h3>")
            content.append("<ul>")
            for pdf in work_efforts[:10]:  # Limit to 10
                size_kb = pdf.stat().st_size / 1024
                rel_path = pdf.relative_to(self.project_path)
                content.append(
                    f"<li><strong>{pdf.name}</strong> ({size_kb:.1f} KB)<br><code>{rel_path}</code></li>"
                )
            if len(work_efforts) > 10:
                content.append(
                    f"<li><em>... and {len(work_efforts) - 10} more work effort documents</em></li>"
                )
            content.append("</ul>")
            content.append("")

        # Other
        if other:
            content.append("<h3>📄 Other Documents</h3>")
            content.append("<ul>")
            for pdf in other[:5]:  # Limit to 5
                size_kb = pdf.stat().st_size / 1024
                rel_path = pdf.relative_to(self.project_path)
                content.append(
                    f"<li><strong>{pdf.name}</strong> ({size_kb:.1f} KB)<br><code>{rel_path}</code></li>"
                )
            if len(other) > 5:
                content.append(f"<li><em>... and {len(other) - 5} more documents</em></li>")
            content.append("</ul>")
            content.append("")

        # Summary
        content.append("<h3>📊 Summary</h3>")
        content.append('<table border="1" cellpadding="5">')
        content.append("<tr><th>Category</th><th>Count</th><th>Total Size (KB)</th></tr>")

        categories = [
            ("Briefs", briefs),
            ("Proofs", proofs),
            ("Studies", studies),
            ("Work Efforts", work_efforts),
            ("Other", other),
        ]

        total_size = 0
        for cat_name, cat_pdfs in categories:
            if cat_pdfs:
                cat_size = sum(p.stat().st_size for p in cat_pdfs) / 1024
                total_size += cat_size
                content.append(
                    f"<tr><td>{cat_name}</td><td>{len(cat_pdfs)}</td><td>{cat_size:.1f}</td></tr>"
                )

        content.append(
            f"<tr><td><strong>Total</strong></td><td><strong>{len(briefs) + len(proofs) + len(studies) + len(work_efforts) + len(other)}</strong></td><td><strong>{total_size:.1f}</strong></td></tr>"
        )
        content.append("</table>")
        content.append("")

        content.append("<h3>📦 Archive Status</h3>")
        content.append(
            "<p>All documents have been catalogued and archived for future reference.</p>"
        )
        content.append(
            "<p><em>The Archivist keeps things tidy, just in case we need them again someday.</em></p>"
        )

        return "\n".join(content)

    def _update_index(self, date: str, archived: list[dict[str, Any]]):
        """Update archive index."""
        if self.index_path.exists():
            index = json.loads(self.index_path.read_text())
        else:
            index = {}

        index[date] = {
            "archived_at": datetime.now().isoformat(),
            "archived_count": len(archived),
            "files": archived,
        }

        self.index_path.write_text(json.dumps(index, indent=2))

    def get_archive_stats(self) -> dict[str, Any]:
        """Get archive statistics."""
        if not self.index_path.exists():
            return {"total_days": 0, "total_files": 0}

        index = json.loads(self.index_path.read_text())
        total_files = sum(entry.get("archived_count", 0) for entry in index.values())

        return {"total_days": len(index), "total_files": total_files, "dates": list(index.keys())}


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="The Archivist - PDF Archive Management")
    parser.add_argument("--date", help="Date to archive (YYYY-MM-DD, default: today)")
    parser.add_argument(
        "--report-only", action="store_true", help="Generate report only, don't archive"
    )
    parser.add_argument(
        "--archive-only", action="store_true", help="Archive only, don't generate report"
    )
    parser.add_argument("--stats", action="store_true", help="Show archive statistics")

    args = parser.parse_args()

    archivist = TheArchivist(project_root)

    if args.stats:
        stats = archivist.get_archive_stats()
        print("📊 Archive Statistics")
        print("=" * 70)
        print(f"Total Days Archived: {stats['total_days']}")
        print(f"Total Files Archived: {stats['total_files']}")
        if stats["dates"]:
            print(f"Date Range: {stats['dates'][0]} to {stats['dates'][-1]}")
        return 0

    date = args.date or datetime.now().strftime("%Y-%m-%d")

    if not args.report_only:
        print("📦 Archiving PDFs...")
        archive_result = archivist.archive_daily_pdfs(date)
        print(f"  ✅ Archived {archive_result['archived_count']} PDFs")
        print(f"  📁 Archive: {archive_result['archive_path']}")
        print()

    if not args.archive_only:
        print("📋 Generating Morning Report...")
        report_path = archivist.generate_morning_report(date)
        print(f"  ✅ Report: {report_path.relative_to(project_root)}")
        print()

        # Open report
        import platform
        import subprocess

        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(report_path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", str(report_path)], shell=True, check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(report_path)], check=False)

    print("✅ The Archivist has completed the daily collection.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
