# Todos

**Todo management and tracking - manage tasks.**

Manages and tracks todos across the project, listing current todos, adding new todos, updating todo status, and showing todo history. Perfect for task tracking and management.

**Use when:** Need to track tasks, manage todos, or see what needs to be done.

---

## Purpose

This command provides:
- **Todo Listing**: List current todos with status
- **Todo Management**: Add, update, and complete todos
- **Todo Tracking**: Track todo history and changes
- **Todo Organization**: Organize todos by category
- **Todo Status**: Show todo status and progress

---

## Philosophy

1. **Simple**: Easy to use and understand
2. **Flexible**: Support various todo formats
3. **Traceable**: Track todo history
4. **Organized**: Group and categorize todos
5. **Actionable**: Clear next actions

---

## Execution Steps

### Todos 1.1: Load Current Todos
**Purpose**: Load existing todos

**Steps**:
1. Check for todo files (`.cursor/todos.md`, `_work_efforts/todos.md`, etc.)
2. Load todos from work effort tickets (via MCP)
3. Parse todo format
4. Organize by status (pending, in_progress, completed)

**Output**: Current todos list

---

### Todos 1.2: Display Todos
**Purpose**: Show todos to user

**Steps**:
1. Format todos by status
2. Show pending todos first
3. Show in-progress todos
4. Show completed todos (if requested)
5. Display counts and statistics

**Output**: Formatted todo list

---

### Todos 1.3: Todo Operations (if requested)
**Purpose**: Perform todo operations

**Steps**:
1. **Add Todo**: Create new todo
   - Get todo description
   - Assign category (if applicable)
   - Set initial status (pending)
   - Save to todo file

2. **Update Todo**: Update existing todo
   - Select todo to update
   - Update status or description
   - Save changes

3. **Complete Todo**: Mark todo as done
   - Select todo to complete
   - Update status to completed
   - Add completion date
   - Move to completed section

4. **Delete Todo**: Remove todo
   - Select todo to delete
   - Confirm deletion
   - Remove from todo file

**Output**: Updated todo list

---

### Todos 1.4: Save Todos
**Purpose**: Save todos to file

**Steps**:
1. Format todos for storage
2. Save to appropriate file
3. Update work effort tickets (if applicable)
4. Update devlog (if significant changes)

**Output**: Saved todos

---

## Execution Flow

```
Todos 1.1: Load Current Todos
  ↓
Todos 1.2: Display Todos
  ↓
[If operations requested]
Todos 1.3: Todo Operations
  ↓
Todos 1.4: Save Todos
  ↓
✅ Complete - Todos displayed/updated
```

---

## Output Format

### Console Output

The command displays todos:

```
📋 Todos: Task Management

Pending (5):
  [ ] TKT-g0ih-003: Implement /todos command
  [ ] TKT-g0ih-004: Implement /search command
  [ ] TKT-g0ih-005: Implement /cleanup command
  [ ] TKT-g0ih-006: Implement /links command
  [ ] Update COMMAND_RECOMMENDATIONS.md

In Progress (1):
  [→] TKT-g0ih-002: Implement /sync command

Completed (2):
  [✓] TKT-g0ih-001: Implement /context command
  [✓] Create work effort for Cursor Development Plan Phase 1

Statistics:
  Total: 8 todos
  Pending: 5
  In Progress: 1
  Completed: 2
  Completion: 25%
```

---

## Todo Format

### File Format

Todos are stored in markdown format:

```markdown
# Todos

## Pending

- [ ] TKT-g0ih-003: Implement /todos command
- [ ] TKT-g0ih-004: Implement /search command

## In Progress

- [→] TKT-g0ih-002: Implement /sync command

## Completed

- [✓] TKT-g0ih-001: Implement /context command (2026-01-12)
```

### Work Effort Integration

Todos can be integrated with work effort tickets:
- Load todos from work effort tickets
- Update ticket status based on todo status
- Sync todos with ticket system

---

## Use Cases

