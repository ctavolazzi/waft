# Decision Engine - Phase 3: Persistence & Tracking

**Status**: 🎯 Design Phase

**Purpose**: Complete the decision engine with persistence, tracking, and decision history.

---

## Current State

### ✅ Phase 1: Mathematical Engine (Complete)
- `decision_matrix.py` - Pure calculation engine
- WSM, WPM, AHP, BWM methodologies
- Validation, ranking, sensitivity analysis
- **Status**: Production-ready, fully documented

### ✅ Phase 2: Interface Layer (Complete)
- `decision_cli.py` - Standardized CLI interface
- Input validation, data building, output formatting
- Rich tables, detailed breakdowns
- **Status**: Production-ready, fully documented

### 🎯 Phase 3: Persistence & Tracking (Design)
- Decision history storage
- Decision tracking over time
- Decision templates
- Decision export/import
- Decision comparison
- **Status**: Design phase

---

## Phase 3 Requirements

### Core Features

1. **Decision Persistence**
   - Save decisions to `_pyrite/decisions/`
   - JSON format for machine-readable
   - Markdown format for human-readable
   - Timestamped, searchable

2. **Decision History**
   - Track all decisions over time
   - Query by problem, date, recommendation
   - Compare decisions
   - Decision audit trail

3. **Decision Templates**
   - Save decision structures (criteria, alternatives)
   - Reuse for similar decisions
   - Template library
   - Template versioning

4. **Decision Export**
   - Export to JSON
   - Export to Markdown
   - Export to CSV (for analysis)
   - Export to HTML (visualization)

5. **Decision Comparison**
   - Compare similar decisions
   - Track decision evolution
   - Identify patterns
   - Learn from past decisions

6. **Decision Analytics**
   - Decision frequency
   - Most common criteria
   - Most common alternatives
   - Decision outcome tracking

---

## Architecture Design

### File Structure

```
_pyrite/
└── decisions/
    ├── decisions.db              # SQLite database (decisions, templates)
    ├── templates/                # Decision templates
    │   ├── template-001.json     # Template: "Feature Priority"
    │   ├── template-002.json     # Template: "Architecture Choice"
    │   └── ...
    └── history/                  # Decision history
        ├── 2026-01-07/
        │   ├── decision-001.json
        │   ├── decision-001.md
        │   └── ...
        └── ...
```

### Database Schema

```sql
-- Decisions table
CREATE TABLE decisions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    problem TEXT NOT NULL,
    alternatives TEXT NOT NULL,  -- JSON array
    criteria TEXT NOT NULL,       -- JSON object
    scores TEXT NOT NULL,         -- JSON object
    methodology TEXT NOT NULL,
    recommendation TEXT,
    results TEXT,                 -- JSON object
    rankings TEXT,                -- JSON array
    metadata TEXT                 -- JSON object (tags, context, etc.)
);

-- Templates table
CREATE TABLE templates (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    alternatives TEXT NOT NULL,  -- JSON array
    criteria TEXT NOT NULL,       -- JSON object (with default weights)
    created_at TEXT NOT NULL,
    updated_at TEXT,
    usage_count INTEGER DEFAULT 0
);

-- Decision tags (many-to-many)
CREATE TABLE decision_tags (
    decision_id TEXT,
    tag TEXT,
    PRIMARY KEY (decision_id, tag)
);
```

---

## Implementation Plan

### Step 1: Decision Persistence Module

**File**: `src/waft/core/decision_persistence.py`

**Class**: `DecisionPersistence`

**Methods**:
- `save_decision(decision_data: Dict) -> str` - Save decision, return ID
- `load_decision(decision_id: str) -> Dict` - Load decision by ID
- `list_decisions(filters: Dict) -> List[Dict]` - Query decisions
- `delete_decision(decision_id: str) -> bool` - Delete decision

**Storage**:
- SQLite database for queries
- JSON files for human-readable
- Markdown files for documentation

---

### Step 2: Decision Templates Module

**File**: `src/waft/core/decision_templates.py`

**Class**: `DecisionTemplateManager`

**Methods**:
- `create_template(name, alternatives, criteria) -> str` - Create template
- `load_template(template_id: str) -> Dict` - Load template
- `list_templates() -> List[Dict]` - List all templates
- `use_template(template_id: str) -> Dict` - Get template for use
- `update_template(template_id: str, updates: Dict) -> bool` - Update template

**Features**:
- Template versioning
- Usage tracking
- Template categories

---

### Step 3: Decision History Module

**File**: `src/waft/core/decision_history.py`

**Class**: `DecisionHistory`

**Methods**:
- `get_recent_decisions(limit: int = 10) -> List[Dict]` - Recent decisions
- `search_decisions(query: str) -> List[Dict]` - Search by problem/criteria
- `compare_decisions(decision_ids: List[str]) -> Dict` - Compare decisions
- `get_decision_timeline(problem_pattern: str) -> List[Dict]` - Decision evolution
- `get_statistics() -> Dict` - Decision analytics

**Features**:
- Full-text search
- Decision comparison
- Pattern recognition
- Analytics dashboard

---

### Step 4: Enhanced DecisionCLI

**Updates to**: `src/waft/core/decision_cli.py`

