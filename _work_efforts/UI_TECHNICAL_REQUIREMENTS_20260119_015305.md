# Technical Requirements - WAFT Command Dashboard

**Date**: 2026-01-19 01:55:00 PST
**Based On**: `UI_DESIGN_DOC_20260119_015305.md` (Verified)
**Status**: Draft

---

## Overview

This document breaks down the design document into implementable technical specifications for the WAFT Command Dashboard UI.

---

## Components Needed

### 1. Command Launcher Component

#### HTML Structure
```html
<section id="command-launcher" class="dashboard-section">
  <header>
    <h2>Commands</h2>
    <input type="search" id="command-search" placeholder="Search commands...">
  </header>
  <div id="command-grid" class="command-grid">
    <!-- Command cards will be inserted here -->
  </div>
</section>
```

#### Command Card Structure
```html
<article class="command-card" data-category="documentation">
  <header class="command-header">
    <h3 class="command-name">/checkpoint</h3>
    <span class="command-category">Documentation</span>
  </header>
  <p class="command-description">Create checkpoint document...</p>
  <div class="command-usage">
    <code>/checkpoint</code>
  </div>
  <div class="command-actions">
    <button class="btn-execute">Execute</button>
    <button class="btn-docs">Docs</button>
  </div>
</article>
```

#### Data Source
- WAFT command registry
- `.cursor/commands/*.md` files
- Parse command documentation for descriptions

#### Functionality
- Display all commands in grid
- Search/filter by name or category
- Category filtering
- Execute command (opens modal or runs directly)
- Link to documentation

---

### 2. Status Dashboard Component

#### HTML Structure
```html
<section id="status-dashboard" class="dashboard-section">
  <header>
    <h2>Status</h2>
    <button id="refresh-status">Refresh</button>
  </header>
  <div class="status-grid">
    <div class="status-card" id="project-overview">
      <!-- Project info -->
    </div>
    <div class="status-card" id="git-status">
      <!-- Git info -->
    </div>
    <div class="status-card" id="system-health">
      <!-- System health -->
    </div>
  </div>
</section>
```

#### Data Source
- `waft info` command output
- `git status` command output
- File system scanning
- Work efforts directory

#### Functionality
- Display project name, version, path
- Show git branch, uncommitted files
- Display system health indicators
- Refresh button to update status

---

### 3. Document Gallery Component

#### HTML Structure
```html
<section id="document-gallery" class="dashboard-section">
  <header>
    <h2>Recent Documents</h2>
    <div class="gallery-filters">
      <select id="doc-type-filter">
        <option value="all">All Types</option>
        <option value="pdf">PDF</option>
        <option value="html">HTML</option>
        <option value="md">Markdown</option>
      </select>
    </div>
  </header>
  <div id="document-list" class="document-list">
    <!-- Document cards -->
  </div>
</section>
```

#### Document Card Structure
```html
<article class="document-card" data-type="pdf">
  <div class="doc-icon">📄</div>
  <div class="doc-info">
    <h4 class="doc-name">Mission Sitrep Dossier.pdf</h4>
    <p class="doc-path">_work_efforts/briefs/</p>
    <p class="doc-date">2026-01-19 01:48</p>
  </div>
  <div class="doc-actions">
    <button class="btn-open">Open</button>
    <button class="btn-preview">Preview</button>
  </div>
</article>
```

#### Data Source
- Scan `_work_efforts/` for PDFs
- Scan `_work_efforts/` for HTML files
- Scan `_pyrite/.waft/` for visualizations
- Scan `_genetics/` for evolution outputs
- Sort by modification time (most recent first)

#### Functionality
- List recently generated files
- Filter by file type
- Open files (system default)
- Preview (for HTML, show in iframe)
- Show file metadata (size, date, path)

---

### 4. Work Effort Tracker Component

#### HTML Structure
```html
<section id="work-effort-tracker" class="dashboard-section">
  <header>
    <h2>Active Work</h2>
    <span class="work-count" id="active-work-count">0</span>
  </header>
  <div id="work-effort-list" class="work-effort-list">
    <!-- Work effort cards -->
  </div>
</section>
```

#### Work Effort Card Structure
```html
<article class="work-effort-card" data-status="active">
  <header class="we-header">
    <h4 class="we-id">WE-260119-xxxx</h4>
    <span class="we-status-badge status-active">Active</span>
  </header>
  <h5 class="we-title">Work Effort Title</h5>
  <div class="we-progress">
    <div class="progress-bar">
      <div class="progress-fill" style="width: 65%"></div>
    </div>
    <span class="progress-text">65%</span>
  </div>
  <div class="we-actions">
    <a href="..." class="btn-view">View</a>
  </div>
</article>
```

#### Data Source
- Scan `_work_efforts/WE-*/` directories
- Read `*_index.md` files
- Extract status from frontmatter
- Calculate progress (if available)

#### Functionality
- List active work efforts
- Show status badges
- Display progress bars
- Link to work effort details
- Filter by status

---

### 5. Session History Component

#### HTML Structure
```html
<section id="session-history" class="dashboard-section">
  <header>
    <h2>Recent Activity</h2>
  </header>
  <div id="activity-list" class="activity-list">
    <!-- Activity items -->
  </div>
</section>
```

