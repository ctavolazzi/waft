#!/usr/bin/env python3
"""
Test Utilities - Leveraging Underutilized Dependencies

Quick tooling built around WAFT dependencies:
1. TinyDB - Test metrics database
2. Rich - Beautiful test output
3. d20 - Random test data generation
4. watchdog - Auto-test on file changes
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

# TinyDB for test metrics storage
try:
    from tinydb import Query, TinyDB

    TINYDB_AVAILABLE = True
except ImportError:
    TINYDB_AVAILABLE = False

# Rich for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.tree import Tree

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# d20 for random test data
try:
    import d20

    D20_AVAILABLE = True
except ImportError:
    D20_AVAILABLE = False

# watchdog for auto-testing
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


class TestMetricsDB:
    """
    TinyDB-based test metrics storage.

    Stores test results, metrics, and historical data for analysis.
    """

    def __init__(self, db_path: Path):
        """Initialize metrics database."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        if TINYDB_AVAILABLE:
            self.db = TinyDB(str(self.db_path))
            self.query = Query()
        else:
            self.db = None
            # Fallback to JSON
            self._data = self._load_json()

    def _load_json(self) -> dict[str, Any]:
        """Load JSON fallback data."""
        if self.db_path.exists():
            try:
                with open(self.db_path) as f:
                    return json.load(f)
            except:
                return {"tests": [], "metrics": {}}
        return {"tests": [], "metrics": {}}

    def _save_json(self):
        """Save JSON fallback data."""
        with open(self.db_path, "w") as f:
            json.dump(self._data, f, indent=2, default=str)

    def record_test(
        self,
        test_id: str,
        phase: int,
        success: bool,
        metrics: dict[str, Any],
        duration: float = 0.0,
    ):
        """Record a test execution."""
        record = {
            "test_id": test_id,
            "phase": phase,
            "success": success,
            "metrics": metrics,
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if TINYDB_AVAILABLE:
            self.db.insert(record)
        else:
            if "tests" not in self._data:
                self._data["tests"] = []
            self._data["tests"].append(record)
            self._save_json()

    def get_phase_stats(self, phase: int) -> dict[str, Any]:
        """Get statistics for a specific phase."""
        if TINYDB_AVAILABLE:
            tests = self.db.search(self.query.phase == phase)
        else:
            tests = [t for t in self._data.get("tests", []) if t.get("phase") == phase]

        if not tests:
            return {"total": 0, "successful": 0, "failed": 0, "success_rate": 0.0}

        successful = sum(1 for t in tests if t.get("success", False))
        total = len(tests)

        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0.0,
            "avg_duration": sum(t.get("duration", 0) for t in tests) / total if total > 0 else 0.0,
        }

    def get_all_stats(self) -> dict[str, Any]:
        """Get overall statistics."""
        if TINYDB_AVAILABLE:
            tests = self.db.all()
        else:
            tests = self._data.get("tests", [])

        if not tests:
            return {"total": 0, "successful": 0, "failed": 0, "success_rate": 0.0}

        successful = sum(1 for t in tests if t.get("success", False))
        total = len(tests)

        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0.0,
            "phases": {phase: self.get_phase_stats(phase) for phase in [1, 2, 3, 4]},
        }


class TestOutputFormatter:
    """
    Rich-based beautiful test output formatting.

    Creates tables, panels, trees, and progress bars for test results.
    """

    def __init__(self):
        """Initialize formatter."""
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def print_test_table(self, results: list[dict[str, Any]]):
        """Print test results as a beautiful table."""
        if not RICH_AVAILABLE:
            # Fallback to simple print
            for r in results:
                print(f"{r.get('test_id')}: {'✓' if r.get('success') else '✗'}")
            return

        table = Table(title="Test Results", show_header=True, header_style="bold magenta")
        table.add_column("Test ID", style="cyan")
        table.add_column("Phase", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Metrics", style="dim")

        for result in results:
            status = "[green]✓ PASS[/green]" if result.get("success") else "[red]✗ FAIL[/red]"
            metrics_str = ", ".join([f"{k}: {v}" for k, v in result.get("metrics", {}).items()][:2])
            table.add_row(
                result.get("test_id", "unknown"), str(result.get("phase", 0)), status, metrics_str
            )

        self.console.print(table)

    def print_phase_panel(self, phase: int, stats: dict[str, Any]):
        """Print phase statistics in a panel."""
        if not RICH_AVAILABLE:
            print(f"Phase {phase}: {stats.get('successful')}/{stats.get('total')} successful")
            return

        content = f"""
[bold]Total Tests:[/bold] {stats.get("total", 0)}
[bold]Successful:[/bold] [green]{stats.get("successful", 0)}[/green]
[bold]Failed:[/bold] [red]{stats.get("failed", 0)}[/red]
[bold]Success Rate:[/bold] {stats.get("success_rate", 0.0):.1%}
[bold]Avg Duration:[/bold] {stats.get("avg_duration", 0.0):.2f}s
"""

        panel = Panel(content, title=f"Phase {phase} Statistics", border_style="blue")
        self.console.print(panel)

    def print_metrics_tree(self, metrics: dict[str, Any]):
        """Print metrics as a tree structure."""
        if not RICH_AVAILABLE:
            print(json.dumps(metrics, indent=2))
            return

        tree = Tree("📊 Test Metrics")

        for key, value in metrics.items():
            if isinstance(value, dict):
                branch = tree.add(f"[cyan]{key}[/cyan]")
                for k, v in value.items():
                    branch.add(f"{k}: [green]{v}[/green]")
            else:
                tree.add(f"[cyan]{key}[/cyan]: [green]{value}[/green]")

        self.console.print(tree)

    def progress_bar(self, description: str = "Running tests..."):
        """Create a progress bar context manager."""
        if not RICH_AVAILABLE:
            return None

        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        )


