"""
Component-Based PDF Generator

A high-level interface for generating adaptive, component-based PDFs.
Integrates with TheFoundation and provides a clean API for one-pagers,
research documents, and other variable-length documents.

Features:
- Component-based architecture (Title, Image, Abstract, Sections, etc.)
- Adaptive layout algorithm (tries different combinations, learns what works)
- Configurable page count (not just 2 pages)
- Science paper structure support
- Learning mechanism (records what works/doesn't work)
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .chat_distiller import ChatDistiller, DistilledChat
from .styling_genome import StylingGenome, StylingGenomeRegistry
from .two_page_generator import TwoPageGenerator
from .document_components import (
    ComponentBuilder, LayoutAlgorithm, DocumentLayout, ComponentType
)


class ComponentPDFGenerator:
    """
    High-level component-based PDF generator.
    
    Provides a clean API for generating adaptive PDFs using the component system.
    Can integrate with TheFoundation for WAFT-specific workflows.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        weasyprint_available: bool = True,
        max_iterations: int = 10,
        default_allowed_pages: int = 2,
    ):
        """
        Initialize ComponentPDFGenerator.
        
        Args:
            project_path: Optional project root path (for image paths, etc.)
            weasyprint_available: Whether WeasyPrint is available
            max_iterations: Max layout attempts
            default_allowed_pages: Default target page count
        """
        self.project_path = project_path or Path.cwd()
        self.weasyprint_available = weasyprint_available
        self.max_iterations = max_iterations
        self.default_allowed_pages = default_allowed_pages
        
        # Initialize core components
        self.distiller = ChatDistiller()
        self.builder = ComponentBuilder()
        self.generator = TwoPageGenerator(
            weasyprint_available=weasyprint_available,
            max_iterations=max_iterations,
            allowed_pages=default_allowed_pages,
        )
    
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
    ) -> Dict[str, Any]:
        """
        Generate a one-pager PDF using component-based system.
        
        Args:
            content: Text content to distill into ideas
            title: Document title
            output_path: Output PDF path (auto-generated if None)
            allowed_pages: Target page count (uses default if None)
            styling_genome: Styling configuration (uses default if None)
            image_paths: Dict of image paths (e.g., {'three_pillars': 'path/to/image.png'})
            author: Author name for attribution
            use_science_paper_structure: Use Title → Image → Abstract → Attribution → Sections
        
        Returns:
            Dictionary with results, learning summary, and metadata
        """
        if allowed_pages is None:
            allowed_pages = self.default_allowed_pages
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.project_path / "_work_efforts" / "one_pagers" / f"ComponentPDF_{timestamp}.pdf"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Distill content
        distilled = self.distiller.distill_text(content, title=title)
        
        # Get or create styling genome
        if styling_genome is None:
            from .styling_genome import StylingGene, StylingGenome
            registry = StylingGenomeRegistry()
            styling_genome = registry.get_best_genome()
            if styling_genome is None:
                # Create default genome
                default_genes = StylingGene(name="default", description="Default styling")
                styling_genome = StylingGenome.from_genes(default_genes)
        
        # Build components
        components = []
        
        # 1. Title
        components.append(self.builder.build_title_component(title))
        
        # 2. Images (if provided)
        if image_paths:
            for img_name, img_path in image_paths.items():
                caption = f"Figure {len([c for c in components if c.component_type == ComponentType.IMAGE]) + 1}: {img_name.replace('_', ' ').title()}"
                # Convert to file:// URI if needed
                img_uri = Path(img_path).absolute().as_uri() if Path(img_path).exists() else img_path
                components.append(self.builder.build_image_component(img_uri, caption))
        
        # 3. Abstract
        components.append(self.builder.build_abstract_component(distilled.summary))
        
        # 4. Attribution
        components.append(self.builder.build_attribution_component(
            author,
            datetime.now().strftime("%Y-%m-%d")
        ))
        
        # 5. Sections from ideas
        all_ideas = distilled.get_top_ideas(n=50, min_importance=0.1)
        
        if use_science_paper_structure:
            # Science paper structure: Introduction, Architecture, Methodology, Conclusion
            sections = self._build_science_paper_sections(all_ideas)
        else:
            # Generic structure: just group ideas into sections
            sections = self._build_generic_sections(all_ideas)
        
        for section_title, section_ideas in sections:
            if section_ideas:
                components.append(self.builder.build_section_component(
                    section_title,
                    section_ideas,
                    level=2
                ))
        
        # Generate using component system
        result = self.generator.generate(
            distilled_chat=distilled,
            styling_genome=styling_genome,
            output_path=output_path,
            target_pages=allowed_pages,
            use_component_system=True,
        )
        
        return {
            'success': result.get('success', False),
            'pdf_path': result.get('pdf_path'),
            'html_path': result.get('html_path'),
            'page_count': result.get('page_count'),
            'target_pages': allowed_pages,
            'learning_summary': result.get('learning_summary', {}),
            'layout': result.get('layout'),
            'fitness': result.get('fitness', {}),
            'distilled_chat': distilled,
        }
    
    def _build_science_paper_sections(self, ideas: List) -> List[tuple]:
        """Build sections following science paper structure."""
        sections = []
        
        # Introduction (first idea)
        if ideas:
            sections.append(("Introduction", ideas[:1]))
        
        # Architecture (find pillar-related ideas)
        substrate_ideas = [idea for idea in ideas if 'substrate' in idea.content.lower() or 'code is dna' in idea.content.lower()][:1]
        physics_ideas = [idea for idea in ideas if 'scint' in idea.content.lower() or 'physics' in idea.content.lower() or 'fitness' in idea.content.lower()][:1]
        flight_recorder_ideas = [idea for idea in ideas if 'flight recorder' in idea.content.lower() or 'lineage' in idea.content.lower() or 'phylogenetic' in idea.content.lower()][:1]
        
        if substrate_ideas or physics_ideas or flight_recorder_ideas:
            # Architecture section header (empty, pillars will be subsections)
            sections.append(("Architecture", []))
            
            if substrate_ideas:
                sections.append(("The Substrate", substrate_ideas))
            if physics_ideas:
                sections.append(("The Physics", physics_ideas))
            if flight_recorder_ideas:
                sections.append(("The Flight Recorder", flight_recorder_ideas))
        
        # Methodology and Conclusion from remaining ideas
        remaining_ideas = [idea for idea in ideas[1:] if idea not in substrate_ideas + physics_ideas + flight_recorder_ideas]
        if remaining_ideas:
            split = len(remaining_ideas) // 2
            if split > 0:
                sections.append(("Methodology", remaining_ideas[:split]))
            if len(remaining_ideas) > split:
                sections.append(("Conclusion", remaining_ideas[split:]))
        
        return sections
    
    def _build_generic_sections(self, ideas: List) -> List[tuple]:
        """Build generic sections from ideas."""
        sections = []
        
        # Group ideas into sections of ~3 ideas each
        section_size = 3
        for i in range(0, len(ideas), section_size):
            section_ideas = ideas[i:i + section_size]
            section_title = f"Section {i // section_size + 1}"
            sections.append((section_title, section_ideas))
        
        return sections
    
    def generate_from_distilled(
        self,
        distilled_chat: DistilledChat,
        output_path: Path,
        allowed_pages: Optional[int] = None,
        styling_genome: Optional[StylingGenome] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate PDF from already-distilled content.
        
        Useful when you already have a DistilledChat object.
        """
        if allowed_pages is None:
            allowed_pages = self.default_allowed_pages
        
        if styling_genome is None:
            registry = StylingGenomeRegistry()
            styling_genome = registry.get_default_genome()
        
        return self.generator.generate(
            distilled_chat=distilled_chat,
            styling_genome=styling_genome,
            output_path=output_path,
            target_pages=allowed_pages,
            use_component_system=True,
            **kwargs
        )


class FoundationComponentGenerator(ComponentPDFGenerator):
    """
    Component generator integrated with TheFoundation.
    
    Extends ComponentPDFGenerator with WAFT-specific features:
    - Integration with TheObserver and TavernKeeper
    - WAFT-specific styling presets
    - Automatic image path resolution
    - Dossier-style output options
    """
    
    def __init__(
        self,
        project_path: Path,
        observer: Optional[Any] = None,
        tavern_keeper: Optional[Any] = None,
        **kwargs
    ):
        """
        Initialize FoundationComponentGenerator.
        
        Args:
            project_path: Project root path
            observer: Optional TheObserver instance
            tavern_keeper: Optional TavernKeeper instance
            **kwargs: Passed to ComponentPDFGenerator
        """
        super().__init__(project_path=project_path, **kwargs)
        
        # Initialize WAFT components
        if observer is None:
            from ..core.science.observer import TheObserver
            self.observer = TheObserver(project_path)
        else:
            self.observer = observer
        
        if tavern_keeper is None:
            from ..core.tavern_keeper import TavernKeeper
            self.tavern_keeper = TavernKeeper(project_path)
        else:
            self.tavern_keeper = tavern_keeper
    
    def generate_waft_one_pager(
        self,
        content: Optional[str] = None,
        title: str = "WAFT: The Evolutionary Code Laboratory",
        output_path: Optional[Path] = None,
        allowed_pages: int = 2,
        use_default_images: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate WAFT-specific one-pager with default settings.
        
        Args:
            content: Content text (uses default WAFT explanation if None)
            title: Document title
            output_path: Output path
            allowed_pages: Target page count
            use_default_images: Use default WAFT images if available
            **kwargs: Passed to generate_one_pager
        
        Returns:
            Generation results
        """
        # Get default content if not provided
        if content is None:
            from examples.generate_waft_intro_one_pager_bw import get_waft_explanation_content
            content = get_waft_explanation_content()
        
        # Get default images if requested
        image_paths = kwargs.pop('image_paths', {})
        if use_default_images:
            images_dir = self.project_path / "_work_efforts" / "one_pagers" / "images"
            three_pillars = images_dir / "three_pillars.png"
            if three_pillars.exists():
                image_paths['three_pillars'] = str(three_pillars)
        
        return self.generate_one_pager(
            content=content,
            title=title,
            output_path=output_path,
            allowed_pages=allowed_pages,
            image_paths=image_paths if image_paths else None,
            **kwargs
        )
