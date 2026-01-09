# Analyze

**Analysis, insights, and action planning - transform data into decisions.**

Takes Phase 1 data (or runs Phase 1 if needed), analyzes patterns, identifies issues and opportunities, generates insights, and creates prioritized action plans. Transforms data gathering into actionable decisions.

**Use when:** After Phase 1, when you need to understand what the data means, identify what needs attention, and plan what to do next.

---

## Purpose

This command provides:
- **Data Analysis**: Deep analysis of Phase 1 findings
- **Pattern Recognition**: Identifies trends, anomalies, and relationships
- **Issue Identification**: Finds problems, gaps, and risks
- **Opportunity Discovery**: Highlights improvements and enhancements
- **Insight Generation**: Creates actionable insights from data
- **Action Planning**: Generates prioritized action plans
- **Recommendations**: Provides clear next steps

---

## Philosophy

1. **Analyze First**: Understand what the data means before acting
2. **Pattern Focus**: Look for trends, not just individual data points
3. **Issue Priority**: Identify what needs attention most urgently
4. **Actionable Insights**: Generate insights that lead to decisions
5. **Prioritized Planning**: Create plans with clear priorities

---

## Execution Phases

### Analyze 2.1: Data Loading & Validation
**Purpose**: Load Phase 1 data and validate completeness

**Steps**:
1. Check for most recent Phase 1 output
2. Load Phase 1 JSON data
3. Validate data completeness
4. If no Phase 1 data exists, run Phase 1 first
5. Load additional context (work efforts, devlog, recent commits)

**Output**: Validated Phase 1 data ready for analysis

---

### Analyze 2.2: Health Analysis
**Purpose**: Assess overall project health

**Steps**:
1. Analyze integrity percentage and trends
2. Check structure validity
3. Evaluate git status (uncommitted files, commits ahead/behind)
4. Assess dependency health (uv.lock status)
5. Review gamification stats (level, insight progress)
6. Calculate health score

**Output**: Project health assessment with scores and indicators

---

### Analyze 2.3: Issue Identification
**Purpose**: Find problems that need attention

**Steps**:
1. Identify structural issues (_pyrite problems, missing files)
2. Find git issues (uncommitted changes, divergence)
3. Detect dependency issues (missing lock, outdated deps)
4. Spot integrity issues (low integrity, declining trends)
5. Find work effort issues (stale efforts, incomplete tasks)
6. Identify memory layer issues (orphaned files, missing structure)

**Output**: Prioritized list of issues with severity ratings

---

### Analyze 2.4: Opportunity Discovery
**Purpose**: Find areas for improvement and enhancement

**Steps**:
1. Identify quick wins (low effort, high impact)
2. Find optimization opportunities (performance, structure)
3. Discover enhancement areas (features, documentation)
4. Spot consolidation opportunities (duplicate work, similar efforts)
5. Find automation opportunities (repetitive tasks)
6. Identify learning opportunities (new patterns, best practices)

**Output**: List of opportunities with impact/effort ratings

---

### Analyze 2.5: Pattern Analysis
**Purpose**: Identify trends and patterns in the data

**Steps**:
1. Analyze file change patterns (most modified, least touched)
2. Identify work effort patterns (active areas, completion rates)
3. Find commit patterns (frequency, size, types)
4. Analyze memory layer patterns (active vs backlog growth)
5. Identify temporal patterns (recent activity, trends over time)
6. Find relationship patterns (connected work, dependencies)

**Output**: Pattern analysis with insights and implications

---

### Analyze 2.6: Insight Generation
**Purpose**: Create actionable insights from analysis

**Steps**:
1. Synthesize findings into key insights
2. Identify root causes of issues
3. Connect patterns to outcomes
4. Generate recommendations
5. Create actionable insights (specific, measurable, relevant)
6. Prioritize insights by impact and urgency

**Output**: Prioritized list of insights with recommendations

---

### Analyze 2.7: Action Planning
**Purpose**: Create prioritized action plans

**Steps**:
1. Group related issues and opportunities
2. Create action items for each insight
3. Estimate effort and impact for each action
4. Prioritize actions (urgent, important, nice-to-have)
5. Create action sequences (dependencies, order)
6. Generate work effort suggestions (if applicable)

**Output**: Prioritized action plan with sequences and estimates

---

### Analyze 2.8: Report Generation
**Purpose**: Create comprehensive analysis report

