"""
The Chief: Pantheon Entity of Iterative Self-Improvement and Evolutionary Loops

The Chief serves as the embodiment of self-referential iteration and continuous
improvement through repeated cycles of development, evaluation, and refinement.
Integrates Chief Wiggum's iterative loop methodology into WAFT's evolutionary framework.

Following "as above, so below" principles:
- As above: Divine force of iterative self-improvement and evolutionary refinement
- So below: File-based system managing iteration loops, completion tracking, and evolution cycles
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class IterationLoop:
    """Represents a self-referential iteration loop."""

    def __init__(
        self,
        loop_id: str,
        prompt: str,
        completion_promise: str | None = None,
        max_iterations: int = 10,
        current_iteration: int = 0,
        status: str = "active",
        created_at: str | None = None,
        completed_at: str | None = None,
        iterations_history: list[dict[str, Any]] | None = None,
    ):
        """
        Initialize iteration loop.

        Args:
            loop_id: Unique loop identifier
            prompt: The prompt to iterate on
            completion_promise: Text phrase that signals completion
            max_iterations: Maximum number of iterations
            current_iteration: Current iteration number
            status: Loop status (active, completed, cancelled, failed)
            created_at: ISO timestamp of creation
            completed_at: ISO timestamp of completion
            iterations_history: History of each iteration's results
        """
        self.loop_id = loop_id
        self.prompt = prompt
        self.completion_promise = completion_promise
        self.max_iterations = max_iterations
        self.current_iteration = current_iteration
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.iterations_history = iterations_history or []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "loop_id": self.loop_id,
            "prompt": self.prompt,
            "completion_promise": self.completion_promise,
            "max_iterations": self.max_iterations,
            "current_iteration": self.current_iteration,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "iterations_history": self.iterations_history,
        }


class TheChief:
    """
    The Chief: Pantheon entity of iterative self-improvement.

    Provides:
    - Iterative development loop management
    - Self-referential AI improvement cycles
    - Completion tracking and promise validation
    - Integration with WAFT's evolutionary system
    - Iteration history and analysis
    """

    def __init__(self, project_path: Path):
        """
        Initialize The Chief.

        Args:
            project_path: Project root path
        """
        self.project_path = project_path
        self.chief_path = project_path / "_pantheon" / "the_chief"
        self.chief_path.mkdir(parents=True, exist_ok=True)

        # The Chief's directories
        self.loops_path = self.chief_path / "loops"
        self.loops_path.mkdir(exist_ok=True)
        self.history_path = self.chief_path / "history"
        self.history_path.mkdir(exist_ok=True)
        self.analytics_path = self.chief_path / "analytics"
        self.analytics_path.mkdir(exist_ok=True)

        # Registry
        self.registry_file = self.chief_path / "chief_registry.json"
        self._ensure_registry()

        # Chief Wiggum integration path
        self.wiggum_path = project_path / "_integrations" / "chief-wiggum"

    def _ensure_registry(self) -> None:
        """Ensure registry file exists."""
        if not self.registry_file.exists():
            registry = {
                "active_loops": [],
                "completed_loops": [],
                "total_iterations": 0,
                "total_loops": 0,
                "last_update": datetime.now().isoformat(),
                "wiggum_integration": {
                    "enabled": True,
                    "version": "chief-wiggum",
                    "integrated_at": datetime.now().isoformat(),
                },
            }
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def start_loop(
        self,
        prompt: str,
        completion_promise: str | None = None,
        max_iterations: int = 10,
    ) -> dict[str, Any]:
        """
        Start a new iteration loop.

        Args:
            prompt: The prompt to iterate on
            completion_promise: Text phrase that signals completion
            max_iterations: Maximum number of iterations (recommended: 10-20)

        Returns:
            Loop initialization data
        """
        # Generate loop ID
        loop_id = f"loop_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create loop
        loop = IterationLoop(
            loop_id=loop_id,
            prompt=prompt,
            completion_promise=completion_promise,
            max_iterations=max_iterations,
        )

        # Save loop
        loop_file = self.loops_path / f"{loop_id}.json"
        loop_file.write_text(json.dumps(loop.to_dict(), indent=2), encoding="utf-8")

        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["active_loops"].append(loop_id)
        registry["total_loops"] += 1
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return {
            "loop_id": loop_id,
            "status": "started",
            "prompt": prompt,
            "max_iterations": max_iterations,
            "completion_promise": completion_promise,
            "message": "The Chief has initiated a new iteration loop",
        }

    def record_iteration(
        self, loop_id: str, iteration_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Record the results of an iteration.

        Args:
            loop_id: Loop identifier
            iteration_data: Data from this iteration (changes, tests, outputs)

        Returns:
            Updated loop status
        """
        loop_file = self.loops_path / f"{loop_id}.json"

        if not loop_file.exists():
            return {"error": f"Loop {loop_id} not found"}

        loop_data = json.loads(loop_file.read_text(encoding="utf-8"))
        loop_data["current_iteration"] += 1
        loop_data["iterations_history"].append(
            {
                "iteration": loop_data["current_iteration"],
                "timestamp": datetime.now().isoformat(),
                "data": iteration_data,
            }
        )

        # Check if completed
        if loop_data["completion_promise"] and iteration_data.get("output"):
            if loop_data["completion_promise"] in str(iteration_data["output"]):
                loop_data["status"] = "completed"
                loop_data["completed_at"] = datetime.now().isoformat()
                self._move_to_completed(loop_id)

        # Check max iterations
        if loop_data["current_iteration"] >= loop_data["max_iterations"]:
            if loop_data["status"] == "active":
                loop_data["status"] = "max_iterations_reached"
                loop_data["completed_at"] = datetime.now().isoformat()
                self._move_to_completed(loop_id)

        loop_file.write_text(json.dumps(loop_data, indent=2), encoding="utf-8")

        # Update registry
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        registry["total_iterations"] += 1
        registry["last_update"] = datetime.now().isoformat()
        self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

        return loop_data

    def cancel_loop(self, loop_id: str) -> dict[str, Any]:
        """
        Cancel an active loop.

        Args:
            loop_id: Loop identifier

        Returns:
            Cancellation confirmation
        """
        loop_file = self.loops_path / f"{loop_id}.json"

        if not loop_file.exists():
            return {"error": f"Loop {loop_id} not found"}

        loop_data = json.loads(loop_file.read_text(encoding="utf-8"))
        loop_data["status"] = "cancelled"
        loop_data["completed_at"] = datetime.now().isoformat()
        loop_file.write_text(json.dumps(loop_data, indent=2), encoding="utf-8")

        self._move_to_completed(loop_id)

        return {
            "loop_id": loop_id,
            "status": "cancelled",
            "message": "The Chief has cancelled this iteration loop",
        }

    def _move_to_completed(self, loop_id: str) -> None:
        """Move loop from active to completed in registry."""
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))

        if loop_id in registry["active_loops"]:
            registry["active_loops"].remove(loop_id)
            registry["completed_loops"].append(loop_id)
            registry["last_update"] = datetime.now().isoformat()
            self.registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def get_loop_status(self, loop_id: str) -> dict[str, Any] | None:
        """
        Get current loop status.

        Args:
            loop_id: Loop identifier

        Returns:
            Loop data or None
        """
        loop_file = self.loops_path / f"{loop_id}.json"

        if loop_file.exists():
            return json.loads(loop_file.read_text(encoding="utf-8"))
        return None

    def get_active_loops(self) -> list[dict[str, Any]]:
        """
        Get all active loops.

        Returns:
            List of active loop data
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))
        active_loops = []

        for loop_id in registry["active_loops"]:
            loop_data = self.get_loop_status(loop_id)
            if loop_data:
                active_loops.append(loop_data)

        return active_loops

    def get_chief_summary(self) -> dict[str, Any]:
        """
        Get The Chief's summary.

        Returns:
            Summary of all iteration loops and analytics
        """
        registry = json.loads(self.registry_file.read_text(encoding="utf-8"))

        active_loops = self.get_active_loops()
        avg_iterations = 0
        if active_loops:
            avg_iterations = sum(
                loop["current_iteration"] for loop in active_loops
            ) / len(active_loops)

        return {
            "active_loops": len(registry["active_loops"]),
            "completed_loops": len(registry["completed_loops"]),
            "total_loops": registry["total_loops"],
            "total_iterations": registry["total_iterations"],
            "average_iterations_per_loop": round(avg_iterations, 2),
            "wiggum_integration": registry["wiggum_integration"],
            "last_update": registry["last_update"],
        }

    def analyze_loop_effectiveness(self, loop_id: str) -> dict[str, Any]:
        """
        Analyze the effectiveness of a completed loop.

        Args:
            loop_id: Loop identifier

        Returns:
            Analytics data
        """
        loop_data = self.get_loop_status(loop_id)

        if not loop_data:
            return {"error": f"Loop {loop_id} not found"}

        analysis = {
            "loop_id": loop_id,
            "total_iterations": loop_data["current_iteration"],
            "status": loop_data["status"],
            "efficiency_ratio": loop_data["current_iteration"]
            / loop_data["max_iterations"],
            "completed_successfully": loop_data["status"] == "completed",
            "duration_seconds": None,
        }

        # Calculate duration if completed
        if loop_data["completed_at"]:
            created = datetime.fromisoformat(loop_data["created_at"])
            completed = datetime.fromisoformat(loop_data["completed_at"])
            analysis["duration_seconds"] = (completed - created).total_seconds()

        # Save analysis
        analysis_file = self.analytics_path / f"{loop_id}_analysis.json"
        analysis_file.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

        return analysis
