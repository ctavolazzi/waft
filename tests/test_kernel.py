"""Tests for WAFT Kernel."""

from pathlib import Path
from datetime import datetime
from waft.core.kernel import WAFTKernel


def test_kernel_init(temp_project_path):
    """Test WAFTKernel initialization."""
    kernel = WAFTKernel(temp_project_path)
    
    assert kernel.project_path == temp_project_path
    assert kernel.identity == "WAFT_KERNEL"
    assert kernel.mission == "Directed Evolution of Self-Modifying AI Agents"
    assert kernel.goal == "Generate data for 'The Physics of Artificial Cognition'"
    assert kernel.epistemic_phase is None
    assert kernel.boot_time is not None
    assert isinstance(kernel.boot_time, datetime)
    
    # Check integration with existing systems
    assert kernel.empirica is not None
    assert kernel.gamification is not None
    assert kernel.observer is not None


def test_kernel_boot_sequence(temp_project_path):
    """Test kernel boot sequence."""
    kernel = WAFTKernel(temp_project_path)
    boot_status = kernel.boot_sequence()
    
    assert "identity" in boot_status
    assert boot_status["identity"] == "WAFT_KERNEL"
    assert "mission" in boot_status
    assert "goal" in boot_status
    assert "boot_time" in boot_status
    assert "status" in boot_status
    assert "epistemic_state" in boot_status
    assert "epistemic_phase" in boot_status
    
    # Epistemic phase should be set
    assert kernel.epistemic_phase is not None
    assert isinstance(kernel.epistemic_phase, str)


def test_get_epistemic_phase(temp_project_path):
    """Test epistemic phase determination."""
    kernel = WAFTKernel(temp_project_path)
    
    phase = kernel.get_epistemic_phase()
    
    assert isinstance(phase, str)
    assert phase in ["Initialization", "Active Development", "Data Gathering", "Synthesis", "Evolution", "Exploration", "Idle"]


def test_get_epistemic_phase_with_work_efforts(project_with_pyrite):
    """Test epistemic phase with work efforts."""
    # Create some work efforts
    work_efforts_dir = project_with_pyrite / "_work_efforts"
    work_efforts_dir.mkdir(exist_ok=True)
    
    # Create a work effort
    we_dir = work_efforts_dir / "WE-260111-test"
    we_dir.mkdir()
    (we_dir / "WE-260111-test_index.md").write_text("# Test Work Effort")
    
    kernel = WAFTKernel(project_with_pyrite)
    phase = kernel.get_epistemic_phase()
    
    assert isinstance(phase, str)
    # Should detect active work efforts
    assert phase in ["Active Development", "Data Gathering", "Synthesis", "Evolution", "Exploration"]


def test_get_epistemic_state_fallback(temp_project_path):
    """Test epistemic state fallback (when Empirica not initialized)."""
    kernel = WAFTKernel(temp_project_path)
    
    # Empirica should not be initialized in temp project
    assert not kernel.empirica.is_initialized()
    
    state = kernel.get_epistemic_state()
    
    assert "source" in state
    assert state["source"] == "kernel_estimate"
    assert "moon_phase" in state
    assert "knowledge_percentage" in state
    assert "uncertainty_percentage" in state
    assert "coverage" in state
    assert "metrics" in state
    
    # Check moon phase is valid
    assert state["moon_phase"] in ["🌑", "🌒", "🌓", "🌔", "🌕"]


def test_get_epistemic_state_with_structure(project_with_pyrite):
    """Test epistemic state estimation with project structure."""
    # Add some structure
    docs_dir = project_with_pyrite / "docs"
    docs_dir.mkdir()
    (docs_dir / "README.md").write_text("# Docs")
    
    tests_dir = project_with_pyrite / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_something.py").write_text("# Test")
    
    kernel = WAFTKernel(project_with_pyrite)
    state = kernel.get_epistemic_state()
    
    assert state["source"] == "kernel_estimate"
    assert "metrics" in state
    assert state["metrics"]["documentation_files"] >= 0
    assert state["metrics"]["test_files"] >= 0


def test_log_kernel_event(temp_project_path):
    """Test kernel event logging to Flight Recorder."""
    kernel = WAFTKernel(temp_project_path)
    
    # Log an event
    context = {"test": "data", "timestamp": datetime.now().isoformat()}
    kernel.log_kernel_event("KERNEL_TEST", context)
    
    # Check that log file exists
    log_file = kernel.observer.log_file
    assert log_file.exists()
    
    # Read the log to verify event was logged
    events = kernel.observer.get_laboratory_log(limit=10)
    assert len(events) > 0
    
    # Find our test event
    test_event = None
    for event in events:
        if event.get("payload", {}).get("event_type") == "KERNEL_TEST":
            test_event = event
            break
    
    assert test_event is not None
    assert test_event["genome_id"] == "waft_kernel"
    assert test_event["agent_id"] == "waft_kernel"
    assert test_event["payload"]["kernel_event"] is True
    assert test_event["payload"]["event_type"] == "KERNEL_TEST"
    assert test_event["payload"]["test"] == "data"


