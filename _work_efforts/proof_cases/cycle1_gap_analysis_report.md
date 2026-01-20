# Cycle 1 Gap Analysis Report

**Created**: 2026-01-18  
**Experiment**: Aeon Anthology Quest Creation - Cycle 1  
**Purpose**: Technical requirements and standards for identified gaps

---

## Executive Summary

This report documents the technical requirements, standards, and strategies for addressing the gaps identified in Cycle 1 observations. The primary gaps are:

1. **Quest-Work Effort Linking**: Missing bidirectional linking mechanism
2. **Development Plan Detail Level**: Need for code examples and API design
3. **Testing Strategy**: Missing integration tests
4. **Documentation Pattern**: Need for standardization

---

## Gap 1: Quest-Work Effort Linking

### Current State

**Quest System**:
- Location: `src/waft/pantheon/fae.py`
- Storage: `_pantheon/fae/quests_registry.json`
- Schema: `id`, `name`, `description`, `fae_guidance`, `difficulty`, `status`, `progress`, `created_at`
- **Missing**: `work_effort_id` field

**Work Effort System**:
- Location: `src/waft/api/services/work_effort_service.py`
- Storage: `_work_efforts/WE-YYMMDD-xxxx/WE-YYMMDD-xxxx_index.md`
- Schema: `id`, `title`, `status`, `created`, `created_by`, `last_updated`, `branch`, `repository`
- **Missing**: `quest_id` field

**MCP Work-Efforts Server**:
- Location: `.mcp-servers/work-efforts/server.js`
- Tool: `create_work_effort`
- Parameters: `repo_path`, `title`, `objective`, `repository`, `tickets`
- **Missing**: `quest_id` parameter

### Technical Requirements

#### 1. Quest Schema Update

**File**: `src/waft/pantheon/fae.py`

**Change**: Add `work_effort_id` to Quest class

```python
class Quest:
    quest_id: str
    name: str
    description: str
    fae_guidance: Optional[str] = None
    difficulty: int
    status: str = "active"
    progress: str = "exploring"
    created_at: Optional[str] = None
    work_effort_id: Optional[str] = None  # NEW FIELD
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.quest_id,
            "name": self.name,
            "description": self.description,
            "fae_guidance": self.fae_guidance,
            "difficulty": self.difficulty,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
            "work_effort_id": self.work_effort_id,  # NEW FIELD
        }
```

**Quest Registry Format**:
```json
{
  "quests": [
    {
      "id": "quest_20260116_082637_the_aeon_anthology:_",
      "name": "The Aeon Anthology: Pantheon-Watched Evolution",
      "work_effort_id": "WE-260116-0t2e",  // NEW FIELD
      ...
    }
  ]
}
```

#### 2. Work Effort Schema Update

**File**: `src/waft/api/schemas/work_efforts.py`

**Change**: Add `quest_id` to request and response models

```python
class WorkEffortCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=10000)
    status: str = Field(default="active")
    tags: List[str] = Field(default_factory=list, max_items=20)
    quest_id: Optional[str] = Field(None, description="Optional quest ID to link")  # NEW FIELD

class WorkEffortResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    tags: List[str]
    created: str
    created_by: Optional[str] = None
    last_updated: str
    path: str
    quest_id: Optional[str] = None  # NEW FIELD
```

**Work Effort Service Update**:

**File**: `src/waft/api/services/work_effort_service.py`

**Change**: Accept and store `quest_id` in `create_work_effort()`

```python
def create_work_effort(
    self,
    title: str,
    description: str = "",
    status: str = "active",
    tags: Optional[List[str]] = None,
    quest_id: Optional[str] = None  # NEW PARAMETER
) -> Dict[str, Any]:
    # ... existing code ...
    
    frontmatter = {
        "id": we_id,
        "title": title,
        "status": status,
        "created": now,
        "created_by": "api",
        "last_updated": now,
        "tags": tags or [],
        "quest_id": quest_id,  # NEW FIELD
    }
    
    # ... rest of method ...
```

**Work Effort Index Template**:

**File**: `_work_efforts/WE-YYMMDD-xxxx/WE-YYMMDD-xxxx_index.md`

**Change**: Add `quest_id` to frontmatter and quest link section

