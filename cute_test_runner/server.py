#!/usr/bin/env python3
"""
Cute Test Runner - FastAPI Backend

A simple, cute test runner with HTML/CSS/JS frontend.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Cute Test Runner", description="A cute little test runner 🧪", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get project root (assuming server.py is in cute_test_runner/)
PROJECT_ROOT = Path(__file__).parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"


class TestResult(BaseModel):
    name: str
    status: str  # passed, failed, skipped
    duration: float = 0.0
    message: str = ""
    error: str = ""


class TestSummary(BaseModel):
    total: int
    passed: int
    failed: int
    skipped: int
    duration: float


class TestResponse(BaseModel):
    tests: list[TestResult]
    summary: TestSummary


def run_pytest() -> dict[str, Any]:
    """Run pytest and parse results."""
    start_time = time.time()

    try:
        # Run pytest with JSON output
        result = subprocess.run(
            [
                "pytest",
                "-v",
                "--tb=short",
                "--json-report",
                "--json-report-file=/tmp/pytest-report.json",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )

        duration = time.time() - start_time

        # Try to parse JSON report if it exists
        json_report_path = Path("/tmp/pytest-report.json")
        if json_report_path.exists():
            try:
                with open(json_report_path) as f:
                    report = json.load(f)
                    return parse_pytest_json(report, duration)
            except Exception:
                pass

        # Fallback: parse stdout
        return parse_pytest_output(result.stdout, result.stderr, result.returncode, duration)

    except subprocess.TimeoutExpired:
        return {
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": time.time() - start_time,
            },
            "error": "Tests timed out after 60 seconds",
        }
    except FileNotFoundError:
        return {
            "tests": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration": 0},
            "error": "pytest not found. Please install pytest: pip install pytest pytest-json-report",
        }
    except Exception as e:
        return {
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": time.time() - start_time,
            },
            "error": str(e),
        }


def parse_pytest_json(report: dict, duration: float) -> dict[str, Any]:
    """Parse pytest JSON report."""
    tests = []
    summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration": duration}

    for test in report.get("tests", []):
        test_name = test.get("nodeid", "unknown")
        outcome = test.get("outcome", "unknown")

        status = (
            "passed" if outcome == "passed" else ("failed" if outcome == "failed" else "skipped")
        )
        duration = test.get("duration", 0.0)
        message = test.get("call", {}).get("longrepr", "") if outcome == "failed" else ""

        tests.append(
            {
                "name": test_name,
                "status": status,
                "duration": duration,
                "message": "",
                "error": message,
            }
        )

        summary["total"] += 1
        if status == "passed":
            summary["passed"] += 1
        elif status == "failed":
            summary["failed"] += 1
        else:
            summary["skipped"] += 1

    return {"tests": tests, "summary": summary}


def parse_pytest_output(
    stdout: str, stderr: str, returncode: int, duration: float
) -> dict[str, Any]:
    """Parse pytest stdout/stderr (fallback method)."""
    tests = []
    summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "duration": duration}

    lines = stdout.split("\n")
    current_test = None

    for line in lines:
        line = line.strip()

        # Match pytest output patterns
        if line.startswith("test_"):
            # Extract test name
            parts = line.split()
            if len(parts) >= 2:
                test_name = parts[0]
                status_str = parts[1] if len(parts) > 1 else "UNKNOWN"

                status = (
                    "passed"
                    if "PASSED" in status_str
                    else ("failed" if "FAILED" in status_str else "skipped")
                )

                tests.append(
                    {
                        "name": test_name,
                        "status": status,
                        "duration": 0.0,
                        "message": "",
                        "error": "",
                    }
                )

                summary["total"] += 1
                if status == "passed":
                    summary["passed"] += 1
                elif status == "failed":
                    summary["failed"] += 1
                else:
                    summary["skipped"] += 1

    # If no tests found, create a dummy result
    if not tests:
        tests.append(
            {
                "name": "No tests found",
                "status": "skipped",
                "duration": 0.0,
                "message": "No tests were discovered. Make sure you have test files in the tests/ directory.",
                "error": "",
            }
        )

    return {"tests": tests, "summary": summary}


@app.post("/api/run-tests", response_model=TestResponse)
async def run_tests():
    """Run tests and return results."""
    result = run_pytest()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return TestResponse(**result)


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "message": "🧪 Test runner is ready!"}


# Serve static files (CSS, JS)
static_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Serve HTML page (must be last to not conflict with static files)
@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    html_path = Path(__file__).parent / "index.html"
    return FileResponse(html_path)


if __name__ == "__main__":
    import uvicorn

    print("🧪 Starting Cute Test Runner...")
    print("📍 Server: http://localhost:8002")
    print("🌐 Open in browser: http://localhost:8002")
    print("\nPress Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