**New Methods**:
- `save_decision(results: Dict) -> str` - Save after calculation
- `load_decision(decision_id: str) -> Dict` - Load for review
- `use_template(template_id: str) -> Dict` - Use template
- `export_decision(decision_id: str, format: str) -> Path` - Export decision

**Enhanced `run_decision_matrix`**:
- Auto-save option (default: True)
- Template support
- Export options

---

### Step 5: CLI Commands

**New Commands in**: `src/waft/main.py`

```python
@app.command()
def decision_history(
    limit: int = typer.Option(10, "--limit", "-l"),
    search: Optional[str] = typer.Option(None, "--search", "-s"),
):
    """List decision history."""

@app.command()
def decision_show(
    decision_id: str = typer.Argument(...),
):
    """Show a specific decision."""

@app.command()
def decision_export(
    decision_id: str = typer.Argument(...),
    format: str = typer.Option("json", "--format", "-f"),
):
    """Export a decision."""

@app.command()
def decision_template(
    name: str = typer.Option(None, "--name", "-n"),
    create: bool = typer.Option(False, "--create", "-c"),
    list_all: bool = typer.Option(False, "--list", "-l"),
):
    """Manage decision templates."""

@app.command()
def decision_compare(
    decision_ids: List[str] = typer.Argument(...),
):
    """Compare multiple decisions."""
```

---

## Data Flow

```mermaid
flowchart TD
    User[User] --> Decide[/decide command]
    Decide --> CLI[DecisionCLI.run_decision_matrix]
    CLI --> Calc[Calculate Results]
    Calc --> Results[Results Dict]
    Results --> Save{Save Decision?}
    Save -->|Yes| Persist[DecisionPersistence.save_decision]
    Save -->|No| Display[Display Results]
    Persist --> DB[(SQLite Database)]
    Persist --> JSON[JSON File]
    Persist --> MD[Markdown File]
    Persist --> Display
    
    Template[Use Template?] --> CLI
    History[View History?] --> HistoryCLI[DecisionHistory]
    HistoryCLI --> DB
    Compare[Compare Decisions?] --> CompareCLI[DecisionHistory.compare]
    CompareCLI --> DB
```

---

## Integration Points

### 1. Integration with `/consider`
- `/consider` identifies options and criteria
- `/decide` uses that output to auto-populate decision matrix
- Decision saved automatically

### 2. Integration with Work Efforts
- Link decisions to work efforts
- Track decision outcomes
- Update work efforts based on decisions

### 3. Integration with Analytics
- Track decision frequency
- Analyze decision patterns
- Measure decision quality

### 4. Integration with Checkout
- Include recent decisions in checkout summary
- Track decisions made during session

---

## Example Usage

### Save Decision Automatically

```python
# Decision is automatically saved after calculation
results = cli.run_decision_matrix(
    problem="Which feature to build?",
    alternatives=["Feature A", "Feature B"],
    criteria={"Value": 0.6, "Effort": 0.4},
    scores={...},
    save=True  # Default: True
)

# Decision ID returned
decision_id = results["decision_id"]
```

### Use Template

```python
# Load template
template = template_manager.load_template("feature-priority")

# Use template (pre-fills alternatives and criteria)
results = cli.run_decision_matrix(
    problem="Which feature to build next?",
    template_id="feature-priority",  # Use template
    scores={...}  # Only need to provide scores
)
```

### View History

```bash
# List recent decisions
waft decision-history --limit 20

# Search decisions
waft decision-history --search "dashboard"

# Show specific decision
waft decision-show decision-001

# Compare decisions
waft decision-compare decision-001 decision-002 decision-003
```

### Export Decision

```bash
# Export to JSON
waft decision-export decision-001 --format json

# Export to Markdown
waft decision-export decision-001 --format markdown

# Export to HTML
waft decision-export decision-001 --format html
```

---

## Benefits

1. **Decision Audit Trail**
   - Track all decisions made
   - Understand decision history
   - Learn from past decisions

2. **Decision Reusability**
   - Templates for common decisions
   - Faster decision-making
   - Consistency across decisions

3. **Decision Learning**
   - Compare similar decisions
   - Identify patterns
   - Improve decision quality

4. **Decision Accountability**
   - Full decision record
   - Traceable decisions
   - Decision documentation

---

## Implementation Priority

### Phase 3.1: Basic Persistence (High Priority)
- Save decisions to JSON/Markdown
- List recent decisions
- Load decision by ID
- **Effort**: 2-3 hours

### Phase 3.2: Templates (Medium Priority)
- Create/load templates
- Use templates in decisions
- Template library
- **Effort**: 2-3 hours

### Phase 3.3: History & Analytics (Medium Priority)
- SQLite database
- Search functionality
- Decision comparison
- **Effort**: 3-4 hours

### Phase 3.4: Advanced Features (Low Priority)
- Decision visualization
- Decision export formats
- Decision integration with other systems
- **Effort**: 2-3 hours

---

## Next Steps

1. **Design Review** - Review this design
2. **Implementation** - Start with Phase 3.1 (Basic Persistence)
3. **Testing** - Test persistence and retrieval
4. **Documentation** - Update decision engine docs
5. **Integration** - Integrate with `/consider` and other commands

---

**Phase 3 completes the decision engine with persistence, tracking, and decision history - making it a complete decision-making system.**
