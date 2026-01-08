# Recommended Cursor Commands

**Purpose**: Suggestions for additional commands that would complement the existing command set.

---

## Current Commands

1. **`/verify`** ✅ - Verification with traceable evidence
2. **`/checkpoint`** ✅ - Situation report and status update
3. **`/consider`** ✅ - Analysis and recommendations
4. **`/decide`** ✅ - Decision matrix with mathematical calculations
5. **`/visualize`** ✅ - Quick interactive browser dashboard
6. **`/phase1`** ✅ - Comprehensive data gathering & visualization
7. **`/stats`** ✅ - Session statistics (files, lines, activity)
8. **`/checkout`** ✅ - End chat session workflow
9. **`/spin-up`** ✅ - Quick orientation
10. **`/explore`** ✅ - Deep exploration
11. **`/orient`** ✅ - Project startup process
12. **`/engineering`** ✅ - Complete workflow

---

## Recommended Commands

### 0. `/consider` ✅ - Analysis and Recommendations

**Purpose**: Pause, analyze, and present options with recommendations

**What it does**:
- Analyzes current situation
- Identifies available options
- Evaluates trade-offs (pros/cons, effort, risk)
- Presents recommendations with reasoning
- Supports decision-making

**Use when**: 
- Facing a decision point
- Multiple options available
- Need to evaluate trade-offs
- Want recommendations
- Need to pause and think

**Output**: Structured analysis with recommendations

**Status**: ✅ Created

---

### 0.5. `/decide` ✅ - Decision Matrix with Mathematical Calculations

**Purpose**: Run mathematical decision matrix calculations using documented decision-making techniques

**What it does**:
- Performs multi-step complex calculations
- Uses documented methodologies (WSM, AHP, WPM, BWM)
- Asks interactive questions to gather data
- Calculates weighted scores and rankings
- Provides sensitivity analysis
- Shows transparent calculations

**Use when**: 
- Need quantitative decision analysis
- Multiple alternatives with multiple criteria
- Want mathematical rigor in decision-making
- Need to document decision process
- Want to reduce bias

**Output**: Decision matrix table, calculations, rankings, recommendations

**Status**: ✅ Created

**Note**: Complements `/consider` - `/consider` is qualitative, `/decide` is quantitative

---

### 0.6. `/visualize` ✅ - Quick Interactive Browser Dashboard

**Purpose**: Create a quick interactive browser UI to visualize current state

**What it does**:
- Generates standalone HTML dashboard
- Shows current project state, git status, work efforts
- Interactive elements (expandable sections, filters)
- Visual indicators (charts, progress bars, color coding)
- Auto-opens in browser
- No server required (standalone file)

**Use when**: 
- Need visual insight into current state
- Want to see what's happening at a glance
- Need interactive exploration of data
- Want to share visual snapshot
- Need quick status overview

**Output**: Standalone HTML file that opens in browser

**Status**: ✅ Created

**Note**: Complements `/status` (text) and `waft serve` (live server)

---

### 0.7. `/phase1` ✅ - Comprehensive Data Gathering & Visualization

**Purpose**: Run complete data gathering phase in logical order, then visualize

**What it does**:
- Runs 8 phases of data gathering sequentially
- Environment verification
- Project discovery
- Git status analysis
- Project health check
- Work effort discovery
- Memory layer analysis
- Integration status
- Visualization generation

**Use when**: 
- Starting a new work session
- Need comprehensive overview
- Preparing for handoff
- Investigating issues
- Want complete state snapshot

**Output**: Complete data gathering + interactive visual dashboard

**Status**: ✅ Created

**Note**: Comprehensive version of `/visualize` with full data gathering workflow

---

### 0.8. `/stats` ✅ - Session Statistics

**Purpose**: Show session statistics - files created, lines written, activity tracking

**What it does**:
- Tracks files created/modified/deleted
- Calculates lines written/changed
- Shows top files by changes
- Groups by file type
- Provides productivity metrics

**Use when**: 
- Want to see what was accomplished
- Need productivity metrics
- Creating session reports
- Understanding scope of work

**Output**: Statistics table with breakdowns

**Status**: ✅ Created

**Note**: Use `waft stats --session` for session stats, `waft stats` for gamification stats

---

### 0.9. `/checkout` ✅ - End Chat Session

**Purpose**: End chat session - run all relevant cleanup, documentation, and summary tasks

**What it does**:
- Captures session statistics
- Reviews git status
- Creates session summary
- Saves all documentation
- Prepares for next session

**Use when**: 
- Ending a chat session
- Want to ensure everything is captured
- Need to prepare for next session
- Want comprehensive session recap

**Output**: Complete checkout workflow with summaries

**Status**: ✅ Created

**Note**: Orchestrates multiple end-of-session tasks in logical order

---

**Purpose**: Create a quick interactive browser UI to visualize current state

**What it does**:
- Generates standalone HTML dashboard
- Shows current project state, git status, work efforts
- Interactive elements (expandable sections, filters)
- Visual indicators (charts, progress bars, color coding)
- Auto-opens in browser
- No server required (standalone file)

