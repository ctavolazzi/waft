# WAFT Status

**Self-aware system status check with documentation generation at multiple complexity levels.**

Checks the current state of the WAFT system (git status, work efforts, recent changes, project health, epistemic state) and can generate comprehensive documentation about what's happening right now at three complexity levels: layman, professional, and scientist.

**Use when:** Need to understand current system state, generate status reports, create handoff documentation, or document current work for different audiences.

---

## Purpose

This command provides:
- **System Status Check**: Comprehensive analysis of current state
- **Multi-Level Documentation**: Generate status docs at layman/professional/scientist levels
- **Self-Awareness**: System documents its own current state
- **Real-Time Analysis**: Captures what's happening right now
- **Integration**: Works with work efforts, git, devlog, epistemic state
- **WAFT Kernel Integration**: Includes kernel identity, boot sequence, epistemic phase, and operational state

---

## Quick Start

### Check Status Only
```
/waft-status
```

Displays current system status without generating documentation.

### Generate Status Documentation
```
/waft-status --docs
```

Generates status documentation at all three complexity levels.

### Generate Specific Level
```
/waft-status --docs --level layman
/waft-status --docs --level professional
/waft-status --docs --level scientist
```

Generates documentation at specific complexity level.

### Printer-Friendly Documentation
```
/waft-status --docs --printer-friendly
```

Generates printer-friendly (black-and-white) status documentation.

---

## Workflow Sequence

### Phase 1: System Status Check

**Execute**: Comprehensive system analysis

**Purpose**: Gather complete picture of current state

**Data Collected**:
1. **Git Status**:
   - Current branch
   - Uncommitted files
   - Commits ahead/behind
   - Recent commit history
   - Staged vs unstaged changes

2. **Work Efforts**:
   - Active work efforts
   - Recent work effort updates
   - Completed work efforts
   - Work effort statistics

3. **Project Health**:
   - _pyrite structure validity
   - uv.lock status
   - Dependency status
   - Test suite status
   - Build status

4. **Recent Activity**:
   - Recent devlog entries
   - Recent file changes
   - Recent commits
   - Active development areas

5. **Epistemic State** (if Empirica initialized):
   - Moon phase indicator
   - Knowledge percentage
   - Uncertainty percentage
   - Epistemic phase (Data Gathering, Exploration, Synthesis, Evolution)
   - Epistemic vectors

6. **Kernel Status**:
   - Kernel status (ONLINE)
   - Epistemic phase
   - Boot time (from flight recorder)
   - Active generation tracking

7. **_pyrite Integrity**:
   - Structure validation
   - Genesis files presence (20.00_state.json, 35.00_ledger.json, 42.00_kernel.md)
   - Directory structure check

**Output**: Comprehensive status data structure

---

### Phase 2: Status Analysis

**Execute**: Analyze collected status data

**Purpose**: Identify key patterns and insights

