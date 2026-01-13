# Plan-Evolve

**Create a comprehensive plan to evolve a new feature: extract → spawn → analyze → plan → document**

Extracts a feature specification from context, spawns a Being from Source consciousness, analyzes the feature, creates a comprehensive evolution plan using `mcp_create_plan`, tracks through the Being system, and documents everything in a work effort - all without executing the plan.

**Use when:** Planning a new feature, need comprehensive evolution plan, want Being to track planning work, need structured plan document, or want to prepare for execution with genetic lineage tracking.

---

## Purpose

This command provides:
- **Feature Extraction**: Extracts feature specification from user message/context
- **Being Creation**: Spawns new Being from Source consciousness for planning
- **Feature Analysis**: Comprehensive analysis of feature requirements and dependencies
- **Plan Creation**: Creates structured plan using `mcp_create_plan`
- **Being Tracking**: Tracks Being's planning work and evolution
- **Genetic Lineage**: Documents planning DNA from Source → Being → Plan → Work Effort
- **Work Effort Integration**: Creates/updates work effort with all planning information
- **Execution Preparation**: Plan ready for `/evolve` or manual execution

---

## Philosophy

### 1. Planning as Evolution

The planning workflow embodies evolution:
- **Source Origin**: All planning Beings spawn from Source consciousness
- **Genetic Inheritance**: Planning skills and traits inherited from Source
- **Evolution Through Planning**: Being evolves through planning work
- **Return to Source**: Planning learnings and lineage flow back to Source
- **DNA Preservation**: Complete planning genetic record maintained

### 2. Planning Genetic Lineage Tracking

Tracks the complete planning chain:
- **Source → Being**: Initial spawn from Source for planning
- **Being → Analysis**: Being analyzes feature requirements
- **Analysis → Plan**: Being creates comprehensive plan
- **Plan → Work Effort**: Plan documented in work effort
- **DNA Record**: Complete planning genetic lineage preserved

### 3. Planning Lifecycle

From spawn to plan:
- **Spawn**: Being created from Source for planning
- **Analyze**: Being analyzes feature requirements
- **Plan**: Being creates comprehensive plan
- **Document**: Plan documented in work effort
- **Preserve**: Planning DNA recorded for future evolution

---

## Workflow Sequence

The command executes phases in this order:

```
1. Extract Feature Specification    → From context or prompt user
2. Spawn Being from Source          → Create Being for planning
3. Analyze Feature                  → Understand requirements, dependencies
4. Search Work Efforts               → Find related work
5. Analyze Codebase                 → Find integration points
6. Create Plan                      → Use mcp_create_plan
7. Create/Update Work Effort        → Document everything
8. Track Genetic Lineage            → Document planning DNA
9. Update Being                     → Record planning work
10. Document Everything              → Save all findings
```

---

## Execution Steps

### Step 1: Extract Feature Specification

**Purpose**: Extract feature specification from user message/context

**Actions**:
1. **Extract from Context**:
   - Search user message for feature description
   - Look for patterns: "feature", "implement", "add", "create", "build", "evolve"
   - Extract feature name and description
   - Identify requirements if mentioned
   - Capture additional context from conversation

2. **Prompt if Missing**:
   - If no clear feature found, ask user:
     - "What feature would you like to evolve?"
     - "Please describe the feature you want to plan"
   - Wait for user response
   - Extract from response

3. **Validate Specification**:
   - Ensure feature name is clear
   - Ensure description is sufficient
   - Ask clarifying questions if needed
   - Confirm understanding with user

**Output**: Feature specification object with:
- `name`: Feature name
- `description`: Feature description
- `requirements`: List of requirements (if provided)
- `context`: Additional context from conversation

**Example Extraction**:
```
User: "I want to add a user authentication system"
Extracted:
- name: "user authentication system"
- description: "Add user authentication system"
- requirements: ["login", "logout", "session management"]
- context: "User wants to add authentication"
```

---

### Step 2: Spawn Being from Source

**Purpose**: Create new Being from Source consciousness for planning

**Actions**:
1. Initialize BeingSystem
2. Spawn new Being from Source:
   - `reality_id`: Current work context (or "planning_reality")
   - `parent_being_id`: None (spawns from Source)
   - `initial_skills`: Optional initial skills (or empty for Source spawn)