class RandomTestData:
    """
    d20-based random test data generation.

    Uses dice rolling for sampling, randomization, and test data generation.
    """

    @staticmethod
    def random_dpi() -> int:
        """Generate random DPI value (150, 300, or 600)."""
        if not D20_AVAILABLE:
            import random

            return random.choice([150, 300, 600])

        # Roll 1d3 to pick DPI
        result = d20.roll("1d3")
        dpi_map = {1: 150, 2: 300, 3: 600}
        return dpi_map.get(result.total, 300)

    @staticmethod
    def random_page_count() -> int:
        """Generate random page count for testing."""
        if not D20_AVAILABLE:
            import random

            return random.randint(1, 10)

        # Roll 1d10 for page count
        result = d20.roll("1d10")
        return result.total

    @staticmethod
    def random_sample(items: list[Any], count: int) -> list[Any]:
        """Randomly sample items using dice rolls."""
        if not D20_AVAILABLE:
            import random

            return random.sample(items, min(count, len(items)))

        # Use dice to determine which items to pick
        selected = []
        available = items.copy()

        for _ in range(min(count, len(items))):
            if not available:
                break
            # Roll dice to pick index
            result = d20.roll(f"1d{len(available)}")
            idx = result.total - 1
            selected.append(available.pop(idx))

        return selected

    @staticmethod
    def random_quality_threshold() -> float:
        """Generate random quality threshold (0.8-1.0)."""
        if not D20_AVAILABLE:
            import random

            return random.uniform(0.8, 1.0)

        # Roll 2d10 for threshold (0.80-1.00)
        result = d20.roll("2d10")
        threshold = 0.80 + (result.total / 100.0)
        return min(threshold, 1.0)


class AutoTestWatcher:
    """
    watchdog-based auto-testing on file changes.

    Watches test files and automatically re-runs tests when code changes.
    """

    def __init__(self, test_dir: Path, callback):
        """
        Initialize file watcher.

        Args:
            test_dir: Directory to watch
            callback: Function to call when files change
        """
        self.test_dir = Path(test_dir)
        self.callback = callback
        self.observer = None

        if WATCHDOG_AVAILABLE:
            self.observer = Observer()
            handler = TestFileHandler(callback)
            self.observer.schedule(handler, str(self.test_dir), recursive=True)

    def start(self):
        """Start watching for file changes."""
        if self.observer:
            self.observer.start()
            print(f"👀 Watching {self.test_dir} for changes...")
        else:
            print("⚠️  watchdog not available - auto-testing disabled")

    def stop(self):
        """Stop watching for file changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()


class TestFileHandler(FileSystemEventHandler):
    """File system event handler for test files."""

    def __init__(self, callback):
        """Initialize handler."""
        self.callback = callback
        self.last_trigger = None

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Debounce rapid changes
        now = datetime.utcnow()
        if self.last_trigger and (now - self.last_trigger).total_seconds() < 2:
            return

        # Only watch Python files
        if event.src_path.endswith(".py"):
            self.last_trigger = now
            print(f"\n🔄 File changed: {event.src_path}")
            print("   Re-running tests...")
            self.callback()


# Convenience functions
def create_metrics_db(research_dir: Path) -> TestMetricsDB:
    """Create a test metrics database."""
    return TestMetricsDB(research_dir / "test_metrics.json")


def create_output_formatter() -> TestOutputFormatter:
    """Create a test output formatter."""
    return TestOutputFormatter()


def create_random_data() -> RandomTestData:
    """Create a random test data generator."""
    return RandomTestData()


def create_auto_watcher(test_dir: Path, callback) -> AutoTestWatcher | None:
    """Create an auto-test watcher."""
    if WATCHDOG_AVAILABLE:
        return AutoTestWatcher(test_dir, callback)
    return None
