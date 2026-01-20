"""
Simple local authentication for WAFT API.

Uses a shared secret token for local development.
In production, this should be replaced with proper OAuth/JWT.
"""

import secrets
from pathlib import Path

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Security scheme
security = HTTPBearer()

# Token storage path (in project root)
TOKEN_FILE = Path(".waft_api_token")


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

    expected_token = token_file.read_text().strip()
    return credentials.credentials == expected_token


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