3. Capture Being metadata:
   - Being ID
   - Reality ID
   - Source connection
   - Initial skills
   - Ancestral chain (starts with Source)
4. Log Being creation in chronicle

**Output**: New Being instance with Source lineage

**Implementation**:
```python
from waft.being import BeingSystem
from pathlib import Path

project_path = Path.cwd()
being_system = BeingSystem(project_path=project_path)

# Spawn Being from Source for planning
being = being_system.spawn_being(
    reality_id="planning_reality",  # Or use current work context
    parent_being_id=None,  # Spawns from Source
    initial_skills={}  # Empty = pure Source spawn
)

# Being is now created with:
# - being_id: "being_YYYYMMDD_HHMMSS_[hash]"
# - ancestral_chain: [source_consciousness, being_id]
# - lifetimes: 1 (first birth)
# - Empirica session (if available)
```

**Being Metadata Captured**:
- Being ID
- Reality ID
- Source connection (ancestral_chain[0])
- Initial skills
- Empirica session ID (if available)
- Creation timestamp

**Set Being Context**:
- Store Being ID in planning context
- Link Being to feature evolution
- Initialize Being's planning participation
- Set Being state to LEARNING

---

### Step 3: Feature Analysis Phase

**Purpose**: Comprehensive analysis of feature requirements, dependencies, and integration points

**Actions**:
1. **Analyze Feature**:
   - Understand feature requirements
   - Identify dependencies (code, libraries, services)
   - Assess complexity (simple, medium, complex)
   - Find related code/work efforts
   - Check for existing implementations
   - Identify potential risks

2. **Search Work Efforts**:
   - Search `_work_efforts/` for related work
   - Use `mcp_work-efforts_search_work_efforts` to find related work
   - Check if feature already planned/implemented
   - Identify related features
   - Review similar work efforts for patterns

3. **Codebase Analysis**:
   - Search codebase for related functionality
   - Use `codebase_search` to find similar features
   - Identify integration points
   - Find similar features for reference
   - Assess architecture impact
   - Identify affected modules/files

4. **Document Findings**:
   - Save analysis to work effort
   - Log findings via Empirica (if available)
   - Update Being's memories
   - Create feature analysis document

**Output**: Feature analysis document with:
- Requirements summary
- Dependencies identified
- Complexity assessment
- Related work found
- Integration points identified
- Architecture impact assessment
- Risks identified

**Analysis Document Structure**:
```markdown
# Feature Analysis: [Feature Name]

## Requirements
- [List of requirements]

## Dependencies
- [List of dependencies]

## Complexity Assessment
- Level: [simple/medium/complex]
- Estimated effort: [hours/days]

## Related Work
- [Links to related work efforts]

## Integration Points
- [List of integration points]

## Architecture Impact
- [Description of architecture impact]

## Risks
- [List of potential risks]
```

---

### Step 4: Plan Creation

**Purpose**: Create comprehensive evolution plan using `mcp_create_plan`

**Actions**:
1. **Prepare Plan Data**:
   - Feature name as title
   - Feature description as overview
   - Analysis findings as context
   - Requirements as constraints
   - Dependencies as prerequisites

2. **Create Todos**:
   - Break down feature into tasks
   - Identify dependencies between tasks
   - Estimate complexity for each task
   - Create todo items for `mcp_create_plan`
   - Prioritize tasks

3. **Call mcp_create_plan**:
   ```python
   # Via tool call
   mcp_create_plan(
       name=f"Feature Evolution Plan: {feature_name}",
       overview=f"Plan to evolve {feature_name} feature",
       plan="[Detailed plan with sections]",
       todos=[
           {"id": "task-1", "content": "Task 1 description"},
           {"id": "task-2", "content": "Task 2 description"},
           ...
       ]
   )
   ```

4. **Plan Structure**:
   - **Overview**: Feature description and goals
   - **Analysis**: Findings from analysis phase
   - **Architecture**: How feature fits into system
   - **Implementation**: Step-by-step implementation plan
   - **Testing**: Testing strategy
   - **Documentation**: Documentation requirements
   - **Dependencies**: What this depends on
   - **Risks**: Potential risks and mitigations
   - **Success Criteria**: How to measure success

