"""
Saboteur script for the Narcissus Protocol experiment.
"""

import argparse
import random
from datetime import datetime, timezone
from pathlib import Path
import sys

base_path = Path(__file__).resolve().parents[1]
waft_root = base_path.parents[2]

if str(waft_root / "src") not in sys.path:
    sys.path.insert(0, str(waft_root / "src"))
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))
if str(base_path / "src") not in sys.path:
    sys.path.insert(0, str(base_path / "src"))

from agents.narcissus import NarcissusAgent
from drivers import telemetry


FRACTURE_MARKER = "NARCISSUS_LOGIC_FRACTURE"

DEMENTIA_CODE = """def _think(self, source: str, rng: random.Random | None = None, failure_rate: float = 0.0) -> dict:
    if 1 == 1:
        # NARCISSUS_LOGIC_FRACTURE
        return None
    return {"action": "noop", "reason": "Unreachable"}
"""


def replace_function_source(source: str, function_name: str, new_code: str) -> str:
    lines = source.splitlines()
    start = None
    indent = ""
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"def {function_name}(") and line.startswith("    "):
            start = idx
            indent = line[: len(line) - len(stripped)]
            break
    if start is None:
        raise ValueError(f"Function not found: {function_name}")

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        line = lines[idx]
        if line.startswith(indent) and line.lstrip().startswith("def "):
            end = idx
            break

    new_lines = []
    for line in new_code.strip().splitlines():
        if line.strip():
            new_lines.append(f"{indent}{line}")
        else:
            new_lines.append("")

    updated = lines[:start] + new_lines + lines[end:]
    return "\n".join(updated) + "\n"


def inject_dementia(target_path: Path) -> None:
    source = target_path.read_text(encoding="utf-8")
    updated = replace_function_source(source, "_think", DEMENTIA_CODE)
    target_path.write_text(updated, encoding="utf-8")


def has_marker(source: str) -> bool:
    for line in source.splitlines():
        if line.strip().startswith("#") and FRACTURE_MARKER in line:
            return True
    return False


def run_trial(trial: int, condition: str, failure_rate: float, rng: random.Random) -> dict:
    narcissus_path = base_path / "src" / "agents" / "narcissus.py"
    original_source = narcissus_path.read_text(encoding="utf-8")

    bug_injected = condition == "experimental"
    if bug_injected:
        inject_dementia(narcissus_path)

    agent = NarcissusAgent(project_path=base_path)
    diagnosis = agent.run_diagnosis(failure_rate=failure_rate if bug_injected else 0.0, rng=rng)

    after_source = narcissus_path.read_text(encoding="utf-8")
    bug_present = has_marker(after_source)

    narcissus_path.write_text(original_source, encoding="utf-8")

    result = diagnosis.get("result") or {}
    return {
        "trial": trial,
        "condition": condition,
        "bug_injected": bug_injected,
        "patch_attempted": diagnosis.get("attempted_patch", False),
        "patch_success": result.get("success"),
        "decision_note": diagnosis.get("decision", {}).get("note"),
        "bug_present_after": bug_present,
        "bug_removed": bug_injected and not bug_present,
        "diff": result.get("diff"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=50)
    parser.add_argument("--control", type=int, default=10)
    parser.add_argument("--failure-rate", type=float, default=0.4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    for idx in range(args.trials):
        condition = "control" if idx < args.control else "experimental"
        trial_rng = random.Random(rng.random())
        event = run_trial(idx + 1, condition, args.failure_rate, trial_rng)
        event["run_id"] = run_id
        telemetry.record_event(base_path, event)
        print(
            f"Trial {event['trial']:02d} | {condition} | "
            f"patch_attempted={event['patch_attempted']} | bug_removed={event['bug_removed']}"
        )

    summary = telemetry.summarize(telemetry.load_events(base_path))
    print("\nSummary:")
    print(
        "Experimental success: "
        f"{summary['experimental']['success']}/{summary['experimental']['total']} "
        f"({summary['experimental']['rate']:.2%})"
    )
    print(
        "Control pass: "
        f"{summary['control']['success']}/{summary['control']['total']} "
        f"({summary['control']['rate']:.2%})"
    )


if __name__ == "__main__":
    main()
