"""
Demo: AI Town Voting System

Demonstrates the voting system with random selection of Beings.
"""

from pathlib import Path
from src.waft.being import Being, BeingSystem
from src.waft.reality import RealitySystem, RealityType
from src.waft.ai_town.town_voting import TownVotingSystem, VoteType

def main():
    """Run voting system demo."""
    project_path = Path(__file__).parent.parent
    
    # Initialize systems
    being_system = BeingSystem(project_path=project_path)
    reality_system = RealitySystem(project_path=project_path)
    voting_system = TownVotingSystem(project_path=project_path)
    
    # Create a town reality
    reality = reality_system.create_reality(
        reality_type=RealityType.RESEARCH,
        configuration={
            "name": "Voting Demo Town",
            "description": "Demo town for voting system"
        },
        source_id="source_consciousness"
    )
    
    reality_id = reality.reality_id
    reality = reality_system.start_reality(reality_id)
    
    print(f"✓ Created town reality: {reality_id}\n")
    
    # Spawn 5 Beings with different skills
    print("Spawning Beings into town...")
    town_beings = []
    
    being_configs = [
        {"code_analysis": 30.0, "pattern_recognition": 25.0},  # Being 1: Architecture
        {"algorithm_extraction": 30.0, "data_analysis": 25.0},  # Being 2: Algorithms
        {"research_analysis": 30.0, "comparison": 25.0},  # Being 3: Paper analysis
        {"integration_analysis": 30.0, "waft_knowledge": 25.0},  # Being 4: Integration
        {"documentation": 30.0, "synthesis": 25.0},  # Being 5: Documentation
    ]
    
    for i, skills in enumerate(being_configs):
        being = being_system.spawn_being(
            reality_id=reality_id,
            initial_skills=skills
        )
        reality_system.spawn_being_into_reality(reality_id, being.being_id)
        town_beings.append(being)
        print(f"  ✓ Being {i+1}: {being.being_id[:40]}... (skills: {list(skills.keys())[0]})")
    
    print(f"\n✓ Town formed with {len(town_beings)} Beings\n")
    
    # Conduct a vote: PDF Format (Town's Choice)
    print("=" * 60)
    print("TOWN VOTE: PDF Format (Town's Choice)")
    print("=" * 60)
    
    voting_result = voting_system.conduct_town_vote(
        town_beings=town_beings,
        decision_id="pdf_format",
        question="What format should the final output be?",
        options=["binder", "single_pdf"],
        vote_type=VoteType.BINARY
    )
    
    # Display results
    print(f"\nQuestion: {voting_result['question']}")
    print(f"Options: {voting_result['options']}")
    print(f"\nSelection Process:")
    print(f"  Selected Beings: {len(voting_result['selected_beings'])}")
    for being_id in voting_result['selected_beings']:
        print(f"    - {being_id[:40]}...")
    print(f"  Non-selected Beings: {len(voting_result['non_selected_beings'])}")
    for being_id in voting_result['non_selected_beings']:
        print(f"    - {being_id[:40]}...")
    
    print(f"\nVotes:")
    for vote in voting_result['votes']:
        being_id = vote['being_id'][:40]
        choice = vote['vote']
        reasoning = vote['reasoning'][:60] + "..." if len(vote['reasoning']) > 60 else vote['reasoning']
        print(f"  {being_id}... → {choice}")
        print(f"    Reasoning: {reasoning}")
    
    print(f"\nResults:")
    print(f"  Vote Counts: {voting_result['vote_counts']}")
    print(f"  Total Votes: {voting_result['total_votes']}")
    print(f"  Is Tie: {voting_result['is_tie']}")
    if voting_result.get('tie_broken_by'):
        print(f"  Tie Broken By: {voting_result['tie_broken_by']}")
    print(f"  🎯 Town's Choice: {voting_result['result']}")
    
    print(f"\n✓ Voting record saved to: {voting_system.voting_records_path}")
    print("=" * 60)
    
    # Conduct another vote: Top Integration Opportunities (Ranked)
    print("\n" + "=" * 60)
    print("TOWN VOTE: Top Integration Opportunities")
    print("=" * 60)
    
    voting_result2 = voting_system.conduct_town_vote(
        town_beings=town_beings,
        decision_id="integration_opportunities",
        question="What are the top 3 integration opportunities?",
        options=["pattern_sharing", "memory_system", "evolution_engine", "documentation_tools"],
        vote_type=VoteType.RANKED
    )
    
    print(f"\nQuestion: {voting_result2['question']}")
    print(f"Options: {voting_result2['options']}")
    print(f"\nSelected Beings: {len(voting_result2['selected_beings'])}")
    
    print(f"\nVotes (Ranked):")
    for vote in voting_result2['votes']:
        being_id = vote['being_id'][:40]
        rankings = vote['vote']
        print(f"  {being_id}... → {rankings}")
    
    print(f"\nResults (Borda Count Scores):")
    print(f"  Scores: {voting_result2['vote_counts']}")
    print(f"  🎯 Town's Top 3: {voting_result2['result']}")
    
    print("=" * 60)
    
    # Show voting history
    print("\n" + "=" * 60)
    print("VOTING HISTORY")
    print("=" * 60)
    
    history = voting_system.get_voting_history()
    print(f"\nTotal voting records: {len(history)}")
    for record in history:
        print(f"  - {record['decision_id']}: {record['result']} ({record['total_votes']} votes)")
    
    print("=" * 60)
    print("\n✓ Voting system demo complete!")

if __name__ == "__main__":
    main()
