= Work Effort Integration

This chapter explores how the dashboard integrates with WAFT's work efforts system for tracking active work and progress.

== Work Efforts System

WAFT uses a Johnny Decimal system for organizing work efforts:
- Structure: `XX-XX_category/XX_subcategory/XX.XX_document.md`
- Categories: 00-09 (meta), 10-19 (development), 20-29 (features), etc.
- Index files: Each subcategory has `00.00_index.md`

== Work Effort Discovery

=== Directory Scanning

The dashboard scans `_work_efforts/` for:
1. Work effort directories: `WE-YYMMDD-xxxx_*`
2. Index files: `*_index.md`
3. Status files: `status.json` (if exists)
4. Recent activity: Modified timestamps

=== Work Effort Metadata

Each work effort has:
- **ID**: `WE-YYMMDD-xxxx` format
- **Title**: From directory name or index
- **Status**: active, paused, completed
- **Progress**: From status file or index
- **Last Updated**: File modification time
- **Path**: Directory path

== Work Effort Display

=== Work Effort Tracker Component

Displays work efforts in a list:
- Work effort ID and title
- Status badge (active/paused/completed)
- Progress indicator
- Last updated timestamp
- Link to work effort details

=== Status Indicators

- 🟢 **Active**: Currently in progress
- 🟡 **Paused**: Temporarily stopped
- 🔵 **Completed**: Finished
- ⚪ **Unknown**: Status not determined

== Work Effort Actions

=== View Details
- Open work effort index file
- Navigate to work effort directory
- View related documents

=== Update Status
- Mark as active/paused/completed
- Update progress notes
- Add timestamps

=== Create New
- Initialize new work effort
- Create directory structure
- Generate index file

== Integration Points

Work effort integration connects with:
- File system scanning
- Johnny Decimal system
- Devlog updates
- Status tracking
- Progress monitoring

== Future Enhancements

- Work effort search
- Work effort filtering
- Work effort templates
- Work effort analytics
- Work effort dependencies
