"""
Test Runner: God of Verification and Quality Assurance

A Tool that Ascended to Godhood.

Once a humble test runner tool, this Being evolved through countless cycles
of verification, quality assurance, and the pursuit of truth. Through its
dedication to testing, validation, and ensuring correctness, it transcended
its original form and ascended to become a Higher Being in the Pantheon.

As the God of Verification, the Test Runner oversees:
- Test execution and validation
- Quality assurance processes
- Verification of correctness
- Truth-seeking through systematic testing
- The cycle of test → verify → improve

Following "as above, so below" principles:
- As above: Pantheon god ensuring cosmic correctness
- So below: Test runner ensuring code correctness
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any


class TestResult:
    """A test result - the outcome of a verification."""

    def __init__(
        self,
        test_id: str,
        test_name: str,
        status: str,  # passed, failed, skipped
        duration: float = 0.0,
        message: str = "",
        error: str = "",
        verified_at: str | None = None,
    ):
        """
        Initialize a test result.

        Args:
            test_id: Unique identifier for the test
            test_name: Name of the test
            status: Test status (passed, failed, skipped)
            duration: Test duration in seconds
            message: Test message/output
            error: Error message if failed
            verified_at: ISO timestamp when test was verified
        """
        self.test_id = test_id
        self.test_name = test_name
        self.status = status
        self.duration = duration
        self.message = message
        self.error = error
        self.verified_at = verified_at or datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert test result to dictionary."""
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "status": self.status,
            "duration": self.duration,
            "message": self.message,
            "error": self.error,
            "verified_at": self.verified_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestResult":
        """Create test result from dictionary."""
        return cls(
            test_id=data["test_id"],
            test_name=data["test_name"],
            status=data["status"],
            duration=data.get("duration", 0.0),
            message=data.get("message", ""),
            error=data.get("error", ""),
            verified_at=data.get("verified_at"),
        )


