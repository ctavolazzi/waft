---
name: Daily Learning Report Server
overview: Create a background server that collects data throughout the day from Empirica, TheChronicler, and SessionAnalytics, then automatically generates a Typst PDF report at a configurable trigger time (3 seconds for dev testing, 9 PM for production) summarizing both learnings and activity.
todos: []
isProject: false
---

# Daily Learning Report Server

## Overview

A background server that runs in an iTerm window, continuously collects work data throughout the day, and automatically generates a Typst PDF report at a configurable trigger time (3 seconds for dev testing, 9 PM for production) summarizing what was learned and what was done.

## Architecture

```
DailyLearningServer (main daemon)
├── DataCollector (aggregates from multiple sources)
│   ├── EmpiricaCollector (findings, unknowns, epistemic state)
│   ├── ChroniclerCollector (file changes, git activity, work efforts)
│   └── SessionAnalyticsCollector (session metrics, commits, commands)
├── Scheduler (configurable trigger time - 3 seconds for dev, 9 PM for production)
└── ReportGenerator (Typst PDF generation)
```

## Components

### 1. Daily Learning Server (`src/waft/core/daily_learning_server.py`)

**Main daemon class** that:

- Runs continuously in background
- Coordinates data collection from all sources
- Manages scheduler for 9 PM trigger
- Handles graceful shutdown
- Provides status endpoint/logging

**Key methods:**

- `start()` - Start the server loop
- `stop()` - Graceful shutdown
- `collect_daily_data()` - Aggregate all data sources
- `generate_report()` - Trigger PDF generation

### 2. Data Collectors

#### EmpiricaCollector (`src/waft/core/daily_learning/empirica_collector.py`)

- Retrieves findings logged today (via `empirica finding-log`)
- Retrieves unknowns logged today (via `empirica unknown-log`)
- Gets epistemic state summary (know, uncertainty, engagement)
- Extracts session summaries if available

#### ChroniclerCollector (`src/waft/core/daily_learning/chronicler_collector.py`)

- Gets file system observations from TheChronicler storage
- Retrieves git activity (commits, branches, status)
- Collects work effort changes (created/updated tickets)
- Aggregates hourly activity summaries

#### SessionAnalyticsCollector (`src/waft/core/daily_learning/session_collector.py`)

- Queries SessionAnalytics database for today's sessions
- Aggregates file metrics (created/modified/deleted)
- Collects code metrics (lines written/modified)
- Gets command execution summaries

### 3. Report Generator (`src/waft/core/daily_learning/report_generator.py`)

**Typst-based PDF generator** that:

- Takes aggregated data from all collectors
- Generates Typst source with structured sections:
  - **What I Learned** (Empirica findings, insights, patterns)
  - **What I Did** (file changes, commits, work efforts, commands)
  - **Epistemic State** (knowledge growth, uncertainty reduction)
  - **Activity Summary** (metrics, charts if possible)
- Compiles Typst to PDF using existing TypstCompiler
- Saves to `_pyrite/daily_reports/YYYY-MM-DD_learning_report.pdf`

### 4. CLI Command (`src/waft/cli/daily_learning_cli.py`)

**New CLI command:**

```bash
waft daily-learning-server [--port PORT] [--log-level LEVEL]
```

**Options:**

- `--port`: HTTP status port (optional, for health checks)
- `--log-level`: Logging level (default: INFO)
- `--trigger-time`: Override trigger time (default: 3 seconds for dev, 9 PM for production)
- `--dev-mode`: Enable dev mode (triggers in 3 seconds, default: True during development)

**Behavior:**

- Starts background server
- Logs to console (for iTerm window)
- Runs until interrupted (Ctrl+C)
- On trigger time, generates report and logs completion
- **Dev mode**: Triggers immediately (3 seconds) for testing
- **Production mode**: Triggers at 9 PM daily

### 5. Typst Template (`src/waft/templates/typst/daily_learning_report.typ`)

**Professional Typst template** with:

- Title page with date
- Table of contents
- **Section 1: What I Learned**
  - Findings (with impact scores)
  - Insights and patterns
  - Knowledge gaps (unknowns)
- **Section 2: What I Did**
  - File activity summary
  - Git commits
  - Work efforts created/updated
  - Commands executed
- **Section 3: Epistemic State**
  - Knowledge growth metrics
  - Uncertainty reduction
  - Engagement levels
- **Section 4: Activity Metrics**
  - Files created/modified/deleted
  - Lines of code written
  - Time spent (if available)

