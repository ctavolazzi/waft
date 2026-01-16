"""
Quest/Mission Integration

Automatically creates Quest (Fae-guided) or Mission (Military Brass) objects
from Plan documents based on plan characteristics.

Quests = Open-ended, whimsical, creative (Right brain, Fae)
Missions = Serious, structured, documented (Left brain, Military Brass)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False


def read_plan_file(plan_path: Path) -> Dict[str, Any]:
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
        "type": "quest"  # Default to quest (open-ended)
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
        first_heading = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if first_heading:
            plan_data["name"] = first_heading.group(1).strip()
    
    # Extract overview
    if "overview" not in plan_data or not plan_data["overview"]:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#'):
                plan_data["overview"] = line.strip()[:200]
                break
    
    # Extract todos
    if "todos" not in plan_data or not plan_data["todos"]:
        todos = []
        todo_pattern = r'^\s*[-*]\s+\[([ x])\]\s*(.+)$'
        for line in content.split('\n'):
            match = re.match(todo_pattern, line)
            if match:
                todos.append({
                    "id": f"todo_{len(todos)}",
                    "content": match.group(2).strip(),
                    "status": "completed" if match.group(1) == "x" else "pending"
                })
        plan_data["todos"] = todos
    
    # Determine type: quest (whimsical) or mission (serious)
    plan_data["type"] = determine_plan_type(plan_data)
    
    return plan_data


def determine_plan_type(plan_data: Dict[str, Any]) -> str:
    """
    Determine if plan should be a quest (whimsical) or mission (serious).
    
    Args:
        plan_data: Plan data dictionary
        
    Returns:
        "quest" or "mission"
    """
    content = (plan_data.get("content", "") + " " + plan_data.get("overview", "")).lower()
    name = plan_data.get("name", "").lower()
    
    # Mission indicators (serious, structured)
    mission_keywords = [
        "secure", "security", "production", "deploy", "critical", "compliance",
        "regulatory", "audit", "certification", "standard", "protocol", "procedure",
        "implementation", "system", "infrastructure", "architecture", "serious",
        "mission", "structured", "documented", "accountable"
    ]
    
    # Quest indicators (whimsical, open-ended)
    quest_keywords = [
        "explore", "experiment", "discover", "creative", "artistic", "whimsical",
        "playful", "fun", "curious", "wonder", "magic", "fae", "quest", "open-ended",
        "see what happens", "let's try", "maybe", "perhaps", "could be"
    ]
    
    # Check explicit type in metadata
    if plan_data.get("type") in ["mission", "serious"]:
        return "mission"
    if plan_data.get("type") in ["quest", "whimsical", "exploratory"]:
        return "quest"
    
    # Count keywords
    mission_count = sum(1 for keyword in mission_keywords if keyword in content or keyword in name)
    quest_count = sum(1 for keyword in quest_keywords if keyword in content or keyword in name)
    
    # Default to mission if has success criteria or structured todos
    if plan_data.get("success_criteria") or len(plan_data.get("todos", [])) > 5:
        mission_count += 2
    
    # Default to quest if very short or vague
    if len(plan_data.get("overview", "")) < 50:
        quest_count += 1
    
    # Decide based on counts
    if mission_count > quest_count:
        return "mission"
    else:
        return "quest"


def create_quest_from_plan(
    plan_path: Path,
    project_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Create a Quest (Fae-guided) from a Plan document.
    
    Args:
        plan_path: Path to plan file
        project_path: Project root path
        
    Returns:
        Quest dictionary
    """
    if project_path is None:
        project_path = Path.cwd()
    
    from ..pantheon.fae import Fae
    
    # Read plan
    plan_data = read_plan_file(plan_path)
    
    # Create Fae instance
    fae = Fae(project_path)
    
    # Create quest
    quest = fae.create_quest(
        name=plan_data.get("name", plan_path.stem),
        description=plan_data.get("overview", ""),
        difficulty=None  # Auto-calculate
    )
    
    return quest.to_dict()


def create_mission_from_plan(
    plan_path: Path,
    project_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Create a Mission (Military Brass) from a Plan document.
    
    Args:
        plan_path: Path to plan file
        project_path: Project root path
        
    Returns:
        Mission dictionary and PDF path
    """
    if project_path is None:
        project_path = Path.cwd()
    
    from ..pantheon.military_brass import MilitaryBrass
    from .mission_pdf_generator import generate_mission_pdf
    
    # Read plan
    plan_data = read_plan_file(plan_path)
    
    # Extract success criteria from todos
    success_criteria = [
        todo.get("content", str(todo))
        for todo in plan_data.get("todos", [])
    ]
    
    # Create Military Brass instance
    brass = MilitaryBrass(project_path)
    
    # Create mission
    mission = brass.create_mission(
        name=plan_data.get("name", plan_path.stem),
        objective=plan_data.get("overview", ""),
        classification=plan_data.get("classification", "INTERNAL"),
        briefing=plan_data.get("content", "")[:1000],  # First 1000 chars
        success_criteria=success_criteria,
        difficulty=None  # Auto-calculate
    )
    
    # Generate mission PDF
    pdf_path = generate_mission_pdf(mission, project_path)
    
    return {
        "mission": mission.to_dict(),
        "pdf_path": str(pdf_path)
    }


def hook_into_plan_creation(
    plan_path: Path,
    project_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Hook function to call when a plan is created.
    Automatically determines if plan should be quest or mission.
    
    Args:
        plan_path: Path to newly created plan file
        project_path: Project root path
        
    Returns:
        Dictionary with created quest/mission info
    """
    try:
        plan_data = read_plan_file(plan_path)
        plan_type = determine_plan_type(plan_data)
        
        if plan_type == "mission":
            result = create_mission_from_plan(plan_path, project_path)
            return {
                "type": "mission",
                "data": result["mission"],
                "pdf_path": result["pdf_path"]
            }
        else:
            result = create_quest_from_plan(plan_path, project_path)
            return {
                "type": "quest",
                "data": result
            }
    except Exception as e:
        print(f"⚠️  Warning: Could not create quest/mission from plan {plan_path}: {e}")
        return {"type": "error", "error": str(e)}
