"""
Quest Guide API endpoints.

Provides REST API for the Meta-Cognitive Guide LLM System quest implementation.
"""

import importlib.util
import sys
from pathlib import Path

# Import the quest system
# We need to import from the scripts directory
from pathlib import Path as PathLib
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel


def _load_quest_manager():
    """Dynamically load QuestManager from scripts directory."""
    # From src/waft/api/routes/quests.py, go up 4 levels to project root
    project_root = PathLib(__file__).parent.parent.parent.parent.parent
    script_path = project_root / "scripts" / "quest_guide_implementation.py"

    # Add scripts to path temporarily
    scripts_dir = str(project_root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    try:
        spec = importlib.util.spec_from_file_location("quest_guide_implementation", script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.QuestManager, module.QuestStatus, module.QuestProgress
        else:
            raise ImportError(f"Could not load quest_guide_implementation from {script_path}")
    except Exception as e:
        raise ImportError(f"Failed to import quest system: {e}")


QuestManager, QuestStatus, QuestProgress = _load_quest_manager()

router = APIRouter(prefix="/api/quests", tags=["quests"])


# ============================================================================
# Pydantic Schemas
# ============================================================================


class QuestStatusResponse(BaseModel):
    """Quest status response."""

    status: str
    total_quests: int
    completed: int
    in_progress: int
    available: int
    locked: int
    total_xp: int
    completion_percentage: float


class CheckpointResponse(BaseModel):
    """Checkpoint response."""

    checkpoint_id: str
    name: str
    description: str
    passed: bool
    message: str


class TestResponse(BaseModel):
    """Test response."""

    test_id: str
    name: str
    description: str
    passed: bool
    message: str


class QuestResponse(BaseModel):
    """Quest response model."""

    quest_id: str
    name: str
    description: str
    difficulty: int
    xp_reward: int
    status: str
    prerequisites: list[str]
    checkpoints: list[str]
    tests: list[str]
    achievements: list[str]
    started_at: str | None = None
    completed_at: str | None = None
    progress: dict[str, Any] | None = None


class QuestListResponse(BaseModel):
    """Quest list response."""

    quests: list[QuestResponse]
    total: int


class QuestStartResponse(BaseModel):
    """Quest start response."""

    success: bool
    message: str
    quest: QuestResponse | None = None


class QuestCompleteResponse(BaseModel):
    """Quest complete response."""

    success: bool
    message: str
    xp_earned: int = 0
    achievements_unlocked: list[str] = []


class CheckpointCheckResponse(BaseModel):
    """Checkpoint check response."""

    passed: bool
    message: str
    checkpoint_id: str


class TestRunResponse(BaseModel):
    """Test run response."""

    passed: bool
    message: str
    test_id: str


# ============================================================================
# Helper Functions
# ============================================================================


def get_quest_manager(request: Request) -> QuestManager:
    """Get QuestManager instance from request."""
    project_path: Path = request.app.state.project_path
    return QuestManager(project_path)


def quest_to_response(quest, manager: QuestManager) -> QuestResponse:
    """Convert Quest object to response model."""
    progress = manager.progress.get(quest.quest_id, QuestProgress(quest_id=quest.quest_id))

    return QuestResponse(
        quest_id=quest.quest_id,
        name=quest.name,
        description=quest.description,
        difficulty=quest.difficulty,
        xp_reward=quest.xp_reward,
        status=quest.status.value,
        prerequisites=quest.prerequisites,
        checkpoints=quest.checkpoints,
        tests=quest.tests,
        achievements=quest.achievements,
        started_at=quest.started_at,
        completed_at=quest.completed_at,
        progress={
            "checkpoints_passed": progress.checkpoints_passed,
            "tests_passed": progress.tests_passed,
            "current_step": progress.current_step,
            "notes": progress.notes,
        }
        if progress
        else None,
    )


# ============================================================================
# API Endpoints
# ============================================================================


@router.get("/status", response_model=QuestStatusResponse)
async def get_quest_status(request: Request):
    """
    Get overall quest system status.

    Returns summary of quest progress, XP earned, and completion percentage.
    """
    manager = get_quest_manager(request)
    status_data = manager.get_status()

    return QuestStatusResponse(status="active", **status_data)


@router.get("", response_model=QuestListResponse)
async def list_quests(request: Request, status_filter: str | None = None):
    """
    List all quests.

    Optionally filter by status: locked, available, in_progress, completed
    """
    manager = get_quest_manager(request)

    quests = []
    for quest in manager.quests.values():
        if status_filter and quest.status.value != status_filter:
            continue
        quests.append(quest_to_response(quest, manager))

    return QuestListResponse(quests=sorted(quests, key=lambda q: q.quest_id), total=len(quests))


@router.get("/{quest_id}", response_model=QuestResponse)
async def get_quest(quest_id: str, request: Request):
    """
    Get detailed information about a specific quest.

    Includes description, prerequisites, checkpoints, tests, and progress.
    """
    manager = get_quest_manager(request)

    if quest_id not in manager.quests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quest not found: {quest_id}"
        )

    quest = manager.quests[quest_id]
    return quest_to_response(quest, manager)


@router.post("/{quest_id}/start", response_model=QuestStartResponse)
async def start_quest(quest_id: str, request: Request):
    """
    Start a quest.

    Marks the quest as in_progress and records the start time.
    """
    manager = get_quest_manager(request)

    if quest_id not in manager.quests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quest not found: {quest_id}"
        )

    success, message = manager.start_quest(quest_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    quest = manager.quests[quest_id]
    return QuestStartResponse(
        success=True, message=message, quest=quest_to_response(quest, manager)
    )


@router.post("/{quest_id}/complete", response_model=QuestCompleteResponse)
async def complete_quest(quest_id: str, request: Request):
    """
    Complete a quest.

    Validates all checkpoints and tests are passed, then marks quest as completed.
    Returns XP earned and achievements unlocked.
    """
    manager = get_quest_manager(request)

    if quest_id not in manager.quests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quest not found: {quest_id}"
        )

    quest = manager.quests[quest_id]

    # Check all checkpoints
    for cp_id in quest.checkpoints:
        passed, msg = manager.check_checkpoint(cp_id)
        if not passed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Checkpoint not passed: {cp_id} - {msg}",
            )

    # Check all tests
    for test_id in quest.tests:
        passed, msg = manager.run_test(test_id)
        if not passed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Test not passed: {test_id} - {msg}",
            )

    # Complete the quest
    success, message = manager.complete_quest(quest_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    return QuestCompleteResponse(
        success=True,
        message=message,
        xp_earned=quest.xp_reward,
        achievements_unlocked=quest.achievements,
    )


@router.post("/checkpoints/{checkpoint_id}/check", response_model=CheckpointCheckResponse)
async def check_checkpoint(checkpoint_id: str, request: Request):
    """
    Check a specific checkpoint.

    Validates that the checkpoint requirement is met.
    """
    manager = get_quest_manager(request)

    if checkpoint_id not in manager.checkpoints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Checkpoint not found: {checkpoint_id}"
        )

    passed, message = manager.check_checkpoint(checkpoint_id)

    return CheckpointCheckResponse(passed=passed, message=message, checkpoint_id=checkpoint_id)


