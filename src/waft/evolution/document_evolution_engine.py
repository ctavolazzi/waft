"""
Document Evolution Engine

The main orchestrator that:
- Uses evolved components with traits
- Learns from generation results
- Incorporates user feedback
- Self-documents its evolution
- Uses randomness for exploration
- Gradually improves over time
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import random

from .component_evolution import (
    ComponentEvolutionEngine, EvolvedComponent, ComponentTrait, SectionPreference
)
from .user_feedback import UserFeedbackCollector, FeedbackEntry
from .component_generator import ComponentPDFGenerator
from .chat_distiller import ChatDistiller, DistilledChat
from .styling_genome import StylingGenome, StylingGenomeRegistry, StylingGene


class DocumentEvolutionEngine(ComponentPDFGenerator):
    """
    Evolutionary document creator that learns and improves over time.
    
    Features:
    - Components evolve with traits (min_pages, height, section preferences)
    - Learns from user feedback
    - Self-documents its evolution
    - Uses randomness for exploration
    - Stores and uses historical data
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        weasyprint_available: bool = True,
        max_iterations: int = 10,
        default_allowed_pages: int = 2,
        evolution_dir: Optional[Path] = None,
        exploration_rate: float = 0.2,  # 20% random exploration
    ):
        """
        Initialize evolution engine.
        
        Args:
            project_path: Project root path
            weasyprint_available: Whether WeasyPrint is available
            max_iterations: Max layout attempts
            default_allowed_pages: Default target page count
            evolution_dir: Directory for evolution data
            exploration_rate: Probability of random exploration (0.0-1.0)
        """
        super().__init__(
            project_path=project_path,
            weasyprint_available=weasyprint_available,
            max_iterations=max_iterations,
            default_allowed_pages=default_allowed_pages,
        )
        
        # Initialize evolution systems
        if evolution_dir is None:
            evolution_dir = project_path / "_genetics" / "document_evolution" if project_path else Path("_genetics/document_evolution")
        
        self.evolution_engine = ComponentEvolutionEngine(evolution_dir=evolution_dir)
        self.feedback_collector = UserFeedbackCollector(feedback_dir=evolution_dir / "feedback")
        self.exploration_rate = exploration_rate
        
        # Self-documentation
        self.documentation_dir = evolution_dir / "documentation"
        self.documentation_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_one_pager(
        self,
        content: str,
        title: str,
        output_path: Optional[Path] = None,
        allowed_pages: Optional[int] = None,
        styling_genome: Optional[StylingGenome] = None,
        image_paths: Optional[Dict[str, str]] = None,
        author: str = "WAFT Research Team",
        use_science_paper_structure: bool = True,
        use_evolved_components: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate one-pager using evolved components.
        
        Args:
            content: Text content
            title: Document title
            output_path: Output path
            allowed_pages: Target pages
            styling_genome: Styling config
            image_paths: Image paths
            author: Author name
            use_science_paper_structure: Use science paper structure
            use_evolved_components: Use evolved components (default: True)
        
        Returns:
            Generation results with evolution metadata
        """
        if allowed_pages is None:
            allowed_pages = self.default_allowed_pages
        
        # Distill content
        distilled = self.distiller.distill_text(content, title=title)
        
        # Get or create styling genome
        if styling_genome is None:
            registry = StylingGenomeRegistry()
            styling_genome = registry.get_best_genome()
            if styling_genome is None:
                from .styling_genome import StylingGene
                default_genes = StylingGene(name="default", description="Default styling")
                styling_genome = StylingGenome.from_genes(default_genes)
        
        # Generate using parent's method (which uses component system)
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.project_path / "_work_efforts" / "one_pagers" / f"EvolvedPDF_{timestamp}.pdf"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use parent's generation method
        result = super().generate_one_pager(
            content=content,
            title=title,
            output_path=output_path,
            allowed_pages=allowed_pages,
            styling_genome=styling_genome,
            image_paths=image_paths,
            author=author,
            use_science_paper_structure=use_science_paper_structure,
        )
        
        # Track components used for learning
        components_used = []
        if use_evolved_components and result.get('layout'):
            # Extract component IDs from layout
            layout = result.get('layout')
            if hasattr(layout, 'components'):
                for comp in layout.components:
                    if hasattr(comp, 'evolved_component'):
                        components_used.append(comp.evolved_component.component_id)
        
        # Learn from results
        if result.get('success') and use_evolved_components:
            # Extract components from layout for learning
            layout = result.get('layout')
            if layout and hasattr(layout, 'components'):
                self._learn_from_generation(
                    components=layout.components,
                    result=result,
                    allowed_pages=allowed_pages,
                )
        
        # Add evolution metadata
        result['evolution'] = {
            'components_used': components_used,
            'exploration_used': result.get('learning_summary', {}).get('strategy_performance', {}),
            'feedback_summary': self.feedback_collector.get_feedback_summary(),
        }
        
        return result
    
    def _build_evolved_components(
        self,
        distilled: DistilledChat,
        title: str,
        image_paths: Optional[Dict[str, str]],
        author: str,
        allowed_pages: int,
        use_science_paper_structure: bool,
    ) -> List[Any]:
        """Build components using evolved traits."""
        from .document_components import DocumentComponent, ComponentType, ComponentBuilder
        
        components = []
        builder = ComponentBuilder()
        
        # Get or create evolved components
        title_comp = self.evolution_engine.get_or_create_component("title", "title_main")
        if allowed_pages >= title_comp.trait.min_pages_required:
            components.append(builder.build_title_component(title))
            # Store component reference for learning
            components[-1].evolved_component = title_comp
        
        # Images
        if image_paths:
            for img_name, img_path in image_paths.items():
                img_comp = self.evolution_engine.get_or_create_component("image", f"image_{img_name}")
                if allowed_pages >= img_comp.trait.min_pages_required:
                    img_uri = Path(img_path).absolute().as_uri() if Path(img_path).exists() else img_path
                    caption = f"Figure {len([c for c in components if hasattr(c, 'component_type') and getattr(c, 'component_type', None) == ComponentType.IMAGE]) + 1}: {img_name.replace('_', ' ').title()}"
                    components.append(builder.build_image_component(img_uri, caption))
                    components[-1].evolved_component = img_comp
        
        # Abstract
        abstract_comp = self.evolution_engine.get_or_create_component("abstract", "abstract_main")
        if allowed_pages >= abstract_comp.trait.min_pages_required:
            components.append(builder.build_abstract_component(distilled.summary))
            components[-1].evolved_component = abstract_comp
        
        # Attribution
        attr_comp = self.evolution_engine.get_or_create_component("attribution", "attribution_main")
        if allowed_pages >= attr_comp.trait.min_pages_required:
            components.append(builder.build_attribution_component(
                author,
                datetime.now().strftime("%Y-%m-%d")
            ))
            components[-1].evolved_component = attr_comp
        
        # Sections from ideas
        all_ideas = distilled.get_top_ideas(n=50, min_importance=0.1)
        
        if use_science_paper_structure:
            sections = self._build_science_paper_sections(all_ideas)
        else:
            sections = self._build_generic_sections(all_ideas)
        
        # Use evolved section components
        for section_title, section_ideas in sections:
            if section_ideas:
                # Decide section preference based on evolved traits
                section_comp = self.evolution_engine.get_or_create_component(
                    "section",
                    f"section_{section_title.lower().replace(' ', '_')}"
                )
                
                # Check if component wants to be in this section
                section_pref = self._get_section_preference(section_title)
                preference_weight = section_comp.trait.section_preferences.get(
                    section_pref, 0.5
                )
                
                # Use randomness for exploration
                use_component = (
                    random.random() < (1.0 - self.exploration_rate) * preference_weight
                    or random.random() < self.exploration_rate  # Random exploration
                )
                
                if use_component and allowed_pages >= section_comp.trait.min_pages_required:
                    components.append(builder.build_section_component(
                        section_title,
                        section_ideas,
                        level=2
                    ))
                    components[-1].evolved_component = section_comp
                    components[-1].section_preference = section_pref
        
        return components
    
    def _build_standard_components(self, *args, **kwargs) -> List[Any]:
        """Fallback to standard component building."""
        # This would use the parent class's standard method
        # For now, just return empty list and let parent handle it
        return []
    
    def _get_section_preference(self, section_title: str) -> SectionPreference:
        """Map section title to preference."""
        title_lower = section_title.lower()
        if "introduction" in title_lower:
            return SectionPreference.BODY_START
        elif "conclusion" in title_lower:
            return SectionPreference.CONCLUSION
        elif "architecture" in title_lower or "methodology" in title_lower:
            return SectionPreference.BODY_MIDDLE
        else:
            return SectionPreference.ANYWHERE
    
    def _learn_from_generation(
        self,
        components: List[Any],
        result: Dict[str, Any],
        allowed_pages: int,
    ):
        """Learn from generation results."""
        success = result.get('page_count') == allowed_pages
        fitness = result.get('fitness', {}).get('overall_fitness', 0.5)
        
        for comp in components:
            if hasattr(comp, 'evolved_component'):
                evolved = comp.evolved_component
                section_pref = getattr(comp, 'section_preference', None)
                
                self.evolution_engine.learn_from_generation(
                    component_id=evolved.component_id,
                    success=success,
                    fitness=fitness,
                    pages_used=allowed_pages,
                    section_used=section_pref,
                )
    
    def record_user_feedback(
        self,
        liked: bool,
        component_id: Optional[str] = None,
        document_id: Optional[str] = None,
        message: Optional[str] = None,
        strength: float = 1.0,
    ):
        """
        Record user feedback and apply learning.
        
        Args:
            liked: True if liked, False if disliked
            component_id: Specific component ID
            document_id: Document ID
            message: Optional feedback message
            strength: Feedback strength (0.0-1.0)
        """
        # Record in feedback collector
        self.feedback_collector.record_feedback(
            liked=liked,
            component_id=component_id,
            document_id=document_id,
            message=message,
            strength=strength,
        )
        
        # Apply learning to evolution engine
        if component_id:
            self.evolution_engine.learn_from_user_feedback(
                component_id=component_id,
                liked=liked,
                feedback_strength=strength,
            )
        
        # Trigger evolution if needed
        self._consider_evolution()
    
    def _consider_evolution(self):
        """Consider evolving components based on feedback patterns."""
        # Get components with low fitness
        low_fitness = [
            comp for comp in self.evolution_engine.components.values()
            if comp.trait.get_fitness() < 0.3 and comp.trait.success_count + comp.trait.failure_count > 5
        ]
        
        # Evolve low-fitness components
        for comp in low_fitness[:3]:  # Evolve up to 3 at a time
            self.evolution_engine.evolve_component(
                component_id=comp.component_id,
                mutation_rate=0.15,  # Higher mutation for struggling components
            )
    
    def generate_evolution_report(self) -> Path:
        """Generate self-documentation report."""
        report_path = self.documentation_dir / f"evolution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = f"""# Document Evolution Engine Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview

This document is generated by the Document Evolution Engine itself, documenting its own evolution and learning.

## Component Evolution

{self.evolution_engine.get_evolution_report()}

## User Feedback Summary

"""
        feedback_summary = self.feedback_collector.get_feedback_summary()
        report += f"""
- **Total Feedback Entries**: {feedback_summary.get('total', 0)}
- **Likes**: {feedback_summary.get('likes', 0)}
- **Dislikes**: {feedback_summary.get('dislikes', 0)}
- **Suggestions**: {feedback_summary.get('suggestions', 0)}

### Component-Level Feedback

"""
        for comp_id, feedback in feedback_summary.get('component_feedback', {}).items():
            report += f"- **{comp_id}**: {feedback.get('likes', 0)} likes, {feedback.get('dislikes', 0)} dislikes\n"
        
        report += f"""

## Evolution Parameters

- **Exploration Rate**: {self.exploration_rate * 100:.1f}%
- **Max Iterations**: {self.max_iterations}
- **Default Allowed Pages**: {self.default_allowed_pages}

## Recent Feedback

"""
        recent = self.feedback_collector.get_recent_feedback(limit=10)
        for entry in recent:
            report += f"- **{entry.timestamp.strftime('%Y-%m-%d %H:%M')}**: {entry.feedback_type} "
            if entry.component_id:
                report += f"(component: {entry.component_id}) "
            if entry.message:
                report += f"- {entry.message}"
            report += "\n"
        
        report_path.write_text(report)
        return report_path
