# Project Startup Process for AI Coding Assistants

**Version**: 1.0
**Purpose**: Comprehensive, reusable guide for AI assistants to orient themselves on a codebase
**Use Cases**: New projects, returning to existing projects, onboarding fresh AI assistants

---

## Philosophy

This process compounds knowledge and capability progressively. Each step builds on the previous, ensuring the AI assistant:
1. **Understands** what exists
2. **Validates** assumptions objectively
3. **Integrates** new capabilities thoughtfully
4. **Documents** everything clearly
5. **Maintains** quality standards

**Key Principle**: Test assumptions objectively, not just confirm what we want to see.

---

## Phase 1: Initial Orientation & Sanity Checks

### Step 1.1: Understand the Request

**AI Action**: Before doing anything, clearly understand:
- What is the user asking for?
- Is this a new feature, bug fix, integration, or exploration?
- What's the scope and priority?
- Are there any constraints or requirements?

**Output**: Echo back your understanding and wait for confirmation.

**Example**:
```
User: "Can we do an experiment right now with what we have to verify if we're understanding everything correctly?"

AI Understanding: "You want to run a sanity check experiment to verify our assumptions about how the codebase works. This is about testing our understanding, not implementing new features."

[Wait for confirmation before proceeding]
```

---

### Step 1.2: Search for Related Work

**AI Action**:
1. Check for `_work_efforts/` directory or similar project management structure
2. Search for existing work efforts, tickets, or documentation related to the request
3. Look for recent devlogs or session notes

**Commands**:
```bash
# Check for work efforts
ls -la _work_efforts/ 2>/dev/null || echo "No _work_efforts directory"

# Search for related documentation
find . -name "*.md" -type f | xargs grep -l "keyword" 2>/dev/null

# Check recent activity
ls -lt _work_efforts/*.md 2>/dev/null | head -5
```

**Decision Point**:
- **If related work found**: Ask user if they want to update it or create new
- **If no related work**: Ask if they want to create a work effort or proceed without one

---

### Step 1.3: Run Sanity Check Experiments

**AI Action**: Test critical assumptions objectively before proceeding.

**Why**: We often assume things work correctly, but objective testing reveals gaps.

**Process**:

1. **Identify Assumptions**
   - What does the code assume will work?
   - What dependencies does it rely on?
   - What formats does it expect?

2. **Design Objective Tests**
   - Test failure cases, not just success cases
   - Test edge cases and boundary conditions
   - Test with invalid/malformed input
   - Test when dependencies are missing

3. **Run Tests**
   ```python
   # Example: Testing TOML parsing assumption
   import tempfile
   from pathlib import Path

   test_cases = [
       ("Simple", 'name = "simple"', "simple"),
       ("Escaped quotes", 'name = "with\\"escaped\\"quotes"', 'with"escaped"quotes'),
       ("No quotes", "name = no_quotes", "no_quotes"),
       # ... more edge cases
   ]

   for name, toml_content, expected in test_cases:
       # Test the assumption
       result = parse_toml_field(toml_content, "name")
       passed = result == expected
       print(f"{'✅' if passed else '❌'} {name}: got '{result}', expected '{expected}'")
   ```

4. **Document Findings**
   - What passed? What failed?
   - What does this reveal about our assumptions?
   - What needs to be fixed or documented?

**Output**: Create a document like `_work_efforts/SANITY_CHECK_RESULTS.md` with:
- Assumptions tested
- Test cases and results
- Failures found
- Recommendations

---

### Step 1.4: Assess Current State

**AI Action**: Understand what exists in the codebase.

**Checklist**:

1. **Project Structure**
   ```bash
   # Understand directory structure
   tree -L 3 -I '__pycache__|*.pyc|.git' .

   # Check for key directories
   ls -la src/ _work_efforts/ _pyrite/ 2>/dev/null
   ```

2. **Dependencies**
   ```bash
   # Check dependencies
   cat pyproject.toml | grep -A 20 "dependencies"
   cat requirements.txt 2>/dev/null || echo "No requirements.txt"
   ```

3. **Configuration Files**
   ```bash
   # Check for config files
   ls -la *.toml *.yaml *.yml *.json .*rc 2>/dev/null
   ```

4. **Documentation**
   ```bash
   # Find documentation
   find . -name "README*.md" -o -name "*.md" | grep -E "(README|docs|_work_efforts)" | head -10
   ```

5. **Recent Changes**
   ```bash
   # Check git history
   git log --oneline -10 2>/dev/null || echo "Not a git repo"
   ```

