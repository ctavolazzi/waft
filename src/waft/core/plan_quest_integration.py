"""
Plan-Quest Integration (Legacy)

DEPRECATED: Use quest_mission_integration.py instead.
This module is kept for backward compatibility.

Automatically creates Quest objects from Plan documents whenever plans are created.
Integrates with TavernKeeper quest system.
"""

import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import frontmatter

    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False


def read_plan_file(plan_path: Path) -> dict[str, Any]:
    """
    Read plan file and extract metadata.

    Args:
        plan_path: Path to plan file

    Returns:
        Dictionary with plan data
    """
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")

    content = plan_path.read_text(encoding="utf-8")

    # Try to parse frontmatter
    plan_data = {
        "path": str(plan_path),
        "id": plan_path.stem,
        "name": plan_path.stem.replace("_", " ").title(),
        "overview": "",
        "todos": [],
        "content": content,
    }

    if FRONTMATTER_AVAILABLE:
        try:
            post = frontmatter.loads(content)
            plan_data.update(post.metadata)
            plan_data["content"] = post.content
        except Exception:
            pass

    # Extract name from frontmatter or first heading
    if "name" not in plan_data or not plan_data["name"]:
        # Try to extract from first heading
        first_heading = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if first_heading:
            plan_data["name"] = first_heading.group(1).strip()

    # Extract overview from frontmatter or first paragraph
    if "overview" not in plan_data or not plan_data["overview"]:
        # Try to extract from content
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith("#"):
                plan_data["overview"] = line.strip()[:200]  # First 200 chars
                break

    # Extract todos from frontmatter or markdown
    if "todos" not in plan_data or not plan_data["todos"]:
        todos = []

        # Try to find todos in frontmatter
        if isinstance(plan_data.get("todos"), list):
            todos = plan_data["todos"]
        else:
            # Try to extract from markdown
            todo_pattern = r"^\s*[-*]\s+\[([ x])\]\s*(.+)$"
            for line in content.split("\n"):
                match = re.match(todo_pattern, line)
                if match:
                    todos.append(
                        {
                            "id": f"todo_{len(todos)}",
                            "content": match.group(2).strip(),
                            "status": "completed" if match.group(1) == "x" else "pending",
                        }
                    )

            # Also try to find todos in YAML frontmatter format
            if not todos:
                todo_yaml_pattern = r"todos:\s*\n((?:\s+-\s+.*\n?)+)"
                match = re.search(todo_yaml_pattern, content)
                if match:
                    # Simple YAML list parsing
                    for line in match.group(1).split("\n"):
                        if line.strip().startswith("-"):
                            todo_content = line.strip()[1:].strip()
                            todos.append(
                                {
                                    "id": f"todo_{len(todos)}",
                                    "content": todo_content,
                                    "status": "pending",
                                }
                            )

        plan_data["todos"] = todos

    return plan_data


