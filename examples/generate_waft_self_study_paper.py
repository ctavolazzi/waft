#!/usr/bin/env python3
"""
Generate WAFT Self-Study Scientific Research Paper

Example script showing how to use WAFT to study itself using the scientific method.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.scientific_paper_generator import generate_waft_self_study_paper


def main():
    """Generate a WAFT self-study research paper."""
    
    # Example: Study how component evolution affects document quality
    research_question = (
        "How does component evolution with genetic ancestry improve "
        "document generation quality in WAFT's two-page generator?"
    )
    
    hypothesis = (
        "Component evolution with genetic ancestry and trait-based selection "
        "will produce higher fitness scores (readability, completeness, constraint satisfaction) "
        "compared to non-evolutionary layout algorithms."
    )
    
    objectives = [
        "Measure fitness scores of evolved vs. non-evolved component layouts",
        "Track component lineage and identify successful genetic patterns",
        "Analyze user feedback to understand quality improvements",
        "Document evolutionary convergence or divergence patterns"
    ]
    
    # Optional: Study Gym challenge configuration
    study_gym_challenge = {
        "name": "component_evolution_quality",
        "objective": "Compare evolved vs. non-evolved component layouts",
        "challenge_type": "comparison",
        "variables": {
            "use_evolution": True,
            "target_pages": 2,
            "content": "WAFT self-study research paper content"
        }
    }
    
    print("=" * 80)
    print("🔬 Generating WAFT Self-Study Scientific Research Paper")
    print("=" * 80)
    print(f"\nResearch Question: {research_question}")
    print(f"\nHypothesis: {hypothesis}")
    print(f"\nObjectives:")
    for i, obj in enumerate(objectives, 1):
        print(f"  {i}. {obj}")
    print()
    
    # Generate paper
    try:
        paper_path = generate_waft_self_study_paper(
            research_question=research_question,
            hypothesis=hypothesis,
            objectives=objectives,
            study_gym_challenge=study_gym_challenge,
            format="summary"  # 2-page summary
        )
        
        print("✅ Paper generated successfully!")
        print(f"📄 Output: {paper_path}")
        print("\n" + "=" * 80)
        print("🎉 WAFT is now studying itself using the scientific method!")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error generating paper: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