**Output**: Create `_work_efforts/CURRENT_STATE_ASSESSMENT.md` with:
- Project structure overview
- Key dependencies and their purposes
- Configuration files and their roles
- Documentation status
- Recent activity

---

## Phase 2: Integration & Enhancement

### Step 2.1: Understand Integration Requirements

**AI Action**: When user requests integration of a new tool/library:

1. **Research the Tool**
   - Read official documentation
   - Understand key features and capabilities
   - Identify integration points
   - Check compatibility requirements

2. **Assess Integration Complexity**
   - What needs to be modified?
   - What new dependencies are needed?
   - Are there breaking changes?
   - What's the migration path?

3. **Plan Integration**
   - Create integration manager/class
   - Identify integration points in existing code
   - Plan for graceful degradation (what if tool unavailable?)
   - Design error handling

**Example Process**:
```
User: "I want you to incorporate 'Empirica' into this project"

AI Actions:
1. Search for Empirica documentation
2. Understand Empirica's features (CASCADE workflow, epistemic tracking, etc.)
3. Identify where it fits in the architecture
4. Create EmpiricaManager class
5. Integrate into existing commands
6. Add to dependencies
7. Update documentation
```

---

### Step 2.2: Create Integration Manager

**AI Action**: Create a dedicated manager class for the integration.

**Pattern**:
```python
"""
[Tool] Manager - Handles [Tool] integration.

[Tool] provides:
- Feature 1
- Feature 2
- Feature 3
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

class ToolManager:
    """Manages [Tool] integration."""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    def is_initialized(self) -> bool:
        """Check if [Tool] is initialized."""
        # Check for tool-specific markers
        pass

    def initialize(self) -> bool:
        """Initialize [Tool] in the project."""
        # Run tool initialization command
        pass

    # Add methods for key features
    def feature_1(self) -> bool:
        """Use feature 1."""
        pass
```

**Best Practices**:
- Handle missing dependencies gracefully
- Provide clear error messages
- Support dry-run/preview modes
- Log operations for debugging

---

### Step 2.3: Integrate into Existing Workflow

**AI Action**: Integrate the new tool into existing commands/workflows.

**Process**:

1. **Identify Integration Points**
   - Where does this tool fit in the workflow?
   - What commands should use it?
   - When should it be initialized?

2. **Modify Existing Code**
   ```python
   # Example: Adding to project creation
   @app.command()
   def new(name: str, ...):
       # ... existing code ...

       # New integration
       tool = ToolManager(project_path)
       if tool.initialize():
           console.print("[green]✅[/green] Tool initialized")
       else:
           console.print("[yellow]⚠️[/yellow]  Tool not initialized (may not be available)")
   ```

3. **Update Status Commands**
   - Add tool status to `info` commands
   - Show initialization state
   - Display configuration

4. **Update Dependencies**
   ```toml
   # pyproject.toml
   dependencies = [
       # ... existing ...
       "new-tool>=1.0.0",  # ← Added
   ]
   ```

---

### Step 2.4: Enhance Based on Full Feature Set

**AI Action**: After initial integration, review full documentation and add missing features.

**Process**:

1. **Review Complete Documentation**
   - Read full README/docs
   - Identify all available features
   - Prioritize which features to support

2. **Add Enhanced Methods**
   ```python
   # Add methods for additional features
   def advanced_feature_1(self) -> Optional[Dict]:
       """Use advanced feature 1."""
       pass

   def advanced_feature_2(self) -> bool:
       """Use advanced feature 2."""
       pass
   ```

3. **Document Capabilities**
   - Create integration guide
   - Document all available methods
   - Provide usage examples

---

## Phase 3: Documentation & Quality

### Step 3.1: Create Comprehensive Documentation

**AI Action**: Document everything you've done.

**Documents to Create**:

1. **Integration Guide** (`INTEGRATION_[TOOL].md`)
   - What the tool is
   - Why it's integrated
   - How to use it
   - API reference
   - Examples

2. **Enhanced Features Guide** (`ENHANCED_INTEGRATION.md`)
   - Advanced features
   - Usage patterns
   - Best practices
   - Future enhancements

3. **Checkpoint Document** (`CHECKPOINT_[DATE]_[TOPIC].md`)
   - What was accomplished
   - Current state
   - Key learnings
   - Next steps
   - Metrics

