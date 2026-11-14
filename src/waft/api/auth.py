"""
Simple local authentication for WAFT API.

Uses a shared secret token for local development.
In production, this should be replaced with proper OAuth/JWT.
"""

import hmac
import os
import secrets
from ipaddress import ip_address, ip_network
from pathlib import Path

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Security scheme
security = HTTPBearer()

# Token storage path (in project root)
TOKEN_FILE = Path(".waft_api_token")


def is_local_client(host: str | None) -> bool:
    """
    True when a request comes from this machine.

    The API hands its token to local clients and lets them write without one, which is what
    makes `waft serve` usable on a laptop. Everyone else must present the token. "testclient"
    is the host Starlette's in-process TestClient reports; a real connection always carries an
    IP address, so it cannot be spoofed over the network.

    WAFT_API_TRUSTED_CLIENTS widens this on purpose: a comma-separated list of addresses or
    networks (for example "172.16.0.0/12" when the server runs in Docker and its published
    port is bound to 127.0.0.1, so the only clients are the host machine seen through the
    Docker bridge). Leave it unset unless you know every machine in the range.
    """
    if not host:
        return False
    if host in ("localhost", "testclient"):
        return True
    try:
        address = ip_address(host)
    except ValueError:
        return False
    if address.is_loopback:
        return True
    for entry in os.environ.get("WAFT_API_TRUSTED_CLIENTS", "").split(","):
        entry = entry.strip()
        if not entry:
            continue
        try:
            if address in ip_network(entry, strict=False):
                return True
        except ValueError:
            continue  # a bad entry trusts nobody
    return False


def token_matches(presented: str, project_path: Path) -> bool:
    """Compare a presented token with the project's token in constant time."""
    token_file = project_path / TOKEN_FILE
    if not token_file.exists():
        return False
    expected = token_file.read_text().strip()
    return bool(expected) and hmac.compare_digest(presented.encode(), expected.encode())


def generate_token() -> str:
    """Generate a new API token."""
    return secrets.token_urlsafe(32)


def get_or_create_token(project_path: Path) -> str:
    """
    Get existing token or create a new one.

    Args:
        project_path: Path to WAFT project

    Returns:
        API token string
    """
    token_file = project_path / TOKEN_FILE

    if token_file.exists():
        return token_file.read_text().strip()

    # Generate new token
    token = generate_token()
    token_file.write_text(token)
    token_file.chmod(0o600)  # Read/write for owner only

    return token


def verify_token(credentials: HTTPAuthorizationCredentials, project_path: Path) -> bool:
    """
    Verify API token.

    CRITICAL: Validates token file permissions for security.

    Args:
        credentials: HTTP Bearer credentials
        project_path: Path to WAFT project

    Returns:
        True if token is valid
    """
    token_file = project_path / TOKEN_FILE

    if not token_file.exists():
        return False

    # CRITICAL: Validate token file permissions (should be 0o600)
    try:
        stat_info = token_file.stat()
        mode = stat_info.st_mode & 0o777
        # Check if file is readable by others (group or world read)
        if mode & 0o044:  # If group or world has read permission
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Token file has insecure permissions: {oct(mode)} (expected 0o600)")
            # Don't fail, but log the security issue
    except OSError:
        pass  # Can't check permissions, continue anyway

    return token_matches(credentials.credentials, project_path)


async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    project_path: Path | None = None,
) -> str:
    """
    Dependency to verify and return current token.

    Raises HTTPException if token is invalid.
    """
    if project_path is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Project path not configured"
        )

    if not verify_token(credentials, project_path):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials
