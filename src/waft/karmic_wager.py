"""
Karmic Wager System - Betting with Karma

Enables WAFT to make karmic wagers on hypotheses, outcomes, and predictions.
This creates engagement through risk/reward mechanics using karma as currency.

Philosophy:
----------
"Put your karma where your hypothesis is."

WAFT can bet karma on:
- Hypothesis outcomes (Study Gym)
- Fitness predictions (evolutionary system)
- Research question answers (scientific papers)
- Component evolution success (document generation)
- Any testable claim

Winners gain karma. Losers lose karma. This creates engagement and accountability.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from enum import Enum
import json
import hashlib

from .karma import KarmaMerchant, InsufficientKarmaError


class WagerStatus(Enum):
    """Status of a karmic wager."""
    PENDING = "pending"  # Wager placed, outcome not yet determined
    WON = "won"  # Wager won, karma awarded
    LOST = "lost"  # Wager lost, karma deducted
    VOID = "void"  # Wager voided (invalid conditions, refunded)
    RESOLVED = "resolved"  # Outcome determined (won or lost)


class WagerType(Enum):
    """Type of karmic wager."""
    HYPOTHESIS = "hypothesis"  # Bet on hypothesis being confirmed/refuted
    FITNESS = "fitness"  # Bet on fitness score threshold
    STUDY_OUTCOME = "study_outcome"  # Bet on Study Gym session outcome
    COMPONENT_EVOLUTION = "component_evolution"  # Bet on component success
    RESEARCH_QUESTION = "research_question"  # Bet on research question answer
    CUSTOM = "custom"  # Custom wager with custom resolution


class KarmicWager:
    """
    A single karmic wager.
    
    Represents a bet placed by WAFT using karma as currency.
    """
    
    def __init__(
        self,
        wager_id: str,
        wager_type: WagerType,
        description: str,
        karma_amount: float,
        prediction: Any,
        resolution_criteria: Dict[str, Any],
        soul_id: str = "waft_system",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a karmic wager.
        
        Args:
            wager_id: Unique identifier for this wager
            wager_type: Type of wager
            description: Human-readable description of what's being wagered
            karma_amount: Amount of karma wagered
            prediction: What WAFT predicts will happen
            resolution_criteria: Criteria for determining win/loss
            soul_id: ID of soul making the wager (default: "waft_system")
            metadata: Additional metadata
        """
        self.wager_id = wager_id
        self.wager_type = wager_type
        self.description = description
        self.karma_amount = karma_amount
        self.prediction = prediction
        self.resolution_criteria = resolution_criteria
        self.soul_id = soul_id
        self.metadata = metadata or {}
        
        # Status tracking
        self.status = WagerStatus.PENDING
        self.created_at = datetime.now().isoformat()
        self.resolved_at: Optional[str] = None
        self.outcome: Optional[Any] = None
        self.karma_payout: float = 0.0  # Positive if won, negative if lost
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert wager to dictionary for storage."""
        return {
            "wager_id": self.wager_id,
            "wager_type": self.wager_type.value,
            "description": self.description,
            "karma_amount": self.karma_amount,
            "prediction": self.prediction,
            "resolution_criteria": self.resolution_criteria,
            "soul_id": self.soul_id,
            "metadata": self.metadata,
            "status": self.status.value,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "outcome": self.outcome,
            "karma_payout": self.karma_payout,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KarmicWager":
        """Create wager from dictionary."""
        wager = cls(
            wager_id=data["wager_id"],
            wager_type=WagerType(data["wager_type"]),
            description=data["description"],
            karma_amount=data["karma_amount"],
            prediction=data["prediction"],
            resolution_criteria=data["resolution_criteria"],
            soul_id=data.get("soul_id", "waft_system"),
            metadata=data.get("metadata", {})
        )
        wager.status = WagerStatus(data["status"])
        wager.created_at = data.get("created_at", datetime.now().isoformat())
        wager.resolved_at = data.get("resolved_at")
        wager.outcome = data.get("outcome")
        wager.karma_payout = data.get("karma_payout", 0.0)
        return wager


class KarmicWagerSystem:
    """
    System for managing karmic wagers.
    
    Enables WAFT to bet karma on hypotheses, outcomes, and predictions.
    Creates engagement through risk/reward mechanics.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        karma_merchant: Optional[KarmaMerchant] = None
    ):
        """
        Initialize the karmic wager system.
        
        Args:
            project_path: Path to project root
            karma_merchant: KarmaMerchant instance (creates new if not provided)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.wagers_dir = project_path / "_hidden" / ".truth" / "wagers"
        self.wagers_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize karma merchant
        self.karma_merchant = karma_merchant or KarmaMerchant(project_path)
        
        # Active wagers (in memory)
        self.active_wagers: Dict[str, KarmicWager] = {}
        self._load_active_wagers()
    
    def _load_active_wagers(self) -> None:
        """Load active (pending) wagers from disk."""
        wagers_file = self.wagers_dir / "active_wagers.json"
        if wagers_file.exists():
            try:
                data = json.loads(wagers_file.read_text())
                for wager_data in data.get("wagers", []):
                    if wager_data.get("status") == "pending":
                        wager = KarmicWager.from_dict(wager_data)
                        self.active_wagers[wager.wager_id] = wager
            except Exception:
                pass  # Start fresh if loading fails
    
    def _save_active_wagers(self) -> None:
        """Save active wagers to disk."""
        wagers_file = self.wagers_dir / "active_wagers.json"
        data = {
            "wagers": [wager.to_dict() for wager in self.active_wagers.values()],
            "updated_at": datetime.now().isoformat()
        }
        wagers_file.write_text(json.dumps(data, indent=2))
    
    def place_wager(
        self,
        wager_type: WagerType,
        description: str,
        karma_amount: float,
        prediction: Any,
        resolution_criteria: Dict[str, Any],
        soul_id: str = "waft_system",
        metadata: Optional[Dict[str, Any]] = None,
        odds: float = 1.0  # Payout multiplier (1.0 = even odds, 2.0 = double, etc.)
    ) -> KarmicWager:
        """
        Place a karmic wager.
        
        Args:
            wager_type: Type of wager
            description: What's being wagered on
            karma_amount: Amount of karma to wager
            prediction: What WAFT predicts
            resolution_criteria: How to determine win/loss
            soul_id: ID of soul making wager
            metadata: Additional metadata
            odds: Payout multiplier (default 1.0 = even odds)
            
        Returns:
            Created KarmicWager
            
        Raises:
            InsufficientKarmaError: If soul doesn't have enough karma
        """
        # Check karma balance
        current_karma = self._get_karma_balance(soul_id)
        if current_karma < karma_amount:
            raise InsufficientKarmaError(
                f"Insufficient karma: {current_karma} < {karma_amount}"
            )
        
        # Create wager ID
        wager_id = f"wager_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{description}{karma_amount}'.encode()).hexdigest()[:8]}"
        
        # Create wager
        wager = KarmicWager(
            wager_id=wager_id,
            wager_type=wager_type,
            description=description,
            karma_amount=karma_amount,
            prediction=prediction,
            resolution_criteria=resolution_criteria,
            soul_id=soul_id,
            metadata={**(metadata or {}), "odds": odds}
        )
        
        # Deduct karma (held in escrow until resolution)
        self._deduct_karma(soul_id, karma_amount, reason=f"Wager: {description}")
        
        # Store wager
        self.active_wagers[wager.wager_id] = wager
        self._save_active_wagers()
        
        # Save wager to history
        self._save_wager_to_history(wager)
        
        return wager
    
    def resolve_wager(
        self,
        wager_id: str,
        outcome: Any,
        resolver: Optional[Callable[[KarmicWager, Any], bool]] = None
    ) -> Dict[str, Any]:
        """
        Resolve a wager based on outcome.
        
        Args:
            wager_id: ID of wager to resolve
            outcome: The actual outcome
            resolver: Optional custom resolution function (wager, outcome) -> bool
            
        Returns:
            Dictionary with resolution details
        """
        if wager_id not in self.active_wagers:
            raise ValueError(f"Wager not found: {wager_id}")
        
        wager = self.active_wagers[wager_id]
        
        # Determine if wager won
        if resolver:
            won = resolver(wager, outcome)
        else:
            won = self._default_resolver(wager, outcome)
        
        # Calculate payout
        odds = wager.metadata.get("odds", 1.0)
        if won:
            payout = wager.karma_amount * odds  # Win: get back wager + winnings
            wager.status = WagerStatus.WON
            wager.karma_payout = payout
            self._award_karma(wager.soul_id, payout, reason=f"Won wager: {wager.description}")
        else:
            payout = -wager.karma_amount  # Lose: lose the wager
            wager.status = WagerStatus.LOST
            wager.karma_payout = payout
            # Karma already deducted, no refund
        
        # Update wager
        wager.outcome = outcome
        wager.resolved_at = datetime.now().isoformat()
        wager.status = WagerStatus.RESOLVED
        
        # Remove from active, save to history
        del self.active_wagers[wager_id]
        self._save_active_wagers()
        self._save_wager_to_history(wager)
        
        return {
            "wager_id": wager_id,
            "won": won,
            "karma_payout": payout,
            "outcome": outcome,
            "description": wager.description
        }
    
    def _default_resolver(self, wager: KarmicWager, outcome: Any) -> bool:
        """Default resolution logic based on wager type."""
        criteria = wager.resolution_criteria
        
        if wager.wager_type == WagerType.HYPOTHESIS:
            # Hypothesis wager: prediction should match outcome
            return wager.prediction == outcome.get("confirmed", False)
        
        elif wager.wager_type == WagerType.FITNESS:
            # Fitness wager: fitness should meet threshold
            threshold = criteria.get("threshold", 0.5)
            fitness = outcome.get("fitness", 0.0)
            direction = criteria.get("direction", "above")  # "above" or "below"
            
            if direction == "above":
                return fitness >= threshold
            else:
                return fitness <= threshold
        
        elif wager.wager_type == WagerType.STUDY_OUTCOME:
            # Study outcome: study should meet success criteria
            success_criteria = criteria.get("success_criteria", {})
            return self._check_study_success(outcome, success_criteria)
        
        elif wager.wager_type == WagerType.COMPONENT_EVOLUTION:
            # Component evolution: component should succeed
            return outcome.get("success", False)
        
        elif wager.wager_type == WagerType.RESEARCH_QUESTION:
            # Research question: answer should match prediction
            return wager.prediction == outcome.get("answer")
        
        else:
            # Custom: use custom criteria
            return criteria.get("check", lambda o: False)(outcome)
    
    def _check_study_success(self, outcome: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if study outcome meets success criteria."""
        # Default: study succeeded if it has findings and conclusions
        if "findings" in outcome and "conclusions" in outcome:
            findings = outcome.get("findings", [])
            conclusions = outcome.get("conclusions", [])
            
            min_findings = criteria.get("min_findings", 1)
            min_conclusions = criteria.get("min_conclusions", 1)
            
            return len(findings) >= min_findings and len(conclusions) >= min_conclusions
        
        return False
    
    def get_active_wagers(self, soul_id: Optional[str] = None) -> List[KarmicWager]:
        """Get all active (pending) wagers."""
        wagers = list(self.active_wagers.values())
        if soul_id:
            wagers = [w for w in wagers if w.soul_id == soul_id]
        return wagers
    
    def get_wager_history(
        self,
        soul_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get wager history."""
        history_file = self.wagers_dir / "wager_history.jsonl"
        if not history_file.exists():
            return []
        
        history = []
        with open(history_file, "r") as f:
            for line in f:
                if line.strip():
                    wager_data = json.loads(line)
                    if soul_id is None or wager_data.get("soul_id") == soul_id:
                        history.append(wager_data)
        
        # Return most recent first
        return list(reversed(history[-limit:]))
    
    def get_wager_stats(self, soul_id: str = "waft_system") -> Dict[str, Any]:
        """Get statistics about wagers."""
        history = self.get_wager_history(soul_id=soul_id)
        active = self.get_active_wagers(soul_id=soul_id)
        
        total_wagered = sum(w.karma_amount for w in active)
        total_won = sum(w["karma_payout"] for w in history if w.get("status") == "won")
        total_lost = sum(abs(w["karma_payout"]) for w in history if w.get("status") == "lost")
        
        won_count = sum(1 for w in history if w.get("status") == "won")
        lost_count = sum(1 for w in history if w.get("status") == "lost")
        
        win_rate = won_count / (won_count + lost_count) if (won_count + lost_count) > 0 else 0.0
        
        return {
            "total_wagered": total_wagered,
            "total_won": total_won,
            "total_lost": total_lost,
            "net_karma": total_won - total_lost,
            "won_count": won_count,
            "lost_count": lost_count,
            "win_rate": win_rate,
            "active_wagers": len(active),
            "total_wagers": len(history)
        }
    
    def _get_karma_balance(self, soul_id: str) -> float:
        """Get current karma balance for a soul."""
        try:
            balance = self.karma_merchant.get_soul_karma(soul_id)
            if balance is None:
                return 1000.0  # Default starting karma
            return float(balance)
        except Exception:
            # If karma system not fully implemented, use default
            return 1000.0  # Default starting karma
    
    def _deduct_karma(self, soul_id: str, amount: float, reason: str = "") -> None:
        """Deduct karma (held in escrow for wager)."""
        # TODO: Implement actual karma deduction
        # For now, just track in wager metadata
        pass
    
    def _award_karma(self, soul_id: str, amount: float, reason: str = "") -> None:
        """Award karma (wager winnings)."""
        # TODO: Implement actual karma award
        # For now, just track in wager metadata
        pass
    
    def _save_wager_to_history(self, wager: KarmicWager) -> None:
        """Save wager to history file."""
        history_file = self.wagers_dir / "wager_history.jsonl"
        with open(history_file, "a") as f:
            f.write(json.dumps(wager.to_dict()) + "\n")


# Convenience functions for common wager types

def wager_on_hypothesis(
    wager_system: KarmicWagerSystem,
    hypothesis: str,
    karma_amount: float,
    prediction: bool,  # True = hypothesis will be confirmed
    study_session_id: Optional[str] = None,
    odds: float = 1.0
) -> KarmicWager:
    """
    Place a wager on a hypothesis being confirmed or refuted.
    
    Args:
        wager_system: KarmicWagerSystem instance
        hypothesis: The hypothesis being tested
        karma_amount: Karma to wager
        prediction: True if predicting confirmation, False if refutation
        study_session_id: Optional Study Gym session ID
        odds: Payout multiplier
        
    Returns:
        Created wager
    """
    return wager_system.place_wager(
        wager_type=WagerType.HYPOTHESIS,
        description=f"Hypothesis: {hypothesis}",
        karma_amount=karma_amount,
        prediction=prediction,
        resolution_criteria={
            "hypothesis": hypothesis,
            "study_session_id": study_session_id
        },
        metadata={"study_session_id": study_session_id},
        odds=odds
    )


def wager_on_fitness(
    wager_system: KarmicWagerSystem,
    description: str,
    karma_amount: float,
    threshold: float,
    direction: str = "above",  # "above" or "below"
    odds: float = 1.0
) -> KarmicWager:
    """
    Place a wager on fitness score.
    
    Args:
        wager_system: KarmicWagerSystem instance
        description: What fitness is being measured
        karma_amount: Karma to wager
        threshold: Fitness threshold
        direction: "above" (fitness >= threshold) or "below" (fitness <= threshold)
        odds: Payout multiplier
        
    Returns:
        Created wager
    """
    return wager_system.place_wager(
        wager_type=WagerType.FITNESS,
        description=f"Fitness {direction} {threshold}: {description}",
        karma_amount=karma_amount,
        prediction={"threshold": threshold, "direction": direction},
        resolution_criteria={
            "threshold": threshold,
            "direction": direction
        },
        odds=odds
    )


def wager_on_study_outcome(
    wager_system: KarmicWagerSystem,
    study_description: str,
    karma_amount: float,
    success_criteria: Dict[str, Any],
    odds: float = 1.0
) -> KarmicWager:
    """
    Place a wager on Study Gym session outcome.
    
    Args:
        wager_system: KarmicWagerSystem instance
        study_description: Description of study
        karma_amount: Karma to wager
        success_criteria: Criteria for study success
        odds: Payout multiplier
        
    Returns:
        Created wager
    """
    return wager_system.place_wager(
        wager_type=WagerType.STUDY_OUTCOME,
        description=f"Study success: {study_description}",
        karma_amount=karma_amount,
        prediction=True,  # Predicting success
        resolution_criteria={"success_criteria": success_criteria},
        metadata={"study_description": study_description},
        odds=odds
    )
