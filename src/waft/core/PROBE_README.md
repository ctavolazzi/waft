# Probe System - Pokey Stick for Testing

A flexible system for probing services, endpoints, files, and collecting data. The "pokey stick" for poking at things and seeing what they are.

## Quick Start

```python
from waft.core.probe import ProbeCollector

# Create collector
collector = ProbeCollector()

# Probe HTTP endpoint
result = collector.probe_http("http://localhost:8507")
print(f"Status: {result.data.get('status_code')}")

# Probe file system
result = collector.probe_file("good_morning.py")
print(f"Type: {result.data.get('type')}")

# Probe service port
result = collector.probe_service("localhost", 8507)
print(f"Open: {result.data.get('open')}")

# Save all results
collector.save_results()

# Get summary
summary = collector.summary()
print(f"Total: {summary['total']}, Successful: {summary['successful']}")
```

## Probe Types

### HTTPProbe
Probe HTTP endpoints - poke at URLs and collect responses.

```python
from waft.core.probe import HTTPProbe

probe = HTTPProbe(timeout=5)
result = probe.probe("http://localhost:8507", method="GET")
```

**Collected Data:**
- Status code
- Headers
- Content type
- Content length
- JSON response (if applicable)
- Text preview (if not JSON)

### FileSystemProbe
Probe file system - poke at files and directories.

```python
from waft.core.probe import FileSystemProbe

probe = FileSystemProbe()
result = probe.probe("path/to/file.py")
```

**Collected Data:**
- File/directory type
- Size (for files)
- Modified timestamp
- Extension (for files)
- Preview (first 10 lines for text files)
- Item count (for directories)

### ServiceProbe
Probe services - check if ports are open.

```python
from waft.core.probe import ServiceProbe

probe = ServiceProbe(timeout=2)
result = probe.probe("localhost", 8507)
```

**Collected Data:**
- Host and port
- Open status (boolean)

## ProbeCollector

The `ProbeCollector` manages multiple probes and stores results.

### Features

- **Quick Methods**: `probe_http()`, `probe_file()`, `probe_service()`
- **Result Storage**: Automatically saves to `_probe_data/` directory
- **Summary Statistics**: Get overview of all probe results
- **JSON Export**: Save all results to JSON file

### Example

```python
from waft.core.probe import ProbeCollector

collector = ProbeCollector()

# Probe multiple things
collector.probe_http("http://localhost:8507")
collector.probe_file("good_morning.py")
collector.probe_service("localhost", 8507)

# Get summary
summary = collector.summary()
print(f"Total: {summary['total']}")
print(f"Successful: {summary['successful']}")
print(f"Failed: {summary['failed']}")

# Save results
filepath = collector.save_results()
print(f"Saved to: {filepath}")
```

## ProbeResult

Each probe returns a `ProbeResult` with:

- `probe_type`: Type of probe (http_get, filesystem, service)
- `target`: What was probed
- `timestamp`: When it was probed
- `success`: Whether it succeeded
- `data`: Collected data (varies by probe type)
- `error`: Error message (if failed)
- `duration_ms`: How long it took

## Use Cases

1. **Service Health Checks**: Probe all your services to see what's running
2. **API Testing**: Probe API endpoints and collect responses
3. **File System Exploration**: Probe files and directories to understand structure
4. **Integration Testing**: Probe services before running tests
5. **Monitoring**: Regularly probe services and save results for analysis

## Example: Probe All WAFT Services

```python
from waft.core.probe import ProbeCollector

collector = ProbeCollector()

# Probe all WAFT services
services = [
    ("http://localhost:8507", "Good Morning Dashboard"),
    ("http://localhost:8000/api/health", "API Server"),
    ("http://localhost:8501", "Main Dashboard"),
]

for url, name in services:
    result = collector.probe_http(url)
    status = "✅" if result.success else "❌"
    print(f"{status} {name}: {result.data.get('status_code', 'N/A')}")

# Save results
collector.save_results("waft_services_check.json")
```

## Storage

Results are saved to `_probe_data/` directory by default. Each save creates a JSON file with:

- Timestamp
- Total probe count
- All probe results (as dictionaries)

You can specify a custom filename or let it auto-generate with timestamp.
