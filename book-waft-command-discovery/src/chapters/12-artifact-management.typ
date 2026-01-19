= Artifact Management

This chapter explores how the dashboard manages and displays generated artifacts (PDFs, HTML files, reports, etc.).

== Artifact Types

=== PDF Documents
- Checkpoints: `CHECKPOINT_*.md` → PDF
- Dossiers: `Mission Sitrep Dossier - *.pdf`
- One-pagers: `_work_efforts/one_pagers/*.pdf`
- Worldbuilding: `_work_efforts/worldbuild/*.pdf`
- Stories: `_work_efforts/stories/*.pdf`

=== HTML Reports
- Show-me reports: `session_overview_*.html`
- Visualize dashboards: `visualize-*.html`
- Evolution wireframes: `*.html`

=== Markdown Documents
- Work efforts: `_work_efforts/WE-*/`
- Checkpoints: `CHECKPOINT_*.md`
- Design docs: `UI_DESIGN_DOC_*.md`
- Technical requirements: `UI_TECHNICAL_REQUIREMENTS_*.md`

== Artifact Discovery

=== Scanning Strategy

The dashboard scans multiple directories:
1. `_work_efforts/` - Main work artifacts
2. `_pyrite/.waft/` - System-generated files
3. `_genetics/` - Evolution outputs
4. `_science/` - Scientific method results

=== File Metadata Extraction

For each artifact:
- **Path**: Full file path
- **Name**: Filename
- **Type**: PDF, HTML, Markdown, etc.
- **Size**: File size in bytes
- **Modified**: Last modification time
- **Category**: Based on directory/pattern

== Artifact Display

=== Document Gallery Component

Displays artifacts in a grid:
- Thumbnail/preview (if available)
- File name
- File type badge
- Size and date
- Open/view buttons

=== Filtering Options

- By type (PDF, HTML, Markdown)
- By date (today, week, month, all)
- By category (checkpoint, dossier, report)
- By size

== Artifact Actions

=== View/Open
- PDFs: Open in system PDF viewer
- HTML: Open in browser
- Markdown: Open in editor

=== Preview
- Generate thumbnails
- Show file metadata
- Display file contents (for text files)

=== Delete
- Remove artifact files
- Clean up directories
- Update registry

== Integration

Artifact management integrates with:
- File system scanning
- Work efforts system
- Document generation commands
- Session history tracking

== Future Enhancements

- Artifact tagging
- Artifact search
- Artifact collections
- Artifact sharing
- Artifact versioning