**Steps**:
1. Compile all analysis results
2. Generate markdown report
3. Create visualizations (if applicable)
4. Save report to `_pyrite/phase2/` directory
5. Display summary in console
6. Provide next steps recommendations

**Output**: Comprehensive analysis report + console summary

---

## Execution Flow

```
Analyze 2.1: Data Loading & Validation
  ↓
Analyze 2.2: Health Analysis
  ↓
Analyze 2.3: Issue Identification
  ↓
Analyze 2.4: Opportunity Discovery
  ↓
Analyze 2.5: Pattern Analysis
  ↓
Analyze 2.6: Insight Generation
  ↓
Analyze 2.7: Action Planning
  ↓
Analyze 2.8: Report Generation
  ↓
✅ Complete - Analysis report generated
```

---

## What Gets Analyzed

### Health Metrics
- Integrity percentage and trends
- Structure validity
- Git health (uncommitted, divergence)
- Dependency health
- Gamification progress

### Issues
- Structural problems
- Git issues
- Dependency problems
- Integrity issues
- Work effort problems
- Memory layer issues

### Opportunities
- Quick wins
- Optimizations
- Enhancements
- Consolidations
- Automations
- Learning opportunities

### Patterns
- File change patterns
- Work effort patterns
- Commit patterns
- Memory layer patterns
- Temporal patterns
- Relationship patterns

### Insights
- Key findings
- Root causes
- Pattern implications
- Recommendations
- Actionable insights
- Priority rankings

### Actions
- Action items
- Effort estimates
- Impact assessments
- Priority rankings
- Action sequences
- Work effort suggestions

---

## Output Format

### Console Output

The command provides progress updates as it runs:

```
🌊 Analyze: Analysis, Insights & Action Planning

Analyze 2.1: Data Loading & Validation... ✓
  ✓ Loaded Phase 1 data: phase1-2026-01-07-205640.json
  ✓ Data complete: 8/8 sections

Analyze 2.2: Health Analysis... ✓
  ✓ Overall Health: 85% (Good)
  ✓ Integrity: 100% (Excellent)
  ✓ Git Status: 54 uncommitted files (Needs attention)
  ✓ Structure: Valid ✓

Analyze 2.3: Issue Identification... ✓
  ⚠️  Found 3 issues:
    1. High uncommitted files (54) - Medium priority
    2. No active work efforts - Low priority
    3. Commits ahead of remote (4) - Low priority

Analyze 2.4: Opportunity Discovery... ✓
  ✨ Found 5 opportunities:
    1. Quick win: Commit uncommitted changes
    2. Enhancement: Create work effort for analysis
    3. Optimization: Review memory layer organization
    4. Learning: Analyze commit patterns
    5. Automation: Auto-commit workflow

Analyze 2.5: Pattern Analysis... ✓
  📊 Patterns identified:
    - Recent activity: High (12 files in last 24h)
    - Work effort completion: 100% (all completed)
    - Memory layer growth: Stable

Analyze 2.6: Insight Generation... ✓
  💡 Generated 4 insights:
    1. Project is healthy but needs cleanup
    2. High activity suggests active development
    3. All work efforts completed - ready for new work
    4. Memory layer is well-organized

Analyze 2.7: Action Planning... ✓
  📋 Created action plan:
    1. [Urgent] Commit uncommitted changes
    2. [Important] Create new work effort
    3. [Nice-to-have] Review memory layer

Analyze 2.8: Report Generation... ✓
  📄 Report saved: analyze-2026-01-07-205700.md
  📊 Analysis complete

✅ Analyze Complete - Analysis and action plan ready
   📁 Output folder: _pyrite/analyze/
   📄 Report: analyze-2026-01-07-205700.md
   🎯 Next steps: Review report and execute action plan
```

### Analysis Report

The report includes:

1. **Executive Summary**
   - Overall health score
   - Key findings
   - Top priorities

2. **Health Analysis**
   - Detailed health metrics
   - Trend analysis
   - Health indicators

3. **Issues Identified**
   - Prioritized issue list
   - Severity ratings
   - Impact assessments

4. **Opportunities Discovered**
   - Opportunity list
   - Impact/effort matrix
   - Quick wins highlighted

5. **Pattern Analysis**
   - Pattern descriptions
   - Trend analysis
   - Implications

6. **Insights & Recommendations**
   - Key insights
   - Root cause analysis
   - Recommendations

7. **Action Plan**
   - Prioritized actions
   - Effort estimates
   - Action sequences
   - Next steps

