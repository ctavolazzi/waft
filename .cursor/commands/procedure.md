# Procedure

**Manage and execute standardized procedures with shortcode identifiers.**

Creates, lists, executes, and manages procedure commands with shortcode identifiers (format: `CAT-###`). Procedures are reusable workflows that can be referenced by their shortcode for quick execution.

**Use when:** You want to create, list, or execute standardized procedures with memorable shortcodes.

---

## Purpose

This command provides:
- **Procedure Creation**: Define new procedures with shortcodes
- **Procedure Listing**: List all available procedures
- **Procedure Execution**: Execute procedures by shortcode or name
- **Procedure Management**: Update, delete, and organize procedures
- **Shortcode System**: Quick reference via `CAT-###` format

---

## Shortcode Format

**Format**: `CAT-###`

**Components**:
- **CAT**: 3-letter category prefix
- **-**: Separator
- **###**: 3-digit sequential number (001-999)

**Categories**:
- **ENG**: Engineering workflows (e.g., `ENG-001`)
- **CMD**: Command creation procedures (e.g., `CMD-002`)
- **PROC**: General procedures (e.g., `PROC-003`)
- **ORC**: Orchestration workflows (e.g., `ORC-004`)
- **ANL**: Analysis procedures (e.g., `ANL-005`)
- **VER**: Verification procedures (e.g., `VER-006`)
- **DOC**: Documentation procedures (e.g., `DOC-007`)
- **TST**: Testing procedures (e.g., `TST-008`)
- **DEP**: Deployment procedures (e.g., `DEP-009`)
- **DBG**: Debugging procedures (e.g., `DBG-010`)

**Examples**:
- `ENG-001`: Full engineering workflow
- `CMD-002`: Create new command procedure
- `ORC-003`: Comprehensive orchestration
- `ANL-004`: Data analysis procedure

---

## Command Categories

### Procedure Management
1. **`/procedure create`** - Create new procedure with shortcode
2. **`/procedure list`** - List all procedures (optionally filter by category)
3. **`/procedure show <shortcode>`** - Show procedure details
4. **`/procedure execute <shortcode>`** - Execute procedure by shortcode
5. **`/procedure update <shortcode>`** - Update existing procedure
6. **`/procedure delete <shortcode>`** - Delete procedure

### Quick Execution
- **`/<shortcode>`** - Execute procedure directly by shortcode (e.g., `/ENG-001`)

---

## Procedure Structure

```markdown
# Procedure: [Name]

**Shortcode**: CAT-###
**Category**: [Category Name]
**Created**: YYYY-MM-DD
**Updated**: YYYY-MM-DD
**Status**: Active | Deprecated | Draft

## Description
[What this procedure does]

## Use When
[When to use this procedure]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

## Steps
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

## Expected Output
[What to expect after execution]

## Notes
[Additional notes or warnings]

## Related Procedures
- [CAT-###] - [Related procedure name]
```

---

## Procedure Registry

**Location**: `.cursor/procedures/registry.json`

**Format**:
```json
{
  "procedures": [
    {
      "shortcode": "ENG-001",
      "name": "Full Engineering Workflow",
      "category": "ENG",
      "description": "Complete engineering workflow from orientation to implementation",
      "file": ".cursor/procedures/ENG-001_full_engineering_workflow.md",
      "created": "2026-01-10",
      "updated": "2026-01-10",
      "status": "active"
    }
  ],
  "categories": {
    "ENG": "Engineering workflows",
    "CMD": "Command creation",
    "PROC": "General procedures",
    "ORC": "Orchestration",
    "ANL": "Analysis",
    "VER": "Verification",
    "DOC": "Documentation",
    "TST": "Testing",
    "DEP": "Deployment",
    "DBG": "Debugging"
  },
  "next_numbers": {
    "ENG": 2,
    "CMD": 1,
    "PROC": 1,
    "ORC": 1,
    "ANL": 1,
    "VER": 1,
    "DOC": 1,
    "TST": 1,
    "DEP": 1,
    "DBG": 1
  }
}
```

---

## Usage Examples

### Create Procedure
```
/procedure create --category ENG --name "Full Engineering Workflow" --description "Complete workflow from orientation to implementation"
```

**Output**: Creates `ENG-001` (or next available number) and procedure file

### List Procedures
```
/procedure list
/procedure list --category ENG
/procedure list --status active
```

### Show Procedure
```
/procedure show ENG-001
```

### Execute Procedure
```
/procedure execute ENG-001
/ENG-001  # Direct shortcode execution
```

### Update Procedure
```
/procedure update ENG-001 --description "Updated description"
```

### Delete Procedure
```
/procedure delete ENG-001
```

---

## Built-in Procedures

### ENG-001: Full Engineering Workflow
**Shortcode**: `ENG-001`  
**Category**: Engineering  
**Description**: Complete engineering workflow (spin-up → explore → draft → critique → finalize → begin)

**Steps**:
1. Execute `/spin-up` - Orientation
2. Execute `/explore` - Deep understanding
3. Execute draft plan phase
4. Execute critique plan phase
5. Execute finalize plan phase
6. Execute begin implementation phase

**Use When**: Starting new feature or significant change requiring full understanding

---

### CMD-001: Create New Command
**Shortcode**: `CMD-001`  
**Category**: Command Creation  
**Description**: Standardized procedure for creating new Cursor commands

