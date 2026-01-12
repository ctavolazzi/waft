#!/usr/bin/env python3
"""
Setup D&D 5e AI Exploration Work Efforts

Creates work efforts for each GitHub repository in the D&D 5e AI exploration initiative.
Clones the installation exploration template and customizes it for each project.

Usage:
    python3 scripts/setup_dnd5e_exploration.py
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import random
import string

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
WORK_EFFORTS_DIR = PROJECT_ROOT / "_work_efforts"
TEMPLATE_DIR = WORK_EFFORTS_DIR / "WE-260111-6vzd_github_project_installation_exploration_template"
PARENT_WORK_EFFORT = WORK_EFFORTS_DIR / "WE-260111-jpw1_dnd5e_ai_exploration_initiative"

# GitHub URLs to explore
GITHUB_URLS = [
    {
        "url": "https://github.com/foundryvtt/dnd5e",
        "name": "foundryvtt-dnd5e",
        "category": "Core D&D 5e",
        "priority": "HIGH"
    },
    {
        "url": "https://github.com/5e-bits/5e-database",
        "name": "5e-database",
        "category": "Core D&D 5e",
        "priority": "HIGH"
    },
    {
        "url": "https://github.com/EllatharTheHalfling/DnD-Books/blob/master/5e/Books/D%26D%205E%20-%20Dungeon%20Master's%20Guide.pdf",
        "name": "dnd-books-pdf",
        "category": "Core D&D 5e",
        "priority": "LOW",
        "note": "PDF resource, not installation project"
    },
    {
        "url": "https://github.com/QuitoTactico/DnD-AI",
        "name": "dnd-ai-quito",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/ctavolazzi/AI-DnD",
        "name": "ai-dnd-user",
        "category": "AI D&D Tools",
        "priority": "HIGH",
        "note": "User's own repository"
    },
    {
        "url": "https://github.com/fedefreak92/dungeon-master-ai-project",
        "name": "dungeon-master-ai",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/chungs10/dnd-ai",
        "name": "dnd-ai-chung",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/deckofdmthings/GameMasterAI",
        "name": "gamemaster-ai",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/raeleus/Hashtag-DnD",
        "name": "hashtag-dnd",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/Tsinx/aidnd",
        "name": "aidnd-tsinx",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
    {
        "url": "https://github.com/mfreeman451/dd-chatgpt-dm",
        "name": "chatgpt-dm",
        "category": "AI D&D Tools",
        "priority": "MEDIUM"
    },
]


def generate_work_effort_id() -> str:
    """Generate a random 4-character work effort ID."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))


