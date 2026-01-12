#!/usr/bin/env python3
"""
Test DocumentEvolutionEngine

Demonstrates the evolutionary document creator that learns over time.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import DocumentEvolutionEngine

def main():
    """Test the evolution engine."""
    # Sample content
    content = """
    WAFT (Wide-Area Functional Taxonomy) is an evolutionary code laboratory.
    It allows AI agents to modify their own code and evolve through generations.
    
    The system has three pillars:
    1. The Substrate: Code is DNA - agents can mutate their own source code
    2. The Physics: Scint Gym evaluates agents through error handling tests
    3. The Flight Recorder: Complete lineage tracking for scientific analysis
    
    Agents evolve through generations, with successful mutations surviving
    and unsuccessful ones being discarded. The system produces phylogenetic
    trees showing the evolution of code over time.
    """
    
    # Initialize evolution engine
    engine = DocumentEvolutionEngine(
        project_path=Path("."),
        default_allowed_pages=2,
        exploration_rate=0.2,  # 20% random exploration
    )
    
    # Generate PDF
    print("🔬 Generating document with evolved components...")
    result = engine.generate_one_pager(
        content=content,
        title="WAFT: The Evolutionary Code Laboratory",
        allowed_pages=2,
        author="WAFT Research Team",
        use_evolved_components=True,
    )
    
    if result['success']:
        print(f"✅ Success!")
        print(f"📄 PDF: {result['pdf_path']}")
        print(f"📊 Pages: {result['page_count']}/{result['target_pages']}")
        print(f"🎯 Learning: {result['learning_summary'].get('successful', 0)}/{result['learning_summary'].get('total_tests', 0)} successful")
        
        # Show evolution info
        if 'evolution' in result:
            print(f"\n🧬 Evolution:")
            print(f"  Components used: {len(result['evolution'].get('components_used', []))}")
            print(f"  Feedback entries: {result['evolution'].get('feedback_summary', {}).get('total', 0)}")
        
        # Simulate user feedback
        print("\n💬 Recording user feedback...")
        engine.record_user_feedback(
            liked=True,
            document_id=str(result.get('pdf_path', '')),
            message="Great layout and structure!",
            strength=0.9,
        )
        
        # Generate evolution report
        print("\n📝 Generating self-documentation...")
        report_path = engine.generate_evolution_report()
        print(f"  Report saved: {report_path}")
        
        print("\n✨ The system is learning and evolving!")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