@router.post("/tests/{test_id}/run", response_model=TestRunResponse)
async def run_test(test_id: str, request: Request):
    """
    Run a specific test.

    Executes the test and returns the result.
    """
    manager = get_quest_manager(request)

    if test_id not in manager.tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Test not found: {test_id}"
        )

    passed, message = manager.run_test(test_id)

    return TestRunResponse(passed=passed, message=message, test_id=test_id)


@router.get("/checkpoints/{checkpoint_id}", response_model=CheckpointResponse)
async def get_checkpoint(checkpoint_id: str, request: Request):
    """
    Get checkpoint information.

    Returns checkpoint details and current status.
    """
    manager = get_quest_manager(request)

    if checkpoint_id not in manager.checkpoints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Checkpoint not found: {checkpoint_id}"
        )

    checkpoint = manager.checkpoints[checkpoint_id]
    passed, message = manager.check_checkpoint(checkpoint_id)

    return CheckpointResponse(
        checkpoint_id=checkpoint.checkpoint_id,
        name=checkpoint.name,
        description=checkpoint.description,
        passed=passed,
        message=message,
    )


@router.get("/tests/{test_id}", response_model=TestResponse)
async def get_test(test_id: str, request: Request):
    """
    Get test information.

    Returns test details and runs the test to get current status.
    """
    manager = get_quest_manager(request)

    if test_id not in manager.tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Test not found: {test_id}"
        )

    test = manager.tests[test_id]
    passed, message = manager.run_test(test_id)

    return TestResponse(
        test_id=test.test_id,
        name=test.name,
        description=test.description,
        passed=passed,
        message=message,
    )


@router.get("/{quest_id}/checkpoints", response_model=list[CheckpointResponse])
async def get_quest_checkpoints(quest_id: str, request: Request):
    """
    Get all checkpoints for a quest.

    Returns list of checkpoints with their current status.
    """
    manager = get_quest_manager(request)

    if quest_id not in manager.quests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quest not found: {quest_id}"
        )

    quest = manager.quests[quest_id]
    progress = manager.progress.get(quest_id, QuestProgress(quest_id=quest_id))

    checkpoints = []
    for cp_id in quest.checkpoints:
        if cp_id not in manager.checkpoints:
            continue

        checkpoint = manager.checkpoints[cp_id]
        passed = cp_id in progress.checkpoints_passed
        if not passed:
            passed, msg = manager.check_checkpoint(cp_id)

        checkpoints.append(
            CheckpointResponse(
                checkpoint_id=checkpoint.checkpoint_id,
                name=checkpoint.name,
                description=checkpoint.description,
                passed=passed,
                message=msg if not passed else f"✅ {checkpoint.name} passed",
            )
        )

    return checkpoints


@router.get("/{quest_id}/tests", response_model=list[TestResponse])
async def get_quest_tests(quest_id: str, request: Request):
    """
    Get all tests for a quest.

    Returns list of tests with their current status.
    """
    manager = get_quest_manager(request)

    if quest_id not in manager.quests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Quest not found: {quest_id}"
        )

    quest = manager.quests[quest_id]
    progress = manager.progress.get(quest_id, QuestProgress(quest_id=quest_id))

    tests = []
    for test_id in quest.tests:
        if test_id not in manager.tests:
            continue

        test = manager.tests[test_id]
        passed = test_id in progress.tests_passed
        if not passed:
            passed, msg = manager.run_test(test_id)
        else:
            msg = f"✅ {test.name} passed"

        tests.append(
            TestResponse(
                test_id=test.test_id,
                name=test.name,
                description=test.description,
                passed=passed,
                message=msg,
            )
        )

    return tests
