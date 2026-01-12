# Work Effort Creation Guide

**Updated**: 2026-01-10  
**Status**: ✅ Standard - All work efforts include tool bag

---

## Quick Start

**Creating a new work effort with tools**:

```bash
# Option 1: Use setup script (recommended)
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description

# Option 2: Copy template manually
cp -r _work_efforts/.tool_bag_template/* _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

---

## Standard Workflow

### Step 1: Create Work Effort Structure
1. Generate work effort ID: `WE-YYMMDD-xxxx_description`
2. Create folder: `_work_efforts/WE-YYMMDD-xxxx_description/`
3. Create index: `WE-YYMMDD-xxxx_index.md` with frontmatter

### Step 2: Setup Tool Bag (REQUIRED)
**This is now standard - always do this!**

```bash
python scripts/setup_work_effort_tools.py _work_efforts/WE-YYMMDD-xxxx_description
```

**Or manually**:
```bash
mkdir -p _work_efforts/WE-YYMMDD-xxxx_description/tools
cp -r _work_efforts/.tool_bag_template/* _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

### Step 3: Add Optional Tools (If Needed)
**If decision-making needed**:
```bash
cp _work_efforts/WE-260110-order66_order_66_execution/tools/decision_matrix.py _work_efforts/WE-YYMMDD-xxxx_description/tools/
cp _work_efforts/WE-260110-order66_order_66_execution/tools/priority_matrix.py _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

**If analysis needed**:
```bash
cp _work_efforts/WE-260110-order66_order_66_execution/tools/analysis_template.md _work_efforts/WE-YYMMDD-xxxx_description/tools/
```

### Step 4: Update Index
Add to work effort index:
```markdown
## Tools Available

**Tool Bag Location**: `tools/`

See `tools/README.md` for complete tool bag documentation.

**Essential Tools**:
- ✅ `work_effort_tracker.md` - Progress tracking
- ✅ `verification_checklist.md` - Verification checklist
- ✅ `README.md` - Tool bag documentation
```

---

## What Gets Created

### Essential Tools (Always)
```
tools/
├── README.md                    # Tool bag documentation
├── work_effort_tracker.md      # Progress tracking template
└── verification_checklist.md   # Verification checklist
```

### Optional Tools (Add As Needed)
```
tools/
├── decision_matrix.py          # Decision calculator
├── priority_matrix.py          # Priority calculator
├── analysis_template.md        # Analysis template
└── templates/                  # Template folder
    ├── decision_matrix_template.md
    └── priority_matrix_template.md
```

---

## Using the Tools

### Work Effort Tracker
1. Copy `work_effort_tracker.md` to track your work effort
2. Update status, progress, milestones regularly
3. Document decisions and blockers

### Verification Checklist
1. Use before completing work effort
2. Check all items
3. Document any issues

### Decision/Priority Tools
1. Run interactive mode: `python tools/decision_matrix.py --interactive`
2. Or use CLI mode with parameters
3. Generate reports for documentation

---

## Automation

### Setup Script
**Location**: `scripts/setup_work_effort_tools.py`

**Features**:
- Creates `tools/` folder
- Copies essential tools
- Updates README with work effort info
- Optional tools flag

**Usage**:
```bash
# Basic
python scripts/setup_work_effort_tools.py <work_effort_path>

# With optional tools
python scripts/setup_work_effort_tools.py <work_effort_path> --include-optional
```

### Template Location
**Location**: `_work_efforts/.tool_bag_template/`

**Contents**: Essential tool templates ready to copy

---

## Commands & Procedures

### Command
**`/create-work-effort`** - Creates work effort with automatic tool bag setup

### Procedure
**`CMD-002`** or `/CMD-002` - Detailed procedure for work effort creation

**Shortcode**: `/create-work-effort` or `/CMD-002`

---

## Best Practices

1. **Always create tools folder** - Don't skip, it's now standard
2. **Start with essentials** - Add optional tools as needed
3. **Document additions** - Update README when adding tools
4. **Reuse tools** - Copy from other work efforts
5. **Keep it simple** - Tools should be easy to use

---

## Examples

### Example 1: Basic Work Effort
```bash
# Create work effort folder
mkdir _work_efforts/WE-260110-test_test_work_effort

# Setup tool bag
python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-test_test_work_effort
```

**Result**: Work effort with essential tools ready

### Example 2: Work Effort with Decision Tools
```bash
# Create work effort
mkdir _work_efforts/WE-260110-decision_decision_analysis

# Setup tool bag
python scripts/setup_work_effort_tools.py _work_efforts/WE-260110-decision_decision_analysis

# Add decision tools
cp _work_efforts/WE-260110-order66_order_66_execution/tools/decision_matrix.py _work_efforts/WE-260110-decision_decision_analysis/tools/
cp _work_efforts/WE-260110-order66_order_66_execution/tools/priority_matrix.py _work_efforts/WE-260110-decision_decision_analysis/tools/
```

**Result**: Work effort with essential + decision tools

---

## Migration

### For Existing Work Efforts
If a work effort doesn't have tools yet:

```bash
python scripts/setup_work_effort_tools.py _work_efforts/WE-XXXX-xxxx_description
```

This will add the tools folder without affecting existing files.

---

## Related Documentation

- **Standard**: `_work_efforts/WORK_EFFORT_TOOL_BAG_STANDARD.md`
- **Procedure**: `.cursor/procedures/CMD-002_create_work_effort_with_tools.md`
- **Command**: `.cursor/commands/create-work-effort.md`
- **Template**: `_work_efforts/.tool_bag_template/`
- **Example**: `_work_efforts/WE-260110-order66_order_66_execution/tools/`

---

**Standard Established**: 2026-01-10  
**Status**: ✅ Active - All new work efforts include tool bag