def test_kernel_status_check(temp_project_path):
    """Test kernel status check."""
    kernel = WAFTKernel(temp_project_path)
    status = kernel.kernel_status_check()
    
    assert "identity" in status
    assert status["identity"] == "WAFT_KERNEL"
    assert "mission" in status
    assert "boot_time" in status
    assert "uptime_seconds" in status
    assert "epistemic_phase" in status
    assert "epistemic_state" in status
    assert "status" in status
    assert "systems" in status
    
    # Check systems integration
    systems = status["systems"]
    assert "flight_recorder" in systems
    assert "empirica" in systems
    assert "gamification" in systems
    
    # Check uptime is reasonable
    assert status["uptime_seconds"] >= 0


def test_get_uptime(temp_project_path):
    """Test kernel uptime calculation."""
    kernel = WAFTKernel(temp_project_path)
    
    uptime = kernel.get_uptime()
    
    assert uptime.total_seconds() >= 0
    assert isinstance(uptime.total_seconds(), float)


def test_perform_status_check(temp_project_path):
    """Test internal status check."""
    kernel = WAFTKernel(temp_project_path)
    status = kernel._perform_status_check()
    
    assert "project_path" in status
    assert "pyrite_exists" in status
    assert "lock_exists" in status
    assert "empirica_initialized" in status
    assert "gamification" in status
    
    # Check gamification data
    assert "integrity" in status["gamification"]
    assert "insight" in status["gamification"]
    assert "level" in status["gamification"]


def test_perform_status_check_with_pyrite(project_with_pyrite):
    """Test status check with _pyrite structure."""
    kernel = WAFTKernel(project_with_pyrite)
    status = kernel._perform_status_check()
    
    assert status["pyrite_exists"] is True


def test_check_git_activity(temp_project_path):
    """Test git activity check."""
    kernel = WAFTKernel(temp_project_path)
    
    # Should return False for temp project without git
    activity = kernel._check_git_activity()
    assert isinstance(activity, bool)


def test_kernel_integration_with_existing_systems(temp_project_path):
    """Test that kernel properly integrates with existing systems."""
    kernel = WAFTKernel(temp_project_path)
    
    # Verify systems are initialized
    assert kernel.empirica.project_path == temp_project_path
    assert kernel.gamification.project_path == temp_project_path
    assert kernel.observer.project_path == temp_project_path
    
    # Verify kernel uses existing systems (not recreates them)
    # Gamification should have default values
    assert kernel.gamification.integrity == 100.0
    assert kernel.gamification.insight == 0.0
    assert kernel.gamification.level == 1


def test_epistemic_state_format_empirica(temp_project_path):
    """Test Empirica state formatting (if Empirica available)."""
    kernel = WAFTKernel(temp_project_path)
    
    # Create mock Empirica context
    mock_context = {
        "epistemic_state": {
            "vectors": {
                "foundation": {
                    "know": 0.7,
                    "do": 0.6,
                    "context": 0.5,
                },
                "engagement": 0.8,
                "uncertainty": 0.2,
            }
        },
        "goals": [],
        "findings": [],
        "unknowns": [],
    }
    
    formatted = kernel._format_empirica_state(mock_context)
    
    assert formatted["source"] == "empirica"
    assert "moon_phase" in formatted
    assert formatted["knowledge_percentage"] == 70.0
    assert formatted["uncertainty_percentage"] == 20.0
    assert "coverage" in formatted
    assert "vectors" in formatted
    assert "goals" in formatted
    assert "findings" in formatted
    assert "unknowns" in formatted


def test_epistemic_state_estimate(temp_project_path):
    """Test epistemic state estimation."""
    kernel = WAFTKernel(temp_project_path)
    
    estimated = kernel._estimate_epistemic_state()
    
    assert estimated["source"] == "kernel_estimate"
    assert "moon_phase" in estimated
    assert "knowledge_percentage" in estimated
    assert "uncertainty_percentage" in estimated
    assert "coverage" in estimated
    assert "metrics" in estimated
    
    # Check metrics structure
    metrics = estimated["metrics"]
    assert "work_efforts" in metrics
    assert "documentation_files" in metrics
    assert "test_files" in metrics
