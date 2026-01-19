= Status Monitoring

This chapter explores how the dashboard monitors and displays system status, project health, and recent activity.

== System Status Components

=== Project Overview
- Project name and path
- Git repository status
- Branch information
- Commit status

=== Git Status
- Modified files count
- Untracked files count
- Staged changes
- Branch ahead/behind status

=== System Health
- Disk usage
- File system status
- Recent errors/warnings
- System metrics

== Status Data Sources

=== WAFT Info Command
- Project information
- System configuration
- Available commands
- Template status

=== Git Commands
- `git status` - Working directory status
- `git branch` - Branch information
- `git log` - Recent commits

=== File System Scanning
- Directory structure
- File counts
- Modification times
- Size information

== Status Display

=== Status Dashboard Component

Real-time status display:
- Project overview card
- Git status indicators
- System health badges
- Refresh button

=== Status Indicators

- ✅ **Healthy**: All systems normal
- ⚠️ **Warning**: Minor issues detected
- ❌ **Error**: Critical issues found
- 🔄 **Refreshing**: Status update in progress

== Status Updates

=== Refresh Mechanism
- Manual refresh button
- Automatic periodic refresh (optional)
- Event-driven updates
- On-demand status checks

=== Update Frequency
- Real-time for critical status
- Periodic for general status
- On-demand for detailed status
- Cached for performance

== Integration

Status monitoring integrates with:
- WAFT command system
- Git integration
- File system scanning
- Work efforts system
- Error tracking

== Future Enhancements

- Status history
- Status alerts
- Status notifications
- Status dashboards
- Status analytics