```yaml
---
id: WE-260116-0t2e
title: "The Aeon Anthology: Pantheon-Watched Evolution"
quest_id: "quest_20260116_082637_the_aeon_anthology:_"  # NEW FIELD
status: active
...
---

# WE-260116-0t2e: The Aeon Anthology: Pantheon-Watched Evolution

## Quest Link

- **Quest**: [quest_20260116_082637_the_aeon_anthology:_](../../_pantheon/fae/quests_registry.json)
- **Fae Guidance**: "Across vast stretches of time, beings shall evolve..."

## Metadata
...
```

#### 3. MCP Work-Efforts Server Update

**File**: `.mcp-servers/work-efforts/server.js`

**Change**: Add `quest_id` parameter to `create_work_effort` tool

```javascript
create_work_effort: {
  name: "create_work_effort",
  description: "Create a new work effort",
  inputSchema: {
    type: "object",
    properties: {
      repo_path: { type: "string" },
      title: { type: "string" },
      objective: { type: "string" },
      repository: { type: "string" },
      tickets: { type: "array", items: { type: "string" } },
      quest_id: { type: "string", description: "Optional quest ID to link" },  // NEW FIELD
    },
    required: ["repo_path", "title", "objective", "repository"],
  },
  // ... handler implementation ...
}
```

#### 4. Bidirectional Linking Function

**File**: `src/waft/core/quest_work_effort_linking.py` (NEW)

**Purpose**: Utility functions for bidirectional linking

```python
from pathlib import Path
from typing import Optional
from ..pantheon.fae import Fae
from ..api.services.work_effort_service import WorkEffortService

def link_quest_to_work_effort(
    quest_id: str,
    work_effort_id: str,
    project_path: Optional[Path] = None
) -> bool:
    """
    Create bidirectional link between quest and work effort.
    
    Args:
        quest_id: Quest ID
        work_effort_id: Work Effort ID
        project_path: Project root path
        
    Returns:
        True if linking successful
    """
    if project_path is None:
        project_path = Path.cwd()
    
    # Update quest with work_effort_id
    fae = Fae(project_path)
    quest = fae.get_quest(quest_id)
    if quest:
        quest.work_effort_id = work_effort_id
        # Update quest in registry
        # (Implementation depends on Fae.update_quest() method)
    
    # Update work effort with quest_id
    service = WorkEffortService(project_path)
    work_effort = service.get_work_effort(work_effort_id)
    if work_effort:
        # Update work effort metadata
        # (Implementation depends on WorkEffortService.update_work_effort() method)
    
    return True
```

#### 5. Migration Script

**File**: `scripts/migrate_quest_work_effort_links.py` (NEW)

**Purpose**: Retroactively link existing quest-work effort pairs

```python
"""
Migration script to retroactively link existing quest-work effort pairs.

Scans quest registry and work efforts to identify pairs that should be linked
based on matching names or creation dates.
"""

from pathlib import Path
import json
from datetime import datetime

def find_matching_pairs(project_path: Path):
    """Find quest-work effort pairs that should be linked."""
    # Load quests
    quests_file = project_path / "_pantheon" / "fae" / "quests_registry.json"
    quests = json.load(quests_file.open()).get("quests", [])
    
    # Load work efforts
    work_efforts_path = project_path / "_work_efforts"
    work_efforts = []
    for we_dir in work_efforts_path.glob("WE-*"):
        index_file = we_dir / f"{we_dir.name}_index.md"
        if index_file.exists():
            # Parse frontmatter
            # ... extract work effort data ...
            work_efforts.append(...)
    
    # Match pairs (by name similarity or creation date)
    pairs = []
    for quest in quests:
        for we in work_efforts:
            if should_link(quest, we):
                pairs.append((quest["id"], we["id"]))
    
    return pairs

def should_link(quest: dict, work_effort: dict) -> bool:
    """Determine if quest and work effort should be linked."""
    # Match by name similarity
    quest_name = quest["name"].lower()
    we_title = work_effort["title"].lower()
    
    # Simple matching (can be improved)
    if quest_name in we_title or we_title in quest_name:
        return True
    
    # Match by creation date (same day)
    quest_date = datetime.fromisoformat(quest["created_at"]).date()
    we_date = datetime.fromisoformat(work_effort["created"]).date()
    if quest_date == we_date:
        return True
    
    return False

def main():
    project_path = Path.cwd()
    pairs = find_matching_pairs(project_path)
    
    for quest_id, work_effort_id in pairs:
        link_quest_to_work_effort(quest_id, work_effort_id, project_path)
        print(f"Linked {quest_id} <-> {work_effort_id}")
```

### Implementation Steps

1. **Update Schemas** (1 hour)
   - Add `quest_id` to work effort schema
   - Add `work_effort_id` to quest schema
   - Update request/response models

