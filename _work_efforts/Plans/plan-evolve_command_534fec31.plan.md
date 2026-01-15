---
name: Plan-Evolve Command
overview: Create a new `/plan-evolve` slash command that extracts a feature specification from context, spawns a Being from Source, creates a comprehensive evolution plan using mcp_create_plan, tracks through the Being system, and documents everything in a work effort - all without executing the plan.
todos:
  - id: create-command-file
    content: Create `.cursor/commands/plan-evolve.md` following the pattern from `evolve.md` but focused on planning rather than execution
    status: completed
  - id: define-feature-extraction
    content: "Document feature extraction logic: extract from context, prompt if missing, validate specification"
    status: completed
  - id: document-being-integration
    content: "Document Being system integration: spawn from Source, track planning work, update skills"
    status: completed
  - id: document-analysis-phase
    content: "Document feature analysis phase: analyze requirements, search work efforts, analyze codebase"
    status: completed
  - id: document-plan-creation
    content: "Document plan creation using mcp_create_plan: prepare data, create todos, call tool"
    status: completed
  - id: document-work-effort
    content: "Document work effort creation/update: check existing, create/update, add plan information"
    status: completed
  - id: document-lineage-tracking
    content: "Document genetic lineage tracking for planning phase: document chain, create lineage doc"
    status: completed
  - id: document-integration-points
    content: Document integration with Being system, MCP tools, and other commands
    status: completed
  - id: add-usage-examples
    content: Add usage examples and when to use / when not to use sections
    status: completed
  - id: update-command-recommendations
    content: Update `.cursor/commands/COMMAND_RECOMMENDATIONS.md` to include new command
    status: completed
---

# Plan: Create `/plan-evolve` Command

## Overview

Create a new Cursor slash command `/plan-evolve` that creates a comprehensive plan for evolving a new feature. The command integrates with the Being system to track planning work and uses `mcp_create_plan` to generate structured plans.

## Command Purpose

**Command Name**: `/plan-evolve`

**Location**: `.cursor/commands/plan-evolve.md`

**Purpose**: Extract feature specification from context, spawn Being from Source, create comprehensive evolution plan, track through Being system, document in work effort

**Key Features**:

- Feature specification extraction from user message/context
- Being system integration (spawn from Source, track planning work)
- Comprehensive plan creation using `mcp_create_plan`
- Work effort creation/update
- Genetic lineage tracking for planning phase
- Preparation for execution (plan only, no execution)

## Implementation Steps

### Step 1: Create Command File

**File**: `.cursor/commands/plan-evolve.md`

**Structure**: Follow the pattern from `.cursor/commands/evolve.md` but focus on planning rather than execution.

**Key Sections**:

1. **Purpose**: Create plan for feature evolution with Being integration
2. **Philosophy**: Planning as evolution, Being tracks planning work, genetic lineage for plans
3. **Workflow Sequence**: Extract feature → Spawn Being → Analyze → Create Plan → Document
4. **Execution Steps**: Detailed steps for each phase
5. **Integration**: Being system, mcp_create_plan, work efforts
6. **When to Use**: Planning new features, need Being tracking, want structured plan

### Step 2: Define Feature Extraction Logic

**Location**: Command documentation (implementation guidance)

**Process**:

1. **Extract from Context**:

   - Search user message for feature description
   - Look for patterns: "feature", "implement", "add", "create", "build"
   - Extract feature name and description
   - Identify requirements if mentioned

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

**Output**: Feature specification object with:

- `name`: Feature name
- `description`: Feature description
- `requirements`: List of requirements (if provided)
- `context`: Additional context from conversation

### Step 3: Being System Integration

**Location**: Command execution logic (documented in command file)

**Process**:

1. **Spawn Being from Source**:
   ```python
   from waft.being import BeingSystem
   from pathlib import Path

   project_path = Path.cwd()
   being_system = BeingSystem(project_path=project_path)

   being = being_system.spawn_being(
       reality_id="planning_reality",  # Or use current work context
       parent_being_id=None,  # Spawns from Source
       initial_skills={}  # Empty = pure Source spawn
   )
   ```

2. **Set Being Context**:

   - Store Being ID in planning context
   - Link Being to feature evolution
   - Initialize Being's planning participation
   - Set Being state to LEARNING

3. **Track Being's Planning Work**:

   - Record Being's participation in planning
   - Track Being's decisions and choices
   - Document Being's learnings about planning
   - Update Being's skills based on planning work

**Output**: Being instance with planning context

### Step 4: Feature Analysis Phase

**Location**: Command execution steps

**Process**:

1. **Analyze Feature**:

   - Understand feature requirements
   - Identify dependencies
   - Assess complexity
   - Find related code/work efforts
   - Check for existing implementations

2. **Search Work Efforts**:

   - Search `_work_efforts/` for related work
   - Check if feature already planned/implemented
   - Identify related features

3. **Codebase Analysis**:

   - Search codebase for related functionality
   - Identify integration points
   - Find similar features for reference
   - Assess architecture impact

4. **Document Findings**:

   - Save analysis to work effort
   - Log findings via Empirica (if available)
   - Update Being's memories

**Output**: Feature analysis document

### Step 5: Plan Creation

