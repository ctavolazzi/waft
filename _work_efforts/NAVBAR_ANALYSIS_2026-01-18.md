# Navbar Button Analysis

**Date**: 2026-01-18
**Purpose**: Understand what each navigation button does and why it exists

---

## Current Navigation Items

### 1. Dashboard
**What it is**: Main overview/home page
**What it does**: 
- Shows project information (name, version)
- Displays project status cards (Project, Status, Git, Health)
- Shows Work Efforts summary
- Displays Gamification stats
- Shows Pyrite structure
- Shows Gym info
- Shows Bob the Cartographer

**Why it's there**: Central hub for project overview - first thing users see

**Label suggestion**: "Overview" or "Dashboard" (current is fine)

---

### 2. Cognitive Tools
**What it is**: New page we're building
**What it does**:
- Shows status of cognitive tools (Empirica, Sequential Thinking, Work Efforts)
- Displays epistemic state
- Tracks findings and unknowns
- Shows session information

**Why it's there**: Dedicated view for cognitive/epistemic tracking tools

**Label suggestion**: "Cognitive Tools" or "Epistemic Tools" or "Tools"

---

### 3. Git
**What it is**: Git status/information
**What it does**: 
- Shows git branch, status, recent commits
- Part of dashboard cards (GitCard component)

**Why it's there**: Quick access to version control status

**Label suggestion**: "Git" or "Version Control" or "Repository"

**Note**: No dedicated route found - might be part of dashboard only

---

### 4. Work Efforts
**What it is**: Work effort tracking system
**What it does**:
- Lists active work efforts
- Shows work effort status
- Part of dashboard cards (WorkEffortsCard component)

**Why it's there**: Track project tasks and work items

**Label suggestion**: "Work Efforts" or "Tasks" or "Projects"

**Note**: No dedicated route found - might be part of dashboard only

---

### 5. Empirica
**What it is**: Epistemic tracking system
**What it does**:
- Tracks knowledge and learning
- Manages findings and unknowns
- Session management
- Epistemic state assessment

**Why it's there**: Core epistemic intelligence system

**Label suggestion**: "Empirica" or "Knowledge" or "Epistemic"

**Note**: No dedicated route found - might be part of dashboard only

---

### 6. Campfire
**What it is**: Storytelling/story creation system
**What it does**:
- Create stories from text
- Generate PDF booklets
- View story library
- Include Oracle insights in stories

**Why it's there**: Creative/narrative feature for generating story PDFs

**Label suggestion**: "Stories" or "Campfire" or "Narratives"

---

### 7. Refresh
**What it is**: Action button (not a page)
**What it does**:
- Refreshes project data
- Calls `projectStore.fetch()`
- Updates all dashboard cards

**Why it's there**: Manual refresh of project state

**Label suggestion**: "Refresh" or "Reload" or "Update"

---

## Questions to Consider

1. **Do Git, Work Efforts, and Empirica need dedicated pages?**
   - Currently they're just cards on the dashboard
   - Should they have full pages with more detail?

2. **Is the organization logical?**
   - Overview (Dashboard)
   - Tools (Cognitive Tools)
   - Data Views (Git, Work Efforts, Empirica)
   - Creative (Campfire)
   - Action (Refresh)

3. **Should we group related items?**
   - Maybe a dropdown for "Project" (Git, Work Efforts)
   - Maybe a dropdown for "Tools" (Cognitive Tools, Empirica)

4. **What's the user's primary workflow?**
   - Check overview → Use tools → Create stories?
   - Or different?

---

## Recommendations

### Option 1: Keep Flat Structure (Current)
- All items visible
- Simple navigation
- Good for discoverability

### Option 2: Group by Category
- **Project**: Dashboard, Git, Work Efforts
- **Tools**: Cognitive Tools, Empirica
- **Creative**: Campfire
- **Actions**: Refresh

### Option 3: Primary + Secondary
- Primary nav: Dashboard, Cognitive Tools, Campfire
- Secondary nav (dropdown): Git, Work Efforts, Empirica

---

**Next Steps**: Decide on organization, then update labels and remove emojis
