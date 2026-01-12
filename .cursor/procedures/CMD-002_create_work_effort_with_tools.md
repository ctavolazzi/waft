# Procedure: Create Work Effort with Tool Bag

**Shortcode**: CMD-002
**Category**: Command Creation
**Created**: 2026-01-10
**Updated**: 2026-01-10
**Status**: Active
**Aliases**: `/create-work-effort`, `/new-work-effort`

## Description

Standardized procedure for creating new work efforts with automatic tool bag setup. Ensures every work effort has essential tools from the start.

## Use When

- Creating a new work effort
- Need to ensure tools are included
- Want standardized work effort structure

## Prerequisites

- Work effort path determined
- Work effort ID generated (WE-YYMMDD-xxxx format)
- Work effort title/description ready

## Steps

### Step 1: Create Work Effort Structure
1. Create work effort folder: `WE-YYMMDD-xxxx_description/`
2. Create index file: `WE-YYMMDD-xxxx_index.md`
3. Add frontmatter with metadata:
   - id, title, status, priority
   - created, created_by, last_updated
   - branch, repository

### Step 2: Setup Tool Bag
1. Run tool bag setup script:
   ```bash
   python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description
   ```
2. Or manually copy from template:
   ```bash
   cp -r _work_efforts/.tool_bag_template/* _work_efforts/WE-YYMMDD-xxxx_description/tools/
   ```
3. Verify tools folder created with:
   - `tools/README.md`
   - `tools/work_effort_tracker.md`
   - `tools/verification_checklist.md`

### Step 3: Add Optional Tools (If Needed)
1. **If decision-making needed**:
   - Copy `decision_matrix.py` from Order 66 tools
   - Copy `priority_matrix.py` from Order 66 tools
   - Copy decision/priority templates
2. **If analysis needed**:
   - Copy `analysis_template.md` from Order 66 tools
3. **If custom tools needed**:
   - Create project-specific scripts/templates

### Step 4: Update Work Effort Index
1. Add "Tools Available" section to index
2. Reference `tools/README.md`
3. List any optional tools added

### Step 5: Create Tickets (If Needed)
1. Create `tickets/` folder if tickets needed
2. Use MCP: `mcp_work-efforts_create_ticket`
3. Link tickets to work effort

### Step 6: Document in Index
1. Update index with tool bag information
2. Add link to tools README
3. Document any custom tools

## Expected Output

After completing this procedure, you will have:
- ✅ Work effort folder with index file
- ✅ Tools folder with essential tools
- ✅ README documenting all tools
- ✅ Work effort tracker ready to use
- ✅ Verification checklist ready to use
- ✅ Optional tools (if needed)

## Tool Bag Contents

### Always Included
- `tools/README.md` - Tool bag documentation
- `tools/work_effort_tracker.md` - Progress tracking template
- `tools/verification_checklist.md` - Verification checklist

### Optional (Add As Needed)
- `tools/decision_matrix.py` - Decision calculator
- `tools/priority_matrix.py` - Priority calculator
- `tools/analysis_template.md` - Analysis template
- `tools/templates/` - Template folder

## Automation

**Script Available**: `scripts/setup_work_effort_tools.py`

**Usage**:
```bash
# Basic setup (essential tools only)
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description

# With optional tools
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description --include-optional
```

**Manual Setup**:
```bash
# Copy template
cp -r _work_efforts/.tool_bag_template/* _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

## Integration with MCP

**When using MCP to create work effort**:
1. Use `mcp_work-efforts_create_work_effort` to create structure
2. Run tool bag setup script after creation
3. Or manually copy template

**Future Enhancement**: MCP server could automatically set up tools

## Notes

- Tool bag is now **standard** for all work efforts
- Essential tools are always included
- Optional tools added based on work effort needs
- Tools can be copied from other work efforts (e.g., Order 66)

## Related Procedures

- `CMD-001` - Create New Command
- `ENG-001` - Full Engineering Workflow (uses work efforts)

---

**This procedure ensures every work effort has the tools it needs from the start.**
