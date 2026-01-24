"""
PocketBase Binary Downloader: Downloads PocketBase for the user's OS.

PocketBase is a single binary that includes SQLite + Realtime API + Admin UI.
"""
import logging
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import urlretrieve

logger = logging.getLogger(__name__)

# PocketBase download URLs
POCKETBASE_VERSION = "0.22.30"  # Latest stable version
BASE_URL = f"https://github.com/pocketbase/pocketbase/releases/download/v{POCKETBASE_VERSION}"

# OS-specific binary names
BINARY_NAMES = {
    "Darwin": "pocketbase_darwin_amd64.zip",  # macOS Intel
    "Darwin_arm64": "pocketbase_darwin_arm64.zip",  # macOS Apple Silicon
    "Linux": "pocketbase_linux_amd64.zip",
    "Linux_arm64": "pocketbase_linux_arm64.zip",
}


def detect_os() -> str:
    """
    Detect the operating system and architecture.

    Returns:
        OS identifier string
    """
    system = platform.system()
    machine = platform.machine()

    if system == "Darwin":
        if machine == "arm64":
            return "Darwin_arm64"
        return "Darwin"
    elif system == "Linux":
        if machine == "aarch64" or machine == "arm64":
            return "Linux_arm64"
        return "Linux"
    else:
        raise RuntimeError(f"Unsupported OS: {system} {machine}")


def download_pocketbase(project_path: Path) -> Path:
    """
    Download PocketBase binary for the current OS.

    Args:
        project_path: Path to project root

    Returns:
        Path to PocketBase binary
    """
    bin_dir = project_path / "src" / "waft" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    binary_path = bin_dir / "pocketbase"
    if binary_path.exists():
        logger.info(f"PocketBase binary already exists at {binary_path}")
        # Verify it's executable
        if not binary_path.stat().st_mode & 0o111:
            binary_path.chmod(0o755)
        return binary_path

    # Detect OS
    os_id = detect_os()
    binary_name = BINARY_NAMES.get(os_id)
    if not binary_name:
        raise RuntimeError(f"Unsupported OS: {os_id}")

    # Download URL
    download_url = f"{BASE_URL}/{binary_name}"
    zip_path = bin_dir / binary_name

    logger.info(f"Downloading PocketBase for {os_id}...")
    logger.info(f"URL: {download_url}")

    try:
        # Download zip
        urlretrieve(download_url, zip_path)
        logger.info(f"Downloaded to {zip_path}")

        # Extract (PocketBase zips contain a single binary)
        # Use Python's zipfile or unzip command
        if shutil.which("unzip"):
            subprocess.run(["unzip", "-o", str(zip_path), "-d", str(bin_dir)], check=True)
        else:
            import zipfile

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(bin_dir)

        # Clean up zip
        zip_path.unlink()

        # Make executable
        binary_path.chmod(0o755)

        logger.info(f"PocketBase binary ready at {binary_path}")
        return binary_path

    except Exception as e:
        logger.error(f"Failed to download PocketBase: {e}")
        if zip_path.exists():
            zip_path.unlink()
        raise


def verify_pocketbase(binary_path: Path) -> bool:
    """
    Verify PocketBase binary works.

    Args:
        binary_path: Path to PocketBase binary

    Returns:
        True if binary is valid
    """
    try:
        result = subprocess.run(
            [str(binary_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            logger.info(f"PocketBase version: {result.stdout.strip()}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to verify PocketBase: {e}")
        return False
