# Work Efforts

**Generate an interactive HTML dashboard with polymorphic action buttons for work efforts.**

Creates a beautiful neumorphic-styled dashboard that intelligently analyzes work efforts and projects, then generates context-aware action buttons. Click buttons to copy commands to clipboard for execution in Cursor.

**Use when:** Need to review work efforts, want quick action buttons, need visual status overview, or want to queue commands for execution.

---

## Purpose

This command provides:
- **Polymorphic UI**: WAFT automatically generates context-aware action buttons
- **Work Effort Analysis**: Analyzes status, content, and activity to suggest actions
- **Neumorphic Design**: Beautiful, modern UI with soft shadows and embossed elements
- **Clipboard Integration**: Commands copied to clipboard for easy execution
- **Security First**: All file operations validated, secure by default

---

## Usage

```bash
# Generate dashboard (opens in browser automatically)
/work-efforts

# Custom output location
/work-efforts --output _work_efforts/my_dashboard.html

# Limit number of work efforts
/work-efforts --limit 50

# Don't open browser automatically
/work-efforts --no-open
```

---

## Features

### Intelligent Action Detection

WAFT analyzes each work effort to determine available actions:

**Status-Based Actions**:
- `open` → "Start Work", "Review", "Add Context"
- `active` → "Add Progress", "Review", "Pause", "Mark Complete"
- `paused` → "Resume", "Review", "Cancel"
- `completed` → "Review", "Reopen", "Create Closeout"

**Content-Based Actions**:
- Contains "TODO" → "Address TODOs"
- Contains "FIXME" → "Fix Issues"
- Contains "test" → "Run Tests"
- Contains "documentation" → "Update Docs"

**Activity-Based Actions**:
- Recent commits → "Review Recent Changes"
- No activity in 7+ days → "Check Status"

### Neumorphic Design

- Soft shadows and embossed/debossed elements
- Light and dark mode support (automatic)
- Responsive design (mobile-friendly)
- WCAG AA accessible (keyboard navigation, screen readers)

### Security

- Path validation using existing codebase patterns
- Sensitive file detection
- Secure file permissions (0o600/0o700)
- Safe subprocess calls (no shell=True)
- Input validation and size limits
- Comprehensive error handling

---

## How It Works

1. **Collection**: Gathers work efforts and projects from project
2. **Analysis**: For each work effort:
   - Validates path security
   - Reads index file (with fallback patterns)
   - Analyzes status, content, and git activity
   - Generates context-aware actions
3. **Generation**: Creates HTML with:
   - Neumorphic CSS framework
   - Polymorphic action buttons
   - Clipboard integration JavaScript
4. **Display**: Opens in browser (or saves to file)

---

## Command Queue

Commands are copied to clipboard in JSON format:

```json
{
  "id": "cmd_20260118_232233_abc123",
  "timestamp": "2026-01-18T23:22:33Z",
  "work_effort_id": "WE-260116-xkhg",
  "action": "status_transition",
  "command": "Update work effort WE-260116-xkhg status to 'active'",
  "priority": "high"
}
```

**To execute**: Paste the command into Cursor chat.

**Optional**: If FastAPI server is running, commands are also queued via API endpoint.

---

## Browser Compatibility

- ✅ Chrome/Edge (clipboard API)
- ✅ Firefox (clipboard fallback)
- ✅ Safari (clipboard fallback)
- ✅ Mobile browsers

---

## Accessibility

- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Focus indicators (visible focus rings)
- ✅ ARIA labels for screen readers
- ✅ WCAG AA contrast ratios (4.5:1 minimum)
- ✅ Touch target sizes (44x44px minimum)

---

## Performance

- Processes up to 100 work efforts by default
- Generation time: < 2 seconds for 100 work efforts
- Efficient file reading with size limits
- Timeout limits on git operations (5 seconds)

---

## Security Notes

All file operations use proven security patterns from the codebase:

- Path validation: `_validate_path_in_storage()` from `src/waft/utils.py`
- Sensitive file detection: `_is_sensitive_file()` from `src/waft/core/html_realm_network_security.py`
- File permissions: 0o600 (files), 0o700 (directories)
- YAML parsing: `yaml.safe_load()` with size limits
- Subprocess: No `shell=True`, uses list arguments only

---

## Examples

### Basic Usage

```bash
/work-efforts
```

Generates dashboard at `_work_efforts/work_dashboard.html` and opens in browser.

### Custom Output

```bash
/work-efforts --output _work_efforts/dashboard_2026-01-18.html
```

Saves to custom location.

### Limited Work Efforts

```bash
/work-efforts --limit 25
```

Processes only the 25 most recent work efforts.

### No Auto-Open

```bash
/work-efforts --no-open
```

Generates dashboard but doesn't open browser automatically.

---

## Integration

This command:
- Uses `scripts/show_me.py` for work effort collection
- Reuses security patterns from `src/waft/utils.py` and `src/waft/core/html_realm_network_security.py`
- Follows YAML parsing patterns from `src/waft/api/services/work_effort_service.py`
- Integrates with existing work effort system

---

## Troubleshooting

**Dashboard doesn't open in browser**:
- Check file path is correct
- Try opening manually: `open _work_efforts/work_dashboard.html` (macOS)
- Use `--no-open` flag and open manually

**No actions generated**:
- Check work effort index files exist
- Verify work effort paths are valid
- Check logs for security validation errors

**Clipboard doesn't work**:
- Check browser permissions for clipboard access
- Use manual copy from command modal
- Try different browser

**Performance issues**:
- Use `--limit` to reduce number of work efforts
- Check for large index files (>1MB)
- Verify git operations aren't timing out

---

## Future Enhancements

- LLM-powered action generation
- Action templates
- Batch actions
- Action history tracking
- Real-time updates (WebSocket)
- Drag & drop reordering
- Filters & search

---

**Work Efforts Dashboard - Intelligent, polymorphic, secure, and beautiful.**
