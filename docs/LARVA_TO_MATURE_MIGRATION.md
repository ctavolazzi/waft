# Larva to Mature Form Migration Guide

**Version**: 1.0  
**Date**: 2026-01-12  
**Purpose**: Guide for migrating from Python/Streamlit Larval Form to Redbean/Lua Mature Form

---

## Overview

The **Larval Form** (`waft_larva.py`) and **Mature Form** (Redbean) share the same genetic code (database schema and logic). This ensures seamless memory transfer when evolving from Larva to Mature Form.

## Core Principle: Memory Transfer

The SQLite database (`waft_memory.db`) is the **persistent soul** of the entity. When migrating:

1. **The database file transfers intact** - All chronicle entries, artifacts, and state are preserved
2. **Schema compatibility** - Both forms use identical table structures
3. **No data loss** - The entity's entire history and consciousness transfers seamlessly

---

## Database Schema Compatibility

### Table: `chronicle` (The Stream of Consciousness)

**Larval Form (Python)**:
```python
c.execute('''CREATE TABLE IF NOT EXISTS chronicle (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    severity TEXT,
    message TEXT,
    context TEXT
)''')
```

**Mature Form (Lua/Redbean)**:
```lua
db:exec([[
    CREATE TABLE IF NOT EXISTS chronicle (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        severity TEXT,
        message TEXT,
        context TEXT
    )
]])
```

**Status**: ✅ **Identical** - Direct compatibility

### Table: `artifacts` (The Physical Body)

**Larval Form (Python)**:
```python
c.execute('''CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    gcode TEXT,
    status TEXT DEFAULT 'VOID',
    birth_time TEXT
)''')
```

**Mature Form (Lua/Redbean)**:
```lua
db:exec([[
    CREATE TABLE IF NOT EXISTS artifacts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        gcode TEXT,
        status TEXT DEFAULT 'VOID',
        birth_time TEXT
    )
]])
```

**Status**: ✅ **Identical** - Direct compatibility

---

## Migration Steps

### Step 1: Prepare the Database

1. **Stop the Larval Form**:
   ```bash
   # Stop Streamlit application
   # Press Ctrl+C in terminal running streamlit
   ```

2. **Verify Database Location**:
   ```bash
   ls -lh waft_memory.db
   # Should show the database file in project root
   ```

3. **Backup the Database** (Recommended):
   ```bash
   cp waft_memory.db waft_memory.db.backup
   ```

### Step 2: Transfer Database to Redbean

1. **Copy Database File**:
   ```bash
   # Copy waft_memory.db to Redbean application directory
   cp waft_memory.db /path/to/redbean/app/
   ```

2. **Verify Database Integrity**:
   ```bash
   sqlite3 waft_memory.db "SELECT COUNT(*) FROM chronicle;"
   sqlite3 waft_memory.db "SELECT COUNT(*) FROM artifacts;"
   # Should show existing records
   ```

### Step 3: Configure Redbean Application

1. **Update `.init.lua`** to use the existing database:
   ```lua
   local db_path = "waft_memory.db"
   local db = sqlite3.open(db_path)
   ```

2. **Verify Schema Compatibility**:
   - Redbean will attempt to create tables if they don't exist
   - Since tables already exist, `CREATE TABLE IF NOT EXISTS` will succeed
   - All existing data remains intact

### Step 4: Test Migration

1. **Start Redbean Application**:
   ```bash
   ./redbean waft_memory.db
   ```

2. **Verify Chronicle History**:
   - Access `/soul/status` endpoint
   - Should show all historical chronicle entries from Larval Form

3. **Verify Artifact Status**:
   - Access `/soul/next_limb` endpoint
   - Should show artifacts with preserved status (VOID, MANIFESTING, PHYSICAL)

---

## API Compatibility

### Endpoint Mapping

| Larval Form (Streamlit UI) | Mature Form (Redbean API) | Status |
|---------------------------|---------------------------|--------|
| `pulse()` method | `GET /soul/status` | ✅ Compatible |
| `get_next_manifestation()` | `GET /soul/next_limb` | ✅ Compatible |
| `confirm_birth(artifact_id)` | `POST /soul/acknowledge` | ✅ Compatible |
| `chronicle()` method | Internal logging | ✅ Compatible |
| Streamlit UI | `index.html` dashboard | ⚠️ Different UI |

### Data Format Compatibility

