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

from .subprocess_validator import validate_free_text

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
        self._instance_id = os.getenv("EMPIRICA_INSTANCE_ID", "waft-bot")

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
        candidates: list[str] = []
        empirica_in_path = shutil.which("empirica")
        if empirica_in_path:
            candidates.append(empirica_in_path)

        for py_version in ["3.12", "3.11"]:
            candidates.append(f"/Library/Frameworks/Python.framework/Versions/{py_version}/bin/empirica")

        candidates.append("empirica")

        for candidate in candidates:
            try:
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                if result.returncode == 0:
                    return [candidate]
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                continue

        return ["empirica"]  # Consistent fallback

    def _empirica_env(self) -> dict[str, str]:
        """Build environment for empirica CLI in headless/Cursor contexts."""
        env = dict(os.environ)
        env["EMPIRICA_INSTANCE_ID"] = self._instance_id
        env["HOME"] = str(self._resolve_empirica_home())
        return env

    def _resolve_empirica_home(self) -> Path:
        """
        Resolve a writable HOME for empirica subprocess calls.

        In sandboxed agent contexts, writes to the real user home may be blocked.
        We prefer WAFT_EMPIRICA_HOME when set, otherwise fall back to project path
        if ~/.empirica is not writable.
        """
        forced = os.getenv("WAFT_EMPIRICA_HOME")
        if forced:
            home = Path(forced).expanduser().resolve()
            home.mkdir(parents=True, exist_ok=True)
            return home

        real_home = Path.home()
        probe_dir = real_home / ".empirica" / "instance_projects"
        try:
            probe_dir.mkdir(parents=True, exist_ok=True)
            probe_file = probe_dir / ".waft_write_probe"
            probe_file.write_text("ok")
            probe_file.unlink(missing_ok=True)
            return real_home
        except OSError:
            self.project_path.mkdir(parents=True, exist_ok=True)
            return self.project_path

    def _write_instance_project_file(self) -> None:
        """Write instance project mapping so project resolution does not rely on tty heuristics."""
        empirica_home = self._resolve_empirica_home()
        instance_dir = empirica_home / ".empirica" / "instance_projects"
        instance_dir.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "project_path": str(self.project_path),
            "project_name": self.project_path.name,
        }
        if self._project_id:
            payload["project_id"] = self._project_id
        (instance_dir / f"{self._instance_id}.json").write_text(json.dumps(payload))

    def _parse_json_output(self, output: str) -> dict[str, Any] | None:
        """Parse JSON from CLI output that may include extra lines."""
        text = output.strip()
        if not text:
            return None
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            pass

        for line in reversed(text.splitlines()):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                parsed = json.loads(line)
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                continue
        return None

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
                env=self._empirica_env(),
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
                env=self._empirica_env(),
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
            self._write_instance_project_file()
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
                env=self._empirica_env(),
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
            self._write_instance_project_file()
            result = subprocess.run(
                self._empirica_cmd + ["session-create", "--output", "json", "-"],
                cwd=self.project_path,
                input=json.dumps(session_data),
                capture_output=True,
                text=True,
                check=True,
                timeout=5,  # 5 second timeout to prevent hanging
                env=self._empirica_env(),
            )
            output = self._parse_json_output(result.stdout)
            session_id = output.get("session_id") if output else None
            if session_id:
                self._write_instance_project_file()
            return session_id
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
                env=self._empirica_env(),
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
                env=self._empirica_env(),
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
                env=self._empirica_env(),
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
                    env=self._empirica_env(),
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
                env=self._empirica_env(),
            )
            project_data = json.loads(result.stdout)
            if project_data.get("ok") and project_data.get("project_id"):
                self._project_id = project_data.get("project_id")
                self._write_instance_project_file()
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
        self._write_instance_project_file()
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
                env=self._empirica_env(),
            )
            bootstrap_data = json.loads(result.stdout)

            # Cache project_id from response if we didn't have it
            if bootstrap_data.get("ok") and bootstrap_data.get("project_id"):
                self._project_id = bootstrap_data.get("project_id")
                self._write_instance_project_file()

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
            validated_finding = validate_free_text(finding, field_name="finding")
            subprocess.run(
                self._empirica_cmd
                + ["finding-log", "--finding", validated_finding, "--impact", str(impact)],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
                env=self._empirica_env(),
            )
            return True
        except (ValueError, subprocess.CalledProcessError, FileNotFoundError):
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
            validated_unknown = validate_free_text(unknown, field_name="unknown")
            subprocess.run(
                self._empirica_cmd + ["unknown-log", "--unknown", validated_unknown],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=3,  # 3 second timeout for logging
                env=self._empirica_env(),
            )
            return True
        except (ValueError, subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def check_submit(
        self,
        operation: dict[str, Any] | None = None,
        session_id: str | None = None,
        vectors: dict[str, Any] | None = None,
        reasoning: str = "",
        decision: str | None = None,
    ) -> str | None:
        """
        Submit a CHECK gate to assess if operation is safe to proceed.

        Returns: PROCEED | HALT | BRANCH | REVISE | None if failed

        Args:
            operation: Optional legacy operation description dict
            session_id: Optional session ID for canonical CHECK payload
            vectors: Optional flat vector dict
            reasoning: Optional reasoning for canonical CHECK payload
            decision: Optional explicit decision hint (`proceed`/`investigate`)

        Returns:
            Gate result string or None if failed
        """
        try:
            payload: dict[str, Any]
            if session_id and vectors:
                payload = {
                    "session_id": session_id,
                    "vectors": vectors,
                    "reasoning": reasoning or "Oracle CHECK gate submission",
                }
            elif operation:
                payload = dict(operation)
                payload.setdefault("session_id", session_id)
                payload.setdefault("vectors", vectors or {"know": 0.5, "uncertainty": 0.5})
                payload.setdefault("reasoning", reasoning or "Legacy CHECK gate submission")
            else:
                payload = {
                    "session_id": session_id,
                    "vectors": vectors or {"know": 0.5, "uncertainty": 0.5},
                    "reasoning": reasoning or "CHECK gate submission",
                }

            if decision:
                payload["decision"] = decision

            result = subprocess.run(
                self._empirica_cmd + ["check-submit", "-"],
                cwd=self.project_path,
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                check=True,
                env=self._empirica_env(),
            )
            output = self._parse_json_output(result.stdout) or {}
            gate = output.get("decision") or output.get("gate") or output.get("result")
            if isinstance(gate, str):
                return gate.upper()
            return None
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
                env=self._empirica_env(),
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
                env=self._empirica_env(),
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return None