**Analysis Performed**:
- Change patterns (what's being worked on)
- Work effort trends (active vs completed)
- Git activity patterns (commit frequency, branch activity)
- Health indicators (what needs attention)
- Development velocity (recent activity levels)
- Risk factors (uncommitted work, broken tests, etc.)

**Output**: Analyzed status with insights

---

### Phase 3: Documentation Generation (Optional)

**Execute**: Generate status documentation

**Purpose**: Create comprehensive documentation about current state

**Documentation Levels**:

#### Level 1: Layman (Simple Explanations)
- What the system is doing right now
- Simple explanations of current state
- What's being worked on (in plain language)
- Current health status (good/needs attention)
- Recent accomplishments

#### Level 2: Professional (Technical Details)
- Detailed technical status
- Git branch and commit analysis
- Work effort breakdown
- Project structure status
- Integration points
- Technical health metrics

#### Level 3: Scientist (Research-Level Depth)
- Deep analysis of system state
- Epistemic state analysis
- Development patterns and trends
- Statistical analysis of activity
- Research-level insights
- Predictive indicators

**Output**: PDF documentation at requested level(s)

---

## Complete Execution Sequence

```
1. Initialize WAFT Kernel      → Boot sequence, identity acknowledgment
2. Check system status        → Gather all status data (including kernel state)
3. Analyze status             → Identify patterns and insights
4. Display status summary     → Show current state (including kernel info)
5. [Optional] Generate docs   → Create documentation at requested level(s)
6. Log kernel event           → Record status check to Flight Recorder
```

## WAFT Kernel Integration

### Kernel Boot Sequence

When `/waft-status` is executed, the WAFT Kernel performs a boot sequence:

1. **Kernel Initialization**
   - Load project path
   - Set identity: WAFT_KERNEL
   - Record boot_time
   - Initialize integration with existing systems (TheObserver, EmpiricaManager, GamificationManager)

2. **Initial Status Check**
   - Git status
   - Work efforts
   - Project health
   - _pyrite integrity
   - uv.lock status

3. **Epistemic Phase Declaration**
   - Analyze system state
   - Determine phase (Data Gathering/Synthesis/Evolution/etc.)
   - Calculate epistemic metrics (via EmpiricaManager or kernel estimates)

4. **Flight Recorder Log**
   - Event: KERNEL_BOOT (using EvolutionaryEvent)
   - Context: boot status
   - Logged to: _pyrite/science/laboratory.jsonl (via TheObserver)

5. **Status Check Integration**
   - Kernel status included in status output
   - Kernel perspective added to documentation
   - Kernel events logged to Flight Recorder

### Kernel Identity

The WAFT Kernel is the **system-level intelligence** that:
- **Role**: Central operating intelligence for directed evolution
- **Mission**: Oversee breeding of self-modifying AI agents
- **Goal**: Generate data for "The Physics of Artificial Cognition"
- **Identity**: WAFT_KERNEL

**Important Distinction**: The WAFT Kernel is NOT the same as `42.00_kernel.md` from Unified Genesis Protocol (that's for UNIT_GENESIS entities). The WAFT Kernel is the system-level orchestrator.

### Kernel Operational State

The kernel provides:
- **Epistemic Phase**: Current operational phase (e.g., "Data Gathering", "Synthesis", "Evolution")
- **Epistemic State**: Moon phase, knowledge %, uncertainty % (from EmpiricaManager or kernel estimates)
- **System Integration**: Status of Flight Recorder, Empirica, Gamification systems
- **Uptime**: Time since kernel boot sequence

---

## Command Options

### Status Check Only
```
/waft-status
```

Displays status without generating documentation.

### Generate All Documentation Levels
```
/waft-status --docs
```

Generates status documentation at all three levels (layman, professional, scientist).

### Generate Specific Level
```
/waft-status --docs --level layman
/waft-status --docs --level professional
/waft-status --docs --level scientist
```

Generates documentation at specific complexity level.

### Printer-Friendly Documentation
```
/waft-status --docs --printer-friendly
```

Generates printer-friendly (black-and-white) versions.

### Focus on Specific Area
```
/waft-status --focus "work efforts"
/waft-status --focus "git activity"
/waft-status --focus "project health"
```

Focuses status check and documentation on specific area.

### Include Historical Data
```
/waft-status --history
```

Includes historical trends and patterns in analysis.

---

## Usage Examples

### Example 1: Quick Status Check
```
/waft-status
```

**What it does**:
1. Checks git status
2. Reviews work efforts
3. Checks project health
4. Displays summary

**Output**:
- Console summary of current state
- Key indicators
- Quick health check

### Example 2: Generate Status Documentation
```
/waft-status --docs
```

**What it does**:
1. Performs complete status check
2. Analyzes current state
3. Generates documentation at all three levels
4. Creates PDFs for each level

**Output**:
- `WAFT_Status_Layman_YYYY-MM-DD.pdf`
- `WAFT_Status_Professional_YYYY-MM-DD.pdf`
- `WAFT_Status_Scientist_YYYY-MM-DD.pdf`

### Example 3: Professional Status Report
```
/waft-status --docs --level professional --printer-friendly
```

**What it does**:
- Generates professional-level status documentation
- Uses printer-friendly template
- Focuses on technical details

**Output**:
- `WAFT_Status_Professional_YYYY-MM-DD_PrinterFriendly.pdf`

### Example 4: Focused Status Check
```
/waft-status --focus "work efforts" --docs --level layman
```

**What it does**:
- Focuses on work efforts status
- Generates layman-level documentation
- Explains work efforts in simple terms

**Output**:
- `WAFT_Status_WorkEfforts_Layman_YYYY-MM-DD.pdf`

---

## Status Check Details

### Git Status Analysis

**Information Collected**:
- Current branch name
- Uncommitted files (staged and unstaged)
- Commits ahead of origin
- Commits behind origin
- Recent commit history (last 10 commits)
- File change statistics
- Branch activity

**Insights Generated**:
- Development activity level
- Commit frequency patterns
- Risk of uncommitted work
- Branch divergence status

---

### Work Efforts Analysis

**Information Collected**:
- Active work efforts count
- Recent work effort updates
- Completed work efforts
- Work effort categories
- Work effort status distribution

**Insights Generated**:
- Active development areas
- Work completion trends
- Work effort health
- Priority areas

---

### Project Health Analysis

**Information Collected**:
- _pyrite structure validity
- uv.lock file status
- Dependency status
- Test suite status
- Build system status
- Configuration validity

**Insights Generated**:
- Overall project health
- Areas needing attention
- Risk factors
- Stability indicators

---

### Recent Activity Analysis

**Information Collected**:
- Recent devlog entries
- Recent file modifications
- Recent commits
- Active development patterns
- File change frequency

**Insights Generated**:
- Development velocity
- Active work areas
- Change patterns
- Activity trends

---

### Epistemic State Analysis (if available)

**Information Collected**:
- Moon phase indicator
- Knowledge percentage
- Uncertainty percentage
- Epistemic vectors (13 dimensions)
- Learning trajectory

**Insights Generated**:
- Epistemic health
- Knowledge gaps
- Learning progress
- Confidence levels

---

## Documentation Content

### Layman Level (Simple Explanations)

**Content Includes**:
- What the system is doing right now (plain language)
- Current work areas (simple descriptions)
- System health (good/needs attention)
- Recent accomplishments
- What needs attention
- Simple analogies and explanations

**Target Audience**: Non-technical stakeholders, project managers, general audience

---

### Professional Level (Technical Details)

**Content Includes**:
- Detailed git status and analysis
- Work effort breakdown with technical details
- Project structure and health metrics
- Integration points and dependencies
- Technical health indicators
- Development patterns
- Code change statistics

**Target Audience**: Developers, engineers, technical leads

---

### Scientist Level (Research Depth)

**Content Includes**:
- Deep statistical analysis of activity
- Epistemic state analysis
- Development pattern analysis
- Predictive indicators
- Research-level insights
- Trend analysis
- Correlation analysis
- Advanced metrics

**Target Audience**: Researchers, data scientists, system architects

---

## Integration with Other Commands

This command integrates with:
- `/waft-docs` - Uses document generation system
- `/checkpoint` - Can create checkpoint from status
- `/recap` - Status can inform recap
- `/verify` - Status check can trigger verification
- `/spin-up` - Status is part of spin-up process

**Recommended Sequence**:
```
1. /waft-boot                → Initialize kernel (first time)
2. /waft-status              → Check current state
3. /waft-status --docs       → Generate status documentation
4. /checkpoint               → Create checkpoint with status
5. /recap                    → Recap with status context
```

---

## When to Use

**Use `/waft-status` when**:
- ✅ Need to understand current system state
- ✅ Want to generate status reports
- ✅ Creating handoff documentation
- ✅ Need to document current work for different audiences
- ✅ Checking project health
- ✅ Preparing for next session
- ✅ Need real-time system awareness

**Don't use `/waft-status` when**:
- ❌ Just need git status (use `git status`)
- ❌ Just need work efforts list (use work efforts tools)
- ❌ Need historical analysis only (use `/analyze`)
- ❌ Need session recap (use `/recap`)

---

## Output Summary

After completion, provides:
1. **Status Summary**: Console output with current state
2. **Status Analysis**: Insights and patterns identified
3. **Documentation PDFs**: Generated at requested level(s)
4. **Health Indicators**: Quick health check results
5. **Recommendations**: Suggested next actions

---

## Best Practices

1. **Run Regularly**: Check status at session start/end
2. **Generate Docs**: Create documentation for handoffs
3. **Use Appropriate Level**: Match documentation level to audience
4. **Focus When Needed**: Use --focus for specific areas
5. **Include History**: Use --history for trend analysis
6. **Update Devlog**: Status can inform devlog updates

---

## Implementation Details

### Status Check Components

1. **Git Status Checker**: Analyzes git repository state
2. **Work Efforts Analyzer**: Reviews work efforts system
3. **Project Health Checker**: Validates project structure
4. **Activity Analyzer**: Reviews recent activity
5. **Epistemic State Checker**: Checks Empirica state (if available)
6. **Gamification Checker**: Reviews gamification state

### Documentation Generation

- Uses existing `/waft-docs` infrastructure
- Generates field guide format documents
- Supports all three complexity levels
- Supports printer-friendly versions
- Integrates with binder system for collections

### Output Location

All generated documentation saved to:
```
_work_efforts/showcase_documents/WAFT_Status_[Level]_YYYY-MM-DD.pdf
```

---

## Time Estimates

- **Status Check**: ~5-10 seconds
- **Status Analysis**: ~2-5 seconds
- **Documentation Generation (Single Level)**: ~10-15 seconds
- **Documentation Generation (All Levels)**: ~30-45 seconds

**Total**: ~15-60 seconds depending on options

---

## Error Handling

If any phase fails:
- Document the failure in status output
- Continue with remaining checks if possible
- Note what was skipped
- Provide partial status if available
- Suggest remediation steps

---

**This command provides self-aware system status checking with the ability to generate comprehensive documentation about current state at multiple complexity levels - perfect for understanding what's happening right now and documenting it for different audiences.**

---

End Command ---