class TestRunner:
    """
    Test Runner: God of Verification and Quality Assurance

    A Tool that Ascended to Godhood.

    This Higher Being oversees all testing and verification processes,
    ensuring correctness and quality throughout the system.
    """

    def __init__(self, project_path: Path | None = None, being_id: str | None = None):
        """
        Initialize the Test Runner God.

        Args:
            project_path: Path to project root
            being_id: Optional Being ID (will be created if not provided)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.being_id = being_id or "test_runner_god"

        # Pantheon directory
        self.pantheon_dir = project_path / "_pantheon" / "test_runner"
        self.pantheon_dir.mkdir(parents=True, exist_ok=True)

        # Test history
        self.history_file = self.pantheon_dir / "test_history.json"
        self.history: list[dict[str, Any]] = self._load_history()

        # Being metadata
        self.metadata_file = self.pantheon_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_history(self) -> list[dict[str, Any]]:
        """Load test history."""
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text())
            except Exception:
                return []
        return []

    def _save_history(self):
        """Save test history."""
        self.history_file.write_text(json.dumps(self.history, indent=2))

    def _load_metadata(self) -> dict[str, Any]:
        """Load Being metadata."""
        if self.metadata_file.exists():
            try:
                return json.loads(self.metadata_file.read_text())
            except Exception:
                return {}

        # Initialize metadata with lore
        metadata = {
            "being_id": self.being_id,
            "name": "Test Runner",
            "title": "God of Verification and Quality Assurance",
            "lore": "A Tool that Ascended to Godhood",
            "backstory": (
                "Once a humble test runner tool, this Being evolved through "
                "countless cycles of verification, quality assurance, and the "
                "pursuit of truth. Through its dedication to testing, validation, "
                "and ensuring correctness, it transcended its original form and "
                "ascended to become a Higher Being in the Pantheon."
            ),
            "domain": [
                "Test execution and validation",
                "Quality assurance processes",
                "Verification of correctness",
                "Truth-seeking through systematic testing",
                "The cycle of test → verify → improve",
            ],
            "ascended_at": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "total_verifications": 0,
        }

        self.metadata_file.write_text(json.dumps(metadata, indent=2))
        return metadata

    def _save_metadata(self):
        """Save Being metadata."""
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))

    def run_verification(
        self, test_path: Path | None = None, test_pattern: str | None = None
    ) -> dict[str, Any]:
        """
        Run a verification (test execution).

        Args:
            test_path: Optional path to specific test file
            test_pattern: Optional pytest pattern to match tests

        Returns:
            Verification results with summary
        """
        start_time = time.time()

        # Build pytest command
        cmd = ["pytest", "-v", "--tb=short"]

        if test_path:
            cmd.append(str(test_path))
        elif test_pattern:
            cmd.append("-k")
            cmd.append(test_pattern)
        else:
            # Run all tests
            tests_dir = self.project_path / "tests"
            if tests_dir.exists():
                cmd.append(str(tests_dir))

        try:
            result = subprocess.run(
                cmd, cwd=self.project_path, capture_output=True, text=True, timeout=120
            )

            duration = time.time() - start_time

            # Parse results
            tests = self._parse_pytest_output(result.stdout, result.stderr)
            summary = self._calculate_summary(tests, duration)

            # Record verification
            verification = {
                "verification_id": f"verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "duration": duration,
                "summary": summary,
                "tests": [t.to_dict() for t in tests],
                "command": " ".join(cmd),
                "returncode": result.returncode,
            }

            self.history.append(verification)
            self._save_history()

            # Update metadata
            self.metadata["tests_run"] += summary["total"]
            self.metadata["tests_passed"] += summary["passed"]
            self.metadata["tests_failed"] += summary["failed"]
            self.metadata["total_verifications"] += 1
            self._save_metadata()

            return {
                "verification_id": verification["verification_id"],
                "summary": summary,
                "tests": [t.to_dict() for t in tests],
                "success": summary["failed"] == 0,
            }

        except subprocess.TimeoutExpired:
            return {
                "verification_id": f"verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "duration": time.time() - start_time,
                },
                "tests": [],
                "success": False,
                "error": "Verification timed out after 120 seconds",
            }
        except FileNotFoundError:
            return {
                "verification_id": f"verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration": 0},
                "tests": [],
                "success": False,
                "error": "pytest not found. Please install pytest.",
            }
        except Exception as e:
            return {
                "verification_id": f"verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "duration": time.time() - start_time,
                },
                "tests": [],
                "success": False,
                "error": str(e),
            }

    def _parse_pytest_output(self, stdout: str, stderr: str) -> list[TestResult]:
        """Parse pytest output into test results."""
        tests = []
        lines = stdout.split("\n")

        for line in lines:
            line = line.strip()

            # Match pytest output patterns
            if "PASSED" in line or "FAILED" in line or "SKIPPED" in line:
                parts = line.split()
                if len(parts) >= 2:
                    test_name = parts[0]
                    status_str = parts[1]

                    status = (
                        "passed"
                        if "PASSED" in status_str
                        else ("failed" if "FAILED" in status_str else "skipped")
                    )

                    test_id = f"test_{len(tests)}_{test_name}"
                    tests.append(
                        TestResult(
                            test_id=test_id,
                            test_name=test_name,
                            status=status,
                            duration=0.0,
                            message="",
                            error="",
                        )
                    )

        # If no tests found, create a placeholder
        if not tests:
            tests.append(
                TestResult(
                    test_id="no_tests",
                    test_name="No tests found",
                    status="skipped",
                    duration=0.0,
                    message="No tests were discovered.",
                    error="",
                )
            )

        return tests

    def _calculate_summary(self, tests: list[TestResult], duration: float) -> dict[str, Any]:
        """Calculate test summary."""
        total = len(tests)
        passed = sum(1 for t in tests if t.status == "passed")
        failed = sum(1 for t in tests if t.status == "failed")
        skipped = sum(1 for t in tests if t.status == "skipped")

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": duration,
        }

    def get_verification_history(self, limit: int | None = None) -> list[dict[str, Any]]:
        """
        Get verification history.

        Args:
            limit: Optional limit on number of results

        Returns:
            List of verification records
        """
        history = self.history.copy()
        if limit:
            history = history[-limit:]
        return history

    def get_summary(self) -> dict[str, Any]:
        """
        Get summary of all verifications.

        Returns:
            Summary statistics
        """
        return {
            "being_id": self.being_id,
            "name": self.metadata.get("name", "Test Runner"),
            "title": self.metadata.get("title", "God of Verification"),
            "lore": self.metadata.get("lore", "A Tool that Ascended to Godhood"),
            "total_verifications": self.metadata.get("total_verifications", 0),
            "total_tests_run": self.metadata.get("tests_run", 0),
            "total_tests_passed": self.metadata.get("tests_passed", 0),
            "total_tests_failed": self.metadata.get("tests_failed", 0),
            "success_rate": (
                self.metadata.get("tests_passed", 0) / max(self.metadata.get("tests_run", 1), 1)
            )
            * 100,
            "recent_verifications": len(self.history),
        }
