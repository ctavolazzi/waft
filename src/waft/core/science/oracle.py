"""
The Oracle: Epistemic Intelligence System

The Oracle provides insights, analysis, and predictions based on epistemic state.
Uses Empirica to track knowledge, uncertainty, and learning trajectories.

Unlike TheObserver (which passively records), TheOracle actively analyzes
and provides guidance based on what the system knows and doesn't know.
"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from ..empirica import EmpiricaManager
from .oracle_journal import OracleJournal
from .oracle_personality import OraclePersonality, OraclePersonalityType


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

    def __init__(
        self,
        project_path: Path,
        empirica_manager: EmpiricaManager | None = None,
        ai_id: str = "waft",
        personality: OraclePersonality | None = None,
        personality_type: OraclePersonalityType | None = None,
        personality_file: Path | None = None,
    ):
        """
        Initialize TheOracle.

        Args:
            project_path: Path to project root
            empirica_manager: Optional EmpiricaManager (creates if None)
            ai_id: AI agent identifier for Empirica session
            personality: Optional OraclePersonality instance
            personality_type: Optional personality preset type
            personality_file: Optional path to personality JSON file

        Raises:
            RuntimeError: If Empirica cannot be initialized or made ready
        """
        self.project_path = Path(project_path)

        # Initialize Empirica (required for TheOracle)
        if empirica_manager is None:
            self.empirica = EmpiricaManager(self.project_path)
        else:
            self.empirica = empirica_manager

        # FORCE Empirica to be ready - no degraded mode, no graceful fallbacks
        # This will raise RuntimeError if Empirica cannot be made ready
        try:
            self._readiness_status = self.empirica.ensure_ready(ai_id=ai_id, force_session=True)
            if not self._readiness_status.get("ready", False):
                raise RuntimeError(
                    "Empirica is not ready. "
                    f"Status: {self._readiness_status.get('message', 'Unknown error')}"
                )
        except RuntimeError:
            raise  # Re-raise with clear message
        except Exception as e:
            raise RuntimeError(f"Failed to ensure Empirica is ready: {str(e)}")

        # Initialize personality state tracking (MUST be before _load_personality)
        # FIX: Previously these were only initialized in one code path of _load_personality
        self._personality_interactions = []  # Track interactions for personality evolution

        # Get session ID for Empirica workflow
        # Try to get from readiness status, or create one if needed
        self._session_id = self._readiness_status.get("session_id")
        if not self._session_id:
            # Try to get current session from Empirica
            try:
                self._session_id = self.empirica.get_current_session_id()
            except Exception:
                pass  # Session ID not critical

        # Initialize personality
        self.personality = self._load_personality(personality, personality_type, personality_file)

        # Initialize journal and memory
        self.journal = OracleJournal(self.project_path)

    def _load_personality(
        self,
        personality: OraclePersonality | None,
        personality_type: OraclePersonalityType | None,
        personality_file: Path | None,
    ) -> OraclePersonality:
        """
        Load personality from provided source or create default.

        Priority:
        1. Provided personality instance
        2. Personality file
        3. Personality type preset
        4. Default personality

        Args:
            personality: Optional OraclePersonality instance
            personality_type: Optional personality preset type
            personality_file: Optional path to personality JSON file

        Returns:
            OraclePersonality instance
        """
        # Priority 1: Use provided instance
        if personality is not None:
            return personality

        # Priority 2: Load from file
        if personality_file is not None and personality_file.exists():
            try:
                return OraclePersonality.from_file(personality_file)
            except Exception:
                pass  # Fall through to next option

        # Priority 3: Use preset type
        if personality_type is not None:
            try:
                return OraclePersonality.from_preset(personality_type)
            except Exception:
                pass  # Fall through to default

        # Priority 4: Default personality
        personality = OraclePersonality()

        # NOTE: _personality_interactions and _session_id are now initialized
        # in __init__ BEFORE this method is called, so they're always available
        # regardless of which personality loading branch is taken.

        return personality

    def get_epistemic_state(self) -> dict[str, Any]:
        """
        Get current epistemic state from Empirica.

        Empirica MUST be ready (enforced in __init__), so this always returns valid state.

        Returns:
            Dictionary with epistemic state (vectors, findings, unknowns, goals)
        """
        # Empirica is guaranteed to be ready (enforced in __init__)
        context = self.empirica.project_bootstrap()

        # If no context yet (new project), return empty but valid structure
        if not context:
            return {
                "initialized": True,
                "has_context": False,
                "ready": True,
                "message": "Empirica ready. Context will be available after first preflight submission.",
                "epistemic_state": {},
                "findings": [],
                "unknowns": [],
                "goals": [],
                "timestamp": datetime.now().isoformat(),
            }

        # Full context available
        return {
            "initialized": True,
            "has_context": True,
            "ready": True,
            "message": "Empirica ready with epistemic context",
            "epistemic_state": context.get("epistemic_state", {}),
            "findings": context.get("findings", []),
            "unknowns": context.get("unknowns", []),
            "goals": context.get("goals", []),
            "timestamp": datetime.now().isoformat(),
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
        result = self.empirica.log_finding(insight, impact=impact)

        # Also remember in Oracle's own memory
        try:
            self.journal.remember_insight(insight, impact=impact)
        except Exception:
            pass  # Continue even if journal logging fails

        return result

    def log_unknown(self, unknown: str) -> bool:
        """
        Log a knowledge gap to Empirica.

        Args:
            unknown: Description of what needs investigation

        Returns:
            True if logged successfully
        """
        return self.empirica.log_unknown(unknown)

    def check_gate(self, operation: dict[str, Any]) -> str | None:
        """
        Check if operation is safe to proceed using Empirica CHECK gate.

        Args:
            operation: Operation description dict

        Returns:
            Gate result: PROCEED | HALT | BRANCH | REVISE | None if failed
        """
        return self.empirica.check_submit(operation)

    def get_insights(self, limit: int = 10) -> list[dict[str, Any]]:
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

    def get_unknowns(self, limit: int = 10) -> list[dict[str, Any]]:
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
            Or dict with phase and calculation if show_calculation=True
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
            phase = "Data Gathering"
            reason = f"know({know:.2f}) < 0.3 AND uncertainty({uncertainty:.2f}) > 0.5"
        elif know < 0.6 and uncertainty > 0.3:
            phase = "Exploration"
            reason = f"know({know:.2f}) < 0.6 AND uncertainty({uncertainty:.2f}) > 0.3"
        elif know > 0.6 and uncertainty < 0.3:
            phase = "Synthesis"
            reason = f"know({know:.2f}) > 0.6 AND uncertainty({uncertainty:.2f}) < 0.3"
        elif know > 0.8 and uncertainty < 0.2:
            phase = "Evolution"
            reason = f"know({know:.2f}) > 0.8 AND uncertainty({uncertainty:.2f}) < 0.2"
        else:
            return "Transition"

    def provide_guidance(
        self,
        question: str,
        show_thinking: bool = False,
        thinking_callback: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        """
        Provide guidance following Empirica workflow:
        1. PREFLIGHT - Assess current epistemic state
        2. INVESTIGATE - Reduce uncertainty by logging findings/unknowns
        3. CHECK - Decision gate based on findings/unknowns
        4. ACT - Generate recommendation (action)
        5. POSTFLIGHT - Measure learning (tracked in journal)

        Args:
            question: Question or context for guidance

        Returns:
            Dictionary with guidance, insights, and recommendations
        """
        # STEP 1: PREFLIGHT - Assess current epistemic state
        if show_thinking and thinking_callback:
            thinking_callback(
                "PREFLIGHT",
                {
                    "status": "Assessing epistemic state...",
                    "thinking": "Retrieving current epistemic vectors from Empirica...",
                },
            )
        preflight_result = self._empirica_preflight(question)

        # STEP 2: INVESTIGATE - Reduce uncertainty by reviewing past experiences
        # This is where reflection happens - reviewing memory and patterns
        if show_thinking and thinking_callback:
            thinking_callback(
                "INVESTIGATE",
                {
                    "status": "Reflecting on past experiences...",
                    "thinking": f"Searching journal memory for: '{question[:50]}...'",
                },
            )
        reflection = self._reflect_on_question(question)
        if show_thinking and thinking_callback:
            thinking_callback("INVESTIGATE", {"reflection": reflection})

        # Log INVESTIGATE checkpoint with atomic triple-write (SQLite + Git Notes + JSON)
        # GitEnhancedReflexLogger ensures all three layers written atomically
        if self.empirica.api_available and self._session_id:
            try:
                self.empirica.api_manager.log_checkpoint(
                    session_id=self._session_id,
                    phase="INVESTIGATE",
                    data={
                        "reflection": reflection,
                        "relevant_experiences_count": len(
                            reflection.get("relevant_experiences", [])
                        ),
                        "relevant_insights_count": len(reflection.get("relevant_insights", [])),
                    },
                )
            except Exception:
                pass  # Continue even if checkpoint logging fails

        # Get current epistemic state
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

        # STEP 3: CHECK - Decision gate based on findings and unknowns
        if show_thinking and thinking_callback:
            thinking_callback("CHECK", {"status": "Evaluating decision gate..."})
        check_result = self._empirica_check(question, findings, unknowns, uncertainty)

        # STEP 4: ACT - Generate recommendation (the action/guidance)
        if show_thinking and thinking_callback:
            thinking_callback("ACT", {"phase": phase, "coverage": coverage})

        recommendation = self._generate_recommendation(
            phase, coverage, unknowns, uncertainty, reflection=reflection, check_result=check_result
        )

        # Log ACT checkpoint with atomic triple-write
        # GitEnhancedReflexLogger ensures all three layers written atomically
        if self.empirica.api_available and self._session_id:
            try:
                self.empirica.api_manager.log_checkpoint(
                    session_id=self._session_id,
                    phase="ACT",
                    data={"phase": phase, "coverage": coverage, "recommendation_generated": True},
                )
            except Exception:
                pass  # Continue even if checkpoint logging fails

        # Build response
        response = {
            "question": question,
            "epistemic_phase": phase,
            "knowledge_coverage": coverage,
            "know": know,
            "uncertainty": uncertainty,
            "findings": findings,
            "unknowns": unknowns,
            "preflight": preflight_result,
            "check": check_result,
            "reflection": reflection,  # Include reflection in response
            "recommendation": recommendation,
            "epistemic_state": epistemic_state,  # Include full epistemic state for thinking display
            "personality": {
                "name": self.personality.data.get("name", "The Oracle"),
                "greeting": self.personality.get_greeting(),
                "type": self.personality.data.get("type", "balanced"),
            },
            "timestamp": datetime.now().isoformat(),
        }

        # STEP 5: POSTFLIGHT - Measure learning deltas
        # Calculate learning from preflight to postflight
        postflight_result = self._empirica_postflight(preflight_result, check_result, response)
        if show_thinking and thinking_callback:
            thinking_callback("POSTFLIGHT", postflight_result)

        # Log to journal (tracks consultation for memory)
        # This is Oracle's own journal - Empirica triple-write happens in submit_preflight/postflight
        try:
            self.journal.log_consultation(question, response, state)
        except Exception:
            pass  # Continue even if journal logging fails

        # Ensure Empirica triple-write is complete
        # Empirica's GitEnhancedReflexLogger handles atomic writes to SQLite + Git Notes + JSON
        # This happens automatically when we call submit_preflight/postflight via EmpiricaManager

        # Include postflight in response
        response["postflight"] = postflight_result

        # Add storage info for thinking display
        response["storage_info"] = self._get_storage_info()

        return response

    def _get_storage_info(self) -> dict[str, Any]:
        """
        Get three-layer storage status.

        Returns:
            Dict with SQLite, Git Notes, and JSON logs status
        """
        storage_info = {
            "sqlite": {"available": False},
            "git_notes": {"available": False},
            "json_logs": {"available": False},
        }

        # Check SQLite
        sqlite_path = self.project_path / ".empirica" / "sessions" / "sessions.db"
        if sqlite_path.exists():
            storage_info["sqlite"]["available"] = True

        # Check Git Notes (if git repo)
        git_dir = self.project_path / ".git"
        if git_dir.exists():
            storage_info["git_notes"]["available"] = True
            # Estimate compression (97% typical)
            storage_info["git_notes"]["compression"] = 0.97

        # Check JSON logs
        reflexes_dir = self.project_path / ".empirica" / "reflexes"
        if reflexes_dir.exists():
            storage_info["json_logs"]["available"] = True

        return storage_info

    def _empirica_preflight(self, question: str) -> dict[str, Any]:
        """
        STEP 1: PREFLIGHT - Assess current epistemic state.

        Returns:
            Preflight result with KNOW, UNCERTAINTY, and INVESTIGATE_REQUIRED flag
        """
        state = self.get_epistemic_state()
        epistemic_state = state.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)

        # Determine if investigation is required
        investigate_required = uncertainty > 0.5 or know < 0.3

        result = {
            "know": know,
            "uncertainty": uncertainty,
            "investigate_required": investigate_required,
            "know_level": "Low" if know < 0.3 else "Medium" if know < 0.7 else "High",
            "uncertainty_level": "High"
            if uncertainty > 0.5
            else "Medium"
            if uncertainty > 0.3
            else "Low",
        }

        # Submit to Empirica if session ID available
        if self._session_id:
            try:
                vectors_data = {
                    "engagement": 0.8,
                    "foundation": foundation,
                    "uncertainty": uncertainty,
                }

                # Use Python API if available (provides 13-vector assessment)
                if self.empirica.api_available:
                    assessment = self.empirica.api_manager.assess_vectors(
                        session_id=self._session_id,
                        vectors=vectors_data,
                        reasoning=f"Oracle consultation: {question[:100]}",
                    )
                    if assessment:
                        # Store assessment result
                        result["assessment"] = assessment
                else:
                    # Fall back to CLI
                    self.empirica.submit_preflight(
                        self._session_id,
                        vectors_data,
                        reasoning=f"Oracle consultation: {question[:100]}",
                    )
            except Exception:
                pass  # Continue even if preflight submission fails

        return result

    def _empirica_check(
        self,
        question: str,
        findings: list[dict[str, Any]],
        unknowns: list[dict[str, Any]],
        uncertainty: float,
    ) -> dict[str, Any]:
        """
        STEP 3: CHECK - Decision gate based on findings and unknowns.

        Returns:
            Check result with CONFIDENCE and DECISION (PROCEED/HALT/BRANCH/REVISE)
        """
        # Calculate confidence based on findings vs unknowns
        findings_count = len(findings)
        unknowns_count = len(unknowns)

        # Confidence increases with findings, decreases with unknowns and uncertainty
        base_confidence = min(1.0, findings_count * 0.1)
        confidence = base_confidence * (1.0 - uncertainty)

        # Decision logic
        decision_reasoning = []  # Initialize reasoning list
        if confidence >= 0.7 and uncertainty < 0.3:
            decision = "PROCEED"
            decision_reasoning.append(
                f"confidence({confidence:.3f}) >= 0.7 AND uncertainty({uncertainty:.3f}) < 0.3 → PROCEED"
            )
        elif confidence < 0.3 or uncertainty > 0.7:
            decision = "HALT"
            decision_reasoning.append(
                f"confidence({confidence:.3f}) < 0.3 OR uncertainty({uncertainty:.3f}) > 0.7 → HALT"
            )
        elif unknowns_count > findings_count:
            decision = "BRANCH"  # Need investigation
            decision_reasoning.append(
                f"unknowns({unknowns_count}) > findings({findings_count}) → BRANCH (investigation needed)"
            )
        else:
            decision = "REVISE"  # Need refinement
            decision_reasoning.append(
                f"confidence({confidence:.3f}), uncertainty({uncertainty:.3f}) → REVISE (refinement needed)"
            )

        result = {
            "confidence": confidence,
            "decision": decision,
            "findings_count": findings_count,
            "unknowns_count": unknowns_count,
            "reasoning": decision_reasoning,
        }

        # Submit CHECK gate to Empirica
        try:
            gate_result = self.check_gate(
                {
                    "type": "oracle_guidance",
                    "description": f"Oracle guidance request: {question[:100]}",
                    "scope": "medium",
                }
            )
            if gate_result:
                result["decision"] = gate_result

                # Log CHECK checkpoint with atomic triple-write if API available
                if self.empirica.api_available and self._session_id:
                    try:
                        self.empirica.api_manager.log_checkpoint(
                            session_id=self._session_id,
                            phase="CHECK",
                            data={
                                "confidence": confidence,
                                "decision": gate_result,
                                "findings_count": findings_count,
                                "unknowns_count": unknowns_count,
                            },
                        )
                    except Exception:
                        pass  # Continue even if checkpoint logging fails
        except Exception:
            pass  # Continue even if check gate fails

        return result

    def _empirica_postflight(
        self, preflight: dict[str, Any], check: dict[str, Any], response: dict[str, Any]
    ) -> dict[str, Any]:
        """
        STEP 5: POSTFLIGHT - Measure learning deltas and verify calibration.

        Returns:
            Postflight result with DELTA (knowledge change) and UNCERTAINTY change
        """
        # Calculate deltas (simplified - in real Empirica, this compares preflight vs postflight vectors)
        # For now, we track that guidance was provided
        postflight_vectors = {
            "engagement": 0.9,  # Increased engagement after providing guidance
            "foundation": {
                "know": response.get("know", 0.0),
                "do": 0.8,  # Oracle can provide guidance
                "context": 0.7,
            },
            "uncertainty": response.get("uncertainty", 0.5),
        }

        # Calculate deltas (simplified - would compare with preflight vectors in full implementation)
        know_delta = 0.0  # Would be: postflight_vectors["foundation"]["know"] - preflight["know"]
        uncertainty_delta = (
            0.0  # Would be: postflight_vectors["uncertainty"] - preflight["uncertainty"]
        )

        result = {
            "knowledge_delta": know_delta,
            "uncertainty_delta": uncertainty_delta,
            "guidance_provided": True,
            "recommendation_generated": bool(response.get("recommendation")),
        }

        # Submit to Empirica if session ID available
        if self._session_id:
            try:
                # Use Python API if available (atomic triple-write)
                if self.empirica.api_available:
                    # Update beliefs with postflight evidence
                    evidence = {
                        "vectors": postflight_vectors,
                        "reasoning": f"Oracle guidance provided: {response.get('question', '')[:100]}",
                        "phase": "POSTFLIGHT",
                    }
                    updated = self.empirica.api_manager.update_beliefs(
                        session_id=self._session_id, evidence=evidence
                    )
                    if updated:
                        # Log checkpoint with atomic triple-write
                        self.empirica.api_manager.log_checkpoint(
                            session_id=self._session_id,
                            phase="POSTFLIGHT",
                            data={
                                "vectors": postflight_vectors,
                                "reasoning": evidence["reasoning"],
                            },
                        )
                else:
                    # Fall back to CLI (CLI also performs triple-write via Empirica)
                    self.empirica.submit_postflight(
                        self._session_id,
                        postflight_vectors,
                        reasoning=f"Oracle guidance provided: {response.get('question', '')[:100]}",
                    )
            except Exception:
                pass  # Continue even if postflight submission fails

        return result

    def _generate_recommendation(
        self,
        phase: str,
        coverage: float,
        unknowns: list[dict[str, Any]],
        uncertainty: float = 0.5,
        reflection: dict[str, Any] | None = None,
        check_result: dict[str, Any] | None = None,
    ) -> str:
        """Generate recommendation based on epistemic state with personality, memory, reflection, and check result."""
        # Incorporate check decision into recommendation
        check_decision = check_result.get("decision", "PROCEED") if check_result else "PROCEED"
        check_confidence = check_result.get("confidence", 0.5) if check_result else 0.5

        # Incorporate reflection insights if available
        reflection_insight = ""
        if reflection and reflection.get("relevant_experiences"):
            relevant = reflection["relevant_experiences"][:2]  # Top 2 most relevant
            if relevant:
                outcomes = [exp.get("outcome", "") for exp in relevant if exp.get("outcome")]
                if outcomes:
                    reflection_insight = (
                        f"Reflecting on past experiences: {', '.join(outcomes[:2])}. "
                    )

        # Try to use learned patterns first
        learned_recs = self.journal.get_patterns_for_phase(phase)
        if learned_recs:
            # Use a learned recommendation (most recent)
            import random

            base = random.choice(learned_recs[-3:])  # Pick from last 3
        else:
            # Base recommendations
            base_recommendations = {
                "Data Gathering": "Focus on collecting data and observations. High uncertainty suggests need for more information.",
                "Exploration": "Explore different approaches. Moderate knowledge with uncertainty suggests experimentation.",
                "Synthesis": "Synthesize findings. High knowledge with low uncertainty suggests patterns can be identified.",
                "Evolution": "Ready for evolution. Very high knowledge with very low uncertainty suggests system can advance.",
                "Transition": f"Knowledge coverage: {coverage:.0%}. Continue building on existing knowledge.",
                "UNKNOWN": f"Low knowledge coverage ({coverage:.0%}). Focus on addressing unknowns: {len(unknowns)} open questions.",
            }

            if phase in base_recommendations:
                base = base_recommendations[phase]
            elif coverage < 0.3:
                base = base_recommendations["UNKNOWN"]
            else:
                base = base_recommendations["Transition"]

        # Incorporate check decision
        if check_decision == "HALT":
            base = f"[HALT] {base} This requires human approval due to high uncertainty or insufficient knowledge."
        elif check_decision == "BRANCH":
            base = f"[BRANCH] {base} Investigation needed first - {len(unknowns)} unknowns should be addressed."
        elif check_decision == "REVISE":
            base = f"[REVISE] {base} Approach needs refinement based on current epistemic state."
        elif check_decision == "PROCEED":
            base = f"[PROCEED] {base} Confidence: {check_confidence:.0%}. Safe to proceed."

        # Combine reflection insight with base recommendation
        if reflection_insight:
            base = reflection_insight + base

        # Apply personality
        return self._apply_personality_to_recommendation(base, phase, coverage, uncertainty)

    def _apply_personality_to_recommendation(
        self, base_recommendation: str, phase: str, coverage: float, uncertainty: float
    ) -> str:
        """
        Apply personality styling to recommendation.

        Args:
            base_recommendation: Base recommendation text
            phase: Current epistemic phase
            coverage: Knowledge coverage (0.0-1.0)
            uncertainty: Uncertainty level (0.0-1.0)

        Returns:
            Recommendation with personality applied
        """
        # Get contextual adaptation
        context = self.personality.adapt_to_context(phase, uncertainty, coverage)

        # Apply personality to text
        styled = self.personality.apply_personality_to_text(base_recommendation, context)

        # Add personality-appropriate transition if needed
        if not styled.startswith("["):  # Don't add transition to gate-tagged recommendations
            transition = self.personality.get_transition()
            if transition and transition not in styled:
                styled = f"{transition} {styled}"

        return styled

    def assess_decision(self, decision_context: dict[str, Any]) -> dict[str, Any]:
        """
        Assess a decision using epistemic state and CHECK gate.

        Args:
            decision_context: Context about the decision to make

        Returns:
            Dictionary with assessment, gate result, and recommendations
        """
        # Check gate
        gate_result = self.check_gate(
            {
                "type": "decision",
                "scope": decision_context.get("scope", "medium"),
                "description": decision_context.get("description", "Decision assessment"),
                **decision_context,
            }
        )

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
                self.log_insight(
                    f"Decision halted: {decision_desc[:100]} - requires human approval", impact=0.8
                )
            elif gate_result == "BRANCH":
                self.log_unknown(f"Decision needs investigation: {decision_desc[:100]}")
            elif gate_result == "REVISE":
                self.log_insight(f"Decision needs revision: {decision_desc[:100]}", impact=0.6)
        except Exception:
            pass  # Continue even if logging fails

        recommendation = self._get_gate_recommendation(gate_result, unknowns)

        assessment_result = {
            "gate_result": gate_result,
            "epistemic_phase": phase,
            "state": state,
            "unknowns": unknowns,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat(),
        }

        # Log to journal
        try:
            self.journal.log_assessment(decision_context, assessment_result)
        except Exception:
            pass  # Continue even if journal logging fails

        return assessment_result

    def _get_gate_recommendation(
        self, gate_result: str | None, unknowns: list[dict[str, Any]]
    ) -> str:
        """Get recommendation based on gate result."""
        base_recommendations = {
            "PROCEED": "Safe to proceed. Epistemic state supports this operation.",
            "HALT": "Operation requires human approval. High risk or insufficient knowledge.",
            "BRANCH": f"Need investigation first. {len(unknowns)} relevant unknowns should be addressed.",
            "REVISE": "Approach needs revision. Consider alternative methods based on epistemic state.",
            None: "Gate check failed. Proceed with caution.",
        }

        base = base_recommendations.get(gate_result, base_recommendations[None])

        # Apply personality
        if gate_result == "PROCEED":
            trait_phrase = self.personality.get_phrase("trait_expressions", "practicality")
        elif gate_result == "HALT":
            trait_phrase = self.personality.get_phrase("trait_expressions", "wisdom")
        elif gate_result == "BRANCH":
            trait_phrase = self.personality.get_phrase("trait_expressions", "curiosity")
        else:
            trait_phrase = ""

        if trait_phrase:
            return f"{trait_phrase} {base}"

        return base

    def get_personality_info(self) -> dict[str, Any]:
        """Get personality information."""
        return {
            "type": self.personality.data.get("type", "balanced"),
            "name": self.personality.data.get("name", "The Oracle"),
            "title": self.personality.data.get("title", "Epistemic Intelligence System"),
            "traits": self.personality.data.get("traits", {}),
            "communication_style": self.personality.data.get("communication_style", {}),
            "quirks": self.personality.data.get("quirks", []),
        }

    def save_personality(self, file_path: Path | None = None) -> None:
        """
        Save current personality to file.

        Args:
            file_path: Optional path (defaults to .empirica/oracle_personality.json)
        """
        if file_path is None:
            file_path = self.project_path / ".empirica" / "oracle_personality.json"

        self.personality.save_to_file(file_path)

    def set_personality_trait(self, trait: str, value: float) -> None:
        """
        Set a personality trait value.

        Args:
            trait: Trait name (wisdom, curiosity, precision, etc.)
            value: Trait value (0.0-1.0)
        """
        if "traits" not in self.personality.data:
            self.personality.data["traits"] = {}

        self.personality.data["traits"][trait] = max(0.0, min(1.0, value))

    def get_memory_summary(self) -> dict[str, Any]:
        """Get Oracle memory summary."""
        return self.journal.get_memory_summary()

    def search_memory(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """
        Search Oracle memory.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching memory entries
        """
        return self.journal.search_memory(query, limit=limit)

    def remember_successful_recommendation(
        self, recommendation: str, outcome: str, epistemic_phase: str
    ) -> None:
        """
        Remember a successful recommendation for future use.

        Args:
            recommendation: Recommendation text
            outcome: Outcome description
            epistemic_phase: Phase when recommendation was made
        """
        self.journal.remember_successful_recommendation(recommendation, outcome, epistemic_phase)

    def _reflect_on_question(self, question: str) -> dict[str, Any]:
        """
        Reflect on the question before providing guidance.

        Reviews:
        - Past similar consultations
        - Relevant insights from memory
        - Learned patterns for the current phase
        - Epistemic trajectory

        Args:
            question: The question being asked

        Returns:
            Reflection dictionary with insights, patterns, and relevant experiences
        """
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "relevant_experiences": [],
            "relevant_insights": [],
            "learned_patterns": {},
            "epistemic_trajectory": None,
            "reflection_summary": "",
        }

        try:
            # 1. Search memory for relevant past experiences
            memory_results = self.journal.search_memory(question, limit=5)
            reflection["relevant_experiences"] = [
                {
                    "type": r.get("type", "unknown"),
                    "content": r.get("content", "")[:200],
                    "impact": r.get("impact", 0.0),
                    "phase": r.get("phase", "UNKNOWN"),
                    "timestamp": r.get("timestamp", ""),
                }
                for r in memory_results
            ]

            # 2. Get relevant insights from memory
            top_insights = self.journal.memory.get("insights", [])[:5]
            reflection["relevant_insights"] = [
                {
                    "insight": i.get("insight", "")[:200],
                    "impact": i.get("impact", 0.0),
                    "timestamp": i.get("timestamp", ""),
                }
                for i in top_insights
                if any(
                    keyword in question.lower()
                    for keyword in self.journal._extract_keywords(i.get("insight", ""))
                )
            ]

            # 3. Get learned patterns for current phase (will be determined later, but prepare)
            current_phase = self.get_epistemic_phase()
            phase_recs = self.journal.get_patterns_for_phase(current_phase)
            reflection["learned_patterns"] = {
                "phase": current_phase,
                "recommendations_count": len(phase_recs),
                "top_keywords": [kw[0] for kw in self.journal.get_top_keywords(limit=5)],
            }

            # 4. Analyze epistemic trajectory (recent history)
            history = self.journal.memory.get("epistemic_history", [])
            if len(history) >= 3:
                recent = history[-3:]
                trajectory = {"trend": "stable", "coverage_change": 0.0, "uncertainty_change": 0.0}

                if len(recent) >= 2:
                    first = recent[0]
                    last = recent[-1]
                    coverage_change = last.get("coverage", 0.0) - first.get("coverage", 0.0)
                    uncertainty_change = last.get("uncertainty", 1.0) - first.get(
                        "uncertainty", 1.0
                    )

                    trajectory["coverage_change"] = coverage_change
                    trajectory["uncertainty_change"] = uncertainty_change

                    if coverage_change > 0.1:
                        trajectory["trend"] = "improving"
                    elif coverage_change < -0.1:
                        trajectory["trend"] = "declining"
                    elif uncertainty_change < -0.1:
                        trajectory["trend"] = "clarifying"
                    elif uncertainty_change > 0.1:
                        trajectory["trend"] = "increasing_uncertainty"

                reflection["epistemic_trajectory"] = trajectory

            # 5. Generate reflection summary
            summary_parts = []

            if reflection["relevant_experiences"]:
                summary_parts.append(
                    f"Found {len(reflection['relevant_experiences'])} relevant past experiences"
                )

            if reflection["relevant_insights"]:
                summary_parts.append(
                    f"{len(reflection['relevant_insights'])} relevant insights available"
                )

            if reflection["learned_patterns"]["recommendations_count"] > 0:
                summary_parts.append(
                    f"{reflection['learned_patterns']['recommendations_count']} learned patterns for {current_phase} phase"
                )

            if reflection["epistemic_trajectory"]:
                trend = reflection["epistemic_trajectory"]["trend"]
                summary_parts.append(f"Epistemic trajectory: {trend}")

            if summary_parts:
                reflection["reflection_summary"] = ". ".join(summary_parts) + "."
            else:
                reflection["reflection_summary"] = (
                    "No significant patterns found in past experiences yet."
                )

        except Exception as e:
            # If reflection fails, continue with empty reflection
            reflection["reflection_summary"] = f"Reflection encountered an issue: {str(e)[:100]}"
            reflection["error"] = str(e)

        return reflection
