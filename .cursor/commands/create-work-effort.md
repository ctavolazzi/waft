# Create Work Effort

**Create a new work effort with automatic tool bag setup.**

Creates a new work effort following the standard structure, including automatic setup of the tool bag with essential tools. Ensures every work effort has the tools it needs from the start.

**Use when:** Starting new work that needs tracking, creating a work effort, or need to ensure tools are included.

---

## Purpose

This command provides:
- **Work Effort Creation**: Creates work effort folder and index file
- **Tool Bag Setup**: Automatically creates tools folder with essential tools
- **Standard Structure**: Follows established work effort patterns
- **Documentation**: Sets up tracking and verification tools

---

## Standard Workflow

### Step 1: Create Work Effort Structure
1. Generate work effort ID: `WE-YYMMDD-xxxx_description`
2. Create work effort folder
3. Create index file with frontmatter
4. Add metadata (id, title, status, priority, etc.)

### Step 2: Setup Tool Bag (Automatic)
1. Create `tools/` folder
2. Copy essential tools from template:
   - `tools/README.md`
   - `tools/work_effort_tracker.md`
   - `tools/verification_checklist.md`
3. Update README with work effort info

### Step 3: Add Optional Tools (If Needed)
1. **If decision-making needed**:
   - Copy decision matrix tools from Order 66
2. **If analysis needed**:
   - Copy analysis template from Order 66
3. **If custom tools needed**:
   - Create project-specific tools

### Step 4: Update Index
1. Add "Tools Available" section
2. Reference `tools/README.md`
3. Document any optional tools

---

## Usage Examples

### Basic Work Effort Creation
```
/create-work-effort --title "Feature Implementation" --description "Implement new feature X"
```

**Output**:
- Creates `WE-260110-xxxx_feature_implementation/`
- Sets up `tools/` folder with essential tools
- Creates index file with metadata

### Work Effort with Optional Tools
```
/create-work-effort --title "Decision Analysis" --description "Analyze options" --include-decision-tools
```

**Output**:
- Creates work effort structure
- Sets up essential tools
- Adds decision matrix and priority matrix tools

### Manual Tool Bag Setup
```
# After creating work effort manually
python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-xxxx_description
```

---

## Tool Bag Contents

### Always Included
- ✅ `tools/README.md` - Tool bag documentation
- ✅ `tools/work_effort_tracker.md` - Progress tracking template
- ✅ `tools/verification_checklist.md` - Verification checklist

### Optional (Add As Needed)
- `tools/decision_matrix.py` - Decision calculator
- `tools/priority_matrix.py` - Priority calculator
- `tools/analysis_template.md` - Analysis template
- `tools/templates/` - Template folder

---

## Integration

### With MCP Work Efforts Server
```python
# Create work effort via MCP
mcp_work-efforts_create_work_effort(...)

# Then setup tool bag
python scripts/setup_work_effort_tools.py <work_effort_path>
```

### With Procedures
- `CMD-002` - Create Work Effort with Tool Bag (detailed procedure)
- `ENG-001` - Full Engineering Workflow (creates work efforts)

---

## Automation

**Setup Script**: `scripts/setup_work_effort_tools.py`

**Template Location**: `_work_efforts/.tool_bag_template/`

**Automatic Process**:
1. Script copies template to work effort
2. Updates README with work effort info
3. Creates folder structure
4. Ready to use immediately

---

## When to Use

**Use `/create-work-effort` when**:
- ✅ Starting new work that needs tracking
- ✅ Creating a work effort
- ✅ Need to ensure tools are included
- ✅ Want standardized structure

**Don't use `/create-work-effort` when**:
- ❌ Work effort already exists (use update instead)
- ❌ Just need to add tools (use setup script directly)
- ❌ Quick task (use simpler tracking)

---

## Best Practices

1. **Always include tools** - Don't skip tool bag setup
2. **Start with essentials** - Add optional tools as needed
3. **Document tools** - Update README when adding tools
4. **Reuse tools** - Copy from other work efforts
5. **Keep it simple** - Don't over-engineer

---

## Related Commands

- `/procedure CMD-002` - Detailed procedure for work effort creation
- `/engineer` - Creates work efforts during engineering workflow
- `/verify` - Uses verification checklist from tool bag

---

**This command ensures every work effort has the tools it needs from the start - making work efforts self-contained and consistent.**

--- End Command ---
