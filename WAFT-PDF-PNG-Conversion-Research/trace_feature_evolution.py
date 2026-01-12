#!/usr/bin/env python3
"""
Retroactively trace the evolution of the PDF/PNG conversion feature.

This script creates IdeaGenes and EvolutionaryEvents for the feature development,
tracking it through WAFT's evolutionary system.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.evolution.chat_distiller import IdeaGene
from waft.core.agent.state import EvolutionaryEvent, EvolutionaryEventType


def create_feature_ideas() -> List[IdeaGene]:
    """Create IdeaGenes for the PDF/PNG conversion feature evolution."""
    
    ideas = [
        # Genesis: The initial need
        IdeaGene(
            content="Add bidirectional PDF/PNG conversion: PDF to PNG (one per page) and PNG to PDF (binder)",
            category="feature",
            context="User needs to convert PDFs to images for viewing and PNGs back to PDFs for storage",
            importance=0.9,
            source_location="session-2026-01-11-141000",
            tags=["pdf", "png", "conversion", "genesis", "feature"]
        ),
        
        # Decision: Multiple backend support
        IdeaGene(
            content="Implement fallback chain for PDF to PNG: pdf2image → ImageMagick → PyMuPDF",
            category="decision",
            context="Ensure robustness across different environments without requiring all dependencies",
            importance=0.85,
            source_location="pdf_image_converter.py",
            tags=["pdf_to_png", "backend", "fallback", "robustness", "decision"]
        ),
        
        # Decision: Standard page size
        IdeaGene(
            content="Use 8.5x11 inches (letter size) as standard for PNG to PDF conversion",
            category="decision",
            context="Consistency with user expectations and standard document sizes",
            importance=0.8,
            source_location="pdf_image_converter.py",
            tags=["png_to_pdf", "page_size", "standard", "decision"]
        ),
        
        # Decision: Automatic integration
        IdeaGene(
            content="Automatically convert PDFs to PNGs after one-pager generation",
            category="decision",
            context="Proactive tooling - system anticipates needs rather than requiring explicit requests",
            importance=0.85,
            source_location="create_chat_one_pager_v2.py",
            tags=["auto_integration", "workflow", "proactive", "decision"]
        ),
        
        # Implementation: PDF to PNG function
        IdeaGene(
            content="Implement pdf_to_pngs() with multiple backend support and DPI configuration",
            category="action",
            context="Core conversion function with fallback chain and configurable quality",
            importance=0.9,
            source_location="pdf_image_converter.py:pdf_to_pngs",
            tags=["implementation", "pdf_to_png", "function", "action"]
        ),
        
        # Implementation: PNG to PDF function
        IdeaGene(
            content="Implement pngs_to_pdf() with 8.5x11 page size and crop-to-size option",
            category="action",
            context="Binder creation function with standard page size and quality preservation",
            importance=0.9,
            source_location="pdf_image_converter.py:pngs_to_pdf",
            tags=["implementation", "png_to_pdf", "function", "action"]
        ),
        
        # Insight: Graceful degradation pattern
        IdeaGene(
            content="Fallback chains enable robustness: try best, fall back gracefully",
            category="insight",
            context="Pattern of 'try best, fall back gracefully' is valuable for any system with optional dependencies",
            importance=0.8,
            source_location="pdf_image_converter.py",
            tags=["pattern", "robustness", "fallback", "insight"]
        ),
        
        # Insight: Proactive tooling
        IdeaGene(
            content="Automatic workflow integration creates seamless user experience",
            category="insight",
            context="Users don't need to remember extra steps - the system handles it",
            importance=0.75,
            source_location="create_chat_one_pager_v2.py",
            tags=["ux", "workflow", "automation", "insight"]
        ),
    ]
    
    return ideas


def create_evolution_events(ideas: List[IdeaGene]) -> List[EvolutionaryEvent]:
    """Create EvolutionaryEvents tracking the feature development."""
    
    events = []
    
    # Find genesis idea (feature creation)
    genesis_idea = next((i for i in ideas if "genesis" in i.tags), None)
    if not genesis_idea:
        return events
    
    # Genesis event (SPAWN - feature was born)
    events.append(EvolutionaryEvent(
        timestamp=datetime(2026, 1, 11, 14, 0, 0),  # Approximate session start
        genome_id=genesis_idea.genome_id,
        parent_id=None,
        generation=0,
        event_type=EvolutionaryEventType.SPAWN,
        payload={
            "feature": "PDF/PNG Conversion",
            "description": "Feature spawned from user need",
            "scientific_name": genesis_idea.scientific_name,
            "source": "session-2026-01-11-141000"
        },
        fitness_metrics=None,
        agent_id="feature_development",
        lineage_path=[genesis_idea.genome_id]
    ))
    
    # Decision events (MUTATE - feature evolved through decisions)
    decision_ideas = [i for i in ideas if i.category == "decision"]
    for i, idea in enumerate(decision_ideas, start=1):
        events.append(EvolutionaryEvent(
            timestamp=datetime(2026, 1, 11, 14, 5, i),  # Sequential decisions
            genome_id=idea.genome_id,
            parent_id=genesis_idea.genome_id,
            generation=1,
            event_type=EvolutionaryEventType.MUTATE,
            payload={
                "mutation_type": "decision",
                "decision": idea.content,
                "scientific_name": idea.scientific_name,
                "context": idea.context
            },
            fitness_metrics=None,
            agent_id="feature_development",
            lineage_path=[genesis_idea.genome_id, idea.genome_id]
        ))
    
    # Implementation events (MUTATE - code changes)
    action_ideas = [i for i in ideas if i.category == "action"]
    for i, idea in enumerate(action_ideas, start=1):
        parent = decision_ideas[0] if decision_ideas else genesis_idea
        events.append(EvolutionaryEvent(
            timestamp=datetime(2026, 1, 11, 14, 8, i),  # After decisions
            genome_id=idea.genome_id,
            parent_id=parent.genome_id,
            generation=2,
            event_type=EvolutionaryEventType.MUTATE,
            payload={
                "mutation_type": "implementation",
                "implementation": idea.content,
                "scientific_name": idea.scientific_name,
                "source_location": idea.source_location
            },
            fitness_metrics=None,
            agent_id="feature_development",
            lineage_path=[genesis_idea.genome_id, parent.genome_id, idea.genome_id]
        ))
    
    # Validation event (GYM_EVAL - testing validated the feature)
    # Use the test suite's end-to-end test as validation
    validation_event = EvolutionaryEvent(
        timestamp=datetime(2026, 1, 11, 22, 21, 34),  # From test execution
        genome_id=genesis_idea.genome_id,
        parent_id=genesis_idea.genome_id,
        generation=0,
        event_type=EvolutionaryEventType.GYM_EVAL,
        payload={
            "validation_type": "comprehensive_testing",
            "test_phases": 4,
            "success_rate": 0.75,
            "scientific_name": genesis_idea.scientific_name
        },
        fitness_metrics={
            "conversion_reliability": 1.0,
            "prose_quality": 0.982,
            "workflow_completeness": 1.0,
            "overall_success": 0.75
        },
        agent_id="test_suite",
        lineage_path=[genesis_idea.genome_id]
    )
    events.append(validation_event)
    
    return events


def main():
    """Main execution: create and save feature evolution tracking."""
    
    research_dir = Path(__file__).parent
    ideas_file = research_dir / "traced_ideas" / "feature_evolution_ideas.jsonl"
    events_file = research_dir / "traced_ideas" / "feature_evolution_events.jsonl"
    
    # Create ideas
    ideas = create_feature_ideas()
    
    # Create events
    events = create_evolution_events(ideas)
    
    # Save ideas
    with open(ideas_file, "w") as f:
        for idea in ideas:
            f.write(json.dumps(idea.to_dict(), default=str) + "\n")
    
    # Save events
    with open(events_file, "w") as f:
        for event in events:
            f.write(json.dumps(event.model_dump(), default=str) + "\n")
    
    print(f"✅ Created {len(ideas)} IdeaGenes for feature evolution")
    print(f"✅ Created {len(events)} EvolutionaryEvents for feature development")
    print(f"📁 Ideas saved to: {ideas_file}")
    print(f"📁 Events saved to: {events_file}")
    
    # Print summary
    print("\n📊 Feature Evolution Summary:")
    print(f"  Genesis: {ideas[0].scientific_name}")
    print(f"  Decisions: {len([i for i in ideas if i.category == 'decision'])}")
    print(f"  Implementations: {len([i for i in ideas if i.category == 'action'])}")
    print(f"  Insights: {len([i for i in ideas if i.category == 'insight'])}")
    print(f"  Total Events: {len(events)}")
    
    return ideas, events


if __name__ == "__main__":
    main()
