"""
Probe System - Pokey Stick for Testing and Exploration

A flexible system for probing services, endpoints, files, and collecting data.
The "pokey stick" for poking at things and seeing what they are.
"""

import json
import socket
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from requests.exceptions import RequestException


@dataclass
class ProbeResult:
    """Result from a single probe operation."""

    probe_type: str
    target: str
    timestamp: str
    success: bool
    data: dict[str, Any]
    error: str | None = None
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return asdict(self)


class Probe:
    """Base probe class - the pokey stick."""

    def __init__(self, name: str = "probe"):
        self.name = name
        self.results: list[ProbeResult] = []

    def probe(self, target: str, **kwargs) -> ProbeResult:
        """Probe a target and return result."""
        raise NotImplementedError("Subclasses must implement probe()")

    def collect(self) -> list[ProbeResult]:
        """Get all collected results."""
        return self.results

    def clear(self):
        """Clear collected results."""
        self.results = []


class HTTPProbe(Probe):
    """Probe HTTP endpoints - poke at URLs."""

    def __init__(self, name: str = "http_probe", timeout: int = 5):
        super().__init__(name)
        self.timeout = timeout

    def probe(self, url: str, method: str = "GET", **kwargs) -> ProbeResult:
        """Probe an HTTP endpoint."""
        start_time = time.time()
        probe_type = f"http_{method.lower()}"

        try:
            response = requests.request(method=method, url=url, timeout=self.timeout, **kwargs)

            duration_ms = (time.time() - start_time) * 1000

            # Collect response data
            data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get("Content-Type", ""),
                "content_length": len(response.content),
                "url": response.url,
            }

            # Try to parse JSON if possible
            try:
                data["json"] = response.json()
            except:
                # If not JSON, include text preview
                text = response.text
                data["text_preview"] = text[:500] if len(text) > 500 else text

            result = ProbeResult(
                probe_type=probe_type,
                target=url,
                timestamp=datetime.now().isoformat(),
                success=200 <= response.status_code < 300,
                data=data,
                duration_ms=duration_ms,
            )

        except RequestException as e:
            duration_ms = (time.time() - start_time) * 1000
            result = ProbeResult(
                probe_type=probe_type,
                target=url,
                timestamp=datetime.now().isoformat(),
                success=False,
                data={},
                error=str(e),
                duration_ms=duration_ms,
            )

        self.results.append(result)
        return result


class FileSystemProbe(Probe):
    """Probe file system - poke at files and directories."""

    def probe(self, path: str, **kwargs) -> ProbeResult:
        """Probe a file or directory."""
        start_time = time.time()
        target_path = Path(path)

        try:
            if not target_path.exists():
                result = ProbeResult(
                    probe_type="filesystem",
                    target=str(path),
                    timestamp=datetime.now().isoformat(),
                    success=False,
                    data={},
                    error="Path does not exist",
                    duration_ms=(time.time() - start_time) * 1000,
                )
            elif target_path.is_file():
                # Probe file
                stat = target_path.stat()
                data = {
                    "type": "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "extension": target_path.suffix,
                }

                # Try to read first few lines if text file
                if target_path.suffix in [".py", ".md", ".txt", ".json", ".yaml", ".yml"]:
                    try:
                        with open(target_path, encoding="utf-8") as f:
                            lines = f.readlines()[:10]
                            data["preview"] = "".join(lines)
                            data["total_lines"] = sum(
                                1 for _ in open(target_path, encoding="utf-8")
                            )
                    except:
                        pass

                result = ProbeResult(
                    probe_type="filesystem",
                    target=str(path),
                    timestamp=datetime.now().isoformat(),
                    success=True,
                    data=data,
                    duration_ms=(time.time() - start_time) * 1000,
                )
            else:
                # Probe directory
                items = list(target_path.iterdir())
                data = {
                    "type": "directory",
                    "item_count": len(items),
                    "items": [item.name for item in items[:20]],  # First 20 items
                }

                result = ProbeResult(
                    probe_type="filesystem",
                    target=str(path),
                    timestamp=datetime.now().isoformat(),
                    success=True,
                    data=data,
                    duration_ms=(time.time() - start_time) * 1000,
                )

        except Exception as e:
            result = ProbeResult(
                probe_type="filesystem",
                target=str(path),
                timestamp=datetime.now().isoformat(),
                success=False,
                data={},
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )

        self.results.append(result)
        return result