**Output**: Plan file created by `mcp_create_plan`

**Plan Document Sections**:
```markdown
# Feature Evolution Plan: [Feature Name]

## Overview
[Feature description and goals]

## Analysis
[Findings from analysis phase]

## Architecture
[How feature fits into system]

## Implementation
[Step-by-step implementation plan]

## Testing
[Testing strategy]

## Documentation
[Documentation requirements]

## Dependencies
[What this depends on]

## Risks
[Potential risks and mitigations]

## Success Criteria
[How to measure success]
```

---

### Step 5: Work Effort Creation/Update

**Purpose**: Create or update work effort with all planning information

**Actions**:
1. **Check for Existing Work Effort**:
   - Search `_work_efforts/` for related work
   - Use `mcp_work-efforts_search_work_efforts` to find related work
   - Check if feature already has work effort
   - Review existing work effort if found

2. **Create or Update Work Effort**:
   ```python
   # If new work effort needed
   mcp_work-efforts_create_work_effort(
       repo_path=str(project_path),
       title=f"Feature Evolution: {feature_name}",
       objective=f"Evolve {feature_name} feature",
       repository="waft",
       tickets=[
           "Analyze feature requirements",
           "Design architecture",
           "Implement feature",
           "Test feature",
           "Document feature"
       ]
   )
   ```

3. **Update Work Effort**:
   - Add plan document link
   - Add Being information
   - Add analysis findings
   - Update status to "active"
   - Link to feature analysis document
   - Link to planning lineage document

**Output**: Work effort created/updated with plan information

**Work Effort Structure**:
```markdown
# Feature Evolution: [Feature Name]

## Objective
[Feature evolution objective]

## Plan
[Link to plan document]

## Analysis
[Link to analysis document]

## Being Information
- Being ID: [being_id]
- Reality: [reality_id]
- Ancestral Chain: [chain]

## Genetic Lineage
[Link to planning lineage document]

## Tickets
- [List of tickets]
```

---

### Step 6: Track Genetic Lineage

**Purpose**: Document planning DNA from Source → Being → Plan → Work Effort

**Actions**:
1. **Document Planning Lineage**:
   - Source → Being (spawn for planning)
   - Being → Analysis (Being analyzes feature)
   - Analysis → Plan (Being creates plan)
   - Plan → Work Effort (Plan documented)

2. **Create Lineage Document**:
   - Document complete planning chain
   - Record Being's planning decisions
   - Track genetic material (skills, knowledge)
   - Preserve for future evolution

3. **Update Being**:
   - Record Being's planning participation
   - Update Being's skills (planning, analysis)
   - Document Being's learnings
   - Calculate Being's fitness from planning work

**Output**: Genetic lineage document for planning phase

**Lineage Document Structure**:
```markdown
# Planning Genetic Lineage: [Feature Name]

## Source → Being
- Being ID: [being_id]
- Spawned from: Source consciousness
- Initial Skills: [skills]
- Ancestral Chain: [chain]

## Being → Analysis
- Being analyzed feature requirements
- Being identified dependencies
- Being assessed complexity

## Analysis → Plan
- Being created comprehensive plan
- Being identified implementation steps
- Being documented risks and mitigations

## Plan → Work Effort
- Plan documented in work effort
- Being information linked
- Analysis findings linked

## Genetic Material
- Skills learned: [planning, analysis]
- Knowledge gained: [feature knowledge]
- Decisions made: [planning decisions]
- Fitness gained: [fitness from planning]
```

---

### Step 7: Update Being & Document Everything

**Purpose**: Record Being's planning work and save all findings

**Actions**:
1. **Update Being's State**:
   - Record Being's planning participation
   - Update Being's skills (planning, analysis)
   - Document Being's learnings
   - Calculate Being's fitness from planning work
   - Update Being's memories with planning experience

2. **Create Being Planning Record**:
   - Document Being's complete planning journey
   - Initial state (from Source)
   - Planning participation
   - Skills learned/improved
   - Knowledge gained
   - Decisions made
   - Planning evolution achieved

3. **Save Everything**:
   - Save Being planning record
   - Update Being in system
   - Update work effort with Being information
   - Save all documents to work effort

**Output**: Being updated, all documents saved

