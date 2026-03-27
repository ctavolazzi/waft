#!/usr/bin/env python3
"""Generate an SCP-style discovery dossier for WAFT meme generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.core.meme_dossier import generate_dossier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate memes and compile SCP-style WAFT meme discovery dossier PDF."
    )
    parser.add_argument(
        "--prompt",
        default="Facility notes indicate WAFT has begun inventing memes about its own operation.",
        help="Base prompt for meme generation.",
    )
    parser.add_argument("--count", type=int, default=4, help="Number of memes to generate.")
    parser.add_argument("--seed", type=int, default=None, help="Optional deterministic seed.")
    parser.add_argument(
        "--artifacts-dir",
        default="_work_efforts/reports/meme_discovery_artifacts",
        help="Directory for generated meme image artifacts.",
    )
    parser.add_argument(
        "--output",
        default="_work_efforts/reports/SCP_WAFT_MEME_DISCOVERY_DOSSIER.pdf",
        help="Output PDF path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = Path.cwd()
    output_pdf = Path(args.output).resolve()
    artifacts_dir = Path(args.artifacts_dir).resolve()

    final_pdf, records = generate_dossier(
        project_path=project_path,
        prompt=args.prompt,
        count=max(1, args.count),
        seed=args.seed,
        output_pdf=output_pdf,
        artifacts_dir=artifacts_dir,
    )

    successes = len([r for r in records if r["success"]])
    failures = len(records) - successes
    print(f"PDF generated: {final_pdf}")
    print(f"Artifacts: {successes} success, {failures} failed")
    for record in records:
        status = "ok" if record["success"] else "failed"
        print(f"- artifact-{record['index']:02d}: {status} -> {record['output_path']}")
        if record["error"]:
            print(f"  error: {record['error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