---

## Use Cases

### 1. Post-Phase 1 Analysis
**Scenario**: Just ran Phase 1, want to understand what it means

**Example**:
```
User: "/phase1"
User: "/phase2"
```

**Output**: Analysis of Phase 1 data with insights and action plan

---

### 2. Project Health Check
**Scenario**: Want to assess project health and identify issues

**Example**:
```
User: "/phase2"
```

**Output**: Health analysis, issue identification, recommendations

---

### 3. Planning Session
**Scenario**: Need to plan next steps and prioritize work

**Example**:
```
User: "/phase2"
```

**Output**: Action plan with prioritized next steps

---

### 4. Issue Investigation
**Scenario**: Suspect there are problems, want to find them

**Example**:
```
User: "/phase2"
```

**Output**: Comprehensive issue identification with priorities

---

### 5. Opportunity Discovery
**Scenario**: Want to find areas for improvement

**Example**:
```
User: "/phase2"
```

**Output**: List of opportunities with impact/effort analysis

---

## Integration with Other Commands

- **`/phase1`**: Data gathering (`/analyze` analyzes Phase 1 output)
- **`/consider`**: Qualitative analysis (`/analyze` is data-driven analysis)
- **`/decide`**: Decision matrix (`/analyze` provides data for decisions)
- **`/engineer`**: Full workflow (note: `/engineer` has its own Phase 2: Explore - different from `/analyze`)
- **`/checkpoint`**: Status snapshot (`/analyze` provides deeper analysis)

---

## When to Use

**Use `/analyze` when**:
- ✅ Just completed `/phase1`
- ✅ Need to understand what data means
- ✅ Want to identify issues and opportunities
- ✅ Need to plan next steps
- ✅ Want actionable insights
- ✅ Need prioritized action plan

**Don't use `/analyze` when**:
- ❌ Haven't run `/phase1` (it will auto-run, but may be slower)
- ❌ Need quick status (use `/status` or `/checkpoint`)
- ❌ Just need visualization (use `/visualize`)
- ❌ Need immediate action (use `/consider` for quick analysis)

---

## Technical Details

### Data Sources

Analyze analyzes:
- `/phase1` JSON output (primary source)
- Work efforts data
- Devlog entries
- Recent git history
- Memory layer structure
- Gamification stats

### Analysis Methods

- **Health Scoring**: Weighted scoring based on multiple factors
- **Issue Prioritization**: Severity × Impact × Urgency  
- **Opportunity Ranking**: Impact / Effort ratio
- **Pattern Detection**: Statistical analysis and trend detection
- **Insight Synthesis**: Multi-factor analysis and correlation

### Performance

- **Total Time**: ~3-8 seconds (depending on data size)
- **Data Loading**: ~1 second
- **Analysis**: ~2-5 seconds
- **Report Generation**: ~1 second

### Error Handling

- **Missing Phase 1 Data**: Automatically runs `/phase1` first
- **Incomplete Data**: Analyzes available data, marks missing sections
- **Analysis Errors**: Graceful degradation, continues with available data
- **Report Generation**: Always generates report, even if some analysis fails

---

## Example Workflow

```
User: "/phase2"

AI: [Runs all 8 phases sequentially]

AI: ✅ Analyze Complete
    - Health: 85% (Good)
    - Issues: 3 found (1 medium, 2 low priority)
    - Opportunities: 5 discovered
    - Insights: 4 generated
    - Actions: 3 prioritized
    - Report: analyze-2026-01-07-205700.md

User: [Reviews report, executes action plan]
```

---

## Advanced Features

### Custom Analysis Depth
Can specify analysis depth:
```bash
/phase2 --deep    # Comprehensive analysis
/phase2 --quick   # Quick analysis (default)
```

### Focus Areas
Can focus on specific areas:
```bash
/phase2 --focus health      # Health analysis only
/phase2 --focus issues      # Issue identification only
/phase2 --focus opportunities  # Opportunity discovery only
```

### Comparison Mode
Compare with previous analyze run:
```bash
/phase2 --compare  # Compare with last Phase 2 report
```

### Export Options
- ✅ Report automatically saved as Markdown in `_pyrite/phase2/`
- ✅ Can export to JSON for programmatic use
- ✅ Can generate visualizations (if data supports)

---

**This command transforms `/phase1` data into actionable insights and prioritized plans - perfect for understanding what needs attention and planning next steps.**