def calculate_difficulty(plan_data: dict[str, Any]) -> int:
    """
    Calculate quest difficulty (1-10) based on plan complexity.

    Args:
        plan_data: Plan data dictionary

    Returns:
        Difficulty level (1-10)
    """
    todos_count = len(plan_data.get("todos", []))

    # Base difficulty from todos count
    if todos_count == 0:
        base_difficulty = 1
    else:
        base_difficulty = min(10, max(1, int(math.log10(max(1, todos_count)) * 3) + 1))

    # Complexity bonus from plan sections
    content = plan_data.get("content", "")
    section_count = len(re.findall(r"^##+\s+", content, re.MULTILINE))
    complexity_bonus = min(3, section_count // 3)

    # Dependency penalty (if plan mentions dependencies)
    has_dependencies = bool(re.search(r"dependenc|prerequisite|requires", content, re.IGNORECASE))
    dependency_penalty = 1 if has_dependencies else 0

    # Final difficulty
    final_difficulty = min(10, max(1, base_difficulty + complexity_bonus + dependency_penalty))

    return final_difficulty


def calculate_loot(difficulty: int, plan_data: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate loot/rewards based on difficulty and plan scope.

    Args:
        difficulty: Quest difficulty (1-10)
        plan_data: Plan data dictionary

    Returns:
        Loot table dictionary
    """
    todos_count = len(plan_data.get("todos", []))

    # Base rewards from difficulty
    xp = difficulty * 10
    insight = difficulty * 5
    karma = difficulty * 3

    # Bonus for more todos
    if todos_count > 5:
        xp += (todos_count - 5) * 2
        insight += todos_count - 5

    return {"xp": xp, "insight": insight, "karma": karma}


def create_quest_from_plan(
    plan_path: Path, project_path: Path | None = None, tavern_keeper=None
) -> dict[str, Any]:
    """
    Create a Quest object from a Plan document.

    Args:
        plan_path: Path to plan file
        project_path: Project root path (default: current directory)
        tavern_keeper: Optional TavernKeeper instance

    Returns:
        Quest dictionary
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # Read plan
    plan_data = read_plan_file(plan_path)

    # Calculate difficulty
    difficulty = calculate_difficulty(plan_data)

    # Calculate rewards
    loot = calculate_loot(difficulty, plan_data)

    # Create quest ID
    plan_id = plan_data.get("id", plan_path.stem)
    quest_id = f"quest_{plan_id}"

    # Create quest
    quest = {
        "id": quest_id,
        "name": plan_data.get("name", plan_path.stem),
        "status": "active",
        "description": plan_data.get("overview", "")[:500],  # Truncate to 500 chars
        "difficulty": difficulty,
        "win_condition": "all_todos_complete",
        "loot_table": loot,
        "plan_path": str(plan_path.relative_to(project_path)),
        "plan_id": plan_id,
        "todos": [
            {
                "id": todo.get("id", f"todo_{i}"),
                "content": todo.get("content", str(todo)),
                "status": todo.get("status", "pending"),
            }
            for i, todo in enumerate(plan_data.get("todos", []))
        ],
        "created_at": datetime.now().isoformat(),
        "progress": "0%",
    }

    # Register in TavernKeeper
    if tavern_keeper is None:
        try:
            from ..core.tavern_keeper.keeper import TavernKeeper

            tavern_keeper = TavernKeeper(project_path)
        except Exception:
            # TavernKeeper not available, return quest without registering
            return quest

    try:
        if tavern_keeper.db:
            # Check if quest already exists
            Quest = tavern_keeper.db.table("quests").search(tavern_keeper.db.Query().id == quest_id)
            if not Quest:
                tavern_keeper.db.table("quests").insert(quest)
        else:
            # Use JSON fallback
            if quest_id not in [q.get("id") for q in tavern_keeper._data.get("quests", [])]:
                tavern_keeper._data.setdefault("quests", []).append(quest)
                tavern_keeper._save_json_data()
    except Exception as e:
        # Log error but don't fail
        print(f"⚠️  Warning: Could not register quest in TavernKeeper: {e}")

    return quest


def hook_into_plan_creation(
    plan_path: Path, project_path: Path | None = None
) -> dict[str, Any] | None:
    """
    Hook function to call when a plan is created.

    DEPRECATED: Use quest_mission_integration.hook_into_plan_creation() instead.
    This function now delegates to the new system.

    Args:
        plan_path: Path to newly created plan file
        project_path: Project root path

    Returns:
        Created quest/mission dictionary, or None if creation failed
    """
    # Delegate to new integration system
    try:
        from .quest_mission_integration import hook_into_plan_creation as new_hook

        return new_hook(plan_path, project_path)
    except Exception as e:
        print(f"⚠️  Warning: Could not create quest/mission from plan {plan_path}: {e}")
        return None


def find_all_plans(plans_dir: Path | None = None) -> list[Path]:
    """
    Find all plan files in the plans directory.

    Args:
        plans_dir: Plans directory (default: _work_efforts/Plans/)

    Returns:
        List of plan file paths
    """
    if plans_dir is None:
        plans_dir = Path.cwd() / "_work_efforts" / "Plans"

    if not plans_dir.exists():
        return []

    # Find all .plan.md files
    plans = list(plans_dir.rglob("*.plan.md"))

    return sorted(plans)


def create_quests_for_all_plans(
    plans_dir: Path | None = None,
    project_path: Path | None = None,
    skip_existing: bool = True,
) -> list[dict[str, Any]]:
    """
    Create quests for all existing plans.

    Args:
        plans_dir: Plans directory
        project_path: Project root path
        skip_existing: Skip plans that already have quests

    Returns:
        List of created quest dictionaries
    """
    plans = find_all_plans(plans_dir)
    created_quests = []

    # Get existing quest IDs if skipping
    existing_quest_ids = set()
    if skip_existing:
        try:
            from ..core.tavern_keeper.keeper import TavernKeeper

            tavern = TavernKeeper(project_path or Path.cwd())
            if tavern.db:
                existing_quests = tavern.db.table("quests").all()
                existing_quest_ids = {q.get("id") for q in existing_quests}
            else:
                existing_quests = tavern._data.get("quests", [])
                existing_quest_ids = {q.get("id") for q in existing_quests}
        except Exception:
            pass

    for plan_path in plans:
        plan_id = plan_path.stem
        quest_id = f"quest_{plan_id}"

        if skip_existing and quest_id in existing_quest_ids:
            continue

        quest = hook_into_plan_creation(plan_path, project_path)
        if quest:
            created_quests.append(quest)

    return created_quests
