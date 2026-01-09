import sys
from waft.core.decision_matrix import (
    DecisionMatrix, Alternative, Criterion, Score, DecisionMatrixCalculator
)

def run_test_scenario(name: str, matrix: DecisionMatrix):
    print(f"\n--- TEST: {name} ---")
    
    # 1. Calculate
    calc = DecisionMatrixCalculator(matrix)
    results = calc.calculate_wsm()
    rankings = calc.rank_alternatives(results)
    detailed = calc.get_detailed_scores()

    # 2. Display Results
    print(f"{'Rank':<5} | {'Alternative':<15} | {'Score':<10}")
    print("-" * 35)
    for name, score, rank in rankings:
        print(f"{rank:<5} | {name:<15} | {score:<10.2f}")
    
    # 3. Validation Logic (Automated Checks)
    return rankings

def test_dominant_option():
    """Scenario A: The Sanity Check"""
    alts = [Alternative("SuperCar"), Alternative("Junker")]
    crits = [Criterion("Speed", 0.5), Criterion("Comfort", 0.5)]
    scores = [
        Score("SuperCar", "Speed", 10), Score("SuperCar", "Comfort", 10),
        Score("Junker", "Speed", 1),    Score("Junker", "Comfort", 1),
    ]
    matrix = DecisionMatrix(alts, crits, scores)
    rankings = run_test_scenario("A. The Dominant Option", matrix)
    
    # Objective Verification
    if rankings[0][0] == "SuperCar":
        print("✅ PASS: The obviously better option won.")
    else:
        print("❌ FAIL: The engine failed to pick the dominant option.")

def test_trade_off():
    """Scenario B: The Weight Sensitivity Check"""
    alts = [Alternative("Ferrari"), Alternative("Toyota")]
    
    # Test B1: Cost is King
    print("\n[Subtest B1: Prioritizing Cost (0.9)]")
    crits_cheap = [Criterion("Cost", 0.9), Criterion("Fun", 0.1)]
    scores = [
        Score("Ferrari", "Cost", 1),  Score("Ferrari", "Fun", 10),
        Score("Toyota", "Cost", 10),  Score("Toyota", "Fun", 5),
    ]
    matrix = DecisionMatrix(alts, crits_cheap, scores)
    rankings = run_test_scenario("B1. Trade-off (Cost Focused)", matrix)
    
    if rankings[0][0] == "Toyota":
        print("✅ PASS: Engine correctly prioritized Cost.")
    else:
        print("❌ FAIL: Engine ignored the heavy Cost weight.")

    # Test B2: Fun is King
    print("\n[Subtest B2: Prioritizing Fun (0.9)]")
    crits_fun = [Criterion("Cost", 0.1), Criterion("Fun", 0.9)]
    # (Same scores, new weights)
    # We must recreate the matrix object because it is immutable (Iron Core!)
    matrix2 = DecisionMatrix(alts, crits_fun, scores)
    rankings2 = run_test_scenario("B2. Trade-off (Fun Focused)", matrix2)

    if rankings2[0][0] == "Ferrari":
        print("✅ PASS: Engine correctly prioritized Fun.")
    else:
        print("❌ FAIL: Engine ignored the heavy Fun weight.")

def test_poison_pill():
    """Scenario C: The 'Fatal Flaw' Weakness"""
    alts = [Alternative("Star_Candidate"), Alternative("Safe_Candidate")]
    
    # Integrity is important (30%), but skills/exp are 70% combined
    crits = [
        Criterion("Skills", 0.35), 
        Criterion("Experience", 0.35), 
        Criterion("Integrity", 0.30)
    ]
    
    scores = [
        # Star Candidate: Perfect skills, but ZERO integrity (Liar)
        Score("Star_Candidate", "Skills", 10), 
        Score("Star_Candidate", "Experience", 10), 
        Score("Star_Candidate", "Integrity", 0),
        
        # Safe Candidate: Average but honest
        Score("Safe_Candidate", "Skills", 6), 
        Score("Safe_Candidate", "Experience", 6), 
        Score("Safe_Candidate", "Integrity", 10),
    ]
    
    matrix = DecisionMatrix(alts, crits, scores)
    rankings = run_test_scenario("C. The Poison Pill (Fatal Flaw)", matrix)
    
    winner = rankings[0][0]
    score = rankings[0][1]
    
    print("\n🤔 ANALYSIS:")
    if winner == "Star_Candidate":
        print(f"⚠️  OBSERVATION: The 'Star' won ({score:.2f}) despite 0 Integrity.")
        print("   This validates that WSM allows high scores to mask fatal flaws.")
        print("   LESSON: You must veto options with '0' scores manually.")
    else:
        print("✅ PASS: The weight on Integrity was high enough to sink the ship.")

if __name__ == "__main__":
    print("=== DECISION ENGINE VALIDATION SUITE ===")
    test_dominant_option()
    test_trade_off()
    test_poison_pill()
