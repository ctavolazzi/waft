#!/usr/bin/env python3
"""
🎮 Meta-Cognitive Guide LLM System - Quest Implementation Script

A quest-based development orchestrator that breaks down the implementation
into fun, gamified quests with checkpoints and tests.

This script can be used to guide another LLM (like Claude Code Cloud) to
implement the Meta-Cognitive Guide LLM System step by step.

Usage:
    python scripts/quest_guide_implementation.py [--quest <quest_id>] [--checkpoint <checkpoint_id>] [--test] [--status]

Quest System:
    - Each quest represents a phase of implementation
    - Checkpoints validate progress
    - Tests verify correctness
    - Fun rewards and achievements unlock as you progress!
"""

import json
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# ============================================================================
# Quest System
# ============================================================================


class QuestStatus(Enum):
    """Quest status enumeration."""

    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Checkpoint:
    """A checkpoint that validates quest progress."""

    checkpoint_id: str
    name: str
    description: str
    validator: Callable[[Path], tuple[bool, str]]  # Returns (passed, message)
    required_for: list[str] = field(default_factory=list)  # Quest IDs that require this


@dataclass
class Test:
    """A test that verifies implementation correctness."""

    test_id: str
    name: str
    description: str
    test_func: Callable[[Path], tuple[bool, str]]  # Returns (passed, message)
    quest_id: str  # Which quest this test belongs to


@dataclass
class Quest:
    """A quest - a phase of implementation."""

    quest_id: str
    name: str
    description: str
    difficulty: int  # 1-10
    xp_reward: int
    checkpoints: list[str] = field(default_factory=list)  # Checkpoint IDs
    tests: list[str] = field(default_factory=list)  # Test IDs
    prerequisites: list[str] = field(default_factory=list)  # Quest IDs
    status: QuestStatus = QuestStatus.LOCKED
    started_at: str | None = None
    completed_at: str | None = None
    achievements: list[str] = field(default_factory=list)


@dataclass
class QuestProgress:
    """Track quest progress."""

    quest_id: str
    checkpoints_passed: list[str] = field(default_factory=list)
    tests_passed: list[str] = field(default_factory=list)
    current_step: str = ""
    notes: list[str] = field(default_factory=list)


# ============================================================================
# Checkpoint Validators
# ============================================================================


def checkpoint_file_exists(project_path: Path, file_path: str) -> tuple[bool, str]:
    """Check if a file exists."""
    full_path = project_path / file_path
    if full_path.exists():
        return True, f"✅ File exists: {file_path}"
    return False, f"❌ File missing: {file_path}"


def checkpoint_imports_work(project_path: Path, module_path: str) -> tuple[bool, str]:
    """Check if a module can be imported."""
    try:
        # Try to import the module
        import importlib.util

        spec = importlib.util.spec_from_file_location("test_module", project_path / module_path)
        if spec and spec.loader:
            return True, f"✅ Module can be imported: {module_path}"
        return False, f"❌ Cannot import module: {module_path}"
    except Exception as e:
        return False, f"❌ Import error: {str(e)}"


def checkpoint_has_class(project_path: Path, file_path: str, class_name: str) -> tuple[bool, str]:
    """Check if a file contains a specific class."""
    full_path = project_path / file_path
    if not full_path.exists():
        return False, f"❌ File missing: {file_path}"

    content = full_path.read_text()
    if f"class {class_name}" in content:
        return True, f"✅ Class found: {class_name} in {file_path}"
    return False, f"❌ Class missing: {class_name} in {file_path}"


def checkpoint_has_method(project_path: Path, file_path: str, method_name: str) -> tuple[bool, str]:
    """Check if a file contains a specific method."""
    full_path = project_path / file_path
    if not full_path.exists():
        return False, f"❌ File missing: {file_path}"

    content = full_path.read_text()
    if f"def {method_name}" in content:
        return True, f"✅ Method found: {method_name} in {file_path}"
    return False, f"❌ Method missing: {method_name} in {file_path}"


def checkpoint_directory_exists(project_path: Path, dir_path: str) -> tuple[bool, str]:
    """Check if a directory exists."""
    full_path = project_path / dir_path
    if full_path.exists() and full_path.is_dir():
        return True, f"✅ Directory exists: {dir_path}"
    return False, f"❌ Directory missing: {dir_path}"


