"""
Cartographer API endpoint - Bob the Cartographer's work data.
"""

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


def parse_markdown_metadata(content: str) -> dict[str, Any]:
    """Parse YAML frontmatter from markdown file."""
    metadata = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value
    return metadata


def extract_bob_data(project_path: Path) -> dict[str, Any]:
    """
    Extract Bob the Cartographer's work data from _pyrite files.

    Returns:
        Dictionary with Bob's information, skills, APIs, and work
    """
    pyrite_path = project_path / "_pyrite" / "active"

    if not pyrite_path.exists():
        return {"found": False, "message": "No _pyrite/active directory found"}

    # Find Bob's files
    bob_files = {}
    being_id = "being_20260113_003031_c29056ab"

    # Look for Bob-related files
    for file_path in pyrite_path.glob("*BOB*.md"):
        bob_files[file_path.stem] = file_path

    for file_path in pyrite_path.glob("*bob*.md"):
        bob_files[file_path.stem] = file_path

    # Also check for being spawn file
    being_file = pyrite_path / f"BEING_SPAWN_{being_id}.md"
    if being_file.exists():
        bob_files["being_spawn"] = being_file

    # Check for repository map
    repo_map_file = pyrite_path / "REPOSITORY_MAP_public-apis_20260113.md"
    if repo_map_file.exists():
        bob_files["repository_map"] = repo_map_file

    # Check for evolution file
    evolution_file = pyrite_path / "BOB_EVOLUTION_API_ACCESS_20260113.md"
    if evolution_file.exists():
        bob_files["evolution"] = evolution_file

    if not bob_files:
        return {"found": False, "message": "No Bob the Cartographer files found"}

    # Parse files
    bob_data = {
        "found": True,
        "being_id": being_id,
        "name": "Bob the Cartographer",
        "role": "Cartographer",
        "files": {},
        "skills": {},
        "apis": [],
        "work": [],
    }

    # Parse being spawn file
    if "being_spawn" in bob_files:
        content = bob_files["being_spawn"].read_text()
        metadata = parse_markdown_metadata(content)
        bob_data["spawned"] = metadata.get("Spawned", "")
        bob_data["reality"] = metadata.get("Reality", "")

        # Extract skills from content
        if "## Skills" in content:
            skills_section = content.split("## Skills")[1].split("##")[0]
            # Look for skill patterns
            skill_pattern = r"(\w+):\s*([\d.]+)"
            matches = re.findall(skill_pattern, skills_section)
            for skill_name, level in matches:
                bob_data["skills"][skill_name] = float(level)

    # Parse evolution file
    if "evolution" in bob_files:
        content = bob_files["evolution"].read_text()
        metadata = parse_markdown_metadata(content)

        # Extract API information
        if "## API Chosen" in content:
            api_section = content.split("## API Chosen")[1].split("##")[0]
            api_name_match = re.search(r"\*\*([^*]+)\*\*", api_section)
            if api_name_match:
                api_name = api_name_match.group(1).strip()

                # Extract API details
                api_data = {
                    "name": api_name,
                    "url": "",
                    "type": "",
                    "auth": "",
                    "https": False,
                    "cors": False,
                }

                url_match = re.search(r"\*\*URL\*\*:\s*([^\n]+)", api_section)
                if url_match:
                    api_data["url"] = url_match.group(1).strip()

                type_match = re.search(r"\*\*Type\*\*:\s*([^\n]+)", api_section)
                if type_match:
                    api_data["type"] = type_match.group(1).strip()

                auth_match = re.search(r"\*\*Authentication\*\*:\s*([^\n]+)", api_section)
                if auth_match:
                    api_data["auth"] = auth_match.group(1).strip()

                https_match = re.search(r"\*\*HTTPS\*\*:\s*([^\n]+)", api_section)
                if https_match:
                    api_data["https"] = https_match.group(1).strip().lower() == "yes"

                cors_match = re.search(r"\*\*CORS\*\*:\s*([^\n]+)", api_section)
                if cors_match:
                    api_data["cors"] = cors_match.group(1).strip().lower() == "yes"

                bob_data["apis"].append(api_data)

        # Extract skills from evolution
        if "## Skills Evolved" in content:
            skills_section = content.split("## Skills Evolved")[1].split("##")[0]
            skill_pattern = r"(\d+)\.\s*\*\*([^*]+)\*\*:\s*Level\s*([\d.]+)"
            matches = re.findall(skill_pattern, skills_section)
            for _, skill_name, level in matches:
                bob_data["skills"][skill_name.strip()] = float(level)

    # Parse repository map
    if "repository_map" in bob_files:
        content = bob_files["repository_map"].read_text()
        metadata = parse_markdown_metadata(content)

        bob_data["work"].append(
            {
                "type": "repository_mapping",
                "title": "Mapped public-apis Repository",
                "date": metadata.get("Mapping Date", ""),
                "repository": "https://github.com/public-apis/public-apis",
                "categories": 51,
                "description": "Comprehensive mapping of 51 API categories",
            }
        )

    # Check for API module
    api_module_path = (
        project_path / "src" / "waft" / "core" / "cartographer" / "bob_cartographer_api.py"
    )
    if api_module_path.exists():
        content = api_module_path.read_text()
        bob_data["code"] = {
            "module": str(api_module_path.relative_to(project_path)),
            "lines": len(content.split("\n")),
            "has_geocoding": "geocode_address" in content,
            "has_reverse_geocoding": "reverse_geocode" in content,
            "has_place_search": "search_place" in content,
        }

    return bob_data


@router.get("/cartographer")
async def get_cartographer_data(request: Request) -> dict[str, Any]:
    """
    Get Bob the Cartographer's work data.

    Returns:
        Bob's information including skills, APIs, and work history
    """
    project_path: Path = request.app.state.project_path
    try:
        bob_data = extract_bob_data(project_path)
        return bob_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting Bob's data: {str(e)}")
