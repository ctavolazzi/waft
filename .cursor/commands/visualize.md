# Visualize

**Create a quick interactive browser UI to visualize current state and get visual insight.**

Generates a standalone HTML dashboard that opens in your browser, showing current project state, git status, active work, and more with interactive visualizations. Perfect for getting immediate visual insight into what's happening.

**Use when:** You need visual insight into current state, want to see what's happening at a glance, or need an interactive view of project status.

---

## Purpose

This command provides:
- **Quick Visual Dashboard**: Standalone HTML file that opens in browser
- **Current State Visualization**: Git status, active work, project health
- **Interactive Elements**: Clickable sections, expandable details
- **Real-time Data**: Shows current state when generated
- **No Server Required**: Standalone file, works offline
- **Auto-Open**: Automatically opens in your default browser

---

## Philosophy

1. **Immediate Insight**: Get visual understanding quickly
2. **Standalone**: No server needed, just open the HTML file
3. **Interactive**: Click, expand, explore the data
4. **Current State**: Shows what's happening right now
5. **Visual First**: Charts, graphs, color coding, status indicators

---

## What Gets Visualized

### 1. Project Overview
- Project name and version
- Project path
- Framework status (waft integrity, level, insight)
- Last updated timestamp

### 2. Git Status
- Current branch
- Uncommitted files (count and list)
- Commits ahead/behind
- Recent commit history (last 5)
- File changes breakdown (added, modified, deleted, untracked)

### 3. Active Work
- Active work efforts (count and list)
- Recent work effort activity
- Pending todos (if any)
- Recent devlog entries

### 4. Project Structure
- _pyrite structure status
- Files in active/, backlog/, standards/
- Template status
- Dependencies status

### 5. System Status
- Current date/time
- Working directory
- Disk space (if available)
- Python version

### 6. Visual Indicators
- Color-coded status badges
- Progress bars
- Charts/graphs where useful
- Interactive expandable sections

---

## Execution Steps

1. **Gather Current State**
   - Run git status
   - Check project health (waft verify/info)
   - List active work efforts
   - Get recent devlog entries
   - Check system status

2. **Generate HTML Dashboard**
   - Create standalone HTML file
   - Include all data inline (no external dependencies)
   - Add interactive JavaScript
   - Style with CSS (modern, dark mode)

3. **Open in Browser**
   - Automatically open generated HTML file
   - Use system default browser
   - Show file path for reference

4. **Optional: Serve Mode**
   - If requested, start a simple server
   - Auto-refresh capability
   - Live updates

---

## Output Format

### Standalone HTML File

The command generates a single HTML file (e.g., `_pyrite/.waft/visualize-YYYY-MM-DD-HHMMSS.html`) that includes:

- **All data inline** - No external API calls needed
- **Self-contained** - Works offline, no server required
- **Interactive** - JavaScript for expand/collapse, filtering
- **Styled** - Modern dark mode theme, responsive design
- **Visual** - Charts, graphs, color coding, status indicators

### Visual Elements

1. **Status Cards**
   - Color-coded status badges
   - Progress indicators
   - Quick stats

2. **Interactive Lists**
   - Expandable file lists
   - Filterable work efforts
   - Sortable tables

3. **Charts/Graphs** (where applicable)
   - File type breakdown
   - Work effort timeline
   - Git activity

4. **Color Coding**
   - Green: Good/Complete
   - Yellow: Warning/In Progress
   - Red: Error/Blocked
   - Blue: Info/Neutral

---

## Use Cases

### 1. Quick Status Check
**Scenario**: Want to see current state at a glance

**Example**:
```
User: "/visualize"
```

**Output**: HTML dashboard opens showing all current state

---

### 2. Git Status Visualization
**Scenario**: Need to see what files changed, commits, etc.

**Example**:
```
User: "Show me git status visually /visualize"
```

**Output**: Dashboard with detailed git visualization

---

### 3. Work Effort Overview
**Scenario**: Want to see all active work visually

**Example**:
```
User: "/visualize"
```

**Output**: Dashboard showing active work efforts, progress, status

---

### 4. Project Health Check
**Scenario**: Quick visual health check

**Example**:
```
User: "/visualize"
```

**Output**: Dashboard with project health indicators, integrity, level

