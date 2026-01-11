# Work Effort Tool Bag - Standard Workflow

**Purpose**: Standard workflow for creating work effort tool bags

---

## Overview

Every work effort should have a `tools/` folder containing utilities, templates, scripts, and checklists needed to complete that work effort. This ensures all necessary tools are in one place and makes work efforts self-contained.

---

## Standard Workflow

### Step 1: Create Work Effort Folder

**Naming Convention**: `WE-YYMMDD-xxxx_description/`

**Example**: `WE-260110-order66_order_66_execution/`

**Structure**:
```
WE-YYMMDD-xxxx_description/
├── WE-YYMMDD-xxxx_index.md    # Main work effort index
├── tickets/                    # Tickets folder (if needed)
└── tools/                      # Tool bag folder
    ├── README.md               # Tool bag documentation
    ├── [tools...]              # Various tools
    └── templates/              # Template folder (if needed)
```

---

### Step 2: Create Tools Folder

**Always create**: `tools/` folder inside work effort

**Always include**: `tools/README.md` documenting all tools

---

### Step 3: Populate Tool Bag

**Essential Tools** (Always Include):
1. **`work_effort_tracker.md`** - Progress tracking template
2. **`verification_checklist.md`** - Verification checklist
3. **`tools/README.md`** - Tool bag documentation

**Decision-Making Tools** (When Needed):
- `decision_matrix.py` - Decision matrix calculator
- `priority_matrix.py` - Priority matrix calculator
- `templates/decision_matrix_template.md` - Decision matrix template
- `templates/priority_matrix_template.md` - Priority matrix template

**Analysis Tools** (When Needed):
- `analysis_template.md` - Analysis document template
- `calculate_scores.py` - Score calculation utility
- `generate_report.py` - Report generation utility

**Custom Tools** (Project-Specific):
- Project-specific scripts
- Custom templates
- Specialized utilities

---

## Tool Selection Guidelines

### Always Include
- ✅ Work effort tracker
- ✅ Verification checklist
- ✅ README (tool bag documentation)

### Include If Decision-Making Needed
- ✅ Decision matrix calculator
- ✅ Priority matrix calculator
- ✅ Decision matrix template
- ✅ Priority matrix template

### Include If Analysis Needed
- ✅ Analysis template
- ✅ Report generation utilities

### Include If Calculations Needed
- ✅ Python calculation scripts
- ✅ Score calculation utilities

### Include If Custom Workflows Needed
- ✅ Custom scripts
- ✅ Workflow automation
- ✅ Specialized utilities

---

## Tool Bag Structure

```
tools/
├── README.md                           # Tool bag documentation
├── work_effort_tracker.md              # Progress tracking
├── verification_checklist.md            # Verification checklist
├── analysis_template.md                # Analysis template (if needed)
├── decision_matrix.py                  # Decision calculator (if needed)
├── priority_matrix.py                  # Priority calculator (if needed)
└── templates/                          # Templates folder (if needed)
    ├── decision_matrix_template.md
    ├── priority_matrix_template.md
    └── [other templates...]
```

---

## Tool Bag README Template

Every `tools/README.md` should include:

1. **Overview** - What the tool bag contains
2. **Tools Available** - List of all tools with descriptions
3. **Usage** - How to use each tool
4. **Standard Workflow** - How to use tools together
5. **Tool Categories** - Organization of tools
6. **Maintenance** - How to keep tools updated

---

## Example: Order 66 Tool Bag

**Created**: `WE-260110-order66_order_66_execution/tools/`

**Tools Included**:
- ✅ `decision_matrix.py` - Decision matrix calculator
- ✅ `priority_matrix.py` - Priority matrix calculator
- ✅ `work_effort_tracker.md` - Progress tracking
- ✅ `analysis_template.md` - Analysis template
- ✅ `verification_checklist.md` - Verification checklist
- ✅ `templates/decision_matrix_template.md` - Decision template
- ✅ `templates/priority_matrix_template.md` - Priority template
- ✅ `README.md` - Tool bag documentation

**Why These Tools**:
- Order 66 involves decision-making → Decision matrix tools
- Order 66 involves prioritization → Priority matrix tools
- Order 66 involves analysis → Analysis template
- Order 66 needs tracking → Work effort tracker
- Order 66 needs verification → Verification checklist

---

## Benefits

### Self-Contained
- All tools in one place
- No need to search for utilities
- Clear what's available

### Reusable
- Tools can be copied to other work efforts
- Templates can be reused
- Patterns emerge over time

### Documented
- README explains all tools
- Usage examples provided
- Clear organization

### Maintainable
- Tools stay with work effort
- Easy to update
- Version controlled

---

## Best Practices

1. **Create tools folder immediately** - Don't wait, create it when work effort is created
2. **Start with essentials** - Always include tracker and checklist
3. **Add tools as needed** - Don't over-engineer, add tools when you need them
4. **Document everything** - README should explain all tools
5. **Keep tools simple** - Tools should be easy to use and understand
6. **Update as you go** - Refine tools based on usage
7. **Share patterns** - If a tool works well, use it in other work efforts

---

## Standard Tool Templates

### Work Effort Tracker
- Status tracking
- Progress monitoring
- Dependency management
- Milestone tracking

### Verification Checklist
- Project state verification
- Quality checks
- Completion criteria
- Issue tracking

### Analysis Template
- Situation analysis
- Options evaluation
- Decision matrix
- Recommendations

### Decision Matrix Calculator
- Weighted sum model
- Multiple criteria
- Score calculation
- Ranking generation

### Priority Matrix Calculator
- Impact/Urgency analysis
- Priority scoring
- Work effort prioritization
- Execution order

---

## Future Enhancements

**Potential Additions**:
- Automated tool generation
- Tool library/shared tools
- Tool versioning
- Tool testing
- Tool validation

---

**Standard Workflow Established**: 2026-01-10  
**Last Updated**: 2026-01-10