#### Activity Item Structure
```html
<article class="activity-item">
  <div class="activity-icon">✅</div>
  <div class="activity-content">
    <p class="activity-action">Executed: /checkpoint</p>
    <p class="activity-time">2026-01-19 01:45:00</p>
    <p class="activity-result">Created: CHECKPOINT_2026-01-19_dnd_campaign_integration.md</p>
  </div>
</article>
```

#### Data Source
- Recent command executions (if logged)
- Generated file timestamps
- Work effort updates
- Git commits

#### Functionality
- List recent commands executed
- Show timestamps
- Display results/artifacts
- Link to generated files
- Limit to last 20 items

---

### 6. Tool Integration Component

#### HTML Structure
```html
<section id="tool-integration" class="dashboard-section">
  <header>
    <h2>Tools</h2>
  </header>
  <div id="tool-grid" class="tool-grid">
    <!-- Tool cards -->
  </div>
</section>
```

#### Tool Card Structure
```html
<article class="tool-card">
  <div class="tool-icon">🔬</div>
  <h4 class="tool-name">Science-Bitch</h4>
  <p class="tool-description">Scientific method workflow</p>
  <button class="btn-launch">Launch</button>
</article>
```

#### Data Source
- Hardcoded tool list
- Tool descriptions
- Tool entry points

#### Functionality
- Display available tools
- Launch tools
- Link to tool interfaces

---

## Layout Structure

### HTML Boilerplate
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WAFT Command Dashboard</title>
  <link rel="stylesheet" href="dashboard.css">
</head>
<body>
  <header id="main-header">
    <!-- Header content -->
  </header>
  <main id="main-content">
    <div class="dashboard-grid">
      <section id="command-launcher" class="col-left">
        <!-- Command launcher -->
      </section>
      <section id="status-dashboard" class="col-middle">
        <!-- Status dashboard -->
      </section>
      <section id="document-gallery" class="col-middle">
        <!-- Document gallery -->
      </section>
      <section id="work-effort-tracker" class="col-right">
        <!-- Work effort tracker -->
      </section>
      <section id="session-history" class="col-right">
        <!-- Session history -->
      </section>
    </div>
  </main>
  <footer id="main-footer">
    <!-- Footer content -->
  </footer>
  <script src="dashboard.js"></script>
</body>
</html>
```

### CSS Grid Layout
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
}

.col-left {
  grid-column: 1;
}

.col-middle {
  grid-column: 2;
}

.col-right {
  grid-column: 3;
}
```

---

## Data Collection

### Command Registry
- Scan `.cursor/commands/*.md` files
- Parse command documentation
- Extract: name, description, usage, options
- Categorize commands

### File System Scanning
- Scan `_work_efforts/` for documents
- Scan `_pyrite/.waft/` for visualizations
- Scan `_genetics/` for evolution outputs
- Get file metadata (size, date, type)

### Git Status
- Run `git status --porcelain`
- Run `git branch --show-current`
- Run `git log --oneline -5`
- Parse output

### Work Efforts
- Scan `_work_efforts/WE-*/` directories
- Read index files
- Extract status, title, progress

---

## JavaScript Functionality

### Command Execution
```javascript
function executeCommand(command, options) {
  // Show execution modal
  // Run command via backend or display instructions
  // Show results
  // Update activity history
}
```

### File Opening
```javascript
function openFile(filePath) {
  // Open file using system default
  // Handle different file types
  // Show preview for HTML
}
```

### Data Refresh
```javascript
function refreshData() {
  // Reload command list
  // Update status
  // Refresh document gallery
  // Update work efforts
}
```

### Search/Filter
```javascript
function filterCommands(query) {
  // Filter command cards
  // Update display
  // Highlight matches
}
```

---

## Styling Requirements

### Color Scheme
- Background: `#1a1a1a` (dark)
- Text: `#d5d5d5` (light gray)
- Accent: `#4a9eff` (blue)
- Success: `#4caf50` (green)
- Warning: `#ff9800` (orange)
- Error: `#f44336` (red)

### Typography
- Headings: System font stack, 600 weight
- Body: System font stack, 400 weight
- Code: Monospace font
- Sizes: Responsive, clamp() for fluid scaling

### Components
- Cards: Rounded corners, subtle shadow, padding
- Buttons: Rounded, hover effects, clear states
- Badges: Pill-shaped, color-coded
- Progress bars: Animated, color-coded

---

## Performance Requirements

### Initial Load
- Load time: < 2 seconds
- Render time: < 500ms
- Data collection: < 1 second

### File Scanning
- Limit to recent files (last 30 days)
- Cache command list
- Lazy load document previews

### Updates
- Refresh on demand (button)
- Auto-refresh optional (every 5 minutes)
- Efficient DOM updates

---

## Browser Compatibility

### Supported Browsers
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

### Features Used
- CSS Grid
- CSS Variables
- Fetch API
- ES6+ JavaScript

---

## File Structure

```
[project_root]/
├── index.html              # Main dashboard file
├── dashboard.css           # Styles
├── dashboard.js            # JavaScript
└── _work_efforts/
    └── [design docs, requirements, etc.]
```

---

## Implementation Order

1. HTML boilerplate
2. CSS grid layout
3. Header component
4. Command launcher (basic structure)
5. Status dashboard (basic structure)
6. Document gallery (basic structure)
7. Work effort tracker (basic structure)
8. Session history (basic structure)
9. Footer component
10. JavaScript data collection
11. JavaScript interactivity
12. Styling and polish

---

**Next Step**: Create wireframe HTML structure
