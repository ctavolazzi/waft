"""
WAFT Kernel - Central Operating Intelligence

The WAFT Kernel is the system-level intelligence that orchestrates the directed
evolution laboratory. It integrates with existing systems (TheObserver, EmpiricaManager,
GamificationManager) to provide self-aware status checks and system coordination.

CRITICAL: This is NOT the same as 42.00_kernel.md from Unified Genesis Protocol
(that's for UNIT_GENESIS entities). The WAFT Kernel is the system-level intelligence.
"""

import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ..cli.epistemic_display import get_moon_phase
from .agent.state import EvolutionaryEvent, EvolutionaryEventType
from .empirica import EmpiricaManager
from .gamification import GamificationManager
from .science.observer import TheObserver


def calculate_epistemic_phase(empirica_manager: EmpiricaManager) -> str:
    """
    Calculate current epistemic phase from Empirica state.

    Phases:
    - Data Gathering: Low knowledge (< 30%), high uncertainty (> 50%)
    - Exploration: Moderate knowledge (30-60%), moderate uncertainty (30-50%)
    - Synthesis: High knowledge (> 60%), low uncertainty (< 30%)
    - Evolution: Very high knowledge (> 80%), very low uncertainty (< 20%)
    - Transition: Other combinations

    Returns "UNKNOWN" if Empirica not initialized or data invalid.

    Args:
        empirica_manager: EmpiricaManager instance

    Returns:
        Phase name as string
    """
    try:
        if not empirica_manager.is_initialized():
            return "UNKNOWN"

        context = empirica_manager.project_bootstrap()
        if not context:
            return "UNKNOWN"

        epistemic_state = context.get("epistemic_state", {})
        if not epistemic_state:
            return "UNKNOWN"

        vectors = epistemic_state.get("vectors", {})
        if not vectors:
            return "UNKNOWN"

        foundation = vectors.get("foundation", {})
        know = foundation.get("know", 0.0) if foundation else 0.0
        uncertainty = vectors.get("uncertainty", 1.0)

        # Validate ranges
        know = max(0.0, min(1.0, know))
        uncertainty = max(0.0, min(1.0, uncertainty))

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
    except Exception:
        # Log error but don't crash
        return "UNKNOWN"


