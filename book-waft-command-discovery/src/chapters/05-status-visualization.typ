= Status & Visualization

WAFT provides powerful commands for viewing system status and project state through comprehensive reports and interactive dashboards.

== The `/show-me` Command

Displays a comprehensive overview of everything relevant happening in the current chat session.

=== Purpose

Shows:
- Work Efforts (current and recent)
- LaTeX Templates (available templates)
- Librarian Catalog (cataloged records)
- Recent Experiments (scientific method)
- Chat Context (key concepts)
- Proof Cases (verification results)

=== Output Format

Default: HTML report with:
- WAFT-branded styling
- Integrated PDF conversion
- Print-optimized CSS
- Responsive design
- Semantic HTML

=== Usage

```bash
/show-me --format html --output overview.html
/show-me --format pdf --output overview.pdf
```

== The `/visualize` Command

Creates a quick interactive browser UI to visualize current state and get visual insight.

=== Purpose

Generates standalone HTML dashboard showing:
- Project overview
- Git status
- Active work efforts
- Project structure
- System status
- Visual indicators

=== Features

- Standalone HTML (no server needed)
- Interactive elements (expandable sections)
- Color-coded status badges
- Real-time data from current state
- Responsive design

=== Output

Saves to: `_pyrite/.waft/visualize-YYYY-MM-DD-HHMMSS.html`

Automatically opens in browser for immediate viewing.

== Comparison

*Show-Me*:
- Focus: Comprehensive session overview
- Format: HTML/PDF report
- Scope: All session data
- Use: Complete status snapshot

*Visualize*:
- Focus: Interactive dashboard
- Format: Standalone HTML
- Scope: Current state visualization
- Use: Quick visual insight

== Integration

Both commands integrate with:
- Work efforts system
- Git status
- Project health monitoring
- Recent activity tracking
- System metrics

== Key Takeaways

- Multiple ways to view project state
- Visual dashboards provide immediate insight
- Reports provide comprehensive documentation
- Both serve different but complementary purposes