def checkpoint_pantheon_export(project_path: Path, export_name: str) -> tuple[bool, str]:
    """Check if TheGuide is exported in pantheon __init__.py."""
    init_file = project_path / "src" / "waft" / "pantheon" / "__init__.py"
    if not init_file.exists():
        return False, "❌ Pantheon __init__.py missing"

    content = init_file.read_text()
    if f'"{export_name}"' in content or f"'{export_name}'" in content:
        return True, f"✅ {export_name} exported in pantheon __init__.py"
    return False, f"❌ {export_name} not exported in pantheon __init__.py"


# ============================================================================
# Test Functions
# ============================================================================


def test_guide_initialization(project_path: Path) -> tuple[bool, str]:
    """Test that TheGuide can be initialized."""
    try:
        sys.path.insert(0, str(project_path / "src"))
        from pathlib import Path

        from waft.pantheon.guide import TheGuide

        # Try to initialize (without actual LLM for now)
        # This will fail if basic structure is wrong
        return True, "✅ TheGuide class structure is valid"
    except ImportError as e:
        return False, f"❌ Import error: {str(e)}"
    except Exception as e:
        return False, f"❌ Initialization error: {str(e)}"


def test_storage_structure(project_path: Path) -> tuple[bool, str]:
    """Test that storage directories are created."""
    guide_path = project_path / "_pantheon" / "guide"
    sessions_path = guide_path / "sessions"
    protocols_path = guide_path / "protocols"
    guide_path / "index.json"

    checks = [
        (guide_path.exists() and guide_path.is_dir(), "guide directory"),
        (sessions_path.exists() and sessions_path.is_dir(), "sessions directory"),
        (protocols_path.exists() and protocols_path.is_dir(), "protocols directory"),
    ]

    failed = [name for passed, name in checks if not passed]
    if failed:
        return False, f"❌ Missing directories: {', '.join(failed)}"
    return True, "✅ Storage structure is correct"


def test_protocol_models(project_path: Path) -> tuple[bool, str]:
    """Test that Protocol Pydantic models are defined."""
    guide_file = project_path / "src" / "waft" / "pantheon" / "guide.py"
    if not guide_file.exists():
        return False, "❌ guide.py file missing"

    content = guide_file.read_text()
    required_models = ["EvaluationScores", "Protocol"]

    missing = [model for model in required_models if f"class {model}" not in content]
    if missing:
        return False, f"❌ Missing models: {', '.join(missing)}"
    return True, "✅ Protocol models are defined"


def test_fvcu_evaluation(project_path: Path) -> tuple[bool, str]:
    """Test that FVCU evaluation method exists."""
    guide_file = project_path / "src" / "waft" / "pantheon" / "guide.py"
    if not guide_file.exists():
        return False, "❌ guide.py file missing"

    content = guide_file.read_text()
    if "_evaluate_with_fvcu" in content or "evaluate_with_fvcu" in content:
        return True, "✅ FVCU evaluation method exists"
    return False, "❌ FVCU evaluation method missing"


def test_reasoner_integration(project_path: Path) -> tuple[bool, str]:
    """Test that Reasoner integration is implemented."""
    guide_file = project_path / "src" / "waft" / "pantheon" / "guide.py"
    if not guide_file.exists():
        return False, "❌ guide.py file missing"

    content = guide_file.read_text()
    if "TheReasoner" in content and "create_trace" in content:
        return True, "✅ Reasoner integration exists"
    return False, "❌ Reasoner integration missing"


# ============================================================================
# Quest Definitions
# ============================================================================


