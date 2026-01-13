# Search

**Search across documentation - find information quickly.**

Searches across documentation files in `_work_efforts/`, `_pyrite/`, and codebase, returning relevant results with context. Perfect for finding information, locating references, or discovering related content.

**Use when:** Need to find information, search documentation, or locate references.

---

## Purpose

This command provides:
- **Documentation Search**: Search `_work_efforts/` files
- **Memory Search**: Search `_pyrite/` files
- **Codebase Search**: Search codebase files
- **Context Results**: Return results with context
- **Relevant Matches**: Rank results by relevance

---

## Philosophy

1. **Fast**: Quick search results
2. **Relevant**: Return most relevant matches
3. **Contextual**: Show context around matches
4. **Comprehensive**: Search all relevant areas
5. **Useful**: Actionable search results

---

## Execution Steps

### Search 1.1: Parse Search Query
**Purpose**: Understand what to search for

**Steps**:
1. Get search query from user
2. Parse query for keywords
3. Identify search scope (if specified)
4. Determine search type (text, regex, etc.)

**Output**: Parsed search query

---

### Search 1.2: Search Work Efforts
**Purpose**: Search `_work_efforts/` directory

**Steps**:
1. Search markdown files in `_work_efforts/`
2. Use grep or codebase search
3. Find matching files and lines
4. Extract context around matches
5. Rank by relevance

**Output**: Work effort search results

---

### Search 1.3: Search Memory Layer
**Purpose**: Search `_pyrite/` directory

**Steps**:
1. Search markdown files in `_pyrite/`
2. Search active/, backlog/, standards/ subdirectories
3. Find matching content
4. Extract context
5. Rank by relevance

**Output**: Memory layer search results

---

### Search 1.4: Search Codebase
**Purpose**: Search codebase files

**Steps**:
1. Search source code files
2. Search documentation files
3. Find matching code and comments
4. Extract context
5. Rank by relevance

**Output**: Codebase search results

---

### Search 1.5: Format and Display Results
**Purpose**: Present search results

**Steps**:
1. Combine all search results
2. Rank by relevance
3. Format with context
4. Display results with file paths
5. Show match counts

**Output**: Formatted search results

---

## Execution Flow

```
Search 1.1: Parse Search Query
  ↓
Search 1.2: Search Work Efforts
  ↓
Search 1.3: Search Memory Layer
  ↓
Search 1.4: Search Codebase
  ↓
Search 1.5: Format and Display Results
  ↓
✅ Complete - Search results displayed
```

---

## Output Format

### Console Output

The command displays search results:

```
🔍 Search: "cursor commands"

Found 15 matches across 8 files

Work Efforts (8 matches):
  _work_efforts/devlog.md
    Line 1350: Created comprehensive Cursor command system
    Line 2732: Engineered `/phase2` command definition
    Line 3301: Created comprehensive Cursor command system

  _work_efforts/CHECKPOINT_2026-01-07_cursor_commands_creation.md
    Line 1: Checkpoint: Cursor Commands Creation
    Line 12: Created comprehensive Cursor command system

Memory Layer (4 matches):
  _pyrite/active/2026-01-06_engineering_spinup.md
    Line 45: Cursor commands for workflow management

  _pyrite/standards/verification/verification_traces.md
    Line 12: Cursor command verification

Codebase (3 matches):
  .cursor/commands/help.md
    Line 23: Cursor commands help system
    Line 45: List of available commands

  .cursor/commands/COMMAND_RECOMMENDATIONS.md
    Line 1: Recommended Cursor Commands

Summary:
  Total Matches: 15
  Files: 8
  Work Efforts: 8 matches
  Memory Layer: 4 matches
  Codebase: 3 matches
```

---

## Search Scope

### Work Efforts (`_work_efforts/`)
- All markdown files
- Work effort indexes
- Devlog entries
- Checkpoint files
- Session recaps

### Memory Layer (`_pyrite/`)
- Active files (`active/`)
- Backlog files (`backlog/`)
- Standards files (`standards/`)
- Journal entries
- Analysis documents

### Codebase
- Source code files
- Documentation files
- Configuration files
- Command definitions
- README files

---

## Use Cases

### 1. Find Information
**Scenario**: Need to find specific information

**Example**:
```
User: "/search cursor commands"
```

**Output**: All matches for "cursor commands"

---

### 2. Locate References
**Scenario**: Find where something is referenced

**Example**:
```
User: "/search 'work effort'"
```

**Output**: All references to work efforts

---

### 3. Discover Related Content
**Scenario**: Find related documentation

**Example**:
```
User: "/search 'PDF generation'"
```

**Output**: All content related to PDF generation

---

### 4. Code Search
**Scenario**: Find code references

**Example**:
```
User: "/search --code 'Visualizer'"
```

**Output**: Code matches for "Visualizer"

---

## Integration with Other Commands

- **`/status`**: Quick status (`/search` finds information)
- **`/context`**: Provides context (`/search` finds related context)
- **`/links`**: Creates links (`/search` finds link targets)
- **`/sync`**: Syncs docs (`/search` finds what to sync)

---

## When to Use

**Use `/search` when**:
- ✅ Need to find information
- ✅ Want to locate references
- ✅ Need to discover related content
- ✅ Want to search documentation
- ✅ Need code search

**Don't use `/search` when**:
- ❌ Need quick status (use `/status`)
- ❌ Need current context (use `/context`)
- ❌ Using external search tool (use that instead)

---

## Technical Details

### Tools Used

**Search Tools**:
- `grep` - Text search
- `codebase_search` - Semantic search (if available)
- `grep` tool - Pattern matching

**File System**:
- `find` - Find files to search
- File reading for context extraction

**MCP Servers** (if available):
- `mcp_docs-maintainer_search_docs` - Search documentation
- `mcp_work-efforts_search_work_efforts` - Search work efforts

### Performance

- **Target Time**: < 10 seconds
- **Query Parse**: ~1 second
- **Work Efforts Search**: ~2 seconds
- **Memory Layer Search**: ~2 seconds
- **Codebase Search**: ~3 seconds
- **Result Formatting**: ~2 seconds

### Error Handling

- **No Results**: Show "No matches found"
- **File Errors**: Skip problematic files, continue
- **Search Errors**: Show error, return partial results
- **Always Complete**: Always show available results

---

## Example Workflow

```
User: "/search 'cursor development plan'"

AI: 🔍 Search: "cursor development plan"

Found 3 matches across 2 files

Work Efforts (2 matches):
  .cursor/CURSOR_DEVELOPMENT_PLAN.md
    Line 1: # Cursor Development Plan
    Line 122: ## Phase 1: Complete Missing Commands

  _work_efforts/devlog.md
    Line 4200: Cursor Development Plan implementation

Summary:
  Total Matches: 3
  Files: 2
  Work Efforts: 2 matches
  Codebase: 1 match

User: [Reviews results, finds information]
```

---

## Advanced Features

### Search Scope
Limit search scope:
```bash
/search "query" --work        # Work efforts only
/search "query" --memory      # Memory layer only
/search "query" --code       # Codebase only
/search "query" --all         # All (default)
```

### Search Type
Specify search type:
```bash
/search "query" --exact       # Exact match
/search "query" --regex       # Regex pattern
/search "query" --case        # Case sensitive
```

### Result Format
Control result format:
```bash
/search "query" --brief       # Brief results
/search "query" --detailed    # Detailed results
/search "query" --json        # JSON output
```

### Limit Results
Limit number of results:
```bash
/search "query" --limit 10    # Limit to 10 results
```

---

## Best Practices

1. **Be Specific**: Use specific search terms
2. **Use Quotes**: Quote multi-word queries
3. **Scope Search**: Limit scope when possible
4. **Review Results**: Review all relevant results
5. **Refine Query**: Refine query if too many/few results

---

## Output Location

Search results are displayed in console.

For persistent results:
- Use `--json` flag for machine-readable output
- Redirect output to file if needed

---

**This command provides fast and comprehensive search across all documentation - essential for finding information quickly.**