---

### 5. Handoff Documentation
**Scenario**: Create visual snapshot for handoff

**Example**:
```
User: "/visualize"
```

**Output**: Standalone HTML file that can be shared or archived

---

## Options

### Standalone Mode (Default)
```bash
/visualize
```
- Generates HTML file
- Opens in browser
- No server needed
- Works offline

### Serve Mode (Optional)
```bash
/visualize --serve
```
- Generates HTML file
- Starts simple HTTP server
- Auto-refresh capability
- Live updates (if implemented)

### Custom Output Path
```bash
/visualize --output /path/to/file.html
```
- Specify custom output location
- Useful for sharing or archiving

---

## Visual Features

### Interactive Elements

1. **Expandable Sections**
   - Click to expand/collapse details
   - Show/hide file lists
   - Toggle work effort details

2. **Filterable Lists**
   - Filter files by type
   - Search work efforts
   - Filter git changes

3. **Sortable Tables**
   - Sort by date, name, status
   - Multiple sort criteria
   - Visual sort indicators

4. **Color-Coded Status**
   - Status badges with colors
   - Progress bars
   - Health indicators

### Charts and Graphs

1. **File Type Breakdown**
   - Pie chart of file types
   - Bar chart of file counts
   - Visual file tree

2. **Work Effort Timeline**
   - Timeline of work efforts
   - Status progression
   - Activity heatmap

3. **Git Activity**
   - Commit timeline
   - File change trends
   - Branch visualization

---

## Integration with Other Commands

- **`/status`**: Quick text status (complements `/visualize`)
- **`/checkpoint`**: Creates checkpoint (may inform visualization)
- **`/verify`**: Verifies state (data used in visualization)
- **`/explore`**: Deep exploration (may inform visualization)

---

## When to Use

**Use `/visualize` when**:
- ✅ Need visual insight into current state
- ✅ Want to see what's happening at a glance
- ✅ Need interactive exploration of data
- ✅ Want to share visual snapshot
- ✅ Need quick status overview
- ✅ Want to see relationships between data

**Don't use `/visualize` when**:
- ❌ Need detailed text output (use `/status`)
- ❌ Need to modify data (use other commands)
- ❌ Need real-time updates (use `waft serve` for live dashboard)
- ❌ Just need quick one-liner (use `/status`)

---

## Technical Details

### HTML Generation

- **Self-contained**: All CSS and JavaScript inline
- **No dependencies**: Works offline, no CDN required
- **Modern**: Uses modern CSS (Grid, Flexbox, CSS Variables)
- **Responsive**: Works on desktop and mobile
- **Accessible**: Semantic HTML, ARIA labels

### Data Collection

- **Git status**: `git status`, `git log`, `git diff --stat`
- **Project info**: `waft info`, `waft verify`
- **Work efforts**: List from `_work_efforts/`
- **Devlog**: Recent entries from `devlog.md`
- **System**: Date, working directory, Python version

### Browser Opening

- Uses system default browser
- Cross-platform (macOS, Linux, Windows)
- Handles errors gracefully (shows file path if open fails)

---

## Example Output

When you run `/visualize`, you'll see:

```
🌊 Generating visual dashboard...

📊 Gathering current state...
  ✓ Git status collected
  ✓ Project info gathered
  ✓ Work efforts listed
  ✓ Devlog entries loaded

📄 Generating HTML dashboard...
  ✓ Dashboard created: _pyrite/.waft/visualize-2026-01-07-201530.html

🌐 Opening in browser...
  ✓ Dashboard opened in default browser

💡 Tip: The dashboard is standalone - you can share or archive the HTML file
```

Then your browser opens showing:
- Project overview card
- Git status with file breakdown
- Active work efforts list
- Project structure visualization
- System status
- All interactive and color-coded

---

## Advanced Features

### Auto-Refresh (Serve Mode)
If using `--serve` flag:
- Dashboard auto-refreshes every 5 seconds
- Shows "Last updated" timestamp
- Live data updates

### Export Options
- Save as PDF (browser print)
- Share HTML file
- Archive for historical reference

### Customization
- Filter what's shown
- Customize colors
- Adjust layout

---

**This command gives you immediate visual insight into your project's current state with an interactive, standalone dashboard.**
