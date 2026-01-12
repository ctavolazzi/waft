# Work Effort Tool Bag - Standard System

**Created**: 2026-01-10  
**Status**: ✅ Active Standard  
**Purpose**: Every work effort now automatically includes a tool bag

---

## Overview

**New Standard**: All work efforts now include a `tools/` folder with essential tools from creation.

**Benefits**:
- ✅ Self-contained work efforts
- ✅ Consistent structure
- ✅ Tools available immediately
- ✅ No need to remember to add tools

---

## Standard Workflow

### When Creating a Work Effort

**Automatic Process**:
1. Create work effort folder: `WE-YYMMDD-xxxx_description/`
2. Create index file: `WE-YYMMDD-xxxx_index.md`
3. **Automatically create `tools/` folder** with:
   - `tools/README.md` - Tool bag documentation
   - `tools/work_effort_tracker.md` - Progress tracking template
   - `tools/verification_checklist.md` - Verification checklist

**Manual Process** (if automation not available):
```bash
# Option 1: Use setup script
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description

# Option 2: Copy template manually
cp -r _work_efforts/.tool_bag_template/* _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

---

## Tool Bag Structure

```
tools/
├── README.md                    # Tool bag documentation (always)
├── work_effort_tracker.md      # Progress tracking (always)
├── verification_checklist.md   # Verification checklist (always)
└── [optional tools...]         # Added as needed
```

---

## Essential Tools (Always Included)

### 1. Work Effort Tracker
**File**: `tools/work_effort_tracker.md`

**Purpose**: Track progress, status, dependencies, milestones

**Usage**:
- Copy template to track specific work effort
- Update status regularly
- Document decisions and blockers

### 2. Verification Checklist
**File**: `tools/verification_checklist.md`

**Purpose**: Verify project state, quality, completion

**Usage**:
- Run before completing work effort
- Check all items
- Document issues found

### 3. README
**File**: `tools/README.md`

**Purpose**: Document all tools in tool bag

**Usage**:
- Explains what tools are available
- How to use each tool
- When to add optional tools

---

## Optional Tools (Add As Needed)

### Decision-Making Tools
**When to add**: Work effort involves decision-making or prioritization

**Tools**:
- `decision_matrix.py` - Decision matrix calculator
- `priority_matrix.py` - Priority matrix calculator
- `templates/decision_matrix_template.md` - Decision template
- `templates/priority_matrix_template.md` - Priority template

**Source**: Copy from `_work_efforts/WE-260110-order66_order_66_execution/tools/`

### Analysis Tools
**When to add**: Work effort involves analysis or evaluation

**Tools**:
- `analysis_template.md` - Analysis document template

**Source**: Copy from `_work_efforts/WE-260110-order66_order_66_execution/tools/`

### Custom Tools
**When to add**: Work effort needs project-specific utilities

**Examples**:
- Custom scripts
- Specialized templates
- Workflow automation
- Data processing utilities

---

## Automation

### Setup Script

**Location**: `scripts/setup_work_effort_tools.py`

**Usage**:
```bash
# Basic setup (essential tools only)
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description

# With optional tools
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description --include-optional
```

**What it does**:
1. Creates `tools/` folder
2. Copies essential tools from template
3. Updates README with work effort info
4. Creates `templates/` folder structure

### Template Location

**Location**: `_work_efforts/.tool_bag_template/`

**Contents**:
- `README.md` - Tool bag documentation template
- `work_effort_tracker.md` - Tracker template
- `verification_checklist.md` - Checklist template

---

## Procedure

**Procedure**: `CMD-002` - Create Work Effort with Tool Bag

**Shortcode**: `/CMD-002` or `/create-work-effort`

**Steps**:
1. Create work effort structure
2. Setup tool bag (automatic or manual)
3. Add optional tools (if needed)
4. Update work effort index
5. Create tickets (if needed)
6. Document in index

**See**: `.cursor/procedures/CMD-002_create_work_effort_with_tools.md`

---

## Integration Points

### MCP Work Efforts Server
**Future Enhancement**: MCP server could automatically set up tools when creating work effort

**Current**: Use setup script after MCP creation

### Commands That Create Work Efforts
- `/engineer` - Creates work efforts during planning
- Manual creation via MCP
- Any procedure that creates work efforts

**All should**: Run tool bag setup after creation

---

## Examples

### Example 1: Basic Work Effort
```bash
# Create work effort
mcp_work-efforts_create_work_effort(...)

# Setup tool bag
python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-xxxx_description
```

**Result**: Work effort with essential tools ready to use

### Example 2: Work Effort with Decision-Making
```bash
# Create work effort
mcp_work-efforts_create_work_effort(...)

# Setup tool bag with optional tools
python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-xxxx_description --include-optional

# Or manually copy decision tools
cp _work_efforts/WE-260110-order66_order_66_execution/tools/decision_matrix.py _work_efforts/WE-260110-xxxx_description/tools/
cp _work_efforts/WE-260110-order66_order_66_execution/tools/priority_matrix.py _work_efforts/WE-260110-xxxx_description/tools/
```

**Result**: Work effort with essential + decision-making tools

---

## Best Practices

1. **Always create tools folder** - Don't skip, it's now standard
2. **Start with essentials** - Don't over-engineer
3. **Add tools as needed** - Add optional tools when you need them
4. **Document additions** - Update README when adding tools
5. **Reuse tools** - Copy tools from other work efforts
6. **Keep it simple** - Tools should be easy to use

---

## Migration

### Existing Work Efforts

**For existing work efforts without tools**:
1. Run setup script:
   ```bash
   python scripts/setup_work_effort_tools.py _work_efforts/WE-XXXX-xxxx_description
   ```
2. Or manually copy template
3. Update work effort index to reference tools

### New Work Efforts

**All new work efforts**:
- ✅ Automatically include tools folder
- ✅ Essential tools always present
- ✅ Optional tools added as needed

---

## Tool Bag Template

**Location**: `_work_efforts/.tool_bag_template/`

**Purpose**: Source template for all new work effort tool bags

**Contents**:
- `README.md` - Documentation template
- `work_effort_tracker.md` - Tracker template
- `verification_checklist.md` - Checklist template

**Usage**: Copied to new work efforts automatically or manually

---

## Success Criteria

**Work effort has tool bag when**:
- ✅ `tools/` folder exists
- ✅ `tools/README.md` exists
- ✅ `tools/work_effort_tracker.md` exists
- ✅ `tools/verification_checklist.md` exists
- ✅ Work effort index references tools

---

## Future Enhancements

1. **MCP Integration**: MCP server automatically sets up tools
2. **Tool Library**: Shared location for common tools
3. **Tool Versioning**: Track tool versions
4. **Tool Testing**: Validate tools work
5. **Tool Templates**: More specialized templates

---

## Related

- **Procedure**: `CMD-002` - Create Work Effort with Tool Bag
- **Template**: `_work_efforts/.tool_bag_template/`
- **Script**: `scripts/setup_work_effort_tools.py`
- **Example**: `WE-260110-order66_order_66_execution/tools/`

---

**Standard Established**: 2026-01-10  
**Status**: ✅ Active - All new work efforts include tool bag