class ServiceProbe(Probe):
    """Probe services - check if ports are open."""

    def __init__(self, name: str = "service_probe", timeout: int = 2):
        super().__init__(name)
        self.timeout = timeout

    def probe(self, host: str, port: int, **kwargs) -> ProbeResult:
        """Probe a service on host:port."""
        start_time = time.time()
        target = f"{host}:{port}"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result_code = sock.connect_ex((host, port))
            sock.close()

            is_open = result_code == 0
            data = {
                "host": host,
                "port": port,
                "open": is_open,
            }

            result = ProbeResult(
                probe_type="service",
                target=target,
                timestamp=datetime.now().isoformat(),
                success=is_open,
                data=data,
                duration_ms=(time.time() - start_time) * 1000,
            )

        except Exception as e:
            result = ProbeResult(
                probe_type="service",
                target=target,
                timestamp=datetime.now().isoformat(),
                success=False,
                data={},
                error=str(e),
                duration_ms=(time.time() - start_time) * 1000,
            )

        self.results.append(result)
        return result


class ProbeCollector:
    """Collector for managing multiple probes and storing results."""

    def __init__(self, storage_path: Path | None = None):
        self.probes: dict[str, Probe] = {}
        self.storage_path = storage_path or Path("_probe_data")
        self.storage_path.mkdir(exist_ok=True)

    def add_probe(self, name: str, probe: Probe):
        """Add a probe to the collector."""
        self.probes[name] = probe

    def get_probe(self, name: str) -> Probe | None:
        """Get a probe by name."""
        return self.probes.get(name)

    def probe_http(self, url: str, method: str = "GET", **kwargs) -> ProbeResult:
        """Quick HTTP probe."""
        if "http" not in self.probes:
            self.add_probe("http", HTTPProbe())
        return self.probes["http"].probe(url, method=method, **kwargs)

    def probe_file(self, path: str) -> ProbeResult:
        """Quick file system probe."""
        if "filesystem" not in self.probes:
            self.add_probe("filesystem", FileSystemProbe())
        return self.probes["filesystem"].probe(path)

    def probe_service(self, host: str, port: int) -> ProbeResult:
        """Quick service probe."""
        if "service" not in self.probes:
            self.add_probe("service", ServiceProbe())
        return self.probes["service"].probe(host, port)

    def collect_all(self) -> list[ProbeResult]:
        """Collect all results from all probes."""
        all_results = []
        for probe in self.probes.values():
            all_results.extend(probe.collect())
        return all_results

    def save_results(self, filename: str | None = None) -> Path:
        """Save all results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"probe_results_{timestamp}.json"

        filepath = self.storage_path / filename

        results = [r.to_dict() for r in self.collect_all()]
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_probes": len(results),
            "results": results,
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return filepath

    def clear_all(self):
        """Clear all probe results."""
        for probe in self.probes.values():
            probe.clear()

    def summary(self) -> dict[str, Any]:
        """Get summary of all probe results."""
        all_results = self.collect_all()
        successful = [r for r in all_results if r.success]
        failed = [r for r in all_results if not r.success]

        return {
            "total": len(all_results),
            "successful": len(successful),
            "failed": len(failed),
            "by_type": {
                probe_type: len([r for r in all_results if r.probe_type == probe_type])
                for probe_type in {r.probe_type for r in all_results}
            },
            "avg_duration_ms": sum(r.duration_ms for r in all_results) / len(all_results)
            if all_results
            else 0,
        }