class WAFTKernel:
    """Central operating intelligence for WAFT directed evolution laboratory.

    Lightweight orchestrator that integrates existing systems:
    - TheObserver (Flight Recorder)
    - EmpiricaManager (Epistemic State)
    - GamificationManager (Gamification)
    """

    def __init__(self, project_path: Path):
        """
        Initialize the WAFT Kernel.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self.identity = "WAFT_KERNEL"
        self.mission = "Directed Evolution of Self-Modifying AI Agents"
        self.goal = "Generate data for 'The Physics of Artificial Cognition'"
        self.epistemic_phase = None
        self.boot_time = datetime.now()

        # Integrate with existing systems
        self.empirica = EmpiricaManager(self.project_path)
        self.gamification = GamificationManager(self.project_path)
        self.observer = TheObserver(self.project_path)

    def boot_sequence(self) -> dict[str, Any]:
        """Execute kernel boot sequence.

        Returns:
            Dictionary with boot status information
        """
        # 1. Acknowledge identity
        boot_status = {
            "identity": self.identity,
            "mission": self.mission,
            "goal": self.goal,
            "boot_time": self.boot_time.isoformat(),
        }

        # 2. Perform initial status check
        status = self._perform_status_check()
        boot_status["status"] = status

        # 3. Get epistemic state
        epistemic_state = self.get_epistemic_state()
        boot_status["epistemic_state"] = epistemic_state

        # 4. Declare epistemic phase
        self.epistemic_phase = self.get_epistemic_phase()
        boot_status["epistemic_phase"] = self.epistemic_phase

        # 5. Log to Flight Recorder (via TheObserver)
        self.log_kernel_event("KERNEL_BOOT", boot_status)

        return boot_status

    def get_epistemic_phase(self) -> str:
        """Determine current epistemic phase from system state.

        Returns:
            Epistemic phase string (e.g., "Data Gathering", "Synthesis", "Evolution")
        """
        # Analyze work efforts, git activity, project health
        work_efforts_dir = self.project_path / "_work_efforts"
        active_efforts = 0
        if work_efforts_dir.exists():
            for item in work_efforts_dir.iterdir():
                if item.is_dir() and item.name.startswith("WE-"):
                    index_file = item / f"{item.name}_index.md"
                    if index_file.exists():
                        active_efforts += 1

        # Check git activity
        git_active = self._check_git_activity()

        # Check project health
        pyrite_exists = (self.project_path / "_pyrite").exists()
        lock_exists = (self.project_path / "uv.lock").exists()

        # Determine phase based on system state
        if active_efforts == 0 and not git_active:
            return "Initialization"
        elif active_efforts > 5 or git_active:
            return "Active Development"
        elif self.empirica.is_initialized():
            # Use Empirica state if available
            context = self.empirica.project_bootstrap()
            if context:
                epistemic_state = context.get("epistemic_state", {})
                vectors = epistemic_state.get("vectors", {})
                foundation = vectors.get("foundation", {})
                know = foundation.get("know", 0.0)
                if know > 0.7:
                    return "Synthesis"
                elif know > 0.4:
                    return "Data Gathering"
                else:
                    return "Exploration"
        else:
            # Fallback logic
            if active_efforts > 0:
                return "Data Gathering"
            else:
                return "Idle"

    def get_epistemic_state(self) -> dict[str, Any]:
        """Get epistemic state (hybrid: Empirica + kernel estimates).

        Returns:
            Dictionary with epistemic state information
        """
        # Try Empirica first (existing system)
        if self.empirica.is_initialized():
            context = self.empirica.project_bootstrap()
            if context:
                return self._format_empirica_state(context)

        # Fallback to kernel estimates (only if Empirica unavailable)
        return self._estimate_epistemic_state()

    def _format_empirica_state(self, context: dict[str, Any]) -> dict[str, Any]:
        """Format Empirica state for kernel use.

        Args:
            context: Empirica project bootstrap context

        Returns:
            Formatted epistemic state dictionary
        """
        epistemic_state = context.get("epistemic_state", {})
        vectors = epistemic_state.get("vectors", {})
        foundation = vectors.get("foundation", {})
        comprehension = vectors.get("comprehension", {})
        execution = vectors.get("execution", {})

        know = foundation.get("know", 0.0)
        do = foundation.get("do", 0.0)
        context_val = foundation.get("context", 0.0)
        engagement = vectors.get("engagement", 0.0)
        uncertainty = vectors.get("uncertainty", 0.0)

        # Calculate coverage
        coverage = know * (1.0 - uncertainty) if know > 0 else 0.0
        moon_phase = get_moon_phase(coverage)

        return {
            "source": "empirica",
            "moon_phase": moon_phase,
            "knowledge_percentage": know * 100,
            "uncertainty_percentage": uncertainty * 100,
            "coverage": coverage * 100,
            "vectors": {
                "foundation": {
                    "know": know,
                    "do": do,
                    "context": context_val,
                },
                "engagement": engagement,
                "uncertainty": uncertainty,
            },
            "goals": context.get("goals", []),
            "findings": context.get("findings", []),
            "unknowns": context.get("unknowns", []),
        }

    def _estimate_epistemic_state(self) -> dict[str, Any]:
        """Estimate epistemic state from project structure (fallback only).

        Returns:
            Estimated epistemic state dictionary
        """
        # Analyze project structure
        work_efforts_dir = self.project_path / "_work_efforts"
        pyrite_dir = self.project_path / "_pyrite"
        docs_dir = self.project_path / "docs"
        tests_dir = self.project_path / "tests"

        # Count work efforts
        work_effort_count = 0
        if work_efforts_dir.exists():
            for item in work_efforts_dir.iterdir():
                if item.is_dir() and item.name.startswith("WE-"):
                    work_effort_count += 1

        # Check documentation
        doc_count = 0
        if docs_dir.exists():
            doc_count = len(list(docs_dir.glob("*.md")))

        # Check tests
        test_count = 0
        if tests_dir.exists():
            test_count = len(list(tests_dir.glob("test_*.py")))

        # Estimate knowledge based on structure
        # More work efforts + docs + tests = higher knowledge
        structure_score = min(1.0, (work_effort_count * 0.1 + doc_count * 0.05 + test_count * 0.05))
        uncertainty = max(0.0, 1.0 - structure_score * 0.5)  # Higher structure = lower uncertainty

        coverage = structure_score * (1.0 - uncertainty)
        moon_phase = get_moon_phase(coverage)

        return {
            "source": "kernel_estimate",
            "moon_phase": moon_phase,
            "knowledge_percentage": structure_score * 100,
            "uncertainty_percentage": uncertainty * 100,
            "coverage": coverage * 100,
            "metrics": {
                "work_efforts": work_effort_count,
                "documentation_files": doc_count,
                "test_files": test_count,
            },
        }

    def _perform_status_check(self) -> dict[str, Any]:
        """Perform basic status check.

        Returns:
            Status dictionary
        """
        status = {
            "project_path": str(self.project_path),
            "pyrite_exists": (self.project_path / "_pyrite").exists(),
            "lock_exists": (self.project_path / "uv.lock").exists(),
            "empirica_initialized": self.empirica.is_initialized(),
            "gamification": {
                "integrity": self.gamification.integrity,
                "insight": self.gamification.insight,
                "level": self.gamification.level,
            },
        }

        # Check git
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            status["git_initialized"] = result.returncode == 0
            if status["git_initialized"]:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                )
                status["git_branch"] = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            status["git_initialized"] = False

        return status

    def _check_git_activity(self) -> bool:
        """Check if there's recent git activity.

        Returns:
            True if there's recent activity
        """
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-1", "--since=24 hours ago"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except Exception:
            return False

    def log_kernel_event(
        self,
        event_type: str,  # KERNEL_BOOT, KERNEL_STATUS_CHECK, etc.
        context: dict[str, Any],
    ) -> None:
        """Log kernel event to Flight Recorder via TheObserver.

        Args:
            event_type: Type of kernel event
            context: Event context data
        """
        # Create event using existing EvolutionaryEvent model
        event = EvolutionaryEvent(
            timestamp=datetime.utcnow(),
            genome_id="waft_kernel",  # System-level identifier
            parent_id=None,
            generation=0,
            event_type=EvolutionaryEventType.MUTATE,  # Using MUTATE for kernel events
            payload={
                "kernel_event": True,
                "event_type": event_type,
                "kernel_identity": self.identity,
                **context,
            },
            agent_id="waft_kernel",
            lineage_path=[],
        )

        # Use existing TheObserver to log
        self.observer.observe_event(event)

    def get_uptime(self) -> timedelta:
        """Get kernel uptime since boot.

        Returns:
            Timedelta since boot
        """
        return datetime.now() - self.boot_time

    def kernel_status_check(self) -> dict[str, Any]:
        """Kernel-specific status check.

        Returns:
            Dictionary with kernel operational state
        """
        status = self._perform_status_check()
        epistemic_state = self.get_epistemic_state()
        uptime = self.get_uptime()

        return {
            "identity": self.identity,
            "mission": self.mission,
            "boot_time": self.boot_time.isoformat(),
            "uptime_seconds": uptime.total_seconds(),
            "epistemic_phase": self.get_epistemic_phase(),
            "epistemic_state": epistemic_state,
            "status": status,
            "systems": {
                "flight_recorder": {
                    "operational": self.observer.log_file.exists()
                    if hasattr(self.observer, "log_file")
                    else False,
                    "log_file": str(self.observer.log_file)
                    if hasattr(self.observer, "log_file")
                    else None,
                },
                "empirica": {
                    "initialized": self.empirica.is_initialized(),
                },
                "gamification": {
                    "integrity": self.gamification.integrity,
                    "insight": self.gamification.insight,
                    "level": self.gamification.level,
                },
            },
        }