def extract_repo_info(url: str) -> Tuple[str, str]:
    """Extract owner and repo name from GitHub URL."""
    # Handle different URL formats
    patterns = [
        r'github\.com/([^/]+)/([^/?#]+)',
        r'github\.com/([^/]+)/([^/?#]+)/blob',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            owner = match.group(1)
            repo = match.group(2)
            return owner, repo
    
    # Fallback
    return "unknown", "unknown"


def create_work_effort(project_info: Dict, work_effort_id: str) -> Path:
    """Create a work effort for a project."""
    # Create work effort directory
    work_effort_name = f"WE-260111-{work_effort_id}_{project_info['name']}_installation_exploration"
    work_effort_dir = WORK_EFFORTS_DIR / work_effort_name
    work_effort_dir.mkdir(exist_ok=True)
    
    print(f"📦 Creating work effort: {work_effort_name}")
    
    # Copy template files
    files_to_copy = [
        "INSTALLATION_EXPLORATION.md",
        "README.md",
    ]
    
    for file_name in files_to_copy:
        src = TEMPLATE_DIR / file_name
        if src.exists():
            dst = work_effort_dir / file_name
            shutil.copy2(src, dst)
            print(f"  ✅ Copied: {file_name}")
    
    # Copy tools directory
    tools_src = TEMPLATE_DIR / "tools"
    tools_dst = work_effort_dir / "tools"
    if tools_src.exists():
        shutil.copytree(tools_src, tools_dst, dirs_exist_ok=True)
        print(f"  ✅ Copied: tools/")
    
    # Extract repo info
    owner, repo = extract_repo_info(project_info['url'])
    
    # Create index file
    index_content = f"""---
id: WE-260111-{work_effort_id}
title: "{project_info['name'].replace('-', ' ').title()} Installation Exploration"
status: pending
created: {datetime.now().isoformat()}
created_by: ctavolazzi
last_updated: {datetime.now().isoformat()}
branch: main
repository: waft
---

# WE-260111-{work_effort_id}: {project_info['name'].replace('-', ' ').title()} Installation Exploration

## Metadata
- **Created**: {datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p %Z')}
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: main
- **Status**: Pending

## Objective
Explore and document the installation process for {project_info['name']}. Learn how to install, configure, and run the project.

## Project Information

**GitHub URL**: `{project_info['url']}`  
**Project Name**: `{project_info['name']}`  
**Repository Owner**: `{owner}`  
**Repository Name**: `{repo}`  
**Category**: {project_info['category']}  
**Priority**: {project_info['priority']}  
**Language/Stack**: [To be determined]

{f"**Note**: {project_info.get('note', '')}" if project_info.get('note') else ""}

## Tools Available

**Tool Bag Location**: `tools/`

See `tools/README.md` for complete tool bag documentation.

**Essential Tools**:
- ✅ `work_effort_tracker.md` - Progress tracking
- ✅ `verification_checklist.md` - Verification checklist
- ✅ `README.md` - Tool bag documentation

**Project-Specific Tools**:
- ✅ `INSTALLATION_EXPLORATION.md` - Installation exploration template

## Documentation

### Installation Exploration
- **`INSTALLATION_EXPLORATION.md`** - Complete installation exploration process and findings

### Progress Tracking
- **`tools/work_effort_tracker.md`** - Track progress, status, and milestones

## Exploration Process

1. **Initial Analysis**
   - [ ] Read README.md
   - [ ] Identify project type and stack
   - [ ] Note installation instructions
   - [ ] Identify dependencies

2. **Environment Setup**
   - [ ] Check system requirements
   - [ ] Install required dependencies
   - [ ] Set up development environment (if applicable)

3. **Installation Attempt**
   - [ ] Follow installation instructions
   - [ ] Document each step
   - [ ] Note any errors or issues
   - [ ] Capture error messages and solutions

4. **Verification**
   - [ ] Verify installation success
   - [ ] Test basic functionality
   - [ ] Document verification steps

5. **Documentation**
   - [ ] Complete installation exploration document
   - [ ] Update work effort tracker
   - [ ] Create summary of findings

## Key Findings

*(To be populated during exploration)*

## Challenges Encountered

*(To be populated during exploration)*

## Next Steps

1. Explore repository on GitHub web interface
2. Read README and documentation
3. Follow installation exploration process
4. Document findings

## Related

- Parent Work Effort: `WE-260111-jpw1_dnd5e_ai_exploration_initiative`
- Template: `WE-260111-6vzd_github_project_installation_exploration_template`

---

**Status**: Pending - Ready for exploration
"""
    
    index_file = work_effort_dir / f"WE-260111-{work_effort_id}_index.md"
    index_file.write_text(index_content)
    print(f"  ✅ Created: {index_file.name}")
    
    # Update INSTALLATION_EXPLORATION.md with project info
    exploration_file = work_effort_dir / "INSTALLATION_EXPLORATION.md"
    if exploration_file.exists():
        content = exploration_file.read_text()
        content = content.replace("[PROJECT_NAME]", project_info['name'])
        content = content.replace("[GITHUB_URL]", project_info['url'])
        content = content.replace("[OWNER]", owner)
        content = content.replace("[REPO_NAME]", repo)
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
        exploration_file.write_text(content)
        print(f"  ✅ Updated: INSTALLATION_EXPLORATION.md")
    
    return work_effort_dir


def update_parent_work_effort(work_efforts: List[Dict]):
    """Update parent work effort with list of created work efforts."""
    index_file = PARENT_WORK_EFFORT / "WE-260111-jpw1_index.md"
    if not index_file.exists():
        print(f"⚠️  Parent work effort index not found: {index_file}")
        return
    
    content = index_file.read_text()
    
    # Create work efforts table
    table_rows = []
    for we in work_efforts:
        table_rows.append(
            f"| {we['name']} | WE-260111-{we['id']} | {we['status']} | {we['priority']} |"
        )
    
    table = "| Project | Work Effort ID | Status | Priority |\n"
    table += "|--------|----------------|--------|----------|\n"
    table += "\n".join(table_rows)
    
    # Replace the work efforts table
    pattern = r'\| Project \| Work Effort ID \| Status \| Priority \|\n\|--------\|----------------\|--------\|\n\| \(To be populated by script\) \| \| \| \|'
    replacement = table
    content = re.sub(pattern, replacement, content)
    
    index_file.write_text(content)
    print(f"✅ Updated parent work effort index")


def main():
    """Main function to create all work efforts."""
    print("🚀 Setting up D&D 5e AI Exploration Work Efforts\n")
    
    if not TEMPLATE_DIR.exists():
        print(f"❌ Template directory not found: {TEMPLATE_DIR}")
        print("   Please ensure the template work effort exists.")
        return 1
    
    if not PARENT_WORK_EFFORT.exists():
        print(f"❌ Parent work effort not found: {PARENT_WORK_EFFORT}")
        print("   Please ensure the parent work effort exists.")
        return 1
    
    print(f"📋 Template: {TEMPLATE_DIR.name}")
    print(f"📋 Parent: {PARENT_WORK_EFFORT.name}\n")
    
    created_work_efforts = []
    
    for project_info in GITHUB_URLS:
        work_effort_id = generate_work_effort_id()
        
        try:
            work_effort_dir = create_work_effort(project_info, work_effort_id)
            created_work_efforts.append({
                "id": work_effort_id,
                "name": project_info['name'],
                "status": "pending",
                "priority": project_info['priority'],
                "dir": work_effort_dir
            })
            print()
        except Exception as e:
            print(f"  ❌ Error creating work effort: {e}\n")
            continue
    
    # Update parent work effort
    if created_work_efforts:
        update_parent_work_effort(created_work_efforts)
    
    print(f"\n✅ Setup complete!")
    print(f"   Created {len(created_work_efforts)} work efforts")
    print(f"   Parent work effort: {PARENT_WORK_EFFORT.name}")
    print(f"\n📖 Next steps:")
    print(f"   1. Review created work efforts")
    print(f"   2. Begin web exploration of repositories")
    print(f"   3. Start installation exploration for prioritized projects")
    
    return 0


if __name__ == "__main__":
    exit(main())
