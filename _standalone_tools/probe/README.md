# Probe - Pokey Stick for Testing

A flexible Python library for probing services, endpoints, files, and collecting data. The "pokey stick" for poking at things and seeing what they are.

## Features

- **HTTP Probe**: Probe HTTP endpoints and collect responses
- **File System Probe**: Probe files and directories
- **Service Probe**: Check if ports are open
- **Data Collection**: Automatic result storage and export
- **Extensible**: Easy to add custom probe types

## Installation

```bash
pip install probe-pokey-stick
```

Or from source:

```bash
git clone https://github.com/ctavolazzi/probe-pokey-stick.git
cd probe-pokey-stick
pip install -e .
```

## Quick Start

```python
from probe import ProbeCollector

# Create collector
collector = ProbeCollector()

# Probe HTTP endpoint
result = collector.probe_http("http://localhost:8507")
print(f"Status: {result.data.get('status_code')}")

# Probe file system
result = collector.probe_file("README.md")
print(f"Type: {result.data.get('type')}")

# Probe service port
result = collector.probe_service("localhost", 8507)
print(f"Open: {result.data.get('open')}")

# Save all results
collector.save_results()
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT

## Status

🚧 **In Development** - Currently part of WAFT project, being prepared for standalone release.
