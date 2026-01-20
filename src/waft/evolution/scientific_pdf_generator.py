"""
Scientific PDF Generator - Research Tools for Self-Examination

Enhances PDFGenerator with scientific research capabilities:
- Self-examination and quality analysis
- Hypothesis testing via Study Gym
- Research tools (comparison, trends, patterns)
- Evolutionary learning
- Traceability and monitoring via TheObserver
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..core.agent.state import EvolutionaryEvent, EvolutionaryEventType
from ..core.science.observer import TheObserver
from ..karmic_wager import KarmicWagerSystem, wager_on_hypothesis
from ..study_gym import StudyGym
from .pdf_generator import PDFGenerator
from .pdf_metrics import PDFMetricsCollector


class ScientificPDFGenerator(PDFGenerator):
    """
    Enhanced PDF generator with scientific research capabilities.

    Features:
    - Self-examination and quality analysis
    - Hypothesis testing via Study Gym
    - Research tools (comparison, trends, patterns)
    - Evolutionary learning from previous PDFs
    """

    def __init__(
        self,
        content: str,
        title: str,
        styling_genome,
        distilled_chat=None,
        custom_css: str | None = None,
        scientific_mode: bool = True,
        study_gym_dir: Path | None = None,
        research_db_path: Path | None = None,
    ):
        """
        Initialize scientific PDF generator.

        Args:
            content: Raw content
            title: Document title
            styling_genome: Styling configuration
            distilled_chat: Pre-distilled chat (optional)
            custom_css: Additional CSS
            scientific_mode: Enable scientific analysis
            study_gym_dir: Study Gym output directory
            research_db_path: Research database path
        """
        super().__init__(content, title, styling_genome, distilled_chat, custom_css)
        self.scientific_mode = scientific_mode
        self.study_gym_dir = study_gym_dir or Path("_work_efforts/study_gym")
        self.research_db_path = research_db_path or Path("_work_efforts/pdf_research_db.json")

        # Initialize scientific components
        if scientific_mode:
            self.study_gym = StudyGym(output_dir=self.study_gym_dir)
            self.metrics_collector = PDFMetricsCollector(metrics_dir=Path("_pyrite/metrics/pdf"))
            self.observer = TheObserver(project_path=Path.cwd())
            self._load_research_db()

        # Generate genome_id for this PDF (for traceability)
        self.genome_id = self._generate_genome_id()
        self.generation = 0
        self.parent_id = None

    def _generate_genome_id(self) -> str:
        """Generate genome_id for this PDF (hash of content + title + timestamp)."""
        content_hash = hashlib.sha256(
            f"{self.title}:{self.content}:{datetime.now().isoformat()}".encode()
        ).hexdigest()
        return content_hash

    def _load_research_db(self):
        """Load research database for evolutionary learning."""
        if self.research_db_path.exists():
            with open(self.research_db_path) as f:
                self.research_db = json.load(f)
        else:
            self.research_db = {"pdfs": [], "hypotheses": [], "findings": [], "knowledge": []}

    def _save_research_db(self):
        """Save research database."""
        self.research_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.research_db_path, "w") as f:
            json.dump(self.research_db, f, indent=2)

    def _record_event(
        self,
        event_type: EvolutionaryEventType,
        payload: dict[str, Any],
        fitness_metrics: dict[str, Any] | None = None,
    ) -> None:
        """
        Record an event to TheObserver for traceability and monitoring.

        Args:
            event_type: Type of evolutionary event
            payload: Context-specific data
            fitness_metrics: Optional fitness scores
        """
        if not self.scientific_mode:
            return

        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id=self.genome_id,
            parent_id=self.parent_id,
            generation=self.generation,
            event_type=event_type,
            payload={
                "pdf_title": self.title,
                "scientific_name": self._get_scientific_name(),
                **payload,
            },
            fitness_metrics=fitness_metrics,
            agent_id=f"pdf_generator_{self.genome_id[:8]}",
            lineage_path=[self.genome_id]
            if self.parent_id is None
            else [self.parent_id, self.genome_id],
        )

        self.observer.observe_event(event)

    def _get_scientific_name(self) -> str:
        """Generate scientific name for this PDF."""
        try:
            from ..core.science.taxonomy import LineagePoet

            return LineagePoet.generate_name(self.genome_id)
        except Exception:
            return f"PDF_{self.genome_id[:8]}"

    def analyze_quality(self) -> dict[str, Any]:
        """
        Self-examination: Analyze the PDF's quality.

        Returns:
            Quality analysis with scores, gaps, and suggestions
        """
        if not self.scientific_mode:
            return {"error": "Scientific mode not enabled"}

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "title": self.title,
            "scores": {},
            "gaps": [],
            "suggestions": [],
            "comparison": {},
        }

        # Analyze content completeness
        if self.distilled_chat:
            total_ideas = self.distilled_chat.total_ideas
            concepts = self.distilled_chat.concepts_count
            actions = self.distilled_chat.actions_count
            insights = self.distilled_chat.insights_count

            completeness = (concepts + actions + insights) / max(total_ideas, 1)
            analysis["scores"]["completeness"] = completeness

            # Identify gaps
            if concepts == 0:
                analysis["gaps"].append("No concepts identified")
            if actions == 0:
                analysis["gaps"].append("No actions identified")
            if insights == 0:
                analysis["gaps"].append("No insights identified")

        # Analyze structure
        content_lower = self.content.lower()
        has_intro = any(
            word in content_lower for word in ["introduction", "overview", "background"]
        )
        has_method = any(word in content_lower for word in ["method", "approach", "process"])
        has_results = any(word in content_lower for word in ["result", "finding", "outcome"])
        has_conclusion = any(word in content_lower for word in ["conclusion", "summary", "final"])

        structure_score = sum([has_intro, has_method, has_results, has_conclusion]) / 4.0
        analysis["scores"]["structure"] = structure_score

        if not has_intro:
            analysis["gaps"].append("Missing introduction/overview section")
        if not has_method:
            analysis["gaps"].append("Missing methodology/approach section")
        if not has_results:
            analysis["gaps"].append("Missing results/findings section")
        if not has_conclusion:
            analysis["gaps"].append("Missing conclusion/summary section")

        # Generate suggestions
        if analysis["scores"].get("completeness", 0) < 0.7:
            analysis["suggestions"].append("Add more detailed content to improve completeness")
        if analysis["scores"].get("structure", 0) < 0.75:
            analysis["suggestions"].append("Improve document structure with clear sections")

        # Compare to previous PDFs
        if self.research_db.get("pdfs"):
            previous_avg = sum(p.get("quality_score", 0) for p in self.research_db["pdfs"]) / len(
                self.research_db["pdfs"]
            )
            current_quality = sum(analysis["scores"].values()) / max(len(analysis["scores"]), 1)
            analysis["comparison"] = {
                "vs_previous_avg": current_quality - previous_avg,
                "trend": "improving" if current_quality > previous_avg else "declining",
            }

        # Record self-examination event to TheObserver
        self._record_event(
            event_type=EvolutionaryEventType.GYM_EVAL,
            payload={
                "action": "self_examination",
                "analysis_type": "quality_analysis",
                "scores": analysis["scores"],
                "gaps_count": len(analysis["gaps"]),
                "suggestions_count": len(analysis["suggestions"]),
            },
            fitness_metrics={
                "quality_score": sum(analysis["scores"].values()) / max(len(analysis["scores"]), 1),
                "completeness": analysis["scores"].get("completeness", 0),
                "structure": analysis["scores"].get("structure", 0),
            },
        )

        return analysis

    def test_hypothesis(
        self,
        statement: str,
        reasoning: str = "",
        assumptions: list[str] | None = None,
        test_plan: str = "",
        wager_karma: float | None = None,
    ) -> dict[str, Any]:
        """
        Test a hypothesis about the PDF using Study Gym.

        Args:
            statement: Hypothesis statement
            reasoning: Why this hypothesis
            assumptions: List of assumptions
            test_plan: How to test
            wager_karma: Optional karma to wager

        Returns:
            Test results
        """
        if not self.scientific_mode:
            return {"error": "Scientific mode not enabled"}

        # Form hypothesis
        hypothesis = self.study_gym.form_hypothesis(
            statement=statement,
            reasoning=reasoning or f"Testing hypothesis about {self.title}",
            assumptions=assumptions or [],
            test_plan=test_plan or "Generate PDF and analyze quality",
            confidence=0.5,
        )

        # Place karmic wager if requested
        wager_id = None
        if wager_karma:
            try:
                wager_system = KarmicWagerSystem(project_path=Path.cwd())
                wager = wager_on_hypothesis(
                    wager_system,
                    hypothesis=statement,
                    karma_amount=wager_karma,
                    prediction=True,
                    odds=2.0,
                )
                wager_id = wager.wager_id
            except Exception:
                pass

        # Test hypothesis by analyzing quality
        analysis = self.analyze_quality()
        overall_quality = sum(analysis["scores"].values()) / max(len(analysis["scores"]), 1)

        # Evaluate hypothesis (simplified - could be more sophisticated)
        test_result = {
            "hypothesis": statement,
            "tested_at": datetime.now().isoformat(),
            "quality_score": overall_quality,
            "confirmed": overall_quality > 0.7,  # Threshold for confirmation
            "wager_id": wager_id,
        }

        # Update hypothesis status
        self.study_gym.test_hypothesis(hypothesis, test_result)

        # Record in research database
        self.research_db["hypotheses"].append(
            {
                "statement": statement,
                "reasoning": reasoning,
                "test_result": test_result,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self._save_research_db()

        return test_result

    def compare_with_previous(self, category: str | None = None) -> dict[str, Any]:
        """
        Compare this PDF with previous PDFs.

        Args:
            category: Optional category filter

        Returns:
            Comparative analysis
        """
        if not self.scientific_mode:
            return {"error": "Scientific mode not enabled"}

        previous_pdfs = [
            p
            for p in self.research_db.get("pdfs", [])
            if not category or p.get("category") == category
        ]

        if not previous_pdfs:
            return {"message": "No previous PDFs to compare"}

        current_analysis = self.analyze_quality()
        current_quality = sum(current_analysis["scores"].values()) / max(
            len(current_analysis["scores"]), 1
        )

        previous_qualities = [p.get("quality_score", 0) for p in previous_pdfs]
        avg_previous = (
            sum(previous_qualities) / len(previous_qualities) if previous_qualities else 0
        )

        comparison = {
            "current_quality": current_quality,
            "previous_avg": avg_previous,
            "improvement": current_quality - avg_previous,
            "trend": "improving" if current_quality > avg_previous else "declining",
            "compared_with": len(previous_pdfs),
            "best_previous": max(previous_qualities) if previous_qualities else 0,
            "worst_previous": min(previous_qualities) if previous_qualities else 0,
        }

        return comparison

    def identify_patterns(self) -> dict[str, Any]:
        """
        Identify patterns across previous PDFs.

        Returns:
            Pattern analysis
        """
        if not self.scientific_mode:
            return {"error": "Scientific mode not enabled"}

        patterns = {
            "styling_patterns": {},
            "quality_patterns": {},
            "content_patterns": {},
            "temporal_patterns": {},
        }

        pdfs = self.research_db.get("pdfs", [])
        if len(pdfs) < 2:
            return {"message": "Need at least 2 PDFs to identify patterns"}

        # Analyze styling patterns
        styles = [p.get("style") for p in pdfs if p.get("style")]
        if styles:
            from collections import Counter

            style_counts = Counter(styles)
            patterns["styling_patterns"]["most_common"] = (
                style_counts.most_common(1)[0][0] if style_counts else None
            )

        # Analyze quality patterns
        qualities = [p.get("quality_score", 0) for p in pdfs]
        if qualities:
            patterns["quality_patterns"]["average"] = sum(qualities) / len(qualities)
            patterns["quality_patterns"]["trend"] = (
                "improving" if qualities[-1] > qualities[0] else "declining"
            )

        # Analyze content patterns
        all_gaps = []
        for p in pdfs:
            all_gaps.extend(p.get("gaps", []))
        if all_gaps:
            from collections import Counter

            gap_counts = Counter(all_gaps)
            patterns["content_patterns"]["common_gaps"] = gap_counts.most_common(3)

        return patterns

    def save(
        self,
        output_path: Path | None = None,
        open_pdf: bool = False,
        include_all_ideas: bool = True,
        target_pages: int | None = None,
        collect_metrics: bool = True,
        convert_to_png: bool = True,
        png_dpi: int = 300,
    ) -> Path:
        """
        Generate and save PDF with scientific analysis.

        Args:
            output_path: Output path
            open_pdf: Open PDF after generation
            include_all_ideas: Include all ideas
            target_pages: Target page count
            collect_metrics: Collect PDF metrics
            convert_to_png: Convert PDF to PNG images after generation (default: True for evolutionary iteration)
            png_dpi: DPI for PNG conversion (default: 300)

        Returns:
            Path to generated PDF
        """
        # Generate PDF using parent method
        pdf_path = super().save(
            output_path=output_path,
            open_pdf=False,  # Don't open yet - we'll do analysis first
            include_all_ideas=include_all_ideas,
            target_pages=target_pages,
            convert_to_png=convert_to_png,
            png_dpi=png_dpi,
        )

        # Scientific analysis
        if self.scientific_mode:
            # Analyze quality
            analysis = self.analyze_quality()

            # Collect metrics if requested
            if collect_metrics:
                try:
                    # Generate with metrics
                    from .two_page_generator import TwoPageGenerator

                    generator = TwoPageGenerator(weasyprint_available=True)

                    all_ideas = self.distilled_chat.get_top_ideas(n=1000, min_importance=0.0)
                    mid_point = len(all_ideas) // 2
                    all_ideas[:mid_point]
                    all_ideas[mid_point:]

                    result = generator.generate(
                        distilled_chat=self.distilled_chat,
                        styling_genome=self.styling_genome,
                        output_path=pdf_path,
                        target_pages=target_pages,
                        collect_metrics=True,
                        use_component_system=False,
                    )

                    # Extract metrics
                    if "metrics" in result:
                        metrics = result["metrics"]
                        analysis["metrics"] = {
                            "quality_grade": metrics.get("quality_grade", "N/A"),
                            "quality_score": metrics.get("quality_score", 0.0),
                            "fitness_overall": metrics.get("fitness_metrics", {}).get(
                                "overall", 0.0
                            ),
                        }
                except Exception:
                    pass

            # Record in research database
            quality_score = sum(analysis["scores"].values()) / max(len(analysis["scores"]), 1)
            self.research_db["pdfs"].append(
                {
                    "title": self.title,
                    "path": str(pdf_path),
                    "timestamp": datetime.now().isoformat(),
                    "quality_score": quality_score,
                    "gaps": analysis["gaps"],
                    "suggestions": analysis["suggestions"],
                    "style": getattr(self.styling_genome.genes, "name", "unknown")
                    if hasattr(self.styling_genome, "genes")
                    else "unknown",
                    "genome_id": self.genome_id,
                }
            )
            self._save_research_db()

            # Save analysis report
            analysis_path = pdf_path.with_suffix(".analysis.json")
            with open(analysis_path, "w") as f:
                json.dump(analysis, f, indent=2)

            # Record PDF generation event to TheObserver
            self._record_event(
                event_type=EvolutionaryEventType.MUTATE,
                payload={
                    "action": "pdf_generation",
                    "pdf_path": str(pdf_path),
                    "title": self.title,
                    "style": getattr(self.styling_genome.genes, "name", "unknown")
                    if hasattr(self.styling_genome, "genes")
                    else "unknown",
                    "pages": target_pages or "unlimited",
                    "collect_metrics": collect_metrics,
                },
                fitness_metrics={
                    "quality_score": quality_score,
                    "completeness": analysis["scores"].get("completeness", 0),
                    "structure": analysis["scores"].get("structure", 0),
                    "gaps_count": len(analysis["gaps"]),
                    "suggestions_count": len(analysis["suggestions"]),
                },
            )

        # Open PDF if requested
        if open_pdf:
            import subprocess

            subprocess.run(["open", str(pdf_path)])

        return pdf_path

    @classmethod
    def from_content(
        cls,
        content: str,
        title: str,
        style: str = "clinical_standard",
        scientific_mode: bool = True,
        **kwargs,
    ) -> "ScientificPDFGenerator":
        """
        Create scientific PDF generator from content.

        Args:
            content: Content string
            title: Document title
            style: Preset style
            scientific_mode: Enable scientific analysis
            **kwargs: Additional arguments passed to parent

        Returns:
            ScientificPDFGenerator instance
        """
        # Use parent to create base generator
        base_generator = super().from_content(
            content=content, title=title, style=style, **kwargs
        )

        # Convert to scientific generator
        return cls(
            content=base_generator.content,
            title=base_generator.title,
            styling_genome=base_generator.styling_genome,
            distilled_chat=base_generator.distilled_chat,
            custom_css=base_generator.custom_css,
            scientific_mode=scientific_mode,
            study_gym_dir=kwargs.get("study_gym_dir"),
            research_db_path=kwargs.get("research_db_path"),
        )


# Convenience function
def generate_scientific_pdf(
    content: str,
    title: str,
    output_path: Path | None = None,
    style: str = "clinical_standard",
    scientific_mode: bool = True,
    open_pdf: bool = False,
    **kwargs,
) -> Path:
    """
    Quick function to generate a scientific PDF with self-examination.

    Example:
        generate_scientific_pdf(
            content="# My Research\n\nContent...",
            title="My Research",
            scientific_mode=True
        )
    """
    generator = ScientificPDFGenerator.from_content(
        content=content, title=title, style=style, scientific_mode=scientific_mode, **kwargs
    )

    # Perform self-examination
    if scientific_mode:
        analysis = generator.analyze_quality()
        print("\n🔬 Self-Examination Results:")
        print(
            f"   Quality Score: {sum(analysis['scores'].values()) / max(len(analysis['scores']), 1):.2f}"
        )
        print(f"   Gaps: {len(analysis['gaps'])}")
        print(f"   Suggestions: {len(analysis['suggestions'])}")

    return generator.save(
        output_path=output_path, open_pdf=open_pdf, collect_metrics=scientific_mode
    )