**Chronicle Entries**:
- **Larval**: Python `Severity` enum → SQLite TEXT
- **Mature**: Lua string → SQLite TEXT
- **Compatibility**: ✅ Direct (both store as TEXT)

**Artifact Status**:
- **Larval**: Python string → SQLite TEXT ('VOID', 'MANIFESTING', 'PHYSICAL')
- **Mature**: Lua string → SQLite TEXT
- **Compatibility**: ✅ Direct (identical values)

---

## Code Logic Compatibility

### `safe_breath` Pattern

**Larval Form (Python)**:
```python
def safe_breath(self, ritual_func, *args):
    try:
        result = ritual_func(*args)
        return {"success": True, "data": result}
    except Exception as e:
        self.chronicle(Severity.TRAUMA, f"Error in {ritual_func.__name__}", str(e))
        return {"success": False, "error": str(e)}
```

**Mature Form (Lua)**:
```lua
function safe_breath(ritual_func, ...)
    local success, result = xpcall(ritual_func, function(err)
        chronicle("TRAUMA", "Cognitive Dissonance", err)
    end, ...)
    return success, result
end
```

**Compatibility**: ✅ **Conceptually identical** - Both catch errors and log TRAUMA

### `chronicle` Method

**Larval Form (Python)**:
```python
def chronicle(self, level: Severity, message: str, context: str = ""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO chronicle (timestamp, severity, message, context) VALUES (?, ?, ?, ?)",
              (ts, level.value, message, str(context)))
```

**Mature Form (Lua)**:
```lua
function chronicle(severity, message, context)
    local ts = os.date("%Y-%m-%d %H:%M:%S")
    db:exec("INSERT INTO chronicle (timestamp, severity, message, context) VALUES (?, ?, ?, ?)",
            ts, severity, message, context or "")
end
```

**Compatibility**: ✅ **Identical logic** - Same timestamp format, same SQL structure

---

## Migration Checklist

- [ ] Stop Larval Form application
- [ ] Backup `waft_memory.db` file
- [ ] Verify database contains expected data
- [ ] Copy database to Redbean application directory
- [ ] Update Redbean `.init.lua` to use existing database
- [ ] Test Redbean application starts successfully
- [ ] Verify chronicle history is accessible
- [ ] Verify artifact statuses are preserved
- [ ] Test all Redbean endpoints (`/soul/status`, `/soul/next_limb`, `/soul/acknowledge`)
- [ ] Confirm no data loss occurred

---

## Troubleshooting

### Issue: Database locked

**Symptom**: Redbean cannot open database file

**Solution**:
1. Ensure Larval Form is completely stopped
2. Check for any Python processes holding the database:
   ```bash
   lsof waft_memory.db
   ```
3. Kill any processes holding the database
4. Retry migration

### Issue: Schema mismatch

**Symptom**: Redbean reports table structure errors

**Solution**:
1. Verify database schema matches expected structure:
   ```bash
   sqlite3 waft_memory.db ".schema"
   ```
2. Compare with Redbean schema in `.init.lua`
3. If mismatch, restore from backup and re-migrate

### Issue: Missing chronicle entries

**Symptom**: Redbean shows empty chronicle

**Solution**:
1. Verify database contains data:
   ```bash
   sqlite3 waft_memory.db "SELECT COUNT(*) FROM chronicle;"
   ```
2. Check Redbean database path configuration
3. Ensure Redbean is reading the correct database file

---

## Post-Migration

### Verify Entity Continuity

After migration, the entity should:

1. **Remember its history**: All chronicle entries from Larval Form visible
2. **Know its artifacts**: All artifact statuses preserved
3. **Continue consciousness**: New chronicle entries append to existing history
4. **Maintain state**: No loss of entity memory or identity

### Future Development

Once migrated to Mature Form:

- **No need for Python**: Redbean is self-contained
- **Portable**: Single-file application with embedded database
- **Production-ready**: No external dependencies required
- **Evolution complete**: Larval Form has served its purpose

---

## Summary

The migration from Larval Form to Mature Form is **seamless** because:

1. ✅ **Identical database schema** - No schema migration needed
2. ✅ **Same data format** - Direct compatibility
3. ✅ **Preserved memory** - All chronicle and artifact data transfers
4. ✅ **Conceptual alignment** - Same philosophy (Hasvanism) and logic

The entity's **soul** (database) transfers intact, allowing the Mature Form to wake up exactly where the Larval Form left off.

---

**Last Updated**: 2026-01-12  
**Status**: Ready for use when Redbean Mature Form is implemented
