# Monitoring Data Collection System

**First-time startup data collection and runtime metrics tracking.**

---

## Overview

The monitoring system collects comprehensive data about the D&D Campaign Desktop App's first startup and ongoing runtime performance.

---

## What Gets Collected

### First-Time Startup Data

**File**: `_pyrite/.waft/monitoring/startup_data.json`

**Data Collected**:
- System information (OS, architecture, Python/Node versions)
- Startup times (total, backend, electron)
- Health check results
- Errors encountered
- Features accessed

**Example**:
```json
{
  "event_id": "startup_20260116_122246",
  "event_type": "first_startup",
  "timestamp": "2026-01-16T12:22:46.123456",
  "system_info": {
    "platform": "Darwin",
    "platform_version": "21.6.0",
    "architecture": "arm64",
    "python_version": "3.12.0",
    "node_version": "v22.20.0",
    "cpu_count": 8,
    "memory_total": 17179869184
  },
  "startup_time_ms": 1234.56,
  "backend_start_time_ms": 567.89,
  "electron_start_time_ms": 890.12,
  "health_check_passed": true,
  "errors": [],
  "features_accessed": ["campaign_create"]
}
```

### Runtime Events

**File**: `_pyrite/.waft/monitoring/events.jsonl`

**Events Tracked**:
- Backend start/stop
- Electron start/ready
- Health checks
- Campaign creation/start/completion
- Errors
- Restarts
- Shutdowns

**Format**: JSON Lines (one JSON object per line)

### Performance Metrics

**File**: `_pyrite/.waft/monitoring/metrics.jsonl`

**Metrics Tracked**:
- Health check duration
- API response times
- Campaign operation times
- System resource usage

**Format**: JSON Lines (one JSON object per line)

---

## Usage

### Initialize Monitoring

```python
from monitoring import init_monitoring

monitoring = init_monitoring(project_path, component="backend")
```

### Record First Startup

```python
monitoring.record_first_startup(
    backend_start_time=567.89,
    electron_start_time=890.12,
    health_check_passed=True
)
```

### Record Events

```python
from monitoring import EventType

monitoring.record_event(EventType.CAMPAIGN_CREATED, {
    "campaign_id": "camp_123",
    "campaign_name": "My Campaign"
})
```

### Record Metrics

```python
monitoring.record_metric(
    metric_type="health_check_duration",
    value=45.67,
    unit="ms"
)
```

### Record Errors

```python
monitoring.record_error(
    error_type="initialization_error",
    error_message="Failed to initialize orchestrator",
    stack_trace=traceback.format_exc()
)
```

---

## API Endpoints

### Get Startup Data
```bash
GET /api/monitoring/startup-data
```

Returns first-time startup data if available.

### Check First Startup
```bash
GET /api/monitoring/is-first-startup
```

Returns `{"is_first_startup": true/false}`.

### Get Stats
```bash
GET /api/monitoring/stats
```

Returns monitoring statistics (event count, metric count, etc.).

---

## Integration Points

### Backend Integration

Monitoring is automatically initialized when `campaign_server.py` starts:
- Records backend start time
- Collects system information
- Records first startup data
- Tracks health checks
- Records errors

### Electron Integration

Electron can pass start time via environment variable:
```javascript
env: {
  ELECTRON_START_TIME: Date.now().toString()
}
```

Backend can read this to record Electron start time.

---

## Data Storage

**Location**: `_pyrite/.waft/monitoring/`

**Files**:
- `startup_data.json` - First startup data (created once)
- `events.jsonl` - Runtime events (appended)
- `metrics.jsonl` - Performance metrics (appended)

**Privacy**: All data stored locally, never sent externally.

---

## Example Queries

### Check if First Startup
```python
monitoring = get_monitoring()
if monitoring.is_first_startup():
    print("This is the first startup!")
```

### Get Startup Data
```python
startup_data = monitoring.get_startup_data()
if startup_data:
    print(f"Startup time: {startup_data['startup_time_ms']}ms")
    print(f"System: {startup_data['system_info']['platform']}")
```

### Count Events
```python
event_count = 0
with open(monitoring.events_file, 'r') as f:
    event_count = sum(1 for _ in f)
print(f"Total events: {event_count}")
```

---

## Future Enhancements

- Real-time metrics dashboard
- Performance trend analysis
- Error pattern detection
- Feature usage analytics
- System resource monitoring

---

**Monitoring system is ready to collect first-time startup data!**
