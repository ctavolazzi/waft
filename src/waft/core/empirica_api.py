"""
Empirica Python API Integration

Direct programmatic access to Empirica core modules.
Uses Python API when available, falls back to CLI.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json

# Try to import Empirica Python API
try:
    from empirica import SessionDatabase, EpistemicAssessor, ProjectManager
    from empirica import GitEnhancedReflexLogger, HandoffGenerator
    EMPIRICA_API_AVAILABLE = True
except ImportError:
    EMPIRICA_API_AVAILABLE = False
    SessionDatabase = None
    EpistemicAssessor = None
    ProjectManager = None
    GitEnhancedReflexLogger = None
    HandoffGenerator = None


class EmpiricaAPIManager:
    """
    Direct Python API access to Empirica.
    
    Provides typed, robust access to:
    - SessionDatabase (session management)
    - EpistemicAssessor (13-vector assessment)
    - ProjectManager (multi-session tracking)
    - GitEnhancedReflexLogger (atomic logging)
    - HandoffGenerator (AI-to-AI continuity)
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize Empirica API manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self._api_available = EMPIRICA_API_AVAILABLE
        
        if self._api_available:
            try:
                # Initialize SessionDatabase
                self.db = SessionDatabase()
                
                # Initialize EpistemicAssessor for 13-vector assessments
                self.assessor = EpistemicAssessor()
                
                # Initialize ProjectManager for project tracking
                self.project_manager = ProjectManager()
                
                # Initialize GitEnhancedReflexLogger for atomic logging
                self.logger = GitEnhancedReflexLogger(project_path=self.project_path)
                
                # Initialize HandoffGenerator for AI-to-AI continuity
                self.handoff = HandoffGenerator()
                
            except Exception as e:
                # API available but initialization failed
                self._api_available = False
                self._init_error = str(e)
        else:
            self.db = None
            self.assessor = None
            self.project_manager = None
            self.logger = None
            self.handoff = None
    
    @property
    def is_available(self) -> bool:
        """Check if Python API is available."""
        return self._api_available
    
    def create_session(
        self, 
        ai_id: str = "waft", 
        session_type: str = "development",
        bootstrap_level: int = 2
    ) -> Optional[str]:
        """
        Create a new session using Python API.
        
        Args:
            ai_id: Unique identifier for agent
            session_type: Type of session
            bootstrap_level: Initial context depth (0-4)
        
        Returns:
            Session ID if successful, None otherwise
        """
        if not self._api_available or not self.db:
            return None
        
        try:
            session_id = self.db.create_session(
                ai_id=ai_id,
                bootstrap_level=bootstrap_level,
                subject=session_type
            )
            return session_id
        except Exception:
            return None
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data.
        
        Args:
            session_id: Session ID
        
        Returns:
            Session data dict or None
        """
        if not self._api_available or not self.db:
            return None
        
        try:
            return self.db.get_session(session_id)
        except Exception:
            return None
    
    def assess_vectors(
        self,
        session_id: str,
        vectors: Dict[str, Any],
        reasoning: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Perform 13-vector epistemic assessment.
        
        Args:
            session_id: Session ID
            vectors: Epistemic vectors dict
            reasoning: Optional reasoning text
        
        Returns:
            Assessment result or None
        """
        if not self._api_available or not self.assessor:
            return None
        
        try:
            assessment = self.assessor.assess_vectors(
                session_id=session_id,
                vectors=vectors,
                reasoning=reasoning
            )
            return assessment
        except Exception:
            return None
    
    def update_beliefs(
        self,
        session_id: str,
        evidence: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update Bayesian beliefs for epistemic vectors.
        
        Args:
            session_id: Session ID
            evidence: Evidence dict
        
        Returns:
            Updated beliefs or None
        """
        if not self._api_available or not self.assessor:
            return None
        
        try:
            # EpistemicAssessor has update_beliefs method
            updated = self.assessor.update_beliefs(
                session_id=session_id,
                evidence=evidence
            )
            return updated
        except Exception:
            return None
    
    def log_checkpoint(
        self,
        session_id: str,
        phase: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Log checkpoint using GitEnhancedReflexLogger.
        
        Performs atomic triple-write:
        - SQLite (.empirica/sessions/sessions.db)
        - Git Notes (git notes add -m compressed_json)
        - JSON Logs (.empirica/reflexes/*.json)
        
        Args:
            session_id: Session ID
            phase: CASCADE phase (PREFLIGHT, INVESTIGATE, CHECK, ACT, POSTFLIGHT)
            data: Checkpoint data
        
        Returns:
            True if successful
        """
        if not self._api_available or not self.logger:
            return False
        
        try:
            # GitEnhancedReflexLogger handles atomic triple-write automatically
            self.logger.add_checkpoint(
                session_id=session_id,
                phase=phase,
                data=data
            )
            # All three layers written atomically:
            # 1. SQLite (fast queries)
            # 2. Git Notes (compressed, distributed)
            # 3. JSON (full audit trail)
            return True
        except Exception:
            return False
    
    def create_handoff(
        self,
        session_id: str,
        target_ai_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create handoff for AI-to-AI continuity.
        
        Args:
            session_id: Source session ID
            target_ai_id: Optional target AI ID
        
        Returns:
            Handoff data or None
        """
        if not self._api_available or not self.handoff:
            return None
        
        try:
            handoff_data = self.handoff.create_handoff(
                session_id=session_id,
                target_ai_id=target_ai_id
            )
            return handoff_data
        except Exception:
            return None
    
    def load_handoff(
        self,
        handoff_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Load handoff data.
        
        Args:
            handoff_data: Handoff data dict
        
        Returns:
            Loaded context or None
        """
        if not self._api_available or not self.handoff:
            return None
        
        try:
            context = self.handoff.load_handoff(handoff_data)
            return context
        except Exception:
            return None
    
    def bootstrap_project_breadcrumbs(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Generate epistemic breadcrumbs for session.
        
        Finds:
        - Findings (validated knowledge)
        - Unknowns (gaps triggering investigation)
        - Dead Ends (failed approaches)
        
        Args:
            session_id: Session ID
        
        Returns:
            Breadcrumbs dict or None
        """
        if not self._api_available or not self.db:
            return None
        
        try:
            breadcrumbs = self.db.bootstrap_project_breadcrumbs(session_id)
            return breadcrumbs
        except Exception:
            return None
    
    def get_project_summary(self, project_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get project summary with goal aggregation.
        
        Args:
            project_id: Optional project ID
        
        Returns:
            Project summary or None
        """
        if not self._api_available or not self.project_manager:
            return None
        
        try:
            if project_id:
                summary = self.project_manager.get_project_summary(project_id)
            else:
                # Try to discover project ID from git remote
                summary = self.project_manager.get_project_summary()
            return summary
        except Exception:
            return None
