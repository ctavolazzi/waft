#!/usr/bin/env python3
"""Lerna Hydra Launcher — one command to start everything.

Usage:
    python launch.py                      # Full stack: PocketBase + llama-server + dashboard
    python launch.py --no-llama           # Skip llama-server (already running)
    python launch.py --no-pocketbase      # Skip PocketBase (no persistence)
    python launch.py --sandbox-dir /tmp/x # Use specific sandbox directory
    python launch.py --clone              # Use git clone instead of worktree
"""
import argparse
import os
import platform
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
import webbrowser
import zipfile
from pathlib import Path


LLAMA_SERVER_DEFAULT = str(Path.home() / "Code" / "llama.cpp" / "build" / "bin" / "llama-server")
MODEL_DEFAULT = str(Path.home() / "google_gemma-4-E4B-it-Q4_K_M.gguf")
WAFT_ROOT = Path(__file__).resolve().parent.parent.parent  # active/waft

PB_VERSION = "0.22.8"
PB_ARCH = "darwin_amd64" if platform.machine() == "x86_64" else "darwin_arm64"
PB_URL = f"https://github.com/pocketbase/pocketbase/releases/download/v{PB_VERSION}/pocketbase_{PB_VERSION}_{PB_ARCH}.zip"

COPILOTKIT_REPO = "https://github.com/CopilotKit/CopilotKit.git"


def find_llama_server() -> str:
    """Find llama-server binary."""
    if Path(LLAMA_SERVER_DEFAULT).exists():
        return LLAMA_SERVER_DEFAULT
    from shutil import which
    found = which("llama-server")
    if found:
        return found
    return LLAMA_SERVER_DEFAULT


def ensure_pocketbase(data_dir: Path) -> Path:
    """Download PocketBase if needed, return path to binary."""
    pb_bin = data_dir / "pocketbase"
    if pb_bin.exists():
        return pb_bin

    print(f"📦 Downloading PocketBase v{PB_VERSION}...")
    zip_path = data_dir / "pb.zip"
    data_dir.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(PB_URL, str(zip_path))
    with zipfile.ZipFile(str(zip_path), "r") as z:
        z.extract("pocketbase", path=str(data_dir))
    zip_path.unlink()
    pb_bin.chmod(0o755)
    print(f"   ✓ PocketBase ready at {pb_bin}")

    # Write migration for sessions + transmissions collections
    migrations_dir = data_dir / "pb_migrations"
    migrations_dir.mkdir(exist_ok=True)
    (migrations_dir / "1712250000_init.js").write_text("""\
migrate((db) => {
    const dao = new Dao(db);

    // Sessions collection
    const sessions = new Collection({
        "name": "sessions",
        "type": "base",
        "schema": [
            { "name": "sandbox_path", "type": "text" },
            { "name": "llama_url", "type": "text" },
            { "name": "model_name", "type": "text" },
            { "name": "started_at", "type": "text" },
            { "name": "status", "type": "text" },
            { "name": "step_count", "type": "number" }
        ],
        "listRule": "", "viewRule": "", "createRule": "", "updateRule": ""
    });
    dao.saveCollection(sessions);

    // Transmissions collection
    const transmissions = new Collection({
        "name": "transmissions",
        "type": "base",
        "schema": [
            { "name": "session_id", "type": "text" },
            { "name": "step", "type": "number" },
            { "name": "prompt", "type": "text" },
            { "name": "thoughts", "type": "text" },
            { "name": "response", "type": "text" },
            { "name": "actions", "type": "text" },
            { "name": "results", "type": "text" }
        ],
        "listRule": "", "viewRule": "", "createRule": "", "updateRule": ""
    });
    dao.saveCollection(transmissions);
})
""")
    return pb_bin


def create_sandbox(method: str = "worktree", target: str | None = None) -> Path:
    """Create the sandbox directory."""
    if target:
        sandbox = Path(target)
        sandbox.mkdir(parents=True, exist_ok=True)
        return sandbox

    sandbox = Path(tempfile.mkdtemp(prefix="lerna-hydra-"))

    if method == "clone":
        print(f"📦 Cloning waft into {sandbox}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", f"file://{WAFT_ROOT}", str(sandbox)],
            check=True, capture_output=True,
        )
    else:
        print(f"🌳 Creating worktree at {sandbox}...")
        try:
            subprocess.run(
                ["git", "-C", str(WAFT_ROOT), "worktree", "add", str(sandbox), "HEAD"],
                check=True, capture_output=True,
            )
        except subprocess.CalledProcessError:
            print("   Worktree failed, falling back to clone...")
            subprocess.run(
                ["git", "clone", "--depth", "1", f"file://{WAFT_ROOT}", str(sandbox)],
                check=True, capture_output=True,
            )

    return sandbox


def clone_copilotkit(sandbox: Path):
    """Clone CopilotKit repo into the sandbox for the agent to explore."""
    target = sandbox / "copilotkit"
    if target.exists():
        print(f"   CopilotKit already in sandbox")
        return

    print(f"📥 Cloning CopilotKit into sandbox...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", COPILOTKIT_REPO, str(target)],
            check=True, capture_output=True, timeout=60,
        )
        print(f"   ✓ CopilotKit cloned ({sum(1 for _ in target.rglob('*'))} files)")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"   ⚠ CopilotKit clone failed: {e}")
        print(f"     Agent will start without it")