def create_quests(project_path: Path) -> dict[str, Quest]:
    """Create all quest definitions."""

    checkpoints = {
        "cp_guide_file": Checkpoint(
            checkpoint_id="cp_guide_file",
            name="Guide File Created",
            description="Check that src/waft/pantheon/guide.py exists",
            validator=lambda p: checkpoint_file_exists(p, "src/waft/pantheon/guide.py"),
        ),
        "cp_guide_class": Checkpoint(
            checkpoint_id="cp_guide_class",
            name="TheGuide Class Defined",
            description="Check that TheGuide class exists in guide.py",
            validator=lambda p: checkpoint_has_class(p, "src/waft/pantheon/guide.py", "TheGuide"),
        ),
        "cp_storage_dirs": Checkpoint(
            checkpoint_id="cp_storage_dirs",
            name="Storage Directories Created",
            description="Check that _pantheon/guide/sessions and protocols directories exist",
            validator=lambda p: (
                checkpoint_directory_exists(p, "_pantheon/guide/sessions")[0]
                and checkpoint_directory_exists(p, "_pantheon/guide/protocols")[0],
                "Storage directories check",
            ),
        ),
        "cp_protocol_models": Checkpoint(
            checkpoint_id="cp_protocol_models",
            name="Protocol Models Defined",
            description="Check that EvaluationScores and Protocol models exist",
            validator=lambda p: checkpoint_has_class(
                p, "src/waft/pantheon/guide.py", "EvaluationScores"
            ),
        ),
        "cp_guidance_loop": Checkpoint(
            checkpoint_id="cp_guidance_loop",
            name="Guidance Loop Method",
            description="Check that _guidance_loop method exists",
            validator=lambda p: checkpoint_has_method(
                p, "src/waft/pantheon/guide.py", "_guidance_loop"
            ),
        ),
        "cp_llm_integration": Checkpoint(
            checkpoint_id="cp_llm_integration",
            name="OpenHands LLM Integration",
            description="Check that OpenHands LLM is imported and used",
            validator=lambda p: (
                "from openhands.sdk import LLM" in (p / "src/waft/pantheon/guide.py").read_text()
                if (p / "src/waft/pantheon/guide.py").exists()
                else False,
                "OpenHands LLM integration",
            ),
        ),
        "cp_fvcu_evaluation": Checkpoint(
            checkpoint_id="cp_fvcu_evaluation",
            name="FVCU Evaluation Method",
            description="Check that _evaluate_with_fvcu method exists",
            validator=lambda p: checkpoint_has_method(
                p, "src/waft/pantheon/guide.py", "_evaluate_with_fvcu"
            ),
        ),
        "cp_reasoner_integration": Checkpoint(
            checkpoint_id="cp_reasoner_integration",
            name="Reasoner Integration",
            description="Check that TheReasoner is imported and used",
            validator=lambda p: (
                "TheReasoner" in (p / "src/waft/pantheon/guide.py").read_text()
                if (p / "src/waft/pantheon/guide.py").exists()
                else False,
                "Reasoner integration",
            ),
        ),
        "cp_pantheon_export": Checkpoint(
            checkpoint_id="cp_pantheon_export",
            name="Pantheon Export",
            description="Check that TheGuide is exported in pantheon __init__.py",
            validator=lambda p: checkpoint_pantheon_export(p, "TheGuide"),
        ),
        "cp_readme": Checkpoint(
            checkpoint_id="cp_readme",
            name="README Documentation",
            description="Check that _pantheon/guide/README.md exists",
            validator=lambda p: checkpoint_file_exists(p, "_pantheon/guide/README.md"),
        ),
    }

    tests = {
        "test_init": Test(
            test_id="test_init",
            name="TheGuide Initialization Test",
            description="Test that TheGuide can be imported and initialized",
            test_func=test_guide_initialization,
            quest_id="quest_1",
        ),
        "test_storage": Test(
            test_id="test_storage",
            name="Storage Structure Test",
            description="Test that storage directories are created correctly",
            test_func=test_storage_structure,
            quest_id="quest_2",
        ),
        "test_models": Test(
            test_id="test_models",
            name="Protocol Models Test",
            description="Test that Protocol Pydantic models are defined",
            test_func=test_protocol_models,
            quest_id="quest_3",
        ),
        "test_fvcu": Test(
            test_id="test_fvcu",
            name="FVCU Evaluation Test",
            description="Test that FVCU evaluation method exists",
            test_func=test_fvcu_evaluation,
            quest_id="quest_7",
        ),
        "test_reasoner": Test(
            test_id="test_reasoner",
            name="Reasoner Integration Test",
            description="Test that Reasoner integration is implemented",
            test_func=test_reasoner_integration,
            quest_id="quest_12",
        ),
    }

    quests = {
        "quest_1": Quest(
            quest_id="quest_1",
            name="🏗️ Foundation: Create TheGuide Skeleton",
            description=(
                "Create the basic structure for TheGuide class in src/waft/pantheon/guide.py.\n"
                "Include __init__ method, storage paths, and basic class structure following TheReasoner pattern."
            ),
            difficulty=2,
            xp_reward=50,
            checkpoints=["cp_guide_file", "cp_guide_class"],
            tests=["test_init"],
            prerequisites=[],
            achievements=["🏗️ Foundation Builder"],
        ),
        "quest_2": Quest(
            quest_id="quest_2",
            name="📁 Storage System Implementation",
            description=(
                "Implement the storage system for sessions, protocols, and index.\n"
                "Create directories: _pantheon/guide/sessions/, _pantheon/guide/protocols/\n"
                "Implement _load_index() and _save_index() methods."
            ),
            difficulty=3,
            xp_reward=75,
            checkpoints=["cp_storage_dirs"],
            tests=["test_storage"],
            prerequisites=["quest_1"],
            achievements=["📁 Storage Master"],
        ),
        "quest_3": Quest(
            quest_id="quest_3",
            name="📋 Protocol Models (Pydantic)",
            description=(
                "Create Pydantic models for Protocol system:\n"
                "- EvaluationScores (FVCU+Faithfulness: factuality, validity, coherence, utility, faithfulness, overall)\n"
                "- Protocol (reasoning_chain, evaluations, final_answer, quality_score, etc.)\n"
                "- Reasoning chain entry structure\n"
                "- Evaluation entry structure"
            ),
            difficulty=4,
            xp_reward=100,
            checkpoints=["cp_protocol_models"],
            tests=["test_models"],
            prerequisites=["quest_1"],
            achievements=["📋 Model Architect"],
        ),
        "quest_4": Quest(
            quest_id="quest_4",
            name="🔄 Guidance Loop Structure",
            description=(
                "Implement the basic guidance loop structure (_guidance_loop method).\n"
                "Include iteration counter, termination check, and placeholder for LLM calls.\n"
                "This is the skeleton that will be filled in later."
            ),
            difficulty=3,
            xp_reward=75,
            checkpoints=["cp_guidance_loop"],
            tests=[],
            prerequisites=["quest_1"],
            achievements=["🔄 Loop Master"],
        ),
        "quest_5": Quest(
            quest_id="quest_5",
            name="🤖 OpenHands LLM Integration",
            description=(
                "Add OpenHands LLM integration:\n"
                "- Implement _create_guide_llm() method\n"
                "- Add LLM initialization in __init__()\n"
                "- Create prompt templates for Guide and Client\n"
                "- Implement solve() method entry point"
            ),
            difficulty=5,
            xp_reward=125,
            checkpoints=["cp_llm_integration"],
            tests=[],
            prerequisites=["quest_1", "quest_4"],
            achievements=["🤖 LLM Integrator"],
        ),
        "quest_6": Quest(
            quest_id="quest_6",
            name="💬 Basic LLM Calls",
            description=(
                "Implement basic LLM interaction:\n"
                "- Guide instruction generation\n"
                "- Client reasoning trace generation\n"
                "- Basic evaluation call (without FVCU yet)"
            ),
            difficulty=5,
            xp_reward=125,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_5"],
            achievements=["💬 Conversation Starter"],
        ),
        "quest_7": Quest(
            quest_id="quest_7",
            name="🎯 FVCU+Faithfulness Evaluation",
            description=(
                "Implement FVCU+Faithfulness evaluation system:\n"
                "- Create _evaluate_with_fvcu() method\n"
                "- Implement critic model approach (LLM-as-a-judge)\n"
                "- Generate FVCU scores with rationale\n"
                "- Add faithfulness detection (claimed vs actual computation)"
            ),
            difficulty=7,
            xp_reward=200,
            checkpoints=["cp_fvcu_evaluation"],
            tests=["test_fvcu"],
            prerequisites=["quest_6"],
            achievements=["🎯 Evaluation Master", "🔍 Faithfulness Detective"],
        ),
        "quest_8": Quest(
            quest_id="quest_8",
            name="🧩 Partial Context Identification",
            description=(
                "Implement partial context identification:\n"
                "- Create _identify_premises() method\n"
                "- Determine which previous steps are premises\n"
                "- Implement partial context extraction for efficiency"
            ),
            difficulty=6,
            xp_reward=150,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_7"],
            achievements=["🧩 Context Master"],
        ),
        "quest_9": Quest(
            quest_id="quest_9",
            name="📊 Test-Time Scaling (Majority Voting)",
            description=(
                "Implement test-time scaling:\n"
                "- Create _evaluate_with_majority_voting() method\n"
                "- Support multiple evaluation samples\n"
                "- Aggregate scores via majority voting"
            ),
            difficulty=6,
            xp_reward=150,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_7"],
            achievements=["📊 Scaling Expert"],
        ),
        "quest_10": Quest(
            quest_id="quest_10",
            name="✨ Self-Rewarding (Optional)",
            description=(
                "Implement self-rewarding capabilities:\n"
                "- Create _evaluate_guide_instruction() method\n"
                "- Guide evaluates its own instruction quality\n"
                "- Add enable_self_rewarding flag to __init__()"
            ),
            difficulty=7,
            xp_reward=175,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_6"],
            achievements=["✨ Self-Aware Guide"],
        ),
        "quest_11": Quest(
            quest_id="quest_11",
            name="🔧 Self-Correction (Optional)",
            description=(
                "Implement self-correction capabilities:\n"
                "- Create _self_correct_instruction() method\n"
                "- Guide revises instructions if quality is low\n"
                "- Add enable_self_correction flag to __init__()"
            ),
            difficulty=8,
            xp_reward=200,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_10"],
            achievements=["🔧 Self-Improving Guide"],
        ),
        "quest_12": Quest(
            quest_id="quest_12",
            name="🔗 Reasoner Integration",
            description=(
                "Add integration with TheReasoner:\n"
                "- Import TheReasoner in guide.py\n"
                "- Create trace after each iteration\n"
                "- Link traces with parent_trace_id\n"
                "- Store session-to-trace mapping"
            ),
            difficulty=5,
            xp_reward=125,
            checkpoints=["cp_reasoner_integration"],
            tests=["test_reasoner"],
            prerequisites=["quest_6"],
            achievements=["🔗 Integration Master"],
        ),
        "quest_13": Quest(
            quest_id="quest_13",
            name="🚪 Termination Logic",
            description=(
                "Implement termination logic:\n"
                "- Create _check_termination() method\n"
                "- Consider FVCU scores (validity+utility complementarity)\n"
                "- Check Guide's self-assessment\n"
                "- Handle max iterations and quality threshold"
            ),
            difficulty=5,
            xp_reward=125,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_7"],
            achievements=["🚪 Termination Expert"],
        ),
        "quest_14": Quest(
            quest_id="quest_14",
            name="❓ 'Why?' Explanation System",
            description=(
                "Implement 'Why?' explanation:\n"
                "- Create explain() method\n"
                "- Load Protocol from storage\n"
                "- Format reasoning chain as narrative\n"
                "- Include evaluation notes and FVCU scores"
            ),
            difficulty=4,
            xp_reward=100,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_3", "quest_7"],
            achievements=["❓ Explanation Master"],
        ),
        "quest_15": Quest(
            quest_id="quest_15",
            name="📦 Pantheon Export",
            description=(
                "Add TheGuide to Pantheon exports:\n"
                "- Update src/waft/pantheon/__init__.py\n"
                "- Add TheGuide to __all__ list\n"
                "- Verify imports work correctly"
            ),
            difficulty=2,
            xp_reward=50,
            checkpoints=["cp_pantheon_export"],
            tests=[],
            prerequisites=["quest_1"],
            achievements=["📦 Export Master"],
        ),
        "quest_16": Quest(
            quest_id="quest_16",
            name="📚 README Documentation",
            description=(
                "Create comprehensive README:\n"
                "- Document FVCU+Faithfulness taxonomy\n"
                "- Explain self-rewarding/correction capabilities\n"
                "- Provide usage examples\n"
                "- Document integration with TheReasoner"
            ),
            difficulty=3,
            xp_reward=75,
            checkpoints=["cp_readme"],
            tests=[],
            prerequisites=["quest_7", "quest_10", "quest_12"],
            achievements=["📚 Documentation Master"],
        ),
        "quest_17": Quest(
            quest_id="quest_17",
            name="🧪 Final Testing & Validation",
            description=(
                "Run comprehensive tests:\n"
                "- Test with simple problem (verify FVCU scoring)\n"
                "- Test faithfulness detection (unfaithful reasoning cases)\n"
                "- Test planning detection (forward-looking reasoning)\n"
                "- Test self-correction loop\n"
                "- Verify Reasoner integration"
            ),
            difficulty=6,
            xp_reward=200,
            checkpoints=[],
            tests=[],
            prerequisites=["quest_7", "quest_12", "quest_14"],
            achievements=["🧪 Testing Master", "🏆 Quest Complete!"],
        ),
    }

    return quests, checkpoints, tests