2. **Update Services** (1 hour)
   - Update `WorkEffortService.create_work_effort()` to accept `quest_id`
   - Update `Fae.create_quest()` to accept `work_effort_id` (optional)
   - Add `Fae.update_quest()` method if missing

3. **Update MCP Server** (30 min)
   - Add `quest_id` parameter to `create_work_effort` tool
   - Update handler to pass `quest_id` to service

4. **Create Linking Utility** (1 hour)
   - Create `quest_work_effort_linking.py` module
   - Implement bidirectional linking function

5. **Update Templates** (30 min)
   - Update work effort index template to include quest link
   - Update quest display to show work effort link

6. **Create Migration Script** (1 hour)
   - Create migration script for existing pairs
   - Run migration for WE-260116-0t2e

**Total Effort**: ~5 hours

---

## Gap 2: Development Plan Detail Level Standards

### Current Standard (Phase 1)

**Appropriate for**: Architecture Design phase

**Includes**:
- High-level component definitions
- Data structure schemas (JSON examples)
- Integration points identified
- Storage structure defined
- CLI commands planned

**Example**: Current `DEVELOPMENT_PLAN.md` for Aeon Anthology

### Enhanced Standard (Phase 2)

**Appropriate for**: Implementation phase

**Additional Requirements**:
- Code examples (skeleton classes)
- API endpoint specifications
- Data flow diagrams
- Error handling specifications

**Code Example Template**:

```markdown
## Code Examples

### Anthology Class

```python
class Anthology:
    """
    Manages collection of stories across Aeons.
    
    Attributes:
        project_path: Path to project root
        anthology_path: Path to anthology storage
    """
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.anthology_path = project_path / "_pantheon" / "anthology"
        self.anthology_path.mkdir(parents=True, exist_ok=True)
    
    def create_story(self, aeon_id: str, being_id: str, evolution_events: List[Dict]) -> str:
        """Create a new anthology story from evolution events."""
        # Implementation here
        pass
    
    def get_stories(self, aeon_id: Optional[str] = None) -> List[Dict]:
        """Get anthology stories, optionally filtered by aeon."""
        # Implementation here
        pass
```
```

**API Design Template**:

```markdown
## API Design

### Endpoints

#### POST /api/anthology/stories

Create a new anthology story.

**Request**:
```json
{
  "aeon_id": "aeon_001",
  "being_id": "being_...",
  "evolution_events": [...],
  "pantheon_observations": [...]
}
```

**Response** (201 Created):
```json
{
  "story_id": "anthology_aeon_001_story_001",
  "aeon_id": "aeon_001",
  "created_at": "2026-01-16T08:26:37Z"
}
```

**Errors**:
- 400 Bad Request: Invalid aeon_id or being_id
- 404 Not Found: Aeon or being not found
- 500 Internal Server Error: Storage failure
```
```

### Standard by Phase

| Phase | Detail Level | Code Examples | API Design | Diagrams |
|-------|-------------|---------------|------------|----------|
| Phase 1: Architecture | High-level | ❌ | ❌ | ❌ |
| Phase 2: Implementation | Detailed | ✅ | ✅ | ✅ |
| Phase 3: Integration | Complete | ✅ | ✅ | ✅ |

---

## Gap 3: Testing Integration Strategy

### Test Structure

**Location**: `tests/test_quest_work_effort_integration.py`

**Test Categories**:

1. **Unit Tests**: Individual component tests
   - Quest creation
   - Work effort creation
   - Linking function

2. **Integration Tests**: Component interaction tests
   - Quest-Work Effort bidirectional linking
   - Automated workflow
   - Error handling

3. **System Tests**: End-to-end workflow tests
   - Full workflow (Quest → Work Effort → Plan → Devlog)
   - Status synchronization
   - Migration script

### Test Examples

**Integration Test**:

```python
import pytest
from pathlib import Path
from waft.pantheon.fae import Fae
from waft.api.services.work_effort_service import WorkEffortService
from waft.core.quest_work_effort_linking import link_quest_to_work_effort