**Steps**:
1. Define command purpose and use cases
2. Create command file in `.cursor/commands/`
3. Follow command template structure
4. Document integration with other commands
5. Add to help system
6. Test command execution

**Use When**: Creating a new "/" command

---

### ORC-001: Comprehensive Orchestration
**Shortcode**: `ORC-001`  
**Category**: Orchestration  
**Description**: Complete orchestration workflow (orchestrate command)

**Steps**:
1. Execute `/spin-up`
2. Execute `/consider`
3. Execute `/visualize`
4. Execute `/analyze`
5. Execute `/checkpoint`
6. Execute `/execute` with probes
7. Form hypothesis
8. Execute `/verify`
9. Execute `/reflect`
10. Execute `/recap`
11. Execute `/proceed`
12. Execute `/decide`

**Use When**: Starting new investigation requiring comprehensive workflow

---

### ANL-001: Data Analysis Workflow
**Shortcode**: `ANL-001`  
**Category**: Analysis  
**Description**: Complete data analysis workflow

**Steps**:
1. Execute `/phase1` - Data gathering
2. Execute `/analyze` - Analysis and insights
3. Generate report
4. Create action plan

**Use When**: Need to analyze project data and generate insights

---

### VER-001: Verification Workflow
**Shortcode**: `VER-001`  
**Category**: Verification  
**Description**: Comprehensive verification workflow

**Steps**:
1. Execute `/verify` - Run verification checks
2. Document verification traces
3. Update verification index
4. Report findings

**Use When**: Need to verify claims or validate information

---

## Procedure File Location

**Directory**: `.cursor/procedures/`

**Structure**:
```
.cursor/procedures/
├── registry.json                    # Procedure registry
├── ENG-001_full_engineering_workflow.md
├── CMD-001_create_new_command.md
├── ORC-001_comprehensive_orchestration.md
└── ...
```

**Naming Convention**: `{SHORTCODE}_{procedure_name}.md`

---

## Execution Steps

### Creating a Procedure

1. **Define Procedure**
   - Name and description
   - Category selection
   - Prerequisites
   - Steps definition

2. **Generate Shortcode**
   - Check registry for next available number in category
   - Assign shortcode (e.g., `ENG-002`)

3. **Create Procedure File**
   - Create markdown file in `.cursor/procedures/`
   - Use procedure template
   - Document all steps

4. **Update Registry**
   - Add to `registry.json`
   - Update `next_numbers` for category
   - Set status to "active"

5. **Register Command** (if needed)
   - Create command alias for shortcode
   - Add to help system

---

## Integration with Other Commands

Procedures can:
- **Call other commands**: Procedures execute other "/" commands
- **Reference work efforts**: Link to work efforts via MCP
- **Use MCP servers**: Leverage all available MCP tools
- **Document findings**: Save to `_pyrite/active/`
- **Update devlog**: Log procedure execution

---

## When to Use

**Use `/procedure` when**:
- ✅ Want to standardize a workflow
- ✅ Need reusable procedure with shortcode
- ✅ Want quick reference for common workflows
- ✅ Need to document standard procedures
- ✅ Want to share procedures across projects

**Don't use `/procedure` when**:
- ❌ One-time task (use commands directly)
- ❌ Simple operation (use single command)
- ❌ Ad-hoc workflow (use commands directly)

---

## Best Practices

1. **Clear Names**: Descriptive procedure names
2. **Complete Steps**: Document all steps clearly
3. **Prerequisites**: List all prerequisites
4. **Expected Output**: Document what to expect
5. **Related Procedures**: Link to related procedures
6. **Regular Updates**: Keep procedures current
7. **Status Management**: Mark deprecated procedures

---

## Shortcode Reference

### Quick Reference Table

| Shortcode | Name | Category | Description |
|-----------|------|----------|-------------|
| `ENG-001` | Full Engineering Workflow | Engineering | Complete engineering workflow |
| `CMD-001` | Create New Command | Command | Standardized command creation |
| `ORC-001` | Comprehensive Orchestration | Orchestration | Complete orchestration workflow |
| `ANL-001` | Data Analysis Workflow | Analysis | Data analysis and insights |
| `VER-001` | Verification Workflow | Verification | Comprehensive verification |

---

## Advanced Features

### Procedure Templates
Create procedure templates for common patterns:
- Engineering workflow template
- Command creation template
- Analysis template
- Verification template

### Procedure Chaining
Procedures can call other procedures:
- `ENG-001` might call `ANL-001` for analysis
- `ORC-001` might call multiple procedures

### Procedure Variants
Create variants of procedures:
- `ENG-001a`: Quick engineering workflow
- `ENG-001b`: Deep engineering workflow

---

## Example Workflow

```
User: "/procedure create --category ENG --name 'Quick Engineering'"

AI: [Creates ENG-002 procedure]
    ✓ Shortcode: ENG-002
    ✓ File: .cursor/procedures/ENG-002_quick_engineering.md
    ✓ Registry updated

User: "/ENG-002"

AI: [Executes procedure steps]
    ✓ Step 1: Orientation
    ✓ Step 2: Quick analysis
    ✓ Step 3: Action plan
    ✓ Complete
```

---

**This command system provides standardized procedures with memorable shortcodes - perfect for reusable workflows and quick execution.**

--- End Command ---