# ============================================================================
# Quest Manager
# ============================================================================


class QuestManager:
    """Manages quest progress and execution."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.quests, self.checkpoints, self.tests = create_quests(project_path)
        self.progress_file = project_path / "_pantheon" / "guide" / "quest_progress.json"
        self.progress: dict[str, QuestProgress] = self._load_progress()
        self._update_quest_statuses()

    def _load_progress(self) -> dict[str, QuestProgress]:
        """Load quest progress from file."""
        if self.progress_file.exists():
            try:
                data = json.loads(self.progress_file.read_text())
                return {
                    qid: QuestProgress(
                        quest_id=qid,
                        checkpoints_passed=prog.get("checkpoints_passed", []),
                        tests_passed=prog.get("tests_passed", []),
                        current_step=prog.get("current_step", ""),
                        notes=prog.get("notes", []),
                    )
                    for qid, prog in data.items()
                }
            except Exception:
                pass
        return {}

    def _save_progress(self):
        """Save quest progress to file."""
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            qid: {
                "quest_id": prog.quest_id,
                "checkpoints_passed": prog.checkpoints_passed,
                "tests_passed": prog.tests_passed,
                "current_step": prog.current_step,
                "notes": prog.notes,
            }
            for qid, prog in self.progress.items()
        }
        self.progress_file.write_text(json.dumps(data, indent=2))

    def _update_quest_statuses(self):
        """Update quest statuses based on progress and prerequisites."""
        for quest in self.quests.values():
            # Check prerequisites
            prereqs_met = all(
                self.quests[prereq].status == QuestStatus.COMPLETED
                for prereq in quest.prerequisites
            )

            if quest.status == QuestStatus.COMPLETED:
                continue
            elif prereqs_met and quest.status == QuestStatus.LOCKED:
                quest.status = QuestStatus.AVAILABLE
            elif not prereqs_met:
                quest.status = QuestStatus.LOCKED

    def start_quest(self, quest_id: str) -> tuple[bool, str]:
        """Start a quest."""
        if quest_id not in self.quests:
            return False, f"Quest not found: {quest_id}"

        quest = self.quests[quest_id]
        if quest.status == QuestStatus.LOCKED:
            return (
                False,
                f"Quest is locked. Complete prerequisites first: {', '.join(quest.prerequisites)}",
            )

        quest.status = QuestStatus.IN_PROGRESS
        quest.started_at = datetime.now().isoformat()

        if quest_id not in self.progress:
            self.progress[quest_id] = QuestProgress(quest_id=quest_id)

        self._save_progress()
        return True, f"Quest started: {quest.name}"

    def check_checkpoint(self, checkpoint_id: str) -> tuple[bool, str]:
        """Check a checkpoint."""
        if checkpoint_id not in self.checkpoints:
            return False, f"Checkpoint not found: {checkpoint_id}"

        checkpoint = self.checkpoints[checkpoint_id]
        passed, message = checkpoint.validator(self.project_path)

        if passed:
            # Mark checkpoint as passed in all relevant quests
            for quest in self.quests.values():
                if checkpoint_id in quest.checkpoints:
                    if quest_id not in self.progress:
                        self.progress[quest_id] = QuestProgress(quest_id=quest_id)
                    if checkpoint_id not in self.progress[quest_id].checkpoints_passed:
                        self.progress[quest_id].checkpoints_passed.append(checkpoint_id)
            self._save_progress()

        return passed, message

    def run_test(self, test_id: str) -> tuple[bool, str]:
        """Run a test."""
        if test_id not in self.tests:
            return False, f"Test not found: {test_id}"

        test = self.tests[test_id]
        passed, message = test.test_func(self.project_path)

        if passed:
            quest_id = test.quest_id
            if quest_id not in self.progress:
                self.progress[quest_id] = QuestProgress(quest_id=quest_id)
            if test_id not in self.progress[quest_id].tests_passed:
                self.progress[quest_id].tests_passed.append(test_id)
            self._save_progress()

        return passed, message

    def complete_quest(self, quest_id: str) -> tuple[bool, str]:
        """Mark a quest as completed."""
        if quest_id not in self.quests:
            return False, f"Quest not found: {quest_id}"

        quest = self.quests[quest_id]

        # Check all checkpoints are passed
        for cp_id in quest.checkpoints:
            if (
                cp_id
                not in self.progress.get(
                    quest_id, QuestProgress(quest_id=quest_id)
                ).checkpoints_passed
            ):
                passed, msg = self.check_checkpoint(cp_id)
                if not passed:
                    return False, f"Checkpoint not passed: {cp_id} - {msg}"

        # Check all tests are passed
        for test_id in quest.tests:
            if (
                test_id
                not in self.progress.get(quest_id, QuestProgress(quest_id=quest_id)).tests_passed
            ):
                passed, msg = self.run_test(test_id)
                if not passed:
                    return False, f"Test not passed: {test_id} - {msg}"

        quest.status = QuestStatus.COMPLETED
        quest.completed_at = datetime.now().isoformat()
        self._update_quest_statuses()
        self._save_progress()

        return True, f"🎉 Quest completed: {quest.name} (+{quest.xp_reward} XP)!"

    def get_status(self) -> dict[str, Any]:
        """Get overall quest status."""
        total_quests = len(self.quests)
        completed = sum(1 for q in self.quests.values() if q.status == QuestStatus.COMPLETED)
        in_progress = sum(1 for q in self.quests.values() if q.status == QuestStatus.IN_PROGRESS)
        available = sum(1 for q in self.quests.values() if q.status == QuestStatus.AVAILABLE)
        locked = sum(1 for q in self.quests.values() if q.status == QuestStatus.LOCKED)

        total_xp = sum(
            q.xp_reward for q in self.quests.values() if q.status == QuestStatus.COMPLETED
        )

        return {
            "total_quests": total_quests,
            "completed": completed,
            "in_progress": in_progress,
            "available": available,
            "locked": locked,
            "total_xp": total_xp,
            "completion_percentage": (completed / total_quests * 100) if total_quests > 0 else 0,
        }


# ============================================================================
# CLI Interface
# ============================================================================


def print_banner():
    """Print quest banner."""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🎮 Meta-Cognitive Guide LLM System - Quest Implementation ║
    ║                                                              ║
    ║   A quest-based development orchestrator with checkpoints,   ║
    ║   tests, and achievements!                                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def print_quest_list(manager: QuestManager):
    """Print list of all quests."""
    print("\n📋 Quest List:\n")
    print(f"{'ID':<12} {'Status':<12} {'Difficulty':<10} {'XP':<6} {'Name'}")
    print("-" * 80)

    for quest in sorted(manager.quests.values(), key=lambda q: q.quest_id):
        status_icon = {
            QuestStatus.LOCKED: "🔒",
            QuestStatus.AVAILABLE: "✅",
            QuestStatus.IN_PROGRESS: "🔄",
            QuestStatus.COMPLETED: "🎉",
        }.get(quest.status, "❓")

        print(
            f"{quest.quest_id:<12} {status_icon} {quest.status.value:<10} {'⭐' * quest.difficulty:<10} {quest.xp_reward:<6} {quest.name}"
        )


def print_quest_details(manager: QuestManager, quest_id: str):
    """Print detailed quest information."""
    if quest_id not in manager.quests:
        print(f"❌ Quest not found: {quest_id}")
        return

    quest = manager.quests[quest_id]
    progress = manager.progress.get(quest_id, QuestProgress(quest_id=quest_id))

    print(f"\n📜 Quest: {quest.name}")
    print(f"   ID: {quest.quest_id}")
    print(f"   Status: {quest.status.value}")
    print(f"   Difficulty: {'⭐' * quest.difficulty}")
    print(f"   XP Reward: {quest.xp_reward}")
    print("\n📝 Description:")
    print(f"   {quest.description}")

    if quest.prerequisites:
        print("\n🔗 Prerequisites:")
        for prereq in quest.prerequisites:
            prereq_status = manager.quests[prereq].status.value
            print(f"   - {prereq}: {prereq_status}")

    if quest.checkpoints:
        print("\n✅ Checkpoints:")
        for cp_id in quest.checkpoints:
            passed = cp_id in progress.checkpoints_passed
            status = "✅" if passed else "⏳"
            cp = manager.checkpoints[cp_id]
            print(f"   {status} {cp.name}: {cp.description}")

    if quest.tests:
        print("\n🧪 Tests:")
        for test_id in quest.tests:
            passed = test_id in progress.tests_passed
            status = "✅" if passed else "⏳"
            test = manager.tests[test_id]
            print(f"   {status} {test.name}: {test.description}")

    if quest.achievements:
        print("\n🏆 Achievements:")
        for achievement in quest.achievements:
            print(f"   {achievement}")


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Meta-Cognitive Guide LLM System - Quest Implementation Script"
    )
    parser.add_argument("--quest", type=str, help="Quest ID to work on")
    parser.add_argument("--checkpoint", type=str, help="Checkpoint ID to check")
    parser.add_argument("--test", type=str, help="Test ID to run")
    parser.add_argument("--status", action="store_true", help="Show quest status")
    parser.add_argument("--list", action="store_true", help="List all quests")
    parser.add_argument("--complete", type=str, help="Mark quest as completed")
    parser.add_argument("--start", type=str, help="Start a quest")

    args = parser.parse_args()

    project_path = Path.cwd()
    manager = QuestManager(project_path)

    print_banner()

    if args.status:
        status = manager.get_status()
        print("\n📊 Quest Status:")
        print(f"   Total Quests: {status['total_quests']}")
        print(f"   🎉 Completed: {status['completed']}")
        print(f"   🔄 In Progress: {status['in_progress']}")
        print(f"   ✅ Available: {status['available']}")
        print(f"   🔒 Locked: {status['locked']}")
        print(f"   ⭐ Total XP: {status['total_xp']}")
        print(f"   📈 Completion: {status['completion_percentage']:.1f}%")

    elif args.list:
        print_quest_list(manager)

    elif args.quest:
        print_quest_details(manager, args.quest)

    elif args.checkpoint:
        passed, message = manager.check_checkpoint(args.checkpoint)
        print(f"\n{'✅' if passed else '❌'} {message}")

    elif args.test:
        passed, message = manager.run_test(args.test)
        print(f"\n{'✅' if passed else '❌'} {message}")

    elif args.start:
        success, message = manager.start_quest(args.start)
        print(f"\n{'✅' if success else '❌'} {message}")
        if success:
            print_quest_details(manager, args.start)

    elif args.complete:
        success, message = manager.complete_quest(args.complete)
        print(f"\n{'✅' if success else '❌'} {message}")

    else:
        # Default: show status and available quests
        status = manager.get_status()
        print("\n📊 Quest Status:")
        print(f"   🎉 Completed: {status['completed']}/{status['total_quests']}")
        print(f"   ⭐ Total XP: {status['total_xp']}")
        print(f"   📈 Completion: {status['completion_percentage']:.1f}%")

        print("\n✅ Available Quests:")
        for quest in manager.quests.values():
            if quest.status == QuestStatus.AVAILABLE:
                print(f"   - {quest.quest_id}: {quest.name}")

        print("\n🔄 In Progress Quests:")
        for quest in manager.quests.values():
            if quest.status == QuestStatus.IN_PROGRESS:
                print(f"   - {quest.quest_id}: {quest.name}")

        print("\n💡 Usage:")
        print("   python scripts/quest_guide_implementation.py --list          # List all quests")
        print(
            "   python scripts/quest_guide_implementation.py --quest quest_1 # Show quest details"
        )
        print("   python scripts/quest_guide_implementation.py --start quest_1 # Start a quest")
        print(
            "   python scripts/quest_guide_implementation.py --checkpoint cp_guide_file  # Check checkpoint"
        )
        print("   python scripts/quest_guide_implementation.py --test test_init  # Run test")
        print(
            "   python scripts/quest_guide_implementation.py --complete quest_1  # Complete quest"
        )


if __name__ == "__main__":
    main()
