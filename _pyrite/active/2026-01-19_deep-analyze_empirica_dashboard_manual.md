# Deep Analysis: Empirica Dashboard Integration + Manual

Date: 2026-01-19

## Relevant WAFT Components
- `src/waft/main.py`: Typer CLI entrypoint and command groups.
- `src/waft/core/empirica.py`: EmpiricaManager for CLI/API integration.
- `src/waft/document_builder.py`: Field guide PDF template builder.
- `src/waft/templates/field_guide.py`: Field guide HTML/CSS layout.

## Empirica Dashboard Components
- `empirica/dashboard/snapshot_monitor.py`: curses-based snapshot monitor.
- `empirica/dashboard/cascade_monitor.py`: CASCADE monitor for tmux.
- `empirica/tui/dashboard.py`: Textual-based TUI dashboard.
- `empirica/dashboard/README.md`: Usage and interaction reference.

## Integration Implications
- The manual should describe all three dashboards and the `waft empirica monitor` CLI entrypoint.
- The field guide template is the best fit for a procedural manual.
- Dependencies to highlight: `empirica`, `textual`, `windows-curses` (Windows).

## Manual Content Requirements
- Quick start and command examples.
- Dashboard type comparison table.
- Troubleshooting section with common error resolutions.
