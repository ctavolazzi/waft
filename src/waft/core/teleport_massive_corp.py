"""
Teleport Massive Corporation - Worldbuilding Documentation System

A comprehensive system for worldbuilding the Teleport Massive corporation
through Typst-generated documentation. Uses various Typst templates to create
corporate documents, reports, and worldbuilding materials.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class TeleportMassiveCorp:
    """
    Teleport Massive Corporation - Worldbuilding Documentation Generator

    Creates comprehensive corporate documentation using Typst templates:
    - biz-report: Business reports and corporate documents
    - brilliant-cv: Employee CVs and personnel files
    - Other Typst templates as needed
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize Teleport Massive Corporation.

        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.corp_path = project_path / "_realms" / "bureaucracy_realm" / "teleport_massive"
        self.corp_path.mkdir(parents=True, exist_ok=True)

        # Corporate structure directories
        self.docs_path = self.corp_path / "docs"
        self.personnel_path = self.corp_path / "personnel"
        self.reports_path = self.corp_path / "reports"
        self.policies_path = self.corp_path / "policies"
        self.worldbuilding_path = self.corp_path / "worldbuilding"

        for path in [
            self.docs_path,
            self.personnel_path,
            self.reports_path,
            self.policies_path,
            self.worldbuilding_path,
        ]:
            path.mkdir(parents=True, exist_ok=True)

        # Corporate manifest
        self.manifest_path = self.corp_path / "corporate_manifest.json"
        self._ensure_manifest()

    def _ensure_manifest(self) -> None:
        """Ensure corporate manifest exists."""
        if not self.manifest_path.exists():
            manifest = {
                "corporation_name": "Teleport Massive",
                "founded": datetime.now().isoformat(),
                "sector": "Teleportation Technology",
                "mission": "Revolutionizing transportation through instant teleportation technology",
                "departments": [],
                "employees": [],
                "documents": [],
                "worldbuilding_notes": [],
            }
            self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    def assign_being_role(
        self, being_id: str, role: str, department: str, title: str, level: int = 1
    ) -> dict[str, Any]:
        """
        Assign a role to a Being within Teleport Massive.

        Args:
            being_id: Being identifier
            role: Role name (e.g., "Documentation Specialist", "Bureaucracy Manager")
            department: Department name
            title: Job title
            level: Seniority level (1-10)

        Returns:
            Role assignment record
        """
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))

        assignment = {
            "being_id": being_id,
            "role": role,
            "department": department,
            "title": title,
            "level": level,
            "assigned_at": datetime.now().isoformat(),
            "status": "active",
        }

        # Add to employees list
        manifest["employees"].append(assignment)

        # Ensure department exists
        if department not in [d["name"] for d in manifest["departments"]]:
            manifest["departments"].append(
                {"name": department, "created_at": datetime.now().isoformat(), "employees": []}
            )

        # Add to department
        for dept in manifest["departments"]:
            if dept["name"] == department:
                dept["employees"].append(being_id)
                break

        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return assignment

    def create_corporate_report(
        self,
        report_type: str,
        title: str,
        content: dict[str, Any],
        author_being_id: str | None = None,
    ) -> Path:
        """
        Create a corporate report using biz-report Typst template.

        Args:
            report_type: Type of report (quarterly, annual, project, etc.)
            title: Report title
            content: Report content dictionary
            author_being_id: Optional Being ID of author

        Returns:
            Path to generated Typst file
        """
        # Generate report using biz-report template
        report_path = self.reports_path / f"{report_type}_{datetime.now().strftime('%Y%m%d')}.typ"

        # Create report using biz-report template structure
        report_content = f"""#import "@preview/biz-report:0.3.1": *

#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(size: 24pt, weight: "bold")[Teleport Massive Corporation]
  #text(size: 18pt)[{title}]
  #text(size: 10pt, style: "italic")[Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
]

#v(1cm)

{content.get("body", "Report content goes here")}
"""

        report_path.write_text(report_content, encoding="utf-8")

        # Update manifest
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["documents"].append(
            {
                "type": "report",
                "subtype": report_type,
                "title": title,
                "path": str(report_path),
                "created_at": datetime.now().isoformat(),
                "author": author_being_id,
            }
        )
        self.manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return report_path

    def get_corporate_structure(self) -> dict[str, Any]:
        """
        Get current corporate structure.

        Returns:
            Dictionary with departments, employees, and structure
        """
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return manifest
