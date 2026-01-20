"""
Science Integration - Bridge between DnD Scenario System and /science-bitch.

Connects experimental iteration with scientific method workflow.
"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from .realm_state_preserver import RealmStatePreserver
from .scenario_orchestrator import ScenarioOrchestrator
from .scenario_realm import ScenarioRealm

# Import TheOracle for Empirica tracking
try:
    from ..science.oracle import TheOracle

    ORACLE_AVAILABLE = True
except (ImportError, RuntimeError, Exception) as e:
    # Oracle may fail if Empirica not ready - that's okay
    ORACLE_AVAILABLE = False
    ORACLE_IMPORT_ERROR = str(e)

# Import scientific method tool
import sys

project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from scientific_method_tool import (
        ExperimentAnalyzer,
        ExperimentLoop,
        ExperimentManager,
        Hypothesis,
        IterationConfig,
        Variable,
        VariableType,
    )

    SCIENTIFIC_METHOD_AVAILABLE = True
except ImportError:
    SCIENTIFIC_METHOD_AVAILABLE = False


class DnDScenarioScienceIntegration:
    """
    Integrates DnD scenario system with scientific method workflow.

    Features:
    - Connect state crystallization with state capture (A)
    - Connect scenario execution with experiment run
    - Connect state restoration with iteration loop
    - Collect data during scenario execution
    - Track experiments in science directory
    - Automatic Empirica tracking via TheOracle
    """

    def __init__(self, scenario_realm: ScenarioRealm, enable_oracle: bool = True):
        """
        Initialize Science Integration.

        Args:
            scenario_realm: ScenarioRealm instance
            enable_oracle: Whether to enable TheOracle for Empirica tracking (default: True)
        """
        if not SCIENTIFIC_METHOD_AVAILABLE:
            raise ImportError(
                "scientific_method_tool not available. Install it to use science integration."
            )

        self.realm = scenario_realm
        self.project_path = scenario_realm.project_path
        self.orchestrator = ScenarioOrchestrator(scenario_realm)
        self.state_preserver = RealmStatePreserver(
            scenario_realm.realm_path, scenario_realm.project_path
        )

        # Initialize experiment manager
        science_path = self.project_path / "_science"
        science_path.mkdir(exist_ok=True)
        self.experiment_manager = ExperimentManager(science_path / "experiments")
        self.analyzer = ExperimentAnalyzer()

        # Initialize TheOracle for Empirica tracking (optional)
        self.oracle = None
        self.oracle_enabled = False
        self.oracle_error = None
        if enable_oracle:
            if not ORACLE_AVAILABLE:
                self.oracle_error = f"Oracle not available: {ORACLE_IMPORT_ERROR if 'ORACLE_IMPORT_ERROR' in globals() else 'Import failed'}"
            else:
                try:
                    self.oracle = TheOracle(
                        project_path=self.project_path, ai_id="dnd_scenario_oracle"
                    )
                    self.oracle_enabled = True
                    # Log insight about experiment system
                    try:
                        self.oracle.log_insight(
                            "DnD Scenario System integrated with scientific method workflow",
                            impact=0.8,
                            category="system_integration",
                        )
                    except Exception:
                        pass  # Logging failed, but Oracle is still enabled
                except RuntimeError as e:
                    # Empirica not ready - that's okay, continue without Oracle
                    self.oracle_enabled = False
                    self.oracle_error = f"Empirica not ready: {e}"
                except Exception as e:
                    # Other Oracle initialization failed - continue without it
                    self.oracle_enabled = False
                    self.oracle_error = str(e)

    def create_experiment_from_hypothesis(
        self, hypothesis: Hypothesis, metadata: dict[str, Any] | None = None
    ):
        """
        Create experiment from hypothesis.

        Args:
            hypothesis: Hypothesis to test
            metadata: Optional metadata

        Returns:
            Experiment instance
        """
        experiment_metadata = {
            "realm_path": str(self.realm.realm_path),
            "realm_id": "dnd_scenario_realm",
            **(metadata or {}),
        }

        return self.experiment_manager.create_experiment(hypothesis, experiment_metadata)

    def capture_initial_state_as_crystallized(
        self, experiment, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Capture initial state using state crystallization.

        This connects state crystallization (A) with experiment initial state.

        Args:
            experiment: Experiment instance
            metadata: Optional metadata

        Returns:
            Crystallization manifest
        """
        # Gather current state
        party_state = self.orchestrator.get_party_state() or {}
        realm_manifest = self.realm.get_realm_manifest()

        state_data = {
            "party_state": party_state,
            "realm_state": realm_manifest,
            "experiment_id": experiment.experiment_id,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {}),
        }

        # Crystallize state
        manifest = self.state_preserver.crystallize_state(state_data)

        # Also capture as SystemState for experiment manager
        components = {
            "party_state": party_state,
            "realm_manifest": realm_manifest,
            "crystallized_state": {
                "manifest": manifest,
                "version": manifest["version"],
                "hash": manifest["hash"],
            },
        }

        initial_state = self.experiment_manager.capture_initial_state(
            experiment,
            components,
            metadata={"crystallization_manifest": manifest, **(metadata or {})},
        )

        return {"crystallization_manifest": manifest, "initial_state": initial_state.to_dict()}

    def run_scenario_as_experiment(
        self,
        experiment,
        mode: str = "encounter",
        experiment_id: str | None = None,
        iteration: int | None = None,
        data_collector_callback: Callable | None = None,
    ) -> dict[str, Any]:
        """
        Run scenario as experiment with data collection.

        Args:
            experiment: Experiment instance
            mode: Scenario mode (encounter, explore, lore)
            experiment_id: Experiment ID (for tracking)
            iteration: Iteration number
            data_collector_callback: Optional callback for custom data collection

        Returns:
            Experiment results
        """
        # Get data collector from experiment
        data_collector = experiment.data_collector

        # Run scenario
        scenario_result = self.orchestrator.run_scenario(
            mode=mode, experiment_id=experiment_id or experiment.experiment_id, iteration=iteration
        )

        # Collect data (C)
        party = self.orchestrator.party_manager.get_party()

        # Collect party metrics
        data_collector.record("party_total_hp", sum([m.hp for m in party]))
        data_collector.record("party_total_max_hp", sum([m.max_hp for m in party]))
        data_collector.record(
            "party_average_level", sum([m.level for m in party]) / len(party) if party else 0
        )
        data_collector.record("party_total_experience", sum([m.experience for m in party]))

        # Collect scenario-specific data
        if mode == "encounter" and "encounter" in scenario_result:
            encounter = scenario_result["encounter"]
            data_collector.record("encounter_rounds", encounter.get("rounds", 0))
            data_collector.record("encounter_xp_gained", encounter.get("xp_gained", 0))
            data_collector.record(
                "encounter_damage_taken", sum(encounter.get("damage_taken", {}).values())
            )

        # Custom data collection callback
        if data_collector_callback:
            data_collector_callback(data_collector, scenario_result, party)

        # Save data
        data_collector.save(experiment.experiment_id)

        return {
            "scenario_result": scenario_result,
            "data_collected": True,
            "experiment_id": experiment.experiment_id,
        }

    def capture_final_state(
        self, experiment, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Capture final state (B) after experiment.

        Args:
            experiment: Experiment instance
            metadata: Optional metadata

        Returns:
            Final state data
        """
        # Gather final state
        party_state = self.orchestrator.get_party_state() or {}
        realm_manifest = self.realm.get_realm_manifest()

        components = {
            "party_state": party_state,
            "realm_manifest": realm_manifest,
            "timestamp": datetime.now().isoformat(),
        }

        final_state = self.experiment_manager.capture_final_state(
            experiment, components, metadata=metadata
        )

        return {"final_state": final_state.to_dict(), "party_state": party_state}

    def run_iterative_experiment(
        self,
        hypothesis: Hypothesis,
        mode: str = "encounter",
        max_iterations: int = 5,
        restore_initial_state: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Run iterative experiment with state restoration.

        This is the main integration point - runs multiple iterations
        with state restoration between each iteration.

        Args:
            hypothesis: Hypothesis to test
            mode: Scenario mode to run
            max_iterations: Maximum number of iterations
            restore_initial_state: Whether to restore initial state between iterations
            metadata: Optional metadata

        Returns:
            Experiment results across all iterations
        """
        # Create experiment
        experiment = self.create_experiment_from_hypothesis(hypothesis, metadata)

        # Capture initial state (A) - crystallize it
        initial_state_data = self.capture_initial_state_as_crystallized(experiment, metadata)

        # Store crystallization manifest for restoration
        crystallization_manifest = initial_state_data["crystallization_manifest"]

        # Run iterations
        all_results = []

        for iteration in range(1, max_iterations + 1):
            # Restore initial state if requested
            if restore_initial_state and iteration > 1:
                # Restore from crystallized state
                state_data = self.state_preserver.restore_state(
                    manifest_path=None  # Use latest
                )

                # Restore party state
                if "party_state" in state_data:
                    self.orchestrator.party_state_manager.save_party_state(
                        state_data["party_state"]
                    )

            # Run scenario as experiment
            result = self.run_scenario_as_experiment(
                experiment, mode=mode, experiment_id=experiment.experiment_id, iteration=iteration
            )

            all_results.append({"iteration": iteration, "result": result})

        # Capture final state (B)
        final_state_data = self.capture_final_state(experiment, metadata)

        # Analyze results - get experiment results first
        # The analyzer needs results, so we'll create a simple analysis
        # based on the collected data
        try:
            # Get all data series from experiment
            data_series = experiment.data_collector.get_all_series()

            # Create simple analysis
            analysis = {
                "experiment_id": experiment.experiment_id,
                "iterations_completed": len(all_results),
                "data_collected": list(data_series.keys()),
                "conclusion": "Experiment completed successfully",
                "confidence": 0.7,  # Default confidence
            }

            # Try to analyze if analyzer supports it
            try:
                # Some analyzers might need results differently
                if hasattr(self.analyzer, "analyze"):
                    analysis.update(self.analyzer.analyze(experiment))
            except Exception:
                pass  # Use simple analysis if analyzer fails
        except Exception as e:
            # Fallback analysis
            analysis = {
                "experiment_id": experiment.experiment_id,
                "iterations_completed": len(all_results),
                "conclusion": f"Experiment completed (analysis error: {e})",
                "confidence": 0.5,
            }

        result = {
            "experiment_id": experiment.experiment_id,
            "hypothesis": hypothesis.statement,
            "initial_state": initial_state_data,
            "final_state": final_state_data,
            "iterations": all_results,
            "analysis": analysis,
            "crystallization_manifest": crystallization_manifest,
            "oracle_enabled": self.oracle_enabled,
            "empirica_session_id": (
                getattr(self.oracle, "_session_id", None)
                or (
                    getattr(self.oracle, "_readiness_status", {}).get("session_id")
                    if hasattr(self.oracle, "_readiness_status")
                    else None
                )
                or (
                    self.oracle.empirica.get_current_session_id()
                    if hasattr(self.oracle.empirica, "get_current_session_id")
                    else None
                )
            )
            if self.oracle_enabled and self.oracle
            else None,
        }

        return result
