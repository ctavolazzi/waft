"""
Empirica Manager - Handles Empirica integration for epistemic tracking.

Empirica provides:
- Epistemic self-assessment (CASCADE workflow)
- Session continuity (project-bootstrap)
- Multi-agent coordination
- Knowledge tracking and learning measurement
- Sentinel safety gates (PROCEED/HALT/BRANCH/REVISE)
- Finding/unknown logging
- Goal management
- Trajectory projection and drift detection

See: https://github.com/Nubaeon/empirica
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any


class EmpiricaManager:
    """Manages Empirica integration for epistemic tracking."""

    def __init__(self, project_path: Path):
        """
        Initialize the Empirica manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path

    def is_initialized(self) -> bool:
        """
        Check if Empirica is initialized in the project.

        Returns:
            True if .empirica-project exists or git is initialized
        """
        # Empirica requires git, so check for .git
        if not (self.project_path / ".git").exists():
            return False

        # Check for .empirica-project directory (Empirica's project marker)
        empirica_project = self.project_path / ".empirica-project"
        return empirica_project.exists()

    def initialize(self) -> bool:
        """
        Initialize Empirica in the project.

        This runs: empirica project-init

        Returns:
            True if successful, False otherwise
        """
        # Empirica requires git to be initialized first
        if not (self.project_path / ".git").exists():
            # Initialize git if not already done
            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=self.project_path,
                    capture_output=True,
                    check=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Git not available or failed - Empirica won't work without it
                return False

        # Run empirica project-init
        try:
            result = subprocess.run(
                ["empirica", "project-init"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            # If already initialized, that's okay
            if "already" in e.stderr.lower() or "already" in e.stdout.lower():
                return True
            return False
        except FileNotFoundError:
            # Empirica not installed
            return False

    def create_session(self, ai_id: str = "waft", session_type: str = "development") -> Optional[str]:
        """
        Create a new Empirica session.

        Args:
            ai_id: AI agent identifier
            session_type: Type of session (development, research, etc.)

        Returns:
            Session ID if successful, None otherwise
        """
        import json

        session_data = {
            "ai_id": ai_id,
            "session_type": session_type,
        }

        try:
            result = subprocess.run(
                ["empirica", "session-create", "-"],
                cwd=self.project_path,
                input=json.dumps(session_data),
                capture_output=True,
                text=True,
                check=True,
            )
            # Parse session ID from output (format: {"session_id": "..."})
            import json as json_module

            output = json_module.loads(result.stdout)
            return output.get("session_id")
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return None

    def submit_preflight(self, session_id: str, vectors: dict, reasoning: str = "") -> bool:
        """
        Submit preflight assessment to Empirica.

        Args:
            session_id: Session ID
            vectors: Epistemic vectors dictionary
            reasoning: Optional reasoning text

        Returns:
            True if successful, False otherwise
        """
        import json

        preflight_data = {
            "session_id": session_id,
            "vectors": vectors,
            "reasoning": reasoning,
        }

        try:
            subprocess.run(
                ["empirica", "preflight-submit", "-"],
                cwd=self.project_path,
                input=json.dumps(preflight_data),
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def submit_postflight(self, session_id: str, vectors: dict, reasoning: str = "") -> bool:
        """
        Submit postflight assessment to Empirica.

        Args:
            session_id: Session ID
            vectors: Epistemic vectors dictionary
            reasoning: Optional reasoning text

        Returns:
            True if successful, False otherwise
        """
        postflight_data = {
            "session_id": session_id,
            "vectors": vectors,
            "reasoning": reasoning,
        }

        try:
            subprocess.run(
                ["empirica", "postflight-submit", "-"],
                cwd=self.project_path,
                input=json.dumps(postflight_data),
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def project_bootstrap(self) -> Optional[Dict[str, Any]]:
        """
        Load project context dynamically (~800 tokens).

        This replaces conversation history with compressed project memory.

        Returns:
            Dictionary with epistemic state, goals, findings, unknowns, or None if failed
        """
        try:
            result = subprocess.run(
                ["empirica", "project-bootstrap"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return None

    def log_finding(self, finding: str, impact: float = 0.5) -> bool:
        """
        Log a finding with impact score.

        Args:
            finding: Description of the finding
            impact: Impact score (0.0-1.0)

        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                ["empirica", "finding-log", "--finding", finding, "--impact", str(impact)],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def log_unknown(self, unknown: str) -> bool:
        """
        Log an unknown that needs investigation.

        Args:
            unknown: Description of what needs investigation

        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                ["empirica", "unknown-log", "--unknown", unknown],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_submit(self, operation: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Submit a CHECK gate to assess if operation is safe to proceed.

        Returns: PROCEED | HALT | BRANCH | REVISE | None if failed

        Args:
            operation: Optional operation description dict

        Returns:
            Gate result string or None if failed
        """
        try:
            if operation:
                result = subprocess.run(
                    ["empirica", "check-submit", "-"],
                    cwd=self.project_path,
                    input=json.dumps(operation),
                    capture_output=True,
                    text=True,
                    check=True,
                )
            else:
                result = subprocess.run(
                    ["empirica", "check-submit", "-"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
            output = json.loads(result.stdout)
            return output.get("gate", output.get("result"))
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return None

    def create_goal(
        self,
        session_id: str,
        objective: str,
        scope: Optional[Dict[str, float]] = None,
        success_criteria: Optional[list] = None,
        estimated_complexity: Optional[float] = None,
    ) -> bool:
        """
        Create a goal with epistemic scope.

        Args:
            session_id: Session ID
            objective: Goal objective
            scope: Optional scope dict (breadth, duration, coordination)
            success_criteria: Optional list of success criteria
            estimated_complexity: Optional complexity estimate (0.0-1.0)

        Returns:
            True if successful, False otherwise
        """
        goal_data = {
            "session_id": session_id,
            "objective": objective,
        }
        if scope:
            goal_data["scope"] = scope
        if success_criteria:
            goal_data["success_criteria"] = success_criteria
        if estimated_complexity is not None:
            goal_data["estimated_complexity"] = estimated_complexity

        try:
            subprocess.run(
                ["empirica", "goals-create", "-"],
                cwd=self.project_path,
                input=json.dumps(goal_data),
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def assess_state(self, session_id: Optional[str] = None, include_history: bool = False) -> Optional[Dict[str, Any]]:
        """
        Assess current epistemic state.

        Args:
            session_id: Optional session ID
            include_history: Include historical data

        Returns:
            State assessment dict or None if failed
        """
        try:
            cmd = ["empirica", "assess-state"]
            if session_id:
                cmd.extend(["--session-id", session_id])
            if include_history:
                cmd.append("--include-history")

            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return None