**Template Structure**:
```markdown
# [Title]

**Created**: YYYY-MM-DD
**Purpose**: [Clear purpose statement]

---

## Overview
[What this is about]

## What We Did
[Step-by-step what was done]

## Results
[What was achieved]

## Key Learnings
[What we learned]

## Next Steps
[What comes next]

## Status
[Current status]
```

---

### Step 3.2: Update Project Documentation

**AI Action**: Update main project documentation.

**Files to Update**:

1. **README.md**
   - Add new features to feature list
   - Update architecture diagrams
   - Add usage examples
   - Update dependencies

2. **CHANGELOG.md**
   - Document new features
   - Note breaking changes
   - List improvements

3. **Devlog** (`_work_efforts/devlog.md`)
   - Add session entry
   - Document what was done
   - Note key decisions

---

### Step 3.3: Run Quality Checks

**AI Action**: Run linters, validators, and quality tools.

**Checks to Run**:

1. **Code Linting**
   ```bash
   # Python
   ruff check .
   ruff format --check .

   # Or use project's lint command
   just lint
   ```

2. **Markdown/Obsidian Linting** (if applicable)
   ```bash
   # If pyrite linter available
   python3 /path/to/pyrite/tools/obsidian-linter/lint.py --scope _work_efforts
   ```

3. **Type Checking** (if applicable)
   ```bash
   mypy src/
   ```

4. **Tests** (if applicable)
   ```bash
   pytest tests/
   ```

**Process**:
- Run all checks
- Document issues found
- Fix auto-fixable issues
- Create tickets for manual fixes

---

## Phase 4: Checkpoint & Continuity

### Step 4.1: Create Checkpoint

**AI Action**: Create a comprehensive checkpoint document.

**When**: After completing a significant piece of work.

**Checkpoint Contents**:

1. **What We Accomplished**
   - List all completed tasks
   - Show before/after state
   - Highlight key achievements

2. **Current State**
   - Architecture overview
   - File structure
   - Dependencies
   - Integration status

3. **Key Learnings**
   - What we discovered
   - Assumptions validated/invalidated
   - Best practices identified

4. **Next Steps**
   - Immediate actions
   - Short-term goals
   - Long-term vision

5. **Metrics**
   - Files created/modified
   - Lines of code
   - Dependencies added
   - Documentation created

**Template**:
```markdown
# Checkpoint: [Topic]

**Date**: YYYY-MM-DD
**Session Focus**: [What this session was about]

---

## 🎯 What We Accomplished

### 1. [Task 1] ✅
[Details]

### 2. [Task 2] ✅
[Details]

## 📊 Current State

[Current architecture/state]

## 🔍 Key Learnings

1. [Learning 1]
2. [Learning 2]

## ⏳ Next Steps

1. [Next step 1]
2. [Next step 2]

## 📈 Metrics

- Files Created: X
- Files Modified: Y
- Lines Added: Z

## 🚀 Status

✅ [Status summary]
```

---

### Step 4.2: Generate Session Recap

**AI Action**: Create a step-by-step recap of the entire session.

**Purpose**:
- Document the complete process
- Create reusable template
- Enable continuity for future sessions

**Process**:

1. **Trace the Conversation**
   - List all user requests in order
   - Document what was done for each
   - Show the progression of understanding

2. **Document Decisions**
   - Why certain approaches were chosen
   - What alternatives were considered
   - Trade-offs made

3. **Create Reusable Template**
   - Extract the process
   - Make it generic
   - Add instructions for reuse

**Output**: `_work_efforts/SESSION_RECAP_[DATE].md` or `PROJECT_STARTUP_PROCESS.md`

---

## Phase 5: Maintenance & Iteration

### Step 5.1: Identify Repetition

**AI Action**: Look for repeated patterns or duplicate work.

**Questions to Ask**:
- "How many times have we been over these same ideas now?"
- "What's unique and original and valuable and worth keeping?"
- "What needs to be updated, thrown out, or changed?"

**Process**:
1. Search for duplicate documentation
2. Identify repeated planning cycles
3. Consolidate similar documents
4. Archive outdated information

**Output**: `_work_efforts/META_ANALYSIS.md` with:
- Duplicate content identified
- Unique content highlighted
- Recommendations for consolidation

---

### Step 5.2: Document Assumptions

**AI Action**: Explicitly document all assumptions made by the codebase.

**Process**:

1. **Identify Assumptions**
   ```python
   # Scan code for common assumption patterns
   assumptions = []

   # Check for subprocess calls (assumes command exists)
   if "subprocess.run" in content:
       assumptions.append("Assumes external commands exist")

   # Check for file operations (assumes filesystem works)
   if ".mkdir(" in content or ".write_text(" in content:
       assumptions.append("Assumes filesystem is writable")
   ```

2. **Categorize by Risk**
   - High risk: External dependencies, file system operations
   - Medium risk: Format parsing, configuration
   - Low risk: Internal logic, data structures

3. **Document Testing Status**
   - Which assumptions are tested?
   - Which need tests?
   - What's the test strategy?

**Output**: `_work_efforts/ASSUMPTIONS_AND_TESTS.md`

---

### Step 5.3: Create Testing Strategy

**AI Action**: Design objective tests for assumptions.

**Principles**:

1. **Test Failure Cases**
   - What happens when things go wrong?
   - How does the code handle errors?
   - Are error messages helpful?

2. **Test Edge Cases**
   - Boundary conditions
   - Invalid input
   - Missing dependencies

3. **Test Invariants**
   - What should always be true?
   - What should never happen?
   - What are the constraints?

4. **Use Property-Based Testing**
   - Test properties, not specific values
   - Generate test cases automatically
   - Find edge cases automatically

**Output**: `_work_efforts/OBJECTIVE_TESTING_STRATEGY.md`

---

## Reusable Questions Template

Use these questions in logical order to compound knowledge:

### Orientation Questions
1. "What is this project about?"
2. "What problem does it solve?"
3. "What are the key components?"
4. "What dependencies does it have?"

### Understanding Questions
5. "Where is data stored, and how?"
6. "What's the database system?" (or "Is there one?")
7. "How does the data look? What's its shape?"
8. "How can we traverse it?"

### Capability Questions
9. "Do we need any scaffolding?"
10. "How about helper functions or utilities - do we need any of that?"
11. "What's something that, if we did it, would make everything else either easier or irrelevant?"

### Quality Questions
12. "Do we have tests to verify that our assumptions are correct?"
13. "Are we even aware of what our assumptions are?"
14. "How can we test these assumptions objectively without bias?"

### Meta Questions
15. "How many times have we been over these same ideas now?"
16. "What's unique and original and valuable and worth keeping?"
17. "What needs to be updated, thrown out, or changed?"

### Integration Questions
18. "Can we integrate [tool] into this project?"
19. "How does [tool] fit into our architecture?"
20. "What features of [tool] should we use?"

### Continuity Questions
21. "Where are we even trying to go right now?"
22. "What's our next most important priority?"
23. "What are our next immediate steps? Do we even know?"
24. "If we don't know... why don't we know?"

### Development Workflow Questions
25. "Am I using this project's own tools to develop it?" (dogfooding)
26. "Am I updating work tickets incrementally as I work, or waiting until the end?"
27. "Am I making frequent commits, or saving everything for one big commit?"
28. "Am I using the project's validation/verification tools during development?"
29. "Am I documenting work in the project's memory system as I go?"
30. "Am I using epistemic tracking (Empirica, finding/unknown logging) if available?"
31. "Am I using MCPs for work effort management during development?"

---

## Workflow Integration

### When Starting a New Session

1. **Read Recent Checkpoints**
   ```bash
   ls -lt _work_efforts/CHECKPOINT_*.md | head -3
   ```

2. **Check Current State**
   ```bash
   # Run project info command if available
   waft info  # or equivalent
   ```

3. **Review Recent Changes**
   ```bash
   git log --oneline -10
   ```

4. **Check for Pending Work**
   ```bash
   # Look for TODO, FIXME, or tickets
   grep -r "TODO\|FIXME" . --include="*.md" --include="*.py" | head -10
   ```

### When User Makes a Request

1. **Echo Understanding** → Wait for confirmation
2. **Search Related Work** → Ask if should update or create new
3. **Run Sanity Checks** → Test assumptions objectively
4. **Plan Approach** → Create development plan
5. **Execute** → Do the work
6. **Document** → Update docs and devlog
7. **Checkpoint** → Create checkpoint if significant

### When Completing Work

1. **Update Devlog** → Document what was done
2. **Create Checkpoint** → If significant work
3. **Run Quality Checks** → Lint, test, validate
4. **Update Documentation** → README, CHANGELOG, etc.
5. **Generate Recap** → For future reference

---

## Using Project Tools During Development

**Critical Principle**: Use the tools you're building/maintaining. If you're working on a project that has its own development tools, use them during development, not just at the end.

