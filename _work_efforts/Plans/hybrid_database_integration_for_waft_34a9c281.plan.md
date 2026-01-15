---
name: Hybrid Database Integration for Waft
overview: ""
todos: []
---

# Hybrid Database Integration for Waft

## Problem Analysis

The current file-based system works well for basic storage, but you've identified several limitations that a database would address:

1. **Search/Query**: No way to search across files or query by content/metadata
2. **Relationships**: Can't link files together or track dependencies
3. **Metadata**: No structured metadata (tags, dates, status, etc.)
4. **Performance**: File scanning gets slow with many files
5. **Structured Data**: Limited ability to store structured data beyond markdown
6. **Collaboration**: File-based doesn't handle concurrent access well
7. **Analytics**: Hard to generate reports or analytics from files
8. **Real-time**: Web dashboard refreshes every 30 seconds (could be real-time)

## Recommended Approach: Hybrid System

**Keep files, add database for metadata/indexing**

This maintains waft's "files over databases" philosophy while adding powerful capabilities:

- ✅ Files remain the source of truth (human-readable, git-friendly)
- ✅ Database stores metadata, indexes, and relationships
- ✅ Files can be regenerated from database if needed
- ✅ Database is optional (opt-in feature)
- ✅ Backward compatible (existing projects work without database)

## Architecture Decision: SQLite vs Pocketbase

### Option 1: SQLite (Recommended for Start)
**Pros:**
- ✅ Embedded, no server needed
- ✅ Single file database (portable like files)
- ✅ Python stdlib support (sqlite3)
- ✅ Zero external dependencies
- ✅ Perfect for local development
- ✅ Can be git-ignored or committed (your choice)

**Cons:**
- ⚠️ No built-in REST API (but we can add one)
- ⚠️ No real-time subscriptions (but we can use polling/WebSockets)
- ⚠️ No built-in auth (but waft is local-only anyway)

### Option 2: Pocketbase
**Pros:**
- ✅ Built-in REST API
- ✅ Real-time subscriptions
- ✅ Built-in auth (if you want multi-user later)
- ✅ File storage built-in
- ✅ Admin UI included
- ✅ You're familiar with it

**Cons:**
- ⚠️ Requires running server process
- ⚠️ External dependency (less "ambient")
- ⚠️ More complex setup
- ⚠️ Less portable (requires Pocketbase binary)

### Recommendation: Start with SQLite, Add Pocketbase as Optional

**Phase 1**: Implement SQLite for core features (metadata, indexing, relationships)
**Phase 2**: Add Pocketbase as optional enhancement for real-time/API features

## Implementation Plan

### Phase 1: SQLite Foundation

#### 1.1 Database Schema Design
Create `waft/core/database.py` with SQLite schema:

```python
# Core tables
- files: id, path, folder (active/backlog/standards), created_at, updated_at, size, content_hash
- metadata: file_id, key, value (JSON)
- relationships: from_file_id, to_file_id, type (link, depends_on, references, etc.)
- tags: id, name
- file_tags: file_id, tag_id
- search_index: file_id, content (full-text search)
```

#### 1.2 Database Manager
Create `waft/core/database.py`:
- `DatabaseManager` class to handle SQLite operations
- Methods: `index_file()`, `search()`, `get_relationships()`, `add_metadata()`, etc.
- Auto-sync: Watch file system and update database

#### 1.3 Integration Points
- **MemoryManager**: Add optional database indexing
- **Web Dashboard**: Query database instead of scanning files
- **CLI**: Add `waft index` command to build/rebuild index

#### 1.4 File Structure
```
src/waft/
├── core/
│   ├── memory.py (existing)
│   ├── substrate.py (existing)
│   └── database.py (NEW - SQLite manager)
├── web.py (enhance with database queries)
└── main.py (add `waft index` command)
```

### Phase 2: Enhanced Features

#### 2.1 Search Capabilities
- Full-text search across file contents
- Search by metadata (tags, dates, status)
- Search by relationships

#### 2.2 Relationship Tracking
- Link files together (e.g., "task.md depends on spec.md")
- Visualize relationships in web dashboard
- Track dependencies

#### 2.3 Metadata System
- Add tags to files
- Track status (active, completed, blocked)
- Store custom metadata (JSON)

#### 2.4 Real-time Updates
- WebSocket support for live updates
- File watcher to detect changes
- Auto-update database on file changes

### Phase 3: Pocketbase Integration (Optional)

#### 3.1 Pocketbase Wrapper
- Detect if Pocketbase is available
- Fallback to SQLite if not
- Unified API for both backends

#### 3.2 Enhanced Features
- REST API endpoints
- Real-time subscriptions
- Multi-user support (if needed)

## File Changes

### New Files
- `src/waft/core/database.py` - SQLite database manager
- `src/waft/core/schema.sql` - Database schema
- `waft.db` - SQLite database file (in project root, git-ignored by default)

### Modified Files
- `src/waft/core/memory.py` - Add optional database indexing
- `src/waft/web.py` - Use database for queries instead of file scanning
- `src/waft/main.py` - Add `waft index` command
- `pyproject.toml` - Add optional dependencies (pocketbase SDK if needed)
- `.gitignore` - Add `waft.db` (or make it configurable)

## Migration Strategy

1. **Backward Compatible**: Existing projects work without database
2. **Opt-in**: Database is created on first `waft index` command
3. **Gradual Migration**: Files remain source of truth, database is enhancement
4. **No Breaking Changes**: All existing commands work as before

## Usage Examples

```bash
# Index project (creates database, scans files)
waft index

# Search files
waft search "authentication"

# Add metadata to file
waft tag active/task.md --tags "urgent,backend"

# Link files
waft link active/task.md --to backlog/feature.md --type depends_on

# Web dashboard with database (faster, searchable)
waft serve
```

## Benefits

1. **Search**: Fast full-text search across all files
2. **Relationships**: Track dependencies and links
3. **Metadata**: Structured tags and custom data
4. **Performance**: Indexed queries instead of file scanning
5. **Analytics**: Query database for reports
6. **Real-time**: Live updates in web dashboard
7. **Structured Data**: Store JSON alongside files
8. **Collaboration**: Better conflict resolution with metadata

## Trade-offs

**Added Complexity:**
- Database file to manage
- Indexing process to run
- More code to maintain

**Benefits:**
- Much more powerful features
- Better perfo