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

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

# Try to import Empirica API
try:
    from .empirica_api import EMPIRICA_API_AVAILABLE, EmpiricaAPIManager
except ImportError:
    EMPIRICA_API_AVAILABLE = False
    EmpiricaAPIManager = None


class EmpiricaManager:
    """Manages Empirica integration for epistemic tracking."""

    def __init__(self, project_path: Path):
        """
        Initialize the Empirica manager.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self._empirica_cmd = self._find_empirica_command()
        self._project_id: str | None = None  # Cached project ID

        # Try to initialize Python API (preferred over CLI)
        self._api_manager: EmpiricaAPIManager | None = None
        if EMPIRICA_API_AVAILABLE and EmpiricaAPIManager:
            try:
                self._api_manager = EmpiricaAPIManager(project_path)
                if self._api_manager.is_available:
                    # Python API available - prefer this over CLI
                    pass
            except Exception:
                # API initialization failed - fall back to CLI
                self._api_manager = None

    @property
    def api_available(self) -> bool:
        """Check if Python API is available."""
        return self._api_manager is not None and self._api_manager.is_available

    @property
    def api_manager(self):
        """Get the Python API manager if available."""
        return self._api_manager if self.api_available else None

    def _find_empirica_command(self) -> list:
        """
        Find the best empirica command to use.
        Tries Python 3.12/3.11's empirica binary first (required for Empirica), then falls back to system command.

        Returns:
            List of command parts for subprocess.run (e.g., ["/path/to/python3.12/bin/empirica"] or ["empirica"])
        """
        # Try Python 3.12/3.11's empirica binary first (Empirica requires 3.11+)
        for py_version in ["3.12", "3.11"]:
            # Try common installation path for Python framework
            empirica_path = (
                f"/Library/Frameworks/Python.framework/Versions/{py_version}/bin/empirica"
            )
            if os.path.exists(empirica_path) and os.access(empirica_path, os.X_OK):
                # Verify it works by checking version
                try:
                    result = subprocess.run(
                        [empirica_path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    if result.returncode == 0 and (
                        "3.12" in result.stdout or "3.11" in result.stdout
                    ):
                        return [empirica_path]
                except (
                    subprocess.TimeoutExpired,
                    FileNotFoundError,
                    subprocess.CalledProcessError,
                ):
                    continue

        # Fallback: try direct empirica command (may use wrong Python version)
        empirica_cmd = shutil.which("empirica")
        if empirica_cmd:
            # Check if it's the Python 3.12/3.11 version
            try:
                result = subprocess.run(
                    [empirica_cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0 and ("3.12" in result.stdout or "3.11" in result.stdout):
                    return [empirica_cmd]
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                pass

        return ["empirica"]  # Will fail with FileNotFoundError, but consistent interface

    def is_initialized(self) -> bool:
        """
        Check if Empirica is initialized in the project.

        Returns:
            True if .empirica directory exists (Empirica's project marker)
        """
        # Empirica requires git, so check for .git
        if not (self.project_path / ".git").exists():
            return False

        # Check for .empirica directory (Empirica's project marker)
        # Empirica creates .empirica/config.yaml when initialized
        empirica_dir = self.project_path / ".empirica"
        empirica_config = empirica_dir / "config.yaml"
        return empirica_dir.exists() and empirica_config.exists()

    def validate_setup(self) -> dict[str, Any]:
        """
        Run preflight validation checks on Empirica setup.

        Returns:
            Dictionary with validation results:
            {
                "git_initialized": bool,
                "empirica_initialized": bool,
                "cli_available": bool,
                "cli_version": str | None,
                "project_exists": bool,
                "project_id": str | None,
                "session_creatable": bool,
                "errors": List[str],
                "warnings": List[str],
                "ready": bool
            }
        """
        validation = {
            "git_initialized": False,
            "empirica_initialized": False,
            "cli_available": False,
            "cli_version": None,
            "project_exists": False,
            "project_id": None,
            "session_creatable": False,
            "errors": [],
            "warnings": [],
            "ready": False,
        }

        # Check 1: Git initialized
        try:
            validation["git_initialized"] = (self.project_path / ".git").exists()
            if not validation["git_initialized"]:
                validation["errors"].append("Git repository not initialized")
        except Exception as e:
            validation["errors"].append(f"Error checking git: {str(e)}")

        # Check 2: Empirica initialized
        try:
            validation["empirica_initialized"] = self.is_initialized()
            if not validation["empirica_initialized"]:
                validation["warnings"].append("Empirica not initialized (will auto-initialize)")
        except Exception as e:
            validation["errors"].append(f"Error checking Empirica initialization: {str(e)}")

        # Check 3: CLI available
        try:
            result = subprocess.run(
                self._empirica_cmd + ["--version"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=3,
            )
            if result.returncode == 0:
                validation["cli_available"] = True
                validation["cli_version"] = result.stdout.strip()
            else:
                validation["errors"].append("Empirica CLI version check failed")
        except FileNotFoundError:
            validation["errors"].append("Empirica CLI not found in PATH")
        except subprocess.TimeoutExpired:
            validation["errors"].append("Empirica CLI version check timed out")
        except Exception as e:
            validation["errors"].append(f"Error checking CLI: {str(e)}")

        # Check 4: Project exists
        if validation["cli_available"]:
            try:
                context = self.project_bootstrap()
                if context and context.get("ok"):
                    validation["project_exists"] = True
                    validation["project_id"] = context.get("project_id") or self._project_id
                else:
                    validation["warnings"].append("Project not found (will auto-create)")
            except Exception as e:
                validation["errors"].append(f"Error checking project: {str(e)}")

        # Check 5: Session creation
        if validation["cli_available"] and validation["empirica_initialized"]:
            try:
                session_id = self.create_session(ai_id="validation_test", session_type="test")
                validation["session_creatable"] = session_id is not None
                if not validation["session_creatable"]:
                    validation["warnings"].append("Session creation failed")
            except Exception as e:
                validation["warnings"].append(f"Error creating test session: {str(e)}")

        # Overall readiness
        validation["ready"] = (
            validation["git_initialized"]
            and validation["cli_available"]
            and len(validation["errors"]) == 0
        )

        return validation

    def ensure_ready(
        self, ai_id: str = "waft", session_type: str = "development", force_session: bool = True
    ) -> dict[str, Any]:
        """
        Ensure Empirica is ready to use - ALWAYS. No degraded mode.

        This method:
        1. Checks if Empirica is initialized (directory exists)
        2. Auto-initializes if needed (including git init)
        3. Verifies Empirica CLI is available and working
        4. Creates a session if needed (if force_session=True)
        5. Ensures context is available

        Args:
            ai_id: AI agent identifier for session creation
            session_type: Type of session to create
            force_session: If True, create a session if none exists

        Returns:
            Dictionary with status information:
            {
                "ready": bool,  # True if fully ready (initialized + CLI + context)
                "initialized": bool,  # True if directory exists
                "cli_available": bool,  # True if CLI command works
                "has_context": bool,  # True if project_bootstrap() returns data
                "message": str,  # Human-readable status message
                "auto_initialized": bool,  # True if we just initialized it
                "session_created": bool  # True if we just created a session
            }

        Raises:
            RuntimeError: If Empirica cannot be made ready (CLI not available, etc.)
        """
        result = {
            "ready": False,
            "initialized": False,
            "cli_available": False,
            "has_context": False,
            "message": "",
            "auto_initialized": False,
            "session_created": False,
        }

        # Step 1: Check if initialized (directory exists)
        try:
            is_init = self.is_initialized()
            result["initialized"] = is_init
        except Exception as e:
            raise RuntimeError(f"Error checking Empirica initialization: {str(e)}")

        # Step 2: Auto-initialize if not initialized
        if not is_init:
            # Check if git is available (required for Empirica)
            git_exists = False
            try:
                git_exists = (self.project_path / ".git").exists()
            except Exception as e:
                raise RuntimeError(f"Error checking git repository: {str(e)}")

            if not git_exists:
                # Try to initialize git
                try:
                    subprocess.run(
                        ["git", "init"],
                        cwd=self.project_path,
                        capture_output=True,
                        check=True,
                        timeout=10,
                    )
                except subprocess.TimeoutExpired:
                    raise RuntimeError(
                        "Git initialization timed out. Please initialize git manually: git init"
                    )
                except FileNotFoundError:
                    raise RuntimeError(
                        "Git not found. Empirica requires git to be installed and in PATH. "
                        "Install git: https://git-scm.com/downloads"
                    )
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(
                        f"Git initialization failed: {str(e)}. "
                        "Please initialize git manually: git init"
                    )
                except Exception as e:
                    raise RuntimeError(f"Unexpected error initializing git: {str(e)}")

            # Try to initialize Empirica
            try:
                initialized = self.initialize()
                result["auto_initialized"] = initialized
                if not initialized:
                    raise RuntimeError(
                        "Failed to initialize Empirica. CLI may not be installed or available. "
                        "Install Empirica: pip install empirica"
                    )
                result["initialized"] = True
            except RuntimeError:
                raise  # Re-raise RuntimeErrors
            except Exception as e:
                raise RuntimeError(f"Unexpected error initializing Empirica: {str(e)}")

        # Step 3: Verify CLI is available
        try:
            # Test CLI by checking version (quick test)
            test_result = subprocess.run(
                self._empirica_cmd + ["--version"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if test_result.returncode != 0:
                error_msg = test_result.stderr or test_result.stdout or "Unknown error"
                raise RuntimeError(
                    f"Empirica CLI is not working correctly (exit code {test_result.returncode}). "
                    f"Command: {' '.join(self._empirica_cmd)}\n"
                    f"Error: {error_msg}"
                )
            result["cli_available"] = True
        except FileNotFoundError:
            raise RuntimeError(
                f"Empirica CLI not found at: {' '.join(self._empirica_cmd)}\n"
                "Install Empirica: pip install empirica"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                "Empirica CLI version check timed out. The CLI may be slow or unresponsive."
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            raise RuntimeError(f"Empirica CLI test failed: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error testing Empirica CLI: {str(e)}")

        # Step 4: Ensure project exists (project_bootstrap will auto-create if needed)
        try:
            project_id = self._ensure_project_exists()
            if project_id:
                result["project_id"] = project_id
        except Exception as e:
            # Project creation is not critical - we can continue
            # But log it as a warning
            result["project_warning"] = f"Project setup issue: {str(e)}"

        # Step 5: Ensure we have a session and context
        try:
            context = self.project_bootstrap()
            if not context and force_session:
                # No context - create a session to ensure we can track
                try:
                    session_id = self.create_session(ai_id=ai_id, session_type=session_type)
                    if session_id:
                        result["session_created"] = True
                        # Try bootstrap again after session creation
                        context = self.project_bootstrap()
                except Exception as e:
                    # Session creation failed - not critical, but log it
                    result["session_warning"] = f"Session creation failed: {str(e)}"

            if context:
                result["has_context"] = True
                result["ready"] = True
                result["message"] = "Empirica is ready with epistemic context."
                # Store project_id from context if available
                if context.get("project_id"):
                    self._project_id = context.get("project_id")
                    result["project_id"] = self._project_id
            else:
                # Even after creating session, no context - this is okay for new projects
                # But we're still "ready" because Empirica is initialized and working
                result["ready"] = True
                result["has_context"] = False
                result["message"] = (
                    "Empirica is ready. Context will be available after first preflight submission."
                )
        except Exception as e:
            # Bootstrap failed - this is not critical for readiness
            # Empirica is still initialized and CLI works
            result["ready"] = True
            result["has_context"] = False
            result["bootstrap_warning"] = f"Project bootstrap failed: {str(e)}"
            result["message"] = (
                "Empirica is ready but project bootstrap failed. This is okay for new projects."
            )

        return result

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
            subprocess.run(
                self._empirica_cmd + ["project-init"],
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

    def create_session(self, ai_id: str = "waft", session_type: str = "development") -> str | None:
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
                self._empirica_cmd + ["session-create", "-"],
                cwd=self.project_path,
                input=json.dumps(session_data),
                capture_output=True,
                text=True,
                check=True,
                timeout=5,  # 5 second timeout to prevent hanging
            )
            # Parse session ID from output (format: {"session_id": "..."})
            import json as json_module

            output = json_module.loads(result.stdout)
            return output.get("session_id")
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            json.JSONDecodeError,
            subprocess.TimeoutExpired,
        ):
            return None

    def submit_preflight(self, session_id: str, vectors: dict, reasoning: str = "") -> bool:
        """
        Submit preflight assessment to Empirica.

        Uses Python API if available, falls back to CLI.

        Args:
            session_id: Session ID
            vectors: Epistemic vectors dictionary
            reasoning: Optional reasoning text

        Returns:
            True if successful, False otherwise
        """
        # Try Python API first (uses EpistemicAssessor)
        if self._api_manager and self._api_manager.is_available:
            assessment = self._api_manager.assess_vectors(
                session_id=session_id, vectors=vectors, reasoning=reasoning
            )
            if assessment:
                # Also log checkpoint
                self._api_manager.log_checkpoint(
                    session_id=session_id,
                    phase="PREFLIGHT",
                    data={"vectors": vectors, "reasoning": reasoning},
                )
                return True

        # Fall back to CLI
        import json

        preflight_data = {
            "session_id": session_id,
            "vectors": vectors,
            "reasoning": reasoning,
        }

        try:
            subprocess.run(
                self._empirica_cmd + ["preflight-submit", "-"],
                cwd=self.project_path,
                input=json.dumps(preflight_data),
                capture_output=True,
                text=True,
                check=True,
                timeout=5,  # 5 second timeout to prevent hanging
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def submit_postflight(self, session_id: str, vectors: dict, reasoning: str = "") -> bool:
        """
        Submit postflight assessment to Empirica.

        Uses Python API if available, falls back to CLI.

        Args:
            session_id: Session ID
            vectors: Epistemic vectors dictionary
            reasoning: Optional reasoning text

        Returns:
            True if successful, False otherwise
        """
        # Try Python API first
        if self._api_manager and self._api_manager.is_available:
            # Update beliefs with postflight evidence
            evidence = {"vectors": vectors, "reasoning": reasoning, "phase": "POSTFLIGHT"}
            updated = self._api_manager.update_beliefs(session_id=session_id, evidence=evidence)
            if updated:
                # Also log checkpoint
                self._api_manager.log_checkpoint(
                    session_id=session_id,
                    phase="POSTFLIGHT",
                    data={"vectors": vectors, "reasoning": reasoning},
                )
                return True

        # Fall back to CLI
        postflight_data = {
            "session_id": session_id,
            "vectors": vectors,
            "reasoning": reasoning,
        }

        try:
            subprocess.run(
                self._empirica_cmd + ["postflight-submit", "-"],
                cwd=self.project_path,
                input=json.dumps(postflight_data),
                capture_output=True,
                text=True,
                check=True,
                timeout=5,  # 5 second timeout to prevent hanging
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _discover_project_id(self) -> str | None:
        """
        Discover project ID by listing projects and matching git remote.

        Returns:
            Project ID if found, None otherwise
        """
        if self._project_id:
            return self._project_id

        try:
            # Get git remote URL
            git_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            git_result.stdout.strip()

            # List projects and find matching one
            result = subprocess.run(
                self._empirica_cmd + ["project-list", "--output", "json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            projects_data = json.loads(result.stdout)

            # Try to find project by git remote
            # Note: Empirica project-list may not include git remote in output
            # So we try project-bootstrap first, and if it fails, we create/link project
            projects = projects_data.get("projects", [])
            if projects:
                # If we have projects, try the first one or search by name
                # For now, we'll use project-bootstrap which will tell us if project exists
                pass

            return None
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError):
            return None

    def _ensure_project_exists(self) -> str | None:
        """
        Ensure Empirica project exists for this git repository.
        Creates project if it doesn't exist.

        This method:
        1. Checks if we already have a cached project_id
        2. Tries project-bootstrap to discover existing project
        3. If no project found, creates a new one
        4. Caches and returns the project_id

        Returns:
            Project ID if successful, None otherwise
        """
        if self._project_id:
            return self._project_id

        try:
            # Try project-bootstrap first to see if project exists
            # This will work if project is already linked to git remote
            try:
                result = subprocess.run(
                    self._empirica_cmd + ["project-bootstrap", "--output", "json"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                bootstrap_data = json.loads(result.stdout)
                if bootstrap_data.get("ok") and bootstrap_data.get("project_id"):
                    self._project_id = bootstrap_data.get("project_id")
                    return self._project_id
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                # Project doesn't exist or not linked - continue to create
                pass

            # Project doesn't exist - create it
            # Extract project name from directory name
            project_name = self.project_path.name

            result = subprocess.run(
                self._empirica_cmd + ["project-create", "--name", project_name, "--output", "json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            project_data = json.loads(result.stdout)
            if project_data.get("ok") and project_data.get("project_id"):
                self._project_id = project_data.get("project_id")
                return self._project_id

            return None
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, KeyError):
            # Git not available or project creation failed - return None
            # This is okay, project_bootstrap will handle it gracefully
            return None

    def project_bootstrap(self) -> dict[str, Any] | None:
        """
        Load project context dynamically (~800 tokens).

        This replaces conversation history with compressed project memory.
        Automatically discovers/creates project if needed.

        Returns:
            Dictionary with epistemic state, goals, findings, unknowns, or None if failed
        """
        # Ensure project exists first
        project_id = self._ensure_project_exists()

        try:
            cmd = self._empirica_cmd + ["project-bootstrap", "--output", "json"]
            if project_id:
                cmd.extend(["--project-id", project_id])

            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            bootstrap_data = json.loads(result.stdout)

            # Cache project_id from response if we didn't have it
            if bootstrap_data.get("ok") and bootstrap_data.get("project_id"):
                self._project_id = bootstrap_data.get("project_id")

            return bootstrap_data if bootstrap_data.get("ok") else None
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
                self._empirica_cmd + ["finding-log", "--finding", finding, "--impact", str(impact)],
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
                self._empirica_cmd + ["unknown-log", "--unknown", unknown],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=3,  # 3 second timeout for logging
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def check_submit(self, operation: dict[str, Any] | None = None) -> str | None:
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
                    self._empirica_cmd + ["check-submit", "-"],
                    cwd=self.project_path,
                    input=json.dumps(operation),
                    capture_output=True,
                    text=True,
                    check=True,
                )
            else:
                result = subprocess.run(
                    self._empirica_cmd + ["check-submit", "-"],
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
        scope: dict[str, float] | None = None,
        success_criteria: list | None = None,
        estimated_complexity: float | None = None,
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
                self._empirica_cmd + ["goals-create", "-"],
                cwd=self.project_path,
                input=json.dumps(goal_data),
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def assess_state(
        self, session_id: str | None = None, include_history: bool = False
    ) -> dict[str, Any] | None:
        """
        Assess current epistemic state.

        Args:
            session_id: Optional session ID
            include_history: Include historical data

        Returns:
            State assessment dict or None if failed
        """
        try:
            cmd = self._empirica_cmd + ["assess-state"]
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
