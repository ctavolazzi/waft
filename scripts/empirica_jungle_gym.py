#!/usr/bin/env python3
"""
Empirica Jungle Gym

Stress-tests WAFT Empirica brain transport behavior:
- mcp preferred
- cli fallback
- degraded fallback
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from waft.core.empirica_handler import EmpericaHandler


def _mock_cli_json(command: str, stdin_data: dict[str, Any] | None = None, extra_args: list[str] | None = None) -> dict[str, Any]:
    responses = {
        "project-list": {"ok": True, "projects": [{"id": "gym-pid", "name": "waft", "trajectory_path": "/tmp/waft"}]},
        "project-create": {"ok": True, "project_id": "gym-pid"},
        "session-create": {"ok": True, "session_id": "gym-sid"},
        "preflight-submit": {"ok": True, "transaction_id": "gym-tid"},
        "check-submit": {"ok": True, "decision": "proceed", "checkpoint_id": "gym-cpid"},
        "postflight-submit": {"ok": True},
    }
    return responses.get(command, {"ok": False, "error": f"unknown command {command}"})


def run_simulated_scenario(project_path: Path, scenario: str) -> dict[str, Any]:
    handler = EmpericaHandler(project_path=project_path, instance_id="waft-jungle-gym", ai_id="waft-jungle-gym")

    if scenario == "mcp":
        handler._mcp_available = lambda: True
        handler._cli_json = _mock_cli_json  # type: ignore[method-assign]
    elif scenario == "cli":
        handler._mcp_available = lambda: False
        handler._cli_json = _mock_cli_json  # type: ignore[method-assign]
    elif scenario == "degraded":
        handler._mcp_available = lambda: False
        handler._cli_json = lambda command, stdin_data=None, extra_args=None: {  # type: ignore[method-assign]
            "ok": False,
            "error": "backend unavailable",
        }
    else:
        return {"scenario": scenario, "ok": False, "error": "unknown scenario"}

    if scenario == "degraded":
        import waft.core.empirica_handler as handler_module

        original_which = handler_module.shutil.which
        handler_module.shutil.which = lambda _: None  # type: ignore[assignment]
        try:
            boot = handler.boot()
        finally:
            handler_module.shutil.which = original_which  # type: ignore[assignment]
    else:
        boot = handler.boot()

    result: dict[str, Any] = {
        "scenario": scenario,
        "boot_ok": bool(boot.ok),
        "transport": handler.transport,
        "fallback_reason": handler.backend_status().get("fallback_reason"),
    }

    if not boot.ok:
        result["ok"] = scenario == "degraded"
        result["message"] = boot.message
        return result

    pre = handler.preflight(reasoning=f"jungle-gym preflight ({scenario})")
    check = handler.check(reasoning=f"jungle-gym check ({scenario})")
    post = handler.postflight(reasoning=f"jungle-gym postflight ({scenario})")

    result.update(
        {
            "ok": bool(pre.get("ok")) and check.proceed and bool(post.get("ok")),
            "session_id": handler.session_id,
            "preflight_ok": bool(pre.get("ok")),
            "check_decision": check.decision.value,
            "postflight_ok": bool(post.get("ok")),
        }
    )
    return result


def run_live(project_path: Path) -> dict[str, Any]:
    handler = EmpericaHandler(project_path=project_path, instance_id="waft-jungle-gym-live", ai_id="waft-jungle-gym-live")
    boot = handler.boot()
    result: dict[str, Any] = {
        "scenario": "live",
        "boot_ok": bool(boot.ok),
        "transport": handler.transport,
        "fallback_reason": handler.backend_status().get("fallback_reason"),
        "message": boot.message,
    }
    if not boot.ok:
        result["ok"] = False
        return result

    pre = handler.preflight(reasoning="jungle-gym live preflight")
    check = handler.check(reasoning="jungle-gym live check")
    post = handler.postflight(reasoning="jungle-gym live postflight")
    result.update(
        {
            "ok": bool(pre.get("ok")) and bool(post.get("ok")),
            "session_id": handler.session_id,
            "preflight_ok": bool(pre.get("ok")),
            "check_decision": check.decision.value,
            "postflight_ok": bool(post.get("ok")),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Empirica transport jungle gym scenarios.")
    parser.add_argument("--path", "-p", default=".", help="Project path (default: current directory)")
    parser.add_argument(
        "--mode",
        choices=["simulated", "live"],
        default="simulated",
        help="Run simulated transport matrix or live environment cycle.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON only.",
    )
    args = parser.parse_args()

    project_path = Path(args.path).resolve()

    if args.mode == "live":
        results = [run_live(project_path)]
    else:
        results = [
            run_simulated_scenario(project_path, "mcp"),
            run_simulated_scenario(project_path, "cli"),
            run_simulated_scenario(project_path, "degraded"),
        ]

    passed = sum(1 for r in results if r.get("ok"))
    total = len(results)
    summary = {"passed": passed, "total": total, "all_passed": passed == total, "results": results}

    if args.json:
        print(json.dumps(summary, indent=2))
        raise SystemExit(0 if summary["all_passed"] else 1)

    print("\nEmpirica Jungle Gym\n")
    for r in results:
        status = "PASS" if r.get("ok") else "FAIL"
        print(
            f"- [{status}] scenario={r.get('scenario')} transport={r.get('transport')} "
            f"boot_ok={r.get('boot_ok')} check={r.get('check_decision', 'n/a')}"
        )
        if r.get("fallback_reason"):
            print(f"  fallback_reason: {r['fallback_reason']}")
        if r.get("message"):
            print(f"  message: {r['message']}")

    print(f"\nSummary: {passed}/{total} passing\n")
    raise SystemExit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()

