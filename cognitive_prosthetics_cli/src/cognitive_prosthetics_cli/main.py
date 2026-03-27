import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


FALLBACK_MANIFEST = {
    "repositories": [
        {
            "id": "waft",
            "name": "waft",
            "path": "~/Code/active/waft",
            "required_paths": ["README.md"],
        }
    ]
}


def _check_uv():
    uv_path = shutil.which("uv")
    return {"ok": uv_path is not None, "path": uv_path}


def _load_manifest(manifest_path):
    if manifest_path.exists():
        try:
            return {
                "ok": True,
                "source": str(manifest_path),
                "manifest": json.loads(manifest_path.read_text(encoding="utf-8")),
                "error": None,
            }
        except Exception as exc:
            return {
                "ok": False,
                "source": str(manifest_path),
                "manifest": None,
                "error": str(exc),
            }
    return {
        "ok": True,
        "source": "fallback",
        "manifest": FALLBACK_MANIFEST,
        "error": None,
    }


def _check_gpu_signal():
    cuda_visible_devices = os.getenv("CUDA_VISIBLE_DEVICES")
    nvidia_smi_path = shutil.which("nvidia-smi")
    nvidia_smi_responding = False
    if nvidia_smi_path:
        try:
            completed = subprocess.run(
                [nvidia_smi_path, "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            nvidia_smi_responding = completed.returncode == 0
        except Exception:
            nvidia_smi_responding = False
    return {
        "cuda_visible_devices": cuda_visible_devices,
        "nvidia_smi_on_path": nvidia_smi_path is not None,
        "nvidia_smi_responding": nvidia_smi_responding,
    }


def _check_repositories(repositories):
    repo_reports = []
    all_required_ok = True
    for repo in repositories:
        repo_id = repo.get("id", "")
        repo_name = repo.get("name", repo_id)
        raw_path = repo.get("path", "")
        required_paths = repo.get("required_paths", [])
        expanded = Path(raw_path).expanduser()
        repo_exists = expanded.is_dir()
        missing_required_paths = []
        if repo_exists:
            for rel in required_paths:
                if not (expanded / rel).exists():
                    missing_required_paths.append(rel)
        else:
            missing_required_paths = list(required_paths)
        repo_ok = repo_exists and len(missing_required_paths) == 0
        all_required_ok = all_required_ok and repo_ok
        repo_reports.append(
            {
                "id": repo_id,
                "name": repo_name,
                "path": str(expanded),
                "exists": repo_exists,
                "required_paths": required_paths,
                "missing_required_paths": missing_required_paths,
                "ok": repo_ok,
            }
        )
    return {"ok": all_required_ok, "repos": repo_reports}


def build_report(manifest_arg=None):
    manifest_path = Path(manifest_arg or "repositories.json")
    manifest_result = _load_manifest(manifest_path)
    python_result = {"ok": True, "executable": sys.executable, "version": sys.version.split()[0]}
    uv_result = _check_uv()
    gpu_signal = _check_gpu_signal()
    repositories = []
    repos_result = {"ok": False, "repos": []}
    if manifest_result["ok"]:
        repositories = manifest_result["manifest"].get("repositories", [])
        repos_result = _check_repositories(repositories)
    required_checks = [
        {"name": "python", "ok": python_result["ok"]},
        {"name": "uv", "ok": uv_result["ok"]},
        {"name": "manifest", "ok": manifest_result["ok"]},
        {"name": "repositories", "ok": repos_result["ok"]},
    ]
    passed_required = sum(1 for item in required_checks if item["ok"])
    total_required = len(required_checks)
    required_ok = passed_required == total_required
    return {
        "ok": required_ok,
        "summary": {
            "required_passed": passed_required,
            "required_total": total_required,
            "repo_count": len(repositories),
        },
        "required_checks": required_checks,
        "tooling": {"python": python_result, "uv": uv_result},
        "manifest": {
            "ok": manifest_result["ok"],
            "source": manifest_result["source"],
            "error": manifest_result["error"],
        },
        "repositories": repos_result["repos"],
        "signals": {"gpu": gpu_signal},
    }


def _render_human(report):
    print("cprost check")
    print(f"status: {'READY' if report['ok'] else 'NOT READY'}")
    print(
        f"required checks: {report['summary']['required_passed']}/{report['summary']['required_total']}"
    )
    print(f"manifest source: {report['manifest']['source']}")
    if report["manifest"]["error"]:
        print(f"manifest error: {report['manifest']['error']}")
    print("")
    print("required checks:")
    for check in report["required_checks"]:
        mark = "PASS" if check["ok"] else "FAIL"
        print(f"- {check['name']}: {mark}")
    print("")
    print("repositories:")
    if not report["repositories"]:
        print("- none")
    for repo in report["repositories"]:
        mark = "PASS" if repo["ok"] else "FAIL"
        print(f"- {repo['id'] or repo['name']}: {mark} ({repo['path']})")
        if repo["missing_required_paths"]:
            print(f"  missing: {', '.join(repo['missing_required_paths'])}")
    print("")
    gpu = report["signals"]["gpu"]
    print("gpu signals (informational):")
    print(f"- CUDA_VISIBLE_DEVICES: {gpu['cuda_visible_devices']}")
    print(f"- nvidia-smi on PATH: {gpu['nvidia_smi_on_path']}")
    print(f"- nvidia-smi responding: {gpu['nvidia_smi_responding']}")


def run_check(manifest_arg=None, json_output=False):
    report = build_report(manifest_arg=manifest_arg)
    if json_output:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _render_human(report)
    return 0 if report["ok"] else 1


def _build_parser():
    parser = argparse.ArgumentParser(prog="cprost")
    subparsers = parser.add_subparsers(dest="command")
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--json", action="store_true", dest="json_output")
    check_parser.add_argument("--manifest", type=str, default=None)
    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return run_check(manifest_arg=args.manifest, json_output=args.json_output)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
