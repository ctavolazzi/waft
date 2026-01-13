"""
Town Voting System: Democratic voting for AI Town Beings.

Implements random selection of Beings for voting (mostly at random, weighted by relevance).
Supports multiple vote types: binary, multiple choice, ranked, weighted.
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
import json
import random
from enum import Enum


class VoteType(Enum):
    """Types of votes."""
    BINARY = "binary"  # Yes/No, Option A/Option B
    MULTIPLE_CHOICE = "multiple_choice"  # Option A/B/C/D
    RANKED = "ranked"  # Rank options 1-3
    WEIGHTED = "weighted"  # Assign weights to options


class TownVotingSystem:
    """
    Voting system for AI town decisions.
    
    Handles:
    - Random selection of Beings to vote (mostly at random, weighted by relevance)
    - Vote collection from selected Beings
    - Result calculation (majority wins, ties broken by Oracle)
    - Vote record storage and transparency
    """
    
    # Decision ID to relevance skill mapping
    # Maps decision types to skills that make a Being more relevant
    DECISION_RELEVANCE_MAP = {
        "pdf_format": ["documentation", "synthesis"],
        "integration_opportunities": ["integration_analysis", "waft_knowledge"],
        "next_steps_priority": [],  # All perspectives valuable
        "section_inclusion": ["documentation", "synthesis"],
        "analysis_depth": ["code_analysis", "algorithm_extraction", "pattern_recognition"],
        "output_style": ["documentation", "synthesis"],
    }
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the voting system.
        
        Args:
            project_path: Path to project root (for storing voting records)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.voting_records_path = project_path / "_hidden" / ".truth" / "voting_records"
        self.voting_records_path.mkdir(parents=True, exist_ok=True)
        
        # Set directory permissions (0700 = owner read/write/execute only)
        try:
            self.voting_records_path.chmod(0o700)
        except (OSError, PermissionError):
            # Ignore if permissions can't be set (e.g., on Windows)
            pass
    
    def select_voting_beings(
        self,
        town_beings: List[Any],  # List of Being objects
        decision_id: str,
        selection_size: Optional[int] = None,
        random_weight: float = 0.7,
        relevance_weight: float = 0.3
    ) -> List[Any]:
        """
        Randomly select some Beings to participate in voting (mostly at random).
        
        Selection is weighted slightly by relevance:
        - Beings with relevant skills more likely selected
        - But still mostly random - not deterministic
        
        Args:
            town_beings: All Beings in town
            decision_id: Decision ID (for relevance weighting)
            selection_size: Number of Beings to select (default: 50-70% of town)
            random_weight: Weight for random component (default: 0.7)
            relevance_weight: Weight for relevance component (default: 0.3)
        
        Returns:
            List of selected Being objects
        """
        if not town_beings:
            return []
        
        if selection_size is None:
            # Default: 50-70% of town
            selection_size = max(2, int(len(town_beings) * random.uniform(0.5, 0.7)))
        
        # Ensure selection_size doesn't exceed available Beings
        selection_size = min(selection_size, len(town_beings))
        
        # Calculate relevance weights (slight weighting, mostly random)
        weights = []
        for being in town_beings:
            relevance = self._calculate_relevance(being, decision_id)
            # Weight: random_weight + (relevance_weight * relevance)
            # This makes it mostly random (70%) but slightly weighted by relevance (30%)
            weight = random_weight + (relevance_weight * relevance)
            weights.append(weight)
        
        # Select Beings based on weights
        # Use random.choices with weights, but ensure we get unique Beings
        selected = []
        available_beings = list(town_beings)
        available_weights = list(weights)
        
        for _ in range(selection_size):
            if not available_beings:
                break
            
            # Select one Being based on weights
            being = random.choices(available_beings, weights=available_weights, k=1)[0]
            selected.append(being)
            
            # Remove selected Being from available pool
            idx = available_beings.index(being)
            available_beings.pop(idx)
            available_weights.pop(idx)
        
        return selected
    
    def _calculate_relevance(self, being: Any, decision_id: str) -> float:
        """
        Calculate relevance score for a Being for a given decision.
        
        Args:
            being: Being object
            decision_id: Decision ID
        
        Returns:
            Relevance score (0.0 to 1.0)
        """
        # Get relevant skills for this decision
        relevant_skills = self.DECISION_RELEVANCE_MAP.get(decision_id, [])
        
        if not relevant_skills:
            # No specific relevance - all Beings equally relevant
            return 0.5
        
        # Calculate relevance based on Being's skills
        if not hasattr(being, 'skills') or not being.skills:
            return 0.0
        
        # Sum up relevant skill levels
        total_relevance = 0.0
        for skill_name in relevant_skills:
            skill_level = being.skills.get(skill_name, 0.0)
            # Normalize skill level (assuming max 100.0)
            normalized_level = min(1.0, skill_level / 100.0)
            total_relevance += normalized_level
        
        # Average relevance across relevant skills
        if relevant_skills:
            avg_relevance = total_relevance / len(relevant_skills)
        else:
            avg_relevance = 0.5
        
        return avg_relevance
    
    def collect_vote(
        self,
        being: Any,
        decision_id: str,
        question: str,
        options: List[str],
        vote_type: VoteType = VoteType.BINARY
    ) -> Dict[str, Any]:
        """
        Collect vote from a selected Being.
        
        Args:
            being: Being object that was selected to vote
            decision_id: Decision ID
            question: Question being voted on
            options: Available options
            vote_type: Type of vote (binary, multiple_choice, ranked, weighted)
        
        Returns:
            Vote record with being_id, vote choice, reasoning, selected status
        """
        # For MVP, we'll use a simple approach:
        # Being votes based on their skills and personality
        # In a full implementation, this would use LLM to generate vote and reasoning
        
        being_id = getattr(being, 'being_id', str(id(being)))
        
        # Simple voting logic based on Being's characteristics
        if vote_type == VoteType.BINARY:
            # Binary: choose one option
            vote_choice = self._being_binary_vote(being, options)
        elif vote_type == VoteType.MULTIPLE_CHOICE:
            # Multiple choice: choose one option
            vote_choice = self._being_multiple_choice_vote(being, options)
        elif vote_type == VoteType.RANKED:
            # Ranked: rank all options
            vote_choice = self._being_ranked_vote(being, options)
        elif vote_type == VoteType.WEIGHTED:
            # Weighted: assign weights to options
            vote_choice = self._being_weighted_vote(being, options)
        else:
            # Default: binary
            vote_choice = self._being_binary_vote(being, options)
        
        # Generate reasoning (simplified for MVP)
        reasoning = self._generate_reasoning(being, vote_choice, question, options)
        
        return {
            "being_id": being_id,
            "vote": vote_choice,
            "reasoning": reasoning,
            "selected": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _being_binary_vote(self, being: Any, options: List[str]) -> str:
        """Being votes on binary choice."""
        if len(options) != 2:
            # Fallback to first option if not exactly 2
            return options[0] if options else ""
        
        # Simple logic: Being with higher synthesis/documentation skills prefers first option
        # This is placeholder - real implementation would use Being's analysis
        skills = getattr(being, 'skills', {})
        synthesis_skill = skills.get('synthesis', 0.0) + skills.get('documentation', 0.0)
        
        # 50% base + skill influence
        preference = 0.5 + (synthesis_skill / 200.0)  # Normalize to 0.5-1.0 range
        
        if random.random() < preference:
            return options[0]
        else:
            return options[1]
    
    def _being_multiple_choice_vote(self, being: Any, options: List[str]) -> str:
        """Being votes on multiple choice."""
        if not options:
            return ""
        
        # Simple: random choice weighted by Being's skills
        # Real implementation would analyze Being's perspective
        return random.choice(options)
    
    def _being_ranked_vote(self, being: Any, options: List[str]) -> List[Dict[str, Any]]:
        """Being ranks options."""
        if not options:
            return []
        
        # Simple: random ranking
        # Real implementation would rank based on Being's analysis
        ranked = list(options)
        random.shuffle(ranked)
        
        return [
            {"option": option, "rank": i + 1}
            for i, option in enumerate(ranked)
        ]
    
    def _being_weighted_vote(self, being: Any, options: List[str]) -> Dict[str, float]:
        """Being assigns weights to options."""
        if not options:
            return {}
        
        # Simple: equal weights with slight variation
        # Real implementation would weight based on Being's analysis
        weights = {}
        base_weight = 1.0 / len(options)
        
        for option in options:
            # Add small random variation
            variation = random.uniform(-0.1, 0.1)
            weights[option] = max(0.0, base_weight + variation)
        
        # Normalize to sum to 1.0
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        
        return weights
    
    def _generate_reasoning(self, being: Any, vote_choice: Any, question: str, options: List[str]) -> str:
        """Generate reasoning for Being's vote."""
        being_id = getattr(being, 'being_id', 'unknown')
        skills = getattr(being, 'skills', {})
        
        # Simple reasoning based on Being's characteristics
        # Real implementation would use LLM to generate thoughtful reasoning
        skill_summary = ", ".join([f"{k}: {v:.1f}" for k, v in list(skills.items())[:3]])
        
        if isinstance(vote_choice, str):
            return f"Being {being_id[:8]}... chose '{vote_choice}' based on skills: {skill_summary}"
        elif isinstance(vote_choice, list):
            return f"Being {being_id[:8]}... ranked options based on skills: {skill_summary}"
        elif isinstance(vote_choice, dict):
            return f"Being {being_id[:8]}... weighted options based on skills: {skill_summary}"
        else:
            return f"Being {being_id[:8]}... voted based on skills: {skill_summary}"
    
    def conduct_town_vote(
        self,
        town_beings: List[Any],
        decision_id: str,
        question: str,
        options: List[str],
        vote_type: VoteType = VoteType.BINARY,
        oracle: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Conduct a town vote on a decision.
        
        Only selected Beings participate in voting.
        
        Args:
            town_beings: All Beings in town
            decision_id: Decision ID
            question: Question being voted on
            options: Available options
            vote_type: Type of vote
            oracle: Optional Oracle instance for tie breaking
        
        Returns:
            Complete voting record with results
        """
        # Select some Beings (mostly at random)
        selected_beings = self.select_voting_beings(town_beings, decision_id)
        non_selected_beings = [b for b in town_beings if b not in selected_beings]
        
        # Collect votes from selected Beings only
        votes = []
        for being in selected_beings:
            vote = self.collect_vote(being, decision_id, question, options, vote_type)
            votes.append(vote)
        
        # Calculate results
        results = self.calculate_results(votes, vote_type)
        
        # Break tie with Oracle if needed
        if results.get("is_tie") and oracle:
            results["result"] = self._oracle_break_tie(oracle, question, options, votes)
            results["tie_broken_by"] = "oracle"
        
        # Create complete voting record
        voting_record = {
            "decision_id": decision_id,
            "question": question,
            "options": options,
            "vote_type": vote_type.value,
            "selected_beings": [getattr(b, 'being_id', str(id(b))) for b in selected_beings],
            "non_selected_beings": [getattr(b, 'being_id', str(id(b))) for b in non_selected_beings],
            "selection_method": "random_weighted_by_relevance",
            "votes": votes,
            "result": results.get("result"),
            "vote_counts": results.get("vote_counts", {}),
            "is_tie": results.get("is_tie", False),
            "total_votes": results.get("total_votes", 0),
            "tie_broken_by": results.get("tie_broken_by"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Save voting record
        self._save_voting_record(voting_record)
        
        return voting_record
    
    def calculate_results(
        self,
        votes: List[Dict[str, Any]],
        vote_type: VoteType = VoteType.BINARY
    ) -> Dict[str, Any]:
        """
        Calculate voting results.
        
        Args:
            votes: List of vote records
            vote_type: Type of vote
        
        Returns:
            Result with winning option, vote counts, tie status
        """
        if not votes:
            return {
                "result": None,
                "vote_counts": {},
                "is_tie": False,
                "total_votes": 0
            }
        
        if vote_type == VoteType.BINARY or vote_type == VoteType.MULTIPLE_CHOICE:
            # Count votes for each option
            vote_counts = {}
            for vote in votes:
                choice = vote.get("vote")
                if choice:
                    vote_counts[choice] = vote_counts.get(choice, 0) + 1
            
            # Find winner (majority)
            if vote_counts:
                winner = max(vote_counts.items(), key=lambda x: x[1])
                is_tie = list(vote_counts.values()).count(winner[1]) > 1
                
                return {
                    "result": winner[0] if not is_tie else None,
                    "vote_counts": vote_counts,
                    "is_tie": is_tie,
                    "total_votes": len(votes)
                }
        
        elif vote_type == VoteType.RANKED:
            # Ranked choice voting - use Borda count
            option_scores = {}
            for vote in votes:
                rankings = vote.get("vote", [])
                for rank_item in rankings:
                    option = rank_item.get("option")
                    rank = rank_item.get("rank", len(rankings))
                    # Borda count: higher rank = more points
                    points = len(rankings) - rank + 1
                    option_scores[option] = option_scores.get(option, 0) + points
            
            if option_scores:
                winner = max(option_scores.items(), key=lambda x: x[1])
                is_tie = list(option_scores.values()).count(winner[1]) > 1
                
                return {
                    "result": winner[0] if not is_tie else None,
                    "vote_counts": option_scores,  # Scores instead of counts
                    "is_tie": is_tie,
                    "total_votes": len(votes)
                }
        
        elif vote_type == VoteType.WEIGHTED:
            # Weighted voting - sum weights
            option_weights = {}
            for vote in votes:
                weights = vote.get("vote", {})
                for option, weight in weights.items():
                    option_weights[option] = option_weights.get(option, 0.0) + weight
            
            if option_weights:
                winner = max(option_weights.items(), key=lambda x: x[1])
                is_tie = list(option_weights.values()).count(winner[1]) > 1
                
                return {
                    "result": winner[0] if not is_tie else None,
                    "vote_counts": option_weights,  # Weights instead of counts
                    "is_tie": is_tie,
                    "total_votes": len(votes)
                }
        
        return {
            "result": None,
            "vote_counts": {},
            "is_tie": False,
            "total_votes": len(votes)
        }
    
    def _oracle_break_tie(self, oracle: Any, question: str, options: List[str], votes: List[Dict[str, Any]]) -> str:
        """
        Use Oracle to break a tie.
        
        Args:
            oracle: Oracle instance
            question: Question being voted on
            options: Available options
            votes: All votes cast
        
        Returns:
            Winning option (Oracle's choice)
        """
        # For MVP, use simple logic
        # Real implementation would consult Oracle system
        if hasattr(oracle, 'break_tie'):
            return oracle.break_tie(question, options, votes)
        
        # Fallback: choose first option
        return options[0] if options else ""
    
    def _save_voting_record(self, voting_record: Dict[str, Any]):
        """
        Save voting record to disk.
        
        Args:
            voting_record: Complete voting record
        """
        decision_id = voting_record.get("decision_id", "unknown")
        timestamp = voting_record.get("timestamp", datetime.utcnow().isoformat())
        
        # Create filename from decision_id and timestamp
        safe_timestamp = timestamp.replace(":", "-").replace(".", "-")
        filename = f"{decision_id}_{safe_timestamp}.json"
        filepath = self.voting_records_path / filename
        
        # Save as JSON
        with open(filepath, 'w') as f:
            json.dump(voting_record, f, indent=2)
        
        # Set file permissions (0600 = owner read/write only)
        try:
            filepath.chmod(0o600)
        except (OSError, PermissionError):
            pass
    
    def get_voting_history(self, decision_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get voting history.
        
        Args:
            decision_id: Optional filter by decision ID
        
        Returns:
            List of voting records
        """
        records = []
        
        for filepath in self.voting_records_path.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    record = json.load(f)
                
                if decision_id is None or record.get("decision_id") == decision_id:
                    records.append(record)
            except (json.JSONDecodeError, IOError):
                # Skip corrupted files
                continue
        
        # Sort by timestamp (newest first)
        records.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return records