def seed_sandbox(sandbox: Path):
    """Write starter index.html if not present."""
    index = sandbox / "index.html"
    if not index.exists():
        index.write_text("""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Lerna Hydra Sandbox</title>
<style>
  body {
    background: #f5f0e6; color: #4a2c2a;
    font-family: 'Courier New', monospace;
    display: flex; align-items: center; justify-content: center;
    height: 100vh; margin: 0;
  }
  .waiting {
    text-align: center; border: 3px solid #4a2c2a;
    padding: 40px; box-shadow: 4px 4px 0 #e07b3c;
  }
  h1 { color: #e07b3c; margin: 0 0 10px; }
  p { color: #7a6b5d; }
</style>
</head>
<body>
<div class="waiting">
  <h1>🐉 LERNA HYDRA</h1>
  <p>Waiting for the agent to begin exploring...</p>
</div>
</body>
</html>
""")
        print(f"   Seeded index.html in sandbox")


def wait_for_server(url: str, name: str, retries: int = 15, delay: float = 2.0):
    """Poll a URL until it responds."""
    for i in range(retries):
        try:
            urllib.request.urlopen(url, timeout=2)
            print(f"   ✓ {name} is ready")
            return True
        except Exception:
            if i < retries - 1:
                print(f"   Waiting for {name}... ({i+1}/{retries})")
                time.sleep(delay)
    print(f"   ⚠ {name} did not respond after {retries} attempts")
    return False


def main():
    parser = argparse.ArgumentParser(description="Lerna Hydra Launcher")
    parser.add_argument("--port", type=int, default=3000, help="Nerve center port")
    parser.add_argument("--llama-port", type=int, default=8080, help="llama-server port")
    parser.add_argument("--pb-port", type=int, default=8090, help="PocketBase port")
    parser.add_argument("--sandbox-dir", type=str, help="Use existing sandbox directory")
    parser.add_argument("--clone", action="store_true", help="Use git clone instead of worktree")
    parser.add_argument("--no-llama", action="store_true", help="Skip starting llama-server")
    parser.add_argument("--no-pocketbase", action="store_true", help="Skip PocketBase")
    parser.add_argument("--no-copilotkit", action="store_true", help="Skip cloning CopilotKit")
    parser.add_argument("--model-path", type=str, default=MODEL_DEFAULT, help="GGUF model path")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")
    args = parser.parse_args()

    procs = []  # Track child processes for cleanup
    sandbox = None
    data_dir = Path(__file__).parent / ".data"

    def cleanup(signum=None, frame=None):
        print("\n🧹 Cleaning up...")
        for name, proc in procs:
            proc.terminate()
            print(f"   Stopped {name}")
        if sandbox and not args.sandbox_dir:
            print(f"   Sandbox at: {sandbox}")
            print(f"   (Run 'rm -rf {sandbox}' to clean up)")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print("🐉 LERNA HYDRA — Starting up...")
    print()

    # 1. Create sandbox
    method = "clone" if args.clone else "worktree"
    sandbox = create_sandbox(method, args.sandbox_dir)
    seed_sandbox(sandbox)
    print(f"   Sandbox: {sandbox}")
    print()

    # 2. Clone CopilotKit into sandbox (first task material)
    if not args.no_copilotkit:
        clone_copilotkit(sandbox)
        print()

    # 3. Start PocketBase (optional)
    pb_url = f"http://127.0.0.1:{args.pb_port}"
    if not args.no_pocketbase:
        pb_bin = ensure_pocketbase(data_dir)
        print(f"🗄️  Starting PocketBase on port {args.pb_port}...")
        pb_proc = subprocess.Popen(
            [str(pb_bin), "serve", f"--http=127.0.0.1:{args.pb_port}",
             f"--dir={data_dir / 'pb_data'}",
             f"--migrationsDir={data_dir / 'pb_migrations'}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        procs.append(("PocketBase", pb_proc))
        wait_for_server(f"{pb_url}/api/health", "PocketBase")
        print()

    # 4. Start llama-server (optional)
    if not args.no_llama:
        llama_bin = find_llama_server()
        print(f"🧠 Starting llama-server...")
        print(f"   Binary: {llama_bin}")
        print(f"   Model:  {args.model_path}")
        llama_proc = subprocess.Popen(
            [llama_bin, "-m", args.model_path, "--port", str(args.llama_port),
             "--host", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        procs.append(("llama-server", llama_proc))
        wait_for_server(f"http://127.0.0.1:{args.llama_port}/health", "llama-server")
        print()

    # 5. Start nerve center
    print(f"📡 Starting Nerve Center on port {args.port}...")
    llama_url = f"http://127.0.0.1:{args.llama_port}"

    sys.path.insert(0, str(Path(__file__).parent))
    from nerve_center import create_app
    app = create_app(sandbox_dir=sandbox, llama_url=llama_url, pb_url=pb_url)

    # Open browser
    if not args.no_browser:
        import threading
        def open_browser():
            time.sleep(2)
            webbrowser.open(f"http://localhost:{args.port}")
        threading.Thread(target=open_browser, daemon=True).start()

    print()
    print(f"   ┌─────────────────────────────────────┐")
    print(f"   │  🐉 LERNA HYDRA — All systems go     │")
    print(f"   ├─────────────────────────────────────┤")
    print(f"   │  Dashboard:  http://localhost:{args.port}    │")
    print(f"   │  PocketBase: http://localhost:{args.pb_port}  │")
    print(f"   │  llama:      http://localhost:{args.llama_port}  │")
    print(f"   │  Sandbox:    {str(sandbox)[:25]}...  │")
    print(f"   └─────────────────────────────────────┘")
    print()
    print("   Press Ctrl+C to stop all services")
    print()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