### Questions to Ask Yourself

1. **"Am I using the project's own tools to develop it?"**
   - If the project has CLI commands, use them during development
   - If the project has epistemic tracking, use it to track your work
   - If the project has memory/documentation systems, use them as you work
   - This is "dogfooding" - using your own product

2. **"Am I updating work tickets incrementally?"**
   - Update ticket status via MCP as you start work (`in_progress`)
   - Update tickets as you complete tasks, not all at the end
   - Add commit hashes to tickets when you commit
   - Document findings and notes in tickets as you discover them

3. **"Am I making frequent commits?"**
   - Commit after each logical unit of work (not all at the end)
   - Use meaningful commit messages with ticket references
   - Commit after completing each ticket or significant milestone
   - Small, focused commits are better than one large commit

4. **"Am I using the project's validation/verification tools?"**
   - Run `waft verify` after making structural changes
   - Run `waft info` to check project status
   - Use project-specific quality checks as you work

5. **"Am I documenting in the project's memory system?"**
   - Document work in `_pyrite/active/` as you go, not just at the end
   - Use the project's documentation structure
   - Update devlogs incrementally

6. **"Am I using epistemic tracking if available?"**
   - Create Empirica sessions for work sessions
   - Submit preflight assessments before starting
   - Log findings and unknowns during work
   - Submit postflight assessments after completing
   - Use `waft finding log` and `waft unknown log` commands

### Workflow: Using Waft to Develop Waft

**Example**: When working on waft framework itself:

1. **Before Starting Work**:
   ```bash
   # Check project status
   waft info
   waft verify

   # Check for active work efforts
   # (Use MCP: list_work_efforts with status="active")

   # If Empirica initialized:
   waft session create --ai-id waft --type development
   waft finding log "Starting work on [ticket]" --impact 0.7
   ```

2. **When Starting a Ticket**:
   ```bash
   # Update ticket status via MCP
   # mcp_work-efforts_update_ticket with status="in_progress"

   # Document in _pyrite/active/
   # Create file: _pyrite/active/YYYY-MM-DD_ticket_description.md
   ```

3. **During Development**:
   ```bash
   # After making changes, verify structure
   waft verify

   # Log discoveries as you find them
   waft finding log "Discovered X" --impact 0.6

   # Log unknowns if you encounter them
   waft unknown log "Need to investigate Y"

   # Check stats periodically
   waft stats
   ```

4. **After Completing a Task**:
   ```bash
   # Verify everything still works
   waft verify
   waft info

   # Commit the work
   git add [files]
   git commit -m "fix: [description] (TKT-XXXX)"

   # Update ticket via MCP with commit hash
   # mcp_work-efforts_update_ticket with status="completed" and commit="[hash]"

   # Document completion in _pyrite/active/
   ```

5. **At End of Session**:
   ```bash
   # If Empirica initialized:
   waft finding log "Completed [summary]" --impact 0.8
   # Submit postflight assessment

   # Update devlog
   # Update work effort status if all tickets complete
   ```

### Common Mistakes to Avoid

1. **❌ Making all changes, then updating all tickets at the end**
   - ✅ Update tickets incrementally as you work

2. **❌ Making all changes, then making one big commit**
   - ✅ Make small, focused commits after each logical unit

3. **❌ Not using the project's own tools during development**
   - ✅ Use `waft verify`, `waft info`, etc. as you work

4. **❌ Documenting work only at the end**
   - ✅ Document in `_pyrite/active/` as you go

5. **❌ Not using epistemic tracking if available**
   - ✅ Use Empirica sessions, finding/unknown logging during work

6. **❌ Not using MCPs for work effort management**
   - ✅ Use MCP tools to update tickets, create work efforts, etc.

### Integration with MCPs

**Work Effort MCP** (`mcp_work-efforts_*`):
- `list_work_efforts` - Check for active work
- `list_tickets` - See what needs to be done
- `update_ticket` - Update status, add notes, add commit hashes
- `update_work_effort` - Update work effort status, add progress notes

**Usage Pattern**:
```python
# When starting work on a ticket
mcp_work-efforts_update_ticket(
    ticket_path="...",
    status="in_progress"
)

# During work
mcp_work-efforts_update_ticket(
    ticket_path="...",
    notes="Discovered X, investigating Y"
)

# After completing
mcp_work-efforts_update_ticket(
    ticket_path="...",
    status="completed",
    commit="abc123",
    files_changed=["src/file.py", "tests/test_file.py"]
)
```

