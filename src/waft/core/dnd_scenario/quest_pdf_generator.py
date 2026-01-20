"""
Quest PDF Generator - Generate D&D Quest PDFs from Markdown using Typst.

Uses Typst templates for professional D&D quest documentation.
"""

import logging
import subprocess
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class QuestPDFGenerator:
    """
    Generate D&D Quest PDFs from Markdown using Typst templates.

    Supports:
    - Wenyuan Campaign template (@preview/wenyuan-campaign:0.1.2)
    - D&D 5e character sheet template (owlbear)
    - Custom Typst templates
    """

    def __init__(self, project_path: Path):
        """
        Initialize Quest PDF Generator.

        Args:
            project_path: Project root path
        """
        self.project_path = Path(project_path)
        self.quests_dir = self.project_path / "_realms" / "dnd_scenario_realm" / "quests"
        self.quests_dir.mkdir(parents=True, exist_ok=True)

        # Typst template directory
        self.templates_dir = self.project_path / "templates" / "typst" / "dnd"
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Check if Typst is available
        self.typst_available = self._check_typst()

    def _check_typst(self) -> bool:
        """Check if Typst is available."""
        try:
            result = subprocess.run(
                ["typst", "--version"], capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _ensure_typst_template(self, template_name: str) -> bool:
        """
        Ensure Typst template is available.

        Args:
            template_name: Template name (e.g., "wenyuan-campaign", "dnd-5e")

        Returns:
            True if template is available
        """
        if template_name == "wenyuan-campaign":
            # Initialize wenyuan-campaign template
            try:
                result = subprocess.run(
                    ["typst", "init", "@preview/wenyuan-campaign:0.1.2"],
                    cwd=str(self.templates_dir),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return result.returncode == 0
            except Exception as e:
                logger.debug(f"Failed to init wenyuan-campaign template: {e}")
                return False
        return True

    def _create_typst_quest_file(
        self, quest_markdown: str, quest_title: str, template: str = "wenyuan-campaign"
    ) -> Path:
        """
        Create Typst file from quest markdown.

        Args:
            quest_markdown: Quest content in markdown
            quest_title: Quest title
            template: Template to use (wenyuan-campaign, dnd-5e, or custom)

        Returns:
            Path to created Typst file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = (
            "".join(c for c in quest_title if c.isalnum() or c in (" ", "-", "_"))
            .strip()
            .replace(" ", "_")
        )
        typst_file = self.quests_dir / f"quest_{safe_title}_{timestamp}.typ"

        if template == "wenyuan-campaign":
            # Use wenyuan-campaign template
            # Note: Template may need to be initialized first with: typst init @preview/wenyuan-campaign:0.1.2
            typst_content = f"""#import "@preview/wenyuan-campaign:0.1.2": *

#show: campaign.with(
  title: "{self._escape_typst(quest_title)}",
  date: {datetime.now().strftime("%Y-%m-%d")},
)

#let content = [
{self._markdown_to_typst(quest_markdown)}
]

#content
"""
        elif template == "dnd-5e":
            # Use D&D 5e template (owlbear) - character sheet style
            typst_content = f"""#import "@preview/owlbear:0.0.1": *

#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(size: 24pt, weight: "bold")[{self._escape_typst(quest_title)}]

  #text(size: 10pt, style: "italic")[Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
]

#v(1cm)

{self._markdown_to_typst(quest_markdown)}
"""
        else:
            # Simple template
            typst_content = f"""#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(size: 24pt, weight: "bold")[{quest_title}]

  #text(size: 10pt, style: "italic")[Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
]

#v(1cm)

