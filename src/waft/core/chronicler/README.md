# TheChronicler: Self-Monitoring System

TheChronicler is WAFT's self-awareness system. It observes, records, and reports on all activity within the system, monitoring the genesis (creation) and exodus (deletion) of all components.

## Architecture

### Core Components

1. **TheChronicler** (`chronicler.py`): Main orchestrator
   - Manages all observers
   - Coordinates report generation
   - Integrates with Oracle

2. **Observers** (`observers.py`):
   - **FileSystemObserver**: Watches file creation, modification, deletion (watchdog)
   - **GitObserver**: Monitors git commits and status changes
   - **WorkEffortObserver**: Tracks work effort and ticket lifecycle

3. **Storage** (`storage.py`):
   - Daily observation folders
   - JSONL format for efficient storage
   - Hourly file organization

4. **Reports** (`reports.py`):
   - Hourly reports (on the hour)
   - Daily reports (5 AM reset cycle)
   - PDF generation using Brief system

5. **Scheduler** (`scheduler.py`):
   - Hourly report triggers
   - Daily reset at 5 AM
   - Thread-safe scheduling

## Usage

### Start Monitoring

```bash
waft chronicler
```

Starts continuous monitoring. Press Ctrl+C to stop.

### View Statistics

```bash
waft chronicler-stats
```

Shows current day's statistics:
- Genesis count (creations)
- Exodus count (deletions)
- Net change
- Observer status

### Generate Reports Manually

```bash
# Generate hourly report for current hour
waft chronicler-report --hourly

# Generate daily report for today
waft chronicler-report --daily
```

## Storage Structure

```
_chronicler/
├── observations/
│   └── YYYY-MM-DD/
│       ├── observations_00.jsonl
│       ├── observations_01.jsonl
│       └── ...
└── reports/
    ├── hourly_YYYYMMDD_HH00.pdf
    └── daily_YYYYMMDD.pdf
```

## Observation Format

Each observation is stored as a JSON line:

```json
{
  "event_type": "genesis|exodus|mutation",
  "observer": "filesystem|git|work_effort",
  "path": "relative/path/to/file",
  "timestamp": "2026-01-13T07:41:24.123456",
  "metadata": {...}
}
```

## Report Schedule

- **Hourly Reports**: Generated automatically on the hour (00:00, 01:00, ..., 23:00)
- **Daily Reports**: Generated at 5 AM (reset cycle)
- **Reset Hour**: Configurable (default: 5 AM)

## Oracle Integration

Significant observations are automatically logged to Oracle:
- Work effort changes
- Git commits
- Major file changes in `src/`, `_work_efforts/`, `scripts/`

## Design Principles

- **Clean Code**: DRY, no spaghetti, thoughtful design
- **Separation of Concerns**: Each component has single responsibility
- **Thread-Safe**: All observers run in separate threads
- **Non-Blocking**: Observations don't block main operations
- **Extensible**: Easy to add new observers

## Future Enhancements

- Real-time dashboard
- Alert system for significant changes
- Integration with more system components
- Historical trend analysis
- Custom observation filters
