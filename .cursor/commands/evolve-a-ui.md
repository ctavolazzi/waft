# Evolve a UI

**Scan work efforts and evolve a UI for whatever is happening in the current chat instance**

Analyzes the current context by scanning work efforts, recent activity, and project state, then generates an evolved UI tailored to what you're working on.

**Use when:** You want a UI that adapts to your current work context, need a dashboard for active work efforts, or want to visualize what's happening in your project.

---

## Purpose

This command provides:
- **Context Analysis**: Scans work efforts, recent files, git status, and project state
- **UI Evolution**: Generates a UI tailored to current work context
- **Work Effort Integration**: Creates dashboards for active work efforts
- **Adaptive Design**: UI evolves based on what you're actually doing
- **Real-time Context**: Reflects current project state and activity

---

## Philosophy

### 1. Context-Aware UI Generation

The UI evolves based on:
- **Active Work Efforts**: What you're currently working on
- **Recent Activity**: Files changed, commits, recent work
- **Project State**: Git status, active branches, system health
- **Chat Context**: Inferred from work efforts and recent activity

### 2. Adaptive Evolution

The UI adapts to:
- **Work Type**: Different UIs for different types of work (features, bugs, research)
- **Project Phase**: Early exploration vs. implementation vs. polish
- **System State**: Active development vs. planning vs. review

### 3. Work Effort Integration

- **Active Work Dashboard**: Visualizes current work efforts
- **Progress Tracking**: Shows status of tickets and tasks
- **Context Visualization**: Displays relationships between work items

---

## Workflow Sequence

The command executes phases in this order:

```
1. Scan Work Efforts        → Analyze _work_efforts/ directory
2. Analyze Recent Activity  → Check recent files, git status, devlog
3. Infer Chat Context       → Determine what you're working on
4. Generate UI Requirements  → Create UI spec based on context
5. Evolve UI Design         → Use WAFT evolution system
6. Generate HTML/CSS        → Create evolved UI files
7. Create Dashboard        → Generate interactive dashboard
8. Open in Browser          → Launch evolved UI
```

---

## Execution Steps

### Step 1: Scan Work Efforts

**Purpose**: Understand current work context

**Actions**:
1. Scan `_work_efforts/` directory for active work efforts
2. Read work effort index files and metadata
3. Identify active tickets and tasks
4. Extract work effort themes and goals
5. Determine work type (feature, bug, research, etc.)

**Output**: List of active work efforts with status, tickets, and context

### Step 2: Analyze Recent Activity

**Purpose**: Understand what's happening right now

**Actions**:
1. Check git status for modified/added files
2. Read recent devlog entries
3. Check recent file modifications
4. Analyze current branch and commits
5. Identify patterns in recent work

**Output**: Recent activity summary with patterns and themes

### Step 3: Infer Chat Context

**Purpose**: Determine what you're working on in this chat

**Actions**:
1. Combine work effort data with recent activity
2. Identify primary focus areas
3. Determine UI requirements based on context
4. Create context summary for UI generation

**Output**: Context summary with UI requirements

### Step 4: Generate UI Requirements

**Purpose**: Create UI specification based on context

**Actions**:
1. Determine UI type (dashboard, form, visualization, etc.)
2. Identify required components
3. Define data sources and interactions
4. Create UI specification document

**Output**: UI requirements specification

### Step 5: Evolve UI Design

**Purpose**: Use WAFT evolution system to generate UI

**Actions**:
1. Initialize DocumentEvolutionEngine
2. Generate evolved design based on requirements
3. Extract design insights (colors, typography, layout)
4. Create component specifications

**Output**: Evolved design with fitness score and components

### Step 6: Generate HTML/CSS

**Purpose**: Create actual UI files

**Actions**:
1. Generate HTML structure
2. Create CSS with evolved styling
3. Add JavaScript for interactivity
4. Integrate with WAFT systems (if needed)

**Output**: Complete HTML/CSS/JS files

### Step 7: Create Dashboard

**Purpose**: Generate interactive dashboard

**Actions**:
1. Create dashboard layout
2. Add data visualization components
3. Integrate work effort data
4. Add navigation and controls

**Output**: Interactive dashboard HTML

### Step 8: Open in Browser

**Purpose**: Launch evolved UI

**Actions**:
1. Save UI files to output directory
2. Open in default browser
3. Provide file path for reference

**Output**: UI opened in browser, file path provided

---

## Usage Examples

### Standard Execution
```
/evolve-a-ui
```

Scans work efforts, analyzes context, and generates evolved UI.

### With Output Path
```
/evolve-a-ui --output ui/dashboard.html
```

Generates UI at specific path.

### With Work Effort Focus
```
/evolve-a-ui --work-effort WE-260114-abc123
```

Focuses on specific work effort for UI generation.

### With UI Type
```
/evolve-a-ui --type dashboard
```

Generates specific UI type (dashboard, form, visualization, etc.).

---

## Output Files

**Generated Files**:
- `_genetics/ui_evolution/[timestamp]_evolved_ui.html` - Main UI file
- `_genetics/ui_evolution/[timestamp]_design_insights.json` - Design metadata
- `_genetics/ui_evolution/[timestamp]_context_analysis.md` - Context summary

**Optional Files**:
- `_genetics/ui_evolution/[timestamp]_requirements.md` - UI requirements
- `_genetics/ui_evolution/[timestamp]_evolution_report.md` - Evolution report

---

## Integration

This command uses:
- **Work Efforts System**: Scans `_work_efforts/` for context
- **DocumentEvolutionEngine**: Evolves UI design
- **ChatDistiller**: Analyzes context patterns
- **Visualizer**: Creates dashboard components
- **Git Integration**: Analyzes recent activity

---

## When to Use

**Use `/evolve-a-ui` when**:
- ✅ Want a UI that adapts to current work
- ✅ Need dashboard for active work efforts
- ✅ Want to visualize project state
- ✅ Need UI for specific work context
- ✅ Want evolved design based on context

**Don't use `/evolve-a-ui` when**:
- ❌ Need static, predefined UI
- ❌ Working on unrelated project
- ❌ No active work efforts to analyze
- ❌ Need production-ready UI (this is for exploration)

---

## Context Analysis

The command analyzes:

1. **Work Efforts**:
   - Active work effort titles and descriptions
   - Ticket status and progress
   - Work effort metadata and tags

2. **Recent Activity**:
   - Modified files in last 24 hours
   - Recent git commits
   - Recent devlog entries

3. **Project State**:
   - Git branch and status
   - Active files and directories
   - System health metrics

4. **Patterns**:
   - Common themes across work efforts
   - Recurring file types and patterns
   - Work type classification

---

## UI Types

The command can generate:

- **Dashboard**: Overview of work efforts and project state
- **Work Effort View**: Focused view on specific work effort
- **Form Interface**: Input forms for data entry
- **Visualization**: Charts and graphs for data
- **Status Board**: Kanban-style status board
- **Timeline**: Chronological view of work

---

## Evolution Process

1. **Context Gathering**: Scan work efforts and activity
2. **Requirement Generation**: Create UI spec from context
3. **Design Evolution**: Use WAFT evolution system
4. **Component Generation**: Create HTML/CSS components
5. **Integration**: Connect to WAFT systems if needed
6. **Output**: Generate files and open in browser

---

## Notes

- UI is generated based on inferred context from work efforts
- Design evolves using WAFT's evolution system
- UI adapts to work type and project phase
- Generated files are saved in `_genetics/ui_evolution/`
- UI opens automatically in default browser
- Can be regenerated as context changes

---

*This command helps you visualize and interact with your work context through an evolved UI that adapts to what you're actually doing.*