### Meta-Learning

**The key insight**: If you're building/maintaining a tool, you should be using it to develop itself. This is:
- **Dogfooding**: Using your own product
- **Validation**: Proves the tools work
- **Improvement**: You'll discover issues and improvements
- **Documentation**: Shows how to use the tools

**If you find yourself not using the project's tools during development, ask yourself why:**
- Are the tools not working? → Fix them
- Are the tools too cumbersome? → Improve them
- Are you forgetting? → Make it part of your workflow
- Are you prioritizing "getting it done" over "doing it right"? → Reconsider priorities

---

## Best Practices

### For AI Assistants

1. **Always Echo Understanding**
   - Don't assume you understand
   - Wait for confirmation before proceeding
   - Ask clarifying questions

2. **Test Assumptions Objectively**
   - Don't just confirm what you want to see
   - Test failure cases
   - Test edge cases

3. **Document Everything**
   - What you did
   - Why you did it
   - What you learned
   - What's next

4. **Create Reusable Artifacts**
   - Templates
   - Scripts
   - Checklists
   - Guides

5. **Maintain Quality**
   - Run linters
   - Check for duplicates
   - Validate assumptions
   - Test thoroughly

### For Code Changes

1. **Follow Existing Patterns**
   - Match code style
   - Use existing utilities
   - Follow architecture patterns

2. **Handle Errors Gracefully**
   - Don't fail silently
   - Provide helpful error messages
   - Support graceful degradation

3. **Update Documentation**
   - Keep docs in sync with code
   - Update examples
   - Document new features

4. **Test Your Changes**
   - Write tests for new code
   - Test edge cases
   - Verify assumptions

---

## Example: Complete Session Flow

```
User: "Can we do an experiment right now with what we have to verify if we're understanding everything correctly?"

AI: [Echoes understanding, waits for confirmation]

User: [Confirms]

AI:
1. Identifies assumption to test (TOML parsing)
2. Creates objective test with edge cases
3. Runs test, finds 2 failures
4. Documents findings in SANITY_CHECK_RESULTS.md
5. Recommends fixes

User: "I want you to incorporate 'Empirica' into this project"

AI:
1. Searches for related work (none found)
2. Asks if should create work effort (user confirms)
3. Researches Empirica documentation
4. Creates EmpiricaManager class
5. Integrates into waft new, init, info commands
6. Adds to dependencies
7. Creates 3 documentation files
8. Updates README and devlog

User: "recap let's make a checkpoint"

AI:
1. Creates comprehensive checkpoint document
2. Summarizes all work
3. Documents learnings
4. Lists next steps
5. Updates devlog

User: "can we run pyrite's linter for obsidian on the project please?"

AI:
1. Locates pyrite project
2. Finds obsidian linter tool
3. Runs linter on _work_efforts/
4. Reports findings (63 warnings, 4 broken links)
5. Offers to auto-fix

User: "can we create some code that runs down this process step by step from my very first message to now?"

AI:
1. Creates SESSION_RECAP document
2. Creates reusable session-recap.py script
3. Documents entire process as template
```

---

## Output Artifacts

After following this process, you should have:

1. **Sanity Check Results** (`SANITY_CHECK_RESULTS.md`)
2. **Current State Assessment** (`CURRENT_STATE_ASSESSMENT.md`)
3. **Integration Guides** (`INTEGRATION_[TOOL].md`, `ENHANCED_INTEGRATION.md`)
4. **Checkpoint Document** (`CHECKPOINT_[DATE]_[TOPIC].md`)
5. **Session Recap** (`SESSION_RECAP_[DATE].md`)
6. **Assumptions Document** (`ASSUMPTIONS_AND_TESTS.md`)
7. **Testing Strategy** (`OBJECTIVE_TESTING_STRATEGY.md`)
8. **Meta Analysis** (`META_ANALYSIS.md`)
9. **Updated Project Docs** (README, CHANGELOG, devlog)

---

## Customization

This process is a template. Customize it for your project:

- **Add project-specific checks** (e.g., "Check for _pyrite structure")
- **Include project-specific tools** (e.g., "Run pyrite linter")
- **Adapt to your workflow** (e.g., work efforts, tickets, etc.)
- **Add domain-specific questions** (e.g., "What's our data model?")

---

## Version History

- **v1.0** (2026-01-04): Initial version based on Empirica integration session

---

**This document is evergreen** - Update it as you learn better practices and patterns.

