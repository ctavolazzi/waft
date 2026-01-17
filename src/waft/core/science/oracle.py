"""
The Oracle: Epistemic Intelligence System

The Oracle provides insights, analysis, and predictions based on epistemic state.
Uses Empirica to track knowledge, uncertainty, and learning trajectories.

Unlike TheObserver (which passively records), TheOracle actively analyzes
and provides guidance based on what the system knows and doesn't know.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..empirica import EmpiricaManager


class TheOracle:
    """
    Epistemic intelligence system that provides insights and guidance.
    
    Uses Empirica to:
    - Track epistemic state (what we know, what we don't know)
    - Log findings and unknowns
    - Provide insights based on knowledge gaps
    - Guide decision-making with epistemic context
    - Project learning trajectories
    """
    
    def __init__(self, project_path: Path, empirica_manager: Optional[EmpiricaManager] = None):
        """
        Initialize TheOracle.
        
        Args:
            project_path: Path to project root
            empirica_manager: Optional EmpiricaManager (creates if None)
        """
        self.project_path = Path(project_path)
        
        # Initialize Empirica (required for TheOracle)
        if empirica_manager is None:
            self.empirica = EmpiricaManager(self.project_path)
        else:
            self.empirica = empirica_manager
        
        # Verify Empirica is initialized
        if not self.empirica.is_initialized():
            raise RuntimeError(
                "TheOracle requires Empirica to be initialized. "
                "Run 'waft init' or initialize Empirica first."
            )
    
    def get_epistemic_state(self) -> Dict[str, Any]:
        """
        Get current epistemic state from Empirica.
        
        Returns:
            Dictionary with epistemic state (vectors, findings, unknowns, goals)
        """
        context = self.empirica.project_bootstrap()
        if not context:
            return {
                "initialized": False,
                "message": "Empirica not initialized or no context available"
            }
        
        return {
            "initialized": True,
            "epistemic_state": context.get("epistemic_state", {}),
            "findings": context.get("findings", []),
            "unknowns": context.get("unknowns", []),
            "goals": context.get("goals", []),
            "timestamp": datetime.now().isoformat()
        }
    
    def log_insight(self, insight: str, impact: float = 0.5) -> bool:
        """
        Log an insight as a finding to Empirica.
        
        Args:
            insight: Description of the insight
            impact: Impact score (0.0-1.0)
        
        Returns:
            True if logged successfully
        """
        return self.empirica.log_finding(insight, impact=impact)
    
    def log_unknown(self, unknown: str) -> bool:
        """
        Log a knowledge gap to Empirica.
        
        Args:
            unknown: Description of what needs investigation
        
        Returns:
            True if logged successfully
        """
        return self.empirica.log_unknown(unknown)
    
    def check_gate(self, operation: Dict[str, Any]) -> Optional[str]:
        """
        Check if operation is safe to proceed using Empirica CHECK gate.
        
        Args:
            operation: Operation description dict
        
        Returns:
            Gate result: PROCEED | HALT | BRANCH | REVISE | None if failed
        """
        return self.empirica.check_submit(operation)
    
    def get_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent insights (findings) from epistemic state.
        
        Args:
            limit: Maximum number of insights to return
        
        Returns:
            List of insight dictionaries
        """
        context = self.empirica.project_bootstrap()
        if not context:
            return []
        
        findings = context.get("findings", [])
        if isinstance(findings, list):
            return findings[-limit:] if len(findings) > limit else findings
        return []
    
    def get_unknowns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent unknowns (knowledge gaps) from epistemic state.
        
        Args:
            limit: Maximum number of unknowns to return
        
        Returns:
            List of unknown dictionaries
        """
        context = self.empirica.project_bootstrap()
        if not context:
            return []
        
        unknowns = context.get("unknowns", [])
        if isinstance(unknowns, list):
            return unknowns[-limit:] if len(unknowns) > limit else unknowns
        return []
    
    def get_epistemic_phase(self) -> str:
        """
        Calculate current epistemic phase from state.
        
        Returns:
            Phase name: Data Gathering | Exploration | Synthesis | Evolution | Transition | UNKNOWN
        """
        context = self.empirica.project_bootstrap()
        if not context:
            return "UNKNOWN"
        
        epistemic_state = context.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        if not vectors:
            return "UNKNOWN"
        
        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)
        
        # Validate ranges
        know = max(0.0, min(1.0, know))
        uncertainty = max(0.0, min(1.0, uncertainty))
        
        # Determine phase
        if know < 0.3 and uncertainty > 0.5:
            return "Data Gathering"
        elif know < 0.6 and uncertainty > 0.3:
            return "Exploration"
        elif know > 0.6 and uncertainty < 0.3:
            return "Synthesis"
        elif know > 0.8 and uncertainty < 0.2:
            return "Evolution"
        else:
            return "Transition"
    
    def provide_guidance(self, question: str) -> Dict[str, Any]:
        """
        Provide guidance based on epistemic state.
        
        Args:
            question: Question or context for guidance
        
        Returns:
            Dictionary with guidance, insights, and recommendations
        """
        state = self.get_epistemic_state()
        phase = self.get_epistemic_phase()
        
        # Get relevant findings and unknowns
        findings = self.get_insights(limit=5)
        unknowns = self.get_unknowns(limit=5)
        
        # Calculate knowledge coverage
        epistemic_state = state.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)
        coverage = know * (1.0 - uncertainty) if know > 0 else 0.0
        
        # Log consultation to Empirica (track Oracle usage)
        try:
            self.log_insight(f"Oracle consultation: {question[:100]}", impact=0.3)
        except Exception:
            pass  # Continue even if logging fails
        
        return {
            "question": question,
            "epistemic_phase": phase,
            "knowledge_coverage": coverage,
            "know": know,
            "uncertainty": uncertainty,
            "findings": findings,
            "unknowns": unknowns,
            "recommendation": self._generate_recommendation(phase, coverage, unknowns),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_recommendation(
        self, 
        phase: str, 
        coverage: float, 
        unknowns: List[Dict[str, Any]]
    ) -> str:
        """Generate recommendation based on epistemic state."""
        if phase == "Data Gathering":
            return "Focus on collecting data and observations. High uncertainty suggests need for more information."
        elif phase == "Exploration":
            return "Explore different approaches. Moderate knowledge with uncertainty suggests experimentation."
        elif phase == "Synthesis":
            return "Synthesize findings. High knowledge with low uncertainty suggests patterns can be identified."
        elif phase == "Evolution":
            return "Ready for evolution. Very high knowledge with very low uncertainty suggests system can advance."
        elif coverage < 0.3:
            return f"Low knowledge coverage ({coverage:.0%}). Focus on addressing unknowns: {len(unknowns)} open questions."
        else:
            return f"Knowledge coverage: {coverage:.0%}. Continue building on existing knowledge."
    
    def assess_decision(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess a decision using epistemic state and CHECK gate.
        
        Args:
            decision_context: Context about the decision to make
        
        Returns:
            Dictionary with assessment, gate result, and recommendations
        """
        # Check gate
        gate_result = self.check_gate({
            "type": "decision",
            "scope": decision_context.get("scope", "medium"),
            "description": decision_context.get("description", "Decision assessment"),
            **decision_context
        })
        
        # Get epistemic state
        state = self.get_epistemic_state()
        phase = self.get_epistemic_phase()
        
        # Get relevant unknowns
        unknowns = self.get_unknowns(limit=3)
        
        # Log decision assessment to Empirica
        try:
            decision_desc = decision_context.get("description", "Decision assessment")
            if gate_result == "PROCEED":
                self.log_insight(f"Decision approved: {decision_desc[:100]}", impact=0.5)
            elif gate_result == "HALT":
                self.log_insight(f"Decision halted: {decision_desc[:100]} - requires human approval", impact=0.8)
            elif gate_result == "BRANCH":
                self.log_unknown(f"Decision needs investigation: {decision_desc[:100]}")
            elif gate_result == "REVISE":
                self.log_insight(f"Decision needs revision: {decision_desc[:100]}", impact=0.6)
        except Exception:
            pass  # Continue even if logging fails
        
        return {
            "gate_result": gate_result,
            "epistemic_phase": phase,
            "state": state,
            "unknowns": unknowns,
            "recommendation": self._get_gate_recommendation(gate_result, unknowns),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_gate_recommendation(self, gate_result: Optional[str], unknowns: List[Dict[str, Any]]) -> str:
        """Get recommendation based on gate result."""
        if gate_result == "PROCEED":
            return "Safe to proceed. Epistemic state supports this operation."
        elif gate_result == "HALT":
            return "Operation requires human approval. High risk or insufficient knowledge."
        elif gate_result == "BRANCH":
            return f"Need investigation first. {len(unknowns)} relevant unknowns should be addressed."
        elif gate_result == "REVISE":
            return "Approach needs revision. Consider alternative methods based on epistemic state."
        else:
            return "Gate check failed. Proceed with caution."
