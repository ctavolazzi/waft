"""
Campaign Binder Generator
=========================

Generates comprehensive PDF binders for D&D campaigns, including:
- Session logs
- Character progression
- Campaign evolution
- Appendices (NPCs, locations, etc.)
"""

from datetime import datetime
from pathlib import Path

from .pdf_generator import PDFGenerator


class CampaignBinderGenerator:
    """
    Generates comprehensive PDF binders for D&D campaigns.
    """

    def __init__(self, tracker, project_path: Path):
        """
        Initialize binder generator.

        Args:
            tracker: CampaignSessionTracker instance
            project_path: Project root path
        """
        self.tracker = tracker
        self.project_path = Path(project_path)
        self.campaign_data = tracker.get_campaign_data()

    def generate_binder(self, output_path: Path | None = None) -> Path:
        """
        Generate complete campaign binder PDF.

        Args:
            output_path: Output file path (defaults to campaign_id_binder.pdf)

        Returns:
            Path to generated PDF
        """
        if output_path is None:
            output_path = self.tracker.base_path.parent / f"{self.tracker.campaign_id}_binder.pdf"

        output_path = Path(output_path)

        # Generate markdown content
        markdown_content = self._generate_markdown()

        # Generate PDF
        generator = PDFGenerator.from_content(
            content=markdown_content,
            title=f"{self.tracker.campaign_id.replace('_', ' ').title()} - Campaign Binder",
            style="premium",
        )

        generator.save(str(output_path))

        return output_path

    def _generate_markdown(self) -> str:
        """Generate complete markdown content for binder."""
        lines = []

        # Cover Page
        lines.append(f"# {self.tracker.campaign_id.replace('_', ' ').title()}")
        lines.append("\n## Campaign Binder\n")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n**Sessions:** {self.campaign_data['session_count']}")
        lines.append(f"\n**Characters:** {self.campaign_data['character_count']}")
        lines.append("\n---\n")

        # Table of Contents
        lines.append("## Table of Contents\n")
        lines.append("\n1. [Sessions](#sessions)")
        lines.append("2. [Character Progression](#character-progression)")
        lines.append("3. [Campaign Evolution](#campaign-evolution)")
        lines.append("\n---\n")

        # Sessions
        lines.append("## Sessions\n")
        for session in self.campaign_data["sessions"]:
            lines.append(f"\n### Session {session['session_number']}: {session['title']}")
            lines.append(f"\n**Date:** {session['date']}")
            lines.append(f"\n**Summary:** {session['summary']}")

            if session.get("characters_present"):
                lines.append("\n**Characters Present:**")
                for char in session["characters_present"]:
                    lines.append(f"- {char}")

            if session.get("key_events"):
                lines.append("\n**Key Events:**")
                for event in session["key_events"]:
                    lines.append(f"- {event}")

            if session.get("evolution_notes"):
                lines.append(f"\n**Evolution Notes:** {session['evolution_notes']}")

            # Try to get markdown content
            md_content = self.tracker.get_session_markdown(session["session_number"])
            if md_content:
                # Extract content after frontmatter
                content_lines = md_content.split("---", 2)
                if len(content_lines) > 2:
                    lines.append(f"\n{content_lines[2].strip()}")

            lines.append("\n---\n")

        # Character Progression
        lines.append("## Character Progression\n")
        for char_name, char_data in self.campaign_data["characters"].items():
            lines.append(f"\n### {char_name}")
            lines.append(f"\n**Created:** {char_data.get('created_at', 'Unknown')}")

            if char_data.get("progression"):
                lines.append("\n**Progression History:**")
                for entry in char_data["progression"]:
                    lines.append(
                        f"\n#### Session {entry.get('session_number', 'N/A')} - {entry.get('date', '')}"
                    )
                    changes = entry.get("changes", {})
                    for key, value in changes.items():
                        lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")

            lines.append("\n---\n")

        # Campaign Evolution
        lines.append("## Campaign Evolution\n")
        for entry in self.campaign_data["evolution"]:
            lines.append(f"\n### {entry.get('type', 'Change').replace('_', ' ').title()}")
            lines.append(f"\n**Date:** {entry.get('date', 'Unknown')}")
            if entry.get("session_number"):
                lines.append(f"**Session:** {entry['session_number']}")
            lines.append(f"\n**Description:** {entry.get('description', '')}")

            if entry.get("metadata"):
                lines.append("\n**Details:**")
                for key, value in entry["metadata"].items():
                    lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")

            lines.append("\n---\n")

        return "\n".join(lines)
