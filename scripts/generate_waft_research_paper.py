#!/usr/bin/env python3
"""
Generate WAFT Self-Study Research Paper - CLI Tool

Usage:
    python scripts/generate_waft_research_paper.py \
        --question "How does X work in WAFT?" \
        --hypothesis "X causes Y" \
        --objectives "Measure X" "Analyze Y" \
        --format summary
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.scientific_paper_generator import generate_waft_self_study_paper


def main():
    """CLI for generating WAFT self-study research papers."""
    parser = argparse.ArgumentParser(
        description="Generate scientific research papers for WAFT self-study",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 2-page summary
  %(prog)s --question "How does evolution work?" \\
           --hypothesis "Evolution improves fitness" \\
           --objectives "Measure fitness" "Track lineage" \\
           --format summary

  # Generate full paper
  %(prog)s --question "How does evolution work?" \\
           --hypothesis "Evolution improves fitness" \\
           --objectives "Measure fitness" "Track lineage" \\
           --format full
        """
    )
    
    parser.add_argument(
        "--question", "-q",
        required=True,
        help="Primary research question"
    )
    
    parser.add_argument(
        "--hypothesis", "-h",
        required=True,
        help="Testable hypothesis"
    )
    
    parser.add_argument(
        "--objectives", "-o",
        nargs="+",
        required=True,
        help="Study objectives (one or more)"
    )
    
    parser.add_argument(
        "--format", "-f",
        choices=["summary", "full"],
        default="summary",
        help="Paper format: 'summary' (2-page) or 'full' (default: summary)"
    )
    
    parser.add_argument(
        "--output", "-O",
        type=Path,
        help="Output path (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    print("🔬 WAFT Self-Study Research Paper Generator")
    print("=" * 80)
    print(f"\nResearch Question: {args.question}")
    print(f"\nHypothesis: {args.hypothesis}")
    print(f"\nObjectives:")
    for i, obj in enumerate(args.objectives, 1):
        print(f"  {i}. {obj}")
    print(f"\nFormat: {args.format}")
    print()
    
    try:
        paper_path = generate_waft_self_study_paper(
            research_question=args.question,
            hypothesis=args.hypothesis,
            objectives=args.objectives,
            format=args.format
        )
        
        print("✅ Paper generated successfully!")
        print(f"📄 Output: {paper_path}")
        print("\n🎉 WAFT is studying itself using the scientific method!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