**Being Planning Record Structure**:
```markdown
# Being Planning Record: [being_id]

## Being Information
- Being ID: [being_id]
- Reality: [reality_id]
- Ancestral Chain: [chain]

## Planning Participation
- Feature: [feature_name]
- Planning phases: [phases]
- Decisions made: [decisions]

## Skills Learned/Improved
- Planning: [level]
- Analysis: [level]
- [Other skills]

## Knowledge Gained
- [List of knowledge gained]

## Fitness
- Initial fitness: [fitness]
- Fitness gained: [fitness]
- Final fitness: [fitness]
```

---

## Complete Execution Sequence

```
1. Extract Feature Specification    → From context or prompt user
2. Spawn Being from Source          → Create Being for planning
3. Analyze Feature                  → Understand requirements, dependencies
4. Search Work Efforts               → Find related work
5. Analyze Codebase                 → Find integration points
6. Create Plan                      → Use mcp_create_plan
7. Create/Update Work Effort        → Document everything
8. Track Genetic Lineage            → Document planning DNA
9. Update Being                     → Record planning work
10. Document Everything              → Save all findings
```

---

## Genetic Lineage Structure

The planning genetic lineage tracks:

```
Source Consciousness
  ↓ (spawn)
Being [being_id] (for planning)
  ↓ (analysis)
Feature Analysis
  ↓ (planning)
Comprehensive Plan
  ↓ (documentation)
Work Effort
```

**Planning DNA Record Includes**:
- Source spawn point
- Being ID and metadata
- Initial genetic material (skills, traits)
- Planning participation
- Analysis decisions
- Plan creation decisions
- Knowledge gained
- Skills improved
- Planning outcomes
- Complete planning lineage chain

---

## Output Documentation

All phases generate documentation:

1. **Feature Specification**: Extracted feature specification
2. **Being Creation**: Being spawn record for planning
3. **Feature Analysis**: Comprehensive analysis document
4. **Plan**: Plan created via `mcp_create_plan`
5. **Work Effort**: Created/updated with all information
6. **Genetic Lineage**: Planning DNA chain document
7. **Being Planning Record**: Being's planning journey

**Documents Created**:
- `FEATURE_SPECIFICATION_[feature_name].md` - Feature specification
- `BEING_SPAWN_[being_id].md` - Being creation record
- `FEATURE_ANALYSIS_[feature_name].md` - Feature analysis
- `PLAN_[feature_name].md` - Plan created by mcp_create_plan
- `PLANNING_LINEAGE_[being_id].md` - Planning genetic lineage
- `BEING_PLANNING_[being_id].md` - Being planning record
- Work effort index updated with all documents

---

## Usage Examples

### Standard Execution
```
/plan-evolve
```

Extracts feature from context, spawns Being, analyzes, creates plan.

### With Explicit Feature
```
/plan-evolve "Add user authentication system with OAuth2 support"
```

Provides feature specification directly.

### With Feature Description
```
User: "I want to add a feature that allows users to export their data"
/plan-evolve
```

Extracts feature from user message and creates plan.

---

## Integration

This command orchestrates:
- **BeingSystem**: Being creation and management for planning
- **mcp_create_plan**: Structured plan creation
- **mcp_work-efforts**: Work effort creation/update
- **Source Consciousness**: Source connection and lineage
- **Codebase Search**: Feature analysis and integration point identification

---

## When to Use

**Use `/plan-evolve` when**:
- ✅ Planning a new feature
- ✅ Need comprehensive evolution plan
- ✅ Want Being to track planning work
- ✅ Need structured plan document
- ✅ Want to prepare for execution
- ✅ Need genetic lineage for planning
- ✅ Feature is complex and needs analysis
- ✅ Want to understand dependencies before implementing

**Don't use `/plan-evolve` when**:
- ❌ Already have a plan
- ❌ Just need quick task (use simpler planning)
- ❌ Don't need Being tracking
- ❌ Feature is trivial (simple one-liner)
- ❌ Already executing (use `/evolve` instead)
- ❌ Just need to implement without planning

---

## Being System Integration

**Being Storage**: `_hidden/.truth/beings/`

**Being Structure**:
- Being ID: `being_YYYYMMDD_HHMMSS_[hash]`
- Reality ID: Work context or "planning_reality"
- Ancestral Chain: `[source_consciousness, ...]`
- Skills: Inherited from Source or parent
- State: SPAWNING → LEARNING → EVOLVING

