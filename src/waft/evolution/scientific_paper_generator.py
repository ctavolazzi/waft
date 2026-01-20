"""
Scientific Research Paper Generator for WAFT Self-Study

Enables WAFT to generate comprehensive scientific research papers about itself
using the scientific method, Study Gym, and evolutionary tracking.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..study_gym import StudyGym, StudySession
from .chat_distiller import ChatDistiller
from .styling_genome import StylingGenome, StylingGenomeRegistry
from .two_page_generator import TwoPageGenerator


class ScientificPaperGenerator:
    """
    Generate scientific research papers for WAFT self-study.

    Integrates:
    - Study Gym (scientific method)
    - Evolutionary tracking (genome IDs, lineage)
    - Flight Recorder (event logging)
    - Document generation (2-page summaries or full papers)
    - Karmic Wager System (bets on hypotheses)
    """

    def __init__(
        self,
        study_gym_dir: Path = Path("_work_efforts/study_gym"),
        genetics_dir: Path = Path("_genetics/scientific_papers"),
        output_dir: Path = Path("_work_efforts/scientific_papers"),
        enable_wagers: bool = True,
    ):
        """Initialize scientific paper generator."""
        self.study_gym_dir = study_gym_dir
        self.genetics_dir = genetics_dir
        self.output_dir = output_dir

        # Ensure directories exist
        self.study_gym_dir.mkdir(parents=True, exist_ok=True)
        self.genetics_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.study_gym = StudyGym(output_dir=self.study_gym_dir)
        self.distiller = ChatDistiller()
        self.registry = StylingGenomeRegistry(registry_dir=self.genetics_dir)

        # Initialize karmic wager system if enabled
        self.wager_system = None
        if enable_wagers:
            try:
                from ..karmic_wager import KarmicWagerSystem

                self.wager_system = KarmicWagerSystem(project_path=Path.cwd())
            except Exception:
                pass  # Continue without wagers if import fails

    def create_study(
        self,
        research_question: str,
        hypothesis: str,
        objectives: list[str],
        study_config: dict[str, Any] | None = None,
        wager_karma: float | None = None,
    ) -> dict[str, Any]:
        """
        Create a new scientific study.

        Args:
            research_question: Primary research question
            hypothesis: Testable hypothesis
            objectives: List of study objectives
            study_config: Additional study configuration
            wager_karma: Optional karma amount to wager on hypothesis

        Returns:
            Study configuration with genome ID
        """
        # Create study configuration
        study_id = f"study_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        study_config = study_config or {}
        study_config.update(
            {
                "study_id": study_id,
                "research_question": research_question,
                "hypothesis": hypothesis,
                "objectives": objectives,
                "created_at": datetime.now().isoformat(),
                "status": "active",
            }
        )

        # Generate genome ID for this study
        study_json = json.dumps(study_config, sort_keys=True)
        genome_id = hashlib.sha256(study_json.encode()).hexdigest()
        study_config["genome_id"] = genome_id

        # Place karmic wager if requested
        wager_id = None
        if wager_karma and self.wager_system:
            try:
                from ..karmic_wager import wager_on_hypothesis

                wager = wager_on_hypothesis(
                    self.wager_system,
                    hypothesis=hypothesis,
                    karma_amount=wager_karma,
                    prediction=True,  # Predicting hypothesis will be confirmed
                    study_session_id=study_id,
                    odds=2.0,  # 2x payout for hypothesis bets
                )
                wager_id = wager.wager_id
                study_config["wager_id"] = wager_id
            except Exception:
                # Continue without wager if it fails
                pass

        # Save study configuration
        study_file = self.output_dir / f"{study_id}_config.json"
        study_file.write_text(json.dumps(study_config, indent=2))

        return study_config

    def conduct_study(
        self, study_config: dict[str, Any], challenge_config: dict[str, Any]
    ) -> StudySession:
        """
        Conduct a study using Study Gym.

        Args:
            study_config: Study configuration
            challenge_config: Study Gym challenge configuration

        Returns:
            Completed StudySession
        """
        # Start Study Gym session
        session = self.study_gym.start_session(challenge_config)

        # Link session to study
        session.study_id = study_config["study_id"]
        session.genome_id = study_config.get("genome_id")

        # Run scientific method workflow
        # (This would integrate with Study Gym's workflow)

        return session

    def resolve_study_wager(
        self, study_config: dict[str, Any], study_session: StudySession
    ) -> dict[str, Any] | None:
        """
        Resolve karmic wager based on study outcome.

        Args:
            study_config: Study configuration
            study_session: Completed StudySession

        Returns:
            Wager resolution result or None if no wager
        """
        wager_id = study_config.get("wager_id")
        if not wager_id or not self.wager_system:
            return None

        # Determine outcome from study session
        # Hypothesis confirmed if confidence >= 0.7 and status is "confirmed"
        confirmed = False
        for hyp in study_session.hypotheses:
            if hyp.confidence >= 0.7 and hyp.status == "confirmed":
                confirmed = True
                break

        outcome = {
            "confirmed": confirmed,
            "hypotheses": len(study_session.hypotheses),
            "confirmed_count": sum(1 for h in study_session.hypotheses if h.status == "confirmed"),
            "findings": study_session.findings,
            "conclusions": study_session.conclusions,
        }

        # Resolve wager
        try:
            result = self.wager_system.resolve_wager(wager_id, outcome)
            return result
        except Exception:
            return None

    def generate_paper(
        self,
        study_config: dict[str, Any],
        study_session: StudySession | None = None,
        format: str = "full",  # "full" or "summary" (2-page)
    ) -> Path:
        """
        Generate scientific research paper from study.

        Args:
            study_config: Study configuration
            study_session: Completed StudySession (optional)
            format: "full" or "summary" (2-page)

        Returns:
            Path to generated paper
        """
        # Load template
        template_path = Path(__file__).parent / "templates" / "scientific_research_paper.md"
        template = template_path.read_text()

        # Gather data for paper
        paper_data = self._gather_paper_data(study_config, study_session)

        # Fill template
        paper_content = self._fill_template(template, paper_data)

        # Generate paper
        if format == "summary":
            # Use TwoPageGenerator for 2-page summary
            return self._generate_summary(paper_content, study_config)
        else:
            # Generate full paper
            return self._generate_full_paper(paper_content, study_config)

    def _gather_paper_data(
        self, study_config: dict[str, Any], study_session: StudySession | None
    ) -> dict[str, Any]:
        """Gather all data needed for paper."""
        data = {
            "title": self._generate_title(study_config),
            "abstract": self._generate_abstract(study_config, study_session),
            "research_question": study_config.get("research_question", ""),
            "hypothesis": study_config.get("hypothesis", ""),
            "objectives": study_config.get("objectives", []),
            "study_id": study_config.get("study_id", ""),
            "genome_id": study_config.get("genome_id", ""),
            "date": study_config.get("created_at", datetime.now().isoformat()),
            "waft_version": self._get_waft_version(),
        }

        # Add Study Gym data if available
        if study_session:
            data.update(
                {
                    "observations": [obs.__dict__ for obs in study_session.observations],
                    "hypotheses": [hyp.__dict__ for hyp in study_session.hypotheses],
                    "findings": study_session.findings,
                    "conclusions": study_session.conclusions,
                }
            )

        # Add wager information if present
        wager_id = study_config.get("wager_id")
        if wager_id and self.wager_system:
            wager_stats = self.wager_system.get_wager_stats()
            data["wager_info"] = {
                "wager_id": wager_id,
                "karma_wagered": study_config.get("wager_karma", 0),
                "wager_stats": wager_stats,
            }

        return data

    def _generate_title(self, study_config: dict[str, Any]) -> str:
        """Generate paper title from study config."""
        research_question = study_config.get("research_question", "WAFT Self-Study")
        return f"Self-Study of WAFT: {research_question}"

    def _generate_abstract(
        self, study_config: dict[str, Any], study_session: StudySession | None
    ) -> str:
        """Generate abstract from study data."""
        abstract_parts = [
            f"This study investigates {study_config.get('research_question', 'WAFT behavior')}.",
            f"Hypothesis: {study_config.get('hypothesis', 'Not specified')}.",
        ]

        if study_session:
            abstract_parts.append(
                f"Using WAFT's Study Gym, we conducted {len(study_session.observations)} observations, "
                f"formed {len(study_session.hypotheses)} hypotheses, and reached "
                f"{len(study_session.conclusions)} conclusions."
            )

        # Add wager info if present
        wager_id = study_config.get("wager_id")
        if wager_id:
            abstract_parts.append(
                f"This study included a karmic wager of {study_config.get('wager_karma', 0)} karma "
                f"on the hypothesis being confirmed, demonstrating WAFT's engagement through risk/reward mechanics."
            )

        abstract_parts.append(
            "This research contributes to understanding the physics of artificial cognition "
            "through WAFT's evolutionary mechanisms."
        )

        return " ".join(abstract_parts)

    def _fill_template(self, template: str, data: dict[str, Any]) -> str:
        """Fill template with data."""
        # Simple template filling (can be enhanced with Jinja2)
        content = template

        # Replace placeholders
        for key, value in data.items():
            if isinstance(value, list):
                value = "\n".join(f"- {item}" for item in value)
            content = content.replace(f"[{key}]", str(value))

        return content

    def _generate_summary(self, paper_content: str, study_config: dict[str, Any]) -> Path:
        """Generate 2-page summary using TwoPageGenerator."""
        # Distill content
        distilled = self.distiller.distill_text(
            paper_content, title=study_config.get("study_id", "WAFT Self-Study")
        )

        # Get or create styling genome
        genome = self._get_or_create_styling_genome()

        # Generate 2-page PDF
        generator = TwoPageGenerator(weasyprint_available=True, allowed_pages=2)
        output_path = self.output_dir / f"{study_config['study_id']}_summary.pdf"

        generator.generate(
            distilled_chat=distilled, styling_genome=genome, output_path=output_path, target_pages=2
        )

        return output_path

    def _generate_full_paper(self, paper_content: str, study_config: dict[str, Any]) -> Path:
        """Generate full-length paper."""
        # Save markdown
        md_path = self.output_dir / f"{study_config['study_id']}_paper.md"
        md_path.write_text(paper_content)

        # Could also generate PDF using DocumentBuilder
        # For now, return markdown path
        return md_path

    def _get_or_create_styling_genome(self) -> StylingGenome:
        """Get or create styling genome for scientific papers."""
        # Try to load existing genome
        # For now, create a new one optimized for scientific papers
        from .styling_genome import ColorGene, FontGene, LayoutGene, MarginGene, StylingGene

        scientific_genes = StylingGene(
            font=FontGene(
                family="Times New Roman, serif",  # Academic standard
                size_body=11,
                size_h1=16,
                size_h2=14,
                size_h3=12,
                size_code=10,
                line_height=1.5,
            ),
            margin=MarginGene(
                top=25, bottom=25, left=25, right=25, paragraph_spacing=6, section_spacing=12
            ),
            color=ColorGene(
                text="#000000",
                background="#FFFFFF",
                heading="#000000",
                accent="#333333",
                code_bg="#f5f5f5",
                code_text="#000000",
                border="#cccccc",
            ),
            layout=LayoutGene(
                columns=1,
                density="normal",
                toc_enabled=False,
                page_numbers=True,
                header_enabled=True,
                footer_enabled=True,
            ),
            name="Scientific Paper Styling",
        )

        genome = StylingGenome.from_genes(scientific_genes)

        # Register genome
        try:
            self.registry.register(genome)
        except Exception:
            pass  # Continue if registration fails

        return genome

    def _get_waft_version(self) -> str:
        """Get current WAFT version."""
        try:
            from ... import __version__

            return __version__
        except ImportError:
            return "unknown"


def generate_waft_self_study_paper(
    research_question: str,
    hypothesis: str,
    objectives: list[str],
    study_gym_challenge: dict[str, Any] | None = None,
    format: str = "summary",
    wager_karma: float | None = None,
) -> Path:
    """
    Convenience function to generate a WAFT self-study paper.

    Args:
        research_question: Primary research question
        hypothesis: Testable hypothesis
        objectives: List of study objectives
        study_gym_challenge: Optional Study Gym challenge config
        format: "full" or "summary" (2-page)
        wager_karma: Optional karma amount to wager on hypothesis

    Returns:
        Path to generated paper
    """
    generator = ScientificPaperGenerator(enable_wagers=True)

    # Create study (with optional wager)
    study_config = generator.create_study(
        research_question=research_question,
        hypothesis=hypothesis,
        objectives=objectives,
        wager_karma=wager_karma,
    )

    # Conduct study if challenge provided
    study_session = None
    if study_gym_challenge:
        study_session = generator.conduct_study(study_config, study_gym_challenge)

        # Resolve wager if study completed
        if wager_karma:
            generator.resolve_study_wager(study_config, study_session)

    # Generate paper
    return generator.generate_paper(study_config, study_session, format=format)