{self._markdown_to_typst(quest_markdown)}
"""

        typst_file.write_text(typst_content)
        return typst_file

    def _markdown_to_typst(self, markdown: str) -> str:
        """
        Convert markdown to Typst syntax.

        Basic conversion - handles headers, bold, italic, lists, code blocks.
        """

        lines = markdown.split("\n")
        typst_lines = []
        in_code_block = False
        in_list = False

        for line in lines:
            # Code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                if in_code_block:
                    typst_lines.append("#raw(`")
                else:
                    typst_lines.append("`)")
                continue

            if in_code_block:
                typst_lines.append(line)
                continue

            # Headers
            if line.startswith("# "):
                typst_lines.append(f"#heading(level: 1)[{self._escape_typst(line[2:].strip())}]")
                in_list = False
            elif line.startswith("## "):
                typst_lines.append(f"#heading(level: 2)[{self._escape_typst(line[3:].strip())}]")
                in_list = False
            elif line.startswith("### "):
                typst_lines.append(f"#heading(level: 3)[{self._escape_typst(line[4:].strip())}]")
                in_list = False
            elif line.startswith("#### "):
                typst_lines.append(f"#heading(level: 4)[{self._escape_typst(line[5:].strip())}]")
                in_list = False
            # Lists
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                if not in_list:
                    typst_lines.append("#list(")
                    in_list = True
                content = line.strip()[2:]
                # Process inline formatting
                content = self._process_inline_formatting(content)
                typst_lines.append(f"  {content},")
            # Empty lines
            elif not line.strip():
                if in_list:
                    typst_lines.append(")")
                    in_list = False
                typst_lines.append("")
            # Regular text
            else:
                if in_list:
                    typst_lines.append(")")
                    in_list = False
                # Process inline formatting
                processed = self._process_inline_formatting(line)
                typst_lines.append(processed)

        if in_list:
            typst_lines.append(")")

        return "\n".join(typst_lines)

    def _process_inline_formatting(self, text: str) -> str:
        """Process inline markdown formatting (bold, italic) in text."""
        import re

        # Escape Typst special characters first
        text = self._escape_typst(text)
        # Bold (**text**)
        text = re.sub(r"\*\*(.+?)\*\*", r"#strong[\1]", text)
        # Italic (*text*) - but not if it's part of **bold**
        text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"#emph[\1]", text)
        # Code (`code`)
        text = re.sub(r"`(.+?)`", r"#code[\1]", text)
        return text

    def _escape_typst(self, text: str) -> str:
        """Escape special Typst characters."""
        # Basic escaping - escape quotes and backslashes
        text = text.replace("\\", "\\\\")
        text = text.replace('"', '\\"')
        return text

    def generate_quest_pdf(
        self,
        quest_markdown: str,
        quest_title: str,
        template: str = "wenyuan-campaign",
        output_path: Path | None = None,
    ) -> Path | None:
        """
        Generate Quest PDF from markdown.

        Args:
            quest_markdown: Quest content in markdown
            quest_title: Quest title
            template: Template to use (wenyuan-campaign, dnd-5e, simple)
            output_path: Optional output path (auto-generated if None)

        Returns:
            Path to generated PDF, or None if generation failed
        """
        if not self.typst_available:
            logger.warning("Typst not available, cannot generate quest PDF")
            return None

        # Ensure template is available
        if template in ["wenyuan-campaign", "dnd-5e"]:
            if not self._ensure_typst_template(template):
                logger.warning(f"Template {template} not available, using simple template")
                template = "simple"

        # Create Typst file
        try:
            typst_file = self._create_typst_quest_file(quest_markdown, quest_title, template)
        except Exception as e:
            logger.error(f"Failed to create Typst file: {e}")
            return None

        # Generate output path
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = (
                "".join(c for c in quest_title if c.isalnum() or c in (" ", "-", "_"))
                .strip()
                .replace(" ", "_")
            )
            output_path = self.quests_dir / f"quest_{safe_title}_{timestamp}.pdf"

        # Compile Typst to PDF
        try:
            # Use typst compile with root directory set to templates_dir for package resolution
            result = subprocess.run(
                [
                    "typst",
                    "compile",
                    "--root",
                    str(self.templates_dir),
                    str(typst_file),
                    str(output_path),
                ],
                cwd=str(self.quests_dir),
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0 and output_path.exists():
                logger.info(f"Quest PDF generated: {output_path}")
                return output_path
            else:
                # Try without root flag if that fails
                logger.debug(f"Typst compilation with root failed, trying without: {result.stderr}")
                result2 = subprocess.run(
                    ["typst", "compile", str(typst_file), str(output_path)],
                    cwd=str(self.quests_dir),
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result2.returncode == 0 and output_path.exists():
                    logger.info(f"Quest PDF generated (fallback): {output_path}")
                    return output_path
                else:
                    logger.error(f"Typst compilation failed: {result2.stderr or result.stderr}")
                    return None
        except subprocess.TimeoutExpired:
            logger.error("Typst compilation timed out")
            return None
        except Exception as e:
            logger.error(f"Failed to compile Typst: {e}")
            return None