**Location**: Use `mcp_create_plan` tool

**Process**:

1. **Prepare Plan Data**:

   - Feature name as title
   - Feature description as overview
   - Analysis findings as context
   - Requirements as constraints

2. **Create Todos**:

   - Break down feature into tasks
   - Identify dependencies
   - Estimate complexity
   - Create todo items for `mcp_create_plan`

3. **Call mcp_create_plan**:
   ```python
   # Via tool call
   mcp_create_plan(
       name="Feature Evolution Plan",
       overview="Plan to evolve [feature_name]",
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

### Step 6: Work Effort Creation/Update

**Location**: Use work-efforts MCP tools

**Process**:

1. **Check for Existing Work Effort**:

   - Search `_work_efforts/` for related work
   - Check if feature already has work effort

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

**Output**: Work effort created/updated with plan information

### Step 7: Genetic Lineage Tracking

**Location**: Command execution steps

**Process**:

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

### Step 8: Documentation

**Location**: Work effort directory

**Documents Created**:

1. **Plan File**: Created by `mcp_create_plan` (in plan location)
2. **Feature Analysis**: `FEATURE_ANALYSIS_[feature_name].md`
3. **Being Planning Record**: `BEING_PLANNING_[being_id].md`
4. **Genetic Lineage**: `PLANNING_LINEAGE_[being_id].md`
5. **Work Effort Index**: Updated with all documents

**Content**:

- Feature specification
- Analysis findings
- Comprehensive plan
- Being participation
- Genetic lineage
- Next steps (execution preparation)

## Command Workflow Sequence

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

## Integration Points

### Being System

- **Spawn**: `BeingSystem.spawn_being()` from Source
- **Track**: Being's planning participation
- **Update**: Being's skills and memories
- **Lineage**: Document planning genetic lineage

### MCP Tools

- **mcp_create_plan**: Create structured plan
- **mcp_work-efforts_create_work_effort**: Create work effort
- **mcp_work-efforts_create_ticket**: Create tickets for tasks
- **mcp_work-efforts_update_work_effort**: Update work effort

### Other Commands

- **/evolve**: Executes plan (use after /plan-evolve)
- **/version-bake**: Quality workflow (use during execution)
- **/run-it**: Complete workflow (use during execution)

## When to Use

**Use `/plan-evolve` when**:

- Planning a new feature
- Need comprehensive evolution plan
- Want Being to track planning work
- Need structured plan document
- Want to prepare for execution
- Need genetic lineage for planning

**Don't use `/plan-evolve` when**:

- Already have a plan
- Just need quick task (use simpler planning)
- Don't need Being tracking
- Feature is trivial
- Already executing (use /evolve instead)

## Output Summary

After completion:

1. **Feature Specification**: Extracted and validated
2. **Being Spawned**: New Being created for planning
3. **Analysis Complete**: Feature analyzed
4. **Plan Created**: Comprehensive plan via mcp_create_plan
5. **Work Effort**: Created/updated with all information
6. **Genetic Lineage**: Planning DNA documented
7. **Being Updated**: Planning work recorded
8. **Ready for Execution**: Plan ready for /evolve or manual execution

## File Locations

- **Command File**: `.cursor/commands/plan-evolve.md`
- **Plan File**: Created by `mcp_create_plan` (location depends on tool)
- **Work Effort**: `_work_efforts/WE-YYMMDD-xxxx_feature_evolution/`
- **Being Records**: `_hidden/.truth/beings/`
- **Analysis**: `_work_efforts/WE-YYMMDD-xxxx_feature_evolution/FEATURE_ANALYSIS.md`
- **Lineage**: `_work_efforts/WE-YYMMDD-xxxx_feature_evolution/PLANNING_LINEAGE.md`

## Next Steps After Planning

Once plan is created:

1. Review plan with user
2. Execute plan using `/evolve` (spawns Being, executes workflow)
3. Or execute manually following plan
4. Track execution through Being system
5. Complete evolution cycle

## Time Estimates

**Per Phase**:

- Feature Extraction: ~1-2 minutes
- Spawn Being: ~1-2 seconds
- Feature Analysis: ~5-10 minutes
- Plan Creation: ~5-10 minutes
- Work Effort: ~2-3 minutes
- Documentation: ~3-5 minutes

**Total**: ~15-30 minutes for complete planning cycle

## Command Template Structure

The command file should follow this structure (based on `/evolve.md` pattern):

```markdown
# Plan-Evolve

**Create a comprehensive plan to evolve a new feature: extract → spawn → analyze → plan → document**

[Full command description following evolve.md pattern]
```

## Implementation Notes

1. **Feature Extraction**: Use natural language processing to extract feature from context
2. **Being Integration**: Spawn Being specifically for planning work
3. **Plan Structure**: Use mcp_create_plan format with todos
4. **Work Effort**: Create or update work effort for feature
5. **Documentation**: Comprehensive documentation of planning process
6. **Genetic Lineage**: Track planning DNA separately from execution DNA

## Success Criteria

- Command file created in `.cursor/commands/plan-evolve.md`
- Command follows existing command patterns
- Integration with Being system documented
- Integration with mcp_create_plan documented
- Integration with work efforts documented
- Command ready for use
- Documentation complete