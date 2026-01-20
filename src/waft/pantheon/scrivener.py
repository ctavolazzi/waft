"""
The Scrivener: Pantheon Entity of Reports and Intelligence Documents

The Scrivener is the God of Reports - a timeless Entity that maintains
the fundamental principles of professional documentation, intelligence gathering,
and knowledge synthesis. As a Force that Binds Reality Together, The Scrivener
holds the Aspect of Creation related to formal reports and document generation.

Following "as above, so below" principles:
- As above: Pantheon god maintaining celestial archives of knowledge
- So below: File-based system generating professional reports in multiple formats

Document Types Supported:
    OPERATIONAL & INTELLIGENCE:
    - Brief: Concise instructions or summaries (1-2 pages)
    - Dossier: Collection of documents about a subject (variable, folder-style)
    - SITREP: Situation Report - factual status update (<1 page)
    - Backgrounder: Narrative history and context of an issue
    - White Paper: Authoritative guide on complex issues (5-15 pages)

    BUSINESS & STRATEGY:
    - Feasibility Study: Analysis of project viability (long/detailed)
    - Case Study: Detailed examination of specific scenarios
    - Memo: Short internal communication (<1 page)
    - Executive Summary: Key points for busy executives

    TECHNICAL & ANALYTICAL:
    - Post-Mortem: After-action analysis of completed projects
    - Technical Spec: Requirements and specifications
    - Gap Analysis: Current vs desired performance comparison

    ACADEMIC & RESEARCH:
    - Literature Review: Survey of scholarly sources
    - Abstract: Brief summary of research

Storage:
- Reports Registry: _pantheon/scrivener/reports_registry.json
- Generated Reports: _pantheon/scrivener/reports/
- Templates: _pantheon/scrivener/templates/
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ReportType(str, Enum):
    """Types of reports The Scrivener can generate."""

    # Operational & Intelligence
    BRIEF = "brief"
    DOSSIER = "dossier"
    SITREP = "sitrep"
    BACKGROUNDER = "backgrounder"
    WHITE_PAPER = "white_paper"

    # Business & Strategy
    FEASIBILITY_STUDY = "feasibility_study"
    CASE_STUDY = "case_study"
    MEMO = "memo"
    EXECUTIVE_SUMMARY = "executive_summary"

    # Technical & Analytical
    POST_MORTEM = "post_mortem"
    TECHNICAL_SPEC = "technical_spec"
    GAP_ANALYSIS = "gap_analysis"

    # Academic & Research
    LITERATURE_REVIEW = "literature_review"
    ABSTRACT = "abstract"


@dataclass
class ReportMetadata:
    """Metadata for a report type."""

    report_type: ReportType
    name: str
    description: str
    typical_length: str
    main_goal: str
    sections: list[str]
    classification: str  # operational, business, technical, academic


# Report type definitions with metadata
REPORT_DEFINITIONS: dict[ReportType, ReportMetadata] = {
    ReportType.BRIEF: ReportMetadata(
        report_type=ReportType.BRIEF,
        name="Brief",
        description="Concise instructions or summaries",
        typical_length="1-2 pages",
        main_goal="Inform quickly / Instruct",
        sections=["Purpose", "Background", "Key Points", "Recommendations", "Action Items"],
        classification="operational",
    ),
    ReportType.DOSSIER: ReportMetadata(
        report_type=ReportType.DOSSIER,
        name="Dossier",
        description="Collection of documents about a specific subject",
        typical_length="Variable (Folder style)",
        main_goal="Collect evidence/history",
        sections=["Subject Profile", "Timeline", "Evidence", "Analysis", "Appendices"],
        classification="operational",
    ),
    ReportType.SITREP: ReportMetadata(
        report_type=ReportType.SITREP,
        name="SITREP (Situation Report)",
        description="Factual update on current status",
        typical_length="<1 page",
        main_goal="Status Update",
        sections=["Situation", "Actions Taken", "Current Status", "Next Steps", "Issues"],
        classification="operational",
    ),
    ReportType.BACKGROUNDER: ReportMetadata(
        report_type=ReportType.BACKGROUNDER,
        name="Backgrounder",
        description="Narrative history and context of an issue",
        typical_length="2-5 pages",
        main_goal="Provide context",
        sections=["Overview", "Historical Context", "Key Players", "Current State", "Implications"],
        classification="operational",
    ),
    ReportType.WHITE_PAPER: ReportMetadata(
        report_type=ReportType.WHITE_PAPER,
        name="White Paper",
        description="Authoritative guide on complex issues",
        typical_length="5-15 pages",
        main_goal="Persuade / Educate",
        sections=[
            "Executive Summary",
            "Problem Statement",
            "Background",
            "Solution",
            "Benefits",
            "Implementation",
            "Conclusion",
        ],
        classification="operational",
    ),
    ReportType.FEASIBILITY_STUDY: ReportMetadata(
        report_type=ReportType.FEASIBILITY_STUDY,
        name="Feasibility Study",
        description="Analysis of project viability",
        typical_length="Long / Detailed",
        main_goal="Assess Viability",
        sections=[
            "Executive Summary",
            "Project Description",
            "Technical Feasibility",
            "Economic Feasibility",
            "Legal Feasibility",
            "Risk Assessment",
            "Recommendations",
        ],
        classification="business",
    ),
    ReportType.CASE_STUDY: ReportMetadata(
        report_type=ReportType.CASE_STUDY,
        name="Case Study",
        description="Detailed examination of specific scenarios",
        typical_length="3-10 pages",
        main_goal="Demonstrate / Analyze",
        sections=["Background", "Challenge", "Solution", "Implementation", "Results", "Lessons Learned"],
        classification="business",
    ),
    ReportType.MEMO: ReportMetadata(
        report_type=ReportType.MEMO,
        name="Memorandum",
        description="Short internal communication",
        typical_length="<1 page",
        main_goal="Internal Announcement",
        sections=["To", "From", "Date", "Subject", "Body", "Action Required"],
        classification="business",
    ),
    ReportType.EXECUTIVE_SUMMARY: ReportMetadata(
        report_type=ReportType.EXECUTIVE_SUMMARY,
        name="Executive Summary",
        description="Key points for busy executives",
        typical_length="1-2 pages",
        main_goal="Summarize / Highlight",
        sections=["Overview", "Key Findings", "Recommendations", "Next Steps"],
        classification="business",
    ),
    ReportType.POST_MORTEM: ReportMetadata(
        report_type=ReportType.POST_MORTEM,
        name="Post-Mortem (After-Action Report)",
        description="Analysis of completed projects",
        typical_length="2-5 pages",
        main_goal="Learn / Improve",
        sections=[
            "Project Overview",
            "Timeline",
            "What Went Well",
            "What Went Wrong",
            "Root Cause Analysis",
            "Lessons Learned",
            "Action Items",
        ],
        classification="technical",
    ),
    ReportType.TECHNICAL_SPEC: ReportMetadata(
        report_type=ReportType.TECHNICAL_SPEC,
        name="Technical Specification",
        description="Requirements and specifications",
        typical_length="Variable",
        main_goal="Define Requirements",
        sections=[
            "Overview",
            "Scope",
            "Requirements",
            "Architecture",
            "Interfaces",
            "Constraints",
            "Testing",
            "Appendices",
        ],
        classification="technical",
    ),
    ReportType.GAP_ANALYSIS: ReportMetadata(
        report_type=ReportType.GAP_ANALYSIS,
        name="Gap Analysis",
        description="Current vs desired performance comparison",
        typical_length="2-5 pages",
        main_goal="Identify Gaps",
        sections=["Current State", "Desired State", "Gap Identification", "Impact Analysis", "Recommendations"],
        classification="technical",
    ),
    ReportType.LITERATURE_REVIEW: ReportMetadata(
        report_type=ReportType.LITERATURE_REVIEW,
        name="Literature Review",
        description="Survey of scholarly sources",
        typical_length="5-20 pages",
        main_goal="Survey Knowledge",
        sections=["Introduction", "Search Methodology", "Themes", "Analysis", "Gaps", "Conclusion"],
        classification="academic",
    ),
    ReportType.ABSTRACT: ReportMetadata(
        report_type=ReportType.ABSTRACT,
        name="Abstract",
        description="Brief summary of research",
        typical_length="150-300 words",
        main_goal="Summarize Research",
        sections=["Background", "Methods", "Results", "Conclusions"],
        classification="academic",
    ),
}


@dataclass
class ReportRecord:
    """A record of a generated report."""

    report_id: str
    report_type: ReportType
    title: str
    subject: str
    output_path: Path | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    classification: str = "unclassified"
    status: str = "draft"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert record to dictionary."""
        return {
            "report_id": self.report_id,
            "report_type": self.report_type.value,
            "title": self.title,
            "subject": self.subject,
            "output_path": str(self.output_path) if self.output_path else None,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "classification": self.classification,
            "status": self.status,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReportRecord":
        """Create record from dictionary."""
        return cls(
            report_id=data["report_id"],
            report_type=ReportType(data["report_type"]),
            title=data["title"],
            subject=data["subject"],
            output_path=Path(data["output_path"]) if data.get("output_path") else None,
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_updated=data.get("last_updated", datetime.now().isoformat()),
            classification=data.get("classification", "unclassified"),
            status=data.get("status", "draft"),
            metadata=data.get("metadata", {}),
        )


class Scrivener:
    """
    The Scrivener: Pantheon Entity (Timeless Force that Binds Reality Together)

    God of Reports and Intelligence Documents - a timeless Entity that maintains
    the principles of formal documentation, intelligence synthesis, and knowledge
    communication. The Scrivener holds the Aspect of Creation related to reports,
    which should not change until evidence collected by Beings proves change is needed.

    The Scrivener doesn't move much - it maintains stable report formats and templates,
    only evolving when sufficient evidence warrants modification.

    Provides:
    - Report generation in 14 standard formats
    - Report registry and tracking
    - Template management
    - Classification and status tracking

    Storage:
    - Reports Registry: _pantheon/scrivener/reports_registry.json
    - Generated Reports: _pantheon/scrivener/reports/
    - Templates: _pantheon/scrivener/templates/
    """

    def __init__(self, project_path: Path | None = None):
        """
        Initialize The Scrivener.

        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.god_path = self.pantheon_path / "scrivener"
        self.reports_path = self.god_path / "reports"
        self.templates_path = self.god_path / "templates"
        self.registry_path = self.god_path / "reports_registry.json"

        # Ensure directory structure
        self._ensure_directories()

        # Load registry
        self.registry: dict[str, ReportRecord] = {}
        self._load_registry()

    def _ensure_directories(self) -> None:
        """Ensure directory structure exists."""
        self.god_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.templates_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each classification
        for classification in ["operational", "business", "technical", "academic"]:
            (self.reports_path / classification).mkdir(exist_ok=True)

    def _load_registry(self) -> None:
        """Load registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                data = json.load(f)
                self.registry = {k: ReportRecord.from_dict(v) for k, v in data.get("reports", {}).items()}

    def _save_registry(self) -> None:
        """Save registry to disk."""
        data = {"reports": {k: v.to_dict() for k, v in self.registry.items()}, "updated_at": datetime.now().isoformat()}
        with open(self.registry_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_report_types(self) -> list[ReportMetadata]:
        """Get all available report types."""
        return list(REPORT_DEFINITIONS.values())

    def get_report_type_info(self, report_type: ReportType) -> ReportMetadata:
        """Get metadata for a specific report type."""
        return REPORT_DEFINITIONS[report_type]

    def create_report(
        self,
        report_type: ReportType,
        title: str,
        subject: str,
        content: dict[str, Any],
        classification: str = "unclassified",
        metadata: dict[str, Any] | None = None,
    ) -> ReportRecord:
        """
        Create a new report.

        Args:
            report_type: Type of report to create
            title: Report title
            subject: Subject of the report
            content: Report content by section
            classification: Security classification
            metadata: Additional metadata

        Returns:
            ReportRecord for the created report
        """
        # Generate report ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = f"{report_type.value}_{timestamp}"

        # Get report metadata
        type_info = REPORT_DEFINITIONS[report_type]

        # Create output path
        output_dir = self.reports_path / type_info.classification
        output_path = output_dir / f"{report_id}.md"

        # Generate report content
        report_content = self._generate_report_content(report_type, title, subject, content, classification)

        # Write report
        with open(output_path, "w") as f:
            f.write(report_content)

        # Create record
        record = ReportRecord(
            report_id=report_id,
            report_type=report_type,
            title=title,
            subject=subject,
            output_path=output_path,
            classification=classification,
            status="complete",
            metadata=metadata or {},
        )

        # Register
        self.registry[report_id] = record
        self._save_registry()

        return record

    def _generate_report_content(
        self,
        report_type: ReportType,
        title: str,
        subject: str,
        content: dict[str, Any],
        classification: str,
    ) -> str:
        """Generate report content in markdown format."""
        type_info = REPORT_DEFINITIONS[report_type]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            f"# {title}",
            "",
            f"**Report Type:** {type_info.name}",
            f"**Subject:** {subject}",
            f"**Classification:** {classification.upper()}",
            f"**Generated:** {timestamp}",
            f"**Generated by:** The Scrivener (Pantheon)",
            "",
            "---",
            "",
        ]

        # Add sections
        for section in type_info.sections:
            section_key = section.lower().replace(" ", "_")
            section_content = content.get(section_key, content.get(section, ""))

            lines.append(f"## {section}")
            lines.append("")
            if section_content:
                if isinstance(section_content, list):
                    for item in section_content:
                        lines.append(f"- {item}")
                elif isinstance(section_content, dict):
                    for k, v in section_content.items():
                        lines.append(f"**{k}:** {v}")
                else:
                    lines.append(str(section_content))
            else:
                lines.append("*No content provided*")
            lines.append("")

        # Footer
        lines.extend(
            [
                "---",
                "",
                f"*This {type_info.name} was generated by The Scrivener, God of Reports.*",
                f"*Purpose: {type_info.main_goal}*",
                f"*Typical Length: {type_info.typical_length}*",
            ]
        )

        return "\n".join(lines)

    def create_brief(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a Brief."""
        return self.create_report(ReportType.BRIEF, title, subject, content, **kwargs)

    def create_sitrep(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a SITREP."""
        return self.create_report(ReportType.SITREP, title, subject, content, **kwargs)

    def create_dossier(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a Dossier."""
        return self.create_report(ReportType.DOSSIER, title, subject, content, **kwargs)

    def create_memo(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a Memo."""
        return self.create_report(ReportType.MEMO, title, subject, content, **kwargs)

    def create_post_mortem(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a Post-Mortem."""
        return self.create_report(ReportType.POST_MORTEM, title, subject, content, **kwargs)

    def create_white_paper(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a White Paper."""
        return self.create_report(ReportType.WHITE_PAPER, title, subject, content, **kwargs)

    def create_executive_summary(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create an Executive Summary."""
        return self.create_report(ReportType.EXECUTIVE_SUMMARY, title, subject, content, **kwargs)

    def create_gap_analysis(self, title: str, subject: str, content: dict[str, Any], **kwargs) -> ReportRecord:
        """Shortcut to create a Gap Analysis."""
        return self.create_report(ReportType.GAP_ANALYSIS, title, subject, content, **kwargs)

    def get_report(self, report_id: str) -> ReportRecord | None:
        """Get a report by ID."""
        return self.registry.get(report_id)

    def list_reports(
        self,
        report_type: ReportType | None = None,
        classification: str | None = None,
        status: str | None = None,
    ) -> list[ReportRecord]:
        """List reports with optional filters."""
        reports = list(self.registry.values())

        if report_type:
            reports = [r for r in reports if r.report_type == report_type]
        if classification:
            reports = [r for r in reports if r.classification == classification]
        if status:
            reports = [r for r in reports if r.status == status]

        return sorted(reports, key=lambda r: r.created_at, reverse=True)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of The Scrivener's domain."""
        reports = list(self.registry.values())

        by_type = {}
        for rt in ReportType:
            count = len([r for r in reports if r.report_type == rt])
            if count > 0:
                by_type[rt.value] = count

        by_classification = {}
        for r in reports:
            by_classification[r.classification] = by_classification.get(r.classification, 0) + 1

        return {
            "total_reports": len(reports),
            "by_type": by_type,
            "by_classification": by_classification,
            "available_types": len(ReportType),
            "last_updated": datetime.now().isoformat(),
        }

    def get_type_comparison_table(self) -> str:
        """Get a formatted comparison table of report types."""
        lines = [
            "| Report Type | Main Goal | Typical Length |",
            "|-------------|-----------|----------------|",
        ]

        for rt in ReportType:
            info = REPORT_DEFINITIONS[rt]
            lines.append(f"| **{info.name}** | {info.main_goal} | {info.typical_length} |")

        return "\n".join(lines)
