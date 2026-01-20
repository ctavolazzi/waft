# Cognitive Tools Page - Content Plan

**Date**: 2026-01-18
**Purpose**: Define what goes in each box on the cognitive tools page

---

## Box Content Plan

### Header Box
**Purpose**: Page title and description
**Content**:
- Page title: "Cognitive Tools"
- Subtitle: "Epistemic tracking and thinking tools"
- Maybe: Last updated timestamp

---

### Navigation Box
**Purpose**: Already handled by AppShell Navbar
**Content**: 
- Remove this box (duplicate of AppShell navbar)
- Or use for breadcrumbs/page-specific nav

---

### Left Sidebar
**Purpose**: Quick status/controls
**Content**:
- **Session Status**
  - Current Empirica session ID
  - Session active/status indicator
  - Time since last activity
- **Quick Actions**
  - Button: "Initialize Tools" (if not ready)
  - Button: "Create Session"
  - Button: "Refresh All"
- **Tool Availability**
  - Empirica: Available/Not Available
  - Sequential Thinking: Available/Not Available
  - Work Efforts: Available/Not Available

---

### Center Content - Tools Status Section
**Purpose**: Overall status of all cognitive tools
**Content**:
- **Status Grid**
  - Empirica: ✅ Ready / ⚠️ Not Ready
  - Sequential Thinking: ✅ Available / ❌ Not Available
  - Work Efforts: ✅ Active / ❌ Inactive
- **Summary Stats**
  - Active sessions: X
  - Total findings: X
  - Total unknowns: X
  - Active work efforts: X
- **Last Activity**
  - Last finding logged: [timestamp]
  - Last unknown logged: [timestamp]
  - Last session created: [timestamp]

---

### Center Content - Sequential Thinking Section
**Purpose**: Show Sequential Thinking activity
**Content**:
- **Current Thought Chain** (if active)
  - Thought number: X of Y
  - Current thought text
  - Progress indicator
- **Recent Thought Chains**
  - List of recent sequential thinking sessions
  - Each shows: thought count, topic, timestamp
- **Statistics**
  - Total thoughts recorded: X
  - Average thoughts per chain: X
  - Most recent: [timestamp]

**Note**: Sequential Thinking is MCP-based, may need to track via logs or create API endpoint

---

### Center Content - Empirica Section
**Purpose**: Detailed Empirica tracking display
**Content**:
- **Current Session**
  - Session ID
  - Status: Active/Inactive
  - Created: [timestamp]
  - Findings count: X
  - Unknowns count: X
- **Epistemic State**
  - Knowledge coverage: X%
  - Uncertainty: X%
  - Epistemic phase: [phase name]
  - Moon phase indicator: 🌑🌒🌓🌔🌕
- **Recent Activity**
  - Last 5 findings (with impact scores)
  - Last 5 unknowns
  - Goals (if any)
- **Quick Actions**
  - Button: "View Full Session"
  - Button: "Log Finding"
  - Button: "Log Unknown"

---

### Center Content - Work Efforts Section
**Purpose**: Work effort tracking integration
**Content**:
- **Active Work Efforts**
  - List of active work efforts (from `_work_efforts/`)
  - Each shows: ID, title, status, last updated
- **Statistics**
  - Total work efforts: X
  - Active: X
  - Completed: X
  - Paused: X
- **Recent Activity**
  - Last 5 updated work efforts
  - Shows: ID, title, update timestamp
- **Quick Actions**
  - Button: "View All Work Efforts"
  - Button: "Create New Work Effort"

---

### Right Sidebar
**Purpose**: Contextual information and insights
**Content**:
- **Current Context**
  - Project: [name]
  - Working directory: [path]
  - Python version: [version]
- **Epistemic Insights** (from Oracle if available)
  - Current phase recommendation
  - Knowledge gaps highlighted
  - Suggested next actions
- **Tool Integration Status**
  - Which tools are talking to each other
  - Integration health indicators

---

### Footer Box
**Purpose**: Metadata and links
**Content**:
- Last page refresh: [timestamp]
- Data source: API endpoint info
- Links: Documentation, API docs, etc.

---

## Data Sources

### Available APIs:
1. `/api/state` - General project state (includes work_efforts list)
2. `/api/empirica` - Empirica epistemic state
3. `/api/oracle/consult` - Oracle insights (POST)
4. `/api/oracle/health` - Oracle health check

### Need to Create:
1. `/api/cognitive-tools/status` - Combined status of all tools
2. `/api/cognitive-tools/sessions` - List of active sessions
3. `/api/cognitive-tools/sequential-thinking` - Sequential thinking history (if trackable)

---

## Implementation Priority

### Phase 1: Basic Status (Wireframe → Content)
1. Header: Title + subtitle
2. Tools Status: Simple status indicators
3. Empirica: Basic session info + findings/unknowns
4. Work Efforts: List from existing API

### Phase 2: Enhanced Features
1. Sequential Thinking: If we can track it
2. Right Sidebar: Oracle insights
3. Interactive actions: Buttons to log findings, etc.

### Phase 3: Advanced
1. Real-time updates (WebSocket or polling)
2. Charts/graphs for epistemic state
3. Thought chain visualization

---

**Next Step**: Start with Phase 1 - basic content in each box