### 1. List Current Todos
**Scenario**: Want to see what needs to be done

**Example**:
```
User: "/todos"
```

**Output**: Current todos list

---

### 2. Add New Todo
**Scenario**: Need to add a new task

**Example**:
```
User: "/todos add 'Review documentation'"
```

**Output**: Todo added, list updated

---

### 3. Update Todo Status
**Scenario**: Mark todo as in progress or completed

**Example**:
```
User: "/todos complete 'Implement /todos command'"
```

**Output**: Todo marked as completed

---

### 4. Todo Management
**Scenario**: Manage todos interactively

**Example**:
```
User: "/todos"
AI: [Shows todos]
User: "Mark 'Implement /search' as in progress"
AI: [Updates todo]
```

**Output**: Todo updated

---

## Integration with Other Commands

- **`/status`**: Shows todo count (`/todos` shows details)
- **`/checkpoint`**: Includes todos (`/todos` manages them)
- **`/context`**: Shows todos (`/todos` manages them)
- **Work Efforts**: Integrates with ticket system

---

## When to Use

**Use `/todos` when**:
- ✅ Need to track tasks
- ✅ Want to see what needs to be done
- ✅ Need to add/update todos
- ✅ Want todo management
- ✅ Need todo organization

**Don't use `/todos` when**:
- ❌ Need quick status (use `/status`)
- ❌ Need comprehensive checkpoint (use `/checkpoint`)
- ❌ Using external todo system (use that instead)

---

## Technical Details

### Tools Used

**File System**:
- File reading/writing for todo files
- Markdown parsing for todo format

**MCP Servers** (if available):
- `mcp_work-efforts_list_tickets` - Load todos from tickets
- `mcp_work-efforts_update_ticket` - Update ticket status

**Todo File Locations**:
- `.cursor/todos.md` (project-level)
- `_work_efforts/todos.md` (work effort todos)
- Work effort tickets (via MCP)

### Performance

- **Target Time**: < 5 seconds
- **Load Todos**: ~1 second
- **Display**: ~1 second
- **Operations**: ~2 seconds
- **Save**: ~1 second

### Error Handling

- **File Errors**: Create new todo file if missing
- **MCP Errors**: Fall back to file-based todos
- **Parse Errors**: Show error, continue with available todos
- **Always Complete**: Always show available todos

---

## Example Workflow

```
User: "/todos"

AI: 📋 Todos: Task Management

Pending (5):
  [ ] Implement /todos command
  [ ] Implement /search command
  [ ] Implement /cleanup command
  [ ] Implement /links command
  [ ] Update COMMAND_RECOMMENDATIONS.md

In Progress (1):
  [→] Implement /sync command

Completed (2):
  [✓] Implement /context command
  [✓] Create work effort

Total: 8 | Pending: 5 | In Progress: 1 | Completed: 2

User: "Add 'Test all new commands'"
AI: ✅ Todo added
📋 Todos updated

User: [Continues work]
```

---

## Advanced Features

### Categories
Organize todos by category:
```bash
/todos --category "commands"    # Show command todos
/todos add "Fix bug" --category "bugs"
```

### Filtering
Filter todos:
```bash
/todos --pending               # Show pending only
/todos --completed             # Show completed only
/todos --in-progress           # Show in progress only
```

### Statistics
Get todo statistics:
```bash
/todos --stats                 # Show statistics
```

### History
View todo history:
```bash
/todos --history              # Show todo history
```

---

## Best Practices

1. **Keep Updated**: Update todo status regularly
2. **Be Specific**: Use clear, actionable todo descriptions
3. **Organize**: Use categories for organization
4. **Complete**: Mark todos as done when finished
5. **Review**: Regularly review and clean up todos

---

## Output Location

Todos are stored in:
- `.cursor/todos.md` (project-level)
- `_work_efforts/todos.md` (work effort todos)
- Work effort tickets (via MCP integration)

Display is shown in console.

---

**This command provides simple and effective todo management - perfect for tracking tasks and staying organized.**