**Use when**: 
- Need visual insight into current state
- Want to see what's happening at a glance
- Need interactive exploration of data
- Want to share visual snapshot
- Need quick status overview

**Output**: Standalone HTML file that opens in browser

**Status**: ✅ Created

**Note**: Complements `/status` (text) and `waft serve` (live server)

---

**Purpose**: Run mathematical decision matrix calculations using documented decision-making techniques

**What it does**:
- Performs multi-step complex calculations
- Uses documented methodologies (WSM, AHP, WPM, BWM)
- Asks interactive questions to gather data
- Calculates weighted scores and rankings
- Provides sensitivity analysis
- Shows transparent calculations

**Use when**: 
- Need quantitative decision analysis
- Multiple alternatives with multiple criteria
- Want mathematical rigor in decision-making
- Need to document decision process
- Want to reduce bias

**Output**: Decision matrix table, calculations, rankings, recommendations

**Status**: ✅ Created

**Note**: Complements `/consider` - `/consider` is qualitative, `/decide` is quantitative

---

### 1. `/status` - Quick Status Check

**Purpose**: Lightweight status check (lighter than spin-up)

**What it does**:
- Current date/time
- Working directory
- Git status (brief)
- Project health (if applicable)
- Active work (count only)

**Use when**: Need quick status without full orientation

**Output**: One-line summary table

---

### 2. `/context` - Get Current Context

**Purpose**: Summarize current context for handoff or continuation

**What it does**:
- Current working state
- Recent conversation topics
- Active work items
- Key decisions made
- Next steps

**Use when**: 
- Handing off to another session
- Resuming after break
- Need context summary

**Output**: Context summary document

---

### 3. `/sync` - Sync Documentation

**Purpose**: Sync documentation across files

**What it does**:
- Update devlog with recent work
- Sync work effort status
- Update related documentation
- Ensure consistency

**Use when**: Documentation is out of sync

**Output**: List of files updated

---

### 4. `/recap` - Conversation Recap

**Purpose**: Create detailed conversation recap

**What it does**:
- Summarize entire conversation
- Extract key points
- Document decisions
- List accomplishments
- Note questions/unknowns

**Use when**: Need detailed conversation summary

**Output**: Recap document in `_work_efforts/`

**Note**: Similar to checkpoint but more conversation-focused

---

### 5. `/todos` - Todo Management

**Purpose**: Manage and track todos

**What it does**:
- List current todos
- Add new todos
- Update todo status
- Show todo history

**Use when**: Need to track tasks

**Output**: Todo list and management

---

### 6. `/links` - Create Documentation Links

**Purpose**: Create bidirectional links between documents

**What it does**:
- Find related documents
- Create links between them
- Update indexes
- Maintain link integrity

**Use when**: Documents need to reference each other

**Output**: Updated documents with links

---

### 7. `/search` - Search Documentation

**Purpose**: Search across documentation

**What it does**:
- Search `_work_efforts/` files
- Search `_pyrite/` files
- Search codebase
- Return relevant results

**Use when**: Need to find information

**Output**: Search results with context

---

### 8. `/cleanup` - Cleanup and Maintenance

**Purpose**: Clean up temporary files and organize

**What it does**:
- Remove temporary files
- Organize `_pyrite/active/` files
- Archive old checkpoints
- Clean up test files

**Use when**: Need to organize or clean up

**Output**: List of actions taken

---

## Priority Recommendations

### High Priority (Most Useful)

0. **`/consider`** ✅ - Analysis and recommendations (qualitative decision support)
0.5. **`/decide`** ✅ - Decision matrix calculations (quantitative decision support)
1. **`/status`** - Quick status check (very useful, lightweight)
2. **`/context`** - Context summary (great for handoffs)
3. **`/recap`** - Conversation recap (complements checkpoint)

### Medium Priority (Nice to Have)

4. **`/sync`** - Documentation sync (useful but less frequent)
5. **`/todos`** - Todo management (if not using external system)
6. **`/search`** - Documentation search (useful for large projects)

### Low Priority (Optional)

7. **`/links`** - Documentation links (nice but manual works)
8. **`/cleanup`** - Cleanup (occasional use)

---

## Command Design Principles

When creating new commands, follow these principles:

1. **Lightweight**: Fast execution, minimal overhead
2. **Focused**: One clear purpose
3. **Traceable**: Document what was done
4. **Incremental**: Builds on previous work
5. **Evolve**: Can grow and change

---

## Implementation Order

Suggested implementation order:

1. ✅ `/verify` - Done
2. ✅ `/checkpoint` - Done
3. ✅ `/consider` - Done
4. ✅ `/decide` - Done (mathematical decision support)
5. ✅ `/visualize` - Done (quick interactive browser dashboard)
6. ✅ `/phase1` - Done (comprehensive data gathering & visualization)
7. **`/status`** - Next (quick win, very useful)
6. **`/context`** - After status (complements checkpoint)
7. **`/recap`** - After context (detailed version)
8. Others as needed

---

**These recommendations are based on common workflows and patterns observed in the codebase.**
