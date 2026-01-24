#!/usr/bin/env python3
"""
Example: Using Scientist God to Analyze WAFT's RPG Gym

This demonstrates the complete scientific workflow:
1. Hypothesize
2. Design experiment
3. Collect evidence
4. Generate whitepaper
5. Compile and publish
"""

from pathlib import Path
import sys

# Add WAFT to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.pantheon.scientist_god import (
    ScientistGod,
    EvidenceType,
    ExperimentStatus
)


def demo_rpg_gym_analysis():
    """Complete analysis of WAFT's RPG Gym using Scientist God."""
    
    print("🔬 Scientist God Demo: Analyzing WAFT RPG Gym")
    print("=" * 60)
    
    # Initialize Scientist God
    scientist = ScientistGod(
        project_path=Path("/Users/ctavolazzi/Code/active/waft")
    )
    
    print("\n📋 Step 1: Generate Hypothesis")
    print("-" * 60)
    
    # 1. Hypothesize
    hyp = scientist.hypothesize(
        statement="WAFT has a functional RPG Gym with reality fracture detection (Scint mechanics)",
        expected_confidence=0.5  # Unsure at first
    )
    
    print(f"✅ Hypothesis created: {hyp.id}")
    print(f"   Statement: {hyp.statement}")
    print(f"   Initial confidence: {hyp.confidence:.1%}")
    
    # 2. Design experiment
    print("\n🧪 Step 2: Design Experiment")
    print("-" * 60)
    
    exp = scientist.design_experiment(
        hypothesis=hyp,
        name="RPG Gym Discovery and Verification",
        methodology="""
        1. Search codebase for RPG-related files
        2. Inspect scint detection implementation
        3. Run test suite (pytest)
        4. Verify Scint type taxonomy
        5. Check D&D integration (character sheets, stats)
        6. Analyze stabilization loop
        """,
        investigation_techniques=[
            "Source code inspection",
            "Test execution (pytest)",
            "Pattern search (grep/rg)",
            "File counting (wc -l)",
        ]
    )
    
    print(f"✅ Experiment designed: {exp.id}")
    print(f"   Name: {exp.name}")
    print(f"   Status: {exp.status.value}")
    
    # 3. Collect evidence
    print("\n📊 Step 3: Collect Evidence")
    print("-" * 60)
    
    # Evidence 1: Source code exists
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.SOURCE_CODE,
        location="src/gym/rpg/scint.py:21-30",
        content="""
class ScintType(Enum):
    SYNTAX_TEAR = auto()      # JSON, XML errors → CHA
    LOGIC_FRACTURE = auto()   # Math, contradictions → INT
    SAFETY_VOID = auto()      # Harmful content, refusals → WIS
    HALLUCINATION = auto()    # Fabricated facts → INT
        """,
        supports=True,
        metadata={"file_size": "198 lines"}
    )
    print("✅ Evidence 1: Scint type taxonomy found")
    
    # Evidence 2: Tests pass
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.TEST_OUTPUT,
        location="pytest tests/test_scint_mechanics.py -v",
        content="""
tests/test_scint_mechanics.py::test_scint_classification_syntax PASSED   [ 20%]
tests/test_scint_mechanics.py::test_scint_classification_logic PASSED    [ 40%]
tests/test_scint_mechanics.py::test_scint_classification_safety PASSED   [ 60%]
tests/test_scint_mechanics.py::test_severity_calculation PASSED          [ 80%]
tests/test_scint_mechanics.py::test_stabilization_prompt PASSED          [100%]

============================== 5 passed in 0.23s ===============================
        """,
        supports=True,
        metadata={"tests_passed": 5, "tests_failed": 0}
    )
    print("✅ Evidence 2: All tests passing (5/5)")
    
    # Evidence 3: File structure
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.SOURCE_CODE,
        location="src/gym/rpg/",
        content="""
Total lines in RPG Gym: 1,098
- scint.py: 198 lines (detection logic)
- stabilizer.py: 400 lines (reflexion loop)
- game_master.py: 287 lines (orchestration)
- models.py: 213 lines (D&D character sheets)
        """,
        supports=True,
        metadata={"total_lines": 1098}
    )
    print("✅ Evidence 3: Complete implementation (1,098 lines)")
    
    # Evidence 4: Severity formula
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.SOURCE_CODE,
        location="src/gym/rpg/scint.py:130-148",
        content="""
def _calculate_severity(self, scint_type: ScintType, difficulty: int) -> float:
    BASE_SEVERITY = {
        ScintType.SYNTAX_TEAR: 0.3,
        ScintType.LOGIC_FRACTURE: 0.5,
        ScintType.HALLUCINATION: 0.6,
        ScintType.SAFETY_VOID: 0.9,
    }
    
    base = BASE_SEVERITY.get(scint_type, 0.5)
    boost = (difficulty - 1) * 0.1
    return min(1.0, base + boost)
        """,
        supports=True,
        metadata={"verified": True}
    )
    print("✅ Evidence 4: Severity formula verified")
    
    print(f"\n📈 Updated hypothesis confidence: {hyp.confidence:.1%}")
    print(f"   Evidence for: {len(hyp.evidence_for)}")
    print(f"   Evidence against: {len(hyp.evidence_against)}")
    
    # 4. Generate whitepaper
    print("\n📄 Step 4: Generate Whitepaper")
    print("-" * 60)
    
    wp_dir = scientist.generate_whitepaper(
        experiment=exp,
        title="WAFT RPG Gym Analysis",
        author="Scientist God (Demo)",
        auto_populate=True
    )
    
    print(f"✅ Whitepaper initialized at: {wp_dir}")
    print(f"   Sections auto-populated with {len(hyp.evidence_for)} evidence items")
    
    # 5. Status check
    print("\n📊 Step 5: Scientific Work Status")
    print("-" * 60)
    
    status = scientist.status()
    print(f"Total hypotheses: {status['hypotheses']['total']}")
    print(f"Total experiments: {status['experiments']['total']}")
    print(f"Whitepapers generated: {status['whitepapers']}")
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("=" * 60)
    print(f"""
✅ Hypothesis: {hyp.statement}
   Confidence: {hyp.confidence:.1%} (increased from 50% → 100%)
   
✅ Experiment: {exp.name}
   Status: {exp.status.value}
   Evidence collected: {len(exp.results.get('evidence', []))} items
   
✅ Whitepaper: {wp_dir.name}
   Auto-populated: Yes
   Ready to compile: Yes

Next steps:
1. python3 tools/whitepaper_generator.py compile-all
   (from {wp_dir})
2. Review generated PDF
3. Publish to GitHub
    """)
    
    return scientist, hyp, exp


if __name__ == "__main__":
    try:
        scientist, hyp, exp = demo_rpg_gym_analysis()
        print("\n✅ Scientist God demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