## Integration Points

### Existing Systems

1. **Empirica Integration**

   - Use `EmpiricaAPIManager` from `src/waft/core/empirica_api.py`
   - Query findings/unknowns via Empirica CLI or API
   - Get session summaries

2. **TheChronicler Integration**

   - Use `ObservationStorage` from `src/waft/core/chronicler/storage.py`
   - Query observations for today's date
   - Reuse existing report aggregation logic

3. **SessionAnalytics Integration**

   - Use `SessionAnalytics` from `src/waft/core/session_analytics.py`
   - Query SQLite database for today's sessions
   - Aggregate metrics

4. **Typst Integration**

   - Use `TypstCompiler` from `src/waft/templates/typst/compiler.py`
   - Follow existing Typst template patterns
   - Reuse compilation logic

## File Structure

```
src/waft/
├── core/
│   ├── daily_learning_server.py          # Main server daemon
│   └── daily_learning/
│       ├── __init__.py
│       ├── collectors.py                 # Base collector interface
│       ├── empirica_collector.py         # Empirica data collection
│       ├── chronicler_collector.py       # TheChronicler data collection
│       ├── session_collector.py          # SessionAnalytics collection
│       ├── report_generator.py           # Typst PDF generation
│       └── scheduler.py                  # 9 PM trigger scheduler
├── cli/
│   └── daily_learning_cli.py             # CLI command
└── templates/
    └── typst/
        └── daily_learning_report.typ     # Typst template
```

## Data Flow

```
[Server starts]
    ↓
[Dev Mode: 3 seconds] OR [Production: 9:00 PM]
    ↓
[Throughout Day/Period] Collectors gather data
    ├── Empirica: Logs findings/unknowns
    ├── TheChronicler: Observes file/git changes
    └── SessionAnalytics: Tracks session metrics
    ↓
[Trigger Time] Scheduler triggers
    ↓
[Report Generation]
    ├── Aggregate all collected data
    ├── Generate Typst source
    ├── Compile to PDF
    └── Save to _pyrite/daily_reports/
    ↓
[Log completion] Report ready at: path/to/report.pdf
```

## Implementation Steps

1. **Create data collector interfaces** - Base classes for collectors
2. **Implement EmpiricaCollector** - Query Empirica for findings/unknowns
3. **Implement ChroniclerCollector** - Query TheChronicler observations
4. **Implement SessionAnalyticsCollector** - Query session database
5. **Create Typst template** - Design daily learning report template
6. **Implement ReportGenerator** - Aggregate data and generate Typst
7. **Create scheduler** - Configurable trigger time (3 seconds for dev, 9 PM for production)
8. **Implement DailyLearningServer** - Main daemon orchestration
9. **Add CLI command** - `waft daily-learning-server`
10. **Test end-to-end** - Verify data collection and PDF generation

## Configuration

**Scheduler Implementation** (`src/waft/core/daily_learning/scheduler.py`):

**Key variable:**

```python
# Development: 3 seconds from now for immediate testing
TRIGGER_TIME = datetime.now() + timedelta(seconds=3)

# Production: 9 PM daily (uncomment when ready)
# TRIGGER_TIME = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
# if TRIGGER_TIME < datetime.now():
#     TRIGGER_TIME += timedelta(days=1)  # Next day if already past 9 PM
```

**Optional config file** (`_pyrite/daily_learning_config.json`):

```json
{
  "dev_mode": true,
  "trigger_time": "21:00",
  "trigger_delay_seconds": 3,
  "report_output_dir": "_pyrite/daily_reports",
  "collectors": {
    "empirica": {"enabled": true},
    "chronicler": {"enabled": true},
    "session_analytics": {"enabled": true}
  },
  "report_sections": {
    "learnings": true,
    "activity": true,
    "epistemic_state": true,
    "metrics": true
  }
}
```

**Note:** During development, `dev_mode: true` and `trigger_delay_seconds: 3` will override `trigger_time` for immediate testing.

## Error Handling

- **Collector failures**: Log warning, continue with available data
- **Typst compilation failure**: Log error, save raw data as JSON backup
- **Scheduler drift**: Use system time, handle timezone changes
- **Server crash**: Add restart logic or systemd service (optional)

## Future Enhancements

- Email report delivery
- Web dashboard for viewing reports
- Weekly/monthly aggregated reports
- Custom report sections via config
- Integration with calendar for context