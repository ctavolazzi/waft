# Procedure: Create New Command

**Shortcode**: CMD-001  
**Category**: Command Creation  
**Created**: 2026-01-10  
**Updated**: 2026-01-10  
**Status**: Active  
**Aliases**: `/new-command`

---

## Description

Standardized procedure for creating new Cursor "/" commands. Ensures consistency, proper documentation, and integration with existing command system.

---

## Use When

- Creating a new "/" command
- Need standardized command structure
- Want to ensure proper integration
- Need command documentation

---

## Prerequisites

- Working directory is project root
- `.cursor/commands/` directory exists
- Understanding of existing command patterns

---

## Steps

### Step 1: Define Command Purpose
**Actions**:
1. Define what the command does
2. Identify use cases
3. Determine when to use it
4. Identify related commands
5. Document purpose clearly

**Output**: Clear command purpose and use cases

---

### Step 2: Review Existing Commands
**Actions**:
1. Review similar commands for patterns
2. Check command structure
3. Identify integration points
4. Note documentation style
5. Review help system integration

**Output**: Understanding of command patterns

---

### Step 3: Create Command File
**Actions**:
1. Create file in `.cursor/commands/`
2. Use command template structure:
   - Title and description
   - Purpose section
   - Philosophy
   - Execution steps
   - Output format
   - Use cases
   - Integration
   - When to use
3. Follow existing command format
4. Include all required sections

**Output**: Command file created

**File Location**: `.cursor/commands/{command-name}.md`

---

### Step 4: Document Integration
**Actions**:
1. Document integration with other commands
2. Note dependencies
3. Document when to use vs. related commands
4. Add to help system (if applicable)
5. Update command recommendations

**Output**: Integration documented

---

### Step 5: Test Command
**Actions**:
1. Review command file
2. Verify structure
3. Check for completeness
4. Test execution (if applicable)
5. Verify documentation

**Output**: Command tested and verified

---

### Step 6: Update Documentation
**Actions**:
1. Add to `.cursor/commands/COMMAND_RECOMMENDATIONS.md` (if applicable)
2. Update `.cursor/commands/help.md` (if applicable)
3. Update `.cursor/commands/GLOBAL_COMMANDS_SETUP.md` (if global)
4. Sync globally (if global command)

**Output**: Documentation updated

---

## Expected Output

After completion:
- ✅ Command file created in `.cursor/commands/`
- ✅ Command properly documented
- ✅ Integration with other commands documented
- ✅ Help system updated (if applicable)
- ✅ Command ready for use

---

## Notes

- Follow existing command patterns for consistency
- Include all required sections in command file
- Document integration points clearly
- Test command before finalizing
- Update help system if command is user-facing

---

## Command Template

```markdown
# [Command Name]

**[Brief description]**

[Longer description of what the command does and when to use it]

**Use when:** [When to use this command]

---

## Purpose

This command provides:
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

## Philosophy

1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

---

## Execution Steps

### Step 1: [Step Name]
**Purpose**: [Why this step]

**Actions**:
1. [Action 1]
2. [Action 2]

**Output**: [What this step produces]

---

## Output Format

[Description of output format]

---

## Use Cases

### 1. [Use Case Name]
**Scenario**: [Description]

**Example**:
```
User: "/command-name"
```

**Output**: [What happens]

---

## Integration with Other Commands

- **`/related-command`**: [How they relate]

---

## When to Use

**Use `/command-name` when**:
- ✅ [Condition 1]
- ✅ [Condition 2]

**Don't use `/command-name` when**:
- ❌ [Condition 1]
- ❌ [Condition 2]

---

**This command [brief summary of what it does].**

--- End Command ---
```

---

## Related Procedures

- **ENG-001**: Full Engineering Workflow (for complex commands)
- **DOC-001**: Documentation Procedure (for command docs)

---

**Procedure Created**: 2026-01-10  
**Last Updated**: 2026-01-10
