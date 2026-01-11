# Procedures

**Quick reference for all available procedures with shortcodes.**

Lists all standardized procedures with their shortcodes, descriptions, and quick execution methods. Use this for quick reference when you need to execute a procedure.

**Use when:** Want to see available procedures, find a procedure by shortcode, or get quick reference for procedure execution.

---

## Purpose

This command provides:
- **Procedure Listing**: All available procedures with shortcodes
- **Quick Reference**: Shortcode format and categories
- **Execution Methods**: How to execute procedures
- **Category Organization**: Procedures grouped by category

---

## Quick Execution

**Direct Shortcode Execution:**
```
/ENG-001    # Execute Full Engineering Workflow
/CMD-001    # Execute Create New Command
/ORC-001    # Execute Comprehensive Orchestration
/ANL-001    # Execute Data Analysis Workflow
/VER-001    # Execute Verification Workflow
```

**Via Procedure Command:**
```
/procedure execute ENG-001
/procedure list
/procedure show ENG-001
```

---

## Available Procedures

### Engineering (ENG)

**ENG-001: Full Engineering Workflow**
- **Shortcode**: `ENG-001`
- **Aliases**: `/engineering`, `/eng`
- **Description**: Complete engineering workflow from orientation to implementation
- **Steps**: spin-up → explore → draft → critique → finalize → begin
- **Use When**: Starting new feature requiring full understanding
- **Execute**: `/ENG-001` or `/engineering`

---

### Command Creation (CMD)

**CMD-001: Create New Command**
- **Shortcode**: `CMD-001`
- **Aliases**: `/new-command`
- **Description**: Standardized procedure for creating new Cursor commands
- **Steps**: Define purpose → Review patterns → Create file → Document integration → Test → Update docs
- **Use When**: Creating a new "/" command
- **Execute**: `/CMD-001` or `/new-command`

---

### Orchestration (ORC)

**ORC-001: Comprehensive Orchestration**
- **Shortcode**: `ORC-001`
- **Aliases**: `/orchestrate`
- **Description**: Complete orchestration workflow (orchestrate command)
- **Steps**: spin-up → consider → visualize → analyze → checkpoint → execute → hypothesis → verify → reflect → recap → proceed → decide
- **Use When**: Starting new investigation requiring comprehensive workflow
- **Execute**: `/ORC-001` or `/orchestrate`

---

### Analysis (ANL)

**ANL-001: Data Analysis Workflow**
- **Shortcode**: `ANL-001`
- **Aliases**: `/analyze-workflow`
- **Description**: Complete data analysis workflow
- **Steps**: phase1 → analyze → review
- **Use When**: Need to analyze project data and generate insights
- **Execute**: `/ANL-001` or `/analyze-workflow`

---

### Verification (VER)

**VER-001: Verification Workflow**
- **Shortcode**: `VER-001`
- **Aliases**: `/verify-workflow`
- **Description**: Comprehensive verification workflow
- **Steps**: Identify claims → Run verification → Document traces → Review results
- **Use When**: Need to verify claims or validate information
- **Execute**: `/VER-001` or `/verify-workflow`

---

## Shortcode Format

**Format**: `CAT-###`

- **CAT**: 3-letter category (ENG, CMD, ORC, ANL, VER, DOC, TST, DEP, DBG)
- **-**: Separator
- **###**: 3-digit number (001-999)

**Categories**:
- **ENG**: Engineering workflows
- **CMD**: Command creation procedures
- **PROC**: General procedures
- **ORC**: Orchestration workflows
- **ANL**: Analysis procedures
- **VER**: Verification procedures
- **DOC**: Documentation procedures
- **TST**: Testing procedures
- **DEP**: Deployment procedures
- **DBG**: Debugging procedures

---

## Procedure Management

### List Procedures
```
/procedure list
/procedure list --category ENG
/procedure list --status active
```

### Show Procedure Details
```
/procedure show ENG-001
/procedure show CMD-001
```

### Execute Procedure
```
/procedure execute ENG-001
/ENG-001  # Direct shortcode
```

### Create New Procedure
```
/procedure create --category ENG --name "Quick Engineering" --description "Fast engineering workflow"
```

---

## Quick Reference Table

| Shortcode | Name | Category | Quick Execute |
|-----------|------|----------|---------------|
| `ENG-001` | Full Engineering Workflow | Engineering | `/ENG-001` |
| `CMD-001` | Create New Command | Command | `/CMD-001` |
| `ORC-001` | Comprehensive Orchestration | Orchestration | `/ORC-001` |
| `ANL-001` | Data Analysis Workflow | Analysis | `/ANL-001` |
| `VER-001` | Verification Workflow | Verification | `/VER-001` |

---

## Usage Examples

### Quick Execution
```
/ENG-001    # Run full engineering workflow
/CMD-001    # Create a new command
/ORC-001    # Run comprehensive orchestration
```

### Procedure Management
```
/procedure list                    # See all procedures
/procedure show ENG-001           # View procedure details
/procedure execute ANL-001        # Execute via command
/procedure create --category DOC   # Create new procedure
```

---

## Integration

Procedures integrate with:
- All "/" commands
- Work efforts MCP
- Documentation system
- Devlog updates
- _pyrite memory layer

---

## When to Use

**Use procedures when**:
- ✅ Need standardized workflow
- ✅ Want reusable procedure
- ✅ Need quick reference
- ✅ Want documented workflow
- ✅ Need consistent execution

**Don't use procedures when**:
- ❌ One-time task (use commands directly)
- ❌ Simple operation (use single command)
- ❌ Ad-hoc workflow (use commands directly)

---

**This command provides quick reference for all available procedures - perfect for discovering and executing standardized workflows.**

--- End Command ---
