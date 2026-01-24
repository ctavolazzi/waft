#!/usr/bin/env python3
"""
Run the prove-it telemetry server.

Stores run metrics in a JSONL evidence log.
"""

import argparse
from pathlib import Path

import uvicorn

from waft.core.prove_it_telemetry import create_app


def main():
    parser = argparse.ArgumentParser(description="Run prove-it telemetry server")
    parser.add_argument(
        "--log",
        type=Path,
        default=Path.cwd()
        / "_work_efforts"
        / "WE-260119-ejtx_teleport_massive_official_guide_to_scint_traversal"
        / "telemetry_evidence.jsonl",
        help="Path to JSONL evidence log",
    )
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8133)
    args = parser.parse_args()

    app = create_app(args.log)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
