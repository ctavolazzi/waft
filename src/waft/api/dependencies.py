"""
Shared FastAPI dependencies for API routes.
"""

from pathlib import Path

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..api.auth import verify_token

security_scheme = HTTPBearer(auto_error=False)


def get_project_path(request: Request) -> Path:
    """Get project path from app state."""
    return request.app.state.project_path


async def require_auth(
    request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme)
) -> str:
    """
    Dependency to require authentication for write operations.

    CRITICAL: Validates token and logs security events.
    """
    if not credentials:
        # Log security event: missing token
        logger = __import__("logging").getLogger(__name__)
        logger.warning(f"Authentication failed: Missing token for {request.url.path}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    project_path = get_project_path(request)

    if not verify_token(credentials, project_path):
        # Log security event: invalid token
        logger = __import__("logging").getLogger(__name__)
        logger.warning(f"Authentication failed: Invalid token for {request.url.path}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials
