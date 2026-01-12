# Journal

**Comprehensive AI journal system hub - view, search, reflect, and analyze your journal.**

The journal is the AI's memory of its thoughts, learnings, and experiences. This command provides a unified interface to interact with the journal system, view recent entries, search history, view statistics, and write new reflections.

**Use when:** You want to interact with the AI journal system - view entries, search history, check statistics, or understand what the AI has been thinking and learning.

---

## Purpose

This command provides:
- **Journal Overview**: Quick view of journal status and recent entries
- **Entry Browsing**: View recent entries with summaries
- **Search Interface**: Quick access to journal search
- **Statistics Dashboard**: View journal analytics
- **Reflection Prompt**: Quick way to write new entries
- **System Health**: Check journal structure and archives

---

## Philosophy

1. **Journal as Memory**: The journal is the AI's persistent memory of its cognitive journey
2. **Easy Access**: One command to access all journal functionality
3. **Discovery**: Help discover patterns, insights, and learnings
4. **Continuity**: Bridge between sessions and work efforts
5. **Self-Awareness**: Enable the AI to understand its own thinking patterns

---

## What the Journal Contains

### 1. Reflections
- **What I'm Doing**: Current work, tasks, features
- **What I'm Thinking**: Thoughts, concerns, ideas
- **What I'm Learning**: Insights, discoveries, realizations
- **Patterns**: Recurring themes, approaches, behaviors
- **Questions**: Uncertainties, curiosities, explorations
- **Feelings**: Emotional/experiential states
- **What I'd Do Differently**: Improvements, adjustments
- **Meta-Reflection**: Thinking about thinking

### 2. Context
- **Git State**: Branch, uncommitted files
- **Session Stats**: Files created/modified, lines written
- **Timestamps**: Precise entry timing
- **Topics**: Focus areas for entries

### 3. History
- **Chronological Record**: All entries in order
- **Archived Entries**: Older entries preserved
- **Searchable**: Full-text search across all entries
- **Indexed**: Fast lookups by topic, date, content

---

## Execution Steps

1. **Check Journal Status**
   - Verify journal exists
   - Check entry count
   - Verify structure

2. **Display Overview**
   - Recent entries (last 3-5)
   - Quick statistics
   - System health

3. **Provide Options**
   - View recent entries
   - Search entries
   - View statistics
   - Write new reflection
   - Check archives

4. **Execute Requested Action**
   - Display results
   - Format nicely
   - Provide next steps

---

## Output Format

### Journal Overview

```markdown
📔 AI Journal System

**Status**: Active
**Location**: _pyrite/journal/ai-journal.md
**Total Entries**: 42
**Last Entry**: 2026-01-12 11:37

**Recent Entries**:
1. 2026-01-12 11:37 - AI Journal System Enhancement
   Reflection on comprehensive journal improvements...
   
2. 2026-01-12 05:45 - Scientific Method Tool Implementation
   Completed implementation of experimental framework...
   
3. 2026-01-12 05:00 - Notebook System: The Self-Engineering Memory
   Implemented notebook system for self-engineering layer...

**Quick Stats**:
- Total Words: 45,230
- Average Entry: 1,077 words
- Archives: 2 files (1.2 MB)
- First Entry: 2026-01-07

**Available Actions**:
- `/journal view` - View full recent entries
- `/journal search <query>` - Search entries
- `/journal stats` - Detailed statistics
- `/journal reflect` - Write new entry
- `/journal archive` - View archives
```

---

## Journal Location

**Default Location**: `_pyrite/journal/ai-journal.md`

**Placement Rationale**: 
- `_pyrite/` is the memory layer - journal is part of AI's memory system
- Consistent with other memory components (active/, backlog/, standards/)
- Separates AI cognitive artifacts from project code
- Enables easy backup and archival

**Structure**:
```
_pyrite/journal/
├── ai-journal.md          # Main journal file (appended entries)
├── index.json             # Fast lookup index for entries
├── entries/               # Individual entry files
│   └── YYYY-MM-DD-HHMM.md
├── archive/               # Archived entries (auto-archived when >500 lines)
│   └── ai-journal-YYYY-MM-DD.md
└── stats/                 # Statistics and analytics data
```

---

## Use Cases

### 1. Quick Overview
**Scenario**: Want to see what the AI has been thinking about recently

**Example**:
```
User: "/journal"

AI: [Displays journal overview with recent entries and quick stats]

AI: ✅ Journal overview displayed
    Recent entries: 3
    Total entries: 42
    Last entry: 2026-01-12 11:37
```

---

### 2. Search History
**Scenario**: Looking for entries about a specific topic

**Example**:
```
User: "/journal search architecture"

AI: [Searches journal and displays matching entries]

AI: ✅ Found 5 entries matching "architecture"
    1. 2026-01-11 - Architecture investigation
    2. 2026-01-09 - Component evolution system
    ...
```

---

### 3. View Statistics
**Scenario**: Want to understand journal usage patterns

**Example**:
```
User: "/journal stats"

AI: [Displays comprehensive statistics table]

AI: ✅ Statistics displayed
    Total entries: 42
    Total words: 45,230
    Average entry: 1,077 words
    Archives: 2 files (1.2 MB)
```

---

### 4. Write Reflection
**Scenario**: Want to prompt AI to reflect on current work

**Example**:
```
User: "/journal reflect"

AI: [Prompts AI to write journal entry, same as /reflect]

AI: ✅ Reflection prompts displayed
    Journal entry structure created
    Ready for AI to write reflection
```

---

### 5. View Recent Entries
**Scenario**: Want to read recent journal entries in detail

**Example**:
```
User: "/journal view"

AI: [Displays full content of recent entries]

AI: ✅ Recent entries displayed
    Showing last 5 entries
    Total: ~3,500 words
```

---

## Command Variations

### `/journal` (default)
- Shows overview with recent entries and quick stats
- Provides action suggestions

### `/journal view [N]`
- View recent entries (default: last 5)
- `N` = number of entries to show

### `/journal search <query> [--topic <topic>] [--from <date>] [--to <date>]`
- Search entries by query
- Optional filters: topic, date range
- Example: `/journal search "learning" --topic "architecture"`

### `/journal stats [--cleanup]`
- Display comprehensive statistics
- Optional: cleanup old archives

### `/journal reflect [--topic <topic>] [--prompt <prompt>]`
- Write new journal entry
- Same as `/reflect` command
- Optional: topic focus, custom prompt

### `/journal archive [--list]`
- View archive information
- Optional: list all archive files

### `/journal entry <date-time>`
- View specific entry by date-time
- Example: `/journal entry 2026-01-12-1137`

---

## Integration with Other Commands

- **`/reflect`**: Same functionality (write entries)
- **`/continue`**: Can reference journal for context
- **`/resume`**: Uses journal for session continuity
- **`/checkpoint`**: Complements journal (state vs reflection)
- **`/analyze`**: Journal captures AI's thoughts about analysis
- **`journal-search`**: CLI command for search (waft journal-search)
- **`journal-stats`**: CLI command for stats (waft journal-stats)

---

## When to Use

**Use `/journal` when**:
- ✅ Want overview of AI's recent thoughts
- ✅ Need to search journal history
- ✅ Want to view statistics
- ✅ Need to understand what AI has learned
- ✅ Want to prompt new reflection
- ✅ Need to explore journal system

**Don't use `/journal` when**:
- ❌ Just want to write reflection (use `/reflect` directly)
- ❌ Need to continue work (use `/continue`)
- ❌ Need to pick up from last session (use `/resume`)
- ❌ Need to document current state (use `/checkpoint`)

---

## Journal Maintenance

### Automatic
- Journal created automatically if missing
- Entries appended with timestamps
- Auto-archiving when >500 lines
- Index updates automatically
- Structure maintained automatically

### Manual
- Journal can be read directly: `_pyrite/journal/ai-journal.md`
- Entries can be reviewed for patterns
- Journal can be searched via CLI: `waft journal-search`
- Statistics available via CLI: `waft journal-stats`
- Archives can be cleaned: `waft journal-stats --cleanup`

### Best Practices
- Use `/journal` regularly to check status
- Search before writing to avoid duplicates
- Review statistics periodically
- Clean up old archives annually
- Use journal for continuity across sessions

---

## Example Journal Overview

```markdown
📔 AI Journal System

**Status**: ✅ Active
**Location**: _pyrite/journal/ai-journal.md
**Total Entries**: 42
**Last Entry**: 2026-01-12 11:37

---

## Recent Entries

### 1. 2026-01-12 11:37 - AI Journal System Enhancement

**What I'm Doing**: Just completed comprehensive enhancement of the AI journal system...

**What I'm Learning**: The journal placement in _pyrite/journal/ is appropriate as part of the memory layer...

**Patterns I Notice**: Comprehensive documentation before implementation, systematic enhancement approach...

---

### 2. 2026-01-12 05:45 - Scientific Method Tool Implementation

**What I'm Doing**: Just completed implementation of the scientific method tool...

**What I'm Learning**: Scientific method structure maps perfectly to software systems...

---

## Quick Statistics

| Metric | Value |
|--------|-------|
| Total Entries | 42 |
| Total Words | 45,230 |
| Average Entry | 1,077 words |
| Archive Files | 2 (1.2 MB) |
| First Entry | 2026-01-07 |
| Last Entry | 2026-01-12 11:37 |

---

## Available Actions

- **`/journal view`** - View full recent entries
- **`/journal search <query>`** - Search entries
- **`/journal stats`** - Detailed statistics
- **`/journal reflect`** - Write new entry
- **`/journal archive`** - View archives
```

---

## Technical Details

### Journal System Components

1. **ReflectManager** (`src/waft/core/reflect.py`)
   - Manages journal entries
   - Handles archiving
   - Provides search
   - Calculates statistics

2. **Index System** (`_pyrite/journal/index.json`)
   - Fast entry lookups
   - Topic tracking
   - Metadata storage

3. **Archive System** (`_pyrite/journal/archive/`)
   - Auto-archiving when >500 lines
   - Retention policy (1 year)
   - Cleanup commands

4. **CLI Commands**
   - `waft journal-search` - Search entries
   - `waft journal-stats` - View statistics
   - `waft reflect` - Write entries

---

## Future Enhancements

### Potential Additions

1. **Visualization**: Charts for entry frequency, word counts
2. **Export**: Export to PDF, HTML, JSON
3. **AI Analysis**: Pattern detection across entries
4. **Tags**: User-defined tags for entries
5. **Integration**: Deeper integration with Empirica, Being system

---

**This command provides a comprehensive hub for interacting with the AI journal system - the AI's memory of its thoughts, learnings, and experiences.**
