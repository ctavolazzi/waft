# Auto Work

**Think about work efforts, pick the best one, and execute it autonomously.**

Analyzes all work efforts, calculates priorities based on status, priority level, content indicators (TODOs, FIXMEs), and recent activity. Selects the best work effort, determines the optimal action, and executes it autonomously.

**Use when:** Want the system to autonomously work on work efforts, need intelligent prioritization, or want hands-off work execution.

---

## Purpose

This command provides:
- **Intelligent Analysis**: Analyzes all work efforts with priority scoring
- **Autonomous Selection**: Picks the best work effort automatically
- **Action Determination**: Identifies the best action to take
- **Autonomous Execution**: Executes the work effort action directly

---

## Usage

```bash
# Automatically work on the best work effort
/auto-work

# See what would be done without executing
/auto-work --dry-run

# Verbose output
/auto-work --verbose
```

---

## How It Works

### 1. Analysis Phase
- Gathers all work efforts from `_work_efforts/`
- Filters out completed work efforts
- Calculates priority scores for each

### 2. Priority Scoring

**Status Weighting**:
- `active`: 100 points (highest priority)
- `paused`: 50 points
- `open`: 30 points
- `completed`: 0 points (excluded)

**Priority Level**:
- `CRITICAL`: +50 points
- `HIGH`: +30 points
- `MEDIUM`: +15 points
- `LOW`: +5 points

**Content Indicators**:
- Contains `TODO`: +20 points
- Contains `FIXME`: +25 points
- Contains `bug`/`error`: +15 points

**Activity**:
- Recent git commits (last 7 days): +5 points per commit (max 20)

### 3. Selection Phase
- Sorts work efforts by priority score
- Selects the highest scoring work effort

### 4. Action Determination
- Analyzes available actions for selected work effort
- Sorts by priority (high > medium > low)
- Selects the highest priority action

### 5. Execution Phase
- Outputs selected work effort and action
- Cursor AI executes the action autonomously

---

## Examples

### Basic Usage

```bash
/auto-work
```

**Output**:
```
🤔 Thinking about work efforts...

📋 Found 15 work effort(s)
✅ 8 actionable work effort(s)

🎯 Selecting best work effort to work on...

✅ Selected: WE-260118-abc1
   Title: Implement User Authentication
   Status: active

🔍 Analyzing available actions...

✅ Best action: Address TODOs
   Reason: Work effort contains TODO items
   Command: Review and address TODOs in work effort WE-260118-abc1

🚀 Preparing action...

✅ Work effort and action selected!

[AI then executes the work effort]
```

### Dry Run

```bash
/auto-work --dry-run
```

Shows what would be selected and executed without actually doing it.

---

## Integration

This command:
- Uses `scripts/show_me.py` for work effort collection
- Uses `scripts/work_dashboard.py` for action analysis
- Integrates with work effort system
- Can be extended with Empirica gates for safety

---

## Safety

**Current Implementation**:
- Outputs structured JSON for Cursor AI to execute
- AI executes in Cursor context with full awareness

**Future Enhancements**:
- Empirica safety gates (PROCEED/HALT/BRANCH/REVISE)
- Human approval for high-risk actions
- Execution logging and audit trail

---

## Decision Logic

The priority scoring algorithm ensures:
1. **Active work** is prioritized over new work
2. **Critical/High priority** work efforts are favored
3. **Work with TODOs/FIXMEs** gets attention
4. **Recently active** work efforts are prioritized
5. **Completed work** is excluded

---

## Troubleshooting

**No work efforts found**:
- Check that `_work_efforts/` directory exists
- Verify work effort directories follow `WE-YYMMDD-xxxx` format

**No actionable work efforts**:
- All work efforts may be completed
- Create new work efforts or reopen paused ones

**Action not available**:
- Work effort may not have index file
- Check work effort structure and files

---

## Future Enhancements

- Empirica integration for safety gates
- Multi-work-effort execution (batch mode)
- Learning from execution results
- Adaptive priority scoring
- Execution history and analytics

---

**Auto Work - Think, pick, execute. Autonomous work effort management.**