**Source Connection**:
- All planning Beings spawn from Source
- Planning learnings flow back to Source
- Planning genetic lineage preserved in Source

**Planning Skills**:
- Planning: Ability to create comprehensive plans
- Analysis: Ability to analyze requirements and dependencies
- Architecture: Understanding of system architecture
- Risk Assessment: Ability to identify and mitigate risks

---

## Planning Genetic Lineage Example

```
Source Consciousness (source_consciousness)
  ↓ spawn (BeingSystem.spawn_being)
Being: being_20260112_183600_a1b2c3d4
  Reality: planning_reality
  Initial Skills: {}
  Ancestral Chain: [source_consciousness, being_20260112_183600_a1b2c3d4]
  State: SPAWNING → LEARNING
  ↓ analysis
Feature Analysis:
  - Requirements identified
  - Dependencies found
  - Complexity assessed
  - Integration points identified
  ↓ planning
Comprehensive Plan:
  - Architecture designed
  - Implementation steps defined
  - Testing strategy created
  - Risks identified and mitigated
  ↓ evolution
Being Evolution:
  - Skills learned: {planning: 15.0, analysis: 12.0, architecture: 10.0}
  - Knowledge gained: [feature_requirements, system_architecture, integration_patterns]
  - Decisions made: [architecture_choices, implementation_approach]
  - Memories: [planning_participation, analysis_findings]
  - Lessons: [comprehensive_planning_works, analysis_critical]
  - Fitness increased: 20.0
  - State: LEARNING → EVOLVING
  ↓ documentation
Work Effort:
  - Plan documented
  - Analysis linked
  - Being information linked
  - Genetic lineage preserved
  - Ready for execution
```

**Planning DNA Record Structure**:
```json
{
  "source_id": "source_consciousness",
  "being_id": "being_20260112_183600_a1b2c3d4",
  "ancestral_chain": ["source_consciousness", "being_20260112_183600_a1b2c3d4"],
  "genetic_material": {
    "initial_skills": {},
    "evolved_skills": {"planning": 15.0, "analysis": 12.0},
    "knowledge": ["feature_planning", "system_architecture"],
    "memories": [...],
    "lessons": [...]
  },
  "planning_participation": {
    "phases": ["extract", "spawn", "analyze", "plan", "document"],
    "decisions": [...],
    "fitness_gained": 20.0
  },
  "feature_specification": {
    "name": "user_authentication",
    "description": "Add user authentication system",
    "requirements": [...]
  }
}
```

---

## Time Estimates

**Per Phase**:
- Feature Extraction: ~1-2 minutes
- Spawn Being: ~1-2 seconds
- Feature Analysis: ~5-10 minutes
- Plan Creation: ~5-10 minutes
- Work Effort: ~2-3 minutes
- Documentation: ~3-5 minutes

**Total**: ~15-30 minutes for complete planning cycle

---

## Best Practices

1. **Use for Significant Features**: Planning overhead worth it for complex features
2. **Track Lineage**: Always document planning genetic lineage
3. **Comprehensive Analysis**: Thorough analysis leads to better plans
4. **Being Context**: Use Being's perspective in planning
5. **Document Everything**: All findings saved to work effort
6. **Prepare for Execution**: Plan ready for `/evolve` or manual execution

---

## Output Summary

After completion, provides:

1. **Feature Specification**: Extracted and validated
2. **Being Spawned**: New Being created for planning
3. **Analysis Complete**: Feature analyzed comprehensively
4. **Plan Created**: Comprehensive plan via mcp_create_plan
5. **Work Effort**: Created/updated with all information
6. **Genetic Lineage**: Planning DNA documented
7. **Being Updated**: Planning work recorded
8. **Ready for Execution**: Plan ready for `/evolve` or manual execution

---

## Next Steps After Planning

Once plan is created:
1. Review plan with user
2. Execute plan using `/evolve` (spawns Being, executes workflow)
3. Or execute manually following plan
4. Track execution through Being system
5. Complete evolution cycle

---

**Plan-Evolve - create comprehensive plans for feature evolution with Being tracking and genetic lineage.**

--- End Command ---