def test_quest_work_effort_bidirectional_linking(tmp_path):
    """Test that quest and work effort can be bidirectionally linked."""
    # Create quest
    fae = Fae(tmp_path)
    quest = fae.create_quest("Test Quest", "Test Description")
    
    # Create work effort with quest_id
    service = WorkEffortService(tmp_path)
    work_effort = service.create_work_effort(
        title="Test Work Effort",
        description="Test",
        quest_id=quest.quest_id
    )
    
    # Link quest to work effort
    link_quest_to_work_effort(quest.quest_id, work_effort["id"], tmp_path)
    
    # Verify bidirectional link
    quest_updated = fae.get_quest(quest.quest_id)
    work_effort_updated = service.get_work_effort(work_effort["id"])
    
    assert quest_updated.work_effort_id == work_effort["id"]
    assert work_effort_updated["quest_id"] == quest.quest_id
```

**System Test**:

```python
def test_full_quest_work_effort_workflow(tmp_path):
    """Test complete workflow: Quest → Work Effort → Plan → Devlog."""
    # Create quest
    fae = Fae(tmp_path)
    quest = fae.create_quest("Test Quest", "Test Description")
    
    # Create work effort
    service = WorkEffortService(tmp_path)
    work_effort = service.create_work_effort(
        title="Test Work Effort",
        description="Test",
        quest_id=quest.quest_id
    )
    
    # Link
    link_quest_to_work_effort(quest.quest_id, work_effort["id"], tmp_path)
    
    # Verify all components exist and are linked
    assert quest.quest_id is not None
    assert work_effort["id"] is not None
    assert (tmp_path / "_work_efforts" / work_effort["id"]).exists()
    assert (tmp_path / "_pantheon" / "fae" / "quests_registry.json").exists()
```

### Test Execution Strategy

**CI/CD Integration**:
- Run unit tests on every commit
- Run integration tests on pull requests
- Run system tests before releases

**Manual Testing**:
- Run validation scripts before releases
- Test migration scripts on staging environment

---

## Gap 4: Documentation Pattern Standardization

### Standard Pattern

**Quest-Work Effort Creation Pattern**:

1. **Create Quest** (via Fae system)
   - Input: Name, description
   - Output: Quest ID, Fae guidance
   - Storage: `_pantheon/fae/quests_registry.json`

2. **Create Work Effort** (via MCP or API)
   - Input: Title, objective, tickets, quest_id
   - Output: Work Effort ID, directory structure
   - Storage: `_work_efforts/WE-YYMMDD-xxxx/`

3. **Link Bidirectionally** (automatic or manual)
   - Update quest with work_effort_id
   - Update work effort with quest_id

4. **Generate Development Plan** (template or manual)
   - Input: Quest context, work effort tickets
   - Output: `DEVELOPMENT_PLAN.md`
   - Storage: `_work_efforts/WE-YYMMDD-xxxx/DEVELOPMENT_PLAN.md`

5. **Update Devlog** (automatic or manual)
   - Input: Quest, work effort, development plan
   - Output: Devlog entry
   - Storage: `_work_efforts/devlog.md`

### Templates

**Development Plan Template**: `templates/development_plan_template.md`

**Devlog Entry Template**: `templates/devlog_entry_template.md`

**Observation Template**: `templates/experiment_observation_template.md`

### Documentation Guide

**Location**: `docs/QUEST_WORK_EFFORT_PATTERN.md`

**Contents**:
- Pattern overview
- Step-by-step guide
- Automation options
- Troubleshooting
- Examples

---

## Implementation Checklist

### Quest-Work Effort Linking
- [ ] Update Quest schema (`src/waft/pantheon/fae.py`)
- [ ] Update Work Effort schema (`src/waft/api/schemas/work_efforts.py`)
- [ ] Update Work Effort service (`src/waft/api/services/work_effort_service.py`)
- [ ] Update MCP server (`.mcp-servers/work-efforts/server.js`)
- [ ] Create linking utility (`src/waft/core/quest_work_effort_linking.py`)
- [ ] Update templates (work effort index, quest display)
- [ ] Create migration script (`scripts/migrate_quest_work_effort_links.py`)
- [ ] Run migration for existing pairs

### Development Plan Standards
- [ ] Define Phase 1 standard (current level)
- [ ] Define Phase 2 standard (with code examples)
- [ ] Create code example template
- [ ] Create API design template
- [ ] Update development plan guide

### Testing Strategy
- [ ] Create integration test file (`tests/test_quest_work_effort_integration.py`)
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Write system tests
- [ ] Integrate into CI/CD pipeline

### Documentation Pattern
- [ ] Create pattern guide (`docs/QUEST_WORK_EFFORT_PATTERN.md`)
- [ ] Create development plan template
- [ ] Create devlog entry template
- [ ] Create observation template
- [ ] Document automation options

---

**Last Updated**: 2026-01-18
