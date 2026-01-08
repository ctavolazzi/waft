# Analytics

**View and analyze historical session data - productivity trends, prompt drift, and approach comparisons.**

Provides comprehensive analytics on session data collected over time, enabling data-driven insights into productivity patterns, prompt effectiveness, and approach comparisons. Foundation for future automated prompt optimization and meta-learning.

**Use when:** You want to understand productivity trends, analyze prompt drift, compare different approaches, or prepare for automated optimization.

---

## Purpose

This command provides:
- **Historical Analysis**: View sessions over time
- **Productivity Trends**: Track files, lines, and activity patterns
- **Prompt Drift Analysis**: See how prompts evolve over time
- **Approach Comparison**: Compare different categories/approaches
- **Iteration Chains**: Track linked sessions and iterations
- **Data Foundation**: Build dataset for automated optimization

---

## Philosophy

1. **Data-Driven**: Use actual metrics, not assumptions
2. **Historical Context**: Understand patterns over time
3. **Comparative**: Enable approach comparison
4. **Foundation**: Build toward automated optimization
5. **Transparent**: Show what data is being used

---

## Available Commands

### 1. `waft analytics sessions`
List recent sessions with filters.

**Options**:
- `--days, -d`: Number of days to show (default: 30)
- `--category, -c`: Filter by category
- `--limit, -l`: Maximum sessions to show (default: 20)

**Example**:
```bash
waft analytics sessions --days 7 --category command_creation
```

---

### 2. `waft analytics trends`
Show productivity trends over time.

**Options**:
- `--days, -d`: Number of days to analyze (default: 30)

**Shows**:
- Total sessions, files, lines
- Average per session
- Breakdown by category
- Daily trends

**Example**:
```bash
waft analytics trends --days 60
```

---

### 3. `waft analytics drift`
Analyze prompt drift (how prompts change over time).

**Options**:
- `--days, -d`: Number of days to analyze (default: 30)

**Shows**:
- Unique prompt signatures
- Sessions per prompt
- Average productivity per prompt
- Success rates

**Example**:
```bash
waft analytics drift --days 90
```

---

### 4. `waft analytics compare`
Compare two approach categories.

**Arguments**:
- `category1`: First category to compare
- `category2`: Second category to compare

**Options**:
- `--days, -d`: Number of days to analyze (default: 30)

**Shows**:
- Side-by-side comparison
- Count, files, lines, success rates

**Example**:
```bash
waft analytics compare command_creation testing --days 30
```

---

### 5. `waft analytics chains`
Show iteration chains (linked sessions).

**Shows**:
- All iteration chains
- Sessions in each chain
- Chain length

**Example**:
```bash
waft analytics chains
```

---

## Data Collection

Data is automatically collected when you run `/checkout`:

- **Session ID**: Unique identifier
- **Timestamp**: When session occurred
- **File Metrics**: Created, modified, deleted
- **Code Metrics**: Lines written, modified, deleted
- **Activity**: Commands executed, work efforts
- **Context**: Project, branch, git status
- **Prompt Signature**: Hash of prompt characteristics
- **Category**: Inferred approach category
- **Iteration Chain**: Links to previous sessions
- **Outcomes**: Success indicators, issues

---

## Storage

### Database
- **Location**: `_pyrite/analytics/sessions.db`
- **Format**: SQLite database
- **Schema**: Structured tables with indexes

### JSON Files
- **Location**: `_pyrite/analytics/sessions/*.json`
- **Format**: Individual session records
- **Purpose**: Easy inspection and backup

---

## Categories

Sessions are automatically categorized:

- **`command_creation`**: Creating Cursor commands
- **`testing`**: Writing or running tests
- **`core_development`**: Core module development
- **`documentation`**: Documentation work
- **`general_development`**: Other development work

---

## Future: Automated Optimization

This analytics system is the foundation for:

1. **Prompt Generation**: Automatically generate new prompts
2. **A/B Testing**: Test different prompts in parallel
3. **Gladiatorial Ring**: Compete prompts against each other
4. **Iteration Tracking**: Track which prompts lead to better outcomes
5. **Meta-Learning**: System learns what works best

### Planned Features

- **Prompt Variants**: Generate variations of successful prompts
- **Automated Testing**: Run prompts in controlled environments
- **Performance Metrics**: Track success rates, productivity, quality
- **Chain Analysis**: Understand which prompt sequences work best
- **Recommendation Engine**: Suggest optimal prompts for tasks

---

## Use Cases

### 1. Productivity Analysis
**Scenario**: Want to understand productivity patterns

**Example**:
```bash
waft analytics trends --days 30
```

**Output**: Shows average files/lines per session, trends over time

---

### 2. Prompt Effectiveness
**Scenario**: Want to see which prompts are most effective

**Example**:
```bash
waft analytics drift --days 60
```

**Output**: Shows prompt signatures with success rates

---

### 3. Approach Comparison
**Scenario**: Want to compare two approaches

**Example**:
```bash
waft analytics compare command_creation testing
```

**Output**: Side-by-side comparison of metrics

---

### 4. Iteration Tracking
**Scenario**: Want to see linked sessions

**Example**:
```bash
waft analytics chains
```

**Output**: Shows iteration chains and their sessions

---

## Integration

### With `/checkout`
- Automatically saves session data
- Creates analytics records
- Links to iteration chains

### With Other Commands
- `/stats`: Can show historical context
- `/phase1`: Can include analytics in visualization
- `/checkpoint`: Can reference analytics data

---

## Data Privacy

- **Local Only**: All data stored locally in `_pyrite/analytics/`
- **No External**: Never sent to external services
- **User Control**: You control what gets tracked
- **Optional**: Can disable analytics if desired

---

## Technical Details

### Database Schema

```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    duration_seconds REAL,
    files_created INTEGER,
    files_modified INTEGER,
    lines_written INTEGER,
    net_lines INTEGER,
    commands_executed TEXT,  -- JSON
    prompt_signature TEXT,
    approach_category TEXT,
    iteration_chain TEXT,
    success_indicators TEXT,  -- JSON
    metadata TEXT,  -- JSON
    ...
)
```

### Indexes
- `timestamp`: For time-based queries
- `category`: For category filtering
- `chain`: For iteration chain queries
- `prompt`: For prompt analysis

---

## Best Practices

1. **Run `/checkout`**: Ensures data is collected
2. **Review Trends**: Check productivity regularly
3. **Compare Approaches**: Understand what works
4. **Track Chains**: See how iterations evolve
5. **Use for Decisions**: Make data-driven choices

---

## Example Output

```
📊 Productivity Trends (Last 30 days)

Total Sessions: 45
Total Files: 234
Total Lines: 12,456
Avg Files/Session: 5.2
Avg Lines/Session: 276.8

By Category:
┌─────────────────────┬──────────┬────────┬─────────┐
│ Category            │ Sessions │ Files  │ Lines   │
├─────────────────────┼──────────┼────────┼─────────┤
│ command_creation    │ 12       │ 45     │ 3,456   │
│ core_development    │ 18       │ 89     │ 5,234   │
│ documentation       │ 9        │ 34     │ 1,234   │
│ testing             │ 6        │ 66     │ 2,532   │
└─────────────────────┴──────────┴────────┴─────────┘
```

---

**This command provides the foundation for data-driven development and future automated optimization.**
