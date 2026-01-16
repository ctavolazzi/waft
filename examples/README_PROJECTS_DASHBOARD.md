# Projects Dashboard

A visual web-based dashboard for viewing and managing WAFT projects.

## Usage

Open the dashboard in your browser:

```bash
open examples/projects_dashboard.html
```

Or double-click the file in Finder.

## Features

- **Visual Project Cards**: See all projects at a glance
- **Progress Bars**: Visual progress indicators
- **Statistics**: Total projects, active projects, average progress
- **Milestone Tracking**: View milestone completion status
- **Project Details**: Click any project card to see full details
- **Auto-refresh**: Updates every 30 seconds

## Integration with WAFT CLI

Currently displays mock data. To integrate with actual WAFT Projects Feature:

1. Run `waft project list --format json` to get project data
2. Parse JSON output in JavaScript
3. Update the `loadProjects()` function to use real data

## Future Enhancements

- Create/edit projects from the dashboard
- Real-time updates via WebSocket
- Filter and search functionality
- Export project data
- Milestone management interface
